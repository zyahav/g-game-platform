# SKILL: Win / Lose Conditions

## What This Does
Detects when the player has won or lost and triggers the appropriate response (show win screen, restart, etc.)

---

## Win Condition Types

### Type A: Collect All Items
The most common for top-down games.

**How it works:**
1. Count how many coins are in the level
2. When a coin is collected, check if all coins are gone
3. If all gone → player wins

**Implementation — in the level script:**

```gdscript
# Level script — checks win condition
extends Node2D

@onready var coins_container: Node2D = $Coins

func _ready() -> void:
    # Connect to each coin's collected signal
    for coin in coins_container.get_children():
        coin.collected.connect(_on_coin_collected)

func _on_coin_collected() -> void:
    # Check if all coins are collected
    # Use call_deferred because the coin is about to be freed
    call_deferred("_check_win")

func _check_win() -> void:
    if coins_container.get_child_count() == 0:
        _win()

func _win() -> void:
    print("You win!")
    # Option 1: Show win screen
    # get_tree().change_scene_to_file("res://scenes/ui/win_screen.tscn")
    
    # Option 2: Show message and pause
    # get_tree().paused = true
```

### Type B: Reach a Goal
Player touches a specific area (door, exit, flag).

**Create a goal scene (`scenes/objects/goal.tscn`):**
```
Goal (Area2D)
├── Sprite2D (door/flag image)
└── CollisionShape2D
```

**Goal script:**
```gdscript
extends Area2D

signal goal_reached

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
    if body.is_in_group("player"):
        goal_reached.emit()
```

### Type C: Defeat All Enemies
Similar to collect all items, but track enemy count instead.

---

## Lose Condition (Optional)

### Health reaches zero:
See `/skills/systems/health.md`

### Time runs out:
```gdscript
var time_left: float = 60.0  # seconds

func _process(delta: float) -> void:
    time_left -= delta
    if time_left <= 0:
        _lose()
```

---

## How to Test

> "Collect all the coins in the level. When you get the last one, you should see 'You win!' in the output console (bottom of Godot).
> Later we'll add a proper win screen!"

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Win triggers too early | Counting wrong | Use `call_deferred` to check after coin is freed |
| Win never triggers | Signals not connected | Make sure each coin's `collected` signal is connected |
| Coins not in container | Coins placed outside `Coins` node | Move all coin instances under the Coins container |
