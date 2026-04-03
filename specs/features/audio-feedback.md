# Audio Feedback Spec

## Goal

Use lightweight sound effects to give feedback for core game actions.

## Requirements

- Jump plays a jump sound.
- Starting a run plays a start sound.
- Winning plays a win sound.
- Losing plays a lose sound.
- Collecting a coin plays a coin sound.

## Acceptance Criteria

- Each sound triggers at the correct event.
- Sounds do not continue incorrectly across restart.
- Volumes are reasonable relative to each other.

## Notes

- Keep audio assets organized under `assets/audio/sfx/`.
