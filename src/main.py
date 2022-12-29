# This file runs the actual code. It is executed automatically after boot.py.
# Usually, this file will start some sort of main loop that keeps running forever.

from machine import Pin
from neopixel import NeoPixel
import time

# -- Define constants

# Which GPIO pin is used to control the LEDs?
LED_DATA_PIN_NUMBER = 10
# How many LEDs does the board have in total?
LED_TOTAL_COUNT = 16

# -- Setup device

# Setup the NeoPixel library, which is an easy way to control the LEDs.
led_pin = Pin(LED_DATA_PIN_NUMBER, Pin.OUT)
neopixel = NeoPixel(led_pin, LED_TOTAL_COUNT)

# This will create a green dot that is moving in a circle. All other pixels will be red.
# (We set the color values to 32 instead of 255, which would be "full brightness", because the LEDs are *very* bright.)
background_color = (32, 0, 0)
dot_color = (0, 32, 0)

while True:
    for i in range(LED_TOTAL_COUNT):
        # Set all pixels to the background color
        neopixel.fill(background_color)
        # Set the moving pixel to a different color
        neopixel[i] = dot_color
        # Send the data to the LEDs
        neopixel.write()
        # Sleep for 0.333 milliseconds
        time.sleep(1 / 3)
