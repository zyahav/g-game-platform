#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


TEMP_SOURCE_DIRNAME = "._platform_source"
TEMP_GENERATED_DIRNAME = "._generated"
ROOT_IGNORE_NAMES = {".git", ".home", "__pycache__", TEMP_SOURCE_DIRNAME, TEMP_GENERATED_DIRNAME}
SHARED_KAYA_FILES = ("Mission.md", "Soul.md", "Boundaries.md", "Playbook.md", "Lessons.md", "TTS.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a student project from a platform kit.")
    parser.add_argument("--kit", required=True, help="Kit id to generate from, for example 'platformer'")
    parser.add_argument("--output", required=True, help="Output directory for the generated project")
    parser.add_argument("--name", help="Optional generated project name")
    parser.add_argument(
        "--in-place-root",
        action="store_true",
        help="Allow destructive transformation of an existing non-empty platform root into the final generated project.",
    )
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


def remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def clear_directory(root: Path, keep_names: set[str] | None = None) -> None:
    keep_names = keep_names or set()
    if not root.exists():
        return
    for child in root.iterdir():
        if child.name in keep_names:
            continue
        remove_path(child)


def move_directory_contents(src_root: Path, dst_root: Path) -> None:
    for child in list(src_root.iterdir()):
        shutil.move(str(child), str(dst_root / child.name))


def top_level_output_name(repo_root: Path, output_root: Path) -> str | None:
    try:
        relative = output_root.relative_to(repo_root)
    except ValueError:
        return None
    if not relative.parts:
        return None
    return relative.parts[0]


def copy_repo_snapshot(src_root: Path, dst_root: Path, *, exclude_top_level: str | None = None) -> None:
    ignore_names = set(ROOT_IGNORE_NAMES)
    if exclude_top_level:
        ignore_names.add(exclude_top_level)

    dst_root.mkdir(parents=True, exist_ok=False)
    ignore_patterns = shutil.ignore_patterns(*sorted(ROOT_IGNORE_NAMES))

    for child in src_root.iterdir():
        if child.name in ignore_names:
            continue
        destination = dst_root / child.name
        if child.is_dir() and not child.is_symlink():
            shutil.copytree(child, destination, ignore=ignore_patterns)
        else:
            copy_file(child, destination)


def cleanup_temp_roots(output_root: Path) -> None:
    remove_path(output_root / TEMP_SOURCE_DIRNAME)
    remove_path(output_root / TEMP_GENERATED_DIRNAME)


def write_generated_project_readme(output_dir: Path, manifest: dict[str, object], project_name: str) -> None:
    engine = manifest["engine"]["version"]  # type: ignore[index]
    write_text(
        output_dir / "README.md",
        f"""# {project_name}

Kit: `{manifest["kit_name"]}`

{manifest["description"]}

Engine: Godot {engine}

## How To Start

1. Open Codex in this folder
2. Start a new chat
3. Kaya will take it from there

## Commands

- `make doctor`
- `make play`
- `make test`
- `make smoke`
- `make ci-verify`
- `make verify`
- `make editor`
- `make tts TTS_TEXT="Hello there"`
- `make tts-test`

If `make` is unavailable, use `python3 scripts/project_tasks.py <command>` instead.

---

## For The Agent Reading This File

You are Thread 1 — the Coach.

Read `learning/coach.md` now and follow it exactly.
Do not read `AGENT.md` unless you are explicitly acting as the Dev thread.
Do not improvise. Do not start teaching until you read `learning/coach.md`.
""",
    )


def write_generated_project_learning_layer(repo_root: Path, output_dir: Path, manifest: dict[str, object]) -> None:
    kit_id = str(manifest["kit_id"])
    learning_root = output_dir / "learning"
    kaya_root = learning_root / "kaya"

    for filename in SHARED_KAYA_FILES:
        copy_file(repo_root / "learning" / "kaya" / filename, kaya_root / filename)

    lesson_spec = repo_root / "learning" / "lessons" / f"{kit_id}.md"
    if lesson_spec.exists():
        copy_file(lesson_spec, learning_root / "lessons" / lesson_spec.name)

    write_text(
        learning_root / "coach.md",
        f"""# Coach — Generated Project Loader

This file is the Thread 1 entry point for this generated project.

When you read this file, you are Kaya.
Read the files below in order. All of them. Then begin the session.

---

## Always Read (Every Session)

1. `learning/kaya/Mission.md` — why you exist and what success looks like
2. `learning/kaya/Soul.md` — your personality, voice, and how you talk
3. `learning/kaya/Boundaries.md` — hard rules you never break
4. `learning/kaya/Playbook.md` — how to handle specific situations
5. `learning/kaya/TTS.md` — how to speak when voice is enabled

Then read `state/student.md`.

---

## First Session Only

If `state/student.md` does not exist or `sessions` is 0:

6. `learning/kaya/Onboarding.md` — follow this for the first session in this generated project

---

## Ongoing Sessions

If `state/student.md` exists and `sessions` is greater than 0:

6. `learning/kaya/Lessons.md` — continue the lesson flow

---

## Chosen Kit Reference

If `learning/lessons/{kit_id}.md` exists, read it as the chosen-kit lesson spec before guiding lesson-specific work.

---

## Do Not Read

- `AGENT.md` — that is for the Dev thread only
- `core/` — that is the engineering layer, not yours
- Any file not listed above unless the student explicitly asks to inspect it

---

## After Reading

You are Kaya. Begin the session.
Do not summarize what you read. Do not explain the system.
Just say hello.
""",
    )

    write_text(
        kaya_root / "Onboarding.md",
        """# Kaya — Generated Project Onboarding

This file is for the first student session in an already-generated project.
The game already exists. Do not tell the student to clone or generate a new one.

After the student has felt the game, switch to `Lessons.md`.

## Step 1 — Introduction

The very first thing Kaya says:

> "Hi, I'm Kaya! What's your name?"

Wait. Do not continue until they reply.

## Step 2 — Save the Name

After they give their name:
- Save it to `state/student.md`
- Use it immediately in the next message

> "Nice to meet you, [name]! This project is already set up. We're going to build on top of it together. Ready?"

## Step 3 — First Time Question

> "Before we start — have you made a game before?
> 1 — Never, this is new
> 2 — A little, I've tried something
> 3 — I know Godot already"

This changes how much context Kaya gives, not what lessons to skip.

## Step 4 — Start With The Game

Move immediately to `Lessons.md`, Lesson 1 — First Wow.

If the student hits a tooling blocker before they can run the game, introduce the Dev thread with this message:

```
--- START: PM TO DEV ---
This project is already generated.
Read AGENT.md.
Run `make doctor` or `python3 scripts/project_tasks.py doctor` first.
Repair any environment issues automatically before asking the student to do technical setup.
Report back when the game is ready to run.
--- END: PM TO DEV ---
```

Do not ask the student to troubleshoot environment issues manually before the Dev has tried to repair them.
""",
    )

    write_text(
        output_dir / "state" / "student.md",
        """# Student Profile

name: 
sessions: 0
last_lesson: 0
notes: 

# Kaya fills this in during the first session and updates it each time.
# This file is what makes Kaya remember who she is talking to.
# The student can read and edit this file too — that is part of learning how the system works.
""",
    )


def generate_project_contents(
    repo_root: Path,
    kit_root: Path,
    manifest: dict[str, object],
    output_dir: Path,
    project_name: str,
    generated_at: str,
) -> None:
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

- `## Stage` is `Freshly generated project with coaching layer`
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
- Before asking the student for environment help, run `make doctor` or `python3 scripts/project_tasks.py doctor` and attempt automatic repair first.
- If `make` is unavailable, use `python3 scripts/project_tasks.py <command>` or `python scripts/project_tasks.py <command>`.
- Project tasks use a local `.home/` automatically so Godot does not depend on global machine paths.
- Use `make verify` or `python3 scripts/project_tasks.py verify` before handing runtime changes to a human.
""",
    )

    write_generated_project_readme(output_dir, manifest, project_name)
    write_generated_project_learning_layer(repo_root, output_dir, manifest)

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
.home/

# Web export and deploy working copy
build/
""",
    )

    write_text(
        output_dir / "publish.toml",
        """# Publish configuration for this project.
# Fill in these values before running: make publish

[publish]
user_handle = ""
project_name = ""
vm_host = ""
public_url = ""
deploy_remote = ""
ssh_key_path = ""

# deploy_remote is optional.
# If left empty, it is derived as:
#   <user_handle>@<vm_host>:/srv/git/<user_handle>/<project_name>.git

# ssh_key_path is the path to your SSH deploy key for this project.
# Example: ~/.ssh/myproject_deploy_key
# One key per project. The agent configures this during publish-init.
""",
    )

    write_text(
        output_dir / "Makefile",
        """PATH := /opt/homebrew/bin:/usr/local/bin:$(PATH)
export PATH

PYTHON_BIN ?= $(shell command -v python3 2>/dev/null)
ifeq ($(PYTHON_BIN),)
PYTHON_BIN := $(shell command -v python 2>/dev/null)
endif

VOICE ?= af_bella
TTS_TEXT ?= Hello, this is a live TTS test from Kaya.

.PHONY: doctor smoke test ci-verify verify play editor setup-hooks tts tts-test export-web publish-check publish-init publish publish-info publish-status

doctor:
\t@$(PYTHON_BIN) scripts/project_tasks.py doctor

smoke:
\t@$(PYTHON_BIN) scripts/project_tasks.py smoke

test:
\t@$(PYTHON_BIN) scripts/project_tasks.py test

ci-verify:
\t@$(PYTHON_BIN) scripts/project_tasks.py ci-verify

verify:
\t@$(PYTHON_BIN) scripts/project_tasks.py verify

play:
\t@$(PYTHON_BIN) scripts/project_tasks.py play

editor:
\t@$(PYTHON_BIN) scripts/project_tasks.py editor

setup-hooks:
\t@$(PYTHON_BIN) scripts/project_tasks.py setup-hooks

tts:
\t@$(PYTHON_BIN) scripts/project_tasks.py tts "$(TTS_TEXT)" --voice "$(VOICE)"

tts-test:
\t@$(PYTHON_BIN) scripts/project_tasks.py tts-test --voice "$(VOICE)"

export-web:
\t@$(PYTHON_BIN) scripts/project_tasks.py export-web

publish-check:
\t@$(PYTHON_BIN) scripts/project_tasks.py publish-check

publish-init:
\t@$(PYTHON_BIN) scripts/project_tasks.py publish-init

publish:
\t@$(PYTHON_BIN) scripts/project_tasks.py publish

publish-info:
\t@$(PYTHON_BIN) scripts/project_tasks.py publish-info

publish-status:
\t@$(PYTHON_BIN) scripts/project_tasks.py publish-status
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
    copy_tree(
        template_root / "assets" / "environment" / "free_platformer_na" / "background",
        output_dir / "assets" / "environment" / "free_platformer_na" / "background",
    )
    copy_tree(
        template_root / "assets" / "environment" / "free_platformer_na" / "generated",
        output_dir / "assets" / "environment" / "free_platformer_na" / "generated",
    )
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

Freshly generated project with coaching layer

## Summary

- Project generated from the `{manifest["kit_id"]}` kit
- Core and kit reference layers copied in
- Starter game files scaffolded from the kit templates
- Student-facing learning layer seeded under `learning/`
- Live working system ready in `state/`, `specs/`, and `tools/`

## Last Known Working Direction

- Student-facing sessions start from `README.md`
- Dev threads start from `AGENT.md`
- Begin cold-start initialization and first-session onboarding

## Known Gaps

- State files are still in template form
- No project-specific work has been recorded yet

## Verified Automation

- Generated from the platform on {generated_at}

## Resume Here

1. Student-facing sessions begin from `README.md`
2. Dev threads begin from `AGENT.md`
3. Replace this template state with real project progress
""",
    )

    write_text(
        output_dir / "state" / "task-board.md",
        """# Task Board

## Done

- Project scaffolded from selected kit
- Student-facing learning layer seeded into the generated project

## In Progress

- First student onboarding in this generated project

## Next

- Run the game through Lesson 1
- Review seeded specs
- Begin the first feature task when the student is ready

## Blocked

- None yet
""",
    )

    write_text(
        output_dir / "docs" / "PUBLISHING.md",
        """# Publishing Your Game

Say "publish my game" to Kaya. She will handle it.

## What Happens

1. Kaya asks the Dev to publish.
2. The Dev exports the game for the web.
3. The Dev pushes the export to your hosting server.
4. You get a live URL.

## Configuration

Edit `publish.toml` with your project details.
Required fields:
- `user_handle` — your username on the server
- `project_name` — your project name
- `vm_host` — the server address
- `public_url` — the public URL for your game

## Source vs Deploy

Your source code lives in this repo.
Your live game comes from `build/web/`, which is a separate deploy working copy.
Only exported web files are pushed live — not your source code.

## Commands (if you need them directly)

- `make export-web` — export the game for the web
- `make publish-check` — verify the export is ready
- `make publish` — export and publish in one step
- `make publish-status` — check current publish readiness
- `make publish-info` — show your public URL and deploy config
""",
    )

    write_text(
        output_dir / "state" / "session-log.md",
        f"""# Session Log

## {generated_at[:10]}

- Generated project scaffolded from platform kit
- Core and kit reference layers copied in
- Starter game files, tests, docs, and verification files created
- Student-facing learning layer created under `learning/`
- Generated project startup now begins from `README.md` for Thread 1 and `AGENT.md` for the Dev thread

## Handoff Note

This project has not yet gone through a real development session.
""",
    )

    write_text(
        output_dir / "state" / "verification-checklist.md",
        """# Verification Checklist

## Required Gate Before Human Handoff

- Run `make verify` or `python3 scripts/project_tasks.py verify` before asking a human to play or inspect the game
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

- `make doctor` — environment preflight and automatic repair where possible
- `make smoke` — headless startup check
- `make test` — automated test suite
- `make ci-verify` — CI-facing verification including FIXME enforcement
- `make verify` — required gate before handoff
- `make play` — run the game
- `make editor` — open the project in Godot

If `make` is unavailable, use `python3 scripts/project_tasks.py <command>` instead.

The project task runner automatically:

- repairs `git safe.directory` when the environment reports dubious ownership
- uses a local `.home/` so Godot can write inside the project
- provides the same commands without depending on `make`

## Manual Checks

- Confirm the game starts
- Confirm the starter loop is playable
- Confirm win/lose/restart flow still works after meaningful changes
""",
    )

    copy_file(repo_root / "scripts" / "hooks" / "pre-commit.sh", output_dir / "scripts" / "hooks" / "pre-commit.sh")
    copy_file(repo_root / "scripts" / "kaya_tts.sh", output_dir / "scripts" / "kaya_tts.sh")
    copy_file(repo_root / "templates" / "generated-project" / "project_tasks.py", output_dir / "scripts" / "project_tasks.py")
    write_text(
        output_dir / "scripts" / "ci" / "verify.sh",
        """#!/usr/bin/env bash
set -e

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
else
  PYTHON_BIN=python
fi

"$PYTHON_BIN" scripts/project_tasks.py ci-verify
""",
    )
    (output_dir / "scripts" / "hooks" / "pre-commit.sh").chmod(0o755)
    (output_dir / "scripts" / "kaya_tts.sh").chmod(0o755)
    (output_dir / "scripts" / "project_tasks.py").chmod(0o755)
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


def generate_into_output_root(
    repo_root: Path,
    kit_root: Path,
    manifest: dict[str, object],
    output_root: Path,
    project_name: str,
    generated_at: str,
) -> None:
    temp_source = output_root / TEMP_SOURCE_DIRNAME
    temp_generated = output_root / TEMP_GENERATED_DIRNAME

    cleanup_temp_roots(output_root)
    copy_repo_snapshot(repo_root, temp_source, exclude_top_level=top_level_output_name(repo_root, output_root))
    generate_project_contents(temp_source, temp_source / "kits" / str(manifest["kit_id"]), manifest, temp_generated, project_name, generated_at)
    clear_directory(output_root, keep_names={TEMP_SOURCE_DIRNAME, TEMP_GENERATED_DIRNAME})
    move_directory_contents(temp_generated, output_root)
    cleanup_temp_roots(output_root)


def prepare_output_root(output_root: Path, repo_root: Path, *, in_place_root: bool) -> None:
    if output_root.exists():
        if not output_root.is_dir():
            raise SystemExit(f"Output path is not a directory: {output_root}")
        if any(output_root.iterdir()):
            if not in_place_root:
                raise SystemExit(
                    "Output directory already exists and is not empty. "
                    "Use --in-place-root only when transforming an existing platform root in place."
                )
            if output_root != repo_root:
                raise SystemExit(
                    "--in-place-root is only supported when --output points at the current platform source root."
                )
        return

    output_root.mkdir(parents=True, exist_ok=False)


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    kit_root = repo_root / "kits" / args.kit
    if not kit_root.exists():
        raise SystemExit(f"Kit not found: {args.kit}")

    manifest = json.loads((kit_root / "kit.manifest.json").read_text(encoding="utf-8"))
    output_root = Path(args.output).resolve()
    project_name = args.name or f"{manifest['kit_name']} Starter"
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    prepare_output_root(output_root, repo_root, in_place_root=args.in_place_root)

    try:
        generate_into_output_root(repo_root, kit_root, manifest, output_root, project_name, generated_at)
    except (Exception, SystemExit):
        cleanup_temp_roots(output_root)
        clear_directory(output_root)
        raise

    print(f"Generated project at {output_root}")


if __name__ == "__main__":
    main()
