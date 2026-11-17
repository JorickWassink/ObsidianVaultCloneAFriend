
F = __import__("bpy").app.driver_namespace["fxlib"]
from mathutils import Vector
projectile, glow, rain, pop, star, at, floor, orbit, clear = (F[k] for k in
    ("projectile","glow","rain","pop","star","at","floor","orbit","clear"))
# effects scale with the boss: bigger bosses throw bigger chunks
SZ = {"B01":1.5,"B02":1.4,"B03":1.3,"B04":1.4,"B05":1.6,"B06":1.7,"B07":1.7,"B08":1.9,"B09":1.9,"B10":2.3}
def ring(tag, clip, name, t, center, r0, r1, rgb, size=(1.6,1.6,0.9), **kw):
    k = SZ[tag]; F["ring"](tag, clip, name, t, center, r0, r1, rgb, size=tuple(x*k for x in size), **kw)
def burst(tag, clip, name, t, center, n, rgb, size=0.9, **kw):
    F["burst"](tag, clip, name, t, center, n, rgb, size=size*SZ[tag], **kw)
DUST = (205,182,142); DIRT = (132,96,60); WHITE = (250,250,246); GOLD = (255,200,60); GREY = (150,150,158)

def mid(a, b): return (a + b) / 2

def intro_pound(tag, r1=10, rgb=DUST, n=16):
    p = floor(mid(at(tag,"Intro",3.35,"LeftHand","low"), at(tag,"Intro",3.35,"RightHand","low")))
    ring(tag, "Intro", "PoundRing", 3.35, p, 1.5, r1, rgb, dur=0.55, n=n)
    burst(tag, "Intro", "PoundDust", 3.35, p, 12, rgb, spread=r1*0.6, up=3, size=1.0, dur=0.7, seed=7, start=2)

def fx_B01():
    tag = "B01"; clear(tag)
    p = floor(mid(at(tag,"Strike",0.55,"LeftHand","low"), at(tag,"Strike",0.55,"RightHand","low")))
    ring(tag, "Strike", "Ring", 0.55, p, 1, 6, DUST, dur=0.45, n=12)
    burst(tag, "Strike", "Dust", 0.55, p, 8, DUST, spread=4, up=2.5, size=0.9, dur=0.55, seed=1)
    pop(tag, "Strike", "Star", star(), 0.55, p + Vector((0,-1,2.5)), s1=1.0)
    # BEAR SLAM: the landing cracks the ground: two dust waves and flying turf
    ring(tag, "SlamHit", "Wave", 0.0, (0,-1,0), 2, 16, DUST, dur=0.6, n=22)
    ring(tag, "SlamHit", "Wave2", 0.12, (0,-1,0), 1.5, 10, DIRT, dur=0.5, n=16)
    burst(tag, "SlamHit", "Dust", 0.0, (0,-1,0.5), 16, DUST, spread=9, up=5, size=1.2, dur=0.8, seed=2, start=6)
    burst(tag, "SlamHit", "Turf", 0.0, (0,-1,0.5), 10, (96,150,70), spread=7, up=7, size=0.8, dur=0.8, seed=3, start=6)
    intro_pound(tag)

def fx_B02():
    tag = "B02"; clear(tag)
    p = floor(at(tag,"Strike",0.55,"RightLeg","low"))
    ring(tag, "Strike", "Ring", 0.55, p, 1, 6, DIRT, dur=0.45, n=12)
    burst(tag, "Strike", "Dirt", 0.55, p, 8, DIRT, spread=4, up=3, size=0.8, dur=0.55, seed=4)
    # CARROT HOP: every landing bursts dirt and carrot chunks
    ring(tag, "SlamHit", "Wave", 0.0, (0,-1,0), 2, 14, DIRT, dur=0.55, n=20)
    burst(tag, "SlamHit", "Dirt", 0.0, (0,-1,0.5), 14, DIRT, spread=8, up=4.5, size=1.0, dur=0.7, seed=5, start=4.5)
    burst(tag, "SlamHit", "Carrot", 0.0, (0,-1,0.8), 8, (240,128,40), spread=7, up=6, size=0.9, dur=0.8, seed=6, start=4.5)
    burst(tag, "SlamHit", "Leaf", 0.05, (0,-1,0.8), 5, (90,180,70), spread=6, up=7, size=0.7, dur=0.85, seed=7, start=4.5)
    intro_pound(tag, rgb=DIRT)

COIN = [((1.8,0.4,1.8),(0,0,0),(0,0,0),GOLD,True), ((1.1,0.5,1.1),(0,0,0),(0,0,0),(230,160,30),True)]
def fx_B03():
    tag = "B03"; clear(tag)
    h = at(tag,"Strike",0.55,"RightHand")
    slash = [((0.35,0.25,3.4),(x,0,0),(0,35,0),WHITE,True) for x in (-0.9,0,0.9)]
    pop(tag, "Strike", "Slash", slash, 0.52, h + Vector((0,-1.5,0)), s0=0.6, s1=1.2, dur=0.3, rot_spin=0)
    burst(tag, "Strike", "Spark", 0.55, h + Vector((0,-1.5,0)), 6, WHITE, spread=3, up=1.5, size=0.5, dur=0.35, glow=True, seed=8)
    # COIN TOSS: a coin glints in the paw while it winds up, then flies, trailing sparkles, and bursts where it lands
    glow(tag, "SpecialWind", "CoinGlint", COIN, (bpy_rig(tag), "RightHand"), base_abs(tag, at(tag,"SpecialWind",0.6,"RightHand") + Vector((0,-1.4,0))), 0.3, 1.6, 0.4, 1.0, 4)
    h0 = at(tag,"SpecialThrow",0.12,"RightHand"); land = Vector((0,-18,0.6))
    projectile(tag, "SpecialThrow", "Coin", COIN, 0.12, 0.55, h0, land, height=5, spin=(0,0,1080))
    for k,(tt,u) in enumerate(((0.22,0.25),(0.32,0.5),(0.42,0.75))):
        pos = h0.lerp(land, u) + Vector((0,0,5*4*u*(1-u)))
        burst(tag, "SpecialThrow", f"Trail{k}", tt, pos, 3, (255,230,120), spread=0.8, up=0.6, size=0.4, dur=0.3, glow=True, seed=20+k)
    burst(tag, "SpecialThrow", "Land", 0.55, land, 10, GOLD, spread=4, up=3, size=0.6, dur=0.5, glow=True, seed=9)
    ring(tag, "SpecialThrow", "LandRing", 0.55, floor(land), 0.8, 5, GOLD, dur=0.4, n=10, size=(0.9,0.9,0.4), glow=True)
    intro_pound(tag)

def fx_B04():
    tag = "B04"; clear(tag)
    def glove(clip, t):
        l = at(tag, clip, t, "LeftHand"); r = at(tag, clip, t, "RightHand")
        return l if l.y < r.y else r
    pop(tag, "Strike", "Star", star(), 0.55, glove("Strike",0.55) + Vector((0,-1.8,0)))
    # TITLE FIGHT COMBO: a star on every punch, the joey's jab, then a big uppercut blast
    for k, ev in enumerate(("hit1","hit2","hit3")):
        t = bpy_ev(tag, "Combo", ev)
        g = glove("Combo", t)
        pop(tag, "Combo", f"Star{k}", star(), t, g + Vector((0,-1.8,0)), s1=1.1)
        burst(tag, "Combo", f"Spark{k}", t, g + Vector((0,-1.8,0)), 5, (255,240,150), spread=2.5, up=1, size=0.45, dur=0.3, glow=True, seed=30+k)
    tj = bpy_ev(tag, "Combo", "joey")
    pop(tag, "Combo", "JoeyStar", star(size=0.6), tj, at(tag,"Combo",tj,"Body") + Vector((0,-5.5,0)), s1=0.9, dur=0.25)
    tu = bpy_ev(tag, "Combo", "uppercut")
    g = glove("Combo", tu) + Vector((0,-1.5,1.0))
    pop(tag, "Combo", "BigStar", star(size=2.2), tu, g, s1=1.5, dur=0.45)
    burst(tag, "Combo", "UpSpark", tu, g, 10, (255,220,90), spread=3, up=6, size=0.6, dur=0.6, glow=True, seed=40)
    ring(tag, "Combo", "Ring", tu, (0,-2,0), 2, 11, DUST, dur=0.5)
    intro_pound(tag)

FLOUR = [((1.9,1.9,1.9),(0,0,0),(0,0,0),WHITE,False), ((0.9,0.9,0.6),(0,0,1.2),(0,0,0),(200,170,120),False)]
PAN = [((4.0,4.0,0.5),(0,0,0),(0,0,0),(60,60,66),False), ((3.1,3.1,0.55),(0,0,0.05),(0,0,0),(90,90,98),False),
       ((0.9,3.6,0.5),(0,3.7,0),(0,0,0),(40,40,44),False)]
def fx_B05():
    tag = "B05"; clear(tag)
    p = floor(at(tag,"Strike",0.55,"RightHand_RollingPin","low"))
    ring(tag, "Strike", "Ring", 0.55, p, 1, 7, DUST, dur=0.45, n=14)
    burst(tag, "Strike", "Flour", 0.55, p, 9, WHITE, spread=4, up=3, size=1.0, dur=0.6, seed=10)
    pop(tag, "Strike", "Star", star(), 0.55, p + Vector((0,0,2.0)))
    # KITCHEN CATASTROPHE: flour bombs that burst into clouds, then a fist slam that rains frying pans
    h0 = at(tag,"SpecialThrow",0.12,"LeftHand"); land = Vector((0,-17,0.8))
    projectile(tag, "SpecialThrow", "FlourBomb", FLOUR, 0.12, 0.55, h0, land, height=6, spin=(360,0,180))
    burst(tag, "SpecialThrow", "Cloud", 0.55, land, 14, WHITE, spread=5, up=3.5, size=1.6, dur=0.9, seed=11)
    ring(tag, "SpecialThrow", "CloudRing", 0.55, floor(land), 1, 6, WHITE, dur=0.5, n=12)
    ring(tag, "SpecialHit", "Wave", 0.15, (0,-3,0), 2, 16, DUST, dur=0.6, n=22)
    burst(tag, "SpecialHit", "Dust", 0.15, (0,-3,0.5), 14, DUST, spread=9, up=4.5, size=1.2, dur=0.8, seed=12, start=7)
    rain(tag, "SpecialHit", "Pan", PAN, 0.35, (0,-12,0), 8, 14, height=22, fall=0.45, gap=0.09, seed=13, land_rgb=GREY)
    intro_pound(tag)

def bpy_rig(tag): return __import__("bpy").data.objects[tag + ":Rig"]
def bpy_ev(tag, clip, ev): return __import__("bpy").data.actions[f"{tag}_{clip}"]["ev_" + ev]
def base_abs(tag, rel): return F["base"](tag) + rel


def rest(tag, objname, mode="center"):
    """where a part sits in the rest pose (absolute world position, for effects riding on a bone)"""
    import bpy
    rig = bpy.data.objects[tag + ":Rig"]; rig.animation_data.action = None
    for p in rig.pose.bones: p.matrix_basis.identity()
    bpy.context.scene.frame_set(1); bpy.context.view_layer.update()
    ob = bpy.data.objects[f"{tag}:{objname}"]; vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
    if mode == "low": return min(vs, key=lambda v: v.z)
    if mode == "top": return max(vs, key=lambda v: v.z)
    return sum(vs, Vector()) / len(vs)

def pound(tag, parts, t=3.35, clip="Intro", r1=10, rgb=DUST):
    p = floor(sum((at(tag, clip, t, q, "low") for q in parts), Vector()) / len(parts))
    ring(tag, clip, "PoundRing", t, p, 1.5, r1, rgb, dur=0.55)
    burst(tag, clip, "PoundDust", t, p, 12, rgb, spread=r1*0.6, up=3, size=1.0, dur=0.7, seed=7, start=2)

GOLDG = (255,210,80); BLUEG = (90,200,255); GREENG = (90,255,140); PURPG = (180,90,255); ORANGEG = (255,150,40)
def slash(rgb): return [((0.35,0.25,3.6),(x,0,0),(0,35,0),rgb,True) for x in (-0.9,0,0.9)]

def fx_B06():
    tag = "B06"; clear(tag)
    rig = bpy_rig(tag)
    h = at(tag,"Strike",0.55,"Head_HornGlow")
    pop(tag, "Strike", "Star", star(GOLDG), 0.55, h + Vector((0,-1.5,0)))
    burst(tag, "Strike", "Spark", 0.55, h, 7, GOLDG, spread=3, up=2, size=0.5, dur=0.4, glow=True, seed=50)
    # PALADIN STAMPEDE: the horn charges up gold while it scrapes, dust kicks behind the gallop, the stomp sends a gold shockwave
    hg = rest(tag, "Head_HornGlow")
    glow(tag, "SpecialWind", "HornGlow", [((2.2,2.2,2.2),(0,0,0),(0,45,45),GOLDG,True)], (rig,"Head"), hg, 0.2, 1.5, 0.3, 1.5, 4)
    for k, tt in enumerate((0.55, 1.05)):
        f = floor(at(tag,"SpecialWind",tt,"RightFrontLeg","low"))
        burst(tag, "SpecialWind", f"Scrape{k}", tt, f, 5, DIRT, spread=3, up=2, size=0.7, dur=0.45, seed=51+k, cone=(90,40), start=0.5)
    for k, (tt, leg) in enumerate(((0.0,"LeftBackLeg"),(0.0,"RightFrontLeg"),(0.25,"RightBackLeg"),(0.25,"LeftFrontLeg"))):
        f = floor(at(tag,"Charge",tt,leg,"low"))
        burst(tag, "Charge", f"Kick{k}", tt, f, 4, DUST, spread=3.5, up=2, size=0.9, dur=0.45, seed=55+k, cone=(90,35), start=0.5)
    h = at(tag,"SpecialHit",0.1,"Head_HornGlow")
    pop(tag, "SpecialHit", "Star", star(GOLDG, 1.4), 0.1, h + Vector((0,-1.5,0)), s1=1.3)
    burst(tag, "SpecialHit", "Spark", 0.1, h, 10, GOLDG, spread=4, up=3, size=0.6, dur=0.5, glow=True, seed=59)
    s = floor(sum((at(tag,"SpecialHit",0.6,q,"low") for q in ("LeftFrontLeg","RightFrontLeg")), Vector())/2)
    ring(tag, "SpecialHit", "GoldWave", 0.6, s, 2, 16, GOLDG, dur=0.6, glow=True, size=(1.4,1.4,0.6))
    ring(tag, "SpecialHit", "DustWave", 0.65, s, 2, 11, DUST, dur=0.55)
    burst(tag, "SpecialHit", "Dust", 0.6, s, 12, DUST, spread=8, up=4, size=1.1, dur=0.75, seed=60, start=5)
    pound(tag, ("LeftFrontLeg","RightFrontLeg"))

CROWN = [((3.4,3.4,1.1),(0,0,0),(0,0,0),(232,172,24),False)] + [((0.9,0.9,1.3),(x,y,1.15),(0,0,0),(232,172,24),False)
         for x,y in ((-1.25,-1.25),(1.25,-1.25),(1.25,1.25),(-1.25,1.25))] + [((0.8,0.35,0.8),(0,-1.75,0.1),(0,45,0),(230,40,50),True)]
def fx_B07():
    tag = "B07"; clear(tag)
    rig = bpy_rig(tag)
    o = at(tag,"Strike",0.55,"RightHand_Orb")
    pop(tag, "Strike", "Star", star(BLUEG), 0.55, o + Vector((0,-1.5,0)))
    burst(tag, "Strike", "Spark", 0.55, o, 8, BLUEG, spread=3.5, up=2, size=0.55, dur=0.45, glow=True, seed=70)
    t0 = at(tag,"Walk",0.0,"RightHand_Gold","low")
    burst(tag, "Walk", "Tap", 0.0, floor(t0), 4, GOLDG, spread=1.6, up=1, size=0.4, dur=0.3, glow=True, seed=71, start=0.3)
    # ROYAL DECREE: the orb swells with light while sparkles circle it, the scepter slams down and crowns rain on the arena
    og = rest(tag, "RightHand_Orb")
    glow(tag, "SpecialWind", "OrbGlow", [((3.0,3.0,3.0),(0,0,0),(45,0,45),BLUEG,True)], (rig,"RightHand"), og, 0.3, 2.0, 0.4, 1.4, 5)
    orbit(tag, "SpecialWind", "Sparkle", GOLDG, (rig,"RightHand"), og, 2.8, 0.4, 2.0, n=5, turns=2.0, size=0.5)
    b = floor(at(tag,"SpecialHit",0.15,"RightHand_Gold","low"))
    ring(tag, "SpecialHit", "GoldWave", 0.15, b, 1.5, 14, GOLDG, dur=0.55, glow=True, size=(1.3,1.3,0.6))
    burst(tag, "SpecialHit", "Spark", 0.15, b, 10, GOLDG, spread=5, up=5, size=0.6, dur=0.6, glow=True, seed=72)
    rain(tag, "SpecialHit", "Crown", CROWN, 0.4, (0,-12,0), 10, 15, height=24, fall=0.45, gap=0.08, seed=73, land_rgb=GOLDG, land_glow=True)
    pound(tag, ("LeftHand","RightHand"))

TORPEDO = [((1.3,1.3,3.4),(0,0,0),(0,0,0),(150,160,172),False), ((1.0,1.0,0.9),(0,0,2.1),(0,0,0),(220,50,40),False),
           ((0.25,2.2,0.9),(0,0,-1.3),(0,0,0),(80,90,100),False), ((2.2,0.25,0.9),(0,0,-1.3),(0,0,0),(80,90,100),False),
           ((0.9,0.9,0.9),(0,0,-2.1),(0,0,45),ORANGEG,True)]
def fx_B08():
    tag = "B08"; clear(tag)
    rig = bpy_rig(tag)
    for k,(tt,leg) in enumerate(((0.0,"LeftLeg"),(0.7,"RightLeg"))):
        f = floor(at(tag,"Walk",tt,leg,"low"))
        burst(tag, "Walk", f"Stomp{k}", tt, f, 5, DUST, spread=3, up=1.5, size=0.8, dur=0.4, seed=80+k, start=1.5)
    d = at(tag,"Strike",0.55,"RightHand","low")
    pop(tag, "Strike", "Star", star((255,230,120)), 0.55, d + Vector((0,-1.5,0)))
    burst(tag, "Strike", "Spark", 0.55, d, 10, (255,220,90), spread=3.5, up=2.5, size=0.45, dur=0.45, glow=True, seed=82)
    # FULL PAYLOAD: tubes vent steam, each launch sends a torpedo arcing out with a smoke trail and an explosion,
    # then the boosters fire for the jump and the landing stomps a shockwave
    tube = at(tag,"SpecialWind",0.5,"Body_Metal","top")
    for k, tt in enumerate((0.3, 0.6, 0.9)):
        burst(tag, "SpecialWind", f"Steam{k}", tt, tube, 4, (230,230,235), spread=1.5, up=4, size=0.9, dur=0.6, seed=83+k, start=0.2)
    t0 = at(tag,"SpecialThrow",0.05,"Body_Metal","top") + Vector((0,0,1.5)); land = Vector((0,-22,1.0))
    projectile(tag, "SpecialThrow", "Torpedo", TORPEDO, 0.05, 0.9, t0, land, height=12, spin=(130,0,0), steps=8, scale=1.5)
    for k in range(5):
        u = (k+1)/6; pos = t0.lerp(land, u) + Vector((0,0,12*4*u*(1-u)))
        burst(tag, "SpecialThrow", f"Smoke{k}", 0.05 + 0.85*u, pos, 3, (200,200,205), spread=0.8, up=1, size=1.0, dur=0.5, seed=86+k, start=0.2)
    pop(tag, "SpecialThrow", "Boom", star(ORANGEG, 1.6), 0.9, land + Vector((0,0,1.5)), s1=1.4, dur=0.4)
    burst(tag, "SpecialThrow", "Fire", 0.9, land, 12, ORANGEG, spread=5, up=4, size=0.9, dur=0.6, glow=True, seed=92)
    ring(tag, "SpecialThrow", "BoomRing", 0.9, floor(land), 1, 7, (90,90,96), dur=0.5)
    for leg in ("LeftLeg","RightLeg"):
        fp = rest(tag, leg + "_Mech", "low") - Vector((0,0,1.0))
        glow(tag, "SpecialHit", f"Booster{leg}", [((1.6,1.6,2.0),(0,0,0),(0,0,45),ORANGEG,True), ((0.9,0.9,1.4),(0,0,-1.4),(0,0,0),(255,230,120),True)],
             (rig, leg), fp, 0.25, 0.75, 0.6, 1.2, 4)
    ring(tag, "SpecialHit", "LaunchRing", 0.3, (0,0,0), 2, 9, DUST, dur=0.45)
    ring(tag, "SpecialHit", "StompWave", 0.8, (0,-1,0), 2, 17, DUST, dur=0.6)
    burst(tag, "SpecialHit", "StompDust", 0.8, (0,-1,0.5), 14, DUST, spread=9, up=5, size=1.2, dur=0.8, seed=93, start=6)
    pound(tag, ("LeftHand","RightHand"))

HAND = [((0.9,0.9,3.4),(0,0,0),(0,0,0),(232,226,208),False), ((1.8,0.9,1.1),(0,0,2.1),(0,0,0),(232,226,208),False)] + \
       [((0.4,0.4,1.4),(x,0,3.3),(0,(x*-14),0),(232,226,208),False) for x in (-0.6,0,0.6)] + [((0.4,0.4,1.0),(1.0,0,2.6),(0,-40,0),(232,226,208),False),
        ((0.5,0.5,0.5),(0,-0.6,1.0),(0,45,45),GREENG,True)]
def fx_B09():
    tag = "B09"; clear(tag)
    rig = bpy_rig(tag)
    h = at(tag,"Strike",0.55,"RightHand")
    pop(tag, "Strike", "Slash", slash(GREENG), 0.52, h + Vector((0,-1.5,0)), s0=0.6, s1=1.3, dur=0.3, rot_spin=0)
    burst(tag, "Strike", "Spark", 0.55, h, 7, GREENG, spread=3, up=1.5, size=0.5, dur=0.4, glow=True, seed=100)
    # SOUL STORM: souls swirl round its ribs, it takes off, skeleton hands claw up from the ground while it hovers, then it dives and crashes
    orbit(tag, "SpecialWind", "Soul", GREENG, (rig,"Body"), rest(tag,"Body_Soul"), 4.5, 0.15, 1.2, n=8, turns=1.5, size=0.8)
    ring(tag, "FlyUp", "Gust", 0.3, (0,0,0), 2, 12, DUST, dur=0.55)
    burst(tag, "FlyUp", "Dust", 0.3, (0,0,0.4), 10, DUST, spread=7, up=2.5, size=1.0, dur=0.6, seed=101, start=3)
    import math, random
    rnd = random.Random(5)
    for i in range(6):
        a = 2*math.pi*i/6 + 0.3; p = Vector((math.cos(a)*12, math.sin(a)*12 - 2, 0)); yaw = math.degrees(a) + 90
        ob = F["prop"](tag, f"Hover_Hand{i}", HAND)
        bb = F["base"](tag)
        K = 1.9
        F["animate"](ob, tag, "Hover", [(0.0, bb+p-Vector((0,0,4.2*K)), (rnd.uniform(-10,10),0,yaw), K, "OUT"), (0.35, bb+p+Vector((0,0,0.2)), (rnd.uniform(-15,15),0,yaw), K, "IO"),
                                        (0.6, bb+p+Vector((0,0,0.5)), (0,10,yaw), K, "IO"), (0.85, bb+p-Vector((0,0,1.5*K)), (0,0,yaw), K, "IN"), (1.0, bb+p-Vector((0,0,4.0*K)), (0,0,yaw), K, "LIN")])
        burst(tag, "Hover", f"HandDirt{i}", 0.0, p+Vector((0,0,0.3)), 4, DIRT, spread=2, up=1.5, size=0.6, dur=0.4, seed=110+i, start=0.5)
    for k, tt in enumerate((0.2, 0.4)):
        burst(tag, "SpecialDive", f"Trail{k}", tt, at(tag,"SpecialDive",tt,"Body_Soul"), 5, GREENG, spread=2, up=0.5, size=0.7, dur=0.4, glow=True, seed=120+k, start=1)
    ring(tag, "SpecialHit", "SoulWave", 0.1, (0,-2,0), 2, 18, GREENG, dur=0.65, glow=True, size=(1.4,1.4,0.6))
    ring(tag, "SpecialHit", "DustWave", 0.15, (0,-2,0), 2, 12, DUST, dur=0.55)
    burst(tag, "SpecialHit", "Souls", 0.1, (0,-2,1), 14, GREENG, spread=8, up=6, size=0.8, dur=0.8, glow=True, seed=122, start=4)
    pound(tag, ("LeftHand","RightHand"))

def rune_circle(r=11, n=28):
    import math
    bl = []
    for i in range(n):
        a = 2*math.pi*i/n; bl.append(((1.6,0.9,0.3),(math.cos(a)*r, math.sin(a)*r, 0),(0,0,math.degrees(a)+90),PURPG,True))
    for i in range(n//2):
        a = 2*math.pi*i/(n//2); rr = r*0.62; bl.append(((1.4,0.8,0.3),(math.cos(a)*rr, math.sin(a)*rr, 0),(0,0,math.degrees(a)+90),PURPG,True))
    for k in range(6):
        a = math.pi*k/3; bl.append(((0.6,r*1.2,0.28),(0,0,0),(0,0,math.degrees(a)),(140,60,220),True))
    for i in range(8):
        a = 2*math.pi*i/8 + 0.2; rr = r*0.81
        bl.append(((1.0,1.0,0.32),(math.cos(a)*rr, math.sin(a)*rr, 0),(0,0,45),(230,190,255),True))
    return bl
PILLAR = [((2.2,2.2,11),(0,0,5.5),(0,0,45),PURPG,True), ((1.2,1.2,12),(0,0,6),(0,0,0),(230,190,255),True), ((4.0,4.0,0.4),(0,0,0.2),(0,0,0),(140,60,220),True)]
def fx_B10():
    tag = "B10"; clear(tag)
    for k,(tt,leg) in enumerate(((0.0,"LeftLeg"),(0.9,"RightLeg"))):
        f = floor(at(tag,"Walk",tt,leg,"low"))
        burst(tag, "Walk", f"Stomp{k}", tt, f, 6, DUST, spread=4, up=1.8, size=0.9, dur=0.45, seed=130+k, start=2)
    h = at(tag,"Strike",0.55,"RightHand")
    pop(tag, "Strike", "Slash", slash(PURPG), 0.52, h + Vector((0,-2,0)), s0=0.7, s1=1.5, dur=0.3, rot_spin=0)
    burst(tag, "Strike", "Spark", 0.55, h, 9, PURPG, spread=4, up=2, size=0.6, dur=0.45, glow=True, seed=132)
    tl = floor(at(tag,"Strike",0.5,"Tail_Rune","low"))
    burst(tag, "Strike", "TailDust", 0.5, tl, 7, DUST, spread=5, up=2, size=1.0, dur=0.55, seed=133, cone=(0,80), start=1)
    # RUNE APOCALYPSE: a rune circle burns into the ground as it roars, it takes off, casts rune pillars that erupt across the arena,
    # then dives and crashes in a purple shockwave
    bb = F["base"](tag)
    ob = F["prop"](tag, "SpecialWind_RuneCircle", rune_circle(r=15, n=36))
    F["animate"](ob, tag, "SpecialWind", [(0.5, bb+Vector((0,0,0.15)), (0,0,0), 0.2, "OUT"), (0.8, bb+Vector((0,0,0.15)), (0,0,25), 1.05, "IO"),
                                          (1.2, bb+Vector((0,0,0.15)), (0,0,45), 0.95, "IO"), (1.6, bb+Vector((0,0,0.15)), (0,0,65), 1.05, "LIN")])
    burst(tag, "SpecialWind", "RuneSparks", 0.5, (0,0,0.5), 16, PURPG, spread=10, up=7, size=0.7, dur=1.0, glow=True, seed=134, start=4)
    ring(tag, "FlyUp", "Gust", 0.35, (0,0,0), 3, 16, DUST, dur=0.6)
    burst(tag, "FlyUp", "Dust", 0.35, (0,0,0.4), 12, DUST, spread=9, up=3, size=1.0, dur=0.6, seed=135, start=4)
    rig = bpy_rig(tag)
    for hand in ("LeftHand","RightHand"):
        pop(tag, "Cast", f"Charge{hand}", [((2.2,2.2,2.2),(0,0,0),(45,0,45),PURPG,True)], 0.25, at(tag,"Cast",0.32,hand), s0=0.3, s1=1.4, dur=0.3)
    import math, random
    rnd = random.Random(9)
    for i in range(10):
        a = 2*math.pi*i/10 + rnd.uniform(-0.2,0.2); r = rnd.uniform(9, 22)
        p = Vector((math.cos(a)*r, math.sin(a)*r - 6, 0)); ts = 0.45 + i*0.03
        ob = F["prop"](tag, f"Cast_Pillar{i}", PILLAR)
        F["animate"](ob, tag, "Cast", [(ts, bb+p-Vector((0,0,11)), (0,0,0), 1.0, "OUT"), (ts+0.15, bb+p, (0,0,20), 1.0, "IO"),
                                       (ts+0.4, bb+p, (0,0,40), 1.0, "IN"), (ts+0.55, bb+p-Vector((0,0,4)), (0,0,50), 0.3, "LIN")])
        burst(tag, "Cast", f"PillarBurst{i}", ts, p+Vector((0,0,0.5)), 5, PURPG, spread=3, up=3, size=0.7, dur=0.45, glow=True, seed=140+i, start=1)
    ring(tag, "SpecialHit", "RuneWave", 0.1, (0,-2,0), 3, 24, PURPG, dur=0.7, glow=True, size=(1.5,1.5,0.6))
    ring(tag, "SpecialHit", "DustWave", 0.15, (0,-2,0), 3, 16, DUST, dur=0.6)
    burst(tag, "SpecialHit", "Shards", 0.1, (0,-2,1), 16, PURPG, spread=11, up=7, size=0.9, dur=0.85, glow=True, seed=150, start=6)
    pop(tag, "SpecialHit", "Flash", star(PURPG, 2.2), 0.1, Vector((0,-8,4)), s1=1.5, dur=0.4)
    pound(tag, ("LeftHand","RightHand"), r1=13)
