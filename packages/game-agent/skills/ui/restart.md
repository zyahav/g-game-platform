# SKILL: Restart System

## What This Does
Lets the player restart the current level or the entire game.

---

## Option 1: Restart Key (Quick Restart)

Add to the player script or level script:

```gdscript
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("restart"):
        ScoreManager.reset()
        get_tree().reload_current_scene()
```

Add `restart` to the Input Map → key R.

---

## Option 2: Restart Button (In Win/Lose Screen)

Already covered in `/skills/ui/win-screen.md`.

```gdscript
func _on_play_again() -> void:
    ScoreManager.reset()
    get_tree().change_scene_to_file("res://scenes/levels/level_01.tscn")
```

---

## Option 3: Pause Menu with Restart

```gdscript
# In any scene — press Escape to pause and show restart option
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("ui_cancel"):  # Escape key
        get_tree().paused = !get_tree().paused
```

This requires a pause menu scene (advanced — implement later).

---

## How to Test

> "Press R during the game. The level should restart, score back to 0."
