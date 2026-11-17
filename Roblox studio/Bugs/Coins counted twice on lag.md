---
status: Open
severity: High
found_in:
  - "[[CoinService]]"
platform: All
reported: 2026-10-28
tags: [bug]
---
# Coins counted twice on lag

## Steps to reproduce
1. Add incoming replication lag in Studio settings (Network → Incoming Replication Lag = 0.3).
2. Touch a coin.

## Expected
+1 coin.

## Actual
Sometimes +2: the coin isn't marked collected before the second request arrives.

## Fix
Mark the coin collected before paying out.
