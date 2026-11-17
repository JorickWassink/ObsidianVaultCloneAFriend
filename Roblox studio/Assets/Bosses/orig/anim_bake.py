# anim_bake.py: Python port of ServerStorage.BossClipBaker (Catmull-Rom between designed key poses, 30 fps) that writes
# KeyframeSequence .rbxmx files in the same format as Documents\CloneAFriendBosses\builds\RobloxUpload.build_rbxmx, ready
# for an Open Cloud "Animation" upload. Key poses come from Studio: BossClips.<tag> evaluated to export/anim/<tag>_keys.json.
# Joint tree from export/<tag>_rig.json (bones: name, parent, ...).
#   python anim_bake.py B01
import json, math, os, sys
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "export"); ANIM = os.path.join(EXP, "anim")
FPS = 30
PRIORITY = {"Idle": 0, "Movement": 1, "Action": 2}

def cr(p0, p1, p2, p3, u):
    u2, u3 = u * u, u * u * u
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u3)

def channels(pose):
    c = [0.0] * 6
    if pose:
        for i in range(6): c[i] = float(pose[i]) if i < len(pose) else 0.0
    return c

def sample(spec, joints, t):
    keys = spec["keys"]; n = len(keys)
    i = 0
    while i < n - 1 and keys[i + 1][0] <= t: i += 1
    if i >= n - 1: i = n - 2
    k1, k2 = keys[i], keys[i + 1]
    span = max(1e-6, k2[0] - k1[0]); u = min(1.0, max(0.0, (t - k1[0]) / span))
    def at(j):  # j is a 0-based index; mirrors the Luau at() with 1-based indices
        if j < 0: return keys[n - 2] if spec["loop"] else keys[0]
        if j > n - 1: return keys[1] if spec["loop"] else keys[n - 1]
        return keys[j]
    k0, k3 = at(i - 1), at(i + 2)
    get = lambda k, name: k[1].get(name) if isinstance(k[1], dict) else None
    out = {}
    for name in joints:
        a, b, c, d = channels(get(k0, name)), channels(get(k1, name)), channels(get(k2, name)), channels(get(k3, name))
        out[name] = [cr(a[ch], b[ch], c[ch], d[ch], u) for ch in range(6)]
    return out

def matrix(rx, ry, rz):
    """rotation of CFrame.Angles(rx, ry, rz) = Rx * Ry * Rz (radians), row-major R00..R22"""
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    Rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]
    Ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]
    Rz = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]
    mul = lambda A, B: [[sum(A[r][k] * B[k][c] for k in range(3)) for c in range(3)] for r in range(3)]
    M = mul(mul(Rx, Ry), Rz)
    return [M[r][c] for r in range(3) for c in range(3)]

def bake(spec, children, joints):
    ref = [0]
    def r(): ref[0] += 1; return "RBX%d" % ref[0]
    f = lambda x: repr(round(float(x), 6))
    names = ["X", "Y", "Z", "R00", "R01", "R02", "R10", "R11", "R12", "R20", "R21", "R22"]
    def pose_xml(name, vals):
        v = vals.get(name)
        if v:
            comps = [v[3], v[4], v[5]] + matrix(math.radians(v[0]), math.radians(v[1]), math.radians(v[2]))
        else:
            comps = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        cf = "".join(f"<{n}>{f(c)}</{n}>" for n, c in zip(names, comps))
        kids = "".join(pose_xml(c, vals) for c in children.get(name, []))
        return (f'<Item class="Pose" referent="{r()}"><Properties><string name="Name">{escape(name)}</string>'
                f'<CoordinateFrame name="CFrame">{cf}</CoordinateFrame><token name="EasingStyle">0</token>'
                f'<token name="EasingDirection">0</token><float name="Weight">1</float></Properties>{kids}</Item>')
    frames = max(1, round(spec["length"] * FPS))
    keys = ""
    for fr in range(frames + 1):
        t = fr / FPS
        vals = sample(spec, joints, t)
        keys += (f'<Item class="Keyframe" referent="{r()}"><Properties><string name="Name">Keyframe</string><float name="Time">{f(t)}</float></Properties>'
                 + pose_xml("HumanoidRootPart", vals) + "</Item>")
    return ('<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">'
            f'<Item class="KeyframeSequence" referent="{r()}"><Properties><string name="Name">{escape(spec["name"])}</string>'
            f'<bool name="Loop">{"true" if spec["loop"] else "false"}</bool><token name="Priority">{PRIORITY[spec["priority"]]}</token></Properties>{keys}</Item></roblox>'), frames + 1

def main(tag):
    rig = json.load(open(os.path.join(EXP, f"{tag}_rig.json")))
    children, joints = {}, []
    for name, parent, *_ in rig["bones"]:
        if parent: children.setdefault(parent, []).append(name); joints.append(name)
    specs = json.load(open(os.path.join(ANIM, f"{tag}_keys.json")))
    out = []
    for key, spec in specs.items():
        xml, n = bake(spec, children, joints)
        p = os.path.join(ANIM, spec["name"] + ".rbxmx")
        open(p, "w", encoding="utf-8").write(xml)
        out.append(f"{spec['name']}: {n} keyframes, {os.path.getsize(p) // 1024} KB")
    print("\n".join(sorted(out)))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "B01")
