# Clone a Friend: Boss 1 "Brown Bear" + Pet 1, faceted endgame restyle (vault: Design/Clone a Friend Boss Restyle).
# v2: clean low-poly lofts (8-sided cross-sections, flat shading, no random lumps), proportions after the creator's
# reference video (huge barrel chest, hunch, long heavy arms, short wide legs), saturated colours with gold trim.
# Run inside Blender:  ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\build_boss01.py").read(), ns); ns["build_all"]()
# 1 BU = 1 stud, Z up, front = -Y, character's LEFT = +X.  Boss feet on z=0 at the origin, Pet at (PET_X, 0, 0).
# Objects: "<P>__<Bone>" main mesh, "<P>__<Bone>_<Colour>" detail welded to it,
#          "<P>__Head_Eyes_<Set+Set>_<Colour>" / "<P>__Head_Mouth_<Set>_<Colour>" swapped face pieces (ADR 0015).
import bpy, bmesh, math, json, os
from mathutils import Vector

OUT = r"C:\obsidian\Roblox studio\Assets\Bosses"
RENDERS = os.path.join(OUT, "renders")
PET_X = 40.0
COLORS = {
    "Fur": "b8601a", "FurDark": "6e300c", "FurLight": "ffd690", "Nose": "2a1810", "Claw": "fff4e0",
    "CapeRed": "ff2418", "CapeWhite": "fffaf0", "Leather": "5a2408", "Gold": "ffc414",
    "Honey": "ff9800", "Jar": "ffb000",
    "EyeGlow": "ffd400n", "Pupil": "2a1208", "Mouth": "3a1010", "Teeth": "fff4e0", "Tongue": "ff4a6e",
    "PetEye": "2a1208", "PetShine": "ffffff", "Blush": "ff7a7a",
}
PARTS = []
CTX = {"bone": "Body", "face": None, "ox": 0.0}
BONES = []

def clear():
    for o in list(bpy.data.objects):
        if o.type == "MESH": bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):
        if m.users == 0: bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)

def mat(key):
    m = bpy.data.materials.get(key)
    if m: return m
    m = bpy.data.materials.new(key); m.use_nodes = True
    h = COLORS[key].rstrip("n"); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*lin, 1); b.inputs["Roughness"].default_value = 0.6
    if COLORS[key].endswith("n"):
        b.inputs["Emission Color"].default_value = (*lin, 1); b.inputs["Emission Strength"].default_value = 4
    m.diffuse_color = (*lin, 1)
    return m

def _obj(bm, col):
    me = bpy.data.meshes.new("m"); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("m", me); bpy.context.collection.objects.link(o)
    for p in o.data.polygons: p.use_smooth = False
    o.data.materials.append(mat(col))
    o["col"] = col; o["bone"] = CTX["bone"]; o["face"] = CTX["face"] or ""
    o.location.x += CTX["ox"]
    PARTS.append(o); return o

def loft(rings, col, sides=8, ref=(0, -1, 0), cap=True, spin=None):
    """Faceted solid through cross-sections. rings: [(centre, rx, ry)], rx across, ry front-back.
    Each ring is perpendicular to the path; flat faces point front/back/sides."""
    pts = [Vector(r[0]) for r in rings]; ref = Vector(ref)
    off = math.pi / sides if spin is None else spin
    bm = bmesh.new(); loops = []
    for i, (c, rx, ry) in enumerate(rings):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        u = ref.cross(d)
        if u.length < 1e-4: u = Vector((1, 0, 0))
        u.normalize(); v = d.cross(u).normalized()
        loop = []
        for k in range(sides):
            a = off + 2 * math.pi * k / sides
            loop.append(bm.verts.new(pts[i] + u * (rx * math.cos(a)) + v * (ry * math.sin(a))))
        loops.append(loop)
    for a, b in zip(loops[:-1], loops[1:]):
        for k in range(sides):
            bm.faces.new((a[k], a[(k + 1) % sides], b[(k + 1) % sides], b[k]))
    if cap:
        bm.faces.new(list(reversed(loops[0]))); bm.faces.new(loops[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(bm, col)

def block(c, s, col, rot=(0, 0, 0), bevel=0.2):
    """chamfered box"""
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * s[0], v.co.y * s[1], v.co.z * s[2]))
    if bevel > 0: bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=1, affect="EDGES")
    from mathutils import Euler
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Euler(rot).to_matrix())
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector(c))
    return _obj(bm, col)

def plate(pts, depth, c, col, rot=(0, 0, 0), bevel=0.0):
    """flat piece from a 2D outline (x, z) extruded along y, placed at c"""
    from mathutils import Euler
    bm = bmesh.new(); vs = [bm.verts.new((x, -depth / 2, z)) for x, z in pts]
    f = bm.faces.new(vs); r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.y += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Euler(rot).to_matrix())
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector(c))
    return _obj(bm, col)

def wedge(base, tip, r, col, sides=4):
    """pointed spike / claw from base to tip"""
    base, tip = Vector(base), Vector(tip)
    return loft([(base, r, r), (base.lerp(tip, 0.55), r * 0.6, r * 0.6), (tip, 0.02, 0.02)], col, sides=sides)

def gem(c, r, col, sides=6, h=1.0):
    """low-poly drop / bead (two cones)"""
    c = Vector(c)
    return loft([(c + Vector((0, 0, r * h)), 0.02, 0.02), (c, r, r), (c - Vector((0, 0, r * h * 0.8)), 0.02, 0.02)], col, sides=sides)

def sheet(grid, cols_, thick=0.3):
    """checkered sheet: grid[j][i] = Vector; two objects (one per colour), each cell solidified"""
    for parity, col in enumerate(cols_):
        bm = bmesh.new()
        for j in range(len(grid) - 1):
            for i in range(len(grid[0]) - 1):
                if (i + j) % 2 != parity: continue
                q = [grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]]
                n = (q[1] - q[0]).cross(q[3] - q[0]).normalized() * thick / 2
                top = [bm.verts.new(p - n) for p in q]; bot = [bm.verts.new(p + n) for p in q]
                bm.faces.new(top); bm.faces.new(list(reversed(bot)))
                for k in range(4):
                    bm.faces.new((top[k], bot[k], bot[(k + 1) % 4], top[(k + 1) % 4]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        _obj(bm, col)

def bone(name, parent, at, store=None):
    (store if store is not None else BONES).append((name, parent, *at)); CTX["bone"] = name

def mirror(f):
    for sx, side in ((1, "Left"), (-1, "Right")): f(sx, side)

# ================= Boss 1 =================
def Boss():
    bone("HumanoidRootPart", None, (0, 0, 6.2))
    # ---- Body: hips + belly, belt, honey jar
    bone("Body", "HumanoidRootPart", (0, 0, 6.2))
    loft([((0, 0.2, 3.6), 3.0, 2.4), ((0, 0.0, 5.0), 4.0, 3.2), ((0, -0.2, 6.8), 4.3, 3.4), ((0, 0.0, 8.4), 3.9, 3.1)], "Fur")
    loft([((0, -2.5, 4.4), 2.4, 0.9), ((0, -3.0, 6.0), 3.0, 1.0), ((0, -2.9, 8.2), 2.8, 0.9)], "FurLight")
    loft([((0, -0.15, 7.1), 4.45, 3.55), ((0, -0.15, 8.0), 4.3, 3.45)], "Leather", sides=10, cap=False)
    block((0, -3.55, 7.55), (1.5, 0.45, 1.15), "Gold", bevel=0.15)
    block((0, -3.8, 7.55), (0.7, 0.2, 0.55), "Leather", bevel=0.08)
    jx, jy, jz = -4.45, -1.0, 6.3
    loft([((jx, jy, jz - 1.0), 0.85, 0.85), ((jx, jy, jz - 0.2), 1.05, 1.05), ((jx, jy, jz + 0.7), 0.95, 0.95),
          ((jx, jy, jz + 0.9), 0.7, 0.7), ((jx, jy, jz + 1.1), 0.7, 0.7)], "Jar")
    loft([((jx, jy, jz + 1.05), 1.05, 1.05), ((jx, jy, jz + 1.45), 0.95, 0.95)], "CapeRed")
    block((jx + 0.1, jy - 1.0, jz - 0.1), (1.05, 0.12, 0.8), "CapeWhite", bevel=0.06)
    for dx, h in ((-0.45, 1.1), (0.4, 0.7)):
        loft([((jx + dx, jy - 0.85, jz + 0.95), 0.2, 0.2), ((jx + dx, jy - 0.95, jz + 0.95 - h), 0.15, 0.15)], "Honey", sides=6)
        gem((jx + dx, jy - 0.95, jz + 0.7 - h), 0.28, "Honey")
    # ---- Legs + feet (short, wide stance)
    def leg(sx, side):
        bone(side + "Leg", "Body", (2.8 * sx, 0.2, 4.8))
        loft([((2.75 * sx, 0.2, 5.6), 2.2, 2.2), ((2.95 * sx, 0.0, 3.6), 2.05, 2.1), ((3.05 * sx, 0.1, 1.2), 1.6, 1.6)], "Fur")
        bone(side + "Foot", side + "Leg", (3.05 * sx, 0.1, 1.2))
        block((3.1 * sx, -0.7, 0.62), (3.0, 4.0, 1.25), "FurDark", bevel=0.35)
        block((3.1 * sx, -2.45, 0.35), (2.2, 0.7, 0.55), "FurLight", bevel=0.15)
        for k in (-1, 0, 1):
            wedge((3.1 * sx + k * 0.8, -2.7, 0.55), (3.1 * sx + k * 0.85, -3.6, 0.2), 0.24, "Claw")
    mirror(leg)
    # ---- Chest: barrel torso widest at the shoulders, hunched
    bone("Chest", "Body", (0, 0.1, 8.0))
    loft([((0, 0.3, 7.6), 3.9, 3.1), ((0, 0.2, 9.6), 5.0, 3.7), ((0, 0.4, 12.0), 6.1, 4.2),
          ((0, 0.9, 14.2), 6.5, 4.1), ((0, 1.4, 15.8), 4.9, 3.2), ((0, 1.5, 16.5), 2.6, 1.9)], "Fur")
    loft([((0, -2.9, 8.4), 2.8, 1.0), ((0, -3.55, 10.5), 3.8, 1.1), ((0, -3.6, 12.6), 4.0, 1.0), ((0, -3.0, 14.0), 3.0, 0.8)], "FurLight")
    # bandana: band + checkered triangle
    loft([((0, -0.8, 15.0), 3.4, 3.0), ((0, -0.8, 15.9), 3.2, 2.8)], "CapeRed", sides=10, cap=False)
    tri = []
    for j in range(4):
        z = 15.3 - j * 0.95; w = 4.2 * (1 - j / 3.6)
        tri.append([Vector((-w / 2 + w * i / 4, -3.9 - j * 0.25, z)) for i in range(5)])
    sheet(tri, ("CapeRed", "CapeWhite"), thick=0.25)
    block((0, -4.0, 15.45), (0.9, 0.5, 0.7), "Gold", bevel=0.12)
    # ---- Head: low and forward
    bone("Head", "Chest", (0, -1.6, 15.6))
    loft([((0, -2.1, 15.3), 2.1, 1.9), ((0, -2.4, 16.6), 2.9, 2.35), ((0, -2.3, 18.0), 2.75, 2.25), ((0, -2.1, 18.9), 1.7, 1.4)], "Fur")
    block((0, -4.95, 16.0), (2.7, 1.8, 1.8), "FurLight", bevel=0.35)
    loft([((0, -5.75, 16.5), 0.75, 0.3), ((0, -6.05, 16.75), 0.55, 0.2)], "Nose", sides=6, ref=(0, 0, 1))
    for sx in (1, -1):
        plate([(x * sx, z) for x, z in [(-1.05, -0.2), (0.9, 0.22), (0.9, 0.58), (-1.05, 0.25)]], 0.55, (1.05 * sx, -4.6, 17.85), "FurDark")
        wedge((2.5 * sx, -2.6, 16.4), (3.4 * sx, -2.4, 15.9), 0.55, "FurDark")
    def ear(sx, side):
        bone(side + "Ear", "Head", (1.9 * sx, -1.9, 18.5))
        loft([((2.0 * sx, -1.9, 18.4), 1.05, 0.5), ((2.15 * sx, -1.9, 19.2), 0.9, 0.45), ((2.2 * sx, -1.9, 19.55), 0.45, 0.3)], "FurDark", sides=6)
        block((2.12 * sx, -2.35, 19.0), (0.95, 0.12, 0.7), "FurLight", bevel=0.1)
    mirror(ear)
    # ---- Arms: long and heavy, paws hang to the knees
    def arm(sx, side):
        S, E, W = Vector((6.1 * sx, 0.6, 14.2)), Vector((7.5 * sx, -0.4, 10.4)), Vector((7.7 * sx, -1.5, 6.6))
        bone(side + "UpperArm", "Chest", tuple(S))
        loft([(S + Vector((0, 0, 1.4)), 1.8, 1.8), (S, 2.55, 2.45), (S.lerp(E, 0.5), 2.15, 2.05), (E, 1.75, 1.7)], "Fur")
        loft([(S.lerp(E, 0.28) + Vector((0, 0, 0.45)), 2.45, 2.35), (S.lerp(E, 0.28) - Vector((0, 0, 0.35)), 2.45, 2.35)], "Gold", sides=8)   # gold arm band
        for k in range(3):
            wedge((S.x + 0.3 * sx * k, 0.9 - 0.6 * k, 15.6 - 0.2 * k), (S.x + 1.1 * sx + 0.5 * sx * k, 1.4 - 0.8 * k, 17.2 - 0.4 * k), 0.6, "FurDark", sides=5)
        bone(side + "LowerArm", side + "UpperArm", tuple(E))
        loft([(E, 1.75, 1.7), (E.lerp(W, 0.45), 2.3, 2.15), (W, 1.75, 1.7)], "Fur")
        loft([(W + Vector((0, 0.1, 0.55)), 1.95, 1.9), (W + Vector((0, 0, -0.15)), 1.95, 1.9)], "Gold", sides=8)   # gold cuff
        bone(side + "Hand", side + "LowerArm", tuple(W))
        block((7.75 * sx, -1.7, 5.15), (3.0, 2.8, 2.5), "FurDark", bevel=0.45)
        block((7.75 * sx, -3.1, 4.75), (1.3, 0.25, 0.9), "FurLight", bevel=0.12)
        for k in range(4):
            x = 7.75 * sx + (k - 1.5) * 0.72
            block((x, -2.55, 3.55), (0.62, 1.1, 1.0), "FurDark", bevel=0.15)
            wedge((x, -3.0, 3.1), (x, -3.75, 2.4), 0.24, "Claw")
        for dx, h in ((0.75, 1.3), (-0.6, 0.8)):
            loft([((7.75 * sx + dx, -1.5, 3.95), 0.24, 0.24), ((7.75 * sx + dx, -1.6, 3.95 - h), 0.16, 0.16)], "Honey", sides=6)
            gem((7.75 * sx + dx, -1.6, 3.7 - h), 0.32, "Honey")
    mirror(arm)
    # ---- Cape: one checkered sheet wrapping the back
    bone("Cape", "Chest", (0, 4.4, 15.4))
    grid = []
    rows, cols = 7, 8
    for j in range(rows + 1):
        z = 15.6 - j * 1.3; spread = 1 + j * 0.05
        row = []
        for i in range(cols + 1):
            x = (-4.8 + 9.6 * i / cols) * spread
            row.append(Vector((x, 5.1 + 0.3 * j - 0.075 * x * x, z)))
        grid.append(row)
    sheet(grid, ("CapeRed", "CapeWhite"), thick=0.3)
    loft([((0, 1.6, 15.4), 4.4, 3.6), ((0, 1.6, 16.0), 4.0, 3.2)], "CapeRed", sides=10, cap=False)   # collar

# ---- face pieces (Head bone) ----
EYE_X, EYE_Y, EYE_Z = 1.12, -4.62, 17.15
MOUTH_Y, MOUTH_Z = -5.88, 15.55
def face(slot, sets):
    CTX["bone"] = "Head"; CTX["face"] = f"{slot}_{'+'.join(sets)}"

def eyes(shape, col="EyeGlow", pupil=None):
    for sx in (1, -1):
        plate([(x * sx, z) for x, z in shape], 0.14, (EYE_X * sx, EYE_Y, EYE_Z), col)
        if pupil:
            p = [(-0.17, -0.17), (0.17, -0.17), (0.17, 0.17), (-0.17, 0.17)]
            plate([(x + pupil[0], z + pupil[1]) for x, z in p], 0.08, (EYE_X * sx, EYE_Y - 0.1, EYE_Z), "Pupil")

def Faces():
    lid = [(-0.62, -0.28), (0.58, -0.3), (0.65, 0.08), (-0.65, 0.34)]
    face("Eyes", ["Grumpy"]); eyes(lid, pupil=(0, -0.04))
    face("Eyes", ["GlanceL"]); eyes(lid, pupil=(0.3, -0.04))
    face("Eyes", ["GlanceR"]); eyes(lid, pupil=(-0.3, -0.04))
    face("Eyes", ["Angry"]); eyes([(-0.62, -0.32), (0.58, -0.32), (0.62, -0.08), (-0.66, 0.45)], pupil=(0, -0.1))
    face("Eyes", ["Hurt"]); eyes([(-0.58, 0.32), (0.38, 0.02), (-0.58, -0.28), (-0.42, 0.02)])
    face("Eyes", ["Blink"]); eyes([(-0.62, -0.08), (0.62, -0.08), (0.62, 0.07), (-0.62, 0.07)])
    face("Eyes", ["Dazed"])
    for sx in (1, -1):
        loft([((EYE_X * sx, EYE_Y + 0.07, EYE_Z), 0.48, 0.48), ((EYE_X * sx, EYE_Y - 0.07, EYE_Z), 0.48, 0.48)], "EyeGlow", sides=8, ref=(0, 0, 1))
        loft([((EYE_X * sx, EYE_Y - 0.06, EYE_Z), 0.3, 0.3), ((EYE_X * sx, EYE_Y - 0.14, EYE_Z), 0.3, 0.3)], "Pupil", sides=8, ref=(0, 0, 1))
        loft([((EYE_X * sx, EYE_Y - 0.1, EYE_Z), 0.13, 0.13), ((EYE_X * sx, EYE_Y - 0.18, EYE_Z), 0.13, 0.13)], "EyeGlow", sides=6, ref=(0, 0, 1))
    def band(w, h, lo, thick, up):
        top, bot = [], []
        for i in range(9):
            t = -1 + i / 4; x = t * w / 2; z = h * (1 - t * t) * (1 if up else -1) + lo
            top.append((x, z + thick / 2)); bot.append((x, z - thick / 2))
        return top + bot[::-1]
    face("Mouth", ["Grumpy"])
    plate(band(1.8, 0.3, -0.12, 0.26, True), 0.12, (0, MOUTH_Y, MOUTH_Z), "Mouth")
    for sx in (1, -1): plate([(-0.13, 0), (0.13, 0), (0, -0.32)], 0.14, (0.5 * sx, MOUTH_Y - 0.05, MOUTH_Z + 0.02), "Teeth")
    face("Mouth", ["Angry"])
    plate([(-0.95, 0.18), (0.95, 0.18), (0.75, -0.38), (-0.75, -0.38)], 0.12, (0, MOUTH_Y, MOUTH_Z), "Mouth")
    for k in range(5): plate([(-0.16, 0), (0.16, 0), (0, -0.26)], 0.14, (-0.64 + k * 0.32, MOUTH_Y - 0.05, MOUTH_Z + 0.16), "Teeth")
    face("Mouth", ["Roar"])
    plate([(-1.0, 0.35), (1.0, 0.35), (0.8, -0.75), (0, -0.98), (-0.8, -0.75)], 0.12, (0, MOUTH_Y, MOUTH_Z - 0.1), "Mouth")
    plate([(-0.5, -0.5), (0.5, -0.5), (0.36, -0.86), (-0.36, -0.86)], 0.14, (0, MOUTH_Y - 0.04, MOUTH_Z - 0.1), "Tongue")
    for sx in (1, -1):
        plate([(-0.19, 0), (0.19, 0), (0, -0.48)], 0.16, (0.62 * sx, MOUTH_Y - 0.06, MOUTH_Z + 0.25), "Teeth")
        plate([(-0.15, 0), (0.15, 0), (0, 0.36)], 0.16, (0.46 * sx, MOUTH_Y - 0.06, MOUTH_Z - 0.86), "Teeth")
    face("Mouth", ["Hurt"])
    plate([(-0.9, 0.2), (-0.42, 0.05), (0, 0.22), (0.42, 0.05), (0.9, 0.2), (0.84, -0.26), (-0.84, -0.26)], 0.12, (0, MOUTH_Y, MOUTH_Z), "Mouth")
    plate([(-0.72, 0.05), (0.72, 0.05), (0.7, -0.12), (-0.7, -0.12)], 0.14, (0, MOUTH_Y - 0.05, MOUTH_Z), "Teeth")
    face("Mouth", ["Dazed"])
    plate([(math.cos(a) * 0.42, math.sin(a) * 0.34) for a in [k * math.pi / 5 for k in range(10)]], 0.12, (0.2, MOUTH_Y, MOUTH_Z - 0.05), "Mouth")
    plate([(-0.23, 0), (0.23, 0), (0.19, -0.42), (-0.19, -0.42)], 0.14, (0.36, MOUTH_Y - 0.05, MOUTH_Z - 0.22), "Tongue")
    CTX["face"] = None

# ================= Pet 1: chibi bear =================
PET_BONES = []
def Pet():
    b = PET_BONES
    bone("HumanoidRootPart", None, (0, 0, 2.6), b)
    bone("Body", "HumanoidRootPart", (0, 0, 2.6), b)
    loft([((0, 0.1, 0.9), 1.6, 1.4), ((0, 0.0, 2.2), 2.3, 1.95), ((0, 0.0, 3.7), 2.0, 1.7), ((0, 0.0, 4.3), 1.3, 1.1)], "Fur")
    loft([((0, -1.55, 1.4), 1.2, 0.4), ((0, -1.85, 2.6), 1.5, 0.45), ((0, -1.6, 3.7), 1.2, 0.35)], "FurLight")
    loft([((-2.15, -0.7, 2.3), 0.5, 0.5), ((-2.15, -0.7, 3.2), 0.5, 0.5)], "Jar", sides=8)
    loft([((-2.15, -0.7, 3.15), 0.6, 0.6), ((-2.15, -0.7, 3.45), 0.55, 0.55)], "CapeRed", sides=8)
    bone("Head", "Body", (0, -0.2, 4.3), b)
    loft([((0, -0.3, 4.4), 2.2, 2.0), ((0, -0.4, 5.6), 3.2, 2.7), ((0, -0.35, 7.6), 3.1, 2.6), ((0, -0.3, 8.6), 2.0, 1.7)], "Fur")
    block((0, -2.95, 5.8), (2.0, 1.2, 1.3), "FurLight", bevel=0.3)
    loft([((0, -3.5, 6.25), 0.5, 0.22), ((0, -3.7, 6.42), 0.36, 0.15)], "Nose", sides=6, ref=(0, 0, 1))
    loft([((0, -0.6, 4.35), 2.5, 2.3), ((0, -0.6, 4.95), 2.35, 2.15)], "CapeRed", sides=10, cap=False)
    tri = []
    for j in range(3):
        z = 4.75 - j * 0.6; w = 2.2 * (1 - j / 2.6)
        tri.append([Vector((-w / 2 + w * i / 3, -2.25 - j * 0.12, z)) for i in range(4)])
    sheet(tri, ("CapeRed", "CapeWhite"), thick=0.18)
    for sx in (1, -1):
        loft([((2.3 * sx, -0.4, 8.3), 1.0, 0.5), ((2.45 * sx, -0.4, 9.1), 0.85, 0.42), ((2.5 * sx, -0.4, 9.45), 0.4, 0.25)], "FurDark", sides=6)
        block((2.42 * sx, -0.85, 8.95), (0.85, 0.12, 0.65), "FurLight", bevel=0.1)
        block((1.65 * sx, -2.95, 6.05), (0.6, 0.1, 0.3), "Blush", bevel=0.06)
    for sx, side in ((1, "Left"), (-1, "Right")):
        bone(side + "UpperArm", "Body", (2.0 * sx, 0, 3.6), b)
        loft([((2.0 * sx, 0, 3.8), 0.85, 0.85), ((2.5 * sx, -0.4, 2.4), 0.8, 0.8), ((2.65 * sx, -0.6, 1.5), 0.85, 0.85)], "Fur", sides=7)
        block((2.7 * sx, -0.7, 1.3), (1.4, 1.4, 1.1), "FurDark", bevel=0.3)
        bone(side + "Leg", "Body", (1.1 * sx, 0, 1.3), b)
        loft([((1.1 * sx, 0, 1.4), 0.95, 0.95), ((1.15 * sx, 0, 0.6), 0.85, 0.85)], "Fur", sides=7)
        block((1.15 * sx, -0.5, 0.33), (1.6, 2.1, 0.66), "FurDark", bevel=0.2)
    ex, ey, ez = 1.1, -3.0, 7.0
    CTX["bone"] = "Head"; CTX["face"] = "Eyes_Happy"
    for sx in (1, -1):
        plate([(-0.38, -0.45), (0.38, -0.45), (0.42, 0.38), (-0.42, 0.38)], 0.14, (ex * sx, ey, ez), "PetEye")
        plate([(-0.12, -0.12), (0.12, -0.12), (0.12, 0.12), (-0.12, 0.12)], 0.06, (ex * sx + 0.14, ey - 0.1, ez + 0.16), "PetShine")
    CTX["face"] = "Eyes_Blink"
    for sx in (1, -1):
        plate([(-0.42, -0.04), (0, 0.16), (0.42, -0.04), (0.42, -0.18), (0, 0.02), (-0.42, -0.18)], 0.14, (ex * sx, ey, ez - 0.1), "PetEye")
    CTX["face"] = "Mouth_Happy"
    plate([(-0.42, 0.06), (0, -0.2), (0.42, 0.06), (0.42, -0.08), (0, -0.36), (-0.42, -0.08)], 0.12, (0, -3.58, 5.55), "Mouth")
    CTX["face"] = None

# ================= finish / export / review =================
def finish(prefix):
    groups = {}
    for o in PARTS: groups.setdefault((o["bone"], o["col"], o["face"]), []).append(o)
    main_col = {}
    for o in PARTS:
        if not o["face"]: main_col.setdefault(o["bone"], o["col"])
    for (b, col, f), objs in groups.items():
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs: o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        if len(objs) > 1: bpy.ops.object.join()
        j = bpy.context.object
        name = f"{b}_{f}_{col}" if f else (b if col == main_col.get(b) else f"{b}_{col}")
        j.name = j.data.name = f"{prefix}__{name}"
    PARTS.clear()

def anchor(prefix, x):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((x, 0, 0)))
    me = bpy.data.meshes.new(prefix + "__Anchor"); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(prefix + "__Anchor", me); bpy.context.collection.objects.link(o)
    o.hide_render = True

def build_all():
    clear(); BONES.clear(); PET_BONES.clear()
    CTX["ox"] = 0.0; Boss(); Faces(); finish("B01"); anchor("B01", 0)
    CTX["ox"] = PET_X; Pet(); finish("P01"); anchor("P01", PET_X)
    json.dump({"colors": COLORS, "boss_bones": BONES, "pet_bones": PET_BONES, "pet_x": PET_X,
               "expressions": {"Grumpy": ["Grumpy", "Grumpy"], "Angry": ["Angry", "Angry"], "Roar": ["Angry", "Roar"],
                               "Hurt": ["Hurt", "Hurt"], "Dazed": ["Dazed", "Dazed"], "Blink": ["Blink", "Grumpy"],
                               "GlanceL": ["GlanceL", "Grumpy"], "GlanceR": ["GlanceR", "Grumpy"]},
               "pet_expressions": {"Happy": ["Happy", "Happy"], "Blink": ["Blink", "Happy"]}},
              open(os.path.join(OUT, "boss01_rig.json"), "w"), indent=1)
    show_expression("B01", "Grumpy", "Grumpy"); show_expression("P01", "Happy", "Happy")

def show_expression(prefix, eyes_set, mouth_set):
    for o in bpy.data.objects:
        n = o.name
        for slot, want in (("Eyes", eyes_set), ("Mouth", mouth_set)):
            tag = f"{prefix}__Head_{slot}_"
            if n.startswith(tag):
                on = want in n[len(tag):].rsplit("_", 1)[0].split("+")
                o.hide_render = not on; o.hide_viewport = not on

def setup_render():
    sc = bpy.context.scene
    cam = bpy.data.objects.get("ReviewCam")
    if not cam:
        cam = bpy.data.objects.new("ReviewCam", bpy.data.cameras.new("ReviewCam")); sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"; sh.color_type = "MATERIAL"; sh.show_shadows = True; sh.show_cavity = False
    sh.show_object_outline = True; sh.object_outline_color = (0.1, 0.06, 0.04)
    sc.display.shadow_focus = 0.6
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"; sc.view_settings.exposure = 0.75
    sc.render.image_settings.file_format = "PNG"
    os.makedirs(RENDERS, exist_ok=True)
    return sc, cam

def shot(name, target, dist, yaw, pitch=0.12, res=(700, 800), lens=50):
    sc, cam = setup_render()
    cam.data.lens = lens
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = res[0], res[1], 100
    t = Vector(target)
    d = Vector((math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), math.sin(pitch))) * dist
    cam.location = t + d
    cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = os.path.join(RENDERS, name + ".png")
    bpy.ops.render.render(write_still=True)
    return sc.render.filepath
