---
topic: Cutscenes
tags: [research, topic, visual]
---
# Cutscenes

How cutscenes are used across the researched games: when they play, who sees them, how long they are, and whether you can skip them. At the end there's a guide to building them in Roblox Studio.

> [!summary] The big picture
> Roblox cutscenes are **short (a few seconds), tied to a reward or milestone, and often shown to the whole server**. The best ones **tell you how good the reward is before you see it** (Sol's RNG), and the worst-received ones are **long and forced on everyone** (Steal a Brainrot's snap cutscene, which was removed after complaints).

## 1. Reveal cutscenes (rarity build-up)
| Game | What triggers it | What happens |
|---|---|---|
| [[Sols RNG]] | Rolling an Epic+ aura | **A different cutscene style for each rarity band.** Epic: black screen with edges glowing in the aura's color. Unique: + a 4-pointed star and a bass drop. Legendary: + a white screen-crack. Mythic: 8-pointed star, colored fog, bell chime. Glorious: unique animation, then a monochrome flash, thunder and a beam for the whole server. Transcendent: fully custom cutscene with its own music. |
| [[Pet Simulator 99]] | Hatching a **Gargantuan** pet | **Shown to everyone in the server:** the sky turns dark, the egg floats up, a crack opens in the sky, the player rises into it and rides the pet back down. One shared cutscene for all Gargantuans; Golden/Rainbow/Shiny shows on the pet. The first pets ever to get a hatch cutscene. |
| [[Fisch]] | Catching a boss fish (Megalodon, Sea Leviathan, Scylla…) | A unique cutscene per boss fish with a shouted line ("WOAH The Meg!", "SHADOW IN THE MIST!"). |

**Patterns:**
- **The build-up escalates with rarity:** darker screen, more star points, louder sound. Players learn to read the signals and get hyped *before* the reveal.
- **The color comes from the reward** (the aura's font color drives the star and background color), so one system serves hundreds of items.
- **Only the very top gets custom work.** Most rarities reuse a template; only the rarest few get bespoke cutscenes.
- **The top tier is shared with others:** server effects, global chat. Your moment becomes everyone's moment.

## 2. Ability / power-up cutscenes
| Game | Cutscene |
|---|---|
| [[Blue Lock Rivals]] | **Awakening cutscenes** for each character style, recreating anime moments with dialogue lines ("I AM... A STRIKER!"), camera cuts to faces, and spirit figures appearing behind the player (a "Monster" for Bachira, a giant skeleton for NEL Nagi). **Shown to everyone, including the goalkeeper.** The match keeps running during it (stamina regenerates), only walking and abilities pause. Limited skins get new awakening cutscenes (a McDonald's-themed Nagi). |
| [[Blox Fruits]] | Some fruit moves trigger a cutscene when they hit (Empyrean Kitsune's held move dashes in and fires an energy ball point-blank). **The user is immune and the target is stunned during it.** Noted to cause lag. |
| [[Rivals]] | **Finishers:** short cosmetic effects after an elimination (Confetti, Petrify, Faceplant, Hacked…). A micro-cutscene sold as a cosmetic. |
| [[Blue Lock Rivals]] | **MVP animations** for the best player at the end of a match, chosen from goals, assists, steals and saves. |

**Patterns:**
- **Keep the game state fair:** immunity for the user (Blox Fruits) or let other actions continue (Blue Lock) so a cutscene doesn't become an exploit or a free kill.
- **Cutscene variants are a cosmetic product:** finishers, MVP animations, limited awakening skins.

## 3. Story / world cutscenes
| Game | When |
|---|---|
| [[Blox Fruits]] | Quest milestones: completing island secrets, lowering a boss to 50% HP, the Draco Temple hologram, Colosseum targets (the camera pans to the next target). **The rip_indra battle cutscene can be re-watched** through the NPC Erin ("Let me see"), and the Draco Temple has an "Archive" option. It can't be skipped. |
| [[Fisch]] | **The first time you enter a new area** (each Lost Jungle zone, the Fischmas locations), plus quest completions (Dr Glimmerfin's boat destroying a golden wave) and update launches (the destruction of Atlantis). |
| [[99 Nights in the Forest]] | **Night raids:** drums, then text on ripped paper, then the Deer arrives. A Ram night has its own short cutscene. Day 99 has an ending cutscene. Story events show the Deer eating BBQ ribs or fighting the Bat. |
| [[Steal a Brainrot]] | Event intros (a train ride "cinematic" to the North Pole event; the Admin Abuse War story animation of the developer stomping a tiny rival dev). |
| [[Grow a Garden]] | Event cutscenes (e.g. a "Players' Garden Grew" cutscene with its own music track; Sam at the beach for the Summer event). |
| [[Murder Mystery 2]] | **Live event transition:** a countdown hits zero, a cutscene plays, and the whole game turns into the Halloween event. Players online got a free pet. |
| [[Pet Simulator 99]] | Anniversary cutscene with a one-time gift for watching it. |

**Patterns:**
- **First-visit only** (Fisch areas) keeps them special without getting annoying.
- **Re-watchable through an NPC** (Blox Fruits Erin / Archive), so players can show friends or relive it.
- **Live update cutscenes** that everyone watches at the same time become events in themselves, often with a reward for being online.
- **Text-on-paper or simple overlays** (99 Nights) are cheap and effective for horror and lore.

## 4. Small scripted moments (micro-cutscenes)
- [[Sols RNG]] The Limbo: falling into the void plays escalating dialogue ("[ ... ]" → "[ You don't belong here... ]" → "[ Fine. ]") before kicking you out.
- [[Steal a Brainrot]] snap animations: a creator's avatar jumping onto the red carpet and leaving a crater.
- [[Blue Lock Rivals]] AFK World: your avatar kicks a ball every 10 seconds and only scores when you win a grand prize. The reward is shown through a tiny animation.

## 5. What players disliked
- **Long, forced, shared cutscenes:** [[Steal a Brainrot]] players complained that the North Pole event "forces you to watch a long cutscene", and the developer **removed** the snap cutscene for the same reason. In a game where you're protecting or stealing items, losing control is a real cost.
- **Unskippable ones you see often:** [[Sols RNG]] solves this with a rarity threshold setting and a paid Quick Roll that skips the roll animation.
- **Bugs:** resetting during a [[Blox Fruits]] cutscene could break the camera or leave music playing. Cutscene code must handle death, reset and leaving.
- **Unfinished content:** [[99 Nights in the Forest]] players joke that the Day 99 ending cutscene has been unfinished for 2 years. The finale matters.

## 6. Rules of thumb (my synthesis)
1. **Length by frequency:** something seen every few minutes should be 1–3 s (or skippable); a once-per-account milestone can be 10–30 s.
2. **Escalate by rarity** with shared templates; save custom cutscenes for the top few.
3. **Make the top moments social:** server effects, chat messages, or showing the cutscene to everyone.
4. **Never take control in a dangerous moment:** keep the player immune, pause threats, or don't show it to others.
5. **Skippable after the first time,** with a settings threshold.
6. **Re-watchable** for story cutscenes (an NPC or archive).
7. **Handle death, reset and leaving** during cutscenes.
8. **Sound sells it:** bass drops, chimes, thunder, music stings, shouted lines.

## 7. How to build them in Roblox Studio
Common building blocks (based on standard Roblox APIs):
- **Camera:** in a LocalScript, set `workspace.CurrentCamera.CameraType = Enum.CameraType.Scriptable`, move it with **TweenService** between invisible "camera parts" placed in the world, then set it back to `Custom`.
- **Character animation:** play an `Animation` on the character's `Animator` (made with the Animation Editor or a plugin like Moon Animator).
- **Overlays:** a ScreenGui with black letterbox bars, a full-screen Frame for fades, colored glow edges (UIGradient / ImageLabel) and text. This is how Sol's RNG-style reveals work: mostly UI over a darkened screen.
- **Effects:** ParticleEmitters, Beams, `Lighting` changes (ColorCorrection for the monochrome flash, Atmosphere for fog), and Sounds.
- **Shared cutscenes:** the server fires a RemoteEvent to all clients (`FireAllClients`) with the cutscene ID and data (e.g. the aura color), and each client plays it locally.
- **Server-authoritative reward:** decide and grant the reward on the server **before** the client plays the reveal; the cutscene is only presentation.

```lua
-- LocalScript: play a simple camera cutscene through a list of camera parts.
local TweenService = game:GetService("TweenService")
local camera = workspace.CurrentCamera

local function playCutscene(shots: { BasePart }, secondsPerShot: number)
	camera.CameraType = Enum.CameraType.Scriptable
	camera.CFrame = shots[1].CFrame
	for i = 2, #shots do
		local tween = TweenService:Create(
			camera,
			TweenInfo.new(secondsPerShot, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut),
			{ CFrame = shots[i].CFrame }
		)
		tween:Play()
		tween.Completed:Wait()
	end
	camera.CameraType = Enum.CameraType.Custom
end
```
*Add a skip button that cancels the tween and restores the camera, and restore the camera if the character dies mid-cutscene.* The `roblox-animation-vfx` skill has more on animation tracks, particles and camera effects.

## Related
[[Sols RNG]] · [[Blue Lock Rivals]] · [[Pet Simulator 99]] · [[Blox Fruits]] · [[Fisch]] · [[99 Nights in the Forest]] · [[Visual Design Reference]] · [[Retention and Live Events]]
