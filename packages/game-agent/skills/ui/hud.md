# SKILL: HUD (Heads-Up Display)

## What This Does
Shows game information on screen — score, health, lives, etc. It stays fixed on screen even when the camera moves.

---

## Core Concepts (Explain to User)

- **CanvasLayer**: A special layer that stays on screen no matter where the camera goes. Perfect for UI.
- **Label**: A node that displays text.

---

## Files to Create

### 1. HUD Scene: `scenes/ui/hud.tscn`

**Node structure:**
```
HUD (CanvasLayer)
└── MarginContainer
    └── ScoreLabel (Label)
```

**Settings:**
- MarginContainer: anchor to top-left, margins of 16px
- ScoreLabel: text = "Score: 0", font size = 24

### 2. HUD Script: `scripts/ui/hud.gd`

```gdscript
# HUD — displays the player's score on screen
extends CanvasLayer

@onready var score_label: Label = $MarginContainer/ScoreLabel

func _ready() -> void:
    ScoreManager.score_changed.connect(_on_score_changed)
    _on_score_changed(ScoreManager.get_score())

func _on_score_changed(new_score: int) -> void:
    score_label.text = "Score: " + str(new_score)
```

---

## Adding to Level

Instance the HUD scene in each level:

```
Level01 (Node2D)
├── TileMapLayer
├── Player
├── Coins
└── HUD (instance of hud.tscn)
```

Because HUD uses CanvasLayer, it will always render on top, even as the camera moves.

---

## How to Test

> "Run the game. You should see 'Score: 0' in the top-left corner.
> Pick up a coin. The score should change to 'Score: 1'."

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| HUD moves with camera | Not using CanvasLayer | Root must be CanvasLayer |
| Score shows but doesn't update | Signal not connected | Check `_ready()` connects to ScoreManager |
| Text too small | Default font size | Increase font size in Label settings |
| ScoreLabel not found | Wrong node path | Check `@onready` path matches scene tree |
