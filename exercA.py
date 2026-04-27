import network, time, dht, ujson
from machine import Pin
from umqtt.simple import MQTTClient

# Configurações
HOST = "mqtt.thingsboard.cloud"
PORT = 1883
TOKEN = "FhpTcpxIqdAZgF1MvqA3"
TOPIC = b"v1/devices/me/telemetry"

# Hardware
sensor = dht.DHT22(Pin(15))
led_alarme = Pin(14, Pin.OUT) # O LED que vai simular o alerta

# WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('Wokwi-GUEST', '')
while not sta.isconnected():
    time.sleep(0.5)
print("WiFi OK!")

# MQTT Setup
client = MQTTClient(
    client_id="esp32_tb_01",
    server=HOST,
    port=PORT,
    user=TOKEN,
    password="",
    keepalive=60
)

client.connect()
print("MQTT ligado ao ThingsBoard!")

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        # --- Lógica do Exercício: Alerta de Temperatura ---
        if temp > 30:
            led_alarme.value(1)  # Acende o LED no Wokwi
            status = "ALERTA"
        else:
            led_alarme.value(0)  # Apaga o LED
            status = "NORMAL"
        
        # Enviamos a temperatura, humidade e o status do alarme
        payload = ujson.dumps({
            "temperature": temp,
            "humidity": hum,
            "alarmStatus": status
        })
        
        client.publish(TOPIC, payload)
        print("Enviado:", payload)

    except Exception as e:
        print("Erro:", e)
        try:
            client.connect()
        except:
            pass
            
    time.sleep(3) # Intervalo de 3 segundos entre envios