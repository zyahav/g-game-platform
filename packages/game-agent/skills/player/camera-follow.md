# SKILL: Camera Follow Player

## What This Does
Makes the camera follow the player as they move around the world, so the player is always visible on screen.

---

## How It Works in Godot

In Godot, the simplest way is to make Camera2D a **child of the player**. That's it — it follows automatically.

---

## Implementation

### If Camera2D is already in the Player scene:
Just make sure `current = true` is set on the Camera2D node.

### If Camera2D is NOT in the Player scene:
Add it as a child of the Player (CharacterBody2D):

```
Player (CharacterBody2D)
├── Sprite2D
├── CollisionShape2D
└── Camera2D  ← add this
```

### Camera2D Settings:
- `current`: true
- `zoom`: Vector2(1, 1) — adjust if the world looks too big/small
- `position_smoothing_enabled`: true
- `position_smoothing_speed`: 5.0

**No script needed** for basic camera follow.

---

## Optional: Camera Limits

If the map has boundaries and you don't want the camera to show empty space:

Set these on Camera2D:
- `limit_left`: 0
- `limit_top`: 0
- `limit_right`: (map width in pixels)
- `limit_bottom`: (map height in pixels)

---

## How to Test

> "Run the game (F5 or F6). Walk to the edge of the map. The camera should follow your character smoothly."

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Camera doesn't follow | `current` is false | Set Camera2D `current = true` |
| Camera follows but jerky | Smoothing off | Enable `position_smoothing_enabled` |
| Two cameras fighting | Multiple cameras with `current = true` | Only one Camera2D should be current |
