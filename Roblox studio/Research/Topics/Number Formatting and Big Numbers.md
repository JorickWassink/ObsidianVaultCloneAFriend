---
topic: Number formatting
tags: [research, topic]
---
# Number Formatting and Big Numbers

Simulator economies reach huge numbers fast ([[Grow a Garden]] seeds up to 1Q; [[Steal An Egg]] trails to 5Q).

## Suffixes seen
[[Grow a Garden]] uses: **K** (1e3), **M** (1e6), **B** (1e9), **T** (1e12), **QA** (1e15), **QI** (1e18), **SX** (1e21).
Before Sept 2025 it showed trillions as "1,000B". It was changed because long numbers are unreadable. During one event it **converted every 1QA sheckles into 1 "Flower"** just to shorten the display.

Other games use the same style: $1.5M, 10Qa ([[Steal a Brainrot]]), 2.5B speed ([[Steal An Egg]]).

## Display tricks
- **A currency symbol right after the number** (¢ in [[Grow a Garden]], $ elsewhere).
- **Percent stats can be huge** ([[Catch Bugs!]] luck "+17,075%"). Inflated numbers feel powerful.
- **Progress bars with both numbers** ("$3Qa / $10Qa" in the [[Steal a Brainrot]] rebirth UI).

## Implementation notes
- Store values as numbers. Luau doubles are exact to 2^53 ≈ 9e15, so beyond ~9Q precision drops. Plan for this if your economy goes that high: cap it, prestige-reset it, or switch to a {mantissa, exponent} format.
- One shared `FormatNumber(n)` module for the HUD, shops, leaderstats and billboards.
- Suffix table: `{"", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"}`.

```lua
local SUFFIXES = {"", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"}
local function formatNumber(n: number): string
	local i = 1
	while math.abs(n) >= 1000 and i < #SUFFIXES do
		n /= 1000
		i += 1
	end
	if i == 1 then
		return tostring(math.floor(n))
	end
	-- "1.50" -> "1.5", "10.00" -> "10"
	local s = string.format("%.2f", n):gsub("0+$", ""):gsub("%.$", "")
	return s .. SUFFIXES[i]
end
```

## Related
[[UI Design]] · [[Balancing]]
