# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy, math
L = bpy.app.driver_namespace["studlib"]
PAL = {"iris":(230,140,30),"fur":(74,74,82),"furD":(58,58,66),"chest":(93,93,102),"face":(150,140,132),"dark":(26,24,26),"white":(250,250,250),"whiteD":(228,228,228),
       "blue":(66,120,206),"stripe":(219,230,247),"red":(216,50,44),"pin":(222,180,122),"pinD":(176,130,74),"stache":(52,34,24),"glint":(255,255,255)}
NAMES = {"fur":"Fur","furD":"FurDark","chest":"Chest","face":"Face","dark":"Dark","white":"Cap","whiteD":"CapBand","blue":"Apron","stripe":"Stripe","red":"Scarf","pin":"RollingPin","pinD":"PinHandle","stache":"Mustache","glint":"Glint"}
MAIN = {"Body":"fur","Head":"fur","LeftUpperArm":"fur","RightUpperArm":"fur","LeftLowerArm":"furD","RightLowerArm":"furD","LeftHand":"dark","RightHand":"dark","LeftLeg":"furD","RightLeg":"furD"}
B = L["Builder"]("B05", PAL, MAIN, names=NAMES, offset=(122,0,0))
B.mirror("LeftLeg","furD",(3.2,3.4,3.4),(2.6,0.6,2.7))
B.mirror("LeftLeg","dark",(3.6,4.4,1.0),(2.6,-0.4,0.5))
B.add("Body","fur",(11,7,8),(0,0,8.4))
B.add("Body","fur",(12,6,2.6),(0,0.4,12.4))
B.add("Body","blue",(8,0.6,7),(0,-3.8,8.2))
for z in (6.0, 8.2, 10.4):
    B.add("Body","stripe",(8.1,0.7,0.5),(0,-3.8,z))
B.sym("Body","blue",(0.8,0.6,1.4),(3.0,-3.75,12.0))
B.add("Body","red",(8.2,6.8,1.2),(0,-0.6,12.15))
B.add("Body","red",(1.8,0.6,2.4),(1.8,-4.3,10.6),(0,-10,0))
# head
B.add("Head","fur",(6,5.6,5.4),(0,-1.4,16.2))
B.add("Head","furD",(6.4,1.6,1.4),(0,-4.2,17.2))
B.add("Head","face",(4.6,1,3),(0,-4.4,15.4))
B.sym("Head","dark",(1.4,0.4,0.4),(1.2,-5.05,17.0),(0,-15,0))
B.sym("Head","dark",(0.4,0.3,0.4),(0.45,-4.95,15.2))
# bushy chef handlebar mustache right under the nose: two puffy halves with a notch, tips curling up
B.sym("Head","stache",(1.5,0.8,0.9),(0.82,-5.25,14.55),(0,-6,0))
B.sym("Head","stache",(0.9,0.7,0.7),(1.75,-5.23,14.8),(0,-35,0))
B.sym("Head","stache",(0.5,0.6,0.7),(2.0,-5.15,15.3),(0,-75,0))
B.add("Head","whiteD",(6.2,5.8,1.2),(0,-1.4,19.4))
B.add("Head","white",(6.6,6.2,2),(0,-1.4,20.9))
# arms (knuckle stance)
B.mirror("LeftUpperArm","fur",(4,4,5),(7.4,0,10.0))
B.mirror("LeftLowerArm","furD",(3.6,3.6,3.8),(7.8,-0.4,6.3))
B.mirror("LeftHand","dark",(4.2,4.2,3),(7.8,-0.6,3.0))
# rolling pin gripped in the right fist: the handle runs through the fist, the roller points forward and a bit up
from mathutils import Euler, Vector
R = Euler((math.radians(70), 0, 0)).to_matrix()
ax = R @ Vector((0,0,1))
h = Vector((-7.8, -0.6, 3.0))                     # fist centre
B.add("RightHand","pinD",(1.2,1.2,4.4),tuple(h + ax*0.7),(70,0,0))          # handle in the fist
B.add("RightHand","pin",(2.6,2.6,9),tuple(h + ax*7.0),(70,0,0))             # roller
B.add("RightHand","pinD",(1.2,1.2,2.0),tuple(h + ax*12.4),(70,0,0))         # far handle

B.shingle("Body", ["furD","fur"], (0,0,8.4), (11,7,8), "x", 1, seed=51)
B.shingle("Body", ["furD","fur"], (0,0,8.4), (11,7,8), "x", -1, seed=52)
B.shingle("Body", ["furD","fur"], (0,0,8.4), (11,7,8), "y", 1, seed=53)
B.shingle("Head", ["furD","fur"], (0,-1.4,17.6), (6,5.6,2.6), "x", 1, seed=55, plate=(1.1,1.6))
B.shingle("Head", ["furD","fur"], (0,-1.4,17.6), (6,5.6,2.6), "x", -1, seed=56, plate=(1.1,1.6))
for side in (1,-1):
    B.shingle("LeftUpperArm" if side>0 else "RightUpperArm", ["furD","fur"], (side*7.4,0,11.0), (4,4,2.4), "x", side, seed=57+side, plate=(1.2,1.6))
    B.shingle("LeftLowerArm" if side>0 else "RightLowerArm", ["fur","furD"], (side*7.8,-0.4,6.0), (3.6,3.6,1.8), "x", side, seed=61+side, plate=(1.0,1.4))
# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(1.2,-4.9,16.2), eye_size=(1.05,0.95), mouth=(0,-4.95,13.9), mouth_w=1.5, iris="iris", lid="furD")
B.scale_part("Head", 1.18, (0,-1.0,13.4))   # restyle: bigger head (was small for his body)
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-1.0,13.4)),
     "LeftUpperArm": ("Body", (6.0,0,12.0)), "RightUpperArm": ("Body", (-6.0,0,12.0)),
     "LeftLowerArm": ("LeftUpperArm", (7.8,-0.2,8.0)), "RightLowerArm": ("RightUpperArm", (-7.8,-0.2,8.0)),
     "LeftHand": ("LeftLowerArm", (7.8,-0.5,4.5)), "RightHand": ("RightLowerArm", (-7.8,-0.5,4.5)),
     "LeftLeg": ("Body", (2.6,0.6,4.6)), "RightLeg": ("Body", (-2.6,0.6,4.6))}
B.build(J)
