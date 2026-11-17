# Clone a Friend: stud-free restyle of the Clone lever, the Hub market stalls and the Arcade Machine.
# Same helpers and look as Assets/Decorations/build_decor.py (rounded primitives, one mesh per colour).
# Run inside Blender:  ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Props Restyle\build_props.py").read(), ns); ns["build_all"]()
# 1 BU = 1 stud, Z up, base at z=0, front = -Y.
# Mesh names: "<Prop>__<colour key>". In Studio the colour key becomes the MeshPart name.
#   LeverConsole  static body; LeverHandle / LeverBall are animated by FriendAvatarSpawner (hinge at z=2.85).
#   Stall         shared stall kit; the "Accent" mesh is recoloured per stand (Market red, Gems blue).
#   MarketProps / GemProps  counter props that sit on the stall (same origin as Stall).
#   ArcadeMachine  keeps the names StationEffects animates: Marquee, Glow1, Glow2.
import bpy, math, json, os

DECOR = r"C:\obsidian\Roblox studio\Assets\Decorations\build_decor.py"
_src = open(DECOR).read()
exec(_src.split("# ---------------- shared bits ----------------")[0], globals())  # helpers + base COLORS only

OUT = r"C:\obsidian\Roblox studio\Assets\Props Restyle"
COLORS.update({
    # lab palette (Clone Tube)
    "LabWhite": "f4f6fa", "LabNavy": "1f2a52", "LabRed": "e5383b", "Chrome": "c9d3df",
    "LabScreen": "4fe3ffn", "LampGreen": "4dff7an", "LampYellow": "ffd23fn", "LampRed": "ff4d4dn",
    "Hazard": "ffc933", "Ink": "22242e",
    # stall
    "Accent": "de2a2c", "Bulb": "fff1a8n", "Gold": "ffc933", "GoldDark": "e0a020", "Steel": "dfe6ee", "Sack": "d9b37a",
    "Gem": "35c8ff", "GemPink": "ff5fc8", "GemPurple": "a66bff", "Velvet": "7a3fd0", "Pot": "c96a3a",
    # arcade
    "ArcPurple": "7b3fe4", "ArcDark": "3a1f96", "Panel": "2b3247", "Bezel": "14204a", "Screen": "16163f",
    "Marquee": "ff4fa3n", "MarqueeStar": "ffd23fn", "Glow1": "35e0ffn", "Glow2": "ff4fa3n",
    "Stick": "2b3247", "StickBall": "e0262c", "Button1": "e0262c", "Button2": "ffc933", "Button3": "35e0ff",
    "PixelGreen": "59ff7an", "PixelYellow": "ffd23fn", "PixelPink": "ff5fc8n", "CoinGlow": "ff9f1cn", "ArtYellow": "ffc933",
})

def star_pts(r_out, r_in, n=5, rot=math.pi / 2):
    pts = []
    for k in range(n * 2):
        r = r_out if k % 2 == 0 else r_in
        a = rot + k * math.pi / n
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts

# ---------------- Clone lever (lab console) ----------------
HINGE_Z = 2.85
def LeverConsole():
    box((3.8, 3.4, 0.45), (0, 0, 0.225), "LabNavy", bevel=0.18)                       # foot
    box((3.5, 0.08, 0.28), (0, -1.71, 0.24), "Hazard", bevel=0.03)                     # hazard strip, front
    for i in range(7):
        box((0.16, 0.1, 0.42), (-1.5 + i * 0.5, -1.74, 0.24), "Ink", bevel=0.02, rot=(0, 0.6, 0))
    box((3.2, 2.8, 2.3), (0, 0, 1.6), "LabWhite", bevel=0.45, seg=4)                   # body
    box((3.34, 2.94, 0.38), (0, 0, 2.05), "LabNavy", bevel=0.15)                       # band
    for y in (-1.48, 1.48):
        for x in (-1.2, -0.4, 0.4, 1.2): ball(0.09, (x, y, 2.05), "LabRed", seg=10, ring=6)
    box((2.7, 2.3, 0.3), (0, 0, 2.8), "LabWhite", bevel=0.14)                          # top cap
    box((0.55, 2.0, 0.06), (0, 0, 2.95), "Ink", bevel=0.02)                             # handle slot
    for sx in (-1, 1):
        box((0.22, 1.0, 1.0), (sx * 0.85, 0, 2.95), "LabNavy", bevel=0.1)                # hinge brackets
        cyl(0.36, 0.12, (sx * 1.02, 0, HINGE_Z), "LabRed", verts=20, bevel=0.04, rot=(0, math.pi / 2, 0))
    cyl(0.32, 2.0, (0, 0, HINGE_Z), "Chrome", verts=20, bevel=0.06, rot=(0, math.pi / 2, 0))  # hinge barrel
    # front: glowing screen with a little DNA helix, status lamps
    box((1.9, 0.12, 1.0), (0, -1.42, 1.25), "LabNavy", bevel=0.08)
    box((1.6, 0.1, 0.72), (0, -1.47, 1.25), "LabScreen", bevel=0.05)
    for i in range(6):
        x = -0.6 + i * 0.24; z = 0.18 * math.sin(i * 1.1)
        ball(0.06, (x, -1.53, 1.25 + z), "LabWhite", seg=8, ring=5); ball(0.06, (x, -1.53, 1.25 - z), "LabNavy", seg=8, ring=5)
    for x, col in ((-0.5, "LampGreen"), (0, "LampYellow"), (0.5, "LampRed")):
        ball(0.13, (x, -1.42, 0.68), col, seg=12, ring=8)
    # side dial (+x)
    cyl(0.4, 0.1, (1.62, 0, 1.25), "LabWhite", verts=20, bevel=0.03, rot=(0, math.pi / 2, 0))
    torus(0.4, 0.06, (1.67, 0, 1.25), "LabNavy", rot=(0, math.pi / 2, 0), seg=20, mseg=6)
    box((0.04, 0.05, 0.3), (1.69, 0.06, 1.33), "LabRed", bevel=0, rot=(0.6, 0, 0))
    # cable out of the back to the ground (towards the Clone Tube)
    tube([(0, 1.35, 0.95), (0, 1.95, 0.7), (0, 2.35, 0.18), (0, 3.1, 0.12)], 0.17, "LabNavy", 10)
    ball(0.26, (0, 1.36, 0.95), "Chrome", seg=12, ring=8)

def LeverHandle():
    cyl(0.17, 3.0, (0, 0, 0), "Chrome", verts=14, bevel=0.03)
    ball(0.24, (0, 0, -1.45), "Chrome", seg=12, ring=8)
    for z in (0.75, 1.05):
        torus(0.2, 0.05, (0, 0, z), "Chrome", seg=14, mseg=6)

def LeverBall():
    ball(0.6, (0, 0, 0), "LabRed", seg=24, ring=16)

# ---------------- Market stall kit ----------------
# Stall frame: ground z=0 (= stand pivot y - 8.5). y = the stand's local z (front = -y).
POSTS = [(-9.4, -2.48), (9.4, -2.48), (-9.4, 1.92), (9.4, 1.92)]
def Stall():
    box((19.8, 4.8, 0.7), (0, -0.28, 0.35), "WoodDark", bevel=0.2)                    # base
    box((19.2, 5.2, 1.6), (0, 3.32, 0.8), "WoodDark", bevel=0.2)                       # keeper deck
    for i in range(4): box((19.0, 0.85, 0.12), (0, 2.2 + i * 0.95, 1.62), "Wood" if i % 2 else "WoodLight", bevel=0.05)
    box((19.2, 4.0, 3.1), (0, -0.28, 2.25), "Wood", bevel=0.3)                          # counter
    for i in range(12):
        box((1.45, 0.18, 2.5), (-8.8 + i * 1.6, -2.32, 2.25), "WoodLight" if i % 2 else "Wood", bevel=0.08)
    box((19.5, 0.32, 0.45), (0, -2.38, 0.95), "Accent", bevel=0.14)
    box((19.5, 0.32, 0.35), (0, -2.38, 3.55), "Accent", bevel=0.12)
    cyl(1.25, 0.22, (0, -2.5, 2.25), "LabWhite", verts=24, bevel=0.06, rot=(math.pi / 2, 0, 0))  # emblem plate
    torus(1.25, 0.14, (0, -2.6, 2.25), "Accent", rot=(math.pi / 2, 0, 0), seg=24, mseg=8)
    box((21.2, 5.6, 0.9), (0, -0.28, 4.25), "WoodLight", bevel=0.35, seg=4)              # counter top
    for (x, y) in POSTS:
        cyl(0.5, 7.5, (x, y, 8.45), "Wood", verts=12, bevel=0.08)
        torus(0.52, 0.12, (x, y, 4.85), "WoodDark", seg=14, mseg=6)
        cyl(0.58, 0.45, (x, y, 10.9), "Accent", verts=12, bevel=0.1)
    # sloped pillow awning: back high, front low
    slope = math.atan(1.6 / 7.4); n = 8; w = 21.6 / n
    for i in range(n):
        x = -10.8 + w * (i + 0.5); col = "Accent" if i % 2 == 0 else "LabWhite"
        box((w + 0.05, 8.2, 0.6), (x, -1.1, 12.85), col, bevel=0.28, seg=4, rot=(slope, 0, 0))
        half = [(1.3 * math.cos(a), -1.3 * math.sin(a)) for a in [k * math.pi / 12 for k in range(13)]]
        prism([(px * (w / 2.7), pz * 0.85) for px, pz in half], 0.32, (x, -5.0, 12.12), col, bevel=0.06)
    cyl(0.32, 21.9, (0, -5.0, 12.12), "LabWhite", verts=14, bevel=0.05, rot=(0, math.pi / 2, 0))  # front roll
    box((21.4, 0.8, 0.8), (0, 2.4, 13.2), "WoodDark", bevel=0.2)
    box((21.0, 0.6, 0.6), (0, -2.48, 11.75), "WoodDark", bevel=0.18)
    # string of bulbs under the front edge
    pts = []
    for s in range(4):
        x0 = -10 + s * 5
        for k in range(6):
            t = k / 5; pts.append((x0 + t * 5, -4.75, 11.55 - 0.55 * math.sin(math.pi * t)))
    tube(pts[::2] + [pts[-1]], 0.04, "Ink", 6)
    for (x, y, z) in pts[1::2]:
        cyl(0.08, 0.14, (x, y, z - 0.07), "Ink", verts=8, bevel=0)
        ball(0.2, (x, y, z - 0.3), "Bulb", seg=10, ring=7)
    # potted plants at the front corners
    for sx in (-1, 1):
        cyl(0.75, 1.3, (sx * 10.7, -3.2, 0.65), "Pot", verts=16, bevel=0.1, r2=0.6)
        torus(0.76, 0.12, (sx * 10.7, -3.2, 1.25), "Pot", seg=16, mseg=6)
        blob(0.95, (sx * 10.7, -3.2, 2.0), "Leaf", (1, 1, 0.9), seed=sx * 3)
        blob(0.6, (sx * 10.7 + 0.4, -3.4, 2.6), "LeafLight", seed=sx * 5)

TOP = 4.7  # counter top height
def _sword(x, y, lean, col_blade="Steel"):
    rot = (0, lean, 0)
    box((0.32, 0.1, 2.0), (x, y, TOP + 2.3), col_blade, bevel=0.04, rot=rot)
    box((1.0, 0.25, 0.22), (x + math.sin(lean) * -0.0, y, TOP + 1.25), "Gold", bevel=0.08, rot=rot)
    cyl(0.12, 0.7, (x, y, TOP + 0.85), "WoodDark", verts=8, bevel=0.03, rot=rot)

def MarketProps():
    # crate of swords (left)
    box((2.6, 2.0, 1.5), (-6.2, 0.2, TOP + 0.75), "Wood", bevel=0.15)
    for z in (0.35, 1.15): box((2.7, 2.1, 0.22), (-6.2, 0.2, TOP + z), "WoodDark", bevel=0.06)
    for x, lean in ((-6.8, -0.18), (-6.0, 0.05), (-5.4, 0.22)):
        rot = (0, lean, 0)
        box((0.3, 0.1, 2.2), (x + math.sin(lean) * 1.5, 0.2, TOP + 2.9), "Steel", bevel=0.04, rot=rot)
        box((0.95, 0.25, 0.2), (x + math.sin(lean) * 0.4, 0.2, TOP + 1.8), "Gold", bevel=0.07, rot=rot)
    # money bag + coin stacks (right)
    blob(0.95, (6.4, 0.6, TOP + 0.85), "Sack", (1, 1, 1.05), lumps=0.12, seed=4, flat_bottom=0.75)
    torus(0.32, 0.1, (6.4, 0.6, TOP + 1.75), "WoodDark", seg=12, mseg=6)
    blob(0.35, (6.4, 0.6, TOP + 2.05), "Sack", lumps=0.1, seed=6)
    for (x, y, n) in ((4.6, -0.6, 5), (5.3, -1.2, 3), (8.0, -0.4, 4)):
        for k in range(n): cyl(0.5, 0.16, (x, y, TOP + 0.08 + k * 0.17), "Gold" if k % 2 else "GoldDark", verts=16, bevel=0.03)
    # front emblem: big coin
    cyl(0.95, 0.25, (0, -2.68, 2.25), "Gold", verts=24, bevel=0.06, rot=(math.pi / 2, 0, 0))
    cyl(0.68, 0.1, (0, -2.83, 2.25), "GoldDark", verts=24, bevel=0.03, rot=(math.pi / 2, 0, 0))

def _gem(r, h, loc, col, rot=(0, 0, 0)):
    x, y, z = loc
    cone(r, h * 0.35, (x, y, z), col, verts=6, rot=(math.pi, 0, 0))
    cyl(r, h * 0.15, (x, y, z + h * 0.24), col, verts=6, bevel=0, r2=r * 0.7)

def GemProps():
    # crystal cluster (left)
    rock(1.0, (-6.2, 0.3, TOP + 0.1), "RockDark", (1.4, 1.1, 0.6), seed=2)
    for (dx, dy, h, tilt, col) in ((0, 0, 2.6, 0, "Gem"), (-0.8, 0.2, 1.8, -0.4, "GemPurple"), (0.8, -0.1, 2.0, 0.35, "Gem"),
                                    (0.2, 0.7, 1.5, 0.2, "GemPink"), (-0.4, -0.6, 1.3, -0.25, "GemPurple")):
        cyl(0.38, h, (-6.2 + dx + math.sin(tilt) * h / 2, 0.3 + dy, TOP + 0.3 + h / 2), col, verts=6, bevel=0.03, rot=(0, tilt, 0))
        cone(0.38, 0.5, (-6.2 + dx + math.sin(tilt) * (h + 0.25), 0.3 + dy, TOP + 0.3 + h + 0.2), col, verts=6, rot=(0, tilt, 0))
    # velvet cushion with a big gem (right)
    box((2.4, 2.0, 0.6), (6.3, 0.3, TOP + 0.3), "Velvet", bevel=0.28, seg=4)
    for (x, y) in ((5.2, -0.6), (7.4, -0.6), (5.2, 1.2), (7.4, 1.2)): ball(0.14, (x, y, TOP + 0.62), "Gold", seg=8, ring=6)
    _gem(0.9, 2.6, (6.3, 0.3, TOP + 1.25), "Gem")
    # small gem pile (front right)
    for k, (x, y, col) in enumerate(((3.6, -1.4, "GemPink"), (4.2, -1.0, "Gem"), (3.9, -1.9, "GemPurple"), (4.6, -1.7, "Gem"), (3.3, -0.9, "GemPurple"))):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.32, location=(x, y, TOP + 0.25))
        _fin(bpy.context.object, col, 0, smooth=False, rot=(k * 0.7, k * 0.4, 0))
    # front emblem: gem
    for s, z in ((1, 0), ):
        pass
    prism([(0, -1.0), (0.85, 0.15), (0.5, 0.65), (-0.5, 0.65), (-0.85, 0.15)], 0.25, (0, -2.68, 2.15), "Gem", bevel=0.05)
    prism([(0, -0.55), (0.4, 0.1), (0.25, 0.4), (-0.25, 0.4), (-0.4, 0.1)], 0.1, (0, -2.84, 2.2), "LabWhite", bevel=0.02)

# ---------------- Arcade Machine ----------------
# Station frame: origin = Base part, front = -y (StandPoint at y=-3.1). Collider 3.5 x 2.9 x 6.3 centred at y=-0.1.
PROFILE = [(1.35, 0.0), (1.35, 6.2), (-1.15, 6.2), (-1.15, 5.2), (-0.55, 3.9), (-1.55, 3.4), (-1.55, 2.95), (-1.0, 2.7), (-1.05, 0.0)]
def ArcadeMachine():
    box((3.7, 3.1, 0.25), (0, -0.1, 0.12), "Ink", bevel=0.08)                          # plinth
    for sx in (-1, 1):
        prism(PROFILE, 0.32, (sx * 1.6, 0, 0.1), "ArcPurple", rot=(0, 0, math.pi / 2), bevel=0.1)
        pr = [(py, pz) for py, pz in [(-1.05, 0.5), (-1.0, 2.7), (-1.55, 2.95), (-1.55, 3.4), (-0.55, 3.9), (-1.15, 5.2), (-1.15, 6.2), (1.35, 6.2)]]
        tube([(sx * 1.79, py, pz + 0.1) for py, pz in pr], 0.07, "Glow1" if sx < 0 else "Glow2", 8)
        star = star_pts(0.75, 0.32)
        prism(star, 0.06, (sx * 1.79, 0.25, 1.9), "ArtYellow", rot=(0, 0, math.pi / 2), bevel=0.02)
        prism(star_pts(0.4, 0.17), 0.06, (sx * 1.79, -0.5, 3.0), "ArtYellow", rot=(0, 0, math.pi / 2), bevel=0.02)
    inner = [(1.3, 0.1), (1.3, 6.15), (-1.1, 6.15), (-1.1, 5.2), (-0.5, 3.9), (-1.5, 3.4), (-1.5, 2.95), (-0.95, 2.7), (-1.0, 0.1)]
    prism(inner, 2.9, (0, 0, 0.1), "ArcDark", rot=(0, 0, math.pi / 2), bevel=0.05)
    box((3.55, 2.95, 0.3), (0, 0.1, 6.35), "ArcPurple", bevel=0.14)                    # top cap
    box((2.9, 0.28, 0.85), (0, -1.22, 5.72), "Marquee", bevel=0.1)
    for x, s in ((-0.85, 0.22), (0, 0.3), (0.85, 0.22)):
        prism(star_pts(s, s * 0.45), 0.06, (x, -1.37, 5.72), "MarqueeStar", bevel=0.01)
    # screen (tilted back)
    th = math.atan(0.6 / 1.3); c = (0, -0.9, 4.55)
    v = (0, -math.sin(th), math.cos(th)); nrm = (0, -math.cos(th), -math.sin(th))
    box((2.6, 0.16, 1.5), c, "Bezel", bevel=0.08, rot=(th, 0, 0))
    def on_screen(a, b, d):
        return (a, c[1] + v[1] * b + nrm[1] * d, c[2] + v[2] * b + nrm[2] * d)
    box((2.25, 0.1, 1.2), on_screen(0, 0, 0.05), "Screen", bevel=0.05, rot=(th, 0, 0))
    invader = ["0100010", "0011100", "0111110", "1101011", "1111111", "1010101"]
    for r_, row in enumerate(invader):
        for k, ch in enumerate(row):
            if ch == "1": box((0.075, 0.04, 0.075), on_screen(-0.3 + k * 0.085, 0.42 - r_ * 0.085, 0.11), "PixelGreen", bevel=0, rot=(th, 0, 0))
    for k in range(5): box((0.07, 0.04, 0.07), on_screen(-0.85 + k * 0.4, -0.15, 0.11), "PixelYellow", bevel=0, rot=(th, 0, 0))
    for (a, b) in ((0, -0.42), (-0.08, -0.5), (0.08, -0.5), (0, -0.5)): box((0.08, 0.04, 0.08), on_screen(a, b, 0.11), "PixelPink", bevel=0, rot=(th, 0, 0))
    # control panel
    ph = math.atan(0.5 / 1.0); pc = (0, -1.05, 3.5)
    pv = (0, math.cos(ph), math.sin(ph)); pn = (0, -math.sin(ph), math.cos(ph))
    box((2.95, 1.15, 0.35), pc, "Panel", bevel=0.1, rot=(ph, 0, 0))
    def on_panel(a, b, d):
        return (a, pc[1] + pv[1] * b + pn[1] * d, pc[2] + pv[2] * b + pn[2] * d)
    cyl(0.2, 0.1, on_panel(-0.75, 0, 0.2), "Ink", verts=14, bevel=0.03, rot=(ph, 0, 0))
    jx, jy, jz = on_panel(-0.75, 0, 0.2)
    cyl(0.06, 0.5, (jx, jy, jz + 0.25), "Stick", verts=8, bevel=0)
    ball(0.17, (jx, jy, jz + 0.55), "StickBall", seg=14, ring=9)
    for k, col in enumerate(("Button1", "Button2", "Button3")):
        p = on_panel(0.15 + k * 0.42, 0.1 - k * 0.05, 0.22)
        cyl(0.15, 0.12, p, col, verts=16, bevel=0.04, rot=(ph, 0, 0))
    # coin door + kick plate
    box((1.3, 0.14, 1.35), (0, -1.07, 1.5), "Panel", bevel=0.07)
    for x in (-0.25, 0.25): box((0.12, 0.06, 0.36), (x, -1.15, 1.78), "CoinGlow", bevel=0.02)
    box((0.6, 0.06, 0.18), (0, -1.15, 1.1), "Ink", bevel=0.02)
    box((3.0, 0.16, 0.45), (0, -1.08, 0.42), "Panel", bevel=0.08)

PROPS = [LeverConsole, LeverHandle, LeverBall, Stall, MarketProps, GemProps, ArcadeMachine]
# Props that share an origin with another (props on the stall) go to the same grid cell.
CELL = {"LeverConsole": (0, 0), "LeverHandle": (8, 0), "LeverBall": (12, 0), "Stall": (0, 30), "MarketProps": (0, 30),
        "GemProps": (30, 30), "ArcadeMachine": (30, 0)}

def build_all(only=None):
    clear(); info = {}
    for fn in PROPS:
        if only and fn.__name__ not in only: continue
        fn(); objs = finish_prop(fn.__name__)
        ox, oy = CELL[fn.__name__]
        for o in objs: o.location = (ox, oy, 0)
        info[fn.__name__] = {"cell": [ox, oy], "meshes": [o.name for o in objs]}
    # a second stall under the Gem props so the scene previews both stands
    json.dump({"colors": COLORS, "props": info, "hinge_z": HINGE_Z}, open(os.path.join(OUT, "props_colors.json"), "w"), indent=1)
    return info

def export_fbx(path=None):
    path = path or r"C:\obsidian\Roblox studio\Assets\Stations and Weapons\PropsRestyle.fbx"
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, apply_unit_scale=True, bake_space_transform=False,
                             object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
    return path
