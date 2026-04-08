# Game Dev Platform — Architecture & Teaching Layer
**Status: Approved. Two architectural decisions added April 2026. Lesson sequence pending pilot validation.**
**Date: April 2026**

## What This Document Is
This document defines how the teaching layer should sit on top of the game-dev platform that already works.

The engineering system is already proven:
- the platform repo can generate a working game project
- the generated project can run, verify, and open in Godot
- a real student already used it successfully

What is still being designed is the learning system:
- how a student enters
- how they are guided
- when the Dev is involved
- how the student learns through doing instead of being lectured

This document is about that layer only.

## The Core Principle
The platform is already a good dev system. We do not replace it.

We add a teaching layer above it.

That means:
- the current engineering workflow stays authoritative
- the generated-project architecture stays authoritative
- the new learning flow must not blur those boundaries

## The Two Boundaries That Must Stay Clean

### 1. Platform Source vs Generated Project
The platform repo is the source.
The generated project is the product.

The student does not work inside the platform source.
The student works inside the generated project created from a selected kit.

One empty directory becomes one generated game project for one chosen kit.

### 2. Engineering Layer vs Teaching Layer
The engineering layer already exists and works:
- `core/`
- `kits/`
- Dev workflow
- specs
- tests
- verification
- handoff rules

The teaching layer is new.
It should sit above that system and guide the student through it without rewriting it.

These layers should remain separate:
- in folder structure
- in agent read order
- in everyone's mental model

## The Startup Chain
When the student pastes the GitHub URL into a new Codex thread, the agent reads files in this exact order:

1. `README.md` — confirms what this repo is and tells the agent to read the learning layer next
2. `learning/coach.md` — turns this thread into the Coach and defines its full behavior
3. `AGENT.md` — is NOT read by the Coach thread; it is read only by the Dev thread (Thread 2)

This means:
- Thread 1 (Coach) is governed by `learning/coach.md`
- Thread 2 (Dev) is governed by `AGENT.md` and `core/`
- `README.md` is the bridge that directs the agent to the right starting file

No other read order is valid.

## The Entry Flow
Every student starts the same way:

1. Create a new empty directory.
2. Open Codex in that directory.
3. Paste the GitHub repo URL.

The Coach takes over immediately. The agent must explicitly ask:

`Is this your first time making a game with this system?`

It must not guess. It must ask.

### If the student says yes — First-Time Onboarding

The Coach follows this exact opening sequence:

**Turn 1 — Coach:**
Greet the student warmly. Tell them they are about to make a real game. Tell them the Dev will generate it for them right now. Ask them to confirm they are ready.

**Turn 2 — Student:**
Confirms they are ready (or asks a question, which the Coach answers simply before continuing).

**Turn 3 — Coach:**
Instructs the Dev to generate the platformer project. Gives the student one simple action to do while they wait: "Open Godot. We'll use it in a moment."

After generation is confirmed by the Dev:

**Turn 4 — Coach:**
Tells the student to press Play in Godot. Nothing else. Just: "Press the Play button at the top. Tell me what you see."

This is Lesson 1: First Wow.

### If the student says no — Returning Student Flow

The Coach shows the available kits and asks which one they want.
After selection, the Dev generates the project and the Coach picks up from the appropriate lesson.

After the kit is selected:
- a generated project is created in that directory
- the student works in that generated project from then on

## The Roles

### The Student
The student is the manager of the project.
They make decisions, approve directions, place things in Godot, run the game, and decide what feels right.

They should feel:
- ownership
- momentum
- control

They should not feel:
- that they are being tested
- that they are doing system administration
- that they are expected to understand architecture before touching the game

### The Coach
The Coach is the student-facing guide.

The Coach combines three functions:
- PM
- instructor
- coach

The Coach:
- guides the student through the lesson sequence
- teaches Godot UI in context
- helps translate ideas into concrete tasks
- decides when the Dev needs to be invoked
- keeps the student moving

The Coach should teach only what is needed at the moment.

### The Dev
The Dev remains the professional implementation layer.

The Dev:
- reads the approved instruction
- confirms understanding
- builds exactly what was approved
- runs tests and verification
- reports back clearly

The Dev is not the teaching layer.
The Dev should remain aligned with the existing proven dev/spec/test/verification workflow.

### The Godot Editor
This is the student's hands-on workspace.

It is where the student:
- selects nodes
- moves things
- scales things
- paints tiles
- runs the game
- observes results

The editor is not separate from learning.
It is one of the main learning surfaces.

## When To Invoke The Dev
Use this rule:

- if the student can do it directly with their hands in Godot, keep it with the Coach
- if it requires a filesystem change, invoke the Dev

Filesystem changes include:
- code
- scenes
- resources
- config
- reusable nodes
- generated assets
- test files

This is the operating line between instruction mode and build mode.

## Thread Model

### Thread 1 — Coach
The student opens this thread by pasting the GitHub URL.
It handles:
- onboarding
- lesson flow
- PM/instructor guidance
- review of Dev reports
- next-step guidance in Godot

This thread stays open the entire session.

### Thread 2 — Dev
The student opens this thread when the Coach instructs them to.

The Dev thread is invoked at exactly two types of moment:

**Moment 1 — Initial generation (always)**
The very first use of the Dev thread is at onboarding, before any lessons begin. The Coach instructs the student to open the Dev thread and send the project generation instruction. This is a filesystem change — the largest one of all — and it follows the same rule: the student carries the message, the Dev confirms understanding, builds, and reports back.

**Moment 2 — Lesson-time filesystem changes**
After generation, the Dev thread is dormant until a lesson requires a filesystem change. The Coach reintroduces it at that moment. In the current platformer flow, the first expected lesson-time Dev moment is Lesson 7 (First World-Building), when TileMap setup is needed. However, if an earlier lesson unexpectedly requires a filesystem change, the Dev thread may be reintroduced sooner. The rule is the trigger, not the lesson number.

The Coach introduces it like this:
> "Now we need the Dev to prepare something in the project files. Open a new thread in this same directory. That's the Dev. I'll tell you what to send them."

The student carries messages between the two threads. That is intentional. The copy-paste ritual slows things down just enough for the student to read and understand what is being built.

## Message Envelope
All cross-thread messages use a strict envelope format:

```
--- START: PM TO DEV ---
[instruction]
--- END: PM TO DEV ---
```

```
--- START: DEV TO PM ---
[plan or report]
--- END: DEV TO PM ---
```

This keeps roles clean and makes handoff explicit.

## Repo Structure
The current engineering structure remains intact.

The learning layer is added as a separate top-level area:

```
platform-repo/
  README.md
  AGENT.md
  core/
  kits/
  learning/
    coach.md          ← loader only
    kaya/
      Mission.md
      Soul.md
      Boundaries.md
      Playbook.md
      Onboarding.md
      Lessons.md
    lessons/
      platformer.md   ← detailed node-level spec
  docs/
    ARCHITECTURE.md
    DECISION-STARTUP-AND-LEARNING-LAYER.md
    PILOT_CHECKLIST.md
```

### What each part means
- `README.md` — short human-facing entry; directs agent to `learning/coach.md`
- `AGENT.md` — machine-facing Dev startup contract; governs Thread 2 only
- `core/` — engineering rules, workflow, verification, protocols
- `kits/` — game-specific knowledge and templates
- `learning/` — teaching logic only; governs Thread 1
- `docs/` — human/team reference documents

## README.md Role
`README.md` stays short and human-facing.

Its job:
- explain what this repo is in one paragraph
- give the student the one starting action
- tell the agent to read `learning/coach.md` next

It does not contain lesson logic, role definitions, or agent behavior. Those live in `learning/coach.md`.

## AGENT.md Role
`AGENT.md` is the machine-facing engineering contract for the Dev thread.

It governs:
- setup/install logic
- generated-project generation
- dev workflow
- verification rules

It is NOT read by the Coach thread. It may need small additions later to cooperate with the learning layer, but it remains the engineering source of truth for the Dev.

## Kit Model
For now, the teaching design focuses on the current proven kit only:

- `platformer`

We do not generalize until this kit's learning flow is validated with real students.

### About `platformer-build`
Still an open design question. May be a second kit or a second learning track inside the same kit. Decision deferred until the normal platformer teaching flow is working well.

## Lesson Philosophy
The student should not begin with code explanation.

The first real student session proved this: when the student says "Teach me", the correct response is not architecture. The correct response is action.

Teaching principle: `visible action first, explanation second`

## Lesson Arc For The Current Platformer
The agreed sequence:

| # | Name | What the student does | Dev needed? |
|---|---|---|---|
| 1 | First wow | Runs the generated game. Plays it. Feels it. | No |
| 2 | First control | Opens Godot. Moves one object. Runs again. Sees the change. | No |
| 3 | First tiny build | Duplicates a platform. Moves it. Tests it. | No |
| 4 | First collectible | Places one coin. Runs and collects it. | No |
| 5 | First hazard | Places one spike. Tests death and restart. | No |
| 6 | First checkpoint | Moves the checkpoint. Tests respawn. | No |
| 7 | First world-building | Paints ground with TileMap tools. | Yes — TileMap setup |
| 8 | First polish | Moves a tree or decoration. Adjusts layering. | No |
| 9 | First code look | Opens one script. One behavior explained. | No |
| 10 | First feature request | Designs something new. Coach specs it. Dev builds it. Student places it. | Yes |

Note: This sequence is directionally validated. Final validation requires another student pilot run.

## Hard Teaching Rules
- Do not start with code.
- Do not explain abstract architecture at the beginning.
- Do not move to the next lesson until the student has felt the result of the current one.
- Do not send a Dev instruction without the student approving it first.
- Do not ask the student to solve environment/tooling problems unless automatic recovery has already been attempted.
- Do not overload one lesson with more than one new concept.
- Do not introduce the Dev thread before it is needed.

## Godot UI Learning
The student learns the UI through actions, not lectures.

First UI module covers only:
- Scene tree — click a node
- Inspector — see its properties
- 2D viewport — move it
- Run button — press play, see what changed

Nothing more at the beginning.

## Environment Responsibility
The student should not be the first surface for environment issues.

The system attempts automatic recovery first for:
- repo access issues
- Godot not on PATH
- `make` missing
- git safe-directory
- writable config/home paths

The student is the manager, not the setup technician.

## What The Student Should Feel
They should feel:
- "I made a game appear"
- "I moved this"
- "I changed this"
- "I made the game react"
- "I told the Dev what to build"
- "I approved the work"

They should not feel:
- "I need to understand code first"
- "I need to fix PATH issues before I can learn"
- "I am following a tutorial about menus"

The learning should feel like project ownership, not classroom instruction.

## Open Questions
1. Should `platformer-build` become a separate kit or a learning track inside `platformer`? (Deferred until platformer teaching flow is validated.)
2. How much should lesson pacing adapt for advanced students versus following a fixed sequence? (Deferred to pilot observation.)

## Next Step
Run a real student pilot session using the current files.
Observe against `docs/PILOT_CHECKLIST.md`.
Change at most three things between pilots.
Generalize only after the platformer teaching flow works well.

## Final Principle
Keep the current engineering platform.
Add the learning system above it.
Teach the current platformer first.
Generalize only after the real student flow works well.

---

## Approved Architectural Decisions

Two architectural decisions were made in April 2026 and are now part of this architecture:

**Startup Flow (stage → promote → cleanup)** and **Generated Project Learning Layer**.

Full decision records, approved answers, and implementation tasks are in:
`docs/DECISION-STARTUP-AND-LEARNING-LAYER.md`
