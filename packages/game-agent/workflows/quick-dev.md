# QUICK DEV — Fast Track Game Building

Adapted from BMAD's `bmad-quick-dev` unified quick flow.
For students who already know what they want.

---

## When to Use Quick Dev

The student says something very specific like:
- "Make me a top-down game where I collect coins"
- "I want a maze game with enemies"
- "Build a platformer with 3 levels"

They skip the detailed question flow and go straight to building.

---

## Quick Dev Flow

### Step 1: Clarify in 1 Question
Extract what you need from their request. Ask ONE clarifying question max:

> "Got it — a top-down coin collector! Quick question: should the player avoid enemies, or keep it simple with just coins?"

### Step 2: Auto-fill the Design
Use template defaults for everything the student didn't specify:
- Theme: Fantasy (default)
- Difficulty: Easy (default)
- Character name: "Hero" (default)

Create a minimal `game-design.md` with these choices.

### Step 3: Generate Task Board
Use the template's build order as-is. No customization needed.

### Step 4: Run Readiness Check (30 seconds)
Quick pass — just verify project structure exists.

### Step 5: Start Building Immediately
Enter the dev-loop. Build features one by one.

---

## Time Target

Quick Dev should go from "I want X" to "player moves on screen" in under 10 minutes.

---

## Differences from Full Flow

| Aspect | Full Flow | Quick Dev |
|--------|-----------|-----------|
| Questions | 5 questions, one at a time | 0-1 questions |
| Design doc | Fully detailed | Minimal, defaults |
| Task planning | Custom task board | Template default order |
| Phase gates | Full readiness check | Quick check |
| Build process | Same | Same |

---

## Guardrails

Even in Quick Dev:
- Still create state files
- Still update after each task
- Still test after each feature
- Still follow RULES.md
- Still track in session-log.md

Quick Dev is about skipping planning, not skipping quality.
