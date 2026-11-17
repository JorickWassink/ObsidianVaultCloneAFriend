# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"iris":(230,60,60),"mechY":(226,172,30),"mechYD":(186,136,20),"metal":(138,150,163),"metalD":(95,107,120),"chrome":(205,213,222),"shark":(98,134,172),
       "sharkD":(76,108,142),"belly":(233,238,242),"dark":(32,32,38),"mouth":(96,30,44),"white":(255,255,255),"lamp":(255,236,130),"red":(255,64,48)}
NAMES = {"mechY":"Mech","mechYD":"MechDark","metal":"Metal","metalD":"MetalDark","chrome":"Chrome","shark":"Shark","sharkD":"SharkDark","belly":"Belly",
         "dark":"Dark","mouth":"Mouth","white":"Teeth","lamp":"Headlight","red":"RedLight"}
MAIN = {"Body":"mechY","Head":"shark","LeftUpperArm":"metal","RightUpperArm":"metal","LeftLowerArm":"mechY","RightLowerArm":"mechY",
        "LeftHand":"chrome","RightHand":"chrome","LeftLeg":"metal","RightLeg":"metal"}
B = L["Builder"]("B08", PAL, MAIN, glow=("lamp","red"), names=NAMES, offset=(228,0,0))
# mech legs
B.mirror("LeftLeg","metal",(2.8,2.8,3.6),(3.4,0.4,6.2))
B.mirror("LeftLeg","metalD",(2.2,2.2,1.8),(3.4,0.4,8.5))   # hip joint into the hull
B.mirror("LeftLeg","mechY",(3.4,3.4,1.6),(3.4,0.2,4.2))
B.mirror("LeftLeg","metalD",(2.4,2.4,2.8),(3.4,0.2,2.4))
B.mirror("LeftLeg","mechY",(4.4,5.6,1.4),(3.4,-0.6,0.7))
B.mirror("LeftLeg","lamp",(1.0,0.3,0.8),(3.4,-1.55,4.2))
# mech torso
B.add("Body","mechY",(11,8,7),(0,0,11.6))
B.add("Body","dark",(10.2,0.4,1.4),(0,-4.1,9.0))
for x in (-4,-2,0,2,4):
    B.add("Body","mechY",(0.9,0.45,1.5),(x,-4.2,9.0),(0,40,0))
B.add("Body","dark",(10,0.4,2.8),(0,-4.1,12.6))
B.sym("Body","lamp",(2.2,0.5,1.6),(3.4,-4.25,12.6))
B.add("Body","red",(1.6,0.5,1.6),(0,-4.25,12.6))
B.add("Body","chrome",(9.6,7.4,1.2),(0,-0.2,15.6))
B.sym("Body","metal",(1.2,1.2,4),(3.2,4.6,15.2))
B.sym("Body","dark",(1.4,1.4,0.5),(3.2,4.6,17.3))
B.shingle("Body", ["mechYD","mechY"], (0,0,11.6), (11,8,7), "x", 1, seed=111, plate=(1.8,2.6))
B.shingle("Body", ["mechYD","mechY"], (0,0,11.6), (11,8,7), "x", -1, seed=112, plate=(1.8,2.6))
B.shingle("Body", ["mechYD","mechY"], (0,0,11.6), (8,8,7), "y", 1, seed=113, plate=(1.8,2.6))
# shark riding in the cockpit
B.add("Body","shark",(7,5,4.4),(0,0.2,17.6))
B.add("Body","belly",(5,0.6,3.0),(0,-2.55,17.3))
B.add("Body","shark",(1.2,3.4,4),(0,2.6,21.0),(22,0,0))
B.sym("Body","shark",(3.6,2,0.6),(4.6,-0.4,17.2),(0,-25,0))
# shark head
B.add("Head","shark",(7.4,7,5.4),(0,-1.2,22.4))
B.add("Head","shark",(6,3,3),(0,-5.9,22.8))
B.add("Head","belly",(6.2,5,1.6),(0,-3.6,20.3))
B.add("Head","mouth",(5.2,0.4,1.4),(0,-7.45,22.0))
for i in range(6):
    x = -2.1 + i*0.84
    B.add("Head","white",(0.6,0.5,0.6),(x,-7.6,22.5))
    B.add("Head","white",(0.6,0.5,0.6),(x+0.42,-7.6,21.5))
B.sym("Head","dark",(1.5,0.4,0.4),(3.3,-4.95,24.3),(0,-15,0))
for k in range(3):
    B.sym("Head","sharkD",(0.3,0.5,1.6),(3.75,-0.2+k*0.9,22.0))
B.shingle("Head", ["sharkD","shark"], (0,-1.2,22.4), (7.4,7,5.4), "z", 1, seed=114, plate=(1.4,2.2), tilt=5, thick=0.35)
# arms with drills
B.mirror("LeftUpperArm","metal",(2.8,2.8,4),(8.1,0,12.6))
B.mirror("LeftUpperArm","mechY",(3.4,3.8,2),(8.1,0,15.0))
B.mirror("LeftUpperArm","metalD",(2.2,1.8,1.8),(6.0,0,14.2))   # shoulder joint into the torso
B.mirror("LeftLowerArm","mechY",(3.2,3.2,3.2),(8.3,-0.6,9.2))
B.mirror("LeftLowerArm","dark",(3.3,3.3,0.5),(8.3,-0.6,10.4))
for (sz, z) in (((3,3,1.4),6.9),((2.4,2.4,1.6),5.4),((1.6,1.6,1.6),3.8),((0.8,0.8,1.4),2.4)):
    B.mirror("LeftHand","chrome",sz,(8.3,-0.6,z))
for (sz, z) in (((2.6,2.6,0.4),6.05),((2.0,2.0,0.4),4.55),((1.3,1.3,0.4),3.05)):
    B.mirror("LeftHand","metalD",sz,(8.3,-0.6,z),(0,0,45))
# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(3.3,-4.75,23.4), eye_size=(1.1,1.15), mouth=None, mouth_w=0, iris="iris", lid="sharkD")   # the shark grin stays
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.6,19.6)),
     "LeftUpperArm": ("Body", (6.9,0,14.4)), "RightUpperArm": ("Body", (-6.9,0,14.4)),
     "LeftLowerArm": ("LeftUpperArm", (8.2,-0.3,10.8)), "RightLowerArm": ("RightUpperArm", (-8.2,-0.3,10.8)),
     "LeftHand": ("LeftLowerArm", (8.3,-0.6,7.6)), "RightHand": ("RightLowerArm", (-8.3,-0.6,7.6)),
     "LeftLeg": ("Body", (3.4,0.4,8.0)), "RightLeg": ("Body", (-3.4,0.4,8.0))}
B.build(J)
