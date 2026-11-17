"""Draws white-on-transparent VFX textures for Clone a Friend's Modifier auras (Sol's RNG style).
Every texture is white with alpha = shape, so Roblox tints it with Color / ImageColor3."""
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
N = 512
SS = 2  # supersample
S = N * SS
C = S / 2
random.seed(7)
np.random.seed(7)


def canvas():
    return Image.new("L", (S, S), 0)


def finish(img, name, glow=0, glow_strength=0.6, blur=0):
    """img: L mask at S. Adds a soft glow, downsamples, saves white RGBA."""
    a = np.asarray(img, dtype=np.float32) / 255
    if blur:
        a = np.asarray(img.filter(ImageFilter.GaussianBlur(blur * SS)), dtype=np.float32) / 255
    if glow:
        g = np.asarray(img.filter(ImageFilter.GaussianBlur(glow * SS)), dtype=np.float32) / 255
        a = np.clip(np.maximum(a, g * glow_strength * 2.2), 0, 1)
    out = Image.fromarray((a * 255).astype(np.uint8)).resize((N, N), Image.LANCZOS)
    white = Image.new("L", (N, N), 255)
    rgba = Image.merge("RGBA", (white, white, white, out))
    rgba.save(os.path.join(OUT, name + ".png"))
    print("saved", name)


def ring(d, r, w, fill=255):
    d.ellipse([C - r, C - r, C + r, C + r], outline=fill, width=int(w))


def polar(r, a):
    return (C + r * math.cos(a), C + r * math.sin(a))


def star_polygon(d, r, points, step, w):
    pts = [polar(r, -math.pi / 2 + i * 2 * math.pi / points) for i in range(points)]
    for i in range(points):
        d.line([pts[i], pts[(i + step) % points]], fill=255, width=int(w))


def glyphs(d, r, count, size, seed):
    rnd = random.Random(seed)
    for i in range(count):
        a = i * 2 * math.pi / count
        cx, cy = polar(r, a)
        # a tiny rune: 2-4 strokes in a box, rotated toward the centre
        for _ in range(rnd.randint(2, 4)):
            p1 = (rnd.uniform(-1, 1) * size, rnd.uniform(-1, 1) * size)
            p2 = (rnd.uniform(-1, 1) * size, rnd.uniform(-1, 1) * size)
            ca, sa = math.cos(a + math.pi / 2), math.sin(a + math.pi / 2)
            q1 = (cx + p1[0] * ca - p1[1] * sa, cy + p1[0] * sa + p1[1] * ca)
            q2 = (cx + p2[0] * ca - p2[1] * sa, cy + p2[0] * sa + p2[1] * ca)
            d.line([q1, q2], fill=255, width=int(3 * SS))


# 1. MagicCircle: the big ornate ground circle (rings, hexagram, rune band, nodes)
img = canvas(); d = ImageDraw.Draw(img)
R = S * 0.48
ring(d, R, 6 * SS); ring(d, R * 0.93, 2.5 * SS); ring(d, R * 0.80, 4 * SS); ring(d, R * 0.77, 2 * SS)
glyphs(d, R * 0.865, 36, 9 * SS, 1)
star_polygon(d, R * 0.77, 6, 2, 4 * SS)
star_polygon(d, R * 0.77, 12, 5, 1.5 * SS)
ring(d, R * 0.40, 4 * SS); ring(d, R * 0.36, 2 * SS); ring(d, R * 0.14, 3 * SS)
star_polygon(d, R * 0.36, 8, 3, 2.5 * SS)
for i in range(6):
    x, y = polar(R * 0.77, -math.pi / 2 + i * math.pi / 3)
    d.ellipse([x - 16 * SS, y - 16 * SS, x + 16 * SS, y + 16 * SS], outline=255, width=int(3 * SS))
    d.ellipse([x - 6 * SS, y - 6 * SS, x + 6 * SS, y + 6 * SS], fill=255)
for i in range(72):
    a = i * 2 * math.pi / 72
    d.line([polar(R * 0.95, a), polar(R * (0.99 if i % 6 else 1.0), a)], fill=255, width=int(2 * SS))
finish(img, "MagicCircle", glow=6, glow_strength=0.35)

# 2. MagicCircle2: a different circle for counter-rotating layers (octagram, triangles, dotted bands)
img = canvas(); d = ImageDraw.Draw(img)
ring(d, R, 3 * SS); ring(d, R * 0.70, 5 * SS); ring(d, R * 0.66, 2 * SS)
star_polygon(d, R * 0.98, 8, 3, 3 * SS)
for i in range(48):
    x, y = polar(R * 0.84, i * 2 * math.pi / 48)
    rr = (7 if i % 4 == 0 else 3) * SS
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
for k in range(2):
    pts = [polar(R * 0.62, -math.pi / 2 + k * math.pi + i * 2 * math.pi / 3) for i in range(3)]
    d.polygon(pts, outline=255, width=int(4 * SS))
glyphs(d, R * 0.48, 24, 8 * SS, 2)
ring(d, R * 0.32, 3 * SS); ring(d, R * 0.12, 6 * SS)
finish(img, "MagicCircle2", glow=6, glow_strength=0.35)

# 3. Halo: a radiant spiked ring (crown of light)
img = canvas(); d = ImageDraw.Draw(img)
ring(d, R * 0.62, 14 * SS)
for i in range(32):
    a = i * 2 * math.pi / 32
    long = R * (0.98 if i % 2 == 0 else 0.82)
    w = 0.05 if i % 2 == 0 else 0.035
    d.polygon([polar(R * 0.66, a - w), polar(long, a), polar(R * 0.66, a + w)], fill=255)
finish(img, "Halo", glow=14, glow_strength=0.6)

# 4. Wing: a feathered wing, root at the left-middle, sweeping up-right
img = canvas(); d = ImageDraw.Draw(img)
root = (S * 0.06, S * 0.62)
for row, (count, length, spread, thick) in enumerate([(9, 0.88, 1.05, 30), (8, 0.62, 0.95, 34), (7, 0.40, 0.85, 36)]):
    for i in range(count):
        t = i / (count - 1)
        a = -math.pi * 0.42 + t * spread  # from up-right to right-down
        L = S * length * (1 - 0.35 * t)
        tip = (root[0] + math.cos(a) * L, root[1] + math.sin(a) * L)
        nx, ny = -math.sin(a), math.cos(a)
        wdt = thick * SS * (1.2 - 0.4 * t)
        mid = (root[0] + math.cos(a) * L * 0.55, root[1] + math.sin(a) * L * 0.55)
        d.polygon([root, (mid[0] + nx * wdt, mid[1] + ny * wdt), tip, (mid[0] - nx * wdt * 0.4, mid[1] - ny * wdt * 0.4)], fill=255 - row * 40)
finish(img, "Wing", glow=10, glow_strength=0.45)

# 5. Lightning: a long jagged vertical bolt with branches
img = canvas(); d = ImageDraw.Draw(img)


def bolt(x, y, angle, length, width, depth):
    pts = [(x, y)]
    steps = 14
    for i in range(steps):
        x += math.sin(angle) * length / steps + random.uniform(-1, 1) * 18 * SS
        y += math.cos(angle) * length / steps
        pts.append((x, y))
    d.line(pts, fill=255, width=int(width), joint="curve")
    if depth > 0:
        for _ in range(2):
            j = random.randint(3, steps - 3)
            bolt(pts[j][0], pts[j][1], angle + random.choice([-1, 1]) * random.uniform(0.4, 0.9), length * 0.4, width * 0.55, depth - 1)


bolt(C, S * 0.02, 0, S * 0.96, 9 * SS, 2)
finish(img, "Lightning", glow=8, glow_strength=0.7)

# 6. Flame: a tall flickering flame tongue (soft)
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
u = (xx - C) / (S * 0.5)
v = 1 - yy / S  # 0 bottom .. 1 top
width = 0.55 * (1 - v) ** 0.7 * (0.6 + 0.4 * np.sin(v * 9) ** 2) + 0.02
wave = 0.12 * np.sin(v * 7 + 1.3) * v
m = np.clip(1 - np.abs(u - wave) / np.maximum(width, 1e-3), 0, 1) ** 1.4
m *= np.clip(v * 6, 0, 1)
inner = np.clip(1 - np.abs(u - wave) / np.maximum(width * 0.45, 1e-3), 0, 1) * np.clip(1.2 - v * 1.6, 0, 1)
m = np.clip(m * 0.75 + inner * 0.6, 0, 1)
finish(Image.fromarray((m * 255).astype(np.uint8)), "Flame", blur=3)

# 7. Shockwave: thick ring with streaky noisy edges
r = np.hypot(xx - C, yy - C) / (S * 0.5)
ang = np.arctan2(yy - C, xx - C)
noise = 0.06 * np.sin(ang * 23) + 0.04 * np.sin(ang * 51 + 2) + 0.03 * np.sin(ang * 97 + 5)
band = np.exp(-((r - 0.82 - noise * 0.4) / 0.07) ** 2)
streaks = np.clip(0.6 + 0.4 * np.sin(ang * 140) * np.sin(ang * 37), 0, 1)
m = np.clip(band * (0.55 + 0.45 * streaks) + np.exp(-((r - 0.82) / 0.2) ** 2) * 0.25, 0, 1) * (r < 1)
finish(Image.fromarray((m * 255).astype(np.uint8)), "Shockwave")

# 8. Spiral: galaxy arms
m = np.zeros_like(r)
for arm in range(3):
    phase = arm * 2 * math.pi / 3
    theta = ang - phase - np.log(np.maximum(r, 1e-3)) * 3.2
    m += np.exp(-((np.sin(theta / 2)) ** 2) / 0.035) * np.clip(1 - r, 0, 1) ** 0.8
m += np.exp(-(r / 0.12) ** 2) * 1.2
m = np.clip(m, 0, 1) * (r < 1)
finish(Image.fromarray((m * 255).astype(np.uint8)), "Spiral", blur=2)

# 9. StarBurst: an 8-point Sol's-style star with a bright core
m = np.zeros_like(r)
for k, (n, sharp, amp) in enumerate([(4, 260, 1.0), (4, 420, 0.6)]):
    a2 = ang + (math.pi / 4 if k else 0)
    m += amp * np.exp(-sharp * (np.sin(a2 * n / 2) ** 2) * r) * np.clip(1 - r, 0, 1) ** 1.5
m += np.exp(-(r / 0.08) ** 2) + 0.35 * np.exp(-(r / 0.3) ** 2)
m = np.clip(m, 0, 1)
finish(Image.fromarray((m * 255).astype(np.uint8)), "StarBurst")

# 10. GodRays: a fan of light rays rising from the bottom centre
by = (S - yy) / S
bx = (xx - C) / (S * 0.5)
ra = np.arctan2(bx, by)
rays = np.clip(np.sin(ra * 18) * 0.5 + 0.5, 0, 1) ** 3 * 0.9 + np.clip(np.sin(ra * 7 + 1) * 0.5 + 0.5, 0, 1) ** 4 * 0.5
fade = np.clip(1 - np.hypot(bx, by), 0, 1) ** 1.2 * (np.abs(ra) < 1.2)
m = np.clip(rays * fade * 1.4, 0, 1)
finish(Image.fromarray((m * 255).astype(np.uint8)), "GodRays", blur=2)

# 11. Crystal: a cluster of faceted crystals growing from the bottom
img = canvas(); d = ImageDraw.Draw(img)
for (cx, h, w, tilt, shade) in [(0.5, 0.92, 0.13, 0, 255), (0.34, 0.62, 0.10, -0.35, 200), (0.66, 0.70, 0.10, 0.3, 220), (0.22, 0.38, 0.07, -0.6, 170), (0.78, 0.42, 0.07, 0.6, 180)]:
    bx0, by0 = cx * S, S * 0.98
    ax, ay = math.sin(tilt), -math.cos(tilt)
    nx, ny = -ay, ax
    L = h * S
    W = w * S
    tip = (bx0 + ax * L, by0 + ay * L)
    shoulder = 0.78
    p = [(bx0 - nx * W, by0 - ny * W), (bx0 - nx * W + ax * L * shoulder, by0 - ny * W + ay * L * shoulder), tip,
         (bx0 + nx * W + ax * L * shoulder, by0 + ny * W + ay * L * shoulder), (bx0 + nx * W, by0 + ny * W)]
    d.polygon(p, fill=shade)
    d.line([(bx0 + ax * L * 0.1, by0 + ay * L * 0.1), tip], fill=255, width=int(3 * SS))
finish(img, "Crystal", glow=8, glow_strength=0.4)

# 12. Snowflake
img = canvas(); d = ImageDraw.Draw(img)
for i in range(6):
    a = i * math.pi / 3
    d.line([(C, C), polar(R, a)], fill=255, width=int(10 * SS))
    for f in (0.35, 0.6, 0.8):
        base = polar(R * f, a)
        for s in (-1, 1):
            br = (base[0] + math.cos(a + s * 0.8) * R * 0.22 * (1.1 - f), base[1] + math.sin(a + s * 0.8) * R * 0.22 * (1.1 - f))
            d.line([base, br], fill=255, width=int(7 * SS))
finish(img, "Snowflake", glow=6, glow_strength=0.4)

# 13. Feather
img = canvas(); d = ImageDraw.Draw(img)
d.line([(C, S * 0.95), (C + S * 0.05, S * 0.05)], fill=255, width=int(6 * SS))
for i in range(40):
    t = i / 39
    y = S * (0.88 - t * 0.8)
    x = C + S * 0.05 * t
    L = S * 0.22 * math.sin(t * math.pi) ** 0.7
    for s in (-1, 1):
        d.line([(x, y), (x + s * L, y - L * 0.5)], fill=200, width=int(5 * SS))
finish(img, "Feather", glow=4, glow_strength=0.4)

# 14. Bubble: a thin ring with a highlight
img = canvas(); d = ImageDraw.Draw(img)
ring(d, R * 0.9, 10 * SS, 220)
d.arc([C - R * 0.7, C - R * 0.7, C + R * 0.7, C + R * 0.7], 200, 250, fill=255, width=int(18 * SS))
finish(img, "Bubble", glow=6, glow_strength=0.4)

# 15. Scanlines: glitch bars of random widths
m = np.zeros((S, S), np.float32)
y = 0
while y < S:
    h = random.randint(4, 40) * SS
    if random.random() < 0.55:
        x0 = random.randint(0, S // 2)
        x1 = random.randint(S // 2, S)
        m[y:y + h, x0:x1] = random.uniform(0.4, 1)
    y += h + random.randint(2, 20) * SS
finish(Image.fromarray((m * 255).astype(np.uint8)), "Scanlines")

# 16. Energy: a vertical streaky strip for beams (pillars, tornadoes)
m = np.zeros((S, S), np.float32)
for _ in range(60):
    x = random.uniform(0.05, 0.95) * S
    w = random.uniform(2, 14) * SS
    a = random.uniform(0.3, 1)
    m += a * np.exp(-((xx - x) / w) ** 2) * (0.6 + 0.4 * np.sin(yy / S * random.uniform(4, 12) * math.pi + random.uniform(0, 6)))
edge = np.clip(np.sin(xx / S * math.pi), 0, 1) ** 0.6
m = np.clip(m * 0.45 * edge, 0, 1)
finish(Image.fromarray((m * 255).astype(np.uint8)), "Energy")

# 17. Orb: a bright core with soft glow and a rim
m = np.exp(-(r / 0.18) ** 2) + 0.5 * np.exp(-(r / 0.5) ** 2) + 0.5 * np.exp(-((r - 0.62) / 0.04) ** 2)
finish(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)), "Orb")

# 18. Sigil: a big triangle-eye arcane sigil (overhead / behind Celestial, Eclipse, Genesis)
img = canvas(); d = ImageDraw.Draw(img)
tri = [polar(R * 0.92, -math.pi / 2 + i * 2 * math.pi / 3) for i in range(3)]
d.polygon(tri, outline=255, width=int(7 * SS))
ring(d, R * 0.98, 4 * SS)
d.ellipse([C - R * 0.32, C - R * 0.16, C + R * 0.32, C + R * 0.16], outline=255, width=int(7 * SS))
d.ellipse([C - R * 0.09, C - R * 0.09, C + R * 0.09, C + R * 0.09], fill=255)
for i in range(12):
    a = -math.pi / 2 + i * math.pi / 6
    d.line([polar(R * 0.42, a), polar(R * 0.52, a)], fill=255, width=int(5 * SS))
finish(img, "Sigil", glow=8, glow_strength=0.45)

# 19. Slash: a curved crescent swipe (orbiting energy arcs, Tempest wind, Supernova)
m = np.exp(-((r - 0.75) / 0.06) ** 2) * np.clip((ang + math.pi) / (2 * math.pi), 0, 1) ** 2.5
finish(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)), "Slash", blur=1)

# 20. Cracks: ground fracture lines from the centre (Glacier, Inferno, Supernova, Genesis)
img = canvas(); d = ImageDraw.Draw(img)
for i in range(11):
    a = i * 2 * math.pi / 11 + random.uniform(-0.2, 0.2)
    x, y = C, C
    w = 9 * SS
    for step in range(12):
        a += random.uniform(-0.35, 0.35)
        nx2, ny2 = x + math.cos(a) * R / 12, y + math.sin(a) * R / 12
        d.line([(x, y), (nx2, ny2)], fill=255, width=int(max(w, 2 * SS)))
        if random.random() < 0.25:
            b = a + random.choice([-1, 1]) * 0.8
            d.line([(nx2, ny2), (nx2 + math.cos(b) * R * 0.12, ny2 + math.sin(b) * R * 0.12)], fill=255, width=int(max(w * 0.5, 2 * SS)))
        x, y = nx2, ny2
        w *= 0.82
finish(img, "Cracks", glow=7, glow_strength=0.5)
