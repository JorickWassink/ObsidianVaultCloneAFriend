# Clone a Friend: Base building (Clone lab look), built in PLOT-LOCAL coordinates so it lines up with the
# game's invisible collision walls. Plot-local: X = front(-6) to back(40), Z = -18..28, Y = up (0 = wall bottom).
# Blender axes: bx = X, by = -Z, bz = Y  (1 BU = 1 stud).
# Variants: G (ground floor, with door), U (upper Floor, window where the door is), R (roof, base at Y = 15.2).
# Objects are named "<Variant>_<Side>__<ColourKey>". In Roblox the part name becomes the colour key, so
# "WallPanel" (Wall*) and "Stripe" get the owner's colours from BuildingLook.paint.
# Run: ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Base Building\build_building.py").read(), ns); ns["build_all"]()
import bpy, bmesh, math, json, os
from mathutils import Vector

OUT = r"C:\obsidian\Roblox studio\Assets\Base Building"
COLORS = {
    "WallPanel": "dfe7f2", "Stripe": "3a8dde", "LabWhite": "f7f9fc", "LabDark": "2b3247", "LabGrey": "b8c2d0",
    "LabGlass": "96d7ffg", "NeonCyan": "35e0ffn", "NeonPink": "ff4fa3n", "Lamp": "ffe9a0n", "Planter": "8a95a8",
    "Leaf": "5cc23a", "LeafDark": "3e9e2b", "RoofTop": "9aa6b8", "Metal": "4a5470", "MetalLight": "6b7894",
    "Step": "c9d1dd", "Mat": "3a4258",
}

def clear():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)

def mat(key):
    m = bpy.data.materials.get(key)
    if m: return m
    m = bpy.data.materials.new(key); m.use_nodes = True
    h = COLORS[key].rstrip("ng"); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*lin, 1); b.inputs["Roughness"].default_value = 0.45
    if COLORS[key].endswith("n"):
        b.inputs["Emission Color"].default_value = (*lin, 1); b.inputs["Emission Strength"].default_value = 3
    if COLORS[key].endswith("g"):
        b.inputs["Alpha"].default_value = 0.5
        try: m.blend_method = "BLEND"
        except Exception: pass
    m.diffuse_color = (*lin, 1 if not COLORS[key].endswith("g") else 0.5)
    return m

GROUP = {"name": "X"}  # current "<Variant>_<Side>" group
PARTS = []

def B(x, y, z): return Vector((x, -z, y))  # plot-local -> blender

def _fin(o, col, bevel=0.0, seg=2, smooth=True, ang=35):
    bpy.ops.object.select_all(action="DESELECT"); o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if bevel > 0:
        b = o.modifiers.new("b", "BEVEL"); b.width = bevel; b.segments = seg; b.limit_method = "ANGLE"
        bpy.ops.object.modifier_apply(modifier=b.name)
    if smooth: bpy.ops.object.shade_auto_smooth(angle=math.radians(ang))
    o.data.materials.clear(); o.data.materials.append(mat(col)); o["col"] = col; o["grp"] = GROUP["name"]
    PARTS.append(o); return o

def boxp(x0, x1, y0, y1, z0, z1, col, bevel=0.08, seg=2):
    """axis-aligned box from plot-local bounds"""
    if x1 - x0 < 0.02 or y1 - y0 < 0.02 or z1 - z0 < 0.02: return None
    c = B((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    bpy.ops.mesh.primitive_cube_add(size=1, location=c); o = bpy.context.object
    o.scale = (x1 - x0, z1 - z0, y1 - y0)
    return _fin(o, col, min(bevel, (x1 - x0) / 2.2, (y1 - y0) / 2.2, (z1 - z0) / 2.2), seg)

def cylp(x, y, z, r, h, col, verts=16, axis="Y", bevel=0.05, r2=None):
    """cylinder at plot-local centre; axis = plot axis it runs along"""
    if r2 is None: bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=B(x, y, z))
    else: bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=h, location=B(x, y, z))
    o = bpy.context.object
    if axis == "X": o.rotation_euler = (0, math.pi / 2, 0)
    elif axis == "Z": o.rotation_euler = (math.pi / 2, 0, 0)
    return _fin(o, col, bevel)

def ballp(x, y, z, r, col, scale=(1, 1, 1), seg=10, ring=6):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=ring, radius=r, location=B(x, y, z))
    o = bpy.context.object; o.scale = (scale[0], scale[2], scale[1]); return _fin(o, col, 0, ang=80)

def tubep(pts, r, col, verts=8):
    for a, b in zip(pts[:-1], pts[1:]):
        a, b = B(*a), B(*b); d = b - a
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(a + b) / 2)
        o = bpy.context.object; o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
        _fin(o, col, 0)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=verts, ring_count=5, radius=r, location=b); _fin(bpy.context.object, col, 0)

def rrect(w, h, r, n=3):
    """rounded rectangle outline, centred, CCW, (u, v) points"""
    pts = []
    r = min(r, w / 2 - 0.01, h / 2 - 0.01)
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def wall_map(side, u, v, d):
    """(u along wall, v up, d out of the wall) -> plot-local xyz. d=0 is the wall's centre plane."""
    if side == "Front": return (-5.5 - d, v, u)
    if side == "Back": return (39.5 + d, v, u)
    if side == "South": return (u, v, -17.5 - d)
    if side == "North": return (u, v, 27.5 + d)

def plate(side, outline, d0, d1, col, inner=None, bevel=0.06):
    """extrude a 2D (u,v) outline (optionally with a hole outline of the same point count) between depths d0..d1"""
    bm = bmesh.new()
    def ring(pts, d): return [bm.verts.new(B(*wall_map(side, u, v, d))) for u, v in pts]
    of, ob = ring(outline, d1), ring(outline, d0)
    n = len(outline)
    if inner is None:
        bm.faces.new(of); bm.faces.new(list(reversed(ob)))
    else:
        inf, inb = ring(inner, d1), ring(inner, d0)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new([of[i], of[j], inf[j], inf[i]]); bm.faces.new([ob[j], ob[i], inb[i], inb[j]])
            bm.faces.new([inf[i], inf[j], inb[j], inb[i]])
    for i in range(n):
        j = (i + 1) % n; bm.faces.new([ob[i], ob[j], of[j], of[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("p"); bm.to_mesh(me); o = bpy.data.objects.new("p", me); bpy.context.collection.objects.link(o)
    return _fin(o, col, bevel, 2, ang=40)

# ---------------- walls ----------------
WALLS = {  # side: (u0, u1, list of holes (u0, u1, v0, v1))
    "Front": (-18, 28, [(-15.25, -3.25, 2.5, 13.5), (13.25, 25.25, 2.5, 13.5)]),
    "Back": (-18, 28, [(-15, -3, 2.5, 13.5), (-1, 11, 2.5, 13.5), (13, 25, 2.5, 13.5)]),
    "South": (-6, 40, [(-3, 9, 2.5, 13.5), (11, 23, 2.5, 13.5), (25, 37, 2.5, 13.5)]),
    "North": (-6, 40, [(-3, 9, 2.5, 13.5), (11, 23, 2.5, 13.5), (25, 37, 2.5, 13.5)]),
}
TOP = 15.2

def wall_with_holes(side, u0, u1, holes, col):
    cuts = sorted(set([u0, u1] + [h[0] for h in holes] + [h[1] for h in holes]))
    for a, b in zip(cuts[:-1], cuts[1:]):
        hole = next((h for h in holes if h[0] <= a + 1e-6 and h[1] >= b - 1e-6), None)
        spans = [(0, TOP)] if hole is None else [(0, hole[2]), (hole[3], TOP)]
        for v0, v1 in spans:
            if v1 - v0 < 0.02: continue
            p0 = wall_map(side, a, v0, -0.5); p1 = wall_map(side, b, v1, 0.5)
            boxp(min(p0[0], p1[0]), max(p0[0], p1[0]), v0, v1, min(p0[2], p1[2]), max(p0[2], p1[2]), col, bevel=0.06)

def window(side, u0, u1, v0, v1, mullion=True):
    w, h = u1 - u0, v1 - v0; cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
    outer = [(cu + x, cv + y) for x, y in rrect(w + 1.4, h + 1.4, 1.8)]
    inner = [(cu + x, cv + y) for x, y in rrect(w - 0.2, h - 0.2, 1.3)]
    plate(side, outer, -0.75, 0.75, "LabWhite", inner=inner, bevel=0.12)       # frame through the wall
    plate(side, [(cu + x, cv + y) for x, y in rrect(w - 0.1, h - 0.1, 1.3)], -0.08, 0.08, "LabGlass", bevel=0)
    if mullion:
        a = wall_map(side, cu - 0.2, v0, -0.25); b = wall_map(side, cu + 0.2, v1, 0.25)
        boxp(min(a[0], b[0]), max(a[0], b[0]), v0, v1, min(a[2], b[2]), max(a[2], b[2]), "LabWhite", 0.08)
        a = wall_map(side, u0, cv + 1.8, -0.25); b = wall_map(side, u1, cv + 2.2, 0.25)
        boxp(min(a[0], b[0]), max(a[0], b[0]), cv + 1.8, cv + 2.2, min(a[2], b[2]), max(a[2], b[2]), "LabWhite", 0.08)
    # sill
    a = wall_map(side, u0 - 0.8, v0 - 0.9, 0.2); b = wall_map(side, u1 + 0.8, v0 - 0.45, 1.3)
    boxp(min(a[0], b[0]), max(a[0], b[0]), v0 - 0.9, v0 - 0.45, min(a[2], b[2]), max(a[2], b[2]), "LabWhite", 0.15)

def band(side, u0, u1, v0, v1, d, col, bevel=0.2):
    a = wall_map(side, u0, v0, -0.5); b = wall_map(side, u1, v1, 0.5 + d)
    boxp(min(a[0], b[0]), max(a[0], b[0]), v0, v1, min(a[2], b[2]), max(a[2], b[2]), col, bevel)

def floor_shell(variant):
    for side, (u0, u1, holes) in WALLS.items():
        GROUP["name"] = f"{variant}_{side}"
        hs = list(holes)
        if side == "Front":
            hs.append((-0.5, 10.5, 0, 10.2) if variant == "G" else (0, 10, 2.5, 13.5))
        wall_with_holes(side, u0, u1, hs, "WallPanel")
        for h in hs:
            if side == "Front" and variant == "G" and h[2] == 0: continue  # door gets its own frame
            window(side, *h, mullion=(h[1] - h[0]) > 11)
        # top band (owner stripe colour), between the corner pillars
        band(side, u0 + 1.2, u1 - 1.2, 13.75, 15.0, 0.35, "Stripe", 0.25)
        if variant == "G":
            # plinth, broken at the door
            spans = [(u0 + 1.2, -0.5), (10.5, u1 - 1.2)] if side == "Front" else [(u0 + 1.2, u1 - 1.2)]
            for a, b in spans: band(side, a, b, 0, 1.3, 0.3, "LabDark", 0.15)
        else:
            band(side, u0 + 1.2, u1 - 1.2, -0.05, 0.55, 0.45, "LabWhite", 0.2)  # floor line ledge
    GROUP["name"] = f"{variant}_Corners"
    for (x, z) in [(-5.6, -17.6), (39.6, -17.6), (-5.6, 27.6), (39.6, 27.6)]:
        cylp(x, TOP / 2, z, 1.25, TOP, "LabWhite", verts=20, bevel=0.1)
        cylp(x, TOP + 0.05, z, 1.45, 0.5, "Stripe" if variant else "Stripe", verts=20, bevel=0.15)
        if variant == "G": cylp(x, 0.6, z, 1.5, 1.2, "LabDark", verts=20, bevel=0.15)
    if variant == "G": entrance()

def entrance():
    GROUP["name"] = "G_Door"
    # door frame (rounded top corners) around the 11 x 10.2 opening, z -0.5..10.5
    outer = [(5 + x, 5.6 + y) for x, y in rrect(13.0, 11.6, 1.6)]
    inner = [(5 + x, 5.1 + y) for x, y in rrect(11.0, 10.4, 1.2)]
    plate("Front", outer, -0.8, 0.9, "LabWhite", inner=inner, bevel=0.12)
    # sliding glass doors, opened to the sides (visual only)
    for z0, z1 in ((-0.4, 2.6), (7.4, 10.4)):
        plate("Front", [(z0, 0.0), (z1, 0.0), (z1, 9.9), (z0, 9.9)], 0.1, 0.35, "LabDark", inner=[(z0 + 0.35, 0.35), (z1 - 0.35, 0.35), (z1 - 0.35, 9.55), (z0 + 0.35, 9.55)], bevel=0.05)
        plate("Front", [(z0 + 0.35, 0.35), (z1 - 0.35, 0.35), (z1 - 0.35, 9.55), (z0 + 0.35, 9.55)], 0.18, 0.27, "LabGlass", bevel=0)
    # canopy over the door with a stripe-coloured edge and two slim posts
    boxp(-10.6, -6.0, 10.9, 11.5, -2.2, 12.2, "LabWhite", 0.25, 3)
    boxp(-10.8, -10.4, 10.7, 11.6, -2.2, 12.2, "Stripe", 0.15)
    for z in (-1.7, 11.7):
        cylp(-10.1, 5.45, z, 0.18, 10.9, "MetalLight", verts=10)
        cylp(-10.1, 0.15, z, 0.4, 0.3, "Metal", verts=12)
    for z in (0.5, 4.5, 8.5):  # little downlights under the canopy
        cylp(-8.3, 10.85, z, 0.35, 0.1, "Lamp", verts=12, bevel=0)
    # glowing DNA sign above the canopy
    boxp(-6.6, -6.0, 11.8, 14.6, -1.0, 11.0, "LabDark", 0.3, 3)
    for k in range(25):
        z = -0.2 + k * 0.42; a = k * 0.55
        y1 = 13.2 + 0.85 * math.sin(a); y2 = 13.2 - 0.85 * math.sin(a)
        ballp(-6.75, y1, z, 0.2, "NeonCyan", seg=8, ring=5); ballp(-6.75, y2, z, 0.2, "NeonPink", seg=8, ring=5)
        if k % 2 == 0 and abs(y1 - y2) > 0.35:
            boxp(-6.8, -6.65, min(y1, y2), max(y1, y2), z - 0.05, z + 0.05, "LabWhite", 0.02)
    # wall lamps beside the door
    for z in (-2.0, 12.0):
        boxp(-6.4, -6.0, 7.0, 9.0, z - 0.4, z + 0.4, "Metal", 0.12)
        ballp(-6.6, 8.0, z, 0.38, "Lamp", (0.8, 1.3, 0.8))
    # entrance platform + mat (the game's own ramp stays as the invisible collision)
    boxp(-10.5, -6.0, 0.0, 0.9, -2.2, 12.2, "Step", 0.25, 3)
    boxp(-9.6, -6.2, 0.9, 1.0, 1.0, 9.0, "Mat", 0.04)
    # planters with bushes
    for z in (-4.6, 14.6):
        boxp(-9.6, -6.6, 0.0, 1.8, z - 1.5, z + 1.5, "Planter", 0.25, 3)
        boxp(-9.4, -6.8, 1.6, 1.9, z - 1.3, z + 1.3, "LabDark", 0.05)
        ballp(-8.1, 2.8, z, 1.35, "Leaf", (1, 0.9, 1)); ballp(-8.6, 2.4, z + 0.8, 0.9, "LeafDark"); ballp(-7.6, 2.5, z - 0.7, 0.85, "LeafDark")

# ---------------- roof ----------------
def roof():
    Y = TOP
    GROUP["name"] = "R_Slab"
    boxp(-6.2, 40.2, Y, Y + 1.0, -18.2, 28.2, "RoofTop", 0.2)
    # parapet
    for (x0, x1, z0, z1) in [(-6.4, 40.4, -18.4, -17.2), (-6.4, 40.4, 27.2, 28.4), (-6.4, -5.2, -18.4, 28.4), (39.2, 40.4, -18.4, 28.4)]:
        boxp(x0, x1, Y + 0.8, Y + 2.2, z0, z1, "LabWhite", 0.35, 3)
    for (x, z) in [(-5.6, -17.6), (39.6, -17.6), (-5.6, 27.6), (39.6, 27.6)]:
        cylp(x, Y + 1.6, z, 1.45, 1.6, "Stripe", verts=20, bevel=0.3)
    GROUP["name"] = "R_Vents"
    for (x, z) in [(30, -10), (30, -1)]:  # AC units with fans
        boxp(x - 3.5, x + 3.5, Y + 1.0, Y + 4.2, z - 3.5, z + 3.5, "LabGrey", 0.35, 3)
        cylp(x, Y + 4.25, z, 2.4, 0.2, "Metal", verts=24, bevel=0.03)
        for k in range(5):
            a = k * 2 * math.pi / 5
            boxp(x - 0.2 + 1.0 * math.cos(a) - 0.9, x + 0.2 + 1.0 * math.cos(a) + 0.9, Y + 4.32, Y + 4.42, z + 1.0 * math.sin(a) - 0.3, z + 1.0 * math.sin(a) + 0.3, "MetalLight", 0.03)
        cylp(x, Y + 4.45, z, 0.45, 0.2, "LabWhite", verts=12)
        for i in range(4): boxp(x - 3.6, x - 3.4, Y + 1.6 + i * 0.6, Y + 1.9 + i * 0.6, z - 2.8, z + 2.8, "Metal", 0.04)
    tubep([(26.5, Y + 2.5, -10), (22, Y + 2.5, -10), (22, Y + 1.4, -10)], 0.35, "MetalLight", 10)
    tubep([(26.5, Y + 2.5, -1), (22, Y + 2.5, -1), (22, Y + 2.5, -10)], 0.35, "MetalLight", 10)
    GROUP["name"] = "R_Tank"
    # big DNA tank: the lab's signature
    cylp(6, Y + 1.6, 18, 4.0, 1.2, "LabWhite", verts=28, bevel=0.3)
    cylp(6, Y + 6.2, 18, 3.2, 8.0, "LabGlass", verts=28, bevel=0)
    cylp(6, Y + 10.7, 18, 3.7, 1.0, "LabWhite", verts=28, bevel=0.3)
    cylp(6, Y + 11.5, 18, 2.2, 0.8, "Stripe", verts=24, bevel=0.2, r2=1.4)
    for k in range(22):
        y = Y + 2.6 + k * 0.33; a = k * 0.6
        x1, z1 = 6 + 1.6 * math.cos(a), 18 + 1.6 * math.sin(a); x2, z2 = 6 - 1.6 * math.cos(a), 18 - 1.6 * math.sin(a)
        ballp(x1, y, z1, 0.32, "NeonCyan", seg=8, ring=5); ballp(x2, y, z2, 0.32, "NeonPink", seg=8, ring=5)
        if k % 2 == 0: tubep([(x1, y, z1), (x2, y, z2)], 0.1, "LabWhite", 6)
    for a in range(4):
        ang = a * math.pi / 2 + math.pi / 4
        cylp(6 + 3.4 * math.cos(ang), Y + 6.2, 18 + 3.4 * math.sin(ang), 0.25, 8.6, "LabWhite", verts=10)
    tubep([(10, Y + 4, 18), (14, Y + 4, 18), (14, Y + 1.2, 18)], 0.4, "MetalLight", 10)
    GROUP["name"] = "R_Skylight"
    boxp(12, 24, Y + 0.9, Y + 1.8, 0, 10, "LabWhite", 0.3, 3)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=12, radius=1, location=B(18, Y + 1.8, 5))
    o = bpy.context.object; o.scale = (5.2, 4.2, 2.2)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.01], context="VERTS"); bm.to_mesh(o.data)
    _fin(o, "LabGlass", 0, ang=80)
    for x in (15, 18, 21): boxp(x - 0.12, x + 0.12, Y + 1.8, Y + 3.9, 0.9, 9.1, "LabWhite", 0.05)
    GROUP["name"] = "R_Antenna"
    cylp(34, Y + 1.4, 22, 1.2, 0.8, "Metal", verts=16)
    cylp(34, Y + 5.0, 22, 0.18, 7.0, "MetalLight", verts=10, bevel=0)
    for y in (Y + 3.5, Y + 5.5): cylp(34, y, 22, 0.08, 2.6, "MetalLight", verts=6, axis="Z", bevel=0)
    ballp(34, Y + 8.7, 22, 0.55, "NeonPink")
    # satellite dish
    cylp(33, Y + 1.8, 8, 0.3, 1.6, "Metal", verts=10)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=10, radius=2.2, location=(0, 0, 0))
    o = bpy.context.object
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > -1.2], context="VERTS"); bm.to_mesh(o.data)
    sol = o.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.12
    bpy.context.view_layer.objects.active = o; bpy.ops.object.modifier_apply(modifier="s")
    o.rotation_euler = (math.radians(-140), 0, math.radians(40)); o.location = B(33, Y + 4.4, 8)
    _fin(o, "LabWhite", 0, ang=80)
    tubep([(33, Y + 3.0, 8), (32.6, Y + 4.9, 7.5)], 0.08, "MetalLight", 6)
    # little rooftop planters
    for (x, z) in [(-2, -14), (-2, 24)]:
        boxp(x - 1.5, x + 1.5, Y + 1.0, Y + 2.4, z - 1.5, z + 1.5, "Planter", 0.25, 3)
        ballp(x, Y + 3.2, z, 1.4, "Leaf", (1, 0.85, 1)); ballp(x + 0.7, Y + 2.8, z - 0.6, 0.8, "LeafDark")

def finish():
    """join per (group, colour) -> '<group>__<colour>', origin at plot origin"""
    groups = {}
    for o in PARTS: groups.setdefault((o["grp"], o["col"]), []).append(o)
    made = []
    for (g, col), objs in groups.items():
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs: o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        if len(objs) > 1: bpy.ops.object.join()
        j = bpy.context.object; j.name = j.data.name = f"{g}__{col}"
        bpy.context.scene.cursor.location = (0, 0, 0); bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        made.append(j)
    PARTS.clear(); return made

def build_all(preview=False):
    clear()
    floor_shell("G"); finish()
    floor_shell("U"); u = finish()
    roof(); r = finish()
    # an anchor cube at the plot origin of every variant lets Roblox recover the exact placement
    for v in ("G", "U", "R"):
        GROUP["name"] = f"{v}_Anchor"; boxp(-0.25, 0.25, -0.25, 0.25, -0.25, 0.25, "LabDark", 0)
    finish()
    if preview:  # stack: ground, upper at +15, roof on top of the upper floor; else variants side by side
        for o in u: o.location.z += 15
        for o in r: o.location.z += 15
    else:
        for o in bpy.data.objects:
            if o.name.startswith("U_"): o.location.x += 70
            if o.name.startswith("R_"): o.location.x += 140
    json.dump({"colors": COLORS}, open(os.path.join(OUT, "building_colors.json"), "w"), indent=1)
