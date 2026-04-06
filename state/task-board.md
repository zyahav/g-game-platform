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

## In Progress

- Hold at Gate A for PM approval before Batch 2
- Preserve the current game as the source material for the first extracted kit

## Next

- Extract the first kit from the proven working game
- Author the first kit manifest, kit rules, seeded specs, acceptance, templates, and reference material
- Build the generation flow and generated-project contract
- Revisit the direct local `scripts/ci/verify.sh` crash if it still reproduces once Batch 2 begins

## Blocked

- Web export depends on export template installation succeeding in Godot
