
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop, make = L["P"], L["drop"], L["make"]
tag, k = "B08", 1.3
def idle_keys(IDLE, BREATH, LOOK):   # engine hum, the shark looks around, drills give a quick rev
    HUM = P(drop(IDLE, 0.12), H=[0,0,0])
    LOOKL = P(HUM, H=[2,18,0]); LOOKR = P(IDLE, H=[2,-18,0])
    REV = P(IDLE, RH=[0,360,0], LH=[0,-360,0], H=[4,0,0])
    return [(0,IDLE,"LIN"),(0.3,HUM,"LIN"),(0.6,IDLE,"LIN"),(1.1,LOOKL,"IO"),(1.7,LOOKR,"IO"),(2.2,IDLE,"IO"),(2.5,REV,"IO"),(2.8,P(IDLE,RH=[0,720,0],LH=[0,-720,0]),"OUT"),(3.0,P(IDLE,RH=[0,720,0],LH=[0,-720,0]),"LIN")]
def stiff(p):
    """the shoulder pads sit close to the cockpit lid: arms swing forward/back, only a little sideways; the shark keeps its chin up"""
    p = dict(p)
    for a, sg in (("LUA",-1),("RUA",1)):
        if a in p:
            v = list(p[a])+[0]*3
            p[a] = [v[0], v[1], sg*max(0,min(12,sg*v[2]))] + v[3:6]
    if "H" in p:
        h = list(p["H"])+[0]*3
        p["H"] = [max(-1,h[0]), h[1], max(-3,min(3,h[2]))] + h[3:6]
    return p
ROAR = P(drop(P(None, B=[0,0,0], H=[0,0,0], LUA=[4,0,-4], RUA=[4,0,4], LLA=[8,0,0], RLA=[8,0,0]), -0.5*k, 8), H=[10,0,0], LUA=[80,0,-8], RUA=[80,0,8], LLA=[50,0,0], RLA=[50,0,0], LH=[0,-720,0], RH=[0,720,0])
_mk = L["make"]
L["make"] = lambda tg, nm, ln, keys, **kw: _mk(tg, nm, ln, [(a, stiff(p), e) for a,p,e in keys], **kw)
S = L["biped_core"](tag, k, arms_out=4, extra_idle=idle_keys, skip=("Walk","Idle"), crouch=0.5, intro_roar=ROAR)
IDLE = S["IDLE"]
keys = idle_keys(IDLE, None, None)
make(tag, "Idle", 3.0, keys, loop=True)
# WALK: clunky robot stomps - each foot lifts stiffly, slams down with a jolt, the shark wobbles in the cockpit
def lift(side):
    p = drop(IDLE, -0.25, 0, side*3, side*4)
    p = P(p, H=[2,0,-side*3], LUA=[-side*16,0,-4], RUA=[side*16,0,4])
    leg = "LL" if side > 0 else "RL"
    l = list(p[leg]); l[0] += 18; l[4] += 1.6; p[leg] = l
    return p
def land(side):
    p = drop(IDLE, 0.45, -2, -side*2, side*4)
    return P(p, H=[0,0,side*3], LUA=[-side*10,0,-4], RUA=[side*10,0,4])
def settle(side):
    p = drop(IDLE, 0.1, 0, 0, side*3)
    return P(p, H=[1,0,-side*3], LUA=[-side*8,0,-4], RUA=[side*8,0,4])
make(tag, "Walk", 1.4, [(0,land(1),"OUT"),(0.12,settle(1),"IO"),(0.4,lift(-1),"IO"),(0.7,land(-1),"OUT"),(0.82,settle(-1),"IO"),(1.1,lift(1),"IO"),(1.4,land(1),"OUT")], loop=True, events={"stomp":0.0, "stomp2":0.7})
# STRIKE: winds the right drill back revving, punches it forward spinning, lands at 0.55
WIND = P(drop(IDLE, 0.2, 2, 0, 16), H=[2,-8,0], RUA=[-30,0,10], RLA=[40,0,0], RH=[0,360,0], LUA=[30,0,-8])
PUNCH = P(drop(IDLE, 0.35, -8, 0, -14), H=[-2,6,0], RUA=[82,0,4], RLA=[0,0,0], RH=[0,1080,0], LUA=[-14,0,-8])
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.4,WIND,"IN"),(0.55,PUNCH,"OUT"),(0.8,P(PUNCH,RH=[0,1440,0]),"IO"),(1.05,P(IDLE,RH=[0,1440,0]),"LIN")], events={"impact":0.55})
# FULL PAYLOAD: braces wide with the launch tubes on its back aimed up (holds), fires 5 torpedoes with recoil (SpecialThrow x5, release 0.05),
# then a booster jump that stomps down (SpecialHit, impact 0.8)
BRACE = P(drop(IDLE, 0.6, 6), H=[4,0,0], LUA=[24,0,-10], RUA=[24,0,10], LLA=[40,0,0], RLA=[40,0,0], LL=[0,0,-6,0,0,0], RL=[0,0,6,0,0,0])
make(tag, "SpecialWind", 1.0, [(0,IDLE,"OUT"),(0.35,BRACE,"BACK"),(1.0,P(BRACE,H=[6,0,0]),"LIN")], hold=True)
KICK = P(drop(IDLE, 0.75, 10), H=[-4,0,4], LUA=[30,0,-12], RUA=[30,0,12], LLA=[44,0,0], RLA=[44,0,0], LL=[0,0,-6,0,0,0], RL=[0,0,6,0,0,0])
make(tag, "SpecialThrow", 0.4, [(0,BRACE,"OUT"),(0.05,KICK,"OUT"),(0.18,P(BRACE,H=[6,0,-3]),"IO"),(0.4,BRACE,"IO")], events={"release":0.05})
CROUCH = P(drop(IDLE, 0.8, -6), H=[-2,0,0], LUA=[-30,0,-14], RUA=[-30,0,14])
JUMP = P(IDLE, B=[6,0,0,0,6.0*k,0], H=[6,0,0], LUA=[-30,0,-10], RUA=[-30,0,10], LL=[-10,0,0], RL=[-10,0,0])
APEX = P(IDLE, B=[-4,0,0,0,7.0*k,0], H=[-4,0,0], LUA=[60,0,-10], RUA=[60,0,10], LL=[16,0,0], RL=[16,0,0])
STOMP = P(drop(IDLE, 0.8, -10), H=[-6,0,0], LUA=[40,0,-10], RUA=[40,0,10])
make(tag, "SpecialHit", 1.5, [(0,BRACE,"IO"),(0.2,CROUCH,"IN"),(0.4,JUMP,"OUT"),(0.62,APEX,"IN"),(0.8,STOMP,"OUT"),(1.1,P(STOMP,H=[-2,0,0]),"IO"),(1.5,IDLE,"LIN")], events={"launch":0.3, "impact":0.8})

L["make"] = _mk
