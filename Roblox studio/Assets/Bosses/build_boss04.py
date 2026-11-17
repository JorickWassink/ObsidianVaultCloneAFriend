# Boss 4 "Champ N Son" + Pet 4: ripped kangaroo champion, huge blue gloves with neon cuffs, glowing gold title belt,
# red shorts, joey in the pouch (Joey joint, own small gloves and a fixed face). First Boss of the gold + neon step.
# Run inside Blender:  ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\build_boss04.py").read(), ns); ns["build"]()
exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\boss_lib.py").read(), globals())

COLORS.update({
    "Fur": "e48a38", "FurDark": "b25c1c", "FurLight": "ffe2b4", "Nose": "2a1810", "Claw": "fff4e0",
    "Glove": "2a78ff", "GloveDark": "1a52cc", "CuffNeon": "3ad8ffn", "Tape": "fffaf0",
    "Shorts": "ff2a2a", "ShortsWhite": "fffaf0", "Belt": "ffc414", "BeltDark": "d08a00", "BeltNeon": "ffe060n", "BeltStar": "ff3a3an",
    "Band": "ff2a2a", "JoeyGlove": "ff2a2a",
    "EyeGlow": "fff0a0n", "Pupil": "2a1810", "Mouth": "3a1010", "Teeth": "fffaf0", "Tongue": "ff4a6e",
    "PetEye": "2a1810", "PetShine": "ffffff", "Blush": "ff8a7a",
})

def glove(c, r, col="Glove", cuff="CuffNeon", sx=1):
    c = Vector(c)
    loft([(c + Vector((0, 0.45 * r, 0.75 * r)), 0.7 * r, 0.7 * r), (c + Vector((0, 0.1 * r, 0.35 * r)), r, r),
          (c + Vector((0, -0.15 * r, -0.35 * r)), 0.95 * r, 0.98 * r), (c + Vector((0, 0, -0.9 * r)), 0.5 * r, 0.5 * r)], col)
    loft([(c + Vector((0.75 * r * sx * -1, -0.35 * r, 0.1 * r)), 0.35 * r, 0.35 * r), (c + Vector((0.85 * r * sx * -1, -0.6 * r, -0.3 * r)), 0.3 * r, 0.3 * r)], col, sides=6)
    if cuff:
        loft([(c + Vector((0, 0.5 * r, 0.95 * r)), 0.78 * r, 0.78 * r), (c + Vector((0, 0.5 * r, 0.6 * r)), 0.82 * r, 0.82 * r)], cuff)

def brows(col, z=16.4, tilt=0.32, w=1.3):
    on("Head"); smooth(False)
    for sx in (1, -1): block((0.95 * sx, -2.45, z), (w, 0.4, 0.32), col, rot=(0, tilt * sx, 0), bevel=0.12)

def Boss():
    COLORS.setdefault("EyeWhite", "ffffff"); COLORS["EyeGlow"] = "ffc414n"
    toon_base("Fur", "FurDark", "FurLight", hand="Glove", foot="FurDark")
    on("Body"); smooth(True)
    loft([((0, 0.0, 2.8), 1.95, 1.75), ((0, 0.0, 3.7), 3.1, 2.7), ((0, -0.1, 5.4), 3.78, 3.18), ((0, -0.1, 6.1), 3.72, 3.12)], "Shorts", sides=14)
    smooth(False)
    loft([((0, -0.1, 6.1), 3.8, 3.2), ((0, -0.1, 6.9), 3.65, 3.08)], "Belt", sides=14, cap=False)
    block((0, -3.2, 6.5), (1.9, 0.4, 1.3), "Belt", bevel=0.14)
    for (x, z, w, h) in ((0, 7.18, 2.1, 0.12), (0, 5.82, 2.1, 0.12), (-1.0, 6.5, 0.12, 1.45), (1.0, 6.5, 0.12, 1.45)):
        block((x, -3.43, z), (w, 0.1, h), "BeltNeon", bevel=0)
    plate(star_pts(0.48, 0.2), 0.12, (0, -3.46, 6.5), "BeltStar")
    for sx, side in ((1, "Left"), (-1, "Right")):
        on(side + "Foot"); smooth(True)
        ell((1.5 * sx, -1.4, 0.38), (1.05, 2.3, 0.42), "FurDark")
        on(side + "Hand"); smooth(True)
        glove((3.45 * sx, -0.7, 6.0), 1.15, sx=sx)
        on(side + "LowerArm"); smooth(False)
        W = Vector(TOON["W"]); W.x *= sx
        loft([(W + Vector((0, 0.05, 0.45)), 0.72, 0.72), (W + Vector((0, 0, 0.0)), 0.7, 0.7)], "Tape", sides=10)
    bone("Tail", "Body", (0, 2.4, 4.4)); smooth(True)
    loft([((0, 2.5, 4.6), 1.05, 0.95), ((0, 4.0, 3.2), 0.85, 0.75), ((0, 5.3, 1.6), 0.6, 0.5), ((0, 6.3, 0.35), 0.28, 0.25)], "Fur", sides=12, ref=(1, 0, 0))
    on("Chest"); smooth(True)
    ell((0, -2.35, 8.55), (1.55, 0.85, 1.05), "FurLight")
    bone("Joey", "Chest", (0, -2.4, 9.2)); smooth(True)
    ell((0, -2.55, 9.75), (0.68, 0.6, 0.62), "Fur")
    ell((0, -3.1, 9.6), (0.3, 0.3, 0.24), "FurLight")
    for sx in (1, -1):
        loft([((0.32 * sx, -2.5, 10.25), 0.16, 0.1), ((0.5 * sx, -2.45, 10.95), 0.05, 0.04)], "Fur", sides=6)
        ell((0.27 * sx, -3.08, 9.92), (0.11, 0.05, 0.13), "Pupil")
        glove((0.8 * sx, -2.95, 9.25), 0.3, col="JoeyGlove", cuff=None, sx=sx)
    on("Head"); smooth(True)
    loft([((0, -2.05, 14.55), 1.15, 0.85), ((0, -3.4, 14.25), 0.75, 0.6), ((0, -3.85, 14.2), 0.4, 0.35)], "FurLight", sides=12, ref=(0, 0, 1))
    ell((0, -4.0, 14.38), (0.3, 0.2, 0.2), "Nose")
    loft([((0, -0.3, 16.25), 2.45, 2.17), ((0, -0.3, 16.8), 2.2, 1.95)], "Band", sides=14, cap=False)
    def ear(sx, side):
        bone(side + "Ear", "Head", (1.0 * sx, -0.3, 17.2)); smooth(True)
        loft([((1.05 * sx, -0.3, 17.0), 0.6, 0.35), ((1.45 * sx, -0.25, 18.9), 0.58, 0.32), ((1.75 * sx, -0.2, 20.3), 0.08, 0.06)], "Fur", sides=10)
        ell((1.42 * sx, -0.58, 18.8), (0.28, 0.07, 1.05), "FurLight")
    mirror(ear)
    brows("FurDark")

def Faces():
    toon_faces(my=-3.7, mz=13.85, s=0.72)

def Pet():
    b = PET_BONES
    bone("HumanoidRootPart", None, (0, 0, 2.6), b)
    bone("Body", "HumanoidRootPart", (0, 0, 2.6), b)
    loft([((0, 0.1, 0.9), 1.6, 1.4), ((0, 0.0, 2.2), 2.2, 1.9), ((0, 0.0, 3.7), 1.95, 1.65), ((0, 0.0, 4.3), 1.3, 1.1)], "Fur")
    loft([((0, -1.5, 1.4), 1.2, 0.4), ((0, -1.8, 2.6), 1.5, 0.45), ((0, -1.55, 3.7), 1.2, 0.35)], "FurLight")
    loft([((0, 0.05, 1.7), 2.25, 1.95), ((0, 0.05, 2.3), 2.25, 1.95)], "Belt", sides=10, cap=False)
    block((0, -1.95, 2.0), (1.1, 0.25, 0.8), "Belt", bevel=0.1)
    plate(star_pts(0.3, 0.13), 0.08, (0, -2.1, 2.0), "BeltStar")
    loft([((0, 1.6, 1.6), 0.9, 0.85), ((0, 2.9, 0.9), 0.65, 0.6), ((0, 3.8, 0.35), 0.3, 0.3)], "Fur", ref=(1, 0, 0))
    bone("Head", "Body", (0, -0.2, 4.3), b)
    loft([((0, -0.3, 4.4), 2.0, 1.9), ((0, -0.4, 5.6), 2.9, 2.6), ((0, -0.35, 7.4), 2.8, 2.5), ((0, -0.3, 8.2), 1.9, 1.6)], "Fur")
    loft([((0, -2.4, 5.9), 1.3, 0.9), ((0, -3.3, 5.75), 0.75, 0.55), ((0, -3.65, 5.7), 0.35, 0.3)], "FurLight", ref=(0, 0, 1))
    puff((0, -3.8, 5.82), 0.25, "Nose")
    loft([((0, -0.35, 7.3), 2.82, 2.52), ((0, -0.35, 7.8), 2.72, 2.42)], "Band", sides=10, cap=False)
    for sx in (1, -1):
        loft([((1.0 * sx, -0.3, 8.0), 0.65, 0.38), ((1.4 * sx, -0.3, 9.7), 0.6, 0.32), ((1.6 * sx, -0.3, 10.6), 0.1, 0.08)], "Fur", sides=5)
        block((1.85 * sx, -2.45, 5.8), (0.55, 0.1, 0.3), "Blush", bevel=0.06)
    for sx, side in ((1, "Left"), (-1, "Right")):
        bone(side + "UpperArm", "Body", (2.0 * sx, 0, 3.6), b)
        loft([((2.0 * sx, 0, 3.8), 0.75, 0.75), ((2.4 * sx, -0.4, 2.6), 0.7, 0.7)], "Fur", sides=7)
        glove((2.55 * sx, -0.75, 2.0), 0.85, sx=sx)
        bone(side + "Leg", "Body", (1.1 * sx, 0, 1.3), b)
        loft([((1.1 * sx, 0, 1.4), 0.9, 0.9), ((1.15 * sx, 0, 0.6), 0.8, 0.8)], "Fur", sides=7)
        block((1.15 * sx, -0.9, 0.33), (1.3, 2.9, 0.66), "FurDark", bevel=0.2)
    pet_faces(1.0, -2.62, 6.8, -3.45, 5.3)

def build():
    build_all(4, Boss, Faces, Pet, height=22.7)
