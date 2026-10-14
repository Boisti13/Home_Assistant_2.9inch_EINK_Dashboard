# Working on Home_Assistant_2.9inch_EINK_Dashboard

The 2.9" e-paper dashboard (device `dash-xs-esps3`, ESP32-S3).

- `git pull` first — the owner works from more than one PC.
- Work on **`dev`**, push to `dev`. `main` is only for releases, and only when
  the owner asks ("merge to main and make a new release"): merge `dev` into
  `main`, tag `vX.Y.Z`, GitHub release with the CHANGELOG section as notes.
- Every user-visible change: an entry under *Unreleased* in `CHANGELOG.md`
  (Added / Changed / Fixed / Removed / Under the hood) and the README updated
  to match.
- **What runs is the copy in Home Assistant**:
  `/homeassistant/esphome/dash-xs-esps3.yaml` (+ `fonts/`, shared with other
  devices) and `/config/packages/dash_xs.yaml`. Keep repo and HA identical:
  edit, copy to HA (back up first: ESPHome files as
  `<file>.bak-<timestamp>` next to them, packages into `/config/backup_yaml/`),
  commit. The one intended difference: the low-battery automation's notify
  actions — the live package notifies the owner's phone and Telegram, the repo
  uses `notify.notify`.
- After changing the package: `ha core check`, then reload templates /
  automations (or *reload all YAML*), not a restart.
- **ESPHome checks run on the build server** (CT 117 `esphome-builder` on
  pve_rptu_dev), never locally as long as pve_rptu_dev is reachable (owner,
  2026-10-14): `bash ../claude-setup/scripts/esphome-check.sh esphome/dash-xs-esps3.yaml`
  (add `config` to skip the compile). It sends the working tree, uncommitted
  changes included, and uses `esphome/secrets.example.yaml` (dummy values);
  same ESPHome as Home Assistant's app. Only if pve_rptu_dev is unreachable,
  validate locally with a venv outside the Drive folder. The owner compiles
  and flashes through the ESPHome app in Home Assistant.
- Layout changes: update `tools/render_preview.py` to match and redraw
  `docs/preview.png` (`python tools/render_preview.py`, needs Pillow).
- OTA: the owner turns on `input_boolean.dash_xs_keep_awake` before
  flashing; uploads use the API key (no OTA password since 2026-10-12).
- Public repo: no secrets, IPs or keys in committed files. Old keys in the
  git history (2025) are no longer used by any device.
