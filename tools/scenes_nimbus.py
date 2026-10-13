#!/usr/bin/env python3
"""Escenas por párrafo de "Nimbus, the Little Cloud" (vocabulario: naturaleza).

Una ilustración por párrafo: images/nimbus/ch<N>/p<NN>.svg. Reutiliza los
personajes y fondos de make_illustrations.py y agrega aquí las expresiones,
el Viento y los encuadres (planos generales, medios y primeros planos) que
necesita cada momento del cuento.

    python3 tools/scenes_nimbus.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import make_illustrations as mi  # noqa: E402
from make_illustrations import (  # noqa: E402
    BLUSH, CLOUD_B, CLOUD_S, LEAF, PLUM, STEM, WHITE,
    big_cloud, blush, calm_eye, circle, cloud, cloud_layer, drop, ellipse, eye, fence, flower, frown, g,
    garden_tree, happy_eye, house, leaf, lin, moon, mountain, n, op, open_mouth, path, pine, rain_field,
    rainbow, rect, rock, round_tree, smile, sparkle, starfield, sun, tuft, url, valley_backdrop,
)

# ------------------------------------------------------------------ cielos

SKY_DAY = [(0, "#BCDBF3"), (0.6, "#D8EAF8"), (1, "#EEF6FB")]
SKY_RAIN = [(0, "#C5D4E9"), (0.65, "#DCE7F3"), (1, "#EEF3F7")]
SKY_GREY = [(0, "#CDD6E4"), (0.65, "#E2E8F0"), (1, "#F1F3F6")]
SKY_HOT = [(0, "#CFE4F5"), (0.7, "#F3F1DC"), (1, "#FFF1C4")]
SKY_BRIGHT = [(0, "#C2DFF5"), (0.7, "#E2F0FA"), (1, "#F1F8FC")]
SKY_EVENING = [(0, "#C7BDE6"), (0.55, "#F1D2E0"), (1, "#FFE0C6")]
SKY_NIGHT = [(0, "#ADA2D9"), (0.6, "#CFC5EC"), (1, "#EBDCEC")]


def sky(stops):
    return lin("sky", stops), rect(0, 0, 800, 600, url("sky"))


def zoom(body, fx, fy, k):
    """Acerca la cámara: el punto (fx, fy) queda en el centro con escala k."""
    return f'<g transform="translate({n(400 - fx * k)} {n(300 - fy * k)}) scale({n(k)})">{body}</g>'


def scale_at(body, cx, cy, k):
    """Escala un grupo alrededor de su centro (cx, cy)."""
    return f'<g transform="translate({n(cx * (1 - k))} {n(cy * (1 - k))}) scale({n(k)})">{body}</g>'


def heart(x, y, s=1.0, fill="#F7A8BC", o=1.0):
    return g(path("M0 6 C-12 -4 -9 -16 0 -9 C9 -16 12 -4 0 6 Z", fill=fill), x, y, s * 1.6, opacity=o if o != 1 else None)


def streak(x0, y0, x1, y1, bend=-30, color="#E3EFFA", sw=7, curl=True):
    """Línea de viento con un rizo al final."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + bend
    d = f"M{n(x0)} {n(y0)} Q{n(mx)} {n(my)} {n(x1)} {n(y1)}"
    if curl:
        d += f" q22 -6 20 -20 q-4 -14 -16 -8"
    return path(d, stroke=color, sw=sw)


def heat_lines(x, y, s=1.0, color="#F5C98A", o=0.8):
    d = "M0 0 q6 -8 0 -16 q-6 -8 0 -16 M18 4 q6 -8 0 -16 q-6 -8 0 -16 M36 0 q6 -8 0 -16 q-6 -8 0 -16"
    return g(path(d, stroke=color, sw=3), x, y, s, opacity=o)


def splash(x, y, s=1.0, color="#A9CBEA"):
    return g(path("M-12 0 Q-9 -9 -5 -3 M12 0 Q9 -9 5 -3 M-3 -6 L-4 -13 M3 -6 L4 -13", stroke=color, sw=2.6), x, y, s)


def bee(x, y, s=1.0, flip=False):
    o = [ellipse(-2, -12, 7, 9, "#FFFFFF", rot=-20, extra=op(0.85)), ellipse(6, -12, 7, 9, "#FFFFFF", rot=20, extra=op(0.85))]
    o.append(ellipse(0, 0, 13, 9, "#FFE08A"))
    o.append(path("M-3 -8 L-3 8 M4 -8 L4 8", stroke=PLUM, sw=3))
    o.append(eye(9, -2, 1.8) + path("M-13 0 L-17 0", stroke=PLUM, sw=2))
    return g("".join(o), x, y, s, flip=flip)


def bubble(x, y, r, tail, content, fill="#FFFFFF"):
    """Globo de pensamiento con burbujitas que bajan hacia `tail`."""
    o = []
    tx, ty = tail
    for k, rr in [(0.62, r * 0.16), (0.82, r * 0.1)]:
        o.append(circle(x + (tx - x) * k, y + (ty - y) * k, rr, fill, ' stroke="#E4DCF7" stroke-width="3"'))
    puffs = [(0, 0, r)] + [(r * 0.62, -r * 0.35, r * 0.55), (-r * 0.62, -r * 0.3, r * 0.55), (r * 0.7, r * 0.35, r * 0.5),
                           (-r * 0.7, r * 0.35, r * 0.5)]
    o.append("".join(circle(x + dx, y + dy, rr + 3, "#E4DCF7") for dx, dy, rr in puffs))
    o.append("".join(circle(x + dx, y + dy, rr, fill) for dx, dy, rr in puffs))
    o.append(content)
    return "".join(o)


# --------------------------------------------------------------- Nimbus

NIM_SHADE = "#E4DCF7"


def brows(y, inner_up=True, w=12, gap=11, sw=2.6):
    """Cejas: inner_up=True da cara preocupada/triste; False, sorprendida."""
    if inner_up:
        return (path(f"M{n(-gap - w)} {n(y)} L{n(-gap)} {n(y - 4)}", stroke=PLUM, sw=sw)
                + path(f"M{n(gap + w)} {n(y)} L{n(gap)} {n(y - 4)}", stroke=PLUM, sw=sw))
    return (path(f"M{n(-gap - w)} {n(y)} Q{n(-gap - w / 2)} {n(y - 6)} {n(-gap)} {n(y)}", stroke=PLUM, sw=sw)
            + path(f"M{n(gap)} {n(y)} Q{n(gap + w / 2)} {n(y - 6)} {n(gap + w)} {n(y)}", stroke=PLUM, sw=sw))


def nim(x, y, s=1.0, expr="happy", rain=False, look=(0, 0), glow=False, full=False, one_drop=None):
    """Nimbus con más expresiones que en make_illustrations.nimbus()."""
    o = []
    if glow:
        o.append(circle(0, -20, 150, url("glow"), op(0.95)))
    if rain:
        for dx, dy in [(-52, 66), (-22, 90), (8, 62), (38, 88), (-38, 122), (-6, 114), (26, 128), (56, 118)]:
            o.append(drop(dx, dy, 0.9, "#A3CDF0"))
    if one_drop:
        o.append(drop(one_drop[0], one_drop[1], 1.0, "#A3CDF0"))
    if full:  # lleno de agua: la sombra se vuelve celeste y asoman gotitas
        o.append(cloud_layer(CLOUD_S, "#BFDDF6", 3) + cloud_layer(CLOUD_S, WHITE, -7))
        for dx in (-62, -40, 40, 62):
            o.append(drop(dx, 36, 0.42, "#A9D4F5"))
    else:
        o.append(cloud_layer(CLOUD_S, NIM_SHADE) + cloud_layer(CLOUD_S, WHITE, -7))
    lx, ly = look
    if expr == "strain":
        o.append(path("M-23 -5 L-12 2 L-23 9", stroke=PLUM, sw=3) + path("M23 -5 L12 2 L23 9", stroke=PLUM, sw=3))
        o.append(circle(-35, 13, 10, BLUSH, op(0.9)) + circle(35, 13, 10, BLUSH, op(0.9)))
        o.append(path("M-8 17 Q-4 13 0 17 Q4 21 8 17", stroke=PLUM, sw=2.8))
        o.append(path("M68 -34 L80 -44 M74 -18 L88 -21 M58 -46 L62 -58", stroke="#A9BCD8", sw=3.2))
        o.append(path("M-68 -34 L-80 -44 M-74 -18 L-88 -21 M-58 -46 L-62 -58", stroke="#A9BCD8", sw=3.2))
        o.append(drop(-84, -40, 0.75, "#B9DCF6"))
    elif expr == "sad":
        o.append(eye(-17, 4, 5.5, (lx, ly + 1)) + eye(17, 4, 5.5, (lx, ly + 1)))
        o.append(brows(-9))
        o.append(blush(-33, 14, 7, 4.5) + blush(33, 14, 7, 4.5))
        o.append(frown(0, 17, 12, 2.8))
    elif expr == "teary":
        o.append(eye(-17, 4, 5.5, (lx, ly + 1)) + eye(17, 4, 5.5, (lx, ly + 1)))
        o.append(brows(-9))
        o.append(blush(-33, 14, 7, 4.5) + blush(33, 14, 7, 4.5))
        o.append(frown(0, 18, 12, 2.8))
        o.append(drop(-24, 24, 0.8, "#A9D4F5"))
    elif expr == "joy":
        o.append(happy_eye(-17, 2, 13) + happy_eye(17, 2, 13))
        o.append(blush(-33, 13, 8, 5) + blush(33, 13, 8, 5))
        o.append(open_mouth(0, 11, 16))
    elif expr == "ask":
        o.append(eye(-17, 2, 5.8, (lx, ly - 2)) + eye(17, 2, 5.8, (lx, ly - 2)))
        o.append(brows(-12, inner_up=False))
        o.append(blush(-33, 13, 8, 5) + blush(33, 13, 8, 5))
        o.append(open_mouth(0, 12, 10))
    elif expr == "hope":
        o.append(eye(-17, 3, 5.8, (lx, ly - 2)) + eye(17, 3, 5.8, (lx, ly - 2)))
        o.append(brows(-10))
        o.append(blush(-33, 14, 7, 4.5) + blush(33, 14, 7, 4.5))
        o.append(smile(0, 15, 9, 2.6, 0.3))
    elif expr == "surprised":
        o.append(eye(-18, 1, 7.2, (lx, ly)) + eye(18, 1, 7.2, (lx, ly)))
        o.append(brows(-15, inner_up=False, w=13, gap=12))
        o.append(blush(-35, 14, 8, 5) + blush(35, 14, 8, 5))
        o.append(ellipse(0, 18, 5.5, 7, PLUM) + ellipse(0, 20, 3, 2.6, "#F49AB0"))
    elif expr == "call":
        o.append(eye(-17, 2, 5.8, (lx, ly)) + eye(17, 2, 5.8, (lx, ly)))
        o.append(brows(-10))
        o.append(blush(-33, 13, 8, 5) + blush(33, 13, 8, 5))
        o.append(open_mouth(0, 11, 13))
    elif expr == "kind":
        o.append(happy_eye(-17, 3, 12) + happy_eye(17, 3, 12))
        o.append(blush(-33, 13, 8.5, 5.5, 0.85) + blush(33, 13, 8.5, 5.5, 0.85))
        o.append(smile(0, 13, 13, 3, 0.4))
    elif expr == "warm":
        o.append(happy_eye(-17, 2, 13) + happy_eye(17, 2, 13))
        o.append(blush(-33, 13, 10, 6.5, 0.95) + blush(33, 13, 10, 6.5, 0.95))
        o.append(smile(0, 12, 18, 3.2, 0.5))
    elif expr == "sleep":
        o.append(calm_eye(-17, 3, 12) + calm_eye(17, 3, 12))
        o.append(blush(-33, 13, 8, 5) + blush(33, 13, 8, 5))
        o.append(smile(0, 15, 8, 2.6, 0.35))
    else:  # happy
        o.append(eye(-17, 2, 5.8, look) + eye(17, 2, 5.8, look))
        o.append(blush(-33, 13, 8, 5) + blush(33, 13, 8, 5))
        o.append(smile(0, 12, 14, 3))
    return g("".join(o), x, y, s)


# ---------------------------------------------------------- Mamá Cúmulo

MAMA = ("#C9D3E6", "#AEBBD3")
MAMA_SOFT = ("#DCE3F0", "#C3CDE0")


def mama(x, y, s=1.0, face="kind", flip=False, colors=MAMA, look=(0, 0), rain=None):
    fill, shade = colors
    o = []
    if rain:
        o.append(rain)
    o.append(cloud_layer(CLOUD_B, shade) + cloud_layer(CLOUD_B, fill, -9))
    if face == "kind":
        o.append(happy_eye(-30, 8, 18, 3.6) + happy_eye(30, 8, 18, 3.6))
        o.append(blush(-56, 24, 12, 7) + blush(56, 24, 12, 7))
        o.append(smile(0, 24, 22, 3.6))
    elif face == "listen":
        o.append(eye(-30, 8, 8, look) + eye(30, 8, 8, look))
        o.append(blush(-56, 24, 12, 7) + blush(56, 24, 12, 7))
        o.append(smile(0, 26, 16, 3.4))
    elif face == "talk":
        o.append(happy_eye(-30, 8, 18, 3.6) + happy_eye(30, 8, 18, 3.6))
        o.append(blush(-56, 24, 12, 7) + blush(56, 24, 12, 7))
        o.append(open_mouth(0, 22, 24))
    elif face == "comfort":
        o.append(eye(-30, 10, 7.5, look) + eye(30, 10, 7.5, look))
        o.append(path("M-44 -6 L-20 -10 M44 -6 L20 -10", stroke=PLUM, sw=3.2))
        o.append(blush(-56, 26, 12, 7) + blush(56, 26, 12, 7))
        o.append(smile(0, 28, 20, 3.4, 0.4))
    elif face == "hug":
        o.append(happy_eye(-34, 2, 20, 3.8) + happy_eye(34, 2, 20, 3.8))
        o.append(blush(-60, 18, 13, 8, 0.9) + blush(60, 18, 13, 8, 0.9))
        o.append(smile(0, 16, 26, 3.8, 0.5))
    elif face == "sleep":
        o.append(calm_eye(-28, 8, 16, 3.4) + calm_eye(28, 8, 16, 3.4))
        o.append(blush(-52, 22, 11, 6) + blush(52, 22, 11, 6))
        o.append(smile(0, 24, 14, 3.2))
    return g("".join(o), x, y, s, flip=flip)


def dark_cloud(x, y, s=1.0, flip=False):
    return big_cloud(x, y, s, "none", "#B9C4DA", "#9EABC6", flip=flip)


# ------------------------------------------------------------- el Viento

WIND = "#E7F1FB"
WIND_D = "#BCD3EC"


def wind(x, y, s=1.0, flip=False, expr="blow"):
    """El Viento: una ráfaga redonda con cara amable y rizos que se alargan."""
    o = [streak(-40, -30, -190, -54, 26, WIND_D, 7), streak(-46, 6, -230, 14, 20, WIND, 8),
         streak(-40, 36, -180, 64, -18, WIND_D, 6)]
    o.append(circle(0, 0, 50, WIND_D) + circle(-3, -4, 46, WIND))
    o.append(path("M-30 -30 C-14 -44 18 -42 30 -24", stroke=WHITE, sw=5, extra=op(0.9)))
    if expr == "blow":
        o.append(happy_eye(-18, -4, 12, 3) + happy_eye(10, -6, 12, 3))
        o.append(blush(-26, 10, 8, 5) + blush(22, 8, 8, 5))
        o.append(ellipse(30, 6, 6, 5, PLUM) + ellipse(30, 7, 3, 2.5, "#F49AB0"))
        o.append(path("M44 0 L64 -4 M44 10 L66 12", stroke=WIND_D, sw=3.4))
    else:
        o.append(eye(-16, -4, 5) + eye(14, -4, 5))
        o.append(blush(-26, 10, 8, 5) + blush(24, 10, 8, 5))
        o.append(smile(0, 10, 16, 3))
    return g("".join(o), x, y, s, flip=flip)


# ------------------------------------------------------------- Daisy

FRESH = ("#FFFFFF", "#FFD86B", STEM, LEAF)
DRY = ("#F2ECDF", "#EBCB82", "#BCCB98", "#D3DDB0")
MID = ("#FAF6EC", "#F4D27C", "#A9CFA0", "#C4E3BC")

POSES = {  # stem path, head position, head rotation
    "up": ("M0 0 C-5 -40 5 -70 0 -96", (0, -104), 0),
    "lift": ("M0 0 C-4 -46 6 -82 22 -94", (28, -96), 32),
    "droop": ("M0 0 C-2 -50 10 -92 40 -82", (50, -62), 78),
}


def daisy_face(expr, petal, center):
    o = []
    for i in range(12):
        o.append(f'<ellipse cx="0" cy="-25" rx="8.5" ry="15" fill="{petal}" stroke="#E4DBEF" stroke-width="1.5" transform="rotate({i * 30})"/>')
    o.append(circle(0, 0, 17, center))
    if expr == "sad":
        o.append(calm_eye(-6, -2, 6, 2.2) + calm_eye(6, -2, 6, 2.2) + frown(0, 6, 7, 2.2))
    elif expr == "sigh":
        o.append(calm_eye(-6, -2, 6, 2.2) + calm_eye(6, -2, 6, 2.2) + frown(0, 7, 6, 2.2))
        o.append(drop(15, -8, 0.42, "#BFE0F7"))
    elif expr == "look":
        o.append(eye(-6, -3, 2.9, (0, -1)) + eye(6, -3, 2.9, (0, -1)) + frown(0, 7, 6, 2.2))
        o.append(blush(-11, 4, 3.4, 2.2, 0.8) + blush(11, 4, 3.4, 2.2, 0.8))
    elif expr == "hope":
        o.append(eye(-6, -3, 2.9, (0, -1)) + eye(6, -3, 2.9, (0, -1)) + smile(0, 5, 6, 2.2, 0.3))
        o.append(blush(-11, 4, 3.4, 2.2, 0.9) + blush(11, 4, 3.4, 2.2, 0.9))
    elif expr == "talk":
        o.append(eye(-6, -3, 2.9) + eye(6, -3, 2.9) + open_mouth(0, 4, 7))
        o.append(blush(-11, 4, 3.4, 2.2, 0.9) + blush(11, 4, 3.4, 2.2, 0.9))
    elif expr == "joy":
        o.append(happy_eye(-6, -2, 6, 2.2) + happy_eye(6, -2, 6, 2.2) + open_mouth(0, 3, 8))
        o.append(blush(-11, 4, 3.6, 2.4, 0.95) + blush(11, 4, 3.6, 2.4, 0.95))
    elif expr == "sleep":
        o.append(calm_eye(-6, -2, 6, 2.2) + calm_eye(6, -2, 6, 2.2) + smile(0, 5, 5, 2, 0.3))
    elif expr == "surprised":
        o.append(eye(-6, -3, 3.2) + eye(6, -3, 3.2) + ellipse(0, 6, 2.6, 3.2, PLUM))
        o.append(blush(-11, 4, 3.4, 2.2, 0.9) + blush(11, 4, 3.4, 2.2, 0.9))
    else:
        o.append(eye(-6, -2, 2.9) + eye(6, -2, 2.9) + smile(0, 4, 8, 2.2))
        o.append(blush(-11, 4, 3.4, 2.2, 0.9) + blush(11, 4, 3.4, 2.2, 0.9))
    return "".join(o)


def daisy2(x, y, s=1.0, pose="up", expr="happy", colors=FRESH, arms_up=False):
    petal, center, stem, lf = colors
    d, (hx, hy), rot = POSES[pose]
    vein = stem if colors is not FRESH else STEM
    o = [path(d, stroke=stem, sw=6)]
    if arms_up:
        o.append(leaf(2, -50, 34, -18, lf, vein) + leaf(-2, -50, 34, -162, lf, vein))
    elif pose == "droop":
        o.append(leaf(0, -28, 30, 35, lf, vein) + leaf(0, -42, 26, 150, lf, vein))
    else:
        o.append(leaf(0, -34, 34, -30, lf, vein) + leaf(0, -54, 30, -150, lf, vein))
    o.append(g(daisy_face(expr, petal, center), hx, hy, rot=rot))
    return g("".join(o), x, y, s)


# ------------------------------------------------------------- paisajes

def ch1_landscape(rng, flowers=False, rain_clouds=False):
    """Montañas, bosque, campos y río (como nimbus_ch1, sin las nubes)."""
    clip_d = "M0 410 Q200 362 400 392 Q600 424 800 372 L800 600 L0 600 Z"
    clip, stripes = mi.fields(clip_d, ["#CFEFE3", "#BEE6D3", "#E6F2CB", "#CFEFE3"])
    o = [mountain(130, 400, 340, 190, "#C9C3E3", snow="#F6F3FC"), mountain(390, 400, 400, 236, "#BDB6DC", snow="#F6F3FC"),
         mountain(650, 400, 340, 128, "#CBC5E4")]
    o.append(path("M0 380 Q160 330 330 360 Q520 395 800 340 L800 420 L0 420 Z", fill="#D9EADF"))
    if rain_clouds:
        o.append(rain_field(rng, 120, 380, 210, 400, 30) + rain_field(rng, 430, 640, 190, 390, 24))
    o.append(stripes)
    o.append(path("M552 410 C530 446 600 470 548 516 C508 552 470 572 462 600 L570 600 C578 570 616 552 646 518 "
                  "C694 466 606 444 576 410 Z", fill="#BFE0F5"))
    o.append(path("M560 440 Q570 436 580 440 M560 530 Q575 524 590 530 M500 580 Q515 574 530 580", stroke="#E3F2FC", sw=3))
    for px, py, ps, c1, c2 in [(30, 404, 0.62, "#9CCDB3", "#86BFA2"), (80, 398, 0.78, "#A6D3BB", "#8FC5A9"),
                               (138, 392, 0.66, "#9CCDB3", "#86BFA2"), (190, 392, 0.82, "#A6D3BB", "#8FC5A9"),
                               (246, 394, 0.64, "#9CCDB3", "#86BFA2"), (296, 398, 0.74, "#A6D3BB", "#8FC5A9")]:
        o.append(pine(px, py, ps, c1, c2))
    o.append(round_tree(112, 410, 0.7) + round_tree(222, 408, 0.6) + round_tree(330, 410, 0.62))
    if flowers:
        for fx, fy, c in [(90, 520, "#F7B7C3"), (160, 560, "#E4DCF7"), (250, 505, "#FFD9CC"), (330, 548, "#F7B7C3"),
                          (400, 500, "#E4DCF7"), (690, 470, "#FFD9CC"), (740, 520, "#F7B7C3"), (420, 575, "#FFD9CC"),
                          (210, 590, "#F7B7C3"), (720, 585, "#E4DCF7")]:
            o.append(flower(fx, fy, 1.0, c, "#FFE38A", 26))
    for tx, ty in [(60, 560), (260, 585), (700, 570), (380, 590)]:
        o.append(tuft(tx, ty, 1.1, "#A7D9C3"))
    return clip, "".join(o)


def far_peaks(base=600, shade=0):
    """Puntas de montañas al fondo del cuadro, para los planos en el cielo."""
    c = ["#D8D2EC", "#CBC5E4", "#DCD6EE"] if not shade else ["#C3B7E0", "#B5A9D8", "#CBC0E6"]
    return (mountain(140, base + 30, 360, 170, c[0], snow="#FBFAFE") + mountain(470, base + 30, 420, 210, c[1], snow="#FBFAFE")
            + mountain(730, base + 30, 300, 140, c[2]))


GROUND = {
    "dry": ("#E9E4C2", "#DEDAB4", "#E2CDB2", "#CBB98E"),
    "shade": ("#E5E3C4", "#D9D9B6", "#DDCBB2", "#C4BC94"),
    "wet": ("#C9EBDC", "#B6E2CC", "#C9AC90", "#9FD6BF"),
    "green": ("#CFEFE3", "#BDE6D2", "#D9BFA4", "#9FD6BF"),
}
DRY_FLOWER = {"#F7B7C3": "#E9CFC8", "#E4DCF7": "#DCD6E0", "#FFD9CC": "#EED8C4"}


def garden2(state="dry", flowers="droop", tree_lush=False, shadow=False, daisy_kw=None, house_on=True):
    """Jardín de los capítulos 2 y 3 con la margarita configurable."""
    g1, g2, soil, tuft_c = GROUND[state]
    o = [path("M-400 440 L0 420 Q400 388 800 420 L1200 440 L1200 1000 L-400 1000 Z", fill=g1)]
    if house_on:
        o.append(house(640, 468, 1.0))
    o.append(path("M-400 486 L0 470 Q400 440 800 470 L1200 486 L1200 1000 L-400 1000 Z", fill=g2))
    o.append(garden_tree(84, 512, 0.82, tree_lush))
    o.append(fence(150, 520, 492, 38))
    o.append(ellipse(330, 545, 210, 34, soil))
    if state in ("dry", "shade"):
        o.append(path("M178 540 L198 548 L214 541 M262 560 L280 552 L298 560 L312 554 M386 536 L402 544 L420 538 "
                      "M448 556 L466 550 L480 558", stroke="#CBAE8C", sw=2.4))
    if state == "wet":
        for px, py, rx in [(230, 556, 24), (430, 552, 28), (300, 572, 18)]:
            o.append(ellipse(px, py, rx, 5, "#B7D9F2", extra=op(0.85)))
            o.append(path(f"M{px - rx * 0.5} {py - 1} L{px - rx * 0.1} {py - 1}", stroke=WHITE, sw=2))
    if shadow:
        o.append(ellipse(330, 545, 190, 38, "#7FA6D6", extra=op(0.16)))
    spots = [(180, 545, "#F7B7C3"), (230, 560, "#E4DCF7"), (270, 538, "#FFD9CC"), (410, 540, "#F7B7C3"),
             (450, 560, "#E4DCF7"), (490, 545, "#FFD9CC")]
    for fx, fy, c in spots:
        if flowers == "up":
            o.append(flower(fx, fy, 1.35, c, "#FFE38A", 40))
        elif flowers == "half":
            o.append(flower(fx, fy, 1.35, {"#F7B7C3": "#F2C6CB", "#E4DCF7": "#E2DCEE", "#FFD9CC": "#F8DCCB"}[c], "#F2DC94", 36))
        else:
            o.append(flower(fx, fy, 1.35, DRY_FLOWER[c], "#E8D6A0", 40, droopy=True))
    kw = {"pose": "droop", "expr": "sad", "colors": DRY}
    kw.update(daisy_kw or {})
    o.append(daisy2(330, 560, 1.25, **kw))
    for tx, ty in [(40, 575), (130, 592), (600, 585), (740, 570)]:
        o.append(tuft(tx, ty, 1.2, tuft_c))
    return "".join(o)


def cottage(x, y, s=1.0):
    """Otra casita (capítulo 3, párrafo 10): lila con techo celeste."""
    o = [rect(-58, -80, 116, 80, "#E9E1F8", rx=8)]
    o.append(path("M-72 -74 L0 -132 L72 -74 Z", fill="#A9D1F0", stroke="#A9D1F0", sw=12))
    o.append(rect(-13, -50, 26, 50, "#9DB9DD", rx=11) + circle(6, -24, 2.4, "#7E9CC6"))
    o.append(rect(24, -62, 24, 22, "#FFF6EA", rx=5) + path("M36 -62 L36 -40 M24 -51 L48 -51", stroke="#E9E1F8", sw=3))
    o.append(circle(0, -98, 9, "#FFF6EA"))
    return g("".join(o), x, y, s)


def sun_face(x, y, r, expr="smile"):
    o = [sun(x, y, r)]
    if expr == "hot":
        for i in range(10):
            a = math.radians(i * 36)
            o.append(path(f"M{n(x + math.cos(a) * r * 1.25)} {n(y + math.sin(a) * r * 1.25)} "
                          f"L{n(x + math.cos(a) * r * 1.55)} {n(y + math.sin(a) * r * 1.55)}", stroke="#FFD27A", sw=4))
        o.append(calm_eye(x - r * 0.32, y - r * 0.05, r * 0.26, 2.6) + calm_eye(x + r * 0.32, y - r * 0.05, r * 0.26, 2.6))
        o.append(smile(x, y + r * 0.28, r * 0.34, 2.6, 0.35))
    else:
        o.append(happy_eye(x - r * 0.32, y - r * 0.05, r * 0.28, 2.8) + happy_eye(x + r * 0.32, y - r * 0.05, r * 0.28, 2.8))
        o.append(blush(x - r * 0.55, y + r * 0.22, r * 0.16, r * 0.1) + blush(x + r * 0.55, y + r * 0.22, r * 0.16, r * 0.1))
        o.append(smile(x, y + r * 0.22, r * 0.42, 2.8, 0.5))
    return "".join(o)


def leaves_blowing(rng, x0, x1, y0, y1, count):
    out = []
    for _ in range(count):
        out.append(leaf(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(20, 26), rng.uniform(-60, 60),
                        rng.choice([LEAF, "#C9E8B8", "#F7D9A8"]), STEM))
    return "".join(out)


# ======================================================== capítulo 1

def c1p01():
    defs, bg = sky(SKY_DAY)
    rng = random.Random(101)
    clip, land = ch1_landscape(rng)
    o = [bg, sun(700, 92, 32), cloud(120, 110, 0.9, o=0.95), cloud(560, 70, 0.6, o=0.9, flip=True), cloud(250, 300, 0.55, o=0.85)]
    o.append(g(land, 0, 110))
    o.append(nim(420, 230, 1.45, "happy"))
    o.append(sparkle(300, 180, 8, WHITE) + sparkle(540, 160, 7, WHITE) + sparkle(520, 300, 6, WHITE))
    return defs + clip, "".join(o)


def c1p02():
    defs, bg = sky(SKY_DAY)
    rng = random.Random(102)
    clip, land = ch1_landscape(rng, flowers=True)
    o = [bg, sun_face(690, 100, 40, "smile"), cloud(400, 80, 0.55, o=0.85)]
    o.append(g(land, 0, 40))
    o.append(nim(190, 150, 0.95, "happy", look=(2, 3)))
    o.append(sparkle(600, 520, 6, WHITE) + sparkle(560, 590, 5, WHITE))
    return defs + clip, "".join(o)


def c1p03():
    defs, bg = sky(SKY_RAIN)
    rng = random.Random(103)
    clip, land = ch1_landscape(rng, rain_clouds=True)
    o = [bg, g(land, 0, 30)]
    o.append(dark_cloud(230, 170, 0.95) + dark_cloud(520, 140, 0.85, flip=True) + dark_cloud(380, 90, 0.6))
    for sx, sy in [(90, 470), (180, 520), (290, 480), (420, 560), (230, 590), (690, 500)]:
        o.append(splash(sx, sy, 1.0, "#9EC3E6"))
    o.append(nim(700, 300, 0.7, "happy", look=(-3, 0)))
    return defs + clip, "".join(o)


def c1p04():
    defs, bg = sky(SKY_DAY)
    o = [bg, far_peaks(560)]
    o.append(mama(250, 190, 1.3, "listen", look=(3, 3)))
    o.append(nim(560, 360, 1.45, "ask"))
    o.append(bubble(660, 210, 46, (600, 300), drop(660, 215, 2.2, "#A3CDF0") + sparkle(690, 190, 6, "#FFFFFF")))
    return defs, "".join(o)


def c1p05():
    defs, bg = sky(SKY_DAY)
    o = [bg, far_peaks(600), cloud(680, 110, 0.5, o=0.9)]
    o.append(mama(340, 250, 1.75, "talk"))
    o.append(nim(640, 430, 0.95, "joy"))
    o.append(sparkle(560, 360, 9, WHITE) + sparkle(710, 360, 7, WHITE) + sparkle(130, 120, 7, WHITE))
    return defs, "".join(o)


def c1p06():
    defs, bg = sky(SKY_DAY)
    o = [bg, far_peaks(600), cloud(140, 110, 0.6, o=0.9), cloud(680, 140, 0.5, o=0.9, flip=True)]
    o.append(nim(400, 280, 2.1, "strain"))
    # ni una gota: solo el contorno punteado de una gota vacía
    o.append(g(path("M0 -11 C4 -5 7 -1 7 3 A7 7 0 0 1 -7 3 C-7 -1 -4 -5 0 -11 Z", fill="none", stroke="#A9C6E6", sw=1.6,
                    extra=' stroke-dasharray="3 3"'), 400, 425, 2.4))
    return defs, "".join(o)


def c1p07():
    defs, bg = sky(SKY_GREY)
    rng = random.Random(107)
    far = (mountain(620, 600, 300, 120, "#D4CFE6", snow="#FBFAFE") + mountain(730, 600, 220, 90, "#DCD7EC"))
    rain = rain_field(rng, 560, 760, 430, 560, 16, "#B5CDE8", 0.5)
    o = [bg, far, rain, dark_cloud(600, 400, 0.38), dark_cloud(700, 380, 0.32, flip=True), dark_cloud(650, 360, 0.28)]
    o.append(nim(250, 290, 0.95, "teary", look=(0, 1)))
    return defs, "".join(o)


def c1p08():
    defs, bg = sky(SKY_DAY)
    o = [bg, far_peaks(600)]
    o.append(mama(320, 220, 1.45, "comfort", look=(4, 4)))
    o.append(nim(560, 390, 1.2, "hope", look=(-2, 0)))
    o.append(heart(445, 350, 1.2, "#F7B7C3", 0.95) + heart(490, 310, 0.8, "#F7B7C3", 0.85))
    return defs, "".join(o)


def c1p09():
    defs, bg = sky(SKY_DAY)
    rng = random.Random(109)
    o = [bg, far_peaks(600), cloud(650, 90, 0.5, o=0.9)]
    o.append(wind(250, 300, 1.15))
    o.append(streak(330, 250, 470, 230, -18, WIND_D, 5, False) + streak(320, 360, 470, 380, 14, WIND, 6, False))
    o.append(leaves_blowing(rng, 330, 500, 200, 420, 6))
    o.append(nim(590, 300, 1.25, "surprised", look=(-2, 0)))
    return defs, "".join(o)


def c1p10():
    defs, bg = sky(SKY_DAY)
    rng = random.Random(110)
    clip, land = ch1_landscape(rng)
    o = [bg, sun(720, 80, 28), g(land, 0, 90)]
    o.append(mama(110, 150, 0.42, "kind") + big_cloud(190, 110, 0.3, "sleepy", flip=True))
    o.append(streak(260, 250, 560, 220, 30, WIND_D, 6) + streak(240, 290, 540, 270, 24, WIND, 7, False))
    o.append(wind(470, 200, 0.5))
    o.append(nim(600, 220, 0.85, "happy", look=(3, -1)))
    return defs + clip, "".join(o)


# ======================================================== capítulo 2

def c2p01():
    defs, bg = sky(SKY_HOT)
    o = [bg, sun(110, 96, 34)]
    o.append(mountain(560, 470, 360, 160, "#D8D2EC"))
    o.append(mountain(290, 470, 520, 320, "#C9C3E3", snow="#FBFAFE", snow_frac=0.32))
    o.append(path("M0 450 Q400 420 800 450 L800 600 L0 600 Z", fill="#E6E3C6"))
    o.append(ellipse(420, 486, 260, 30, "#A9D2F0") + path("M260 484 Q285 478 310 484 M470 490 Q500 484 530 490 M600 480 Q620 476 640 480",
                                                       stroke="#D6EBFA", sw=3))
    o.append(path("M0 530 Q400 500 800 530 L800 600 L0 600 Z", fill="#DCD7B8"))
    for rx, ry, rs in [(70, 560, 1.0), (130, 575, 0.7), (250, 568, 1.1), (560, 572, 0.9), (640, 560, 1.2), (720, 580, 0.7),
                       (380, 582, 0.6)]:
        o.append(rock(rx, ry, rs))
    o.append(streak(330, 180, 560, 160, 30, WIND_D, 6) + streak(320, 216, 540, 200, 20, WIND, 7, False))
    o.append(wind(430, 190, 0.5))
    o.append(nim(600, 170, 0.95, "joy"))
    return defs, "".join(o)


def mini_garden(x, y, s=1.0):
    """El jardín seco visto de lejos, junto a la casita amarilla."""
    o = [ellipse(0, 22, 200, 34, "#E2CDB2"), garden_tree(-190, 20, 0.7, False), fence(-150, 110, 6, 34)]
    for fx, c in [(-110, "#E9CFC8"), (-60, "#DCD6E0"), (50, "#EED8C4"), (100, "#E9CFC8")]:
        o.append(flower(fx, 34, 1.1, c, "#E8D6A0", 34, droopy=True))
    o.append(daisy2(0, 40, 0.95, "droop", "sad", DRY))
    o.append(house(220, 10, 0.9))
    return g("".join(o), x, y, s)


def c2p02():
    defs, bg = sky(SKY_HOT)
    o = [bg, sun(110, 100, 36), g(valley_backdrop(), 0, 20)]
    o.append(path("M0 440 Q400 410 800 440 L800 600 L0 600 Z", fill="#E9E4C2"))
    o.append(path("M0 500 Q400 476 800 500 L800 600 L0 600 Z", fill="#DEDAB4"))
    for rx, ry, rs in [(60, 560, 0.9), (720, 570, 1.0), (640, 590, 0.6)]:
        o.append(rock(rx, ry, rs))
    o.append(mini_garden(340, 505, 0.7))
    o.append(sparkle(200, 440, 8, WHITE) + sparkle(470, 420, 7, WHITE) + sparkle(340, 400, 6, WHITE))
    o.append(nim(610, 170, 1.35, "surprised", look=(-2, 3)))
    return defs, "".join(o)


def c2p03():
    defs, bg = sky(SKY_HOT)
    scene = valley_backdrop() + garden2("dry")
    o = [bg, sun_face(110, 100, 40, "hot"), zoom(scene, 300, 470, 1.4)]
    o.append(heat_lines(300, 250, 1.2) + heat_lines(540, 230, 1.0) + heat_lines(150, 300, 0.9))
    return defs, "".join(o)


def c2p04():
    defs, bg = sky(SKY_HOT)
    scene = valley_backdrop() + garden2("dry", daisy_kw={"expr": "look"})
    o = [bg, sun(110, 100, 40), scene]
    o.append(nim(420, 240, 1.05, "call", look=(-2, 2)))
    o.append(path("M330 300 Q316 316 330 332 M312 290 Q290 316 312 342", stroke="#C9C1E2", sw=3.4))
    return defs, "".join(o)


def c2p05():
    defs, bg = sky(SKY_HOT)
    rng = random.Random(205)
    far = dark_cloud(620, 96, 0.3) + dark_cloud(712, 80, 0.26, flip=True) + rain_field(rng, 580, 760, 110, 175, 10, "#B5CDE8", 0.4)
    scene = garden2("dry", daisy_kw={"expr": "sigh"})
    o = [bg, far, sun_face(150, 110, 54, "hot"), zoom(scene, 360, 470, 2.0)]
    o.append(heat_lines(340, 180, 1.4) + heat_lines(520, 150, 1.1))
    return defs, "".join(o)


def c2p06():
    defs, bg = sky(SKY_HOT)
    memory = (circle(180, 140, 80, "#D8EAF8") + big_cloud(140, 135, 0.32, "none", "#C9D3E6", "#AEBBD3")
              + big_cloud(225, 115, 0.26, "none", "#C9D3E6", "#AEBBD3", flip=True) + nim(205, 170, 0.32, "sad"))
    o = [bg, far_peaks(610), bubble(180, 140, 92, (330, 260), memory)]
    o.append(nim(470, 320, 1.85, "sad", look=(-2, 0)))
    return defs, "".join(o)


def c2p07():
    defs, bg = sky(SKY_HOT)
    scene = valley_backdrop() + garden2("dry", daisy_kw={"expr": "hope", "pose": "droop"}) + nim(400, 330, 0.9, "kind")
    o = [bg, sun(120, 90, 40), zoom(scene, 360, 440, 1.5)]
    o.append(heart(640, 110, 1.0, "#F7B7C3", 0.9) + heart(600, 160, 0.6, "#F7B7C3", 0.8))
    return defs, "".join(o)


def c2p08():
    defs, bg = sky(SKY_HOT)
    o = [bg, sun(250, 120, 40), valley_backdrop()]
    o.append(garden2("shade", flowers="half", shadow=True, daisy_kw={"pose": "lift", "expr": "hope", "colors": MID}))
    o.append(nim(330, 205, 1.25, "kind"))
    o.append(path("M240 270 L190 520 M420 270 L480 520", stroke="#9EC0E8", sw=2, extra=' stroke-dasharray="2 10" opacity="0.6"'))
    for sx, sy in [(230, 470), (430, 470), (330, 440)]:
        o.append(sparkle(sx, sy, 7, "#EAF4FF", 0.95))
    return defs, "".join(o)


def c2p09():
    defs, bg = sky(SKY_HOT)
    scene = garden2("shade", flowers="half", shadow=True, daisy_kw={"pose": "up", "expr": "talk", "colors": MID})
    o = [bg, zoom(scene, 340, 470, 2.2)]
    o.append(nim(250, 30, 1.6, "joy"))
    o.append(sparkle(560, 160, 9, WHITE) + sparkle(600, 240, 6, WHITE) + heart(560, 210, 1.1, "#F7B7C3", 0.9))
    return defs, "".join(o)


def c2p10():
    defs, bg = sky(SKY_HOT)
    o = [bg, far_peaks(620), nim(400, 300, 2.0, "warm", glow=True)]
    for hx, hy, hs in [(250, 190, 1.2), (560, 170, 1.4), (600, 330, 0.9), (210, 340, 0.8), (470, 120, 0.8)]:
        o.append(heart(hx, hy, hs, "#F7B7C3", 0.9))
    o.append(sparkle(320, 130, 8, WHITE) + sparkle(660, 250, 7, WHITE) + sparkle(160, 260, 6, WHITE))
    return defs, "".join(o)


# ======================================================== capítulo 3

def c3p01():
    defs, bg = sky(SKY_BRIGHT)
    told = (mountain(110, 175, 90, 70, "#C9C3E3", snow="#FBFAFE") + mountain(160, 175, 70, 50, "#D8D2EC")
            + ellipse(140, 186, 54, 10, "#A9D2F0") + path("M96 200 C120 206 150 196 186 206", stroke="#A9D2F0", sw=6))
    seed = (ellipse(538, 150, 9, 6, "#C9A07E", rot=-20) + path("M580 172 L580 150", stroke=STEM, sw=3) + leaf(580, 152, 13, -40)
            + leaf(580, 154, 12, -145) + path("M580 172 L572 186 M580 172 L588 188 M580 174 L580 192", stroke="#C9A98F", sw=2)
            + bee(618, 140, 0.9))
    o = [bg, sun(700, 90, 30), valley_backdrop()]
    o.append(garden2("shade", flowers="half", daisy_kw={"pose": "up", "expr": "talk", "colors": MID}))
    o.append(nim(260, 300, 0.95, "happy", look=(2, 1)))
    o.append(bubble(140, 175, 70, (230, 260), scale_at(told, 138, 178, 1.08)))
    o.append(bubble(580, 165, 70, (400, 420), scale_at(seed, 580, 162, 1.2)))
    return defs, "".join(o)


def c3p02():
    defs, bg = sky(SKY_BRIGHT)
    o = [bg, far_peaks(620), nim(400, 290, 2.15, "warm", full=True)]
    for sx, sy, r in [(190, 170, 10), (620, 160, 9), (640, 340, 7), (170, 330, 7), (400, 90, 8), (520, 110, 6)]:
        o.append(sparkle(sx, sy, r, "#FFF6C8"))
    o.append(path("M226 236 L206 230 M232 270 L210 272 M574 236 L594 230 M568 270 L590 272", stroke="#C9C1E2", sw=3.4))
    o.append(heart(300, 120, 0.9, "#F7B7C3", 0.9) + heart(560, 380, 0.8, "#F7B7C3", 0.85))
    return defs, "".join(o)


def c3p03():
    defs, bg = sky(SKY_BRIGHT)
    o = [bg]
    o.append(path("M0 470 Q400 430 800 470 L800 600 L0 600 Z", fill="#E5E3C4"))
    o.append(flower(120, 600, 3.0, "#F2C6CB", "#F2DC94", 40) + flower(690, 600, 2.6, "#E2DCEE", "#F2DC94", 40))
    o.append(path("M420 640 C410 560 430 500 420 440", stroke="#A9CFA0", sw=16))
    o.append(leaf(420, 560, 70, -30, "#C4E3BC", "#A9CFA0") + leaf(420, 590, 64, -150, "#C4E3BC", "#A9CFA0"))
    o.append(g(daisy_face("surprised", "#FAF6EC", "#F4D27C"), 420, 330, 3.6))
    # la gota en el pétalo, con salpicadura
    o.append(drop(470, 228, 2.4, "#A3CDF0") + path("M440 238 Q446 226 452 234 M488 234 Q494 226 500 238", stroke="#A3CDF0", sw=3))
    o.append(sparkle(500, 200, 9, WHITE))
    o.append(g(cloud_layer(CLOUD_S, NIM_SHADE) + cloud_layer(CLOUD_S, WHITE, -7), 470, -10, 2.6))
    return defs, "".join(o)


def c3p04():
    defs, bg = sky(SKY_BRIGHT)
    o = [bg, far_peaks(640)]
    o.append(path("M0 560 Q400 540 800 560 L800 600 L0 600 Z", fill="#E5E3C4"))
    o.append(fence(-10, 810, 610, 60))
    o.append(nim(400, 260, 2.1, "surprised", one_drop=(0, 110)))
    o.append(path("M560 140 L590 120 M572 176 L606 172 M240 140 L210 120 M228 176 L194 172", stroke="#C9C1E2", sw=3.6))
    return defs, "".join(o)


def c3p05():
    defs, bg = sky([(0, "#C9D9EC"), (0.7, "#E2ECF6"), (1, "#F1F6FB")])
    rng = random.Random(305)
    o = [bg, valley_backdrop()]
    o.append(garden2("wet", flowers="up", tree_lush=True, daisy_kw={"pose": "up", "expr": "joy", "colors": FRESH}))
    o.append(rain_field(rng, 200, 470, 270, 520, 34, "#A3CDF0", 0.8) + rain_field(rng, 40, 140, 380, 470, 6, "#A3CDF0", 0.7))
    for sx, sy in [(200, 556), (290, 572), (380, 548), (460, 566)]:
        o.append(splash(sx, sy, 0.9, "#9EC3E6"))
    o.append(nim(330, 200, 1.15, "joy", rain=True))
    return defs, "".join(o)


def c3p06():
    defs, bg = sky(SKY_BRIGHT)
    rng = random.Random(306)
    scene = garden2("wet", flowers="up", tree_lush=True, daisy_kw={"pose": "up", "expr": "joy", "colors": FRESH, "arms_up": True})
    o = [bg, zoom(scene, 340, 480, 2.1)]
    o.append(rain_field(rng, 120, 680, 120, 420, 18, "#A3CDF0", 0.9))
    o.append(nim(400, 20, 1.7, "joy"))
    o.append(sparkle(560, 260, 9, WHITE) + sparkle(220, 230, 8, WHITE) + sparkle(640, 380, 6, WHITE))
    return defs, "".join(o)


def c3p07():
    defs, bg = sky(SKY_BRIGHT)
    o = [bg, valley_backdrop(), rainbow(400, 470, 360, 18, 0.95)]
    o.append(garden2("green", flowers="up", tree_lush=True, daisy_kw={"pose": "up", "expr": "joy", "colors": FRESH}))
    o.append(sun(510, 140, 40))
    o.append(nim(440, 175, 1.1, "joy"))
    for sx, sy in [(250, 260), (330, 300), (560, 280), (620, 330), (200, 350)]:
        o.append(sparkle(sx, sy, 7, "#FFF6C8"))
    for dx, dy in [(380, 300), (470, 320)]:
        o.append(drop(dx, dy, 0.8, "#A3CDF0"))
    return defs, "".join(o)


def c3p08():
    defs, bg = sky(SKY_EVENING)
    o = [bg, sun(660, 470, 46)]
    o.append(mountain(120, 610, 380, 250, "#BFB2DE", snow="#F6F1FB") + mountain(420, 610, 460, 310, "#B1A4D6", snow="#F6F1FB")
             + mountain(700, 610, 360, 220, "#C6B9E2"))
    o.append(path("M0 560 Q400 520 800 560 L800 600 L0 600 Z", fill="#A99CCF"))
    o.append(mama(650, 140, 0.45, "kind", colors=MAMA_SOFT))
    o.append(streak(150, 260, 380, 230, 30, "#F2E6F4", 6) + streak(140, 300, 360, 280, 24, "#F8EEF6", 7, False))
    o.append(wind(230, 250, 0.6))
    o.append(nim(420, 230, 1.15, "joy"))
    o.append(sparkle(540, 150, 6, WHITE) + sparkle(300, 120, 5, WHITE))
    return defs, "".join(o)


def c3p09():
    defs, bg = sky(SKY_EVENING)
    fill, shade = MAMA_SOFT
    o = [bg, far_peaks(640, shade=1)]
    o.append(mama(400, 250, 1.55, "hug", colors=MAMA_SOFT))
    o.append(nim(400, 398, 1.05, "warm"))
    # los "brazos" esponjosos de Mamá rodeando a Nimbus
    for side in (-1, 1):
        o.append(circle(400 + side * 104, 402, 36, shade) + circle(400 + side * 100, 396, 34, fill))
        o.append(circle(400 + side * 76, 430, 26, shade) + circle(400 + side * 74, 425, 24, fill))
    for hx, hy, hs in [(120, 190, 1.1), (690, 160, 1.3), (690, 330, 0.8), (110, 340, 0.8)]:
        o.append(heart(hx, hy, hs, "#F7A8BC", 0.9))
    return defs, "".join(o)


def c3p10():
    defs, bg = sky(SKY_BRIGHT)
    rng = random.Random(310)
    o = [bg, sun(110, 90, 30), mountain(620, 430, 360, 150, "#D8D2EC", snow="#FBFAFE"), mountain(760, 430, 260, 110, "#E0DBF0")]
    o.append(path("M0 420 Q400 380 800 430 L800 600 L0 600 Z", fill="#D9EADF"))
    o.append(path("M0 480 Q400 450 800 480 L800 600 L0 600 Z", fill="#CBE6D6"))
    o.append(cottage(610, 486, 1.0) + round_tree(720, 488, 0.9))
    o.append(ellipse(300, 540, 220, 34, "#D2B79C"))
    for fx, fy, c in [(140, 540, "#F7B7C3"), (200, 560, "#FFD9CC"), (260, 535, "#E4DCF7"), (320, 560, "#F7B7C3")]:
        o.append(flower(fx, fy, 1.3, c, "#FFE38A", 38))
    for fx, fy, c in [(380, 540, "#FFD9CC"), (440, 560, "#E4DCF7"), (490, 538, "#F7B7C3")]:
        o.append(flower(fx, fy, 1.3, DRY_FLOWER[c], "#E8D6A0", 38, droopy=True))
    o.append(rain_field(rng, 130, 340, 270, 510, 22, "#A3CDF0", 0.8))
    o.append(nim(240, 200, 1.1, "joy", rain=True))
    o.append(bee(560, 380, 1.1, flip=True))
    o.append(path("M520 392 q-20 -16 -40 0 q-20 16 -40 0", stroke="#D9CFA0", sw=2, extra=' stroke-dasharray="3 6"'))
    return defs, "".join(o)


def c3p11():
    defs, bg = sky(SKY_NIGHT)
    rng = random.Random(311)
    o = [bg, starfield(rng, 26, 40, 760, 40, 300, avoid=[(640, 110, 90)]), moon(640, 110, 40)]
    o.append(mountain(160, 560, 420, 230, "#A99DD3", snow="#EFEAF8") + mountain(520, 560, 460, 270, "#9E92CB", snow="#EFEAF8")
             + mountain(760, 560, 300, 170, "#B0A5D8"))
    o.append(path("M0 520 Q400 480 800 520 L800 600 L0 600 Z", fill="#9D97C6"))
    o.append(house(560, 560, 0.35).replace("#D2E7F7", "#FFE9A8"))
    o.append(mama(320, 330, 1.15, "sleep", colors=MAMA_SOFT))
    o.append(nim(500, 360, 0.9, "sleep"))
    o.append(sparkle(470, 280, 6, "#FFF6C8") + sparkle(250, 250, 5, "#FFF6C8"))
    return defs, "".join(o)


SCENES = [
    (1, 1, "Nimbus the little cloud floats high in the blue sky above the mountains and the forest", c1p01),
    (1, 2, "Nimbus looks down at trees, a shiny river, fields of flowers and the smiling sun", c1p02),
    (1, 3, "Big dark clouds rain over the mountains, the forest and the fields while Nimbus watches", c1p03),
    (1, 4, "Nimbus asks Mama Cumulus if he can make rain too", c1p04),
    (1, 5, "Mama Cumulus smiles kindly and tells Nimbus to try", c1p05),
    (1, 6, "Nimbus squeezes and puffs up his cheeks, but not a single raindrop falls", c1p06),
    (1, 7, "Nimbus feels small and sad, alone in the big grey sky", c1p07),
    (1, 8, "Mama Cumulus comforts Nimbus: everyone has their own way to help", c1p08),
    (1, 9, "The gentle Wind arrives and invites Nimbus to see the world", c1p09),
    (1, 10, "Nimbus floats away on the wind over the forest and the river", c1p10),
    (2, 1, "The Wind carries Nimbus over a snowy mountain, a blue lake and a rocky valley", c2p01),
    (2, 2, "Nimbus spots a tiny garden next to a little yellow house", c2p02),
    (2, 3, "A thirsty garden with cracked soil, brown grass, a dry tree and a droopy daisy", c2p03),
    (2, 4, "Nimbus calls down to the droopy daisy", c2p04),
    (2, 5, "The daisy sighs under the hot sun while the big clouds stay far away", c2p05),
    (2, 6, "Nimbus remembers feeling too small next to the big clouds", c2p06),
    (2, 7, "Nimbus floats down kindly to stay with the daisy", c2p07),
    (2, 8, "Nimbus makes a cool shadow over the garden and the daisy lifts her head", c2p08),
    (2, 9, "The daisy thanks Nimbus in the cool shade", c2p09),
    (2, 10, "Nimbus feels a warm, happy glow inside", c2p10),
    (3, 1, "Nimbus tells the daisy about mountains and lakes; she tells him about seeds, roots and bees", c3p01),
    (3, 2, "Nimbus feels so happy that he is full and tingly", c3p02),
    (3, 3, "A single raindrop lands on the daisy's petal", c3p03),
    (3, 4, "Nimbus gasps in surprise as a raindrop falls from him", c3p04),
    (3, 5, "Gentle rain falls, the soil drinks, the grass turns green and the tree gets new leaves", c3p05),
    (3, 6, "The daisy cheers in the rain: Nimbus made rain", c3p06),
    (3, 7, "The sun peeks out and a rainbow appears over the green garden", c3p07),
    (3, 8, "In the evening the Wind carries a proud Nimbus home over the mountains", c3p08),
    (3, 9, "Mama Cumulus gives Nimbus a big, fluffy hug", c3p09),
    (3, 10, "Nimbus rains on another thirsty garden while a bee buzzes by", c3p10),
    (3, 11, "Nimbus and Mama Cumulus sleep under the moon above the mountains", c3p11),
]


def main():
    for chapter, para, title, fn in SCENES:
        mi._P = f"nimbus-ch{chapter}-p{para:02d}"
        defs, body = fn()
        out, size = mi.write_svg("nimbus", f"ch{chapter}/p{para:02d}", 800, 600, title, defs, body)
        print(f"{os.path.relpath(out, mi.ROOT)}  {size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
