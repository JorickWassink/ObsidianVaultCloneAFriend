
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop, make = L["P"], L["drop"], L["make"]
tag, k = "B09", 1.2
def X(n, p):   # wings half open and the tail alive in every core pose
    p = dict(p); p.setdefault("LW", [0,0,10]); p.setdefault("RW", [0,0,-10]); p.setdefault("T", [0,0,0]); return p
def W(p, fold=10, fwd=0, tail=0, tl=0):
    return P(p, LW=[fwd,0,fold], RW=[fwd,0,-fold], T=[tl,tail,0])
def idle_keys(IDLE, BREATH, LOOK):   # rattling breath, jaw twitches, wings creak, tail swishes
    A1 = W(P(BREATH, H=[4,10,0]), 4, 0, 14)
    A2 = W(P(IDLE, H=[-2,-12,4]), 14, 4, -14)
    TW = W(P(BREATH, H=[6,0,-6], LUA=[14,0,-12], RUA=[14,0,12]), 0, -4, 6)
    return [(0,W(IDLE),"IO"),(0.9,A1,"IO"),(1.8,A2,"IO"),(2.1,TW,"BACK"),(2.4,A2,"IO"),(3.2,W(IDLE),"IO")]
def lift_tail(p):   # leaning back would push the tail tip into the floor: it lifts to match
    p = dict(p); b = p.get("B",[0]); t = list(p.get("T",[0,0,0]))+[0]*3
    t[0] -= 1.4*max(0, b[0]); p["T"] = t[:6]; return p
_mk = L["make"]
L["make"] = lambda tg, nm, ln, keys, **kw: _mk(tg, nm, ln, [(a, lift_tail(p), e) for a,p,e in keys], **kw)
make = L["make"]
S = L["biped_core"](tag, k, arms_out=6, extra=X, extra_idle=idle_keys, skip=("Walk",), crouch=0.5)
IDLE = W(S["IDLE"])
# WALK: creepy skitter - hunched low, quick short steps, claws reaching, wings half open twitching, tail swishing
def sk(side):
    p = drop(IDLE, 0.4, -12, side*4, side*8)
    p = P(p, H=[8,-side*10,side*5], LUA=[40-side*12,0,-14], RUA=[40+side*12,0,14], LLA=[50,0,0], RLA=[50,0,0])
    leg = "RL" if side > 0 else "LL"
    l = list(p[leg]); l[0] += 16; l[4] += 0.9; p[leg] = l
    return W(p, 22+side*4, 6, side*22, -4)
def mid(side):
    p = drop(IDLE, 0.55, -13, 0, side*2)
    return W(P(p, H=[10,side*4,0], LUA=[38,0,-12], RUA=[38,0,12], LLA=[56,0,0], RLA=[56,0,0]), 18, 6, side*8, -4)
make(tag, "Walk", 0.9, [(0,sk(1),"OUT"),(0.22,mid(1),"IN"),(0.45,sk(-1),"OUT"),(0.67,mid(-1),"IN"),(0.9,sk(1),"OUT")], loop=True)
# STRIKE: right claw rears up and back, rakes down across, lands at 0.55
REAR = W(P(drop(IDLE, -0.2, 8, 0, 20), H=[12,-8,0], RUA=[150,0,42], RLA=[30,0,0], LUA=[20,0,-20]), 0, 0, -16, -4)
RAKE = W(P(drop(IDLE, 0.45, -16, 0, -22), H=[-2,12,0], RUA=[30,0,-6], RLA=[10,0,0], LUA=[-10,0,-14]), 14, 8, 18)
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.4,REAR,"IN"),(0.55,RAKE,"OUT"),(0.75,RAKE,"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# SOUL STORM: screeches with wings flared (holds) -> flaps up into the air -> hovers (loops, skeleton hands rise below)
#   -> dives (SpecialDive) -> crashes down (SpecialHit, impact 0.1)
FLARE = W(P(drop(IDLE, 0.4, 10), H=[14,0,0], LUA=[60,0,-50], RUA=[60,0,50], LLA=[40,0,0], RLA=[40,0,0]), -24, -6, 0, -4)
make(tag, "SpecialWind", 1.2, [(0,IDLE,"OUT"),(0.4,FLARE,"BACK"),(0.8,P(FLARE,H=[16,0,6]),"IO"),(1.2,P(FLARE,H=[16,0,-6]),"IO")], hold=True)
def air(h, up, lean=0, wing=0):
    return W(P(None, B=[lean,0,0,0,h,0], H=[4-lean*0.5,0,0], LUA=[30,0,-20], RUA=[30,0,20], LLA=[40,0,0], RLA=[40,0,0],
               LL=[-12,0,0], RL=[-8,0,0]), wing, 0, 0, -10)
make(tag, "FlyUp", 1.0, [(0,FLARE,"IN"),(0.15,W(P(drop(IDLE,0.6,-6)),20,0),"OUT"),(0.4,air(4*k,1,0,-34),"OUT"),(0.7,air(7*k,1,0,24),"IO"),(1.0,air(9*k,1,0,-30),"IO")], events={"liftoff":0.3})
make(tag, "Hover", 1.0, [(0,air(9*k,1,0,-30),"IO"),(0.5,air(8.4*k,1,4,26),"IO"),(1.0,air(9*k,1,0,-30),"IO")], loop=True, events={"flap":0.0})
DIVE = W(P(None, B=[-34,0,0,0,6*k,-4], H=[-6,0,0], LUA=[110,0,-14], RUA=[110,0,14], LLA=[10,0,0], RLA=[10,0,0], LL=[-20,0,0], RL=[-20,0,0]), 30, 10, 0, 8)
make(tag, "SpecialDive", 0.6, [(0,air(9*k,1,0,-30),"IN"),(0.2,P(air(10*k,1,-10,-20)),"IN"),(0.6,DIVE,"IN")])
CRASH = W(P(drop(IDLE, 0.9, -24), H=[4,0,0], LUA=[60,0,-50], RUA=[60,0,50], LLA=[20,0,0], RLA=[20,0,0]), -16, 4, 0, -6)
make(tag, "SpecialHit", 1.1, [(0,DIVE,"OUT"),(0.1,CRASH,"OUT"),(0.5,P(CRASH,H=[12,0,0]),"IO"),(1.1,IDLE,"LIN")], events={"impact":0.1})

L["make"] = _mk
