# Configuration
TTY_PATH ?= /dev/ttyACM0
RSHELL_OPTS := --quiet

# -- Dev environment

# Create venv and install dependencies
.PHONY: install-venv
install-venv:
	python -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

# -- Deployment

# Copy all .py files from src/ to the board
.PHONY: deploy
deploy:
	rshell $(RSHELL_OPTS) -p $(TTY_PATH) cp "src/*.py" /pyboard

# Restart (reset) the board
.PHONY: restart
restart:
	rshell $(RSHELL_OPTS) -p $(TTY_PATH) repl "~ import machine ~ machine.soft_reset() ~"

# Copy files from src/ to the board and then restart the board
.PHONY: deploy-restart
deploy-restart: deploy restart
