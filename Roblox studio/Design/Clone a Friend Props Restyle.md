---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-12
---
# Clone a Friend: Stud-free props (lever, stalls, arcade)

Follows [[Clone a Friend Decorations]] and [[Clone a Friend Base Buildings]]: smooth, rounded Blender models, bright cartoon colours, no studs. The glossary lives in the place (`ServerStorage.Docs`).

## Stud scan (2026-11-12)
Still studded and visible before this batch: the Clone lever on every Base, both Hub stalls (Market and Gems), one face each on the Art Easel and Money Printer, and the Bosses and Pets ("Studs" SurfaceAppearance). The Arcade Machine had no studs but was a flat, boxy cabinet.

## Decisions (grilling, 2026-11-12)
| Topic | Decision |
|---|---|
| Scope | Lever, both stalls, Arcade Machine, the two Station faces. Bosses **and Pets** wait for the Boss model batch (a Pet is a small version of its Boss) |
| Lever | A lab console in the Clone Tube's white / navy / red: chrome handle, big red ball (turns green when pulled), DNA screen, status lamps, hazard stripes, cable towards the tube. It stays a lever ("pulling the lever") and stands alone, because a Base can have up to 3 Clone Tubes |
| Lever spot | Same spot, about 1.5x bigger |
| Stalls | Keep the striped stall, rebuilt rounded: pillow awning with scallops, bulb string, wooden counter with an emblem, potted plants. Market: sword crate, money bag, coins. Gems: crystal cluster, cushion with a big gem, gem pile. Same footprint |
| Arcade | Its own colours (purple and pink), rounded retro cabinet, glowing screen and marquee, joystick and buttons, same 6x6 footprint |
| Review | Straight into the game, old models backed up |

## Built (2026-11-12)
- Models: `Assets/Props Restyle/PropsRestyle.blend`, rebuilt by `build_props.py` (reuses the helpers of `Assets/Decorations/build_decor.py`). FBX in `Assets/Stations and Weapons/PropsRestyle.fbx`, uploaded through Open Cloud as asset 70863325171061.
- In the place: templates in `ServerStorage.PropsRestyle`; backups in `ServerStorage.PropsBackup_BeforeRestyle`.
- Lever: `Lever.Console` on all 6 Bases; Handle and Ball are the new meshes, hinge 2.85 above the ground, `HandleOffset` 1.405, `BallOffset` 3.5. Swing, green ball and pity glow tested (no errors in a playtest).
- Stalls: a `StallLook` model in each stand; one shared Stall kit whose `Accent` mesh takes the stand colour (Market de2a2c, Gems 2878eb). Old parts are invisible and still do the collisions.
- Arcade Machine: new meshes in `BuildItems.ArcadeMachine`; `Marquee`, `Glow1`, `Glow2` keep their names so the colour-cycling effect still works.
- Note: smoothing the Art Easel and Money Printer faces also smoothed the same parts in the old-look backup `BuildItems_OldParts`.

## Next
- Boss and Pet model batch: replace the "Studs" SurfaceAppearance on `BossModels` 1-10 and `PetModels` 1-10.
