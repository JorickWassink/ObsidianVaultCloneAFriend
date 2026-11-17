# SmoothLib: the original Boss builder (StudLib, Documents\CloneAFriendBosses\builds) restyled (ADR 0017,
# vault: Design/Clone a Friend Boss Restyle). Same Builder API and joints, so skeletons and part names stay.
# Changes: no stud texture (plain smooth materials), colours brightened (same hues), rounder two-step bevels with
# weighted normals, calmer fur plates (shingle), blocky cartoon face pieces (face_blocky), and export_boss()
# writing <tag>.fbx (with a "<tag>__Anchor" cube at the model origin) + <tag>_rig.json for Studio's BossRigSmooth.
# Load:  exec(compile(open(r"...\SmoothLib.py").read(), "SmoothLib", "exec"), ns); bpy.app.driver_namespace["studlib"] = ns
import bpy, bmesh, math, os, json, colorsys, random
from mathutils import Vector, Euler, Matrix

OUT = r"C:\obsidian\Roblox studio\Assets\Bosses\orig\export"
FBX_DIR = r"C:\obsidian\Roblox studio\Assets\Stations and Weapons"
BEVEL = 0.16          # was 0.06
SHINGLE = {"density": 0.45, "tilt": 3.0}   # fewer, flatter fur plates than the original (1.0, 7)
FACE_PAL = {"eyeW": (250, 250, 250), "faceD": (30, 24, 26), "tongue": (232, 92, 112), "teeth": (252, 249, 240)}

def bright(c, sat=1.18, val=1.35):
    r, g, b = [x / 255 for x in c]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s > 0.08: s = min(1.0, s * sat)
    v = min(1.0, v * (val if s >= 0.18 else 1.1))   # greys stay grey
    return tuple(round(x * 255) for x in colorsys.hsv_to_rgb(h, s, v))

def srgb(c): return tuple((x / 255.0) ** 2.2 for x in c)

def smooth_mat(name, rgb255, glow=False, strength=2.5):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type not in ("BSDF_PRINCIPLED", "OUTPUT_MATERIAL"): nt.nodes.remove(n)
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"); rgb = srgb(rgb255)
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = 0.5
    if glow:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = strength
    else:
        b.inputs["Emission Strength"].default_value = 0
    m.diffuse_color = (*rgb, 1); m["rbx_color"] = list(rgb255); m["rbx_glow"] = glow
    return m

def block_bm(bm, size, loc, rot, rnd=0.0):
    tmp = bmesh.new(); bmesh.ops.create_cube(tmp, size=1.0)
    for v in tmp.verts: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    off = min(max(BEVEL, rnd), min(size) * 0.3)
    bmesh.ops.bevel(tmp, geom=list(tmp.edges) + list(tmp.verts), offset=off, segments=2 if off > 0.05 else 1, affect="EDGES", profile=0.5)
    M = Matrix.Translation(loc) @ Euler([math.radians(r) for r in rot]).to_matrix().to_4x4()
    bmesh.ops.transform(tmp, matrix=M, verts=tmp.verts)
    me = bpy.data.meshes.new("tmp"); tmp.to_mesh(me); tmp.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)

class Builder:
    """add(part, colorKey, size(x,y,z), loc, rot_deg). Left = +X, front = -Y, z up, 1 unit = 1 stud.
    One object per (part, colour[, face set]): main colour -> '<Part>', others -> '<Part>_<ColorName>',
    face pieces -> 'Head_<Eyes|Mouth>_<Set+Set>_<ColorName>'."""
    def __init__(self, tag, palette, main, glow=(), names=None, offset=(0, 0, 0)):
        self.tag, self.main, self.glow = tag, main, set(glow)
        self.pal = dict(palette); self.pal.update({k: v for k, v in FACE_PAL.items() if k not in self.pal})
        self.names = names or {}
        for k in self.pal: self.names.setdefault(k, k[0].upper() + k[1:])
        self.off = Vector(offset); self.items = []; self.face = None; self.joints = {}
    def add(self, part, col, size, loc, rot=(0, 0, 0), rnd=None):
        if rnd is None: rnd = 0.45 if min(size) >= 2.5 else (0.25 if min(size) >= 1.4 else 0.0)
        self.items.append((part, col, size, Vector(loc) + self.off, rot, rnd, self.face))
    def mirror(self, part_l, col, size, loc, rot=(0, 0, 0), rnd=None):
        self.add(part_l, col, size, loc, rot, rnd)
        self.add(part_l.replace("Left", "Right"), col, size, (-loc[0], loc[1], loc[2]), (rot[0], -rot[1], -rot[2]), rnd)
    def sym(self, part, col, size, loc, rot=(0, 0, 0), rnd=None):
        self.add(part, col, size, loc, rot, rnd)
        self.add(part, col, size, (-loc[0], loc[1], loc[2]), (rot[0], -rot[1], -rot[2]), rnd)
    def shingle(self, part, cols, center, size, axis, sign, seed=1, plate=(1.6, 2.6), tilt=7, thick=0.45, density=1.0):
        rng = random.Random(seed)
        tilt = min(tilt, SHINGLE["tilt"]); density *= SHINGLE["density"]
        ai = "xyz".index(axis); u, v = [i for i in range(3) if i != ai]
        cu, cv = center[u], center[v]; su, sv = size[u], size[v]
        n = max(1, int((su * sv) / (plate[1] ** 2) * 1.6 * density))
        rows = max(1, round((sv / plate[1]) * 1.2 * min(1.0, density * 1.6))); per = max(1, round(n / rows))
        k = 0
        for r in range(rows):
            for c in range(per):
                w = rng.uniform(*plate); h = rng.uniform(*plate)
                pu = cu - su / 2 + w / 2 + (su - w) * ((c + 0.5 + rng.uniform(-0.2, 0.2)) / per if per > 1 else 0.5)
                pv = cv - sv / 2 + h / 2 + (sv - h) * ((r + 0.5 + rng.uniform(-0.2, 0.2)) / rows if rows > 1 else 0.5)
                pos = [0, 0, 0]; pos[ai] = center[ai] + sign * (size[ai] / 2 + thick * 0.5 - 0.12); pos[u] = pu; pos[v] = pv
                sz = [0, 0, 0]; sz[ai] = thick; sz[u] = min(w, su * 0.95); sz[v] = min(h, sv * 0.95)
                rot = [0, 0, 0]; rot[u] = rng.choice((-1, 1)) * rng.uniform(1.0, tilt); rot[v] = rng.choice((-1, 1)) * rng.uniform(1.0, tilt * 0.6)
                self.add(part, cols[k % len(cols)], tuple(sz), tuple(pos), tuple(rot), rnd=0.2)
                k += 1

    # ---------- blocky cartoon faces (ADR 0015 swapped pieces) ----------
    def face_blocky(self, eye, eye_size, mouth, mouth_w, iris, lid, part="Head", buck=False, white="eyeW", pupil="faceD", highlight=True):
        """eye = (x, yFront, z) of the LEFT eye (+X); the right eye mirrors it. yFront = the head's front plane.
        Sets: Eyes Grumpy/Angry/GlanceL/GlanceR/Hurt/Blink/Dazed; Mouth Grumpy/Angry/Roar/Hurt/Dazed."""
        ex, yf, ez = eye; ew, eh = eye_size; mx, my, mz = mouth if mouth else (0, 0, 0); mw = mouth_w
        def put(col, size, x, depth_at, z, rot=(0, 0, 0)):
            self.add(part, col, size, (x, depth_at - size[1] / 2, z), rot, rnd=min(0.08, min(size) * 0.25))
        def eyes_open(dx, lid_h, lid_tilt, iris_k=1.0):
            for sx in (1, -1):
                cx = ex * sx
                put(iris, (0.56 * ew * iris_k, 0.14, 0.6 * eh * iris_k), cx + dx * ew, yf - 0.24, ez - 0.08 * eh)
                put(pupil, (0.28 * ew * iris_k, 0.1, 0.32 * eh * iris_k), cx + dx * ew, yf - 0.36, ez - 0.08 * eh)
                if highlight: put("eyeW", (0.15 * ew, 0.08, 0.15 * eh), cx + dx * ew + 0.13 * ew, yf - 0.44, ez + 0.08 * eh)
                if lid_h > 0:
                    put(lid, (ew * 1.1, 0.2, eh * lid_h), cx, yf - 0.3, ez + eh * (0.5 - lid_h / 2) + 0.05, (0, -lid_tilt * sx, 0))
        self.face = "Eyes_Grumpy+Angry+GlanceL+GlanceR+Dazed"
        for sx in (1, -1): put(white, (ew, 0.3, eh), ex * sx, yf, ez)
        self.face = "Eyes_Grumpy"; eyes_open(0, 0.34, 12)
        self.face = "Eyes_GlanceL"; eyes_open(0.2, 0.34, 12)
        self.face = "Eyes_GlanceR"; eyes_open(-0.2, 0.34, 12)
        self.face = "Eyes_Angry"; eyes_open(0, 0.5, 22, 0.85)
        self.face = "Eyes_Dazed"
        for sx in (1, -1):
            cx = ex * sx; s = 0.62
            for (w, h, dx, dz) in ((s * ew, 0.1 * eh, 0, s / 2 * eh), (s * ew, 0.1 * eh, 0, -s / 2 * eh), (0.1 * ew, s * eh, s / 2 * ew, 0), (0.1 * ew, s * eh, -s / 2 * ew, 0)):
                put("faceD", (w, 0.1, h), cx + dx, yf - 0.3, ez + dz)
            put("faceD", (0.22 * ew, 0.1, 0.22 * eh), cx, yf - 0.3, ez)
        self.face = "Eyes_Hurt"
        for sx in (1, -1):
            cx = ex * sx
            put("faceD", (0.7 * ew, 0.2, 0.14 * eh), cx, yf, ez + 0.16 * eh, (0, -28 * sx, 0))
            put("faceD", (0.7 * ew, 0.2, 0.14 * eh), cx, yf, ez - 0.16 * eh, (0, 28 * sx, 0))
        self.face = "Eyes_Blink"
        for sx in (1, -1): put("faceD", (ew, 0.2, 0.16 * eh), ex * sx, yf, ez - 0.1 * eh)
        if mouth is None:
            self.face = None; return
        # mouths
        def bucks(dz):
            for sx in (1, -1): put("teeth", (0.16 * mw, 0.14, 0.24 * mw), mx + 0.09 * mw * sx, my - 0.14, mz + dz)
        self.face = "Mouth_Grumpy"
        put("faceD", (0.46 * mw, 0.2, 0.12 * mw), mx, my, mz)
        for sx in (1, -1): put("faceD", (0.3 * mw, 0.2, 0.12 * mw), mx + 0.34 * mw * sx, my, mz - 0.05 * mw, (0, 24 * sx, 0))
        if buck: bucks(-0.14 * mw)
        else: put("teeth", (0.1 * mw, 0.12, 0.14 * mw), mx + 0.16 * mw, my - 0.14, mz - 0.11 * mw)
        self.face = "Mouth_Angry"
        put("faceD", (mw, 0.2, 0.34 * mw), mx, my, mz)
        if buck: bucks(0.0)
        else:
            for sx in (1, -1): put("teeth", (0.12 * mw, 0.12, 0.14 * mw), mx + 0.28 * mw * sx, my - 0.14, mz + 0.1 * mw)
        self.face = "Mouth_Roar"
        put("faceD", (mw * 1.05, 0.2, 0.72 * mw), mx, my, mz - 0.12 * mw)
        put("tongue", (0.6 * mw, 0.12, 0.2 * mw), mx, my - 0.14, mz - 0.36 * mw)
        if buck: bucks(0.1 * mw)
        else:
            for sx in (1, -1): put("teeth", (0.14 * mw, 0.12, 0.22 * mw), mx + 0.3 * mw * sx, my - 0.14, mz + 0.1 * mw)
        self.face = "Mouth_Hurt"
        for k in range(4):
            put("faceD", (0.3 * mw, 0.2, 0.1 * mw), mx + (-0.36 + k * 0.24) * mw, my, mz + (0.04 if k % 2 else -0.04) * mw, (0, (24 if k % 2 else -24), 0))
        put("teeth", (0.62 * mw, 0.12, 0.1 * mw), mx, my - 0.14, mz - 0.12 * mw)
        self.face = "Mouth_Dazed"
        put("faceD", (0.28 * mw, 0.2, 0.26 * mw), mx + 0.1 * mw, my, mz)
        put("tongue", (0.18 * mw, 0.12, 0.22 * mw), mx + 0.18 * mw, my - 0.14, mz - 0.18 * mw)
        self.face = None

    def blink_set(self, eye, w, col="dark", part="Head"):
        """Pet blink: a closed ^ arc per eye (face set Eyes_Blink). eye = (x, yFront, z) of the left eye."""
        ex, yf, ez = eye
        self.face = "Eyes_Blink"
        for sx in (1, -1):
            for side in (1, -1):
                self.add(part, col, (0.55 * w, 0.2, 0.15 * w), (ex * sx + side * 0.22 * w, yf - 0.1, ez + 0.02 * w), (0, side * 25, 0), rnd=0.04)
        self.face = None

    def scale_part(self, part, k, pivot):
        """scale every block of one part about a pivot (e.g. a bigger head about the neck joint)"""
        pv = Vector(pivot) + self.off
        for i, it in enumerate(self.items):
            if it[0] != part: continue
            size = tuple(v * k for v in it[2]); loc = pv + (it[3] - pv) * k
            self.items[i] = (it[0], it[1], size, loc, it[4], it[5] * k, it[6])

    def build(self, joints):
        coll = bpy.data.collections.get(self.tag)
        if coll:
            coll.hide_viewport = False
            for o in list(coll.objects): bpy.data.objects.remove(o, do_unlink=True)
        else:
            coll = bpy.data.collections.new(self.tag); bpy.context.scene.collection.children.link(coll)
        for me in list(bpy.data.meshes):
            if me.users == 0: bpy.data.meshes.remove(me)
        groups = {}
        for part, col, size, loc, rot, rnd, face in self.items: groups.setdefault((part, col, face), []).append((size, loc, rot, rnd))
        pre = self.tag + ":"
        for (part, col, face), its in groups.items():
            if face: name = f"{part}_{face}_{self.names[col]}"
            else: name = part if self.main.get(part) == col else f"{part}_{self.names[col]}"
            bm = bmesh.new()
            for size, loc, rot, rnd in its: block_bm(bm, size, loc, rot, rnd)
            me = bpy.data.meshes.new(pre + name); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new(pre + name, me); coll.objects.link(ob); ob["rbx_name"] = name; ob["rbx_part"] = part
            rgb = bright(self.pal[col]) if col not in FACE_PAL else self.pal[col]
            glow = col in self.glow
            me.materials.append(smooth_mat(f"S_{self.tag}_{col}", rgb, glow))
            ob["rbx_hex"] = "%02x%02x%02x" % rgb + ("n" if glow else "")
            for p in me.polygons: p.use_smooth = True
            wn = ob.modifiers.new("wn", "WEIGHTED_NORMAL"); wn.keep_sharp = True
            cen = sum((Vector(v) for v in ob.bound_box), Vector()) / 8
            me.transform(Matrix.Translation(-cen)); ob.location = cen
        bpy.context.view_layer.update()
        arm = bpy.data.armatures.new(pre + "Rig"); rig = bpy.data.objects.new(pre + "Rig", arm)
        coll.objects.link(rig); arm.display_type = "STICK"; rig.show_in_front = True; rig["boss_tag"] = self.tag
        J = {}
        for bname, (par, pos) in joints.items():
            J[bname] = (par, bpy.data.objects[pre + pos].location.copy() if isinstance(pos, str) else Vector(pos) + self.off)
        self.joints = J
        for o in bpy.context.view_layer.objects: o.select_set(False)
        bpy.context.view_layer.objects.active = rig; rig.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        for bname, (par, pos) in J.items():
            eb = arm.edit_bones.new(bname); eb.head = pos; eb.tail = pos + Vector((0, 1.0, 0)); eb.roll = 0
        for bname, (par, pos) in J.items():
            if par: arm.edit_bones[bname].parent = arm.edit_bones[par]
        bpy.ops.object.mode_set(mode="OBJECT")
        for b in rig.pose.bones: b.rotation_mode = "QUATERNION"
        for o in coll.objects:
            if o.type != "MESH": continue
            if o["rbx_part"] not in arm.bones: continue
            mw = o.matrix_world.copy(); o.parent = rig; o.parent_type = "BONE"; o.parent_bone = o["rbx_part"]; o.matrix_world = mw
        bpy.context.view_layer.update()
        tris = sum(len(p.vertices) - 2 for o in coll.objects if o.type == "MESH" for p in o.data.polygons)
        print(self.tag, "objects", len(groups), "tris", tris)
        bpy.app.driver_namespace.setdefault("smooth_builders", {})[self.tag] = self
        return rig

def export_pair(tags, name):
    """one FBX holding several models (e.g. a Boss and its Pet), each with its own anchor; a rig json per tag"""
    keep = []
    for tag in tags:
        B = bpy.app.driver_namespace["smooth_builders"][tag]
        meshes = [o for o in bpy.data.collections[tag].objects if o.type == "MESH"]
        for o in meshes: keep.append((o, o.name)); o.name = f"{tag}__{o['rbx_name']}"
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
        me = bpy.data.meshes.new(f"{tag}__Anchor"); bm.to_mesh(me); bm.free()
        anc = bpy.data.objects.new(f"{tag}__Anchor", me); bpy.context.scene.collection.objects.link(anc); anc.location = B.off
        keep.append((anc, None))
        bones = [[n, par, round((pos - B.off).x, 3), round((pos - B.off).y, 3), round((pos - B.off).z, 3)] for n, (par, pos) in B.joints.items()]
        bones.sort(key=lambda b: (0 if b[1] is None else 1 if b[1] == "HumanoidRootPart" else 2))
        os.makedirs(OUT, exist_ok=True)
        json.dump({"tag": tag, "bones": bones, "parts": {o["rbx_name"]: o["rbx_hex"] for o in meshes}}, open(os.path.join(OUT, f"{tag}_rig.json"), "w"), indent=1)
    bpy.ops.object.select_all(action="DESELECT")
    for o, _ in keep: o.select_set(True)
    path = os.path.join(FBX_DIR, f"{name}.fbx")
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, apply_unit_scale=True, object_types={"MESH"},
                             use_mesh_modifiers=True, mesh_smooth_type="OFF", add_leaf_bones=False)
    for o, n in keep:
        if n is None: bpy.data.objects.remove(o, do_unlink=True)
        else: o.name = n
    return path

def export_boss(tag, display=None):
    """FBX of one model (objects renamed '<tag>__<rbx_name>', plus '<tag>__Anchor' at the model origin) and
    <tag>_rig.json: bones {name, parent, x, y, z} in Blender coords relative to the anchor, parts {name: hex}."""
    B = bpy.app.driver_namespace["smooth_builders"][tag]
    coll = bpy.data.collections[tag]
    meshes = [o for o in coll.objects if o.type == "MESH"]
    old = {o: o.name for o in meshes}
    for o in meshes: o.name = f"{tag}__{o['rbx_name']}"
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    me = bpy.data.meshes.new(f"{tag}__Anchor"); bm.to_mesh(me); bm.free()
    anc = bpy.data.objects.new(f"{tag}__Anchor", me); bpy.context.scene.collection.objects.link(anc); anc.location = B.off
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes + [anc]: o.select_set(True)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(FBX_DIR, f"Restyle_{tag}.fbx")
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, apply_unit_scale=True, object_types={"MESH"},
                             use_mesh_modifiers=True, mesh_smooth_type="OFF", add_leaf_bones=False)
    bpy.data.objects.remove(anc, do_unlink=True)
    for o, n in old.items(): o.name = n
    bones = []
    for name, (par, pos) in B.joints.items():
        p = pos - B.off
        bones.append([name, par, round(p.x, 3), round(p.y, 3), round(p.z, 3)])
    order = {"HumanoidRootPart": 0}
    bones.sort(key=lambda b: (0 if b[1] is None else 1 if b[1] == "HumanoidRootPart" else 2))
    parts = {o["rbx_name"]: o["rbx_hex"] for o in meshes}
    json.dump({"tag": tag, "display": display, "bones": bones, "parts": parts}, open(os.path.join(OUT, f"{tag}_rig.json"), "w"), indent=1)
    return path, len(meshes)

def wing(B, part, root, ang, length, th, y, fingers, cols, mem_th=0.5, strip=1.4, scallop=1.8, inner=None, tip=None, seed=1, tear=0.0, side=1):
    """unchanged from StudLib: block wing in the XZ plane (see the original for details)"""
    rnd = random.Random(seed)
    B_mirror = B.mirror if part.startswith("Left") else B.sym
    a = math.radians(ang); d = (math.sin(a), math.cos(a))
    x0, z0 = root
    sz = lambda x: z0 + (x - x0) * d[1] / d[0]
    vh = (th / 2) / d[0]
    cx, cz = x0 + d[0] * length / 2, z0 + d[1] * length / 2
    B_mirror(part, cols["spar"], (th, th, length), (cx, y, cz), (0, ang, 0))
    if tip:
        tx, tz = x0 + d[0] * (length + tip[1] * 0.4), z0 + d[1] * (length + tip[1] * 0.4)
        B_mirror(part, tip[0], (tip[1] * 0.8, tip[1] * 0.8, tip[1]), (tx, y, tz), (0, ang, 0))
    fpts = []
    for t, dx, zb in fingers:
        tx, tz = x0 + d[0] * length * t, z0 + d[1] * length * t
        bx = tx + dx
        L = math.hypot(tx - bx, tz - zb) + th * 0.3
        fa = math.degrees(math.atan2(tx - bx, tz - zb))
        ft = cols.get("finger_th", th * 0.6)
        B_mirror(part, cols["finger"], (ft, ft, L), ((tx + bx) / 2, y, (tz + zb) / 2 + th * 0.15), (0, fa, 0))
        fpts.append((tx, bx, zb))
    fpts.sort()
    xs = [inner[0]] + [p[1] for p in fpts]
    zs = [inner[1]] + [p[2] for p in fpts]
    k = 0
    for i in range(len(xs) - 1):
        xa, xb = xs[i], xs[i + 1]
        n = max(1, round((xb - xa) / strip))
        w = (xb - xa) / n
        col = cols["mem"][i % len(cols["mem"])]
        for j in range(n):
            xi = xa + j * w
            u = (j + 0.5) / n
            top = sz(xi) + vh * 0.75
            bot = zs[i] + (zs[i + 1] - zs[i]) * u + scallop * math.sin(math.pi * u)
            if tear and rnd.random() < tear: bot += rnd.uniform(0.6, 1.4)
            h = top - bot
            if h < 0.4: continue
            yy = y + (0.03 if k % 2 else -0.03)
            B_mirror(part, col, (w + 0.02, mem_th - (0.04 if k % 2 else 0), h), (xi + w / 2, yy, (top + bot) / 2))
            k += 1
    return sz
