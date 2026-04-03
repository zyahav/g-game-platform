# Verification Checklist

Run this checklist after implementing a meaningful feature or refactor.

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

## Verification Result

- State what was tested
- State what could not be tested from the current session
- Add follow-up tasks if verification is blocked

## Handoff

Update:

- `state/current-status.md`
- `state/task-board.md`
- `state/session-log.md`
