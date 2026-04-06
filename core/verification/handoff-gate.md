# Handoff Gate

Generated projects must use a hard verification gate before human playback or handoff.

## Required Commands

- `make smoke` checks that the project starts cleanly in headless mode.
- `make test` runs the automated test suite.
- `make verify` is the required handoff gate and must run both smoke and tests together.

## Rules

- Blocked verification is not verified.
- Debug instrumentation follows the same gate as production changes.
- If verification fails, fix it before handing the build to a human.
- If verification cannot complete, state clearly that the build is not ready for user execution.

## Ready For Handoff Means

A build is ready for handoff only when:

- parse/load succeeds
- automated tests pass
- smoke startup succeeds
- the agent can explain what was verified and what remains unverified
