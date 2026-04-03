# Coins And HUD Spec

## Goal

Add collectible coins and a HUD that tracks score during the run.

## Requirements

- Coins appear along the staircase course.
- Touching a coin collects it.
- Collecting a coin increases score by 1.
- Coin collection plays a sound.
- The HUD displays current score and collected coins out of total.
- Restart resets score and restores all coins.

## Acceptance Criteria

- Each coin disappears when collected.
- Score increments immediately after collection.
- HUD updates immediately after collection.
- All coins return after restart.
- The HUD remains visible during gameplay.

## Assets / Inputs

- Coin sprite: `assets/collectibles/coins/coin4.png`
- Coin sound: `assets/audio/sfx/coin_collect.mp3`

## Notes

- Coin behavior should be reusable via a dedicated coin scene.
