# Clone a Friend: Boss 1 "Brown Bear" (picnic grizzly) + its Pet, smooth cartoon look.
# Same rig as the original stud bear (Documents\CloneAFriendBosses\builds\B01Build.py / P01Build.py):
# same part names, same joint spots, same size, so every animation keeps working.
# Blender axes like StudLib: Left = +X, front = -Y, Z up, 1 unit = 1 stud. Pet is built at Y = +40 like the original.
# Objects: "<Tag>__<RigName>"; RigName = "<Part>" for the part's main colour, else "<Part>_<ColourName>".
# Run: ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\build_bear.py").read(), ns); ns["build_all"]()
import bpy, bmesh, math, json, os, random
from mathutils import Vector, Matrix, Euler

OUT = r"C:\obsidian\Roblox studio\Assets\Bosses"
PAL = {  # key: (rgb, Roblox colour name, glow)
    "fur": ((122, 82, 52), "Fur", 0), "furD": ((84, 54, 34), "FurDark", 0), "light": ((214, 172, 120), "Light", 0),
    "dark": ((30, 22, 22), "Dark", 0), "red": ((206, 46, 46), "Cape", 0), "white": ((250, 242, 228), "White", 0),
    "scar": ((150, 92, 78), "Scar", 0), "eye": ((255, 255, 255), "Eye", 0), "glow": ((255, 170, 40), "EyeGlow", 1),
    "honey": ((255, 170, 30), "Honey", 0), "belt": ((70, 44, 28), "Belt", 0), "gold": ((232, 180, 60), "Gold", 0),
    "wicker": ((214, 162, 92), "Wicker", 0), "wickerD": ((160, 112, 56), "WickerDark", 0), "bread": ((232, 172, 96), "Bread", 0),
    "crust": ((196, 132, 64), "Crust", 0), "bottle": ((70, 168, 106), "Bottle", 0), "metal": ((182, 190, 204), "Metal", 0),
    "metalD": ((120, 128, 144), "MetalDark", 0), "wood": ((150, 98, 56), "Wood", 0), "pad": ((60, 40, 32), "Pad", 0),
    "ear": ((220, 140, 112), "EarInner", 0), "claw": ((246, 236, 214), "Claw", 0), "mouth": ((70, 24, 30), "Mouth", 0),
    "tongue": ((214, 92, 104), "Tongue", 0), "sausage": ((178, 82, 58), "Sausage", 0), "string": ((240, 222, 186), "String", 0),
    "meat": ((150, 78, 40), "Meat", 0), "bone": ((250, 240, 222), "Bone", 0),
}
MAIN = {"Body": "fur", "Head": "fur", "LeftUpperArm": "fur", "RightUpperArm": "fur", "LeftLowerArm": "furD",
        "RightLowerArm": "furD", "LeftHand": "furD", "RightHand": "furD", "LeftLeg": "furD", "RightLeg": "furD"}
PET_MAIN = {"Body": "fur", "Head": "fur"}

STATE = {"tag": "B01", "main": MAIN, "off": Vector((0, 0, 0))}
ITEMS = []  # (part, col, obj)

def clear():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)

def mat(col):
    m = bpy.data.materials.get(col)
    if m: return m
    m = bpy.data.materials.new(col); m.use_nodes = True
    rgb = [c / 255 for c in PAL[col][0]]; lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*lin, 1); b.inputs["Roughness"].default_value = 0.5 if col not in ("honey", "metal", "metalD", "bottle", "dark") else 0.2
    m.diffuse_color = (*lin, 1); return m

def V(p): return Vector(p) + STATE["off"]

def _add(part, col, o, smooth=True, bevel=0.0, seg=2, ang=60):
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if bevel > 0:
        b = o.modifiers.new("b", "BEVEL"); b.width = bevel; b.segments = seg; b.limit_method = "ANGLE"
        bpy.ops.object.modifier_apply(modifier=b.name)
    if smooth: bpy.ops.object.shade_auto_smooth(angle=math.radians(ang))
    o.data.materials.clear(); o.data.materials.append(mat(col))
    ITEMS.append((part, col, o)); return o

def ell(part, col, c, r, rot=(0, 0, 0), seg=20, ring=12, lumps=0.0, seed=0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=1, location=V(c))
    o = bpy.context.object
    if lumps:
        rng = random.Random(seed)
        for v in o.data.vertices: v.co *= 1 + lumps * (rng.random() - 0.5)
    o.scale = r; o.rotation_euler = [math.radians(a) for a in rot]
    return _add(part, col, o, ang=80)

def _superify(o, sq, taper):
    """push a unit sphere's vertices towards a rounded box (sq 0 = sphere, ~0.6 = chunky block) and taper it:
    taper = (scale at the bottom, scale at the top) for x/y, along local z"""
    e = max(0.2, 1.0 - sq)
    for v in o.data.vertices:
        x, y, z = v.co
        x = math.copysign(abs(x) ** e, x); y = math.copysign(abs(y) ** e, y); z = math.copysign(abs(z) ** e, z)
        k = taper[0] + (taper[1] - taper[0]) * (z + 1) / 2
        v.co = Vector((x * k, y * k, z))

def blk(part, col, c, r, rot=(0, 0, 0), sq=0.55, taper=(1, 1), seg=24, ring=16):
    """chunky sculpted block: a superellipsoid with flatter planes and crisper edges than ell()"""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=1, location=V(c))
    o = bpy.context.object; _superify(o, sq, taper)
    o.scale = r; o.rotation_euler = [math.radians(a) for a in rot]
    return _add(part, col, o, ang=38)

def limb(part, col, p0, p1, w0, w1, sq=0.5, flat=1.0, seg=20, ring=14):
    """tapered block running from p0 (width w0) to p1 (width w1); flat < 1 squashes it front-to-back"""
    a, b = V(p0), V(p1); d = b - a
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=1, location=(a + b) / 2)
    o = bpy.context.object
    wmax = max(w0, w1)
    _superify(o, sq, (w0 / wmax, w1 / wmax))
    o.scale = (wmax, wmax * flat, d.length / 2 + (w0 + w1) * 0.22)
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    return _add(part, col, o, ang=38)

def cap(part, col, p0, p1, r0, r1=None, verts=16):
    """capsule / tapered tube between two points"""
    r1 = r0 if r1 is None else r1
    a, b = V(p0), V(p1); d = b - a
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r0, radius2=r1, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    _add(part, col, o, ang=80)
    for p, r in ((a, r0), (b, r1)):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=verts, ring_count=max(6, verts // 2), radius=r, location=p)
        _add(part, col, bpy.context.object, ang=80)

def tube(part, col, pts, r, verts=8):
    for p0, p1 in zip(pts[:-1], pts[1:]): cap(part, col, p0, p1, r, r, verts)

def cone(part, col, base, tip, r, verts=10):
    a, b = V(base), V(tip); d = b - a
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=0, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    return _add(part, col, o, ang=50)

def box(part, col, c, s, rot=(0, 0, 0), bevel=0.2, seg=3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=V(c)); o = bpy.context.object
    o.scale = s; o.rotation_euler = [math.radians(a) for a in rot]
    return _add(part, col, o, bevel=min(bevel, min(s) / 2.2), seg=seg, ang=40)

def cyl(part, col, c, r, h, rot=(0, 0, 0), verts=20, bevel=0.1):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=V(c)); o = bpy.context.object
    o.rotation_euler = [math.radians(a) for a in rot]
    return _add(part, col, o, bevel=min(bevel, r / 2, h / 2.2), ang=40)

def sheet(part, cols, centre, rx, ry, a0, a1, z0, z1, nu, nv, thick=0.25, flare=0.0, wave=0.0):
    """curved checker sheet around a vertical axis (cape). Cells alternate between cols."""
    for i in range(nu):
        for j in range(nv):
            col = cols[(i + j) % len(cols)]
            bm = bmesh.new(); grid = []
            for di in range(3):
                row = []
                for dj in range(3):
                    u = a0 + (a1 - a0) * (i + di / 2) / nu; t = (j + dj / 2) / nv
                    z = z1 - (z1 - z0) * t + (wave * math.sin(u * 5) if j + dj / 2 >= nv - 0.01 else 0)
                    k = 1 + flare * t
                    row.append(Vector((centre[0] + rx * k * math.cos(u), centre[1] + ry * k * math.sin(u), z)))
                grid.append(row)
            vs = [[bm.verts.new(p + STATE["off"]) for p in row] for row in grid]
            for a in range(2):
                for b in range(2):
                    bm.faces.new([vs[a][b], vs[a + 1][b], vs[a + 1][b + 1], vs[a][b + 1]])
            me = bpy.data.meshes.new("s"); bm.to_mesh(me); o = bpy.data.objects.new("s", me); bpy.context.collection.objects.link(o)
            s = o.modifiers.new("s", "SOLIDIFY"); s.thickness = thick; s.offset = 1
            bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.modifier_apply(modifier="s")
            _add(part, col, o, ang=60)

def tri(part, col, pts_xz, y, thick=0.25):
    """flat shape in the x/z plane at depth y (bandana)"""
    bm = bmesh.new(); vs = [bm.verts.new(V((x, y, z))) for x, z in pts_xz]
    f = bm.faces.new(vs); r = bmesh.ops.extrude_face_region(bm, geom=[f])
    for v in [e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)]: v.co.y -= thick
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("t"); bm.to_mesh(me); o = bpy.data.objects.new("t", me); bpy.context.collection.objects.link(o)
    return _add(part, col, o, bevel=0.08, seg=2, ang=40)

def mirror(fn, part, col, *args, npts=1, **kw):
    """call fn for a Left part and its mirrored Right twin; the first npts args are points (x gets flipped)"""
    fn(part, col, *args, **kw)
    flipped = [(-a[0], a[1], a[2]) if i < npts else a for i, a in enumerate(args)]
    fn(part.replace("Left", "Right"), col, *flipped, **kw)

def finish():
    groups = {}
    for part, col, o in ITEMS: groups.setdefault((part, col), []).append(o)
    made = {}
    for (part, col), objs in groups.items():
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs: o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        if len(objs) > 1: bpy.ops.object.join()
        j = bpy.context.object
        name = part if STATE["main"].get(part) == col else f"{part}_{PAL[col][1]}"
        j.name = j.data.name = f"{STATE['tag']}__{name}"
        bpy.context.scene.cursor.location = (0, 0, 0); bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        made[name] = list(PAL[col][0]) + [PAL[col][2]]
    ITEMS.clear(); return made

# =====================================================================================
# ---------- surface helpers: place straps / cape / scars on the real body surface ----------
from mathutils.bvhtree import BVHTree

def skin(filter_fn):
    """BVH of the pieces built so far that pass filter_fn(part, col)"""
    verts, polys = [], []
    for part, col, o in ITEMS:
        if not filter_fn(part, col): continue
        base = len(verts); mw = o.matrix_world
        verts += [mw @ v.co for v in o.data.vertices]
        polys += [[base + i for i in p.vertices] for p in o.data.polygons]
    return BVHTree.FromPolygons(verts, polys)

def project(bvh, origin, target, off):
    """outermost surface point on the ray from origin through target, pushed out by off along the normal"""
    o, t = V(origin), V(target); d = (t - o).normalized()
    hit = bvh.ray_cast(o + d * 40, -d)
    if hit[0] is None: return None
    n = hit[1] if hit[1].dot(d) > 0 else -hit[1]
    return hit[0] + n * off - STATE["off"]

def resample(pts, step):
    pts = [Vector(p) for p in pts]
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int((b - a).length / step))
        for k in range(1, n + 1): out.append(a.lerp(b, k / n))
    return out

def surface_sheet(part, cols, bvh, axis_y, a0, a1, z_top, z_bot, nu, nv, off=0.14, flare=0.35, thick=0.2, tear=0.0, seed=1):
    """one continuous curved sheet hugging the body (cape), checker-split into cols without overlaps"""
    rng = random.Random(seed)
    grid = []
    for j in range(nv * 2 + 1):
        t = j / (nv * 2); row = []
        for i in range(nu * 2 + 1):
            u = a0 + (a1 - a0) * i / (nu * 2)
            z = z_top - (z_top - z_bot) * t
            if j == nv * 2 and tear: z += (tear if i % 2 else -tear * 0.6) + rng.uniform(-tear, tear) * 0.4
            d = Vector((math.cos(u), math.sin(u), 0))
            p = project(bvh, (0, axis_y, z), (d.x * 3, axis_y + d.y * 3, z), off + flare * t)
            row.append(p if p is not None else Vector((d.x * 5, axis_y + d.y * 5, z)))
        grid.append(row)
    for ci, col in enumerate(cols):
        bm = bmesh.new(); vmap = {}
        def vert(j, i):
            if (j, i) not in vmap: vmap[(j, i)] = bm.verts.new(grid[j][i] + STATE["off"])
            return vmap[(j, i)]
        for cj in range(nv):
            for cu in range(nu):
                if (cu + cj) % len(cols) != ci: continue
                for j in range(cj * 2, cj * 2 + 2):
                    for i in range(cu * 2, cu * 2 + 2):
                        bm.faces.new([vert(j, i), vert(j, i + 1), vert(j + 1, i + 1), vert(j + 1, i)])
        me = bpy.data.meshes.new("c"); bm.to_mesh(me); o = bpy.data.objects.new("c", me); bpy.context.collection.objects.link(o)
        s = o.modifiers.new("s", "SOLIDIFY"); s.thickness = thick; s.offset = 0
        bpy.context.view_layer.objects.active = o; o.select_set(True); bpy.ops.object.modifier_apply(modifier="s")
        _add(part, col, o, ang=50)
    return grid

def along(pts):
    """arc-length sampler over a polyline: returns (total length, f(s) -> point)"""
    acc, total = [], 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        acc.append((total, a, b)); total += (b - a).length
    def at(s):
        for t0, a, b in acc:
            l = (b - a).length
            if l > 0 and s <= t0 + l: return a.lerp(b, (s - t0) / l)
        return pts[-1]
    return total, at

def bear():
    STATE.update(tag="B01", main=MAIN, off=Vector((0, 0, 0)))
    body_skin = lambda part, col: part == "Body" and col in ("fur", "furD", "light")
    # ---------- legs: short, thick, big clawed feet ----------
    mirror(blk, "LeftLeg", "furD", (2.6, 0.1, 3.2), (2.0, 2.0, 1.95), sq=0.5, taper=(0.8, 1.0))
    mirror(blk, "LeftLeg", "furD", (2.6, -0.9, 0.8), (1.85, 2.55, 0.8), sq=0.65, taper=(1.0, 0.85))
    for k in range(7):  # shaggy fur shards over the ankle
        a = k * 2 * math.pi / 7 + 0.3
        mirror(cone, "LeftLeg", "fur", (2.6 + 1.2 * math.cos(a), 0.1 + 1.2 * math.sin(a), 2.3), (2.6 + 2.0 * math.cos(a), 0.1 + 2.0 * math.sin(a), 1.35), 0.6, verts=4, npts=2)
    for dx in (-0.95, 0, 0.95):
        mirror(cone, "LeftLeg", "claw", (2.6 + dx, -3.0, 0.6), (2.6 + dx * 1.15, -4.2, 0.2), 0.34, npts=2)
    # ---------- body: broad chest, heavy shoulders, narrow belly, hunched back ----------
    blk("Body", "fur", (0, 0.1, 10.0), (5.1, 3.8, 3.5), rot=(12, 0, 0), sq=0.55, taper=(0.78, 1.0))
    blk("Body", "fur", (0, -0.2, 6.7), (3.95, 3.35, 2.8), sq=0.45, taper=(0.92, 1.0))
    for s in (-1, 1):
        blk("Body", "fur", (s * 3.5, 0.5, 11.8), (2.1, 2.3, 1.6), sq=0.5)
        blk("Body", "fur", (s * 1.9, -2.75, 10.7), (1.85, 1.0, 1.25), rot=(12, 0, s * -8), sq=0.55)   # pecs
    blk("Body", "fur", (0, 1.7, 12.0), (3.4, 2.5, 2.1), sq=0.45)
    blk("Body", "light", (0, -2.85, 7.2), (2.7, 0.85, 2.5), sq=0.6, taper=(0.85, 1.0))
    for k in range(5):  # chest fluff
        x = -1.6 + 0.8 * k
        cone("Body", "light", (x, -3.35, 10.2 - 0.15 * abs(k - 2)), (x * 1.05, -3.7, 9.0 - 0.2 * abs(k - 2)), 0.5, verts=4)
    for k in range(9):  # spiky mane along the back of the neck and shoulders
        a = math.radians(25 + k * 16.25)
        base = (2.9 * math.cos(a), 1.6 + 1.9 * math.sin(a), 13.1)
        tip = (4.0 * math.cos(a), 2.2 + 3.0 * math.sin(a), 14.6 + 0.5 * math.sin(a))
        cone("Body", "furD", base, tip, 0.8, verts=4)
    bvh = skin(body_skin)
    # claw scars across the left chest (lying on the surface)
    for k in range(3):
        a = (-1.0 - 0.55 * k, -3, 11.6 - 0.25 * k); b = (-2.4 - 0.55 * k, -3, 9.2 - 0.25 * k)
        pts = [project(bvh, (0, 0.2, 9.5), tuple(p), 0.02) for p in resample([a, b], 0.45)]
        tube("Body", "scar", [tuple(p) for p in pts if p], 0.13, 6)
    # tattered checkered cape hugging the back (one continuous surface)
    cape_skin = skin(lambda part, col: part == "Body" and col in ("fur", "furD"))
    surface_sheet("Body", ["red", "white"], cape_skin, 0.4, math.radians(38), math.radians(142), 12.9, 7.4, 6, 4, off=0.12, flare=0.35, tear=0.45, seed=4)
    bvh = skin(lambda part, col: part == "Body" and col in ("fur", "furD", "light", "red", "white"))
    # belt (ring projected onto the belly) + buckle
    ring = [project(bvh, (0, -0.2, 5.8), (math.cos(a) * 3, -0.2 + math.sin(a) * 3, 5.8), 0.24) for a in [k * 2 * math.pi / 28 for k in range(29)]]
    tube("Body", "belt", [tuple(p) for p in ring if p], 0.32, 8)
    front = project(bvh, (0, -0.2, 5.8), (0, -3, 5.8), 0.5)
    box("Body", "gold", tuple(front), (1.5, 0.35, 1.15), bevel=0.15)
    box("Body", "belt", tuple(front + Vector((0, -0.2, 0))), (0.8, 0.12, 0.55), bevel=0.05)
    # honey jar hanging off the belt, front-left
    a = math.radians(90)
    hp = Vector(project(bvh, (0, -0.2, 5.8), (math.cos(a) * 3, -0.2 + math.sin(a) * 3, 5.8), 1.15)) + Vector((0, 0, -1.2))
    cyl("Body", "honey", tuple(hp), 0.92, 1.6, verts=20, bevel=0.25)
    cyl("Body", "red", tuple(hp + Vector((0, 0, 0.93))), 1.0, 0.28, verts=20, bevel=0.1)
    cyl("Body", "light", tuple(hp + Vector((0, 0, -0.1))), 0.94, 0.55, verts=20, bevel=0.04)
    out = Vector((math.cos(a), math.sin(a), 0))
    tube("Body", "honey", [tuple(hp + out * 0.9 + Vector((0, 0, -0.35))), tuple(hp + out * 0.93 + Vector((0, 0, -1.0)))], 0.12, 8)
    # sausage garland swagged across the front of the belt (hangs under the belly, clear of head, arms and thighs)
    sausage_pts = []
    swag = []
    for k in range(13):
        t = k / 12
        a = math.radians(-58 - 64 * t)
        p = project(bvh, (0, -0.2, 5.8), (math.cos(a) * 3, -0.2 + math.sin(a) * 3, 5.8), 0.75)
        if p: swag.append(Vector(p) + Vector((0, -0.25 * math.sin(math.pi * t), -1.3 * math.sin(math.pi * t))))
    total, at = along(swag)
    s = 0.0
    while s + 1.0 < total:
        cap("Body", "sausage", tuple(at(s + 0.08)), tuple(at(s + 0.92)), 0.4, verts=12)
        ell("Body", "string", tuple(at(s + 1.0)), (0.2, 0.2, 0.2), seg=8, ring=5)
        sausage_pts += [at(s + 0.5)]
        s += 1.08
    for p in (swag[0], swag[-1]):   # tied to the belt
        ell("Body", "string", tuple(p + Vector((0, 0, 0.3))), (0.32, 0.32, 0.32), seg=10, ring=6)
    # crumbs sitting on the belly
    rng = random.Random(3)
    for k in range(5):
        p = project(bvh, (0, 0, 7.2), (rng.uniform(-2, 2), -3, rng.uniform(6.8, 9.2)), 0.08)
        if p and all((p - q).length > 1.1 for q in sausage_pts): box("Body", "bread", tuple(p), (0.32, 0.22, 0.26), (rng.uniform(0, 40), rng.uniform(0, 40), rng.uniform(0, 90)), bevel=0.06, seg=1)
    # open picnic basket strapped flat against the back, centred on the spine, following the slope of the back
    zc = 9.4
    hit = bvh.ray_cast(Vector((0, 30, zc)), Vector((0, -1, 0)))
    bp, bn = hit[0], (hit[1] if hit[1].y > 0 else -hit[1])
    up = (Vector((0, 0, 1)) - bn * bn.z).normalized()
    side = bn.cross(up).normalized()
    M = Matrix.Translation(bp + bn * 1.28) @ Matrix((side, bn, up)).transposed().to_4x4()
    first = len(ITEMS)
    box("Body", "wicker", (0, 0, 0), (4.6, 2.4, 3.0), bevel=0.4)
    for z in (-0.9, 0.0): box("Body", "wickerD", (0, 0, z), (4.68, 2.48, 0.26), bevel=0.1)
    for x in (-1.4, 0, 1.4): box("Body", "wickerD", (x, 1.22, 0), (0.26, 0.1, 3.0), bevel=0.04)
    for (cx, cy, sx, sy) in ((0, -1.2, 4.8, 0.32), (0, 1.2, 4.8, 0.32), (-2.3, 0, 0.32, 2.6), (2.3, 0, 0.32, 2.6)):
        box("Body", "wickerD", (cx, cy, 1.55), (sx, sy, 0.32), bevel=0.1)
    tube("Body", "wickerD", [(-2.0, 0.3, 1.7), (-1.3, 0.3, 3.1), (1.3, 0.3, 3.1), (2.0, 0.3, 1.7)], 0.16, 8)
    ell("Body", "red", (0.6, -0.2, 1.55), (1.3, 0.9, 0.35))
    b0, b1 = Vector((-0.8, -0.35, 1.0)), Vector((-1.6, 0.35, 3.7))
    cap("Body", "bread", tuple(b0), tuple(b1), 0.45, 0.4, verts=12)
    for t in (0.45, 0.65, 0.85):
        p = b0.lerp(b1, t)
        box("Body", "crust", (p.x + 0.05, p.y - 0.4, p.z), (0.7, 0.12, 0.15), (0, -35, 20), bevel=0.04)
    cyl("Body", "bottle", (1.0, 0.68, 1.9), 0.45, 2.0, verts=14, bevel=0.15)
    cap("Body", "bottle", (1.0, 0.68, 2.9), (1.0, 0.68, 3.7), 0.34, 0.2, verts=12)
    cyl("Body", "red", (1.0, 0.68, 3.85), 0.24, 0.28, verts=12, bevel=0.06)
    for part, col, o in ITEMS[first:]:
        o.matrix_world = M @ o.matrix_world
    # harness: top corners up to a buckle on the upper back, bottom corners down to the belt
    W = lambda v: M @ Vector(v)
    buckle = project(bvh, (0, 0.5, 12.2), (0, 5, 12.4), 0.2)
    for sgn in (-1, 1):
        top = W((sgn * 2.25, -1.2, 1.45))
        mid = project(bvh, (0, 0.5, 11.4), (sgn * 1.3, 5, 11.6), 0.2)
        tube("Body", "belt", [tuple(top), tuple(mid), tuple(buckle)], 0.18, 8)
        bot = W((sgn * 1.9, -1.15, -1.45))
        low = project(bvh, (0, 0, 6.8), (sgn * 1.9, 5, 6.8), 0.2)
        at_belt = project(bvh, (0, -0.2, 5.8), (sgn * 2.0, 5, 5.8), 0.45)
        tube("Body", "belt", [tuple(bot), tuple(low), tuple(at_belt)], 0.18, 8)
        box("Body", "gold", tuple(at_belt), (0.5, 0.3, 0.5), bevel=0.1)
    box("Body", "gold", tuple(buckle), (0.8, 0.3, 0.7), bevel=0.12)
    STATE["off"] = Vector((0, -0.3, 0.55))   # head geometry offset (the neck joint itself does not move)
    # ---------- head: low, forward, snarling (neck joint stays at 0,-1.6,12.8) ----------
    blk("Head", "fur", (0, -2.7, 15.0), (3.25, 2.85, 2.7), sq=0.5, taper=(1.0, 0.86))
    for s in (-1, 1):
        blk("Head", "fur", (s * 2.8, -3.4, 14.0), (1.3, 1.25, 1.15), sq=0.45)
        for k in range(3):
            cone("Head", "fur", (s * 3.4, -3.0 + 0.7 * (k - 1), 14.5 - 0.35 * k), (s * 4.8, -2.4 + 0.9 * (k - 1), 14.2 - 0.35 * k), 0.55, verts=4)
        blk("Head", "fur", (s * 1.35, -4.85, 16.25), (1.45, 0.75, 0.5), rot=(0, s * -18, s * 8), sq=0.65)       # heavy brow
        ell("Head", "glow", (s * 1.2, -5.1, 15.55), (0.6, 0.28, 0.32), rot=(0, s * -16, 0), seg=14, ring=8)
        ell("Head", "dark", (s * 1.1, -5.33, 15.55), (0.13, 0.08, 0.3), seg=10, ring=6)
        blk("Head", "fur", (s * 2.55, -2.1, 17.25), (1.1, 0.7, 1.1), sq=0.35)
        ell("Head", "ear", (s * 2.55, -2.75, 17.25), (0.62, 0.22, 0.62), seg=12, ring=8)
    blk("Head", "light", (0, -5.5, 14.35), (1.9, 1.7, 1.1), sq=0.6, taper=(1.0, 0.82))          # upper muzzle
    blk("Head", "light", (0, -5.0, 12.95), (1.65, 1.5, 0.7), sq=0.65)          # lower jaw, dropped open
    ell("Head", "mouth", (0, -5.75, 13.55), (1.3, 1.0, 0.42))          # dark mouth inside
    ell("Head", "tongue", (0, -5.75, 13.25), (0.8, 0.8, 0.22), seg=12, ring=8)
    ell("Head", "dark", (0, -7.05, 14.75), (0.95, 0.6, 0.6))
    ell("Head", "white", (0.3, -7.5, 15.0), (0.22, 0.1, 0.14), seg=8, ring=5)
    for s in (-1, 1):
        cone("Head", "white", (s * 0.85, -6.5, 13.85), (s * 0.9, -6.55, 12.95), 0.27, verts=10)   # big fangs
        cone("Head", "white", (s * 1.15, -6.15, 12.9), (s * 1.18, -6.3, 13.55), 0.2, verts=8)     # lower fangs
        cone("Head", "white", (s * 0.4, -6.62, 13.9), (s * 0.42, -6.68, 13.5), 0.14, verts=8)
    tube("Head", "honey", [(-0.9, -6.55, 13.0), (-0.92, -6.55, 12.35)], 0.11, 8)
    ell("Head", "honey", (-0.92, -6.55, 12.22), (0.18, 0.18, 0.24), seg=10, ring=6)
    for k in range(4): cone("Head", "furD", (-0.9 + 0.6 * k, -2.6, 17.5), (-1.2 + 0.8 * k, -2.4 + 0.3 * k, 18.7 - 0.15 * abs(k - 1.5)), 0.5, verts=4)
    head_bvh = skin(lambda part, col: part == "Head" and col in ("fur", "light"))
    sp = [project(head_bvh, (0, -2.5, 15.2), (2.0 + 0.35 * t, -5, 17.4 - 3.0 * t), 0.03) for t in (0, 0.25, 0.5, 0.75, 1.0)]
    tube("Head", "scar", [tuple(p) for p in sp if p], 0.12, 6)
    for t in (1, 2, 3):
        if sp[t]: box("Head", "scar", tuple(sp[t]), (0.5, 0.12, 0.1), (0, 20, 0), bevel=0.03)
    box("Head", "white", (2.55, -2.95, 17.3), (1.1, 0.1, 0.32), (0, 35, 0), bevel=0.05)   # bandage on the left ear
    box("Head", "white", (2.55, -2.95, 17.3), (1.1, 0.1, 0.32), (0, -35, 0), bevel=0.05)
    STATE["off"] = Vector((0, 0, 0))
    # ---------- arms: heavy shoulders, huge forearms, big paws ----------
    mirror(limb, "LeftUpperArm", "fur", (5.0, 0.0, 11.9), (6.2, -0.3, 9.0), 1.75, 1.45, sq=0.5, npts=2)
    for k in range(3):
        mirror(cone, "LeftUpperArm", "fur", (6.4, 0.6 + 0.5 * (k - 1), 9.4 + 0.5 * k), (7.7, 1.3 + 0.7 * (k - 1), 8.9 + 0.6 * k), 0.5, verts=4, npts=2)
    for s, part in ((1, "LeftUpperArm"), (-1, "RightUpperArm")):   # pie-tin pauldrons
        c = Vector((s * 6.05, -0.1, 13.55)); R = Euler((0, math.radians(s * 40), 0)).to_matrix()
        bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=2.25, radius2=1.2, depth=0.8, location=c)
        o = bpy.context.object; o.rotation_euler = (0, math.radians(s * 40), 0); _add(part, "metal", o, bevel=0.12, ang=40)
        rim = [c + R @ Vector((2.3 * math.cos(a), 2.3 * math.sin(a), -0.38)) for a in [k * 2 * math.pi / 24 for k in range(25)]]
        tube(part, "metalD", [tuple(p) for p in rim], 0.16, 6)
        for k in range(10):
            a = k * 2 * math.pi / 10
            ell(part, "metalD", tuple(c + R @ Vector((1.75 * math.cos(a), 1.75 * math.sin(a), 0.05))), (0.12, 0.12, 0.12), seg=6, ring=4)
    mirror(limb, "LeftLowerArm", "furD", (6.3, -0.2, 8.4), (6.4, -0.5, 6.0), 1.5, 1.8, sq=0.5, npts=2)
    mirror(cyl, "LeftLowerArm", "belt", (6.4, -0.45, 6.6), 1.85, 0.75, verts=20, bevel=0.15)
    mirror(cyl, "LeftLowerArm", "belt", (6.38, -0.4, 7.35), 1.75, 0.45, verts=20, bevel=0.12)
    mirror(blk, "LeftHand", "furD", (6.4, -0.9, 4.25), (1.85, 1.95, 1.45), sq=0.55, taper=(0.9, 1.0))
    for dx in (-0.9, 0, 0.9):
        mirror(blk, "LeftHand", "furD", (6.4 + dx, -2.5, 4.1), (0.55, 0.5, 0.62), sq=0.5, seg=14, ring=10)
    mirror(ell, "LeftHand", "pad", (6.4, -2.65, 3.45), (0.95, 0.3, 0.55), seg=12, ring=8)
    for dx in (-1.0, -0.33, 0.33, 1.0):
        cone("LeftHand", "claw", (6.4 + dx, -2.6, 3.25), (6.4 + dx * 1.15, -3.7, 2.1), 0.3, verts=8)
    for dx in (-1.2, 1.2):
        cone("RightHand", "claw", (-6.4 + dx, -2.5, 3.3), (-6.4 + dx * 1.15, -3.5, 2.2), 0.3, verts=8)
    cap("LeftHand", "honey", (6.75, -3.2, 2.6), (6.78, -3.25, 2.0), 0.1, verts=8)
    # the battle fork in the right paw, held in front of the arm (Right = -X)
    f0, f1 = Vector((-6.45, -2.35, 0.4)), Vector((-6.85, -3.75, 14.2))
    cap("RightHand", "wood", tuple(f0), tuple(f1), 0.38, 0.34, verts=12)
    d = (f1 - f0).normalized()
    for t in (1.2, 1.7, 2.2): cyl("RightHand", "belt", tuple(f0 + d * t), 0.46, 0.38, verts=12, bevel=0.08)
    cyl("RightHand", "gold", tuple(f0), 0.46, 0.35, verts=12, bevel=0.08)
    head = f1 + d * 0.4
    cap("RightHand", "metal", tuple(f1 - d * 0.2), tuple(head), 0.5, 0.46, verts=14)
    tilt = -math.degrees(math.atan2(-d.y, d.z))
    box("RightHand", "metal", tuple(head + d * 0.35), (3.2, 0.5, 0.65), rot=(tilt, 0, 0), bevel=0.22)
    for k in range(4):
        b = head + d * 0.5 + Vector((-1.2 + k * 0.8, 0, 0))
        bend = Vector((0.35, 0, 0)) if k == 3 else Vector((0, 0, 0))
        t = b + d * 2.6 + bend
        cap("RightHand", "metal", tuple(b), tuple(t), 0.18, 0.16, verts=8)
        cone("RightHand", "metal", tuple(t), tuple(t + d * 0.8 + bend * 0.5), 0.16, verts=8)
    mid = head + d * 1.9 + Vector((-0.3, -0.05, 0))      # skewered drumstick on the tines
    ell("RightHand", "meat", tuple(mid), (1.15, 0.95, 0.85), rot=(0, 20, 0))
    cap("RightHand", "bone", tuple(mid + Vector((0.9, 0, -0.4))), tuple(mid + Vector((2.0, 0, -0.9))), 0.22, verts=10)
    for dz in (-0.18, 0.18): ell("RightHand", "bone", tuple(mid + Vector((2.1, 0, -0.95 + dz))), (0.28, 0.28, 0.28), seg=10, ring=6)
    return finish()

def pet():
    STATE.update(tag="P01", main=PET_MAIN, off=Vector((0, 40, 0)))
    ell("Body", "fur", (0, 0, 3.0), (2.5, 2.0, 2.15))
    ell("Body", "light", (0, -1.75, 2.9), (1.5, 0.5, 1.45))
    for s in (-1, 1):
        ell("Body", "furD", (s * 1.35, -0.5, 0.65), (0.9, 1.15, 0.62))
        for dx in (-0.35, 0, 0.35): cone("Body", "claw", (s * 1.35 + dx, -1.5, 0.45), (s * 1.35 + dx, -1.85, 0.3), 0.13, verts=6)
        ell("Body", "furD", (s * 2.4, -0.9, 3.2), (0.75, 0.8, 1.15), rot=(0, s * -25, 0))
    # tiny honey jar hugged on the belly
    cyl("Body", "honey", (0, -2.2, 2.6), 0.7, 1.15, verts=16, bevel=0.2)
    cyl("Body", "red", (0, -2.2, 3.28), 0.78, 0.22, verts=16, bevel=0.08)
    ell("Body", "light", (0, -2.85, 2.6), (0.45, 0.08, 0.35), seg=10, ring=6)
    # mini checkered cape + bandana
    sheet("Body", ["red", "white"], (0, 0.1), 2.6, 2.15, math.radians(20), math.radians(160), 1.6, 4.9, 4, 3, thick=0.2, flare=0.1, wave=0.12)
    tri("Body", "red", [(-1.6, 5.0), (1.6, 5.0), (0, 3.7)], -1.85, thick=0.2)
    ell("Body", "white", (0, -2.07, 4.6), (0.18, 0.08, 0.18), seg=8, ring=5)
    # big head
    ell("Head", "fur", (0, -0.4, 8.2), (3.5, 3.05, 3.0))
    for s in (-1, 1):
        ell("Head", "fur", (s * 2.9, -1.2, 7.2), (1.2, 1.1, 1.05))
        ell("Head", "fur", (s * 2.4, -0.2, 11.0), (1.0, 0.7, 1.0))
        ell("Head", "ear", (s * 2.4, -0.8, 11.0), (0.55, 0.2, 0.55), seg=12, ring=8)
        ell("Head", "eye", (s * 1.45, -3.0, 8.85), (0.8, 0.4, 0.9))
        ell("Head", "dark", (s * 1.35, -3.35, 8.75), (0.52, 0.18, 0.6), seg=12, ring=8)
        ell("Head", "white", (s * 1.15, -3.5, 9.05), (0.17, 0.06, 0.17), seg=8, ring=5)
        cap("Head", "dark", (s * 2.35, -3.0, 10.1), (s * 0.7, -3.4, 9.75), 0.2, 0.16, verts=10)
    ell("Head", "light", (0, -3.25, 7.2), (1.5, 1.0, 1.0))
    ell("Head", "dark", (0, -4.15, 7.65), (0.6, 0.35, 0.42))
    ell("Head", "white", (0.2, -4.45, 7.82), (0.14, 0.06, 0.09), seg=8, ring=5)
    tube("Head", "dark", [(-0.6, -4.05, 6.75), (0, -4.2, 6.95), (0.6, -4.05, 6.75)], 0.09, 8)
    cap("Head", "scar", (1.9, -3.05, 10.3), (1.1, -3.4, 8.2), 0.1, verts=8)
    tube("Head", "honey", [(0.6, -4.0, 6.75), (0.62, -3.95, 6.3)], 0.1, 8); ell("Head", "honey", (0.62, -3.95, 6.2), (0.16, 0.16, 0.2), seg=10, ring=6)
    for k in range(3): cone("Head", "furD", (-0.4 + 0.4 * k, -0.4, 11.0), (-0.55 + 0.55 * k, -0.6, 11.8 - 0.1 * abs(k - 1)), 0.32, verts=8)
    return finish()

def body_centre(tag):
    o = bpy.data.objects[f"{tag}__Body"]
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    c = (mn + mx) / 2
    return [round(-c.x, 3), round(c.z, 3), round(c.y, 3)]  # Roblox rig-data space: (-x, z, y)

def build_all():
    clear()
    b = bear(); p = pet()
    # anchors (plain 0.5 cubes at the rig origins) let Studio recover the import transform
    for tag, off in (("B01", (0, 0, 0)), ("P01", (0, 40, 0))):
        STATE.update(tag=tag, off=Vector((0, 0, 0)))
        box("Anchor", "dark", off, (0.5, 0.5, 0.5), bevel=0)
        for part, col, o in ITEMS: o.name = o.data.name = f"{tag}__Anchor"
        ITEMS.clear()
    data = {"B01": {"body": body_centre("B01"), "parts": {k: list(v) for k, v in b.items()}},
            "P01": {"body": body_centre("P01"), "parts": {k: list(v) for k, v in p.items()}}}
    json.dump(data, open(os.path.join(OUT, "bear_rigdata.json"), "w"), indent=1)
    return data
