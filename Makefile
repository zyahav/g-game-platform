PATH := /opt/homebrew/bin:/usr/local/bin:$(PATH)
export PATH

GODOT_BIN ?= $(shell command -v godot 2>/dev/null)
ifeq ($(GODOT_BIN),)
GODOT_BIN := /Applications/Godot.app/Contents/MacOS/Godot
endif
GH_BIN ?= /opt/homebrew/bin/gh
PROJECT_ROOT := $(CURDIR)
PROJECT_NAME ?= $(notdir $(PROJECT_ROOT))
NPX ?= npx
KIT ?= platformer
OUTPUT_DIR ?= apps/$(KIT)-generated

.PHONY: help check-env git-status gh-version gh-auth gh-create-private gh-push-main godot-version godot-import godot-smoke gut-test godot-editor editor smoke test ci-verify setup-hooks verify play forge-help generate-project

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
	@echo "  make gut-test      - run the current automated GUT test suite"
	@echo "  make smoke         - platform-standard alias for the headless startup check"
	@echo "  make test          - platform-standard alias for the automated test suite"
	@echo "  make ci-verify     - CI-facing verification gate including FIXME enforcement"
	@echo "  make setup-hooks   - install the local pre-commit hook"
	@echo "  make verify        - run the required preflight before handing work to a human"
	@echo "  make editor        - platform-standard alias for opening the Godot editor"
	@echo "  make godot-editor  - launch the Godot editor for this project"
	@echo "  make play          - run preflight, then launch the game directly"
	@echo "  make forge-help    - smoke-test Godot Forge availability via npx"
	@echo "  make generate-project KIT=name OUTPUT_DIR=path - generate a student project from a kit"

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

gut-test: godot-import
	@$(GODOT_BIN) --headless -d -s --path "$(PROJECT_ROOT)" addons/gut/gut_cmdln.gd -gconfig=res://.gutconfig.json -gexit

test: gut-test

smoke: godot-smoke

ci-verify: test smoke
	@echo "[ci] Checking for FIXME markers..."
	@if grep -R "FIXME" . \
		--include="*.gd" \
		--exclude-dir=".git" \
		--exclude-dir="node_modules" \
		--exclude-dir="scripts" \
		--exclude-dir="templates"; then \
		echo "[ci] ❌ FIXME found in gameplay files"; \
		exit 1; \
	fi
	@echo "[ci] ✅ Full verification passed."

setup-hooks:
	@chmod +x scripts/hooks/pre-commit.sh
	@ln -sf ../../scripts/hooks/pre-commit.sh .git/hooks/pre-commit
	@echo "✅ Pre-commit hook installed"

editor: godot-editor

verify: test smoke
	@echo "Verification passed: assets imported and headless startup succeeded."

godot-editor:
	@$(GODOT_BIN) --editor --path "$(PROJECT_ROOT)"

play: verify
	@$(GODOT_BIN) --path "$(PROJECT_ROOT)"

generate-project:
	@python3 scripts/generate_project.py --kit "$(KIT)" --output "$(OUTPUT_DIR)"

forge-help:
	@$(NPX) -y godot-forge --help
