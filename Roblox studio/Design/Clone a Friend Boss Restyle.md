---
tags: [design, clone-a-friend]
game: Clone a Friend
date: 2026-11-12
---
# Clone a Friend: Boss and Pet restyle (endgame look)

Replaces the look in [[Clone a Friend Boss 1 Redesign]] (its swappable faces and animation rules stay). Last studded models in the game, after [[Clone a Friend Props Restyle]].

## References
- Creator's video: a "Haunted Necropolis" boss. Faceted low-poly, flat shading, huge chest and shoulders on short legs, hood with a glowing grin, spiky gold crown, gold trim, chain, lantern, cape, floating crystal shards; lantern slam, ground beam and collapse animations.
- Steal An Egg endgame pets ([[Steal An Egg]]; Shattered Colossus, World Eater, Voidmaw, Ringlord, Tombstone Bear): no studs, crystal plates, dark base with neon seams, big toothy maws, chunky top-heavy builds.
- Blox Fruits big non-humanoid bosses (sea beast type): huge, layered fins and spines, glowing eyes, one strong silhouette.

## Decisions (grilling, 2026-11-12)
| Topic | Decision |
|---|---|
| Themes | Every Boss keeps its creature, colours, mood and props; only the style changes ("same, just restyled") |
| Surface | Faceted low-poly, flat shaded, with gold trim and neon accents |
| Ramp | The look grows with Boss Rarity: 1-3 warm with little glow, 4-7 armour, gold, more neon, 8-10 dark with neon and floating shards |
| Faces | Swappable face pieces on **all ten** Bosses (ADR 0015): Grumpy, Angry, Roar, Hurt, Dazed, blinks, glances |
| Skeletons | **New** skeletons per Boss; every clip is remade |
| Clips | Baked from Blender curves at 30 fps (arcs, anticipation, overshoot); same clip names and Event_ timings so the specials keep working; a Hurt flinch every 10% Health lost |
| Size | Each Boss keeps its current height (14 to 35 studs) |
| Effects | Each Boss's attack effects are restyled together with its model (no more stud-block bursts) |
| Pets | A chibi Pet per Boss in the same style, in the same batch |
| Build | Blender meshes, uploaded from the approved folder |
| Order | Boss 1 + Pet 1 first as the template (Blender renders for the OK), then 2-5 and 6-10 as rendered batches |

## Boss 1: Brown Bear
| Topic | Decision |
|---|---|
| Shape | Top-heavy brute: huge chest, shoulders and paws, short legs, small head sunk into the shoulders |
| Colours / mood | Brown bear, grumpy, as before |
| Props | Red and white checkered bandana and short cape; honey jar on the belt and honey dripping from the paws. No basket, no eye mask or scar |
| Glow | Eyes only |
| Bear Slam effect | Faceted ground shards burst up in a ring, honey splash, dust shockwave |

## Built: Boss 1 + Pet 1 (2026-11-12)
- First try was rejected ("this is bad": lumpy rock-like shapes, wrong proportions, dull colours). Rebuilt from clean 8-sided lofts with big flat facets, the video's proportions (barrel chest, hunch, long heavy arms, short wide legs) and a saturated palette; "more saturated" pushed it further (renders use Blender's Standard view transform, AgX washed colours out).
- Approved from the review sheet `Assets/Bosses/renders/B01_review_sheet.png` (body, 8 expressions, Pet).
- Source: `Assets/Bosses/build_boss01.py` -> `Boss01.blend`, FBX `Assets/Stations and Weapons/Boss01.fbx`, asset 111003641627472.
- In the place: `BossModels.1` and `PetModels.1` replaced (old ones in `ServerStorage.BossBackup_BeforeRestyle`). Rig builder `ServerStorage.BossRigSmooth` + data `BossRigDataV2` are reusable for Bosses 2-10.
- Clips: key poses in `ServerStorage.BossClips.B01`, baked at 30 fps by `BossClipBaker` (Catmull-Rom between designed keys, done in Studio rather than Blender). Same names, lengths and attack timings, plus Hurt. Each clip carries its face timeline.
- Faces: client `BossFace` plays clip timelines, a wince on hits (max every 1.5 s), blinks and glances; Pets blink. Pets cannot play keyframed clips (they are anchored), so Pet 1 keeps the bob from `PetFollow`.
- Bear Slam effect: faceted rock shards burst up and sink back, honey splash and puddle, dust ring.
- Tested in a playtest (forced Boss 1, Void so it lasts): Strike, SlamWind/Leap/Hit, three Hurt flinches between attacks, six winces, Pet blinks; no errors.
- **Open:** the 9 clips are not published (they play in Studio only). Publish them and fill `PublishedId` before the game goes live, or Boss 1 stands still in the live game.

## Bosses 2-5 (grilling, 2026-11-12)
| Boss | Design |
|---|---|
| 2 Rabbeat | Bulky brute rabbit (same top-heavy build as the bear), carrot club in hand, leaf headband. Glow: eyes only |
| 3 Robcoon | Sneaky hunched thief: long clawed hands, big bushy striped tail (new Tail joint), overflowing loot sack on his back. Glow: eyes + gold coins glint |
| 4 Champ N Son | Champion fighter: ripped boxer, huge blue gloves with neon cuffs, glowing gold title belt, red shorts, joey in the pouch with his own small gloves and face |
| 5 Le Ape | Plain chef, faceted: chef hat, mustache, striped apron, scarf, rolling pin. Glow: eyes only |

## Chibi change (2026-11-12)
Creator, while Bosses 2-5 were being built: "make them more chibi. they all look too buff."
| Topic | Decision |
|---|---|
| Scope | All five, **including Boss 1** (already in the game: rebuilt, re-rigged, clips adjusted) |
| Level | Chunky chibi: head about 35-40% of the height, round soft body, short stubby arms and legs, big hands and feet. Faces, glow and props stay; clearly bigger and meaner than the Pet |
| Size | Each Boss is scaled back to its old height |
| Pets | Unchanged (already chibi) |
| Designs above | Still apply (Rabbeat's carrot club, Robcoon's tail and sack, Champ's gloves and belt, Le Ape's chef outfit) on the chibi body |

## Correction: "cartoony", not chibi (2026-11-12)
The chibi 3D build looked "horrifying". Creator: "maybe chibi was not the right wording. cartooney is probably better. the designs were first way too buff and not cartooney enough." The chibi rows above are replaced by:
- Cartoon-villain proportions: head about a quarter to a third of the height, soft pear/belly bodies (no muscles), bendy arms with big hands and feet.
- Friendly cartoon faces: big rounded eyes with white, iris and highlight, an angled brow for attitude, small mouths with one or two small fangs; no rows of realistic teeth, no flat glowing eye plates.
- A pose that sells each character (bear holding up his honey jar, rabbit with the carrot on his shoulder, raccoon hauling the sack, kangaroo in a boxing guard, ape waving the rolling pin).
- Designs are first drawn as 2D concepts for the creator's OK before anything is rebuilt in 3D.

## New direction: restyle the originals (2026-11-13)
After the cartoon 3D build the creator chose: "lets try using the original skeletons but just tweaking the rough parts and adding the faces + no longer having the stud texture but something more in line with the rest of the game." ADR 0017 (in the place) supersedes ADR 0016.
| Topic | Decision |
|---|---|
| Base | The original Boss and Pet models (source `Documents\CloneAFriendBosses\Bosses_v3.blend`, build scripts in `builds\`): same skeletons, part names and joint spots |
| Boss 1 | Original Brown Bear and its 8 published clips restored; the faceted bear is kept in `ServerStorage.BossFaceted_Attempt` |
| Surface | No stud texture: softened, rounded block edges and smooth colours like the Decorations and Stations; also check whether some textures could work |
| Faces | Swappable faces (ADR 0015) in a blocky cartoon style: square-ish eyes with white, coloured iris and highlight, thick brow, simple mouth |
| Rough parts | Stiff animations and ugly details |
| Surface (tested in Blender, 2026-11-13) | **Smooth**: rounded block edges (bevel), brighter and more saturated colours of the same hues, plain smooth surface. Fabric and Vivid variants were rejected. Render: `Assets/Bosses/renders/surface_test.png` |
| Details to fix | Jagged fur clusters (Bear, Champ N Son); plain belly squares -> shaped belly patches; Rabbeat's eye patch, strap and hidden carrot; Le Ape's small head; Paladin Rhino's noisy armour plates |
| Animations | Remake every clip, Boss by Boss, on the original skeletons: smooth curves at 30 fps, same names and attack timings, plus the Hurt flinch. Each must be republished |

## Built: restyled originals (2026-11-13)
- Source: `Assets/Bosses/orig/` (copies of the original `builds\` scripts) + `SmoothLib.py`; Blender file `Assets/Bosses/Originals_Restyle.blend` (the original `Documents\CloneAFriendBosses` is untouched).
- All ten Bosses and Pets approved from renders (`Assets/Bosses/renders/RS_*`), uploaded (one FBX per Boss + Pet), rigged by `BossRigSmooth.buildRS` from `BossRigDataRS`, and swapped into `BossModels` / `PetModels`. Old models in `ServerStorage.BossBackup_BeforeRestyle`.
- Faces: Bosses get the full blocky set (Grumpy, Angry, Roar, Hurt, Dazed, Blink, glances); RoboJawsh, Grave Wyrm and Obsidian Dragon swap eyes only (their grin, jaw and snout stay). Pets: Happy + Blink.
- Same skeletons, so the 82 published clips still play: tested with a forced Paladin Rhino fight (joints move, faces swap, no errors).
- **Next:** remake the stiff clips Boss by Boss (smooth curves, same names and timings, plus Hurt), then republish them.

## Built: Boss 1 animations (2026-11-13)
- Key poses: `ServerStorage.BossClips.B01` (original skeleton; legs "grounded" so the feet stay planted when the body leans or crouches). Baked at 30 fps with smooth Catmull-Rom curves into the same 8 clip names, lengths and attack timings, plus `Boss1Hurt`.
- Published through Open Cloud and `PublishedId` filled in; IDs in `Assets/Bosses/orig/export/anim/published_ids.json`.
- Publish route (works without the old Blender upload server): Studio evaluates the key poses -> `Assets/Bosses/orig/anim_bake.py` (Python port of the baker) writes `.rbxmx` -> upload from `Assets/Stations and Weapons` as Animation assets.
- Tested: forced Boss 1 fight plays the published clips (Idle, Strike, Hurt, SlamWind/Leap/Hit), no errors. Not yet watched by eye in a running game.
- Next: Bosses 2-10, same way.
- **Boss 2 animations (2026-11-13):** `BossClips.B02`: Stomp Kick (right-leg kick on the impact beat, standing leg planted), Carrot Hop (deep crouch, tucked leap, squat landing), foot-thumps on the Intro pound beats, a hoppy Idle and Walk, plus Hurt. Published; tested in a forced Boss 2 fight (Strike and the slam chain played), no errors.
- **Boss 3 animations (2026-11-13):** `BossClips.B03`: sneaky hunched Idle (hands rubbing), tiptoe Walk, Claw Hook Strike, Coin Toss (SpecialWind reaches into the loot sack and holds; SpecialThrow is an overhand flick, release 0.12), cackling Intro, plus Hurt. Published.

## Built: Bosses 4-10 animations (2026-11-13)
- Key poses are now written in Python: `Assets/Bosses/orig/clipkit.py` (same helpers as the Luau modules: `arms`, `grounded`/`G`, 4-leg grounding for the rhino) and one script per Boss: `B04_clips.py` ... `B08_clips.py`, `dragon_clips.py` (Grave Wyrm + Obsidian Dragon share it). `python B0N_clips.py` writes `export/anim/<tag>_keys.json` + `<tag>_meta.json` (faces, events), bakes the `.rbxmx` and copies them to `Assets/Stations and Weapons` for upload.
- In Studio, `ServerStorage.BossClipApply.apply{...}` sets `PublishedId` + `Expressions` on each `FightAnimations` sequence (old sequence backed up in `BossBackup_BeforeRestyle`, a stub created for the new `Hurt`). The Studio keyframes of Bosses 4-10 are still the old clips; the published ID is what plays.
- Same clip names, lengths, Hold and Event_ timings as before, plus `Boss<N>Hurt` for every Boss.
  - 4 Champ N Son: boxer guard bounce, kangaroo hop Walk, right cross; Title Fight Combo = jab 0.3, cross 0.65, hook 1.0, leans back for the joey 1.25, uppercut 1.85.
  - 5 Le Ape: heavy gorilla sway, rolling-pin overhead smash; Kitchen Catastrophe = scoop from the apron (hold), flour-bomb throws, two-fist slam (0.15); chest-pound Intro.
  - 6 Paladin Rhino: diagonal walk, looping gallop Charge, horn toss Strike; hoof scrapes (hold), slams through at 0.1, rears up and stomps at 0.6.
  - 7 Lion King: regal chest-out Idle (fist on hip, scepter right), Walk taps the scepter, backhand swing; Royal Decree raises the scepter (hold) and slams it at 0.15.
  - 8 RoboJawsh: servo Idle scan, stomping Walk (0 / 0.7), hammer-fist Strike; Full Payload braces launchers (hold), torpedo recoil (0.05), booster jump (launch 0.3, slam 0.8).
  - 9 Grave Wyrm / 10 Obsidian Dragon: wing flaps on Hover (flap at 0), FlyUp downstroke at liftoff, tucked SpecialDive, landing slam; Obsidian Dragon is slower and heavier and has the Cast (claws thrust down at erupt 0.45). They have no Roar mouth, so faces use Angry.
- Tested: all 74 clips of Bosses 3-10 load on their rigs in Play mode, and a forced Obsidian Dragon fight played its whole chain (Intro, Walk, Strike, Hurt, SpecialWind, FlyUp, Hover, Cast, SpecialDive, SpecialHit) with no script errors. 92 boss clips in `FightAnimations` all have a `PublishedId`; IDs in `published_ids.json`.
- Not yet watched by eye in a running fight for Bosses 3-9; poses were checked on still previews (Champ's jab, the rhino's rear-up and gallop, the dragon wings).
