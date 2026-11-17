---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-04
---
# Clone a Friend: feedback round 2026-11-04

The game's glossary and ADRs live in the place (`ServerStorage.Docs`). This round added ADR 0011 and ADR 0012 there, and a change list at the end of `ServerStorage.README`. See also [[Clone a Friend Modifiers]].

## Decisions (grilling)
| Topic | Decision |
|---|---|
| Weapon picker | The Friend popup's Weapon window is removed. Weapons are given from the Weapons tab (card → Friend picker) or with **Equip Best**. Fighters get an "Unequip" button in the popup. |
| Lock | Free, at most **3** Locked Friends, can be taken off again. Consumables tabs hidden while there are none (ADR 0011, supersedes 0004). |
| Boss Cash | **Fixed per Boss**: 5K · 15K · 40K · 100K · 250K · 600K · 1.5M · 4M · 10M · 25M × √(Modifier Multiplier). Same for every winner; damage share only scales Gems (ADR 0012). |
| Station prices | 10 · 80 · 400 · 1.5K · 6K · 25K · 100K · 400K · 1.5M (Money Printer is now a post-first-Rebirth goal). |
| Stock odds | Stations +0.1 each; Weapons 0.85 / 0.7 / 0.55 / 0.4 / 0.25 (Laser Sword about one every 6 min). |
| Boss end | Full **Boss Result** window: Victory (Cash/Gems count-up, damage %, Pet + Equip) or Defeated (Health left + tip). |
| Daily Wheel | Stud UI game-show wheel: stud rim with blinking bulbs, two-tone slices, outlined icons, ticking pointer, idle spin. |
| Pity lever FX | Glow + sparks + shock ring + chime on the lever when a pull lands on a Clone Pity roll. |
| Pity text | Shows the pity's own multiplier (x100 / x2.5K, Boss x50 / x1K), not the player's Luck. |

## Window headers
"Topbar backgrounds" = a thin line out of the top-left of every window header. It was the "HeaderFine" glass-streak reflection: on a wide header the gradient stripe stretches into a long flat line coming from under the icon. Removed from window headers, the Fighters topbar, tooltip headers and the Boss bar. The stud texture stays as it was (creator: the studs were fine).
