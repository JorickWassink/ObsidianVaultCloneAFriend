# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"iris":(220,50,70),"fur":(154,160,168),"furD":(125,131,140),"light":(214,216,220),"pink":(242,163,181),"dark":(30,26,26),"white":(250,250,250),
       "orange":(240,127,30),"orangeD":(200,97,26),"leaf":(63,174,70),"leafD":(47,143,56),"strap":(110,74,44)}
NAMES = {"fur":"Fur","furD":"FurDark","light":"Light","pink":"Pink","dark":"Dark","white":"White","orange":"Carrot","orangeD":"CarrotDark","leaf":"Leaf","leafD":"LeafDark","strap":"Strap"}
MAIN = {"Body":"fur","Head":"fur","LeftUpperArm":"fur","RightUpperArm":"fur","LeftLowerArm":"fur","RightLowerArm":"fur","LeftHand":"light","RightHand":"light","LeftLeg":"fur","RightLeg":"fur"}
B = L["Builder"]("B02", PAL, MAIN, names=NAMES, offset=(30,0,0))
B.mirror("LeftLeg","fur",(3.6,4,3.4),(2.6,0.6,2.8))
B.mirror("LeftLeg","furD",(3.4,6,1.2),(2.6,-1.4,0.6))
B.add("Body","fur",(8,6,7),(0,0,7.8))
B.add("Body","light",(5,1,5),(0,-3.1,7.6))
B.add("Body","white",(2.4,2,2.4),(0,3.6,5.8))
# stolen carrot strapped to the back
B.add("Body","orange",(2.4,2.4,9),(1.0,4.2,9.8),(0,-15,0))
B.add("Body","orangeD",(1.4,1.4,2),(2.42,4.2,4.49),(0,-15,0))
for z in (9.0, 11.4, 13.8):
    B.add("Body","orangeD",(2.6,2.6,0.3),(1.0-(z-1.2-9.8)*0.268,4.2,z-1.2),(0,-15,0))
B.add("Body","leaf",(0.8,0.8,2.8),(-0.45,3.9,15.45),(0,-40,0))
B.add("Body","leafD",(0.8,0.8,2.6),(-0.05,4.25,15.65),(0,-15,0))
B.add("Body","leaf",(0.8,0.8,2.2),(-1.05,4.6,15.05),(0,-65,0))
B.add("Body","strap",(1.2,0.35,7.2),(0,-3.6,8.3),(0,38,0))
B.add("Body","strap",(0.8,0.5,6.0),(0,3.3,9.0),(0,-35,0))
# head
B.add("Head","fur",(7,6,6),(0,-0.8,14.4))
B.add("Head","furD",(3.6,3.0,1.6),(0,-0.6,11.5))   # neck
B.add("Head","light",(3,1,2),(0,-4.2,13.2))
B.add("Head","pink",(1.2,0.5,0.8),(0,-4.8,13.9))
B.sym("Head","dark",(1.8,0.4,0.5),(1.6,-3.9,16.4),(0,-15,0))
B.add("Head","leaf",(7.4,6.4,0.8),(0,-0.8,17.1))
B.add("Head","leafD",(1.8,0.4,1.0),(3.0,-3.9,17.4),(0,-30,0))
B.add("Head","leaf",(1.6,0.4,0.9),(1.4,-3.95,17.6),(0,20,0))
B.sym("Head","fur",(1.6,1.2,7),(1.8,-0.4,20.8))
B.sym("Head","pink",(0.8,0.3,5.6),(1.8,-1.05,20.8))
# arms
B.mirror("LeftUpperArm","fur",(2.2,2.2,3.2),(5.0,0,9.6))
B.mirror("LeftLowerArm","fur",(2,2,2.6),(5.2,-0.3,7.0))
B.mirror("LeftHand","light",(2.6,2.8,1.8),(5.2,-0.5,5.2))

B.shingle("Body", ["furD","fur"], (0,0,9.2), (8,6,4.2), "x", 1, seed=21)
B.shingle("Body", ["furD","fur"], (0,0,9.2), (8,6,4.2), "x", -1, seed=22)
B.shingle("Head", ["furD","fur"], (0,-0.8,15.6), (7,6,3.4), "x", 1, seed=23, plate=(1.3,1.8))
B.shingle("Head", ["furD","fur"], (0,-0.8,15.6), (7,6,3.4), "x", -1, seed=24, plate=(1.3,1.8))
for side in (1,-1):
    B.shingle("LeftUpperArm" if side>0 else "RightUpperArm", ["furD","fur"], (side*5.0,0,10.3), (2.2,2.2,1.6), "x", side, seed=25+side, plate=(0.9,1.3))
    B.shingle("LeftLeg" if side>0 else "RightLeg", ["furD","fur"], (side*2.6,0.6,2.1), (3.6,4,2.0), "x", side, seed=27+side, plate=(1.0,1.4))
# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(1.6,-3.8,15.0), eye_size=(1.2,1.2), mouth=(0,-4.7,12.55), mouth_w=1.7, iris="iris", lid="furD", buck=True)
# carrot moved over the right shoulder so it shows (was hidden flat on the back)
from mathutils import Vector as _V
for _i, _it in enumerate(B.items):
    if _it[0] == "Body" and _it[1] in ("orange", "orangeD", "leaf", "leafD"):
        B.items[_i] = (_it[0], _it[1], _it[2], _it[3] + _V((-3.4, 0.2, 1.6)), _it[4], _it[5], _it[6])
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.6,11.4)),
     "LeftUpperArm": ("Body", (4.2,0,10.6)), "RightUpperArm": ("Body", (-4.2,0,10.6)),
     "LeftLowerArm": ("LeftUpperArm", (5.1,-0.2,8.2)), "RightLowerArm": ("RightUpperArm", (-5.1,-0.2,8.2)),
     "LeftHand": ("LeftLowerArm", (5.2,-0.4,6.0)), "RightHand": ("RightLowerArm", (-5.2,-0.4,6.0)),
     "LeftLeg": ("Body", (2.6,0.6,4.6)), "RightLeg": ("Body", (-2.6,0.6,4.6))}
B.build(J)
