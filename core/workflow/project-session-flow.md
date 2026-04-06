# Project Session Flow

Generated projects follow a spec-driven loop with two explicit startup modes.

## Cold Start

Use cold start when the generated project has just been scaffolded or the live state files are still template-empty.

1. Read `project.kit.json`.
2. Read copied `core/` docs.
3. Read copied `kit/` docs.
4. Initialize the live project files in `state/`, `specs/`, and `tools/`.
5. Begin development from the selected kit's constraints and starter specs.

## Ongoing Session

Use ongoing-session mode when the generated project already has real state.

1. Read `project.kit.json`.
2. Read `state/current-status.md`, `state/task-board.md`, and `state/session-log.md`.
3. Read relevant specs under `specs/`.
4. Read `tools/tooling-registry.md` if the task touches testing, verification, or tooling.
5. Consult `core/` and `kit/` only as reference layers when needed.

## Development Loop

1. Understand current state and active specs.
2. Implement the smallest complete change that advances the current task.
3. Run the required verification gate.
4. Update state and verification records before handoff.
5. Only then ask for review or approval.
