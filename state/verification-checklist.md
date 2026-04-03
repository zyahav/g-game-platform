# Verification Checklist

Run this checklist after implementing a meaningful feature or refactor.

## Required Gate Before Human Playback

- Run `make verify` before asking a human to play or inspect the game
- If `make verify` fails, fix the issue first or state the blocker clearly
- If `make verify` cannot be run, say that explicitly before handing off

## Files

- New files are in the correct folders
- Asset paths point inside this project
- Reusable logic is in scenes/scripts rather than duplicated inline

## Scene Wiring

- Root node types make sense
- Signals are connected correctly
- Required collision shapes and audio players exist
- Scene references still match current file locations

## Script Quality

- Exported values are used for tunable gameplay values when practical
- No obvious broken node paths or renamed references
- New code matches the current project structure

## Integration

- Feature works with existing systems
- Restart/reset flow still works
- HUD/state/audio interactions still work if relevant
- No known Godot editor errors were introduced

## Respawn Safety

- Any checkpoint or respawn logic restores a safe playable state, not only a position
- Respawning does not immediately trigger game over without player input
- If checkpoint logic exists, tests cover death-loop prevention after respawn

## Verification Result

- State what was tested
- State what could not be tested from the current session
- State whether `make verify` passed
- Add follow-up tasks if verification is blocked

## Handoff

Update:

- `state/current-status.md`
- `state/task-board.md`
- `state/session-log.md`
