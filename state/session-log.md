# Session Log

## 2026-04-03

- Fixed player scene/script mismatches and switched to platformer movement
- Added jump physics, run/jump animations, and smoother camera behavior
- Rebuilt the main level into a staircase prototype with win/lose flow
- Added generated level art from existing source images
- Added jump, start, win, and lose sound effects
- Added strict asset structure for sound effects and collectibles
- Copied in `coin4.png` and coin pickup sound
- Added reusable coin scene, score HUD, and coin collection logic
- Added project specs and handoff/state documentation
- Imported reusable `game-agent` package into `packages/game-agent`
- Added `SESSION_START.md` and root verification checklist to make new sessions resume from root state
- Imported `FreePlatformerNA` into structured environment folders
- Rebuilt the main scene to use layered background art, moving clouds, decorative trees, and a collect-all-coins objective
- Added `tools/godot-agent-tooling-registry.md` to track external Godot dev tools, fit, status, and trial order
- Initialized local Git in the project
- Added a `Makefile` with `check-env`, `godot-smoke`, `godot-import`, and Forge smoke-test targets
- Confirmed `make godot-smoke` starts the project headlessly and exits successfully
- Smoke-tested `Godot Forge` via `make forge-help`
- Confirmed GitHub CLI auth on this machine and created the private repo `https://github.com/zyahav/farm-game`
- Added `make verify` and made `make play` depend on that preflight gate
- Installed `GUT` 9.6.0 under `addons/gut`
- Added `.gutconfig.json` and the first automated tests under `test/unit/`
- Wired `make gut-test` into `make verify`
- Confirmed the first `GUT` suite passes: 3 tests, 15 assertions
- Expanded `GUT` coverage for start/play state, coin score updates, win gating, and fall-to-game-over flow
- Current `GUT` suite now passes: 7 tests, 33 assertions
- Expanded `GUT` coverage further for restart behavior, goal filtering, and win overlay text
- Current `GUT` suite now passes: 10 tests, 45 assertions
- Added reusable spike hazards and wired hazard-triggered game over into the main scene
- Expanded `GUT` coverage for hazard-triggered lose flow
- Current `GUT` suite now passes: 12 tests, 49 assertions
- Added reusable checkpoints that save coin/score progress and restore it after game over
- Expanded `GUT` coverage for checkpoint activation, checkpoint restore, and fresh restart after win
- Current `GUT` suite now passes: 15 tests, 63 assertions
- Added gameplay invariants documenting that checkpoint respawn must restore a safe playable state
- Implemented validated safe checkpoint respawn instead of restoring raw checkpoint coordinates
- Added automated checkpoint death-loop prevention coverage that waits under gravity after respawn
- Confirmed `make verify` now passes with the safe-respawn checkpoint flow: 16 tests, 68 assertions
- Fixed `make godot-editor` so it opens the editor UI instead of running the game scene
- Fixed the lose overlay so spike deaths and fall deaths show different messages
- Expanded automated coverage for death messaging and confirmed `make verify` now passes with 16 tests and 70 assertions
- Added a repo-level discussion-first protocol for changing system rules, reusable skills, and workflow policy

## 2026-04-06

- Added a repo-level hard handoff gate: no human playback after runtime changes unless parse/load, tests, and smoke startup are green
- Explicitly documented that blocked verification is not verified
- Explicitly documented that debug instrumentation follows the same handoff gate as production changes
- Started Batch 1 of the platform build on branch `codex/platform-v4-build`
- Added the root platform `AGENT.md` with setup/install mode instructions
- Added the platform `core/` contract and initial docs under `core/agent-rules/`, `core/workflow/`, `core/verification/`, and `core/protocols/`
- Added the top-level platform skeleton directories: `kits/`, `templates/`, `docs/`, and `.github/workflows/`
- Added `scripts/hooks/pre-commit.sh` and `scripts/ci/verify.sh`
- Extended the root `Makefile` with `make test`, `make smoke`, `make editor`, and `make setup-hooks`
- Added `.github/workflows/verify.yml`
- Verified the new hook script, hook installation, YAML validity, `make test`, and `make smoke`
- Confirmed Gate A is ready for review, with one extra non-gate note: direct local `./scripts/ci/verify.sh` currently crashes inside Godot's headless logging path in this Codex sandbox even though `make test` and `make smoke` pass when run independently

## Handoff Note

Batch 1 is complete and waiting at Gate A. Do not start Batch 2 until approval is given.
