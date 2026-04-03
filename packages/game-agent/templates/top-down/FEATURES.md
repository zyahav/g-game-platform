# TOP-DOWN GAME — FEATURE CATALOG

This file maps every possible feature to its skill file and dependencies.

---

## Core Features

| Feature | Skill File | Depends On | Priority |
|---------|-----------|------------|----------|
| Player movement | `/skills/player/movement-topdown.md` | nothing | 1 |
| Camera follow | `/skills/player/camera-follow.md` | player movement | 2 |
| TileMap world | `/skills/world/tilemap.md` | nothing | 3 |
| Collision with walls | `/skills/world/tilemap.md` (collision section) | tilemap | 4 |

## Collectible System

| Feature | Skill File | Depends On | Priority |
|---------|-----------|------------|----------|
| Coin/item pickup | `/skills/systems/coins.md` | player + collision | 5 |
| Score tracking | `/skills/systems/score.md` | coins | 6 |
| Score HUD | `/skills/ui/hud.md` | score tracking | 7 |

## Win/Lose Conditions

| Feature | Skill File | Depends On | Priority |
|---------|-----------|------------|----------|
| Win condition | `/skills/systems/win-lose.md` | depends on goal type | 8 |
| Win screen | `/skills/ui/win-screen.md` | win condition | 9 |
| Restart | `/skills/ui/restart.md` | win/lose screen | 10 |

## Optional Features

| Feature | Skill File | Depends On | Priority |
|---------|-----------|------------|----------|
| Start menu | `/skills/ui/start-menu.md` | nothing | 11 |
| Sound effects | `/skills/systems/audio.md` | nothing (can add anytime) | 12 |
| Basic enemy | `/skills/systems/enemy-basic.md` | tilemap + collision | 13 |
| Health system | `/skills/systems/health.md` | player | 14 |
| NPC dialogue | `/skills/systems/dialogue.md` | player + collision | 15 |
| Keys & doors | `/skills/systems/keys-doors.md` | player + collision | 16 |
| Multiple levels | `/skills/world/level-transition.md` | win condition | 17 |

---

## How to Use This File

1. After the user answers all questions, check which features they want
2. Find the matching skills in this table
3. Build the task board using the Priority column (lower number = build first)
4. Always respect the "Depends On" column — never build something before its dependency
