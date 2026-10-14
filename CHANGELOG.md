# Changelog

All notable changes, newest first. Versions follow [semantic versioning](https://semver.org/); releases are tagged `vX.Y.Z` on `main`.

## Unreleased

### Under the hood
- Config checks run on the ESPHome build server (`claude-setup/scripts/esphome-check.sh`, see `CLAUDE.md`); `secrets.example.yaml` has a valid dummy API key so `esphome config` works with it.
- `CLAUDE.md`: backups of the live files go to `/config/project-backups/` (`esphome/`, `home-assistant/`), as everywhere since 2026-10-12, not next to the files or into `/config/backup_yaml/`.

## v2.0.0 — 2026-10-12

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
- **Keep awake** (`input_boolean.dash_xs_keep_awake`, off by default) for updates over Wi-Fi: while it's on the dash doesn't sleep; switching it off sends it back to sleep at once.
- **Wi-Fi signal** and **wake time** sensors (*Wake: connected after*, *Wake: total*), sent right before each sleep.
- `secrets.example.yaml`; README with install steps, page layout, entities, battery and hardware.
- A rendered preview of the page (`docs/preview.png`, drawn by `tools/render_preview.py`).

### Changed
- **ESP32-S3** instead of ESP32-C3, ESP-IDF instead of Arduino. Same GPIOs, so the PCB still fits.
- **Wakes on every full hour** instead of every 10 minutes, and goes back to sleep as soon as every value has arrived and the page is drawn — not after a fixed minute. A wake up to 10 minutes early counts for that hour (the sleep timer runs about 1 % fast).
- **No wakes from 23:00 to 6:00**: the last page is drawn at 23:00, the next at 6:00.
- The page is drawn once per wake instead of every 20 seconds.
- Time of the page in 24-hour format, small, at the top left.
- CO₂: *Good* below 1000 ppm, *Fair* up to 1200, *Bad* above (was 1120 / 2000) — adjustable with `co2_fair` / `co2_bad`; *Unknown* without data.
- **Without Home Assistant the last page stays**: when the dash can't connect within 40 s it goes back to sleep without drawing, instead of replacing a good page with dashes.
- Device name *Dash XS* (was *dash_xs_esps3*); entity IDs start with `dash_xs_` (were `dash_xs_esps3_`), e.g. `sensor.dash_xs_battery_voltage`.
- Outside values come from `sensor.virtual_outdoor_*` (24 h highs and lows from Home Assistant) instead of the Netatmo outdoor module directly.
- The battery reading is the median of several samples, because the voltage sags while Wi-Fi connects.

### Fixed
- The low-battery notification would almost never have been sent: the device reports `unknown` at the start of most wakes, so the drop below 3.5 V came from `unknown` and was ignored. It now checks every reading. Readings that jump around 3.5 V no longer send it again and again.

### Removed
- The old ESP32-C3 files (`esp-dash.yaml`, `esp-dash-sensors.yaml`, `fonts.yaml`, `backup.yaml`); they're in the git history.

### Under the hood
- API key, hotspot password and the fixed IP address come from `secrets.yaml`. The keys that used to be in the repository are no longer used by any device.
- Fonts moved to `esphome/fonts/`.
- `channel_colors` instead of the deprecated `rgb_order` for the LED.
- OTA uploads are encrypted with the API key instead of using a separate password (saves about 3.5 KB of flash and RAM).
- The page is drawn once per wake, also while Keep awake is on.
- After drawing, it waits for the panel's BUSY line instead of a fixed 4 seconds, then sleeps — a full refresh takes about 2–3 s. Every wake does a full refresh (the driver starts fresh after deep sleep), so no ghosting.

## 2025-03 — first version (ESP32-C3, not tagged)

### Added
- ESPHome config for an ESP32-C3 with a Waveshare 2.9" e-paper: outside and inside temperature and humidity, outdoor highs and lows, tomorrow's weather with icon and high/low, CO₂ with air quality, battery voltage, clock.
- Deep sleep: awake 1 minute, asleep 10 minutes, and from 0:30 until 6:00.
- PCB (schematic, Gerber, EasyEDA) and a folder for the 3D-printed case.
