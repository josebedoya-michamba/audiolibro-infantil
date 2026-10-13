#!/usr/bin/env python3
"""Escenas por párrafo de "Benny's Fruit Garden" (una ilustración por párrafo).

Reutiliza los personajes y ayudantes de make_illustrations.py (sin modificarlo)
y escribe images/benny/ch<N>/p<NN>.svg. Uso:

    python3 tools/scenes_benny.py            # las 28 escenas
    python3 tools/scenes_benny.py ch2        # solo un capítulo
    python3 tools/scenes_benny.py ch3/p05    # una escena
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_illustrations as mi  # noqa: E402
from make_illustrations import (  # noqa: E402
    BLUSH, LEAF, PLUM, STEM, WHITE, apple, banana, basket, blush, bowl, calm_eye, cherries, circle, cloud,
    cloud_layer, drop, ellipse, eye, frown, g, grapes, happy_eye, leaf, lemon, lemon_sapling, lin, milo, milo_paws,
    moon, op, open_mouth, orange, path, pear, pitcher, rect, rotated, round_tree, seed_bag, smile, soil_row, sparkle,
    sprout, strawberry, strawberry_plant, sun, tilly, tuft, url, watering_can, watermelon_slice, blueberries,
)

BUN, BUN_D, BUN_L, BUN_PINK, NOSE = mi.BUN, mi.BUN_D, mi.BUN_L, mi.BUN_PINK, mi.NOSE
GRANNY = mi.GRANNY
MOUSE, MOUSE_D, MOUSE_L = mi.MOUSE, mi.MOUSE_D, mi.MOUSE_L
CROW, CROW_D, BEAK = mi.CROW, mi.CROW_D, mi.BEAK

GREEN_APPLE = "#B8DD8C"
SEED = "#B98B6B"


# ------------------------------------------------------------------ cámara

def cam(body, cx=400, cy=300, z=1.0):
    """Acerca la cámara al punto (cx, cy) sin dejar bordes vacíos."""
    if z == 1:
        return body
    hw, hh = 400 / z, 300 / z
    cx = min(max(cx, hw), 800 - hw)
    cy = min(max(cy, hh), 600 - hh)
    t = f"translate(400 300) scale({mi.n(float(z))}) translate({mi.n(float(-cx))} {mi.n(float(-cy))})"
    return f'<g transform="{t}">{body}</g>'


# ------------------------------------------------------------------- Benny

def bun(x, y, s=1.0, flip=False, pose="stand", expr="happy", ears="up", holding="", look=(0, 0),
        pal=None, mid="", face_extra=""):
    """Benny con más poses y expresiones que make_illustrations.benny (misma forma)."""
    B, BD, BL = pal or (BUN, BUN_D, BUN_L)
    o = []
    if ears in ("up", "perk"):
        o.append(g(ellipse(0, -40, 14, 44, B) + ellipse(0, -38, 7, 32, BUN_PINK), -20, -150, rot=-10))
        if ears == "perk":
            o.append(g(ellipse(0, -40, 14, 44, B) + ellipse(0, -38, 7, 32, BUN_PINK), 20, -150, rot=10))
        else:
            o.append(path("M8 -148 C12 -200 66 -204 84 -154 C88 -141 77 -131 69 -141 C58 -170 34 -174 26 -146 Z", fill=B))
            o.append(path("M17 -153 C22 -186 60 -190 74 -156 C63 -170 38 -172 27 -151 Z", fill=BUN_PINK))
    o.append(ellipse(0, -50, 40, 48, B))
    o.append(ellipse(0, -44, 26, 33, BL))
    if pose == "hop":
        o.append(ellipse(-24, -8, 20, 9, BL, rot=-18) + ellipse(24, -8, 20, 9, BL, rot=18))
    elif pose == "stomp":
        o.append(ellipse(-22, -7, 21, 10, BL) + ellipse(28, -18, 20, 9, BL, rot=-28))
    elif pose == "sit":
        o.append(ellipse(-26, -8, 24, 11, BL) + ellipse(26, -8, 24, 11, BL))
        o.append(ellipse(-30, -7, 7, 4, BUN_PINK, extra=op(0.8)) + ellipse(30, -7, 7, 4, BUN_PINK, extra=op(0.8)))
    else:
        o.append(ellipse(-22, -7, 21, 10, BL) + ellipse(22, -7, 21, 10, BL))
        o.append(ellipse(-24, -6, 6, 3.5, BUN_PINK, extra=op(0.8)) + ellipse(24, -6, 6, 3.5, BUN_PINK, extra=op(0.8)))

    arms = []

    def paw(px, py):
        return circle(px, py, 8.5, BL)

    def arm(d):
        return path(d, stroke=BD, sw=15)

    def side(sx):
        return ellipse(sx * 34, -56, 10, 19, BD, rot=-sx * 15)

    def up(sx):
        return arm(f"M{sx * 30} -76 Q{sx * 48} -86 {sx * 54} -108") + paw(sx * 55, -111)

    if pose == "hold":
        arms.append(holding)
        for sx in (-1, 1):
            arms.append(arm(f"M{sx * 32} -78 Q{sx * 32} -60 {sx * 14} -60") + paw(sx * 13, -60))
    elif pose == "eat":
        arms.append(holding)
        for sx in (-1, 1):
            arms.append(arm(f"M{sx * 32} -78 Q{sx * 34} -66 {sx * 15} -76") + paw(sx * 14, -77))
    elif pose in ("hop", "cheer"):
        arms.append(up(-1) + up(1))
    elif pose == "wave":
        arms.append(side(-1) + up(1))
    elif pose == "plant":
        arms.append(side(-1))
        arms.append(arm("M30 -74 Q56 -62 62 -36") + paw(62, -32))
        arms.append(ellipse(66, -14, 3.6, 5, SEED) + ellipse(60, 0, 3.6, 5, SEED, rot=30))
    elif pose == "chin":
        for sx in (-1, 1):
            arms.append(arm(f"M{sx * 32} -76 Q{sx * 36} -66 {sx * 15} -84") + paw(sx * 14, -86))
    elif pose == "think":
        arms.append(side(-1))
        arms.append(arm("M30 -76 Q40 -62 17 -84") + paw(15, -86))
    elif pose == "cross":
        arms.append(arm("M-32 -74 Q-12 -54 20 -64") + paw(21, -64))
        arms.append(arm("M32 -74 Q12 -56 -20 -66") + paw(-21, -66))
    elif pose == "reach":
        arms.append(side(-1))
        arms.append(arm("M30 -76 Q50 -78 66 -72") + paw(68, -72))
        arms.append(holding)
    elif pose == "hug":
        for sx in (-1, 1):
            arms.append(arm(f"M{sx * 30} -76 Q{sx * 52} -80 {sx * 66} -94") + paw(sx * 68, -96))
    elif pose == "stomp":
        for sx in (-1, 1):
            arms.append(arm(f"M{sx * 32} -76 L{sx * 42} -44") + paw(sx * 43, -41))
    else:
        arms.append(side(-1) + side(1))

    if pose in ("hold", "eat", "reach"):
        o.append(mid + "".join(arms))
    else:
        o.append("".join(arms) + mid)
    o.append(circle(0, -116, 44, B))
    if ears == "droop":
        for sx in (-1, 1):
            o.append(g(ellipse(0, 0, 13, 42, B) + ellipse(0, 2, 6.5, 30, BUN_PINK), sx * 47, -116, rot=sx * 18))
    o.append(circle(-14, -100, 15, BL) + circle(14, -100, 15, BL))

    bunny_mouth = (rect(-3.5, -98.5, 7, 6, WHITE, rx=1.5)
                   + path("M0 -103 L0 -99 M-7 -97 Q-3.5 -94 0 -99 Q3.5 -94 7 -97", stroke=PLUM, sw=2.4))
    face = []
    if expr == "joy":
        face.append(happy_eye(-17, -124, 13, 3.2) + happy_eye(17, -124, 13, 3.2) + open_mouth(0, -99, 13))
    elif expr in ("dreamy", "proud"):
        face.append(happy_eye(-17, -124, 13, 3.2) + happy_eye(17, -124, 13, 3.2) + bunny_mouth)
    elif expr == "surprised":
        face.append(eye(-17, -126, 7.4, look) + eye(17, -126, 7.4, look))
        for sx in (-1, 1):
            face.append(path(f"M{sx * 17 - 8} -144 Q{sx * 17} -150 {sx * 17 + 8} -144", stroke=PLUM, sw=2.6))
        face.append(ellipse(0, -93, 5.5, 7, PLUM) + ellipse(0, -90, 3, 2.4, "#F49AB0"))
    elif expr == "eager":
        face.append(eye(-17, -126, 7, look) + eye(17, -126, 7, look))
        face.append(open_mouth(0, -99, 13))
    elif expr == "grumpy":
        face.append(eye(-17, -123, 5.8, look) + eye(17, -123, 5.8, look))
        for sx in (-1, 1):
            face.append(path(f"M{sx * 28} -140 L{sx * 9} -133", stroke=PLUM, sw=3.4))
        face.append(frown(0, -94, 13, 2.8))
    elif expr == "sad":
        face.append(eye(-17, -123, 6, (0, 2)) + eye(17, -123, 6, (0, 2)))
        for sx in (-1, 1):
            face.append(path(f"M{sx * 26} -133 L{sx * 10} -139", stroke=PLUM, sw=2.6))
        face.append(frown(0, -94, 11, 2.6))
    elif expr == "think":
        face.append(eye(-17, -126, 6.2, (3, -3)) + eye(17, -126, 6.2, (3, -3)))
        face.append(path("M9 -144 Q17 -151 25 -144", stroke=PLUM, sw=2.6))
        face.append(path("M-5 -95 Q0 -93 6 -97", stroke=PLUM, sw=2.4))
    elif expr == "bored":
        for sx in (-1, 1):
            ex = sx * 17
            face.append(eye(ex, -123, 6.2, (0, 1)))
            face.append(path(f"M{ex - 9} -124 L{ex + 9} -124 L{ex + 9} -135 L{ex - 9} -135 Z", fill=B))
            face.append(path(f"M{ex - 8} -124 L{ex + 8} -124", stroke=PLUM, sw=2.6))
        face.append(path("M-6 -95 L6 -95", stroke=PLUM, sw=2.4))
    elif expr == "sleep":
        face.append(calm_eye(-17, -122, 13, 3) + calm_eye(17, -122, 13, 3))
        face.append(smile(0, -96, 9, 2.4))
    elif expr == "smile":
        face.append(eye(-17, -125, 6.2, look) + eye(17, -125, 6.2, look))
        face.append(smile(0, -97, 13, 2.8, 0.55))
    else:
        face.append(eye(-17, -125, 6.2, look) + eye(17, -125, 6.2, look) + bunny_mouth)
    o.append("".join(face))
    o.append(blush(-31, -104, 7, 4.5, 0.95 if expr in ("proud", "joy", "eager") else 0.75)
             + blush(31, -104, 7, 4.5, 0.95 if expr in ("proud", "joy", "eager") else 0.75))
    for sx in (-1, 1):
        o.append(path(f"M{sx * 27} -104 L{sx * 45} -108 M{sx * 27} -99 L{sx * 45} -97", stroke=PLUM, sw=1.4, extra=op(0.35)))
    o.append(ellipse(0, -107, 6, 4.4, NOSE))
    o.append(face_extra)
    return g("".join(o), x, y, s, flip=flip)


def granny(x, y, s=1.0, flip=False, pose="stand", expr="happy", holding="", look=(0, 0)):
    """La abuela Bunny (pelaje gris, chal lila y lentes) con poses y expresiones."""
    shawl = (path("M-44 -86 Q0 -64 44 -86 L36 -46 Q0 -30 -36 -46 Z", fill="#CDBDF0", stroke="#CDBDF0", sw=6)
             + path("M-30 -44 L-32 -36 M-18 -38 L-19 -30 M-6 -35 L-6 -27 M6 -35 L6 -27 M18 -38 L19 -30 M30 -44 L32 -36",
                    stroke="#B8A6E6", sw=3)
             + circle(0, -70, 6, "#F6B8A8"))
    glasses = (circle(-17, -125, 11, "none", f' stroke="{PLUM}" stroke-width="2.4"')
               + circle(17, -125, 11, "none", f' stroke="{PLUM}" stroke-width="2.4"')
               + path("M-6 -126 Q0 -130 6 -126", stroke=PLUM, sw=2.4))
    return bun(x, y, s, flip=flip, pose=pose, expr=expr, holding=holding, look=look, pal=GRANNY, mid=shawl,
               face_extra=glasses)


# ------------------------------------------------------- Milo y el cuervo

def milo_full(x, y, s=1.0):
    """Milo sentado con la panza llenita, ojos felices y patitas sobre la panza."""
    o = [path("M20 -8 C50 -4 58 -36 42 -42 C31 -46 29 -28 40 -29", stroke=MOUSE_D, sw=4)]
    o.append(ellipse(0, -26, 31, 28, MOUSE))
    o.append(ellipse(0, -24, 23, 21, MOUSE_L))
    o.append(ellipse(-6, -30, 6, 4, WHITE, rot=-30, extra=op(0.55)))
    o.append(ellipse(-16, -3, 10, 5, BUN_PINK) + ellipse(16, -3, 10, 5, BUN_PINK))
    o.append(circle(-16, -26, 6, MOUSE_D) + circle(16, -26, 6, MOUSE_D))
    for sx in (-1, 1):
        o.append(circle(sx * 21, -86, 15, MOUSE) + circle(sx * 21, -86, 9.5, BUN_PINK))
    o.append(circle(0, -66, 24, MOUSE))
    o.append(ellipse(0, -58, 12, 9, MOUSE_L))
    o.append(happy_eye(-9, -70, 9, 2.6) + happy_eye(9, -70, 9, 2.6))
    o.append(blush(-16, -59, 5, 3.2, 0.95) + blush(16, -59, 5, 3.2, 0.95))
    o.append(open_mouth(0, -54, 9))
    o.append(circle(0, -61, 3.6, NOSE))
    for sx in (-1, 1):
        o.append(path(f"M{sx * 10} -60 L{sx * 30} -64 M{sx * 10} -57 L{sx * 30} -55", stroke=PLUM, sw=1.2, extra=op(0.35)))
    return g("".join(o), x, y, s)


def milo_chew(x, y, s=1.0, flip=False, holding=""):
    """Milo masticando: cachete inflado."""
    base = milo(0, 0, 1.0, holding=holding)
    cheek = circle(15, -55, 8.5, MOUSE) + blush(17, -55, 5, 3.4, 0.9)
    munch = path("M34 -70 Q40 -66 36 -60 M40 -76 Q48 -70 43 -62", stroke=PLUM, sw=1.8, extra=op(0.4))
    return g(base + cheek + munch, x, y, s, flip=flip)


def crow_fly(x, y, s=1.0, flip=False):
    """Cuervo volando (alas arriba). Mira a la derecha."""
    o = [path("M-26 -4 L-54 4 L-48 -12 Z", fill=CROW_D, stroke=CROW_D, sw=6)]
    o.append(path("M-14 -12 Q-30 -54 -4 -66 Q-4 -40 8 -18 Z", fill=CROW_D, stroke=CROW_D, sw=4))
    o.append(ellipse(0, -6, 28, 18, CROW))
    o.append(path("M2 -14 Q12 -58 40 -60 Q28 -36 22 -12 Z", fill=CROW, stroke=CROW, sw=4))
    o.append(circle(26, -20, 15, CROW))
    o.append(path("M38 -23 L54 -18 L38 -12 Z", fill=BEAK, stroke=BEAK, sw=3))
    o.append(eye(29, -23, 3.8, (1, 0)))
    o.append(blush(30, -13, 4, 2.6, 0.8))
    return g("".join(o), x, y, s, flip=flip)


# ------------------------------------------------------------ utilidades

def heart(x, y, s=1.0, fill="#F7A9B8"):
    return g(path("M0 6 C-14 -4 -12 -16 -4 -16 C-1 -16 0 -13 0 -11 C0 -13 1 -16 4 -16 C12 -16 14 -4 0 6 Z", fill=fill), x, y, s)


def bubble(cx, cy, rx, ry, tail, content="", clip_id=None, fill=WHITE, shade="#E4DCF7"):
    """Globo de pensamiento con colita de burbujas hacia `tail` (x, y)."""
    o = []
    lobes = []
    k = 9
    for i in range(k):
        a = 2 * math.pi * i / k
        lobes.append((cx + rx * 0.82 * math.cos(a), cy + ry * 0.8 * math.sin(a), min(rx, ry) * 0.42))
    for lx, ly, lr in lobes:
        o.append(circle(lx, ly + 5, lr, shade))
    o.append(ellipse(cx, cy + 5, rx * 0.92, ry * 0.9, shade))
    for lx, ly, lr in lobes:
        o.append(circle(lx, ly, lr, fill))
    o.append(ellipse(cx, cy, rx * 0.92, ry * 0.9, fill))
    tx, ty = tail
    for t, r in [(0.55, 12), (0.75, 8), (0.92, 5)]:
        bx = cx + (tx - cx) * t
        by = cy + (ty - cy) * t
        o.append(circle(bx, by + 3, r, shade) + circle(bx, by, r, fill))
    if content:
        if clip_id:
            o.append(f'<g clip-path="url(#{mi.uid(clip_id)})">{content}</g>')
        else:
            o.append(content)
    return "".join(o)


def bubble_clip(clip_id, cx, cy, rx, ry):
    return f'<clipPath id="{mi.uid(clip_id)}"><ellipse cx="{mi.n(float(cx))}" cy="{mi.n(float(cy))}" rx="{mi.n(float(rx))}" ry="{mi.n(float(ry))}"/></clipPath>'


def motion(x, y, s=1.0, color="#FFFFFF", o=0.85):
    return g(path("M0 0 Q-10 10 -6 22 M14 -6 Q8 8 12 20 M-14 4 Q-22 14 -20 24", stroke=color, sw=3.2), x, y, s, opacity=o)


def puffs(x, y, s=1.0):
    return g(circle(0, 0, 9, "#EADFCC") + circle(-14, 4, 7, "#EADFCC") + circle(-26, 2, 5, "#EADFCC"), x, y, s, opacity=0.85)


def burst(x, y, r=40, color="#FFE38A"):
    o = []
    for i in range(10):
        a = math.radians(i * 36 - 90)
        r0, r1 = r * 0.55, r * (1.0 if i % 2 == 0 else 0.8)
        o.append(path(f"M{mi.n(x + r0 * math.cos(a))} {mi.n(y + r0 * math.sin(a))} L{mi.n(x + r1 * math.cos(a))} {mi.n(y + r1 * math.sin(a))}",
                      stroke=color, sw=4.5))
    return "".join(o)


def bulb(x, y, s=1.0):
    o = [circle(0, 0, 46, url("glow"), op(0.95))]
    o.append(burst(0, -2, 52, "#FFD86B"))
    o.append(circle(0, -4, 20, "#FFF1A8") + circle(0, -4, 20, "none", ' stroke="#F5C84C" stroke-width="3"'))
    o.append(path("M-6 6 Q-6 -8 0 -8 Q6 -8 6 6", stroke="#F5C84C", sw=2.4))
    o.append(rect(-10, 15, 20, 12, "#CFC8DA", rx=3) + path("M-10 20 L10 20", stroke="#B8B0C8", sw=2))
    o.append(ellipse(-7, -12, 4, 7, WHITE, rot=25, extra=op(0.7)))
    return g("".join(o), x, y, s)


def watermelon(x, y, s=1.0, rot=0):
    """Sandía entera rayada."""
    o = [ellipse(0, 0, 42, 30, "#8FD0A0")]
    for dx in (-24, -8, 8, 24):
        o.append(path(f"M{dx} -29 Q{dx + (6 if dx > 0 else -6)} 0 {dx} 29", stroke="#6CB884", sw=6))
    o.append(ellipse(-16, -14, 9, 5, WHITE, rot=-20, extra=op(0.35)))
    o.append(path("M38 -10 Q50 -18 46 -28", stroke=STEM, sw=3))
    return g("".join(o), x, y, s, rot=rot)


def tree(x, y, s=1.0, fruit="apple"):
    """Árbol frutal: apple, green, pear, cherry, lemon, orange."""
    canopy = [("c", 0, -176, 62), ("c", -50, -144, 46), ("c", 50, -144, 46), ("c", -28, -210, 44), ("c", 30, -208, 44)]
    o = [rect(-9, -130, 18, 130, "#D2B296", rx=6), path("M0 -96 L-26 -126 M0 -110 L22 -134", stroke="#D2B296", sw=8)]
    o.append(cloud_layer(canopy, "#9FD6B6", 8) + cloud_layer(canopy, "#B4E2C6"))
    spots = [(-60, -150), (-30, -186), (2, -214), (36, -184), (62, -146), (-8, -152), (24, -140), (-40, -216), (44, -222)]
    for fx, fy in spots:
        if fruit == "apple":
            o.append(apple(fx, fy, 0.62))
        elif fruit == "green":
            o.append(apple(fx, fy, 0.62, GREEN_APPLE))
        elif fruit == "pear":
            o.append(pear(fx, fy, 0.6))
        elif fruit == "cherry":
            o.append(cherries(fx, fy, 0.62))
        elif fruit == "orange":
            o.append(orange(fx, fy, 0.62))
        else:
            o.append(lemon(fx, fy, 0.55, rot=-20))
    return g("".join(o), x, y, s)


def melon_vine(x, y, s=1.0, melons=1):
    o = [path("M-80 0 Q-40 -20 0 -6 Q40 8 80 -10", stroke="#8CCB9B", sw=4)]
    for lx, rot in [(-60, -140), (-22, -40), (30, -130), (66, -50)]:
        o.append(leaf(lx, -6, 26, rot, "#9ED7AE", "#86C79A"))
    o.append(path("M-40 -12 q-6 -10 2 -14 M44 -4 q8 -8 0 -14", stroke="#8CCB9B", sw=2))
    o.append(watermelon(6, -22, 1.0))
    if melons > 1:
        o.append(watermelon(-56, -14, 0.65, -10))
    return g("".join(o), x, y, s)


def seed_pile(x, y, kind):
    o = []
    rng = random.Random(hash(kind) % 1000)
    if kind == "apple":
        for _ in range(7):
            o.append(ellipse(rng.uniform(-14, 14), rng.uniform(-6, 6), 3.4, 5.2, "#8E6A50", rot=rng.uniform(-40, 40)))
    elif kind == "cherry":
        for _ in range(5):
            o.append(circle(rng.uniform(-14, 14), rng.uniform(-6, 6), 5.6, "#EBD9BE"))
    elif kind == "melon":
        for _ in range(8):
            o.append(ellipse(rng.uniform(-15, 15), rng.uniform(-6, 6), 2.8, 4.8, PLUM, rot=rng.uniform(-60, 60), extra=op(0.85)))
    return g("".join(o), x, y)


def badge(x, y, content, r=34, fill="#FFFDF7"):
    return circle(x, y + 3, r, "#E6DCCB") + circle(x, y, r, fill) + content


def sun_path(cx, cy, positions):
    """Soles tenues a lo largo de un arco (el tiempo pasa)."""
    o = []
    for i, (px, py) in enumerate(positions):
        o.append(g(sun(0, 0, 18), px, py, opacity=0.35 + 0.65 * i / max(1, len(positions) - 1)))
    pts = " ".join(f"{mi.n(float(px))},{mi.n(float(py))}" for px, py in positions)
    o.insert(0, f'<polyline points="{pts}" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="2 10" opacity="0.8"/>')
    return "".join(o)


def crate(x, y, s=1.0):
    o = [rect(-36, -34, 72, 34, "#E5C9A5", rx=5), path("M-36 -17 L36 -17", stroke="#D1B18A", sw=3)]
    o.append(path("M-24 -34 L-24 0 M24 -34 L24 0", stroke="#D1B18A", sw=3))
    return g("".join(o), x, y, s)


def weed_pile(x, y, s=1.0):
    o = []
    for rot, L in [(-160, 24), (-120, 28), (-60, 26), (-20, 22), (-95, 30)]:
        o.append(leaf(0, -2, L, rot, "#C9D9A0", "#AFC487"))
    o.append(ellipse(0, 0, 20, 6, "#CDB394"))
    return g("".join(o), x, y, s)


def star_sky(rng, count, x0, x1, y0, y1, avoid=()):
    return mi.starfield(rng, count, x0, x1, y0, y1, avoid=avoid)


# --------------------------------------------------------------- fondos

SKIES = {
    "day": [(0, "#D6F1E5"), (0.7, "#F1FAF4"), (1, "#FFF8F0")],
    "morning": [(0, "#FFE4D4"), (0.55, "#F6F4EA"), (1, "#EAF7EF")],
    "golden": [(0, "#FFDDBE"), (0.55, "#FFEFC8"), (1, "#FFF8EA")],
    "dusk": [(0, "#B7AEDF"), (0.55, "#F2C8D2"), (1, "#FFE2C6")],
    "night": [(0, "#958DCB"), (0.6, "#BDB3E2"), (1, "#E2D6EF")],
}
HILLS = {
    "day": ("#D5F0E2", "#C2E8D4"),
    "morning": ("#D5F0E2", "#C2E8D4"),
    "golden": ("#D9EDCB", "#CBE6BC"),
    "dusk": ("#C9DDCB", "#BAD4BF"),
    "night": ("#AFC7C0", "#A0BCB4"),
}


def sky(time):
    return lin("sky", SKIES[time]), rect(0, 0, 800, 600, url("sky"))


def hills(time, back=True):
    h1, h2 = HILLS[time]
    o = []
    if back:
        o.append(path("M0 360 Q200 320 420 350 Q620 378 800 335 L800 600 L0 600 Z", fill=h1))
    o.append(path("M0 410 Q400 380 800 410 L800 600 L0 600 Z", fill=h2))
    return "".join(o)


def garden_rows(stage, front=True):
    """Hileras de tierra. stage: empty, planted, sprouts."""
    o = [soil_row(80, 720, 448, 22)]
    if stage == "sprouts":
        for sx in range(150, 640, 62):
            o.append(sprout(sx, 438, 0.9))
    o.append(soil_row(40, 760, 500, 26))
    if stage == "planted":
        for sx in range(110, 720, 70):
            o.append(ellipse(sx, 487, 12, 5, "#C9AB8C"))
        for sx in range(150, 680, 76):
            o.append(ellipse(sx, 437, 10, 4, "#C9AB8C"))
    elif stage == "sprouts":
        for i, sx in enumerate(range(110, 720, 70)):
            if i % 2 == 0:
                o.append(strawberry_plant(sx, 492, 0.85, flowers=True, berries=False))
            else:
                o.append(sprout(sx, 488, 1.1))
    if front:
        o.append(soil_row(0, 800, 572, 32))
    return "".join(o)


def day_backdrop(time="day", sun_at=(110, 100), trees=True):
    o = []
    o.append(sun(*sun_at, 36))
    o.append(cloud(560, 110, 0.9) + cloud(320, 70, 0.6, o=0.85))
    if trees:
        o.append(round_tree(470, 352, 0.8) + round_tree(720, 346, 1.0) + round_tree(770, 344, 0.75))
    return "".join(o)


# ============================================================ capítulo 1

def ch1_p01():
    """Benny sueña con un jardín lleno de fruta."""
    defs, bg = sky("day")
    o = [bg, day_backdrop()]
    o.append(hills("day"))
    o.append(bun(250, 540, 1.25, pose="chin", expr="dreamy"))
    cx, cy, rx, ry = 560, 205, 190, 140
    defs += bubble_clip("dream", cx, cy, rx * 0.95, ry * 0.92)
    dream = (rect(cx - rx, cy - ry, rx * 2, ry * 2, "#EAF8EF")
             + path(f"M{cx - rx} {cy + 30} Q{cx} {cy} {cx + rx} {cy + 26} L{cx + rx} {cy + ry} L{cx - rx} {cy + ry} Z", fill="#CDEBD7")
             + tree(cx - 100, cy + 62, 0.48, "apple") + tree(cx + 96, cy + 62, 0.46, "lemon")
             + tree(cx, cy + 50, 0.4, "cherry")
             + melon_vine(cx + 14, cy + 96, 0.62)
             + strawberry_plant(cx - 64, cy + 100, 1.0) + strawberry_plant(cx + 104, cy + 102, 0.9)
             + sparkle(cx - 130, cy - 70, 10, "#FFE38A") + sparkle(cx + 130, cy - 76, 8, "#FFE38A"))
    o.append(bubble(cx, cy, rx, ry, (318, 380), dream, "dream"))
    o.append(sparkle(330, 330, 9, WHITE) + sparkle(372, 290, 6, WHITE))
    o.append(tuft(60, 560, 1.3, "#9FD6BF") + tuft(740, 570, 1.3, "#9FD6BF"))
    return defs, "".join(o)


def ch1_p02():
    """La abuela Bunny le da la bolsita de semillas."""
    defs, bg = sky("day")
    o = [bg, day_backdrop(trees=False)]
    o.append(round_tree(90, 350, 1.0) + round_tree(150, 346, 0.7))
    o.append(hills("day"))
    o.append(garden_rows("empty", front=False))
    o.append(granny(290, 560, 1.3, pose="reach", holding=seed_bag(84, -44, 1.25), look=(3, 0)))
    o.append(bun(520, 560, 1.3, pose="cheer", expr="eager", ears="perk", look=(-3, 2)))
    for sx, sy, r in [(410, 380, 11), (440, 340, 7), (372, 352, 6), (452, 410, 6)]:
        o.append(sparkle(sx, sy, r, "#FFE38A"))
    o.append(soil_row(0, 800, 600, 30))
    body = cam("".join(o), 420, 380, 1.12)
    return defs, body


def ch1_p03():
    """Primer plano: lo que hay dentro de la bolsita."""
    defs, bg = sky("day")
    defs += (f'<pattern id="{mi.uid("cloth")}" width="44" height="44" patternUnits="userSpaceOnUse">'
             f'<rect width="44" height="44" fill="#FFF7EE"/><rect width="22" height="44" fill="#D4EEDF" opacity="0.55"/>'
             f'<rect width="44" height="22" fill="#D4EEDF" opacity="0.55"/></pattern>')
    o = [bg, cloud(150, 90, 0.8), cloud(690, 70, 0.6, o=0.9)]
    o.append(round_tree(90, 300, 1.0) + round_tree(720, 296, 0.9))
    o.append(path("M0 270 Q400 240 800 266 L800 600 L0 600 Z", fill="#C2E8D4"))
    o.append(bun(420, 400, 1.25, expr="surprised", ears="perk", look=(0, 3)))
    o.append(path("M0 300 L800 286 L800 600 L0 600 Z", fill=url("cloth")))
    o.append(circle(372, 300, 13, BUN_L) + circle(468, 298, 13, BUN_L))
    o.append(g(seed_bag(0, 0, 1.0), 110, 590, 2.4))
    items = [(250, "apple", apple(0, 0, 1.25)), (360, "cherry", cherries(0, 2, 1.3)), (470, "melon", watermelon_slice(0, -8, 1.15))]
    for x, kind, fruit in items:
        o.append(badge(x, 380, g(fruit, x, 380), 36))
        o.append(g(seed_pile(0, 0, kind), x, 456, 1.7))
    o.append(badge(590, 380, g(strawberry(0, 0, 1.0), 590, 380, 1.7), 36))
    o.append(g(strawberry_plant(0, 0, 1.0, berries=False), 590, 500, 1.4))
    o.append(badge(700, 380, g(lemon(0, 0, 1.0), 700, 382, 1.15), 36))
    o.append(g(rect(-34, -50, 68, 50, "#F4B4A2", rx=8) + rect(-40, -58, 80, 14, "#EFA592", rx=6)
               + lemon_sapling(0, -52, 0.8), 700, 590, 0.95))
    for sx, sy, r in [(300, 520, 8), (520, 540, 9), (420, 330, 7), (640, 300, 7)]:
        o.append(sparkle(sx, sy, r, "#FFE38A"))
    return defs, "".join(o)


def ch1_p04():
    """¡Hooray! Benny salta de alegría."""
    defs, bg = sky("day")
    o = [bg, day_backdrop()]
    o.append(hills("day"))
    o.append(garden_rows("empty", front=False))
    o.append(path("M320 560 Q400 548 480 560", stroke="#9FD6BF", sw=4))
    o.append(burst(400, 230, 190, "#FFFFFF"))
    o.append(bun(400, 520, 1.4, pose="hop", expr="joy", ears="perk"))
    o.append(seed_bag(520, 340, 0.9))
    for sx, sy, r, c in [(250, 230, 12, "#FFE38A"), (560, 220, 14, "#FFE38A"), (300, 140, 8, WHITE), (520, 130, 9, WHITE),
                         (220, 330, 7, "#F7B7C3"), (590, 320, 8, "#F7B7C3")]:
        o.append(sparkle(sx, sy, r, c))
    o.append(leaf(240, 400, 18, -40, "#B4E2C0", "#8CCB9B") + leaf(570, 390, 16, 210, "#B4E2C0", "#8CCB9B"))
    o.append(soil_row(0, 800, 600, 30))
    return defs, cam("".join(o), 400, 330, 1.1)


def ch1_p05():
    """Cava hoyitos, planta y riega con la regadera azul."""
    defs, bg = sky("day")
    o = [bg, day_backdrop()]
    o.append(hills("day"))
    o.append(soil_row(80, 720, 448, 22))
    for sx in range(150, 680, 76):
        o.append(ellipse(sx, 437, 10, 4, "#C9AB8C"))
    o.append(soil_row(40, 760, 500, 26))
    for sx in range(110, 720, 70):
        o.append(ellipse(sx, 487, 12, 5, "#C9AB8C"))
    o.append(lemon_sapling(150, 494, 0.85))
    can = g(watering_can(0, 0, 1.0), 104, -38, 0.9, rot=18)
    o.append(bun(330, 552, 1.1, pose="reach", expr="smile", holding=can, look=(3, 2)))
    o.append(soil_row(0, 800, 572, 32))
    for dx, dy in [(482, 494), (494, 512), (474, 522), (502, 532), (486, 544)]:
        o.append(drop(dx, dy, 0.7, "#9CCBEF"))
    for sx, sy in [(240, 548), (262, 556), (420, 552)]:
        o.append(ellipse(sx, sy, 3.6, 5, SEED))
    o.append(tuft(30, 600, 1.2, "#9FD6BF") + tuft(790, 598, 1.2, "#9FD6BF"))
    return defs, "".join(o)


def ch1_p06():
    """Benny se sienta a esperar... y esperar."""
    defs, bg = sky("day")
    o = [bg]
    o.append(sun_path(400, 200, [(120, 210), (230, 120), (370, 80), (510, 100), (640, 170)]))
    o.append(cloud(700, 90, 0.7, o=0.85))
    o.append(round_tree(720, 346, 1.0) + round_tree(770, 344, 0.75))
    o.append(hills("day"))
    o.append(garden_rows("planted", front=False))
    o.append(lemon_sapling(150, 494, 0.85))
    o.append(crate(400, 560, 1.3))
    o.append(bun(400, 520, 1.15, pose="chin", expr="bored", ears="up"))
    o.append(soil_row(0, 800, 600, 30))
    o.append(watering_can(560, 590, 0.9))
    return defs, "".join(o)


def ch1_p07():
    """Tilly pasa caminando muy despacio."""
    defs, bg = sky("day")
    o = [bg, day_backdrop()]
    o.append(hills("day"))
    o.append(garden_rows("planted", front=False))
    o.append(lemon_sapling(522, 494, 0.85))
    o.append(crate(200, 568, 1.1))
    o.append(bun(200, 534, 0.95, pose="stand", expr="happy", look=(4, 0)))
    o.append(soil_row(0, 800, 590, 26))
    o.append(tilly(560, 572, 0.95, flip=True, expr="open"))
    o.append(puffs(686, 566, 0.7))
    for fx in (700, 726, 752, 778):
        o.append(ellipse(fx, 586, 6, 3.5, "#C9AB8C"))
    return defs, "".join(o)


def ch1_p08():
    """'¡Estarán listas en un minuto!' Benny piensa en manzanas y frutillas."""
    defs, bg = sky("day")
    o = [bg, day_backdrop()]
    o.append(hills("day"))
    o.append(garden_rows("planted", front=False))
    o.append(bun(300, 560, 1.4, pose="cheer", expr="eager", ears="perk", look=(2, -2)))
    o.append(tilly(630, 562, 0.9, flip=True, expr="open"))
    cx, cy, rx, ry = 520, 170, 140, 100
    o.append(bubble(cx, cy, rx, ry, (380, 300), apple(cx - 48, cy, 2.6) + strawberry(cx + 58, cy + 4, 2.7)
                    + sparkle(cx + 4, cy - 50, 9, "#FFE38A")))
    o.append(soil_row(0, 800, 600, 30))
    return defs, cam("".join(o), 430, 300, 1.08)


def ch1_p09():
    """Primer plano: la sonrisa lenta y sabia de Tilly. Lo bueno toma tiempo."""
    defs, bg = sky("day")
    o = [bg, day_backdrop(trees=False, sun_at=(680, 110))]
    o.append(round_tree(80, 352, 0.9))
    o.append(hills("day"))
    o.append(garden_rows("planted", front=False))
    o.append(tilly(380, 560, 2.0, flip=True, expr="calm"))
    # globo: semilla -> brote -> árbol con fruta
    cx, cy, rx, ry = 470, 150, 180, 84
    stages = (ellipse(cx - 120, cy + 30, 8, 11, SEED)
              + path(f"M{cx - 92} {cy + 20} l18 0 m-6 -6 l6 6 l-6 6", stroke="#C9B8E8", sw=3)
              + sprout(cx - 30, cy + 40, 1.6)
              + path(f"M{cx + 2} {cy + 20} l18 0 m-6 -6 l6 6 l-6 6", stroke="#C9B8E8", sw=3)
              + tree(cx + 100, cy + 72, 0.42, "apple"))
    defs += bubble_clip("time", cx, cy, rx * 0.95, ry * 0.92)
    o.append(bubble(cx, cy, rx, ry, (300, 330), stages, "time"))
    o.append(sparkle(250, 300, 8, "#FFE38A") + sparkle(170, 360, 6, WHITE))
    return defs, cam("".join(o), 360, 310, 1.12)


def ch1_p10():
    """A Benny se le caen las orejas: ¿semanas? ¿meses?"""
    defs, bg = sky("day")
    o = [bg]
    o.append(cloud(170, 120, 0.9, fill="#F4F2FA") + cloud(600, 90, 0.75, fill="#F4F2FA"))
    o.append(round_tree(720, 346, 1.0) + round_tree(770, 344, 0.75))
    o.append(hills("day"))
    o.append(garden_rows("planted", front=False))
    o.append(bun(400, 560, 1.55, pose="stand", expr="sad", ears="droop"))
    o.append(g(cloud(0, 0, 0.55, fill="#EEF0F6", shade="#DAD6E8"), 560, 250))
    o.append(drop(540, 290, 0.6, "#B9D6EE") + drop(570, 300, 0.5, "#B9D6EE"))
    o.append(soil_row(0, 800, 600, 30))
    return defs, cam("".join(o), 400, 330, 1.15)


# ============================================================ capítulo 2

def ch2_bg(stage, time="day", sun_at=(680, 95)):
    defs, bg = sky(time)
    o = [bg, sun(*sun_at, 38)]
    o.append(cloud(170, 100, 0.85) + cloud(450, 70, 0.6, o=0.85))
    o.append(round_tree(60, 344, 1.0) + round_tree(110, 340, 0.75) + round_tree(520, 358, 0.8))
    o.append(hills(time))
    o.append(garden_rows(stage, front=False))
    return defs, o


def ch2_p01():
    """A la mañana siguiente: ni manzanas ni frutillas, solo tierra café."""
    defs, o = ch2_bg("planted", "morning", sun_at=(690, 250))
    o.append(lemon_sapling(700, 444, 1.0))
    o.append(soil_row(0, 800, 572, 32))
    o.append(bun(360, 560, 1.25, pose="stand", expr="surprised", ears="perk", look=(0, 3)))
    o.append(motion(250, 420, 1.2, WHITE) + motion(232, 470, 0.9, WHITE))
    return defs, "".join(o)


def ch2_p02():
    """Milo asoma bajo una hoja comiendo arándanos; Benny está gruñón."""
    defs, o = ch2_bg("planted")
    o.append(soil_row(0, 800, 572, 32))
    o.append(bun(250, 560, 1.3, pose="cross", expr="grumpy", look=(4, 0)))
    o.append(leaf(660, 585, 150, -72, "#B4E2C0", "#8CCB9B"))
    o.append(milo_chew(590, 548, 1.2, holding=blueberries(0, -32, 0.8)))
    o.append(leaf(470, 606, 240, -8, "#9ED7AE", "#86C79A"))
    o.append(blueberries(552, 500, 1.15))
    o.append(blueberries(690, 560, 1.2) + blueberries(720, 575, 0.9))
    o.append(path("M150 260 Q140 236 160 228 M176 250 Q172 226 192 222", stroke="#B9B0CC", sw=3.5, extra=op(0.7)))
    return defs, cam("".join(o), 430, 420, 1.25)


def ch2_p03():
    """'¡Quiero una manzana roja grande ya!' Benny pisotea."""
    defs, o = ch2_bg("planted")
    o.append(soil_row(0, 800, 572, 32))
    o.append(bun(340, 560, 1.5, pose="stomp", expr="grumpy"))
    for sx in (250, 430):
        o.append(path(f"M{sx - 20} 572 L{sx - 34} 582 M{sx} 566 L{sx} 580 M{sx + 20} 572 L{sx + 34} 582", stroke="#C9AB8C", sw=3.5))
    cx, cy, rx, ry = 570, 180, 130, 110
    o.append(bubble(cx, cy, rx, ry, (420, 330), apple(cx, cy + 6, 4.0) + sparkle(cx + 66, cy - 56, 9, "#FFE38A")))
    o.append(path("M200 300 q-10 -20 6 -30 M226 288 q-4 -22 14 -28", stroke="#E9A8A8", sw=3.4))
    return defs, cam("".join(o), 430, 320, 1.12)


def ch2_p04():
    """Milo le ofrece un arándano a Benny."""
    defs, o = ch2_bg("planted")
    o.append(soil_row(0, 800, 572, 32))
    o.append(leaf(640, 590, 130, -80, "#B4E2C0", "#8CCB9B"))
    o.append(bun(300, 572, 1.4, pose="stand", expr="smile", look=(4, 3)))
    o.append(milo(500, 580, 1.4, expr="happy", holding=blueberries(0, -26, 1.1)))
    o.append(blueberries(580, 590, 1.1))
    o.append(sparkle(470, 440, 9, "#FFE38A") + sparkle(530, 420, 6, WHITE))
    return defs, cam("".join(o), 400, 440, 1.3)


def ch2_p05():
    """Benny riega, saca malezas y espanta a los cuervos."""
    defs, o = ch2_bg("planted", sun_at=(560, 80))
    o.append(soil_row(0, 800, 572, 32))
    o.append(weed_pile(120, 584, 1.4))
    o.append(bun(300, 565, 1.05, pose="wave", expr="smile", look=(4, -2)))
    o.append(g(watering_can(0, 0, 1.0, pour=True), 210, 560, 0.95, rot=-14))
    o.append(crow_fly(560, 210, 1.1) + crow_fly(680, 150, 0.8))
    o.append(path("M470 240 Q500 230 520 238 M480 262 Q510 256 528 262", stroke=WHITE, sw=3.5, extra=op(0.8)))
    for sx in range(420, 760, 70):
        o.append(path(f"M{sx} 546 Q{sx + 6} 534 {sx + 2} 524", stroke="#9FD6BF", sw=3))
    o.append(drop(242, 548, 0.55) + drop(256, 560, 0.5))
    return defs, "".join(o)


def ch2_p06():
    """Brotes, florcitas blancas en las frutillas y un limoncito verde."""
    defs, o = ch2_bg("sprouts")
    o.append(bun(300, 445, 0.7, pose="stand", expr="surprised", ears="perk", look=(3, 2)))
    o.append(soil_row(0, 800, 600, 50))
    for i, sx in enumerate([90, 230, 380]):
        o.append(strawberry_plant(sx, 584, 1.7, flowers=True, berries=False))
    o.append(lemon_sapling(620, 590, 2.2, bump=True))
    o.append(circle(650, 462, 30, "none", ' stroke="#FFFFFF" stroke-width="4" stroke-dasharray="4 8"'))
    for sx, sy, r in [(690, 420, 10), (604, 430, 7), (120, 470, 8), (260, 476, 6), (400, 470, 7)]:
        o.append(sparkle(sx, sy, r, "#FFE38A"))
    return defs, cam("".join(o), 420, 400, 1.12)


def ch2_p07():
    """'¿Es un limón?' Benny salta en círculos."""
    defs, o = ch2_bg("sprouts")
    o.append(lemon_sapling(640, 470, 1.4, bump=True))
    o.append(sparkle(676, 360, 9, "#FFE38A"))
    o.append(ellipse(340, 556, 120, 22, "none", extra=' stroke="#FFFFFF" stroke-width="4" stroke-dasharray="6 12" opacity="0.9"'))
    o.append(path("M220 540 Q200 500 236 470 M460 540 Q480 500 444 470", stroke=WHITE, sw=4, extra=op(0.8)))
    o.append(bun(340, 520, 1.15, pose="hop", expr="joy", ears="perk"))
    o.append(soil_row(0, 800, 600, 32))
    for sx in range(60, 780, 80):
        o.append(sprout(sx, 584, 1.3))
    return defs, "".join(o)


def ch2_p08():
    """Tilly asiente: esperar es difícil, pero con las patas ocupadas es más fácil."""
    defs, o = ch2_bg("sprouts")
    o.append(lemon_sapling(700, 444, 1.15, bump=True))
    o.append(soil_row(0, 800, 572, 32))
    for sx in range(60, 780, 80):
        o.append(sprout(sx, 556, 1.3))
    o.append(bun(480, 545, 1.15, pose="hold", expr="smile", holding=g(watering_can(0, 0, 0.7), 0, -40), look=(-4, 1)))
    o.append(tilly(220, 568, 1.25, expr="calm", nod=True))
    o.append(heart(340, 360, 1.3) + heart(372, 330, 0.9, "#F9C3CF"))
    return defs, cam("".join(o), 360, 420, 1.15)


# ============================================================ capítulo 3

def full_garden(time="day"):
    o = []
    o.append(tree(90, 400, 0.9, "green") + tree(270, 380, 0.8, "cherry") + tree(520, 380, 0.8, "pear") + tree(710, 400, 0.9, "lemon"))
    o.append(hills(time, back=False))
    return "".join(o)


def ch3_p01():
    """Meses después: el jardín lleno de fruta."""
    defs, bg = sky("day")
    o = [bg, sun(400, 90, 38), cloud(170, 110, 0.8) + cloud(640, 90, 0.7)]
    o.append(path("M0 330 Q200 300 420 325 Q620 350 800 315 L800 600 L0 600 Z", fill="#D5F0E2"))
    o.append(full_garden())
    o.append(melon_vine(560, 520, 1.3, melons=2))
    for sx, sy in [(90, 560), (200, 576), (320, 556)]:
        o.append(strawberry_plant(sx, sy, 1.5))
    o.append(bun(420, 548, 0.85, pose="cheer", expr="joy", ears="perk"))
    for sx, sy, r in [(270, 200, 8), (520, 210, 8), (720, 200, 7), (90, 210, 7)]:
        o.append(sparkle(sx, sy, r, "#FFFFFF"))
    o.append(tuft(30, 590, 1.2, "#9FD6BF") + tuft(770, 590, 1.2, "#9FD6BF"))
    return defs, "".join(o)


def fruit_pile(x, y, s=1.0):
    o = []
    rows = [
        [(-90, 0, "melon"), (-30, 4, "apple"), (20, 2, "pear"), (70, 0, "lemon"), (116, 4, "apple_g")],
        [(-64, -36, "lemon"), (-14, -34, "apple"), (36, -36, "cherry"), (86, -34, "pear")],
        [(-40, -70, "straw"), (10, -72, "apple_g"), (58, -68, "lemon")],
        [(-14, -104, "apple"), (34, -102, "straw")],
        [(10, -134, "cherry")],
    ]
    for row in rows:
        for fx, fy, k in row:
            if k == "melon":
                o.append(watermelon(fx, fy - 6, 0.9))
            elif k == "apple":
                o.append(apple(fx, fy, 1.3))
            elif k == "apple_g":
                o.append(apple(fx, fy, 1.3, GREEN_APPLE))
            elif k == "pear":
                o.append(pear(fx, fy, 1.25))
            elif k == "lemon":
                o.append(lemon(fx, fy, 1.15, rot=-15))
            elif k == "cherry":
                o.append(cherries(fx, fy, 1.3))
            else:
                o.append(strawberry(fx, fy, 1.5))
    return g("".join(o), x, y, s)


def ch3_p02():
    """Benny, orgulloso, siente que es demasiada fruta para un solo conejo."""
    defs, bg = sky("day")
    o = [bg, sun(660, 90, 36), cloud(200, 100, 0.8)]
    o.append(path("M0 330 Q200 300 420 325 Q620 350 800 315 L800 600 L0 600 Z", fill="#D5F0E2"))
    o.append(full_garden())
    o.append(bun(240, 560, 1.3, pose="stand", expr="think", look=(4, -2)))
    o.append(fruit_pile(520, 560, 1.15))
    o.append(basket(400, 590, 1.1, apple(-14, -26, 1.0) + pear(10, -28, 1.0) + lemon(0, -18, 0.9)))
    o.append(drop(296, 380, 0.8, "#BFE0F5"))
    return defs, cam("".join(o), 400, 380, 1.1)


def ch3_p03():
    """Benny recuerda: la abuela, Tilly y Milo."""
    defs, bg = sky("day")
    o = [bg, sun(400, 380, 30)]
    o.append(path("M0 330 Q200 300 420 325 Q620 350 800 315 L800 600 L0 600 Z", fill="#D5F0E2"))
    o.append(tree(90, 420, 0.8, "green") + tree(710, 420, 0.8, "lemon"))
    o.append(hills("day", back=False))
    o.append(bun(400, 575, 1.25, pose="think", expr="think"))
    mems = [
        (150, 150, "m1", granny(0, 0, 0.62, pose="hold", holding=seed_bag(0, -40, 1.3)), (330, 360)),
        (400, 105, "m2", tilly(0, 0, 0.62, flip=True, expr="calm"), (400, 330)),
        (650, 150, "m3", milo(0, 0, 0.95, expr="joy", holding=blueberries(0, -40, 0.8)), (470, 360)),
    ]
    for cx, cy, cid, char, tail in mems:
        rx, ry = 105, 85
        defs += bubble_clip(cid, cx, cy, rx * 0.95, ry * 0.92)
        ox = cx + (0 if cid != "m2" else -10)
        oy = cy + (70 if cid == "m1" else 50 if cid == "m3" else 40)
        inner = rect(cx - rx, cy - ry, rx * 2, ry * 2, "#F2ECFA") + ellipse(cx, cy + 70, 110, 36, "#DCEFE3") + g(char, ox, oy)
        o.append(bubble(cx, cy, rx, ry, tail, inner, cid))
    return defs, "".join(o)


def ch3_p04():
    """'¡Ya sé!' Benny tiene una idea: un picnic de frutas para todos."""
    defs, bg = sky("day")
    o = [bg, sun(120, 90, 34)]
    o.append(path("M0 330 Q200 300 420 325 Q620 350 800 315 L800 600 L0 600 Z", fill="#D5F0E2"))
    o.append(full_garden())
    o.append(bun(260, 560, 1.35, pose="wave", expr="joy", ears="perk"))
    o.append(bulb(330, 190, 1.1))
    cx, cy, rx, ry = 580, 230, 160, 110
    defs += (f'<pattern id="{mi.uid("check")}" width="24" height="24" patternUnits="userSpaceOnUse">'
             f'<rect width="24" height="24" fill="#FFF4EC"/><rect width="12" height="24" fill="#FFC6B4" opacity="0.6"/>'
             f'<rect width="24" height="12" fill="#FFC6B4" opacity="0.6"/></pattern>')
    defs += bubble_clip("idea", cx, cy, rx * 0.95, ry * 0.92)
    picnic = (rect(cx - rx, cy - ry, rx * 2, ry * 2, "#FFF6E6")
              + path(f"M{cx - 110} {cy + 10} L{cx + 110} {cy + 10} L{cx + 140} {cy + 90} L{cx - 140} {cy + 90} Z", fill=url("check"))
              + bowl(cx, cy + 40, 1.3, orange(-14, -18, 0.6) + strawberry(4, -22, 0.7) + grapes(18, -18, 0.4) + banana(0, -12, 0.5))
              + basket(cx - 90, cy + 60, 0.7, apple(-10, -24, 0.9) + pear(10, -26, 0.9))
              + watermelon_slice(cx + 90, cy + 60, 0.9)
              + heart(cx - 60, cy - 50, 1.2) + heart(cx + 70, cy - 60, 0.9, "#F9C3CF"))
    o.append(bubble(cx, cy, rx, ry, (380, 330), picnic, "idea"))
    return defs, cam("".join(o), 420, 330, 1.08)


def picnic_defs():
    return (f'<pattern id="{mi.uid("check")}" width="40" height="40" patternUnits="userSpaceOnUse">'
            f'<rect width="40" height="40" fill="#FFF4EC"/><rect width="20" height="40" fill="#FFC6B4" opacity="0.6"/>'
            f'<rect width="40" height="20" fill="#FFC6B4" opacity="0.6"/></pattern>')


def picnic_bg(time, sun_at=(400, 214), stars=0):
    defs, bg = sky(time)
    defs += picnic_defs()
    o = [bg]
    if stars:
        o.append(star_sky(random.Random(stars), stars, 20, 780, 20, 260, avoid=[(640, 110, 70)]))
    if time in ("dusk", "night"):
        o.append(moon(640, 110, 34))
    else:
        o.append(sun(*sun_at, 50))
    hill = {"golden": "#D9EDCB", "dusk": "#C9DDCB", "night": "#AFC7C0"}[time]
    o.append(path("M0 330 Q200 300 420 325 Q620 350 800 315 L800 600 L0 600 Z", fill=hill))
    o.append(tree(96, 420, 0.86, "apple") + tree(704, 420, 0.86, "lemon"))
    o.append(path("M0 400 Q400 370 800 400 L800 600 L0 600 Z", fill=HILLS[time][1]))
    o.append(path("M170 448 L630 448 L720 572 L80 572 Z", fill=url("check")))
    return defs, o


def ch3_p05():
    """El sábado llegan los amigos: naranjas, uvas, bananas y limonada rosada."""
    defs, o = picnic_bg("golden")
    o.append(granny(150, 560, 0.95, pose="hold", holding=pitcher(0, -36, 1.35)))
    o.append(puffs(70, 556, 0.9))
    o.append(bun(330, 532, 1.0, pose="hug", expr="joy", ears="perk"))
    o.append(milo(500, 568, 0.95, expr="joy", holding=grapes(0, -36, 0.6)))
    o.append(g(banana(0, 0, 1.0, -30) + banana(8, 6, 1.0, -20) + banana(16, 12, 1.0, -10), 548, 560, 0.85))
    o.append(tilly(680, 568, 0.85, flip=True, expr="open"))
    o.append(basket(690, 494, 0.85, orange(-16, -24, 0.9) + orange(10, -28, 0.9) + orange(0, -14, 0.85) + orange(22, -16, 0.8)))
    o.append(puffs(770, 560, 0.8))
    for sx, sy, r in [(250, 380, 8), (420, 370, 7)]:
        o.append(sparkle(sx, sy, r, "#FFFFFF"))
    return defs, "".join(o)


def ch3_p06():
    """La ensalada de frutas más grande del valle."""
    defs, o = picnic_bg("golden")
    salad = (orange(-22, -20, 0.75) + apple(18, -24, 0.7) + pear(-2, -28, 0.65) + cherries(-30, -32, 0.6)
             + strawberry(30, -32, 0.8) + grapes(8, -40, 0.45) + banana(-8, -14, 0.65, 12) + strawberry(-14, -40, 0.7)
             + orange(26, -12, 0.6) + cherries(4, -48, 0.55) + apple(-34, -14, 0.6, GREEN_APPLE))
    o.append(bowl(400, 520, 3.4, salad))
    o.append(bun(170, 560, 1.1, pose="cheer", expr="joy", ears="perk"))
    o.append(milo(590, 560, 1.05, expr="joy"))
    o.append(tilly(672, 584, 0.58, flip=True, expr="calm"))
    for sx, sy, r in [(300, 250, 11), (510, 240, 9), (400, 210, 7), (250, 330, 6), (560, 320, 7)]:
        o.append(sparkle(sx, sy, r, "#FFE38A"))
    return defs, cam("".join(o), 400, 420, 1.2)


def ch3_p07():
    """Comen sandía fresca y ríen hasta que salen las estrellas."""
    defs, o = picnic_bg("dusk", stars=12)
    o.append(granny(150, 556, 0.85, pose="eat", expr="joy", holding=watermelon_slice(0, -82, 1.25)))
    o.append(bun(320, 540, 0.95, pose="eat", expr="joy", holding=watermelon_slice(0, -82, 1.3)))
    o.append(milo(500, 560, 0.95, expr="joy", holding=watermelon_slice(0, -32, 0.85)))
    o.append(tilly(660, 568, 0.8, flip=True, expr="calm"))
    o.append(watermelon_slice(600, 520, 0.7, -6))
    o.append(watermelon_slice(420, 548, 0.7, 10) + path("M380 556 Q400 566 420 556", stroke="#9ED7AE", sw=4))
    for sx, sy in [(230, 380), (410, 370), (560, 380)]:
        o.append(path(f"M{sx} {sy} q6 -10 12 0 q6 10 12 0", stroke=WHITE, sw=3, extra=op(0.85)))
    return defs, "".join(o)


def ch3_p08():
    """Milo con la panza llenita: el mejor jardín del mundo."""
    defs, o = picnic_bg("dusk", stars=14)
    o.append(bowl(250, 540, 1.4))
    o.append(path("M180 560 Q200 576 220 560 M560 560 Q580 576 600 560", stroke="#9ED7AE", sw=5))
    o.append(milo_full(400, 560, 1.6))
    o.append(heart(470, 360, 1.6) + heart(330, 340, 1.1, "#F9C3CF"))
    o.append(bun(610, 560, 1.0, pose="stand", expr="smile", look=(-4, 0)))
    return defs, cam("".join(o), 420, 440, 1.3)


def ch3_p09():
    """Benny sonríe con sus amigos: un jardín para todos."""
    defs, o = picnic_bg("dusk", stars=16)
    o.append(granny(210, 556, 0.95, pose="stand", expr="smile", look=(4, 0)))
    o.append(tilly(640, 570, 0.85, flip=True, expr="calm"))
    o.append(bun(420, 548, 1.05, pose="hug", expr="smile", look=(0, 1)))
    o.append(milo(300, 576, 0.85, expr="joy"))
    o.append(basket(704, 572, 0.7, apple(-12, -24, 0.9) + orange(10, -26, 0.9)))
    o.append(heart(400, 260, 1.8) + heart(330, 300, 1.0, "#F9C3CF") + heart(476, 296, 1.1, "#F9C3CF"))
    return defs, cam("".join(o), 410, 420, 1.12)


def ch3_p10():
    """Fin: noche tranquila en el jardín, todos se quedan dormidos juntos."""
    defs, o = picnic_bg("night", stars=24)
    rng = random.Random(7)
    o.append(granny(200, 556, 0.85, pose="stand", expr="sleep"))
    o.append(bun(330, 548, 0.95, pose="stand", expr="sleep"))
    o.append(milo(450, 560, 0.85, expr="joy"))
    o.append(tilly(590, 568, 0.8, flip=True, expr="calm"))
    for _ in range(9):
        fx, fy = rng.uniform(120, 700), rng.uniform(300, 470)
        o.append(circle(fx, fy, 8, url("glow"), op(0.9)) + circle(fx, fy, 2.6, "#FFF4B8"))
    o.append(path("M470 470 q8 -8 16 0 M500 450 q6 -6 12 0", stroke=WHITE, sw=2.6, extra=op(0.8)))
    o.append(path("M300 420 l10 0 l-10 12 l10 0 M322 398 l8 0 l-8 10 l8 0", stroke=WHITE, sw=2.6, extra=op(0.8)))
    return defs, "".join(o)


# ----------------------------------------------------------------- índice

SCENES = {
    1: [
        (ch1_p01, "Benny dreams of a garden full of fruit"),
        (ch1_p02, "Grandma Bunny gives Benny a little bag of fruit seeds"),
        (ch1_p03, "Inside the bag: apple seeds, cherry pits, watermelon seeds, strawberry plants and a baby lemon tree"),
        (ch1_p04, "Benny jumps and shouts hooray"),
        (ch1_p05, "Benny plants the seeds and waters them with his blue watering can"),
        (ch1_p06, "Benny sits and waits while the sun moves across the sky"),
        (ch1_p07, "Tilly the turtle walks by very slowly"),
        (ch1_p08, "Benny thinks his apples and strawberries will be ready any minute"),
        (ch1_p09, "Tilly smiles a slow, wise smile: good things take time"),
        (ch1_p10, "Benny's ears droop: weeks and months sound like forever"),
    ],
    2: [
        (ch2_p01, "The next morning Benny finds only brown dirt"),
        (ch2_p02, "Milo peeks out from under a leaf eating blueberries while Benny looks grumpy"),
        (ch2_p03, "Grumpy Benny stomps: he wants a big red apple now"),
        (ch2_p04, "Milo offers Benny a blueberry"),
        (ch2_p05, "Benny waters the garden, pulls weeds and shoos away the crows"),
        (ch2_p06, "Tiny sprouts, white strawberry flowers and a little green lemon"),
        (ch2_p07, "Benny hops in circles: is that a lemon?"),
        (ch2_p08, "Tilly nods: waiting is easier with busy paws"),
    ],
    3: [
        (ch3_p01, "Benny's garden is full of strawberries, cherries, apples, pears, watermelons and lemons"),
        (ch3_p02, "Benny looks at a big pile of fruit: too much for one bunny"),
        (ch3_p03, "Benny remembers Grandma, Tilly and Milo"),
        (ch3_p04, "Benny has an idea: a fruit picnic for everyone"),
        (ch3_p05, "Friends arrive with oranges, grapes, bananas and pink lemonade"),
        (ch3_p06, "The biggest fruit salad in the valley"),
        (ch3_p07, "Everyone eats watermelon and laughs as the stars come out"),
        (ch3_p08, "Milo has a very full tummy: the best garden ever"),
        (ch3_p09, "Benny smiles with his friends: a garden for everyone"),
        (ch3_p10, "The friends fall asleep together under the stars"),
    ],
}


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    total = 0
    for ch, scenes in SCENES.items():
        for i, (fn, title) in enumerate(scenes, start=1):
            name = f"ch{ch}/p{i:02d}"
            if only and not (name == only or name.startswith(only + "/") or only == f"ch{ch}"):
                continue
            mi._P = f"benny-ch{ch}-p{i:02d}"
            defs, body = fn()
            out, size = mi.write_svg("benny", name, 800, 600, title, defs, body)
            total += 1
            print(f"{os.path.relpath(out, mi.ROOT)}  {size / 1024:.1f} KB")
    print(f"{total} scenes")


if __name__ == "__main__":
    main()
