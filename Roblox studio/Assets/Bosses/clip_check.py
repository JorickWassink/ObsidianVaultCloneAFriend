# Clip check for curved models: splits every mesh object into its loose pieces (one piece = one primitive),
# then for every pair of pieces with overlapping bounds measures how many of A's vertices are inside B.
# A piece that is partly inside another (between LOW and HIGH) means two surfaces cross = visible clipping.
# Pieces fully inside (>= HIGH) are just buried. Pairs on different rig parts are flagged: they clip worse once animated.
# Run after build_bear.build_all():  ns2={}; exec(open(r"...clip_check.py").read(), ns2); ns2["check"]("B01")
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

LOW, HIGH = 0.04, 0.97

def pieces(tag):
    out = []
    for o in bpy.data.objects:
        if o.type != "MESH" or not o.name.startswith(tag + "__") or "Anchor" in o.name: continue
        name = o.name.split("__", 1)[1]; part = name.split("_")[0]
        bm = bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world)
        bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
        seen = set()
        for f0 in bm.faces:
            if f0.index in seen: continue
            stack, isl = [f0], []
            while stack:
                f = stack.pop()
                if f.index in seen: continue
                seen.add(f.index); isl.append(f)
                for e in f.edges:
                    for g in e.link_faces:
                        if g.index not in seen: stack.append(g)
            vids = sorted({v.index for f in isl for v in f.verts})
            remap = {vi: k for k, vi in enumerate(vids)}
            verts = [bm.verts[vi].co.copy() for vi in vids]
            polys = [[remap[v.index] for v in f.verts] for f in isl]
            mn = Vector((min(v.x for v in verts), min(v.y for v in verts), min(v.z for v in verts)))
            mx = Vector((max(v.x for v in verts), max(v.y for v in verts), max(v.z for v in verts)))
            out.append({"obj": name, "part": part, "verts": verts, "bvh": BVHTree.FromPolygons(verts, polys),
                        "mn": mn, "mx": mx, "c": (mn + mx) / 2, "size": (mx - mn)})
        bm.free()
    return out

def inside(p, bvh, mn, mx):
    if not (mn.x <= p.x <= mx.x and mn.y <= p.y <= mx.y and mn.z <= p.z <= mx.z): return False
    # ray parity along two directions (robust against grazing hits)
    votes = 0
    for d in (Vector((1, 0.013, 0.007)).normalized(), Vector((-0.011, 0.009, 1)).normalized()):
        n, o = 0, p.copy()
        for _ in range(16):
            hit = bvh.ray_cast(o, d)
            if hit[0] is None: break
            n += 1; o = hit[0] + d * 1e-4
        votes += n % 2
    return votes == 2

def frac_inside(a, b, samples=80):
    vs = a["verts"]; step = max(1, len(vs) // samples)
    pts = vs[::step]
    return sum(inside(p, b["bvh"], b["mn"], b["mx"]) for p in pts) / len(pts)

def overlap(a, b, pad=0.02):
    return all(a["mn"][i] <= b["mx"][i] + pad and b["mn"][i] <= a["mx"][i] + pad for i in range(3))

def check(tag, ignore_same_obj=True, show=60):
    ps = pieces(tag)
    hits = []
    for i, a in enumerate(ps):
        for j, b in enumerate(ps):
            if i == j or (ignore_same_obj and a["obj"] == b["obj"]) or not overlap(a, b): continue
            f = frac_inside(a, b)
            if LOW < f < HIGH:
                hits.append((round(f, 2), a["obj"], tuple(round(x, 1) for x in a["c"]), b["obj"], tuple(round(x, 1) for x in b["c"]), a["part"] != b["part"]))
    hits.sort(key=lambda h: (not h[5], -h[0]))
    print(f"[clip {tag}] pieces {len(ps)}, crossing pairs {len(hits)}, across rig parts {sum(h[5] for h in hits)}")
    for h in hits[:show]: print(("  MOVES " if h[5] else "  ") + f"{h[0]:.2f} {h[1]}@{h[2]} in {h[3]}@{h[4]}")
    return hits
