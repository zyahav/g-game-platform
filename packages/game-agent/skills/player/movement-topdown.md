# SKILL: Top-Down Player Movement

## What This Does
Makes a character move in 4 directions (up, down, left, right) using arrow keys or WASD.

---

## Prerequisites
- Godot project exists with `project.godot`
- Input map has: `move_up`, `move_down`, `move_left`, `move_right`

## If Input Map Is Missing

Add this to `project.godot` or instruct the user to set it up manually:

The agent should check if the Input Map actions exist. If not, guide the user:
> "Go to Project → Project Settings → Input Map. Add these actions:
> - `move_up` → press W and Arrow Up
> - `move_down` → press S and Arrow Down
> - `move_left` → press A and Arrow Left
> - `move_right` → press D and Arrow Right"

---

## Files to Create

### 1. Player Scene: `scenes/player/player.tscn`

**Node structure:**
```
Player (CharacterBody2D)
├── Sprite2D
├── CollisionShape2D
└── Camera2D
```

**Settings:**
- Sprite2D: use a placeholder (32x32 blue square) or an imported sprite
- CollisionShape2D: RectangleShape2D, size 28x28 (slightly smaller than sprite)
- Camera2D: set `current = true`

### 2. Player Script: `scripts/player/player.gd`

```gdscript
# Player movement script — handles 4-direction top-down movement
extends CharacterBody2D

@export var speed: float = 200.0

func _physics_process(_delta: float) -> void:
    var direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity = direction * speed
    move_and_slide()
```

---

## Attach Script to Scene

The script `scripts/player/player.gd` must be attached to the `Player` (CharacterBody2D) root node.

---

## How to Test

Tell the user:
> "Let's test! Do this:
> 1. Open `scenes/player/player.tscn`
> 2. Press F6 (Run Current Scene)
> 3. Press the arrow keys or WASD
> 4. Your blue square should move around!"

---

## What Success Looks Like
- Character moves smoothly in all 4 directions
- Diagonal movement works (pressing two keys)
- Character stops when keys are released

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Character doesn't move | Script not attached | Attach script to root node |
| Character doesn't move | Input map not set up | Set up input actions in Project Settings |
| Character flies off screen | Speed too high | Reduce `speed` to 200 |
| Character moves but no visual | No Sprite2D | Add a Sprite2D with a texture |
