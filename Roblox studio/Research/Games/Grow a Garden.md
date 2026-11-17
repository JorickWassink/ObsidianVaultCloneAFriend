---
genre: Farming simulator
core_loop: Buy seeds → plant → harvest → sell → buy rarer seeds/gear/eggs
main_currency: Sheckles
progression_gate: Money (seed prices), plot expansions, Ascension
social: Shared weather & shop stock, gifting, trading, stealing, friend boost
monetization: Robux price on every seed/gear, shop restocks, timer skips, steal, packs, season pass
wiki: https://growagarden.fandom.com/wiki/Grow_a_Garden_Wiki
images: 2667
tags: [research, game]
---
# Grow a Garden

![The two starting stalls on the classic studded baseplate|500](https://static.wikia.nocookie.net/growagarden/images/1/10/Shops.png/revision/latest)

## In one sentence
You plant seeds in your own plot, wait for them to grow, harvest the fruit and sell it. The money buys rarer seeds, gear that boosts growth or mutations, and eggs that hatch helper pets.

## Core loop
**Buy seeds → plant → wait/grow → harvest → sell at the stand → buy better seeds/gear/eggs → repeat**

- **Multi-harvest crops** keep producing after harvest. This turns early purchases into long-term income without extra clicks.
- The wait is the core tension: the game is mostly *idle with check-ins*, so players come back to see what grew and mutated.

## Popular mechanics worth stealing
| Mechanic | How it works | Why it works |
|---|---|---|
| **Global timed shop stock** | Seed shop restocks every 5 min, egg shop every 30 min. All servers see the same stock, and rare seeds have tiny restock chances (Carrot 100%, top seeds ~0.1%). | Creates "be online when it restocks" moments and a shared topic of conversation. Robux restock (79 R$) or watching an ad skips the wait. |
| **Weather events** | Server-wide weather (frost, rain, aurora…) gives crops a chance at a mutation, and some weathers boost grow speed. | Gives a reason to stay online and turns waiting into anticipation. |
| **Mutations + variants** | Mutations (Chilled, Choc, Fiery, Glimmering…) and variants (Silver ×5, Gold ×20, Rainbow ×50) multiply sell value. | Every harvest is a mini lottery. |
| **Weight rolls** | Each fruit rolls 0.7×–1.4× its base weight, with a rare lucky roll of ×3–4 more. Value scales with weight². | Rare "huge" fruits are screenshot moments. |
| **Pets from eggs** | Eggs cost money and hatch over real time (Common Egg: 10 min). Pets have passives: dig up seeds, eat carrots for 1.5× value, apply mutations. | Gacha excitement plus automation. |
| **Admin Abuse events** | The developer goes live weekly (Saturday update, "Watering Wednesday") and spawns rare weather, restocks shops and gives items. | Huge concurrent-player spikes and appointment gaming. |
| **Stealing & gifting** | You can steal fruit from other gardens (Robux), gift items, and trade with a Trading Ticket. | Social drama and interaction between players. |
| **Friend boost** | +10% sheckles per friend in the server, up to +40%. | Brings friends in, so it works as viral growth. |
| **Ascension (prestige)** | Spend a growing sheckle amount plus a mutated fruit for Garden Coins → permanent upgrades. 4-hour cooldown. | Long-term sink for the late game. |

## Balancing notes
**Fruit value formula** (from the wiki):

`Value = round(BaseValue × MutationMult × VariantMult × clamp(Weight / BaseWeight, 0.95, ∞)²)`

- Mutation multipliers **add** around 1 (`1 + Σ(mᵢ − 1)`), so stacking several is strong but not explosive.
- Weight is **squared**, so a lucky ×3 weight roll is worth ~9×.

**Seed price curve.** Price rises fast while restock chance falls:

| Seed | Price | Restock chance |
|---|---|---|
| Carrot | 10 | 100% |
| Blueberry | 400 | 100% |
| Watermelon | 2,500 | 12.5% |
| Coconut | 6,000 | 5% |
| Dragon Fruit | 50,000 | 2% |
| Grape | 850,000 | 1% |
| Beanstalk | 10M | 0.48% |
| Elder Strawberry | 70M | 0.25% |
| Romanesco | 10B | 0.23% |
| Crimson Thorn | 10T | 0.13% |

Roughly ×2–10 per tier early on, then jumping by 1000× at the very end. The Robux price stays fairly flat (7 R$ → ~1,700 R$), so **Robux is the shortcut for rare seeds, not for cheap ones**.

**Egg odds.** Even the Common Egg splits evenly between 3 pets (33.33% each). Rarer eggs appear in the shop less often (Common 99% → Jungle 2%).

**Sinks:**
- Plot expansions: 250M / 250M / 500M / 1B, with real-time timers of 24h/72h that can be skipped with Robux.
- Save slots up to 100T.
- Pet loadout slots up to 1Q.
- Ascension cost grows by +1T each time.

**Inventory caps** (200 items, 60 pets, 3 equipped pets, 3 egg slots) are upgrade targets in themselves.

## UI design
![Seed shop UI|320](https://static.wikia.nocookie.net/growagarden/images/1/1d/SeedshopUI.png/revision/latest) ![Gear shop UI|320](https://static.wikia.nocookie.net/growagarden/images/6/60/GearShopNewUI.png/revision/latest)

- **The shop is a vertical scrolling list.** Each card has a big item render on the left, a bold name, stock count, a green price, and a rarity pill on the right (grey Common, blue Rare, yellow Legendary).
- **The countdown is in the header** ("New seeds in 3m 9s"), with a bright yellow **RESTOCK** button (Robux) right next to it and a red X close button.
- **Theming:** the frame uses wood-brown planks and a grass-green border, so the UI looks like the farm world.
- **Sold out** shows as red "NO STOCK" text instead of hiding the item. Players still see what they're missing.
- **Currency text** is a chunky rounded font with a thick dark outline and the ¢ symbol. Big numbers use suffixes (K, M, B, T, QA, QI, SX).

![Currency HUD|300](https://static.wikia.nocookie.net/growagarden/images/a/a9/NewSheckleUpd.png/revision/latest) ![Pet equip slots|300](https://static.wikia.nocookie.net/growagarden/images/2/21/Pet_Equip_Slots.png/revision/latest)

## Models & art style
- **Classic Roblox look:** a studded green baseplate, bright blue sky with cartoon clouds, and simple striped-awning market stalls with blocky NPCs.
- **Crops are low-poly and chunky,** in saturated colors. A mutation shows as a material/particle change on the same model (e.g. a fiery carrot), so you need **one model per crop, plus effects**.
- **Seeds in the shop** are simple colored packets, which makes them cheap to produce at scale.

![Tomato plant|250](https://static.wikia.nocookie.net/growagarden/images/4/47/TomatoPlantPic.png/revision/latest) ![Fiery carrot mutation|200](https://static.wikia.nocookie.net/growagarden/images/3/33/Carrot_Fiery.png/revision/latest) ![Pet egg stand|300](https://static.wikia.nocookie.net/growagarden/images/e/e3/Pet_Egg_stand.png/revision/latest)

## Takeaways for my game
- Timed global stock plus a paid instant restock is a strong, simple monetization pattern.
- Square the size bonus (weight²) to make rare big rolls feel amazing.
- Weekly live events with the developer are a retention engine, but they need someone to run them.
- Have one model and many material/particle variants. It's cheap content that still looks rare.

## Galleries
2667 images in total:
- [[Grow a Garden - Cosmetics and Decor (1 of 5)]] (200)
- [[Grow a Garden - Cosmetics and Decor (2 of 5)]] (200)
- [[Grow a Garden - Cosmetics and Decor (3 of 5)]] (200)
- [[Grow a Garden - Cosmetics and Decor (4 of 5)]] (200)
- [[Grow a Garden - Cosmetics and Decor (5 of 5)]] (12)
- [[Grow a Garden - Crops (1 of 4)]] (200)
- [[Grow a Garden - Crops (2 of 4)]] (200)
- [[Grow a Garden - Crops (3 of 4)]] (200)
- [[Grow a Garden - Crops (4 of 4)]] (2)
- [[Grow a Garden - Gear]] (184)
- [[Grow a Garden - Mutations (1 of 2)]] (200)
- [[Grow a Garden - Mutations (2 of 2)]] (53)
- [[Grow a Garden - Pets and Eggs (1 of 3)]] (200)
- [[Grow a Garden - Pets and Eggs (2 of 3)]] (200)
- [[Grow a Garden - Pets and Eggs (3 of 3)]] (84)
- [[Grow a Garden - Shops and NPCs]] (101)
- [[Grow a Garden - Systems]] (45)
- [[Grow a Garden - UI and Screens]] (51)
- [[Grow a Garden - Weather and Events]] (135)

*Source: [Grow a Garden Wiki](https://growagarden.fandom.com/wiki/Grow_a_Garden_Wiki): Mechanics, Seed Shop, Pet Eggs, Common Egg, Weather, Admin Abuse, Sheckles pages.*
