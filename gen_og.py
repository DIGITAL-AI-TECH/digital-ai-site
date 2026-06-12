#!/usr/bin/env python3
"""
OG Image 1200x630 — Digital AI
Layout adapted from linkedin-cover.svg identity
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630

# ── Fonts ────────────────────────────────────────────────────────────────
try:
    f_bold    = ImageFont.truetype("/tmp/PlusJakartaSans-Bold.ttf", 80)
    f_xbold   = ImageFont.truetype("/tmp/PlusJakartaSans-ExtraBold.ttf", 82)
    f_tag     = ImageFont.truetype("/tmp/PlusJakartaSans-Bold.ttf", 15)
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
        t = (x / W * 0.6 + y / H * 0.4)   # diagonal blend
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
# Scale from 1584x396 → 1200x630: factor_x=0.757, factor_y=1.591
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

# ── Top-left tag: blue dot + "DIGITAL-AI.TECH" ───────────────────────────
tag_x, tag_y = 72, 44
draw.ellipse([tag_x, tag_y + 1, tag_x + 8, tag_y + 9], fill=(45, 82, 239))
draw.text((tag_x + 18, tag_y - 2), "DIGITAL-AI.TECH",
          fill=(255, 255, 255, 209), font=f_tag)

# ── Top-right: D logo favicon (matching identity) ────────────────────────
# Position so it stays inside the canvas
ico_x, ico_y = 1100, 34
ico_w, ico_h = 54, 60

# Background pill
draw.rounded_rectangle(
    [ico_x, ico_y, ico_x + ico_w, ico_y + ico_h],
    radius=10, fill=(45, 82, 239, 210)
)
# Left vertical bar of D
draw.rectangle(
    [ico_x + 10, ico_y + 10, ico_x + 20, ico_y + ico_h - 10],
    fill=(255, 255, 255)
)
# D right arc fill
draw.rounded_rectangle(
    [ico_x + 16, ico_y + 10, ico_x + ico_w - 8, ico_y + ico_h - 10],
    radius=9, fill=(255, 255, 255)
)
# Punch arc center
draw.ellipse(
    [ico_x + 24, ico_y + 18, ico_x + ico_w - 10, ico_y + ico_h - 18],
    fill=(45, 82, 239, 210)
)

# ── Separator line top ────────────────────────────────────────────────────
draw.line([(72, 95), (200, 95)], fill=(45, 82, 239), width=3)

# ── Main headline — "O crescimento tem" ──────────────────────────────────
headline1 = "O crescimento tem"
headline2 = "método."

h1_y = 160
draw.text((72, h1_y), headline1, fill=(255, 255, 255), font=f_bold)

# "método." in ExtraBold #E8EEFF (slightly blue-white, italic feel via color)
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
# Gradient line (approx — draw in segments)
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
