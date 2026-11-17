---
topic: Balancing
tags: [research, topic]
---
# Balancing

Numbers and formulas pulled from the wikis, plus what they teach. These are reference points for tuning your own economy.

## Value formulas
| Game | Formula | Notes |
|---|---|---|
| [[Grow a Garden]] | `round(Base × Mutation × Variant × clamp(W/BaseW, 0.95, ∞)²)` | Mutations combine **additively** (`1 + Σ(mᵢ−1)`); variants multiply (Silver 5, Gold 20, Rainbow 50, Ember 60). Weight is **squared**. |
| [[Steal An Egg]] | `Base × Color × Size` where size value ≈ `(W/BaseW)^0.62`, then `^0.4` past 125× | **Diminishing returns**: 100× weight ≈ 17× value, 1000× ≈ 45×. |
| [[Steal a Brainrot]] | `Base × Mutation + Σ Traits` | Mutation multiplies, traits **add** (e.g. Fire +5×). |
| [[Fisch]] | One mutation (highest wins) + stackable attributes | If boosted chances go over 100%, the lowest mutations drop out. |
| [[Catch Bugs!]] | Mutation multiplies both sell value and Vivarium income | Vivarium mult is slightly higher than sell mult, so displaying is rewarded. |

> [!tip] Choosing a size curve
> - **Squared (GaG):** huge rolls are *explosive*. Great for hype, but the economy inflates.
> - **Root with diminishing returns (Steal An Egg):** huge rolls still feel good, but stay controllable.
> - **Linear:** predictable but less exciting.

## Mutation multiplier ranges
| Game | Range | Feel |
|---|---|---|
| [[Catch Bugs!]] | 1.3× – 3.25× | Gentle bonus |
| [[Steal An Egg]] | 1.2× – 3.5× | Gentle bonus |
| [[Steal a Brainrot]] | 1.25× (Gold) – 11× (Cyber) | Big |
| [[Grow a Garden]] | ×2 mutations, ×5–60 variants, stacking | Huge |
| [[Storage Hunters Open World]] | **0.8×** – 175× | Huge, and can be negative |

## Mutation rarity (how often)
- [[Catch Bugs!]]: 1 in 90 catches is mutated, then a weighted pick. The common ones (Electrified) are ~24% of mutations; the rarest (Evil) ~2.4%.
- [[Steal An Egg]]: weights out of 100: Silver 6, Golden 4, Rainbow 1.
- Weather boosts: [[Catch Bugs!]] gives a 1 in 3 chance for the weather's mutation during the event.

**Pattern:** the multiplier roughly goes up as the chance goes down. Rainbow is ~6× rarer than Silver for ~3× the value.

## Price curves
### Seeds ([[Grow a Garden]])
10 → 50 → 400 → 800 → 2.5K → 6K → 15K → 50K → 100K → 850K → 1M → 5.5M → 10M → 70M → 10B → 10T → 500T → 1Q.
Restock chance falls from 100% → 0.1%. **Early steps are ×2–8, late steps jump ×100–1000.**

### Treadmills ([[Steal An Egg]])
| Speed/step | Price | Price × | Power × |
|---|---|---|---|
| +2 | free | | |
| +5 | 15K | | 2.5 |
| +12 | 250K | 17 | 2.4 |
| +30 | 5M | 20 | 2.5 |
| +80 | 120M | 24 | 2.7 |
| +100 | 3B | 25 | 1.25 |
| +200 | 75B | 25 | 2 |
| +500 | 2T | 27 | 2.5 |
| +1K | 50T | 25 | 2 |

**About 25× the price for about 2.5× the power each tier.** Each upgrade is ~10× worse value for money, which works because pet income also grows ~10–30× per rarity tier.

### Trails ([[Steal An Egg]])
1.5× → 2× → 2.5× → 3× → 3.5× → 4× → 5× → 7× → 10× → 14× → 20×, priced 100 → 5K → 75K → 1.5M → 30M → 750M → 20B → 500B → 12.5T → 300T → 5Q.

### Vivarium ([[Catch Bugs!]])
$1.5K → 15K → 90K → 400K → 1.2M → 3M → 7M → 12M → 20M → 200M → 600M → 1.5B.
Upgrade *time* also grows: 30s → 10m → 30m → 1.5h → 4h → **caps at 12h**.

### Nets ([[Catch Bugs!]])
$10 → 600 → 5.2K → 8K → 76K → 360K → 2.4M → 12M → 23.5M → 140M → 800M.

### Rebirths ([[Steal a Brainrot]])
500K → 1.5M → 12.5M → 35M → 100M → 350M… with multipliers ×0.5, ×1, ×2, ×3, ×4, ×5.
The early thresholds were **cut after launch** (1M → 500K, 3M → 1.5M). That's evidence that a fast first rebirth matters.

### Rods ([[Fisch]])
Rowboat 400 → Midas 55K → Fallen 175K → Rod of the Depths 750K → then 1.25M – 5M plus Level 200 / 350 / 750.

## Income by rarity
### [[Steal An Egg]] pets ($/s)
| Rarity | Count | Income |
|---|---|---|
| Common | 5 | 1–6 |
| Uncommon | 3 | 8–18 |
| Rare | 10 | 35–280 |
| Epic | 13 | 180–5K |
| Legendary | 29 | 1.8K–600K |
| Mythic | 32 | 16K–13M |
| Cosmic | 41 | 190K–430M |
| Secret | 51 | 1.3M–1.4B |
| Eternal | 36 | 65M–6B |
| Divine | 20 | 1B–15B |

**Ranges overlap between tiers**, so a great Epic can beat a bad Legendary. That keeps lower rarities relevant.

### [[Steal a Brainrot]] (price vs income)
| Rarity | Income | Price | Payback |
|---|---|---|---|
| Common | 1–14 | 25–1.7K | ~25–120s |
| Rare | 15–75 | 2K–9.7K | ~130s |
| Epic | 75–325 | 10K–47.5K | ~130–150s |
| OG | ~750M | ~750B | ~1,000s |

**Payback time grows with rarity.** Rare items are partly prestige.

## Odds & drop tables
- [[Grow a Garden]] Common Egg: 3 pets at 33.33% each (plus a 0.01% chance of nothing).
- [[Grow a Garden]] egg stock chance: Common 99%, Uncommon 55%, Rare 26%, Legendary 15%, Mythical 9%, Bug 5%, Jungle 2%.
- [[Steal a Brainrot]] conveyor: Commons ~55% of spawns, Mythic-ish ~10%.
- [[Fisch]]: Enchant Relic 1/350 anywhere.

## Inventory & slot caps (as upgrade targets)
- [[Grow a Garden]]: 200 items, 60 pets (→ ~300), 3 equipped pets, 3 egg slots, 4 save slots, 3–6 loadouts.
- [[Catch Bugs!]]: 12 traps, Vivarium slots 2 → 13.
- [[Steal a Brainrot]]: base slots 10 → 18 → 25 by rebirth, lock 60s + 10s per rebirth.
- [[Storage Hunters Open World]]: 100 inventory, 40 selling slots, 3 trophies, 25 boxes, 30 plot tiles.

**Lesson:** every cap is a future upgrade, so start players with tight caps.

## Real-time timers
- [[Grow a Garden]]: egg hatch (Common 10 min), plot expansion 24h/72h (Robux skip), Ascension cooldown 4h.
- [[Catch Bugs!]]: Vivarium upgrades up to 12h.
- [[Rivals]]: contracts up to 72h of weapon playtime.

## Starter generosity
- [[Rivals]]: beginner tasks give ~18 Keys fast. The default weapon is "good at all ranges".
- [[Storage Hunters Open World]]: early auctions "rarely lose money".
- [[Fisch]]: the first goal (a 400 C$ boat) is reachable in the first session.

## Second batch: more numbers
### Area costs and currency switching ([[Pet Simulator 99]])
900 → 2.5K → 8K → 20K → 60K → 150K → 400K coins, then **switches to Gold Bars**: 1 → 2 (+500K) → 6 → 15 → 35 → 80.
- **×2.5–3 per area.**
- **Switching currency every ~10 areas resets number inflation.** It avoids the 1e15+ problem in [[Number Formatting and Big Numbers]].

### Level curve ([[Blox Fruits]])
`EXP to next level = 2 × level^2.3 + 84` → polynomial, not exponential. +3 stat points per level; a maxed stat is ~`maxLevel × 0.028` times stronger. **Only 3 of 5 stats can be maxed.**

### Earning caps (protect the economy)
- [[Adopt Me!]]: **300 Bucks per in-game day** (500 with a certificate), doubled on 2× weekends.
- [[Murder Mystery 2]]: **40 coins per round** (50 with the Elite pass). Box prices were rebalanced when the cap was raised from 10–15.

### Diminishing returns
- [[Pet Simulator 99]] enchants: the same enchant stacks at 100% → 60% → 38% → 27.5%.
- [[Steal An Egg]] size value: `^0.62` then `^0.4`.

### Crafting ratios
- [[Murder Mystery 2]]: 12 → 1 per tier.
- [[Adopt Me!]]: 4 → 1 per neon tier (16 → 1 for Mega).

### Egg odds pattern
- [[Pet Simulator 99]]: most eggs ≈ **90% / 10% / tiny chase pet**.
- [[Grow a Garden 2]]: Rainbow variant **0.5%** per egg; Big = 2× passive, Mega = 3×.

### Shared-roll odds
- [[Grow a Garden 2]] night moons: Normal 77%, Gold 13%, Rainbow 6%, Blood 2%, Mega 2%.
- [[Blox Fruits]] starting race: Human 62.5%, Rabbit/Shark/Angel 12.5% each.

### Pity
- [[Murder Mystery 2]]: the chance of Murderer grows each round you don't get it.

### PvP risk scaling
- [[Blox Fruits]] bounty: max gain 21K, max loss 42K. At high bounty you lose 2× what the killer gains, and you can only earn from players within 25% of your level.

### Meta currency scarcity (run-based)
- [[99 Nights in the Forest]]: 2 diamonds at day 50, 3 at day 99, 5 per daily quest (15 for all three). It's scarce and tied to milestones.

### Robux currency packs
- [[Grow a Garden 2]]: **linear** (5K Sheckles = 10 R$ … 100K = 200 R$), no bulk discount.
- [[Rivals]]: **bulk discount** (4.9 → 4.5 R$ per key).

### Gacha odds with a "lucky" tier ([[Blue Lock Rivals]])
| Rarity | Normal spin | Lucky spin |
|---|---|---|
| Rare | 62.25% | 0% |
| Epic | 30% | 0% |
| Legendary | 7% | ~91% |
| Mythic | 0.5% | 5% |
| World Class | 0.25% | 2.5% |
| Master | 0.0325% | 0.2% |

- A lucky spin **removes the bottom tiers** and makes the top tiers ~10× more likely.
- **Pity:** 50 Flow spins guarantees at least Legendary.
- **Earn rate:** 10–40 ¥ per in-match action, 2.5K–4K ¥ per daily quest, against 2,500 ¥ per spin. That's about one spin per quest.

### Odds-band rarities and buff stacking ([[Sols RNG]])
- **Rarity is defined by odds bands:** Epic 1 in 1K–9,999, Unique 10K–99,998, Legendary 99,999–999,999, Mythic 1M–9.99M, Exalted 10M–99.99M, Glorious ~100M+, Transcendent over 1 in 999,999,999. Every new item automatically falls into the right band.
- **Potions:** durations stack but boosts don't. Two of the same potion = the same boost for longer.
- **Luck-proof top items:** the rarest regular aura (1 in 10M) ignores luck and only rolls in a rare biome, so no amount of buffs makes it common.
- **Boss HP scales with player count:** 15,000 solo → 24,210 with 4 players.

## Rules of thumb (my synthesis)
1. **Exponential costs, exponential income.** Keep the *time to next upgrade* roughly steady or slowly growing, not the price.
2. **Overlapping tier ranges** keep lower tiers useful.
3. **One stat gates progress.** Tune that stat's curve first.
4. **Cap real-time waits at ~12h** for upgrades, and ~10 min for early hatches.
5. **Make the first prestige fast**, as Steal a Brainrot learned by lowering R1/R2.
6. **Include bad outcomes** (Dirty, Trash, Glitched) so good ones feel better.
7. **Switch currency before numbers get silly** ([[Pet Simulator 99]] gold bars).
8. **Cap daily or per-round earnings** if you have a trading economy ([[Adopt Me!]], [[Murder Mystery 2]]).
9. **Give duplicates a fixed N → 1 upgrade path** (4 → 1, 12 → 1).
10. **Use diminishing returns on stacking the same buff** to push variety.

## Related
[[Popular Gameplay Mechanics]] · [[Rarity Systems Compared]] · [[Monetization Patterns]] · [[Number Formatting and Big Numbers]]
