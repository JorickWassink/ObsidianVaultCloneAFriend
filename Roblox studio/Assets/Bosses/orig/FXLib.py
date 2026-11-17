
import bpy, bmesh, math, random
from mathutils import Vector, Euler, Matrix
S = bpy.app.driver_namespace["studlib"]
FPS = 30
HIDE = 0.001
def fr(t): return t*FPS + 1

def fx_coll(tag):
    root = bpy.data.collections.get("FX")
    if not root:
        root = bpy.data.collections.new("FX"); bpy.context.scene.collection.children.link(root)
    c = bpy.data.collections.get(tag + "_FX")
    if not c:
        c = bpy.data.collections.new(tag + "_FX"); root.children.link(c)
    return c

def clear(tag):
    c = bpy.data.collections.get(tag + "_FX")
    if c:
        for o in list(c.objects): bpy.data.objects.remove(o, do_unlink=True)
    for a in list(bpy.data.actions):
        if a.get("fx_boss") == tag: bpy.data.actions.remove(a)
    for m in list(bpy.data.meshes):
        if m.users == 0: bpy.data.meshes.remove(m)

_mats = {}
def mat(rgb, glow):
    key = (tuple(rgb), glow)
    if key not in _mats or _mats[key].name not in bpy.data.materials:
        _mats[key] = S["stud_mat"]("FX_%02x%02x%02x%s" % (rgb[0], rgb[1], rgb[2], "_glow" if glow else ""), rgb, glow, 1.3)
    return _mats[key]

def prop(tag, name, blocks):
    """blocks: [(size, loc, rot_deg, rgb, glow)] in the prop's own space -> one mesh object (hidden until animated)"""
    bm = bmesh.new(); mats = []
    for size, loc, rot, rgb, glow in blocks:
        m = mat(rgb, glow)
        if m not in mats: mats.append(m)
        n0 = len(bm.faces)
        S["block_bm"](bm, size, loc, rot)
        bm.faces.ensure_lookup_table()
        for f in bm.faces[n0:]: f.material_index = mats.index(m)
    me = bpy.data.meshes.new(tag + "FX:" + name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    ob = bpy.data.objects.new(tag + "FX:" + name, me); fx_coll(tag).objects.link(ob)
    ob.rotation_mode = 'XYZ'; ob["fx_prop"] = name
    return ob

def animate(ob, tag, clip, keys, attach=None):
    """keys: [(t, loc, rot_deg, scale, interp)] ; the prop is hidden (scale ~0) before the first and after the last key.
    attach=(rig, bone) parents the prop to a bone so it rides along with the boss."""
    if attach:
        rig, bone = attach
        ob.parent = rig; ob.parent_type = 'BONE'; ob.parent_bone = bone
        ob.matrix_parent_inverse = Matrix.Identity(4)
        pb = rig.pose.bones[bone]
        ob.matrix_parent_inverse = (rig.matrix_world @ Matrix.Translation(pb.bone.tail_local)).inverted()
    ob.animation_data_create(); ob.animation_data.action = None
    t0, t1 = keys[0][0], keys[-1][0]
    full = [(max(0, t0 - 1/FPS), keys[0][1], keys[0][2], HIDE, "CONSTANT")] + list(keys) + [(t1 + 1/FPS, keys[-1][1], keys[-1][2], HIDE, "CONSTANT")]
    if t0 - 1/FPS <= 0 and t0 > 0: full[0] = (0, keys[0][1], keys[0][2], HIDE, "CONSTANT")
    for t, loc, rot, sc, ip in full:
        f = fr(t)
        ob.location = Vector(loc)
        ob.rotation_euler = Euler([math.radians(a) for a in rot])
        ob.scale = (sc, sc, sc) if isinstance(sc, (int, float)) else sc
        for p in ("location", "rotation_euler", "scale"): ob.keyframe_insert(p, frame=f)
    act = ob.animation_data.action
    act.name = f"{tag}FX_{clip}:{ob['fx_prop']}"; act.use_fake_user = True
    act["fx_boss"] = tag; act["fx_clip"] = clip
    ips = {round(fr(t), 3): ip for t, *_, ip in full}
    for fc in S_fcurves(act):
        for kp in fc.keyframe_points:
            ip = ips.get(round(kp.co.x, 3), "BEZIER")
            if ip == "CONSTANT": kp.interpolation = 'CONSTANT'
            elif ip == "LIN": kp.interpolation = 'LINEAR'
            elif ip == "OUT": kp.interpolation = 'CUBIC'; kp.easing = 'EASE_OUT'
            elif ip == "IN": kp.interpolation = 'CUBIC'; kp.easing = 'EASE_IN'
            else: kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    # the step BEFORE the first visible key must jump, not grow from zero
    for fc in S_fcurves(act):
        if fc.data_path == "scale":
            kps = fc.keyframe_points
            if kps[0].co.y <= HIDE*2: kps[0].interpolation = 'CONSTANT'
            kps[len(kps)-2].interpolation = 'CONSTANT'
    ob["fx_clip"] = clip; ob["fx_boss"] = tag
    return ob

def S_fcurves(act):
    if hasattr(act, "fcurves") and len(act.fcurves): return list(act.fcurves)
    return [fc for l in act.layers for s in l.strips for cb in s.channelbags for fc in cb.fcurves]

def base(tag):
    rig = bpy.data.objects[tag + ":Rig"]; return Vector((rig.data.bones["HumanoidRootPart"].head_local.x, 0, 0))

# ---------- effect builders (all positions relative to the boss's feet, +Y is behind, -Y in front) ----------
def ring(tag, clip, name, t, center, r0, r1, rgb, dur=0.5, n=None, size=(1.6,1.6,0.9), glow=False, z=0.4, seed=11):
    """shockwave ring of chunky blocks sliding outward along the floor, bumping up as it travels"""
    rnd = random.Random(seed); b = base(tag); c = Vector(center); c.z = 0
    n = n if n and n >= int(2*math.pi*r1/(size[0]*2.2)) else max(10, int(2*math.pi*r1/(size[0]*2.2)))
    for i in range(n):
        a = 2*math.pi*(i + rnd.uniform(-0.2,0.2))/n; d = Vector((math.cos(a), math.sin(a), 0))
        k = rnd.uniform(0.8, 1.2); sz = (size[0]*k, size[1]*k, size[2]*rnd.uniform(0.8,1.3))
        ob = prop(tag, f"{clip}_{name}{i:02d}", [(sz, (0,0,0), (0,0,0), rgb, glow)])
        yaw = math.degrees(a) + rnd.uniform(-15,15); tl = rnd.uniform(-12,12)
        P = lambda u, h: b + c + d*(r0 + (r1-r0)*u) + Vector((0,0,z + h))
        animate(ob, tag, clip, [(t, P(0,0), (tl,0,yaw), 0.6, "OUT"),
                                (t+dur*0.3, P(0.55,0.9), (tl,tl,yaw), 1.15, "LIN"),
                                (t+dur*0.7, P(0.9,0.3), (0,tl,yaw), 0.9, "IN"),
                                (t+dur, P(1.0,0), (0,0,yaw), 0.1, "LIN")])

def burst(tag, clip, name, t, center, n, rgb, spread=4.0, up=3.0, size=0.9, dur=0.6, glow=False, seed=1, fall=0.0, cone=None, start=1.0):
    """chunks flying out in an arc and shrinking away (dust, crumbs, sparks)"""
    rnd = random.Random(seed); b = base(tag); c = Vector(center)
    for i in range(n):
        a = rnd.uniform(0, 2*math.pi) if cone is None else math.radians(cone[0] + rnd.uniform(-cone[1], cone[1]))
        d = Vector((math.cos(a), math.sin(a), 0)) * spread * rnd.uniform(0.6, 1.0)
        h = up * rnd.uniform(0.6, 1.2); s = size * rnd.uniform(0.7, 1.2)
        ob = prop(tag, f"{clip}_{name}{i:02d}", [((s,s,s), (0,0,0), (0,0,0), rgb, glow)])
        spin = [rnd.uniform(-200, 200) for _ in range(3)]
        e = lambda u: 1 - (1-u)**2                     # fast out, slowing down
        dn = d.normalized() if d.length else Vector((1,0,0)); L = d.length
        p = lambda u: b + c + dn*(start + L*e(u)) + Vector((0, 0, h*4*e(u)*(1-e(u))*0.9 + h*0.25*e(u) - fall*u))
        animate(ob, tag, clip, [(t, p(0), (0,0,0), 0.7, "LIN"), (t+dur*0.2, p(0.2), [x*0.3 for x in spin], 1.15, "LIN"),
                                (t+dur*0.5, p(0.5), [x*0.6 for x in spin], 1.0, "LIN"), (t+dur*0.8, p(0.8), [x*0.85 for x in spin], 0.7, "LIN"),
                                (t+dur, p(1.0), spin, 0.1, "LIN")])

def projectile(tag, clip, name, blocks, t0, t1, p0, p1, height=4.0, spin=(0,0,720), steps=6, scale=1.0):
    b = base(tag); p0 = Vector(p0); p1 = Vector(p1)
    ob = prop(tag, f"{clip}_{name}", blocks)
    keys = []
    for k in range(steps+1):
        u = k/steps
        pos = b + p0.lerp(p1, u) + Vector((0, 0, height*4*u*(1-u)))
        keys.append((t0 + (t1-t0)*u, pos, [a*u for a in spin], scale, "LIN"))
    animate(ob, tag, clip, keys)
    return ob

def glow(tag, clip, name, blocks, attach, offset, t0, t1, s0=0.4, s1=1.3, pulses=3):
    """glow that rides on a bone, growing and pulsing between t0 and t1"""
    ob = prop(tag, f"{clip}_{name}", blocks)
    keys = [(t0, offset, (0,0,0), s0, "OUT")]
    for k in range(1, pulses+1):
        u = k/pulses; tt = t0 + (t1-t0)*u
        keys.append((tt - (t1-t0)/pulses*0.5, offset, (0,0,45*u), s0 + (s1-s0)*u*1.1, "IO"))
        keys.append((tt, offset, (0,0,90*u), s0 + (s1-s0)*u*0.9, "IO"))
    animate(ob, tag, clip, keys, attach=attach)
    return ob

def rain(tag, clip, name, blocks, t0, area, n, radius, height=18.0, fall=0.45, gap=0.12, seed=3, land_rgb=(240,220,160), land_glow=False):
    """props dropping from the sky across the arena, each with a little dust pop where it lands"""
    rnd = random.Random(seed); b = base(tag)
    for i in range(n):
        a = rnd.uniform(0, 2*math.pi); r = radius*math.sqrt(rnd.uniform(0.05, 1))
        p = Vector(area) + Vector((math.cos(a)*r, math.sin(a)*r, 0))
        ts = t0 + i*gap; yaw = rnd.uniform(0, 360)
        ob = prop(tag, f"{clip}_{name}{i:02d}", blocks)
        animate(ob, tag, clip, [(ts, b+p+Vector((0,0,height)), (0,0,yaw), 1.0, "IN"), (ts+fall, b+p+Vector((0,0,0.5)), (0,0,yaw+40), 1.0, "LIN"),
                                (ts+fall+0.25, b+p+Vector((0,0,0.5)), (0,0,yaw+40), 1.0, "LIN"), (ts+fall+0.4, b+p+Vector((0,0,0.2)), (0,0,yaw+40), 0.1, "LIN")])
        burst(tag, clip, f"{name}{i:02d}pop", ts+fall, p+Vector((0,0,0.4)), 4, land_rgb, spread=1.8, up=1.2, size=0.5, dur=0.35, glow=land_glow, seed=seed*100+i)

def preview(tag, clip, frame=1):
    """plays the boss clip with its effects: other clips' effects are hidden"""
    bpy.app.driver_namespace["animlib"]["show"](tag, clip, frame)
    for c in bpy.data.collections:
        if c.name.endswith("_FX"):
            for o in c.objects: o.hide_viewport = not (o.get("fx_boss") == tag and o.get("fx_clip") == clip)
    bpy.context.scene.frame_set(frame)


def at(tag, clip, t, objname, mode="center"):
    """where a boss part is at time t of a clip (relative to the boss's feet): centre, or its lowest/front point"""
    rig = bpy.data.objects[tag + ":Rig"]; rig.animation_data_create()
    bpy.data.collections[tag].hide_viewport = False   # hidden collections are not evaluated
    rig.animation_data.action = bpy.data.actions[f"{tag}_{clip}"]
    bpy.context.scene.frame_set(int(round(fr(t)))); bpy.context.view_layer.update()
    ob = bpy.data.objects[f"{tag}:{objname}"]
    vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
    c = sum(vs, Vector()) / len(vs)
    if mode == "low": c = min(vs, key=lambda v: v.z)
    elif mode == "front": c = min(vs, key=lambda v: v.y)
    elif mode == "top": c = max(vs, key=lambda v: v.z)
    rig.animation_data.action = None
    for p in rig.pose.bones: p.matrix_basis.identity()
    bpy.context.scene.frame_set(1)
    return c - base(tag)

def floor(v, z=0.4):
    v = Vector(v); return Vector((v.x, v.y, z))

def star(rgb=(255,240,150), size=1.0, glow=True, rays=8):
    """impact flash: a flat star of thin bars facing the camera (front, -Y)"""
    bl = [((0.9*size,0.3,0.9*size),(0,0,0),(0,45,0),(255,255,255),glow)]
    for i in range(rays):
        a = 360*i/rays; L = (2.4 if i%2==0 else 1.5)*size
        r = math.radians(a)
        bl.append(((0.35*size,0.25,L),(math.sin(r)*L*0.55,0,math.cos(r)*L*0.55),(0,a,0),rgb,glow))
    return bl

def pop(tag, clip, name, blocks, t, pos, s0=0.3, s1=1.2, dur=0.3, yaw=0, rot_spin=30):
    """a prop that pops in, grows and vanishes (impact stars, flashes)"""
    b = base(tag); p = b + Vector(pos)
    ob = prop(tag, f"{clip}_{name}", blocks)
    animate(ob, tag, clip, [(t, p, (0,0,yaw), s0, "OUT"), (t+dur*0.35, p, (0,rot_spin*0.5,yaw), s1, "IO"), (t+dur, p, (0,rot_spin,yaw), 0.05, "IN")])
    return ob

def orbit(tag, clip, name, rgb, attach, center, radius, t0, t1, n=6, turns=2.0, size=0.8, rise=0.0, glow=True):
    """glowing cubes circling a point on a bone (soul swirls, magic charging)"""
    c = Vector(center)
    for i in range(n):
        ob = prop(tag, f"{clip}_{name}{i:02d}", [((size,size,size),(0,0,0),(0,0,0),rgb,glow)])
        keys = []; steps = 8
        for k in range(steps+1):
            u = k/steps; a = 2*math.pi*(i/n + turns*u)
            p = c + Vector((math.cos(a)*radius, math.sin(a)*radius, rise*u + 0.6*math.sin(a*2)))
            sc = 1.0 if 0 < k < steps else 0.4
            keys.append((t0 + (t1-t0)*u, p, (45*u, 45*u, 0), sc, "LIN"))
        animate(ob, tag, clip, keys, attach=attach)
