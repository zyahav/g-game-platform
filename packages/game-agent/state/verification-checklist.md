# VERIFICATION CHECKLIST

Run this checklist after implementing ANY feature.

---

## 1. Files Check
- [ ] All new files are in the correct folders (scenes/, scripts/, assets/)
- [ ] File names follow snake_case convention
- [ ] No files left in the project root

## 2. Scene Check
- [ ] Every scene has a proper root node type
- [ ] Every physics body has a CollisionShape2D
- [ ] Scripts are attached to the correct nodes
- [ ] Node names follow PascalCase

## 3. Script Check
- [ ] Script has a comment at the top explaining what it does
- [ ] No magic numbers (use @export or constants)
- [ ] Signals are connected (either in code or editor)
- [ ] No hardcoded node paths longer than 2 levels deep

## 4. Integration Check
- [ ] New feature works with existing features
- [ ] No errors in the Godot console
- [ ] No warnings that affect gameplay

## 5. User Can Test
- [ ] Told the user HOW to test (which key to press, what to look for)
- [ ] Told the user what SUCCESS looks like
- [ ] Told the user what to do IF IT FAILS

## 6. State Updated
- [ ] `/state/current-status.md` updated
- [ ] `/state/task-board.md` — task moved to DONE
- [ ] `/state/session-log.md` — entry added
