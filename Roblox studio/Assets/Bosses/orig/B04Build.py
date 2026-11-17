# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"iris":(150,95,40),"fur":(201,138,85),"furD":(165,110,64),"light":(236,201,162),"ear":(215,161,132),"dark":(30,26,26),"blue":(47,111,214),
       "cuff":(244,244,244),"gold":(232,168,20),"goldL":(252,204,40),"red":(216,50,44)}
NAMES = {"fur":"Fur","furD":"FurDark","light":"Light","ear":"EarInner","dark":"Dark","blue":"Glove","cuff":"Cuff","gold":"Belt","goldL":"BeltPlate","red":"Red"}
MAIN = {"Tail":"fur","Body":"fur","Head":"fur","LeftUpperArm":"fur","RightUpperArm":"fur","LeftLowerArm":"furD","RightLowerArm":"furD","LeftHand":"blue","RightHand":"blue","LeftLeg":"furD","RightLeg":"furD"}
B = L["Builder"]("B04", PAL, MAIN, names=NAMES, offset=(90,0,0))
# legs: big haunches + long feet
B.mirror("LeftLeg","furD",(3.6,4.4,3.4),(2.5,0.6,2.7))
B.mirror("LeftLeg","fur",(3.2,7,1.2),(2.5,-1.6,0.6))
# tail
B.add("Tail","fur",(3,7,2.6),(0,6.0,2.2),(-10,0,0))
B.add("Tail","fur",(2.4,2.2,1.8),(0,2.5,4.0))   # tail root inside the rump
B.add("Tail","furD",(2.2,3,2),(0,10.2,1.1))
# body
B.add("Body","fur",(8,6,9.6),(0,0,8.9))
B.add("Body","light",(5,1,7),(0,-3.1,8.8))
B.add("Body","light",(5.4,1.6,2.4),(0,-3.6,8.0))
# joey peeking out of the pouch
B.add("Body","fur",(2.8,2.4,2.4),(0,-3.7,9.8))
B.add("Body","light",(1.4,0.6,1.0),(0,-5.05,9.4))
B.sym("Body","fur",(0.6,0.5,1.4),(0.8,-3.7,11.6))
B.sym("Body","dark",(0.4,0.2,0.45),(0.65,-4.97,10.3))
B.sym("Body","red",(1.1,1.1,1.1),(1.7,-4.6,9.0))
# champion belt
B.add("Body","gold",(8.4,6.4,1.6),(0,0,6.5))
B.add("Body","goldL",(3.6,0.8,2.0),(0,-3.5,6.5))
B.add("Body","red",(1.0,0.4,1.2),(0,-4.05,6.5))
# head
B.add("Head","fur",(5.6,5,5),(0,-1.6,16.4))
B.add("Head","fur",(3.4,3.2,1.4),(0,-1.3,13.6))   # neck
B.add("Head","light",(3.4,3,2.4),(0,-5.0,15.2))
B.add("Head","dark",(1.6,0.6,0.8),(0,-6.7,15.9))
B.sym("Head","dark",(1.6,0.4,0.4),(1.4,-4.25,18.1),(0,-15,0))
B.sym("Head","fur",(1.4,1,4),(1.7,-0.8,20.6),(0,-10,0))
B.sym("Head","ear",(0.7,0.3,3),(1.7,-1.35,20.6),(0,-10,0))
# arms with blue gloves
B.mirror("LeftUpperArm","fur",(2.2,2.2,3),(5.0,-0.4,12.0))
B.mirror("LeftLowerArm","furD",(2,2,2.4),(5.2,-1.2,9.6))
B.mirror("LeftHand","blue",(3.4,3.6,3.4),(5.2,-2.1,7.0))
B.mirror("LeftHand","cuff",(3.6,3.7,0.6),(5.2,-2.1,8.8))

B.shingle("Body", ["furD","fur"], (0,0,10.8), (8,6,5.4), "x", 1, seed=41)
B.shingle("Body", ["furD","fur"], (0,0,10.8), (8,6,5.4), "x", -1, seed=42)
B.shingle("Body", ["furD","fur"], (0,0,11.0), (8,6,4.6), "y", 1, seed=43)
B.shingle("Head", ["furD","fur"], (0,-1.6,17.4), (5.6,5,3.0), "x", 1, seed=44, plate=(1.2,1.6))
B.shingle("Head", ["furD","fur"], (0,-1.6,17.4), (5.6,5,3.0), "x", -1, seed=45, plate=(1.2,1.6))
for side in (1,-1):
    B.shingle("LeftLeg" if side>0 else "RightLeg", ["fur","furD"], (side*2.5,0.6,2.2), (3.6,4.4,2.4), "x", side, seed=47+side, plate=(1.1,1.5))
# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(1.4,-4.1,17.2), eye_size=(1.1,1.05), mouth=(0,-6.5,14.45), mouth_w=1.6, iris="iris", lid="furD")
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-1.2,13.8)),
     "LeftUpperArm": ("Body", (4.2,-0.4,12.8)), "RightUpperArm": ("Body", (-4.2,-0.4,12.8)),
     "LeftLowerArm": ("LeftUpperArm", (5.1,-0.8,10.6)), "RightLowerArm": ("RightUpperArm", (-5.1,-0.8,10.6)),
     "LeftHand": ("LeftLowerArm", (5.2,-1.4,9.0)), "RightHand": ("RightLowerArm", (-5.2,-1.4,9.0)),
     "LeftLeg": ("Body", (2.5,0.6,5.0)), "RightLeg": ("Body", (-2.5,0.6,5.0)), "Tail": ("Body", (0,2.8,4.0))}
B.build(J)
