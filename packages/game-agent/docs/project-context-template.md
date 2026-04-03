# PROJECT CONTEXT

This file is the "constitution" of the project (BMAD concept).
Every agent session reads this to stay aligned.
Generated at the end of Phase 2 (DESIGN), updated during BUILD.

---

## Project Identity

| Field | Value |
|-------|-------|
| Project name | (from game-design.md) |
| Game type | (from game-design.md) |
| Engine | Godot Engine 4.x |
| Language | GDScript |
| Current phase | (DREAM / DESIGN / BUILD / POLISH / COMPLETE) |

---

## Technology Stack

- **Engine:** Godot 4.x
- **Language:** GDScript
- **Scene format:** .tscn (text-based)
- **Resource format:** .tres (text-based)
- **Art style:** Pixel art / Placeholder shapes
- **Tile size:** 32x32 pixels

---

## Project Conventions

### Code Style
- Snake_case for variables and functions
- PascalCase for node names and class names
- UPPER_SNAKE for constants
- Every script starts with a comment explaining its purpose
- Use @export for tweakable values
- Use signals for inter-node communication
- Max 100 lines per script

### File Organization
- Scenes in `scenes/` (mirroring game structure)
- Scripts in `scripts/` (mirroring scenes/)
- Assets in `assets/` (sprites, audio, fonts)
- One scene per reusable object

### Godot-Specific Rules
- Use CharacterBody2D for moving entities
- Use Area2D for triggers and collectibles
- Use TileMapLayer for world building
- Camera2D as child of player
- CanvasLayer for UI elements
- Autoloads for global managers (Score, Health)

---

## Current Implementation State

(Auto-updated by agent after each task)

### Autoloads Registered
- [ ] ScoreManager
- [ ] HealthManager

### Input Actions Configured
- [ ] move_up
- [ ] move_down
- [ ] move_left
- [ ] move_right
- [ ] restart (optional)

### Scenes Created
- [ ] Player (scenes/player/player.tscn)
- [ ] Level 01 (scenes/levels/level_01.tscn)
- [ ] Coin (scenes/objects/coin.tscn)
- [ ] HUD (scenes/ui/hud.tscn)
- [ ] Main Menu (scenes/ui/main_menu.tscn)
- [ ] Win Screen (scenes/ui/win_screen.tscn)

---

## Known Issues

(Agent adds issues here as they're discovered)

---

## Decisions Log

(Agent logs important decisions and why they were made)

| Date | Decision | Reason |
|------|----------|--------|
| | | |
