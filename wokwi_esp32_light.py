import time
import network
from machine import Pin
from umqtt.simple import MQTTClient

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""
BROKER_IP = "broker.hivemq.com"
CLIENT_ID = "pravina_esp_node_01"

TOPIC_SET = b"pravina_group/light/set"
TOPIC_STATE = b"pravina_group/light/state"

relay = Pin(5, Pin.OUT)
relay.value(0)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Wi-Fi connected!")

def sub_cb(topic, msg):
    cmd = msg.decode().strip().upper()
    print("Command received:", cmd)
    if cmd == "ON":
        relay.value(1)
        client.publish(TOPIC_STATE, b"ON", retain=True)
    elif cmd == "OFF":
        relay.value(0)
        client.publish(TOPIC_STATE, b"OFF", retain=True)

connect_wifi()
client = MQTTClient(CLIENT_ID, BROKER_IP)
client.set_callback(sub_cb)
client.connect()
client.subscribe(TOPIC_SET)
client.publish(TOPIC_STATE, b"OFF", retain=True)
print("Ready and listening on", TOPIC_SET)

while True:
    client.check_msg()
    time.sleep_ms(20)
