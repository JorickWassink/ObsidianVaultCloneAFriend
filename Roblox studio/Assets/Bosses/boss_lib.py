# Shared Blender helpers for the faceted Boss restyle (vault: Design/Clone a Friend Boss Restyle, ADR 0016).
# A boss file does:  exec(open(LIB).read(), globals());  sets COLORS;  defines Boss(), Faces(), Pet();  calls build_all(...)
# 1 BU = 1 stud, Z up, front = -Y, character's LEFT = +X. Boss feet on z=0 at the origin, Pet at (PET_X, 0, 0).
# Objects: "<P>__<Bone>" main mesh, "<P>__<Bone>_<Colour>" detail welded to it,
#          "<P>__Head_Eyes_<Set+Set>_<Colour>" / "<P>__Head_Mouth_<Set>_<Colour>" swapped face pieces (ADR 0015).
import bpy, bmesh, math, json, os
from mathutils import Vector, Euler

BOSS_DIR = r"C:\obsidian\Roblox studio\Assets\Bosses"
RENDERS = os.path.join(BOSS_DIR, "renders")
PET_X = 40.0
COLORS = {}
PARTS = []
CTX = {"bone": "Body", "face": None, "ox": 0.0}
BONES, PET_BONES = [], []
BOSS_EXPRESSIONS = {"Grumpy": ["Grumpy", "Grumpy"], "Angry": ["Angry", "Angry"], "Roar": ["Angry", "Roar"],
                    "Hurt": ["Hurt", "Hurt"], "Dazed": ["Dazed", "Dazed"], "Blink": ["Blink", "Grumpy"],
                    "GlanceL": ["GlanceL", "Grumpy"], "GlanceR": ["GlanceR", "Grumpy"]}
PET_EXPRESSIONS = {"Happy": ["Happy", "Happy"], "Blink": ["Blink", "Happy"]}

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
    for p in o.data.polygons: p.use_smooth = bool(CTX.get("smooth"))
    o.data.materials.append(mat(col))
    o["col"] = col; o["bone"] = CTX["bone"]; o["face"] = CTX["face"] or ""
    o.location.x += CTX["ox"]
    PARTS.append(o); return o

def loft(rings, col, sides=8, ref=(0, -1, 0), cap=True, spin=None):
    """Faceted solid through cross-sections [(centre, rx, ry)]; rx across, ry front-back."""
    pts = [Vector(r[0]) for r in rings]; ref = Vector(ref)
    off = math.pi / sides if spin is None else spin
    bm = bmesh.new(); loops = []
    for i, (c, rx, ry) in enumerate(rings):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        u = ref.cross(d)
        if u.length < 1e-4: u = Vector((1, 0, 0))
        u.normalize(); v = d.cross(u).normalized()
        loops.append([bm.verts.new(pts[i] + u * (rx * math.cos(off + 2 * math.pi * k / sides)) + v * (ry * math.sin(off + 2 * math.pi * k / sides))) for k in range(sides)])
    for a, b in zip(loops[:-1], loops[1:]):
        for k in range(sides): bm.faces.new((a[k], a[(k + 1) % sides], b[(k + 1) % sides], b[k]))
    if cap: bm.faces.new(list(reversed(loops[0]))); bm.faces.new(loops[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(bm, col)

def block(c, s, col, rot=(0, 0, 0), bevel=0.2):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * s[0], v.co.y * s[1], v.co.z * s[2]))
    if bevel > 0: bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=1, affect="EDGES")
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Euler(rot).to_matrix())
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector(c))
    return _obj(bm, col)

def plate(pts, depth, c, col, rot=(0, 0, 0)):
    """flat piece from a 2D outline (x, z) extruded along y"""
    bm = bmesh.new(); vs = [bm.verts.new((x, -depth / 2, z)) for x, z in pts]
    f = bm.faces.new(vs); r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.y += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Euler(rot).to_matrix())
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector(c))
    return _obj(bm, col)

def wedge(base, tip, r, col, sides=4):
    base, tip = Vector(base), Vector(tip)
    return loft([(base, r, r), (base.lerp(tip, 0.55), r * 0.6, r * 0.6), (tip, 0.02, 0.02)], col, sides=sides)

def gem(c, r, col, sides=6, h=1.0):
    c = Vector(c)
    return loft([(c + Vector((0, 0, r * h)), 0.02, 0.02), (c, r, r), (c - Vector((0, 0, r * h * 0.8)), 0.02, 0.02)], col, sides=sides)

def puff(c, r, col, sub=1):
    """faceted ball (low-poly ico sphere), no random jitter"""
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=r)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector(c))
    return _obj(bm, col)

def disc(c, r, depth, col, sides=12, axis="Y"):
    rot = {"Y": (0, 0, 0), "X": (0, 0, math.pi / 2), "Z": (math.pi / 2, 0, 0)}[axis]
    c = Vector(c); d = Vector((0, depth / 2, 0)); d.rotate(Euler(rot))
    return loft([(c - d, r, r), (c + d, r, r)], col, sides=sides, ref=(0, 0, 1) if axis != "Z" else (0, 1, 0))

def sheet(grid, cols_, thick=0.3):
    for parity, col in enumerate(cols_):
        bm = bmesh.new()
        for j in range(len(grid) - 1):
            for i in range(len(grid[0]) - 1):
                if len(cols_) > 1 and (i + j) % 2 != parity: continue
                q = [grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]]
                n = (q[1] - q[0]).cross(q[3] - q[0]).normalized() * thick / 2
                top = [bm.verts.new(p - n) for p in q]; bot = [bm.verts.new(p + n) for p in q]
                bm.faces.new(top); bm.faces.new(list(reversed(bot)))
                for k in range(4): bm.faces.new((top[k], bot[k], bot[(k + 1) % 4], top[(k + 1) % 4]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        _obj(bm, col)

def bone(name, parent, at, store=None):
    (store if store is not None else BONES).append((name, parent, *at)); CTX["bone"] = name

def mirror(f):
    for sx, side in ((1, "Left"), (-1, "Right")): f(sx, side)

def star_pts(r_out, r_in, n=5, rot=math.pi / 2):
    return [((r_out if k % 2 == 0 else r_in) * math.cos(rot + k * math.pi / n), (r_out if k % 2 == 0 else r_in) * math.sin(rot + k * math.pi / n)) for k in range(n * 2)]

# ---------------- chunky chibi Boss body (2026-11-12: "make them more chibi, they all look too buff") ----------------
# Template units: head top at z 17.4 (head = z 10.2..17.4, about 40%), feet on z 0. normalize_height() scales the
# finished Boss to its real height afterwards. Bones: Body, Chest, Head, Left/Right UpperArm, LowerArm, Hand, Leg, Foot.
# Returns key spots for the boss file: head centre/front, eye and mouth spots, shoulders/elbows/wrists, hand centres.
CHIBI = {
    "head_c": (0, -0.75, 13.4), "head_front": -4.42, "eye_z": 14.0, "eye_x": 1.6, "mouth_z": 11.75,
    "S": (4.0, 0.2, 9.0), "E": (4.9, -0.5, 7.2), "W": (5.2, -1.0, 5.6), "hand": (5.3, -1.3, 4.6),
}

def on(name):
    CTX["bone"] = name

def chibi_base(fur="Fur", dark="FurDark", light="FurLight", hand=None, foot=None, arm_low=None, belly=True, chest=True,
               head=True, wide=1.0):
    hand = hand or dark; foot = foot or dark; arm_low = arm_low or fur
    bone("HumanoidRootPart", None, (0, 0, 4.4))
    bone("Body", "HumanoidRootPart", (0, 0, 4.4))
    loft([((0, 0.15, 2.3), 2.6 * wide, 2.3), ((0, 0.0, 3.8), 3.6 * wide, 3.15), ((0, -0.1, 5.4), 3.8 * wide, 3.3), ((0, 0.0, 6.6), 3.35 * wide, 3.0)], fur)
    if belly:
        loft([((0, -2.55, 2.9), 2.2 * wide, 0.8), ((0, -3.2, 4.5), 2.8 * wide, 0.9), ((0, -3.0, 6.1), 2.4 * wide, 0.8)], light)
    def leg(sx, side):
        bone(side + "Leg", "Body", (2.0 * sx, 0.1, 3.0))
        loft([((2.0 * sx, 0.1, 3.4), 1.7, 1.7), ((2.15 * sx, 0.0, 1.0), 1.5, 1.5)], fur)
        bone(side + "Foot", side + "Leg", (2.15 * sx, 0.0, 1.0))
        block((2.2 * sx, -0.6, 0.55), (2.6, 3.4, 1.1), foot, bevel=0.45)
    mirror(leg)
    bone("Chest", "Body", (0, 0.0, 6.4))
    loft([((0, 0.0, 6.2), 3.35 * wide, 3.0), ((0, 0.05, 7.8), 4.0 * wide, 3.35), ((0, 0.2, 9.2), 4.2 * wide, 3.35), ((0, 0.3, 10.2), 3.2, 2.6), ((0, 0.3, 10.6), 1.8, 1.5)], fur)
    if chest:
        loft([((0, -2.75, 6.8), 2.4 * wide, 0.8), ((0, -3.15, 8.2), 2.8 * wide, 0.85), ((0, -2.85, 9.4), 2.2 * wide, 0.7)], light)
    if head:
        bone("Head", "Chest", (0, -0.4, 10.4))
        loft([((0, -0.5, 10.2), 2.6, 2.4), ((0, -0.7, 11.4), 4.0, 3.6), ((0, -0.8, 13.4), 4.4, 3.9),
              ((0, -0.7, 15.4), 4.1, 3.6), ((0, -0.5, 16.8), 2.9, 2.6), ((0, -0.4, 17.4), 1.4, 1.3)], fur)
    def arm(sx, side):
        S, E, W = Vector(CHIBI["S"]), Vector(CHIBI["E"]), Vector(CHIBI["W"])
        S.x *= sx; E.x *= sx; W.x *= sx
        bone(side + "UpperArm", "Chest", tuple(S))
        loft([(S + Vector((0, 0, 0.9)), 1.25, 1.25), (S, 1.65, 1.6), (E, 1.3, 1.25)], fur)
        bone(side + "LowerArm", side + "UpperArm", tuple(E))
        loft([(E, 1.3, 1.25), (E.lerp(W, 0.5), 1.42, 1.35), (W, 1.2, 1.15)], arm_low)
        bone(side + "Hand", side + "LowerArm", tuple(W))
        h = Vector(CHIBI["hand"]); h.x *= sx
        block(tuple(h), (2.5, 2.4, 2.2), hand, bevel=0.55)
    mirror(arm)
    return CHIBI

# ---------------- cartoon Boss (2026-11-12: "cartooney", approved 2D concepts) ----------------
# Smooth rounded low-poly (CTX smooth on) for body and head; props are built with smooth(False).
# Template units: head top about z 17.7, feet on z 0; normalize_height() scales to the real height.
TOON = {"head_c": (0, -0.3, 15.2), "head_r": (2.7, 2.4, 2.5), "eye_x": 0.95, "eye_z": 15.5, "eye_y": -2.55,
        "muzzle": (0, -2.55, 14.15), "S": (2.3, 0.0, 11.0), "E": (3.2, -0.2, 8.6), "W": (3.4, -0.4, 6.7),
        "hand": (3.45, -0.5, 6.0)}

def smooth(on=True):
    CTX["smooth"] = on

def ell(c, r, col, seg=14, ring=10):
    """smooth low-poly ellipsoid, radii r = (x, y, z)"""
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=ring, radius=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * r[0], v.co.y * r[1], v.co.z * r[2])) + Vector(c)
    return _obj(bm, col)

def tube(points, r, col, sides=10):
    """bendy limb through points, radius r (number or list), round caps"""
    rs = r if isinstance(r, (list, tuple)) else [r] * len(points)
    loft([(p, q, q) for p, q in zip(points, rs)], col, sides=sides, ref=(0, -1, 0))
    ell(points[0], (rs[0], rs[0], rs[0]), col, seg=10, ring=6); ell(points[-1], (rs[-1], rs[-1], rs[-1]), col, seg=10, ring=6)

def toon_base(fur="Fur", dark="FurDark", light="FurLight", hand=None, foot=None, arm=None, leg=None, belly=True, wide=1.0):
    hand = hand or dark; foot = foot or dark; arm = arm or fur; leg = leg or fur
    smooth(True)
    bone("HumanoidRootPart", None, (0, 0, 4.0))
    bone("Body", "HumanoidRootPart", (0, 0, 4.0))
    loft([((0, 0.0, 2.9), 1.8 * wide, 1.6), ((0, 0.0, 3.7), 3.0 * wide, 2.6), ((0, -0.1, 5.4), 3.7 * wide, 3.1), ((0, -0.05, 7.4), 3.45 * wide, 2.95), ((0, 0.0, 8.2), 3.1 * wide, 2.7)], fur, sides=14)
    if belly: ell((0, -2.15, 5.9), (2.15 * wide, 1.05, 2.5), light)
    def legf(sx, side):
        bone(side + "Leg", "Body", (1.4 * sx, 0.0, 3.4))
        tube([(1.4 * sx, 0.0, 3.6), (1.45 * sx, 0.0, 0.9)], 0.78, leg)
        bone(side + "Foot", side + "Leg", (1.45 * sx, 0.0, 0.8))
        ell((1.5 * sx, -0.55, 0.45), (1.25, 1.65, 0.5), foot)
    mirror(legf)
    bone("Chest", "Body", (0, 0.0, 7.8))
    loft([((0, 0.0, 7.6), 3.4 * wide, 2.9), ((0, 0.05, 9.4), 3.05 * wide, 2.6), ((0, 0.0, 10.6), 2.6, 2.2), ((0, 0.0, 11.6), 1.95, 1.65), ((0, 0.0, 12.3), 1.3, 1.1)], fur, sides=14)
    if belly: ell((0, -2.1, 8.6), (1.8 * wide, 0.8, 1.5), light)
    bone("Head", "Chest", (0, -0.2, 12.4))
    ell(TOON["head_c"], TOON["head_r"], fur, seg=16, ring=12)
    def armf(sx, side):
        S, E, W = Vector(TOON["S"]), Vector(TOON["E"]), Vector(TOON["W"])
        S.x *= sx; E.x *= sx; W.x *= sx
        bone(side + "UpperArm", "Chest", tuple(S))
        tube([S, S.lerp(E, 0.5) + Vector((0.25 * sx, 0, 0)), E], [0.8, 0.72, 0.68], arm)
        bone(side + "LowerArm", side + "UpperArm", tuple(E))
        tube([E, W], [0.68, 0.64], arm)
        bone(side + "Hand", side + "LowerArm", tuple(W))
        h = Vector(TOON["hand"]); h.x *= sx
        ell(tuple(h), (1.0, 0.95, 1.0), hand)
    mirror(armf)
    return TOON

def toon_faces(ex=None, ey=None, ez=None, my=None, mz=None, s=1.0, iris="EyeGlow", white="EyeWhite", pupil="Pupil",
               lid="FurDark", mouth="Mouth", teeth="Teeth", tongue="Tongue", buck=False, look=(0, 0)):
    """cartoon face sets: 3D eye whites, glowing iris, pupil, highlight; lids for Grumpy/Angry"""
    ex = ex if ex is not None else TOON["eye_x"]; ey = ey if ey is not None else TOON["eye_y"]; ez = ez if ez is not None else TOON["eye_z"]
    my = my if my is not None else -3.32; mz = mz if mz is not None else 13.85
    smooth(True)
    def whites():
        for sx in (1, -1): ell((ex * sx, ey, ez), (0.56 * s, 0.3 * s, 0.66 * s), white, seg=14, ring=8)
    def iris_at(dx, dz, r=0.36):
        for sx in (1, -1):
            c = Vector((ex * sx + dx * s, ey - 0.31 * s, ez + dz * s))
            loft([(c + Vector((0, 0.05, 0)), r * s, r * s), (c - Vector((0, 0.04, 0)), r * s, r * s)], iris, sides=12, ref=(0, 0, 1))
            loft([(c - Vector((0, 0.03, 0)), 0.17 * s, 0.17 * s), (c - Vector((0, 0.08, 0)), 0.17 * s, 0.17 * s)], pupil, sides=10, ref=(0, 0, 1))
            loft([(c + Vector((0.13 * s, -0.08, 0.15 * s)), 0.09 * s, 0.09 * s), (c + Vector((0.13 * s, -0.11, 0.15 * s)), 0.09 * s, 0.09 * s)], white, sides=8, ref=(0, 0, 1))
    def lids(drop, tilt):
        for sx in (1, -1):
            plate([(x * sx, z) for x, z in [(-0.66, 0.2 - tilt * 0.3), (0.66, 0.2 + tilt * 0.3), (0.62, 0.75), (-0.62, 0.75)]], 0.12 * s,
                  (ex * sx, ey - 0.3 * s, ez + (0.38 - drop) * s), lid)
    smooth(True)
    _face("Eyes", ["Grumpy", "Angry", "GlanceL", "GlanceR", "Dazed"]); whites()
    smooth(False)
    _face("Eyes", ["Grumpy"]); iris_at(0, -0.1); lids(0.15, 0.25)
    _face("Eyes", ["GlanceL"]); iris_at(0.2, -0.1); lids(0.15, 0.25)
    _face("Eyes", ["GlanceR"]); iris_at(-0.2, -0.1); lids(0.15, 0.25)
    _face("Eyes", ["Angry"]); iris_at(0, -0.15, 0.3); lids(0.35, 0.6)
    _face("Eyes", ["Dazed"])
    for sx in (1, -1):
        for rr in (0.36, 0.18):
            c = Vector((ex * sx, ey - 0.3 * s, ez))
            loft([(c, rr * s, rr * s), (c - Vector((0, 0.05, 0)), rr * s, rr * s)], pupil, sides=12, ref=(0, 0, 1), cap=False)
            loft([(c, (rr - 0.07) * s, (rr - 0.07) * s), (c - Vector((0, 0.05, 0)), (rr - 0.07) * s, (rr - 0.07) * s)], white, sides=12, ref=(0, 0, 1))
    _face("Eyes", ["Hurt"])
    for sx in (1, -1):
        plate([(x * sx * s, z * s) for x, z in [(-0.5, 0.35), (0.35, 0.03), (-0.5, -0.3), (-0.34, 0.03)]], 0.14 * s, (ex * sx, ey - 0.12 * s, ez), pupil)
    _face("Eyes", ["Blink"])
    for sx in (1, -1):
        plate([(x * s, z * s) for x, z in [(-0.55, 0.05), (0, -0.12), (0.55, 0.05), (0.55, -0.08), (0, -0.26), (-0.55, -0.08)]], 0.14 * s, (ex * sx, ey - 0.12 * s, ez), pupil)
    S = lambda pts: [(x * s, z * s) for x, z in pts]
    def bucks(dz=0.0):
        for sx in (1, -1): plate(S([(-0.17, 0), (0.17, 0), (0.17, -0.36), (-0.17, -0.36)]), 0.12 * s, (0.19 * s * sx, my - 0.06 * s, mz + (0.08 + dz) * s), teeth)
    _face("Mouth", ["Grumpy"])
    plate(S([(-0.7, -0.05), (0, 0.22), (0.7, -0.05), (0.7, -0.2), (0, 0.06), (-0.7, -0.2)]), 0.12 * s, (0, my, mz), mouth)
    if buck: bucks(0.02)
    else: plate(S([(-0.1, 0), (0.1, 0), (0, -0.24)]), 0.14 * s, (0.3 * s, my - 0.05 * s, mz - 0.02 * s), teeth)
    _face("Mouth", ["Angry"])
    plate(S([(-0.7, 0.1), (0.7, 0.1), (0.5, -0.32), (-0.5, -0.32)]), 0.12 * s, (0, my, mz), mouth)
    if buck: bucks(0.1)
    else:
        for sx in (1, -1): plate(S([(-0.11, 0), (0.11, 0), (0, -0.24)]), 0.14 * s, (0.32 * s * sx, my - 0.05 * s, mz + 0.08 * s), teeth)
    _face("Mouth", ["Roar"])
    plate(S([(math.cos(a) * 0.62, math.sin(a) * 0.55 - 0.15) for a in [k * math.pi / 8 for k in range(16)]]), 0.12 * s, (0, my, mz), mouth)
    plate(S([(-0.36, -0.42), (0.36, -0.42), (0.22, -0.68), (-0.22, -0.68)]), 0.14 * s, (0, my - 0.04 * s, mz), tongue)
    if buck: bucks(0.32)
    else:
        for sx in (1, -1): plate(S([(-0.13, 0), (0.13, 0), (0, -0.3)]), 0.16 * s, (0.33 * s * sx, my - 0.06 * s, mz + 0.36 * s), teeth)
    _face("Mouth", ["Hurt"])
    plate(S([(-0.66, 0.12), (-0.33, 0.0), (0, 0.14), (0.33, 0.0), (0.66, 0.12), (0.62, -0.2), (-0.62, -0.2)]), 0.12 * s, (0, my, mz), mouth)
    plate(S([(-0.5, 0.03), (0.5, 0.03), (0.48, -0.1), (-0.48, -0.1)]), 0.14 * s, (0, my - 0.05 * s, mz), teeth)
    _face("Mouth", ["Dazed"])
    plate(S([(math.cos(a) * 0.28, math.sin(a) * 0.24) for a in [k * math.pi / 5 for k in range(10)]]), 0.12 * s, (0.1 * s, my, mz), mouth)
    plate(S([(-0.16, 0), (0.16, 0), (0.13, -0.32), (-0.13, -0.32)]), 0.14 * s, (0.22 * s, my - 0.05 * s, mz - 0.14 * s), tongue)
    CTX["face"] = None; smooth(False)

def normalize_height(target, bones):
    """scale every built part (and the joint spots) about the origin so the Boss is `target` studs tall"""
    top = 0.0
    for o in PARTS:
        for v in o.data.vertices: top = max(top, (o.matrix_world @ v.co).z)
    k = target / top
    for o in PARTS:
        for v in o.data.vertices: v.co = v.co * k
        o.location = o.location * k
    for i, b in enumerate(bones):
        bones[i] = (b[0], b[1], b[2] * k, b[3] * k, b[4] * k)
    return k

# ---------------- faces ----------------
def _face(slot, sets):
    CTX["bone"] = "Head"; CTX["face"] = f"{slot}_{'+'.join(sets)}"

def boss_faces(ex, ey, ez, my, mz, s=1.0, glow="EyeGlow", pupil="Pupil", mouth="Mouth", teeth="Teeth", tongue="Tongue", buck=False, eye_tilt=0.0):
    """The standard Boss face set (Grumpy, Angry, Hurt, Blink, Dazed, GlanceL/R eyes; Grumpy, Angry, Roar, Hurt,
    Dazed mouths). ex = eye distance from the centre, (ey, ez) eye front/height, (my, mz) mouth, s = scale."""
    S = lambda pts: [(x * s, z * s) for x, z in pts]
    def eyes(shape, pup=None):
        for sx in (1, -1):
            plate([(x * sx, z) for x, z in S(shape)], 0.14 * s, (ex * sx, ey, ez), glow, rot=(0, eye_tilt * sx, 0))
            if pup:
                p = [(-0.17, -0.17), (0.17, -0.17), (0.17, 0.17), (-0.17, 0.17)]
                plate(S([(x + pup[0], z + pup[1]) for x, z in p]), 0.08 * s, (ex * sx, ey - 0.1 * s, ez), pupil)
    lid = [(-0.62, -0.28), (0.58, -0.3), (0.65, 0.08), (-0.65, 0.34)]
    _face("Eyes", ["Grumpy"]); eyes(lid, (0, -0.04))
    _face("Eyes", ["GlanceL"]); eyes(lid, (0.3, -0.04))
    _face("Eyes", ["GlanceR"]); eyes(lid, (-0.3, -0.04))
    _face("Eyes", ["Angry"]); eyes([(-0.62, -0.32), (0.58, -0.32), (0.62, -0.08), (-0.66, 0.45)], (0, -0.1))
    _face("Eyes", ["Hurt"]); eyes([(-0.58, 0.32), (0.38, 0.02), (-0.58, -0.28), (-0.42, 0.02)])
    _face("Eyes", ["Blink"]); eyes([(-0.62, -0.08), (0.62, -0.08), (0.62, 0.07), (-0.62, 0.07)])
    _face("Eyes", ["Dazed"])
    for sx in (1, -1):
        loft([((ex * sx, ey + 0.07 * s, ez), 0.48 * s, 0.48 * s), ((ex * sx, ey - 0.07 * s, ez), 0.48 * s, 0.48 * s)], glow, sides=8, ref=(0, 0, 1))
        loft([((ex * sx, ey - 0.06 * s, ez), 0.3 * s, 0.3 * s), ((ex * sx, ey - 0.14 * s, ez), 0.3 * s, 0.3 * s)], pupil, sides=8, ref=(0, 0, 1))
        loft([((ex * sx, ey - 0.1 * s, ez), 0.13 * s, 0.13 * s), ((ex * sx, ey - 0.18 * s, ez), 0.13 * s, 0.13 * s)], glow, sides=6, ref=(0, 0, 1))
    def band(w, h, lo, thick, up):
        top, bot = [], []
        for i in range(9):
            t = -1 + i / 4; x = t * w / 2; z = h * (1 - t * t) * (1 if up else -1) + lo
            top.append((x, z + thick / 2)); bot.append((x, z - thick / 2))
        return top + bot[::-1]
    def bucks(dz=0.0):
        if buck:
            for sx in (1, -1): plate(S([(-0.2, 0), (0.2, 0), (0.2, -0.45), (-0.2, -0.45)]), 0.16 * s, (0.22 * s * sx, my - 0.07 * s, mz + (0.12 + dz) * s), teeth)
    _face("Mouth", ["Grumpy"])
    plate(S(band(1.8, 0.3, -0.12, 0.26, True)), 0.12 * s, (0, my, mz), mouth)
    if buck: bucks(0.02)
    else:
        for sx in (1, -1): plate(S([(-0.13, 0), (0.13, 0), (0, -0.32)]), 0.14 * s, (0.5 * s * sx, my - 0.05 * s, mz + 0.02 * s), teeth)
    _face("Mouth", ["Angry"])
    plate(S([(-0.95, 0.18), (0.95, 0.18), (0.75, -0.38), (-0.75, -0.38)]), 0.12 * s, (0, my, mz), mouth)
    for k in range(5): plate(S([(-0.16, 0), (0.16, 0), (0, -0.26)]), 0.14 * s, ((-0.64 + k * 0.32) * s, my - 0.05 * s, mz + 0.16 * s), teeth)
    _face("Mouth", ["Roar"])
    plate(S([(-1.0, 0.35), (1.0, 0.35), (0.8, -0.75), (0, -0.98), (-0.8, -0.75)]), 0.12 * s, (0, my, mz - 0.1 * s), mouth)
    plate(S([(-0.5, -0.5), (0.5, -0.5), (0.36, -0.86), (-0.36, -0.86)]), 0.14 * s, (0, my - 0.04 * s, mz - 0.1 * s), tongue)
    if buck: bucks(0.22)
    else:
        for sx in (1, -1): plate(S([(-0.19, 0), (0.19, 0), (0, -0.48)]), 0.16 * s, (0.62 * s * sx, my - 0.06 * s, mz + 0.25 * s), teeth)
    for sx in (1, -1): plate(S([(-0.15, 0), (0.15, 0), (0, 0.36)]), 0.16 * s, (0.46 * s * sx, my - 0.06 * s, mz - 0.86 * s), teeth)
    _face("Mouth", ["Hurt"])
    plate(S([(-0.9, 0.2), (-0.42, 0.05), (0, 0.22), (0.42, 0.05), (0.9, 0.2), (0.84, -0.26), (-0.84, -0.26)]), 0.12 * s, (0, my, mz), mouth)
    plate(S([(-0.72, 0.05), (0.72, 0.05), (0.7, -0.12), (-0.7, -0.12)]), 0.14 * s, (0, my - 0.05 * s, mz), teeth)
    _face("Mouth", ["Dazed"])
    plate(S([(math.cos(a) * 0.42, math.sin(a) * 0.34) for a in [k * math.pi / 5 for k in range(10)]]), 0.12 * s, (0.2 * s, my, mz - 0.05 * s), mouth)
    plate(S([(-0.23, 0), (0.23, 0), (0.19, -0.42), (-0.19, -0.42)]), 0.14 * s, (0.36 * s, my - 0.05 * s, mz - 0.22 * s), tongue)
    CTX["face"] = None

def pet_faces(ex, ey, ez, my, mz, s=1.0, eye="PetEye", shine="PetShine", mouth="Mouth", buck_col=None):
    S = lambda pts: [(x * s, z * s) for x, z in pts]
    CTX["bone"] = "Head"; CTX["face"] = "Eyes_Happy"
    for sx in (1, -1):
        plate(S([(-0.38, -0.45), (0.38, -0.45), (0.42, 0.38), (-0.42, 0.38)]), 0.14 * s, (ex * sx, ey, ez), eye)
        plate(S([(-0.12, -0.12), (0.12, -0.12), (0.12, 0.12), (-0.12, 0.12)]), 0.06 * s, (ex * sx + 0.14 * s, ey - 0.1 * s, ez + 0.16 * s), shine)
    CTX["face"] = "Eyes_Blink"
    for sx in (1, -1):
        plate(S([(-0.42, -0.04), (0, 0.16), (0.42, -0.04), (0.42, -0.18), (0, 0.02), (-0.42, -0.18)]), 0.14 * s, (ex * sx, ey, ez - 0.1 * s), eye)
    CTX["face"] = "Mouth_Happy"
    plate(S([(-0.42, 0.06), (0, -0.2), (0.42, 0.06), (0.42, -0.08), (0, -0.36), (-0.42, -0.08)]), 0.12 * s, (0, my, mz), mouth)
    if buck_col:
        plate(S([(-0.22, 0), (0.22, 0), (0.22, -0.32), (-0.22, -0.32)]), 0.12 * s, (0, my - 0.06 * s, mz - 0.18 * s), buck_col)
    CTX["face"] = None

# ---------------- finish / export / review ----------------
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
    return main_col

def anchor(prefix, x):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((x, 0, 0)))
    me = bpy.data.meshes.new(prefix + "__Anchor"); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(prefix + "__Anchor", me); bpy.context.collection.objects.link(o)
    o.hide_render = True

def build_all(n, boss_fn, faces_fn, pet_fn, height=None):
    """n = Boss number (2 -> B02 / P02). height = the Boss's real height (scaled after building).
    Writes bossNN_rig.json (bones, colours, main colours)."""
    bt, pt = f"B{n:02d}", f"P{n:02d}"
    clear(); BONES.clear(); PET_BONES.clear()
    CTX["ox"] = 0.0; CTX["face"] = None; boss_fn(); faces_fn()
    if height: normalize_height(height, BONES)
    bm = finish(bt); anchor(bt, 0)
    CTX["ox"] = PET_X; CTX["face"] = None; CTX["smooth"] = False; pet_fn(); pm = finish(pt); anchor(pt, PET_X)
    json.dump({"colors": COLORS, "boss_bones": BONES, "pet_bones": PET_BONES, "boss_main": bm, "pet_main": pm,
               "pet_x": PET_X, "expressions": BOSS_EXPRESSIONS, "pet_expressions": PET_EXPRESSIONS},
              open(os.path.join(BOSS_DIR, f"boss{n:02d}_rig.json"), "w"), indent=1)
    show_expression(bt, "Grumpy", "Grumpy"); show_expression(pt, "Happy", "Happy")

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

def review(n, height, face_target, pet_height):
    """front/back/face renders, all expressions, pet happy/blink/back -> renders/bNN_*.png, pNN_*.png"""
    bt, pt = f"B{n:02d}", f"P{n:02d}"
    k = height / 19.6
    shot(f"b{n:02d}_front34", (0, 0, height / 2), 46 * k, -0.55)
    shot(f"b{n:02d}_back34", (0, 0, height / 2), 46 * k, math.pi - 0.6)
    for name, (e, m) in BOSS_EXPRESSIONS.items():
        show_expression(bt, e, m)
        shot(f"b{n:02d}_expr_{name}", face_target, 14, -0.2, pitch=0.04, res=(420, 420))
    show_expression(bt, "Grumpy", "Grumpy")
    for name, (e, m) in PET_EXPRESSIONS.items():
        show_expression(pt, e, m)
        shot(f"p{n:02d}_{name}", (PET_X, 0, pet_height / 2), 26 * pet_height / 9.5, -0.5, pitch=0.12, res=(520, 600))
    show_expression(pt, "Happy", "Happy")
    shot(f"p{n:02d}_back", (PET_X, 0, pet_height / 2), 26 * pet_height / 9.5, math.pi - 0.6, pitch=0.12, res=(520, 600))

def export(n):
    for o in bpy.data.objects: o.hide_viewport = False; o.hide_set(False)
    bpy.ops.object.select_all(action="DESELECT")
    for o in bpy.data.objects:
        if o.type == "MESH" and (o.name.startswith(f"B{n:02d}__") or o.name.startswith(f"P{n:02d}__")): o.select_set(True)
    p = os.path.join(r"C:\obsidian\Roblox studio\Assets\Stations and Weapons", f"Boss{n:02d}.fbx")
    bpy.ops.export_scene.fbx(filepath=p, use_selection=True, apply_unit_scale=True, object_types={"MESH"}, mesh_smooth_type="FACE", add_leaf_bones=False)
    return p
