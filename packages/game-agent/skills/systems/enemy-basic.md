# SKILL: Basic Enemy AI

## What This Does
Creates simple enemies that patrol back and forth. If the player touches them, something happens (lose health, game over, etc.)

---

## Core Concepts (Explain to User)

- **Patrol**: The enemy walks between two points automatically
- **Area2D for detection**: The enemy has an area that detects the player
- **CharacterBody2D**: The enemy is a physics body that can't walk through walls

---

## Files to Create

### 1. Enemy Scene: `scenes/objects/enemy.tscn`

**Node structure:**
```
Enemy (CharacterBody2D)
├── Sprite2D (red square placeholder, 32x32)
├── CollisionShape2D (RectangleShape2D, 28x28)
└── HitArea (Area2D)
    └── HitShape (CollisionShape2D, slightly larger)
```

### 2. Enemy Script: `scripts/objects/enemy.gd`

```gdscript
# Enemy — patrols left and right, hurts the player on contact
extends CharacterBody2D

@export var speed: float = 80.0
@export var patrol_distance: float = 100.0

var start_position: Vector2
var direction: float = 1.0

signal player_hit

func _ready() -> void:
    start_position = position
    $HitArea.body_entered.connect(_on_hit_area_body_entered)

func _physics_process(_delta: float) -> void:
    # Move in current direction
    velocity.x = direction * speed
    move_and_slide()
    
    # Reverse direction at patrol limits
    if position.x > start_position.x + patrol_distance:
        direction = -1.0
    elif position.x < start_position.x - patrol_distance:
        direction = 1.0

func _on_hit_area_body_entered(body: Node2D) -> void:
    if body.is_in_group("player"):
        player_hit.emit()
```

---

## What Happens When Player Is Hit

**Simple version (game over):**
```gdscript
# In level script
func _on_enemy_player_hit() -> void:
    get_tree().change_scene_to_file("res://scenes/ui/main_menu.tscn")
```

**Better version (lose health):**
See `/skills/systems/health.md`

---

## Adding Enemies to a Level

```
Level01
├── TileMapLayer
├── Player
├── Coins
├── Enemies (Node2D)
│   ├── Enemy1 (instance)
│   └── Enemy2 (instance)
└── HUD
```

For each enemy instance, you can adjust `patrol_distance` in the Inspector.

---

## How to Test

> "Run the game. You should see red squares moving left and right.
> Walk into one. Something should happen (game over or lose health)."

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Enemy doesn't move | Script not attached | Attach script to root node |
| Enemy walks through walls | No collision with tilemap | Ensure enemy is on same collision layer |
| Player not detected | Player not in "player" group | Add player to group |
| Enemy jitters at edges | Patrol distance too small | Increase `patrol_distance` |
