---
type: ModuleScript
location: ServerScriptService
runs_on: Server
status: Done
depends_on:
  - "[[Config]]"
features:
  - "[[Coin collection]]"
  - "[[Shop]]"
tags: [script]
---
# DataManager

## Purpose
Loads and saves player data ([[PlayerData]]). Session-locks profiles, auto-saves every 60 s, saves everyone on `game:BindToClose`.

## API
- `DataManager.Get(player) -> table?`
- `DataManager.AddCoins(player, amount)`
- `DataManager.Spend(player, amount) -> boolean`
