#!/usr/bin/env python3
"""Escenas por párrafo de «Pip and the Fallen Star» (una ilustración por párrafo).

Reutiliza los personajes y ayudantes de make_illustrations.py y escribe
images/pip/ch<N>/p<NN>.svg (800×600). Las poses y expresiones que faltan
(hablar, sorprenderse, guiñar, dormir, señalar...) se definen aquí.

    python3 tools/scenes_pip.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import make_illustrations as mi  # noqa: E402
from make_illustrations import (  # noqa: E402
    BLUSH, FOX, FOX_CREAM, FOX_D, FOX_LIMB, FOX_PAW, EAR_PINK, PLUM, STAR, STAR_DIM, WHITE,
    OWL, OWL_D, OWL_L, BEAR, BEAR_D, BEAR_L, FROG, FROG_D, FROG_L, FOREST_MOUSE, BUN_PINK, NOSE,
    blades, blade, blush, calm_eye, circle, cloud_layer, drop, ellipse, eye, flower, frown, g,
    happy_eye, lily_pad, lin, moon, n, op, open_mouth, path, pine, rect, rock, rotated, round_tree,
    smile, sparkle, star_points, starfield, tuft, url, rabbit, squirrel, duck, fish, beaver,
    log_bridge, berry_bush, deer, cloud,
)

# ------------------------------------------------------------------ cámara


def cam(body, cx=400, cy=300, z=1.0):
    """Acerca la composición a (cx, cy) con zoom z sin dejar bordes vacíos."""
    if z == 1:
        return body
    cx = min(max(cx, 400 / z), 800 - 400 / z)
    cy = min(max(cy, 300 / z), 600 - 300 / z)
    return f'<g transform="translate(400 300) scale({n(z)}) translate({n(-cx)} {n(-cy)})">{body}</g>'


def world_at(sx, sy, cx=400, cy=300, z=1.0):
    """Punto del mundo que la cámara cam(cx, cy, z) muestra en (sx, sy) de la pantalla."""
    cx = min(max(cx, 400 / z), 800 - 400 / z)
    cy = min(max(cy, 300 / z), 600 - 300 / z)
    return (cx + (sx - 400) / z, cy + (sy - 300) / z)


# ------------------------------------------------------------- Pip (zorro)

def fox_head(expr="happy", look=(0, 0)):
    """Cabeza de Pip en las mismas coordenadas que mi.pip (centro ≈ (0, -128))."""
    h = []
    for sx in (-1, 1):
        h.append(path(f"M{sx * 16} -150 L{sx * 42} -197 L{sx * 50} -128 Z", fill=FOX, stroke=FOX, sw=10))
        h.append(path(f"M{sx * 24} -150 L{sx * 41} -184 L{sx * 44} -142 Z", fill=EAR_PINK, stroke=EAR_PINK, sw=5))
    h.append(path("M-52 -122 C-56 -168 56 -168 52 -122 C60 -108 38 -92 0 -90 C-38 -92 -60 -108 -52 -122 Z", fill=FOX))
    h.append(path("M-54 -118 C-40 -110 -20 -124 0 -112 C20 -124 40 -110 54 -118 C55 -104 36 -91 0 -90 C-36 -91 -55 -104 -54 -118 Z",
                  fill=FOX_CREAM))
    # ojos
    if expr == "joy":
        h.append(happy_eye(-20, -131, 14, 3.2) + happy_eye(20, -131, 14, 3.2))
    elif expr == "wink":
        h.append(happy_eye(-20, -131, 14, 3.2) + eye(20, -132, 6.4, look))
    elif expr == "sleepy":
        h.append(calm_eye(-20, -133, 13, 3) + calm_eye(20, -133, 13, 3))
    elif expr == "surprised":
        h.append(eye(-20, -133, 7.6, look) + eye(20, -133, 7.6, look))
    else:
        h.append(eye(-20, -132, 6.4, look) + eye(20, -132, 6.4, look))
    if expr == "tired":
        for sx in (-1, 1):
            h.append(path(f"M{sx * 20 - 9} -131 Q{sx * 20} -143 {sx * 20 + 9} -131 Z", fill=FOX)
                     + path(f"M{sx * 20 - 8} -131.5 L{sx * 20 + 8} -131.5", stroke=PLUM, sw=2.2))
    # cejas
    if expr in ("sad", "worried"):
        h.append(path("M-29 -146 L-14 -150", stroke=PLUM, sw=2.6) + path("M29 -146 L14 -150", stroke=PLUM, sw=2.6))
    elif expr == "determined":
        h.append(path("M-30 -151 L-13 -147", stroke=PLUM, sw=2.8) + path("M30 -151 L13 -147", stroke=PLUM, sw=2.8))
    elif expr == "surprised":
        h.append(path("M-28 -149 Q-20 -156 -12 -149", stroke=PLUM, sw=2.6) + path("M28 -149 Q20 -156 12 -149", stroke=PLUM, sw=2.6))
    elif expr == "think":
        h.append(path("M12 -151 Q20 -157 29 -152", stroke=PLUM, sw=2.6))
    h.append(blush(-35, -114, 8, 5) + blush(35, -114, 8, 5))
    h.append(ellipse(0, -113, 6.8, 5, PLUM) + ellipse(-2, -115, 2, 1.2, WHITE, extra=op(0.7)))
    # boca
    if expr == "curious":
        h.append(ellipse(0, -101, 3.6, 4.2, PLUM))
    elif expr == "surprised":
        h.append(ellipse(0, -100, 4.6, 5.6, PLUM))
    elif expr == "joy":
        h.append(open_mouth(0, -106, 14))
    elif expr == "talk":
        h.append(open_mouth(0, -106, 10))
    elif expr == "sad":
        h.append(frown(0, -103, 10, 2.6))
    elif expr == "worried":
        h.append(path("M-7 -102 Q-3.5 -105.5 0 -102 Q3.5 -98.5 7 -102", stroke=PLUM, sw=2.4))
    elif expr == "think":
        h.append(path("M-6 -103 Q1 -100 7 -104", stroke=PLUM, sw=2.4))
    elif expr == "tired":
        h.append(ellipse(0, -102, 3.4, 2.6, PLUM))
    elif expr in ("wink", "determined"):
        h.append(smile(0, -105, 14, 2.8, 0.5))
    elif expr == "sleepy":
        h.append(smile(0, -104, 8, 2.4, 0.4))
    else:
        h.append(path("M-8 -105 Q-4 -100 0 -106 Q4 -100 8 -105", stroke=PLUM, sw=2.6))
    return "".join(h)


def fox(x, y, s=1.0, flip=False, pose="sit", expr="happy", look=(0, 0), head_rot=0, holding="", lean=0):
    """Pip con más poses: sit, hold, wave, step, think, chest, reach, point, cheer."""
    o = ['<g transform="rotate(32 62 -62)">' + ellipse(62, -62, 31, 62, FOX_CREAM) + ellipse(62, -50, 32, 51, FOX) + "</g>"]
    o.append(ellipse(-32, -24, 20, 26, FOX_D) + ellipse(32, -24, 20, 26, FOX_D))
    o.append(ellipse(0, -54, 46, 52, FOX))
    o.append(ellipse(0, -46, 28, 38, FOX_CREAM))
    o.append(ellipse(-34, -7, 18, 9, FOX_PAW) + ellipse(34, -7, 18, 9, FOX_PAW))

    def leg(sx):
        return rect(sx * 19 - 7, -60, 14, 54, FOX_LIMB, rx=7) + ellipse(sx * 19, -7, 10, 7, FOX_PAW)

    def arm(d, px, py):
        return path(d, stroke=FOX_LIMB, sw=15) + circle(px, py, 9, FOX_PAW)

    def arm_hold(sx):
        return path(f"M{sx * 34} -84 Q{sx * 42} -66 {sx * 29} -60", stroke=FOX_LIMB, sw=15) + circle(sx * 28, -60, 8.5, FOX_PAW)

    if pose == "hold":
        o.append(holding + arm_hold(-1) + arm_hold(1))
    elif pose == "wave":
        o.append(leg(-1) + arm("M28 -84 Q56 -98 60 -130", 60, -133))
        o.append(path("M76 -150 Q84 -140 80 -128 M86 -160 Q98 -142 92 -124", stroke=WHITE, sw=3, extra=op(0.8)))
    elif pose == "step":
        o.append(leg(-1) + path("M19 -58 Q22 -40 34 -36", stroke=FOX_LIMB, sw=14) + circle(35, -35, 7.5, FOX_PAW))
    elif pose == "think":
        o.append(leg(-1) + arm("M30 -82 Q46 -94 26 -98", 24, -99))
    elif pose == "chest":
        o.append(leg(-1) + arm("M30 -82 Q34 -64 10 -68", 8, -68))
    elif pose == "reach":
        o.append(leg(-1) + arm("M30 -80 Q56 -72 74 -54", 76, -52))
    elif pose == "point":
        o.append(leg(-1) + arm("M30 -84 Q62 -92 88 -104", 90, -105))
    elif pose == "cheer":
        o.append(arm("M-30 -84 Q-70 -96 -84 -142", -85, -146) + arm("M30 -84 Q70 -96 84 -142", 85, -146))
    else:
        o.append(leg(-1) + leg(1))
    head = fox_head(expr, look)
    if head_rot:
        head = rotated(head, head_rot, 0, -95)
    o.append(head)
    if expr == "tired":
        o.append(drop(58, -150, 0.6, "#BFE0F5") + drop(70, -128, 0.45, "#BFE0F5"))
    return g("".join(o), x, y, s, flip=flip, rot=lean)


def fox_sleeping(x, y, s=1.0, flip=False):
    """Pip dormido hecho un ovillo, con la cola de manta."""
    o = [ellipse(10, -36, 76, 36, FOX)]
    o.append(ellipse(22, -30, 46, 20, FOX_CREAM))
    o.append(path("M80 -44 C118 -30 108 4 66 2 C40 0 22 -2 6 -6", stroke=FOX_D, sw=36))
    o.append(path("M80 -44 C114 -32 104 0 66 -2 C42 -4 24 -6 10 -8", stroke=FOX, sw=30))
    o.append(ellipse(2, -8, 22, 15, FOX_CREAM, rot=-6))
    o.append(g(fox_head("sleepy"), -50, 80, 0.78, rot=-14))
    o.append(path("M-4 -126 L10 -126 L-4 -112 L10 -112", stroke="#E4DCF7", sw=3)
             + path("M22 -150 L32 -150 L22 -140 L32 -140", stroke="#E4DCF7", sw=2.6))
    return g("".join(o), x, y, s, flip=flip)


# ----------------------------------------------------------------- Twinkle

def star(x, y, s=1.0, expr="happy", glow="normal", rot=0, look=(0, 0)):
    """Twinkle con más expresiones: cry, sob (llora hablando), worried, hope, smile, bright, wink, talk."""
    o = []
    radius, gop = {"dim": (72, 0.5), "normal": (100, 0.85), "big": (180, 1.0), "huge": (250, 1.0)}[glow]
    o.append(circle(0, 0, radius, url("glow"), op(gop)))
    color = STAR_DIM if glow == "dim" else STAR
    o.append(path(star_points(44, 22), fill=color, stroke=color, sw=14))
    o.append(ellipse(-15, -17, 6, 3.4, WHITE, rot=-50, extra=op(0.7)))
    lx, ly = look
    if expr in ("cry", "sob"):
        o.append(eye(-10, 0, 4.4, (lx, ly + 1)) + eye(10, 0, 4.4, (lx, ly + 1)))
        o.append(path("M-16 -9 L-6 -12", stroke=PLUM, sw=2.4) + path("M16 -9 L6 -12", stroke=PLUM, sw=2.4))
        o.append(open_mouth(0, 9, 8) if expr == "sob" else frown(0, 11, 9, 2.4))
        o.append(drop(-13, 13, 0.55, "#9FCDF2") + drop(14, 16, 0.45, "#9FCDF2"))
    elif expr == "worried":
        o.append(eye(-10, 1, 4.4, (lx, ly + 1)) + eye(10, 1, 4.4, (lx, ly + 1)))
        o.append(path("M-16 -9 L-6 -12", stroke=PLUM, sw=2.4) + path("M16 -9 L6 -12", stroke=PLUM, sw=2.4))
        o.append(path("M-6 11 Q-3 8 0 11 Q3 14 6 11", stroke=PLUM, sw=2.2))
    elif expr == "hope":
        o.append(eye(-10, 0, 4.8, (lx, ly)) + eye(10, 0, 4.8, (lx, ly)))
        o.append(blush(-19, 8, 5, 3.2) + blush(19, 8, 5, 3.2))
        o.append(ellipse(0, 10, 3, 3.6, PLUM))
    elif expr == "smile":
        o.append(happy_eye(-10, 0, 10, 2.6) + happy_eye(10, 0, 10, 2.6))
        o.append(blush(-19, 8, 5, 3.2) + blush(19, 8, 5, 3.2))
        o.append(smile(0, 7, 11, 2.4, 0.5))
    elif expr in ("bright", "talk"):
        if expr == "bright":
            o.append(happy_eye(-10, 0, 10, 2.6) + happy_eye(10, 0, 10, 2.6))
        else:
            o.append(eye(-10, 0, 4.6, look) + eye(10, 0, 4.6, look))
        o.append(blush(-19, 8, 5, 3.2) + blush(19, 8, 5, 3.2))
        o.append(open_mouth(0, 7, 11))
    elif expr == "wink":
        o.append(happy_eye(-10, 0, 10, 2.6) + eye(10, 0, 4.6))
        o.append(blush(-19, 8, 5, 3.2) + blush(19, 8, 5, 3.2))
        o.append(smile(0, 8, 11, 2.4, 0.5))
    else:
        o.append(eye(-10, 0, 4.6, look) + eye(10, 0, 4.6, look))
        o.append(blush(-19, 8, 5, 3.2) + blush(19, 8, 5, 3.2))
        o.append(smile(0, 8, 10, 2.4))
    if glow in ("big", "huge"):
        for a, d, r in [(-60, 78, 10), (20, 84, 8), (110, 80, 9), (190, 76, 7), (260, 86, 11), (330, 72, 6)]:
            ar = math.radians(a)
            o.append(sparkle(d * math.cos(ar), d * math.sin(ar), r, "#FFF8D6"))
    return g("".join(o), x, y, s, rot=rot)


def wink_star(x, y, s=1.0):
    """Estrella del cielo guiñando (sin brillo grande), con destellos alrededor."""
    o = [circle(0, 0, 70, url("glow"), op(0.9)), path(star_points(30, 15), fill=STAR, stroke=STAR, sw=9)]
    o.append(happy_eye(-7, -1, 8, 2.2) + eye(7, -1, 3.4) + smile(0, 6, 8, 2, 0.5))
    for a, d, r in [(-40, 48, 7), (60, 52, 6), (160, 50, 8), (230, 46, 5)]:
        o.append(sparkle(d * math.cos(math.radians(a)), d * math.sin(math.radians(a)), r, "#FFF8D6"))
    return g("".join(o), x, y, s)


# ------------------------------------------------------- más personajes

def owl2(x, y, s=1.0, flip=False, blink=False, talk=False, wing=None, joy=False):
    """Abuelo Búho: pestañea, habla, señala con el ala (wing='point') o vuela (wing='fly')."""
    o = []
    for sx in (-1, 1):
        o.append(path(f"M{sx * 22} -150 L{sx * 46} -176 L{sx * 46} -132 Z", fill=OWL, stroke=OWL, sw=8))
    if wing == "fly":
        o.append(ellipse(-82, -96, 18, 54, OWL_D, rot=62) + ellipse(82, -96, 18, 54, OWL_D, rot=-62))
    o.append(ellipse(0, -62, 46, 62, OWL))
    if wing == "point":
        o.append(ellipse(-44, -60, 14, 38, OWL_D, rot=12) + ellipse(78, -92, 14, 42, OWL_D, rot=-62))
    elif wing != "fly":
        o.append(ellipse(-44, -60, 14, 38, OWL_D, rot=12) + ellipse(44, -60, 14, 38, OWL_D, rot=-12))
    o.append(ellipse(0, -122, 52, 42, OWL))
    o.append(ellipse(0, -48, 30, 40, OWL_L))
    for row, yy in enumerate((-70, -56, -42, -28)):
        xs = (-12, 6) if row % 2 else (-18, 0, 18)
        if row == 3:
            xs = (-6, 10)
        for xx in xs:
            o.append(path(f"M{xx - 6} {yy} Q{xx} {yy + 6} {xx + 6} {yy}", stroke=OWL_D, sw=2.2))
    for sx in (-1, 1):
        o.append(circle(sx * 21, -120, 24, OWL_L))
        closed = joy or (blink and sx == -1)
        if closed:
            o.append(happy_eye(sx * 21, -118, 22, 3.6))
        else:
            o.append(circle(sx * 21, -120, 16, WHITE) + circle(sx * 21, -119, 11, STAR) + circle(sx * 21, -119, 6.5, PLUM)
                     + circle(sx * 21 + 2.5, -122, 2.4, WHITE))
        o.append("".join(circle(sx * bx, by, br, WHITE) for bx, by, br in [(9, -142, 5), (18, -146, 6.5), (28, -145, 6), (37, -139, 4.6)]))
    o.append(blush(-40, -100, 7, 4.5) + blush(40, -100, 7, 4.5))
    if talk or joy:
        o.append(path("M-7 -108 L7 -108 L0 -101 Z", fill="#F4A06B", stroke="#F4A06B", sw=4)
                 + path("M-5 -97 L5 -97 L0 -91 Z", fill="#E58E5A", stroke="#E58E5A", sw=3)
                 + ellipse(0, -99, 4, 1.6, PLUM))
    else:
        o.append(path("M-7 -108 L7 -108 L0 -95 Z", fill="#F4A06B", stroke="#F4A06B", sw=4))
    if wing != "fly":
        for sx in (-1, 1):
            o.append(circle(sx * 8, -1, 4.4, "#F4A06B") + circle(sx * 15, 0, 4.4, "#F4A06B"))
    return g("".join(o), x, y, s, flip=flip)


def bear2(x, y, s=1.0, flip=False, pose="sit", expr="happy"):
    """Oso pardo: sit, berries (comiendo), point (señala arriba a la derecha), cheer, joke."""
    o = [ellipse(-34, -20, 24, 20, BEAR_D) + ellipse(34, -20, 24, 20, BEAR_D)]
    o.append(ellipse(0, -62, 54, 60, BEAR) + ellipse(0, -54, 33, 41, BEAR_L))
    o.append(ellipse(-38, -9, 15, 9, BEAR_L) + ellipse(38, -9, 15, 9, BEAR_L))

    def paw_arm(d, px, py):
        return path(d, stroke=BEAR_D, sw=22) + circle(px, py, 14, BEAR_D) + circle(px, py - 2, 6.5, BEAR_L)

    if pose == "berries":
        o.append(path("M-48 -88 Q-46 -66 -16 -62", stroke=BEAR_D, sw=20) + path("M48 -88 Q46 -66 16 -62", stroke=BEAR_D, sw=20))
        for bx, by, c in [(-8, -70, "#B48DD6"), (6, -72, "#E58FA6"), (-1, -80, "#B48DD6"), (12, -82, "#B48DD6"), (-12, -81, "#E58FA6")]:
            o.append(circle(bx, by, 6, c) + circle(bx - 2, by - 2, 1.6, WHITE, op(0.7)))
    elif pose == "point":
        o.append(ellipse(-44, -64, 13, 26, BEAR_D, rot=16) + paw_arm("M46 -88 Q86 -112 108 -150", 110, -154))
    elif pose == "cheer":
        o.append(paw_arm("M-46 -88 Q-74 -120 -76 -166", -76, -170) + paw_arm("M46 -88 Q74 -120 76 -166", 76, -170))
    elif pose == "joke":
        o.append(ellipse(-44, -64, 13, 26, BEAR_D, rot=16) + paw_arm("M46 -88 Q74 -96 80 -124", 80, -128))
    else:
        o.append(ellipse(-44, -64, 13, 26, BEAR_D, rot=16) + ellipse(44, -64, 13, 26, BEAR_D, rot=-16))
    for sx in (-1, 1):
        o.append(circle(sx * 32, -168, 15, BEAR) + circle(sx * 32, -168, 8, BEAR_L))
    o.append(circle(0, -138, 42, BEAR))
    o.append(ellipse(0, -122, 20, 15, BEAR_L))
    o.append(ellipse(0, -129, 7.5, 5.5, PLUM) + ellipse(-2, -131, 2, 1.2, WHITE, extra=op(0.7)))
    if expr == "joy":
        o.append(happy_eye(-16, -146, 11, 3) + happy_eye(16, -146, 11, 3) + open_mouth(0, -119, 12))
    elif expr == "talk":
        o.append(eye(-16, -146, 5.2) + eye(16, -146, 5.2) + open_mouth(0, -119, 9))
    elif expr == "munch":
        o.append(happy_eye(-16, -146, 11, 3) + happy_eye(16, -146, 11, 3)
                 + ellipse(0, -116, 7, 4.5, PLUM) + circle(-26, -120, 7, BEAR) + circle(26, -120, 7, BEAR))
    else:
        o.append(eye(-16, -146, 5.2) + eye(16, -146, 5.2))
        o.append(path("M-7 -118 Q-3.5 -114 0 -119 Q3.5 -114 7 -118", stroke=PLUM, sw=2.4))
    o.append(blush(-30, -124, 7, 4.5) + blush(30, -124, 7, 4.5))
    return g("".join(o), x, y, s, flip=flip)


def mouse(x, y, s=1.0, flip=False, expr="happy", look=(0, 0)):
    """Ratoncito del bosque (colores FOREST_MOUSE): happy, joy, sleepy."""
    MOUSE, MOUSE_D, MOUSE_L = FOREST_MOUSE
    o = [path("M16 -8 C46 -4 54 -36 38 -42 C27 -46 25 -28 36 -29", stroke=MOUSE_D, sw=4)]
    o.append(ellipse(0, -27, 22, 27, MOUSE) + ellipse(0, -23, 14, 17, MOUSE_L))
    o.append(ellipse(-10, -3, 9, 4.5, BUN_PINK) + ellipse(10, -3, 9, 4.5, BUN_PINK))
    o.append(ellipse(-17, -30, 5, 10, MOUSE_D, rot=20) + ellipse(17, -30, 5, 10, MOUSE_D, rot=-20))
    for sx in (-1, 1):
        o.append(circle(sx * 21, -82, 15, MOUSE) + circle(sx * 21, -82, 9.5, BUN_PINK))
    o.append(circle(0, -62, 24, MOUSE) + ellipse(0, -54, 12, 9, MOUSE_L))
    if expr == "joy":
        o.append(happy_eye(-9, -66, 9, 2.6) + happy_eye(9, -66, 9, 2.6))
    elif expr == "sleepy":
        o.append(calm_eye(-9, -66, 8, 2.4) + calm_eye(9, -66, 8, 2.4))
    else:
        o.append(eye(-9, -66, 4.2, look) + eye(9, -66, 4.2, look))
    o.append(blush(-16, -55, 4.5, 3) + blush(16, -55, 4.5, 3))
    o.append(path("M-4 -51 Q-2 -48 0 -51 Q2 -48 4 -51", stroke=PLUM, sw=1.8))
    for sx in (-1, 1):
        o.append(path(f"M{sx * 10} -56 L{sx * 30} -60 M{sx * 10} -53 L{sx * 30} -51", stroke=PLUM, sw=1.2, extra=op(0.35)))
    o.append(circle(0, -57, 3.6, NOSE))
    return g("".join(o), x, y, s, flip=flip)


def frog2(x, y, s=1.0, flip=False, expr="happy", pose="sit"):
    """Rana: sit, jump (en el aire) o dance (brazos arriba)."""
    o = []
    if pose == "jump":
        o.append(path("M-20 -14 Q-40 6 -56 18", stroke=FROG_D, sw=12) + path("M20 -14 Q40 6 56 18", stroke=FROG_D, sw=12)
                 + ellipse(-60, 20, 9, 5, FROG_D) + ellipse(60, 20, 9, 5, FROG_D))
    elif pose == "dance":
        o.append(ellipse(-24, -8, 15, 9, FROG_D, rot=20) + path("M18 -14 Q36 -20 44 -34", stroke=FROG_D, sw=11)
                 + ellipse(46, -38, 8, 5, FROG_D, rot=-50))
    else:
        o.append(ellipse(-26, -10, 16, 10, FROG_D) + ellipse(26, -10, 16, 10, FROG_D))
    o.append(ellipse(0, -24, 30, 22, FROG) + ellipse(0, -18, 18, 13, FROG_L))
    if pose == "dance":
        o.append(path("M-22 -30 Q-40 -44 -42 -62", stroke=FROG_D, sw=8) + path("M22 -30 Q40 -44 42 -62", stroke=FROG_D, sw=8)
                 + circle(-42, -64, 5, FROG_D) + circle(42, -64, 5, FROG_D))
    elif pose != "jump":
        o.append(ellipse(-12, -3, 8, 4, FROG_D) + ellipse(12, -3, 8, 4, FROG_D))
    else:
        o.append(path("M-16 -16 Q-26 -4 -30 2", stroke=FROG_D, sw=7) + path("M16 -16 Q26 -4 30 2", stroke=FROG_D, sw=7))
    for sx in (-1, 1):
        if expr == "joy":
            o.append(circle(sx * 16, -44, 11, FROG) + happy_eye(sx * 16, -44, 10, 2.6))
        else:
            o.append(circle(sx * 16, -44, 11, FROG) + circle(sx * 16, -45, 7.5, WHITE)
                     + circle(sx * 16, -44, 4.6, PLUM) + circle(sx * 16 + 1.6, -46, 1.6, WHITE))
    o.append(blush(-21, -29, 5, 3) + blush(21, -29, 5, 3))
    if expr in ("joy", "shout"):
        o.append(open_mouth(0, -32, 14))
    else:
        o.append(smile(0, -33, 20, 2.6, 0.3))
    return g("".join(o), x, y, s, flip=flip)


def duck2(x, y, s=1.0, flip=False, baby=False, swim=True, sing=False):
    """Pato que puede cantar (pico abierto)."""
    body = mi.duck(0, 0, 1.0, baby=baby, swim=swim)
    if sing:
        dy = 0 if swim else -12
        body += (path(f"M33 {-32 + dy} L44 {-25 + dy} L33 {-27 + dy} Z", fill="#E9A055", stroke="#E9A055", sw=2)
                 + ellipse(36, -31 + dy, 3, 1.4, PLUM))
    return g(body, x, y, s, flip=flip)


def bird(x, y, s=1.0, flip=False, sleep=True, color="#F7C9D4", shade="#EDB2C1"):
    """Pajarito redondo (dormido o despierto). Mira a la derecha."""
    o = [path("M-14 -16 L-30 -24 L-26 -10 Z", fill=shade, stroke=shade, sw=4)]
    o.append(ellipse(0, -16, 19, 15, color) + ellipse(-4, -14, 10, 7, shade, rot=-15))
    o.append(circle(11, -27, 11, color))
    o.append(path("M20 -29 L28 -26 L20 -23 Z", fill="#F7C873", stroke="#F7C873", sw=2))
    o.append(calm_eye(13, -29, 7, 2) if sleep else eye(13, -29, 2.6))
    o.append(blush(13, -22, 3, 2))
    return g("".join(o), x, y, s, flip=flip)


def nest(x, y, s=1.0):
    o = [ellipse(0, 0, 46, 15, "#D8BBA0")]
    for k in range(5):
        o.append(path(f"M{-42 + k * 6} {-4 + k % 2 * 4} Q0 {10 + k % 3 * 2} {42 - k * 5} {-4 + k % 2 * 3}", stroke="#C9A98F", sw=2.4))
    return g("".join(o), x, y, s)


def zzz(x, y, s=1.0, c="#E4DCF7"):
    return g(path("M0 0 L12 0 L0 12 L12 12", stroke=c, sw=3) + path("M18 -20 L27 -20 L18 -11 L27 -11", stroke=c, sw=2.6)
             + path("M32 -36 L39 -36 L32 -29 L39 -29", stroke=c, sw=2.2), x, y, s)


def note(x, y, s=1.0, c="#B9A9E3", rot=0):
    return g(ellipse(0, 0, 7, 5, c, rot=-20) + path("M6 -2 L6 -28 Q14 -24 16 -14", stroke=c, sw=2.8), x, y, s, rot=rot)


def honey_pot(x, y, s=1.0):
    o = [path("M-22 -6 C-26 -30 -18 -38 -14 -40 L14 -40 C18 -38 26 -30 22 -6 C18 4 -18 4 -22 -6 Z", fill="#F7C873")]
    o.append(rect(-18, -48, 36, 10, "#E9B35F", rx=5))
    o.append(path("M-8 -40 Q-8 -30 -4 -28 Q0 -26 0 -34", fill="#FFE29A", stroke="#FFE29A", sw=3))
    o.append(ellipse(-9, -22, 4, 7, WHITE, rot=10, extra=op(0.5)))
    return g("".join(o), x, y, s)


def bubble(x, y, w, h, tail, body="", kind="speech"):
    """Globo de diálogo o de pensamiento con contenido dibujado (sin texto)."""
    tx, ty = tail
    o = []
    if kind == "thought":
        parts = [("c", x - w * 0.28, y, h * 0.42), ("c", x, y - h * 0.12, h * 0.52), ("c", x + w * 0.28, y, h * 0.42),
                 ("r", x - w / 2, y - h * 0.18, w, h * 0.62, h * 0.31)]
        o.append(cloud_layer(parts, "#E9E2F7", 5) + cloud_layer(parts, WHITE))
        for k, r in enumerate((10, 7, 5)):
            f = (k + 1) / 4
            o.append(circle(x + (tx - x) * f, y + h * 0.35 + (ty - y - h * 0.35) * f, r, WHITE))
    else:
        o.append(rect(x - w / 2, y - h / 2, w, h, WHITE, rx=min(w, h) / 2.3))
        o.append(path(f"M{n(x - 14)} {n(y + h / 2 - 2)} L{n(tx)} {n(ty)} L{n(x + 14)} {n(y + h / 2 - 2)} Z", fill=WHITE))
    o.append(body)
    return g("".join(o), opacity=0.97)


def motion(x, y, s=1.0, rot=0, c="#FFFFFF", o_=0.85):
    return g(path("M0 0 L-26 0 M4 14 L-18 14 M0 -14 L-20 -14", stroke=c, sw=3.4), x, y, s, rot=rot, opacity=o_)


def sound(x, y, s=1.0, rot=0, c="#FFFFFF"):
    return g(path("M0 -10 L12 -18 M4 2 L20 2 M0 14 L12 22", stroke=c, sw=3.2), x, y, s, rot=rot, opacity=0.9)


def fireflies(pts):
    return "".join(circle(fx, fy, 9, url("glow")) + circle(fx, fy, 2.4, "#FFF6C8") for fx, fy in pts)


def trail(points, color="#FFF6C8"):
    """Estela de destellos a lo largo de una lista de puntos (de la cola a la cabeza)."""
    o = []
    for i, (px, py) in enumerate(points):
        f = (i + 1) / len(points)
        o.append(sparkle(px, py, 3 + 7 * f, color, 0.35 + 0.6 * f))
    return "".join(o)


def den(x, y, s=1.0):
    """La madriguera de Pip: un montículo con la entrada. Origen: base central."""
    o = [path("M-150 0 Q-110 -120 0 -126 Q110 -120 150 0 Z", fill="#BCD7CA")]
    o.append(path("M-120 -30 Q-60 -60 -20 -50 M40 -96 Q80 -90 110 -60", stroke="#A9CDBF", sw=5))
    o.append(ellipse(0, -46, 58, 44, "#9C91B8") + ellipse(0, -40, 48, 36, "#857AA3"))
    o.append(path("M-56 -40 Q-62 -10 -40 0 M58 -38 Q66 -12 44 0", stroke="#C9A98F", sw=5))
    return g("".join(o), x, y, s)


def daisy_big(x, y, s=1.0):
    return flower(x, y, s, WHITE, "#FFE38A", 60)


# ------------------------------------------------------- fondos del cap. 1

def ch1_sky(rng, moon_at=(120, 100), stars=28, y1=290, avoid=()):
    defs = lin("sky", [(0, "#B5AADF"), (0.6, "#DED5F3"), (1, "#F7DCD8")])
    av = list(avoid) + ([(moon_at[0], moon_at[1], 70)] if moon_at else [])
    o = [rect(0, 0, 800, 600, url("sky")), starfield(rng, stars, 40, 760, 30, y1, avoid=av)]
    if moon_at:
        o.append(moon(moon_at[0], moon_at[1], 34))
    return defs, o


def ch1_hills():
    return [path("M0 360 Q200 300 420 345 Q620 385 800 330 L800 600 L0 600 Z", fill="#C9DFD8"),
            path("M0 440 Q400 380 800 440 L800 600 L0 600 Z", fill="#AFD2C2")]


def forest_edge(rng, x0=0, x1=330):
    o = []
    x = x0 + 10
    while x < x1:
        if rng.random() < 0.6:
            o.append(pine(x, 372 - rng.uniform(0, 18), rng.uniform(0.62, 0.86), "#A9CDBF", "#93BBAE"))
        else:
            o.append(round_tree(x, 372 - rng.uniform(0, 14), rng.uniform(0.7, 0.9), "#A9CDBF", "#93BBAE"))
        x += rng.uniform(34, 54)
    return "".join(o)


def pond(cx=660, cy=458, rx=118, ry=26):
    return (ellipse(cx, cy, rx, ry, "#BFE0F5")
            + path(f"M{n(cx - 80)} {n(cy - 6)} Q{n(cx - 62)} {n(cy - 10)} {n(cx - 44)} {n(cy - 6)} "
                   f"M{n(cx + 30)} {n(cy + 12)} Q{n(cx + 48)} {n(cy + 8)} {n(cx + 66)} {n(cy + 12)}", stroke="#E3F2FC", sw=3))


def front_grass(rng, y0=560, y1=610, count=40):
    return blades(rng, count, 0, 800, y0, y1, 30, 60, ["#93C2AC", "#8BBDA6", "#9CCAB5"])


def back_grass(rng, x0=0, x1=800, y0=425, y1=470, count=50):
    return blades(rng, count, x0, x1, y0, y1, 30, 70, ["#9CCAB5", "#A6D0BC", "#93C2AC"])


def meadow_flowers(pts, s=1.0):
    return "".join(flower(fx, fy, s, WHITE, "#FFE38A", 40) for fx, fy in pts)


# ------------------------------------------------------------ capítulo 1

def c1p01():
    rng = random.Random(101)
    defs, o = ch1_sky(rng)
    o.append(forest_edge(rng))
    o += ch1_hills()
    o.append(back_grass(rng, 0, 800, 430, 470, 40))
    o.append(den(610, 486, 1.05))
    o.append(bird(250, 318, 0.9, sleep=False))
    o.append(rabbit(120, 535, 0.56, expr="happy"))
    o.append(blade(160, 540, 40, 6, "#93C2AC") + blade(176, 544, 32, -4, "#9CCAB5"))
    o.append(frog2(300, 560, 0.5))
    o.append(mouse(724, 548, 0.5, flip=True))
    o.append(fox(372, 560, 1.18, pose="wave", expr="joy", head_rot=-4))
    o.append(meadow_flowers([(60, 590), (230, 598), (560, 600), (770, 590)], 1.1))
    o.append(front_grass(rng, 572, 612, 30))
    o.append(fireflies([(380, 330), (520, 300), (700, 360), (200, 420)]))
    return defs, "".join(o), "Pip the fox waves in front of his den at the edge of the forest, with his animal friends"


def c1p02():
    rng = random.Random(102)
    defs = lin("sky", [(0, "#B5AADF"), (0.7, "#DED5F3"), (1, "#EADCEB")])
    defs += lin("soil", [(0, "#EAD8C8"), (1, "#DCC4B0")])
    o = [rect(0, 0, 800, 600, url("sky")), starfield(rng, 22, 30, 520, 26, 230, avoid=[(110, 80, 60)]), moon(110, 80, 28)]
    # árbol con el nido
    canopy = [("c", 640, 70, 78), ("c", 560, 96, 50), ("c", 726, 96, 52), ("c", 600, 30, 46), ("c", 690, 26, 44)]
    o.append(path("M600 290 C612 220 606 170 618 120 L660 120 C670 170 664 220 680 290 Z", fill="#C9A98F"))
    o.append(path("M612 196 C570 186 520 186 470 174", stroke="#C9A98F", sw=14))
    o.append(cloud_layer(canopy, "#93BBAE", 8) + cloud_layer(canopy, "#A9CDBF"))
    o.append(nest(520, 178, 1.0))
    o.append(bird(500, 172, 0.95) + bird(542, 172, 0.95, flip=True, color="#CDE4F5", shade="#B3D2EC"))
    o.append(zzz(560, 120, 0.9))
    # suelo en corte
    o.append(path("M0 272 Q200 256 400 268 Q600 282 800 262 L800 600 L0 600 Z", fill="#AFD2C2"))
    o.append(path("M0 294 Q200 282 400 292 Q600 302 800 288 L800 600 L0 600 Z", fill=url("soil")))
    for px, py, r in [(60, 360, 8), (420, 330, 6), (460, 560, 9), (740, 540, 7), (360, 470, 5), (90, 540, 6)]:
        o.append(ellipse(px, py, r * 1.4, r, "#D3BCA6"))
    o.append(blades(rng, 34, 0, 800, 262, 284, 16, 34, ["#9CCAB5", "#93C2AC"]))
    # madriguera de los conejos
    o.append(path("M96 276 C104 326 140 366 186 386", stroke="#CDB4A0", sw=46))
    o.append(ellipse(250, 420, 140, 66, "#CDB4A0") + ellipse(250, 446, 118, 32, "#C3A994"))
    o.append(rabbit(196, 470, 0.56, expr="sleepy") + rabbit(306, 470, 0.56, flip=True, expr="sleepy"))
    # raíces con los ratones
    for d in ["M616 292 C604 344 566 366 520 404", "M664 292 C676 352 714 374 742 424", "M640 294 C644 352 636 396 646 446"]:
        o.append(path(d, stroke="#C9A98F", sw=9))
    o.append(ellipse(612, 488, 92, 44, "#CDB4A0") + ellipse(612, 506, 74, 22, "#C3A994"))
    o.append(mouse(578, 522, 0.62, expr="sleepy") + mouse(648, 522, 0.58, flip=True, expr="sleepy"))
    o.append(zzz(650, 410, 0.8, "#F4ECF9") + zzz(300, 360, 0.9, "#F4ECF9"))
    return defs, "".join(o), "Rabbits asleep in their burrow, mice asleep under the roots and birds asleep in their nest"


def c1p03():
    rng = random.Random(103)
    defs, o = ch1_sky(rng, moon_at=None, stars=24, y1=300, avoid=[(600, 180, 160)])
    o.append(moon(90, 90, 26))
    o.append(path("M300 400 Q500 350 800 380 L800 600 L300 600 Z", fill="#C9DFD8"))
    o.append(pond(660, 452, 96, 20))
    o.append(path("M300 470 Q560 420 800 468 L800 600 L300 600 Z", fill="#AFD2C2"))
    o.append(back_grass(rng, 380, 800, 456, 490, 28))
    pts = [(752 - 22 * k, 70 + 30 * k + 1.6 * k * k) for k in range(9)]
    o.append(trail(pts))
    o.append(star(pts[-1][0] - 14, pts[-1][1] + 34, 0.42, "hope", "normal", rot=-20))
    o.append(circle(590, 438, 40, url("glow"), op(0.8)))
    # la madriguera de cerca con Pip asomándose
    o.append(path("M-30 600 Q-10 400 210 392 Q420 400 450 600 Z", fill="#BCD7CA"))
    o.append(path("M40 450 Q90 420 140 428 M290 420 Q350 430 390 470", stroke="#A9CDBF", sw=6))
    o.append(ellipse(210, 506, 104, 82, "#9C91B8") + ellipse(210, 516, 88, 68, "#857AA3"))
    o.append(g(fox_head("surprised", look=(3, -5)), 210, 660, 1.08, rot=8))
    o.append(ellipse(150, 574, 26, 14, FOX_PAW) + ellipse(276, 574, 26, 14, FOX_PAW))
    o.append(path("M100 512 Q92 560 112 600 M322 510 Q332 560 312 600", stroke="#C9A98F", sw=8))
    o.append(blades(rng, 18, 0, 460, 586, 612, 24, 46, ["#93C2AC", "#8BBDA6"]))
    return defs, "".join(o), "Pip peeks out of his den and sees a tiny light falling from the sky"


def c1p04():
    rng = random.Random(104)
    defs, o = ch1_sky(rng, moon_at=world_at(110, 95, 450, 420, 1.12))
    o += ch1_hills()
    o.append(back_grass(rng, 0, 520, 430, 470, 36))
    o.append(pond(640, 466, 150, 30))
    o.append(lily_pad(560, 476, 0.55) + lily_pad(676, 470, 0.9))
    o.append(path("M520 470 Q560 330 640 398", stroke=WHITE, sw=3, extra=' stroke-dasharray="2 12"' + op(0.8)))
    o.append(frog2(652, 420, 0.72, expr="shout", pose="jump", flip=True))
    o.append(sound(612, 388, 1.0, rot=180) + drop(690, 470, 0.5, "#E3F2FC") + drop(708, 462, 0.4, "#E3F2FC"))
    o.append(circle(470, 520, 46, url("glow"), op(0.8)))
    o.append(blade(450, 530, 54, -6, "#93C2AC") + blade(480, 534, 60, 8, "#8BBDA6") + blade(500, 530, 44, -4, "#9CCAB5"))
    o.append(fox(250, 560, 1.15, pose="step", expr="surprised", look=(5, -1), lean=6))
    o.append(meadow_flowers([(80, 470), (160, 456), (400, 452)]))
    o.append(front_grass(rng))
    o.append(meadow_flowers([(60, 590), (380, 600), (740, 596)], 1.2))
    o.append(fireflies([(430, 380), (300, 330), (760, 390)]))
    return defs, cam("".join(o), 450, 420, 1.12), "Pip tiptoes through the grass as a green frog jumps onto a lily pad shouting ribbit"


def c1p05():
    rng = random.Random(105)
    defs = lin("sky", [(0, "#C4BAE6"), (0.7, "#E4DCF5"), (1, "#F5DDDB")])
    o = [rect(0, 0, 800, 600, url("sky")), starfield(rng, 14, 40, 760, 30, 200)]
    o.append(path("M0 330 Q400 280 800 330 L800 600 L0 600 Z", fill="#C2DCD1"))
    o.append(blades(rng, 26, 0, 800, 360, 400, 70, 150, ["#A6D0BC", "#9CCAB5"]))
    o.append(path("M0 420 Q400 370 800 420 L800 600 L0 600 Z", fill="#AFD2C2"))
    o.append(daisy_big(220, 590, 3.0) + daisy_big(590, 590, 2.8))
    o.append(star(405, 446, 1.55, "cry", "dim", rot=10))
    o.append(blades(rng, 30, 0, 800, 560, 612, 50, 110, ["#93C2AC", "#8BBDA6", "#9CCAB5"]))
    o.append(fireflies([(140, 250), (660, 230), (720, 380), (90, 400)]))
    return defs, "".join(o), "Close-up of Twinkle, a little star, crying between two daisies"


def c1p06():
    rng = random.Random(106)
    defs, o = ch1_sky(rng, moon_at=world_at(110, 95, 420, 420, 1.18))
    o += ch1_hills()
    o.append(back_grass(rng))
    o.append(meadow_flowers([(90, 470), (180, 456), (700, 452)]))
    o.append(fox(290, 566, 1.28, pose="reach", expr="talk", look=(5, 3), head_rot=6, lean=6))
    o.append(daisy_big(470, 560, 1.4) + daisy_big(600, 560, 1.4))
    o.append(star(535, 512, 0.95, "cry", "dim", rot=-8, look=(-2, -2)))
    o.append(front_grass(rng))
    o.append(meadow_flowers([(60, 590), (720, 596)], 1.2))
    o.append(fireflies([(430, 360), (650, 330), (230, 300)]))
    return defs, cam("".join(o), 420, 420, 1.18), "Pip leans down and gently whispers hello to the crying star"


def c1p07():
    rng = random.Random(107)
    defs, o = ch1_sky(rng, avoid=[(540, 190, 170)])
    o += ch1_hills()
    o.append(back_grass(rng))
    o.append(fox(220, 562, 1.12, expr="sad", look=(4, 2)))
    o.append(daisy_big(420, 556, 1.3) + daisy_big(580, 556, 1.3))
    o.append(star(500, 508, 1.0, "sob", "dim", rot=6))
    tag = (g(circle(0, 0, 34, "#FFF7DC") + circle(-10, -6, 6, "#F4E8C2") + happy_eye(-10, 2, 10, 2.4) + happy_eye(10, 2, 10, 2.4)
             + smile(0, 13, 12, 2.4), 470, 190)
           + g(path(star_points(18, 9), fill=STAR, stroke=STAR, sw=6) + happy_eye(-4, 0, 6, 1.8) + happy_eye(4, 0, 6, 1.8), 586, 166, rot=-18)
           + motion(560, 176, 0.6, rot=0, c="#CFC6E6")
           + path("M600 184 Q640 220 626 262", stroke="#CFC6E6", sw=3, extra=' stroke-dasharray="2 9"')
           + g(path(star_points(10, 5), fill=STAR, stroke=STAR, sw=4), 626, 272, rot=40))
    o.append(bubble(540, 200, 250, 150, (500, 420), tag, "thought"))
    o.append(front_grass(rng))
    o.append(meadow_flowers([(60, 590), (720, 596)], 1.2))
    return defs, "".join(o), "Twinkle tells Pip how she slipped while playing tag with the moon"


def c1p08():
    rng = random.Random(108)
    defs = lin("sky", [(0, "#A99CD8"), (0.65, "#D9CFF1"), (1, "#F5DCD9")])
    o = [rect(0, 0, 800, 600, url("sky")), starfield(rng, 34, 30, 770, 24, 330, avoid=[(600, 80, 50)]), moon(120, 110, 30)]
    o.append(path("M600 62 L606 76 L621 77 L610 87 L613 102 L600 94 L587 102 L590 87 L579 77 L594 76 Z", fill="none",
                  stroke="#FFF6C8", sw=2.4, extra=' stroke-dasharray="4 5"'))
    o.append(path("M420 470 Q520 300 596 116", stroke="#FFF6C8", sw=2.6, extra=' stroke-dasharray="2 12"' + op(0.75)))
    o.append(path("M0 470 Q400 420 800 470 L800 600 L0 600 Z", fill="#C2DCD1"))
    o.append(path("M0 520 Q400 480 800 520 L800 600 L0 600 Z", fill="#AFD2C2"))
    o.append(rabbit(210, 560, 0.62, expr="sleepy", flip=False))
    o.append(motion(150, 520, 0.7, c="#F4ECF9"))
    o.append(mouse(300, 566, 0.52, look=(1, -3)))
    o.append(fox(410, 566, 0.92, expr="curious", look=(1, -5), head_rot=-12))
    o.append(star(520, 548, 0.5, "worried", "dim", look=(-1, -3)))
    o.append(front_grass(rng, 572, 610, 30))
    return defs, "".join(o), "Pip, Twinkle, a sleepy rabbit and a little mouse look up at the faraway sky"


def c1p09():
    rng = random.Random(109)
    defs, o = ch1_sky(rng, moon_at=world_at(110, 95, 410, 430, 1.1))
    o += ch1_hills()
    o.append(back_grass(rng))
    o.append(rabbit(200, 562, 0.72, expr="joy"))
    o.append(fox(390, 566, 1.3, pose="chest", expr="determined"))
    o.append(star(540, 506, 0.86, "hope", "dim", look=(-2, -1)))
    o.append(mouse(650, 566, 0.62, flip=True, expr="joy"))
    o.append(front_grass(rng))
    o.append(meadow_flowers([(60, 590), (480, 600), (760, 596)], 1.2))
    o.append(fireflies([(300, 330), (560, 300), (720, 380)]))
    return defs, cam("".join(o), 410, 430, 1.1), "Pip promises Twinkle that he and his friends will help her get home"


def c1p10():
    rng = random.Random(110)
    defs = lin("sky", [(0, "#C4BAE6"), (0.7, "#E4DCF5"), (1, "#F5DDDB")])
    o = [rect(0, 0, 800, 600, url("sky")), starfield(rng, 16, 40, 760, 30, 230, avoid=[(450, 330, 200)])]
    o.append(path("M0 420 Q400 360 800 420 L800 600 L0 600 Z", fill="#C2DCD1"))
    o.append(daisy_big(640, 600, 2.4))
    o.append(star(450, 340, 1.7, "smile", "normal", rot=-6))
    for sx, sy, r in [(330, 220, 12), (590, 230, 10), (600, 440, 9), (300, 450, 8), (450, 170, 9)]:
        o.append(sparkle(sx, sy, r, "#FFF6C8"))
    o.append(g(fox_head("joy"), 170, 668, 1.22))
    o.append(blades(rng, 26, 0, 800, 570, 612, 40, 90, ["#93C2AC", "#8BBDA6", "#9CCAB5"]))
    return defs, "".join(o), "Twinkle smiles and her light grows a little brighter while Pip smiles back"


# ------------------------------------------------------- fondos del cap. 2

def ch2_sky(rng, stars=16):
    defs = lin("sky", [(0, "#C1B5E6"), (0.6, "#E6DCF6"), (1, "#FFE2D4")])
    return defs, [rect(0, 0, 800, 600, url("sky")), starfield(rng, stars, 300, 780, 30, 200, avoid=[(640, 150, 60)])]


def ch2_hill():
    return (path("M330 440 Q470 380 560 210 Q620 110 690 210 Q760 320 800 360 L800 600 L330 600 Z", fill="#C2D8D2")
            + path("M600 168 Q610 230 580 290 Q560 340 600 400", stroke="#E3EEE9", sw=6, extra=' stroke-dasharray="2 14"')
            + sparkle(632, 150, 12, "#FFF6C8"))


def ch2_river(ducks=False, fish_jump=False, k=1.0):
    o = [path("M0 420 Q200 390 420 425 Q620 455 800 420 L800 600 L0 600 Z", fill="#C8E3D6")]
    o.append(berry_bush(648, 446, 0.62))
    o.append(path("M0 470 C200 440 400 500 800 455 L800 505 C400 550 200 490 0 522 Z", fill="#BFE0F5"))
    o.append(path("M60 478 Q90 472 120 478 M420 500 Q450 494 480 500 M700 470 Q725 465 750 470", stroke="#E3F2FC", sw=3))
    if ducks:
        o.append(duck2(252, 503, 0.55 * k, sing=True) + duck(252 + 44 * k, 506, 0.36 * k, baby=True)
                 + duck(252 + 78 * k, 504, 0.34 * k, baby=True))
    if fish_jump:
        o.append(fish(392 + 30 * (k - 1), 446, 0.66 * k, rot=-35))
        o.append(drop(366, 478, 0.55, "#E3F2FC") + drop(412, 476, 0.5, "#E3F2FC") + drop(390, 486, 0.42, "#E3F2FC")
                 + drop(350, 470, 0.4, "#E3F2FC"))
    o.append(path("M0 525 C200 495 400 548 800 505 L800 600 L0 600 Z", fill="#B3D7C6"))
    return "".join(o)


def owl_tree(owl_svg="", squirrel_svg=""):
    o = [path("M108 548 C122 450 118 330 136 250 L178 250 C190 330 186 450 206 548 Z", fill="#C9A98F")]
    o.append(path("M92 556 Q116 546 122 516 L192 516 Q200 546 226 556 Z", fill="#C9A98F"))
    o.append(ellipse(160, 557, 82, 9, "#A3CBB8"))
    o.append(path("M168 342 C220 326 270 322 336 300", stroke="#C9A98F", sw=18))
    o.append(path("M150 300 Q138 330 150 360", stroke="#B8977C", sw=4))
    canopy = [("c", 150, 140, 92), ("c", 66, 190, 58), ("c", 236, 172, 60), ("c", 104, 80, 56), ("c", 200, 74, 56)]
    o.append(cloud_layer(canopy, "#93BBAE", 8) + cloud_layer(canopy, "#A9CDBF"))
    o.append(circle(120, 120, 6, "#C3DDD3") + circle(190, 160, 5, "#C3DDD3") + circle(80, 200, 5, "#C3DDD3"))
    o.append(squirrel_svg + owl_svg)
    return "".join(o)


def ch2_tufts():
    return "".join(tuft(tx, ty, 1.1, "#98C6B1") for tx, ty in [(40, 560), (300, 575), (560, 590), (100, 562), (230, 566), (780, 575)])


# ------------------------------------------------------------ capítulo 2

def c2p01():
    rng = random.Random(201)
    defs, o = ch1_sky(rng, moon_at=world_at(110, 95, 420, 400, 1.15), stars=34, y1=330)
    o += ch1_hills()
    o.append(back_grass(rng))
    o.append(path("M470 330 Q500 250 520 160 Q536 100 560 60", stroke="#FFF6C8", sw=3, extra=' stroke-dasharray="2 12"' + op(0.8)))
    o.append(fox(400, 566, 1.3, pose="hold", expr="happy", look=(2, -3),
                 holding=star(0, -60, 0.66, "hope", "normal", look=(1, -3))))
    o.append(front_grass(rng))
    o.append(meadow_flowers([(90, 590), (250, 598), (620, 600), (740, 590)], 1.2))
    o.append(fireflies([(250, 330), (620, 280), (150, 420)]))
    return defs, cam("".join(o), 420, 400, 1.15), "Twinkle, held by Pip, asks where the closest place to the sky is"


def c2p02():
    rng = random.Random(202)
    defs, o = ch1_sky(rng, moon_at=world_at(700, 95, 380, 380, 1.12), avoid=[(212, 190, 120)])
    o += ch1_hills()
    o.append(back_grass(rng))
    o.append(rock(520, 560, 1.6))
    o.append(star(520, 494, 0.62, "hope", "normal", look=(-2, -2)))
    o.append(fox(330, 566, 1.25, pose="think", expr="think", look=(-2, -4)))
    owl_head = g(owl2(0, 0, 1.0, joy=True), 0, 0, 0.42)
    o.append(bubble(212, 190, 170, 120, (290, 330), g(owl_head, 212, 250), "thought"))
    o.append(sparkle(410, 240, 16, "#FFF6C8") + sparkle(440, 280, 9, "#FFF6C8"))
    o.append(front_grass(rng))
    o.append(meadow_flowers([(80, 590), (680, 600)], 1.2))
    return defs, cam("".join(o), 380, 380, 1.12), "Pip thinks and thinks, then remembers wise Grandpa Owl"


def c2p03():
    rng = random.Random(203)
    defs, o = ch2_sky(rng)
    o.append(ch2_hill())
    o.append(ch2_river())
    o.append(owl_tree(owl2(286, 308, 0.74, blink=True), squirrel(172, 424, 0.56, rot=96)))
    o.append(motion(176, 360, 0.7, rot=-90, c="#F4ECF9"))
    o.append(ch2_tufts())
    o.append(fox(470, 578, 1.0, pose="hold", expr="curious", look=(-3, -3), head_rot=-9,
                 holding=star(0, -60, 0.6, "happy", "normal", look=(-2, -2))))
    o.append(fireflies([(60, 470), (690, 385), (420, 360), (250, 420)]))
    return defs, "".join(o), "Pip carries Twinkle to the oldest tree, where a squirrel runs down and Grandpa Owl blinks"


def c2p04():
    rng = random.Random(204)
    defs, o = ch2_sky(rng)
    o.append(ch2_hill())
    o.append(ch2_river())
    o.append(owl_tree(owl2(286, 308, 0.74, talk=True, wing="point"), squirrel(206, 327, 0.46)))
    o.append(ch2_tufts())
    o.append(fox(460, 566, 0.88, pose="hold", expr="curious", look=(-3, -3), head_rot=-10,
                 holding=star(0, -60, 0.6, "hope", "normal", look=(-2, -2))))
    o.append(sparkle(540, 260, 10, "#FFF6C8", 0.9) + sparkle(470, 300, 7, "#FFF6C8", 0.8))
    return defs, cam("".join(o), 390, 330, 1.2), "Grandpa Owl points toward the Tallest Hill and the river"


def c2p05():
    rng = random.Random(205)
    defs, o = ch2_sky(rng)
    o.append(ch2_hill())
    o.append(ch2_river(ducks=True, fish_jump=True, k=1.3))
    o.append(note(232, 446, 0.8, "#F4ECF9") + note(206, 424, 0.62, "#F4ECF9", rot=10))
    o.append(sound(286, 460, 0.8, rot=-20))
    o.append(ch2_tufts())
    o.append(fox(118, 586, 0.84, pose="hold", expr="joy",
                 holding=star(0, -60, 0.6, "smile", "normal")))
    o.append(fireflies([(200, 260), (330, 230), (470, 300), (90, 330)]))
    return defs, cam("".join(o), 330, 420, 1.3), "A duck family swims and quacks while a silver fish jumps out of the river"


def c2p06():
    rng = random.Random(206)
    defs, o = ch2_sky(rng)
    o.append(ch2_hill())
    o.append(ch2_river())
    o.append(ch2_tufts())
    o.append(fox(470, 580, 1.05, pose="hold", expr="worried", look=(1, -1),
                 holding=star(0, -60, 0.6, "worried", "normal")))
    return defs, cam("".join(o), 520, 440, 1.3), "Pip stands at the river and wonders how they can cross"


def c2p07():
    rng = random.Random(207)
    defs, o = ch2_sky(rng)
    o.append(ch2_hill())
    o.append(ch2_river())
    o.append(log_bridge(536, 540, 650, 452, 20))
    o.append(beaver(500, 568, 0.66))
    o.append(motion(456, 530, 0.8, c="#F4ECF9"))
    o.append(sparkle(600, 470, 10, "#FFF6C8") + sparkle(660, 440, 8, "#FFF6C8") + sparkle(570, 510, 7, "#FFF6C8"))
    o.append(ch2_tufts())
    o.append(fox(330, 580, 1.0, pose="hold", expr="surprised", look=(4, -1),
                 holding=star(0, -60, 0.6, "talk", "normal", look=(2, 0))))
    return defs, cam("".join(o), 480, 450, 1.25), "A busy beaver pushes a big log across the river to make a bridge"


def far_bank(rng):
    defs, o = ch2_sky(rng, 20)
    o.append(path("M300 460 Q450 360 560 180 Q630 70 700 180 Q770 300 800 330 L800 600 L300 600 Z", fill="#C2D8D2"))
    o.append(path("M628 140 Q640 210 610 280 Q590 330 630 400", stroke="#E3EEE9", sw=6, extra=' stroke-dasharray="2 14"'))
    o.append(sparkle(660, 120, 12, "#FFF6C8"))
    o.append(path("M0 380 Q300 360 800 390 L800 430 Q300 400 0 420 Z", fill="#BFE0F5"))
    o.append(log_bridge(40, 430, 120, 376, 10))
    o.append(path("M0 418 Q300 398 800 428 L800 600 L0 600 Z", fill="#C8E3D6"))
    o.append(path("M0 520 Q400 490 800 525 L800 600 L0 600 Z", fill="#B3D7C6"))
    return defs, o


def c2p08():
    rng = random.Random(208)
    defs, o = far_bank(rng)
    o.append(berry_bush(640, 530, 1.25))
    o.append(bear2(540, 552, 0.82, pose="berries", expr="munch"))
    o.append(fox(250, 566, 1.0, pose="hold", expr="surprised", look=(5, -2),
                 holding=star(0, -60, 0.6, "hope", "normal", look=(3, 0))))
    o.append("".join(tuft(tx, ty, 1.1, "#98C6B1") for tx, ty in [(60, 560), (380, 570), (730, 580)]))
    return defs, "".join(o), "On the other side of the river, Pip meets a big brown bear eating berries"


def c2p09():
    rng = random.Random(209)
    defs, o = far_bank(rng)
    o.append(berry_bush(660, 530, 1.1))
    o.append(bear2(520, 552, 0.82, pose="point", expr="talk"))
    o.append(fox(250, 566, 1.0, pose="hold", expr="joy", head_rot=-6,
                 holding=star(0, -60, 0.6, "smile", "normal")))
    o.append(sparkle(600, 250, 10, "#FFF6C8", 0.9) + sparkle(640, 200, 8, "#FFF6C8", 0.8))
    o.append("".join(tuft(tx, ty, 1.1, "#98C6B1") for tx, ty in [(60, 560), (380, 570), (730, 580)]))
    return defs, "".join(o), "The bear points his paw toward the Tallest Hill and tells Pip to be brave"


def slope(rng, stars=28):
    defs = lin("sky", [(0, "#B3A7DD"), (0.6, "#DED4F3"), (1, "#FAE0D6")])
    o = [rect(0, 0, 800, 600, url("sky")), starfield(rng, stars, 30, 770, 24, 330, avoid=[(700, 90, 60)])]
    o.append(path("M0 600 L0 540 Q260 500 470 360 Q600 270 800 230 L800 600 Z", fill="#C2D8D2"))
    o.append(path("M60 560 Q300 500 470 390 Q600 300 780 262", stroke="#E3EEE9", sw=6, extra=' stroke-dasharray="2 14"'))
    o.append(path("M0 600 L0 580 Q300 560 520 440 Q660 360 800 330 L800 600 Z", fill="#B3D7C6"))
    return defs, o


def c2p10():
    rng = random.Random(210)
    defs, o = slope(rng)
    o.append(rock(250, 560, 1.3) + rock(650, 420, 1.0))
    o.append("".join(tuft(tx, ty, 1.0, "#98C6B1") for tx, ty in [(120, 590), (560, 470), (720, 400), (330, 545)]))
    o.append(fox(430, 486, 1.1, pose="hold", expr="tired", lean=10,
                 holding=star(0, -60, 0.6, "talk", "normal", look=(0, -2))))
    o.append(sparkle(520, 330, 8, "#FFF6C8") + sparkle(540, 360, 5, "#FFF6C8"))
    return defs, cam("".join(o), 440, 380, 1.15), "Pip is tired but keeps climbing while Twinkle tells him he is very brave"


def c2p11():
    rng = random.Random(211)
    defs = lin("sky", [(0, "#A99CD8"), (0.6, "#D7CCF0"), (1, "#F9D9D2")])
    o = [rect(0, 0, 800, 600, url("sky")), starfield(rng, 36, 30, 770, 24, 300, avoid=[(560, 300, 120)])]
    for sx, sy, r in [(120, 80, 13), (300, 60, 11), (480, 110, 14), (700, 70, 12)]:
        o.append(sparkle(sx, sy, r, "#FFF6C8"))
    # el valle allá abajo: el río y el árbol del búho, chiquitos
    o.append(path("M0 420 Q200 400 420 430 L420 600 L0 600 Z", fill="#CFE3DC"))
    o.append(path("M0 470 C120 456 260 486 420 466 L420 480 C260 500 120 470 0 486 Z", fill="#BFE0F5"))
    o.append(round_tree(110, 452, 0.62, "#A9CDBF", "#93BBAE") + round_tree(200, 444, 0.42, "#A9CDBF", "#93BBAE"))
    o.append(path("M0 600 L0 560 Q200 540 360 470 Q520 380 640 300 Q720 250 800 236 L800 600 Z", fill="#C2D8D2"))
    o.append(path("M180 560 Q340 500 470 410 Q580 330 700 272", stroke="#E3EEE9", sw=6, extra=' stroke-dasharray="2 14"'))
    o.append(path("M0 600 L0 590 Q300 580 520 470 Q660 390 800 360 L800 600 Z", fill="#B3D7C6"))
    o.append(fox(560, 392, 1.0, pose="step", expr="joy", lean=12))
    o.append(star(700, 236, 0.6, "smile", "normal"))
    o.append(rock(420, 500, 1.0) + tuft(700, 380, 1.0, "#98C6B1") + tuft(320, 540, 1.0, "#98C6B1"))
    return defs, "".join(o), "Step by step, Pip and Twinkle climb higher and higher above the valley"


# ------------------------------------------------------- fondos del cap. 3

def ch3_sky(rng, stars=40, avoid=()):
    defs = lin("sky", [(0, "#A99CD8"), (0.6, "#D7CCF0"), (1, "#F9D9D2")])
    return defs, [rect(0, 0, 800, 600, url("sky")), starfield(rng, stars, 30, 770, 25, 380, avoid=list(avoid))]


def ch3_hill():
    return [path("M0 500 Q200 450 400 490 Q600 525 800 470 L800 600 L0 600 Z", fill="#CBE0D9"),
            path("M0 600 L0 520 Q300 400 600 470 Q700 492 800 520 L800 600 Z", fill="#B3D7C6")]


def ch3_decor():
    o = [tuft(tx, ty, 1.1, "#98C6B1") for tx, ty in [(110, 545), (380, 470), (520, 500), (650, 525), (740, 565), (250, 520)]]
    o += [flower(fx, fy, 1.1, c) for fx, fy, c in [(120, 560, "#F7B7C3"), (556, 566, "#FFF1BF"), (610, 530, "#E4DCF7"), (700, 560, "#F7B7C3")]]
    return "".join(o)


def big_stars(pts):
    return "".join(sparkle(x, y, r, "#FFF6C8") + circle(x, y, r * 2.2, url("glow"), op(0.5)) for x, y, r in pts)


# ------------------------------------------------------------ capítulo 3

def c3p01():
    rng = random.Random(301)
    defs, o = ch3_sky(rng, 46, avoid=[(400, 330, 130)])
    o.append(big_stars([(150, 120, 16), (330, 70, 14), (520, 110, 18), (680, 180, 15), (250, 230, 12), (600, 260, 11)]))
    o += ch3_hill()
    o.append(ch3_decor())
    o.append(fox(380, 478, 1.3, pose="hold", expr="surprised", look=(1, -5), head_rot=-6,
                 holding=star(0, -60, 0.62, "hope", "normal", look=(1, -3))))
    return defs, "".join(o), "Pip reaches the top of the Tallest Hill, where the stars look so close"


def c3p02():
    rng = random.Random(302)
    defs, o = ch3_sky(rng, 40)
    o.append(big_stars([(150, 120, 14), (520, 90, 16), (680, 180, 13)]))
    o += ch3_hill()
    o.append(ch3_decor())
    o.append(fox(400, 520, 1.3, pose="hold", expr="worried", look=(0, 2),
                 holding=star(0, -60, 0.62, "worried", "dim")))
    return defs, cam("".join(o), 400, 380, 1.6), "Twinkle is worried she is too dim to fly back up"


def c3p03():
    rng = random.Random(303)
    defs, o = ch3_sky(rng, 40)
    o.append(big_stars([(150, 120, 14), (620, 110, 16)]))
    o += ch3_hill()
    o.append(ch3_decor())
    o.append(fox(400, 500, 1.3, pose="hold", expr="joy",
                 holding=star(0, -60, 0.62, "hope", "dim", look=(0, -2))))
    o.append(circle(400, 210, 46, url("glow")) + sparkle(400, 210, 22, "#FFF6C8")
             + path("M400 166 L400 150 M444 210 L460 210 M356 210 L340 210 M432 178 L444 166 M368 178 L356 166",
                    stroke="#FFF6C8", sw=4))
    return defs, cam("".join(o), 400, 340, 1.3), "Pip has an idea: maybe Twinkle needs to feel happy to shine bright"


def c3p04():
    rng = random.Random(304)
    defs, o = ch3_sky(rng, 34, avoid=[(660, 220, 90)])
    o += ch3_hill()
    o.append(ch3_decor())
    o.append(owl2(660, 290, 0.44, wing="fly", joy=True))
    o.append(deer(52, 500, 0.54))
    o.append(motion(40, 440, 0.8, c="#F4ECF9"))
    o.append(bear2(690, 506, 0.5, expr="joy"))
    o.append(squirrel(722, 540, 0.46, flip=True))
    o.append(duck2(612, 492, 0.42, swim=False, flip=True) + duck2(648, 500, 0.32, baby=True, swim=False, flip=True))
    o.append(motion(760, 470, 0.8, rot=180, c="#F4ECF9"))
    o.append(rabbit(150, 470, 0.56, expr="joy"))
    o.append(motion(108, 420, 0.7, c="#F4ECF9"))
    o.append(mouse(232, 512, 0.48, expr="joy"))
    o.append(frog2(292, 470, 0.48, expr="joy", pose="jump"))
    o.append(rock(536, 486, 1.1))
    o.append(star(536, 444, 0.42, "smile", "normal"))
    o.append(fox(380, 462, 1.1, pose="wave", expr="joy", head_rot=-4))
    return defs, "".join(o), "All of Pip's friends arrive on the hilltop to help"


def c3p05():
    rng = random.Random(305)
    defs, o = ch3_sky(rng, 34, avoid=[(160, 260, 90)])
    o += ch3_hill()
    o.append(ch3_decor())
    o.append(deer(46, 470, 0.42) + owl2(728, 474, 0.3, joy=True))
    o.append(bear2(150, 500, 0.56, pose="joke", expr="talk"))
    o.append(bubble(160, 270, 120, 90, (176, 380), honey_pot(160, 296, 1.0) + sparkle(204, 252, 8, "#F7C873"), "speech"))
    o.append(fox(330, 470, 0.92, pose="hold", expr="joy", holding=star(0, -60, 0.6, "smile", "normal")))
    o.append(frog2(450, 508, 0.66, expr="joy", pose="dance"))
    o.append(note(420, 410, 0.8, "#F4ECF9") + note(490, 392, 0.7, "#F4ECF9", rot=12))
    o.append(rabbit(520, 520, 0.46, expr="joy", flip=True))
    o.append(duck2(618, 500, 0.5, swim=False, flip=True, sing=True) + duck2(670, 512, 0.38, baby=True, swim=False, flip=True, sing=True))
    o.append(note(600, 420, 0.8, "#F4ECF9", rot=-10) + note(650, 404, 0.65, "#F4ECF9") + note(700, 430, 0.6, "#F4ECF9", rot=8))
    o.append(mouse(250, 528, 0.42, expr="joy"))
    o.append(squirrel(720, 548, 0.4, flip=True))
    return defs, "".join(o), "The frog dances, the ducks sing a silly song and the bear tells a joke about honey"


def c3p06():
    rng = random.Random(306)
    defs, o = ch3_sky(rng, 30, avoid=[(400, 260, 190)])
    o += ch3_hill()
    o.append(ch3_decor())
    o.append(star(400, 262, 1.15, "bright", "huge"))
    o.append(deer(46, 486, 0.44) + owl2(726, 484, 0.32, joy=True))
    o.append(bear2(150, 504, 0.52, expr="joy"))
    o.append(rabbit(250, 520, 0.5, expr="joy"))
    o.append(fox(400, 540, 1.0, pose="cheer", expr="joy"))
    o.append(frog2(520, 520, 0.55, expr="joy"))
    o.append(duck2(600, 506, 0.46, swim=False, flip=True, sing=True) + duck2(646, 514, 0.34, baby=True, swim=False, flip=True))
    o.append(mouse(312, 548, 0.42, expr="joy") + squirrel(690, 548, 0.42, flip=True))
    for sx, sy in [(200, 400), (560, 410), (320, 440), (470, 430)]:
        o.append(sound(sx, sy, 0.5, rot=-60, c="#FFF6C8"))
    return defs, "".join(o), "Everyone laughs, and with every laugh Twinkle glows brighter and brighter"


def c3p07():
    rng = random.Random(307)
    defs, o = ch3_sky(rng, 30, avoid=[(400, 210, 170)])
    o += ch3_hill()
    o.append(ch3_decor())
    o.append(star(400, 220, 1.05, "talk", "big", look=(0, 2)))
    o.append(trail([(400, 420), (402, 380), (400, 340), (398, 310)]))
    o.append(rabbit(150, 520, 0.5, expr="happy") + bear2(250, 516, 0.5, expr="happy"))
    o.append(fox(400, 534, 1.05, pose="cheer", expr="joy", head_rot=0))
    o.append(frog2(540, 520, 0.5) + duck2(620, 510, 0.44, swim=False, flip=True))
    o.append(mouse(320, 548, 0.42, look=(1, -3)) + deer(700, 520, 0.4, flip=True))
    return defs, "".join(o), "Twinkle begins to float and thanks Pip and everyone"


def c3p08():
    rng = random.Random(308)
    defs, o = ch3_sky(rng, 44, avoid=[(560, 120, 110)])
    o.append(star(560, 120, 0.62, "bright", "big"))
    o.append(trail([(390, 450), (410, 400), (432, 350), (456, 300), (482, 250), (510, 200), (536, 160)]))
    o.append(path("M0 540 Q200 500 400 520 Q600 540 800 510 L800 600 L0 600 Z", fill="#CBE0D9"))
    o.append(path("M0 600 L0 560 Q300 490 600 530 Q700 545 800 560 L800 600 Z", fill="#B3D7C6"))
    o.append(rabbit(250, 548, 0.32, expr="joy") + bear2(320, 548, 0.3, expr="joy") + fox(400, 552, 0.55, pose="wave", expr="joy")
             + frog2(470, 548, 0.3, expr="joy") + duck2(520, 545, 0.28, swim=False, flip=True) + deer(580, 552, 0.28, flip=True))
    return defs, "".join(o), "Up, up, up Twinkle flies until she finds her place in the sky"


def c3p09():
    rng = random.Random(309)
    defs, o = ch3_sky(rng, 46, avoid=[(560, 130, 80)])
    o.append(wink_star(560, 130, 1.2))
    o += ch3_hill()
    o.append(ch3_decor())
    o.append(bear2(150, 506, 0.52, pose="cheer", expr="joy"))
    o.append(rabbit(250, 500, 0.5, expr="joy") + motion(250, 520, 0.5, rot=-90, c="#F4ECF9"))
    o.append(fox(390, 520, 1.0, pose="cheer", expr="joy", look=(2, -3)))
    o.append(frog2(510, 500, 0.5, expr="joy", pose="dance"))
    o.append(duck2(590, 500, 0.44, swim=False, flip=True, sing=True) + owl2(700, 486, 0.32, wing="fly", joy=True))
    o.append(mouse(300, 548, 0.42, expr="joy") + squirrel(660, 548, 0.42, flip=True) + deer(40, 486, 0.42))
    return defs, "".join(o), "The animals cheer as one little star winks at them"


def c3p10():
    rng = random.Random(310)
    defs, o = ch1_sky(rng, moon_at=(120, 100), stars=30, avoid=[(600, 110, 70)])
    o.append(wink_star(600, 110, 0.9))
    o.append(forest_edge(rng))
    o += ch1_hills()
    o.append(back_grass(rng, 0, 800, 430, 470, 34))
    o.append(den(620, 520, 1.15))
    o.append(fox(460, 552, 0.92, expr="wink", look=(2, -4), head_rot=-10))
    o.append(meadow_flowers([(80, 590), (300, 598), (760, 590)], 1.1))
    o.append(front_grass(rng, 576, 612, 30))
    o.append(fireflies([(380, 330), (240, 420), (720, 380)]))
    return defs, "".join(o), "Every night before he goes to sleep, Pip looks up and winks back at the star"


def c3p11():
    rng = random.Random(311)
    defs, o = ch1_sky(rng, moon_at=(120, 100), stars=30, avoid=[(600, 110, 70)])
    o.append(star(600, 110, 0.5, "smile", "normal"))
    o.append(forest_edge(rng))
    o += ch1_hills()
    o.append(back_grass(rng, 0, 800, 430, 470, 34))
    o.append(den(560, 520, 1.15))
    o.append(fox_sleeping(560, 540, 0.95))
    o.append(rabbit(330, 556, 0.5, expr="sleepy") + mouse(420, 566, 0.42, expr="sleepy"))
    o.append(meadow_flowers([(80, 590), (250, 598), (760, 590)], 1.1))
    o.append(front_grass(rng, 576, 612, 30))
    o.append(fireflies([(380, 330), (240, 420), (720, 380), (470, 300)]))
    return defs, "".join(o), "Pip and his friends fall asleep under the stars. The End"


CHAPTERS = {
    1: [c1p01, c1p02, c1p03, c1p04, c1p05, c1p06, c1p07, c1p08, c1p09, c1p10],
    2: [c2p01, c2p02, c2p03, c2p04, c2p05, c2p06, c2p07, c2p08, c2p09, c2p10, c2p11],
    3: [c3p01, c3p02, c3p03, c3p04, c3p05, c3p06, c3p07, c3p08, c3p09, c3p10, c3p11],
}


def main():
    only = set(sys.argv[1:])  # p.ej. "2/5" para regenerar una sola escena
    for ch, fns in CHAPTERS.items():
        for i, fn in enumerate(fns, start=1):
            key = f"{ch}/{i}"
            if only and key not in only:
                continue
            mi._P = f"pip-ch{ch}-p{i:02d}"
            defs, body, title = fn()
            out, size = mi.write_svg("pip", f"ch{ch}/p{i:02d}", 800, 600, title, defs, body)
            print(f"{os.path.relpath(out, mi.ROOT)}  {size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
