
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop, make = L["P"], L["drop"], L["make"]
tag, k = "B01", 1.0
S = L["biped_core"](tag, k, arms_out=8, skip=("Walk",))
IDLE = S["IDLE"]
# WALK: heavy lumbering waddle - big side sway, body rolls over the planted leg, head bobs, arms swing loose
def step(side):  # side = +1: left foot planted forward, right leg lifting
    p = drop(IDLE, 0.3, -4, side*7, side*6)
    p = P(p, H=[-4, -side*6, -side*5], LUA=[-side*22, 0, -16], RUA=[side*22, 0, 16], LLA=[18,0,0], RLA=[18,0,0])
    lift, plant = ("RL","LL") if side > 0 else ("LL","RL")
    l = list(p[lift]); l[0] -= 8; l[4] += 1.1; p[lift] = l
    return p
UPL = P(IDLE, B=[-3, 0, 2, 0, 0.25, 0], H=[2,0,0], LL=[4,0,-2,0,0.3,0], RL=[4,0,-2,0,0.3,0], LUA=[4,0,-14], RUA=[4,0,14], LLA=[14,0,0], RLA=[14,0,0])
UPR = P(UPL, B=[-3, 0, -2, 0, 0.25, 0], LL=[4,0,2,0,0.3,0], RL=[4,0,2,0,0.3,0])
make(tag, "Walk", 1.4, [(0,step(1),"OUT"),(0.35,UPL,"IN"),(0.7,step(-1),"OUT"),(1.05,UPR,"IN"),(1.4,step(1),"OUT")], loop=True)
# STRIKE: two-paw overhead swipe, lands at 0.55
PRE = P(drop(IDLE, 0.3, -4), H=[-4,0,0], LUA=[-14,0,-12], RUA=[-14,0,12], LLA=[16,0,0], RLA=[16,0,0])
UP = P(drop(IDLE, -0.4, 10), H=[12,0,0], LUA=[160,0,-18], RUA=[160,0,18], LLA=[30,0,0], RLA=[30,0,0])
SWIPE = P(drop(IDLE, 1.0, -20), H=[10,0,0], LUA=[70,0,-4], RUA=[70,0,4], LLA=[6,0,0], RLA=[6,0,0])
SETTLE = P(drop(IDLE, 0.8, -16), H=[8,0,0], LUA=[64,0,-6], RUA=[64,0,6], LLA=[8,0,0], RLA=[8,0,0])
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.12,PRE,"IO"),(0.42,UP,"IN"),(0.55,SWIPE,"OUT"),(0.62,SETTLE,"IO"),(0.75,SETTLE,"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# BEAR SLAM: rears up tall (SlamWind, holds), leaps belly first (SlamLeap, holds), belly-flop crash (SlamHit)
REAR = P(drop(IDLE, -0.7, 12), H=[10,0,0], LUA=[150,0,-38], RUA=[150,0,38], LLA=[30,0,0], RLA=[30,0,0])
REAR2 = P(drop(IDLE, -0.8, 14), H=[12,0,0], LUA=[160,0,-42], RUA=[160,0,42], LLA=[24,0,0], RLA=[24,0,0])
make(tag, "SlamWind", 1.6, [(0,IDLE,"OUT"),(0.5,REAR,"IO"),(1.0,P(REAR, H=[11,0,6]),"IO"),(1.6,REAR2,"LIN")], hold=True)
CROUCH = P(drop(IDLE, 1.2, -12), H=[12,0,0], LUA=[-30,0,-24], RUA=[-30,0,24], LLA=[20,0,0], RLA=[20,0,0])
FLY = P(None, B=[-40,0,0,0,1.4,0], H=[10,0,0], LUA=[150,0,-40], RUA=[150,0,40], LLA=[10,0,0], RLA=[10,0,0], LL=[-20,0,0], RL=[-20,0,0])
make(tag, "SlamLeap", 0.7, [(0,CROUCH,"OUT"),(0.15,P(FLY, B=[-20,0,0,0,1.2,0]),"IO"),(0.7,FLY,"LIN")], hold=True)
FLOP = P(drop(IDLE, 1.0, -22), H=[10,0,0], LUA=[60,0,-30], RUA=[60,0,30], LLA=[4,0,0], RLA=[4,0,0])
make(tag, "SlamHit", 1.1, [(0,FLOP,"LIN"),(0.08,P(drop(IDLE, 1.1, -24), H=[12,0,0], LUA=[58,0,-34], RUA=[58,0,34], LLA=[2,0,0], RLA=[2,0,0]),"OUT"),
    (0.55,P(FLOP, H=[8,0,0]),"IO"),(1.1,IDLE,"LIN")], events={"impact":0.0})
