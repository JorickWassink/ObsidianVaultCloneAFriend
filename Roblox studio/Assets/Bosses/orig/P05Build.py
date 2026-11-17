# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"fur":(74,74,82),"furD":(58,58,66),"face":(150,140,132),"dark":(26,24,26),"white":(250,250,250),"whiteD":(228,228,228),"blue":(66,120,206),"stripe":(219,230,247),"red":(216,50,44),"pin":(222,180,122),"pinD":(176,130,74),"stache":(52,34,24),"glint":(255,255,255)}
NAMES = {"fur":"Fur","furD":"FurDark","face":"Face","dark":"Dark","white":"Cap","whiteD":"CapBand","blue":"Apron","stripe":"Stripe","red":"Scarf","pin":"RollingPin","pinD":"PinHandle","stache":"Mustache","glint":"Glint"}
B = L["Builder"]("P05", PAL, {"Body":"fur","Head":"fur"}, names=NAMES, offset=(122,40,0))
B.add("Body","fur",(5.4,4,4),(0,0,3.0))
B.add("Body","blue",(3.4,0.5,3),(0,-2.2,2.8))
B.add("Body","stripe",(3.5,0.6,0.4),(0,-2.2,2.4))
B.sym("Body","dark",(1.8,2.2,1.0),(1.4,-0.4,0.5))
B.sym("Body","fur",(1.8,1.8,2.4),(3.4,-0.2,2.8),(0,8,0))
B.sym("Body","dark",(1.9,1.9,1.2),(3.5,-0.3,1.2))
# little rolling pin held in the right fist, pointing forward
B.add("Body","pinD",(0.5,0.5,2.2),(-3.50,-0.58,1.30),(70,0,0))
B.add("Body","pin",(1.0,1.0,3.4),(-3.50,-2.93,2.16),(70,0,0))
B.add("Body","pinD",(0.5,0.5,0.8),(-3.50,-4.86,2.86),(70,0,0))
B.add("Body","red",(5.6,4.4,0.8),(0,-0.1,4.9))
B.add("Head","fur",(6.6,6,5.6),(0,-0.4,7.9))
B.add("Head","furD",(6.8,1.2,1.0),(0,-3.4,9.1))
B.add("Head","face",(4.6,0.8,3),(0,-3.6,7.3))
B.face = "Eyes_Happy"; B.sym("Head","dark",(1.0,0.3,1.0),(1.3,-4.1,8.0)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","glint",(0.35,0.32,0.35),(1.1,-4.15,8.3)); B.face = None
B.sym("Head","dark",(1.5,0.3,0.4),(1.3,-4.05,9.1),(0,-14,0))
# bushy handlebar mustache under the nose
B.sym("Head","dark",(0.3,0.3,0.3),(0.35,-4.12,7.25))
B.sym("Head","stache",(1.3,0.6,1.0),(0.7,-4.25,6.6),(0,-6,0))
B.sym("Head","stache",(0.7,0.52,0.75),(1.5,-4.24,6.85),(0,-30,0))
B.sym("Head","stache",(0.42,0.46,0.55),(1.75,-4.23,7.32),(0,-70,0))
B.add("Head","whiteD",(6.8,6.2,1.0),(0,-0.4,11.2))
B.add("Head","white",(7.2,6.6,1.8),(0,-0.4,12.6))

B.shingle("Head", ["furD","fur"], (0,-0.4,7.9), (6.6,6,5.6), "x", 1, seed=98, plate=(1.2,2.0))
B.shingle("Head", ["furD","fur"], (0,-0.4,7.9), (6.6,6,5.6), "x", -1, seed=99, plate=(1.2,2.0))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((1.3,-4.0,8.0), 1.0)
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,5.1))}
B.build(J)
