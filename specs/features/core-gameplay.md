# Core Gameplay Spec

## Goal

Provide a playable vertical staircase platformer prototype.

## Requirements

- The player can move left and right.
- The player can jump between platforms.
- Falling below the level causes game over.
- Reaching the goal area causes a win state.
- The run can be restarted after winning or losing.

## Acceptance Criteria

- The player can complete the course using current movement values.
- Falling shows a lose overlay and stops gameplay.
- Reaching the goal shows a win overlay and stops gameplay.
- Restart returns the player to spawn and re-enables gameplay.

## Notes

- Jump spacing should be based on actual movement values, not visual guesswork.
