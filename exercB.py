import network
import time
import ujson
from machine import Pin
from umqtt.simple import MQTTClient

# --- CONFIGURAÇÃO ---
TOKEN = "FhpTcpxIqdAZgF1MvqA3"  # Substitui pelo teu Access Token
HOST = "mqtt.thingsboard.cloud"

# Pino do LED
led = Pin(14, Pin.OUT)

# --- FUNÇÃO QUE LIGA O LED ---
def processar_comando(topic, msg):
    # Quando carregas no botão, o ThingsBoard envia uma mensagem JSON
    dados = ujson.loads(msg)
    
    # Se o método for 'setLedStatus', mudamos o LED
    if dados['method'] == 'setLedStatus':
        valor_do_botao = dados['params'] # Recebe True ou False
        if valor_do_botao == True:
            led.value(1)  # Liga o LED
            print("Botão do Dashboard: LIGADO")
        else:
            led.value(0)  # Desliga o LED
            print("Botão do Dashboard: DESLIGADO")

# --- CONEXÃO ---
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected(): pass

client = MQTTClient("esp32_botao", HOST, user=TOKEN, password="")
client.set_callback(processar_comando)
client.connect()

# SUBSCREVER (Diz ao ESP32 para ouvir os comandos)
client.subscribe(b"v1/devices/me/rpc/request/+")
print("Sistema pronto! Carrega no botão do Dashboard.")

while True:
    # Verifica se o botão foi pressionado no site
    client.check_msg()
    time.sleep(0.2)