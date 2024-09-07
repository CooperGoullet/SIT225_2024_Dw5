#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <Arduino_LSM6DS3.h>

// Replace with your network credentials
const char* ssid = "iPhonec";
const char* password = "Password";

// MQTT Broker details
const char* mqtt_server = "10a7edd7e39341c2a763df486f287484.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_username = "CooperGoullet";
const char* mqtt_password = "Username";
const char* mqtt_topic = "accelerometer/data";  // Add your MQTT topic

WiFiSSLClient wifiClient;  // Use WiFiSSLClient for secure connections
PubSubClient client(wifiClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect with MQTT username and password
    if (client.connect("ArduinoClient", mqtt_username, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  setup_wifi();

  // Set up secure connection
  client.setServer(mqtt_server, mqtt_port);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("IMU initialized successfully");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float x, y, z;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    char msg[50];
    snprintf(msg, 50, "x: %f, y: %f, z: %f", x, y, z);
    Serial.print("Publishing message: ");
    Serial.println(msg);
    client.publish(mqtt_topic, msg);
  }

  delay(1000);  // Publish every second
}


