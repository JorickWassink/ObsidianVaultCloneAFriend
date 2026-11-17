# Roblox Dev Vault: how to use

Needs Obsidian 1.9 or newer (Bases is built in). No community plugins required.

1. Open this folder in Obsidian: **Open folder as vault**.
2. Open **00 Home** for the dashboard.
3. To add something, make a new note in the right folder and insert a template
   (Command palette → *Templates: Insert template*). Templates live in `Templates/`.
   If the command is missing, turn on **Settings → Core plugins → Templates**.

| Folder    | One note per…               | Table              |
|-----------|-----------------------------|--------------------|
| Scripts   | Script / LocalScript / Module | Bases/Scripts.base |
| Remotes   | RemoteEvent / RemoteFunction | Bases/Remotes.base |
| Assets    | Mesh, sound, image, animation | Bases/Assets.base  |
| Data      | DataStore key / schema       | Bases/Data.base    |
| Features  | Feature on the roadmap       | Bases/Features.base |
| Bugs      | Bug                          | Bases/Bugs.base    |

Tables find notes by **folder**, so keep each note in its folder.
Property values the tables expect:
- Script `runs_on`: Server, Client, Shared
- Feature `status`: Planned, In progress, Done · `priority`: High, Medium, Low
- Bug `status`: Open, In progress, Fixed · `severity`: High, Medium, Low
