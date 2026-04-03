# HELP SYSTEM

Inspired by BMAD's `bmad-help` skill — an always-available guide that tells the student (and agent) what to do next.

---

## How It Works

When the student says "help", "what do I do?", "I'm stuck", or anything similar, the agent:

1. Reads `current-status.md`
2. Reads `task-board.md`
3. Determines the current phase
4. Gives specific, actionable guidance

---

## Help Responses by Phase

### Phase: No Game Chosen Yet

> "We haven't picked a game type yet! Let's start there.
> What kind of game do you want to make?
> 1. Top-down (walk around and explore)
> 2. Platformer (run and jump)
> 3. Puzzle (solve challenges)
> 4. Surprise me!"

### Phase: DREAM (Answering Questions)

> "We're figuring out what your game will be like!
> I still need to know: [next unanswered question from QUESTIONS.md]
> Or if you're ready, say 'let's build it!' and I'll use defaults for the rest."

### Phase: DESIGN (Planning)

> "We're planning how to build your game.
> Right now I'm setting up: [current design task]
> Once the plan is ready, we'll start building!"

### Phase: BUILD (In Progress)

> "We're building your game!
> Here's where we are:
> ✅ Done: [list done tasks]
> 🔨 Current: [current task]
> 📋 Next up: [next 2-3 tasks]
>
> Want to keep going with [current task], or do something else?"

### Phase: BUILD (Task Complete, Needs Testing)

> "I just finished [feature name]!
> Let's test it:
> [test instructions]
> Did it work? Tell me 'yes' or what went wrong."

### Phase: POLISH

> "Your game is almost done! Let's make it awesome.
> Still to polish:
> [list remaining polish items]
> Or try playing through the whole game and tell me what feels weird!"

### Phase: COMPLETE

> "Your game is DONE! 🎮
> You can:
> 1. Add more features (tell me what)
> 2. Start a new game
> 3. Just play and enjoy it!"

---

## Stuck / Error Help

When the student reports something isn't working:

1. Ask what they see (error message? nothing happens? wrong behavior?)
2. Check the most common problems from the relevant skill file
3. Suggest a fix
4. If the fix doesn't work, offer to revert and try again

> "That's okay! Bugs happen to everyone. Let's figure it out together.
> Can you tell me exactly what happens when you [action]?"

---

## "What Can I Do?" Response

When the student asks what's possible:

> "Here's what we can do right now:
> - Keep building (next task: [task])
> - Change something we already built
> - Add something new to the game
> - Test what we have so far
> - Take a break and come back later (I'll remember where we left off!)
>
> What sounds good?"
