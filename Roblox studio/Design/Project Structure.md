---
tags: [design]
---
# Project Structure

```
ServerScriptService
  CoinService        (Script)
  DataManager        (ModuleScript)
ReplicatedStorage
  Config             (ModuleScript)
  Remotes/
    CollectCoin, PurchaseItem, UpdateCoins, RequestData
StarterPlayer/StarterPlayerScripts
  ShopController     (LocalScript)
  HUDController      (LocalScript)
```

> [!warning] Rules
> - The server owns all currency. The client only asks.
> - Every Client → Server remote gets a note in `Remotes/` with its validation checklist.
