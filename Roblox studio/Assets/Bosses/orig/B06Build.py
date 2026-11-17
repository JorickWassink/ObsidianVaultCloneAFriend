# Restyle copy of the original (ADR 0017): built with SmoothLib; static eyes/mouth replaced by face_blocky.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"iris":(70,140,230),"hide":(138,144,153),"hideD":(111,117,126),"snout":(160,166,173),"horn":(233,226,207),"dark":(26,24,26),"armor":(240,234,216),
       "gold":(222,176,40),"blue":(47,111,214),"shield":(233,206,120),"glowGold":(255,184,30),"glowBlue":(80,190,255),"glint":(255,255,255)}
NAMES = {"hide":"Hide","hideD":"HideDark","snout":"Snout","horn":"Horn","dark":"Dark","armor":"Armor","gold":"Trim","blue":"Tabard",
         "shield":"Shield","glowGold":"HornGlow","glowBlue":"Gem","glint":"Glint"}
MAIN = {"Body":"hide","Head":"hide","LeftFrontLeg":"hide","RightFrontLeg":"hide","LeftBackLeg":"hide","RightBackLeg":"hide","Tail":"hide"}
B = L["Builder"]("B06", PAL, MAIN, glow=("glowGold","glowBlue"), names=NAMES, offset=(155,0,0))
# legs
for part, y in (("LeftFrontLeg",-2.8),("LeftBackLeg",6.0)):
    B.mirror(part,"hide",(3.4,3.4,4.8),(3.4,y,2.6))
    B.mirror(part,"hideD",(3.8,3.8,1.0),(3.4,y-0.4,0.5))
    B.mirror(part,"armor",(3.7,3.7,1.4),(3.4,y,3.6))
    B.mirror(part,"gold",(3.8,3.8,0.4),(3.4,y,4.4))
# body
B.add("Body","hide",(10,16,9),(0,1,8.5))
B.add("Body","hideD",(3.0,14,1),(0,1,4.0))
B.add("Body","armor",(10.6,10,1.4),(0,0.4,13.4))
B.add("Body","gold",(10.8,0.6,0.6),(0,-4.6,13.4)); B.add("Body","gold",(10.8,0.6,0.6),(0,5.4,13.4))
B.add("Body","armor",(9,3,1.0),(0,-5.8,12.6))
B.sym("Body","armor",(1.8,5,5),(5.6,-4.2,10.0))
B.sym("Body","glowBlue",(0.4,1.0,1.0),(6.55,-4.2,10.6))
# blue tabard on the left side, round shield on the right side
B.add("Body","blue",(0.6,5.4,5.0),(5.3,1.0,8.8))
B.add("Body","armor",(0.7,1.0,4.2),(5.45,1.0,8.8)); B.add("Body","armor",(0.76,4.4,1.0),(5.45,1.0,9.6))
B.add("Body","shield",(0.8,5.0,5.0),(-5.4,1.0,8.9))
B.add("Body","shield",(0.7,3.6,6.0),(-5.4,1.0,8.9))
B.add("Body","blue",(0.9,0.9,4.0),(-5.55,1.0,8.9)); B.add("Body","blue",(0.96,3.2,0.9),(-5.55,1.0,9.5))
# tail
B.add("Tail","hide",(1.0,2.4,1.0),(0,9.8,10.6),(30,0,0))
B.add("Tail","hideD",(1.4,1.2,1.4),(0,10.8,9.6))
# head
B.add("Head","hide",(7,7,6.4),(0,-9.6,8.6))
B.add("Head","snout",(5,3.6,4),(0,-14.6,7.6))
B.sym("Head","dark",(0.6,0.3,0.6),(1.2,-16.45,7.8))
B.sym("Head","dark",(1.5,0.4,0.4),(2.6,-13.25,10.7),(0,-15,0))
B.sym("Head","hide",(1.2,0.8,1.8),(2.8,-7.0,12.6),(0,-15,0))
B.add("Head","horn",(2.2,2.2,4.2),(0,-15.0,10.6),(-12,0,0))
B.add("Head","glowGold",(1.5,1.5,1.8),(0,-14.6,13.4),(-12,0,0))
B.add("Head","horn",(1.4,1.4,2),(0,-12.0,12.4))
# paladin helmet plate with gold trim
B.add("Head","armor",(7.4,5,1.2),(0,-9.2,12.2))
B.add("Head","gold",(7.5,0.5,0.5),(0,-11.5,12.2))

for sx in ():  # restyle: no noisy hide plates
    B.shingle("Body", ["hideD","hide"], (0,7.4,10.8), (10,3.2,4.0), "x", sx, seed=64+sx, plate=(1.3,1.8))
    B.shingle("Head", ["hideD","hide"], (0,-9.6,8.6), (7,7,6.4), "x", sx, seed=66+sx, plate=(1.4,2.2))
# B.shingle("Body", ["hideD","hide"], (0,1,10.4), (10,16,5.0), "y", 1, seed=68)
# restyle (ADR 0017): blocky cartoon face (ADR 0015)
B.face_blocky(eye=(2.6,-13.1,9.8), eye_size=(1.1,1.1), mouth=(0,-16.4,6.3), mouth_w=2.2, iris="iris", lid="hideD")
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-5.8,10.0)),
     "LeftFrontLeg": ("Body", (3.4,-2.8,4.6)), "RightFrontLeg": ("Body", (-3.4,-2.8,4.6)),
     "LeftBackLeg": ("Body", (3.4,6.0,4.6)), "RightBackLeg": ("Body", (-3.4,6.0,4.6)),
     "Tail": ("Body", (0,9.0,11.0))}
B.build(J)
