# Task Board

## Done

- Create playable staircase platformer prototype
- Add start, win, and lose flow
- Add player idle, run, and jump animations
- Add generated level art from source assets
- Add jump, start, win, and lose sound effects
- Add structured folders for collectible and sound assets
- Add reusable coin scene
- Add HUD with score and coin counter
- Import reusable `game-agent` package under `packages/game-agent/`
- Add root startup and verification docs for session continuity
- Import `FreePlatformerNA` into structured environment folders
- Upgrade the level with layered background art, decorative trees, and a stronger collect-all-coins goal
- Add a live repo tooling registry under `tools/` seeded from the Godot tooling handoff
- Initialize local Git and add a `Makefile` for repeatable Godot/tooling commands
- Create and connect the private GitHub remote
- Add a `make verify` preflight gate before human playback
- Install `GUT` and wire it into `make verify`
- Add reusable spike hazards with automated coverage
- Add reusable checkpoints with saved progress and automated coverage

## In Progress

- Verify latest HUD, coin, and sound changes inside Godot
- Verify the new environment-driven scene and cloud motion inside Godot
- Set up reliable web export workflow
- Begin gradual evaluation of Godot dev tooling from `tools/godot-agent-tooling-registry.md`

## Next

- Add better review and verification routine
- Deepen the `Godot Forge` trial beyond the current smoke test
- Trial `GDScript Toolkit`
- Expand `GUT` coverage to restart flow and future hazards/checkpoints
- Add the next sophistication pass: richer level progression or another checkpoint
- Document browser export steps in-project
- Consider adding a second checkpoint or a second section of the level

## Blocked

- Web export depends on export template installation succeeding in Godot
