# Skill: Progression Safety

Use this skill when implementing checkpoints, hazards, respawns, or other recovery systems in the platformer kit.

## Purpose

Preserve player trust by ensuring recovery systems restore a safe playable state.

## Pattern

- Implement hazards and checkpoints as reusable scenes connected through signals.
- Treat respawn as a validated safe state, not only a position.
- Store progression state explicitly: score, collected items, and active respawn location.
- Differentiate lose reasons when the game presents failure feedback.

## Proven Behaviors

- Hazard contact triggers game over for the player and ignores unrelated bodies.
- Checkpoint activation updates the active respawn state and saved progress.
- Respawn validation checks for ground and rejects invalid placements.
- Restart after win resets to a fresh run.

## Verification

- Test checkpoint activation and restore.
- Test safe respawn over initial physics frames.
- Test hazard-triggered failure separately from fall failure.
