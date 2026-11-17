
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop, make = L["P"], L["drop"], L["make"]
tag, k = "B02", 0.9
def idle_keys(IDLE, BREATH, LOOK):   # twitchy: quick head tilts left and right
    return [(0,IDLE,"IO"),(0.5,P(BREATH,H=[4,10,5]),"OUT"),(1.1,BREATH,"IO"),(1.6,P(IDLE,H=[2,-10,-5]),"OUT"),(2.2,IDLE,"IO")]
S = L["biped_core"](tag, k, arms_out=8, extra_idle=idle_keys, skip=("Walk",))
IDLE = S["IDLE"]
# WALK: bunny hops - crouch, push off with both feet, tuck in the air, squash on landing
CROUCH = P(drop(IDLE, 0.8, -10), H=[-4,0,0], LUA=[-24,0,-10], RUA=[-24,0,10], LLA=[20,0,0], RLA=[20,0,0])
PUSH = P(None, B=[-6,0,0,0,2.2,0], H=[6,0,0], LL=[-28,0,0], RL=[-28,0,0], LUA=[30,0,-14], RUA=[30,0,14], LLA=[10,0,0], RLA=[10,0,0])
APEX = P(None, B=[-2,0,0,0,3.0,0], H=[4,0,0], LL=[18,0,0], RL=[18,0,0], LUA=[20,0,-18], RUA=[20,0,18], LLA=[24,0,0], RLA=[24,0,0])
LAND = P(drop(IDLE, 0.7, -12), H=[-6,0,0], LUA=[40,0,-20], RUA=[40,0,20], LLA=[14,0,0], RLA=[14,0,0])
make(tag, "Walk", 1.0, [(0,CROUCH,"OUT"),(0.2,PUSH,"OUT"),(0.45,APEX,"IN"),(0.7,LAND,"OUT"),(1.0,CROUCH,"IO")], loop=True)
# STRIKE: hop and double-foot stomp, lands at 0.55
PRE = P(drop(IDLE, 1.0, -12), H=[-6,0,0], LUA=[-30,0,-12], RUA=[-30,0,12], LLA=[24,0,0], RLA=[24,0,0])
UP = P(None, B=[4,0,0,0,2.6,0], H=[8,0,0], LL=[36,0,0], RL=[36,0,0], LUA=[120,0,-30], RUA=[120,0,30], LLA=[30,0,0], RLA=[30,0,0])
STOMP = P(drop(IDLE, 0.7, -14), H=[6,0,0], LUA=[-30,0,-30], RUA=[-30,0,30], LLA=[10,0,0], RLA=[10,0,0])
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.2,PRE,"OUT"),(0.42,UP,"IN"),(0.55,STOMP,"OUT"),(0.75,STOMP,"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# CARROT HOP: deep wiggly crouch (holds), huge stretched leap (holds), crash landing
DEEP = P(drop(IDLE, 1.3, -16), H=[-4,0,0], LUA=[-40,0,-16], RUA=[-40,0,16], LLA=[30,0,0], RLA=[30,0,0])
make(tag, "SlamWind", 1.6, [(0,IDLE,"OUT"),(0.45,DEEP,"IO"),(0.8,P(DEEP, B=[-16,0,4,0,-1.3,0]),"IO"),(1.15,P(DEEP, B=[-16,0,-4,0,-1.3,0]),"IO"),(1.6,DEEP,"LIN")], hold=True)
STRETCH = P(None, B=[6,0,0,0,1.6,0], H=[10,0,0], LL=[-22,0,0], RL=[-22,0,0], LUA=[170,0,-14], RUA=[170,0,14], LLA=[4,0,0], RLA=[4,0,0])
TUCK = P(None, B=[-10,0,0,0,1.6,0], H=[4,0,0], LL=[40,0,-6], RL=[40,0,6], LUA=[150,0,-24], RUA=[150,0,24], LLA=[40,0,0], RLA=[40,0,0])
make(tag, "SlamLeap", 0.7, [(0,DEEP,"OUT"),(0.12,STRETCH,"IO"),(0.45,TUCK,"IN"),(0.7,TUCK,"LIN")], hold=True)
CRASH = P(drop(IDLE, 1.0, -18), H=[8,0,0], LUA=[50,0,-36], RUA=[50,0,36], LLA=[4,0,0], RLA=[4,0,0])
make(tag, "SlamHit", 1.1, [(0,CRASH,"LIN"),(0.08,P(drop(IDLE, 1.15, -20), H=[8,0,0], LUA=[46,0,-40], RUA=[46,0,40]),"OUT"),(0.55,P(CRASH,H=[4,0,0]),"IO"),(1.1,IDLE,"LIN")], events={"impact":0.0})
