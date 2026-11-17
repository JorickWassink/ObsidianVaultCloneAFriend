# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"iris":(220,150,40),"fur":(224,168,74),"furD":(190,136,52),"mane":(154,90,36),"maneD":(122,67,24),"light":(246,220,166),"nose":(90,58,42),"dark":(26,24,26),
       "red":(184,36,44),"ermine":(244,244,244),"gold":(232,172,24),"gem":(216,50,44),"orb":(30,160,255),"glint":(255,255,255)}
NAMES = {"fur":"Fur","furD":"FurDark","mane":"Mane","maneD":"ManeDark","light":"Light","nose":"Nose","dark":"Dark","red":"Cape","ermine":"Ermine",
         "gold":"Gold","gem":"Gem","orb":"Orb","glint":"Glint"}
MAIN = {"Body":"fur","Head":"mane","LeftUpperArm":"fur","RightUpperArm":"fur","LeftLowerArm":"furD","RightLowerArm":"furD","LeftHand":"light","RightHand":"light","LeftLeg":"furD","RightLeg":"furD"}
B = L["Builder"]("B07", PAL, MAIN, glow=("orb",), names=NAMES, offset=(190,0,0))
B.mirror("LeftLeg","furD",(3.2,3.4,3.6),(2.5,0.4,2.8))
B.mirror("LeftLeg","light",(3.6,4.6,1.2),(2.5,-0.4,0.6))
B.add("Body","fur",(8,6,8),(0,0,8.6))
B.add("Body","light",(5,1,6),(0,-3.1,8.4))
# royal cape with an ermine collar
B.add("Body","red",(10.6,0.6,11),(0,3.5,8.0),(4,0,0))
B.add("Body","ermine",(11,7.4,1.4),(0,0.2,12.2))
for x in (-3.6,-1.2,1.2,3.6):
    B.add("Body","dark",(0.4,0.3,0.6),(x,-3.6,12.2))
B.add("Body","fur",(1,1,5),(2.6,4.4,3.4),(0,-40,0))
B.add("Body","maneD",(1.8,1.8,1.8),(4.7,4.4,5.4))
# head: big mane, face, crown
B.add("Head","mane",(10,8,9.6),(0,-0.4,17.0))
B.add("Head","maneD",(8,2,8),(0,3.8,16.6))
B.add("Head","fur",(6.4,1,6),(0,-4.8,16.6))
B.add("Head","light",(3.6,1.6,2.4),(0,-5.9,15.2))
B.add("Head","nose",(1.4,0.6,0.8),(0,-6.85,16.0))
B.sym("Head","dark",(1.6,0.4,0.4),(1.5,-5.5,18.5),(0,-15,0))
B.sym("Head","fur",(1.6,1,1.6),(3.4,-1.6,22.4))
B.add("Head","gold",(6,5,1.6),(0,-0.6,22.6))
for p in ((2.3,-2.6,24.0),(-2.3,-2.6,24.0),(2.3,1.4,24.0),(-2.3,1.4,24.0)):
    B.add("Head","gold",(1.2,1.2,1.4),p)
B.add("Head","gold",(1.2,1.2,1.8),(0,-2.6,24.2))   # taller centre point
B.add("Head","gem",(0.8,0.4,0.8),(0,-3.25,22.6)); B.sym("Head","gem",(0.6,0.4,0.6),(1.8,-3.25,22.6))
# arms
B.mirror("LeftUpperArm","fur",(2.6,2.6,3.2),(5.4,0,10.2))
B.mirror("LeftLowerArm","furD",(2.4,2.4,3),(5.6,-0.4,7.2))
B.mirror("LeftHand","light",(2.8,3,2),(5.6,-0.6,5.0))
# scepter with a glowing orb in the right paw
# fingers wrap around the staff in front of the palm
B.add("RightHand","light",(2.4,1.6,1.6),(-5.6,-2.5,5.0))
B.add("RightHand","gold",(0.8,0.8,12),(-5.6,-2.5,8.0))
B.add("RightHand","gold",(1.8,1.8,0.6),(-5.6,-2.5,14.1))
B.add("RightHand","orb",(2.4,2.4,2.4),(-5.6,-2.5,15.6))
B.add("RightHand","gold",(1.2,1.2,0.6),(-5.6,-2.5,2.0))

for sx in (1,-1):
    B.shingle("Head", ["maneD","mane"], (0,-0.4,17.0), (10,8,9.6), "x", sx, seed=74+sx, plate=(1.6,2.6))
    B.shingle("Body", ["furD","fur"], (0,0,8.6), (8,6,8), "x", sx, seed=76+sx)
    B.shingle("LeftUpperArm" if sx>0 else "RightUpperArm", ["furD","fur"], (sx*5.4,0,10.9), (2.6,2.6,1.8), "x", sx, seed=78+sx, plate=(1.0,1.6))
B.shingle("Head", ["maneD","mane"], (0,-0.4,17.0), (10,8,9.6), "y", 1, seed=80, plate=(1.6,2.6))
B.shingle("Head", ["maneD","mane"], (-3.5,-0.4,17.0), (3,8,9.6), "y", -1, seed=81, plate=(1.2,2.0))
B.shingle("Head", ["maneD","mane"], (3.5,-0.4,17.0), (3,8,9.6), "y", -1, seed=82, plate=(1.2,2.0))
# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(1.5,-5.3,17.6), eye_size=(1.15,1.15), mouth=(0,-6.7,14.35), mouth_w=1.8, iris="iris", lid="furD")
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.6,12.6)),
     "LeftUpperArm": ("Body", (4.4,0,12.0)), "RightUpperArm": ("Body", (-4.4,0,12.0)),
     "LeftLowerArm": ("LeftUpperArm", (5.5,-0.2,8.8)), "RightLowerArm": ("RightUpperArm", (-5.5,-0.2,8.8)),
     "LeftHand": ("LeftLowerArm", (5.6,-0.5,6.2)), "RightHand": ("RightLowerArm", (-5.6,-0.5,6.2)),
     "LeftLeg": ("Body", (2.5,0.4,4.8)), "RightLeg": ("Body", (-2.5,0.4,4.8))}
B.build(J)
