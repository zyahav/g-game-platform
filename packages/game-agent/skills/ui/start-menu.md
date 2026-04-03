# SKILL: Start Menu

## What This Does
A simple title screen with a "Play" button. This is the first thing the player sees.

---

## Files to Create

### 1. Main Menu Scene: `scenes/ui/main_menu.tscn`

**Node structure:**
```
MainMenu (Control)
├── ColorRect (background color)
├── VBoxContainer (centered)
│   ├── TitleLabel (Label: game name)
│   └── PlayButton (Button: "Play")
```

**Settings:**
- Control: full rect
- ColorRect: full rect, pick a color that fits the game theme
- VBoxContainer: centered
- TitleLabel: font size 48, centered
- PlayButton: minimum size 200x50

### 2. Main Menu Script: `scripts/ui/main_menu.gd`

```gdscript
# Main menu — the first screen the player sees
extends Control

@onready var play_button: Button = $VBoxContainer/PlayButton

func _ready() -> void:
    play_button.pressed.connect(_on_play)

func _on_play() -> void:
    ScoreManager.reset()
    get_tree().change_scene_to_file("res://scenes/levels/level_01.tscn")
```

---

## Set as Starting Scene

In `project.godot`, set:
```
run/main_scene="res://scenes/ui/main_menu.tscn"
```

Or instruct the user:
> "Go to Project → Project Settings → General → Run. Set 'Main Scene' to `res://scenes/ui/main_menu.tscn`"

---

## How to Test

> "Press F5. You should see the game title and a Play button.
> Click Play. The game level should start!"

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Game doesn't start at menu | Main scene not set | Set main scene in Project Settings |
| Button does nothing | Signal not connected | Check `_ready()` connection |
| Level doesn't load | Wrong scene path | Verify the path to level_01.tscn |
