# Boss 1 "Brown Bear" + Pet 1, chunky chibi (2026-11-12). The earlier buff version is build_boss01_buff.py.
# Run inside Blender:  ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\build_boss01.py").read(), ns); ns["build"]()
exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\boss_lib.py").read(), globals())

COLORS.update({
    "Fur": "b8601a", "FurDark": "6e300c", "FurLight": "ffd690", "Nose": "2a1810", "Claw": "fff4e0",
    "CapeRed": "ff2418", "CapeWhite": "fffaf0", "Leather": "5a2408", "Gold": "ffc414",
    "Honey": "ff9800", "Jar": "ffb000",
    "EyeGlow": "ffd400n", "Pupil": "2a1208", "Mouth": "3a1010", "Teeth": "fff4e0", "Tongue": "ff4a6e",
    "PetEye": "2a1208", "PetShine": "ffffff", "Blush": "ff7a7a",
})

def brows(col, z=16.4, tilt=0.32, w=1.3):
    on("Head"); smooth(False)
    for sx in (1, -1): block((0.95 * sx, -2.45, z), (w, 0.4, 0.32), col, rot=(0, tilt * sx, 0), bevel=0.12)

def Boss():
    COLORS.setdefault("EyeWhite", "ffffff"); COLORS["EyeGlow"] = "ffb400n"
    toon_base("Fur", "FurDark", "FurLight")
    on("Head"); smooth(True)
    ell(TOON["muzzle"], (1.25, 0.75, 0.85), "FurLight")
    ell((0, -3.25, 14.55), (0.42, 0.25, 0.27), "Nose")
    def ear(sx, side):
        bone(side + "Ear", "Head", (1.9 * sx, -0.3, 17.0)); smooth(True)
        ell((2.0 * sx, -0.3, 17.45), (0.78, 0.42, 0.78), "FurDark")
        ell((2.0 * sx, -0.66, 17.45), (0.42, 0.14, 0.42), "FurLight")
    mirror(ear)
    brows("FurDark")
    on("Body"); smooth(False)
    loft([((0, -0.05, 6.6), 3.62, 3.07), ((0, -0.05, 7.15), 3.55, 3.0)], "Leather", sides=14, cap=False)
    block((0, -3.12, 6.88), (0.9, 0.3, 0.62), "Gold", bevel=0.1)
    on("Chest"); smooth(False)
    loft([((0, 0.0, 11.75), 2.05, 1.75), ((0, 0.0, 12.3), 1.7, 1.45)], "CapeRed", sides=12, cap=False)
    tri = []
    for j in range(4):
        z = 11.9 - j * 0.45; w = 2.6 * (1 - j / 3.6)
        tri.append([Vector((-w / 2 + w * i / 4, -1.95 - j * 0.15, z)) for i in range(5)])
    sheet(tri, ("CapeRed", "CapeWhite"), thick=0.16)
    on("LeftHand"); smooth(True)
    loft([((3.45, -1.55, 5.7), 0.55, 0.55), ((3.45, -1.55, 6.3), 0.62, 0.62), ((3.45, -1.55, 6.8), 0.52, 0.52)], "Jar", sides=12)
    smooth(False)
    loft([((3.45, -1.55, 6.75), 0.62, 0.62), ((3.45, -1.55, 7.0), 0.58, 0.58)], "CapeRed", sides=12)
    loft([((3.2, -2.05, 6.7), 0.12, 0.12), ((3.15, -2.1, 5.9), 0.09, 0.09)], "Honey", sides=6)
    gem((3.15, -2.1, 5.75), 0.17, "Honey")

def Faces():
    toon_faces()

def Pet():
    b = PET_BONES
    bone("HumanoidRootPart", None, (0, 0, 2.6), b)
    bone("Body", "HumanoidRootPart", (0, 0, 2.6), b)
    loft([((0, 0.1, 0.9), 1.6, 1.4), ((0, 0.0, 2.2), 2.3, 1.95), ((0, 0.0, 3.7), 2.0, 1.7), ((0, 0.0, 4.3), 1.3, 1.1)], "Fur")
    loft([((0, -1.55, 1.4), 1.2, 0.4), ((0, -1.85, 2.6), 1.5, 0.45), ((0, -1.6, 3.7), 1.2, 0.35)], "FurLight")
    loft([((-2.15, -0.7, 2.3), 0.5, 0.5), ((-2.15, -0.7, 3.2), 0.5, 0.5)], "Jar", sides=8)
    loft([((-2.15, -0.7, 3.15), 0.6, 0.6), ((-2.15, -0.7, 3.45), 0.55, 0.55)], "CapeRed", sides=8)
    bone("Head", "Body", (0, -0.2, 4.3), b)
    loft([((0, -0.3, 4.4), 2.2, 2.0), ((0, -0.4, 5.6), 3.2, 2.7), ((0, -0.35, 7.6), 3.1, 2.6), ((0, -0.3, 8.6), 2.0, 1.7)], "Fur")
    block((0, -2.95, 5.8), (2.0, 1.2, 1.3), "FurLight", bevel=0.3)
    loft([((0, -3.5, 6.25), 0.5, 0.22), ((0, -3.7, 6.42), 0.36, 0.15)], "Nose", sides=6, ref=(0, 0, 1))
    loft([((0, -0.6, 4.35), 2.5, 2.3), ((0, -0.6, 4.95), 2.35, 2.15)], "CapeRed", sides=10, cap=False)
    tri = []
    for j in range(3):
        z = 4.75 - j * 0.6; w = 2.2 * (1 - j / 2.6)
        tri.append([Vector((-w / 2 + w * i / 3, -2.25 - j * 0.12, z)) for i in range(4)])
    sheet(tri, ("CapeRed", "CapeWhite"), thick=0.18)
    for sx in (1, -1):
        loft([((2.3 * sx, -0.4, 8.3), 1.0, 0.5), ((2.45 * sx, -0.4, 9.1), 0.85, 0.42), ((2.5 * sx, -0.4, 9.45), 0.4, 0.25)], "FurDark", sides=6)
        block((2.42 * sx, -0.85, 8.95), (0.85, 0.12, 0.65), "FurLight", bevel=0.1)
        block((1.65 * sx, -2.95, 6.05), (0.6, 0.1, 0.3), "Blush", bevel=0.06)
    for sx, side in ((1, "Left"), (-1, "Right")):
        bone(side + "UpperArm", "Body", (2.0 * sx, 0, 3.6), b)
        loft([((2.0 * sx, 0, 3.8), 0.85, 0.85), ((2.5 * sx, -0.4, 2.4), 0.8, 0.8), ((2.65 * sx, -0.6, 1.5), 0.85, 0.85)], "Fur", sides=7)
        block((2.7 * sx, -0.7, 1.3), (1.4, 1.4, 1.1), "FurDark", bevel=0.3)
        bone(side + "Leg", "Body", (1.1 * sx, 0, 1.3), b)
        loft([((1.1 * sx, 0, 1.4), 0.95, 0.95), ((1.15 * sx, 0, 0.6), 0.85, 0.85)], "Fur", sides=7)
        block((1.15 * sx, -0.5, 0.33), (1.6, 2.1, 0.66), "FurDark", bevel=0.2)
    ex, ey, ez = 1.1, -3.0, 7.0
    CTX["bone"] = "Head"; CTX["face"] = "Eyes_Happy"
    for sx in (1, -1):
        plate([(-0.38, -0.45), (0.38, -0.45), (0.42, 0.38), (-0.42, 0.38)], 0.14, (ex * sx, ey, ez), "PetEye")
        plate([(-0.12, -0.12), (0.12, -0.12), (0.12, 0.12), (-0.12, 0.12)], 0.06, (ex * sx + 0.14, ey - 0.1, ez + 0.16), "PetShine")
    CTX["face"] = "Eyes_Blink"
    for sx in (1, -1):
        plate([(-0.42, -0.04), (0, 0.16), (0.42, -0.04), (0.42, -0.18), (0, 0.02), (-0.42, -0.18)], 0.14, (ex * sx, ey, ez - 0.1), "PetEye")
    CTX["face"] = "Mouth_Happy"
    plate([(-0.42, 0.06), (0, -0.2), (0.42, 0.06), (0.42, -0.08), (0, -0.36), (-0.42, -0.08)], 0.12, (0, -3.58, 5.55), "Mouth")
    CTX["face"] = None


def build():
    build_all(1, Boss, Faces, Pet, height=19.4)
