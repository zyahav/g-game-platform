# Codex Game Dev Platform

This repository is the platform source for kit-based game generation.

## Setup Mode

When a student points an agent at this repository and says `install`, the agent should:

1. Read the available kit manifests under `kits/*/kit.manifest.json`.
2. Present the available kits clearly and let the student choose one.
3. Generate a new project directory from the selected kit.
4. Copy only the reduced project-facing `core/` content and the selected kit's generated-project reference content.
5. Consume the kit templates into real project files.
6. Create the generated project's own `AGENT.md`, `project.kit.json`, and working-system folders.
7. Run the generated project's environment preflight and automatic repair path before asking the student for setup help.
8. Stop working inside this platform clone once generation is complete and continue in the generated project directory.

The platform repository is the source. The generated project is the product.

## Development Mode Note

This `AGENT.md` is only for the platform repository.

Generated student projects must have their own root `AGENT.md` with:

- cold-start instructions
- ongoing-session instructions
- project-specific read order
- project-specific verification and handoff rules

Do not treat the generated project's `AGENT.md` as interchangeable with this platform file.
