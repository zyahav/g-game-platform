# Current Status

## Stage

Platform build, Batch 5 complete

## Implementation Tracker

- Current batch: Batch 5
- Current step: 49
- Last completed step: 49
- Gate status: Gate E ready for review

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
- A generator fix that strips stale source-resource UIDs from generated scenes so Godot loads the generated project cleanly by text paths without UID warnings
- A second clean runtime verification sample at `apps/platformer-generated-clean`
- A CI-facing `make ci-verify` target for both the platform and generated projects
- Generated project CI now runs `make ci-verify` directly instead of shell-wrapping verification
- Generated project cold-start guidance now names the exact template markers that distinguish cold-start from ongoing sessions
- A fresh Gate E verification sample at `apps/platformer-generated-gatee3`
- A verified Codex CLI end-to-end install flow from `/Users/zyahav/Documents/dev/codex-e2e-test`

## Last Known Working Direction

- Hold at Gate E for PM approval and end-to-end sign-off
- Use `apps/platformer-generated-gatee3` as the current generated-project startup-flow sample
- Keep generated projects separate from the platform repo, with `core/` and `kit/` copied in as read-only reference layers
- Preserve the current game as the proven source behind future kit changes

## Known Gaps

- The generated project samples under `apps/` are local verification outputs and are intentionally not committed
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
- `apps/platformer-generated-clean` passes:
  - `make setup-hooks`
  - `make smoke`
  - `make test`
  - `make verify`
  - `make play`
  - `make editor`
- `apps/platformer-generated-gatee2` passes:
  - `make setup-hooks`
  - `make verify`
  - `make ci-verify`
- `apps/platformer-generated-gatee2` fails `make ci-verify` as expected when `scripts/player.gd` contains `FIXME`
- Generated `AGENT.md` now explicitly distinguishes cold-start from ongoing sessions using named template markers
- `codex exec --skip-git-repo-check --full-auto` successfully generated `/Users/zyahav/Documents/dev/codex-e2e-test/student-project` from the platform repo and verified it
- Inside the Codex CLI sandbox, Godot verification needed a workspace-local `HOME`, `XDG_DATA_HOME`, and `XDG_CONFIG_HOME` to avoid macOS user-data path crashes
- The cleaned generator no longer emits stale source-resource UID warnings during generated-project startup
- The current `GUT` suite still passes with:
  - 2 test scripts
  - 16 tests
  - 72 assertions

## Resume Here

1. Review Gate E and approve or reject Batch 5
2. If approved, treat the platform repo skeleton plus extracted first kit as end-to-end verified
3. Use `apps/platformer-generated-gatee3` for any follow-up startup-flow demos
4. Decide whether to keep `scripts/ci/verify.sh` as a legacy helper or replace it later with documentation that points CI users to `make ci-verify`
5. Decide whether the generated-project `Makefile` should gain a student-facing Godot local-`HOME` helper for sandboxed Codex CLI runs
