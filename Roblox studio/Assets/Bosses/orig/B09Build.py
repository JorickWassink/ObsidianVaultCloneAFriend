# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy, math
L = bpy.app.driver_namespace["studlib"]
PAL = {"bone":(232,226,208),"boneD":(189,182,162),"boneDD":(150,143,124),"mem":(62,58,76),"memD":(44,42,56),"dark":(18,18,22),"soul":(40,255,100),"soulL":(170,255,200)}
NAMES = {"bone":"Bone","boneD":"BoneDark","boneDD":"BoneShadow","mem":"Membrane","memD":"MembraneDark","dark":"Dark","soul":"Soul","soulL":"SoulLight"}
MAIN = {"Body":"boneD","Head":"bone","LeftUpperArm":"bone","RightUpperArm":"bone","LeftLowerArm":"bone","RightLowerArm":"bone","LeftHand":"boneD","RightHand":"boneD",
        "LeftLeg":"bone","RightLeg":"bone","LeftWing":"bone","RightWing":"bone","Tail":"bone"}
B = L["Builder"]("B09", PAL, MAIN, glow=("soul","soulL"), names=NAMES, offset=(268,0,0))
# legs
B.mirror("LeftLeg","bone",(1.4,1.4,4),(3,0.6,6.0),(15,0,0))
B.mirror("LeftLeg","boneD",(2,2,2),(3,-0.1,4.0))
B.mirror("LeftLeg","bone",(1.2,1.2,3),(3,0.4,2.3),(-15,0,0))
B.mirror("LeftLeg","boneD",(3.4,4.6,1),(3,-1,0.5))
for x in (-1.1,0,1.1):
    B.mirror("LeftLeg","bone",(0.6,1.2,0.6),(3+x,-3.7,0.4))
# pelvis, spine, ribs, soul
B.add("Body","boneD",(7,4,2.4),(0,0.6,8.4))
for i in range(6):
    B.add("Body","bone" if i%2==0 else "boneD",(1.6-0.05*(i%2),1.6-0.05*(i%2),1.2),(0,1.8,9.9+i*1.2))   # vertebrae stacked, alternating shade
for i, z in enumerate((10.2, 11.4, 12.6, 13.8, 15.0)):
    w = 2.2 + 0.9*math.sin(math.pi*(i+0.5)/5)
    B.sym("Body","bone",(0.8,5.4,0.7),(w,-0.5,z))
    B.sym("Body","bone",(1.4,0.7,0.7),(w-0.9,-3.0,z))
B.add("Body","soul",(2.6,2.6,2.6),(0,-0.6,12.6),(0,45,30))
for p in ((1.75,-1.6,10.2),(-1.75,-1.6,11.4),(1.75,-1.6,13.8),(-1.75,-1.6,15.0)):   # soul wisps drifting inside the ribcage
    B.add("Body","soulL",(0.6,0.6,0.6),p,(30,45,0))
B.add("Body","boneD",(8,3,1.4),(0,0.8,16.4))
for i in range(3):
    B.add("Body","bone",(1.4-i*0.12,1.4-i*0.12,1.1),(0,0.4-i*0.7,17.5+i*0.75))
# skull
B.add("Head","bone",(5.4,5.4,4.4),(0,-3.2,21.6))
B.add("Head","bone",(3.8,4,2.6),(0,-7.0,21.0))
B.add("Head","boneD",(3.6,4.8,1.0),(0,-6.0,19.2),(10,0,0))
for x in (-1.2,-0.4,0.4,1.2):
    B.add("Head","bone",(0.5,0.5,0.8),(x,-8.4,19.95))
B.sym("Head","dark",(0.4,0.3,0.4),(0.7,-9.05,21.7))
B.sym("Head","boneD",(2.2,0.6,0.6),(1.6,-6.1,23.9),(0,-15,0))
B.sym("Head","bone",(1.2,1.2,4),(2.0,-1.4,24.8),(-35,-10,0))
B.sym("Head","boneD",(0.8,0.8,2.4),(2.9,-0.6,23.4),(-50,-15,0))
B.shingle("Head", ["boneD","bone"], (0,-3.2,21.6), (5.4,5.4,4.4), "x", 1, seed=121, plate=(1.2,1.8), thick=0.35)
B.shingle("Head", ["boneD","bone"], (0,-3.2,21.6), (5.4,5.4,4.4), "x", -1, seed=122, plate=(1.2,1.8), thick=0.35)
# arms
B.mirror("LeftUpperArm","bone",(1.2,1.2,4),(5.0,0.2,14.2))
B.mirror("LeftUpperArm","boneD",(1.5,1.5,1.5),(4.4,0.3,16.1))   # shoulder ball
B.mirror("LeftWing","boneD",(1.6,1.6,1.6),(3.5,2.6,16.6))   # wing root knob
B.mirror("LeftLowerArm","boneD",(1.8,1.8,1.8),(5.4,-0.2,12.2))
B.mirror("LeftLowerArm","bone",(1.0,1.0,3),(5.6,-0.5,10.6))
B.mirror("LeftHand","boneD",(2,2,1),(5.6,-0.8,8.8))
for x in (-0.6,0,0.6):
    B.mirror("LeftHand","bone",(0.45,0.45,1.6),(5.6+x,-1.4,7.8))
# ragged wings (left = +X): bone spar, three finger bones, torn membrane strips tucked under the spar
L["wing"](B, "LeftWing", (4.1,17.24), 55, 11, 1.3, 3.0,
     [(1.0,-0.6,14.0), (0.68,-0.2,14.2), (0.38,0.2,15.2)],
     {"spar":"bone", "finger":"boneD", "finger_th":0.7, "mem":["mem","memD","mem"]},
     mem_th=0.4, strip=1.2, scallop=1.4, inner=(5.0,15.8), tip=("boneD",1.6), seed=9, tear=0.35)
# tail
for i in range(7):
    s = 1.5 - i*0.12
    B.add("Tail","bone" if i%2==0 else "boneD",(s,s*1.1,s),(0,3.2+i*1.5,7.8-i*0.85))
B.add("Tail","bone",(0.6,1.8,0.6),(0,13.9,1.6),(20,0,0))
# spine cord running through the tail vertebrae so they read as one tail
B.add("Tail","boneDD",(0.5,13.4,0.5),(0,8.3,4.75),(-29.5,0,0))
B.add("Tail","soul",(0.7,0.7,0.7),(0,14.9,1.3),(45,0,45))
# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(1.5,-5.8,22.9), eye_size=(1.4,1.2), mouth=None, mouth_w=0, iris="soul", lid="boneD", white="dark", pupil="soulL", highlight=False)   # sockets + soul light; jaw stays
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-1.6,19.4)),
     "LeftUpperArm": ("Body", (4.2,0.4,16.2)), "RightUpperArm": ("Body", (-4.2,0.4,16.2)),
     "LeftLowerArm": ("LeftUpperArm", (5.4,-0.2,12.2)), "RightLowerArm": ("RightUpperArm", (-5.4,-0.2,12.2)),
     "LeftHand": ("LeftLowerArm", (5.6,-0.6,9.2)), "RightHand": ("RightLowerArm", (-5.6,-0.6,9.2)),
     "LeftLeg": ("Body", (3,0.6,7.8)), "RightLeg": ("Body", (-3,0.6,7.8)),
     "LeftWing": ("Body", (3.0,2.6,16.6)), "RightWing": ("Body", (-3.0,2.6,16.6)),
     "Tail": ("Body", (0,2.6,8.0))}
B.build(J)
