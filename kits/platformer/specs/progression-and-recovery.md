# Progression And Recovery

## Goal

Provide reusable hazards and checkpoints so failure and recovery are part of the platformer loop.

## Requirements

- Hazards trigger game over when the player touches them.
- Checkpoints save respawn state and relevant progress.
- Respawn after a checkpoint must restore a safe playable state.
- Respawn must not immediately kill the player or create a death loop.
- Restart after a win begins a fresh run rather than resuming from a checkpoint.

## Acceptance Criteria

- Hazard contact shows a lose state with hazard-specific messaging.
- Activating a checkpoint saves score and collectible progress.
- Restart after checkpointed failure resumes from the checkpoint instead of level start.
- Respawn remains stable under gravity for initial frames without player input.
- Win then restart clears checkpoint state.

## Proven Source

- `scenes/hazards/SpikeHazard.tscn`
- `scripts/hazards/spike_hazard.gd`
- `scenes/progression/Checkpoint.tscn`
- `scripts/progression/checkpoint.gd`
- `main.gd`
- `test/unit/test_main_scene.gd`
