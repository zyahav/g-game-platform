# Current Status

## Stage

Platform build, Batch 2 complete

## Implementation Tracker

- Current batch: Batch 2
- Current step: 20
- Last completed step: 19
- Gate status: Gate B ready for review

## Summary

The repo currently has:

- A playable staircase platformer level
- Layered environment art using the `FreePlatformerNA` pack
- Player movement and jumping
- Start, win, and lose states
- HUD with score and coin count
- Reusable coin scene and coin collection
- Reusable spike hazard scene and hazard-triggered lose flow
- Reusable checkpoint scene with saved progress and validated safe respawn on restart after game over
- Basic audio feedback
- Integrated reusable framework package under `packages/game-agent/`
- A repo-native tooling registry under `tools/`
- A `Makefile` command surface for repeatable Godot and tooling commands
- A private GitHub repo connected at `origin`
- A `make verify` preflight gate before human playback
- A working `GUT` test setup wired into `make verify`
- Documented gameplay invariants for safe respawn behavior
- A discussion-first protocol for changing repo rules, skills, and workflow
- A hard handoff gate that requires green verification before user execution
- A root platform `AGENT.md` for setup/install mode
- A reduced platform `core/` contract with agent rules, workflow, verification, and protocols
- Platform skeleton folders for `kits/`, `templates/`, `docs/`, and `.github/workflows/`
- Platform hook and CI scripts under `scripts/hooks/` and `scripts/ci/`
- Platform-standard `Makefile` aliases: `make test`, `make smoke`, `make editor`, and `make setup-hooks`
- A first extracted `platformer` kit under `kits/platformer/`
- Distilled platformer kit specs, skills, acceptance docs, templates, and reference notes based on the working game
- A runnable kit template snapshot that smoke-tests successfully in isolation

## Last Known Working Direction

- Hold at Gate B for PM approval before starting project generation
- Use the extracted `platformer` kit as the source for generated project files in Batch 3
- Keep generation aligned with the copied `core/` contract and the distilled kit contract
- Preserve the current game as the proven source behind future kit changes

## Known Gaps

- Project generation has not started yet
- The platform repo still contains the current game because the first generated-project flow has not been built yet
- Direct local invocation of `scripts/ci/verify.sh` currently crashes inside Godot's headless logging path in this Codex sandbox even though `make test` and `make smoke` both pass on their own
- Web export templates are still not fully installed
- Automated coverage is still small even though `GUT` is installed and running
 
## Verified Automation

- `make test` passes through the new platform-standard alias
- `make smoke` passes through the new platform-standard alias
- `make setup-hooks` installs the new `scripts/hooks/pre-commit.sh` symlink successfully
- `kits/platformer/kit.manifest.json` validates as JSON
- `kits/platformer/templates/` smoke-tests successfully with Godot headless startup
- The current `GUT` suite still passes with:
  - 2 test scripts
  - 16 tests
  - 72 assertions

## Resume Here

1. Review Gate B and approve or reject Batch 2
2. If approved, start Batch 3 and build project generation from the extracted `platformer` kit
3. Keep generated-project output aligned with the agreed root contract and cold-start/ongoing-session rules
4. Revisit the direct `scripts/ci/verify.sh` crash before later CI-focused gates if it persists
