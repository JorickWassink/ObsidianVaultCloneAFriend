
import bpy, bmesh, math, os
from mathutils import Vector, Euler, Matrix
BEVEL = 0.06
def srgb(c): return tuple((x/255.0)**2.2 for x in c)
def snap(s): return s
def stud_image():
    img = bpy.data.images.get("RobloxStud")
    if img is None:
        p = os.path.join(os.path.expanduser("~"), "Documents", "CloneAFriendBosses", "RobloxStud.png")
        img = bpy.data.images.load(p); img.name = "RobloxStud"; img.pack()
    return img
def stud_mat(name, rgb255, glow=False, strength=2.5):
    img = stud_image()
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; nt = m.node_tree; N, L = nt.nodes, nt.links
    for n in list(N):
        if n.type not in ('BSDF_PRINCIPLED','OUTPUT_MATERIAL'): N.remove(n)
    b = N["Principled BSDF"]; rgb = srgb(rgb255)
    b.inputs["Roughness"].default_value = 0.55
    uv = N.new("ShaderNodeUVMap"); uv.uv_map = "UVMap"
    tx = N.new("ShaderNodeTexImage"); tx.image = img; tx.interpolation = 'Linear'
    mx = N.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.inputs["A"].default_value = (*rgb, 1)
    L.new(uv.outputs["UV"], tx.inputs["Vector"]); lum = 0.2126*rgb255[0]/255 + 0.7152*rgb255[1]/255 + 0.0722*rgb255[2]/255
    k = max(0.4, min(1.0, 0.4 + lum*1.2))
    m["rbx_stud_strength"] = round(k, 2)
    mul = N.new("ShaderNodeMath"); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = k
    L.new(tx.outputs["Alpha"], mul.inputs[0]); L.new(mul.outputs[0], mx.inputs["Factor"])
    L.new(tx.outputs["Color"], mx.inputs["B"]); L.new(mx.outputs["Result"], b.inputs["Base Color"])
    if glow:
        L.new(mx.outputs["Result"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = strength
    else:
        b.inputs["Emission Strength"].default_value = 0
    m.diffuse_color = (*rgb, 1); m["rbx_color"] = list(rgb255); m["rbx_glow"] = glow
    return m
def block_bm(bm, size, loc, rot, rnd=0.0):
    size = tuple(snap(s) for s in size)
    tmp = bmesh.new(); bmesh.ops.create_cube(tmp, size=1.0)
    for v in tmp.verts: v.co = Vector((v.co.x*size[0], v.co.y*size[1], v.co.z*size[2]))
    bmesh.ops.bevel(tmp, geom=list(tmp.edges)+list(tmp.verts), offset=min(max(BEVEL, rnd), min(size)*0.3), segments=1, affect='EDGES', profile=0.5)
    uvl = tmp.loops.layers.uv.new("UVMap")
    for f in tmp.faces:
        n = f.normal; ax = max(range(3), key=lambda i: abs(n[i])); a, b = [i for i in range(3) if i != ax]
        for lp in f.loops: co = lp.vert.co; lp[uvl].uv = (co[a] + size[a]/2, co[b] + size[b]/2)
    M = Matrix.Translation(loc) @ Euler([math.radians(r) for r in rot]).to_matrix().to_4x4()
    bmesh.ops.transform(tmp, matrix=M, verts=tmp.verts)
    me = bpy.data.meshes.new("tmp"); tmp.to_mesh(me); tmp.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)

class Builder:
    """add(part, colorKey, size(x,y,z), loc, rot_deg). Left = +X, front = -Y, z up, 1 unit = 1 stud.
    One object per (part, color): main color -> '<Part>', others -> '<Part>_<ColorName>'.
    Objects are named '<tag>:<name>' in Blender; the export strips the tag."""
    def __init__(self, tag, palette, main, glow=(), names=None, offset=(0,0,0)):
        self.tag, self.pal, self.main, self.glow = tag, palette, main, set(glow)
        self.names = names or {k: k[0].upper()+k[1:] for k in palette}
        self.off = Vector(offset); self.items = []
    def add(self, part, col, size, loc, rot=(0,0,0), rnd=None):
        if rnd is None: rnd = 0.45 if min(size) >= 2.5 else (0.25 if min(size) >= 1.4 else 0.0)
        self.items.append((part, col, size, Vector(loc)+self.off, rot, rnd))
    def shingle(self, part, cols, center, size, axis, sign, seed=1, plate=(1.6,2.6), tilt=7, thick=0.45, density=1.0):
        """Overlapping raised plates over one face of a block (axis 'x'|'y'|'z', sign +1/-1).
        center/size = the block the plates sit on. Plates alternate between the given colours."""
        import random
        rng = random.Random(seed)
        ai = "xyz".index(axis); u, v = [i for i in range(3) if i != ai]
        cu, cv = center[u], center[v]; su, sv = size[u], size[v]
        n = max(1, int((su*sv) / (plate[1]**2) * 1.6 * density))
        rows = max(1, round((sv / plate[1]) * 1.2)); per = max(1, round(n / rows))
        k = 0
        for r in range(rows):
            for c in range(per):
                w = rng.uniform(*plate); h = rng.uniform(*plate)
                pu = cu - su/2 + w/2 + (su - w) * ((c + 0.5 + rng.uniform(-0.3,0.3)) / per if per > 1 else 0.5)
                pv = cv - sv/2 + h/2 + (sv - h) * ((r + 0.5 + rng.uniform(-0.3,0.3)) / rows if rows > 1 else 0.5)
                pos = [0,0,0]; pos[ai] = center[ai] + sign*(size[ai]/2 + thick*0.5 - 0.12); pos[u] = pu; pos[v] = pv
                sz = [0,0,0]; sz[ai] = thick; sz[u] = min(w, su*0.95); sz[v] = min(h, sv*0.95)
                rot = [0,0,0]; rot[u] = rng.choice((-1,1)) * rng.uniform(2.5, tilt); rot[v] = rng.choice((-1,1)) * rng.uniform(2.0, tilt*0.6)
                rot[ai] = rng.uniform(-6, 6)
                self.add(part, cols[k % len(cols)], tuple(sz), tuple(pos), tuple(rot), rnd=0.12)
                k += 1
    def mirror(self, part_l, col, size, loc, rot=(0,0,0), rnd=None):
        self.add(part_l, col, size, loc, rot, rnd)
        self.add(part_l.replace("Left","Right"), col, size, (-loc[0], loc[1], loc[2]), (rot[0], -rot[1], -rot[2]), rnd)
    def sym(self, part, col, size, loc, rot=(0,0,0), rnd=None):
        """mirrored pair on the same part (e.g. both eyes on Head)"""
        self.add(part, col, size, loc, rot, rnd)
        self.add(part, col, size, (-loc[0], loc[1], loc[2]), (rot[0], -rot[1], -rot[2]), rnd)
    def build(self, joints):
        coll = bpy.data.collections.get(self.tag)
        if coll:
            coll.hide_viewport = False
            for o in list(coll.objects): bpy.data.objects.remove(o, do_unlink=True)
        else:
            coll = bpy.data.collections.new(self.tag); bpy.context.scene.collection.children.link(coll)
        for me in list(bpy.data.meshes):
            if me.users == 0: bpy.data.meshes.remove(me)
        for a in list(bpy.data.armatures):
            if a.users == 0: bpy.data.armatures.remove(a)
        groups = {}
        for part, col, size, loc, rot, rnd in self.items: groups.setdefault((part,col), []).append((size,loc,rot,rnd))
        pre = self.tag + ":"
        for (part,col), its in groups.items():
            name = part if self.main.get(part)==col else f"{part}_{self.names[col]}"
            bm = bmesh.new()
            for size,loc,rot,rnd in its: block_bm(bm, size, loc, rot, rnd)
            me = bpy.data.meshes.new(pre+name); bm.to_mesh(me); bm.free()
            ob = bpy.data.objects.new(pre+name, me); coll.objects.link(ob); ob["rbx_name"] = name; ob["rbx_part"] = part
            me.materials.append(stud_mat(f"{self.tag}_{col}", self.pal[col], col in self.glow))
            cen = sum((Vector(v) for v in ob.bound_box), Vector())/8
            me.transform(Matrix.Translation(-cen)); ob.location = cen
        bpy.context.view_layer.update()
        arm = bpy.data.armatures.new(pre+"Rig"); rig = bpy.data.objects.new(pre+"Rig", arm)
        coll.objects.link(rig); arm.display_type = 'STICK'; rig.show_in_front = True; rig["boss_tag"] = self.tag
        J = {}
        for bname, (par, pos) in joints.items():
            J[bname] = (par, bpy.data.objects[pre+pos].location.copy() if isinstance(pos, str) else Vector(pos)+self.off)
        for o in bpy.context.view_layer.objects: o.select_set(False)
        bpy.context.view_layer.objects.active = rig; rig.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        for bname, (par, pos) in J.items():
            eb = arm.edit_bones.new(bname); eb.head = pos; eb.tail = pos + Vector((0,1.0,0)); eb.roll = 0
        for bname, (par, pos) in J.items():
            if par: arm.edit_bones[bname].parent = arm.edit_bones[par]
        bpy.ops.object.mode_set(mode='OBJECT')
        for b in rig.pose.bones: b.rotation_mode = 'QUATERNION'
        missing = []
        for o in coll.objects:
            if o.type != 'MESH': continue
            if o["rbx_part"] not in arm.bones: missing.append(o.name); continue
            mw = o.matrix_world.copy(); o.parent = rig; o.parent_type = 'BONE'; o.parent_bone = o["rbx_part"]; o.matrix_world = mw
        bpy.context.view_layer.update()
        tris = sum(len(p.vertices)-2 for o in coll.objects if o.type=='MESH' for p in o.data.polygons)
        zs = [(o.matrix_world @ v.co).z for o in coll.objects if o.type=='MESH' for v in o.data.vertices]
        xs = [(o.matrix_world @ v.co).x for o in coll.objects if o.type=='MESH' for v in o.data.vertices]
        print(self.tag, "objects", len(groups), "tris", tris, "height", round(max(zs)-min(zs),1), "width", round(max(xs)-min(xs),1), "unparented", missing)
        clip_check(self.tag)
        return rig

def frame(prefixes, rot=(1.3,0,-0.5), pad=1.0):
    win = bpy.context.window_manager.windows[0]
    area = [a for a in win.screen.areas if a.type=='VIEW_3D'][0]
    region = [r for r in area.regions if r.type=='WINDOW'][0]
    sp = area.spaces[0]; sp.shading.type='MATERIAL'; sp.overlay.show_overlays=False
    r3 = sp.region_3d; r3.view_perspective='PERSP'; r3.view_rotation = Euler(rot).to_quaternion()
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in bpy.context.view_layer.objects:
        if o.type=='MESH' and any(o.name.startswith(p) for p in prefixes) and o.visible_get(): o.select_set(True)
    with bpy.context.temp_override(window=win, area=area, region=region):
        bpy.ops.view3d.view_selected()
    r3.view_distance *= pad
    for o in bpy.context.view_layer.objects: o.select_set(False)
    with bpy.context.temp_override(window=win, area=area, region=region):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


def clip_check(tag, verbose=True):
    """Static clipping check for one model:
    - zfight: two blocks with faces in the same plane, facing the same way, overlapping (flicker / hidden detail)
    - buried: a block completely inside another block (never visible)"""
    import bmesh
    from mathutils import Vector
    coll = bpy.data.collections.get(tag)
    islands = []   # (objname, mn, mx, faces[(normal_axis, sign, plane, (u0,v0,u1,v1))])
    for o in coll.objects:
        if o.type != 'MESH': continue
        bm = bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world)
        seen = set()
        for f0 in bm.faces:
            if f0.index in seen: continue
            stack = [f0]; isl = []
            while stack:
                f = stack.pop()
                if f.index in seen: continue
                seen.add(f.index); isl.append(f)
                for e in f.edges:
                    for g in e.link_faces:
                        if g.index not in seen: stack.append(g)
            vs = [v.co for f in isl for v in f.verts]
            mn = Vector(map(min, *[(v.x,v.y,v.z) for v in vs])); mx = Vector(map(max, *[(v.x,v.y,v.z) for v in vs]))
            faces = []
            for f in isl:
                if f.calc_area() < 0.05: continue
                n = f.normal; ax = max(range(3), key=lambda i: abs(n[i]))
                if abs(n[ax]) < 0.999: continue
                a, b = [i for i in range(3) if i != ax]
                us = [v.co[a] for v in f.verts]; ws = [v.co[b] for v in f.verts]
                faces.append((ax, 1 if n[ax] > 0 else -1, round(f.verts[0].co[ax], 2), (min(us), min(ws), max(us), max(ws))))
            aligned = all(abs(f.normal[max(range(3), key=lambda i: abs(f.normal[i]))]) > 0.999 for f in isl if f.calc_area() >= 0.05)
            islands.append((o.get("rbx_name", o.name), mn, mx, faces, aligned))
        bm.free()
    zf, buried, zfwhere = {}, [], {}
    # coplanar same-facing overlap between different blocks
    idx = {}
    for i, (_, _, _, faces, _) in enumerate(islands):
        for (ax, sg, pl, r) in faces:
            idx.setdefault((ax, sg, pl), []).append((i, r))
    for key, lst in idx.items():
        for p in range(len(lst)):
            for q in range(p+1, len(lst)):
                i, r1 = lst[p]; j, r2 = lst[q]
                if i == j: continue
                w = min(r1[2], r2[2]) - max(r1[0], r2[0]); h = min(r1[3], r2[3]) - max(r1[1], r2[1])
                if w > 0.15 and h > 0.15:
                    k = tuple(sorted((islands[i][0], islands[j][0])))
                    zf[k] = zf.get(k, 0) + 1
                    zfwhere[k] = ("xyz"[key[0]], key[2])
    eps = 0.02
    for i, (ni, mn, mx, _, _) in enumerate(islands):
        for j, (nj, mn2, mx2, _, al2) in enumerate(islands):
            if i == j or not al2: continue
            if all(mn[k] >= mn2[k]-eps and mx[k] <= mx2[k]+eps for k in range(3)) and (mx-mn).length < (mx2-mn2).length:
                buried.append((ni, nj, tuple(round(x,1) for x in (mn+mx)/2))); break
    if verbose:
        print(f"[clip check {tag}] blocks {len(islands)}, z-fighting pairs {len(zf)}, buried blocks {len(buried)}")
        for k, v in zf.items(): print("   zfight", k, v, zfwhere.get(k))
        for b in buried: print("   buried", b)
    return zf, buried


def wing(B, part, root, ang, length, th, y, fingers, cols, mem_th=0.5, strip=1.4, scallop=1.8, inner=None, tip=None, seed=1, tear=0.0, side=1):
    """Block wing in the XZ plane (left wing = side 1, mirrored by B.mirror). root=(x,z) of the spar start,
    ang = spar tilt from vertical (deg, outward), fingers = [(t along spar 0..1, dx at the bottom, bottom z)].
    Membrane strips hang under the spar with their tops tucked inside it, scalloped between the finger bones."""
    import random
    rnd = random.Random(seed)
    B_mirror = B.mirror if part.startswith("Left") else B.sym
    a = math.radians(ang); d = (math.sin(a), math.cos(a))
    x0, z0 = root
    sz = lambda x: z0 + (x - x0) * d[1] / d[0]          # spar centre line height at x
    vh = (th/2) / d[0]                                   # half the spar thickness, measured vertically
    cx, cz = x0 + d[0]*length/2, z0 + d[1]*length/2
    B_mirror(part, cols["spar"], (th, th, length), (cx, y, cz), (0, ang, 0))
    if tip:
        tx, tz = x0 + d[0]*(length+tip[1]*0.4), z0 + d[1]*(length+tip[1]*0.4)
        B_mirror(part, tip[0], (tip[1]*0.8, tip[1]*0.8, tip[1]), (tx, y, tz), (0, ang, 0))
    fpts = []
    for t, dx, zb in fingers:
        tx, tz = x0 + d[0]*length*t, z0 + d[1]*length*t
        bx = tx + dx
        L = math.hypot(tx - bx, tz - zb) + th*0.3
        fa = math.degrees(math.atan2(tx - bx, tz - zb))
        ft = cols.get("finger_th", th*0.6)
        B_mirror(part, cols["finger"], (ft, ft, L), ((tx+bx)/2, y, (tz+zb)/2 + th*0.15), (0, fa, 0))
        fpts.append((tx, bx, zb))
    fpts.sort()
    xs = [inner[0]] + [p[1] for p in fpts]
    zs = [inner[1]] + [p[2] for p in fpts]
    k = 0
    for i in range(len(xs) - 1):
        xa, xb = xs[i], xs[i+1]
        n = max(1, round((xb - xa) / strip))
        w = (xb - xa) / n
        col = cols["mem"][i % len(cols["mem"])]
        for j in range(n):
            xi = xa + j*w
            u = (j + 0.5) / n
            top = sz(xi) + vh*0.75
            bot = zs[i] + (zs[i+1] - zs[i]) * u + scallop * math.sin(math.pi * u)
            if tear and rnd.random() < tear: bot += rnd.uniform(0.6, 1.4)
            h = top - bot
            if h < 0.4: continue
            yy = y + (0.03 if k % 2 else -0.03)
            B_mirror(part, col, (w + 0.02, mem_th - (0.04 if k % 2 else 0), h), (xi + w/2, yy, (top + bot)/2))
            k += 1
    return sz
