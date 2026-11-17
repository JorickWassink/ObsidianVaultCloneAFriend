---
topic: UI design
tags: [research, topic, visual]
---
# UI Design

Based on actual in-game screenshots from the wikis. More images are in [[Visual Design Reference]] and each game's UI gallery.

## Side-by-side
![GaG seed shop|300](https://static.wikia.nocookie.net/growagarden/images/1/1d/SeedshopUI.png/revision/latest) ![GaG gear shop|300](https://static.wikia.nocookie.net/growagarden/images/6/60/GearShopNewUI.png/revision/latest)
![SAB index|360](https://static.wikia.nocookie.net/stealabr/images/a/ae/Index.png/revision/latest) ![SAB rebirth|360](https://static.wikia.nocookie.net/stealabr/images/6/67/Screenshot_2026-01-24_162225.png/revision/latest)
![Catch Bugs mutation cards|600](https://static.wikia.nocookie.net/catch-bugs/images/1/12/Mutations_Showcase.png/revision/latest)

## Two dominant panel styles
| | Themed / "world-material" | Flat dark |
|---|---|---|
| Example | [[Grow a Garden]] shops | [[Steal a Brainrot]] index & rebirth, [[Fisch]] |
| Look | Wood-plank brown frame, grass-green border, cartoon font | Slate/navy translucent panel, white bold sans font |
| Pros | Instantly on-theme and charming | Clean, readable, easy to reuse everywhere |
| Cons | More art work per screen | Can feel generic |

## Patterns that repeat
### Shop list cards ([[Grow a Garden]])
- **One item per row:** a big render on the left, then name (large bold), stock ("X5 Stock"), price (green), and a **rarity pill** on the right (grey Common, blue Rare, yellow Legendary).
- **Header:** the countdown to the next restock ("New seeds in 3m 9s") with a bright yellow **RESTOCK** button (paid) right next to it, and a red X close.
- **Sold-out items stay visible**, with "NO STOCK" in red. You see what you're missing, which builds desire.
- Small round **ⓘ info buttons** on gear explain what it does.

### Collection index ([[Steal a Brainrot]])
- A grid of cards; unowned entries are **black silhouettes**.
- **Mutation tabs** down the left, each label in its own color (Gold yellow, Diamond cyan, Rainbow gradient, Cyber blue). Timed ones show a countdown ("41d 20h").
- A search bar and a counter (343/463) at the top.
- A progress bar at the bottom with the reward spelled out ("Collect 75% Normal Brainrots for +0.5x Base Multi").

### Confirmation for big decisions ([[Steal a Brainrot]] rebirth)
- A **red warning line** at the top (what you lose).
- **"You Will Unlock"** reward tiles in a row (multiplier, cash, lock time, slot, new gear).
- **Requirements** with a progress bar ($3Qa / $10Qa) and the required item cards.
- **One big gold primary button.**

### Item cards ([[Catch Bugs!]])
- Stacked colored text: **mutation name (mutation color) → rarity (rarity color) → item name → weight**.
- A star in the corner for favorites.

### Minigame bars
- [[Fisch]]: a horizontal bar. Hold to move right, release to drift left, and keep the fish inside it.
- [[Storage Hunters Open World]]: a moving marker plus a colored target zone, where the zone's color hints at contents.
- [[Catch Bugs!]]: a slider whose width depends on net Strength.

## Color coding
- **Rarity colors are the most important UI language.** Every game has a ladder; see [[Rarity Systems Compared]].
- **Green = money/price**, **red = warning/no stock/close**, **yellow/gold = primary or premium action** (Restock, Rebirth).
- Special tiers get **gradients or animated** text (rainbow Exotic in [[Catch Bugs!]], Rainbow mutation tab in [[Steal a Brainrot]]).

## Typography
- **Chunky rounded display font with a thick dark outline** for currency and numbers ([[Grow a Garden]] "2.8QA¢"). Readable on any background.
- **Bold uppercase** for buttons and signs (RESTOCK, NO STOCK, QUICK SELL, REBIRTH).
- Big numbers use **suffixes**; see [[Number Formatting and Big Numbers]].

## In-world UI (diegetic)
- **Shops are physical stalls** with signs ([[Grow a Garden]] "SEED SHOP", [[Steal a Brainrot]] "Robux Shop" in floating pink 3D text).
- **Store signage** in [[Storage Hunters Open World]]: a black sign, green trim, a cash icon and a white label.
- Walking up to an NPC opens the menu, which keeps the menu count low.

## Mobile-first details
- Big tap targets (Shake button in [[Fisch]], RESTOCK).
- Favoriting has separate controls per platform (right-click, double-tap, L2/LT in [[Grow a Garden]]).
- Vertical scrolling lists rather than dense grids for shops.

## Second batch: more UI patterns
![Blox Fruits stats|360](https://static.wikia.nocookie.net/roblox-blox-piece/images/c/c2/NewStats.jpeg/revision/latest) ![MM2 crafting|360](https://static.wikia.nocookie.net/murder-mystery-2/images/c/c6/Crafting_Station.png/revision/latest)
![Adopt Me role picker|300](https://static.wikia.nocookie.net/adoptme/images/1/12/Adopt_Me%21_Choose_a_role.jpeg/revision/latest) ![99 Nights crafting bench|340](https://static.wikia.nocookie.net/99-nights-in-the-forest/images/6/6b/Crafting_Bench_3_In-game.png/revision/latest)

### Stat allocation ([[Blox Fruits]])
- A row per stat, each with **its own color and icon** (Melee red fist, Defense blue shield, Sword green, Gun orange, Fruit purple).
- "Lv. 2804 (MAX)" on the right and a **yellow +1 button** per row.
- A Custom Amount input, Stat Points remaining, and a **Refund** button.
- An orange-yellow header bar with a bold title, a blue **?** help button and a red **X**.

### Crafting / salvage ([[Murder Mystery 2]])
- A dark panel with a **red warning banner**.
- Recipe rows: a **"?" silhouette** for random rewards, a rarity-colored name, and material slots with counts.
- **Craft / Salvage tab toggle** at the top right, then materials → reward → **Confirm**.

### Themed paper UI ([[Adopt Me!]])
- The role picker is a **lined paper note pinned to a cork board** (red and teal push pins). Very warm and kid-friendly.
- Rounded font, with an orange vs blue color pair for the two choices.

### Diegetic UI ([[99 Nights in the Forest]])
- Resource counts on **signs attached to the crafting bench** in the world, not in a menu.
- **The map stops working if the campfire goes out**, so the UI is tied to game state.

### Size as a rarity signal ([[Pet Simulator 99]])
- Titanic pet icons are **~4× normal size** with a **crown** instead of stars. Rarity is shown by icon size.

### Anti-scam trading UIs
- [[Adopt Me!]]: a 5-second countdown that **resets on every change**, a trade license test, and distinct Mega Neon icons.
- [[Murder Mystery 2]]: a 6-second wait after each change, and level 10 required.
- [[Pet Simulator 99]]: a 3-second cooldown before newly listed booth items can be bought.

### Physical lobby menus ([[Blue Lock Rivals]])
![BLR lobby|360](https://static.wikia.nocookie.net/bluelockrivals-roblox/images/a/af/Hallowlobby.png/revision/latest) ![BLR spins area|360](https://static.wikia.nocookie.net/bluelockrivals-roblox/images/0/06/Hallowspins.png/revision/latest)
- The lobby **is** the main menu: glowing 3D signs over terminals (PLAY, event, SPINS, 8v8), **floor arrows** guiding new players to the Play terminal, and an event countdown on a big screen.
- **The gacha is a room** with glowing platforms and a billboard advertising the newest character.
- Position selection uses a **bird's-eye view of the field** with colored jerseys on each spawn spot.

### One-button UI ([[Sols RNG]])
![Sol's RNG roll button|300](https://static.wikia.nocookie.net/sol-rng/images/9/97/AutoRoll_New.gif/revision/latest)
- **One central Roll button** with a counter ("x2 Luck Ready"), flanked by **Auto roll** and **Quick roll** toggles. Thin white outlines on dark translucent boxes.
- **Chat is the feed:** rare rolls post color-coded messages; the rarest get a [GLOBAL] prefix in every server.
- **Rarity-threshold settings** for auto-equip, skip warnings, cutscene skipping and chat filtering.

## Checklist for my UI
- [ ] Rarity color ladder defined once and used everywhere
- [ ] Shop cards: render, name, price (green), rarity pill, stock
- [ ] Restock timer plus a paid restock button in the header
- [ ] Silhouettes for undiscovered items
- [ ] Warning plus "You will unlock" plus a single primary button for resets
- [ ] Outlined chunky number font, with suffixes for big numbers
- [ ] In-world stalls/signs for each shop
- [ ] A distinct color and icon per stat or category
- [ ] "?" silhouettes for random rewards in craft or gacha menus
- [ ] Trade countdown that resets on every change (if trading)
- [ ] Bigger icons or a crown for the top rarity

## Related
[[Visual Design Reference]] · [[Art Style]] · [[Rarity Systems Compared]] · [[Number Formatting and Big Numbers]]
