# 🏥 Smart Patient Health Monitor
An IoT-enabled health monitoring system that streams simulated patient vitals over a wireless network, detects anomalies in real-time, and visualizes the data on a live clinical dashboard.
##  Features & Syllabus Alignment
* **Wireless Communication:** Uses the MQTT protocol (HiveMQ Cloud Broker) to simulate a wearable IoT device transmitting data over a network.
* **AI/Anomaly Detection:** Real-time logic engine flags tachycardia (HR > 100) and hypoxia (SpO2 < 95).
* **DBMS Integration:** All vitals and generated alerts are permanently logged using SQLite.
* **Live UI:** A responsive, Google Material-inspired dashboard featuring a flashing "Snitch" alert system and live-scrolling Chart.js graphs.
##  Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite
* **IoT/Network:** `paho-mqtt`
* **Frontend:** HTML/CSS, Vanilla JS, Chart.js
##  How to Run Locally
1. Install dependencies:
   `pip install -r requirements.txt`
2. Start the central dashboard server:
   `python app.py`
3. In a separate terminal, start the simulated wearable device:
   `python sensor_sim.py`
4. Open your browser and navigate to `http://localhost:5000`