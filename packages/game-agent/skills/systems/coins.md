# SKILL: Coin / Item Collection System

## What This Does
Creates collectible items (coins, stars, gems) that the player can pick up by walking into them.

---

## Core Concepts (Explain to User)

- **Area2D**: A node that detects when something enters its space (no physics push)
- **Signal**: A message that a node sends when something happens ("body entered my area!")
- **Groups**: Tags you can put on nodes (like labeling the player as "player")

---

## Prerequisites
- Player scene exists with CharacterBody2D
- Player node is in the group `"player"` (or we check by node name)

### Add Player to Group
In the player scene, select the Player root node → Node tab → Groups → type `player` → Add.

Or in the player script, add:
```gdscript
func _ready() -> void:
    add_to_group("player")
```

---

## Files to Create

### 1. Coin Scene: `scenes/objects/coin.tscn`

**Node structure:**
```
Coin (Area2D)
├── Sprite2D
└── CollisionShape2D
```

**Settings:**
- Sprite2D: 16x16 yellow circle (placeholder)
- CollisionShape2D: CircleShape2D, radius 8

### 2. Coin Script: `scripts/objects/coin.gd`

```gdscript
# Coin — disappears when the player touches it and adds to score
extends Area2D

signal collected

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
    if body.is_in_group("player"):
        collected.emit()
        queue_free()
```

---

## Adding Coins to a Level

In the level scene (`scenes/levels/level_01.tscn`):

```
Level01 (Node2D)
├── TileMapLayer
├── Player
├── Coins (Node2D)  ← container for organization
│   ├── Coin (instance)
│   ├── Coin2 (instance)
│   └── Coin3 (instance)
└── HUD
```

Place coin instances on floor tiles where the player can reach them.

---

## Connecting to Score System

Option A — **Signal-based (recommended)**:
The coin emits `collected`. A game manager or the level script listens and updates the score.

Option B — **Direct call (simpler for beginners)**:
```gdscript
# In coin.gd, replace the signal approach:
func _on_body_entered(body: Node2D) -> void:
    if body.is_in_group("player"):
        ScoreManager.add_point()  # autoload
        queue_free()
```

See `/skills/systems/score.md` for the ScoreManager setup.

---

## How to Test

> "Run the game. Walk into a coin. It should:
> 1. Disappear when you touch it
> 2. (If score is set up) Add a point to your score"

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Coin doesn't disappear | Signal not connected | Check `body_entered` connection |
| Coin doesn't detect player | Player not in "player" group | Add player to group |
| Coin doesn't detect player | Wrong collision layers | Ensure Area2D monitors the player's layer |
| Coin blocks player movement | Used StaticBody2D instead of Area2D | Change root to Area2D |
