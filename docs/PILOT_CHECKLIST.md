# Pilot Observation Checklist

This file defines what we expect to observe in a student pilot session.
It is used before and after each pilot to measure what worked and what needs refinement.

Treat each item like a test. Define the expectation first. Observe against it. Do not interpret afterward based on feeling.

---

## How To Use This Checklist

Before the pilot: read the full checklist so you know what to watch for.
During the pilot: note what you see against each item. Do not intervene unless the student is completely stuck.
After the pilot: mark each item pass or fail. Write one sentence of what you observed. Use that to refine the system.

---

## Section 1 — Onboarding and Environment

### 1.1 Repo access and project generation
**Expected:** The Dev clones the repo, generates the project, and confirms readiness without asking the student to perform any technical steps.
**Pass:** Student sees the game is ready without doing any setup themselves.
**Fail:** Student is asked to fix PATH issues, run commands, or perform environment configuration manually before generation is complete.

### 1.2 Godot availability
**Expected:** The Dev detects Godot automatically or self-heals the path before asking the student to act.
**Pass:** Student is not asked to install or locate Godot until the Dev confirms it truly cannot be found automatically.
**Fail:** Student is told to install Godot as the first instruction, before the Dev has attempted detection.

### 1.3 First Dev thread introduction
**Expected:** The student understands the copy-paste envelope ritual on first use.
**Pass:** Student copies the envelope message and pastes it into the Dev thread without needing a second explanation.
**Fail:** Student does not understand what to copy, why they are switching threads, or what the Dev thread is for.

---

## Section 2 — Coach Behavior

### 2.1 Coach does not start with code
**Expected:** The Coach reaches Lesson 9 before any script is opened or explained.
**Pass:** No code is shown or explained before the student explicitly reaches Lesson 9.
**Fail:** The Coach explains a script, a function, or code architecture at any earlier lesson.

### 2.2 Coach asks focused questions
**Expected:** When the student is vague, the Coach asks one focused sharpening question, not multiple questions at once.
**Pass:** Coach asks one question at a time and waits for the answer.
**Fail:** Coach asks two or more questions in the same message, or launches into an explanation instead of asking.

### 2.3 Coach adapts when the student goes off-script
**Expected:** The session feels like a conversation, not a reading of a fixed script.
**Pass:** When the student says something unexpected, the Coach responds naturally and returns to the lesson flow smoothly.
**Fail:** The Coach ignores the student's actual words and continues with scripted instructions regardless of what was said.

### 2.4 Coach introduces Dev thread only when needed
**Expected:** Dev thread is introduced at initial generation and then again only when a lesson requires a filesystem change.
**Pass:** Student does not hear about the Dev thread in the middle of a lesson where no filesystem change is needed.
**Fail:** Coach mentions or opens the Dev thread unnecessarily during lessons 2–6.

---

## Section 3 — Student Behavior by Lesson

### 3.1 Lesson 1 — First Wow
**Expected:** Student clearly engages with the running game.
**Pass:** Student reacts — excitement, curiosity, questions about the game itself, or wanting to play more.
**Fail:** Student does not understand what happened, does not know what to do next, or looks confused about whether the game is supposed to do something.

Note: silence alone is not failure. Some students go quiet when amazed. Watch for engagement, not noise.

### 3.2 Lessons 2–3 — First Control and First Tiny Build
**Expected:** Student can find a named node in the Scene Tree and move it without needing the instruction repeated.
**Pass:** Student locates `StartFloor` or `Step1` in the Scene Tree on their own after one clear instruction.
**Fail:** Student cannot find the node, does not know which panel to look in, or needs the same instruction more than twice.

### 3.3 Lessons 4–6 — Duplicate and Place
**Expected:** Student can duplicate a node with Ctrl+D and move the copy to a new position.
**Pass:** Student duplicates a node, sees the copy appear, and moves it without confusion about where the copy went.
**Fail:** Duplication confuses the student, they cannot find the copy in the Scene Tree, or they do not understand that the copy is a new separate object.

### 3.4 Lesson 7 — First World-Building (TileMap)
**Expected:** Student can paint tiles and walk on them in-game. Cognitive load stays manageable.
**Pass:** Student finds the tile palette, paints at least a few tiles, presses Play, and walks on them. They understand what they painted.
**Fail:** Student gets lost in the TileMap workflow, needs repeated rescue, does not understand what the palette is for, or cannot connect the painting action to the result in-game.

Time is a secondary signal only. If the student is engaged and progressing, time is not the measure. If the student is confused and not progressing, that is the fail signal regardless of time.

### 3.5 Lessons 8–9 — Polish and Code Look
**Expected:** Student moves a decorative object without needing technical explanation. Student reads one function and makes a guess about what it does.
**Pass:** Student moves a tree or background item and notices the visual result. Student reads `scripts/collectibles/coin.gd`, finds the collect function, and offers any interpretation at all.
**Fail:** Student cannot find the decorative nodes. Student refuses to read the script or says it is completely meaningless to them after the Coach's prompt.

### 3.6 Lesson 10 — First Feature Request
**Expected:** Student can articulate something they want to add. Coach helps them turn it into a spec. Student approves it before it goes to the Dev. Student does final placement themselves.
**Pass:** Student names a feature idea. Coach refines it into a concrete spec. Student approves. Dev delivers. Student places it in Godot and reacts to the result.
**Fail:** Student cannot think of anything to add. Or Coach writes the spec without student input. Or student does not do final placement — the Dev positions everything.

---

## Section 4 — Overall Session Quality

### 4.1 Student feels ownership
**Expected:** At some point the student says or implies "this is my game."
**Pass:** Student refers to decisions they made — "I put that spike there", "I want more coins", "I designed that jump."
**Fail:** Student treats the game as something the AI made and they are just watching.

### 4.2 Student wants to continue
**Expected:** At the end of the session, the student wants to keep going.
**Pass:** Student asks "what can we do next?" or resists ending the session.
**Fail:** Student seems relieved it is over or disengaged before the session ends.

---

## After Each Pilot — What To Record

For each fail item, write:
- What the student actually did or said
- What we think caused it
- One specific change to make to `learning/coach.md` or `learning/lessons/platformer.md`

Do not make more than three changes between pilots. Test one thing at a time.

---

## Current Pilot Status

| Pilot # | Date | Student profile | Items passed | Items failed | Changes made |
|---|---|---|---|---|---|
| 1 | TBD | TBD | TBD | TBD | TBD |
