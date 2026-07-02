"""
mqtt_publisher.py
------------------
Optional MQTT publishing layer. Mirrors the topics used by the ESP32
firmware (arduino_code/smart_agriculture_esp32.ino) so this simulation can
either print locally (default, no broker required) or publish to a real
broker such as broker.hivemq.com if paho-mqtt is installed and a broker is
reachable.

Usage:
    publisher = MQTTPublisher(enabled=False)   # local console mode (default)
    publisher.publish_reading(reading)
"""

import json


TOPIC_DATA = "farm/node1/data"
TOPIC_STATUS = "farm/node1/status"


class MQTTPublisher:
    def __init__(self, enabled: bool = False, broker: str = "broker.hivemq.com", port: int = 1883):
        self.enabled = enabled
        self.client = None
        if enabled:
            try:
                import paho.mqtt.client as mqtt
                self.client = mqtt.Client(client_id="farmNode1-sim")
                self.client.connect(broker, port, keepalive=30)
            except Exception as exc:  # pragma: no cover - network optional
                print(f"[MQTT] Could not connect to broker ({exc}); falling back to console mode.")
                self.enabled = False

    def publish_reading(self, reading: dict) -> None:
        payload = json.dumps({
            "temp": reading["temperature_c"],
            "hum": reading["humidity_pct"],
            "soil": reading["soil_moisture_raw"],
            "light": reading["light_raw"],
        })
        status = reading.get("pump_status", "PumpOFF")

        if self.enabled and self.client:
            self.client.publish(TOPIC_DATA, payload)
            self.client.publish(TOPIC_STATUS, status)
        else:
            print(f"[MQTT:{TOPIC_DATA}] {payload}")
            print(f"[MQTT:{TOPIC_STATUS}] {status}")


if __name__ == "__main__":
    pub = MQTTPublisher(enabled=False)
    pub.publish_reading({
        "temperature_c": 27.4, "humidity_pct": 55.0,
        "soil_moisture_raw": 1400, "light_raw": 2200, "pump_status": "PumpON",
    })
