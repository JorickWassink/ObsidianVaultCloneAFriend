---
kind: RemoteFunction
direction: Client → Server
payload: none
validated: false
rate_limited: false
fired_by:
  - "[[HUDController]]"
handled_by:
  - "[[DataManager]]"
tags: [remote]
---
# RequestData

Client asks for its own data once on join.

## Server validation
- [ ] Only return the calling player's own data
- [ ] Rate limit
