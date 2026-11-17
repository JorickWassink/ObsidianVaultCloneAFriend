
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop, make = L["P"], L["drop"], L["make"]
tag, k = "B04", 1.0
L["GROUND"] = ["LL","RL","T"]
GUARD = P(None, B=[0,0,0], H=[0,0,0], LUA=[52,0,-18], RUA=[52,0,18], LLA=[84,0,0], RLA=[84,0,0])
def idle_keys(IDLE, BREATH, LOOK):   # always ready to box: bounces on its toes with its guard up
    G = GUARD
    return [(0,P(drop(G, 0.3, -4)),"OUT"),(0.3,P(drop(G, -0.5, -2), H=[2,0,0]),"IN"),(0.6,P(drop(G, 0.3, -4)),"OUT"),(0.9,P(drop(G, -0.5, -2), H=[2,6,0]),"IN"),
            (1.2,P(drop(G, 0.3, -4)),"OUT"),(1.6,P(drop(G, 0.1, -3), LUA=[56,0,-10], LLA=[82,0,0], H=[0,-6,0]),"IO"),(2.0,P(drop(G, 0.3, -4)),"IO")]
S = L["biped_core"](tag, k, arms_out=8, extra_idle=idle_keys, skip=("Walk",), crouch=0.35)
IDLE = S["IDLE"]
# WALK: boxer bounce - little two-footed hops with the guard up, shoulders rolling
def bounce(side):
    p = P(drop(GUARD, -0.9, -6, 0, side*10), H=[0, -side*6, 0])
    for leg in ("LL","RL"):
        l = list(p[leg]); l[0] -= 6; l[4] += 0.9; p[leg] = l
    return p
LANDB = P(drop(GUARD, 0.16, -8))
make(tag, "Walk", 0.8, [(0,LANDB,"OUT"),(0.2,bounce(1),"IN"),(0.4,LANDB,"OUT"),(0.6,bounce(-1),"IN"),(0.8,LANDB,"IO")], loop=True)
# STRIKE: one-two, the right cross lands at 0.55
JAB = P(drop(GUARD, 0.08, -6, 0, 14), LUA=[90,0,-10], LLA=[4,0,0], H=[0,-10,0])
CROSS = P(drop(GUARD, 0.2, -10, 0, -20), RUA=[86,0,24], RLA=[2,0,0], LUA=[52,0,-18], LLA=[84,0,0], H=[0,4,0])
make(tag, "Strike", 1.05, [(0,P(drop(GUARD, 0.08,-4)),"IO"),(0.18,P(drop(GUARD, 0.12,-6,0,-6)),"IN"),(0.3,JAB,"OUT"),(0.42,P(drop(GUARD, 0.12,-6,0,4)),"IN"),
    (0.55,CROSS,"OUT"),(0.75,CROSS,"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# TITLE FIGHT COMBO: squares up (holds), then jab, jab, hook, joey bump, big uppercut
SQUARE = P(drop(GUARD, 0.28, -10), H=[-4,0,0])
make(tag, "SpecialWind", 0.8, [(0,P(drop(GUARD, 0.08,-4)),"OUT"),(0.4,SQUARE,"IO"),(0.8,P(SQUARE, B=[-10,6,0,0,-0.7,0]),"LIN")], hold=True)
JAB2 = P(drop(GUARD, 0.16, -8, 0, -14), RUA=[90,0,16], RLA=[4,0,0], H=[0,4,0])
HOOK = P(drop(GUARD, 0.2, -10, 0, 24), LUA=[78,0,-44], LLA=[36,0,0], H=[0,-14,0])
BUMP = P(drop(GUARD, 0.08, -2), B=[4,0,0,0,-0.2,0])
LOAD = P(drop(GUARD, 0.52, -14, 0, -10), RUA=[-20,0,20], RLA=[90,0,0], H=[-6,0,0])
UPPER = P(None, B=[10,-14,0,0,1.6,0], T=[-10,14,0,0,1.0,0], H=[14,10,0], RUA=[165,0,14], RLA=[6,0,0], LUA=[40,0,-24], LLA=[80,0,0], LL=[-4,14,0,0,0.4,0], RL=[-12,14,0,0,0.8,0])
make(tag, "Combo", 2.4, [(0,SQUARE,"IN"),(0.3,JAB,"OUT"),(0.48,SQUARE,"IN"),(0.65,JAB2,"OUT"),(0.82,SQUARE,"IN"),(1.0,HOOK,"OUT"),
    (1.15,SQUARE,"IO"),(1.25,BUMP,"OUT"),(1.5,LOAD,"IN"),(1.85,UPPER,"OUT"),(2.05,UPPER,"IO"),(2.4,IDLE,"LIN")],
    events={"hit1":0.3,"hit2":0.65,"hit3":1.0,"joey":1.25,"uppercut":1.85})
