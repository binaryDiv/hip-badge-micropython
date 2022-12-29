# Configuration
TTY_PATH ?= /dev/ttyACM0
RSHELL_OPTS := --quiet

# MicroPython firmware
MPY_FIRMWARE_FILENAME := esp32c3-usb-20220618-v1.19.1.bin
MPY_FIRMWARE_URL := https://micropython.org/resources/firmware/$(MPY_FIRMWARE_FILENAME)

# Helper variables
ACTIVATE_VENV := source venv/bin/activate

# Default target (deploys code)
all: deploy

# -- Dev environment

# Create venv and install dependencies
.PHONY: install-venv
install-venv:
	python3 -m venv venv
	$(ACTIVATE_VENV) && pip install -r requirements.txt

# -- Deployment

# Copy all .py files from src/ to the board
.PHONY: deploy
deploy:
	$(ACTIVATE_VENV) && rshell $(RSHELL_OPTS) -p $(TTY_PATH) cp "src/*.py" /pyboard

# Restart (reset) the board
.PHONY: restart
restart:
	$(ACTIVATE_VENV) && rshell $(RSHELL_OPTS) -p $(TTY_PATH) repl "~ import machine ~ machine.soft_reset() ~"

# Copy files from src/ to the board and then restart the board
.PHONY: deploy-restart
deploy-restart: deploy restart

# -- Firmware flashing

# Download the MicroPython firmware to the downloads directory (if it does not exist yet)
.PHONY: download-firmware
download-firmware: downloads/$(MPY_FIRMWARE_FILENAME)

# Actually downloads the firmware
downloads/$(MPY_FIRMWARE_FILENAME):
	@mkdir -p downloads/
	@if ! which wget >/dev/null 2>&1; then \
		echo "ERROR: wget is not installed! Please install wget first."; \
		echo; \
		echo "Alternatively, download the MicroPython firmware manually from the following URL into the \"downloads\" directory," \
			"and then rerun this command:"; \
		echo "$(MPY_FIRMWARE_URL)"; \
		echo; \
		exit 1; \
	fi
	wget -O "downloads/$(MPY_FIRMWARE_FILENAME)" "$(MPY_FIRMWARE_URL)"

# Flash the firmware to the ESP32 (automatically downloads the firmware first)
.PHONY: flash-firmware
flash-firmware: download-firmware
	$(ACTIVATE_VENV) && esptool.py --chip esp32c3 --port $(TTY_PATH) erase_flash
	$(ACTIVATE_VENV) && esptool.py --chip esp32c3 --port $(TTY_PATH) --baud 460800 write_flash -z 0x0 downloads/$(MPY_FIRMWARE_FILENAME)
	@echo
	@echo "MicroPython has been flashed to the board!"
