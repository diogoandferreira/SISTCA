import network, time, dht, ujson 

from machine import Pin 

from umqtt.simple import MQTTClient 

  

HOST  = "mqtt.thingsboard.cloud" 

PORT  = 1883 

TOKEN = "YOUR_ACCESS_TOKEN_HERE" 

TOPIC = b"v1/devices/me/telemetry" 

  

sensor = dht.DHT22(Pin(15)) 	#if you choose another GPIO pin, change his number here

led_cold = Pin(X, Pin.OUT)
led_normal = Pin(Y, Pin.OUT)
LED_hot = Pin(Z, Pin.OUT)

T_MIN = 10.0
T_NORMAL = 26.5
T_MAX = 37.0
  

# Connect to Wi-Fi 

sta = network.WLAN(network.STA_IF) 

sta.active(True) 

sta.connect("Wokwi-GUEST", "") 

while not sta.isconnected(): 

    time.sleep(0.5) 

print("WiFi OK!") 
  

# Connect via MQTT 

client = MQTTClient( 

    client_id="esp32_tb", 

    server=HOST, port=PORT, 

    user=TOKEN, password="", 

    keepalive=60 

) 

client.connect() 

print("MQTT connected!") 

  

# Main loop — publish every 10 seconds 

while True: 

    sensor.measure() 
    temp = sensor.temperature()

    if temp < T_MIN:
        led_cold.on()

    elif temp > T_MIN & temp < T_MAX:
        led_normal.on()

    else:
        LED_hot.on()

    payload = ujson.dumps({ 

        "temperature": sensor.temperature(), 

        "humidity":    sensor.humidity() 
    }) 

    client.publish(TOPIC, payload) 

    print("Sent:", payload) 

    time.sleep(3) 
