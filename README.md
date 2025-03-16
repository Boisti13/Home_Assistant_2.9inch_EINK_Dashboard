# ESPHome Configuration for E-Paper Display

![20250316_101429](https://github.com/user-attachments/assets/db89b938-55b5-4abd-bded-a953400ee35b)

## Overview
This ESPHome configuration is designed for an **ESP32-C3** microcontroller with an **E-Paper display**. It integrates with **Home Assistant** to display real-time environmental data, including temperature, humidity, CO2 levels, weather forecast, and battery voltage. Additionally, the device operates in a **deep sleep** mode to optimize power consumption.

## Features
- **E-Paper Display (Waveshare 2.9-inch)**
  - Displays indoor & outdoor temperature and humidity
  - Displays min/max temperature values for outdoor conditions
  - Shows battery voltage and CO2 levels with air quality indication
  - Weather forecast for the next day with icons and temperature range
  - Real-time clock synchronization with Home Assistant
- **Connectivity**
  - Wi-Fi integration with manual IP setup
  - Home Assistant API for data exchange
  - Over-the-air (OTA) firmware updates
- **Power Optimization**
  - Deep sleep enabled with a schedule to conserve power
  - Runs for **1 minute**, then sleeps for **10 minutes**
  - Nighttime deep sleep until 06:00 AM

## Hardware Requirements
- **ESP32-C3-DevKitM-1**
- **Waveshare 2.9-inch E-Paper display (2.90inv2-r2 model)**
- **Battery (if using portable mode, voltage monitoring included)**

## Configuration Details
### ESPHome Setup
```yaml
esphome:
  name: dash_small_esp
  friendly_name: dash_esp

esp32:
  board: esp32-c3-devkitm-1
  framework:
    type: arduino
```

### Home Assistant API & OTA
```yaml
api:
  encryption:
    key: "YOUR_ENCRYPTION_KEY"

ota:
  password: "YOUR_OTA_PASSWORD"
```

### Wi-Fi Configuration
```yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  fast_connect: true
  manual_ip:
    static_ip: 192.168.178.70
    gateway: 192.168.178.1
    subnet: 255.255.255.0
  ap:
    ssid: "Esp-Dash Fallback Hotspot"
    password: "WW5yGpGDsNge"
```

### Deep Sleep Mode
```yaml
deep_sleep:
  id: deep_sleep_1
  run_duration: 1min
  sleep_duration: 10min
```

### Time Synchronization
```yaml
time:
  - platform: homeassistant
    id: ha_time
    timezone: Europe/Berlin
    on_time:
      - seconds: 0
        minutes: 30
        hours: 0
        then:
          - deep_sleep.enter:
              id: deep_sleep_1
              until: "06:00:00"
              time_id: ha_time
```

### Display Configuration
```yaml
display:
  - platform: waveshare_epaper
    id: epaper_display
    cs_pin: GPIO6
    dc_pin: GPIO9
    busy_pin: GPIO5
    reset_pin: GPIO8
    model: 2.90inv2-r2
    rotation: 90°
    update_interval: 20s
    full_update_every: 30
    reset_duration: 100ms
    lambda: |-
      it.printf(0, 15, id(mdi_icons), "\U000F0531");
```

### Sensors
```yaml
sensor:
  - platform: homeassistant
    id: outdoor_temp
    entity_id: sensor.indoor_aussenmodul_temperature
    accuracy_decimals: 1
    unit_of_measurement: "°C"
  - platform: homeassistant
    id: outdoor_humidity
    entity_id: sensor.indoor_aussenmodul_humidity
    accuracy_decimals: 0
    unit_of_measurement: "%"
```

## Installation Guide
1. **Prepare the ESP32-C3**
   - Flash ESPHome firmware using `esphome-flasher` or ESPHome dashboard.
   - Ensure your Wi-Fi credentials are set correctly in `secrets.yaml`.

2. **Home Assistant Integration**
   - Navigate to `Settings -> Devices & Services`.
   - Click `Add Integration` and search for ESPHome.
   - Add the ESP device using the assigned IP `192.168.178.70`.

3. **OTA Updates**
   - Once the device is connected, you can push updates wirelessly using:
     ```sh
     esphome run dash_small_esp.yaml --upload-port <DEVICE_IP>
     ```

## Notes
- Ensure **ESPHome and Home Assistant** are running the latest versions.
- The ESP32 operates on **deep sleep mode** for power efficiency.
- The E-Paper display only **updates every 20 seconds** to reduce wear.
- Fonts and icons are loaded from the `fonts/` directory.

## License
This project is licensed under the MIT License. Contributions and modifications are welcome!
