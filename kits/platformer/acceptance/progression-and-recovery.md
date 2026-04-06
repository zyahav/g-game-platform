# Progression And Recovery Acceptance

## Feature/System Name

Hazards, checkpoints, and safe respawn

## Pass/Fail Criteria

- Pass if hazards trigger failure, checkpoints save progress, and respawn after failure resumes safely from the last valid checkpoint.
- Fail if hazard contact is ignored, checkpoint progress is lost, or respawn creates an immediate death loop or returns to the wrong place.

## Manual Verification Scenario

1. Start the run and collect progress before the checkpoint.
2. Touch the checkpoint and confirm it activates visually.
3. Move into a hazard or fail the course.
4. Restart and confirm the player resumes from the checkpoint with the saved progress state.
5. Win the course and restart again to confirm a fresh run begins.

## Expected Automated Coverage

- Hazard-triggered failure for the player.
- Checkpoint activation saves score and collected-item state.
- Restart after checkpoint restores saved progress.
- Respawn stays safe for initial frames without input.
- Win then restart clears checkpoint state.
