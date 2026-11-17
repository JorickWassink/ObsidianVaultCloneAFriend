# Boss 3 "Robcoon" + Pet 3: sneaky hunched raccoon thief, bushy striped tail (Tail joint), overflowing loot sack
# (Sack joint). Glow: eyes + a few gold coins glint.
# Run inside Blender:  ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\build_boss03.py").read(), ns); ns["build"]()
exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\boss_lib.py").read(), globals())

COLORS.update({
    "Fur": "8a94aa", "FurDark": "596276", "FurLight": "f0f2f5", "Mask": "1e1c26", "Hand": "2a2834", "Claw": "f4f0e6",
    "Bandana": "f02e28", "Sack": "e2b468", "SackDark": "b0843e", "Rope": "8a5626", "Gold": "ffc414", "CoinGlow": "ffd83an",
    "EyeGlow": "c8ff3cn", "Pupil": "10200a", "Mouth": "301018", "Teeth": "fffaf0", "Tongue": "ff4a6e",
    "PetEye": "1e1c26", "PetEyeLime": "b8f040", "PetShine": "ffffff", "Blush": "ff8a9a",
})

def brows(col, z=16.4, tilt=0.32, w=1.3):
    on("Head"); smooth(False)
    for sx in (1, -1): block((0.95 * sx, -2.45, z), (w, 0.4, 0.32), col, rot=(0, tilt * sx, 0), bevel=0.12)

def coin(c, r, col):
    loft([(Vector(c) - Vector((0, 0.07, 0)), r, r), (Vector(c) + Vector((0, 0.07, 0)), r, r)], col, sides=12, ref=(0, 0, 1))

def Boss():
    COLORS.setdefault("EyeWhite", "ffffff")
    toon_base("Fur", "FurDark", "FurLight", hand="Hand", foot="Hand", arm="FurDark", leg="FurDark")
    on("Head"); smooth(True)
    ell((0, -0.65, 15.55), (2.78, 2.15, 0.72), "Mask")
    loft([((0, -2.2, 14.3), 1.1, 0.8), ((0, -3.5, 14.05), 0.55, 0.42), ((0, -3.95, 14.0), 0.18, 0.16)], "FurLight", sides=12, ref=(0, 0, 1))
    ell((0, -4.0, 14.05), (0.3, 0.22, 0.22), "Mask")
    def ear(sx, side):
        bone(side + "Ear", "Head", (1.7 * sx, -0.3, 17.2)); smooth(True)
        loft([((1.75 * sx, -0.3, 17.0), 0.75, 0.38), ((2.05 * sx, -0.3, 18.2), 0.38, 0.22), ((2.2 * sx, -0.3, 18.9), 0.05, 0.05)], "Fur", sides=10)
        ell((2.05 * sx, -0.55, 18.3), (0.22, 0.06, 0.45), "Mask")
    mirror(ear)
    brows("FurLight", z=16.55)
    on("Body"); smooth(False)
    loft([((0, -0.05, 6.4), 3.66, 3.1), ((0, -0.05, 6.85), 3.6, 3.05)], "Rope", sides=14, cap=False)
    loft([((2.3, -2.3, 5.4), 0.55, 0.42), ((2.3, -2.4, 6.3), 0.48, 0.36)], "SackDark", sides=8)
    coin((2.3, -2.82, 6.35), 0.22, "Gold")
    on("Chest"); smooth(False)
    loft([((0, 0.0, 11.75), 2.05, 1.75), ((0, 0.0, 12.3), 1.7, 1.45)], "Bandana", sides=12, cap=False)
    plate([(-1.1, 0), (1.1, 0), (0, -1.2)], 0.2, (0, -1.95, 11.9), "Bandana", rot=(-0.25, 0, 0))
    for sx, side in ((1, "Left"), (-1, "Right")):
        on(side + "Hand")
        for k in range(3):
            x = 3.45 * sx + (k - 1) * 0.42
            wedge((x, -1.15, 5.2), (x, -1.6, 4.5), 0.13, "Claw")
        on(side + "Foot")
        for k in (-1, 0, 1): wedge((1.5 * sx + k * 0.45, -2.0, 0.4), (1.5 * sx + k * 0.5, -2.5, 0.15), 0.13, "Claw")
    bone("Sack", "Chest", (0, 2.2, 10.0)); smooth(True)
    ell((0, 4.0, 9.2), (2.3, 1.8, 2.6), "Sack")
    loft([((0, 3.7, 11.6), 0.9, 0.75), ((0, 3.7, 12.2), 0.75, 0.62)], "Rope", sides=10)
    smooth(False)
    for k, (x, y, z, r) in enumerate(((0.25, 3.5, 12.6, 0.38), (-0.45, 3.9, 12.4, 0.34), (0.6, 4.0, 12.3, 0.3), (-0.05, 3.3, 13.0, 0.32))):
        coin((x, y, z), r, "CoinGlow" if k in (0, 3) else "Gold")
    bone("Tail", "Body", (0, 2.4, 3.8)); smooth(True)
    pts = [Vector((0, 2.5, 3.7)), Vector((0.2, 4.0, 3.5)), Vector((0.6, 5.4, 4.6)), Vector((0.8, 6.0, 6.5)), Vector((0.6, 5.7, 8.3)), Vector((0.2, 4.8, 9.4))]
    widths = [1.0, 1.35, 1.5, 1.35, 1.0]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; w = widths[i]
        loft([(a, w * 0.7, w * 0.7), (a.lerp(b, 0.5), w, w), (b, w * 0.7, w * 0.7)], "Fur" if i % 2 == 0 else "FurDark", sides=12, ref=(1, 0, 0))
    ell(pts[-1] + Vector((-0.1, -0.4, 0.4)), (0.75, 0.75, 0.75), "FurDark")

def Faces():
    toon_faces(my=-3.42, mz=13.55, s=0.85)

def Pet():
    b = PET_BONES
    bone("HumanoidRootPart", None, (0, 0, 2.6), b)
    bone("Body", "HumanoidRootPart", (0, 0, 2.6), b)
    loft([((0, 0.1, 0.9), 1.6, 1.4), ((0, 0.0, 2.2), 2.2, 1.9), ((0, 0.0, 3.7), 1.95, 1.65), ((0, 0.0, 4.3), 1.3, 1.1)], "Fur")
    loft([((0, -1.5, 1.4), 1.2, 0.4), ((0, -1.8, 2.6), 1.5, 0.45), ((0, -1.55, 3.7), 1.2, 0.35)], "FurLight")
    loft([((0, -0.3, 4.1), 2.2, 2.0), ((0, -0.3, 4.6), 2.1, 1.9)], "Bandana", sides=10, cap=False)
    loft([((0, 1.6, 1.4), 0.9, 0.9), ((0.4, 2.8, 2.4), 1.15, 1.15), ((0.6, 3.1, 3.9), 1.05, 1.05), ((0.4, 2.8, 4.9), 0.4, 0.4)], "FurDark", sides=8, ref=(1, 0, 0))
    loft([((0.42, 2.85, 2.3), 1.2, 1.2), ((0.5, 3.0, 2.9), 1.2, 1.2)], "Fur", sides=8)
    loft([((0, 1.4, 2.6), 1.0, 0.8), ((0, 1.8, 3.6), 1.2, 0.95), ((0, 1.6, 4.4), 0.6, 0.5)], "Sack", sides=8)
    coin((0.1, 1.5, 4.7), 0.3, "Gold")
    bone("Head", "Body", (0, -0.2, 4.3), b)
    loft([((0, -0.3, 4.4), 2.2, 2.0), ((0, -0.4, 5.6), 3.1, 2.65), ((0, -0.35, 7.4), 3.0, 2.55), ((0, -0.3, 8.3), 2.0, 1.7)], "Fur")
    loft([((0, -2.4, 5.8), 1.4, 0.9), ((0, -3.3, 5.7), 0.75, 0.55), ((0, -3.7, 5.65), 0.35, 0.3)], "FurLight", ref=(0, 0, 1))
    puff((0, -3.85, 5.75), 0.28, "Mask")
    block((0, -2.6, 6.95), (4.4, 0.4, 1.3), "Mask", bevel=0.25)
    for sx in (1, -1):
        loft([((1.9 * sx, -0.3, 8.0), 0.85, 0.42), ((2.15 * sx, -0.3, 9.2), 0.45, 0.25), ((2.25 * sx, -0.3, 9.7), 0.06, 0.06)], "Fur", sides=4)
        block((2.0 * sx, -2.6, 5.75), (0.6, 0.1, 0.3), "Blush", bevel=0.06)
    for sx, side in ((1, "Left"), (-1, "Right")):
        bone(side + "UpperArm", "Body", (2.0 * sx, 0, 3.6), b)
        loft([((2.0 * sx, 0, 3.8), 0.75, 0.75), ((2.45 * sx, -0.4, 2.4), 0.7, 0.7), ((2.6 * sx, -0.6, 1.5), 0.72, 0.72)], "FurDark", sides=7)
        block((2.65 * sx, -0.7, 1.3), (1.2, 1.2, 1.0), "Hand", bevel=0.3)
        bone(side + "Leg", "Body", (1.1 * sx, 0, 1.3), b)
        loft([((1.1 * sx, 0, 1.4), 0.9, 0.9), ((1.15 * sx, 0, 0.6), 0.8, 0.8)], "FurDark", sides=7)
        block((1.15 * sx, -0.5, 0.33), (1.5, 2.1, 0.66), "Hand", bevel=0.2)
    pet_faces(1.1, -2.85, 6.95, -3.5, 5.15, eye="PetEyeLime")

def build():
    build_all(3, Boss, Faces, Pet, height=18.8)
