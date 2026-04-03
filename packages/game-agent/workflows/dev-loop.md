# DEV LOOP — How Each Feature Gets Built

Adapted from BMAD's `bmad-dev-story` workflow.
This is the core loop that repeats for EVERY task in the task board.

---

## The Loop

```
PICK TASK → READ SKILL → IMPLEMENT → VERIFY → UPDATE STATE → NEXT
```

---

## Step 1: Pick the Next Task

1. Read `task-board.md`
2. Find the first task in TODO
3. Check dependencies (is everything it needs already DONE?)
4. Move it to IN PROGRESS

If a dependency is missing:
- Skip to the next task that CAN be done
- Or go back and build the dependency first

---

## Step 2: Announce and Explain

Tell the student what's happening:

> "Let's add [feature name]! This will [what it does in simple terms]."

If the feature introduces a new Godot concept, explain it briefly:

> "We're going to use something called an Area2D. Think of it like an invisible zone — when the player walks into it, something happens."

---

## Step 3: Read the Skill File

1. Check `/skills/` for a matching skill file
2. If a skill exists: follow its instructions exactly
3. If no skill exists: use general Godot knowledge, but follow the same pattern (create scene → write script → attach → configure)

---

## Step 4: Implement

Create files in this order:

1. **Assets first** (placeholder sprites, sounds)
2. **Scene file** (.tscn) — create the node tree
3. **Script file** (.gd) — write the behavior
4. **Wire it up** — attach script to scene, connect signals, set properties
5. **Integrate** — instance the scene in the level, connect to existing systems

### Implementation Rules
- Create ONE complete feature at a time
- Never leave a half-built feature
- If something is too complex, break it into sub-tasks
- Use placeholder assets — don't block on art
- Always use @export for values the student might change

---

## Step 5: Explain What Was Done

Brief summary for the student:

> "I created a Coin scene — it's a yellow circle that disappears when you walk into it. Each coin adds 1 point to your score."

Keep it to 2-3 sentences. Don't explain every line of code unless asked.

---

## Step 6: Test Instructions

Tell the student exactly how to verify:

> "To test:
> 1. Press F5 to run the game
> 2. Walk into a coin
> 3. It should disappear and your score should go up by 1
>
> Did it work?"

---

## Step 7: Handle Results

### If it works:
> "Awesome! That's working perfectly. Let's move on!"
→ Continue to Step 8

### If it doesn't work:
1. Ask what the student sees
2. Check the skill file's "Common Problems" table
3. Fix the issue
4. Test again

> "Hmm, let me check... [diagnoses] ... Got it! The problem was [simple explanation]. I fixed it. Try again!"

### If the student wants to change something:
> "Sure! What would you like different?"
→ Adjust, re-test, then continue

---

## Step 8: Update State

After EVERY completed task:

1. **task-board.md**: Move task from IN PROGRESS → DONE
2. **current-status.md**: Update progress, last action, next step
3. **session-log.md**: Add entry with date and what was done
4. **project-context.md**: Update scenes/autoloads/inputs if changed

---

## Step 9: Transition or Continue

Check:
- Are there more tasks in TODO? → Pick next task (Step 1)
- Are all "Must Have" tasks DONE? → Suggest moving to POLISH phase
- Is the student tired/done for now? → End session properly (update all state)

---

## Session Boundaries

### Starting a Session
1. Read ALL state files
2. Find the current IN PROGRESS or next TODO task
3. Summarize where we are
4. Continue from there

### Ending a Session
1. Finish current task (or revert if incomplete)
2. Update all state files
3. Summarize what was accomplished
4. Preview what's next

> "Great session! We added [features]. Next time we'll work on [next tasks]. See you soon!"
