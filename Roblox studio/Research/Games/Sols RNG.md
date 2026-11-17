---
genre: RNG / aura-rolling collector
core_loop: Press Roll → random aura (1 in N) → rare rolls play a cutscene + server/global announcement → equip/collect → craft gears from auras → more luck → roll again
main_currency: Coins (cap 5M), Dark Points, Fish Points
progression_gate: Luck stat (gears, potions, biomes), quests to unlock areas (e.g. The Limbo)
social: Server & global roll announcements, shared biomes, boss raids (1–20 players), PvP auras (toggle)
monetization: VIP 249 R$ (1.2× final luck), VIP+ 350 R$, Quick Roll 100 R$ (skip the roll animation), Merchant Teleporter 40 R$, Starter Pack 49 R$, potion bundles
wiki: https://sol-rng.fandom.com/wiki/Sol%27s_RNG_Wiki
images: 1269
tags: [research, game]
---
# Sol's RNG

![Roll button UI|300](https://static.wikia.nocookie.net/sol-rng/images/9/97/AutoRoll_New.gif/revision/latest) ![Blossom aura on a player|340](https://static.wikia.nocookie.net/sol-rng/images/6/6d/BlossomCollectionStatic.png/revision/latest)

## In one sentence
You press **Roll** and get a random "aura" (an equippable visual effect around your avatar) with odds from 1 in 2 up to **1 in 10,000,000+**. The rarer the aura, the bigger the **roll cutscene** and the louder the **announcement to the server or the whole game**.

*The vault's reference for **pure RNG games** and the best example of **tiered reveal cutscenes**. See [[Cutscenes]].*

## Core loop
**Roll → reveal (cutscene for Epic+) → keep or auto-skip → use auras as crafting materials for gears → gears and potions raise Luck and Roll Speed → roll again**

- **The whole game is one button.** Everything else (gears, potions, biomes, quests) modifies your odds or speed.
- **Auras are both the trophy and the crafting material.** Common auras are consumed to craft gears, e.g. Luck Glove = 2× Divinus + 1× Crystallized + 3× Rare → +25% luck.
- **Auto roll and quick roll** buttons sit next to the main Roll button at the bottom.

## Popular mechanics worth stealing
| Mechanic | How it works | Why it works |
|---|---|---|
| **Tiered roll cutscenes** | Epic and above play a cutscene. Each rarity band has its own style: darker screen, more star points (4 → 8), different sound (bass drop, bell chime, thunder), cracking-glass screen, colored fog. The rarest auras get fully custom cutscenes with their own music. | You **know how rare it is before you see it**, so the build-up is the reward. See [[Cutscenes]]. |
| **Announcements by rarity** | Every Epic+ roll posts "[player] HAS FOUND [aura], CHANCE OF 1 IN N!" in chat, colored like the aura. ~1 in 100M+ is announced **globally to every server**. | Social proof and bragging, and everyone sees what's possible. |
| **Server-wide map effect** | Rare rolls trigger effects over the whole map that everyone sees: yellow lines (Unique), cyan arches (Legendary), pink circles (Mythic+), and for Glorious a **monochrome flash, thunder and a giant beam** on every player's screen. | Other players feel the moment too, which builds hype for the whole server. |
| **Biomes rolled every second** | The weather/biome itself is a roll (e.g. Starfall 1 in 7,500 per second). Each biome boosts its native auras; rolling a biome aura outside its biome is a "Breakthrough" (rarer). Rare biomes include Glitched, Dreamspace and Cyberspace. | Random server events that change *what* you can get. |
| **Bonus roll** | Every 10th roll has 2× luck ("x2 Luck Ready" on the button). Some gears change it to 6×, or every 5 rolls. | A tiny rhythm inside the grind. |
| **Settings to skip cutscenes** | "Cutscene Skip Rarity": auras below your chosen rarity skip their cutscene. "Play New Aura Cutscene" always shows the first time. Separate thresholds for auto-skip warnings and chat spam. | Long sessions stay fast, but new discoveries still feel special. |
| **Quick Roll pass** | 100 R$ to **skip the roll animation** (~1 second per roll). | Players pay to remove friction they enjoyed at first. |
| **The Bank** | A broken slot machine you repair with a Lucky Penny. It stores coins whenever you roll Jackpot/Gilded and pays out at daily reset (capped), and it gives a Roll Speed buff that grows with upgrades. | An idle bonus tied to the core loop. |
| **Hidden dimension** | The Limbo: unlocked through quests and candles, only its own auras can roll there, and most buffs are disabled. Falling into the void plays escalating dialogue ("[ ... ]" → "[ You don't belong here... ]" → "[ Fine. ]") before kicking you out. | Mystery and lore through small scripted moments. |
| **Boss raids** | 1–20 players. Boss HP scales with player count (15,000 solo → 24,210 with 4). You fight with auras that have damage abilities, and 3 weekly rental auras deal 70% damage. | Gives auras a use beyond looking cool. |
| **Day/night talismans** | +100% basic luck during day (Sunstone) or night (Moonstone), 100K coins each. | Time-of-day matters to builds. |

## Balancing notes
**Rarity bands are defined by odds**, not hand-picked:

| Band | Odds | Cutscene |
|---|---|---|
| Basic | below 1 in 1,000 | none |
| Epic | 1 in 1,000 – 9,999 | black screen, edges glow in aura color, ominous sound |
| Unique | 1 in 10,000 – 99,998 | + 4-pointed star and bass drop; yellow lines over the map |
| Legendary | 1 in 99,999 – 999,999 | + white screen-crack; cyan arches over the map |
| Mythic | 1 in 1M – 9.99M | 8-pointed star, colored fog, bell chime and wind; pink circles |
| Exalted | 1 in 10M – 99.99M | colored background; dark blue circles and sparkles |
| Glorious | 1 in ~100M+ | unique animation and symbol; server-wide monochrome, thunder, beam; **global message** |
| Transcendent | over 1 in 999,999,999 | fully custom cutscene with its own music and a unique global message |

**Luck and buffs:**
- **Potions:** duration stacks, the boost doesn't. Two Lucky Potions = same +25% for twice as long. Different tiers of the same potion don't stack.
- **Luck tiers:** Lucky +25%, Fortune I/II/III +50/75/100%, Jewelry +120%…
- **VIP** 1.2× final luck, **VIP+** 1.2× (1.3× together).
- **Some top auras ignore luck entirely.** The rarest regular one (Illusionary, 1 in 10M) is luck-unaffected and only rolls in a rare biome, so it can't be bought with buffs.

**Economy:**
- Coins are capped at 5,000,000.
- Daily quests: 5,000 coins. Map coins: 50 (100 gilded).
- Talismans cost 100K coins.

## UI design
- **One central Roll button** at the bottom with a roll counter ("x2 Luck Ready"), flanked by **Auto roll: OFF** and **Quick roll: OFF** toggles. Thin white outlines on dark translucent boxes, so it's minimal and modern.
- **Chat as a feed:** announcements are color-coded by aura. A global prefix [GLOBAL] marks the rarest.
- **Big settings menu** (Rolling / Notifications / Misc / Sound) with rarity thresholds for auto-equip, skip warnings, cutscene skip and chat filtering. Power users tune the experience.
- **Aura names have their own fonts and colors** in the collection, and the cutscene star color is taken from that font color, so the visual identity is consistent.

## Models & art style
- **Auras are pure VFX:** particles, beams, glow, floating symbols, and name text above the player (like the pink "Blossom" aura). **The collectible is the effect itself.**
- **Higher rarity = more spectacle:** more particles, unique animations, custom music, and abilities in raids.
- **The world is a simple low-poly island** that changes look with each biome (rain, snow, starfall, hell, glitched), so the auras pop against it.
- **Gears** are visible gloves/devices on the arms; an Invisible Gear pass hides them.

![Hollow Purple aura in-game|300](https://static.wikia.nocookie.net/sol-rng/images/1/13/Hollow_Purple_Ingame.gif/revision/latest) ![Global message example|380](https://static.wikia.nocookie.net/sol-rng/images/9/95/Prologue_server_message.jpg/revision/latest)

## Takeaways for my game
- Tier your reveal cutscenes by rarity so the build-up tells players what they got.
- Make rare moments visible to everyone (map effects, colored chat, global messages).
- Let players set a rarity threshold for skipping cutscenes, but always show the first time.
- Use collectibles as crafting material so commons stay useful.
- Make some top items luck-proof so they stay truly rare.

## Galleries
1269 images in total:
- [[Sols RNG - Auras (1 of 3)]] (200)
- [[Sols RNG - Auras (2 of 3)]] (200)
- [[Sols RNG - Auras (3 of 3)]] (86)
- [[Sols RNG - Biomes and Map]] (68)
- [[Sols RNG - Bosses and Events]] (134)
- [[Sols RNG - Gears and Crafting]] (120)
- [[Sols RNG - Items]] (137)
- [[Sols RNG - NPCs]] (34)
- [[Sols RNG - Potions and Effects]] (150)
- [[Sols RNG - Roll Cutscenes]] (21)
- [[Sols RNG - Shop and Gamepasses]] (70)
- [[Sols RNG - UI and Screens]] (49)

*Source: [Sol's RNG Wiki](https://sol-rng.fandom.com/wiki/Sol%27s_RNG_Wiki): Auras, Opening Animations, Rolling, Biomes, Effects, Currency, Gamepasses, Gears, Jake's Workshop, Bank, The Limbo, Boss Raids, Talismans, Settings.*
