# SKILL: Health System

## What This Does
Gives the player health (lives/hearts). When hit by an enemy, the player loses health. When health reaches 0, the game ends.

---

## Core Concepts (Explain to User)

- **Health**: A number that goes down when you get hurt
- **Invincibility frames**: After getting hit, the player blinks and can't be hurt again for a short time (so one enemy doesn't kill you instantly)

---

## Files to Create

### 1. Health Manager (Autoload): `scripts/systems/health_manager.gd`

```gdscript
# HealthManager — tracks player health (global autoload)
extends Node

signal health_changed(new_health: int)
signal player_died

@export var max_health: int = 3
var current_health: int

func _ready() -> void:
    current_health = max_health

func take_damage(amount: int = 1) -> void:
    current_health -= amount
    health_changed.emit(current_health)
    if current_health <= 0:
        player_died.emit()

func heal(amount: int = 1) -> void:
    current_health = mini(current_health + amount, max_health)
    health_changed.emit(current_health)

func reset() -> void:
    current_health = max_health
    health_changed.emit(current_health)
```

Register as Autoload: add to `project.godot` under `[autoload]`:
```
HealthManager="*res://scripts/systems/health_manager.gd"
```

### 2. Add Invincibility to Player: update `scripts/player/player.gd`

Add these variables and functions to the player script:

```gdscript
var is_invincible: bool = false
@export var invincibility_time: float = 1.5

func take_hit() -> void:
    if is_invincible:
        return
    HealthManager.take_damage(1)
    _start_invincibility()

func _start_invincibility() -> void:
    is_invincible = true
    # Blink effect
    var tween = create_tween()
    for i in range(5):
        tween.tween_property($Sprite2D, "modulate:a", 0.3, 0.15)
        tween.tween_property($Sprite2D, "modulate:a", 1.0, 0.15)
    await tween.finished
    is_invincible = false
```

### 3. Update HUD to Show Health: update `scripts/ui/hud.gd`

```gdscript
@onready var health_label: Label = $MarginContainer/VBoxContainer/HealthLabel

func _ready() -> void:
    ScoreManager.score_changed.connect(_on_score_changed)
    HealthManager.health_changed.connect(_on_health_changed)
    _on_score_changed(ScoreManager.get_score())
    _on_health_changed(HealthManager.current_health)

func _on_health_changed(new_health: int) -> void:
    health_label.text = "Health: " + str(new_health)
```

---

## Connecting Enemy Hits to Health

Update the enemy hit handler (in level script or player):

```gdscript
# When enemy hits player
func _on_enemy_player_hit() -> void:
    # Find the player and call take_hit
    var player = get_tree().get_first_node_in_group("player")
    if player and player.has_method("take_hit"):
        player.take_hit()
```

## Handling Death

In the level script:

```gdscript
func _ready() -> void:
    HealthManager.player_died.connect(_on_player_died)

func _on_player_died() -> void:
    # Go to game over or restart
    await get_tree().create_timer(1.0).timeout
    ScoreManager.reset()
    HealthManager.reset()
    get_tree().change_scene_to_file("res://scenes/ui/main_menu.tscn")
```

---

## How to Test

> "Run the game. Walk into an enemy.
> 1. Your character should blink
> 2. Health should go down by 1
> 3. Walk into the enemy again — health goes down again
> 4. When health reaches 0, the game should end"

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Player dies instantly | No invincibility frames | Add the `is_invincible` check |
| Health doesn't show | HUD not connected to HealthManager | Connect signal in HUD `_ready()` |
| Player never dies | `take_hit()` not called | Check enemy → player connection |
| Health carries over | Not resetting | Call `HealthManager.reset()` on restart |
