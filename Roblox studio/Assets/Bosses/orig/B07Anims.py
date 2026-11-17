
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop, make = L["P"], L["drop"], L["make"]
tag, k = "B07", 1.0
def keep(p, tilt=0):
    """keeps the scepter upright in the right paw (tilt+ leans the orb back, tilt- forward)"""
    ua = p.get("RUA",[0,0,0]); la = p.get("RLA",[0,0,0])
    p = dict(p); p["RH"] = [-(ua[0]+la[0])+tilt, 0, -ua[2]]
    return p
def calm(p):
    """the big mane sits right on the collar: the head only nods and turns a little, the body does the acting"""
    p = dict(p)
    if "H" in p:
        h = list(p["H"])+[0]*3
        p["H"] = [max(-2,min(2,h[0])), max(-7,min(7,h[1])), 0]
    for a, sg in (("LUA",-1),("RUA",1)):   # the mane overhangs the shoulders: arms stay low, elbows do the lifting
        if a in p:
            v = list(p[a])+[0]*3
            p[a] = [max(-30,min(20,v[0])), v[1], sg*max(0,min(32,sg*v[2]))] + v[3:6]
    return p
X = lambda n, p: keep(calm(p))
def idle_keys(IDLE, BREATH, LOOK):   # chin up, looks over its kingdom, taps the scepter once
    PROUD = keep(P(BREATH, B=[3,10,0], H=[2,6,0]))
    PROUD2 = keep(P(BREATH, B=[3,-10,0], H=[2,-6,0]))
    LIFT = keep(P(IDLE, RUA=[16,0,6], RLA=[10,0,0]))
    TAP = keep(P(drop(IDLE, 0.08), RUA=[2,0,6], RLA=[6,0,0]))
    return [(0,IDLE,"IO"),(0.8,PROUD,"IO"),(1.6,PROUD2,"IO"),(2.2,IDLE,"IO"),(2.45,LIFT,"OUT"),(2.6,TAP,"IN"),(3.2,IDLE,"IO")]
ROAR = keep(P(drop(P(None, B=[0,0,0], H=[0,0,0], LUA=[4,0,-6], RUA=[4,0,6], LLA=[8,0,0], RLA=[8,0,0]), -0.5*k, 8), H=[2,0,0], LUA=[16,0,-34], LLA=[60,0,0], RUA=[18,0,32], RLA=[60,0,0]))
_mk = L["make"]
L["make"] = lambda tg, nm, ln, keys, **kw: _mk(tg, nm, ln, [(a, keep(calm(p)), e) for a,p,e in keys], **kw)
S = L["biped_core"](tag, k, arms_out=6, extra=X, extra_idle=idle_keys, skip=("Walk",), crouch=0.5, intro_roar=ROAR)
L["make"] = _mk
IDLE = S["IDLE"]
# WALK: regal strut - chest out, knees high, the scepter taps the floor like a cane on every right step
def step(side, staff):
    p = drop(IDLE, 0.1, 4, side*2, side*5)
    p = P(p, H=[0, -side*4, 0], LUA=[-side*14, 0, -10], LLA=[16,0,0])
    lift = "RL" if side > 0 else "LL"
    l = list(p[lift]); l[0] += 22; l[4] += 1.0; p[lift] = l
    if staff == "plant": p = keep(P(p, RUA=[10,0,6], RLA=[4,0,0]), -4)
    else: p = keep(P(p, RUA=[20,0,6], RLA=[20,0,0]), -10)
    return p
MID = keep(P(drop(IDLE, -0.15, 4), H=[0,0,0], LUA=[2,0,-10], RUA=[18,0,6], RLA=[8,0,0]), -6)
make(tag, "Walk", 1.3, [(0,step(-1,"plant"),"OUT"),(0.33,MID,"IN"),(0.65,step(1,"lift"),"OUT"),(0.98,MID,"IN"),(1.3,step(-1,"plant"),"OUT")], loop=True, events={"tap":0.0})
# STRIKE: winds the orb back over its shoulder, bonks it down in front, lands at 0.55
WIND = keep(P(drop(IDLE, -0.2, 6, 0, -12), H=[1,0,0], RUA=[20,0,25], RLA=[60,0,0], LUA=[16,0,-16]), 40)
BONK = keep(P(drop(IDLE, 0.3, -10, 0, 8), H=[0,0,0], RUA=[20,0,10], RLA=[40,0,0], LUA=[-10,0,-14]), -60)
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.42,WIND,"IN"),(0.55,BONK,"OUT"),(0.75,BONK,"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# ROYAL DECREE: raises the scepter high with the orb charging (holds), slams the butt down, crowns rain on the arena
DECREE = keep(P(drop(IDLE, -0.3, 6), H=[2,0,0], RUA=[20,0,30], RLA=[70,0,0], LUA=[14,0,-28], LLA=[60,0,0]))
DECREE2 = keep(P(DECREE, RUA=[22,0,32], RLA=[80,0,0], LUA=[16,0,-30], LLA=[70,0,0]))
make(tag, "SpecialWind", 2.0, [(0,IDLE,"OUT"),(0.6,DECREE,"IO"),(1.3,DECREE2,"IO"),(2.0,DECREE,"LIN")], hold=True)
SLAM = keep(P(drop(IDLE, 0.4, -6), H=[4,0,0], RUA=[16,0,6], RLA=[20,0,0], LUA=[16,0,-26], LLA=[20,0,0]))
make(tag, "SpecialHit", 1.1, [(0,keep(P(DECREE, RUA=[22,0,32], RLA=[85,0,0])),"IN"),(0.15,SLAM,"OUT"),(0.6,P(SLAM,H=[2,0,0]),"IO"),(1.1,IDLE,"LIN")], events={"impact":0.15})
# DEFEAT: staggers and leans heavily on its scepter, crown askew
HIT = keep(P(drop(IDLE, -0.1, 6, 3), H=[2,0,0], LUA=[10,0,-30], RUA=[20,0,10]))
LEAN = keep(P(drop(IDLE, 0.3, -6, -3, 6), H=[-2,4,0], LUA=[4,0,-20], LLA=[6,0,0], RUA=[10,0,14], RLA=[24,0,0]), -6)
make(tag, "Defeat", 1.4, [(0,IDLE,"OUT"),(0.2,HIT,"IN"),(0.65,LEAN,"OUT"),(1.4,P(LEAN,H=[-2,6,0]),"LIN")], hold=True)
