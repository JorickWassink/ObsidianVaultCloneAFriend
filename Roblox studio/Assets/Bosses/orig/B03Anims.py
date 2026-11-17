
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop, make = L["P"], L["drop"], L["make"]
tag, k = "B03", 0.85
def idle_keys(IDLE, BREATH, LOOK):   # shifty: glances left and right, rubs paws
    RUB = P(BREATH, LUA=[44,0,-4], RUA=[44,0,4], LLA=[66,0,0], RLA=[66,0,0], H=[2,0,0])
    return [(0,IDLE,"IO"),(0.6,P(BREATH,H=[0,14,0]),"IO"),(1.2,RUB,"IO"),(1.6,P(RUB,LUA=[48,0,-2],RUA=[40,0,2]),"IO"),(2.0,P(BREATH,H=[0,-14,0]),"IO"),(2.6,IDLE,"IO")]
S = L["biped_core"](tag, k, arms_out=8, extra_idle=idle_keys, skip=("Walk",))
IDLE = S["IDLE"]
# WALK: sneaky tiptoe - hunched, paws held up in front, high careful steps, head scanning
HUNCH = P(drop(IDLE, 0.3, -12), LUA=[48,0,-10], RUA=[48,0,10], LLA=[56,0,0], RLA=[56,0,0])
def tip(side, look):
    p = P(HUNCH, H=[2, look*0.7, 0], B=list(HUNCH["B"]))
    b = list(p["B"]); b[2] = side*3; p["B"] = b
    lift = "RL" if side > 0 else "LL"
    l = list(p[lift]); l[0] += 24; l[4] += 1.0; p[lift] = l
    return p
make(tag, "Walk", 1.4, [(0,tip(1,14),"IO"),(0.35,P(HUNCH,H=[2,0,0]),"IO"),(0.7,tip(-1,-14),"IO"),(1.05,P(HUNCH,H=[2,0,0]),"IO"),(1.4,tip(1,14),"IO")], loop=True)
# STRIKE: right claw hook, lands at 0.55
PRE = P(drop(IDLE, 0.2, -6, 0, -18), RUA=[-24,0,34], RLA=[40,0,0], LUA=[40,0,-14], LLA=[56,0,0])
HOOK = P(drop(IDLE, 0.3, -12, 0, 24), RUA=[84,0,-6], RLA=[14,0,0], LUA=[30,0,-16], LLA=[50,0,0], H=[4,-6,0])
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.3,PRE,"IN"),(0.55,HOOK,"OUT"),(0.75,HOOK,"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# COIN TOSS: reaches back into the sack (holds), then hurls the loot (release at 0.12)
REACH = P(drop(IDLE, -0.2, 6, 0, -12), RUA=[138,0,34], RLA=[56,0,0], LUA=[20,0,-18], LLA=[30,0,0], H=[4,-14,0])
make(tag, "SpecialWind", 1.6, [(0,IDLE,"OUT"),(0.5,REACH,"IO"),(1.0,P(REACH, RLA=[62,0,0], H=[6,-16,0]),"IO"),(1.6,P(REACH, RUA=[142,0,34]),"LIN")], hold=True)
THROW = P(drop(IDLE, 0.3, -14, 0, 18), RUA=[70,0,6], RLA=[6,0,0], LUA=[10,0,-30], LLA=[20,0,0], H=[6,0,0])
make(tag, "SpecialThrow", 0.55, [(0,P(REACH, RUA=[142,0,34]),"IN"),(0.12,THROW,"OUT"),(0.3,P(THROW,RUA=[60,0,8]),"IO"),(0.55,IDLE,"LIN")], events={"release":0.12})
