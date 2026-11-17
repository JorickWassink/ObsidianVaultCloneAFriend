---
genre: Collection / catching simulator
core_loop: Catch bugs → put best in Vivarium → sell extras → upgrade net/lure/vivarium → unlock zones
main_currency: Coins ($)
progression_gate: Bugs discovered (index count) + net strength/max weight
social: Light; mainly a solo progression game
monetization: Paid weather events, potions for Robux, gamepass luck
wiki: https://catch-bugs.fandom.com/wiki/Catch_Bugs!_Wiki
images: 538
tags: [research, game]
---
# Catch Bugs!

![Thumbnail: "EARNS OFFLINE"|500](https://static.wikia.nocookie.net/catch-bugs/images/b/bf/Catch_bugs_cover_image_1.png/revision/latest)

## In one sentence
You swing a net at bugs across themed zones, display the best ones in a **Vivarium** that earns money (even offline), and upgrade nets and traps to catch bigger, rarer bugs in new zones.

## Core loop
The wiki describes it as: **Catch → Upgrade → Automate → Discover → Vivarium → Repeat**

- **Active income:** catching bugs with your net.
- **Passive income:** the Vivarium pays money over time based on the bugs you display.
- **Automation:** traps (up to 12) catch bugs on their own on blue placement pads.
- **Guidance:** a "Finder" questline asks you to catch 1 of each common bug, which teaches the index.

## Popular mechanics worth stealing
| Mechanic | How it works | Why it works |
|---|---|---|
| **Catch minigame with stats** | Nets have Strength (heavier catches, wider timing bar), Speed (faster progress bar, fewer swats), Luck, and **Max Weight** (a hard cap: a bug heavier than the cap can't be caught). | Gear feels meaningful, and max weight is a clean progression gate. |
| **Vivarium (idle display)** | Limited **slots** and total **capacity** (bug size). Higher level = more slots and higher income. Upgrades take real time: 30s up to 12h. | Gives an "offline earnings" hook and a reason to swap in better bugs. |
| **Discovery gates** | Zones unlock by **number of bugs discovered** (e.g. 60 for Dune Burrow, 70 for Jewel Jungle), not just money. | Pushes collection over grinding a single spot. |
| **Mutations on catch** | 1 in 90 catches is mutated, then a weighted roll picks which mutation. | A small lottery on every catch. |
| **Scheduled weather** | Every 45 min a 5-min weather event. During it, 1 in 3 catches gets that weather's mutation. **Players can buy a weather for Robux** (99–199 R$). | Appointment play plus a paid server-wide event, which is social monetization. |
| **Potions & crafting** | Temporary buffs (10–15 min) bought with coins or Robux, or crafted from specific bugs (e.g. 4 Monarch Butterflies → Butterfly Potion, 2× butterfly odds). | Gives common bugs a use beyond selling. |
| **Traps + bait** | Each trap has luck, catch speed and capacity, and some only work at night. Bait changes its goal: speed, luck or size. | Automation that still needs decisions. |
| **Puzzle/endgame zones** | Late zones add builder puzzles, quest chains and titles. | Gives variety once the loop gets stale. |

## Balancing notes
**Mutation table** (value multiplier / Vivarium multiplier / share of mutated catches):

| Mutation | Value | Vivarium | Share |
|---|---|---|---|
| Electrified | 1.5× | 1.59× | 24.4% |
| Frozen | 1.8× | 1.97× | 19.5% |
| Infernal | 2.2× | 2.52× | 17.1% |
| Radioactive | 2.0× | 2.24× | 14.6% |
| Radiant | 2.5× | 2.95× | 9.8% |
| Chromatic | 3.0× | 3.72× | 7.3% |
| Extraterrestrial | 3.15× | 3.96× | 4.9% |
| Evil | 3.25× | 4.13× | 2.4% |

- Note how flat the multipliers are (1.3×–3.25×) compared with Grow a Garden. Mutations here are a *bonus*, not the whole economy.
- The Vivarium multiplier is slightly higher than the sell multiplier, which **rewards displaying over selling**.

**Vivarium upgrade curve:**

| Level | Capacity | Slots | Cost | Upgrade time |
|---|---|---|---|---|
| 1 | 3 | 2 | free | instant |
| 2 | 6 | 3 | $1.5K | 30s |
| 3 | 11 | 4 | $15K | 10 min |
| 4 | 17 | 5 | $90K | 30 min |
| 5 | 30 | 6 | $400K | 1.5h |
| 6 | 38 | 7 | $1.2M | 4h |
| 7 | 45 | 8 | $3M | 12h |
| 10 | 90 | 10 | $20M | 12h |
| 13 | 150 | 13 | $1.5B | 12h |

Slots grow by about +1 per level while cost grows ~×3–10. Upgrade time caps at 12h, which is good for a "come back tomorrow" rhythm.

**Net progression by zone:**
- Basic $10, Steel $600, Lucky $5.2K
- Royal $76K, Demon $360K, Hellfire $2.4M
- Dreamcatcher $23.5M, Steampunk $140M, Ancient Relic $800M

**Luck numbers are shown as huge percentages** (+355% → +17,000%). That's inflated presentation, which feels good to see.

## UI design
- **Rarity tiers each have their own text color:** Common white with a black outline, Uncommon green, Rare blue, Legendary orange, Exotic a rainbow gradient, Mythical purple, and up to Primordial silver.
- **Bug cards** show the mutation name in its own color on top, then rarity, then the bug name, the weight in kg, and a star for favorites.
- **The thumbnail sells the idle hook in big text** ("EARNS OFFLINE") over a bright glass vivarium scene.

![Mutation showcase cards|600](https://static.wikia.nocookie.net/catch-bugs/images/1/12/Mutations_Showcase.png/revision/latest)

## Models & art style
- Stylized but **recognizable real insects** (wasps, centipedes, scorpions), scaled up and brightly colored.
- **Zones are themed biomes:** grassland, forest, night hollow, caves, desert, tomb, jungle, Japanese garden, swamp, prehistoric, volcanic. Each has a strong color identity.
- Traps are plant-themed props (flytrap, sundew, glowworm). Equipment fits the world's fiction.

![Trap shop banner|500](https://static.wikia.nocookie.net/catch-bugs/images/5/53/Trap_Shop_Banner.png/revision/latest)
![Steel net|200](https://static.wikia.nocookie.net/catch-bugs/images/e/e9/Steel_Net.png/revision/latest) ![Flytrap|200](https://static.wikia.nocookie.net/catch-bugs/images/2/28/Flytrap.png/revision/latest) ![Potion trader|300](https://static.wikia.nocookie.net/catch-bugs/images/7/7c/Potion_Trader.png/revision/latest)

## Takeaways for my game
- "Display your best X to earn passive income" is a great way to make collecting *matter*.
- Gate zones by **discovery count**, which keeps players exploring.
- Selling a server-wide weather event for Robux is clever. Everyone benefits, so the buyer looks generous.
- Make a hard stat cap (max weight) on gear. It's a very readable progression rule.

## Galleries
538 images in total:
- [[Catch Bugs! - Bugs (1 of 2)]] (200)
- [[Catch Bugs! - Bugs (2 of 2)]] (101)
- [[Catch Bugs! - Equipment]] (115)
- [[Catch Bugs! - Mutations]] (11)
- [[Catch Bugs! - UI and Screens]] (13)
- [[Catch Bugs! - Zones]] (98)

*Source: [Catch Bugs! Wiki](https://catch-bugs.fandom.com/wiki/Catch_Bugs!_Wiki): Main page, Progress Guide, Nets, Vivarium, Traps, Potions, Mutations, Zones, Quests, Rarities.*
