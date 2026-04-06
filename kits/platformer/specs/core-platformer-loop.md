# Core Platformer Loop

## Goal

Provide a complete side-view platformer loop that can be played immediately after scaffolding.

## Requirements

- The player can move left and right.
- The player can jump between platforms.
- The level has a clear start point and end goal.
- Falling below the level causes a lose state.
- Reaching the goal after satisfying progression requirements causes a win state.
- The run can be restarted after win or loss.

## Acceptance Criteria

- The player can complete the starter course using current movement values.
- Falling shows a lose overlay and stops gameplay.
- Reaching the goal shows a win overlay and stops gameplay.
- Restart returns the player to a valid respawn point and re-enables gameplay.

## Proven Source

- `project.godot`
- `Main.tscn`
- `Player.tscn`
- `main.gd`
- `player.gd`
- `test/unit/test_main_scene.gd`
