# Paths
REPO_PATH = $(shell pwd)
VENV = $(REPO_PATH)/venv

# Configuration
BOT_TOKEN = {YOUR_BOT_TOKEN}
HL_DEFAULT_VAULT = {YOUR_HYPERLIQUID_VAULT_ADDRESS}

all: deploy

bootstrap:
	@echo "Bootstraping python venv"
	python -m venv $(VENV)
	. $(VENV)/bin/activate && pip install -r requirements.txt
	@echo "Source it using: . $(VENV)/bin/activate"

clean:
	@echo "Removing folders"
	rm -rf $(VENV)

deploy:
	python hl.py $(BOT_TOKEN) $(HL_DEFAULT_VAULT)

.PHONY: all bootstrap clean deploy
.SILENT: deploy
