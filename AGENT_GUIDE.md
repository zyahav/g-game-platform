# Agent Guide

This project is a small Godot 4.6 2D platformer prototype.

## Read Order For A New Session

Read these files in order before making meaningful changes:

1. `SESSION_START.md`
2. `state/current-status.md`
3. `state/task-board.md`
4. `state/session-log.md`
5. Relevant specs under `specs/`
6. `tools/godot-agent-tooling-registry.md` when the task touches testing, verification, automation, or dev tooling

Use the reusable framework in `packages/game-agent/` as support material, not as the source of truth for this specific project.

## What Lives Where

- Project-specific truth lives in the repo root:
  - `state/`
  - `specs/`
  - `tools/`
  - `AGENT_GUIDE.md`
  - `SESSION_START.md`
- Reusable process/framework material lives in:
  - `packages/game-agent/`

## Working Style

- Be spec-driven when adding or changing features.
- Prefer direct implementation over long planning unless a choice is risky.
- Keep the project organized and predictable.
- Prefer existing `make` targets for repeatable project commands before inventing new one-off commands.
- Copy source assets into this project instead of referencing outside folders.
- Reusable gameplay elements should live in dedicated scenes and scripts.
- Use the package workflow only if it helps; do not let framework ceremony block shipping the game.

## Folder Structure

- `assets/audio/sfx/` for sound effects
- `assets/audio/music/` for music
- `assets/characters/` for character art
- `assets/collectibles/` for collectible art
- `assets/generated/` for generated or cropped art used in-game
- `scenes/` for game scenes
- `scenes/collectibles/` for reusable collectible scenes
- `scenes/ui/` for UI scenes when needed
- `scripts/` for gameplay scripts
- `scripts/collectibles/` for collectible logic
- `specs/` for project and feature specs
- `state/` for current progress, task tracking, and session handoff notes
- `tools/` for the repo's live tooling registry and tool-evaluation notes
- `Makefile` for repeatable local commands such as Godot smoke tests and tooling checks
- `packages/game-agent/` for the reusable project-starter package

## Quality Bar

- Wire features end to end, not partially.
- After meaningful changes, review for bugs, regressions, and missing verification.
- State clearly what was verified and what could not be run locally.
- Keep file and node names clear and stable.
- Use `state/verification-checklist.md` before closing a significant task.
- If a session evaluates external tooling, update `tools/godot-agent-tooling-registry.md`.

## Handoff Rule

Before ending a significant work session, update:

- `state/current-status.md`
- `state/task-board.md`
- `state/session-log.md`
- `state/verification-checklist.md` when relevant

That way the next session can resume from repo state instead of chat history.
