# Restyle copy (ADR 0017): SmoothLib, eye patch removed, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"fur":(154,160,168),"furD":(125,131,140),"light":(214,216,220),"pink":(242,163,181),"dark":(30,26,26),"white":(250,250,250),
       "orange":(240,127,30),"leaf":(63,174,70),"leafD":(47,143,56)}
NAMES = {"fur":"Fur","furD":"FurDark","light":"Light","pink":"Pink","dark":"Dark","white":"White","orange":"Carrot","leaf":"Leaf","leafD":"LeafDark"}
B = L["Builder"]("P02", PAL, {"Body":"fur","Head":"fur"}, names=NAMES, offset=(30,40,0))
B.add("Body","fur",(4.6,4,4),(0,0,3.0))
B.add("Body","light",(2.8,0.6,2.6),(0,-2.1,3.0))
B.sym("Body","furD",(1.6,2.6,1.0),(1.3,-0.6,0.5))
B.sym("Body","fur",(1.3,1.5,2),(2.9,-0.2,3.1),(0,10,0))
B.add("Body","white",(1.6,1.4,1.6),(0,2.5,2.0))
B.add("Body","orange",(1.4,1.4,4.4),(0.6,2.9,4.4),(0,-25,0))
B.add("Body","leaf",(0.6,0.6,1.4),(-0.4,2.9,6.8),(0,-30,0))
B.add("Head","fur",(7,6,6),(0,-0.4,8.2))
B.add("Head","light",(2.6,1,1.6),(0,-3.8,7.0))
B.add("Head","pink",(1,0.4,0.6),(0,-4.35,7.6))
B.add("Head","white",(1.2,0.4,0.9),(0,-4.25,6.4))
B.face = "Eyes_Happy"; B.sym("Head","dark",(1.1,0.3,1.3),(1.7,-3.5,8.9)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","white",(0.4,0.32,0.4),(1.45,-3.55,9.3)); B.face = None
B.sym("Head","dark",(1.5,0.3,0.4),(1.7,-3.5,10.1),(0,-14,0))
B.add("Head","leaf",(7.4,6.4,0.7),(0,-0.4,11.1))
B.add("Head","leafD",(1.4,0.4,0.8),(2.6,-3.5,11.2),(0,-30,0))
B.sym("Head","fur",(1.4,1.1,4.4),(1.6,-0.2,13.4))
B.sym("Head","pink",(0.7,0.3,3.4),(1.6,-0.8,13.4))

B.shingle("Head", ["furD","fur"], (0,-0.4,8.2), (7,6,6), "x", 1, seed=93, plate=(1.2,2.0))
B.shingle("Head", ["furD","fur"], (0,-0.4,8.2), (7,6,6), "x", -1, seed=94, plate=(1.2,2.0))
# restyle: no eye patch; Happy/Blink eye sets (ADR 0015)
B.blink_set((1.7,-3.4,8.9), 1.1)
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,5.2))}
B.build(J)
