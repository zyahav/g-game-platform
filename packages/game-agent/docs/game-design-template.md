# GAME DESIGN DOCUMENT (GDD)

This file is generated at the end of Phase 1 (DREAM) and finalized in Phase 2 (DESIGN).
It is the single source of truth for what the game IS.

Inspired by BMAD Game Dev Studio's GDD workflow.

---

## Game Identity

| Field | Value |
|-------|-------|
| **Game Title** | (student names it) |
| **Game Type** | (top-down / platformer / puzzle / clicker) |
| **Engine** | Godot Engine |
| **Target Audience** | Kids / Beginners |

---

## Core Concept

(1–3 sentences describing the game in plain language)

Example: "You play as a hero exploring a fantasy kingdom from above. Collect all the magic crystals to unlock the castle gate and win!"

---

## Player Experience Goals

What should the player FEEL?

- [ ] Excited (fast action)
- [ ] Curious (exploring)
- [ ] Smart (solving puzzles)
- [ ] Powerful (defeating enemies)
- [ ] Creative (building things)

---

## Core Mechanics

### Movement
- Type: (4-direction / 8-direction / platformer)
- Speed: (slow / medium / fast)

### Main Action
- What the player DOES: (collect / fight / solve / build)
- Primary interaction: (touch/overlap / button press / automatic)

### Goal
- Win condition: (collect all items / reach exit / defeat boss / score target)
- Lose condition: (health reaches 0 / time runs out / none)

---

## World Design

### Theme
- Setting: (fantasy / space / school / island / custom)
- Visual style: (pixel art / simple shapes / placeholder)
- Tile size: 32x32

### Level Structure
- Number of levels: (1 / 3 / 5)
- Level layout: (open / maze / linear path)
- Difficulty progression: (same / gradually harder)

---

## Game Objects

| Object | Type | Behavior | Quantity per Level |
|--------|------|----------|-------------------|
| Player | CharacterBody2D | Moves, collects, interacts | 1 |
| (coins/items) | Area2D | Collected on touch | (5-20) |
| (enemies) | CharacterBody2D | Patrol / chase | (0-5) |
| (NPCs) | Area2D | Talk on interaction | (0-3) |
| (exit/goal) | Area2D | Triggers win | 1 |

---

## User Interface

| Screen | Elements | When Shown |
|--------|----------|-----------|
| Start Menu | Title, Play button | Game launch |
| HUD | Score, Health (if applicable) | During gameplay |
| Win Screen | "You Win!", Score, Play Again, Quit | On win |
| Lose Screen (optional) | "Game Over", Try Again | On lose |

---

## Audio (Optional)

| Event | Sound Type |
|-------|-----------|
| Coin pickup | Short SFX |
| Enemy hit | Short SFX |
| Win | Jingle |
| Background | Loop music |

---

## Technical Notes

- Input actions needed: (list from template)
- Autoloads needed: ScoreManager, HealthManager (if applicable)
- Collision layers: Player (1), World (2), Items (3), Enemies (4)

---

## Build Order

(Copied from template, adjusted based on student's choices)

1. ...
2. ...
3. ...

---

## Status

- [ ] Student confirmed concept
- [ ] Task board generated
- [ ] Project structure created
- [ ] Ready for BUILD phase
