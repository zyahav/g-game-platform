# Godot Agent Tooling Registry

This document tracks external tools that can make the agent more capable when working on this Godot project.

These tools are similar to skills in the sense that each one adds a specific capability, but they are not the same thing:

- Codex skills are instruction bundles the agent can read and follow
- tooling in this file is installable software, plugins, MCP servers, CLIs, or frameworks we may adopt for this repo

Use this file as the source of truth for:

- what tools we know about
- what each tool is good for
- whether we tested it
- whether it fits this project
- what to try next

## Source

Initial list seeded from:

- `/Users/zyahav/Documents/GitHub/p-Narration/AudioProcessing/assets/originals/godot-dev-agent-tooling-handoff.md`

Some entries were also separately researched on April 3, 2026 during this project, especially around testing frameworks.

## Status Legend

- `Captured` = listed here, but not independently validated in this repo yet
- `Researched` = read docs / repo information, but not installed here
- `Smoke Tested` = basic startup or CLI check worked here, but deeper project validation is still pending
- `Queued` = likely a good fit and should be tried soon
- `Blocked` = cannot proceed yet because of environment, cost, or setup issues
- `Installed` = added locally, but not verified in this project yet
- `Verified` = tested and confirmed useful in this repo
- `Not Now` = valid tool, but not worth adopting at the moment
- `Rejected` = tested or reviewed and intentionally not using

## Recommended Trial Order For This Repo

1. `Godot Forge`
Reason: lightweight API-correctness protection for Godot 4 and likely the fastest value.
2. `GUT` or `GdUnit4`
Reason: we need a real test path for gameplay logic and scene flow.
3. `GDScript Toolkit`
Reason: gives linting and formatting outside the editor.
4. One MCP server
Reason: biggest power boost, but also the most setup complexity.
5. `GodotEnv`
Reason: useful later if we start juggling multiple Godot versions.

## Tool Summary

| Tool | Category | Best For | Current Status | Fit For This Repo | Next Step |
| --- | --- | --- | --- | --- | --- |
| `Codex CLI` | Agent CLI / project setup | Student install flow, generated-project bootstrap, verification from a fresh directory | `Verified` | Strong fit as the student-facing entrypoint for this platform | Document the verified install command and local `HOME` workaround for Godot verification |
| `GodotIQ` | MCP / runtime intelligence | Deep scene understanding, spatial context, code analysis | `Captured` | Promising, especially if we want richer editor/runtime visibility | Validate install path and compatibility with Codex workflow |
| `Godot MCP (Coding-Solo)` | MCP / runtime control | Launching editor, running project, debug output, scene operations | `Captured` | Strong candidate for a first general MCP server | Evaluate against GodotIQ as the first MCP trial |
| `GDAI MCP` | MCP / paid runtime control | Screenshots, input simulation, run-fix-verify loops | `Captured` | Interesting, but likely overkill before free options are tested | Leave for later unless free tools fall short |
| `Godot MCP Pro` | MCP / paid full suite | Broadest tool coverage across editor and runtime | `Captured` | Powerful, but tool count and paid setup add complexity | Revisit only if smaller MCP options are insufficient |
| `Godot MCP (tomyud)` | MCP / runtime control | Mid-sized open-source MCP with project browser | `Captured` | Viable fallback if the first MCP choice is awkward | Keep as backup |
| `Godot MCP (bradypp)` | MCP / runtime control | Lean open-source MCP with read-only mode option | `Captured` | Good safety-oriented option for analysis-first use | Keep as backup |
| `Godot Forge` | API correctness / project analysis | Catching Godot 3 to Godot 4 mistakes, scene structure checks, compiler feedback | `Smoke Tested` | Very strong fit | Add a deeper project-level Forge check after the first smoke pass |
| `GUT` | Testing framework | Simple Godot 4 GDScript tests and CLI test runs | `Verified` | Strong fit for this GDScript-heavy project | Expand test coverage and keep it inside `make verify` |
| `GdUnit4` | Testing framework | Richer scene/integration testing, fluent assertions, reports | `Researched` | Also a strong fit, especially for gameplay flow tests | Compare against `GUT` before installing |
| `GDScript Toolkit` | Linting / formatting | `gdlint` and `gdformat` from the terminal | `Queued` | Strong fit for faster local verification | Trial after the testing framework decision |
| `Godot GDScript Linter (godot-qube)` | In-engine static analysis | Complexity and style analysis from headless Godot | `Captured` | Useful, but likely second priority after toolkit + tests | Leave for later evaluation |
| `GodotEnv` | Environment management | Managing multiple Godot versions and addon installs | `Captured` | Helpful later, not urgent for one active project version | Revisit if version management becomes painful |
| `godot-mcp-docs` | Documentation MCP | Querying official Godot docs from an agent workflow | `Captured` | Nice support tool, but not the top blocker right now | Consider after core testing/runtime tools |

## Detailed Notes

### Codex CLI

**Category:** Agent CLI / project setup  
**Good for:** starting from an empty directory, pointing the agent at the platform repo, generating a student project, and running the generated verification gate.  
**Why it could help us:** this is the actual student-facing path for the platform. It lets a student begin from a clean directory and have Codex read the platform `AGENT.md`, select a kit, generate the project, and continue inside the generated repo.  
**Cautions:** in this environment, `codex exec` was unstable in `/tmp` but worked from a real directory under `/Users/zyahav/Documents/dev`. Also, Godot inside the CLI sandbox initially failed when it tried to write to the default macOS user-data path.  
**Current status:** `Verified`  
**Evidence:** on April 6, 2026, the full flow was verified from `/Users/zyahav/Documents/dev/codex-e2e-test` using `codex exec --skip-git-repo-check --full-auto`. Codex read `/Users/zyahav/farm-game/AGENT.md`, selected the `platformer` kit, generated `student-project`, switched into it, and passed the generated verification gate after retrying with a workspace-local `HOME`, `XDG_DATA_HOME`, and `XDG_CONFIG_HOME`. The platform repo remained clean during the flow.  
**Verified command shape:**

```bash
mkdir -p /Users/zyahav/Documents/dev/codex-e2e-test
cd /Users/zyahav/Documents/dev/codex-e2e-test
codex exec --skip-git-repo-check --full-auto \
  -C /Users/zyahav/Documents/dev/codex-e2e-test \
  "Read /Users/zyahav/farm-game/AGENT.md and use /Users/zyahav/farm-game as the platform repository source. Follow setup mode. Choose the platformer kit automatically. Generate the student project into ./student-project. After generation, switch to that generated project directory, run make verify, and summarize whether it passed. Do not modify the platform source repository."
```

**Godot verification workaround inside the generated project:**

```bash
mkdir -p .home
HOME="$PWD/.home" \
XDG_DATA_HOME="$PWD/.home/.local/share" \
XDG_CONFIG_HOME="$PWD/.home/.config" \
make verify
```

**Next evaluation step:** decide whether the generated-project `Makefile` should officially expose a student-friendly helper for the local-`HOME` Godot path, or whether this remains a CLI-environment note only.

### GodotIQ

**Category:** MCP server  
**Good for:** richer scene intelligence, code analysis, signal tracing, and spatial understanding. It stands out because part of its tooling can work from the filesystem even when Godot is not running.  
**Why it could help us:** our current bottleneck is weak runtime visibility. A tool like this could reduce scene-node guessing and make visual debugging less blind.  
**Cautions:** higher setup surface area than a plain test tool, and we have not validated the Codex-side integration yet.  
**Current status:** `Captured`  
**Next evaluation step:** confirm install path and whether it fits our local agent workflow cleanly.

### Godot MCP (Coding-Solo)

**Category:** MCP server  
**Good for:** launching the editor, running the project, capturing output, and doing general scene operations.  
**Why it could help us:** this looks like one of the simplest ways to give the agent actual runtime eyes without going straight to a huge paid setup.  
**Cautions:** still untested here, and MCP installation flow may need extra environment setup.  
**Current status:** `Captured`  
**Next evaluation step:** compare with `GodotIQ` and choose one first MCP candidate.

### GDAI MCP

**Category:** MCP server  
**Good for:** screenshots, input simulation, and closed-loop error fixing.  
**Why it could help us:** if it works as described, it gets closer to the “browser DevTools for Godot” feeling.  
**Cautions:** paid, untested here, and not the best first step while free options remain unexplored.  
**Current status:** `Captured`  
**Next evaluation step:** defer until we know whether the free stack is enough.

### Godot MCP Pro

**Category:** MCP server  
**Good for:** very broad coverage across scenes, physics, animation, shaders, input simulation, and testing.  
**Why it could help us:** maximum control if we decide this repo needs a serious Godot automation stack.  
**Cautions:** paid, large tool surface area, and possibly more than we need at this stage.  
**Current status:** `Captured`  
**Next evaluation step:** only revisit if smaller open-source MCP options are not enough.

### Godot MCP (tomyud)

**Category:** MCP server  
**Good for:** open-source runtime/editor control with a project browser.  
**Why it could help us:** attractive fallback if the first MCP choice does not fit.  
**Cautions:** not yet compared against the other MCP options for maintenance quality or workflow fit.  
**Current status:** `Captured`  
**Next evaluation step:** keep as backup during MCP selection.

### Godot MCP (bradypp)

**Category:** MCP server  
**Good for:** lean open-source runtime/editor control, with optional read-only mode.  
**Why it could help us:** read-only mode could make early exploration safer before we trust automated edits.  
**Cautions:** narrower feature set than some alternatives.  
**Current status:** `Captured`  
**Next evaluation step:** keep as a safety-oriented backup option.

### Godot Forge

**Category:** API correctness and project analysis  
**Good for:** catching deprecated Godot 3 patterns, checking scene/resource structure, talking to the Godot language server, and running the project for output capture.  
**Why it could help us:** this directly targets one of the biggest AI failure modes in Godot projects: using the wrong API generation or missing project-level breakage. It is likely the fastest way to improve correctness before we add heavier runtime control.  
**Cautions:** still needs installation and real verification.  
**Current status:** `Smoke Tested`  
**Evidence:** on April 3, 2026, `make forge-help` resolved via `npx` and printed the Godot Forge banner from this machine. A direct `npx -y godot-forge` run stayed alive without an immediate crash, which is consistent with an MCP server waiting for a client.  
**Next evaluation step:** perform a deeper project-level validation once we decide the exact Forge command flow we want to standardize in the `Makefile`.

### GUT

**Category:** Testing framework  
**Good for:** straightforward unit and gameplay-oriented tests in GDScript, command-line execution, and low-friction adoption.  
**Why it could help us:** this repo is primarily GDScript, and we want a simple repeatable testing path. `GUT` looks like the lower-friction option.  
**Cautions:** the current suite is still small, so passing tests should be treated as a meaningful gate but not full gameplay confidence.  
**Current status:** `Verified`  
**Evidence:** on April 3, 2026, GUT `9.6.0` was installed under `addons/gut`, `.gutconfig.json` was added, `make gut-test` passed, and `make verify` was updated to run GUT before human playback. The first suite currently covers coin behavior and main-scene instantiation.  
**Next evaluation step:** keep `GUT` as the primary first-line test framework and grow coverage around gameplay flow, restart behavior, and win/lose logic.

### GdUnit4

**Category:** Testing framework  
**Good for:** richer scene and integration tests, fluent assertions, reports, and more advanced testing features.  
**Why it could help us:** it may be better if we want to test level flow, scene logic, and gameplay behavior more deeply rather than just isolated scripts.  
**Cautions:** potentially a slightly heavier setup than `GUT`.  
**Current status:** `Researched`  
**Evidence:** official docs and repo were reviewed on April 3, 2026.  
**Next evaluation step:** compare with `GUT` and decide on one primary framework first.

### GDScript Toolkit

**Category:** Linting and formatting  
**Good for:** running `gdlint` and `gdformat` from the terminal and tightening script quality outside the editor.  
**Why it could help us:** fast local verification, consistent formatting, and a way for the agent to lint its own GDScript changes.  
**Cautions:** external Python dependency and not yet installed here.  
**Current status:** `Queued`  
**Next evaluation step:** trial after we choose the initial testing framework.

### Godot GDScript Linter (godot-qube)

**Category:** In-engine static analysis  
**Good for:** complexity/style analysis and report generation through headless Godot.  
**Why it could help us:** useful if we want stricter project-level quality analysis later.  
**Cautions:** overlaps somewhat with the toolkit and is lower priority than having any test framework at all.  
**Current status:** `Captured`  
**Next evaluation step:** revisit after basic linting and testing are in place.

### GodotEnv

**Category:** Environment and version management  
**Good for:** installing and switching Godot versions and managing addon installation.  
**Why it could help us:** valuable if this package becomes reusable across multiple projects or we start testing against multiple Godot versions.  
**Cautions:** introduces .NET setup and is not necessary for a single active local version right now.  
**Current status:** `Captured`  
**Next evaluation step:** postpone until version management becomes an actual pain point.

### godot-mcp-docs

**Category:** Documentation access  
**Good for:** giving the agent a direct way to query official Godot docs instead of guessing APIs.  
**Why it could help us:** helpful support layer, especially if we begin relying on more advanced engine features.  
**Cautions:** useful, but not as urgent as runtime control, tests, or linting.  
**Current status:** `Captured`  
**Next evaluation step:** consider later as a support tool.

## Prerequisites To Track

Before trying any of the tools above, verify whether this machine has:

- Node.js
- npm
- Python 3
- pip
- Git
- .NET SDK
- Godot 4.x
- `uvx`

When we test a tool, record the actual environment result in this file instead of assuming it is installed.

## How To Update This File

When a session evaluates a tool, update:

1. the row in `Tool Summary`
2. the detailed section for that tool
3. the evidence / notes in plain language
4. the next step

Also update:

- `state/current-status.md`
- `state/task-board.md`
- `state/session-log.md`

## Current Decision

For this repo, the current best next tooling trials are:

1. `Godot Forge`
2. one testing framework: `GUT` or `GdUnit4`
3. `GDScript Toolkit`

We should avoid trying too many tools at once. The goal is to build a trusted stack gradually, not collect unused tooling.
