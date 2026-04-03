# GLOBAL RULES

These rules apply to EVERY game project, regardless of type.

---

## 1. Project Folder Structure

Every Godot project MUST follow this structure:

```
project-root/
├── project.godot
├── assets/
│   ├── sprites/
│   │   ├── player/
│   │   ├── enemies/
│   │   ├── items/
│   │   └── environment/
│   ├── audio/
│   │   ├── sfx/
│   │   └── music/
│   └── fonts/
├── scenes/
│   ├── player/
│   │   └── player.tscn
│   ├── levels/
│   │   └── level_01.tscn
│   ├── ui/
│   │   ├── hud.tscn
│   │   └── main_menu.tscn
│   └── objects/
│       ├── coin.tscn
│       └── enemy.tscn
├── scripts/
│   ├── player/
│   │   └── player.gd
│   ├── systems/
│   │   ├── game_manager.gd
│   │   └── score_manager.gd
│   ├── ui/
│   │   └── hud.gd
│   └── objects/
│       ├── coin.gd
│       └── enemy.gd
└── levels/
    └── tilemaps/
```

### Rules:
- **Never put files in the root** unless it's `project.godot`
- **Every scene has its own folder** under `scenes/`
- **Every script goes in `scripts/`**, mirroring the `scenes/` structure
- **All art/audio goes in `assets/`** — never reference files outside the project

---

## 2. Naming Conventions

| Thing          | Convention          | Example              |
|----------------|--------------------|-----------------------|
| Folders        | lowercase          | `scenes/player/`     |
| Scene files    | snake_case.tscn    | `player.tscn`        |
| Script files   | snake_case.gd      | `player.gd`          |
| Node names     | PascalCase         | `Player`, `CoinArea` |
| Variables      | snake_case         | `move_speed`         |
| Constants      | UPPER_SNAKE        | `MAX_HEALTH`         |
| Signals        | past_tense         | `coin_collected`     |
| Functions      | snake_case         | `take_damage()`      |

---

## 3. Code Quality Rules

- **Every script must have a comment at the top** explaining what it does (1–2 lines)
- **No magic numbers** — use `@export` variables or constants
- **Keep scripts under 100 lines** — if longer, split into smaller scripts
- **Use signals for communication** between nodes — never use `get_node("../../some/deep/path")`
- **Use `@export`** for values the user might want to change (speed, health, etc.)
- **Use groups** for finding nodes at runtime (e.g., `enemies`, `coins`)

---

## 4. Scene Rules

- **One root node per scene** — the root defines what it is (CharacterBody2D for player, Area2D for coins, etc.)
- **Always add a CollisionShape2D** to anything that interacts physically
- **Use separate scenes** for reusable objects (coins, enemies, projectiles)
- **Never hardcode positions** — use markers or spawn points

---

## 5. Asset Rules

- **Always use placeholder assets first** — colored rectangles are fine
- **Standard sprite sizes:** 16x16, 32x32, or 64x64 pixels for pixel art
- **Import settings:** For pixel art, set filter to "Nearest" (not Linear)
- **Audio:** Use `.ogg` for music, `.wav` for short sound effects

---

## 6. Testing After Every Change

After implementing ANY feature, tell the user:

1. What to do to test it (e.g., "Press F5 to run the scene")
2. What they should see (e.g., "Your character should move when you press arrow keys")
3. What to do if it doesn't work (e.g., "Check that the script is attached to the Player node")

---

## 7. Error Handling

- If a feature doesn't work: **fix it before moving on**
- If you can't fix it: **revert to the last working state and document what went wrong**
- Never say "it should work" — verify or tell the user how to verify

---

## 8. State Management

After completing ANY task:
1. Update `/state/current-status.md` with what changed
2. Move the task in `/state/task-board.md`
3. Add an entry to `/state/session-log.md`

This is NOT optional. Future sessions depend on accurate state.
