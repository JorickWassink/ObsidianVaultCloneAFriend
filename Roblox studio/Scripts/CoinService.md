---
type: Script
location: ServerScriptService
runs_on: Server
status: In progress
depends_on:
  - "[[DataManager]]"
  - "[[Config]]"
features:
  - "[[Coin collection]]"
tags: [script]
---
# CoinService

## Purpose
Spawns coins, handles [[CollectCoin]], checks distance, pays out through [[DataManager]] and fires [[UpdateCoins]].

## Notes
- Distance check: player must be within 12 studs of the coin.
- See bug [[Coins counted twice on lag]].
