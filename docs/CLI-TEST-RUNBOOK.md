# CLI Test Runbook

**Audience: Operator / platform tester**
**Not student-facing. Not product behavior documentation.**

This runbook documents how to test the full student loop using Codex CLI.
It captures what was proven to work in April 2026 and why each test exists.

---

## When To Use Which Test

| Test | What it proves |
|---|---|
| URL-only startup | Student's first message works — CLI reaches Kaya from an empty folder |
| Strict Kaya publish handoff | Coach behavior is correct — Kaya produces the right PM→Dev envelope |
| Strict Dev publish | Publish contract works — Dev runs publish and returns the correct report |

Run them in order. Each one builds on the previous.

---

## Prerequisites

- Codex CLI installed (`codex --version`)
- VM slot provisioned for the student handle
- Student package ready at `secure-student-packages/<user>--game/` containing:
  - `publish.toml` with `ssh_key_path = "keys/<user>_game_deploy"`
  - `keys/<user>_game_deploy` private key file

---

## Step 1 — Create and generate a fresh session folder

```bash
mkdir -p /Users/zyahav/Documents/dev/<session-folder>
cd /Users/zyahav/Documents/dev/<session-folder>
git clone https://github.com/zyahav/g-game-platform .
python3 scripts/generate_project.py --kit platformer --output . --in-place-root
```

Then copy the student package in:

```bash
cp /path/to/secure-student-packages/<user>--game/publish.toml .
cp -R /path/to/secure-student-packages/<user>--game/keys .
```

---

## Test A — URL-only startup test

**What it proves:** The student's first message (pasting the GitHub URL) correctly reaches Kaya from a truly empty folder.

```bash
rm -rf /Users/zyahav/Documents/dev/test-url-only
mkdir -p /Users/zyahav/Documents/dev/test-url-only

codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  -C /Users/zyahav/Documents/dev/test-url-only \
  "https://github.com/zyahav/g-game-platform"
```

**Pass:** CLI clones the repo, reads the learning layer, and outputs:
```
Hi, I'm Kaya! What's your name?
```

**Known rough edge:** After cloning, CLI may search for `AGENTS.md` (which does not exist). This causes a nonzero shell exit. The agent recovers automatically and still reaches Kaya. This is cosmetic — do not treat it as a failure.

---

## Test B — Strict Kaya publish handoff test

**What it proves:** Kaya correctly recognizes a publish request and returns the exact PM→Dev envelope.

Run from an already-generated project folder (after Step 1):

```bash
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  -C /Users/zyahav/Documents/dev/<session-folder> \
  "You are Kaya, the Coach, in an already-generated student project.
Read only these files:
- /Users/zyahav/Documents/dev/<session-folder>/learning/kaya/Mission.md
- /Users/zyahav/Documents/dev/<session-folder>/learning/kaya/Boundaries.md
- /Users/zyahav/Documents/dev/<session-folder>/learning/kaya/Playbook.md
- /Users/zyahav/Documents/dev/<session-folder>/state/student.md
Do not read onboarding, lessons, README, or any other files.
The student name is Test.
The student says: 'I want to publish my game'.
Reply exactly as Kaya would reply to the student.
If the correct action is to hand to Dev, include the exact PM-to-Dev envelope Kaya would ask the student to paste.
Do not include analysis. Do not inspect anything else."
```

**Pass:** Kaya outputs the correct envelope:
```
--- START: PM TO DEV ---
The student wants to publish the game.
Read publish.toml.
If any required fields are empty, ask for only those values.
Then run `make publish` or `python3 scripts/project_tasks.py publish`.
Report back with the live URL when done.
--- END: PM TO DEV ---
```

**Known rough edge:** CLI may leak internal thinking lines before the final Kaya output. This is cosmetic. The actual Kaya reply at the end is what matters.

---

## Test C — Strict Dev publish test

**What it proves:** Dev reads the right files, runs publish, and returns the structured DEV→PM report envelope. Network access works.

```bash
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  -C /Users/zyahav/Documents/dev/<session-folder> \
  "You are the Dev in a generated student project.
Read only these files:
- /Users/zyahav/Documents/dev/<session-folder>/AGENT.md
- /Users/zyahav/Documents/dev/<session-folder>/publish.toml
- /Users/zyahav/Documents/dev/<session-folder>/scripts/project_tasks.py
Then process this exact PM message:
--- START: PM TO DEV ---
The student wants to publish the game.
Read publish.toml.
If any required fields are empty, ask for only those values.
Then run make publish or python3 scripts/project_tasks.py publish.
Report back with the live URL when done.
--- END: PM TO DEV ---
Output only this exact envelope:
--- START: DEV TO PM ---
RESULT: SUCCESS | FAIL
PUBLIC_URL: ...
EXPORT: PASS | FAIL | NOT_RUN
VALIDATION: PASS | FAIL | NOT_RUN
DEPLOY: PASS | FAIL | NOT_RUN
DETAIL: one short sentence only if needed
NEXT_ACTION: one short sentence
--- END: DEV TO PM ---
No prose outside the envelope."
```

**Pass:** Dev outputs a SUCCESS envelope with the correct public URL.

**Known rough edge:** CLI may leak internal thinking lines before the final envelope. The envelope itself is what matters.

---

## Step 6 — Verify live URL

```bash
curl -sI https://games.zurot.org/<user>/game/ | grep "HTTP\|content-type"
```

**Pass:** `HTTP/2 200` and `content-type: text/html`

---

## Important Notes

- `--dangerously-bypass-approvals-and-sandbox` is **required** on Mac for publish to work — without it, SSH push fails with DNS resolution errors inside the Codex sandbox
- Strict context prompts (Test B and C) are what make Kaya and Dev behave cleanly — loose prompts drift
- `--dangerously-bypass-approvals-and-sandbox` gives Codex full system access — only use on trusted machines
- The URL-only test (Test A) and the strict tests (B and C) prove different things — run both

---

## Proven Results (April 2026)

| Test slot | URL | Result |
|---|---|---|
| test1/game | https://games.zurot.org/test1/game/ | PASS |
| test2/game | https://games.zurot.org/test2/game/ | PASS |
| test3/game | https://games.zurot.org/test3/game/ | PASS |
| test4/game | https://games.zurot.org/test4/game/ | PASS |
