import network
import time
import ujson
from machine import Pin, PWM
from umqtt.simple import MQTTClient
import dht

# --- CONFIGURAÇÃO ---
TOKEN = "FhpTcpxIqdAZgF1MvqA3"
HOST = "mqtt.thingsboard.cloud"

# --- SENSORES E ATUADORES ---
sensor = dht.DHT22(Pin(15))
motor_pwm = PWM(Pin(14), freq=5000)

# --- CONEXÃO WIFI ---
print("A ligar ao WiFi...")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')

while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.5)

print("\nWiFi Ligado! IP: ", sta_if.ifconfig()[0])

# --- CONEXÃO MQTT COM SSL ---
client = None
try:
    # ssl=True força o uso de encriptação na porta 8883 (ThingsBoard Cloud)
    client = MQTTClient("esp32_pwm", HOST, port=8883, user=TOKEN, password="", ssl=True)
    client.connect()
    print("Conectado com sucesso ao ThingsBoard Cloud com encriptação (SSL)!")
except Exception as e:
    print("Erro ao ligar ao MQTT:", e)
    print("Aguardando 5 segundos...")
    time.sleep(5)

def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# --- LOOP PRINCIPAL ---
while True:
    try:
        if client is None:
            client = MQTTClient("esp32_pwm", HOST, port=8883, user=TOKEN, password="", ssl=True)
            client.connect()
            print("Reconectado ao MQTT!")

        sensor.measure()
        temp = sensor.temperature()
        
        # Lógica de Borda
        if temp <= 20:
            velocidade_pct = 0
        elif temp >= 35:
            velocidade_pct = 100
        else:
            velocidade_pct = map_range(temp, 20, 35, 20, 100)
            
        duty_value = int((velocidade_pct / 100) * 1023)
        motor_pwm.duty(duty_value)
        
        payload = ujson.dumps({
            "temperature": temp,
            "fan_speed_pct": velocidade_pct
        })
        
        client.publish("v1/devices/me/telemetry", payload)
        print("Temp: {}°C | Velocidade da Ventoinha: {}%".format(temp, velocidade_pct))
        
    except Exception as e:
        print("Erro no ciclo principal:", e)
        time.sleep(5)
        
    time.sleep(2)