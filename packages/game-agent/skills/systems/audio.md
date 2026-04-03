# SKILL: Sound Effects & Music

## What This Does
Adds audio feedback to game events — coin pickup sounds, win jingles, background music.

---

## Core Concepts (Explain to User)

- **AudioStreamPlayer**: Plays sound globally (good for music, UI sounds)
- **AudioStreamPlayer2D**: Plays sound at a position in the world (good for coin pickup — louder when nearby)
- **Formats**: Use `.ogg` for music, `.wav` for short sound effects

---

## Adding a Coin Pickup Sound

### Step 1: Get/Create a Sound
Use a simple `.wav` or `.ogg` file. Place it in `assets/audio/sfx/coin_pickup.wav`.

The agent can suggest free sound sources:
> "You can find free sounds at freesound.org or use a simple beep for now."

### Step 2: Add to Coin Scene

Add an AudioStreamPlayer2D to the coin:
```
Coin (Area2D)
├── Sprite2D
├── CollisionShape2D
└── PickupSound (AudioStreamPlayer2D)
```

Load the audio file into PickupSound's `stream` property.

### Step 3: Play Before Freeing

Update coin script:
```gdscript
func _on_body_entered(body: Node2D) -> void:
    if body.is_in_group("player"):
        collected.emit()
        # Hide the coin but don't free yet — let sound play
        visible = false
        $CollisionShape2D.set_deferred("disabled", true)
        $PickupSound.play()
        await $PickupSound.finished
        queue_free()
```

---

## Adding Background Music

In the level scene or as an Autoload:

```
Level01
├── ...
└── BackgroundMusic (AudioStreamPlayer)
```

Settings:
- Load an `.ogg` file
- Set `autoplay = true`
- Set `volume_db` to around -10 (not too loud)

---

## How to Test

> "Pick up a coin. You should hear a sound!
> If no sound plays, check that the audio file is loaded in the PickupSound node."

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| No sound at all | Audio file not loaded | Assign audio stream in Inspector |
| Sound cuts off | `queue_free()` called too early | Use `await finished` before freeing |
| Music too loud | Default volume | Reduce `volume_db` to -10 or lower |
