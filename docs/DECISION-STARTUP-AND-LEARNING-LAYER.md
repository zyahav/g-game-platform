# Decision Record — Startup Flow and Generated Project Learning Layer

**Status: APPROVED**
**Date: April 2026**
**Authors: PM + Dev**

This document is the approved decision record for two architectural decisions.
Both decisions were reached through a structured review process.
The full decision-making history is in the git log.
Implementation tasks are derived from these decisions.

---

## Decision 1 — Startup Flow: Staging, Promotion, and Cleanup

### Product Goal
One folder = one game project. Forever.

The student creates an empty folder, pastes the platform GitHub URL, and ends up with
one clean portable game repo in that folder. They push it to their own GitHub and pull
it on any machine to continue exactly where they left off.

### The Approved Flow

Use a two-phase bootstrap with stage → promote → cleanup:

**Phase 1 — Before generation:**
The platform source is at root. Thread 1 reads the platform `README.md` and becomes Kaya.
Kaya onboards the student and instructs the Dev to generate the game.

**Phase 2 — After generation:**
The stage → promote → cleanup flow runs. After completion, the root contains only
the clean generated project. Thread 1 reads the generated project `README.md` and
becomes Kaya again, resuming from `state/student.md`.

Both phases use the same Thread 1 contract. The bootstrap is unbroken across the transition.

### Approved Answers

1. Temporary platform source lives in `._platform_source/` inside the student's root folder.
2. Temporary generated project lives in `._generated/` inside the student's root folder.
3. Promote everything from `._generated/` wholesale into root. No curation during promotion.
4. Both `._platform_source/` and `._generated/` are physically deleted after successful promotion.
5. On failure: report clearly, delete partial temp folders, leave the student's root empty for a clean retry.
6. The final root IS the student's chosen folder. No child folders.
7. Two-phase bootstrap contract: platform `README.md` governs Phase 1. Generated project `README.md`
   governs Phase 2. Both point Thread 1 to `learning/coach.md`. This is a contract, not an
   assumption about Codex runtime behavior.

### What Is NOT Being Decided Here

- Exact code changes to `generate_project.py`
- Agent commands that trigger the flow
- Whether `make doctor` runs before or after promotion

---

## Decision 2 — Generated Project Learning Layer

### Product Goal
Every generated project must be fully portable and self-contained.

A student must be able to push to their own GitHub, pull on a new machine, open a new
Codex thread, and have Kaya know who they are, where they left off, and what comes next.

### Approved Answers

1. **Generate-and-customize model** — not a wholesale copy of the platform learning layer.
   - Copy unchanged: `Mission.md`, `Soul.md`, `Boundaries.md`, `Playbook.md`, `Lessons.md`
   - Generate project-specific: `Onboarding.md` (resume this game, not clone and generate)
   - Generate project-specific: `coach.md` loader (points to generated project's learning layer)
   - Reason: platform `Onboarding.md` contains generation instructions that would be a bug if copied into an existing project.

2. Learning layer lives at `learning/` in the generated project root. Same structure as the platform.

3. Learning files are static after generation. Only `state/student.md` evolves during sessions.

4. Students keep the Kaya version they were generated with. No automatic updates. Opt-in upgrades only.

5. Generated project `README.md` is written by the generator with two sections:
   one human paragraph for the student, and one agent instruction pointing Thread 1 to `learning/coach.md`.
   This is consistent with the Phase 2 bootstrap contract from Decision 1.

6. `state/student.md` initialized by generator as an empty template. Kaya fills in name, sessions,
   and notes during the first session. (Option C — both generator and Kaya own it.)

### What Is NOT Being Decided Here

- Exact content of each Kaya file (handled separately)
- How the student edits Kaya files (progressive exposure model)
- Whether the learning layer is visible or hidden initially

---

## Implementation Tasks (for Dev)

These tasks follow directly from the approved decisions above.

1. Update `generate_project.py` to support the stage → promote → cleanup flow
2. Add the `learning/` layer generation to the generator (generate-and-customize model)
3. Write the generated-project-specific `Onboarding.md` template
4. Write the generated-project-specific `coach.md` loader template
5. Add `state/student.md` empty template to the generator output
6. Update the generated project `README.md` template to point Thread 1 to `learning/coach.md`
7. Verify `make doctor` runs cleanly after promotion in the generated project
