# hip-badge-micropython

This repository contains instructions and various code examples for how to hack the [#HiP22](https://hip-berlin.de/) electronic badge using [MicroPython](https://micropython.org/).

## What's this, and why?

The HiP22 badge is a very cool board based on an ESP32 RISC-V chip, with RGB LEDs and a bunch of other peripherals.

However, since the official firmware is written in C, it sadly isn't that accessible to hack for people who don't already know how to do embedded programming with C.

MicroPython is a special implementation of Python intended for embedded devices, like this badge. It's very easy to learn, yet still very powerful. It also features a built-in library for controlling RGB LEDs like the ones featured on this badge, making it possible to control the LEDs with only a few lines of code.

To make it as easy as possible to install MicroPython on the badge and learn how to use it, I've created this repository. It contains installation instructions and example code that you can use as a base for your very own badge firmware.

## Prerequisites

You'll need a USB-C cable to connect the badge to your computer.

Your computer ideally should be running Linux. You can use any other system as well, however, you might need to adjust the instructions a bit and install some tools manually.

You need to have Python 3, pip and virtualenv installed on your system. If your system does not already come with that, please install them [using your system's package manager](https://packaging.python.org/en/latest/guides/installing-using-linux-tools/) (for example with `apt install python3-venv python3-pip` on Debian/Ubuntu).

You also need two other tools, `esptool.py` and `rshell`. These will be installed automatically inside the Python venv. However, you can also install them globally on your system if you like.

## Quick start

(TODO)
