# SKILL: Level Transitions

## What This Does
Lets the player move from one level to the next — through a door, exit zone, or after completing a goal.

---

## Core Concept

Each level is a separate scene file. To go to the next level, we just load the next scene.

---

## Implementation

### 1. Level Exit Scene: `scenes/objects/level_exit.tscn`

```
LevelExit (Area2D)
├── Sprite2D (door or portal image)
└── CollisionShape2D
```

### 2. Level Exit Script: `scripts/objects/level_exit.gd`

```gdscript
# LevelExit — takes the player to the next level when touched
extends Area2D

@export var next_level_path: String = ""

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
    if body.is_in_group("player") and next_level_path != "":
        get_tree().change_scene_to_file(next_level_path)
```

### 3. Usage in a Level

Place a LevelExit instance in the level scene. In the Inspector, set `next_level_path` to:
- `res://scenes/levels/level_02.tscn` (for level 1 → 2)
- `res://scenes/ui/win_screen.tscn` (for the last level → win)

---

## Level Naming Convention

```
scenes/levels/
├── level_01.tscn
├── level_02.tscn
└── level_03.tscn
```

---

## Score Persistence

The ScoreManager autoload keeps the score between levels automatically. Only reset it when the player goes back to the main menu or restarts.

---

## How to Test

> "Walk to the door/exit in level 1. You should be taken to level 2.
> Your score should carry over!"

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Nothing happens at exit | `next_level_path` is empty | Set the path in the Inspector |
| Scene not found | Wrong path | Double-check the `.tscn` file path |
| Score resets | ScoreManager reset called | Only reset on menu/restart, not level change |
| Player not detected | Player not in "player" group | Add to group |
