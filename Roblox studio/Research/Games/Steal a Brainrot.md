---
genre: Steal tycoon (base + conveyor)
core_loop: Buy a brainrot off the red carpet → it walks to your base → earns $/s → steal others' / defend your own → rebirth
main_currency: Cash ($/s)
progression_gate: Rebirth requirements (cash + specific brainrots)
social: Stealing from other bases, base locks, outbidding, admin events
monetization: Robux brainrots, lucky blocks, gamepasses (VIP lock time), gear
wiki: https://stealabrainrot.fandom.com/wiki/Steal_a_Brainrot_Wiki
images: 1185
tags: [research, game]
---
# Steal a Brainrot

![Player base with laser lock|420](https://static.wikia.nocookie.net/stealabr/images/8/85/Base.png/revision/latest)

## In one sentence
Meme characters ("brainrots") walk down a red carpet, and you buy them so they walk into your base and earn money. Other players can **run into your base and steal them** while your lock is down, so you defend your base with gear and lock timers.

## Core loop
**Buy from the carpet → brainrot earns $/s in your base → buy rarer ones → steal or defend → rebirth for multipliers and slots**

- **The red carpet is a conveyor of offers.** Anyone can buy a brainrot as it walks, and others can **outbid it mid-walk for 150% of its price**. It then turns toward the new owner.
- **The base** has floors with slots (10 → 18 → 25…, unlocked by rebirth). Brainrots in it generate cash.
- **Base lock:** 60 seconds plus 10s per rebirth (and +10s VIP). While it's open, others can steal.

## Popular mechanics worth stealing
| Mechanic | How it works | Why it works |
|---|---|---|
| **Stealing** | Walk into an unlocked base, pick up a brainrot, carry it home. | High drama with real stakes, which makes clips that spread. |
| **Live outbidding on the conveyor** | The price goes up 50% when someone snipes it. | Players compete for the same visible object. |
| **Announcements for rare spawns** | God/Secret spawns are announced in the server, and OG spawns are announced globally. | Everyone sprints to the carpet: a shared hype moment. |
| **Rebirth with item requirements** | Each rebirth needs cash **and specific brainrots**. It resets cash and brainrots but gives a permanent multiplier, a cash bonus, +lock time, +slots and new gear. | Requiring specific items forces collecting, not just grinding. |
| **Index + base skins** | Collect 75% of all brainrots in a mutation (Normal/Gold/Diamond/Rainbow) for +0.5× base multiplier **and** a base skin. | A collection goal with visible status. |
| **Gear (slaps, coils, traps, cloaks…)** | Tools to steal or defend, unlocked by rebirth. | Combat-lite PvP layer. |
| **Machines (Craft/Fuse)** | Combine brainrots into exclusive ones. Machines rotate out with events. | A sink for duplicates, plus FOMO. |
| **Weekly update + admin abuse** | Every Saturday the update drops with an Admin Abuse live event, plus "Taco Tuesday". Early players get a free Secret Lucky Block. | Appointment gaming that rewards showing up early. |

## Balancing notes
**Rarity price/income ranges:**

| Rarity | Count | Income ($/s) | Price | Notes |
|---|---|---|---|---|
| Common | 12 | 1–14 | 25–1.7K | ~55% of spawns |
| Rare | 12 | 15–75 | 2K–9.7K | |
| Epic | 20 | 75–325 | 10K–47.5K | |
| Legendary | 26 | | | |
| Mythic | | 2K–18K | 350K–6M+ | |
| Brainrot God | | | 5M–47M+ | name is said out loud on spawn |
| Secret | | | 80M–425B | |
| OG | | e.g. 750M | e.g. 750B | |

**Payback time grows with rarity:** a Common pays itself back in ~25s, an Epic in ~2 min, an OG in ~1,000s. **The price-to-income ratio rises from ~25× to ~1000×.** Rare items are prestige as much as income.

**Mutation vs trait math:** `Income = Base × MutationMult + Trait bonuses`.
- One mutation per brainrot: Gold 1.25×, Rainbow 10×, Divine 10×, Cyber 11×.
- Traits stack **additively** (e.g. Fire +5×), and you can have many traits.

**Rebirth curve:**

| Rebirth | Cash needed | Multiplier | Cash bonus | Other |
|---|---|---|---|---|
| 1 | 500K | ×0.5 | 5K | |
| 2 | 1.5M | ×1 | 10K | |
| 3 | 12.5M | ×2 | 25K | |
| 4 | 35M | ×3 | 50K | |
| 5 | 100M | ×4 | 100K | |
| 6 | 350M | ×5 | 250K | |

Each rebirth also gives +10s lock time and usually +1 slot. Several thresholds were **lowered after launch** (R1 was 1M, R2 was 3M), so the developers tune the early game for speed.

**Content volume:** 557 indexable brainrots. Content rate is a big part of this game's success.

## UI design
![Index menu|420](https://static.wikia.nocookie.net/stealabr/images/a/ae/Index.png/revision/latest)
![Rebirth menu|420](https://static.wikia.nocookie.net/stealabr/images/6/67/Screenshot_2026-01-24_162225.png/revision/latest)

- **The Index is a grid of character cards.** Unowned brainrots show as **black silhouettes** (curiosity!). Mutation tabs sit on the left (Normal, Gold, Diamond, Rainbow, Cyber…), each in its mutation color. A progress bar at the bottom shows "Collect 75% … for +0.5x Base Multi".
- **The rebirth panel** has a red WARNING line (you lose cash and brainrots), then a row of "You Will Unlock" reward tiles (multi, cash, lock time, slot, new gear), then the requirements with a cash progress bar and the required brainrot cards, then one big gold Rebirth button.
- **The style is flat dark-slate panels** with a white bold font and a red X, simpler than Grow a Garden's themed wood.
- **In the world, signs are floating 3D text** in pink/purple over stalls (e.g. "Robux Shop").

![Robux shop stall|360](https://static.wikia.nocookie.net/stealabr/images/a/af/Robux_Shop.png/revision/latest)

## Models & art style
- **The characters are the selling point.** They're low-poly 3D versions of viral Italian-brainrot memes (shark in sneakers, crocodile bomber plane…), so they're instantly recognizable to the audience.
- **The base is a simple grey box** with a red laser door and a green "slot" floor. The environment is plain so characters stand out.
- **Mutations are material swaps** (gold, diamond, rainbow, lava, galaxy, bloodrot…). Mutation icons are colored badges.

![Gold|120](https://static.wikia.nocookie.net/stealabr/images/0/0f/Gold_Mutation_Icon.png/revision/latest) ![Rainbow|120](https://static.wikia.nocookie.net/stealabr/images/e/e5/Rainbow_Mutation_Icon.png/revision/latest) ![Bloodrot|120](https://static.wikia.nocookie.net/stealabr/images/8/8e/Bloodrot_Mutation_Icon.png/revision/latest) ![Craft machine|260](https://static.wikia.nocookie.net/stealabr/images/4/49/Craft_Machine.png/revision/latest)

## Takeaways for my game
- Stealing plus a lock timer is the core drama. The defense window is what makes it fair.
- Silhouettes in the index make players want to fill them in.
- Rebirths that need specific items make collecting matter.
- Simple environments let the characters be the show.

## Galleries
1185 images in total:
- [[Steal a Brainrot - Base and Map]] (157)
- [[Steal a Brainrot - Brainrots (1 of 3)]] (200)
- [[Steal a Brainrot - Brainrots (2 of 3)]] (200)
- [[Steal a Brainrot - Brainrots (3 of 3)]] (77)
- [[Steal a Brainrot - Gear]] (46)
- [[Steal a Brainrot - Machines and Events]] (183)
- [[Steal a Brainrot - Mutations and Traits (1 of 2)]] (200)
- [[Steal a Brainrot - Mutations and Traits (2 of 2)]] (70)
- [[Steal a Brainrot - Systems]] (47)
- [[Steal a Brainrot - UI and Screens]] (5)

*Source: [Steal a Brainrot Wiki](https://stealabrainrot.fandom.com/wiki/Steal_a_Brainrot_Wiki): Brainrots, Base, Red Carpet, Rebirth, Mutations, Traits, Rarities, Index, Gears, Craft Machine, Admin Abuse.*
