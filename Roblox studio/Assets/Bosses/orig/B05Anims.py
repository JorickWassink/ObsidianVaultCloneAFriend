
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop = L["P"], L["drop"]
tag, k = "B05", 1.1
def pin(p):
    """keeps the rolling pin pointing sensibly: when the right arm is raised forward the wrist turns the roller
    level-forward instead of letting it point straight up (poses that set RH themselves are left alone)"""
    if "RH" in p or "RUA" not in p: return p
    ua = p["RUA"][0]; la = p.get("RLA",[0])[0]
    if 30 <= ua <= 125:
        p = dict(p); p["RH"] = [max(-40, -(ua + la) + 10), 0, 0]
    return p
_mk = L["make"]
L["make"] = lambda tg, nm, ln, keys, **kw: _mk(tg, nm, ln, [(a, pin(p), e) for a,p,e in keys], **kw)
make = L["make"]
def idle_keys(IDLE, BREATH, LOOK):   # breathes heavy, then beats its chest left-right-left
    BEAT_L = P(BREATH, LUA=[84,0,6], LLA=[52,0,0], H=[6,0,0])
    BEAT_R = P(BREATH, LUA=[70,0,4], LLA=[44,0,0], H=[6,0,0])
    return [(0,IDLE,"IO"),(1.0,BREATH,"IO"),(1.35,BEAT_L,"OUT"),(1.55,BREATH,"IN"),(1.75,BEAT_R,"OUT"),(1.95,BREATH,"IN"),(2.15,BEAT_L,"OUT"),(2.6,IDLE,"IO")]
ROAR = P(drop(P(None, B=[0,0,0], H=[0,0,0], LUA=[4,0,-4], RUA=[4,0,4], LLA=[8,0,0], RLA=[8,0,0]), -0.5*k, 10), H=[10,0,0], LUA=[110,0,-50], RUA=[110,0,50], LLA=[40,0,0], RLA=[6,0,0])
S = L["biped_core"](tag, k, arms_out=4, extra_idle=idle_keys, skip=("Walk",), crouch=0.5, intro_roar=ROAR)
IDLE = S["IDLE"]
# WALK: knuckle-walk - leaning forward, arms swinging onto the fists, heavy shoulders rolling
def step(side):
    p = drop(IDLE, 0.25, -8, side*5, side*7)
    p = P(p, H=[6, -side*5, 0], LUA=[side*26, 0, -6], RUA=[-side*16, 0, 6], RH=[side*12, 0, 0], LLA=[-side*6+6,0,0], RLA=[side*6+6,0,0])
    lift = "RL" if side > 0 else "LL"
    l = list(p[lift]); l[0] += 14; l[4] += 0.8; p[lift] = l
    return p
MID = P(drop(IDLE, 0.05, -8), H=[6,0,0], LUA=[4,0,-6], RUA=[4,0,6])
make(tag, "Walk", 1.3, [(0,step(1),"OUT"),(0.33,MID,"IN"),(0.65,step(-1),"OUT"),(0.98,MID,"IN"),(1.3,step(1),"OUT")], loop=True)
# STRIKE: rolling pin overhead smash, lands at 0.55
UP = P(drop(IDLE, -0.3, 8, 0, -10), H=[10,0,0], RUA=[160,0,18], RLA=[8,0,0], LUA=[20,0,-16])
SMASH = P(drop(IDLE, 0.4, -16, 0, 6), H=[8,0,0], RUA=[24,0,6], RLA=[0,0,0], RH=[-13,0,0], LUA=[10,0,-18])
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.42,UP,"IN"),(0.55,SMASH,"OUT"),(0.75,SMASH,"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# KITCHEN CATASTROPHE: reaches back for flour (holds), throws a flour bomb (x3, release at 0.12), double fist slam (impact 0.15)
REACH = P(drop(IDLE, 0.1, 4, 0, 14), H=[4,18,0], LUA=[-46,0,-20], LLA=[70,0,0], RUA=[24,0,20])
make(tag, "SpecialWind", 1.2, [(0,IDLE,"OUT"),(0.45,REACH,"IO"),(1.2,P(REACH, LUA=[-52,0,-22]),"LIN")], hold=True)
COCK = P(drop(IDLE, -0.2, 8, 0, 18), H=[6,10,0], LUA=[150,0,-14], LLA=[60,0,0], RUA=[30,0,20])
TOSS = P(drop(IDLE, 0.3, -12, 0, -16), H=[6,-8,0], LUA=[70,0,-6], LLA=[6,0,0], RUA=[10,0,22])
make(tag, "SpecialThrow", 0.55, [(0,COCK,"IN"),(0.12,TOSS,"OUT"),(0.3,P(TOSS,LUA=[50,0,-8]),"IO"),(0.55,P(IDLE, LUA=[-20,0,-14], LLA=[40,0,0]),"LIN")], events={"release":0.12})
RAISE = P(drop(IDLE, -0.4, 10), H=[14,0,0], LUA=[165,0,-20], RUA=[165,0,20], LLA=[30,0,0], RLA=[6,0,0])
POUND = P(drop(IDLE, 0.5, -20), H=[10,0,0], LUA=[46,0,-14], RUA=[46,0,14], LLA=[0,0,0], RLA=[0,0,0])
make(tag, "SpecialHit", 1.1, [(0,RAISE,"IN"),(0.15,POUND,"OUT"),(0.6,P(POUND,H=[4,0,0]),"IO"),(1.1,IDLE,"LIN")], events={"impact":0.15})

# gentler head on the defeat (the scarf sits close under its chin)
HIT = P(drop(IDLE, -0.2*k, 10, 5), H=[6,0,0], LUA=[30,0,-45], RUA=[30,0,45])
SLUMP = P(drop(IDLE, 0.5*k, -14, 6), H=[-2,0,4], LUA=[5,0,-25], RUA=[5,0,25], LLA=[0,0,0], RLA=[0,0,0])
make(tag, "Defeat", 1.4, [(0,IDLE,"OUT"),(0.2,HIT,"IN"),(0.65,SLUMP,"OUT"),(1.4,P(SLUMP,H=[-4,0,5]),"LIN")], hold=True)

L["make"] = _mk
