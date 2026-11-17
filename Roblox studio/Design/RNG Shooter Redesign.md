---
tags: [design]
source: RNG Shooter Design Document.pdf
date: 2026-11-02
---
# RNG Shooter Redesign

Outcome of a grilling session on the original PDF and the open RNGShooter place (placeId 88381853779695). Glossary: [[CONTEXT]]. Decisions: [[0001-rarity-gives-options-not-stats|ADR 0001]] · [[0002-rolling-modeled-on-blue-lock-rivals-no-modifiers|ADR 0002]] · [[0003-robux-sells-lucky-rolls|ADR 0003]].

## Decisions
| # | Topic | Decision |
|---|---|---|
| 1 | Rarity | Higher Rarity = more options in a fight, never raw stats. A Common can always win. |
| 2 | Roll result | Many Classes across the 4 existing Rarities. Blue Lock: Rivals style. **No Modifiers.** |
| 3 | Roll source | Earned in Matches. |
| 4 | Opponents | PvP only. Dummies only in the Practice Range. |
| 5 | Options | Everyone keeps Q/E/F; rarer abilities do more (charges, alt-uses, modes). Epic+ get a Passive. |
| 6 | Roster | 16 Classes at launch: 5 Common, 5 Rare, 3 Epic, 3 Legendary. No rule forcing each combat range into every Rarity. "More options" is a loose guideline judged per Class, not a fixed budget. Archetypes: see [[Randomizer]] for wacky inspiration and [[RNG Shooter Roster]]. |
| 7 | Chase | A specific Legendary takes a few hours of play. |
| 8 | Roll rule | A Roll replaces the Equipped Class; the Locker keeps the Classes you want. |
| 9 | Currency | Cash from kills, assists, the Finish Bonus and Daily Quests; fixed price per Roll, about 3 Rolls per Match. |
| 10 | Pity / Lucky | Both. Pity guarantees a Legendary (~150 Rolls); a Lucky Roll can't land on Common. |
| 11 | Robux | Sells Lucky Rolls (ADR 0003). |
| 12 | Locker | 2 slots at the start, more unlocked by Level. |
| 13 | Level | XP from the same Match actions as Cash. |
| 14 | Pity counting | All Rolls, Robux or Cash, share one Pity counter. |
| 15 | Ultimate | Charges from kills, damage and time; everyone gets at least one per Match. |
| 16 | Weapons | Shared types, each Class uses whatever fits its idea; no fixed count. |
| 17 | Platform | Mobile and PC from day one. |
| 18 | Match flow | 12 players; back to the menu after each Match, with a results screen (Cash/XP). |
| 19–23 | Maps | 3 hand-built destructible Maps, voted on during the Intermission. |
| 20 | Current Classes | Rookie, Bruiser, Twin Fang and Phantom are placeholders; design all 16 from scratch. |
| 21 | Touch movement | Context buttons: jump into a wall to climb or wall-jump, crouch while sprinting to slide. Same on PC. |
| 22 | Aim | Light aim assist (slowdown only) for touch; one shared lobby. |
| 24 | Theme | Silly archetypes (janitor, chef, mascot…) with readable weapon types. |
| 25 | First session | Starter Class plus Cash for 3 Rolls; the first Roll is guided. |
| 26 | Leaving | Leave at any time; lose the Finish Bonus, keep earned Cash. Replaces the "M before moving" rule. |
| 27 | Duplicates | Nothing extra. |
| 28 | Vaulting | Yes; owners keep the Class. |
| 29 | Daily Quests | 3 a day, Cash each, plus a Lucky Roll for finishing all 3. |
| 30 | Practice Range | Equipped and Locker Classes only. |
| 41 | Roll weights | Common 60 / Rare 27 / Epic 10 / Legendary 3. A specific Legendary ≈ 1 in 100 Rolls ≈ 3 hours. |
| 42 | Pity | A guaranteed Legendary after 100 Rolls without one (~5% of players reach it); resets on any Legendary. |
| 43 | Lucky Roll weights | 0 / 62 / 28 / 10 (about 3× the Legendary chance, no Commons). |
| 44 | Cash | A Roll costs 100. Kill 50, assist 20, Finish Bonus 100, Daily Quest 300. An average Match ≈ 290 ≈ 3 Rolls. |
| 45 | Map themes | Suburb (outdoor streets), Shopping Mall (indoor, close range, glass), Theme Park (open, rides). |
| 46/49 | Destruction | Every building, floor and prop can be levelled; only the base ground is solid. |
| 47 | Intermission | 20 s; the vote closes at 12 s and the chosen Map loads in the last 8 s. |
| 48 | Daily Quests | A rotating pool that works with any Class (play, kills, damage, destruction, Ultimates); one easy, one medium and one hard each day. |
| 50 | UI style | **Stud UI** (the stud-ui-clean-roblox kit): 3D stud buttons with sticker icons, heavy outlined Montserrat text, stud-header windows (rarity-coloured for the Equipped Class), extruded lime money counter. Replaces a short-lived clean-FPS attempt. |
| 31 | Animation | Authored Animations for abilities, idles and Roll reveals; code poses kept for movement. |

## Build progress
**Milestone 1, economy and Match rules: done (2026-11-02).** Old scripts are backed up in `ServerStorage._Backup_PreRedesign`.
- `Config`: weights 60/27/10/3, Lucky 0/62/28/10, Pity 100, Roll 100 Cash, 300 starting Cash, Locker 2 → 5 (Levels 5/15/30), Cash/XP payouts, Ultimate 0–100 charge, Intermission 20 s.
- `PlayerData`: Cash, XP/Level, Pity, Lucky Rolls; session-locked `UpdateAsync` saves; `BindToClose` waits for the saves.
- `Roll`: Cash or Lucky Rolls, Pity, Vaulted, Level-gated Locker, no duplicate locks.
- `Damage`/`Match`: PvP only (Dummies only in Studio and they never pay), assists, Finish Bonus, results screen, Ultimate kept through death.
- Leave a Match any time with M (forfeits the Finish Bonus).
- **UI style: Stud UI.** The kit is installed as `ReplicatedStorage.StudKit` (StudUI and StudMotion). `UIKit` is an adapter, so every `UIKit.Button`, `Label` and bordered panel draws through the kit without changing the code that calls it. The Equipped Class card and the results screen are real kit windows. The in-Match HUD is in the kit style too:
  - the health bar is a glossy stud progress bar that collapses from both sides
  - timer, Kills and Cash sit in an inset box
  - abilities are dark item slots with spinning sunbursts, a key tag, a draining cooldown cover, and a pulsing lime outline when the Ultimate is ready
  - the Ultimate charge is a gold progress bar above F
  - banners are stud panels tinted to the banner's colour

**Not done yet:** set Max Players to 12 in Game Settings, and test saving with Studio API access on.

**Next milestones:** 2. the 16 Classes · 3. the Maps and the Map vote · 4. mobile controls · 5. Daily Quests, Robux Lucky Rolls, Practice Range.

## What to change in the Studio project
**Rolling and data** (`Roll`, `PlayerData`, `Config`)
- Add Cash, XP/Level, Pity counter and Lucky Rolls to the save data, and charge Cash per Roll (it's free every 3s right now).
- Locker: 2 slots, more by Level (currently `Config.LockerSlots = 3`).
- Add a Vaulted flag per Class; vaulted Classes are skipped in `Roll.RollClass`.
- Replace `SetAsync` with session-locked saves (ProfileStore or `UpdateAsync` + lock) **before** any Robux sale. Saves on shutdown currently rely on a single `task.wait(2)`.
- Robux: a developer product for Lucky Rolls, with idempotent `ProcessReceipt`.

**Match** (`Match`, `Damage`, `Characters`, `Dummies`)
- Remove Dummies from Matches; move them to a Practice Range. Right now dummy kills add to the kill count, charge the Ultimate and decide the winner (`Damage.CreditKill`).
- Ultimate charge: kills + damage + time instead of `UltKills = 5`.
- Pay out Cash and XP per kill and assist (assist tracking is new), plus the Finish Bonus; add a results screen.
- 12-player servers, a Map vote during the Intermission (20 s; the current `IntermissionLength` is 15), and 3 hand-built Maps (Suburb, Mall, Theme Park). The current `Map` service generates one town in code; its brick and explosion code can be reused, and the ground has to be made unbreakable.
- Set `Config.Rarities` weights to 60/27/10/3 (currently 60/25/12/3) and add Lucky weights and a Pity counter of 100.
- Replace the M-before-moving rule with leaving at any time (forfeiting the Finish Bonus).

**Classes** (`Config.Classes`, `Abilities`, `AbilitiesClient`, `WeaponModels`)
- 16 new silly-archetype Classes; ability effects with charges, alt-uses and modes; a Passive system for Epic+.
- Weapons stay data-driven in `Config.Weapons`; add types as the Classes need them.

**Input and platforms** (`Movement`, `Weapons`, `HUD`)
- Touch controls: move stick, fire, Q/E/F, jump (context climb/wall-jump), crouch/slide, scope.
- Light aim assist for touch input.
- Mobile layout for the HUD and the warehouse menus.

**Onboarding and retention**
- Starter Class + Cash for 3 Rolls, with a guided first Roll.
- 3 Daily Quests with a Lucky Roll reward.

**Animation** (`Animator`)
- Authored AnimationTracks for abilities, Class idles and Roll reveals, using the existing `Animator.SKIP` hook; keep the code poses for movement.

## Open, not decided yet
- A spawn rule for a heavily destroyed Map (the PDF's "spawn where you can still stand").
- The Robux price of a Lucky Roll.
- Daily Quest targets (how many kills or how much damage for easy, medium and hard).
- Exact numbers for each Class kit (damage, cooldowns, durations). The roster itself is approved in [[RNG Shooter Roster]]; the Starter Class is the Janitor.
