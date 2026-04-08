# Generator Implementation Plan

**Status: Active implementation plan**
**Date: April 2026**

This document translates the approved startup and learning-layer decisions into
the concrete generator work needed in this repo.

## Summary

The generator must move from "write a project into a brand-new output folder"
to a two-phase flow that supports the approved one-folder student experience:

1. stage the platform source
2. generate the project into a temporary output
3. promote the generated project into the final root
4. delete temporary scaffolding

At the same time, generated projects must stop booting Thread 1 into `AGENT.md`
and instead include their own portable coaching layer.

## Implementation Order

1. Keep the current generator logic intact behind a reusable
   `generate_project_contents(...)` function.
2. Add generated-project coaching outputs:
   - generated `README.md` with Thread 1 → `learning/coach.md`
   - generated `learning/` layer
   - generated `state/student.md`
   - generated-project-specific `learning/coach.md`
   - generated-project-specific `learning/kaya/Onboarding.md`
3. Update the generated project state templates so they reflect the new startup
   contract.
4. Add stage → promote → cleanup orchestration around the existing generator.
5. Add failure cleanup so retries always start from a clean root.
6. Verify both:
   - standard generation into a new destination
   - destructive in-place transformation of a platform checkout root

## Generator Behavior Changes

### Staging and Promotion

- Use `._platform_source/` under the chosen output root as the staged platform snapshot.
- Use `._generated/` under the chosen output root as the temporary generated project.
- Promote the full contents of `._generated/` into the final root with no curation step.
- Delete both temp folders after successful promotion.
- On failure, delete temp folders and leave the final root empty.

### Safety Guard

- Destructive transformation of an already non-empty output root must require an
  explicit opt-in flag.
- The initial implementation uses `--in-place-root` for this guard.
- Without that flag, existing non-empty output roots remain an error.

### Generated Project Coaching Contract

- Copy unchanged from platform:
  - `learning/kaya/Mission.md`
  - `learning/kaya/Soul.md`
  - `learning/kaya/Boundaries.md`
  - `learning/kaya/Playbook.md`
  - `learning/kaya/Lessons.md`
- Generate project-specific:
  - `learning/coach.md`
  - `learning/kaya/Onboarding.md`
  - `README.md`
  - `state/student.md`
- Copy the chosen kit lesson spec into `learning/lessons/` when it exists.

### Generated Project Entry Contract

- Human-facing `README.md` tells the student how to start from this folder.
- Agent-facing `README.md` tells Thread 1 to read `learning/coach.md`.
- `AGENT.md` remains the Dev thread contract only.

## Verification Plan

### Non-GUI Checks

- Generate a fresh project into a new temp root and verify:
  - generated root contains the project, not temp scaffolding
  - generated `README.md` points Thread 1 to `learning/coach.md`
  - generated `learning/` exists with the expected files
  - generated `state/student.md` exists
  - `make doctor` passes
  - `make verify` passes
  - `make ci-verify` passes

### In-Place Root Transformation

- Create a disposable platform-root copy.
- Run the generator against that root with `--in-place-root`.
- Verify:
  - final root becomes the generated project
  - no `._platform_source/` or `._generated/` remain
  - Thread 1 now boots from the generated-project `README.md`

### Failure Path

- Force a generator failure in a disposable root.
- Verify the root is left empty and retryable.

### Remaining Manual Checks

- `make play`
- `make editor`

These still require a real local/UI-capable check after the non-GUI path is green.

## Out of Scope

- Real student pilot results
- Commit/push decisions
- Automatic upgrade flow for previously generated student projects
