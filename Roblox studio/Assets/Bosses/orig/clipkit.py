# clipkit.py: Python authoring kit for boss clips (Bosses 4-10), same conventions as the Luau BossClips.B01-B03 modules.
# Pose = [rx, ry, rz, px, py, pz] in degrees / studs, per part name (Body, Head, LeftUpperArm, ...).
#   +rx swings a limb forward, tips the Body back, tilts the Head up, drops a Tail; left limb out = -rz, right out = +rz.
# grounded() keeps feet planted by subtracting the Body's rx/rz/px/py/pz from the legs.
# emit(tag, clips) writes export/anim/<tag>_keys.json + <tag>_meta.json, bakes .rbxmx (anim_bake.py) and copies them to
# the approved upload folder Assets/Stations and Weapons.
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ANIM = os.path.join(HERE, "export", "anim")
UPLOAD = os.path.normpath(os.path.join(HERE, "..", "..", "Stations and Weapons"))
REST = {}

def pad(v):
    v = list(v) + [0] * (6 - len(v))
    return [round(float(x), 3) for x in v[:6]]

def merge(*ts):
    out = {}
    for t in ts:
        for k, v in t.items(): out[k] = list(v)
    return out

def arms(lx, lz, rx, rz, lowL=0, lowR=None, ly=0, ry=0):
    return {"LeftUpperArm": [lx, ly, lz], "RightUpperArm": [rx, ry, rz],
            "LeftLowerArm": [lowL, 0, 0], "RightLowerArm": [lowL if lowR is None else lowR, 0, 0]}

LEGS2 = ("LeftLeg", "RightLeg")
LEGS4 = ("LeftFrontLeg", "RightFrontLeg", "LeftBackLeg", "RightBackLeg")

def grounded(p, legs=LEGS2):
    b = pad(p.get("Body", []))
    for leg in legs:
        l = pad(p.get(leg, []))
        p[leg] = [l[0] - b[0], l[1], l[2] - b[2], l[3] - b[3], l[4] - b[4], l[5] - b[5]]
    return p

def G(*ts, legs=LEGS2):
    return grounded(merge(*ts), legs)

def clip(name, length, keys, loop=False, hold=False, priority="Action", events=None, expressions=""):
    return {"name": name, "length": length, "loop": loop, "hold": hold, "priority": priority,
            "events": events or {}, "expressions": expressions, "keys": keys}

def emit(tag, clips):
    keys, meta = {}, {}
    for k, c in clips.items():
        assert abs(c["keys"][-1][0] - c["length"]) < 1e-6, f"{c['name']}: last key {c['keys'][-1][0]} != length {c['length']}"
        keys[k] = {"name": c["name"], "length": c["length"], "loop": c["loop"], "priority": c["priority"],
                   "keys": [[t, {j: pad(v) for j, v in p.items()}] for t, p in c["keys"]]}
        meta[c["name"]] = {"length": c["length"], "loop": c["loop"], "hold": c["hold"], "priority": c["priority"],
                           "events": c["events"], "expressions": c["expressions"]}
    json.dump(keys, open(os.path.join(ANIM, f"{tag}_keys.json"), "w"))
    json.dump(meta, open(os.path.join(ANIM, f"{tag}_meta.json"), "w"), indent=1)
    subprocess.run([sys.executable, os.path.join(HERE, "anim_bake.py"), tag], check=True)
    for c in clips.values():
        shutil.copy(os.path.join(ANIM, c["name"] + ".rbxmx"), UPLOAD)
    print("meta:", json.dumps({n: {"expr": m["expressions"]} for n, m in meta.items()}))
