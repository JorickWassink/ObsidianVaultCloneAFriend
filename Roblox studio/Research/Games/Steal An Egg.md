---
genre: Steal / run-back tycoon
core_loop: Run to a biome → grab an egg past the guardian → carry it home → hatch → pet earns $/s → buy treadmill/trail → more Speed → farther biomes
main_currency: Cash ($/s from pets)
progression_gate: Speed stat (from treadmill training)
social: Competing for the same eggs; event bosses
monetization: Limited eggs in store, event items
wiki: https://stealanegg.fandom.com/wiki/Steal_An_Egg_Wiki
images: 432
tags: [research, game]
---
# Steal An Egg

![Golden Treadmill|260](https://static.wikia.nocookie.net/stealanegg/images/c/c0/Golden_Treadmill.png/revision/latest) ![Dr. Scramble event|300](https://static.wikia.nocookie.net/stealanegg/images/4/4d/DrScramble.png/revision/latest)

## In one sentence
You sneak into nests guarded by sleeping monsters, grab an egg and run it back to your base pen to hatch a pet that earns money per second. That money buys treadmills that raise your **Speed**, letting you reach farther and more dangerous biomes.

## Core loop
**Steal egg → escape guardian → hatch at base → earn $/s → train Speed → unlock next biome**

- **Everything is one stat (Speed).** That makes progression very easy to understand.
- **Bigger eggs are worth more but slow you down while carrying them.** That's a built-in risk/reward choice on every run.
- Nests **reset every 5 minutes**.

## Popular mechanics worth stealing
| Mechanic | How it works | Why it works |
|---|---|---|
| **Physical carry-back** | You must carry the egg home on foot, and the guardian chases you. | It turns "buying an item" into a short action sequence. |
| **Speed gates** | Biomes need Speed: Lake 900 → Desert 10K → Jungle 40K → Snow 170K → Volcano 700K → Abyss 2.5M → Prehistoric 18M → Cosmic 700M → Cherry Blossom 2.5B → Titan Temple 7B. | One number tells you exactly what's next. |
| **Treadmill training** | You stand on a treadmill to gain Speed per step. Better treadmills give more per step. | A visible, physical "grind" that you upgrade. |
| **Trails as multipliers** | Trails multiply treadmill gains (1.5× → 20×). Only one can be equipped. | Cosmetic *and* functional, so it's a status symbol. |
| **Size + color mutation rolls** | Each hatch rolls size (weight) and color (Silver/Golden/Rainbow…) independently. | Same pet, many collectible versions. |
| **Event boss** | Every 30 min Dr. Scramble's mecha takes over the map. Beating it gives Samples and progress on a 100-tier milestone track. | A server-wide co-op moment on a timer. |

## Balancing notes
**Income formula:** `Income = Base × ColorMult × SizeMult`.

Size has **diminishing returns**:
- Below 125× base weight: value grows with `(weight/base)^(37/60)` (≈ ^0.62).
- Above that: it grows with ^0.4.
- Examples: 100× weight ≈ 17× value, 200× ≈ 23×, 1000× ≈ 45×.

This is a nice way to keep giant rolls exciting without breaking the economy.

**Color mutation roll weights:**

| Color | Multiplier | Roll weight |
|---|---|---|
| Silver | 1.2× | 6/100 |
| Golden | 2.5× | 4/100 |
| Rainbow | 3.5× | 1/100 |

Special colors come from events and consumables (2.75×–3×).

**Treadmills** (Speed per step / price):

| Treadmill | Speed/step | Price |
|---|---|---|
| Base | +2 | free |
| Sci-Fi | +5 | 15K |
| Flame | +12 | 250K |
| Celebrity | +30 | 5M |
| Golden | +80 | 120M |
| Freeze | +100 | 3B |
| Lucky Block | +200 | 75B |
| Hacker | +500 | 2T |
| Demonic | +1K | 50T |

Price grows ~×20–25 per tier while power grows ~×2–2.5. **Each tier is roughly 10× worse value**, so the curve is steep and keeps you hatching.

**Trails** (multiplier / price):
- Grey 1.5× (100), Green 2× (5K), Blue 2.5× (75K), Purple 3× (1.5M)
- Golden 3.5× (30M), Red 4× (750M), Galaxy 5× (20B), Secret 7× (500B)
- Eternal 10× (12.5T), Divine 14× (300T), Moonbloom 20× (5Q)
- Price is ×25–50 per tier.

**Pet income by rarity** (from the wiki's pet data):

| Rarity | Pets | Income ($/s) |
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

**Most content sits in the high rarities.** Only 8 common or uncommon pets exist, but 51 Secret ones. Players move through the early game fast, and most of the collection is late-game.

**Rarity ladder (10 tiers):** Common → Uncommon → Rare → Epic → Legendary → Mythic → Cosmic → Secret → Eternal → Divine, plus Brainrot, Monster and Event specials. The same ladder is reused for treadmills and trails.

## UI design
- **Rarity names are shared across every system** (pets, treadmills, trails), so players learn the color code once.
- **Pet cards show weight in kg plus a color mutation badge.**
- **Event pages use "chips"** (e.g. "22 new pets", "Boss Milestone Event") and a milestone track with **100 tiers**, which is a season-pass-style UI.

## Models & art style
- **Treadmills are the hero props.** Each tier has a strong material theme: sci-fi, flame, gold with sparkles, ice, hacker, demonic, angelic. A dark base gets bright emissive accents.
- **Pets are simple animals** (chicken, dog, frog → dragons, cosmic beings). Color mutations are material swaps (gold, silver, animated rainbow).
- **Biomes go from familiar to fantastical:** forest → lake → desert → jungle → snow → volcano → ocean → prehistoric → space → Japanese garden → temple. The visual escalation matches the power escalation.

![Base treadmill|220](https://static.wikia.nocookie.net/stealanegg/images/c/c3/Treadmill_Base.png/revision/latest) ![Galaxy trail|220](https://static.wikia.nocookie.net/stealanegg/images/a/aa/Galaxy_Trail.png/revision/latest) ![Chicken|200](https://static.wikia.nocookie.net/stealanegg/images/a/a3/Chicken.png/revision/latest)
![Golden mutation|180](https://static.wikia.nocookie.net/stealanegg/images/5/55/Golden.png/revision/latest) ![Rainbow mutation|180](https://static.wikia.nocookie.net/stealanegg/images/1/1e/Rainbow.png/revision/latest)

## Takeaways for my game
- Have one clear gating stat that you can physically train.
- Make carrying loot home a risk/reward moment, where heavier means slower.
- Use diminishing returns on size so huge rolls feel great without breaking the economy.
- Reuse one rarity ladder for every system.

## Galleries
432 images in total:
- [[Steal An Egg - Biomes]] (37)
- [[Steal An Egg - Eggs and Pets (1 of 2)]] (200)
- [[Steal An Egg - Eggs and Pets (2 of 2)]] (161)
- [[Steal An Egg - Events]] (2)
- [[Steal An Egg - Mutations]] (9)
- [[Steal An Egg - Treadmills and Trails]] (23)

*Source: [Steal An Egg Wiki](https://stealanegg.fandom.com/wiki/Steal_An_Egg_Wiki): Eggs, Pets, Mutations, Biomes, Treadmill, Trail, Dr. Scramble's Laboratory, Pets/Treadmills/Trails data modules.*
