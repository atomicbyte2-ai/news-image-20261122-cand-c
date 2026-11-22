#!/usr/bin/env python3
"""news-image-20261122-cand-c: "THE WORLD TODAY - 42 STORIES".

Generates entry.png (1600x4272, <=1 MiB) deterministically with Pillow.
Flat vector-style illustrations drawn with PIL shapes (no photos).
All text is programmatic; region counts sum exactly to 42.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 4272
OUT = os.path.join(HERE, "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


# Palette
CREAM = (247, 242, 231)
PAPER = (255, 253, 247)
NAVY = (20, 38, 74)
NAVY2 = (28, 52, 96)
RED = (178, 44, 36)
TEAL = (14, 124, 123)
GOLD = (217, 164, 65)
INK = (24, 24, 24)
GREY = (90, 88, 80)
LINE = (200, 192, 172)
SKY = (174, 214, 232)
SEA = (23, 78, 120)
GREEN = (46, 125, 62)
PITCH = (58, 140, 72)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
MX = 48  # margin
CW = W - 2 * MX  # 1504


def text_w(s, font):
    return d.textlength(s, font=font)


def wrap(s, font, max_w):
    words = s.split(" ")
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def center(y, s, font, fill, x0=MX, x1=W - MX):
    tw = text_w(s, font)
    d.text(((x0 + x1 - tw) / 2, y), s, font=font, fill=fill)


def rule(y, fill=NAVY, width=3):
    d.line([(MX, y), (W - MX, y)], fill=fill, width=width)


def section_head(y, s):
    f = F(SANS_B, 28)
    d.text((MX, y), s, font=f, fill=RED)
    rule(y + 40, fill=RED, width=3)
    return y + 52


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 10], fill=NAVY)
center(26, "THE WORLD TODAY", F(SERIF_B, 100), NAVY)
center(140, "42 STORIES  \u00b7  7 REGIONS  \u00b7  SUNDAY 22 NOVEMBER 2026",
       F(SANS_B, 29), NAVY)
rule(188, fill=NAVY, width=3)

# ---------------------------------------------------------------- giant date
d.rectangle([MX, 204, W - MX, 296], fill=NAVY)
center(216, "Sunday 22 November 2026", F(SERIF_B, 68), CREAM)

# ---------------------------------------------------------------- headline strip
center(314, "COP31 deal faces a 06:00 GMT vote  \u00b7  Two tankers struck off Oman  \u00b7",
       F(SANS_B, 25), NAVY)
center(348, "France seeks UN action on Myanmar",
       F(SANS_B, 25), NAVY)

# ---------------------------------------------------------------- 6-number strip
NUMBERS = [
    ("03:00", "GMT \u2014 objections to the COP31 deal due"),
    ("06:00", "GMT \u2014 approval session opens in Antalya"),
    ("~200", "nations deadlocked at COP31"),
    ("$7.25bn", "Roundup settlement endorsed in the US"),
    ("37\u201312", "England thrash the All Blacks"),
    ("40,000", "runners in the Philadelphia Marathon"),
]
ny0, ny1 = 396, 528
cell_w = CW / 6
for i, (num, cap) in enumerate(NUMBERS):
    x0 = MX + i * cell_w
    if i:
        d.line([(x0, ny0 + 8), (x0, ny1 - 8)], fill=LINE, width=2)
    center(ny0 + 6, num, F(SANS_B, 42), RED, x0, x0 + cell_w)
    for j, ln in enumerate(wrap(cap, F(SANS, 16), cell_w - 18)):
        center(ny0 + 62 + j * 21, ln, F(SANS, 16), GREY, x0, x0 + cell_w)
rule(ny1 + 6, fill=LINE, width=2)

# ---------------------------------------------------------------- region bar
center(552, "STORIES BY REGION", F(SANS_B, 22), NAVY)
REGIONS = [
    ("EUROPE", 10), ("ASIA", 12), ("MIDDLE EAST", 3), ("AFRICA", 2),
    ("AMERICAS", 10), ("OCEANIA", 3), ("GLOBAL", 2),
]
assert sum(c for _, c in REGIONS) == 42
rcell = CW / 7
for i, (name, cnt) in enumerate(REGIONS):
    x0 = MX + i * rcell
    if i:
        d.line([(x0, 586), (x0, 652)], fill=LINE, width=2)
    center(584, name, F(SANS_B, 17), GREY, x0, x0 + rcell)
    center(606, str(cnt), F(SERIF_B, 40), NAVY, x0, x0 + rcell)
rule(658, fill=LINE, width=2)

# ---------------------------------------------------------------- illustrations
def ill_cop(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(18, 90, 96))
    cx, cy, r = x + w * 0.30, y + h * 0.30, 16
    for k in range(8):
        import math
        a = k * math.pi / 4
        dr.line([(cx + r * 1.6 * math.cos(a), cy + r * 1.6 * math.sin(a)),
                 (cx + r * 2.6 * math.cos(a), cy + r * 2.6 * math.sin(a))],
                fill=GOLD, width=5)
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    gx, gy, gr = x + w * 0.62, y + h * 0.58, min(w, h) * 0.30
    dr.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(64, 150, 210))
    dr.ellipse([gx - gr * 0.7, gy - gr * 0.5, gx - gr * 0.1, gy + gr * 0.1], fill=GREEN)
    dr.ellipse([gx + gr * 0.1, gy + gr * 0.2, gx + gr * 0.7, gy + gr * 0.6], fill=GREEN)
    dr.rectangle([x, y + h * 0.88, x + w, y + h], fill=(12, 60, 52))


def ill_tanker(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=SKY)
    dr.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    hx, hy = x + w * 0.08, y + h * 0.42
    dr.polygon([(hx, hy), (hx + w * 0.84, hy), (hx + w * 0.78, hy + h * 0.20),
                (hx + w * 0.06, hy + h * 0.20)], fill=(60, 60, 66))
    for i, c in enumerate([(178, 44, 36), (217, 164, 65), (14, 124, 123), (178, 44, 36)]):
        dr.rectangle([hx + w * (0.10 + i * 0.17), hy - h * 0.16,
                      hx + w * (0.24 + i * 0.17), hy - h * 0.02], fill=c)
    dr.rectangle([hx + w * 0.78, hy - h * 0.22, hx + w * 0.86, hy - h * 0.02],
                 fill=(240, 240, 235))
    fx, fy = hx + w * 0.62, hy - h * 0.30
    dr.polygon([(fx - 14, fy + 26), (fx, fy), (fx + 14, fy + 26)], fill=(230, 120, 30))
    dr.ellipse([fx - 12, fy + 6, fx + 12, fy + 30], fill=(240, 180, 40))
    for k in range(3):
        wx = x + w * (0.15 + k * 0.3)
        dr.arc([wx, y + h * 0.72, wx + w * 0.18, y + h * 0.86], 0, 180, fill=(255, 255, 255), width=4)


def ill_un(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(28, 52, 96))
    bx, by = x + w * 0.22, y + h * 0.30
    bw, bh = w * 0.56, h * 0.52
    dr.polygon([(bx - 8, by), (bx + bw / 2, by - h * 0.14), (bx + bw + 8, by)],
               fill=(240, 236, 222))
    dr.rectangle([bx, by, bx + bw, by + bh], fill=(240, 236, 222))
    for i in range(5):
        cx = bx + bw * (0.12 + i * 0.19)
        dr.rectangle([cx, by + 6, cx + bw * 0.07, by + bh - 6], fill=NAVY2)
    dr.rectangle([bx - 10, by + bh, bx + bw + 10, by + bh + h * 0.06], fill=(200, 192, 172))
    dr.ellipse([x + w * 0.72, y + h * 0.08, x + w * 0.94, y + h * 0.30], fill=(64, 150, 210))
    dr.ellipse([x + w * 0.76, y + h * 0.12, x + w * 0.84, y + h * 0.20], fill=GREEN)


def ill_plane(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=SKY)
    dr.ellipse([x + w * 0.10, y + h * 0.12, x + w * 0.30, y + h * 0.24], fill=(255, 255, 255))
    dr.ellipse([x + w * 0.22, y + h * 0.06, x + w * 0.42, y + h * 0.18], fill=(255, 255, 255))
    fx, fy = x + w * 0.12, y + h * 0.48
    dr.polygon([(fx, fy + h * 0.06), (fx + w * 0.62, fy), (fx + w * 0.76, fy + h * 0.10),
                (fx + w * 0.62, fy + h * 0.20), (fx, fy + h * 0.20)], fill=(250, 250, 245))
    dr.polygon([(fx + w * 0.55, fy), (fx + w * 0.68, fy - h * 0.18),
                (fx + w * 0.76, fy - h * 0.18), (fx + w * 0.66, fy)], fill=RED)
    dr.polygon([(fx + w * 0.30, fy + h * 0.20), (fx + w * 0.44, fy + h * 0.38),
                (fx + w * 0.54, fy + h * 0.38), (fx + w * 0.44, fy + h * 0.20)], fill=NAVY2)
    for i in range(5):
        wx = fx + w * (0.14 + i * 0.09)
        dr.ellipse([wx, fy + h * 0.06, wx + 10, fy + h * 0.06 + 10], fill=NAVY2)


def ill_flags(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    dr.rectangle([x + w * 0.18, y + h * 0.15, x + w * 0.20, y + h * 0.90], fill=INK)
    dr.rectangle([x + w * 0.62, y + h * 0.15, x + w * 0.64, y + h * 0.90], fill=INK)
    dr.rectangle([x + w * 0.20, y + h * 0.18, x + w * 0.58, y + h * 0.48], fill=(65, 137, 222))
    dr.polygon([(x + w * 0.39, y + h * 0.22), (x + w * 0.42, y + h * 0.30),
                (x + w * 0.50, y + h * 0.30), (x + w * 0.43, y + h * 0.35),
                (x + w * 0.46, y + h * 0.43), (x + w * 0.39, y + h * 0.38),
                (x + w * 0.32, y + h * 0.43), (x + w * 0.35, y + h * 0.35),
                (x + w * 0.28, y + h * 0.30), (x + w * 0.36, y + h * 0.30)], fill=(255, 255, 255))
    dr.rectangle([x + w * 0.64, y + h * 0.18, x + w * 0.92, y + h * 0.28], fill=(0, 122, 61))
    dr.rectangle([x + w * 0.64, y + h * 0.28, x + w * 0.92, y + h * 0.38], fill=(255, 255, 255))
    dr.rectangle([x + w * 0.64, y + h * 0.38, x + w * 0.92, y + h * 0.48], fill=(0, 0, 0))
    dr.rectangle([x + w * 0.64, y + h * 0.18, x + w * 0.71, y + h * 0.48], fill=RED)


def ill_parliament(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    bx, by = x + w * 0.18, y + h * 0.42
    bw, bh = w * 0.64, h * 0.42
    dr.rectangle([bx, by, bx + bw, by + bh], fill=(240, 236, 222))
    dr.pieslice([bx + bw * 0.25, by - h * 0.26, bx + bw * 0.75, by + h * 0.10],
                180, 360, fill=TEAL)
    dr.rectangle([bx + bw * 0.48, by - h * 0.34, bx + bw * 0.52, by - h * 0.24], fill=GOLD)
    for i in range(4):
        cx = bx + bw * (0.10 + i * 0.24)
        dr.rectangle([cx, by + 4, cx + bw * 0.08, by + bh - 4], fill=NAVY2)
    dr.rectangle([bx - 8, by + bh, bx + bw + 8, by + bh + h * 0.05], fill=(200, 192, 172))


def ill_blast(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(44, 44, 60))
    for i, bh in enumerate([0.42, 0.55, 0.34, 0.48, 0.38]):
        bx = x + w * (0.08 + i * 0.17)
        dr.rectangle([bx, y + h * (0.88 - bh), bx + w * 0.13, y + h * 0.88],
                     fill=(24, 24, 32))
    bx, by = x + w * 0.60, y + h * 0.34
    for r, c in [(46, (230, 120, 30)), (30, (240, 180, 40)), (14, (255, 240, 160))]:
        dr.ellipse([bx - r, by - r, bx + r, by + r], fill=c)
    dr.rectangle([x, y + h * 0.88, x + w, y + h], fill=(20, 20, 28))


def ill_aid(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    dr.rectangle([x + w * 0.12, y + h * 0.55, x + w * 0.48, y + h * 0.85], fill=(176, 132, 80))
    dr.rectangle([x + w * 0.52, y + h * 0.42, x + w * 0.86, y + h * 0.72], fill=(196, 152, 96))
    dr.rectangle([x + w * 0.60, y + h * 0.28, x + w * 0.78, y + h * 0.42], fill=(176, 132, 80))
    for cx, cy, s in [(x + w * 0.30, y + h * 0.70, 14), (x + w * 0.69, y + h * 0.57, 12)]:
        dr.ellipse([cx - s, cy - s, cx + s, cy + s], fill=(255, 255, 255))
        dr.rectangle([cx - 3, cy - s + 4, cx + 3, cy + s - 4], fill=RED)
        dr.rectangle([cx - s + 4, cy - 3, cx + s - 4, cy + 3], fill=RED)


def ill_gavel(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(28, 52, 96))
    dr.rectangle([x + w * 0.20, y + h * 0.68, x + w * 0.80, y + h * 0.80], fill=(176, 132, 80))
    dr.rectangle([x + w * 0.24, y + h * 0.60, x + w * 0.76, y + h * 0.68], fill=(150, 108, 62))
    dr.polygon([(x + w * 0.22, y + h * 0.28), (x + w * 0.62, y + h * 0.16),
                (x + w * 0.66, y + h * 0.30), (x + w * 0.26, y + h * 0.42)], fill=(196, 152, 96))
    dr.line([(x + w * 0.62, y + h * 0.30), (x + w * 0.82, y + h * 0.62)],
            fill=(196, 152, 96), width=10)


def ill_f1(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    dr.rectangle([x, y + h * 0.70, x + w, y + h * 0.78], fill=(60, 60, 66))
    dr.polygon([(x + w * 0.10, y + h * 0.62), (x + w * 0.16, y + h * 0.44),
                (x + w * 0.42, y + h * 0.38), (x + w * 0.62, y + h * 0.44),
                (x + w * 0.86, y + h * 0.52), (x + w * 0.88, y + h * 0.62)],
               fill=RED)
    dr.polygon([(x + w * 0.30, y + h * 0.38), (x + w * 0.44, y + h * 0.30),
                (x + w * 0.52, y + h * 0.38)], fill=(20, 38, 74))
    for wx in (0.24, 0.70):
        cx, cy = x + w * wx, y + h * 0.62
        dr.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(20, 20, 20))
        dr.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(200, 200, 200))
    dr.rectangle([x + w * 0.08, y + h * 0.40, x + w * 0.14, y + h * 0.56], fill=NAVY2)


def ill_rugby(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=PITCH)
    dr.line([(x + w * 0.72, y + h * 0.12), (x + w * 0.72, y + h * 0.70)], fill=(255, 255, 255), width=4)
    dr.line([(x + w * 0.86, y + h * 0.12), (x + w * 0.86, y + h * 0.70)], fill=(255, 255, 255), width=4)
    dr.line([(x + w * 0.72, y + h * 0.40), (x + w * 0.86, y + h * 0.40)], fill=(255, 255, 255), width=4)
    dr.ellipse([x + w * 0.12, y + h * 0.34, x + w * 0.58, y + h * 0.72],
               fill=(150, 90, 40))
    dr.arc([x + w * 0.30, y + h * 0.34, x + w * 0.40, y + h * 0.72], 270, 90,
           fill=(255, 255, 255), width=4)


def ill_football(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=PITCH)
    cx, cy, r = x + w * 0.5, y + h * 0.5, min(w, h) * 0.32
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    import math
    pts = []
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        pts.append((cx + r * 0.38 * math.cos(a), cy + r * 0.38 * math.sin(a)))
    dr.polygon(pts, fill=(20, 20, 20))
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        ex, ey = cx + r * 0.95 * math.cos(a), cy + r * 0.95 * math.sin(a)
        vx, vy = cx + r * 0.38 * math.cos(a), cy + r * 0.38 * math.sin(a)
        dr.line([(vx, vy), (ex, ey)], fill=(20, 20, 20), width=3)


def ill_tennis(dr, x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(58, 110, 190))
    dr.rectangle([x + w * 0.10, y + h * 0.10, x + w * 0.90, y + h * 0.90],
                 outline=(255, 255, 255), width=4)
    dr.line([(x + w * 0.10, y + h * 0.50), (x + w * 0.90, y + h * 0.50)],
            fill=(255, 255, 255), width=3)
    cx, cy, r = x + w * 0.62, y + h * 0.66, min(w, h) * 0.20
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 230, 60))
    dr.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=(255, 255, 255), width=4)
    dr.arc([cx - r, cy - r, cx + r, cy + r], 120, 240, fill=(255, 255, 255), width=4)


ILL = {"cop": ill_cop, "tanker": ill_tanker, "un": ill_un, "plane": ill_plane,
       "flags": ill_flags, "parliament": ill_parliament, "blast": ill_blast,
       "aid": ill_aid, "gavel": ill_gavel, "f1": ill_f1, "rugby": ill_rugby,
       "football": ill_football, "tennis": ill_tennis}

# ---------------------------------------------------------------- data
LEADS = [
    dict(n=1, ill="cop", kicker="01 \u00b7 ANTALYA \u00b7 CLIMATE",
         head="COP31 DEAL FACES DAWN VOTE AFTER ALL-NIGHT TALKS",
         deck=("Negotiators in Antalya unveiled a late-night package after about 200 "
               "nations deadlocked over fossil fuels and finance. Objections are due "
               "at 03:00 GMT; the approval session opens at 06:00 GMT on Sunday. "
               "The draft Antalya Accords concede the 1.5C goal has been missed."),
         place="Antalya \u00b7 Climate", src="Reuters / AP / BBC"),
    dict(n=2, ill="tanker", kicker="02 \u00b7 OFF OMAN \u00b7 SHIPPING",
         head="TWO TANKERS STRUCK OFF OMAN AS GULF TENSIONS FLARE",
         deck=("UKMTO reported two vessels hit as they left the Gulf, and Iran said a "
               "third struck a mine east of Hormuz. The attacks raised fresh fears "
               "for shipping through the world\u2019s busiest oil chokepoint."),
         place="Off Oman \u00b7 Shipping", src="UKMTO"),
    dict(n=3, ill="un", kicker="03 \u00b7 NEW YORK / PARIS \u00b7 JUSTICE",
         head="FRANCE SEEKS UN ACTION AFTER MYANMAR REJECTS COURT RULING",
         deck=("Paris moved at the United Nations after Myanmar rejected the world "
               "court\u2019s ruling. The step puts the junta\u2019s defiance before the "
               "Security Council on Sunday, with allies pressing for a response."),
         place="New York / Paris \u00b7 Justice", src="AFP"),
]

SMALL = [
    dict(n=4, ill="plane", head="NEPAL PM FLIES TO DELHI FOR FIRST STATE VISIT",
         deck="Balendra Shah meets Modi today; a joint press conference follows on Monday.",
         place="New Delhi \u00b7 Diplomacy", src="MEA / Radio Nepal"),
    dict(n=5, ill="flags", head="SOMALIA ORDERS UAE ENVOY TO LEAVE",
         deck="Mogadishu expels the envoy and recalls its own ambassador in a deepening rift.",
         place="Mogadishu \u00b7 Diplomacy", src="Wire reports"),
    dict(n=6, ill="parliament", head="EISENKOT ASKED TO FORM ISRAEL\u2019S GOVERNMENT",
         deck="Herzog passes over Netanyahu; the mandate ceremony is held on Sunday.",
         place="Jerusalem \u00b7 Politics", src="Wire reports"),
    dict(n=7, ill="blast", head="MISSILES HIT ZELENSKYY\u2019S HOMETOWN",
         deck="Two dead and 60 wounded in Kryvyi Rih; a hospital and 25 blocks hit.",
         place="Kryvyi Rih \u00b7 War", src="AP"),
    dict(n=8, ill="aid", head="FOUR NATIONS PRESS ISRAEL ON GAZA AID",
         deck="Australia, Canada, Italy and the UK demand more aid as flood misery grows.",
         place="Gaza \u00b7 Aid", src="Wire reports"),
    dict(n=9, ill="gavel", head="COURT BACKS $7.25BN ROUNDUP PAYOUT",
         deck="A US court endorses the huge settlement in the weedkiller cases.",
         place="United States \u00b7 Courts", src="AP"),
    dict(n=10, ill="f1", head="VERSTAPPEN ON POLE IN LAS VEGAS",
         deck="Antonelli fastest but drops five places after a penalty.",
         place="Las Vegas \u00b7 F1", src="Autosport"),
    dict(n=11, ill="rugby", head="ENGLAND THRASH ALL BLACKS 37\u201312",
         deck="A record margin of victory for England in the autumn Test.",
         place="London \u00b7 Rugby", src="BBC"),
    dict(n=12, ill="football", head="LEEDS STUN CHELSEA 4\u20131; ARSENAL HELD 2\u20132",
         deck="Madueke rescues a point for the Gunners at Newcastle.",
         place="England \u00b7 Football", src="Wire reports"),
    dict(n=13, ill="tennis", head="ZVEREV v ALCARAZ FOR YEAR-END TITLE",
         deck="The ATP Finals showdown in Turin starts at 18:00 CET today.",
         place="Turin \u00b7 Tennis", src="Wire reports"),
]

ONELINERS = [
    (14, "India resume Day 3 trailing New Zealand, 159/1; Rahul century headlines",
     "Wellington \u00b7 Times of India"),
    (15, "Air India extends Jeddah suspension to 24 November", "India \u00b7 Daily Jagran"),
    (16, "Cyclone Akvan: 14 flights axed at Ranchi as the storm spreads",
     "Ranchi \u00b7 Daily Jagran"),
    (17, "Modi opens Nitish Setu bridge linking Patna and Vaishali", "Patna \u00b7 Daily Jagran"),
    (18, "TikTok launches a deepfake-spotting tool", "London \u00b7 TikTok"),
    (19, "Prince William backs cover for 10,000 forest staff", "London \u00b7 Daily Jagran"),
    (20, "Sensex falls, ending a two-day rally on Fed rate worries", "Mumbai \u00b7 pw.live"),
    (21, "France: sixth straight Saturday of cost-of-living protests", "Paris \u00b7 Wire reports"),
    (22, "Trump warns of a \u201ctremendous tax\u201d on AI centres abroad",
     "Washington \u00b7 Wire reports"),
    (23, "Man convicted of starting the deadly 2025 Palisades fire", "Los Angeles \u00b7 AP"),
    (24, "US details $12bn of Venezuelan oil revenue", "Washington \u00b7 Wire reports"),
    (25, "Ebola death toll passes 5,700 as containment goes on", "Africa \u00b7 Wire reports"),
    (26, "India-China commanders meet on the Arunachal frontier", "India-China \u00b7 Wire reports"),
    (27, "Bangladesh: 30 homes of Awami League members set on fire", "Dhaka \u00b7 Wire reports"),
    (28, "Thailand: dengue due in six provinces on Sunday", "Bangkok \u00b7 Met Dept"),
    (29, "Japan forces to train live-fire at Indian facilities, a first",
     "Tokyo \u00b7 Wire reports"),
    (30, "India signs off 100 health technology transfers", "New Delhi \u00b7 Daily Jagran"),
    (31, "Cummins wins unanimous backing as Australia captain", "Sydney \u00b7 Wire reports"),
    (32, "4,000-year-old bronze ring found in melting Swiss ice", "Switzerland \u00b7 France 24"),
    (33, "Drones sample whale breath; whole genomes sequenced", "Canada \u00b7 Wire reports"),
    (34, "Bystanders pull driver from burning car in Canberra", "Canberra \u00b7 Wire reports"),
    (35, "Dead man in Tasmania linked to a police officer shooting", "Tasmania \u00b7 Wire reports"),
    (36, "Leapmotor profit falls 73% despite record sales", "Business \u00b7 Wire reports"),
    (37, "PSG win 3-2 at Nice; Doue hurt badly", "Paris \u00b7 Wire reports"),
    (38, "Estonia to close its Russia border; Moscow cries \u201cIron Curtain\u201d",
     "Tallinn \u00b7 Wire reports"),
    (39, "Trump busts cyber director after outage criticism", "Washington \u00b7 Wire reports"),
    (40, "NFL Sunday: Week 12 games across the league", "United States \u00b7 Wire reports"),
    (41, "Santa Ana Volcano reopens its ascent at 08:30", "Volcano \u00b7 ad-hoc-news"),
    (42, "Philadelphia Marathon: 40,000 runners take to the streets",
     "Philadelphia \u00b7 Travel and Tour World"),
]
assert len(LEADS) + len(SMALL) + len(ONELINERS) == 42
assert [n for n, _, _ in ONELINERS] == list(range(14, 43))

# ---------------------------------------------------------------- big leads
y = section_head(676, "THE THREE BIG LEADS")
for i, s in enumerate(LEADS):
    ly = y + i * 272
    d.rectangle([MX, ly, W - MX, ly + 260], fill=PAPER, outline=LINE, width=2)
    iw = 430
    if i % 2 == 0:
        ILL[s["ill"]](d, MX + 2, ly + 2, iw - 4, 256)
        tx = MX + iw + 24
        tw = W - MX - tx - 20
    else:
        ILL[s["ill"]](d, W - MX - iw + 2, ly + 2, iw - 4, 256)
        tx = MX + 20
        tw = W - MX - iw - tx - 4
    d.text((tx, ly + 16), s["kicker"], font=F(SANS_B, 18), fill=RED)
    yy = ly + 46
    for ln in wrap(s["head"], F(SANS_B, 29), tw):
        d.text((tx, yy), ln, font=F(SANS_B, 29), fill=NAVY)
        yy += 36
    yy += 6
    for ln in wrap(s["deck"], F(SANS, 20), tw):
        d.text((tx, yy), ln, font=F(SANS, 20), fill=INK)
        yy += 27
    yy += 4
    d.text((tx, yy), f"{s['place']}  \u00b7  {s['src']}", font=F(SANS, 17), fill=GREY)

# ---------------------------------------------------------------- small cards
y = section_head(1544, "TEN MORE STORIES")
card_w = (CW - 16) // 2
card_h = 172
for i, s in enumerate(SMALL):
    col, row = i % 2, i // 2
    cx = MX + col * (card_w + 16)
    cy = y + row * (card_h + 12)
    d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=PAPER, outline=LINE, width=2)
    ILL[s["ill"]](d, cx + 2, cy + 2, 150, card_h - 4)
    tx = cx + 166
    tw = cx + card_w - tx - 14
    d.text((tx, cy + 10), f"{s['n']:02d}", font=F(SANS_B, 17), fill=RED)
    yy = cy + 34
    for ln in wrap(s["head"], F(SANS_B, 19), tw):
        d.text((tx, yy), ln, font=F(SANS_B, 19), fill=NAVY)
        yy += 24
    yy += 2
    for ln in wrap(s["deck"], F(SANS, 16), tw):
        d.text((tx, yy), ln, font=F(SANS, 16), fill=INK)
        yy += 21
    d.text((tx, cy + card_h - 26), f"{s['place']}  \u00b7  {s['src']}",
           font=F(SANS, 14), fill=GREY)

# ---------------------------------------------------------------- one-liners
y = section_head(2516, "ALSO ON SUNDAY 22 NOVEMBER \u2014 29 MORE STORIES")
col_w = (CW - 16) // 2
row_h = 44
for idx, (n, head, src) in enumerate(ONELINERS):
    col = 0 if idx < 15 else 1
    row = idx if idx < 15 else idx - 15
    ox = MX + col * (col_w + 16)
    oy = y + row * row_h
    d.text((ox, oy), f"{n:02d}", font=F(SANS_B, 18), fill=RED)
    lines = wrap(f"{head} \u2014 {src}", F(SANS, 17), col_w - 52)
    yy = oy
    for ln in lines[:2]:
        d.text((ox + 44, yy), ln, font=F(SANS, 17), fill=INK)
        yy += 21
    if row < 14:
        d.line([(ox, oy + row_h - 6), (ox + col_w, oy + row_h - 6)], fill=LINE, width=1)

# ---------------------------------------------------------------- world map
y = section_head(3240, "WHERE IT HAPPENED \u2014 STORIES 01\u201313")
map_x0, map_y0, map_w, map_h = MX, y, CW, 372
d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h], fill=(226, 236, 240),
            outline=LINE, width=2)


def lonlat_to_xy(lon, lat):
    return (map_x0 + (lon + 180) / 360 * map_w,
            map_y0 + (75 - lat) / 135 * map_h)


def inside(px, py, poly):
    ins = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > py) != (yj > py):
            xin = (xj - xi) * (py - yi) / (yj - yi) + xi
            if px < xin:
                ins = not ins
        j = i
    return ins


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66), (-80, 73),
     (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 32), (-85, 30),
     (-90, 21), (-95, 19), (-97, 16), (-105, 20), (-110, 23), (-115, 30), (-120, 34),
     (-125, 40), (-125, 48), (-135, 58), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 11), (-70, 12), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -52), (-73, -50),
     (-73, -40), (-73, -30), (-70, -18), (-77, -12), (-80, -5), (-81, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 65), (20, 70), (15, 70),
     (10, 64), (5, 60), (5, 58), (0, 55), (-2, 50), (-5, 48), (-10, 44), (-10, 38)],
    [(-17, 15), (-17, 21), (-10, 31), (-5, 35), (10, 37), (20, 32), (30, 31),
     (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10), (48, 0),
     (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (17, -32), (14, -22),
     (12, -15), (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 12)],
    [(30, 60), (40, 68), (55, 70), (70, 72), (85, 73), (100, 77), (115, 76),
     (130, 72), (145, 72), (160, 69), (178, 65), (170, 60), (162, 56), (158, 52),
     (150, 59), (142, 55), (140, 50), (135, 43), (130, 42), (127, 40), (122, 38),
     (120, 32), (122, 28), (115, 22), (110, 20), (108, 18), (105, 10), (103, 8),
     (100, 8), (98, 12), (95, 16), (92, 21), (90, 22), (86, 20), (80, 15), (77, 8),
     (75, 20), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26), (56, 27), (52, 28),
     (50, 29), (48, 30), (44, 29), (40, 31), (36, 36), (33, 36), (30, 36), (27, 37),
     (26, 40), (23, 40), (22, 37), (19, 42), (19, 45), (23, 46), (20, 44), (15, 44),
     (12, 45), (8, 44), (7, 44), (3, 43), (0, 40)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (137, -35), (140, -38), (142, -39), (145, -38),
     (147, -39), (150, -37), (153, -32), (153, -27), (150, -23), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20)],
]
lon = -177.5
while lon < 180:
    lat = 72.5
    while lat > -58:
        if any(inside(lon, lat, c) for c in CONTINENTS):
            px, py = lonlat_to_xy(lon, lat)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(150, 160, 150))
        lat -= 3.0
    lon += 3.0

PINS = [(1, 30.7, 36.9, 0, 0), (2, 58.0, 23.0, 0, 0), (3, 2.3, 48.9, 0, 0),
        (4, 77.2, 28.6, 0, 0), (5, 45.3, 2.0, 0, 0), (6, 35.2, 31.8, 26, -20),
        (7, 33.4, 47.9, 0, 0), (8, 34.5, 31.5, 0, 0), (9, -77.0, 38.9, 0, 0),
        (10, -115.1, 36.2, 0, 0), (11, -0.1, 51.5, 0, 0), (12, -1.5, 53.8, -26, -16),
        (13, 7.7, 45.1, 24, 16)]
for n, lo, la, dx, dy in PINS:
    px, py = lonlat_to_xy(lo, la)
    qx, qy = px + dx, py + dy
    if dx or dy:
        d.line([(px, py), (qx, qy)], fill=RED, width=2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.ellipse([qx - 12, qy - 12, qx + 12, qy + 12], fill=RED, outline=(255, 255, 255), width=2)
    t = str(n)
    fw = d.textlength(t, font=F(SANS_B, 15))
    d.text((qx - fw / 2, qy - 8), t, font=F(SANS_B, 15), fill=(255, 255, 255))
d.text((map_x0 + 12, map_y0 + map_h - 30), "Dots mark stories 01\u201313.",
       font=F(SANS, 15), fill=GREY)

# ---------------------------------------------------------------- date check
y = section_head(3676, "DATE CHECK \u2014 WHAT WE LEFT OUT (AND WHY)")
LEFT_OUT = [
    ("Peru M6.8 quake", "reported Sat 21 Nov, 06:30 Lima time"),
    ("Sparta II hit by drones", "Sat 21 Nov morning, Gulf of Finland"),
    ("\u201cEl Chapo Isidro\u201d captured", "Sat 21 Nov, Sinaloa"),
    ("Kyiv bridge strikes", "Friday\u2019s news, not Sunday\u2019s"),
    ("Shenzhen summit, Trump\u2013Xi", "not a Sunday story"),
    ("Denmark \u201cassassination plot\u201d", "an earlier report"),
    ("Wall Street correction", "Friday\u2019s close"),
    ("BepiColombo at Mercury", "earlier in the week"),
]
for i, (item, why) in enumerate(LEFT_OUT):
    col, row = i % 2, i // 2
    ox = MX + col * ((CW - 16) // 2 + 16)
    oy = y + row * 44
    d.text((ox, oy), "\u00d7", font=F(SANS_B, 20), fill=RED)
    d.text((ox + 26, oy), item, font=F(SANS_B, 18), fill=NAVY)
    d.text((ox + 26, oy + 22), why, font=F(SANS, 16), fill=GREY)
d.text((MX, y + 4 * 44 + 8),
       "Strict Sunday: every story above happened, or was first reported, on 22 November 2026.",
       font=F(SANS, 17), fill=INK)

# ---------------------------------------------------------------- footer
rule(4046, fill=NAVY, width=3)
center(4064, "Every story here happened, or was first reported, on Sunday 22 November 2026.",
       F(SERIF, 22), NAVY)
center(4096, "Sources named beside each story  \u00b7  Original drawings  \u00b7  Built from wire reports",
       F(SANS, 18), GREY)
center(4130, "THE WORLD TODAY \u00b7 42 STORIES \u00b7 SUNDAY 22 NOVEMBER 2026",
       F(SANS_B, 18), NAVY)

img.save(OUT, optimize=True)
print(f"saved {OUT} {img.size} {os.path.getsize(OUT)} bytes")
