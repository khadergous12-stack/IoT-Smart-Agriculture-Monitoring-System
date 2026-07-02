/*
  IoT-Enabled Smart Agriculture Monitoring System
  ------------------------------------------------
  Board      : ESP32 Dev Module (Wi-Fi enabled)
  Sensors    : Soil Moisture (capacitive, analog), DHT22 (temp/humidity),
               LDR (light intensity, analog), Water Level (analog float/ultrasonic)
  Actuator   : 5V relay module -> irrigation pump
  Cloud      : MQTT (broker.hivemq.com, public test broker)

  Wiring (see circuit_diagram/ for the full diagram):
    Soil Moisture AO -> GPIO 34 (ADC1_CH6)
    DHT22 Data        -> GPIO 4  (10k pull-up to 3.3V)
    LDR (divider)      -> GPIO 35 (ADC1_CH7)
    Water Level AO     -> GPIO 32 (ADC1_CH4)
    Relay IN            -> GPIO 25
    Status LED          -> GPIO 2 (onboard)

  Publishes JSON sensor data + pump status to MQTT every 5 seconds and
  applies the same threshold/hysteresis irrigation logic as
  python_simulation/irrigation_logic.py so hardware and simulation match.
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// ---------- Pin Configuration ----------
#define DHTPIN      4
#define DHTTYPE     DHT22
#define SOIL_PIN    34
#define LDR_PIN     35
#define WATER_PIN   32
#define RELAY_PIN   25
#define STATUS_LED  2

// ---------- Thresholds (match python_simulation/irrigation_logic.py) ----------
const int   SOIL_DRY_THRESHOLD   = 1500;   // below = dry -> irrigate
const int   SOIL_WET_THRESHOLD   = 2600;   // above = wet -> stop irrigating
const float TEMP_HIGH_ALERT_C    = 38.0;
const float WATER_LEVEL_LOW_PCT  = 15.0;

// ---------- Wi-Fi / MQTT Configuration ----------
const char* WIFI_SSID     = "Your_SSID";
const char* WIFI_PASSWORD = "Your_Password";
const char* MQTT_BROKER   = "broker.hivemq.com";
const int   MQTT_PORT     = 1883;
const char* MQTT_CLIENT_ID = "farmNode1";
const char* TOPIC_DATA    = "farm/node1/data";
const char* TOPIC_STATUS  = "farm/node1/status";
const char* TOPIC_ALERT   = "farm/node1/alert";

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

bool pumpOn = false;
unsigned long lastPublish = 0;
const unsigned long PUBLISH_INTERVAL_MS = 5000;

// ---------- Setup ----------
void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(STATUS_LED, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);   // most relay modules: HIGH = OFF (active-low)
  dht.begin();

  connectWiFi();
  client.setServer(MQTT_BROKER, MQTT_PORT);
}

void connectWiFi() {
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected.");
  Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT broker...");
    if (client.connect(MQTT_CLIENT_ID)) {
      Serial.println("connected.");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 2s");
      delay(2000);
    }
  }
}

// Convert raw water-level ADC (0-4095) to a 0-100% reading
float readWaterLevelPct() {
  int raw = analogRead(WATER_PIN);
  return constrain((raw / 4095.0) * 100.0, 0.0, 100.0);
}

// ---------- Main Loop ----------
void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!client.connected()) reconnectMQTT();
  client.loop();

  if (millis() - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = millis();

    float temperature = dht.readTemperature();
    float humidity    = dht.readHumidity();
    int   soil        = analogRead(SOIL_PIN);
    int   light       = analogRead(LDR_PIN);
    float waterLevel  = readWaterLevelPct();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("DHT22 read failed, skipping this cycle.");
      return;
    }

    // ---- Irrigation decision (hysteresis, mirrors Python simulation) ----
    if (waterLevel <= WATER_LEVEL_LOW_PCT) {
      pumpOn = false;                       // never run pump dry
      client.publish(TOPIC_ALERT, "LOW_WATER_LEVEL");
    } else if (soil < SOIL_DRY_THRESHOLD) {
      pumpOn = true;
    } else if (soil > SOIL_WET_THRESHOLD) {
      pumpOn = false;
    }

    digitalWrite(RELAY_PIN, pumpOn ? LOW : HIGH);   // active-low relay
    digitalWrite(STATUS_LED, pumpOn ? HIGH : LOW);

    // ---- Alerts ----
    if (soil < SOIL_DRY_THRESHOLD) {
      client.publish(TOPIC_ALERT, "LOW_SOIL_MOISTURE");
    }
    if (temperature >= TEMP_HIGH_ALERT_C) {
      client.publish(TOPIC_ALERT, "HIGH_TEMPERATURE");
    }

    // ---- Publish sensor JSON ----
    char payload[220];
    snprintf(payload, sizeof(payload),
      "{\"temp\":%.1f,\"hum\":%.1f,\"soil\":%d,\"light\":%d,\"water\":%.1f}",
      temperature, humidity, soil, light, waterLevel);
    client.publish(TOPIC_DATA, payload);
    client.publish(TOPIC_STATUS, pumpOn ? "PumpON" : "PumpOFF");

    // ---- Serial monitor output ----
    Serial.print("Temp: "); Serial.print(temperature);
    Serial.print(" C | Hum: "); Serial.print(humidity);
    Serial.print(" % | Soil: "); Serial.print(soil);
    Serial.print(" | Light: "); Serial.print(light);
    Serial.print(" | Water: "); Serial.print(waterLevel);
    Serial.print(" % | Pump: "); Serial.println(pumpOn ? "ON" : "OFF");
  }
}
