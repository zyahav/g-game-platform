# Current Status

## Stage

Platform build, Batch 3 complete

## Implementation Tracker

- Current batch: Batch 3
- Current step: 35
- Last completed step: 34
- Gate status: Gate C ready for review

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
- A project generator at `scripts/generate_project.py`
- A generated student project sample at `apps/platformer-generated` for local verification only
- Generated projects now receive copied `core/`, copied distilled `kit/`, seeded docs/state/specs/tests, and a separate Git repo

## Last Known Working Direction

- Hold at Gate C for PM approval before starting Batch 4 runtime verification
- Use `scripts/generate_project.py` as the current generation flow
- Keep generated projects separate from the platform repo, with `core/` and `kit/` copied in as read-only reference layers
- Preserve the current game as the proven source behind future kit changes

## Known Gaps

- Batch 4 end-to-end runtime verification on the generated project has not started yet
- The generated project sample under `apps/` is local verification output and is intentionally not committed
- Direct local invocation of `scripts/ci/verify.sh` currently crashes inside Godot's headless logging path in this Codex sandbox even though `make test` and `make smoke` both pass on their own
- Web export templates are still not fully installed
- Automated coverage is still small even though `GUT` is installed and running
 
## Verified Automation

- `make test` passes through the new platform-standard alias
- `make smoke` passes through the new platform-standard alias
- `make setup-hooks` installs the new `scripts/hooks/pre-commit.sh` symlink successfully
- `kits/platformer/kit.manifest.json` validates as JSON
- `kits/platformer/templates/` smoke-tests successfully with Godot headless startup
- `apps/platformer-generated/project.kit.json` validates as JSON
- `apps/platformer-generated/.github/workflows/verify.yml` parses as valid YAML
- `apps/platformer-generated/Makefile` contains all six required targets
- `apps/platformer-generated/kit/` excludes `templates/` and `reference/`
- `apps/platformer-generated/make setup-hooks` succeeds inside the generated project's own Git repo
- The current `GUT` suite still passes with:
  - 2 test scripts
  - 16 tests
  - 72 assertions

## Resume Here

1. Review Gate C and approve or reject Batch 3
2. If approved, start Batch 4 and verify the generated project's actual runtime commands end to end
3. Use `apps/platformer-generated` as the current local verification target for Batch 4
4. Revisit the direct `scripts/ci/verify.sh` crash before later CI-focused gates if it persists
