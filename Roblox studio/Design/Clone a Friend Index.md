---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-04
---
# Clone a Friend: Index

The collection menu for Modifiers and Bosses. The glossary terms (Index, Found, Index Group, Index Luck) and ADR 0013 are in the place (`ServerStorage.Docs`). See also [[Clone a Friend Modifiers]] and [[Clone a Friend Feedback 2026-11-04]].

Inspiration: [[Steal a Brainrot]] (silhouettes for unowned entries, a reward at a percentage of a group), [[Catch Bugs!]] and [[Fisch]] (discovery count, bestiary).

## Decisions (grilling, 2026-11-04)
| Topic | Decision |
|---|---|
| Purpose | A **collection**: unfound entries are dark silhouettes with "???", but their chance stays visible (the chase). |
| Modifiers tab | The 23 Modifiers. **Found** when one lands in your own Clone Tube (even if you reroll it). Card: Modifier card effects, a coloured orb with the Cash multiplier, name, chance, Aura Level. |
| Bosses tab | **Every Boss × Modifier**: 10 Bosses × 24 (plain + 23) = 240. A column of Boss buttons (x/24) outside the window; picking one shows its 24 cards with a 3D Boss picture (black until Found). **Found** = you defeated that exact Boss + Modifier. |
| Reward | **Index Luck**: each of the 11 groups pays +5% Luck at 25 / 50 / 75 % Found (up to +165%), claimed with a CLAIM button. It multiplies with the Gem Shop Luck, Pets and Luck Boost, and counts toward the server's combined Luck. |
| Old saves | Everyone starts empty; owned Friends and Pets don't count. |
| Placement | New sidebar button "Index" (book) with a notification count; MODIFIERS / BOSSES tabs in the header. |

## Why milestones and not 100%
A full Boss group needs a Genesis Boss kill (about 1/150B for the Obsidian Dragon), so a completion-only bonus would never pay out. Milestones keep rewards coming while the top end stays a flex.
