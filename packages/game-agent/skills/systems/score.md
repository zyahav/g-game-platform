# SKILL: Score System

## What This Does
Tracks the player's score across the game. Uses an Autoload (global script) so any scene can access it.

---

## Core Concepts (Explain to User)

- **Autoload**: A script that runs the whole time the game is open. Every scene can access it. Think of it like a scoreboard hanging on the wall — everyone can see it.
- **Signal**: The score manager sends a message whenever the score changes, so the HUD can update automatically.

---

## Files to Create

### 1. Score Manager Script: `scripts/systems/score_manager.gd`

```gdscript
# ScoreManager — keeps track of the player's score (global autoload)
extends Node

signal score_changed(new_score: int)

var score: int = 0

func add_points(amount: int = 1) -> void:
    score += amount
    score_changed.emit(score)

func reset() -> void:
    score = 0
    score_changed.emit(score)

func get_score() -> int:
    return score
```

### 2. Register as Autoload

The agent must add this to `project.godot` under `[autoload]`:

```
ScoreManager="*res://scripts/systems/score_manager.gd"
```

Or instruct the user:
> "Go to Project → Project Settings → Autoload. Add:
> - Path: `res://scripts/systems/score_manager.gd`
> - Name: `ScoreManager`
> - Click 'Add'"

---

## How to Use from Other Scripts

### From a coin (when collected):
```gdscript
ScoreManager.add_points(1)
```

### From a level (to reset score):
```gdscript
ScoreManager.reset()
```

### From HUD (to display score):
```gdscript
func _ready() -> void:
    ScoreManager.score_changed.connect(_on_score_changed)
    # Show initial score
    _on_score_changed(ScoreManager.get_score())

func _on_score_changed(new_score: int) -> void:
    $ScoreLabel.text = "Score: " + str(new_score)
```

---

## How to Test

> "Pick up a coin. The HUD should update and show your new score.
> Pick up all coins. The score should match the number of coins."

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| `ScoreManager` not found | Not registered as Autoload | Add to Project Settings → Autoload |
| Score doesn't update HUD | Signal not connected | Connect `score_changed` in HUD `_ready()` |
| Score carries between levels | That's actually correct! | Use `reset()` if you want it to reset |
