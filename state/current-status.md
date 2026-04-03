# Current Status

## Stage

Prototype development

## Summary

The game currently has:

- A playable staircase platformer level
- Layered environment art using the `FreePlatformerNA` pack
- Player movement and jumping
- Start, win, and lose states
- HUD with score and coin count
- Reusable coin scene and coin collection
- Basic audio feedback
- Integrated reusable framework package under `packages/game-agent/`
- A repo-native tooling registry under `tools/`
- A `Makefile` command surface for repeatable Godot and tooling commands
- A private GitHub repo connected at `origin`
- A `make verify` preflight gate before human playback
- A working `GUT` test setup wired into `make verify`

## Last Known Working Direction

- Continue improving structure and verification workflow
- Evaluate and adopt external Godot dev tools gradually through the tooling registry
- Use `Makefile` targets as the default local command entry point
- Treat `make verify` as the minimum gate before asking the user to play a change
- Continue polishing the new environment-driven level presentation in steps
- Use `SESSION_START.md` and root `state/` files as the primary session handoff path
- Set up web export once Godot export templates are installed
- Reopen and test recent HUD / coin / sound changes in Godot

## Known Gaps

- Recent coin and HUD changes were not run in Godot from this session
- Recent `FreePlatformerNA` environment upgrade was not run in Godot from this session
- Web export templates are still not fully installed
- Automated coverage is still small even though `GUT` is now installed and running
- External tooling is partially adopted: `GUT` is verified, `Godot Forge` is only smoke-tested so far
- `Godot Forge` is only smoke-tested so far, not deeply exercised against project checks yet
- `make verify` is now stronger, but still needs broader test coverage to catch more gameplay regressions
 
## Verified Automation

- `make verify` now runs:
  - asset import
  - `GUT` tests
  - headless Godot startup smoke check

The current `GUT` suite passes with:

- 2 test scripts
- 7 tests
- 33 assertions

## Resume Here

1. Run `make verify` after meaningful gameplay changes before asking for human playback
2. Open the project in Godot
3. Verify the new background layers, cloud motion, objective HUD, and collect-all-coins finish flow
4. Expand `GUT` coverage to restart flow and any new hazards/checkpoints
5. Continue tooling trials from `tools/godot-agent-tooling-registry.md`, starting with a deeper `Godot Forge` validation
6. Continue polishing the level and then resume web export setup
