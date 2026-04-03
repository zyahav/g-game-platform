# SKILL: TileMap World Building

## What This Does
Creates a 2D world using tiles — small square images arranged in a grid to form floors, walls, and terrain.

---

## Core Concepts (Explain to User)

- **TileSet**: A collection of tile images (floor, wall, grass, etc.)
- **TileMapLayer**: A node that uses a TileSet to paint the world
- **Tile size**: Usually 32x32 pixels for simple games
- **Physics layer**: Makes certain tiles solid (walls the player can't walk through)

---

## Implementation

### Step 1: Create Placeholder Tile Art

Create simple 32x32 pixel images:
- `assets/sprites/environment/floor.png` — light gray
- `assets/sprites/environment/wall.png` — dark gray

The agent can generate these as solid-color PNGs using code.

### Step 2: Create a TileSet

In the level scene:

1. Add a `TileMapLayer` node
2. In the Inspector, create a **New TileSet**
3. Set tile size: 32x32
4. Open the TileSet editor (bottom panel)
5. Drag tile images into the TileSet

### Step 3: Set Up Wall Collision

In the TileSet editor:
1. Select the **wall tile**
2. Go to the **Physics** tab
3. Add a collision polygon (full square) to the physics layer

This makes walls solid — the player's `move_and_slide()` will stop at walls.

### Step 4: Paint the Level

Using the TileMap editor:
1. Select floor tile → paint the ground
2. Select wall tile → paint borders and obstacles

### Minimum Viable Map

A simple starting map:
```
W W W W W W W W W W
W . . . . . . . . W
W . . . . . . . . W
W . . . W W . . . W
W . . . . . . . . W
W . . . . . . . . W
W . . . W . . . . W
W . . . . . . . . W
W . . . . . . . . W
W W W W W W W W W W
```
(W = wall, . = floor)

---

## Level Scene Structure

```
Level01 (Node2D)
├── TileMapLayer
└── Player (instanced from player.tscn)
```

Place the Player instance on a floor tile.

---

## How to Create Programmatically (Agent Approach)

If the agent is creating the level via code/files:

1. Create the TileSet resource (`.tres` file)
2. Create the level scene (`.tscn` file) with TileMapLayer
3. Set tile data in the scene file

**However**, it's often easier to:
- Create the scene structure programmatically
- Then instruct the user to paint tiles manually in the editor

> "I set up the TileMap with floor and wall tiles. Now open `scenes/levels/level_01.tscn`, select the TileMapLayer, and paint your world! Use the floor tile for walkable areas and the wall tile for barriers."

---

## How to Test

> "Press F5 to run. Walk around with arrow keys. You should:
> 1. See the tiles you painted
> 2. Be able to walk on floor tiles
> 3. Be BLOCKED by wall tiles"

## Common Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Player walks through walls | No physics layer on wall tile | Add collision polygon to wall tile in TileSet |
| Tiles look blurry | Filter set to Linear | Change import filter to Nearest for pixel art |
| Tiles have gaps | Tile size mismatch | Ensure tile size matches in TileSet AND art |
| Can't paint tiles | TileMapLayer has no TileSet | Assign a TileSet in the Inspector |
