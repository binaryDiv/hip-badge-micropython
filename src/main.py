# This file runs the actual code. It is executed automatically after boot.py.
# Usually, this file will start some sort of main loop that keeps running forever.

from machine import Pin
from neopixel import NeoPixel

# -- Define constants

# Which GPIO pin is used to control the LEDs?
LED_DATA_PIN_NUMBER = 10
# How many LEDs does the board have in total?
LED_TOTAL_COUNT = 16

# -- Setup device

# Setup the Neopixel library, which is an easy way to control the LEDs.
led_pin = Pin(LED_DATA_PIN_NUMBER, Pin.OUT)
neopixel = NeoPixel(led_pin, LED_TOTAL_COUNT)

# For now, just set some static color for the LEDs and exit. (The LEDs will stay
# on unless they are explicitly deactivated.)
color = (32, 0, 0)  # RGB values from 0 to 255 as a tuple
neopixel.fill(color)
neopixel.write()
