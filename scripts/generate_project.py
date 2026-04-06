#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a student project from a platform kit.")
    parser.add_argument("--kit", required=True, help="Kit id to generate from, for example 'platformer'")
    parser.add_argument("--output", required=True, help="Output directory for the generated project")
    parser.add_argument("--name", help="Optional generated project name")
    return parser.parse_args()


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def replace_text(path: Path, replacements: list[tuple[str, str]]) -> None:
    content = path.read_text(encoding="utf-8")
    for old, new in replacements:
        content = content.replace(old, new)
    path.write_text(content, encoding="utf-8")


def strip_ext_resource_uids(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    content = re.sub(r' uid="uid://[^"]+"', "", content)
    path.write_text(content, encoding="utf-8")


def add_gitkeeps(root: Path) -> None:
    for directory in sorted(p for p in root.rglob("*") if p.is_dir()):
        if any(directory.iterdir()):
            continue
        (directory / ".gitkeep").write_text("", encoding="utf-8")


def ensure_git_repo(output_dir: Path) -> None:
    subprocess.run(["git", "init", "-b", "main", str(output_dir)], check=True)


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    kit_root = repo_root / "kits" / args.kit
    if not kit_root.exists():
        raise SystemExit(f"Kit not found: {args.kit}")

    manifest = json.loads((kit_root / "kit.manifest.json").read_text(encoding="utf-8"))
    output_dir = Path(args.output).resolve()
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")

    project_name = args.name or f"{manifest['kit_name']} Starter"
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    output_dir.mkdir(parents=True, exist_ok=False)
    ensure_git_repo(output_dir)

    copy_tree(repo_root / "core", output_dir / "core")

    kit_output = output_dir / "kit"
    kit_output.mkdir()
    copy_file(kit_root / "kit.manifest.json", kit_output / "kit.manifest.json")
    copy_file(kit_root / "KIT.md", kit_output / "KIT.md")
    copy_file(kit_root / "AGENT_RULES.md", kit_output / "AGENT_RULES.md")
    copy_tree(kit_root / "specs", kit_output / "specs")
    copy_tree(kit_root / "skills", kit_output / "skills")
    copy_tree(kit_root / "acceptance", kit_output / "acceptance")

    template_root = kit_root / "templates"

    copy_file(template_root / "project.godot", output_dir / "project.godot")
    copy_file(template_root / "icon.svg", output_dir / "icon.svg")

    write_text(
        output_dir / "project.kit.json",
        json.dumps(
            {
                "kit_id": manifest["kit_id"],
                "kit_name": manifest["kit_name"],
                "kit_version": manifest["version"],
                "core_version": (repo_root / "core" / "VERSION").read_text(encoding="utf-8").strip(),
                "engine": manifest["engine"],
                "generated_at": generated_at,
            },
            indent=2,
        )
        + "\n",
    )

    write_text(
        output_dir / "AGENT.md",
        f"""# Generated Project Agent Guide

This is a generated student project based on the `{manifest["kit_id"]}` kit.

## Cold Start Mode

Use cold start when `state/current-status.md` is missing, or when it still reflects the generated template state.

Cold-start markers include:

- `## Stage` is `Freshly generated project`
- `## Known Gaps` still says `State files are still in template form`

1. Read `project.kit.json`.
2. Read `core/`.
3. Read `kit/`.
4. Initialize and update `specs/`, `state/`, and `tools/`.
5. Begin development from the selected kit.

## Ongoing Session Mode

Use ongoing-session mode when the project already has real project state and the cold-start markers above have been replaced.

1. Read `project.kit.json`.
2. Read `state/`.
3. Read `specs/`.
4. Read `tools/`.
5. Consult `core/` and `kit/` only as reference layers when needed.
6. Continue from the current in-progress work.

## Project Rules

- Treat `core/` and `kit/` as read-only reference layers by default.
- Treat `specs/`, `state/`, and `tools/` as the live working system.
- Use `make verify` before handing runtime changes to a human.
""",
    )

    write_text(
        output_dir / "README.md",
        f"""# {project_name}

Kit: `{manifest["kit_name"]}`

{manifest["description"]}

Engine: Godot {manifest["engine"]["version"]}

## Commands

- `make play`
- `make test`
- `make smoke`
- `make verify`
- `make editor`

Start new sessions by reading `AGENT.md`.
""",
    )

    write_text(
        output_dir / ".gitignore",
        """# Godot 4+ specific ignores
.godot/
/android/

# OS/editor junk
.DS_Store
Thumbs.db

# Temp/build output
*.tmp
*.temp
*.log
""",
    )

    write_text(
        output_dir / "Makefile",
        """PATH := /opt/homebrew/bin:/usr/local/bin:$(PATH)
export PATH

GODOT_BIN ?= $(shell command -v godot 2>/dev/null)
ifeq ($(GODOT_BIN),)
GODOT_BIN := /Applications/Godot.app/Contents/MacOS/Godot
endif
PROJECT_ROOT := $(CURDIR)

.PHONY: smoke test ci-verify verify play editor setup-hooks

smoke:
\t@$(GODOT_BIN) --headless --path "$(PROJECT_ROOT)" --editor --quit-after 1

test:
\t@$(GODOT_BIN) --headless --path "$(PROJECT_ROOT)" --import --quit
\t@$(GODOT_BIN) --headless -d -s --path "$(PROJECT_ROOT)" addons/gut/gut_cmdln.gd -gconfig=res://.gutconfig.json -gexit

ci-verify: test smoke
\t@echo "[ci] Checking for FIXME markers..."
\t@if grep -R "FIXME" . \\
\t\t--include="*.gd" \\
\t\t--exclude-dir=".git" \\
\t\t--exclude-dir="node_modules"; then \\
\t\techo "[ci] ❌ FIXME found in gameplay files"; \\
\t\texit 1; \\
\tfi
\t@echo "[ci] ✅ Full verification passed."

verify: test smoke
\t@echo "Verification passed."

play: verify
\t@$(GODOT_BIN) --path "$(PROJECT_ROOT)"

editor:
\t@$(GODOT_BIN) --editor --path "$(PROJECT_ROOT)"

setup-hooks:
\t@chmod +x scripts/hooks/pre-commit.sh
\t@mkdir -p .git/hooks
\t@ln -sf ../../scripts/hooks/pre-commit.sh .git/hooks/pre-commit
\t@echo "✅ Pre-commit hook installed"
""",
    )

    copy_tree(repo_root / "addons" / "gut", output_dir / "addons" / "gut")
    write_text(
        output_dir / ".gutconfig.json",
        json.dumps(
            {
                "dirs": ["res://tests/unit"],
                "include_subdirs": True,
                "prefix": "test_",
                "suffix": ".gd",
                "log_level": 1,
                "should_exit": True,
                "should_maximize": False,
                "ignore_pause": True,
                "tests": [],
            },
            indent=2,
        )
        + "\n",
    )

    game_dirs = [
        output_dir / "assets" / "audio" / "sfx",
        output_dir / "assets" / "audio" / "music",
        output_dir / "assets" / "characters" / "player",
        output_dir / "assets" / "collectibles" / "coins",
        output_dir / "assets" / "environment" / "free_platformer_na" / "background",
        output_dir / "assets" / "environment" / "free_platformer_na" / "generated",
        output_dir / "assets" / "generated",
        output_dir / "scenes" / "collectibles",
        output_dir / "scenes" / "hazards",
        output_dir / "scenes" / "progression",
        output_dir / "scenes" / "ui",
        output_dir / "scripts" / "collectibles",
        output_dir / "scripts" / "hazards",
        output_dir / "scripts" / "progression",
        output_dir / "tests" / "unit",
        output_dir / "state",
        output_dir / "specs" / "features",
        output_dir / "tools",
        output_dir / "docs",
        output_dir / "scripts" / "hooks",
        output_dir / "scripts" / "ci",
        output_dir / ".github" / "workflows",
    ]
    for directory in game_dirs:
        directory.mkdir(parents=True, exist_ok=True)

    copy_file(template_root / "Main.tscn", output_dir / "scenes" / "Main.tscn")
    copy_file(template_root / "Player.tscn", output_dir / "scenes" / "Player.tscn")
    copy_file(template_root / "main.gd", output_dir / "scripts" / "main.gd")
    copy_file(template_root / "player.gd", output_dir / "scripts" / "player.gd")
    copy_tree(template_root / "scenes" / "collectibles", output_dir / "scenes" / "collectibles")
    copy_tree(template_root / "scenes" / "hazards", output_dir / "scenes" / "hazards")
    copy_tree(template_root / "scenes" / "progression", output_dir / "scenes" / "progression")
    copy_tree(template_root / "scripts" / "collectibles", output_dir / "scripts" / "collectibles")
    copy_tree(template_root / "scripts" / "hazards", output_dir / "scripts" / "hazards")
    copy_tree(template_root / "scripts" / "progression", output_dir / "scripts" / "progression")
    copy_tree(template_root / "assets" / "audio" / "sfx", output_dir / "assets" / "audio" / "sfx")
    copy_tree(template_root / "assets" / "collectibles" / "coins", output_dir / "assets" / "collectibles" / "coins")
    copy_tree(template_root / "assets" / "environment" / "free_platformer_na" / "background", output_dir / "assets" / "environment" / "free_platformer_na" / "background")
    copy_tree(template_root / "assets" / "environment" / "free_platformer_na" / "generated", output_dir / "assets" / "environment" / "free_platformer_na" / "generated")
    copy_tree(template_root / "assets" / "generated", output_dir / "assets" / "generated")
    copy_tree(template_root / "Player", output_dir / "assets" / "characters" / "player")

    replace_text(
        output_dir / "project.godot",
        [
            ('config/name="FarmGame"', f'config/name="{project_name}"'),
            ('run/main_scene="uid://4kjj8gh3oya3"', 'run/main_scene="res://scenes/Main.tscn"'),
        ],
    )

    replace_text(
        output_dir / "scenes" / "Main.tscn",
        [
            ('path="res://main.gd"', 'path="res://scripts/main.gd"'),
            ('path="res://Player.tscn"', 'path="res://scenes/Player.tscn"'),
        ],
    )

    replace_text(
        output_dir / "scenes" / "Player.tscn",
        [
            ('path="res://player.gd"', 'path="res://scripts/player.gd"'),
            ('path="res://Player/', 'path="res://assets/characters/player/'),
        ],
    )
    strip_ext_resource_uids(output_dir / "scenes" / "Main.tscn")
    strip_ext_resource_uids(output_dir / "scenes" / "Player.tscn")

    write_text(
        output_dir / "state" / "current-status.md",
        f"""# Current Status

## Stage

Freshly generated project

## Summary

- Project generated from the `{manifest["kit_id"]}` kit
- Core and kit reference layers copied in
- Starter game files scaffolded from the kit templates
- Live working system ready in `state/`, `specs/`, and `tools/`

## Last Known Working Direction

- Begin cold-start initialization
- Confirm the starter project runs with `make play`
- Continue work from the seeded feature specs

## Known Gaps

- State files are still in template form
- No project-specific work has been recorded yet

## Verified Automation

- Generated from the platform on {generated_at}

## Resume Here

1. Read `AGENT.md`
2. Confirm cold-start initialization
3. Update this file with real project state
""",
    )

    write_text(
        output_dir / "state" / "task-board.md",
        """# Task Board

## Done

- Project scaffolded from selected kit

## In Progress

- Cold-start project initialization

## Next

- Confirm the starter project runs
- Review seeded specs
- Begin the first feature task

## Blocked

- None yet
""",
    )

    write_text(
        output_dir / "state" / "session-log.md",
        f"""# Session Log

## {generated_at[:10]}

- Generated project scaffolded from platform kit
- Core and kit reference layers copied in
- Starter game files, tests, docs, and verification files created

## Handoff Note

This project has not yet gone through a real development session.
""",
    )

    write_text(
        output_dir / "state" / "verification-checklist.md",
        """# Verification Checklist

## Required Gate Before Human Handoff

- Run `make verify` before asking a human to play or inspect the game
- Treat runtime-affecting changes as gate-worthy, including gameplay code, scene edits, config changes, and debug instrumentation
- If verification fails, fix it before handoff
- If verification is blocked, say so clearly and do not hand off the build as runnable

## Verification Result

- State what was tested
- State what could not be tested
- State whether `make verify` passed

## Handoff

Update:

- `state/current-status.md`
- `state/task-board.md`
- `state/session-log.md`
""",
    )

    write_text(
        output_dir / "specs" / "vision.md",
        f"""# Vision

## Project

`{project_name}` is a generated Godot project based on the `{manifest["kit_name"]}` kit.

## Core Loop

- Start the run
- Move and jump across the course
- Collect progress items
- Avoid hazards
- Reach the goal

## Design Goals

- Fast iteration
- Clear folder structure
- Reusable gameplay systems
- Spec-driven development
""",
    )
    copy_file(repo_root / "specs" / "feature-template.md", output_dir / "specs" / "feature-template.md")
    copy_tree(kit_root / "specs", output_dir / "specs" / "features")

    write_text(
        output_dir / "tools" / "tooling-registry.md",
        """# Tooling Registry

Track project-level tooling decisions here.

## Status Legend

- `Considering`
- `Accepted`
- `Rejected`
- `Blocked`

## Entries

Add tools here when the project evaluates them so future sessions do not repeat the same decision process.
""",
    )

    write_text(
        output_dir / "docs" / "TESTING.md",
        """# Testing

Use these commands during development:

- `make smoke` — headless startup check
- `make test` — automated test suite
- `make ci-verify` — CI-facing verification including FIXME enforcement
- `make verify` — required gate before handoff
- `make play` — run the game
- `make editor` — open the project in Godot

## Manual Checks

- Confirm the game starts
- Confirm the starter loop is playable
- Confirm win/lose/restart flow still works after meaningful changes
""",
    )

    copy_file(repo_root / "scripts" / "hooks" / "pre-commit.sh", output_dir / "scripts" / "hooks" / "pre-commit.sh")
    copy_file(repo_root / "scripts" / "ci" / "verify.sh", output_dir / "scripts" / "ci" / "verify.sh")
    (output_dir / "scripts" / "hooks" / "pre-commit.sh").chmod(0o755)
    (output_dir / "scripts" / "ci" / "verify.sh").chmod(0o755)

    write_text(
        output_dir / ".github" / "workflows" / "verify.yml",
        """name: Verify

on:
  pull_request:
    branches:
      - main

jobs:
  verify:
    runs-on: macos-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Install Godot
        run: brew install godot

      - name: Run verification
        run: make ci-verify
""",
    )

    copy_file(repo_root / "test" / "unit" / "test_coin.gd", output_dir / "tests" / "unit" / "test_coin.gd")
    copy_file(repo_root / "test" / "unit" / "test_main_scene.gd", output_dir / "tests" / "unit" / "test_main_scene.gd")
    replace_text(
        output_dir / "tests" / "unit" / "test_main_scene.gd",
        [('res://Main.tscn', 'res://scenes/Main.tscn')],
    )

    add_gitkeeps(output_dir / "assets")
    add_gitkeeps(output_dir / "scenes")
    add_gitkeeps(output_dir / "scripts")

    print(f"Generated project at {output_dir}")


if __name__ == "__main__":
    main()
