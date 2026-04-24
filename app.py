from flask import Flask, jsonify, render_template
import sqlite3
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)
# DATABASE & MEMORY 
DB_FILE = "hospital.db"
latest_data = {
    "patient_id": "--", "hr": "--", "spo2": "--", "temp": "--",
    "status": "Waiting for wireless sensor...", "is_alert": False
}
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vitals_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER, hr INTEGER, spo2 INTEGER, temp REAL,
            is_alert BOOLEAN, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
init_db()
# WIRELESS MQTT RECEIVER 
BROKER = "broker.hivemq.com"
TOPIC = "smarthealth/bhushan/vitals"
def on_connect(client, userdata, flags, rc):
    print("✅ Flask Server connected to HiveMQ Cloud!")
    client.subscribe(TOPIC) # Start listening to your specific channel
def on_message(client, userdata, msg):
    global latest_data
    # This triggers every time the cloud receives data from your sensor
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    # 1. Update Memory
    latest_data.update(data)
    # 2. Check AI Rules
    is_alert = False
    if data['hr'] > 100 or data['spo2'] < 95:
        latest_data['status'] = " ANOMALY DETECTED!"
        latest_data['is_alert'] = True
        is_alert = True
        print(f" ALERT -> HR: {data['hr']} | SpO2: {data['spo2']}")
    else:
        latest_data['status'] = " Normal Vitals"
        latest_data['is_alert'] = False
        print(f"Received -> HR: {data['hr']} | SpO2: {data['spo2']}")
    # 3. Save to Database
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO vitals_log (patient_id, hr, spo2, temp, is_alert)
                              VALUES (?, ?, ?, ?, ?)''', 
                           (data['patient_id'], data['hr'], data['spo2'], data['temp'], is_alert))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Setup the background MQTT thread
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(BROKER, 1883, 60)
mqtt_client.loop_start() # Runs silently alongside Flask
# WEB ROUTES
@app.route('/')
def dashboard():
    return render_template('index.html')
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(latest_data)
if __name__ == '__main__':
    print("Starting Smart Health Backend...")
    app.run(debug=True, port=5000)