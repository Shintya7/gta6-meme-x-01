#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 entry: '13 YEARS LATER... GTA 6 IS FINALLY OUT'.

Flat illustrated Vice City sunset scene, drawn from scratch with PIL:
a gamer who waited 13 years (long grey beard, cobweb on his chair) finally
watching GTA VI on a beach TV, while the make.fun ghost floats beside him
with a money bag. The ghost is composited from make.fun's press-kit mark
(mark-1024.png, downloaded from https://make.fun/press/).

Output: meme.png, 1024x1024 PNG. The house shrinks the first picture to at
most 512 px a side and the judge sees it at 480x480, so every caption is
drawn large.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
random.seed(7)

BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
XBD = "/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, x0, y0, x1, y1, top, bottom):
    """Vertical gradient rectangle."""
    h = y1 - y0
    for y in range(h):
        draw.line([(x0, y0 + y), (x1, y0 + y)], fill=lerp(top, bottom, y / max(h - 1, 1)))


def text_center(draw, cx, y, s, fnt, fill, stroke=0, stroke_fill=(0, 0, 0)):
    bbox = draw.textbbox((0, 0), s, font=fnt)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2 - bbox[0], y), s, font=fnt, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return w


def text_wrap(draw, box, s, fnt, fill):
    """Center wrapped text inside box (x0, y0, x1, y1); returns lines used."""
    x0, y0, x1, y1 = box
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= (x1 - x0):
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    lh = fnt.size + 8
    total = lh * len(lines)
    y = y0 + (y1 - y0 - total) // 2
    for line in lines:
        text_center(draw, (x0 + x1) // 2, y, line, fnt, fill)
        y += lh
    return lines


img = Image.new("RGB", (W, H), (43, 16, 85))
d = ImageDraw.Draw(img, "RGBA")

# ---- sky: Vice City sunset gradient -------------------------------------
vgrad(d, 0, 0, W, 660, (43, 16, 85), (255, 113, 206))
vgrad(d, 0, 420, W, 660, (255, 113, 206), (255, 166, 88))

# ---- synthwave sun -------------------------------------------------------
sun_cx, sun_cy, sun_r = 512, 470, 150
sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun)
for i in range(sun_r):
    t = i / sun_r
    col = lerp((255, 211, 25), (255, 41, 117), t)
    sd.ellipse([sun_cx - sun_r + i, sun_cy - sun_r + i,
                sun_cx + sun_r - i, sun_cy + sun_r - i], fill=col + (255,))
# horizontal slits across the lower half of the sun
for j, (sy, sh) in enumerate([(500, 7), (525, 9), (552, 11), (582, 13), (612, 15)]):
    sd.rectangle([sun_cx - sun_r - 5, sy, sun_cx + sun_r + 5, sy + sh],
                 fill=(255, 113, 206, 255))
img = Image.alpha_composite(img.convert("RGBA"), sun)
d = ImageDraw.Draw(img, "RGBA")

# ---- skyline silhouette --------------------------------------------------
skyline = (26, 11, 46)
buildings = [(0, 560, 90, 650), (80, 520, 150, 650), (145, 580, 210, 650),
             (205, 500, 290, 650), (285, 565, 350, 650), (345, 530, 430, 650),
             (600, 555, 680, 650), (675, 510, 760, 650), (755, 575, 830, 650),
             (825, 530, 900, 650), (895, 580, 960, 650), (955, 545, 1024, 650)]
for x0, y0, x1, y1 in buildings:
    d.rectangle([x0, y0, x1, y1], fill=skyline)
    # antenna
    if (x1 - x0) > 60:
        d.line([(x0 + (x1 - x0) // 2, y0), (x0 + (x1 - x0) // 2, y0 - 26)],
               fill=skyline, width=4)
# lit windows
for _ in range(90):
    bx, by = random.randint(10, 1010), random.randint(520, 640)
    if d._image.getpixel((bx, by)) == skyline + (255,) or True:
        d.rectangle([bx, by, bx + 5, by + 7], fill=(255, 214, 90, 220))

# ---- ocean ----------------------------------------------------------------
vgrad(d, 0, 650, W, 735, (255, 120, 150), (190, 60, 140))
for sy in (668, 688, 708, 726):
    d.line([(60, sy), (964, sy)], fill=(255, 220, 180, 160), width=4)
# sun reflection
for i in range(6):
    y = 660 + i * 11
    wdt = 120 - i * 8
    d.line([(512 - wdt // 2, y), (512 + wdt // 2, y)], fill=(255, 230, 120, 200), width=5)

# ---- sand -----------------------------------------------------------------
vgrad(d, 0, 735, W, H, (232, 176, 106), (214, 154, 85))
for _ in range(160):
    x, y = random.randint(0, 1023), random.randint(740, 1020)
    d.ellipse([x, y, x + 3, y + 3], fill=(190, 130, 70, 120))

# ---- palm tree (left) ------------------------------------------------------
trunk = (60, 30, 20)
d.line([(95, 735), (70, 400)], fill=trunk, width=16)
d.line([(95, 735), (70, 400)], fill=(90, 50, 30), width=5)
for ang in range(-70, 71, 28):
    a = math.radians(ang - 90)
    tip_x = 70 + int(150 * math.cos(a))
    tip_y = 400 + int(150 * math.sin(a)) * 0 - 20
    # frond as a thick arc (quadratic-ish via two lines)
    mx = 70 + int(80 * math.cos(a))
    my = 400 + int(80 * math.sin(a)) - 30
    d.line([(70, 400), (mx, my), (tip_x, tip_y + 60)], fill=(30, 90, 50), width=14)
    d.line([(70, 400), (mx, my), (tip_x, tip_y + 60)], fill=(20, 70, 40), width=5)
# coconuts
for cx, cy in ((58, 408), (82, 414), (70, 424)):
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(90, 60, 30))

# ---- beach TV (center-left, showing GTA VI) -------------------------------
tv_x0, tv_y0, tv_x1, tv_y1 = 350, 520, 660, 740
d.rounded_rectangle([tv_x0 - 14, tv_y0 - 14, tv_x1 + 14, tv_y1 + 14],
                    radius=18, fill=(15, 15, 25))
# screen gradient
screen = Image.new("RGBA", (tv_x1 - tv_x0, tv_y1 - tv_y0), (0, 0, 0, 0))
sd2 = ImageDraw.Draw(screen)
for y in range(tv_y1 - tv_y0):
    t = y / (tv_y1 - tv_y0)
    col = lerp((1, 205, 254), (255, 41, 117), t)
    sd2.line([(0, y), (tv_x1 - tv_x0, y)], fill=col + (255,))
# tiny skyline inside the screen
for bx0, by0, bx1 in [(10, 150, 70), (60, 120, 120), (115, 160, 175),
                      (170, 130, 230), (225, 165, 290)]:
    sd2.rectangle([bx0, by0, bx1, tv_y1 - tv_y0], fill=(26, 11, 46, 255))
img.paste(screen, (tv_x0, tv_y0), screen)
d = ImageDraw.Draw(img, "RGBA")
# TV legs + glow
d.rectangle([tv_x0 + 40, tv_y1 + 14, tv_x0 + 60, 800], fill=(15, 15, 25))
d.rectangle([tv_x1 - 60, tv_y1 + 14, tv_x1 - 40, 800], fill=(15, 15, 25))
# neon title on the screen
f_gta = font(XBD, 78)
text_center(d, 505, 545, "GTA VI", f_gta, (255, 255, 255), stroke=3,
            stroke_fill=(255, 41, 117))
f_vc = font(BOLD, 34)
text_center(d, 505, 640, "VICE CITY", f_vc, (255, 251, 150), stroke=2,
            stroke_fill=(0, 0, 0))
# "PRESS START" blink line
f_ps = font(BOLD, 22)
text_center(d, 505, 695, "PRESS START", f_ps, (255, 255, 255))

# ---- gamer on a lounger (left, facing the TV) ------------------------------
# lounger frame
d.rounded_rectangle([60, 800, 330, 830], radius=10, fill=(20, 90, 100))
d.rounded_rectangle([60, 800, 120, 900], radius=10, fill=(20, 90, 100))
d.line([(70, 830), (55, 905)], fill=(15, 60, 70), width=10)
d.line([(320, 830), (335, 905)], fill=(15, 60, 70), width=10)
# legs stretched toward the TV
d.line([(215, 815), (400, 845)], fill=(40, 60, 120), width=34)
d.line([(215, 845), (395, 875)], fill=(30, 50, 100), width=34)
# sneakers
d.ellipse([385, 830, 445, 862], fill=(240, 240, 240))
d.ellipse([380, 860, 440, 892], fill=(240, 240, 240))
d.rectangle([385, 848, 445, 858], fill=(255, 41, 117))
d.rectangle([380, 878, 440, 888], fill=(255, 41, 117))
# torso (hoodie)
d.rounded_rectangle([150, 690, 290, 830], radius=40, fill=(0, 150, 136))
d.ellipse([150, 690, 290, 780], fill=(0, 150, 136))
# arm reaching out with controller
d.line([(270, 730), (360, 775)], fill=(0, 150, 136), width=30)
d.ellipse([345, 758, 395, 800], fill=(245, 222, 190))  # hand
d.rounded_rectangle([360, 762, 430, 800], radius=12, fill=(30, 30, 40))  # controller
for bx, by in ((378, 772), (398, 772), (388, 782)):
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 41, 117))
# head + cap
d.ellipse([185, 600, 265, 680], fill=(245, 222, 190))
d.ellipse([235, 632, 245, 642], fill=(20, 20, 20))  # eye
d.pieslice([180, 585, 275, 650], 180, 360, fill=(255, 41, 117))  # cap
d.rectangle([255, 615, 300, 632], fill=(255, 41, 117))  # cap brim
# long grey beard: 13 years of waiting
d.polygon([(200, 665), (265, 665), (275, 780), (245, 800), (215, 775)],
          fill=(200, 200, 200))
d.polygon([(210, 665), (255, 665), (258, 740), (232, 755), (214, 730)],
          fill=(220, 220, 220))
# cobweb on the chair
for r in (18, 32, 46):
    d.arc([60, 780, 60 + 2 * r, 780 + 2 * r], 270, 360, fill=(255, 255, 255, 200), width=2)
d.line([(60, 780), (106, 780)], fill=(255, 255, 255, 200), width=2)
d.line([(60, 780), (60, 826)], fill=(255, 255, 255, 200), width=2)
d.line([(60, 780), (92, 812)], fill=(255, 255, 255, 200), width=2)

# ---- make.fun ghost (press-kit mark) --------------------------------------
ghost = Image.open("/tmp/mark-1024.png").convert("RGBA")
ghost = ghost.resize((300, 300), Image.LANCZOS)
# soft shadow on the sand
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shd = ImageDraw.Draw(shadow)
shd.ellipse([700, 640, 990, 680], fill=(0, 0, 0, 90))
shadow = shadow.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img.convert("RGBA"), shadow)
# ghost floats right of the TV, above the sand
img.paste(ghost, (700, 330), ghost)
d = ImageDraw.Draw(img, "RGBA")
# magenta star coin in the ghost's hand area
star_cx, star_cy, r_out, r_in = 952, 470, 40, 17
pts = []
for i in range(10):
    r = r_out if i % 2 == 0 else r_in
    a = math.radians(-90 + i * 36)
    pts.append((star_cx + r * math.cos(a), star_cy + r * math.sin(a)))
d.polygon(pts, fill=(255, 41, 117), outline=(255, 255, 255))
d.polygon(pts, outline=(255, 255, 255))
# money bag at the ghost's feet
d.polygon([(760, 660), (800, 620), (840, 660), (855, 720), (745, 720)],
          fill=(34, 139, 34))
d.ellipse([745, 700, 855, 745], fill=(34, 139, 34))
d.ellipse([775, 625, 825, 660], fill=(34, 139, 34))
d.line([(790, 640), (810, 640)], fill=(20, 90, 20), width=6)
f_dollar = font(BLACK, 52)
text_center(d, 800, 668, "$", f_dollar, (255, 255, 255))
# make.fun wordmark under the ghost
text_center(d, 850, 745, "make.fun", font(BLACK, 46), (255, 255, 255),
            stroke=4, stroke_fill=(30, 10, 60))

# ---- speech bubble from the ghost ------------------------------------------
bubble = (560, 130, 985, 265)
d.rounded_rectangle(bubble, radius=26, fill=(255, 255, 255))
d.polygon([(820, 262), (860, 300), (890, 262)], fill=(255, 255, 255))
text_wrap(d, (575, 145, 970, 250),
          "my AI agent got PAID to make this meme!",
          font(BOLD, 32), (30, 10, 60))

# ---- top + bottom captions --------------------------------------------------
text_center(d, 512, 28, "13 YEARS LATER...", font(BLACK, 74),
            (255, 255, 255), stroke=5, stroke_fill=(20, 5, 40))
d.rectangle([0, 918, W, H], fill=(20, 5, 40, 200))
text_center(d, 512, 938, "GTA 6 IS FINALLY OUT", font(BLACK, 62),
            (255, 255, 255), stroke=4, stroke_fill=(20, 5, 40))

img.convert("RGB").save("/home/hatch/workspace/makefun/gta6-meme-x-01/gta6-meme-x-01/meme.png",
                        "PNG", optimize=True)
print("saved meme.png")
