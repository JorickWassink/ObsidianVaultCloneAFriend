# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"fur":(201,138,85),"furD":(165,110,64),"light":(236,201,162),"ear":(215,161,132),"dark":(30,26,26),"blue":(47,111,214),"cuff":(244,244,244),"gold":(232,168,20),"red":(216,50,44)}
NAMES = {"fur":"Fur","furD":"FurDark","light":"Light","ear":"EarInner","dark":"Dark","blue":"Glove","cuff":"Cuff","gold":"Belt","red":"Red"}
B = L["Builder"]("P04", PAL, {"Body":"fur","Head":"fur"}, names=NAMES, offset=(90,40,0))
B.add("Body","fur",(4.6,4,4),(0,0,3.0))
B.add("Body","light",(2.8,0.6,2.6),(0,-2.1,3.2))
B.add("Body","gold",(5.0,4.4,0.8),(0,0,1.7))
B.add("Body","red",(0.8,0.3,0.6),(0,-2.35,1.7))
B.sym("Body","furD",(1.6,3,1.0),(1.3,-0.8,0.5))
B.add("Body","fur",(1.6,3.4,1.4),(0,3.2,1.2),(-10,0,0))
B.sym("Body","blue",(1.8,1.9,1.8),(3.0,-1.0,2.6))
B.sym("Body","cuff",(1.9,2.0,0.5),(3.0,-1.0,3.6))
B.add("Body","fur",(1.2,0.6,1.0),(0,-2.55,3.8))
B.sym("Body","fur",(0.3,0.3,0.6),(0.35,-2.55,4.6))
B.add("Head","fur",(6.6,6,6),(0,-0.4,8.2))
B.add("Head","light",(3,1.4,2),(0,-4.0,7.2))
B.add("Head","dark",(1.2,0.4,0.6),(0,-4.85,7.8))
B.face = "Eyes_Happy"; B.sym("Head","dark",(1.1,0.3,1.3),(1.6,-3.5,8.9)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","cuff",(0.4,0.32,0.4),(1.35,-3.55,9.3)); B.face = None
B.sym("Head","dark",(1.5,0.3,0.4),(1.6,-3.5,10.1),(0,-14,0))
B.sym("Head","fur",(1.3,1.0,3.4),(1.7,-0.2,12.6),(0,-10,0))
B.sym("Head","ear",(0.6,0.3,2.4),(1.7,-0.75,12.6),(0,-10,0))

B.shingle("Head", ["furD","fur"], (0,-0.4,8.2), (6.6,6,6), "x", 1, seed=96, plate=(1.2,2.0))
B.shingle("Head", ["furD","fur"], (0,-0.4,8.2), (6.6,6,6), "x", -1, seed=97, plate=(1.2,2.0))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((1.6,-3.4,8.9), 1.1)
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,5.2))}
B.build(J)
