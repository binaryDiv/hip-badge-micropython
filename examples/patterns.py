# This is an example containing multiple color combinations and simple animations:
# When deployed as main.py, you can use it as follows:
# Gray button: Cycle through color combinations
# Red button: Toggle color animation (Changes direction every time you turn it off and on again)
# Black button: Cycle through brightness levels
# Gray + Red button: Cycle through animation speeds
# Black + Red button: Toggle brightness "animation" (this is annoying and should not be left on for too long)
#
# You can easily add your own color combinations by adding them as an array of tuples that contain RGB values.

from machine import Pin
from neopixel import NeoPixel
import time

# -- Define constants

# Which GPIO pin is used to control the LEDs?
LED_DATA_PIN_NUMBER = 10
# How many LEDs does the board have in total?
LED_TOTAL_COUNT = 16

# -- Setup device

# Set up the Neopixel library, which is an easy way to control the LEDs.
led_pin = Pin(LED_DATA_PIN_NUMBER, Pin.OUT)
neopixel = NeoPixel(led_pin, LED_TOTAL_COUNT)

# Define an array of colors
color_combinations = [
    # Transgender pride flag
    [
        (255, 255, 255),
        (2, 186, 247),
        (247, 2, 239),
        (2, 186, 247),
    ],
    # Pansexual pride flag
    [
        (255, 2, 2),
        (243, 247, 2),
        (2, 80, 247),
    ],
    # Gummy Worm!
    [
        (247, 2, 2),
        (247, 47, 2),
        (247, 149, 2),
        (222, 247, 2),
        (59, 247, 2),
        (2, 247, 112),
        (2, 247, 231),
        (2, 108, 247),
        (2, 10, 247),
        (75, 2, 247),
        (149, 2, 247),
        (194, 2, 247),
        (247, 2, 223),
        (247, 2, 169),
        (247, 2, 116),
        (247, 2, 59),
    ]
]

color_combination_index = 0

# Set brightness by multiplying all color values with a value between 0 and 1
brightness_levels = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

mutable_state = {
    'brightness_index': 1,
    'color_index': 0,
    'animate': False,
    'animationFrame': 0,
    'reverse': False,
    'animateBrightness': False,
    'tick': 0,
    'animationSlowdown': 1,
}


def set_colors():
    current_colors = [tuple(int(colorPart * brightness_levels[mutable_state['brightness_index']]) for colorPart in color)
                      for color in color_combinations[mutable_state['color_index']]]

    # Loop through all neopixels and set their colors
    color_index = 0
    if mutable_state['animate']:
        color_index = mutable_state['animationFrame']
        if mutable_state['reverse']:
            if mutable_state['animationFrame'] < len(current_colors) - 1:
                mutable_state['animationFrame'] += 1
            else:
                mutable_state['animationFrame'] = 0
        else:
            if mutable_state['animationFrame'] > 0:
                mutable_state['animationFrame'] -= 1
            else:
                mutable_state['animationFrame'] = len(current_colors) - 1

    for i in range(0, len(neopixel)):
        neopixel[i] = current_colors[color_index]
        if color_index < len(current_colors) - 1:
            color_index += 1
        else:
            color_index = 0
    neopixel.write()


def update_brightness(skip_zero: bool = False):
    if mutable_state['brightness_index'] < len(brightness_levels) - 1:
        mutable_state['brightness_index'] += 1
    else:
        mutable_state['brightness_index'] = 1 if skip_zero else 0


def read_pins():
    black_button_value = black_button.value()
    gray_button_value = gray_button.value()
    red_button_value = red_button.value()
    if black_button_value == 0 and red_button_value == 0:
        mutable_state['animateBrightness'] = not mutable_state['animateBrightness']
    elif red_button_value == 0 and gray_button_value == 0:
        if mutable_state['animationSlowdown'] < 3:
            mutable_state['animationSlowdown'] += 1
        else:
            mutable_state['animationSlowdown'] = 1
    elif red_button_value == 0:
        if mutable_state['animate']:
            mutable_state['animate'] = False
            mutable_state['reverse'] = not mutable_state['reverse']
        else:
            mutable_state['animate'] = True
            mutable_state['animationFrame'] = 0
    elif black_button_value == 0:
        mutable_state['animateBrightness'] = False
        update_brightness()
    elif gray_button_value == 0:
        mutable_state['animationFrame'] = 0
        if mutable_state['color_index'] < len(color_combinations) - 1:
            mutable_state['color_index'] += 1
        else:
            mutable_state['color_index'] = 0
    else:
        # We return false if no known button combination was pressed
        return False
    return True


set_colors()

gray_button = Pin(2, Pin.IN)
red_button = Pin(8, Pin.IN)
black_button = Pin(9, Pin.IN)

while True:
    if read_pins():
        set_colors()
    # Only change colors every animationSlowdown ticks
    if mutable_state['tick'] % mutable_state['animationSlowdown'] == 0:
        if mutable_state['animateBrightness']:
            update_brightness(True)
        set_colors()
    # Count up the tick counter until it reaches 9999, once it does, jump back to 1. This is done to prevent overflows after long runtimes.
    mutable_state['tick'] = mutable_state['tick'] + 1 if mutable_state['tick'] < 10000 else 1
    time.sleep(0.1)
