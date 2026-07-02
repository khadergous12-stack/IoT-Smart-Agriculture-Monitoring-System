# Tech Stack Options

## Option A — Easy
- Arduino UNO
- DHT11 (temperature/humidity)
- Basic soil moisture sensor (analog)
- LDR (light)
- Serial Monitor output only, no cloud
- Good for: first-time IoT students, no Wi-Fi needed

## Option B — Intermediate *(selected for this project)*
- ESP32 (built-in Wi-Fi)
- DHT22 (better accuracy than DHT11)
- Capacitive soil moisture sensor
- LDR
- Water level sensor
- Relay module driving a pump
- MQTT publish to a public broker (broker.hivemq.com)
- Python simulation layer for when hardware isn't available
- Standalone HTML dashboard

## Option C — Advanced
- ESP32 + LoRa for multi-node, long-range field coverage
- pH and EC sensors for fertilizer/nutrient control
- Edge Impulse TinyML model for crop health image classification
- AWS IoT Core / Azure FarmBeats cloud pipeline
- Grafana + InfluxDB for historical analytics
- Weather API integration for rain-skip irrigation logic

## Why Option B was selected

Option B is the right level for a course project used as a GitHub proof
of work: it's fully achievable without owning real hardware (Wokwi
simulation + Python simulation cover that), it produces a real working
dashboard and firmware, and it still demonstrates the complete IoT loop
— sensing, connectivity, cloud, and actuation — without the added
infrastructure cost of Option C's LoRa/cloud/ML stack.
