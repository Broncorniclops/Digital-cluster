#!/usr/bin/env python3

import time
from ambient_light_sensor import AmbientLightSensor
import os

# Constants for brightness
MAX_BRIGHTNESS = 255
MIN_BRIGHTNESS = 30
DARK_LUX_THRESHOLD = 30
BRIGHT_LUX_THRESHOLD = 200

def map_lux_to_brightness(lux):
    if lux < DARK_LUX_THRESHOLD:
        return MIN_BRIGHTNESS
    elif lux > BRIGHT_LUX_THRESHOLD:
        return MAX_BRIGHTNESS
    else:
        scale = (lux - DARK_LUX_THRESHOLD) / (BRIGHT_LUX_THRESHOLD - DARK_LUX_THRESHOLD)
        return int(MIN_BRIGHTNESS + scale * (MAX_BRIGHTNESS - MIN_BRIGHTNESS))

def set_brightness(value):
    try:
        with open("/sys/class/backlight/rpi_backlight/brightness", "w") as f:
            f.write(str(value))
    except Exception as e:
        print(f"Failed to set brightness: {e}")

def main():
    sensor = AmbientLightSensor()
    while True:
        lux = sensor.read_lux()
        brightness = map_lux_to_brightness(lux)
        set_brightness(brightness)
        time.sleep(5)

if __name__ == "__main__":
    main()
