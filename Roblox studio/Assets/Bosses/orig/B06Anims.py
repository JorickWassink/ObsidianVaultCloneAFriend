
L = __import__("bpy").app.driver_namespace["animlib"]
P, drop, make = L["P"], L["drop"], L["make"]
tag, k = "B06", 1.0
IDLE = P(None, B=[0,0,0], H=[0,0,0], T=[0,0,0])
BREATH = P(drop(IDLE, -0.15, 0), H=[-3,0,0], T=[-4,6,0])
SNORT = P(drop(IDLE, 0.1, -2), H=[6,0,0], T=[0,-8,0])
PAW1 = P(drop(IDLE, 0.05, -1), H=[-6,0,0], LFL=[22,0,0,0,0.9,0])
PAW2 = P(drop(IDLE, 0.05, -1), H=[-8,0,0], LFL=[-18,0,0,0,0.5,0])
make(tag, "Idle", 2.8, [(0,IDLE,"IO"),(0.8,BREATH,"IO"),(1.2,SNORT,"OUT"),(1.5,IDLE,"IO"),(1.8,PAW1,"IO"),(2.05,PAW2,"IO"),(2.3,PAW1,"IO"),(2.8,IDLE,"IO")], loop=True)
# WALK: trot - diagonal pairs, head bobbing, tail swishing
s = 18
WA = P(IDLE, B=[0,0,3,0,0.1,0], H=[-4,0,0], T=[0,16,0], LFL=[s,0,0,0,0.5,0], RBL=[s,0,0,0,0.5,0], RFL=[-s,0,0,0,0.5,0], LBL=[-s,0,0,0,0.5,0])
Bp = P(IDLE, B=[0,0,-3,0,0.1,0], H=[-4,0,0], T=[0,-16,0], RFL=[s,0,0,0,0.5,0], LBL=[s,0,0,0,0.5,0], LFL=[-s,0,0,0,0.5,0], RBL=[-s,0,0,0,0.5,0])
PA = P(IDLE, B=[0,0,0,0,0.45,0], H=[3,0,0], T=[0,0,0], RFL=[0,0,0,0,1.2,0], LBL=[0,0,0,0,1.2,0])
PB = P(IDLE, B=[0,0,0,0,0.45,0], H=[3,0,0], T=[0,0,0], LFL=[0,0,0,0,1.2,0], RBL=[0,0,0,0,1.2,0])
make(tag, "Walk", 1.0, [(0,WA,"IO"),(0.25,PA,"IO"),(0.5,Bp,"IO"),(0.75,PB,"IO"),(1.0,WA,"IO")], loop=True)
# STRIKE: lowers the horn, lunges and jabs upward, lands at 0.55
LOWER = P(drop(IDLE, 0.3, -4), H=[-16,0,0], T=[-8,0,0])
JAB = P(drop(IDLE, 0.2, -2), B=[-2,0,0,0,-0.2,-1.4], H=[14,0,0], T=[-4,0,0])
make(tag, "Strike", 1.05, [(0,IDLE,"IO"),(0.35,LOWER,"IN"),(0.55,JAB,"OUT"),(0.75,P(JAB,H=[10,0,0]),"IO"),(1.05,IDLE,"LIN")], events={"impact":0.55})
# PALADIN STAMPEDE: scrapes its hoof with the horn glowing (holds), gallops (loops while charging), rears and crashes
SCRAPE_A = P(drop(IDLE, 0.12, -4), H=[-15,0,0], T=[-12,0,0], RFL=[-24,0,0,0,0.7,0])
SCRAPE_B = P(drop(IDLE, 0.12, -4), H=[-15,0,0], T=[-12,0,0], RFL=[10,0,0,0,0.9,0])
make(tag, "SpecialWind", 1.5, [(0,IDLE,"OUT"),(0.3,SCRAPE_B,"IO"),(0.55,SCRAPE_A,"IO"),(0.8,SCRAPE_B,"IO"),(1.05,SCRAPE_A,"IO"),(1.5,P(SCRAPE_A, H=[-17,0,0]),"LIN")], hold=True)
G1 = P(IDLE, B=[5,0,0,0,0.6,0], H=[-14,0,0], T=[-18,0,0], LFL=[28,0,0,0,0.9,0], RFL=[24,0,0,0,0.9,0], LBL=[-24,0,0,0,0.6,0], RBL=[-28,0,0,0,0.6,0])
G2 = P(IDLE, B=[-5,0,0,0,0.9,0], H=[-16,0,0], T=[-22,0,0], LFL=[-22,0,0,0,0.9,0], RFL=[-26,0,0,0,0.9,0], LBL=[22,0,0,0,1.0,0], RBL=[26,0,0,0,1.0,0])
make(tag, "Charge", 0.5, [(0,G1,"IO"),(0.25,G2,"IO"),(0.5,G1,"IO")], loop=True)
REAR = P(drop(IDLE, -1.4, 16), H=[10,0,0], T=[8,0,0], LFL=[36,0,0,0,1.0,0], RFL=[40,0,0,0,1.0,0])
STOMP = P(drop(IDLE, 0.3, -4), H=[-6,0,0], T=[-10,0,0])
make(tag, "SpecialHit", 1.1, [(0,P(G2),"OUT"),(0.1,P(drop(IDLE,0.2,-2),H=[12,0,0]),"OUT"),(0.4,REAR,"IN"),(0.6,STOMP,"OUT"),(0.8,P(STOMP,H=[-2,0,0]),"IO"),(1.1,IDLE,"LIN")],
     events={"impact":0.1, "stomp":0.6})
# INTRO: asleep, wakes, snorts and shakes its head, rears up, slams down
SLEEP = P(drop(IDLE, 0.4, -3), H=[-12,0,0], T=[-10,0,0])
make(tag, "Intro", 4.2, [(0,SLEEP,"IO"),(0.9,P(SLEEP,H=[-10,0,0]),"OUT"),(1.4,P(IDLE,H=[4,0,0]),"IO"),(1.65,P(IDLE,H=[2,16,0]),"IO"),(1.9,P(IDLE,H=[2,-16,0]),"IO"),
    (2.4,REAR,"IO"),(2.8,P(REAR,H=[12,0,0]),"IN"),(3.35,STOMP,"OUT"),(3.6,STOMP,"IO"),(4.2,IDLE,"LIN")], events={"roar":2.4, "pound":3.35})
# DEFEAT: staggers, slumps forward with its head on the floor
STAG = P(drop(IDLE, 0.05, 2), H=[8,10,0], T=[0,20,0])
SAG = P(drop(IDLE, 0.08, -2), H=[-14,-6,8], T=[-10,-8,0])
make(tag, "Defeat", 1.4, [(0,IDLE,"OUT"),(0.25,STAG,"IN"),(0.45,P(STAG,H=[10,-8,0]),"IO"),(0.8,SAG,"OUT"),(1.4,P(SAG,H=[-16,-6,10]),"LIN")], hold=True)
