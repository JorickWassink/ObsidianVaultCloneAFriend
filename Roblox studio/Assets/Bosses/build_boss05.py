# Boss 5 "Le Ape" + Pet 5: plain gorilla chef, faceted: chef hat, mustache, blue striped apron, red scarf,
# rolling pin. Glow: eyes only.
# Run inside Blender:  ns={}; exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\build_boss05.py").read(), ns); ns["build"]()
exec(open(r"C:\obsidian\Roblox studio\Assets\Bosses\boss_lib.py").read(), globals())

COLORS.update({
    "Fur": "4e4e62", "FurDark": "35353f", "Skin": "c0a08a", "SkinDark": "937664", "Nose": "24202a",
    "Apron": "3478ff", "ApronStripe": "eef4ff", "Scarf": "ff2a2a", "Hat": "fafbfd", "HatShade": "d8dfe8",
    "Mustache": "3a2210", "Pin": "eab874", "PinHandle": "b07838",
    "EyeGlow": "ffb43an", "Pupil": "2a1408", "Mouth": "3a1010", "Teeth": "fffaf0", "Tongue": "ff4a6e",
    "PetEye": "2a1408", "PetShine": "ffffff", "Blush": "ff8a8a",
})

def striped(z_top, z_bot, half, y0, wrap, flare, cols=8, rows=4):
    """apron panel as vertical stripes (Apron / ApronStripe), wrapped round the body"""
    for i in range(cols):
        grid = []
        for j in range(rows + 1):
            z = z_top - (z_top - z_bot) * j / rows; f = 1 + flare * (z_top - z)
            row = []
            for x0 in (-half + 2 * half * i / cols, -half + 2 * half * (i + 1) / cols):
                x = x0 * f
                row.append(Vector((x, y0 + wrap * x * x, z)))
            grid.append(row)
        sheet(grid, ("ApronStripe",) if i % 2 else ("Apron",), thick=0.22)

def brows(col, z=16.4, tilt=0.32, w=1.3):
    on("Head"); smooth(False)
    for sx in (1, -1): block((0.95 * sx, -2.45, z), (w, 0.4, 0.32), col, rot=(0, tilt * sx, 0), bevel=0.12)

def Boss():
    COLORS.setdefault("EyeWhite", "ffffff"); COLORS["EyeGlow"] = "ff9a10n"; COLORS.setdefault("FaceGrey", "8a7e82")
    toon_base("Fur", "FurDark", "FaceGrey", hand="FurDark", foot="FurDark", belly=False, wide=1.08)
    on("Head"); smooth(True)
    ell((0, -2.2, 15.35), (1.95, 0.55, 1.25), "FaceGrey")
    ell((0, -2.45, 16.3), (1.95, 0.45, 0.38), "FurDark")
    ell((0, -2.75, 13.95), (1.6, 0.95, 1.05), "FaceGrey")
    for sx in (1, -1):
        ell((0.42 * sx, -3.6, 14.45), (0.2, 0.1, 0.14), "Nose")
        ell((2.7 * sx, -0.3, 15.1), (0.25, 0.35, 0.45), "FurDark")
    smooth(False)
    for sx in (1, -1):
        plate([(x * sx, z) for x, z in [(0, 0.08), (0.45, 0.2), (0.95, 0.08), (1.15, -0.2), (0.95, -0.42), (0.8, -0.16), (0.45, -0.05), (0, -0.12)]],
              0.2, (0.05 * sx, -3.62, 14.05), "Mustache")
    loft([((0, -0.3, 16.95), 2.15, 1.95), ((0, -0.3, 17.55), 2.15, 1.95)], "HatShade", sides=14)
    smooth(True)
    loft([((0, -0.3, 17.5), 2.05, 1.85), ((0, -0.25, 18.7), 2.65, 2.4), ((0, -0.2, 19.9), 2.75, 2.5), ((0, -0.2, 20.6), 2.15, 1.95), ((0, -0.2, 21.0), 1.1, 1.0)], "Hat", sides=14)
    on("Body"); smooth(False)
    striped(7.6, 2.9, 2.5, -3.2, 0.075, 0.05, cols=8, rows=4)
    loft([((0, -0.05, 7.4), 3.75, 3.2), ((0, -0.05, 7.8), 3.65, 3.1)], "ApronStripe", sides=14, cap=False)
    on("Chest"); smooth(False)
    striped(10.6, 7.9, 1.7, -2.75, 0.1, 0.0, cols=6, rows=3)
    loft([((0, 0.0, 11.75), 2.05, 1.75), ((0, 0.0, 12.3), 1.7, 1.45)], "Scarf", sides=12, cap=False)
    loft([((0.7, -1.7, 11.8), 0.35, 0.14), ((0.95, -2.05, 10.6), 0.32, 0.14), ((0.9, -2.15, 9.9), 0.28, 0.12)], "Scarf", sides=4, ref=(1, 0, 0))
    on("LeftHand"); smooth(True)
    loft([((3.45, -0.9, 6.0), 0.22, 0.22), ((3.45, -1.5, 6.0), 0.22, 0.22)], "PinHandle", sides=10, ref=(0, 0, 1))
    loft([((3.45, -1.5, 6.0), 0.58, 0.58), ((3.45, -4.6, 6.0), 0.58, 0.58)], "Pin", sides=12, ref=(0, 0, 1))
    loft([((3.45, -4.6, 6.0), 0.22, 0.22), ((3.45, -5.3, 6.0), 0.22, 0.22)], "PinHandle", sides=10, ref=(0, 0, 1))
    on("Head"); brows("FurDark", z=16.55, tilt=0.25, w=1.2)

def Faces():
    toon_faces(my=-3.6, mz=13.45, s=0.85)

def Pet():
    b = PET_BONES
    bone("HumanoidRootPart", None, (0, 0, 2.6), b)
    bone("Body", "HumanoidRootPart", (0, 0, 2.6), b)
    loft([((0, 0.1, 0.9), 1.6, 1.4), ((0, 0.0, 2.2), 2.3, 1.95), ((0, 0.0, 3.7), 2.0, 1.7), ((0, 0.0, 4.3), 1.3, 1.1)], "Fur")
    striped(3.9, 1.0, 1.6, -1.95, 0.12, 0.05, cols=4, rows=2)
    loft([((0, -0.3, 4.1), 2.25, 2.0), ((0, -0.3, 4.6), 2.15, 1.9)], "Scarf", sides=10, cap=False)
    bone("Head", "Body", (0, -0.2, 4.3), b)
    loft([((0, -0.3, 4.4), 2.1, 1.9), ((0, -0.4, 5.6), 2.9, 2.6), ((0, -0.35, 7.0), 2.8, 2.5), ((0, -0.3, 7.6), 1.9, 1.6)], "Fur")
    block((0, -2.5, 6.1), (2.6, 0.7, 2.4), "Skin", bevel=0.4)
    block((0, -2.85, 5.45), (1.8, 0.8, 1.0), "SkinDark", bevel=0.3)
    for sx in (1, -1):
        plate([(x * sx, z) for x, z in [(0, 0.05), (0.35, 0.15), (0.75, 0.05), (0.9, -0.18), (0.6, -0.12), (0, -0.1)]], 0.15, (0.05 * sx, -3.28, 5.65), "Mustache")
        block((1.85 * sx, -2.45, 5.6), (0.5, 0.1, 0.28), "Blush", bevel=0.06)
    loft([((0, -0.35, 7.3), 2.75, 2.45), ((0, -0.35, 7.9), 2.75, 2.45)], "HatShade", sides=10)
    loft([((0, -0.35, 7.8), 2.6, 2.3), ((0, -0.3, 9.0), 3.1, 2.75), ((0, -0.3, 9.9), 2.4, 2.1), ((0, -0.3, 10.2), 1.2, 1.0)], "Hat", sides=10)
    for sx, side in ((1, "Left"), (-1, "Right")):
        bone(side + "UpperArm", "Body", (2.0 * sx, 0, 3.6), b)
        loft([((2.0 * sx, 0, 3.8), 0.85, 0.85), ((2.55 * sx, -0.4, 2.3), 0.85, 0.85), ((2.7 * sx, -0.6, 1.5), 0.9, 0.9)], "FurDark", sides=7)
        block((2.75 * sx, -0.7, 1.25), (1.4, 1.4, 1.1), "FurDark", bevel=0.3)
        bone(side + "Leg", "Body", (1.1 * sx, 0, 1.3), b)
        loft([((1.1 * sx, 0, 1.4), 0.95, 0.95), ((1.15 * sx, 0, 0.6), 0.85, 0.85)], "Fur", sides=7)
        block((1.15 * sx, -0.5, 0.33), (1.6, 2.1, 0.66), "FurDark", bevel=0.2)
    pet_faces(0.95, -2.9, 6.75, -3.3, 5.05, s=0.85)

def build():
    build_all(5, Boss, Faces, Pet, height=21.9)
