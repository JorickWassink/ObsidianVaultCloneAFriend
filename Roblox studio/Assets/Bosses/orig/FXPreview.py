# EFFECTS PREVIEW
# 1. Set the boss and the clip below (clips: Idle, Walk, Strike, Intro, Defeat and the special clips listed per boss)
# 2. Press Alt+P (or the play button at the top of this editor) to run it
# 3. Press Space in the 3D view to play: the boss and its effects play together. Other bosses and effects are hidden.
#    Bosses: B01 bear, B02 rabbit, B03 raccoon, B04 kangaroo, B05 gorilla, B06 rhino, B07 lion, B08 shark mech, B09 grave wyrm, B10 runelord
BOSS = "B10"
CLIP = "Cast"

import bpy
for name, src in (("studlib","StudLib"),("animlib","AnimLib"),("fxlib","FXLib")):
    if name not in bpy.app.driver_namespace:
        ns = {"__name__": name}; exec(bpy.data.texts[src].as_string(), ns)
        if name == "animlib": exec(bpy.data.texts["AnimSets"].as_string(), ns)
        bpy.app.driver_namespace[name] = ns
F = bpy.app.driver_namespace["fxlib"]
for c in bpy.data.collections:
    if len(c.name) == 3 and c.name[0] in "BP": c.hide_viewport = c.name != BOSS
F["preview"](BOSS, CLIP, 1)
sc = bpy.context.scene
ends = [a.frame_range[1] for a in bpy.data.actions if a.get("fx_boss") == BOSS and a.get("fx_clip") == CLIP]
sc.frame_end = int(max([sc.frame_end] + ends))
act = bpy.data.actions[f"{BOSS}_{CLIP}"]
print(BOSS, CLIP, "events:", {k[3:]: act[k] for k in act.keys() if k.startswith("ev_")})
