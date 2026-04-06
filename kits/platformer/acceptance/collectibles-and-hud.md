# Collectibles And HUD Acceptance

## Feature/System Name

Collectibles, score, and HUD

## Pass/Fail Criteria

- Pass if coins collect once, score increases immediately, HUD text updates immediately, and collectible state resets or restores correctly.
- Fail if coins do not disappear, score/HUD lag behind, or restart/checkpoint restore leaves collectible state inconsistent.

## Manual Verification Scenario

1. Start the run.
2. Collect at least one coin.
3. Confirm the coin disappears and score/HUD update.
4. Collect all required coins and confirm the objective text changes.
5. Restart and confirm the correct collectible state returns.

## Expected Automated Coverage

- Coin collection hides the coin and disables collision.
- Coin reset restores visibility and collision.
- Main scene score and HUD labels update after collection.
- Restart and checkpoint restore apply the expected collectible state.
