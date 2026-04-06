# Platformer Kit Agent Rules

These rules apply when building with the `platformer` kit.

## Build From Proven Patterns

- Use the existing proven game as the source of truth for kit behavior.
- Distill mechanics, acceptance, and starter files from working scenes, scripts, and tests.
- Do not invent speculative systems when a proven pattern already exists in the source project.

## Structural Rules

- Keep player movement in a dedicated player scene and script.
- Keep level flow, HUD updates, checkpoints, hazards, and win/lose orchestration in a main scene controller.
- Keep collectibles, hazards, and checkpoints as reusable scenes with dedicated scripts.
- Prefer signals and groups for reusable gameplay systems over hard-coded scene-only logic.

## Gameplay Rules

- A platformer kit project must always remain playable from the keyboard.
- Checkpoints must update the active respawn state and must not create a death loop.
- Hazards and fall loss must be distinguishable in game-over feedback.
- HUD and overlay state must stay consistent across start, win, lose, and restart flows.

## Verification Rules

- `make verify` is the required handoff gate.
- Runtime-affecting changes need smoke and test coverage before handoff.
- New progression or respawn features must include automated coverage where practical.
