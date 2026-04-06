# Skill: Movement And State Flow

Use this skill when implementing or extending the core platformer loop.

## Purpose

Keep movement logic, level-state transitions, and overlay/HUD flow predictable and reusable.

## Pattern

- Put movement and animation behavior in the player scene and script.
- Put run-state orchestration in the main scene controller.
- Use explicit enums for state transitions such as ready, playing, game over, and won.
- Keep restart and reset paths explicit rather than relying on implicit scene reloads.

## Proven Signals And Behaviors

- The main scene starts in a ready state with an overlay.
- Start input hides the overlay and activates physics.
- Win and lose both disable player control and show the correct overlay copy.
- Restart either resumes from checkpoint or starts a fresh run based on current state.

## Verification

- Smoke test scene startup.
- Test start, win, lose, and restart transitions with automated coverage.
