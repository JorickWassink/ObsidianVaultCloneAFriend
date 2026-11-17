# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"bone":(232,226,208),"boneD":(189,182,162),"mem":(62,58,76),"memD":(44,42,56),"dark":(18,18,22),"soul":(40,255,100)}
NAMES = {"bone":"Bone","boneD":"BoneDark","mem":"Membrane","memD":"MembraneDark","dark":"Dark","soul":"Soul"}
B = L["Builder"]("P09", PAL, {"Body":"boneD","Head":"bone"}, glow=("soul",), names=NAMES, offset=(268,40,0))
B.add("Body","boneD",(3.6,2.4,1.2),(0,0.4,1.2))
for i,z in enumerate((2.15,3.2,4.2)):
    B.sym("Body","bone",(0.6,3.2,0.6),(1.5,0.0,z))
    B.sym("Body","boneD",(1.3,0.6,0.5),(0.75,1.3,z))   # rib joins the spine
B.add("Body","bone",(1.0,1.0,3.6),(0,1.4,3.2))
B.add("Body","soul",(1.8,1.8,1.8),(0,-0.2,3.2),(0,45,30))
B.sym("Body","bone",(0.8,1.6,1.4),(1.2,-0.2,0.4))
B.sym("Body","bone",(0.7,0.7,2.2),(2.4,-0.4,3.0))
B.sym("Body","boneD",(0.9,0.9,0.9),(2.0,-0.33,4.0))   # shoulder joint
# little torn wings growing from the spine, tucked under the skull
B.sym("Body","boneD",(0.8,1.0,0.8),(0.6,2.3,3.8))   # wing joint on the spine
L["wing"](B, "Body", (0.6,3.8), 45, 4.0, 0.5, 2.7, [(1.0,-0.4,1.6),(0.6,0.0,2.0)],
     {"spar":"bone","finger":"boneD","finger_th":0.35,"mem":["memD","mem"]}, mem_th=0.3, strip=0.6, scallop=0.4, inner=(1.0,3.0), seed=4, tear=0.3)
B.add("Body","bone",(0.7,2.4,0.7),(0,2.6,1.4),(-20,0,0))
B.add("Head","bone",(6.2,5.6,5.0),(0,-0.6,7.6))
B.add("Head","bone",(3.6,2,2.2),(0,-4.2,6.6))
B.add("Head","boneD",(3.4,2.4,0.7),(0,-3.6,5.2),(8,0,0))
B.face = "Eyes_Happy"; B.sym("Head","dark",(1.6,0.3,1.6),(1.6,-3.5,8.4)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","soul",(0.6,0.35,0.6),(1.6,-3.6,8.4)); B.face = None
B.sym("Head","dark",(0.3,0.3,0.3),(0.6,-5.25,7.2))
B.sym("Head","boneD",(1.6,0.4,0.4),(1.6,-3.55,9.5),(0,-15,0))
B.sym("Head","bone",(0.9,0.9,2.6),(1.8,0.2,11.0),(-30,-10,0))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((1.6,-3.4,8.4), 1.5, col="dark")
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,5.0))}
B.build(J)
