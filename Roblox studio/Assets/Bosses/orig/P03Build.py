# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"fur":(141,147,156),"furD":(108,114,123),"light":(236,234,230),"dark":(30,26,26),"belly":(185,190,198),"red":(210,58,50),"sack":(201,167,106),"gold":(242,201,76)}
NAMES = {"fur":"Fur","furD":"FurDark","light":"Light","dark":"Mask","belly":"Belly","red":"Bandana","sack":"Sack","gold":"Coins"}
B = L["Builder"]("P03", PAL, {"Body":"fur","Head":"fur"}, names=NAMES, offset=(60,40,0))
B.add("Body","fur",(4.6,4,4),(0,0,3.0))
B.add("Body","belly",(2.8,0.6,2.6),(0,-2.1,3.0))
B.sym("Body","dark",(1.6,2,1.0),(1.3,-0.4,0.5))
B.sym("Body","fur",(1.3,1.5,2),(2.9,-0.2,3.1),(0,10,0))
B.add("Body","fur",(1.8,1.8,1.6),(1.2,2.6,2.0)); B.add("Body","dark",(1.8,1.8,1.4),(1.6,3.6,3.2)); B.add("Body","fur",(1.6,1.6,1.4),(1.8,4.1,4.6))
B.add("Body","sack",(2.6,2.4,2.6),(-2.0,2.7,4.2))
B.add("Body","gold",(0.9,0.9,0.3),(-2.0,2.4,6.1),(0,25,0))
B.add("Body","red",(5,4.4,0.8),(0,-0.1,4.9))
B.add("Body","red",(1.2,0.6,1.2),(0,-2.35,4.6),(0,45,0))
B.add("Head","fur",(7.4,6,6),(0,-0.4,8.2))
B.add("Head","dark",(7.6,6.2,1.8),(0,-0.4,8.8))
B.face = "Eyes_Happy"; B.sym("Head","light",(1.3,0.32,1.3),(1.7,-4.0,8.8)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","dark",(0.5,0.34,0.5),(1.5,-4.05,8.7)); B.face = None
B.sym("Head","light",(1.8,0.3,0.4),(1.7,-3.5,10.0),(0,-12,0))
B.add("Head","light",(2.8,1.2,1.6),(0,-3.8,6.9))
B.add("Head","dark",(1,0.4,0.6),(0,-4.45,7.5))
B.sym("Head","fur",(1.8,1.2,1.8),(2.6,-0.2,11.6))
B.sym("Head","light",(0.9,0.3,0.9),(2.6,-0.85,11.6))

B.shingle("Head", ["furD","fur"], (0,-0.4,8.2), (7.4,6,6), "z", 1, seed=95, plate=(1.2,2.0))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((1.7,-3.5,8.8), 1.3, col="light")
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,5.2))}
B.build(J)
