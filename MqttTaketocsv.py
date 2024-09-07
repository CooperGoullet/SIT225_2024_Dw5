import paho.mqtt.client as mqtt
import ssl
import csv
import re
import time
import warnings

# Suppress deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# MQTT Broker details
mqtt_broker = "10a7edd7e39341c2a763df486f287484.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_username = "CooperGoullet"
mqtt_password = "Geelong2004"
mqtt_topic = "accelerometer/data"

# CSV file setup
csv_file = "accelerometer_data_Mqtt.csv"

# Write header to CSV file if it doesn't exist
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if file.tell() == 0:  # Check if the file is empty
        writer.writerow(["timestamp", "x", "y", "z"])

# Callback when client connects to broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to broker")
        client.subscribe(mqtt_topic)
        print(f"Subscribed to topic: {mqtt_topic}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a message is received
def on_message(client, userdata, message):
    data = message.payload.decode()
    print(f"Received message: {data}")

    # Parse the message
    match = re.match(r"x:\s*(-?\d+\.\d+),\s*y:\s*(-?\d+\.\d+),\s*z:\s*(-?\d+\.\d+)", data)
    if match:
        x, y, z = match.groups()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        data_list = [timestamp, float(x), float(y), float(z)]

        # Write the data to the CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_list)
        
        print(f"Data written to CSV: {data_list}")
    else:
        print("Failed to parse message")

# Setup MQTT client with TLS/SSL
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

# Enable TLS/SSL
client.tls_set_context(ssl.create_default_context())
client.tls_insecure_set(True)  # Disable certificate verification (for testing)

# Connect to the broker
print("Connecting to broker...")
client.connect(mqtt_broker, mqtt_port)

# Start the MQTT loop
client.loop_forever()
