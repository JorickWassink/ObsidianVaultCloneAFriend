# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"fur":(224,168,74),"furD":(190,136,52),"mane":(154,90,36),"light":(246,220,166),"nose":(90,58,42),"dark":(26,24,26),
       "red":(184,36,44),"ermine":(244,244,244),"gold":(232,172,24),"gem":(216,50,44),"orb":(30,160,255),"glint":(255,255,255)}
NAMES = {"fur":"Fur","furD":"FurDark","mane":"Mane","light":"Light","nose":"Nose","dark":"Dark","red":"Cape","ermine":"Ermine","gold":"Gold","gem":"Gem","orb":"Orb","glint":"Glint"}
B = L["Builder"]("P07", PAL, {"Body":"fur","Head":"mane"}, glow=("orb",), names=NAMES, offset=(190,40,0))
B.add("Body","fur",(4.6,4,4),(0,0,3.0))
B.add("Body","light",(2.8,0.6,2.6),(0,-2.1,3.0))
B.add("Body","red",(5.4,0.5,4.0),(0,2.3,3.0),(4,0,0))
B.add("Body","ermine",(6,4.8,0.8),(0,0.1,4.9))
B.sym("Body","light",(1.6,2,1.0),(1.3,-0.4,0.5))
B.sym("Body","fur",(1.3,1.5,2),(2.9,-0.2,3.1),(0,10,0))
B.add("Body","light",(1.6,1.2,1.0),(-4.4,-0.95,2.0))
B.add("Body","gold",(0.5,0.5,5),(-4.9,-1.0,3.8))
B.add("Body","orb",(1.4,1.4,1.4),(-4.9,-1.0,6.8))
B.add("Head","mane",(8,7,7),(0,-0.2,8.6))
B.add("Head","fur",(5.4,0.8,5),(0,-3.9,8.4))
B.add("Head","light",(2.6,1.2,1.8),(0,-4.6,7.2))
B.add("Head","nose",(1.0,0.4,0.6),(0,-5.35,7.8))
B.face = "Eyes_Happy"; B.sym("Head","dark",(1.1,0.3,1.3),(1.4,-4.4,9.2)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","glint",(0.4,0.32,0.4),(1.15,-4.45,9.55)); B.face = None
B.sym("Head","dark",(1.4,0.3,0.4),(1.4,-4.4,10.3),(0,-14,0))
B.add("Head","gold",(4.6,4,1.2),(0,-0.4,12.6))
for p in ((1.7,-1.9,13.6),(-1.7,-1.9,13.6)):
    B.add("Head","gold",(0.9,0.9,1.0),p)
B.add("Head","gold",(0.9,0.9,1.4),(0,-1.9,13.8))
B.add("Head","gem",(0.6,0.3,0.6),(0,-2.5,12.6))

B.shingle("Head", ["mane","fur"], (0,-0.2,8.6), (8,7,7), "x", 1, seed=102, plate=(1.4,2.2))
B.shingle("Head", ["mane","fur"], (0,-0.2,8.6), (8,7,7), "x", -1, seed=103, plate=(1.4,2.2))
B.shingle("Head", ["mane","fur"], (0,-0.2,8.6), (8,7,7), "y", 1, seed=104, plate=(1.4,2.2))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((1.4,-4.3,9.2), 1.1)
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,5.2))}
B.build(J)
