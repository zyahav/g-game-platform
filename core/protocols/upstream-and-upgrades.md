# Upstream And Upgrade Protocols

## System Upgrade Protocol

Reusable platform changes must follow a discussion-first workflow.

1. Observe the problem or gap.
2. Discuss the design and extract the reusable lesson.
3. Agree on the operating model or invariant.
4. Only then update platform docs, rules, skills, or workflow files.

Do not upgrade the system from the first implementation pass.

## Generated Project Upgrade Policy

Generated projects are snapshots, not auto-synced mirrors of the platform.

- Record the `core_version` and `kit_version` in `project.kit.json`.
- Treat future platform upgrades as deliberate, opt-in changes.
- Compare newer core or kit versions before applying them to an existing student project.

## Upstream Contribution Guidance

If a change is reusable and not project-specific:

- extract it into a core or kit improvement
- review it separately from student-game code
- avoid mixing platform changes with project-specific gameplay work
