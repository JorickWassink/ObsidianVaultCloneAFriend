# Clone a Friend decorations (v2, detailed): builds every decoration prop in Blender (1 BU = 1 stud, Z up, base at z=0).
# Run inside Blender:  ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Decorations\build_decor.py").read(), ns); ns["build_all"]()
# Each prop's pieces are joined per colour into one mesh "<Prop>__<colour key>" (fewer MeshParts in Roblox).
# Colour keys map to COLORS; a trailing "n" in the hex means Neon in Roblox, "g" means Glass.
import bpy, bmesh, math, random, json, os
from mathutils import Vector, noise

OUT = r"C:\obsidian\Roblox studio\Assets\Decorations"
COLORS = {
    # foliage
    "Leaf": "5cc23a", "LeafDark": "3e9e2b", "LeafLight": "8bd94a", "LeafTop": "a8e85c",
    "Pine": "2f8a4a", "PineDark": "23703b", "PineLight": "47a85c",
    "BirchLeaf": "b3dd52", "BirchLeafDark": "8cc23e", "Bark": "8a5a34", "BarkDark": "6b4325", "BarkLight": "a8744a",
    "Birch": "f2efe6", "BirchMark": "3a3a3a", "Apple": "e5383b", "AppleLeaf": "4caf50",
    # ground bits
    "Grass": "5cd02e", "GrassDark": "45b022", "Rock": "9aa3ad", "RockDark": "7b8590", "RockLight": "b9c0c8", "Moss": "6cbf3a",
    "Pink": "ff6fa8", "PinkDark": "e04e8a", "Yellow": "ffd23f", "White": "ffffff", "Purple": "a77bff", "Blue": "5aa9ff",
    "MushRed": "e0453a", "MushGill": "f7d9b8", "Stem": "f3e6cf", "WoodCut": "e8c08a", "WoodRing": "c9955a",
    # built things
    "Wood": "a0683a", "WoodLight": "b97c48", "WoodDark": "6e4426", "Metal": "2b3247", "MetalLight": "4a5470",
    "Glow": "ffe9a0n", "Water": "4fc3f7", "WaterLight": "a6e4ff", "Stone": "c7ccd4", "StoneDark": "a4abb6", "StoneLight": "dde1e7",
    "Roof": "d64545", "RoofDark": "b33636", "Rope": "d9c08a", "Tent": "ff8c42", "TentDark": "e0702a", "TentLight": "fff1d6",
    "Interior": "5a3a2a", "Hay": "e8c35a", "HayDark": "c9a23f", "HayLight": "f5d97a", "Blanket": "e63946",
    "Fire": "ff8a00n", "FireTip": "ffd23fn", "Ember": "ff4d1an", "Ash": "4a4a4a", "MailRed": "d63a3a", "MailDark": "a82a2a",
    "Sign": "d9a066", "SignDark": "b8844e", "Bread": "e8b46a", "Cheese": "ffd54f", "Plate": "f5f5f5", "Juice": "ff9f1c",
    # cliffs
    "Cliff": "c9824a", "CliffDark": "a8652f", "CliffLight": "dd9a5e",
}

def clear():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)

def mat(key):
    m = bpy.data.materials.get(key)
    if m: return m
    m = bpy.data.materials.new(key); m.use_nodes = True
    h = COLORS[key].rstrip("ng"); rgb = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*lin, 1); bsdf.inputs["Roughness"].default_value = 0.55
    if COLORS[key].endswith("n"):
        bsdf.inputs["Emission Color"].default_value = (*lin, 1); bsdf.inputs["Emission Strength"].default_value = 3
    m.diffuse_color = (*lin, 1)
    return m

PARTS = []
R = random.Random()

def _fin(o, col, bevel=0.0, seg=3, smooth=True, rot=(0, 0, 0), ang=40):
    o.rotation_euler = rot
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if bevel > 0:
        b = o.modifiers.new("b", "BEVEL"); b.width = bevel; b.segments = seg; b.limit_method = "ANGLE"
        bpy.ops.object.modifier_apply(modifier=b.name)
    if smooth: bpy.ops.object.shade_auto_smooth(angle=math.radians(ang))
    else:
        for p in o.data.polygons: p.use_smooth = False
    o.data.materials.clear(); o.data.materials.append(mat(col)); o["col"] = col
    PARTS.append(o); return o

def box(size, loc, col, bevel=0.15, rot=(0, 0, 0), seg=3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = size
    return _fin(o, col, bevel, rot=rot, seg=seg)

def cyl(r, h, loc, col, verts=16, bevel=0.1, r2=None, rot=(0, 0, 0)):
    if r2 is None: bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc)
    else: bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=h, location=loc)
    return _fin(bpy.context.object, col, bevel, rot=rot)

def cone(r, h, loc, col, verts=12, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=0, depth=h, location=loc)
    return _fin(bpy.context.object, col, bevel, rot=rot)

def ball(r, loc, col, scale=(1, 1, 1), seg=14, ring=9, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=r, location=loc)
    o = bpy.context.object; o.scale = scale; return _fin(o, col, 0, rot=rot)

def blob(r, loc, col, scale=(1, 1, 1), lumps=0.18, seed=0, sub=2, flat_bottom=None):
    """soft lumpy sphere for leaf clumps / bushes"""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=18 if sub >= 2 else 12, ring_count=12 if sub >= 2 else 8, radius=r, location=(0, 0, 0))
    o = bpy.context.object; off = Vector((seed * 3.1, seed * 1.7, seed * 2.3)); lumps *= 0.6
    for v in o.data.vertices:
        n = noise.noise(v.co * (1.6 / r) + off)
        v.co *= 1 + lumps * n
        if flat_bottom is not None and v.co.z < -r * flat_bottom: v.co.z = -r * flat_bottom + (v.co.z + r * flat_bottom) * 0.25
    o.scale = scale; o.location = loc; return _fin(o, col, 0, ang=180)

def rock(r, loc, col, scale=(1, 1, 1), seed=0, sub=2, jag=0.22):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=r, location=(0, 0, 0))
    o = bpy.context.object; off = Vector((seed * 5.3, seed * 2.9, seed * 1.1))
    for v in o.data.vertices:
        v.co *= 1 + jag * noise.noise(v.co * (1.2 / r) + off)
        if v.co.z < -r * 0.35: v.co.z = -r * 0.35
    o.scale = scale; o.location = loc; return _fin(o, col, 0, ang=35)

def torus(Rm, r, loc, col, rot=(0, 0, 0), seg=20, mseg=8):
    bpy.ops.mesh.primitive_torus_add(major_radius=Rm, minor_radius=r, major_segments=seg, minor_segments=mseg, location=loc)
    return _fin(bpy.context.object, col, 0, rot=rot)

def prism(pts, depth, loc, col, rot=(0, 0, 0), bevel=0.06):
    """extrude a 2D outline (x,z points) along y"""
    bm = bmesh.new(); vs = [bm.verts.new((x, -depth / 2, z)) for x, z in pts]
    f = bm.faces.new(vs); r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.y += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("p"); bm.to_mesh(me); o = bpy.data.objects.new("p", me); bpy.context.collection.objects.link(o)
    o.location = loc; return _fin(o, col, bevel, rot=rot, smooth=False)

def tube(points, r, col, verts=8):
    """a bent cylinder through points (used for branches, roots, ropes)"""
    for a, b in zip(points[:-1], points[1:]):
        a, b = Vector(a), Vector(b); d = b - a
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(a + b) / 2)
        o = bpy.context.object; o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True); o.rotation_mode = "XYZ"
        _fin(o, col, 0); ball(r * 1.02, tuple(b), col, seg=verts, ring=5)

def finish_prop(name):
    groups = {}
    for o in PARTS: groups.setdefault(o["col"], []).append(o)
    made = []
    for col, objs in groups.items():
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs: o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        if len(objs) > 1: bpy.ops.object.join()
        j = bpy.context.object; j.name = j.data.name = f"{name}__{col}"; j["prop"] = name
        bpy.context.scene.cursor.location = (0, 0, 0); bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        made.append(j)
    PARTS.clear(); return made

# ---------------- shared bits ----------------
def trunk(h, r, col="Bark", dark="BarkDark", roots=4, seed=0):
    cyl(r * 1.25, h, (0, 0, h / 2), col, verts=14, r2=r * 0.8, bevel=0.1)
    for k in range(roots):  # root flares
        a = k * 2 * math.pi / roots + seed
        tube([(r * 0.6 * math.cos(a), r * 0.6 * math.sin(a), 1.0), (r * 1.7 * math.cos(a), r * 1.7 * math.sin(a), 0.15)], r * 0.38, col, 8)
    for k in range(5):  # bark ridges
        a = k * 1.27 + seed; z = 1.2 + k * (h - 2) / 5
        if z < h - 2.5: tube([(r * 1.12 * math.cos(a), r * 1.12 * math.sin(a), z - 0.6), (r * 1.08 * math.cos(a + 0.1), r * 1.08 * math.sin(a + 0.1), z + 0.7)], 0.09, dark, 6)

def leaf_crown(center, rad, cols, n=9, seed=0, squash=0.82):
    R.seed(seed); cx, cy, cz = center
    blob(rad, (cx, cy, cz), cols[0], (1, 1, squash), seed=seed, flat_bottom=0.5)
    for i in range(n):
        a = i * 2.399 + seed; t = (i % 3) / 2
        rr = rad * (0.55 + 0.25 * R.random()); r = rad * (0.42 + 0.16 * R.random())
        z = cz + rad * (-0.25 + 0.55 * t)
        blob(r, (cx + rr * math.cos(a), cy + rr * math.sin(a), z), cols[(i % (len(cols) - 1)) + 1], (1, 1, squash), seed=seed + i + 1)
    blob(rad * 0.5, (cx + rad * 0.1, cy - rad * 0.1, cz + rad * 0.62), cols[-1], (1, 1, squash), seed=seed + 50)

def flower(x, y, col, h=1.4, dark=None):
    tube([(x, y, 0.2), (x + 0.08, y, h * 0.5), (x, y, h)], 0.07, "LeafDark", 6)
    for s in (-1, 1):  # stem leaves
        ball(0.24, (x + s * 0.22, y, h * 0.45), "Leaf", (1.6, 0.6, 0.35), seg=8, ring=5, rot=(0, s * 0.5, 0))
    for k in range(6):
        a = k * math.pi / 3
        ball(0.2, (x + 0.24 * math.cos(a), y + 0.24 * math.sin(a), h), col, (1.6, 0.9, 0.38), seg=8, ring=5, rot=(0, 0, a))
    ball(0.15, (x, y, h + 0.07), "Yellow" if col != "Yellow" else "WoodLight", (1, 1, .7), seg=8, ring=5)

def grass_blades(cx, cy, n, h, seed=0, cols=("Grass", "Leaf", "GrassDark")):
    R.seed(seed)
    for k in range(n):
        a = k * 2.39 + seed; r = 0.15 + 0.35 * R.random(); hh = h * (0.7 + 0.5 * R.random())
        x, y = cx + r * math.cos(a), cy + r * math.sin(a); lean = 0.3 * hh
        tube([(x, y, 0), (x + lean * 0.3 * math.cos(a), y + lean * 0.3 * math.sin(a), hh * 0.55),
              (x + lean * math.cos(a), y + lean * math.sin(a), hh)], 0.09, cols[k % len(cols)], 5)

# ---------------- trees ----------------
def TreeRound():
    trunk(8.5, 0.95, seed=0.3)
    tube([(0, 0, 6.5), (1.6, 0.3, 8.6), (2.8, 0.6, 9.6)], 0.32, "Bark", 8)
    tube([(0, 0, 7.2), (-1.5, -0.6, 9.0), (-2.6, -1.0, 9.8)], 0.3, "Bark", 8)
    leaf_crown((0, 0, 11.0), 4.6, ["Leaf", "LeafDark", "Leaf", "LeafDark", "LeafTop"], n=10, seed=3)

def TreePine():
    trunk(4.5, 0.75, seed=1.1, roots=3)
    tiers = [(6.2, 3.6), (5.2, 6.6), (4.2, 9.4), (3.1, 12.0), (2.0, 14.3)]
    for i, (r, z) in enumerate(tiers):
        col = ["Pine", "PineDark"][i % 2]
        bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=r, radius2=r * 0.22, depth=4.0, location=(0, 0, z + 2.0))
        o = bpy.context.object
        for v in o.data.vertices:  # wavy, drooping bottom edge
            if v.co.z < -1.9:
                a = math.atan2(v.co.y, v.co.x); v.co.z += -0.45 * math.cos(a * 10) - 0.3
        _fin(o, col, bevel=0.3, seg=2, ang=50)
        torus(r * 0.97, 0.18, (0, 0, z + 0.05), "PineLight", seg=20, mseg=5)
    cone(1.0, 2.2, (0, 0, 17.0), "Pine", verts=12, bevel=0.1)
    star = [(math.cos(a) * (0.75 if i % 2 == 0 else 0.32), math.sin(a) * (0.75 if i % 2 == 0 else 0.32)) for i, a in enumerate([math.pi / 2 + k * math.pi / 5 for k in range(10)])]
    prism(star, 0.25, (0, 0, 18.6), "Yellow", bevel=0.05)

def TreeBirch():
    cyl(0.78, 12, (0, 0, 6), "Birch", verts=14, r2=0.52, bevel=0.08)
    for k in range(3):
        a = k * 2.1; tube([(0.4 * math.cos(a), 0.4 * math.sin(a), 0.9), (1.1 * math.cos(a), 1.1 * math.sin(a), 0.1)], 0.28, "Birch", 8)
    R.seed(7)
    for i in range(12):  # dark birch lenticels
        a = R.random() * 6.28; z = 1.0 + i * 0.85; rr = 0.78 - z * 0.022
        box((0.55 + R.random() * 0.4, 0.12, 0.16), (rr * math.cos(a), rr * math.sin(a), z), "BirchMark", bevel=0.04, rot=(0, 0, a + math.pi / 2))
    tube([(0, 0, 8.0), (1.4, 0.4, 9.8), (2.2, 0.6, 11.0)], 0.22, "Birch", 8)
    tube([(0, 0, 9.0), (-1.3, -0.3, 10.6), (-2.0, -0.6, 11.8)], 0.2, "Birch", 8)
    for (x, y, z, r) in [(0, 0, 14.2, 3.4), (2.7, 0.8, 12.0, 2.7), (-2.5, -0.8, 12.6, 2.6), (0.5, -2.0, 11.4, 2.3), (-0.4, 2.0, 12.0, 2.3)]:
        leaf_crown((x, y, z), r, ["BirchLeaf", "BirchLeafDark", "BirchLeaf", "LeafTop"], n=4, seed=int(z * 10 + x), squash=1.15)

def TreeFruit():
    trunk(6.2, 0.9, seed=2.0)
    tube([(0, 0, 5.0), (1.8, 0.5, 6.6)], 0.3, "Bark", 8); tube([(0, 0, 5.4), (-1.7, -0.4, 7.0)], 0.28, "Bark", 8)
    leaf_crown((0, 0, 8.8), 4.4, ["Leaf", "LeafDark", "Leaf", "LeafTop"], n=9, seed=11, squash=0.88)
    R.seed(5)
    for i in range(14):
        a = i * 2.39; z = 7.0 + (i % 4) * 1.1; rr = 4.3 - (i % 4) * 0.55
        x, y = rr * math.cos(a), rr * math.sin(a)
        ball(0.5, (x, y, z), "Apple", (1, 1, 0.92), seg=12, ring=8)
        cyl(0.05, 0.3, (x, y, z + 0.55), "BarkDark", verts=5, bevel=0)
        ball(0.18, (x + 0.15, y, z + 0.6), "AppleLeaf", (1.6, 0.6, 0.3), seg=6, ring=4)
    for (x, y) in [(2.6, -1.8), (-2.0, 2.4)]:  # fallen apples
        ball(0.5, (x, y, 0.45), "Apple", seg=12, ring=8)

# ---------------- nature ----------------
def Bush():
    leaf_crown((0, 0, 1.6), 1.9, ["Leaf", "LeafDark", "Leaf", "LeafTop"], n=7, seed=21, squash=0.75)
    blob(1.5, (2.1, 0.4, 1.1), "LeafDark", (1, 1, .7), seed=22); blob(1.3, (-2.0, -0.3, 1.0), "Leaf", (1, 1, .7), seed=23)

def BushFlower():
    leaf_crown((0, 0, 1.6), 2.0, ["LeafDark", "Leaf", "LeafDark", "Leaf"], n=7, seed=31, squash=0.75)
    blob(1.4, (2.0, -0.3, 1.0), "Leaf", (1, 1, .7), seed=32)
    R.seed(4)
    for i in range(16):
        a = i * 2.39; z = 1.0 + R.random() * 1.6; rr = 2.0 - (z - 1.0) * 0.35
        col = "Pink" if i % 3 else "White"; x, y = rr * math.cos(a), rr * math.sin(a)
        for k in range(5):
            b = k * 2 * math.pi / 5
            ball(0.13, (x + 0.15 * math.cos(b), y + 0.15 * math.sin(b), z), col, (1.4, 0.9, 0.5), seg=6, ring=4, rot=(0, 0, b))
        ball(0.08, (x, y, z + 0.04), "Yellow", seg=6, ring=4)

def FlowerPatch():
    blob(2.6, (0, 0, -0.9), "Grass", (1, 1, 0.45), seed=41, lumps=0.1)
    for i, (x, y, c) in enumerate([(0, 0, "Pink"), (1.3, 0.6, "Yellow"), (-1.2, 0.8, "Purple"), (0.6, -1.3, "White"),
                                   (-0.9, -1.0, "Pink"), (1.6, -0.7, "Purple"), (-1.7, -0.1, "Blue")]):
        flower(x, y, c, 1.3 + (i % 3) * 0.35)
    grass_blades(0.3, 1.5, 6, 0.9, seed=1); grass_blades(-0.4, -1.8, 6, 0.9, seed=2)

def FlowerPatch2():
    blob(2.2, (0, 0, -0.8), "Grass", (1, 1, 0.45), seed=42, lumps=0.1)
    for i, (x, y) in enumerate([(0, 0), (1.1, 0.5), (-1.0, 0.7), (0.4, -1.1), (-0.8, -0.8), (1.3, -0.7)]):
        flower(x, y, "Yellow" if i % 2 == 0 else "White", 1.2 + (i % 2) * 0.45)
    grass_blades(-1.3, 0.2, 7, 1.0, seed=3)

def RockBig():
    rock(2.7, (0, 0, 1.4), "Rock", (1.35, 1, .8), seed=1)
    rock(1.5, (2.6, 1.1, 0.7), "RockDark", (1, 1, .85), seed=2)
    rock(0.9, (-2.9, -1.0, 0.4), "RockLight", seed=3)
    blob(1.3, (-0.6, 0.3, 3.2), "Moss", (1.6, 1.2, 0.35), seed=4, lumps=0.25)
    grass_blades(1.6, -1.9, 7, 1.1, seed=5)

def RockSmall():
    rock(1.4, (0, 0, 0.75), "Rock", (1.2, 1, .8), seed=6); rock(0.8, (1.4, -0.6, 0.4), "RockDark", seed=7)
    rock(0.45, (-1.3, 0.9, 0.25), "RockLight", seed=8); blob(0.7, (0.1, 0.2, 1.65), "Moss", (1.5, 1.1, 0.35), seed=9)
    grass_blades(-1.1, -1.0, 5, 0.8, seed=6)

def Mushrooms():
    blob(1.8, (0, 0, -0.6), "Grass", (1.2, 1, 0.4), seed=51, lumps=0.1)
    for i, (x, y, s) in enumerate([(0, 0, 1.0), (1.2, 0.6, 0.65), (-1.0, 0.7, 0.55), (0.6, -1.0, 0.45)]):
        tube([(x, y, 0), (x + 0.1 * s, y, 0.9 * s), (x, y, 1.6 * s)], 0.3 * s, "Stem", 10)
        torus(0.34 * s, 0.07 * s, (x, y, 1.05 * s), "Stem")
        ball(1.05 * s, (x, y, 1.55 * s), "MushGill", (1, 1, .25), seg=16, ring=8)
        ball(1.05 * s, (x, y, 1.62 * s), "MushRed" if i != 3 else "Purple", (1, 1, .62), seg=16, ring=10)
        R.seed(i)
        for k in range(6):
            a = k * 1.05 + R.random() * 0.4; rr = (0.35 + 0.35 * (k % 2)) * s
            z = 1.62 * s + 0.62 * s * math.sqrt(max(0, 1 - (rr / (1.05 * s)) ** 2)) - 0.02
            ball((0.13 + 0.05 * (k % 2)) * s, (x + rr * math.cos(a), y + rr * math.sin(a), z), "White", (1, 1, .45), seg=8, ring=5)

def Stump():
    cyl(1.45, 1.8, (0, 0, 0.9), "Bark", verts=16, bevel=0.12, r2=1.25)
    for k in range(10):  # bark ridges
        a = k * 2 * math.pi / 10; box((0.22, 0.45, 1.5), (1.37 * math.cos(a), 1.37 * math.sin(a), 0.85), "BarkDark", bevel=0.08, rot=(0, 0, a))
    cyl(1.18, 0.1, (0, 0, 1.82), "WoodCut", verts=16, bevel=0.03)
    for rr in (0.85, 0.55, 0.25): torus(rr, 0.035, (0, 0, 1.87), "WoodRing", seg=16, mseg=4)
    for k in range(4):
        a = k * 1.6 + 0.3
        tube([(1.0 * math.cos(a), 1.0 * math.sin(a), 0.7), (1.9 * math.cos(a), 1.9 * math.sin(a), 0.15), (2.3 * math.cos(a), 2.3 * math.sin(a), 0.05)], 0.3, "Bark", 8)
    # little mushrooms on the side
    for (a, z, s) in [(2.2, 0.7, 0.35), (2.6, 0.45, 0.25)]:
        x, y = 1.45 * math.cos(a), 1.45 * math.sin(a)
        ball(s, (x, y, z), "MushRed", (1.2, 1.2, 0.5), seg=10, ring=6); ball(s * 0.25, (x * 1.05, y * 1.05, z + s * 0.35), "White", seg=6, ring=4)
    box((0.15, 1.6, 0.35), (0.3, 0.2, 2.35), "WoodDark", bevel=0.05, rot=(0.4, 0, 0.5))  # axe handle
    prism([(0, 0), (0.7, 0.15), (0.75, -0.55), (0, -0.35)], 0.12, (0.0, -0.4, 2.0), "MetalLight", rot=(0, 0, 0.5))

def GrassTuft():
    grass_blades(0, 0, 14, 1.6, seed=9)
    flower(0.5, 0.3, "White", 1.8)

# ---------------- park props ----------------
def Bench():
    for x in (-2.5, 2.5):  # cast iron sides with scroll arm
        box((0.28, 1.7, 0.28), (x, 0, 1.45), "Metal", bevel=0.08)
        for y in (-0.7, 0.6): box((0.28, 0.28, 1.45), (x, y, 0.72), "Metal", bevel=0.08)
        tube([(x, 0.75, 1.5), (x, 0.95, 2.4), (x, 1.05, 3.1)], 0.13, "Metal", 8)
        tube([(x, 0.8, 2.3), (x, -0.4, 2.3), (x, -0.75, 2.05), (x, -0.7, 1.6)], 0.12, "Metal", 8)
        torus(0.22, 0.06, (x, -0.72, 1.85), "MetalLight", rot=(0, math.pi / 2, 0), seg=12, mseg=5)
        box((0.5, 0.5, 0.12), (x, -0.7, 0.06), "Metal", bevel=0.04); box((0.5, 0.5, 0.12), (x, 0.6, 0.06), "Metal", bevel=0.04)
    for i in range(4):
        box((6.0, 0.36, 0.16), (0, -0.62 + i * 0.4, 1.66), "Wood" if i % 2 else "WoodLight", bevel=0.07)
    for i in range(3):
        box((6.0, 0.14, 0.34), (0, 0.98 + i * 0.05, 2.1 + i * 0.45), "Wood" if i % 2 else "WoodLight", bevel=0.06, rot=(-0.12, 0, 0))
    for x in (-2.5, 2.5):
        for i in range(4): ball(0.05, (x - 0.16 * (1 if x > 0 else -1) * -1, -0.62 + i * 0.4, 1.75), "MetalLight", seg=6, ring=4)

def LampPost():
    cyl(0.95, 0.35, (0, 0, 0.18), "Metal", verts=16, bevel=0.08); cyl(0.7, 0.35, (0, 0, 0.52), "Metal", verts=16, bevel=0.08)
    cyl(0.42, 1.6, (0, 0, 1.5), "Metal", verts=12, r2=0.26, bevel=0.06)
    for z in (0.75, 2.35, 6.0): torus(0.3, 0.07, (0, 0, z), "MetalLight", seg=12, mseg=5)
    cyl(0.2, 7.0, (0, 0, 5.8), "Metal", verts=10, bevel=0.03)
    for k in range(4):  # fluting
        a = k * math.pi / 2; box((0.06, 0.06, 5.0), (0.2 * math.cos(a), 0.2 * math.sin(a), 5.0), "MetalLight", bevel=0.02)
    tube([(0, 0, 8.4), (0.5, 0, 8.8), (0.6, 0, 9.4)], 0.07, "Metal", 6); tube([(0, 0, 8.4), (-0.5, 0, 8.8), (-0.6, 0, 9.4)], 0.07, "Metal", 6)
    cyl(0.55, 0.25, (0, 0, 9.4), "Metal", verts=8, bevel=0.06)
    box((0.85, 0.85, 1.3), (0, 0, 10.2), "Glow", bevel=0.1)
    for (x, y) in [(-0.47, -0.47), (0.47, -0.47), (0.47, 0.47), (-0.47, 0.47)]: box((0.12, 0.12, 1.4), (x, y, 10.2), "Metal", bevel=0.03)
    cyl(0.75, 0.2, (0, 0, 10.95), "Metal", verts=4, bevel=0.05, rot=(0, 0, math.pi / 4))
    cone(0.95, 0.75, (0, 0, 11.4), "Metal", verts=4, rot=(0, 0, math.pi / 4), bevel=0.04)
    cyl(0.1, 0.3, (0, 0, 11.85), "Metal", verts=8, bevel=0); ball(0.17, (0, 0, 12.05), "MetalLight", seg=10, ring=6)

def Fence():
    for x in (-3.8, 3.8):
        box((0.5, 0.5, 3.1), (x, 0, 1.55), "WoodDark", bevel=0.1)
        cone(0.42, 0.4, (x, 0, 3.3), "WoodDark", verts=4, rot=(0, 0, math.pi / 4), bevel=0.04)
    for z in (0.85, 2.15): box((8.0, 0.22, 0.4), (0, 0.12, z), "Wood", bevel=0.07)
    tube([(-3.6, 0.2, 0.9), (3.6, 0.2, 2.1)], 0.1, "WoodDark", 6)  # diagonal brace
    R.seed(12)
    for i in range(6):
        x = -2.9 + i * 1.16; h = 2.45 + R.uniform(-0.1, 0.1)
        col = "WoodLight" if i % 2 else "Wood"
        prism([(-0.3, 0), (0.3, 0), (0.3, h), (0, h + 0.4), (-0.3, h)], 0.16, (x, -0.06, 0), col, bevel=0.05)
        for z in (0.85, 2.15): ball(0.05, (x, -0.16, z), "Metal", seg=6, ring=4)
    grass_blades(-3.8, -0.4, 5, 0.9, seed=13); grass_blades(3.8, -0.4, 5, 0.9, seed=14)

def Fountain():
    cyl(6.0, 0.4, (0, 0, 0.2), "StoneDark", verts=28, bevel=0.1)
    n = 14
    for k in range(n):  # rim made of stone blocks
        a = k * 2 * math.pi / n
        box((2.6, 1.0, 1.4), (5.4 * math.cos(a), 5.4 * math.sin(a), 1.0), "Stone" if k % 2 else "StoneLight", bevel=0.18, rot=(0, 0, a + math.pi / 2))
    cyl(5.0, 0.9, (0, 0, 0.6), "StoneDark", verts=28, bevel=0.05)
    cyl(4.95, 0.12, (0, 0, 1.3), "Water", verts=28, bevel=0)
    for rr in (1.8, 3.0, 4.1): torus(rr, 0.05, (0, 0, 1.38), "WaterLight", seg=24, mseg=4)
    cyl(1.1, 0.6, (0, 0, 1.5), "Stone", verts=16, bevel=0.1)
    cyl(0.8, 2.6, (0, 0, 3.0), "StoneLight", verts=14, bevel=0.1, r2=0.55)
    for z in (1.9, 4.2): torus(0.75, 0.12, (0, 0, z), "Stone", seg=14, mseg=6)
    cyl(1.0, 0.6, (0, 0, 4.4), "Stone", verts=20, bevel=0.15, r2=2.8)
    torus(2.75, 0.22, (0, 0, 4.75), "StoneLight", seg=24, mseg=6)
    cyl(2.55, 0.12, (0, 0, 4.7), "Water", verts=24, bevel=0)
    cyl(0.4, 1.4, (0, 0, 5.5), "StoneLight", verts=10, bevel=0.08)
    cyl(0.4, 0.5, (0, 0, 6.4), "Stone", verts=12, bevel=0.1, r2=1.1)
    ball(0.5, (0, 0, 7.0), "WaterLight", (1, 1, 1.3), seg=12, ring=8); cone(0.3, 0.9, (0, 0, 7.8), "WaterLight", verts=8)
    for k in range(8):  # falling streams from the top bowl
        a = k * math.pi / 4
        tube([(2.8 * math.cos(a), 2.8 * math.sin(a), 4.8), (3.2 * math.cos(a), 3.2 * math.sin(a), 4.2), (3.5 * math.cos(a), 3.5 * math.sin(a), 1.4)], 0.12, "WaterLight", 6)

def Well():
    for row in range(4):  # stone courses
        n = 12; off = (row % 2) * math.pi / n
        for k in range(n):
            a = k * 2 * math.pi / n + off
            box((1.35, 0.8, 0.62), (2.4 * math.cos(a), 2.4 * math.sin(a), 0.33 + row * 0.64), ["Stone", "StoneLight", "StoneDark"][(k + row) % 3], bevel=0.14, seg=2, rot=(0, 0, a + math.pi / 2))
    cyl(2.1, 2.4, (0, 0, 1.2), "StoneDark", verts=18, bevel=0)
    cyl(2.0, 0.1, (0, 0, 2.0), "Water", verts=18, bevel=0)
    torus(2.45, 0.32, (0, 0, 2.7), "StoneLight", seg=20, mseg=6)
    for x in (-2.4, 2.4):
        box((0.45, 0.45, 4.8), (x, 0, 4.9), "WoodDark", bevel=0.08)
        box((0.35, 0.7, 0.35), (x, 0, 7.15), "WoodDark", bevel=0.06)
    cyl(0.18, 5.2, (0, 0, 5.6), "Wood", verts=10, bevel=0.03, rot=(0, math.pi / 2, 0))  # winch
    tube([(2.75, 0, 5.6), (3.05, 0, 5.6), (3.05, 0, 5.0), (3.3, 0, 5.0)], 0.07, "Metal", 6)  # crank
    cyl(0.12, 0.5, (3.45, 0, 5.0), "WoodLight", verts=8, bevel=0.02, rot=(0, math.pi / 2, 0))
    torus(0.24, 0.08, (0.4, 0, 5.6), "Rope", rot=(0, math.pi / 2, 0), seg=12, mseg=5)
    tube([(0.4, 0, 5.4), (0.4, 0, 4.25)], 0.04, "Rope", 6)
    cyl(0.5, 0.8, (0.4, 0, 3.8), "Wood", verts=12, bevel=0.06, r2=0.62)
    for z in (3.55, 4.05): torus(0.58, 0.04, (0.4, 0, z), "Metal", seg=14, mseg=4)
    torus(0.45, 0.04, (0.4, 0, 4.25), "Metal", rot=(math.pi / 2, 0, 0), seg=14, mseg=4)
    for s in (-1, 1):  # shingled roof
        for row in range(4):
            for k in range(6):
                y = s * (0.35 + row * 0.55); z = 7.95 - row * 0.4
                box((1.08, 0.75, 0.16), (-2.7 + k * 1.08 + (row % 2) * 0.3, y, z), "Roof" if (k + row) % 2 else "RoofDark", bevel=0.05, seg=1, rot=(s * math.radians(36), 0, 0))
    box((6.8, 0.3, 0.3), (0, 0, 8.25), "WoodDark", bevel=0.06)

def Signpost():
    blob(1.2, (0, 0, -0.4), "Grass", (1.2, 1, 0.45), seed=61, lumps=0.15)
    box((0.42, 0.42, 6.8), (0, 0, 3.4), "WoodDark", bevel=0.08)
    cone(0.36, 0.4, (0, 0, 7.0), "WoodDark", verts=4, rot=(0, 0, math.pi / 4))
    for z, d, col in ((5.8, 1, "Sign"), (4.6, -1, "SignDark"), (3.4, 1, "SignDark")):
        L = 3.6
        pts = [(0, -0.45), (L, -0.45), (L + 0.6, 0), (L, 0.45), (0, 0.45)] if d > 0 else [(0, -0.45), (-L, -0.45), (-L - 0.6, 0), (-L, 0.45), (0, 0.45)]
        prism([(x + d * 0.1, zz) for x, zz in pts], 0.22, (0, -0.32, z), col, bevel=0.06)
        for x in (d * 0.5, d * (L - 0.3)): ball(0.07, (x, -0.45, z), "Metal", seg=6, ring=4)
        box((L - 0.8, 0.04, 0.1), (d * (L / 2 + 0.1), -0.44, z + 0.15), "WoodDark", bevel=0.02)
        box((L - 1.4, 0.04, 0.1), (d * (L / 2), -0.44, z - 0.12), "WoodDark", bevel=0.02)
    grass_blades(0.6, -0.5, 6, 0.9, seed=62)

def Mailbox():
    blob(1.0, (0, 0, -0.35), "Grass", (1.1, 1, 0.45), seed=71, lumps=0.15)
    box((0.42, 0.42, 3.2), (0, 0, 1.6), "WoodDark", bevel=0.08)
    tube([(0, 0.2, 2.4), (0, 0.65, 3.05)], 0.1, "WoodDark", 6)
    box((1.6, 2.4, 0.18), (0, 0, 3.25), "WoodDark", bevel=0.05)
    box((1.3, 2.3, 0.65), (0, 0, 3.65), "MailRed", bevel=0.08)
    cyl(0.65, 2.3, (0, 0, 3.95), "MailRed", verts=20, bevel=0.06, rot=(math.pi / 2, 0, 0))
    for y in (-0.55, 0.0, 0.55): torus(0.66, 0.035, (0, y, 3.95), "MailDark", rot=(math.pi / 2, 0, 0), seg=20, mseg=4)
    box((1.25, 0.08, 1.2), (0, -1.17, 3.7), "MailDark", bevel=0.04)
    box((0.35, 0.1, 0.1), (0, -1.25, 3.95), "MetalLight", bevel=0.03)
    box((0.08, 0.12, 1.1), (0.72, 0.6, 4.25), "Metal", bevel=0.02)
    prism([(0, 0), (0.7, 0), (0.7, 0.4), (0, 0.4)], 0.06, (0.74, 0.55, 4.55), "Yellow", rot=(0, 0, math.pi / 2), bevel=0.02)
    ball(0.08, (0.74, 0.6, 3.85), "MetalLight", seg=6, ring=4)

# ---------------- camp ----------------
def Campfire():
    for k in range(10):
        a = k * 2 * math.pi / 10; rock(0.5, (1.7 * math.cos(a), 1.7 * math.sin(a), 0.3), ["RockDark", "Rock", "RockLight"][k % 3], (1.1, 1, .75), seed=10 + k)
    cyl(1.3, 0.1, (0, 0, 0.05), "Ash", verts=14, bevel=0)
    for k in range(4):
        a = k * math.pi / 4 + 0.2
        cyl(0.24, 2.8, (0, 0, 0.5), "Bark", verts=10, bevel=0.06, rot=(0, math.radians(72), a))
        for s in (-1, 1):
            d = Vector((math.cos(a) * math.sin(math.radians(72)), math.sin(a) * math.sin(math.radians(72)), math.cos(math.radians(72)))) * 1.4 * s
            cyl(0.2, 0.04, (d.x, d.y, 0.5 + d.z), "WoodCut", verts=10, bevel=0, rot=(0, math.radians(72), a))
    for (x, y, z, r, h, c) in [(0, 0, 1.2, 0.9, 2.4, "Fire"), (0.35, 0.2, 1.2, 0.55, 2.0, "FireTip"), (-0.35, -0.2, 1.0, 0.5, 1.6, "FireTip"),
                               (0.2, -0.45, 0.9, 0.4, 1.3, "Fire"), (-0.3, 0.45, 0.9, 0.38, 1.2, "Fire")]:
        ball(r, (x, y, z - h * 0.25), c, (1, 1, 0.9), seg=10, ring=6); cone(r, h, (x, y, z + h * 0.15), c, verts=10)
    for k in range(6):
        a = k * 1.1; ball(0.12, (0.9 * math.cos(a), 0.9 * math.sin(a), 0.2), "Ember", seg=6, ring=4)
    for k in range(2):  # log seats
        a = k * math.pi + 0.6; c = Vector((3.3 * math.cos(a), 3.3 * math.sin(a), 0.55))
        cyl(0.55, 2.4, tuple(c), "Bark", verts=14, bevel=0.08, rot=(0, math.pi / 2, a + math.pi / 2))
        for s in (-1, 1):
            e = c + Vector((-math.sin(a), math.cos(a), 0)) * 1.21 * s
            cyl(0.45, 0.04, tuple(e), "WoodCut", verts=14, bevel=0, rot=(0, math.pi / 2, a + math.pi / 2))
    tube([(2.3, -1.6, 0.9), (1.2, -0.9, 1.6), (0.3, -0.25, 2.3)], 0.04, "WoodDark", 5)  # marshmallow stick
    ball(0.18, (0.3, -0.25, 2.3), "Stem", (1, 1, 1.3), seg=8, ring=5)

def Tent():
    w, d, h = 5.2, 6.0, 4.4
    def tri_prism(w, d, h, y0, col, solid=True):
        bm = bmesh.new()
        vs = [bm.verts.new(p) for p in [(-w / 2, y0, 0), (w / 2, y0, 0), (0, y0, h), (-w / 2, y0 + d, 0), (w / 2, y0 + d, 0), (0, y0 + d, h)]]
        for f in [(0, 1, 2), (3, 5, 4), (0, 2, 5, 3), (1, 4, 5, 2), (0, 3, 4, 1)]: bm.faces.new([vs[i] for i in f])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        me = bpy.data.meshes.new("t"); bm.to_mesh(me); o = bpy.data.objects.new("t", me); bpy.context.collection.objects.link(o)
        return _fin(o, col, bevel=0.12, smooth=False)
    tri_prism(w, d, h, -d / 2, "Tent")
    tri_prism(w * 0.62, 0.1, h * 0.62, -d / 2 - 0.02, "Interior")  # dark opening
    for s in (-1, 1):  # rolled-open door flaps + stripes on the roof
        prism([(0, 0), (s * 1.6, 0), (0, h * 0.66)], 0.08, (0, -d / 2 - 0.12, 0), "TentDark", bevel=0.02)
        cyl(0.2, 2.2, (s * 0.85, -d / 2 - 0.25, 1.6), "TentLight", verts=10, bevel=0.03, rot=(0, s * -0.55, 0))
        for i in range(3):
            y = -d / 2 + 1.2 + i * 1.8
            box((0.12, 0.5, h * 1.15), (s * w / 4 + s * 0.03, y, h / 2), "TentLight", bevel=0.02, rot=(0, s * -math.atan2(w / 2, h), 0))
    box((0.3, d + 0.3, 0.3), (0, 0, h), "TentDark", bevel=0.08)
    for y in (-d / 2 - 0.2, d / 2 + 0.2): cyl(0.12, h + 0.9, (0, y, (h + 0.9) / 2), "WoodDark", verts=8, bevel=0)
    for (sx, sy) in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:  # guy ropes + stakes
        top = (0, sy * (d / 2 + 0.2), h + 0.6); stake = (sx * 1.6, sy * (d / 2 + 2.2), 0.3)
        tube([top, stake], 0.03, "Rope", 5); cyl(0.07, 0.7, (stake[0], stake[1], 0.2), "WoodDark", verts=6, bevel=0)
    box((2.6, 1.6, 0.25), (0, -d / 2 - 1.6, 0.12), "TentLight", bevel=0.1)  # mat at the door

def HayBale():
    box((3.4, 2.2, 2.0), (0, 0, 1.0), "Hay", bevel=0.4, seg=4)
    for x in (-0.95, 0.95): box((0.2, 2.32, 2.12), (x, 0, 1.0), "Rope", bevel=0.09)
    R.seed(3)
    for k in range(24):  # straw tufts poking out
        side = k % 4; u = R.uniform(-1.4, 1.4); v = R.uniform(0.3, 1.8)
        if side == 0: p, d = (u, -1.1, v), (0, -1, 0)
        elif side == 1: p, d = (u, 1.1, v), (0, 1, 0)
        elif side == 2: p, d = (u * 0.6, R.uniform(-0.9, 0.9), 2.0), (0, 0, 1)
        else: p, d = (1.7 * (1 if k % 8 == 3 else -1), u * 0.7, v), ((1 if k % 8 == 3 else -1), 0, 0)
        q = Vector(p) + Vector(d) * 0.35 + Vector((R.uniform(-.2, .2), R.uniform(-.2, .2), R.uniform(-.1, .2)))
        tube([p, tuple(q)], 0.035, "HayLight" if k % 2 else "HayDark", 4)
    box((1.2, 1.0, 0.04), (0.8, -0.4, 2.0), "HayLight", bevel=0.02)

def PicnicBlanket():
    box((5.0, 5.0, 0.12), (0, 0, 0.06), "White", bevel=0.04)
    for i in range(5):
        for j in range(5):
            if (i + j) % 2 == 0: box((0.98, 0.98, 0.04), (-2 + i, -2 + j, 0.13), "Blanket", bevel=0.01)
    prism([(0, 0), (1.2, 0), (0, 1.2)], 0.1, (1.9, 2.0, 0.17), "Blanket", rot=(math.pi / 2, 0, math.pi), bevel=0.02)  # folded corner
    # basket with weave bands, lid and handle
    box((1.7, 1.15, 0.95), (1.3, 1.0, 0.62), "Hay", bevel=0.14)
    for z in (0.35, 0.62, 0.89): box((1.75, 1.2, 0.08), (1.3, 1.0, z), "HayDark", bevel=0.03)
    box((1.8, 1.25, 0.14), (1.3, 1.0, 1.16), "HayDark", bevel=0.05)
    torus(0.6, 0.08, (1.3, 1.0, 1.25), "HayDark", rot=(math.pi / 2, 0, 0), seg=16, mseg=5)
    box((0.9, 0.08, 0.35), (1.3, 0.38, 0.95), "Blanket", bevel=0.03)  # cloth peeking out
    for (x, y) in [(-1.2, -0.6), (0.4, -1.4)]:  # plates with sandwiches
        cyl(0.6, 0.06, (x, y, 0.2), "Plate", verts=18, bevel=0.02)
        box((0.7, 0.7, 0.1), (x, y, 0.3), "Bread", bevel=0.04, rot=(0, 0, 0.7))
        box((0.68, 0.68, 0.06), (x, y, 0.37), "Cheese", bevel=0.02, rot=(0, 0, 0.75))
        box((0.7, 0.7, 0.1), (x, y, 0.45), "Bread", bevel=0.04, rot=(0, 0, 0.7))
    cyl(0.25, 0.9, (-0.2, 1.3, 0.6), "Juice", verts=12, bevel=0.05); cyl(0.12, 0.25, (-0.2, 1.3, 1.15), "Juice", verts=10, bevel=0.03)
    cyl(0.14, 0.12, (-0.2, 1.3, 1.32), "MailRed", verts=10, bevel=0.03)
    for (x, y) in [(-1.6, 1.0), (-1.1, 1.5), (-1.7, 1.6)]:
        ball(0.32, (x, y, 0.45), "Apple", seg=12, ring=8); cyl(0.04, 0.2, (x, y, 0.82), "BarkDark", verts=5, bevel=0)

# ---------------- cliffs ----------------
def column(cx, cy, r, h, col, seed, sides=7, taper=0.88):
    """an irregular, rounded rock column (cartoon basalt), base at z=-1 so it sinks into the ground"""
    R.seed(seed)
    bm = bmesh.new(); ring_lo, ring_hi = [], []
    for k in range(sides):
        a = k * 2 * math.pi / sides + R.uniform(-0.25, 0.25); rr = r * R.uniform(0.82, 1.08)
        ring_lo.append(bm.verts.new((cx + rr * math.cos(a), cy + rr * math.sin(a), -1)))
        ring_hi.append(bm.verts.new((cx + rr * taper * math.cos(a), cy + rr * taper * math.sin(a), h)))
    bm.faces.new(ring_hi); bm.faces.new(list(reversed(ring_lo)))
    for k in range(sides):
        bm.faces.new([ring_lo[k], ring_lo[(k + 1) % sides], ring_hi[(k + 1) % sides], ring_hi[k]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("c"); bm.to_mesh(me); o = bpy.data.objects.new("c", me); bpy.context.collection.objects.link(o)
    _fin(o, col, bevel=min(0.9, r * 0.22), seg=2, ang=35)
    return [(v.co.x, v.co.y) for v in ring_hi]

def grass_cap(pts, z, seed, drip=True):
    """soft grass slab following a column top, slightly overhanging, with a lumpy drip edge"""
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    big = [(cx + (x - cx) * 1.12, cy + (y - cy) * 1.12) for x, y in pts]
    bm = bmesh.new()
    lo = [bm.verts.new((x, y, z - 0.6)) for x, y in big]; hi = [bm.verts.new((x, y, z + 0.9)) for x, y in big]
    bm.faces.new(hi); bm.faces.new(list(reversed(lo)))
    n = len(big)
    for k in range(n): bm.faces.new([lo[k], lo[(k + 1) % n], hi[(k + 1) % n], hi[k]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("g"); bm.to_mesh(me); o = bpy.data.objects.new("g", me); bpy.context.collection.objects.link(o)
    _fin(o, "Grass", bevel=0.55, seg=2, ang=60)
    if drip:
        R.seed(seed)
        for k in range(n):
            if R.random() < 0.6:
                x0, y0 = big[k]; x1, y1 = big[(k + 1) % n]; t = R.uniform(0.3, 0.7)
                ball(R.uniform(0.45, 0.7), (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, z - 0.55), "GrassDark" if k % 2 else "Grass", (1.4, 1.4, 0.8), seg=8, ring=5)

def _cliff(h, seed):
    """24 x 24 wall piece. The play area is on -y. Columns of different heights stand along the front,
    a big rounded fill block sits behind them so neighbouring pieces close the ring."""
    R.seed(seed)
    tones = ["Cliff", "CliffDark", "CliffLight"]
    # back fill (sits behind the columns, slightly lower than the tallest)
    box((25, 16, h - 1.5), (0, 4, (h - 1.5) / 2 - 0.5), "CliffDark", bevel=1.4)
    box((25.6, 16.6, 1.6), (0, 4, h - 1.6), "Grass", bevel=0.7, seg=4)
    # front columns (two rows, staggered)
    xs = [-10.5, -6.0, -1.5, 3.0, 7.5, 11.0]
    for i, x in enumerate(xs):
        r = R.uniform(2.6, 3.4); hh = h + R.uniform(-3.5, 1.5)
        tops = column(x + R.uniform(-0.6, 0.6), -7.0 + R.uniform(-0.8, 0.8), r, hh, tones[i % 3], seed * 100 + i)
        grass_cap(tops, hh, seed * 100 + i)
    for i, x in enumerate([-8.3, -3.8, 0.8, 5.3, 9.6]):
        r = R.uniform(2.6, 3.2); hh = h + R.uniform(-1.0, 2.5)
        tops = column(x + R.uniform(-0.5, 0.5), -2.0 + R.uniform(-0.6, 0.6), r, hh, tones[(i + 1) % 3], seed * 100 + 50 + i)
        grass_cap(tops, hh, seed * 100 + 50 + i, drip=False)
    # low ledges and boulders at the foot
    for i in range(3):
        x = -8 + i * 8 + R.uniform(-1.5, 1.5); hh = R.uniform(2.5, 4.5)
        tops = column(x, -10.6, R.uniform(1.6, 2.2), hh, tones[(i + 2) % 3], seed * 100 + 80 + i, sides=6)
        grass_cap(tops, hh, seed * 100 + 80 + i)
    for i in range(4):
        rock(R.uniform(0.7, 1.2), (-10 + i * 6.5 + R.uniform(-1, 1), -12.6 + R.uniform(-0.4, 0.4), 0.3), ["Rock", "RockDark", "RockLight"][i % 3], (1.2, 1, 0.75), seed=seed * 7 + i)
    # life on top and at the foot
    for i in range(2):
        grass_blades(-6 + i * 11 + R.uniform(-1, 1), -12.2, 5, 1.0, seed=seed + 30 + i)
    for i in range(3):
        x = -7 + i * 7 + R.uniform(-1, 1)
        tube([(x, -10.4, h - 1.2), (x + 0.3, -10.9, h - 3.0), (x, -10.7, h - 5.0)], 0.12, "LeafDark", 6)
        ball(0.32, (x, -10.7, h - 5.0), "Leaf", seg=8, ring=5)
    bush_spots = [(-9, 3), (4, 6)]
    for (x, y) in bush_spots:
        blob(1.6, (x, y, h - 0.2), "Leaf", (1, 1, 0.75), seed=seed + x)
        blob(1.1, (x + 1.4, y + 0.5, h - 0.4), "LeafDark", (1, 1, 0.75), seed=seed + y)


def CliffA(): _cliff(12, 1)
def CliffB(): _cliff(15, 2)
def CliffC(): _cliff(18, 3)

PROPS = [TreeRound, TreePine, TreeBirch, TreeFruit, Bush, BushFlower, FlowerPatch, FlowerPatch2, RockBig, RockSmall,
         Mushrooms, Stump, GrassTuft, Bench, LampPost, Fence, Fountain, Well, Signpost, Mailbox, Campfire, Tent,
         HayBale, PicnicBlanket, CliffA, CliffB, CliffC]

def build_all(spacing=30, only=None):
    clear(); layout = {}
    for i, fn in enumerate(PROPS):
        if only and fn.__name__ not in only: continue
        fn(); objs = finish_prop(fn.__name__)
        ox, oy = (i % 7) * spacing, (i // 7) * spacing
        for o in objs: o.location = (ox, oy, 0)
        layout[fn.__name__] = [ox, oy]
    json.dump({"colors": COLORS, "layout": layout}, open(os.path.join(OUT, "decor_colors.json"), "w"), indent=1)
    return layout
