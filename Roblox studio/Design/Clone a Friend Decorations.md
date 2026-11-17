---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-08
---
# Clone a Friend: Decorations and stud-free world

The game's glossary and ADRs live in the place (`ServerStorage.Docs`). Style follows [[Clone a Friend Stations and Weapons]] and the Clone Tube: smooth, rounded Blender models, bright cartoon colours, no studs. Ideas from the vault's Grow a Garden decor and props galleries.

## Decisions (grilling, 2026-11-08)
| Topic | Decision |
|---|---|
| Restyle | Everything outdoors loses its studs: ground, Hub floor, border, trees |
| Ground | Same two-tone green checker, studs removed |
| Hub floor | Same blue/white checker, studs removed, plus park props around its rim |
| Border | Rebuilt from Blender cartoon cliff pieces (rock + grass top), same size and height |
| Trees | 4 kinds (round, pine, birch, fruit); the whole layout redone in clusters |
| Decor set | Nature (bushes, flowers, rocks, mushrooms, stumps, grass tufts), park props (benches, lamp posts, fence, fountain, well, signpost), cozy camp (campfire, tent, hay bales, picnic blanket) |
| Density | Medium: small clusters, one park corner (fountain + benches), one camp spot; open grass between Bases |
| Every Base | Mailbox, lamp posts, a bench and a low brown wooden fence (sides and back, open at the front), clear of the build area, spawn pad and Clone Tube |
| Collisions | All decorations are solid |
| Review | Straight into the game (no render sheet first) |
| Old look | Old trees, border and tiles kept as a backup in ServerStorage |

## Built (2026-11-08)
- Models: `Assets/Decorations/Decorations.blend`, rebuilt by `Assets/Decorations/build_decor.py` (colours in `decor_colors.json`). Uploaded as asset 91024068615225 (the FBX sits in `Assets/Stations and Weapons`, the folder Studio may upload from).
- 27 props: TreeRound, TreePine, TreeBirch, TreeFruit, Bush, BushFlower, FlowerPatch, FlowerPatch2, RockBig, RockSmall, Mushrooms, Stump, GrassTuft, Bench, LampPost, Fence, Fountain, Well, Signpost, Mailbox, Campfire, Tent, HayBale, PicnicBlanket, CliffA, CliffB, CliffC.
- First version was too plain ("make them more detailed") and the first walls were boxes ("the walls are horrible"); the walls are now clusters of rounded rock columns with their own grass caps, vines and boulders.
- In the place: `ServerStorage.DecorModels` (source), `Workspace.Scenery` (Wall, Nature, Park, Camp, Hub, BaseYards). Lamp posts and the campfire have a PointLight.
- Resizing a copy: `m:ScaleTo(m:GetScale() * factor)`, never `m:ScaleTo(factor)`.

## Lighting and effects (2026-11-08)
Asked for: animations and effects where they make sense, and lighting/shaders that are "less insanely bright".
- Lighting: softer afternoon (lower brightness, later sun, slight negative exposure), light haze, calmer bloom, a "WorldGrade" colour correction (less saturation, a bit more contrast, warm tint). Grass toned from neon green to a natural green. Old values are kept on `ServerStorage.LightingBackup_Bright`.
- Effects: campfire flames, smoke and embers; fountain spray and mist; glowing mushroom spores; bubbles in the DNA tanks on the lab roofs.
- Animations (client, `DecorFX`): trees and bushes sway in the wind, the campfire light and flames flicker, lab neon breathes, the roof antenna blinks, fountain water shimmers, butterflies flutter around flower patches. Distance-culled, 30 Hz, works with streaming.
