# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"iris":(140,210,40),"fur":(141,147,156),"furD":(108,114,123),"light":(236,234,230),"dark":(30,26,26),"belly":(185,190,198),"red":(210,58,50),
       "sack":(201,167,106),"sackD":(138,106,58),"gold":(242,201,76)}
NAMES = {"fur":"Fur","furD":"FurDark","light":"Light","dark":"Mask","belly":"Belly","red":"Bandana","sack":"Sack","sackD":"SackTie","gold":"Coins"}
MAIN = {"Body":"fur","Head":"fur","LeftUpperArm":"fur","RightUpperArm":"fur","LeftLowerArm":"furD","RightLowerArm":"furD","LeftHand":"dark","RightHand":"dark","LeftLeg":"furD","RightLeg":"furD"}
B = L["Builder"]("B03", PAL, MAIN, names=NAMES, offset=(60,0,0))
B.mirror("LeftLeg","furD",(3.2,3.4,3.6),(2.2,0.3,2.8))
B.mirror("LeftLeg","dark",(3.6,4.4,1.2),(2.2,-0.5,0.6))
B.add("Body","fur",(8,6,7),(0,0,7.6))
B.add("Body","belly",(5,1,3.4),(0,-3.1,8.2))
for i,(p,c) in enumerate((((2.4,3.6,5.6),"fur"),((3.2,5.2,6.8),"dark"),((3.6,6.4,8.6),"fur"),((3.7,7.0,10.6),"dark"),((3.6,7.2,12.4),"fur"))):
    B.add("Body", c, (2.6,2.6,2.2), p, (20+i*10,0,0))
# loot sack slung over the right shoulder
B.add("Body","sack",(5,5,5.6),(-4.4,4.9,9.6),(0,10,0))
B.add("Body","sackD",(1.8,1.8,1.2),(-4.8,4.4,12.8))
B.add("Body","gold",(1.8,0.3,1.8),(-4.4,7.45,9.6))
B.add("Body","sackD",(0.8,0.5,5.2),(-2.0,-3.3,9.2),(0,-30,0))
for p,r in (((-3.6,4.6,13.4),(0,30,0)),((-5.6,4.2,13.2),(0,-20,10)),((-4.6,5.2,13.8),(60,0,0))):
    B.add("Body","gold",(1,1,0.3),p,r)
# head
B.add("Head","fur",(7.6,6,6),(0,-0.6,14.0))
B.add("Head","dark",(7.8,6.2,2),(0,-0.6,14.6))
B.sym("Head","light",(2.6,0.4,0.6),(1.7,-3.75,16.0),(0,-12,0))
B.add("Head","light",(3.6,1.6,2),(0,-4.2,12.4))
B.add("Head","dark",(1.2,0.6,0.8),(0,-5.0,13.2))
B.sym("Head","fur",(2,1.2,2),(2.6,-0.4,17.8))
B.sym("Head","light",(1,0.3,1),(2.6,-1.05,17.8))
# bandana
B.add("Body","red",(7.0,6.6,1.0),(0,-0.2,11.0))
B.add("Body","red",(1.8,1,1.8),(0,-3.7,10.6),(0,45,0))
B.add("Body","red",(0.8,0.6,1.8),(0.8,-3.8,9.4),(0,-25,0))
# arms
B.mirror("LeftUpperArm","fur",(2.4,2.4,3.4),(5.4,0,9.6))
B.mirror("LeftLowerArm","furD",(2.2,2.2,2.6),(5.6,-0.3,7.0))
B.mirror("LeftHand","dark",(2.6,2.6,1.8),(5.6,-0.6,5.2))

B.shingle("Body", ["furD","fur"], (0,0,8.8), (8,6,4.0), "x", 1, seed=31)
B.shingle("Body", ["furD","fur"], (0,0,8.8), (8,6,4.0), "x", -1, seed=32)
B.shingle("Head", ["furD","fur"], (0,-0.6,14.0), (7.6,6,6), "z", 1, seed=33, plate=(1.4,2.2))
for side in (1,-1):
    B.shingle("LeftUpperArm" if side>0 else "RightUpperArm", ["furD","fur"], (side*5.4,0,10.4), (2.4,2.4,1.6), "x", side, seed=35+side, plate=(0.9,1.3))

# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(1.6,-3.7,14.6), eye_size=(1.3,1.15), mouth=(0,-5.0,11.95), mouth_w=1.6, iris="iris", lid="dark")
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.6,11.2)),
     "LeftUpperArm": ("Body", (4.5,0,10.6)), "RightUpperArm": ("Body", (-4.5,0,10.6)),
     "LeftLowerArm": ("LeftUpperArm", (5.5,-0.2,8.2)), "RightLowerArm": ("RightUpperArm", (-5.5,-0.2,8.2)),
     "LeftHand": ("LeftLowerArm", (5.6,-0.4,6.0)), "RightHand": ("RightLowerArm", (-5.6,-0.4,6.0)),
     "LeftLeg": ("Body", (2.2,0.3,4.6)), "RightLeg": ("Body", (-2.2,0.3,4.6))}
B.build(J)
