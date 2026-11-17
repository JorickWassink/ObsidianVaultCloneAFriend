# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"obs":(48,43,60),"obsD":(30,27,40),"belly":(80,68,104),"wing":(62,50,88),"wingD":(44,36,66),"horn":(217,210,233),"hornD":(168,158,194),
       "gold":(232,172,24),"rune":(150,50,255),"gem":(180,90,255),"dark":(14,12,18)}
NAMES = {"obs":"Scales","obsD":"ScalesDark","belly":"Belly","wing":"Wing","wingD":"WingDark","horn":"Horn","hornD":"HornDark","gold":"Crown","rune":"Rune","gem":"Gem","dark":"Dark"}
B = L["Builder"]("P10", PAL, {"Body":"obs","Head":"obs"}, glow=("rune","gem"), names=NAMES, offset=(318,40,0))
B.add("Body","obs",(4.6,4,4),(0,0,3.0))
B.add("Body","belly",(2.8,0.6,3),(0,-2.1,3.0))
B.add("Body","gem",(0.8,0.4,0.8),(0,-2.45,3.4),(0,45,0))
B.sym("Body","obsD",(1.6,2.2,1.0),(1.3,-0.4,0.5))
B.sym("Body","horn",(0.4,0.6,0.4),(1.3,-1.6,0.25))
B.sym("Body","obsD",(1.2,1.4,1.8),(2.9,-0.3,3.0),(0,10,0))
# little wings on the back, spar tucked under the head, membrane hanging between two finger bones
B.sym("Body","obsD",(1.0,1.2,1.0),(1.8,2.5,4.0))   # wing joint on the back
sz = L["wing"](B, "Body", (1.8,4.0), 45, 3.8, 0.6, 2.9, [(1.0,-0.4,2.3),(0.55,0.0,2.6)],
     {"spar":"obsD","finger":"obsD","finger_th":0.4,"mem":["wing","wing"]}, mem_th=0.3, strip=0.6, scallop=0.5, inner=(2.3,3.3), seed=3)
B.sym("Body","rune",(0.8,0.2,0.25),(3.4,2.67,sz(3.4)-1.5))
B.add("Body","obs",(1.4,2.6,1.4),(0,2.8,1.6),(-20,0,0))
B.add("Body","rune",(1.0,0.4,1.0),(0,4.2,1.0),(0,45,0))
B.add("Head","obs",(6.6,6,5.4),(0,-0.6,7.8))
B.add("Head","obs",(3.8,2,2.2),(0,-4.4,6.8))
B.sym("Head","rune",(0.4,0.3,0.4),(0.8,-5.45,7.2))
B.face = "Eyes_Happy"; B.sym("Head","gem",(1.4,0.3,1.0),(1.8,-3.7,8.8)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","dark",(0.5,0.32,0.5),(1.6,-3.75,8.7)); B.face = None
B.sym("Head","obsD",(1.6,0.4,0.4),(1.8,-3.75,9.8),(0,-16,0))
B.sym("Head","horn",(0.9,0.9,2.8),(2.0,0.2,11.4),(-28,-12,0))
B.sym("Head","hornD",(0.7,0.7,1.8),(3.0,0.6,10.2),(-50,-35,0))
B.add("Head","gold",(4.4,3.8,0.9),(0,-1.0,10.9))
for p in ((1.6,-2.6,11.8),(-1.6,-2.6,11.8)):
    B.add("Head","gold",(0.7,0.7,1.2),p)
B.add("Head","gold",(0.7,0.7,1.6),(0,-2.7,12.0))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((1.8,-3.6,8.8), 1.4, col="gem")
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,5.1))}
B.build(J)
