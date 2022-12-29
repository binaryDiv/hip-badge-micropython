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

You need to have Python 3, pip and [virtualenv](https://docs.python.org/3/library/venv.html) installed on your system. If your system does not already come with that, please install them [using your system's package manager](https://packaging.python.org/en/latest/guides/installing-using-linux-tools/) (for example with `apt install python3-venv python3-pip` on Debian/Ubuntu).

You also need `make` and `wget` installed, with are pretty much standard tools in Linux, so you should already have those.

Everything else that you need (mainly `esptool.py` and `rshell`) will be automatically installed inside the Python venv in the next steps.

## Quick start

### Prepare your environment

If you haven't done this already, clone this git repository somewhere in your home directory, and `cd` into it:

```shell
$ git clone https://github.com/binaryDiv/hip-badge-micropython.git
$ cd hip-badge-micropython
```

Now, use the following `make` command to create the virtual environment with all the dependencies you need:

```shell
$ make install-venv
```

The venv will automatically be used for all other `make` commands, so you don't need to activate it manually.

### Flash the firmware

To flash the MicroPython firmware to your board, the firmware first needs to be downloaded from the official MicroPython website. Then, `esptool.py` is used to first erase the current firmware, and then to flash the new firmware.

Luckily, there is a `make` command which does all of this automatically for you. Connect your badge using a USB-C cable, turn the device on, and enter the following command:

```shell
$ make flash-firmware
```

(If you're further interested: The correct firmware for the badge is found on [this page](https://micropython.org/download/esp32c3-usb/), which also describes the `esptool.py` commands that are needed to flash the firmware.)

#### Notes for MacOS

Basically, this step should work fine under MacOS, but you need to adjust the TTY device path, since MacOS has a different naming scheme (for Linux this is typically `/dev/ttyACM0`).

First, find out the correct TTY path. Search for a file with a name like `/dev/tty.usbmodem*` or `/dev/tty.usbserial*`, for example `/dev/tty.usbmodem14201`. If you're unsure, unplug the board and check which file disappeared.

Then create a file called `Makefile.local` with the following content, replacing the path with the one you just found out:

```makefile
TTY_PATH := /dev/tty.usbmodem14201
```

Now, you should be able to run the `make flash-firmware` command.

### Deploy the MicroPython code

Your badge is now running on MicroPython. But there is no actual code on it yet, so it doesn't really do anything right now. (The LEDs might still be on, because they keep their state if nothing else is controlling them.)

To deploy the actual MicroPython code to it (which can be found in the `src` directory), you need to run another `make` command:

```shell
$ make deploy
```

Now, press the reset button on the badge (which is the small blue button in the corner, labeled as "SW3") to run the code.

And you're done! \o/

### Updating the code

The code in this repository is still in development. When there is an update, simply run `git pull` to update the files, run `make deploy` again to deploy the new code to your badge and reset the device.

## Hack your badge!

This is where the fun part begins: How to hack the existing code and experiment with your badge.

The code that is now running on your badge can be found in the `src` directory. The most important file is `main.py`, which is the file that is automatically executed when starting the board and which contains the main program.

Of course, you can directly edit `src/main.py` and deploy the modified code. However, this will cause conflicts when there are updates in this repository that you want to pull.

Instead, it is recommended to write your own code in the `src_custom` directory. You can start by copying the code of `src/main.py` to `src_custom/main.py` and modify it as you like.

To deploy your custom code, use the command `make deploy-custom` and press reset. Alternatively, you can run `make run-custom`, which will copy your code to the board like the other command, but then automatically reset the board.

With the `make run-custom` command, you can also see the output of the device, so you can use `print()` statements in your code to debug it (and see error messages if anything goes wrong). You can exit this again by pressing `Ctrl-C`.

Feel free to play around with the code!

(To be continued!)
