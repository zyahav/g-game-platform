GODOT_BIN ?= /Applications/Godot.app/Contents/MacOS/Godot
PROJECT_ROOT := $(CURDIR)
NPX ?= npx

.PHONY: help check-env git-status godot-version godot-import godot-smoke godot-editor forge-help

help:
	@echo "Available targets:"
	@echo "  make check-env     - verify local tools used by this repo"
	@echo "  make git-status    - show local git status"
	@echo "  make godot-version - print the Godot binary version"
	@echo "  make godot-import  - import project assets in headless editor mode"
	@echo "  make godot-smoke   - open the project headlessly and quit after startup"
	@echo "  make godot-editor  - launch the Godot editor for this project"
	@echo "  make forge-help    - smoke-test Godot Forge availability via npx"

check-env:
	@echo "git: $$(git --version)"
	@echo "make: $$(make --version | sed -n '1p')"
	@echo "node: $$(node --version)"
	@echo "npm: $$(npm --version)"
	@echo "python3: $$(python3 --version)"
	@echo "godot: $$($(GODOT_BIN) --version)"
	@echo "gh: $$(command -v gh || echo missing)"
	@echo "uvx: $$(command -v uvx || echo missing)"

git-status:
	@git status -sb

godot-version:
	@$(GODOT_BIN) --version

godot-import:
	@$(GODOT_BIN) --headless --path "$(PROJECT_ROOT)" --import --quit

godot-smoke:
	@$(GODOT_BIN) --headless --path "$(PROJECT_ROOT)" --editor --quit-after 1

godot-editor:
	@$(GODOT_BIN) --path "$(PROJECT_ROOT)"

forge-help:
	@$(NPX) -y godot-forge --help
