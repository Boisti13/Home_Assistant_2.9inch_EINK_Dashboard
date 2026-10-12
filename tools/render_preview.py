"""Render the dashboard page as a PNG, for the README.

Follows the display lambda in esphome/dash-xs-esps3.yaml coordinate for
coordinate, with the same fonts, in 1 bit like the panel (296x128, landscape).
Keep it in step when the layout changes.

    python tools/render_preview.py [docs/preview.png]

Needs Pillow. The values below are an example; edit them to taste.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "esphome" / "fonts"

VALUES = {
    "time": "19:00",
    "outdoor_temp": 12.5,
    "outdoor_temp_max": 18.0,
    "outdoor_temp_min": 5.6,
    "outdoor_humidity": 71,
    "outdoor_humidity_max": 89.4,
    "outdoor_humidity_min": 49.0,
    "bedroom_temp": 21.3,
    "bedroom_humidity": 56,
    "forecast_condition": "cloudy",
    "forecast_temp": 16.6,
    "forecast_templow": 9.5,
    "co2": 860,
    "pressure": 1020.6,
    "pressure_trend": "stable",
    "battery_level": 83,
    "battery_voltage": 4.03,
    "data_incomplete": False,
}

# Substitutions from the yaml
LOW_BATTERY_VOLTAGE = 3.50
CO2_FAIR = 1000
CO2_BAD = 1200

ICON = {
    "arrow_up": "\U000F0143",
    "arrow_down": "\U000F0140",
    "arrow_stable": "\U000F0142",
    "temp_max": "\U000F0E03",
    "temp_min": "\U000F0E02",
    "tree": "\U000F0531",
    "house": "\U000F02DC",
    "battery_alert": "\U000F0083",
}

WEATHER = {
    "sunny": ("\U000F0599", "Sunny"),
    "clear-night": ("\U000F0594", "Clear Night"),
    "partlycloudy": ("\U000F0595", "Partly Cloudy"),
    "cloudy": ("\U000F0590", "Cloudy"),
    "fog": ("\U000F0591", "Foggy"),
    "rainy": ("\U000F0597", "Rainy"),
    "snowy": ("\U000F0598", "Snowy"),
    "snowy-rainy": ("\U000F067F", "Snow & Rain"),
    "pouring": ("\U000F0596", "Heavy Rain"),
    "lightning-rainy": ("\U000F067E", "Thunderstorm"),
    "windy": ("\U000F059D", "Windy"),
    "windy-variant": ("\U000F059E", "Windy & Cloudy"),
    "hail": ("\U000F0592", "Hail"),
    "exceptional": ("\U000F05D6", "Exceptional"),
}
WEATHER_UNKNOWN = ("\U000F0625", "Unknown")


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


font_big = font("Ubuntu-Medium.ttf", 24)
font_small = font("Ubuntu-Medium.ttf", 12)
font_xs = font("Ubuntu-Medium.ttf", 9)
min_max_icons = font("MaterialDesignIconsDesktop.ttf", 14)
mdi_icons = font("MaterialDesignIconsDesktop.ttf", 38)
weather_icons = font("MaterialDesignIconsDesktop.ttf", 40)

# ESPHome's TextAlign → Pillow anchors (y is the top of the font's ascent)
ANCHOR = {"TOP_LEFT": "la", "RIGHT": "ra", "TOP_RIGHT": "ra", "TOP_CENTER": "ma"}


def render(v):
    img = Image.new("1", (296, 128), 1)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"

    def p(x, y, f, text, align="TOP_LEFT"):
        d.text((x, y), text, font=f, fill=0, anchor=ANCHOR[align])

    main_x = 115
    icon_x = main_x + 20
    value_x = main_x + 55

    # Outdoor temperature, 24 h high/low
    p(0, 15, mdi_icons, ICON["tree"])
    p(main_x, 5, font_big, f"{v['outdoor_temp']:.1f}°C", "RIGHT")
    p(icon_x, 5, min_max_icons, ICON["arrow_up"], "RIGHT")
    p(icon_x, 17, min_max_icons, ICON["arrow_down"], "RIGHT")
    p(value_x, 5, font_small, f"{v['outdoor_temp_max']:.1f}°C", "RIGHT")
    p(value_x, 17, font_small, f"{v['outdoor_temp_min']:.1f}°C", "RIGHT")

    # Outdoor humidity, 24 h high/low
    main_2_y, min_max_2_y = 34, 46
    p(main_x, main_2_y, font_big, f"{v['outdoor_humidity']:.0f}%", "RIGHT")
    p(icon_x, main_2_y, min_max_icons, ICON["arrow_up"], "RIGHT")
    p(icon_x, min_max_2_y, min_max_icons, ICON["arrow_down"], "RIGHT")
    p(value_x, main_2_y, font_small, f"{v['outdoor_humidity_max']:.0f}%", "RIGHT")
    p(value_x, min_max_2_y, font_small, f"{v['outdoor_humidity_min']:.0f}%", "RIGHT")

    # Inside
    logo_2_y = 85
    p(0, logo_2_y, mdi_icons, ICON["house"])
    p(main_x, logo_2_y - 15, font_big, f"{v['bedroom_temp']:.1f}°C", "RIGHT")
    p(main_x, logo_2_y + 14, font_big, f"{v['bedroom_humidity']:.0f}%", "RIGHT")

    # Time of this page
    p(0, 0, font_xs, v["time"])

    # Tomorrow
    cx = 239
    icon, text = WEATHER.get(v["forecast_condition"], WEATHER_UNKNOWN)
    p(cx, 5, font_small, "Tomorrow", "TOP_CENTER")
    p(cx, 20, weather_icons, icon, "TOP_CENTER")
    p(cx, 60, font_small, text, "TOP_CENTER")
    p(190, 80, min_max_icons, ICON["temp_max"])
    p(190 + 12, 80, font_small, f" {v['forecast_temp']:.1f}°C")
    p(245, 80, min_max_icons, ICON["temp_min"])
    p(245 + 12, 80, font_small, f" {v['forecast_templow']:.1f}°C")

    # Battery
    p(0, 118, font_xs, f"{v['battery_level']:.0f}%")
    if v["battery_voltage"] < LOW_BATTERY_VOLTAGE:
        p(28, 114, min_max_icons, ICON["battery_alert"])

    if v["data_incomplete"]:
        p(295, 110, font_small, "!", "TOP_RIGHT")

    # CO2 and air pressure
    co2 = v["co2"]
    quality = "Good" if co2 < CO2_FAIR else "Fair" if co2 <= CO2_BAD else "Bad"
    p(icon_x - 10, 110, font_small, f"CO2: {co2:.0f} ppm [{quality}]")
    p(icon_x - 10, 95, font_small, f"{v['pressure']:.0f} hPa")
    trend = {"up": "arrow_up", "down": "arrow_down", "stable": "arrow_stable"}.get(v["pressure_trend"])
    if trend:
        p(icon_x + 40, 95, min_max_icons, ICON[trend])

    return img


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "preview.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img = render(VALUES)
    # 3x, with a thin frame, so it reads well on GitHub
    scale = 3
    big = img.convert("L").resize((296 * scale, 128 * scale), Image.NEAREST)
    framed = Image.new("L", (big.width + 2 * scale, big.height + 2 * scale), 120)
    framed.paste(big, (scale, scale))
    framed.save(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
