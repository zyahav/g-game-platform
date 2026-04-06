# Generated Project Agent Rules

These rules define how the agent must behave inside generated student projects.

## Core Behavior

- Be spec-driven. New features should be anchored in project specs before or while they are implemented.
- Treat `specs/`, `state/`, and `tools/` as the live working system for the generated project.
- Treat `core/` and `kit/` as read-only reference layers unless the user explicitly requests a deliberate system change.
- Prefer repeatable project commands from `Makefile` over one-off manual flows.
- Preserve the boundary between platform rules and project-specific work.

## Session Startup

- On cold start, read the generated project's `project.kit.json`, then the copied `core/` and `kit/` docs, then initialize the live working files.
- On ongoing sessions, read the generated project's state and specs first, then consult `core/` and `kit/` only as reference when needed.

## Safety And Verification

- No human handoff is allowed until the changed build is green again.
- Runtime-affecting changes include gameplay code, scene edits, configuration changes, debug instrumentation, and temporary logging.
- The user validates behavior, not build stability.

## System Change Discipline

- If the work changes reusable process, rules, workflow, or skills, follow the discussion-first protocol before editing the system.
- Do not silently upgrade the system from a single bug fix.
