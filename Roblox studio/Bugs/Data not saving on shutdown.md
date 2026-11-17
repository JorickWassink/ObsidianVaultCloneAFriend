---
status: Fixed
severity: High
found_in:
  - "[[DataManager]]"
platform: All
reported: 2026-10-20
tags: [bug]
---
# Data not saving on shutdown

## Fix
Added `game:BindToClose` that saves every loaded profile.
