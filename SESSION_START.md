# Session Start

If you are a new session starting work on this repo, read these in order:

1. `AGENT_GUIDE.md`
2. `state/current-status.md`
3. `state/task-board.md`
4. `state/session-log.md`
5. Relevant feature specs in `specs/features/`
6. `tools/godot-agent-tooling-registry.md` if the work touches testing, tooling, automation, or verification

## How To Use The Package

The reusable framework package lives at:

- `packages/game-agent/`

Use it for:

- workflow ideas
- starter templates
- skill references
- checklist patterns

Do not use the package's own `state/` folder as the active state for this project.

## Source Of Truth

For this project, the source of truth is:

- `state/`
- `specs/`
- `tools/`
- the actual project files in the repo root

## System Change Rule

If the work changes the agent system itself, do not implement that change on the first pass.

System changes include:

- new or changed repo rules
- new or changed reusable skills
- workflow/process changes
- verification-policy changes
- reusable package changes

For those changes, first read the current repo rules, then follow the discussion-first protocol in `AGENT_GUIDE.md` before editing the system.

## Handoff Rule

If the work changes runtime behavior, do not ask the user to run the game until the handoff gate in `AGENT_GUIDE.md` is satisfied.

This includes:

- gameplay code
- scene changes
- config changes
- debug instrumentation
- temporary logging

If verification is blocked or incomplete, do not hand the build to the user as runnable.

## Current Resume Goal

Resume from the first item in `state/task-board.md` under `In Progress`.
