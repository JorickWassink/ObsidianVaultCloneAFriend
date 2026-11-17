# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy, math
L = bpy.app.driver_namespace["studlib"]
PAL = {"obs":(48,43,60),"obsD":(30,27,40),"belly":(80,68,104),"bellyD":(60,51,82),"wing":(62,50,88),"wingD":(44,36,66),"horn":(217,210,233),
       "hornD":(168,158,194),"gold":(232,172,24),"rune":(150,50,255),"gem":(180,90,255),"dark":(14,12,18)}
NAMES = {"obs":"Scales","obsD":"ScalesDark","belly":"Belly","bellyD":"BellyDark","wing":"Wing","wingD":"WingDark","horn":"Horn","hornD":"HornDark",
         "gold":"Crown","rune":"Rune","gem":"Gem","dark":"Dark"}
MAIN = {"Body":"obs","Head":"obs","LeftUpperArm":"obs","RightUpperArm":"obs","LeftLowerArm":"obsD","RightLowerArm":"obsD","LeftHand":"obs","RightHand":"obs",
        "LeftLeg":"obs","RightLeg":"obs","LeftWing":"obsD","RightWing":"obsD","Tail":"obs"}
B = L["Builder"]("B10", PAL, MAIN, glow=("rune","gem"), names=NAMES, offset=(318,0,0))
# legs
B.mirror("LeftLeg","obs",(5,5.6,5.4),(4.2,0.6,6.3))
B.mirror("LeftLeg","obsD",(3.0,3.6,2.2),(4.0,0.6,9.8))   # hip block reaching up into the torso
B.mirror("LeftLeg","obsD",(3.6,4,4),(4.2,-0.1,3.0))
B.mirror("LeftLeg","obsD",(5,7,1.6),(4.2,-1.4,0.8))
for x in (-1.6,0,1.6):
    B.mirror("LeftLeg","horn",(0.9,1.6,0.9),(4.2+x,-5.5,0.55))
B.mirror("LeftLeg","rune",(0.3,2.4,0.4),(6.75,0.6,7.4))
# torso
B.add("Body","obs",(12,9,10.4),(0,0.6,14.9))
B.mirror("LeftWing","obsD",(2.0,2.0,2.0),(4.2,4.4,19.8))   # wing root knob in the shoulder
B.add("Body","belly",(8,1,8.8),(0,-4.2,15.0))
for z in (11.0,13.0,15.0,17.0):
    B.add("Body","bellyD",(8.1,1.1,0.4),(0,-4.2,z))
for z in (18.6,15.9,13.2):
    B.add("Body","gem",(1.5,0.6,1.5),(0,-4.95,z),(0,45,0))
for sx in (1,-1):
    B.add("Body","rune",(0.3,0.5,4.4),(sx*6.1,-1.6,15.0))
    B.add("Body","rune",(0.3,3.4,0.5),(sx*6.16,-0.1,17.0))
    B.add("Body","rune",(0.3,0.9,0.9),(sx*6.22,1.6,13.6),(45,0,0))
for i,z in enumerate((19.6,17.2,14.8,12.4)):
    B.add("Body","hornD",(1.4,1.4,2.4),(0,5.3,z),(-30,0,0))
B.add("Body","obs",(5,5,4),(0,-1.6,21.8))
B.shingle("Body", ["obsD","obs"], (0,0.6,14.9), (12,9,10.4), "x", 1, seed=131, plate=(1.8,2.8))
B.shingle("Body", ["obsD","obs"], (0,0.6,14.9), (12,9,10.4), "x", -1, seed=132, plate=(1.8,2.8))
B.shingle("Body", ["obsD","obs"], (0,-1.6,21.8), (5,5,4), "x", 1, seed=133, plate=(1.2,1.8))
B.shingle("Body", ["obsD","obs"], (0,-1.6,21.8), (5,5,4), "x", -1, seed=134, plate=(1.2,1.8))
# head
B.add("Head","obs",(8,7,6),(0,-3.4,26.6))
B.add("Head","obs",(6,5,3.6),(0,-8.6,25.6))
B.add("Head","obsD",(5.6,5,1.4),(0,-8.0,23.4))
for y in (-7.4,-8.6,-9.8):
    B.sym("Head","horn",(0.6,0.6,0.9),(2.2,y,24.3))
B.sym("Head","rune",(0.6,0.3,0.6),(1.4,-11.15,26.6))
B.sym("Head","obsD",(2.6,0.6,0.7),(2.6,-7.1,28.7),(0,-18,0))
B.sym("Head","horn",(1.6,1.6,6),(2.8,-1.4,31.6),(-30,-12,0))
B.sym("Head","hornD",(1.2,1.2,4),(4.0,-0.4,29.4),(-55,-35,0))
B.add("Head","gold",(6,5,1.2),(0,-3.6,30.2))
for p in ((2.4,-5.6,31.6),(-2.4,-5.6,31.6),(0,-5.8,31.65),(2.6,-1.9,31.4),(-2.6,-1.9,31.4)):
    B.add("Head","gold",(1,1,1.8),p)
B.add("Head","rune",(1,0.4,1),(0,-6.25,30.2),(0,45,0))
B.shingle("Head", ["obsD","obs"], (0,-3.4,26.6), (8,7,6), "x", 1, seed=135, plate=(1.4,2.2))
B.shingle("Head", ["obsD","obs"], (0,-3.4,26.6), (8,7,6), "x", -1, seed=136, plate=(1.4,2.2))
# arms
B.mirror("LeftUpperArm","obs",(3.4,3.4,5),(7.6,0,17.4))
B.mirror("LeftLowerArm","obsD",(3,3,4.4),(8.0,-0.8,13.0))
B.mirror("LeftHand","obs",(3.4,3.6,2.4),(8.0,-1.2,10.0))
for x in (-1.0,0,1.0):
    B.mirror("LeftHand","horn",(0.6,1.2,1.4),(8.0+x,-3.2,9.0))
for sx in (1,-1):
    B.shingle("LeftUpperArm" if sx>0 else "RightUpperArm", ["obsD","obs"], (sx*7.6,0,18.2), (3.4,3.4,3.4), "x", sx, seed=137+sx, plate=(1.2,1.8))
    B.shingle("LeftLeg" if sx>0 else "RightLeg", ["obsD","obs"], (sx*4.2,0.6,6.3), (5,5.6,5.4), "y", -1, seed=139+sx, plate=(1.4,2.0))
# great wings (left = +X): spar from the shoulder blade, three finger bones, membrane strips tucked under the spar
sz = L["wing"](B, "LeftWing", (4.67,20.4), 50, 16, 1.8, 5.4,
     [(1.0,-1.2,15.0), (0.7,-0.5,15.0), (0.42,0.3,16.2)],
     {"spar":"obsD", "finger":"obsD", "finger_th":1.0, "mem":["wing","wingD","wing"]},
     mem_th=0.5, strip=1.4, scallop=1.8, inner=(6.9,18.2), tip=("horn",2.2), seed=10)
# glowing runes painted on the front of the membrane
B.mirror("LeftWing","rune",(0.4,0.3,5.0),(11.6,5.03,sz(11.6)-4.0),(0,50,0))
B.mirror("LeftWing","rune",(0.4,0.3,3.0),(14.4,5.03,sz(14.4)-6.5))
B.mirror("LeftWing","rune",(1.0,0.3,1.0),(8.4,5.03,sz(8.4)-3.6),(0,45,0))
# tail
for i in range(8):
    s = 1 - i*0.1
    B.add("Tail","obs" if i%2==0 else "obsD",(3.6*s,3.0,3.2*s),(0,5.6+i*2.1,9.0-i*1.0))
    B.add("Tail","hornD",(0.8,0.8,1.6*s),(0,5.6+i*2.1,9.0-i*1.0+1.6*s+0.55*s),(-25,0,0))
B.add("Tail","rune",(2.2,0.6,2.2),(0,22.1,2.0),(0,45,0))
# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(2.6,-6.85,27.7), eye_size=(1.6,1.0), mouth=None, mouth_w=0, iris="obsD", lid="obsD", white="gem", pupil="obsD", highlight=False)   # glowing eyes; snout stays
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-2.6,23.8)),
     "LeftUpperArm": ("Body", (6.2,0,19.6)), "RightUpperArm": ("Body", (-6.2,0,19.6)),
     "LeftLowerArm": ("LeftUpperArm", (7.9,-0.4,15.0)), "RightLowerArm": ("RightUpperArm", (-7.9,-0.4,15.0)),
     "LeftHand": ("LeftLowerArm", (8.0,-1.0,11.4)), "RightHand": ("RightLowerArm", (-8.0,-1.0,11.4)),
     "LeftLeg": ("Body", (4.2,0.6,9.6)), "RightLeg": ("Body", (-4.2,0.6,9.6)),
     "LeftWing": ("Body", (4.0,4.6,19.8)), "RightWing": ("Body", (-4.0,4.6,19.8)),
     "Tail": ("Body", (0,4.8,10.0))}
B.build(J)
