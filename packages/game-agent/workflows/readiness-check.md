# IMPLEMENTATION READINESS CHECK

Adapted from BMAD's `bmad-check-implementation-readiness` workflow.
Run this BEFORE starting Phase 3 (BUILD).

---

## Purpose

This is a gate check. Before writing any code, verify that everything is in place. This prevents wasted effort and confusion.

---

## Checklist

### 1. Game Design Complete
- [ ] Game type is chosen and recorded in `current-status.md`
- [ ] All template questions answered (or defaults chosen)
- [ ] Game Design Document (`docs/game-design.md`) exists and is filled in
- [ ] Student has confirmed the concept

### 2. Task Board Ready
- [ ] `task-board.md` has tasks in TODO
- [ ] Tasks are ordered by dependency
- [ ] Each task is small enough to complete in one step (5-15 min)
- [ ] No task depends on something that isn't planned

### 3. Project Structure Exists
- [ ] `project.godot` exists
- [ ] Folder structure matches RULES.md (assets/, scenes/, scripts/)
- [ ] No files in wrong locations

### 4. Prerequisites Verified
- [ ] Godot Engine is available on the student's machine
- [ ] Project can be opened in Godot
- [ ] Agent has file access to the project directory

### 5. Context Files Updated
- [ ] `project-context.md` exists with correct game type and conventions
- [ ] `current-status.md` shows Phase = DESIGN complete

---

## Result

| Outcome | Action |
|---------|--------|
| **ALL PASS** | Proceed to BUILD phase |
| **MINOR ISSUES** | Fix them quickly, then proceed |
| **MAJOR GAPS** | Go back to DESIGN phase and complete missing items |

---

## Agent Behavior

If the check fails:

> "Before we start building, let me make sure everything is ready..."
> [runs through checklist]
> "I noticed [issue]. Let me fix that first, then we'll start building!"

The agent fixes issues silently when possible, and only asks the student when their input is needed.
