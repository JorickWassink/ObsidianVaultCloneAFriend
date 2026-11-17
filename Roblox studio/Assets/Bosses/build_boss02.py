# Boss 2 "Rabbeat" + Pet 2: bulky brute bandit rabbit, carrot club in hand, leaf headband. Glow: eyes only.
# Run inside Blender:  ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\build_boss02.py").read(), ns); ns["build"]()
exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\boss_lib.py").read(), globals())

COLORS.update({
    "Fur": "8e9ab2", "FurDark": "667189", "FurLight": "f2f4f8", "Pink": "ff8fb4", "Nose": "ff5a8a",
    "Leaf": "38c848", "LeafDark": "23963a", "Carrot": "ff7814", "CarrotDark": "d4560a", "Strap": "6e3a16", "Gold": "ffc414",
    "EyeGlow": "ff3a5an", "Pupil": "2a0a10", "Mouth": "3a1018", "Teeth": "fffaf0", "Tongue": "ff4a6e",
    "PetEye": "2a0a10", "PetShine": "ffffff", "Blush": "ff7a9a",
})

def brows(col, z=16.4, tilt=0.32, w=1.3):
    on("Head"); smooth(False)
    for sx in (1, -1): block((0.95 * sx, -2.45, z), (w, 0.4, 0.32), col, rot=(0, tilt * sx, 0), bevel=0.12)

def Boss():
    COLORS.setdefault("EyeWhite", "ffffff")
    toon_base("Fur", "FurDark", "FurLight", hand="FurLight", foot="FurLight")
    on("Body"); smooth(True)
    ell((0, 2.95, 4.6), (0.9, 0.8, 0.9), "FurLight")
    on("Head")
    ell(TOON["muzzle"], (1.2, 0.72, 0.82), "FurLight")
    ell((0, -3.22, 14.55), (0.34, 0.2, 0.22), "Nose")
    loft([((0, -0.3, 16.35), 2.4, 2.12), ((0, -0.3, 16.85), 2.15, 1.9)], "Leaf", sides=14, cap=False)
    smooth(False)
    for k, (dx, dz) in enumerate(((0.4, 0.15), (-0.3, -0.15), (0.1, -0.45))):
        plate([(0, 0), (0.4, 0.25), (1.3, 0.15), (0.4, -0.22)], 0.1, (dx, 1.9, 16.5 + dz), "LeafDark" if k % 2 else "Leaf", rot=(0, 0.3 * k, math.pi / 2 + 0.3))
    for sx in (1, -1):
        for k in range(3): block((1.55 * sx, -3.0, 14.3 - k * 0.2), (1.2, 0.04, 0.05), "FurLight", rot=(0, (0.15 - k * 0.15) * sx, 0), bevel=0)
    def ear(sx, side):
        bone(side + "Ear", "Head", (0.85 * sx, -0.3, 17.2)); smooth(True)
        if sx > 0:
            loft([((0.85, -0.3, 17.0), 0.62, 0.38), ((1.0, -0.3, 19.2), 0.7, 0.4), ((1.2, -0.3, 21.2), 0.52, 0.32), ((1.25, -0.3, 22.0), 0.15, 0.12)], "Fur", sides=10)
            ell((1.02, -0.62, 19.4), (0.36, 0.08, 1.7), "Pink")
        else:
            loft([((-0.85, -0.3, 17.0), 0.62, 0.38), ((-1.0, -0.3, 19.0), 0.7, 0.4), ((-1.25, -0.45, 20.3), 0.6, 0.36)], "Fur", sides=10)
            loft([((-1.25, -0.45, 20.3), 0.6, 0.36), ((-2.1, -0.65, 20.5), 0.48, 0.3), ((-2.7, -0.8, 19.9), 0.15, 0.12)], "Fur", sides=10)
            ell((-1.02, -0.62, 19.0), (0.34, 0.08, 1.3), "Pink")
    mirror(ear)
    brows("FurDark")
    on("Chest"); smooth(False)
    pts = []
    for i in range(7):
        t = i / 6; x = 2.4 - 5.0 * t
        pts.append((x, -3.25 + 0.075 * x * x, 10.2 - 5.4 * t))
    for a, b in zip(pts[:-1], pts[1:]): loft([(a, 0.38, 0.16), (b, 0.38, 0.16)], "Strap", sides=4, ref=(0, 0, 1))
    block((-0.1, -3.35, 7.5), (0.75, 0.25, 0.6), "Gold", bevel=0.08)
    on("RightHand"); smooth(True)
    base, tip = Vector((-3.45, -1.4, 6.6)), Vector((-3.6, -2.0, 0.7))
    d = tip - base
    loft([(base, 0.75, 0.75), (base + d * 0.15, 0.95, 0.95), (base + d * 0.6, 0.6, 0.6), (tip, 0.06, 0.06)], "Carrot", sides=12, ref=(0, 0, 1))
    smooth(False)
    for t in (0.3, 0.5, 0.7):
        p = base + d * t; r = 0.98 - t * 0.7
        loft([(p - d.normalized() * 0.06, r, r), (p + d.normalized() * 0.06, r, r)], "CarrotDark", sides=12, ref=(0, 0, 1))
    for k in range(3):
        a = k * 2.1 + 0.4
        wedge((-3.45 + 0.15 * math.cos(a), -1.4 + 0.15 * math.sin(a), 6.8), (-3.4 + 0.7 * math.cos(a), -1.3 + 0.5 * math.sin(a), 8.3), 0.25, "Leaf" if k % 2 else "LeafDark")

def Faces():
    toon_faces(buck=True)

def Pet():
    b = PET_BONES
    bone("HumanoidRootPart", None, (0, 0, 2.6), b)
    bone("Body", "HumanoidRootPart", (0, 0, 2.6), b)
    loft([((0, 0.1, 0.9), 1.6, 1.4), ((0, 0.0, 2.2), 2.2, 1.9), ((0, 0.0, 3.7), 1.95, 1.65), ((0, 0.0, 4.3), 1.3, 1.1)], "Fur")
    loft([((0, -1.5, 1.4), 1.2, 0.4), ((0, -1.8, 2.6), 1.5, 0.45), ((0, -1.55, 3.7), 1.2, 0.35)], "FurLight")
    puff((0, 1.9, 1.8), 0.85, "FurLight")
    bone("Head", "Body", (0, -0.2, 4.3), b)
    loft([((0, -0.3, 4.4), 2.2, 2.0), ((0, -0.4, 5.6), 3.1, 2.65), ((0, -0.35, 7.5), 3.0, 2.55), ((0, -0.3, 8.4), 2.0, 1.7)], "Fur")
    block((0, -2.9, 5.8), (2.0, 1.2, 1.3), "FurLight", bevel=0.3)
    loft([((0, -3.45, 6.3), 0.42, 0.18), ((0, -3.62, 6.45), 0.3, 0.13)], "Nose", sides=6, ref=(0, 0, 1))
    loft([((0, -0.4, 7.6), 2.95, 2.55), ((0, -0.4, 8.1), 2.85, 2.45)], "Leaf", sides=10, cap=False)
    for sx in (1, -1):
        loft([((1.0 * sx, -0.4, 8.2), 0.75, 0.42), ((1.25 * sx, -0.4, 10.0), 0.8, 0.42), ((1.4 * sx, -0.4, 11.4), 0.3, 0.2)], "Fur", sides=6)
        block((1.22 * sx, -0.8, 9.7), (0.65, 0.12, 2.2), "Pink", bevel=0.08)
        block((1.95 * sx, -2.62, 5.9), (0.6, 0.1, 0.3), "Blush", bevel=0.06)
    for sx, side in ((1, "Left"), (-1, "Right")):
        bone(side + "UpperArm", "Body", (2.0 * sx, 0, 3.6), b)
        loft([((2.0 * sx, 0, 3.8), 0.8, 0.8), ((2.45 * sx, -0.4, 2.4), 0.75, 0.75), ((2.6 * sx, -0.6, 1.5), 0.8, 0.8)], "Fur", sides=7)
        block((2.65 * sx, -0.7, 1.3), (1.3, 1.3, 1.0), "FurLight", bevel=0.3)
        bone(side + "Leg", "Body", (1.1 * sx, 0, 1.3), b)
        loft([((1.1 * sx, 0, 1.4), 0.95, 0.95), ((1.15 * sx, 0, 0.6), 0.85, 0.85)], "Fur", sides=7)
        block((1.15 * sx, -0.8, 0.33), (1.5, 2.6, 0.66), "FurLight", bevel=0.2)
    CTX["bone"] = "RightUpperArm"   # a small carrot to hold
    loft([((-2.7, -1.5, 1.6), 0.45, 0.45), ((-2.75, -2.6, 0.8), 0.05, 0.05)], "Carrot", sides=8, ref=(0, 0, 1))
    wedge((-2.7, -1.2, 1.8), (-2.6, -0.8, 2.6), 0.25, "Leaf")
    pet_faces(1.1, -2.98, 6.95, -3.56, 5.55, buck_col="Teeth")

def build():
    build_all(2, Boss, Faces, Pet, height=24.3)
