---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-06
---
# Clone a Friend: Stations and Weapons update

The game's glossary and ADRs live in the place (`ServerStorage.Docs`). See also [[Clone a Friend Modifiers]].

## Decisions (grilling, 2026-11-06)
| Topic | Decision |
|---|---|
| Amount | 6 new Stations, 5 new Weapons |
| Ladder | Mostly above the current top, a few in the gaps |
| Station theme | Sillier as they get pricier |
| Weapon theme | Fantasy to sci-fi to cosmic, carrying on from the Laser Sword |
| Top Weapon | Moderate: x40, because Boss Health is fixed (ADR 0008) and every stronger Weapon makes Bosses easier |
| Size | Gold Mine and Time Machine are 5x5 Squares; the rest stay 3x3 to 4x4 |
| Old Stations | All 9 rebuilt in Blender in the Clone Tube style: same size, price and income, moving parts keep working |
| Old Weapons | Stay as they are |
| Review | Renders of every model first; nothing goes in the game before the creator's OK |
| Each new Station | Its own work pose, held prop, sound and machine animation |

## New Stations
| Station | Cash | Income | Place in the ladder |
|---|---|---|---|
| Ice Cream Cart | 3K | 6/s | gap: Burger Grill to Pizza Oven |
| Arcade Machine | 50K | 18/s | gap: Computer to Streaming Desk |
| Rocket Workshop | 6M | 350/s | above Money Printer |
| Robot Factory | 25M | 800/s | above Money Printer |
| Gold Mine | 100M | 2K/s | above Money Printer, 5x5 |
| Time Machine | 500M | 5K/s | top, 5x5 |

Stock gets rarer the higher a Station sits.

## New Weapons
| Weapon | Cash | Damage | Place in the ladder |
|---|---|---|---|
| Crystal Spear | 150K | x6 | gap: Battle Axe to War Hammer |
| Plasma Axe | 25M | x16 | above Laser Sword |
| Thunder Hammer | 100M | x22 | above Laser Sword |
| Void Scythe | 500M | x30 | above Laser Sword |
| Galaxy Greatsword | 2.5B | x40 | top |

Weapons only change Damage, no abilities (glossary: Weapon).

## Built (2026-11-08)
- Models: `Assets/Stations and Weapons/StationsAndWeapons.blend` (render sheets next to it). Uploaded as assets 99093453012041 (Stations) and 88802371460416 (Weapons).
- Old Stations keep their invisible original parts for collisions, seats, screens and animations; a backup of the old look is in `ServerStorage.BuildItems_OldParts`.
- New Stations reuse sounds already in the game (washer hum, keyboard, fire crackle, printer, sandpaper, bubbles). Swap them for better Creator Store sounds later.
- Gold Mine work animation: a heavy pickaxe chop every 1.5 s (wind-up, hold, fast chop, bounce) with gold sparks on the hit.
