# PHASES — Game Development Lifecycle

Adapted from BMAD Method's 4-phase workflow system.
Each phase produces artifacts that feed the next phase.

---

## Phase Overview

```
Phase 1: DREAM    → What game? What's fun about it?
Phase 2: DESIGN   → How does it work? What are the rules?
Phase 3: BUILD    → Create it, feature by feature
Phase 4: POLISH   → Make it feel good, fix issues, add juice
```

---

## Phase 1: DREAM (Analysis)

**Goal:** Understand what the student wants to build.

**Workflows:**
1. Welcome the student
2. Ask game type (from templates)
3. Ask guided questions (from QUESTIONS.md)
4. Summarize the game concept

**Produces:**
- Game definition in `current-status.md`
- Game Design Document in `docs/game-design.md`

**Exit criteria:**
- Student has confirmed the game concept
- Game type is chosen
- Core mechanics are defined

**Hat:** Game Designer

---

## Phase 2: DESIGN (Planning + Solutioning)

**Goal:** Turn the dream into a buildable plan.

**Workflows:**
1. Read the template for the chosen game type
2. Read the FEATURES.md to map features → skills
3. Create the task board with ordered tasks
4. Set up the Godot project structure

**Produces:**
- Populated `task-board.md`
- Project folder structure created on disk
- `docs/game-design.md` finalized

**Exit criteria:**
- Task board has ordered tasks
- All dependencies are clear
- Project structure exists on disk

**Hat:** Game Architect

---

## Phase 3: BUILD (Implementation)

**Goal:** Build the game, one feature at a time.

**Workflows — for EACH task:**
1. Announce what we're building
2. Read the relevant skill file
3. Implement (create scenes, scripts, assets)
4. Explain what was done
5. Test (tell student how to verify)
6. Update state files

**Produces:**
- Working game features
- Updated `task-board.md` (tasks move TODO → DONE)
- Updated `session-log.md`

**Exit criteria per task:**
- Feature works when tested
- State files updated
- Student confirmed it works

**Hat:** Game Developer + Game Tester (alternating)

---

## Phase 4: POLISH (Quality)

**Goal:** Make the game feel complete.

**Workflows:**
1. Review all features together
2. Add missing elements (sounds, menus, transitions)
3. Fix any remaining bugs
4. Create the start menu (if not done)
5. Set the main scene
6. Final playthrough

**Produces:**
- Complete, playable game
- All menus and screens in place
- `current-status.md` shows COMPLETE

**Exit criteria:**
- Game starts from menu
- All features work together
- Student is happy with the result

**Hat:** Game Tester → Game Developer (for fixes)

---

## Phase Transitions

The agent checks these conditions before moving to the next phase:

| Transition | Condition |
|-----------|-----------|
| DREAM → DESIGN | Student confirmed game concept |
| DESIGN → BUILD | Task board populated, project structure exists |
| BUILD → POLISH | All core tasks (from template "Must Have") are DONE |
| POLISH → COMPLETE | Game runs from start to finish without issues |

**Never skip a phase.** If the student says "just build it," still do a quick DREAM + DESIGN pass (can be very brief).

---

## Quick Flow (BMAD Quick Dev equivalent)

For students who already know what they want:

1. Skip detailed questions
2. Use template defaults
3. Go straight to BUILD
4. Still track state

Triggered when the student gives a very specific request like:
> "I want a top-down game where I collect coins. Just make it."

In Quick Flow, DREAM + DESIGN happen in 2 minutes instead of 10.
