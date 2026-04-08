# Current Status

## Stage

Architecture frozen. Generator/startup rollout and publish flow implemented. Production snapshot pushed. First live web deploy verified.

## Implementation Tracker

- Current phase: Pilot readiness after first live deploy
- Current focus: tighten generated export readiness and student meeting flow
- Last completed milestone: first live website deploy for `pilot-test-1`
- Ready for: student meeting + follow-up refinement

## Summary

The repo currently has:

- A proven `platformer` kit extracted from the working game
- Generated-project environment self-healing through `scripts/project_tasks.py`
- Approved architecture and decision records for startup flow and generated-project learning behavior
- A platform entry `README.md` that boots Thread 1 into `learning/coach.md`
- A platform `learning/` layer with Kaya identity, onboarding, lessons, and the platformer lesson spec
- A new execution-facing implementation plan in `docs/IMPLEMENTATION-PLAN-GENERATOR.md`
- A refactored `scripts/generate_project.py` that now:
  - supports stage → promote → cleanup generation
  - supports destructive in-place transformation with `--in-place-root`
  - writes generated-project `README.md` for Thread 1 → `learning/coach.md`
  - seeds a generated-project coaching layer under `learning/`
  - seeds `state/student.md`
  - keeps generated-project `AGENT.md` as the Dev-only contract
- An implemented generated-project publish flow that now:
  - adds generated `publish.toml`
  - adds publish-aware generated `Makefile` targets
  - adds generated `docs/PUBLISHING.md`
  - adds publish commands to `templates/generated-project/project_tasks.py`
  - keeps publish requests in the Coach → Dev handoff through `learning/kaya/Playbook.md`
- Two approved publish specs:
  - `docs/IMPLEMENTATION-SPEC-PUBLISH.md`
  - `docs/IMPLEMENTATION-SPEC-VM-HOSTING.md`
- External VM/operator preparation for first publish:
  - Hetzner VM baseline verified
  - `/srv/git` and `/var/www/projects` prepared
  - `allow-one-repo-push` helper installed on the VM
  - split hostname plan prepared for web vs Git/SSH hosting
- The production snapshot is pushed to GitHub and the first live student site is now verified at:
  - `https://games.zurot.org/zyahav/pilot-test-1/`

## Last Known Working Direction

- Treat `docs/ARCHITECTURE.md` and `docs/DECISION-STARTUP-AND-LEARNING-LAYER.md` as frozen source-of-truth docs unless implementation or pilot exposes a contradiction
- Use `docs/IMPLEMENTATION-PLAN-GENERATOR.md` as the execution plan for this rollout
- Use the new generated-project `README.md` + `learning/coach.md` contract for Thread 1 in generated projects
- Keep `core/` and `kit/` copied into generated projects as read-only reference layers
- Treat `docs/IMPLEMENTATION-SPEC-PUBLISH.md` as the generated-project publish source of truth
- Treat `docs/IMPLEMENTATION-SPEC-VM-HOSTING.md` as the operator/VM reference for live publish setup

## Known Gaps

- Full automatic conversational TTS is still not solved; tonight's safe choice is manual short Kaya TTS plus the cleaned event-only notify hook
- Publish failure output still exposes fairly raw Git stderr and should be cleaned up in a later refinement pass
- Older generated projects created before the publish rollout may still be missing `export_presets.cfg`

## Verified Automation

- `python3 -m py_compile scripts/generate_project.py templates/generated-project/project_tasks.py` passes
- Fresh generated sample at `/tmp/ggen-fresh.u0DRg1/project` passed:
  - `make doctor`
  - `make verify`
  - `make ci-verify`
- Fresh generated sample now contains:
  - generated-project `README.md` with Thread 1 → `learning/coach.md`
  - generated-project `learning/` layer
  - generated `state/student.md`
- In-place bootstrap transformation at `/tmp/ggen-inplace.ZeM0zV/root` passed:
  - `python3 scripts/generate_project.py --kit platformer --output ... --in-place-root`
  - temp folders removed after promotion
  - root now boots Kaya from generated-project `README.md`
  - `make doctor` passes
- Forced failure path at `/tmp/ggen-failsrc.qvFtXz/root` left the root empty after cleanup, confirming clean-retry behavior
- The current repo `GUT` suite passes with:
  - 2 test scripts
  - 16 tests
  - 72 assertions
- A fresh generated project also now passes with:
  - `python3 scripts/project_tasks.py doctor`
  - `python3 scripts/project_tasks.py verify`
- The generated-project task runner is now Python 3.9-compatible
- The checkpoint respawn / nearby-coin flake has been fixed in both the live repo and the platform kit templates
- The publish implementation now passes local verification:
  - `python3 -m py_compile scripts/generate_project.py`
  - `python3 -m py_compile templates/generated-project/project_tasks.py`
  - `make verify`
- A fresh generated publish sample now contains:
  - `publish.toml`
  - `docs/PUBLISHING.md`
  - publish targets in generated `Makefile`
- Fresh generated publish behavior is verified to:
  - fail clearly on empty `publish.toml` required fields
  - report publish readiness clearly with `make publish-status`
- Hetzner VM baseline step is verified:
  - `nginx` and `git` present
  - `/srv/git` and `/var/www/projects` created
  - `/usr/local/bin/allow-one-repo-push` installed and executable
- Local machine web export templates are now verified installed for Godot 4.6.1
- First live deployment is verified:
  - `pilot-test-1` exported successfully after adding the Web preset file
  - deploy repo updated on `git.games.zurot.org`
  - public URL serves the real Godot export HTML

## Resume Here

1. Use `docs/TTS-INTEGRATION-NOTES.md` as the TTS source of truth for tonight
2. Use the live `pilot-test-1` website for the student meeting if needed
3. Regenerate older projects from the updated platform when you want the full native publish flow
4. Capture only concrete failures or confusion points from live use
