---
datastore: PlayerData
store_type: DataStore
key_pattern: "Player_{UserId}"
version: 2
tags: [data]
---
# PlayerData

Managed by [[DataManager]].

## Schema
| Field | Type | Default | Notes |
|-------|------|---------|-------|
| coins | number | 0 | |
| rebirths | number | 0 | |
| upgrades | {[string]: number} | {} | itemId → level |
| lastDaily | number | 0 | os.time() of last claim |
| version | number | 2 | |

## Migrations
- **v1 → v2:** added `lastDaily` (default 0).
