# Project Architecture

## Text-Based Architecture Diagram

```
 ┌───────────────────────────────┐
 │            INPUT               │
 │  Soil Moisture · Temperature   │
 │  Humidity · Light · Water Level│
 └───────────────┬─────────────────┘
                 │  analog / digital read
                 ▼
 ┌───────────────────────────────┐
 │        ESP32 (Edge Node)       │
 │  sensor reading → threshold     │
 │  comparison → irrigation logic  │
 │  → alert logic → data framing   │
 └───────────────┬─────────────────┘
                 │  Wi-Fi / MQTT
                 ▼
 ┌───────────────────────────────┐
 │     MQTT Broker (HiveMQ)       │
 │  farm/node1/data                │
 │  farm/node1/status               │
 │  farm/node1/alert                 │
 └───────────────┬─────────────────┘
                 │
                 ▼
 ┌───────────────────────────────┐
 │            OUTPUT               │
 │  Dashboard visualization        │
 │  Pump ON/OFF status             │
 │  Low moisture / high temp /     │
 │    low water alerts             │
 │  CSV sensor report               │
 └───────────────────────────────┘
```

## Hardware / Software Flow

1. Sensors take a reading (soil, temperature, humidity, light, water level)
2. ESP32 reads all channels on a fixed interval (5 seconds)
3. Firmware compares soil moisture against dry/wet thresholds (with hysteresis to avoid rapid pump cycling)
4. Firmware checks the water reservoir level before ever turning the pump on
5. If conditions warrant it, the relay is switched and the pump runs
6. Sensor values + pump state are packaged as JSON and published over MQTT
7. Alerts are published separately when thresholds are crossed
8. The dashboard (or Python simulation, if no hardware) subscribes/consumes this data and updates in real time
9. All readings are logged to CSV for historical reporting

## Sensor Data Flow

```
Sensor → ADC/Digital Read → Threshold Engine → Actuation (Relay) 
                                   │
                                   └─→ MQTT Publish → Dashboard / CSV Log
```

## Why hysteresis matters

Using a single threshold for both "turn on" and "turn off" causes the pump
to flicker rapidly right at the boundary value. This project uses two
separate thresholds — a lower "dry" threshold that triggers irrigation and
a higher "wet" threshold that stops it — so the pump runs in clean,
complete cycles instead of chattering on and off.
