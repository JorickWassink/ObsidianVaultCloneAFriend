---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-08
---
# Clone a Friend: Base building redesign

Follows [[Clone a Friend Decorations]] (stud-free world) and the Clone Tube look. The glossary lives in the place (`ServerStorage.Docs`): a Base is the plot and its building, a Floor is one level of the building.

## Decisions (2026-11-08)
| Topic | Decision |
|---|---|
| Style | Clone lab: rounded wall panels, big rounded windows with white frames, a canopy over the door, a glowing DNA sign and lab vents on the roof |
| Colours | Keep the owner's random colour (walls and band); unowned Bases stay the default |
| Inside floor | Smooth two-tone tiles on every Floor, no studs |
| Review | Straight into the game |

## Fixed by the game (not up for change)
- Footprint 46 x 46 (plot-local x -6..40, z -18..28), 15.2 tall per Floor, door on the Hub side (-X), stair lane inside along z -17..-11.
- Window spots stay where they are (Stations are placed around them).
- Upper Floors are built at runtime by `RebirthService` from the ground floor, painted by `BuildingLook`, animated by `FloorBuildAnimation`.

## Built (2026-11-08)
- Model: `Assets/Base Building/BaseBuilding.blend`, rebuilt by `build_building.py` (plot-local coordinates, so it lines up with the game's walls). Three pieces: Ground (door, canopy, glowing DNA sign, wall lamps, planters), Upper (window where the door is) and Roof (vents, DNA tank, skylight, antenna, dish, planters). Uploaded as asset 114169429749997; the FBX and the floor tile image sit in `Assets/Stations and Weapons` (the folder Studio may upload from).
- In the place: `ServerStorage.BuildingShell` (Ground / Upper / Roof). The old block parts stay as invisible collision (attribute `Hidden`). `RebirthService` adds an Upper piece per extra Floor and the Roof on top; `BuildingLook.addShell` / `showRoof` do this. The owner colour lands on the mesh parts `WallPanel` and `Stripe`.
- Floor: smooth with a tile texture (`FloorTile.png`), on every Floor and the ramps.
- Tested in a playtest with 2 extra Floors: Upper pieces on each, the Roof on top, the owner colour on every Floor, no errors.
- Backups: `ServerStorage.BuildingBackup_BeforeLab`, `ServerStorage.ScriptBackups_BeforeLab`.
