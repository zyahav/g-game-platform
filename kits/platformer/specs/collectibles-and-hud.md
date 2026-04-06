# Collectibles And HUD

## Goal

Use reusable collectibles and a HUD to make progress visible during the run.

## Requirements

- Coins appear along the platforming route.
- Touching a coin collects it and increases score.
- The HUD shows score and collected coins out of total.
- The goal objective text updates when all coins are collected.
- Restart restores collectible state according to the current progression rules.

## Acceptance Criteria

- Each coin disappears when collected.
- Score and HUD update immediately after collection.
- The objective text changes when all required coins are collected.
- Restart or checkpoint restore applies the correct coin state.

## Proven Source

- `scenes/collectibles/Coin.tscn`
- `scripts/collectibles/coin.gd`
- `Main.tscn`
- `main.gd`
- `test/unit/test_coin.gd`
- `test/unit/test_main_scene.gd`
