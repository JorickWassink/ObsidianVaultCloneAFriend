# Restyle copy (ADR 0017): SmoothLib, Happy/Blink eye sets.

import bpy
L = bpy.app.driver_namespace["studlib"]
PAL = {"mechY":(226,172,30),"mechYD":(186,136,20),"metal":(138,150,163),"chrome":(205,213,222),"shark":(98,134,172),"sharkD":(76,108,142),"belly":(233,238,242),
       "dark":(32,32,38),"mouth":(96,30,44),"white":(255,255,255),"lamp":(255,236,130),"red":(255,64,48)}
NAMES = {"mechY":"Mech","mechYD":"MechDark","metal":"Metal","chrome":"Chrome","shark":"Shark","sharkD":"SharkDark","belly":"Belly","dark":"Dark","mouth":"Mouth","white":"Teeth","lamp":"Headlight","red":"RedLight"}
B = L["Builder"]("P08", PAL, {"Body":"mechY","Head":"shark"}, glow=("lamp","red"), names=NAMES, offset=(228,40,0))
B.add("Body","mechY",(5.4,4.4,3.4),(0,0,2.6))
B.add("Body","dark",(4.4,0.4,1.4),(0,-2.25,2.8))
B.sym("Body","lamp",(1.0,0.4,0.9),(1.3,-2.4,2.8))
B.add("Body","red",(0.8,0.4,0.9),(0,-2.4,2.8))
B.sym("Body","metal",(1.2,1.2,1.0),(1.6,0,0.5))
B.sym("Body","chrome",(1.4,1.4,1.0),(3.4,-0.4,2.0))
B.sym("Body","chrome",(0.8,0.8,1.0),(3.4,-0.4,1.0))
B.add("Body","chrome",(5,4,0.6),(0,0,4.5))
B.add("Head","shark",(6.6,6,5.4),(0,-0.4,7.4))
B.add("Head","belly",(5,0.6,2.2),(0,-3.6,5.8))
B.add("Head","mouth",(4.2,0.4,0.9),(0,-3.6,7.2))
for i in range(5):
    B.add("Head","white",(0.5,0.45,0.5),(-1.6+i*0.8,-3.75,7.5))
B.face = "Eyes_Happy"; B.sym("Head","dark",(1.1,0.3,1.3),(1.8,-3.5,8.9)); B.face = None
B.face = "Eyes_Happy"; B.sym("Head","white",(0.4,0.32,0.4),(1.55,-3.55,9.25)); B.face = None
B.sym("Head","dark",(1.5,0.3,0.4),(1.8,-3.5,10.0),(0,-14,0))
B.add("Head","shark",(1.0,2.6,2.4),(0,0.6,11.0),(22,0,0))
# restyle: Happy eyes above are a swappable set; Blink set (ADR 0015)
B.blink_set((1.8,-3.4,8.9), 1.1)
J = {"HumanoidRootPart": (None, "Body"), "Body": ("HumanoidRootPart", "Body"), "Head": ("Body", (0,-0.2,4.8))}
B.build(J)
