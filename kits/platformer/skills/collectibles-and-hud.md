# Skill: Collectibles And HUD

Use this skill when adding reusable pickups, score, and HUD feedback.

## Purpose

Keep collectibles reusable and make progression visible through immediate UI feedback.

## Pattern

- Implement collectibles as reusable `Area2D` scenes with their own scripts and signals.
- Let the main scene listen for collection events and update score and HUD state.
- Keep collectible reset logic reusable so restart and checkpoint restore can reuse the same code path.

## Proven Behaviors

- Coin collection hides the coin, disables collision safely, and emits a value signal.
- HUD labels update immediately after collection.
- Objective text changes when all required collectibles are gathered.

## Verification

- Test collectible visibility/collision changes.
- Test score/HUD updates in the main scene.
