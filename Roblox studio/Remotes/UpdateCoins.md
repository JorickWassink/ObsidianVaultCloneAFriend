---
kind: RemoteEvent
direction: Server → Client
payload: coins (number)
validated: true
rate_limited: true
fired_by:
  - "[[CoinService]]"
handled_by:
  - "[[HUDController]]"
tags: [remote]
---
# UpdateCoins

Server tells the client its new balance. Nothing to validate on the server side.
