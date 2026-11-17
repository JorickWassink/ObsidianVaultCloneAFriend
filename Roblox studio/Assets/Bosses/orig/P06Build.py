# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"hide":(138,144,153),"hideD":(111,117,126),"snout":(160,166,173),"horn":(233,226,207),"dark":(26,24,26),"armor":(240,234,216),
       "gold":(222,176,40),"blue":(47,111,214),"glowGold":(255,184,30),"glint":(255,255,255)}
NAMES = {"hide":"Hide","hideD":"HideDark","snout":"Snout","horn":"Horn","dark":"Dark","armor":"Armor","gold":"Trim","blue":"Tabard","glowGold":"HornGlow","glint":"Glint"}
B = L["Builder"]("P06", PAL, {"Body":"hide","Head":"hide"}, glow=("glowGold",), names=NAMES, offset=(155,40,0))
B.add("Body","hide",(5,6.4,3.6),(0,1.2,2.8))
B.add("Body","armor",(5.4,4,0.8),(0,1.4,4.9))
B.add("Body","gold",(5.5,0.5,0.4),(0,-0.4,4.9))
B.sym("Body","blue",(0.4,3.6,2.4),(2.65,1.6,2.8))
for y in (-0.8, 3.4):
    B.sym("Body","hideD",(1.6,1.6,1.4),(1.5,y,0.7))
B.add("Body","hide",(0.6,1.2,0.6),(0,4.7,3.8))
B.add("Head","hide",(6.4,5.4,5.4),(0,-3.4,5.2))
B.add("Head","snout",(4,1.8,2.6),(0,-6.9,4.3))
B.sym("Head","dark",(0.5,0.3,0.5),(0.9,-7.85,4.7))
B.face = "Eyes_Happy"; B.sym("Head","dark",(1.1,0.3,1.2),(2.3,-6.15,6.4)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","glint",(0.4,0.32,0.4),(2.05,-6.2,6.75)); B.face = None
B.sym("Head","dark",(1.4,0.3,0.4),(2.3,-6.15,7.4),(0,-14,0))
B.sym("Head","hide",(1.2,0.8,1.4),(2.6,-1.4,8.4),(0,-15,0))
B.add("Head","horn",(1.4,1.4,2.0),(0,-7.3,6.4),(-20,0,0))
B.add("Head","glowGold",(1.0,1.0,1.0),(0,-7.0,7.8),(-20,0,0))
B.add("Head","armor",(6.8,4,0.9),(0,-2.8,8.2))
B.add("Head","gold",(6.9,0.4,0.4),(0,-4.75,8.2))

B.shingle("Head", ["hideD","hide"], (0,-3.4,5.2), (6.4,5.4,5.4), "x", 1, seed=100, plate=(1.2,1.8))
B.shingle("Head", ["hideD","hide"], (0,-3.4,5.2), (6.4,5.4,5.4), "x", -1, seed=101, plate=(1.2,1.8))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((2.3,-6.1,6.4), 1.1)
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-1.2,4.0))}
B.build(J)
