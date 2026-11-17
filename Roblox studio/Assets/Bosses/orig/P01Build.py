# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"fur":(118,86,58),"furD":(86,62,42),"light":(196,160,118),"dark":(30,26,26),"red":(216,60,50),"white":(244,239,230),"scar":(62,47,34)}
NAMES = {"fur":"Fur","furD":"FurDark","light":"Light","dark":"Dark","red":"Cape","white":"White","scar":"Scar"}
B = L["Builder"]("P01", PAL, {"Body":"fur","Head":"fur"}, names=NAMES, offset=(0,40,0))
B.add("Body","fur",(5,4,4),(0,0,3.0))
B.add("Body","light",(3,0.6,2.6),(0,-2.1,3.0))
B.sym("Body","furD",(1.6,2,1.2),(1.4,-0.4,0.6))
B.sym("Body","furD",(1.4,1.6,2.2),(3.1,-0.2,3.0),(0,10,0))
B.add("Body","red",(4.4,0.5,3.4),(0,2.25,3.1))
B.add("Body","white",(1.4,0.7,1.4),(-1.0,2.45,3.9)); B.add("Body","white",(1.4,0.7,1.4),(1.0,2.45,2.4))
B.add("Body","red",(4.4,0.8,0.8),(0,-1.75,4.9))
B.add("Head","fur",(7,6,6),(0,-0.4,8.2))
B.add("Head","light",(3,1.2,1.8),(0,-3.8,7.2))
B.add("Head","dark",(1.2,0.4,0.8),(0,-4.5,7.8))
B.face = "Eyes_Happy"; B.sym("Head","dark",(1.1,0.3,1.3),(1.7,-3.5,8.9)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","white",(0.4,0.32,0.4),(1.45,-3.55,9.3)); B.face = None
B.sym("Head","dark",(1.6,0.3,0.4),(1.7,-3.5,10.0),(0,-14,0))
B.add("Head","fur",(1.8,1.2,1.8),(-2.4,-0.2,11.6)); B.add("Head","light",(0.9,0.3,0.9),(-2.4,-0.85,11.6))
B.add("Head","fur",(1.8,1.2,1.1),(2.4,-0.2,11.3))
B.add("Head","scar",(0.3,0.4,1.8),(0.5,-3.55,9.0),(0,20,0))

B.shingle("Head", ["furD","fur"], (0,-0.4,8.2), (7,6,6), "x", 1, seed=91, plate=(1.2,2.0))
B.shingle("Head", ["furD","fur"], (0,-0.4,8.2), (7,6,6), "x", -1, seed=92, plate=(1.2,2.0))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((1.7,-3.4,8.9), 1.1)
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,5.2))}
B.build(J)
