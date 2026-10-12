# Changelog

All notable changes, newest first. Versions follow [semantic versioning](https://semver.org/); releases are tagged `vX.Y.Z` on `main`.

## Unreleased

The ESP32-S3 version, as it has been running since October 2026.

### Added
- **Air pressure** with a rising / falling / steady arrow (`sensor.indoor_pressure_trend`).
- **Battery percentage** from a LiPo voltage curve, and a **warning icon** on the page below 3.5 V (`low_battery_voltage`).
- **Low-battery notification** in Home Assistant below 3.5 V (*Dash XS – Low battery alert* in `packages/dash_xs.yaml`): sent once, armed again after the battery has been charged above 3.9 V (`input_boolean.dash_xs_battery_alerted`).
- **Wake button** on GPIO2 for a fresh page at any time.
- **!** at the bottom right when Home Assistant didn't send every value within 40 s; the page is drawn anyway with `--` for what's missing.
- The board's RGB LED as a light in Home Assistant, and a *Restart* button.
- **Home Assistant package** `packages/dash_xs.yaml` with `sensor.forecast_next_day` (tomorrow's condition and high/low from `weather.forecast_home`).
- Every Home Assistant entity is a **substitution** at the top of the config.
- `secrets.example.yaml`; README with install steps, page layout, entities, battery and hardware.

### Changed
- **ESP32-S3** instead of ESP32-C3, ESP-IDF instead of Arduino. Same GPIOs, so the PCB still fits.
- **Wakes on every full hour** instead of every 10 minutes, and goes back to sleep as soon as every value has arrived and the page is drawn — not after a fixed minute. A wake up to 10 minutes early counts for that hour (the sleep timer runs about 1 % fast).
- **No wakes from 23:00 to 6:00**: the last page is drawn at 23:00, the next at 6:00.
- The page is drawn once per wake instead of every 20 seconds.
- Time of the page in 24-hour format, small, at the top left.
- CO₂: *Good* below 1000 ppm, *Fair* up to 1400, *Bad* above (was 1120 / 2000); *Unknown* without data.
- Outside values come from `sensor.virtual_outdoor_*` (24 h highs and lows from Home Assistant) instead of the Netatmo outdoor module directly.
- The battery reading is the median of several samples, because the voltage sags while Wi-Fi connects.

### Fixed
- The low-battery notification would almost never have been sent: the device reports `unknown` at the start of most wakes, so the drop below 3.5 V came from `unknown` and was ignored. It now checks every reading. Readings that jump around 3.5 V no longer send it again and again.

### Removed
- The old ESP32-C3 files (`esp-dash.yaml`, `esp-dash-sensors.yaml`, `fonts.yaml`, `backup.yaml`); they're in the git history.

### Under the hood
- API key, OTA password, hotspot password and the fixed IP address come from `secrets.yaml`. The keys that used to be in the repository are no longer used by any device.
- Fonts moved to `esphome/fonts/`.
- `channel_colors` instead of the deprecated `rgb_order` for the LED.

## 2025-03 — first version (ESP32-C3, not tagged)

### Added
- ESPHome config for an ESP32-C3 with a Waveshare 2.9" e-paper: outside and inside temperature and humidity, outdoor highs and lows, tomorrow's weather with icon and high/low, CO₂ with air quality, battery voltage, clock.
- Deep sleep: awake 1 minute, asleep 10 minutes, and from 0:30 until 6:00.
- PCB (schematic, Gerber, EasyEDA) and a folder for the 3D-printed case.
