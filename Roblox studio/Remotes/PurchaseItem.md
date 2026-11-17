---
kind: RemoteFunction
direction: Client → Server
payload: itemId (string)
validated: true
rate_limited: true
fired_by:
  - "[[ShopController]]"
handled_by:
  - "[[DataManager]]"
tags: [remote]
---
# PurchaseItem

Returns `success: boolean, newBalance: number`.

## Server validation
- [x] itemId exists in [[Config]]
- [x] Price read from server-side Config, never from the client
- [x] Rate limit
