
import bpy
L = bpy.app.driver_namespace["studlib"]
# Restyle (ADR 0017): SmoothLib, rounded belly patch, blocky cartoon face (static eyes + mouth removed).
PAL = {"iris":(236,160,20),"fur":(118,86,58),"furD":(86,62,42),"light":(196,160,118),"dark":(30,26,26),"red":(216,60,50),"redD":(181,47,39),
       "white":(244,239,230),"scar":(62,47,34)}
NAMES = {"fur":"Fur","furD":"FurDark","light":"Light","dark":"Dark","red":"Cape","redD":"CapeDark","white":"White","scar":"Scar"}
MAIN = {"Body":"fur","Head":"fur","LeftUpperArm":"fur","RightUpperArm":"fur","LeftLowerArm":"furD","RightLowerArm":"furD",
        "LeftHand":"furD","RightHand":"furD","LeftLeg":"furD","RightLeg":"furD"}
B = L["Builder"]("B01", PAL, MAIN, names=NAMES, offset=(0,0,0))
# legs + feet
B.mirror("LeftLeg","furD",(3.4,3.6,4),(2.6,0.2,2.8))
B.mirror("LeftLeg","fur",(4,5,1.4),(2.6,-0.6,0.7))
for x in (-1.2,0,1.2):
    B.mirror("LeftLeg","white",(0.7,0.8,0.6),(2.6+x,-3.25,0.35))
# body
B.add("Body","fur",(10,7,8),(0,0,8.6))
B.add("Body","light",(6.2,1,6.4),(0,-3.6,8.2),rnd=1.4)
B.add("Body","furD",(6,3,2.2),(0,3.0,12.3))
B.add("Body","fur",(7.4,6,1.6),(0,0,4.3))
# picnic blanket cape on the back, tied at the neck
B.add("Body","red",(11,0.6,9),(0,3.9,8.3),(6,0,0))
for i in range(5):
    for j in range(4):
        if (i+j) % 2 == 0:
            z = 11.5 - j*2.2
            B.add("Body","white",(2.1,0.8,2.1),(-4.4+i*2.2, 4.2 - (z-8.3)*0.105, z),(6,0,0))
B.add("Body","red",(9,1.2,1.2),(0,-2.4,12.6))
B.add("Body","redD",(1.8,1.2,1.8),(0,-3.6,12.4),(0,45,0))
B.add("Body","red",(1.0,0.6,2.2),(0.9,-3.6,11.0),(0,-20,0))
# head
B.add("Head","fur",(6,6,5.6),(0,-2.2,15.4))
B.add("Head","light",(3.4,2.4,2.2),(0,-5.8,14.3))
B.add("Head","dark",(1.6,0.8,1.0),(0,-7.1,15.0))
B.face_blocky(eye=(1.3,-5.2,16.25), eye_size=(1.15,1.05), mouth=(0,-7.0,13.75), mouth_w=1.8, iris="iris", lid="furD")
B.sym("Head","dark",(1.8,0.4,0.5),(1.4,-5.3,17.1),(0,-15,0))
B.add("Head","fur",(1.6,1,1.6),(-2.4,-1.8,18.6))
B.add("Head","light",(0.8,0.3,0.8),(-2.4,-2.35,18.6))
B.add("Head","fur",(1.6,1,1.0),(2.4,-1.8,18.3))
B.add("Head","furD",(0.6,1.05,0.5),(2.75,-1.8,18.7))
B.add("Head","scar",(0.3,0.25,2.2),(1.0,-5.35,16.1),(0,20,0))
# arms
B.mirror("LeftUpperArm","fur",(3,3,4),(6.2,0,10.2))
B.mirror("LeftLowerArm","furD",(2.8,2.8,3.4),(6.4,-0.4,6.9))
B.mirror("LeftHand","furD",(3.2,3.4,2.2),(6.4,-0.6,4.4))
for x in (-0.9,0,0.9):
    B.mirror("LeftHand","white",(0.6,0.8,0.6),(6.4+x,-2.45,3.7))

# layered fur plates for depth
B.shingle("Body", ["furD","fur"], (0,0,8.6), (10,7,8), "x", 1, seed=1)
B.shingle("Body", ["furD","fur"], (0,0,8.6), (10,7,8), "x", -1, seed=2)
B.shingle("Head", ["furD","fur"], (0,-2.2,16.2), (6,6,3.6), "x", 1, seed=4, plate=(1.4,2.0))
B.shingle("Head", ["furD","fur"], (0,-2.2,16.2), (6,6,3.6), "x", -1, seed=5, plate=(1.4,2.0))
B.shingle("Head", ["furD","fur"], (0,-1.4,15.4), (6,4,5.6), "z", 1, seed=6, plate=(1.4,2.2))
for side, sd in ((1,7),(-1,8)):
    B.shingle("LeftUpperArm" if side>0 else "RightUpperArm", ["furD","fur"], (side*6.2,0,10.6), (3,3,2.6), "x", side, seed=sd+20, plate=(1.2,1.6))
    B.shingle("LeftLeg" if side>0 else "RightLeg", ["fur","furD"], (side*2.6,0.2,1.8), (3.4,3.6,1.6), "x", side, seed=sd+10, plate=(1.0,1.3))
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-1.6,12.8)),
     "LeftUpperArm": ("Body", (5.0,0,11.8)), "RightUpperArm": ("Body", (-5.0,0,11.8)),
     "LeftLowerArm": ("LeftUpperArm", (6.3,-0.2,8.4)), "RightLowerArm": ("RightUpperArm", (-6.3,-0.2,8.4)),
     "LeftHand": ("LeftLowerArm", (6.4,-0.5,5.5)), "RightHand": ("RightLowerArm", (-6.4,-0.5,5.5)),
     "LeftLeg": ("Body", (2.6,0.2,4.6)), "RightLeg": ("Body", (-2.6,0.2,4.6))}
B.build(J)
