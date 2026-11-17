---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-10
---
# Clone a Friend: Boss 1 (Brown Bear) redesign

> [!warning] Superseded 2026-11-12 by [[Clone a Friend Boss Restyle]]: faceted endgame look, new skeletons. The face pieces and animation rules below still apply; the cartoon look, picnic basket, eye mask and the Studio-parts build do not.

Boss 1 is the Brown Bear (model `B01_PicnicGrizzly`): a grumpy picnic grizzly. Old look: blocky, stud-textured, cream belly, red bandana and small cape, dark eye mask with a scar, white claws. Follows the stud-free style of [[Clone a Friend Decorations]] and [[Clone a Friend Base Buildings]]. Boss 1 is the template for Bosses 2 to 10.

## Decisions (grilling, 2026-11-10)
These replace the 2026-11-08 round below.

| Topic | Decision |
|---|---|
| Start point | Start over; the 8 Nov "picnic warlord" bear is dropped |
| Look | Big grumpy cartoon: clean chunky shapes, bright flat colours, oversized head and paws, a big readable grumpy face. A boss through size and attitude, not scariness |
| Picnic touches | Checkered bandana + cape, picnic basket on the back, honey details (jar, drips). No fork: he hits with his paws |
| Face | Swapped pieces, eyes and mouth apart (ADR 0015 in `ServerStorage.Docs`). Not a dynamic head, not jointed brows/jaw |
| Expressions | Grumpy (rest), Angry, Roar, Hurt, Dazed, plus blinks and glances. No Smug, no Enraged |
| What drives the face | Each body clip sets its own Expression, plus fight reactions: a wince when hit (at most about once per 1.5 s) and random blinks and glances |
| Skeleton | The old 10 joints plus secondary ones: waist, ears, cape, knees/feet, basket |
| Animations | All 8 clips redone (Idle, Walk, Intro, Strike, SlamWind, SlamLeap, SlamHit, Defeat) plus a new Hurt flinch |
| Smoothness | The complaint is robotic pose-to-pose motion: clips are baked from Blender curves at 30 frames a second, with arcs, anticipation and overshoot, instead of 3 to 9 key poses |
| Hurt flinch | Plays for every 10% Health lost; never interrupts an attack in progress |
| Pet | Remodelled to match, blinking and a happy face only, new smooth Idle |
| Review | Blender renders first (front, side, back, every Expression); nothing is uploaded or swapped before the OK |
| Scope | Standard for all ten Bosses, one at a time, each keeping its theme; the next starts after the previous is approved in the game |

## Where it stands (2026-11-10)
- Built in Studio instead of Blender (changed later on 2026-11-10): the bear is assembled from primitive parts by the builder script `ServerStorage.BossBuilds.B01_Bear` (`build(origin)`, `setExpression(model, name)`). No FBX, no upload. Review is by Studio screenshots instead of Blender renders, and clips will have to be generated in Studio too.
- Preview only, waiting for the OK: `Workspace._ClaudeBearPreview` at (80, 300, 0), with a line-up of all 8 faces in its `Sheet` folder. The old stud bear is still live; `BossModels.1` is untouched.
- Model: 154 parts, 20 studs tall, 17 joints (Root, Waist, Neck, two ears, shoulders/elbows/wrists, hips/ankles, CapeJoint, BasketJoint). Face pieces carry the attributes `FaceSlot` (Eyes/Mouth) and `FaceSets`; hidden pieces have Transparency 1.
- Not done yet: the 9 clips, the code that drives the face in a fight, the Pet, and swapping it into the game.

## Earlier round (2026-11-08, dropped)
Smooth cartoon bear that grew into a hunched "picnic warlord" (glowing eyes, fangs, pauldrons, battle fork) after the feedback "clipping everywhere", "make it feel like a boss", "too round", "backpack not aligned", "make the animations better". It kept the old 10 joints so the old clips would still play. Blender only, never put in the game. Files: `Assets/Bosses/build_bear.py`, `BrownBear.blend`, `bear_rigdata.json`, `clip_check.py`, and `Assets/Stations and Weapons/BrownBear.fbx`.

Still useful from that round:
- Upload path: FBX in `Assets/Stations and Weapons` (the folder Studio may upload from), open_cloud_invoke as Model; recover the transform from the `B01__Anchor` / `P01__Anchor` cubes (mapping (-x, z, y), scale = anchor distance / 40), strip the `B01__` / `P01__` prefixes.
- `BossRigData` needs a `smooth = true` flag and `BossRigBuilder` must skip the stud overlay when it is set (Neon for glow parts).
- Swap `ReplicatedStorage.BossModels.1` and `PetModels.1`, backing the old ones up in `ServerStorage.OldBossModels`.
- `clip_check.py` measures clipping between parts.
