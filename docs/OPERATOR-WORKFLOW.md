# Operator Workflow

This document defines how live tutoring sessions are run operationally.

## Core Rule

The tutor/operator talks to Codex as the single coordinator.

Codex owns:

- relaying work to Platform Dev and VM Dev
- sequencing the next step
- tracking current state
- reducing tutor/operator overhead during live sessions

The operator should not need to manage multiple technical roles in parallel unless there is a deliberate exception.

## Role Model

### Operator / Tutor

Owns:

- the human session
- the student relationship
- physical computer handoff and Zoom/chat logistics
- deciding when to start the next live step

Does not need to own:

- detailed Dev prompts
- VM provisioning commands
- package/path bookkeeping
- cross-thread state reconstruction

### Codex Coordinator

Owns:

- translating operator intent into precise Dev / VM instructions
- checking whether a requested step is already done
- deciding the safest next single step
- verifying artifacts and paths before asking the operator to continue
- keeping the flow calm and sequential

### Platform Dev

Owns:

- platform repo behavior
- generated-project behavior
- Coach / Dev flow contracts
- verification of local project behavior

### VM Dev

Owns:

- slot provisioning
- package generation
- package zip generation
- absolute-path artifact reporting

## Default Session Pattern

1. Operator asks Codex what to do next.
2. Codex checks state and chooses the next single step.
3. If VM work is needed, Codex issues the VM instruction or runs the verified VM protocol.
4. If platform work is needed, Codex issues the Dev instruction or applies the verified repo workflow.
5. Codex verifies outputs before asking the operator to continue.
6. Operator only performs the human-facing step that is actually needed now.

## VM Slot Workflow

Default operator intent:

`create slot <handle>`

Meaning:

- `project_name = game`
- local-only package
- no upload
- no commit
- package folder created
- zip archive created
- full absolute paths returned

Codex should prefer handling this through the durable VM protocol rather than making the operator manually orchestrate packaging steps.

## Live Student Principle

During a real session, prefer one-step-at-a-time guidance.

Do not jump ahead.
Do not ask the operator to prepare multiple technical steps at once if Codex can resolve sequencing first.

## Source Of Truth

- Platform workflow state: `state/current-status.md`
- VM/operator packaging details: `docs/IMPLEMENTATION-SPEC-VM-HOSTING.md`
- CLI rehearsal details: `docs/CLI-TEST-RUNBOOK.md`
