import time
import json
import random
import paho.mqtt.client as mqtt
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "smarthealth/bhushan/vitals" # Your unique channel
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(" Connected to HiveMQ Cloud Broker!")
    else:
        print(f" Connection failed: {rc}")
# Setup MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start() # Runs the network loop in the background
def generate_vitals(patient_id=1):
    if random.random() < 0.9:
        hr = random.randint(60, 95)
        spo2 = random.randint(95, 100)
        temp = round(random.uniform(36.5, 37.5), 1)
    else:
        print(" Simulating anomaly...")
        hr = random.randint(110, 150)
        spo2 = random.randint(85, 92)
        temp = round(random.uniform(38.0, 39.5), 1)
    return {"patient_id": patient_id, "hr": hr, "spo2": spo2, "temp": temp}
print("Starting Version 2 Sensor (Wireless MQTT Mode)...")
try:
    while True:
        vitals = generate_vitals()
        payload = json.dumps(vitals)
        
        # Broadcast the data to the cloud
        client.publish(TOPIC, payload)
        print(f" Broadcasted: {payload}")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nSimulation stopped.")
    client.loop_stop()
    client.disconnect()