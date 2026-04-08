# Current Status

## Stage

Architecture frozen. Generator/startup rollout implemented and verified locally. Ready to push the first production snapshot.

## Implementation Tracker

- Current phase: Post-decision generator rollout
- Current focus: production push readiness
- Last completed milestone: stable generated-project rollout plus live student-flow rehearsal
- Ready for: commit + push + student use

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

## Last Known Working Direction

- Treat `docs/ARCHITECTURE.md` and `docs/DECISION-STARTUP-AND-LEARNING-LAYER.md` as frozen source-of-truth docs unless implementation or pilot exposes a contradiction
- Use `docs/IMPLEMENTATION-PLAN-GENERATOR.md` as the execution plan for this rollout
- Use the new generated-project `README.md` + `learning/coach.md` contract for Thread 1 in generated projects
- Keep `core/` and `kit/` copied into generated projects as read-only reference layers

## Known Gaps

- Full automatic conversational TTS is still not solved; tonight's safe choice is manual short Kaya TTS plus the cleaned event-only notify hook
- Web export templates are still not fully installed
- The repo still needs its first production commit/push from this machine

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

## Resume Here

1. Use `docs/TTS-INTEGRATION-NOTES.md` as the TTS source of truth for tonight
2. Commit and push this production snapshot
3. Have the student start from the generated-project bootstrap flow
4. Capture only concrete failures or confusion points from live use
5. Make a small follow-up refinement pass if needed
