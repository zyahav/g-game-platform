# TOP-DOWN GAME TEMPLATE

## What Is a Top-Down Game?

A 2D game where the player sees the world from above and moves in all directions (up, down, left, right). Think of it like looking at a board game from above — you see everything from a bird's eye view.

**Examples kids might know:** Pokémon (the walking parts), early Zelda, Pac-Man (sort of!)

---

## Base Features (Every Top-Down Game Has These)

### Must Have (Phase 1 — Prototype)
1. **Player character** that moves in 4 directions
2. **A simple map** made with tiles (floor, walls)
3. **Camera** that follows the player
4. **Collision** — the player can't walk through walls

### Should Have (Phase 2 — Core Game)
5. **Collectible items** (coins, stars, gems)
6. **Score display** (HUD showing points)
7. **A goal** (collect all coins, reach a door, etc.)
8. **Win screen** when the goal is achieved

### Nice to Have (Phase 3 — Polish)
9. **Sound effects** (footsteps, coin pickup, win sound)
10. **Start menu** (play button)
11. **Multiple levels**
12. **Enemies** (simple patrol movement)
13. **Restart button** when you lose or win

---

## Build Order (IMPORTANT — Follow This Sequence)

```
Step 1: Player scene + movement script
Step 2: Simple test level (one room with walls)
Step 3: Camera follows player
Step 4: Add collectible items (coins)
Step 5: Score system + HUD
Step 6: Win condition (all coins collected)
Step 7: Win screen
Step 8: Start menu
Step 9: Sound effects
Step 10: Second level (optional)
Step 11: Enemies (optional)
```

Each step produces something testable. Never skip ahead.

---

## Node Structure

### Player Scene (`scenes/player/player.tscn`)
```
Player (CharacterBody2D)
├── Sprite2D (or AnimatedSprite2D)
├── CollisionShape2D (rectangle or circle)
└── Camera2D (set to Current)
```

### Coin Scene (`scenes/objects/coin.tscn`)
```
Coin (Area2D)
├── Sprite2D
├── CollisionShape2D
└── AudioStreamPlayer2D (optional, for pickup sound)
```

### Level Scene (`scenes/levels/level_01.tscn`)
```
Level01 (Node2D)
├── TileMapLayer (floor + walls)
├── Player (instance of player.tscn)
├── Coins (Node2D, container)
│   ├── Coin1 (instance)
│   ├── Coin2 (instance)
│   └── Coin3 (instance)
└── HUD (instance of hud.tscn)
```

### HUD Scene (`scenes/ui/hud.tscn`)
```
HUD (CanvasLayer)
└── ScoreLabel (Label)
```

---

## Default Values

| Setting | Value | Notes |
|---------|-------|-------|
| Player speed | 200 | pixels per second |
| Tile size | 32x32 | pixels |
| Player sprite size | 32x32 | matches tile size |
| Coin sprite size | 16x16 | smaller than player |
| Camera zoom | 1.0 | default, adjust if needed |

---

## Input Map

These inputs must be configured in Project → Project Settings → Input Map:

| Action Name | Key(s) |
|-------------|--------|
| `move_up` | W, Arrow Up |
| `move_down` | S, Arrow Down |
| `move_left` | A, Arrow Left |
| `move_right` | D, Arrow Right |

**Note:** If the Input Map is not set up, the agent should create it using code or instruct the user clearly.

---

## Placeholder Assets

Until real art is added, use simple colored shapes:

| Object | Placeholder |
|--------|------------|
| Player | Blue square (32x32) |
| Wall tile | Dark gray square (32x32) |
| Floor tile | Light gray square (32x32) |
| Coin | Yellow circle (16x16) |
| Enemy | Red square (32x32) |

The agent can generate these as simple `.png` files using code.
