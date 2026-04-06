# Core Gameplay Acceptance

## Feature/System Name

Core platformer loop

## Pass/Fail Criteria

- Pass if the player can start, move, jump, finish the course, and restart after win or loss.
- Fail if input does not start the run, movement is broken, or win/lose flow does not stop and restart gameplay correctly.

## Manual Verification Scenario

1. Launch the starter project with `make play`.
2. Start the run.
3. Move and jump across the platforms.
4. Reach the goal after satisfying the progression requirement.
5. Restart and confirm the run begins again correctly.

## Expected Automated Coverage

- Scene loads with required nodes.
- Start transitions to playing state.
- Fall triggers lose state.
- Goal triggers win state once progression requirement is satisfied.
- Restart restores a playable run.
