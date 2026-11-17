---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-03
---
# Clone a Friend: Modifiers

The game's own glossary and ADRs live **inside the place** (`ServerStorage.Docs.CONTEXT`, `ServerStorage.Docs.ADR`), not in this vault. The vault's [[CONTEXT]] is for RNG Shooter, a different game, and rejects Modifiers there.

Inspiration: [[Sols RNG]] (aura looks, tiered roll cutscenes), [[Cutscenes]], [[Popular Gameplay Mechanics]] (mutations/variants).

## Decisions (grilling session, 2026-11-03)
| # | Topic | Decision |
|---|---|---|
| 1 | Existing 13 | Visual rework only. Chances and multipliers unchanged. |
| 2 | New ones | 10 new, all **above Void** (Luck / Pity / sort order of the old 13 untouched). |
| 3 | Tail | Rarest is about 1/150M. Same Luck formula (Luck ^ (position × 0.1)). Pet Boost curve not capped. |
| 4 | Surfaces | Every Modifier shows up everywhere: Friend, Boss, Pet, world name text, Friend/Pet card, Tooltip, Boss Intro band, Boss Bar, Fighters Panel, Clone Tube, clone reveal, chat. Bronze to Gold stay subtle. |
| 5 | Cutscenes | **Modifier Cutscene** from Rainbow up, custom per Modifier, 3 s (Rainbow) to 12 s (Genesis). For the cloner when their tube lands it, and in place of the Boss Intro hold for a Boss with it (squeezed to 9 s). |
| 6 | Skipping | First cutscene of each Modifier always plays; after that a tap skips it. |
| 7 | Sound | Roblox-licensed audio only (Pro Sound Effects / APM), so it plays in any experience. |

## The ladder
| Modifier | Chance | Cash | Look |
|---|---|---|---|
| Bronze | 1/7 | x2 | copper flecks drifting down |
| Silver | 1/14 | x3 | shine sweep, frost glints |
| Gold | 1/40 | x5 | crown of stars circling the head |
| Platinum | 1/100 | x8 | thin halo over the head |
| Emerald | 1/250 | x12 | crystal shards sprouting at the feet |
| Sapphire | 1/500 | x18 | water ring orbiting the waist |
| Ruby | 1/1K | x25 | heartbeat + shock ring at the feet |
| Amethyst | 1/2.5K | x40 | rune motes orbiting the head |
| Diamond | 1/5K | x60 | prism rays fanning out behind |
| Obsidian | 1/10K | x100 | magma cracks in the ground |
| Rainbow | 1/25K | x150 | rainbow arc over the head · *cutscene* |
| Galaxy | 1/50K | x250 | constellation ring · *cutscene* |
| Void | 1/100K | x500 | event-horizon ring underfoot · *cutscene* |
| **Aurora** | 1/250K | x750 | aurora curtains above, body waving green→violet |
| **Inferno** | 1/500K | x1K | burning cracked-lava body, flames, ring of fire |
| **Glacier** | 1/1M | x1.5K | frost creeping up, ice shards, snow, frost breath |
| **Tempest** | 1/2M | x2.5K | storm cloud, rain, lightning striking the body |
| **Toxic** | 1/4M | x4K | pulsing neon slime, drips, bubbles, fumes |
| **Eclipse** | 1/8M | x6K | black body with gold rim, black sun + corona |
| **Glitch** | 1/15M | x9K | parts jumping colours and blinking, pixel cubes |
| **Celestial** | 1/30M | x13K | halo, wings of light, golden feathers |
| **Supernova** | 1/60M | x18K | sucks in light, then BOOMS every 6 s |
| **Genesis** | 1/150M | x25K | cycles every Modifier's colour, all their symbols orbit |

## Aura Levels (2026-11-03, round 3)
Friends work close together inside a building, so the Sol's RNG-style aura (`ReplicatedStorage.AuraFX`) is capped by **Aura Level** (`FriendModifiers.AURA_LEVELS`):

| Level | Modifiers | What they get |
|---|---|---|
| **Calm** | Bronze → Obsidian | Only their own look. No magic circles, rings, pillars or god rays. |
| **Medium** | Rainbow → Toxic | One compact magic circle (~7 studs), one ring, moderate particles. No pillar, no god rays. |
| **Crazy** | Eclipse → Genesis | Circles (≤ 11 studs), up to 3 rings, a halo, a short pillar (16–20 studs) that fades out, small god rays. Celestial and Genesis get wings. Shockwaves ≤ 22 studs. |

The Clone Tube and the cards follow the same levels: no aura for Calm, one circle for Medium, the full set for Crazy. Cutscenes are full-screen, so they stay as they are. New textures: [[Aura Textures]].

## Modifier Showcase (admin only)
Admin menu → **Modifier Showcase** (or `/modshowcase`) teleports you to a stage 1500 studs above the map:
- 23 pedestals in four rising rows, commonest on the left, each with a Friend and a Pet wearing that Modifier, plus a sign with its name, chance and Cash multiplier.
- Rainbow and up: walk to the pedestal, then **E** plays the full cutscene and **R** plays the Boss Intro version (squeezed to 9 s). Showcase cutscenes are always skippable and never count as "seen".
- A card wall at the entrance shows every Modifier's card effect.

## Rewards rework (2026-11-03)
- **Daily Wheel** moved into the Rewards window as a **WHEEL** tab; the Hub wheel was removed (backup in ServerStorage).
- **Login Rewards** (7 days, a missed day only pauses): 15 min Cash · 2 Wheel Spins · 400 Gems · Lucky Clone (Super Lucky from week 3) · x2 Luck 30 min · x2 Cash 30 min · Pet (1/1K+, rising).
- **Playtime Gifts**: 12 over 2 hours (1, 3, 5, 8, 12, 16, 20, 30, 45, 60, 90, 120 min), ending in a Lucky Pet.
- **Wheel**: Cash 22% · 150 Gems 20% · Spin Again 12% · x2 Luck 12% · x2 Cash 12% · 600 Gems 10% · Lucky Clone 8% · 1/1K+ Pet jackpot 4%.
- **Lucky Clone** = next Clone at least 1/100; **Super Lucky Clone** = at least 1/2.5K. Saved until used and used up by the next filled Clone Tube, never the free first Clone.

## Rarity order review (suggestions, not applied)
- **Diamond (1/5K) already uses a rainbow sweep and rainbow glints**, which blurs it with Rainbow (1/25K) two steps later. Consider an icy white-blue prism for Diamond and keep full rainbow for Rainbow/Genesis.
- **Four purples close together**: Amethyst (1/2.5K), Obsidian (1/10K), Galaxy (1/50K), Void (1/100K). Obsidian's purple magma could become orange/red (classic obsidian-and-lava), which would set it apart from Void.
- **Silver (1/14) and Platinum (1/100) are both cool white metals.** Platinum's new halo helps, but a warmer champagne tint would separate them at a glance.
- **Luck scales hard at the top**: Genesis gets Luck^2.3. At x4 Luck it's ~26× likelier (about 1/6M); at x20 Luck about 1/150K. Fine for a chase, but worth watching if Luck upgrades keep climbing.
- The chance and multiplier curve itself is smooth: each step is about 2× rarer and 1.3–1.7× more Cash. No reordering needed.
