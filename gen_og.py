#!/usr/bin/env python3
"""
OG Image 1200x630 — Digital AI
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630

# ── Fonts ────────────────────────────────────────────────────────────────
try:
    f_bold    = ImageFont.truetype("/tmp/PlusJakartaSans-Bold.ttf", 80)
    f_xbold   = ImageFont.truetype("/tmp/PlusJakartaSans-ExtraBold.ttf", 82)
    f_wordmark = ImageFont.truetype("/tmp/PlusJakartaSans-Bold.ttf", 26)
    f_body    = ImageFont.truetype("/tmp/DMSans-Regular.ttf", 22)
    f_body_sm = ImageFont.truetype("/tmp/DMSans-Regular.ttf", 18)
    f_url     = ImageFont.truetype("/tmp/PlusJakartaSans-Bold.ttf", 17)
except Exception as e:
    raise SystemExit(f"Font error: {e}")

# ── Background gradient (#0B1847 → #0F1F5C → #3B2FC9, diagonal) ─────────
img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

c1 = (11, 24, 71)    # #0B1847
c2 = (15, 31, 92)    # #0F1F5C
c3 = (59, 47, 201)   # #3B2FC9

for y in range(H):
    for x in range(W):
        t = (x / W * 0.6 + y / H * 0.4)
        if t < 0.45:
            tt = t / 0.45
            r = int(c1[0] + (c2[0] - c1[0]) * tt)
            g = int(c1[1] + (c2[1] - c1[1]) * tt)
            b = int(c1[2] + (c2[2] - c1[2]) * tt)
        else:
            tt = (t - 0.45) / 0.55
            r = int(c2[0] + (c3[0] - c2[0]) * tt)
            g = int(c2[1] + (c3[1] - c2[1]) * tt)
            b = int(c2[2] + (c3[2] - c2[2]) * tt)
        draw.point((x, y), fill=(r, g, b))

draw = ImageDraw.Draw(img)

# ── Diamond shapes — right side ──────────────────────────────────────────
fx, fy = 1200/1584, 630/396

def scale_pts(pts):
    return [(int(x * fx), int(y * fy)) for x, y in pts]

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)

d1 = scale_pts([(1200,-52),(1400,198),(1200,448),(1000,198)])
d2 = scale_pts([(1330,0),(1495,190),(1330,380),(1165,190)])
d3 = scale_pts([(1100,43),(1235,198),(1100,353),(965,198)])

od.polygon(d1, fill=(255,255,255,14), outline=(255,255,255,28))
od.polygon(d2, fill=(255,255,255,10), outline=(255,255,255,18))
od.polygon(d3, fill=(255,255,255,7))

img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img)

# ── Top-left logo: D icon (white) + "Digital AI" wordmark ────────────────
logo_src = Image.open(
    "/cortex/files/identity-engine/digital-ai/logos/png/favicon-32.png"
).convert("RGBA")

# Recolor every non-transparent pixel to white
logo_size = 52
logo = logo_src.resize((logo_size, logo_size), Image.LANCZOS)
pixels = logo.load()
for py in range(logo.height):
    for px in range(logo.width):
        r, g, b, a = pixels[px, py]
        if a > 30:
            pixels[px, py] = (255, 255, 255, a)

logo_x, logo_y = 64, 36
img_rgba = img.convert("RGBA")
img_rgba.paste(logo, (logo_x, logo_y), logo)
img = img_rgba.convert("RGB")
draw = ImageDraw.Draw(img)

# "Digital AI" wordmark next to logo
draw.text(
    (logo_x + logo_size + 14, logo_y + (logo_size // 2) - 14),
    "Digital AI",
    fill=(255, 255, 255),
    font=f_wordmark
)

# ── Separator line below header ───────────────────────────────────────────
draw.line([(64, logo_y + logo_size + 16), (220, logo_y + logo_size + 16)],
          fill=(45, 82, 239), width=2)

# ── Main headline — "O crescimento tem" ──────────────────────────────────
headline1 = "O crescimento tem"
headline2 = "método."

h1_y = 170
draw.text((72, h1_y), headline1, fill=(255, 255, 255), font=f_bold)
draw.text((72, h1_y + 92), headline2, fill=(232, 238, 255), font=f_xbold)

# ── Body text ─────────────────────────────────────────────────────────────
body_y = h1_y + 210
draw.text((72, body_y),
          "ENTREGAMOS SOLUÇÕES COM DADOS,",
          fill=(255, 255, 255, 224), font=f_body_sm)
draw.text((72, body_y + 28),
          "MACHINE LEARNING E IA GENERATIVA.",
          fill=(255, 255, 255, 224), font=f_body_sm)

# ── Separator line before body ────────────────────────────────────────────
line_y = body_y - 16
for x in range(72, 380):
    t = (x - 72) / (380 - 72)
    if t < 0.35:
        alpha = int(255 * t / 0.35 * 0.7)
        r2, g2, b2 = 45, 82, 239
    else:
        tt = (t - 0.35) / 0.65
        alpha = int(255 * 0.7 * (1 - tt * 0.6))
        r2 = int(45 + (232 - 45) * tt)
        g2 = int(82 + (238 - 82) * tt)
        b2 = int(239 + (255 - 239) * tt)
    draw.point((x, line_y), fill=(r2, g2, b2, alpha))
    draw.point((x, line_y + 1), fill=(r2, g2, b2, alpha // 2))

# ── URL bottom left ───────────────────────────────────────────────────────
draw.text((72, H - 56), "digital-ai.tech",
          fill=(45, 82, 239), font=f_url)

# ── Save ──────────────────────────────────────────────────────────────────
out = "/workspace/og-image.png"
img.save(out, "PNG", optimize=True)

import os
print(f"Saved {out} ({os.path.getsize(out):,} bytes)")
