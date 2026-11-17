---
tags: [design, clone-a-friend, ui, mobile]
game: Clone a Friend
date: 2026-11-16
---
# Clone a Friend: Mobile UI (phones in landscape)

Fixes for phones held sideways (about 360–430 px tall), found on a real phone: the HUD ran into Roblox's jump button, windows covered the Sidebar, and text overlapped. Glossary words: Sidebar, Money Counter, Boss Timer, Boss Pity, Boss Bar, Your Stations (ServerStorage.Docs.CONTEXT).

## Problems found (phone screenshots)
- The Boss Timer and both Boss Pity lines sat on top of the Shop button.
- Sidebar: the Settings gear covered "Rewards", and the Luck clover covered "Index".
- The Inventory window ran into the Money Counter, and the Friend tooltip covered the tabs.
- The Money Counter sat under the jump button (gems "55" right on it).
- Boss Fight: the Boss Bar took half the screen, and the Fighters Panel covered the income.
- Loading screen: SKIP sat on top of the progress bar and its tip.
- The Tutorial card covered Build and Rebirth.
- PC too: income cash icons launched right on top of "x2 CASH".

## Decisions (grilling, 2026-11-16)
| Topic | Decision |
|---|---|
| Who gets what | Overlap fixes apply **everywhere**. Layout moves are **touch only** (`UIStyle.isTouch()`: `UserInputService.PreferredInput == Touch`, like Roblox's PlayerModule; Studio's device emulator reports a mouse too, so "touch and no mouse" missed it); the PC layout stays the same |
| Money Counter (touch) | **Bottom centre**: Cash and Gems in one row, with the income / Cash Boost on one line above |
| Boss Pity (touch) | Folded into the Boss Timer; **hold** the timer to drop the two lines out, let go to fold them back |
| Sidebar (touch) | Hangs right under the Boss Timer and shrinks (down to 50%) to stay above the Settings gear + Luck row |
| Windows | **Shrink to fit**: on touch they centre in the space right of the Sidebar and stay above the Money Counter |
| Inventory tooltip (touch) | Beside the finger (right, else left), not above it |
| Boss Fight (touch) | Boss Bar compact, centred right of the Sidebar; Fighters Panel top-right under it, kept above the jump button |
| Placing Stations (touch) | Rotate / Place / Cancel stacked on the **right above the jump button**; the hint moves to the top |
| Moving a Station (touch) | **Drag** it: a touch that starts on the preview drags it, and the camera holds still. A quick tap elsewhere still moves it there, and a camera drag no longer moves it |
| Loading screen | On short screens (< 560 px) SKIP sits to the right of the bar, on the same row |
| Backups | `ServerStorage.ScriptBackups_BeforeMobileFix` (disabled copies of every script touched) |

## Where it lives
- `UIStyle`: `isTouch`, `freeStrip`, `guiArea`, `sidebarRight`, touch Sidebar fit, `placeWindow` touch branch. Also fixes `sidebarRight` looking at `Sidebar.Buttons` instead of `Sidebar.Column.Buttons`.
- `MoneyCounter`, `CashFlyFX` (where the stream starts), `PityLines` + `BossClient` (hold to show; Boss Bar), `FightersPanel`, `InventoryUI` (tooltip), `TutorialUI` (card), `BuildUI` (placement column and drag), `ReplicatedFirst.LoadingScreen`.

## Not changed
- Menus built on `StudMotion.Window` (Shop, Gem Shop, Rebirth, Index, Rewards, Settings) still scale with `ScreenScale`. They aren't moved right of the Sidebar; check them on a phone.
- The Admin button (admins only).
