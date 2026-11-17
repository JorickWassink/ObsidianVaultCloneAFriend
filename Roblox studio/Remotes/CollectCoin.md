---
kind: RemoteEvent
direction: Client → Server
payload: coinId (string)
validated: true
rate_limited: false
fired_by:
  - "[[HUDController]]"
handled_by:
  - "[[CoinService]]"
tags: [remote]
---
# CollectCoin

## Payload
| Arg | Type | Notes |
|-----|------|-------|
| coinId | string | ID of the coin touched |

## Server validation
- [x] Type-check every argument
- [x] Coin exists and player is within 12 studs
- [ ] Rate limit (max ~10/s)
