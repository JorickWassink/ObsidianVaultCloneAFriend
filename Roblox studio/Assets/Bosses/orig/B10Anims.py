
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop = L["P"], L["drop"]
tag, k = "B10", 1.5
def lift_tail(p):   # leaning back would push the tail tip into the floor: it lifts to match
    p = dict(p); b = p.get("B",[0]); t = list(p.get("T",[0,0,0]))+[0]*3
    t[0] -= 1.4*max(0, b[0]); p["T"] = t[:6]; return p
_mk = L["make"]
L["make"] = lambda tg, nm, ln, keys, **kw: _mk(tg, nm, ln, [(a, lift_tail(p), e) for a,p,e in keys], **kw)
make = L["make"]
def W(p, fold=16, fwd=0, tail=0, tl=0):
    return P(p, LW=[fwd,0,fold], RW=[fwd,0,-fold], T=[tl,tail,0])
def X(n, p):
    p = dict(p); p.setdefault("LW", [0,0,16]); p.setdefault("RW", [0,0,-16]); p.setdefault("T", [-6,0,0]); return p
def idle_keys(IDLE, BREATH, LOOK):   # slow heavy breaths, the tail drags side to side, wings shift
    A1 = W(P(BREATH, H=[2,8,0]), 12, 0, 14)
    A2 = W(P(BREATH, H=[2,-8,0]), 18, 0, -14)
    return [(0,W(IDLE),"IO"),(1.2,A1,"IO"),(2.0,W(IDLE),"IO"),(3.2,A2,"IO"),(4.0,W(IDLE),"IO")]
S = L["biped_core"](tag, k, arms_out=6, extra=X, extra_idle=idle_keys, skip=("Walk",), crouch=0.12)
IDLE = W(S["IDLE"])
# WALK: slow heavy stomp - wings folded, tail swaying behind, the head stays level while the body rolls
def stomp(side):
    p = drop(IDLE, 0.25, -3, side*4, side*6)
    p = P(p, H=[3,-side*6,-side*4], LUA=[-side*14,0,-8], RUA=[side*14,0,8], LLA=[16,0,0], RLA=[16,0,0])
    return W(p, 24, 0, -side*18)
def raise_(side):
    p = drop(IDLE, -0.2, -2, -side*2, side*3)
    p = P(p, H=[2,-side*3,side*2], LUA=[-side*6,0,-8], RUA=[side*6,0,8], LLA=[14,0,0], RLA=[14,0,0])
    leg = "LL" if side > 0 else "RL"
    l = list(p[leg]); l[0] += 14; l[4] += 0.4; p[leg] = l
    return W(p, 24, 0, 0)
make(tag, "Walk", 1.8, [(0,stomp(1),"OUT"),(0.45,raise_(-1),"IO"),(0.9,stomp(-1),"OUT"),(1.35,raise_(1),"IO"),(1.8,stomp(1),"OUT")], loop=True, events={"stomp":0.0, "stomp2":0.9})
# STRIKE: twists away swinging the tail around, then a heavy right claw swipe, lands at 0.55
COIL = W(P(drop(IDLE, 0.12, -4, 0, 26), H=[4,-14,0], RUA=[60,0,40], RLA=[50,0,0], LUA=[20,0,-20]), 20, 0, 30, -8)
SWIPE = W(P(drop(IDLE, 0.2, -10, 0, -24), H=[0,14,0], RUA=[56,0,4], RLA=[6,0,0], LUA=[-10,0,-16]), 20, 0, -34)
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.4,COIL,"IN"),(0.55,SWIPE,"OUT"),(0.75,SWIPE,"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# RUNE APOCALYPSE: roars with wings flared and runes blazing (holds) -> takes off -> hovers (loops) -> casts runes that erupt
#   across the arena (Cast, erupt 0.45) -> dives (SpecialDive) -> crashes (SpecialHit, impact 0.1)
ROAR = W(P(drop(IDLE, 0.3, 10), H=[16,0,0], LUA=[60,0,-50], RUA=[60,0,50], LLA=[40,0,0], RLA=[40,0,0]), -26, -4, 0, -4)
make(tag, "SpecialWind", 1.6, [(0,IDLE,"OUT"),(0.5,ROAR,"BACK"),(1.0,P(ROAR,H=[18,6,0]),"IO"),(1.6,P(ROAR,H=[18,-6,0]),"IO")], hold=True, events={"roar":0.5})
def air(h, lean=0, wing=0, arms=30):
    return W(P(None, B=[lean,0,0,0,h,0], H=[4-lean*0.5,0,0], LUA=[arms,0,-20], RUA=[arms,0,20], LLA=[40,0,0], RLA=[40,0,0],
               LL=[-14,0,0], RL=[-10,0,0]), wing, 0, 0, -10)
make(tag, "FlyUp", 1.2, [(0,ROAR,"IN"),(0.2,W(P(drop(IDLE,0.6,-6)),20,0),"OUT"),(0.5,air(4*k,0,-36),"OUT"),(0.85,air(7*k,0,24),"IO"),(1.2,air(9*k,0,-32),"IO")], events={"liftoff":0.35})
make(tag, "Hover", 1.2, [(0,air(9*k,0,-32),"IO"),(0.6,air(8.4*k,4,26),"IO"),(1.2,air(9*k,0,-32),"IO")], loop=True, events={"flap":0.0})
CHARGE = air(9.4*k, 8, -36, 120)
CAST = W(P(air(8.6*k, -8, 20, 70), H=[-4,0,0], LLA=[0,0,0], RLA=[0,0,0]), 20, 0, 0, -10)
make(tag, "Cast", 1.0, [(0,air(9*k,0,-32),"IO"),(0.3,CHARGE,"IN"),(0.45,CAST,"OUT"),(0.7,CAST,"IO"),(1.0,air(9*k,0,-32),"IO")], events={"erupt":0.45})
DIVE = W(P(None, B=[-34,0,0,0,6*k,-4], H=[-6,0,0], LUA=[110,0,-14], RUA=[110,0,14], LLA=[10,0,0], RLA=[10,0,0], LL=[-20,0,0], RL=[-20,0,0]), 18, 4, 0, -4)
make(tag, "SpecialDive", 0.7, [(0,air(9*k,0,-32),"IN"),(0.25,air(10*k,-10,-20),"IN"),(0.7,DIVE,"IN")])
CRASH = W(P(drop(IDLE, 0.35, -16), H=[4,0,0], LUA=[60,0,-50], RUA=[60,0,50], LLA=[20,0,0], RLA=[20,0,0]), -16, 4, 0, -6)
make(tag, "SpecialHit", 1.2, [(0,DIVE,"OUT"),(0.1,CRASH,"OUT"),(0.55,P(CRASH,H=[14,0,0]),"IO"),(1.2,IDLE,"LIN")], events={"impact":0.1})
# DEFEAT: the runes flicker out, it sags, wings droop open and its head drops
HIT = W(P(drop(IDLE, -0.1, 8, 3), H=[10,0,0], LUA=[30,0,-40], RUA=[30,0,40]), 6, 0, 10, -10)
SAG = W(P(drop(IDLE, 0.15, -8), H=[-10,0,6], LUA=[6,0,-20], RUA=[6,0,20], LLA=[4,0,0], RLA=[4,0,0]), 22, 0, -6, -8)
make(tag, "Defeat", 1.4, [(0,IDLE,"OUT"),(0.2,HIT,"IN"),(0.7,SAG,"OUT"),(1.4,P(SAG,H=[-12,0,8]),"LIN")], hold=True)
L["make"] = _mk
