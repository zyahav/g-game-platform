PATH := /opt/homebrew/bin:/usr/local/bin:$(PATH)
export PATH

GODOT_BIN ?= /Applications/Godot.app/Contents/MacOS/Godot
GH_BIN ?= /opt/homebrew/bin/gh
PROJECT_ROOT := $(CURDIR)
PROJECT_NAME ?= $(notdir $(PROJECT_ROOT))
NPX ?= npx

.PHONY: help check-env git-status gh-version gh-auth gh-create-private gh-push-main godot-version godot-import godot-smoke godot-editor verify play forge-help

help:
	@echo "Available targets:"
	@echo "  make check-env     - verify local tools used by this repo"
	@echo "  make git-status    - show local git status"
	@echo "  make gh-version    - print the GitHub CLI version"
	@echo "  make gh-auth       - show GitHub CLI auth status"
	@echo "  make gh-create-private PROJECT_NAME=name - create a private GitHub repo and add origin"
	@echo "  make gh-push-main  - push the current main branch to origin"
	@echo "  make godot-version - print the Godot binary version"
	@echo "  make godot-import  - import project assets in headless editor mode"
	@echo "  make godot-smoke   - open the project headlessly and quit after startup"
	@echo "  make verify        - run the required preflight before handing work to a human"
	@echo "  make godot-editor  - launch the Godot editor for this project"
	@echo "  make play          - run preflight, then launch the game directly"
	@echo "  make forge-help    - smoke-test Godot Forge availability via npx"

check-env:
	@echo "git: $$(git --version)"
	@echo "make: $$(make --version | sed -n '1p')"
	@echo "node: $$(node --version)"
	@echo "npm: $$(npm --version)"
	@echo "python3: $$(python3 --version)"
	@echo "godot: $$($(GODOT_BIN) --version)"
	@echo "gh: $$(command -v $(GH_BIN) || echo missing)"
	@echo "uvx: $$(command -v uvx || echo missing)"

git-status:
	@git status -sb

gh-version:
	@$(GH_BIN) --version | sed -n '1p'

gh-auth:
	@$(GH_BIN) auth status

gh-create-private:
	@$(GH_BIN) repo create "$(PROJECT_NAME)" --private --source . --remote origin --push

gh-push-main:
	@git push -u origin main

godot-version:
	@$(GODOT_BIN) --version

godot-import:
	@$(GODOT_BIN) --headless --path "$(PROJECT_ROOT)" --import --quit

godot-smoke:
	@$(GODOT_BIN) --headless --path "$(PROJECT_ROOT)" --editor --quit-after 1

verify: godot-import godot-smoke
	@echo "Verification passed: assets imported and headless startup succeeded."

godot-editor:
	@$(GODOT_BIN) --path "$(PROJECT_ROOT)"

play: verify
	@$(GODOT_BIN) --path "$(PROJECT_ROOT)"

forge-help:
	@$(NPX) -y godot-forge --help
