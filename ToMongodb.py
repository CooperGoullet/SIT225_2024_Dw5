import paho.mqtt.client as mqtt
import ssl
import pymongo
from pymongo import MongoClient
import json
import warnings
import re

# Suppress deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# MQTT Broker details
mqtt_broker = "10a7edd7e39341c2a763df486f287484.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_username = "CooperGoullet"
mqtt_password = "Geelong2004"
mqtt_topic = "accelerometer/data"

# MongoDB connection (replace with your actual connection string for MongoDB Atlas)
mongo_client = MongoClient("mongodb+srv://s222326285:Hy07boTyJknc4YF4@accelerometer1.a16ok.mongodb.net/?retryWrites=true&w=majority&appName=Accelerometer1")
db = mongo_client["accelerometer_data"]
collection = db["sensor_readings"]

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
        data_dict = {
            "x": float(x),
            "y": float(y),
            "z": float(z)
        }
        # Insert the parsed data into MongoDB
        collection.insert_one(data_dict)
        print("Data inserted into MongoDB")
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
