# SKILL: Win Screen

## What This Does
Shows a "You Win!" screen when the player completes the goal, with options to restart or quit.

---

## Files to Create

### 1. Win Screen Scene: `scenes/ui/win_screen.tscn`

**Node structure:**
```
WinScreen (Control)
├── ColorRect (background overlay, semi-transparent black)
├── VBoxContainer (centered)
│   ├── TitleLabel (Label: "You Win!")
│   ├── ScoreLabel (Label: "Score: X")
│   ├── PlayAgainButton (Button: "Play Again")
│   └── QuitButton (Button: "Quit")
```

**Settings:**
- Control: full rect (anchors fill entire screen)
- ColorRect: full rect, color = black with ~50% transparency
- VBoxContainer: centered on screen
- TitleLabel: font size 48, centered
- Buttons: minimum size 200x50

### 2. Win Screen Script: `scripts/ui/win_screen.gd`

```gdscript
# Win screen — shown when the player wins
extends Control

@onready var score_label: Label = $VBoxContainer/ScoreLabel
@onready var play_again_button: Button = $VBoxContainer/PlayAgainButton
@onready var quit_button: Button = $VBoxContainer/QuitButton

func _ready() -> void:
    score_label.text = "Score: " + str(ScoreManager.get_score())
    play_again_button.pressed.connect(_on_play_again)
    quit_button.pressed.connect(_on_quit)

func _on_play_again() -> void:
    ScoreManager.reset()
    get_tree().change_scene_to_file("res://scenes/levels/level_01.tscn")

func _on_quit() -> void:
    get_tree().quit()
```

---

## How to Trigger the Win Screen

From the level script, when the player wins:

```gdscript
func _win() -> void:
    get_tree().change_scene_to_file("res://scenes/ui/win_screen.tscn")
```

---

## How to Test

> "Collect all the coins. A 'You Win!' screen should appear showing your score.
> Click 'Play Again' — the level should restart with score at 0."

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Screen doesn't show | Wrong scene path | Check path in `change_scene_to_file` |
| Score shows 0 | ScoreManager reset too early | Reset score only when Play Again is pressed |
| Buttons don't work | Signals not connected | Check `_ready()` connections |
