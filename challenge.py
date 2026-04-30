##
import network, time, dht, ujson 

from machine import Pin 

from umqtt.simple import MQTTClient 
  

HOST  = "mqtt.thingsboard.cloud" 

PORT  = 1883 

TOKEN = "YOUR_ACCESS_TOKEN_HERE" 

TOPIC = b"v1/devices/me/telemetry"   

sensor = dht.DHT22(Pin(15)) 	#if you choose another GPIO pin, change his number here

fan = Pin(2, Pin.OUT)           #choose a GPIO pin for the LED'S and change the number
fan.off()
temp_high = 30.0
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

    payload = ujson.dumps({ 

        "temperature": sensor.temperature(), 

        "humidity":    sensor.humidity() 

    }) 

    if sensor.temperature() > temp_high:
        fan.on()
    else:
        fan.off()


    client.publish(TOPIC, payload) 

    print("Sent:", payload) 

    time.sleep(3) 
