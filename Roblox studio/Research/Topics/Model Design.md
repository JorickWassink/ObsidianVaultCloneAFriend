---
topic: Model design
tags: [research, topic, visual]
---
# Model Design

How the researched games build their 3D content, and how they get *thousands* of collectibles out of a manageable number of models.

## Content volume (images on the wikis, roughly)
- [[Steal a Brainrot]]: 557 indexable characters
- [[Steal An Egg]]: ~280 pets in the data module
- [[Grow a Garden]]: hundreds of crops, pets, gear and ~800 cosmetic/decor items
- [[Fisch]]: hundreds of fish, ~330 boat renders, ~600 rod/gear images
- [[Rivals]]: 53 weapons, but **1,000+ skin/wrap/charm cosmetics**

## The multiplier trick: one mesh, many looks
| Technique | Example |
|---|---|
| **Material swap mutations** | Gold/Diamond/Rainbow/Galaxy brainrots ([[Steal a Brainrot]]), Silver/Golden/Rainbow pets ([[Steal An Egg]]), fiery/frozen crops ([[Grow a Garden]]) |
| **Particle/effect overlays** | Fiery, glimmering and electrified effects on the same base model |
| **Size scaling** | Weight rolls change scale: "Huge" or "Giant" versions |
| **Texture wraps** | [[Rivals]] wraps recolor every weapon. 65 common wraps alone × every weapon |
| **Recolor + name** | [[Catch Bugs!]] bug variants and [[Fisch]] fish variants |

**Lesson:** budget *one* good model per collectible, then plan **material + particle + scale** variants from the start. Keep materials as separate parts or SurfaceAppearance so swapping is easy in code.

## Model categories by game
### Characters / creatures
- **Meme characters** ([[Steal a Brainrot]]): instantly recognizable silhouettes, low-poly, exaggerated features.
- **Real animals and insects, stylized** ([[Steal An Egg]], [[Catch Bugs!]], [[Fisch]]): oversized and saturated, but recognizable as real species.
- **Fantasy escalation:** later tiers become dragons, cosmic beings, demons and angels. Visual power matches stat power.

### Equipment as status
- **Treadmills** ([[Steal An Egg]]): each tier is a hero prop with a theme (sci-fi, flame, gold, ice, hacker, demonic, angelic). A dark base with **bright emissive trim and sparkles**.
- **Rods** ([[Fisch]]): distinct silhouettes plus an effect per rod.
- **Nets & traps** ([[Catch Bugs!]]): traps are plant-themed (flytrap, sundew, glowworm).
- **Weapons** ([[Rivals]]): skins replace the whole model, with unique reload/inspect animations at higher rarity.
- **Vehicles** ([[Storage Hunters Open World]]): functional (capacity, speed, handling).

### Environments
- **Biome ladders** ([[Steal An Egg]], [[Catch Bugs!]], [[Fisch]]): familiar → exotic → fantastical. Each biome has a strong color identity.
- **Competitive maps** ([[Rivals]]): grey-box blocks with a grid texture. Readability over decoration, and Normal/Big/Legacy variants reuse layouts.
- **Plots / bases:** simple frames that the *player's items* fill ([[Steal a Brainrot]] grey box with a red laser door).

### Props for shops/NPCs
- **Striped-awning market stalls** ([[Grow a Garden]], [[Steal a Brainrot]]). The same simple stall, recolored per shop.
- **Themed garages and containers** ([[Storage Hunters Open World]]) hint at loot type from the outside.

### Second batch
- **Scale as a tier** ([[Pet Simulator 99]]): Normal → Huge → Titanic → Gargantuan are the same idea at bigger sizes, with extra effects and ridable at Titanic.
- **Glow-part variants** ([[Adopt Me!]]): build pets with separate "neon" parts that can be switched to Neon material, or color-cycled for Mega Neon. One mesh gives 3 collectible tiers.
- **Size variants with a gameplay effect** ([[Grow a Garden 2]]): Big = 2× size and 2× passive, Mega = 4× size and 3× passive.
- **Weapon skins at scale** ([[Murder Mystery 2]]): ~550 knives and ~300 guns, all on the same simple hitbox. Only the visual changes.
- **Ability VFX over meshes** ([[Blox Fruits]]): fruits are simple models; the 4–5 moves per fruit carry the visual identity.
- **Monster = silhouette** ([[99 Nights in the Forest]]): a few parts and a strong outline read better in the dark than detail.
- **Mascot NPCs in costumes** ([[99 Nights in the Forest]] kids: Dino, Kraken, Squid, Koala), each with a color-coded tent and cave.

## Rarity → model fidelity
- [[Rivals]] skins: Common = a new model; Legendary = + unique reload/inspect/sounds; Mythical = + unique effects/trails.
- [[Steal An Egg]] treadmills: higher tier = more glow, more particles, more saturated accents.
- **Pattern:** more rarity means **more senses involved** (sound, particles, animation, glow), not necessarily more polygons.

## Checklist for my models
- [ ] One base mesh per collectible, with material slots planned for mutations
- [ ] A particle preset per mutation (reusable across all models)
- [ ] Scale variants tested (Huge/Giant must not clip the world)
- [ ] A clear silhouette from far away (the player sees it walking on a conveyor or in a shop)
- [ ] Higher rarity = more glow, particles and sound, not more detail
- [ ] Shop stalls built as one reusable kit

## Related
[[Art Style]] · [[Visual Design Reference]] · [[UI Design]]
