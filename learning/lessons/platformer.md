# Platformer Kit — Lesson Spec

This file defines the detailed spec for each of the 10 lessons in the platformer kit.

The Coach reads this file alongside `learning/coach.md`.
It is the source of truth for what each lesson requires, what nodes to reference, and what success looks like.

All node names in this file are verified against the real `Main.tscn` scene.

---

## Lesson 1 — First Wow

**Goal:** The student experiences a real working game before touching anything.

**What the student does:**
- Opens Godot
- Opens the generated project folder
- Presses the Play button (F5 or the triangle at the top)
- Plays the game

**What the Coach says:**
> "The game is ready. We are working in this project folder: [current project folder path]. Fastest path: open Terminal there and run `make play`. If you prefer Godot, open that same folder as the project and press the Play button at the top. Tell me what you see."

**What the Coach does NOT do:**
- Explain anything about the project structure
- Explain what a scene is
- Explain what nodes are
- Ask the student to look at any panel

**Success signal:**
The student reacts emotionally — "it works", "whoa", "it's a real game", or starts asking questions about the game itself.

**Nodes used:** None — student only plays, does not inspect.

**Dev needed:** No.

---

## Lesson 2 — First Control

**Goal:** The student moves one object in Godot and sees the change in-game.

**What the student does:**
- Opens the Scene Tree (left panel in Godot)
- Clicks on `StartFloor`
- Opens the Inspector (right panel)
- Changes the Y position by +50
- Presses Play
- Sees the floor has moved

**What the Coach says:**
> "Now let's make your first change. In Godot, look at the left panel — that's the Scene Tree. Click on `StartFloor`. Now look at the right panel — that's the Inspector. You'll see a Position value. Change the Y value — add 50 to whatever it shows. Then press Play again. Tell me what changed."

**What the Coach does NOT do:**
- Explain what StaticBody2D means
- Explain what a CollisionShape is
- Explain what Y axis means before the student asks

**UI concepts introduced (in context only):**
- Scene Tree — "the left panel, the list of everything in your game"
- Inspector — "the right panel, the settings for whatever you clicked"
- Run button — already used in Lesson 1

**Success signal:**
The student says the floor moved or the game looked different.

**Nodes used:** `StartFloor`

**Dev needed:** No.

---

## Lesson 3 — First Tiny Build

**Goal:** The student adds a platform that did not exist before.

**What the student does:**
- Clicks `Step1` in the Scene Tree
- Presses Ctrl+D to duplicate it
- Sees `Step1 2` appear in the Scene Tree
- Changes its Position in the Inspector to somewhere new
- Presses Play
- Tries to reach the new platform

**What the Coach says:**
> "Now you're going to add a platform that didn't exist before. In the Scene Tree, click on `Step1`. Press Ctrl+D to duplicate it. You'll see `Step1 2` appear. Move it somewhere new using the Position in the Inspector. Press Play and try to reach it."

**What the Coach does NOT do:**
- Explain scene instancing or what a PackedScene is
- Explain why Ctrl+D works
- Explain collision shapes

**Success signal:**
The student runs the game and tries to jump to the new platform — whether they reach it or not.

**Nodes used:** `Step1`

**Dev needed:** No.

**Coach tip:** If the student places the platform somewhere unreachable, that is fine. Ask them: "Could you reach it? What would you change to make it easier to jump to?" Let them figure out placement through play.

---

## Lesson 4 — First Collectible

**Goal:** The student places a new coin and collects it in-game.

**What the student does:**
- Finds `CoinStart` in the Scene Tree
- Duplicates it (Ctrl+D)
- Moves the copy to a new position
- Presses Play
- Collects the new coin
- Sees the coin counter go up

**What the Coach says:**
> "See the coins in the game? Each one is a reusable piece you can copy and place anywhere. Find `CoinStart` in the Scene Tree. Duplicate it. Move the copy somewhere you want a coin. Press Play and collect it. Watch the coin counter in the top left."

**What the Coach does NOT do:**
- Explain signals
- Explain how the coin script works
- Explain what a PackedScene instance is

**Success signal:**
The student collects the coin and sees the counter increase.

**Nodes used:** `CoinStart`, `Coin1`, `Coin2`, `Coin3`, `Coin4`, `CoinGoal` (for reference — student duplicates from `CoinStart`)

**Dev needed:** No.

**Coach tip:** After they collect it, ask: "Where else would you put a coin to make it harder to collect?" Let them place another one.

---

## Lesson 5 — First Hazard

**Goal:** The student places a spike and experiences death and restart.

**What the student does:**
- Finds `Spikes1` in the Scene Tree
- Duplicates it
- Moves the copy somewhere the player will land
- Presses Play
- Walks into the spike
- Sees the game-over screen and restarts

**What the Coach says:**
> "Now let's add danger. Find `Spikes1` in the Scene Tree. Duplicate it. Move the copy somewhere the player is likely to land — maybe right after a jump. Press Play and walk into it. What happens?"

**What the Coach does NOT do:**
- Explain Area2D
- Explain collision layers
- Explain how the hazard script detects the player

**Success signal:**
The student dies and sees the game-over state, then restarts.

**Nodes used:** `Spikes1`, `Spikes2` (for reference)

**Dev needed:** No.

**Coach tip:** After they die, ask: "Did it feel fair? Or was the spike hidden somewhere unfair?" Introduce the idea that game design is about feel, not just mechanics.

---

## Lesson 6 — First Checkpoint

**Goal:** The student moves the checkpoint and experiences respawn from a mid-level position.

**What the student does:**
- Finds `Checkpoint1` in the Scene Tree
- Moves it to a different position — somewhere after a hard jump
- Presses Play
- Reaches the checkpoint (flag activates)
- Dies deliberately
- Sees they respawn from the checkpoint, not the start

**What the Coach says:**
> "See `Checkpoint1` in the Scene Tree? Move it to a spot further into the level — somewhere after a difficult jump. Then press Play. Reach the checkpoint, then die on purpose. Where do you respawn?"

**What the Coach does NOT do:**
- Explain how checkpoint state is stored
- Explain signals or groups
- Explain the respawn logic in code

**Success signal:**
The student touches the checkpoint, dies, and respawns from that position instead of the start.

**Nodes used:** `Checkpoint1`

**Dev needed:** No.

**Coach tip:** Ask after: "What would happen if you put the checkpoint right before the spikes you placed in Lesson 5?" Let them experiment.

---

## Lesson 7 — First World-Building

**Goal:** The student paints ground tiles using TileMap tools.

**This lesson requires Dev involvement first.**

**Current project state:**
- Tile images exist in `TileSet1/` (Tileset.png, TilesExamples.png, Trees.png)
- No TileSet resource exists yet
- No TileMap or TileMapLayer node exists in `Main.tscn`

**Dev instruction (Coach sends this via the student):**

```
--- START: PM TO DEV ---
The project has tile images in TileSet1/ (Tileset.png, TilesExamples.png, Trees.png)
but no TileSet resource and no TileMap node exists yet.

Please:
1. Create a TileSet resource from the images in TileSet1/.
2. Add a TileMapLayer node to Main.tscn and assign the new TileSet to it.
3. Position the TileMapLayer at a sensible z-index so it appears behind the player.
4. Confirm when ready and tell the student exactly which node to click
   and where the tile palette appears in the Godot editor.
--- END: PM TO DEV ---
```

**What the Coach says after Dev confirms:**
> "Open Godot. Find the TileMapLayer node the Dev just added in the Scene Tree. Click on it. You should see a tile palette appear at the bottom of the screen. Pick a tile and click or drag in the 2D view to paint ground. Press Play and walk on it."

**What the Coach does NOT do:**
- Explain TileSet structure
- Explain physics layers for tiles
- Explain z-index before the student asks

**Success signal:**
The student paints at least a few tiles and walks on them in-game.

**Dev needed:** Yes — TileSet + TileMapLayer creation.

**Coach tip:** If the student finds painting intuitive, let them build freely for a few minutes. Ask: "What would you paint next — more ground, or something decorative?"

---

## Lesson 8 — First Polish

**Goal:** The student moves a decorative object and notices how small changes affect game feel.

**What the student does:**
- Finds one of the tree nodes: `TreeStart`, `TreeStep2`, `TreeStep4`, or `TreeGoal`
- Moves it to a new position
- Optionally scales it up or down using the Inspector Scale fields
- Presses Play
- Observes the visual difference

**What the Coach says:**
> "Now look at the trees in the scene — `TreeStart`, `TreeStep2`, `TreeStep4`, `TreeGoal`. Pick one. Move it somewhere else. Scale it bigger or smaller if you want. Press Play and see how it feels. This is how game artists work — small changes until it looks right."

**What the Coach does NOT do:**
- Explain z-index unless the student notices layering and asks
- Explain sprite rendering
- Turn this into a technical lesson

**Success signal:**
The student moves or scales something decorative and notices the visual result.

**Nodes used:** `TreeStart`, `TreeStep2`, `TreeStep4`, `TreeGoal`

**Dev needed:** No.

**Coach tip:** If the student wants to move background elements too (clouds, BGBack), let them. Say: "That's the background. Game artists often work in layers — background, midground, foreground. You just found the layers."

---

## Lesson 9 — First Code Look

**Goal:** The student opens one real script, reads one function, and connects it to game behavior they already experienced.

**What the student does:**
- Opens `scripts/collectibles/coin.gd` in Godot
- Finds the function that runs when the player touches the coin
- Reads it
- Guesses what it does

**What the Coach says:**
> "You've been changing the game without touching a single line of code. Now let's peek inside just one script — just to see what's there. In Godot, open the FileSystem panel at the bottom left. Find `scripts/collectibles/coin.gd` and double-click it. Find the function that says what happens when the player touches the coin. Read it out loud if you want. What do you think it does?"

**What the Coach does NOT do:**
- Explain GDScript syntax before the student asks
- Walk through the entire file
- Explain signals in depth
- Make this feel like a coding lesson

**One behavior only:**
The collect function — what happens when the player overlaps the coin area.

**Success signal:**
The student reads the function and makes a guess — correct or not. Either answer opens a real conversation.

**Nodes used:** None — this is a script reading exercise.

**Dev needed:** No.

**Coach tip:** If the student says "I don't understand it" — that is fine. Say: "That's okay. What words do you recognize?" Let them find `queue_free()` or `emit_signal` or `score` on their own. One word is enough.

---

## Lesson 10 — First Feature Request

**Goal:** The student designs something new, approves a Dev plan, and places the result.

**What the student does:**
- Tells the Coach what they want to add
- Works with the Coach to turn the idea into a concrete spec
- Approves the spec before it goes to the Dev
- Waits for the Dev to build it
- Goes to Godot and does the final placement themselves
- Plays the game and decides if it feels right

**What the Coach says:**
> "Now you're the game designer. What do you want to add? More coins? A new platform section? A harder jump? Something that makes the game more fun for you? Tell me what you want and we'll make it happen."

**Coach process:**
1. Listen to the idea
2. Ask one sharpening question: "Where do you want it?" or "How hard should it be to get?"
3. Draft the spec together
4. Show the student the draft: "Does this match what you meant?"
5. Only send to Dev after student approves
6. When Dev delivers, tell student: "Go to Godot. The Dev placed the pieces. You decide exactly where they go."

**Success signal:**
The student places the delivered feature themselves and plays it. They say something like "yes, that's what I wanted" or "actually, let's move it."

**Dev needed:** Yes — implements whatever the student designed.

**Coach tip:** This lesson has no fixed content. The student's idea is the content. The Coach's job is to help them express it clearly enough for the Dev to build it. If the idea is too big, help them scope it: "Let's start with one part of that. Which part do you want first?"

---

## Node Reference — Main.tscn

For quick reference, confirmed nodes from the actual scene:

**Platforms:**
- `StartFloor` — starting ground
- `Step1`, `Step2`, `Step3`, `Step4` — staircase platforms
- `FinalFloor` — goal platform

**Coins:**
- `CoinStart`, `Coin1`, `Coin2`, `Coin3`, `Coin4`, `CoinGoal`

**Hazards:**
- `Spikes1`, `Spikes2`

**Progression:**
- `Checkpoint1`
- `SpawnPoint`
- `GoalArea`

**Decorative:**
- `TreeStart`, `TreeStep2`, `TreeStep4`, `TreeGoal`
- `StartBackdrop`, `GoalBackdrop`, `GoalPillar`

**Background (parallax):**
- `BGBack1/2/3`, `BGFront1/2/3`, `CloudsBack1/2/3`, `CloudsFront1/2/3`

**Audio:**
- `StartSfx`, `WinSfx`, `LoseSfx`, `CoinSfx`

**TileMap:**
- Not yet in scene. Added by Dev in Lesson 7.
