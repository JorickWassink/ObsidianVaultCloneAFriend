---
genre: Co-op survival horror (run-based)
core_loop: Gather wood/scrap by day → fuel campfire & craft → survive the Deer at night → rescue the 4 kids → reach day 99
main_currency: Diamonds (meta, between runs)
progression_gate: Campfire level (expands map), days survived; meta: classes bought with diamonds
social: 1–5 player teams, shared camp
monetization: Diamonds for Robux, class level skips (250 / 400 R$), event class currencies
developer: Grandma's Favourite Games
wiki: https://99-nights-in-the-forest.fandom.com/wiki/99_Nights_in_the_Forest_Wiki
images: 656
tags: [research, game]
---
# 99 Nights in the Forest

![The Deer|200](https://static.wikia.nocookie.net/99-nights-in-the-forest/images/6/61/TheDeerGame.webp/revision/latest) ![Crafting bench in-game|380](https://static.wikia.nocookie.net/99-nights-in-the-forest/images/6/6b/Crafting_Bench_3_In-game.png/revision/latest)

## In one sentence
A co-op survival run: you and up to 4 friends build a camp in a dark forest, keep the **campfire** burning, craft tools, and rescue four kidnapped children while an **unkillable Deer monster** hunts you every night. The goal is to survive 99 nights.

*The vault's reference for **run-based (roguelite) design, co-op, and horror pacing**. It's a different structure from the persistent simulators.*

## Core loop
**Day: explore, chop wood, scrap junk, hunt → feed the campfire and grinder → craft → Night: retreat to the fire's light, survive the Deer and cultists → next day**

- **Each run starts fresh.** Meta progression is **Diamonds → Classes** (bought in the lobby).
- **Team size 1–5 is chosen in a matchmaking box**, and bigger teams make it harder.

## Popular mechanics worth stealing
| Mechanic | How it works | Why it works |
|---|---|---|
| **Campfire = safe zone + progression** | The fire drains constantly (faster in rain/snow). Adding fuel levels it 1 → 6. **Each level enlarges both the safe zone and the explorable map.** | One object is your lifeline, your upgrade track and your map unlock. Very elegant. |
| **Unkillable stalker** | The Deer can't be damaged. A flashlight stuns it, and it won't enter the firelight. It gets faster the longer it chases. | Pure tension with no "solution", so the only answer is skill and preparation. |
| **Rescue objectives** | 4 kids in colored locked caves (red, blue, yellow, grey). Each rescue = +1 day and multipliers, and they set up tents at camp. | A clear mid-run goal list with visible progress at camp. |
| **Grinder crafting** | Throw junk into a grinder for Scrap/Wood. The item icons show yield (🔩 = 1, 🔩🔩 = 3, 🔩🔩🔩 = 5, 🔩🔩🔩🔩 = 8). Benches tier up. | Simple, readable crafting economy. |
| **Classes (meta)** | Bought with Diamonds; each has starter tools and perks, and levels 1 → 3 by doing class tasks (or 250/400 R$ skips). **4 random classes go on sale daily** (-10% to -20%). | Replayability and a daily-sale check-in. |
| **Day boosters** | Beds and rescued kids skip days. | Rewards preparation by fast-forwarding. |
| **Strongholds & bosses** | Cultist stronghold, Ice Temple, Frog King, UFO, each with a special chest. | Optional high-risk points of interest. |

## Balancing notes
- **Diamonds:** +2 at day 50 and +3 at day 99 (4 / 8 in hard mode). 5 per daily quest, 15 for all 3 daily quests. Diamond chest in the cultist stronghold gives 5.
  → **Meta currency is scarce and tied to milestones and dailies.**
- **Cultist HP scales with stronghold level:** 120 → 180 → 240 → 300.
- **Deer damage** is 25+ and grows with the day count.
- **Guaranteed early resources:** a coal pile or 6 logs at fire level 1 almost guarantees reaching level 2. The first upgrade is never luck-based.

## UI design
- **In-world diegetic UI:** the crafting bench shows resource counts on **red/white signs attached to the bench** (5 wood, 18 scrap), not in a menu.
- **Map item** shows explored areas and teammates, and becomes **unusable if the fire goes out** (a UI tied to game state).
- **The wiki uses deep blue tables** (#2f398f), which match the night mood.

## Models & art style
- **Low-poly, slightly cartoony horror:** bright green grass and simple blocky props by day, darkness and fog by night.
- **The monster design is simple but unsettling:** the Deer is a skinny bipedal deer with antlers and a wide-open mouth. **Silhouette over detail.**
- **Kids are mascots in animal costumes** (Dino, Kraken, Squid, Koala), each with their own tent color.
- Holiday reskins (Halloween kids) reuse the same models.

## Takeaways for my game
- Make one central object do everything: safe zone, upgrade track and map unlock.
- An unkillable threat with a counter (light) creates tension without combat balancing.
- Show resource yield as icons (🔩 × n) on items.
- Daily random sales on meta items give a check-in reason.

## Galleries
656 images in total:
- [[99 Nights in the Forest - Camp and Crafting]] (117)
- [[99 Nights in the Forest - Classes]] (128)
- [[99 Nights in the Forest - Entities]] (179)
- [[99 Nights in the Forest - Items]] (176)
- [[99 Nights in the Forest - Locations]] (18)
- [[99 Nights in the Forest - UI and Screens]] (38)

*Source: [99 Nights in the Forest Wiki](https://99-nights-in-the-forest.fandom.com/wiki/99_Nights_in_the_Forest_Wiki): Main page, Campfire, Classes, Crafting, Entities, Kids, Chests, Diamonds, Tips and Tricks, Deer, Cultist.*
