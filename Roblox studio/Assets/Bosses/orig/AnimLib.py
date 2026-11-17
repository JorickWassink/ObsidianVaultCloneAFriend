
import bpy, math
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
FPS = 30
A = Matrix(((-1,0,0),(0,0,1),(0,1,0)))   # Roblox axes -> Blender axes
# short names used in pose tables (Roblox convention, like BossAnimBuilder):
#   UpperArm rx+ raises forward, Left rz- / Right rz+ lifts out sideways; LowerArm rx+ bends the elbow
#   Body rx- leans forward, ry+ turns left, py up, pz+ back; Leg rx+ swings forward; Head rx+ looks up
#   Wings: Left rz- / Right rz+ flaps UP; rx+ sweeps them forward.  Tail: ry swings sideways, rx+ lifts
SHORT = {"B":"Body","H":"Head","LUA":"LeftUpperArm","LLA":"LeftLowerArm","LH":"LeftHand","RUA":"RightUpperArm","RLA":"RightLowerArm","RH":"RightHand",
         "LL":"LeftLeg","RL":"RightLeg","LW":"LeftWing","RW":"RightWing","T":"Tail",
         "LFL":"LeftFrontLeg","RFL":"RightFrontLeg","LBL":"LeftBackLeg","RBL":"RightBackLeg"}
LONG = {v:k for k,v in SHORT.items()}
LEGS = ("LL","RL","LFL","RFL","LBL","RBL")

def P(base=None, **ch):
    t = dict(base or {})
    for k,v in ch.items(): t[k] = list(v)
    return t
GROUND = ["LL","RL","LFL","RFL","LBL","RBL"]   # parts pinned to the floor in grounded poses (a boss may add "T")
def drop(pose, d, lean=0, roll=0, turn=0):
    """Body down by d (negative = up), leaning (rx), turning (ry), rolling (rz). The pose is GROUNDED:
    legs (and anything in GROUND) stay exactly where they stand at rest; their own values are extra swing on top."""
    b = list(pose.get("B",[0,0,0,0,0,0])) + [0]*6
    t = P(pose, B=[lean, turn or b[1], roll, b[3], -d, b[5]])
    t["_ground"] = True
    for k in GROUND:
        t.setdefault(k, [0,0,0,0,0,0])
    return t
def basis(v):
    v = list(v)+[0]*(6-len(v))
    R = Matrix.Rotation(math.radians(v[0]),3,'X') @ Matrix.Rotation(math.radians(v[1]),3,'Y') @ Matrix.Rotation(math.radians(v[2]),3,'Z')
    return Matrix.Translation(A @ Vector(v[3:6])) @ (A @ R @ A.transposed()).to_4x4()
EASE = {"IO":("BEZIER","AUTO"),"IN":("CUBIC","EASE_IN"),"OUT":("CUBIC","EASE_OUT"),"LIN":("LINEAR","AUTO"),"BACK":("BACK","EASE_OUT")}
def _fcurves(act):
    if hasattr(act, "fcurves") and len(act.fcurves): return list(act.fcurves)
    return [fc for l in act.layers for s in l.strips for cb in s.channelbags for fc in cb.fcurves]
LEG_SLACK = 0.1
def set_pose(rig, pose):
    """Sets every bone's basis from the pose table. In grounded poses, GROUND parts are solved so they stay
    at their rest placement in the rig (feet planted), with their own values applied as extra local swing."""
    grounded = pose.get("_ground", False)
    mats = {}
    def arm_mat(pb):   # armature-space matrix from the bases set so far (parents first)
        if pb.name in mats: return mats[pb.name]
        rel = pb.bone.matrix_local if not pb.parent else (pb.parent.bone.matrix_local.inverted() @ pb.bone.matrix_local)
        base = Matrix.Identity(4) if not pb.parent else arm_mat(pb.parent)
        m = base @ rel @ pb.matrix_basis
        mats[pb.name] = m; return m
    order = sorted(rig.pose.bones, key=lambda b: len(b.parent_recursive))
    for pb in order:
        short = LONG.get(pb.name, "?")
        val = pose.get(short, [0,0,0])
        if grounded and short in GROUND and pb.parent:
            parent_m = arm_mat(pb.parent)
            rel = pb.parent.bone.matrix_local.inverted() @ pb.bone.matrix_local
            target = pb.bone.matrix_local @ basis(val)
            mb = (parent_m @ rel).inverted() @ target
            tr = mb.translation.copy()
            # legs may sink into the body when it drops (feet stay planted), but never pull away from it:
            # downward / sideways slide is capped so no gap opens at the hip, the feet lift instead
            tr.z = max(tr.z, -LEG_SLACK)
            h = (tr.x**2 + tr.y**2) ** 0.5
            if h > LEG_SLACK:
                tr.x *= LEG_SLACK / h; tr.y *= LEG_SLACK / h
            mb.translation = tr
            pb.matrix_basis = mb
        else:
            pb.matrix_basis = basis(val) if pb.name != "HumanoidRootPart" else Matrix.Identity(4)
        mats.pop(pb.name, None); arm_mat(pb)

def make(tag, name, length, keys, loop=False, hold=False, events=None):
    """keys: [(time, pose, ease)] ; ease applies from that key to the next. events: {"impact": t, ...} (seconds)"""
    rig = bpy.data.objects[tag + ":Rig"]; rig.animation_data_create()
    bones = [b for b in rig.pose.bones if b.name != "HumanoidRootPart"]
    an = f"{tag}_{name}"
    old = bpy.data.actions.get(an)
    if old: bpy.data.actions.remove(old)
    act = bpy.data.actions.new(an); act.use_fake_user = True
    act["boss"] = tag; act["clip"] = name; act["length"] = length; act["loop"] = loop; act["hold"] = hold
    for k,v in (events or {}).items(): act["ev_"+k] = v
    rig.animation_data.action = act
    for t, pose, ease in keys:
        f = t*FPS + 1
        set_pose(rig, pose)
        for pb in bones:
            pb.keyframe_insert("location", frame=f); pb.keyframe_insert("rotation_quaternion", frame=f)
    seg = {round(t*FPS+1, 3): e for t,_,e in keys}
    for fc in _fcurves(act):
        for kp in fc.keyframe_points:
            ip, ea = EASE[seg.get(round(kp.co.x, 3), "IO")]
            kp.interpolation = ip
            if ip in ("CUBIC","BACK"): kp.easing = ea
            else: kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    act.frame_range = (1, length*FPS + 1)
    rig.animation_data.action = None
    for b in rig.pose.bones: b.matrix_basis.identity()
    return act

def show(tag, name, frame=1):
    rig = bpy.data.objects[tag + ":Rig"]; act = bpy.data.actions[f"{tag}_{name}"]
    rig.animation_data_create(); rig.animation_data.action = act
    sc = bpy.context.scene; sc.frame_start = 1; sc.frame_end = int(act.frame_range[1]); sc.frame_set(frame)

def clip_check_anims(tag, step=2, verbose=True):
    """Frame-by-frame overlap check for every animation of one boss: reports block groups of DIFFERENT parts
    that touch during an animation but not at rest, plus anything dipping under the floor."""
    coll = bpy.data.collections[tag]; rig = bpy.data.objects[tag + ":Rig"]
    was_hidden = coll.hide_viewport; coll.hide_viewport = False
    obs = [o for o in coll.objects if o.type == 'MESH']
    part = lambda o: o.get("rbx_part", o.name)
    bones = rig.data.bones
    def jointed(pa, pb):
        ba, bb = bones.get(pa), bones.get(pb)
        return bool(ba and bb and ((ba.parent and ba.parent.name == pb) or (bb.parent and bb.parent.name == pa)))
    def allowed(a, b):   # main blocks of two directly connected parts may meet at their joint
        return a.get("rbx_name") == part(a) and b.get("rbx_name") == part(b) and jointed(part(a), part(b))
    pairs = [(a,b) for i,a in enumerate(obs) for b in obs[i+1:] if part(a) != part(b) and not allowed(a,b)]
    def trees():
        bpy.context.view_layer.update()
        return {o.name: BVHTree.FromPolygons([o.matrix_world @ v.co for v in o.data.vertices], [p.vertices for p in o.data.polygons]) for o in obs}
    rig.animation_data_create(); rig.animation_data.action = None
    for b in rig.pose.bones: b.matrix_basis.identity()
    T = trees(); rest = {}
    for a,b in pairs:
        n0 = len(T[a.name].overlap(T[b.name]))
        if n0: rest[(a.name,b.name)] = n0
    res, floor = {}, {}
    sc = bpy.context.scene
    for act in [a for a in bpy.data.actions if a.get("boss") == tag]:
        rig.animation_data.action = act
        for f in range(1, int(act.frame_range[1])+1, step):
            sc.frame_set(f); T = trees()
            for a,b in pairs:
                k = (a.name,b.name)
                n = len(T[a.name].overlap(T[b.name]))
                if k in rest:
                    if n <= rest[k]*2 + 12: continue
                    n = n - rest[k]
                if n:
                    r = res.setdefault((a.get("rbx_name"), b.get("rbx_name")), {}); r[act["clip"]] = max(r.get(act["clip"],0), n)
            mz = min((o.matrix_world @ Vector(c)).z for o in obs for c in o.bound_box)
            if mz < -0.4: floor[act["clip"]] = min(floor.get(act["clip"], 0), round(mz,2))
    rig.animation_data.action = None
    for b in rig.pose.bones: b.matrix_basis.identity()
    sc.frame_set(1)
    coll.hide_viewport = was_hidden
    if verbose:
        print(f"[anim clip check {tag}] new overlaps: {len(res)}, under floor: {floor}")
        for k,v in sorted(res.items(), key=lambda kv: -sum(kv[1].values())): print("   ", k, v)
    return res, floor
