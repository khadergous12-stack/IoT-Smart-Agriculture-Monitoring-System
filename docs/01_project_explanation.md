# Project Explanation

## What is an IoT-Enabled Smart Agriculture Monitoring System?

It is a network of sensors and a microcontroller that continuously watches
field conditions — soil moisture, temperature, humidity, and light — and
uses that data to make irrigation decisions automatically, without a person
having to walk the field and check by hand.

## What problem does it solve?

Manual field monitoring is slow, inconsistent, and easy to miss. A field
technician can't check soil moisture every hour across an entire farm.
Crops get over-watered (wasting water and money) or under-watered
(stressing the plant) simply because nobody was there to notice in time.
This system replaces that guesswork with continuous, automated sensing.

## Why smart agriculture matters

Water is a limited resource, and agriculture is one of its largest
consumers. Precision, sensor-driven irrigation is one of the most direct
ways to cut water waste while protecting yield — which is why the
approach has been adopted across commercial farming, greenhouse operation,
and agri-tech research.

## Who uses systems like this

- **Farmers** — day-to-day irrigation decisions without manual field checks
- **Greenhouse owners** — tight climate control in an enclosed space
- **Irrigation teams** — scheduling water delivery across large plots
- **Smart farming startups** — building data products on top of field sensors
- **Agriculture companies** — monitoring multiple sites remotely

## How the sensors work together

- **Soil moisture sensor** — reports how much water is in the root zone
- **DHT22** — reports air temperature and humidity
- **LDR** — reports light intensity (helps interpret evaporation rate and daylight hours)
- **Water level sensor** — reports how much water remains in the irrigation reservoir, so the pump never runs dry

## How alerts help

The system doesn't just log numbers — it compares each reading against a
threshold and raises an alert the moment something needs attention: soil
too dry, temperature too high, or reservoir too low. That turns raw sensor
data into an actionable signal a farmer can respond to immediately.

## How this demonstrates IoT concepts

This project touches the full IoT stack in miniature:
sensing → edge processing (threshold logic on the microcontroller) →
connectivity (Wi-Fi/MQTT) → cloud/dashboard visualization → automated
actuation (relay-controlled pump). It's a complete, self-contained example
of the sense–think–act loop that defines IoT systems.

## Workflow

```
sensor data → microcontroller/simulation → data processing →
threshold checking → dashboard update → alert generation → irrigation decision
```

## Simple explanation

Sensors sit in the field and check the soil, air, and light. A small
computer (ESP32) reads them every few seconds. If the soil is too dry, it
turns on the water pump by itself. If something looks wrong — too hot,
too dry, or the tank is nearly empty — it sends an alert. All of this is
visible on a live dashboard.

## Technical explanation

An ESP32 samples four analog/digital sensor channels on a fixed interval,
applies hysteresis-based threshold logic to avoid rapid pump cycling,
publishes JSON payloads over MQTT to a broker, and drives a relay-switched
irrigation pump based on the same decision logic that runs identically in
the Python simulation layer (`python_simulation/irrigation_logic.py`) —
ensuring the simulated and hardware versions of this project behave the same way.
