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
- Add safe checkpoint respawn invariants and automated death-loop prevention coverage
- Add a formal discussion-first protocol for system/rule/skill upgrades
- Complete Batch 1 platform skeleton work:
  - root `AGENT.md`
  - `core/` contract and docs
  - platform folder skeleton
  - hook and CI scripts
  - `Makefile` platform aliases
  - GitHub Actions verification workflow
- Verify Gate A requirements except for the final clean-commit checkpoint
- Complete Batch 2 first-kit extraction work:
  - `kits/platformer/` manifest
  - kit overview and agent rules
  - distilled feature specs
  - distilled skills
  - multi-file acceptance docs
  - runnable template snapshot
  - authoring reference notes
- Complete Batch 3 generation work:
  - generator script
  - generated root files
  - copied `core/`
  - copied distilled `kit/`
  - seeded state/specs/tools/docs/tests
  - generated project CI and hooks
- Complete Batch 4 runtime verification work:
  - `make play`
  - `make smoke`
  - `make test`
  - `make verify`
  - `make setup-hooks`
  - `make editor`
  - generator cleanup for stale UID warnings

## In Progress

- Hold at Gate D for PM approval before Batch 5

## Next

- Verify cold-start and ongoing-session `AGENT.md` behavior on the generated project
- Check that the generated project's pre-commit hook blocks `FIXME` in `.gd` files
- Check that generated-project CI passes clean and fails on intentional `FIXME`
- Revisit the direct local `scripts/ci/verify.sh` crash if it still reproduces once Batch 2 begins

## Blocked

- Web export depends on export template installation succeeding in Godot
