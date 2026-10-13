#!/usr/bin/env python3
"""Genera las 12 ilustraciones SVG de los cuentos.

Cada personaje se dibuja una sola vez como función (posición, escala, pose,
expresión) y las escenas lo componen, así se ve igual en todos los capítulos.
Solo usa la librería estándar:

    python3 tools/make_illustrations.py
"""
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLUM = "#3B3355"
BLUSH = "#F7B7C3"
WHITE = "#FFFFFF"
LEAF = "#A8DDB5"
STEM = "#8CCB9B"

_P = "x"  # prefijo de ids del archivo que se está generando


def uid(name):
    return f"{_P}-{name}"


def url(name):
    return f"url(#{uid(name)})"


def n(v):
    if isinstance(v, float):
        s = f"{v:.1f}"
        return s[:-2] if s.endswith(".0") else s
    return str(v)


# ---------------------------------------------------------------- primitivas

def op(o):
    return f' opacity="{n(float(o))}"'


def circle(cx, cy, r, fill, extra=""):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"{extra}/>'


def ellipse(cx, cy, rx, ry, fill, rot=0, extra=""):
    t = f' transform="rotate({n(rot)} {n(cx)} {n(cy)})"' if rot else ""
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="{fill}"{t}{extra}/>'


def rect(x, y, w, h, fill, rx=0, extra=""):
    r = f' rx="{n(rx)}"' if rx else ""
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"{r} fill="{fill}"{extra}/>'


def path(d, fill="none", stroke=None, sw=None, extra=""):
    s = f' stroke="{stroke}" stroke-width="{n(sw)}"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{s}{extra}/>'


def g(body, x=0, y=0, s=1.0, flip=False, rot=0, opacity=None):
    t = []
    if x or y:
        t.append(f"translate({n(x)} {n(y)})")
    if rot:
        t.append(f"rotate({n(rot)})")
    if s != 1 or flip:
        t.append(f"scale({n(-s if flip else s)} {n(s)})")
    attrs = f' transform="{" ".join(t)}"' if t else ""
    if opacity is not None:
        attrs += op(opacity)
    return f"<g{attrs}>{body}</g>"


def rotated(body, deg, cx, cy):
    return f'<g transform="rotate({n(deg)} {n(cx)} {n(cy)})">{body}</g>'


# ------------------------------------------------------------------- caras

def eye(x, y, r=5.5, look=(0, 0)):
    x, y = x + look[0], y + look[1]
    return circle(x, y, r, PLUM) + circle(x + r * 0.35, y - r * 0.38, r * 0.36, WHITE)


def happy_eye(x, y, w=11, sw=3):
    return path(f"M{n(x - w / 2)} {n(y + 2)} Q{n(x)} {n(y - w * 0.55)} {n(x + w / 2)} {n(y + 2)}", stroke=PLUM, sw=sw)


def calm_eye(x, y, w=11, sw=3):
    return path(f"M{n(x - w / 2)} {n(y - 2)} Q{n(x)} {n(y + w * 0.5)} {n(x + w / 2)} {n(y - 2)}", stroke=PLUM, sw=sw)


def blush(x, y, rx=8, ry=5, o=0.75):
    return ellipse(x, y, rx, ry, BLUSH, extra=op(o))


def smile(x, y, w=12, sw=3, depth=0.45):
    return path(f"M{n(x - w / 2)} {n(y)} Q{n(x)} {n(y + w * depth)} {n(x + w / 2)} {n(y)}", stroke=PLUM, sw=sw)


def frown(x, y, w=12, sw=3):
    return path(f"M{n(x - w / 2)} {n(y + w * 0.2)} Q{n(x)} {n(y - w * 0.25)} {n(x + w / 2)} {n(y + w * 0.2)}", stroke=PLUM, sw=sw)


def open_mouth(x, y, w=14):
    return (path(f"M{n(x - w / 2)} {n(y)} Q{n(x)} {n(y + w * 0.95)} {n(x + w / 2)} {n(y)} Z", fill=PLUM, stroke=PLUM, sw=2)
            + ellipse(x, y + w * 0.42, w * 0.22, w * 0.14, "#F49AB0"))


# ------------------------------------------------------------ decoraciones

def sparkle(x, y, r, fill="#FFFFFF", o=1.0):
    k = r * 0.22
    d = (f"M{n(x)} {n(y - r)} Q{n(x + k)} {n(y - k)} {n(x + r)} {n(y)} "
         f"Q{n(x + k)} {n(y + k)} {n(x)} {n(y + r)} Q{n(x - k)} {n(y + k)} {n(x - r)} {n(y)} "
         f"Q{n(x - k)} {n(y - k)} {n(x)} {n(y - r)} Z")
    return path(d, fill=fill, extra=op(o) if o != 1 else "")


def drop(x, y, s=1.0, fill="#9CCBEF"):
    return g(path("M0 -11 C4 -5 7 -1 7 3 A7 7 0 0 1 -7 3 C-7 -1 -4 -5 0 -11 Z", fill=fill), x, y, s)


def tuft(x, y, s=1.0, color="#93C2AC"):
    return g(path("M-9 0 Q-8 -10 -13 -17 M0 0 Q-1 -13 2 -22 M9 0 Q9 -9 14 -15", stroke=color, sw=3.4), x, y, s)


def blade(x, y, h, lean, color):
    return path(f"M{n(x - 5)} {n(y)} Q{n(x + lean * 0.4 - 2)} {n(y - h * 0.55)} {n(x + lean)} {n(y - h)} "
                f"Q{n(x + lean * 0.4 + 3)} {n(y - h * 0.5)} {n(x + 5)} {n(y)} Z", fill=color)


def blades(rng, count, x0, x1, y0, y1, hmin, hmax, colors):
    out = []
    for _ in range(count):
        out.append(blade(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(hmin, hmax),
                         rng.uniform(-14, 14), rng.choice(colors)))
    return "".join(out)


def leaf(x, y, length, rot, fill=LEAF, vein=STEM):
    L = length
    d = (f"M0 0 C{n(L * 0.25)} {n(-L * 0.38)} {n(L * 0.75)} {n(-L * 0.38)} {n(L)} 0 "
         f"C{n(L * 0.75)} {n(L * 0.38)} {n(L * 0.25)} {n(L * 0.38)} 0 0 Z")
    return g(path(d, fill=fill) + path(f"M3 0 L{n(L * 0.8)} 0", stroke=vein, sw=2), x, y, rot=rot)


def starfield(rng, count, x0, x1, y0, y1, avoid=(), color="#FFFBEA"):
    pts, tries = [], 0
    while len(pts) < count and tries < count * 40:
        tries += 1
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if any((px - ax) ** 2 + (py - ay) ** 2 < ar ** 2 for ax, ay, ar in avoid):
            continue
        if any((px - qx) ** 2 + (py - qy) ** 2 < 30 ** 2 for qx, qy in pts):
            continue
        pts.append((px, py))
    out = []
    for i, (px, py) in enumerate(pts):
        if i % 3 == 0:
            out.append(sparkle(px, py, rng.uniform(5, 9), color, 0.95))
        else:
            out.append(circle(px, py, rng.uniform(1.5, 2.7), color, op(rng.uniform(0.6, 1))))
    return "".join(out)


def moon(x, y, r):
    c = "#F4E8C2"
    return (circle(x, y, r * 2.3, url("soft"), op(0.75)) + circle(x, y, r, "#FFF7DC")
            + circle(x - r * 0.3, y - r * 0.15, r * 0.2, c) + circle(x + r * 0.35, y + r * 0.32, r * 0.13, c)
            + circle(x + r * 0.2, y - r * 0.45, r * 0.1, c))


def sun(x, y, r):
    return circle(x, y, r * 2.4, url("glow"), op(0.9)) + circle(x, y, r, "#FFE38A") + circle(x - r * 0.15, y - r * 0.15, r * 0.72, "#FFEDAE")


# rojo, naranja, amarillo, verde, azul y morado (en pastel)
RAINBOW = ["#F5A3AE", "#FFC59A", "#FFE99A", "#B3E2BC", "#A9D1F0", "#CBBCEF"]


def rainbow(cx, cy, R, w, o=0.95):
    out = []
    for i, c in enumerate(RAINBOW):
        r = R - w / 2 - i * w
        out.append(f'<path d="M{n(cx - r)} {n(cy)} A{n(r)} {n(r)} 0 0 1 {n(cx + r)} {n(cy)}" fill="none" '
                   f'stroke="{c}" stroke-width="{n(w + 0.8)}" stroke-linecap="butt"/>')
    return g("".join(out), opacity=o)


# ------------------------------------------------------------------- nubes

CLOUD_S = [("r", -80, -6, 160, 40, 20), ("c", -44, -8, 32), ("c", -4, -28, 42), ("c", 38, -10, 32)]
CLOUD_B = [("r", -150, -10, 300, 64, 32), ("c", -98, -14, 50), ("c", -36, -50, 70), ("c", 42, -40, 62), ("c", 104, -8, 44)]
CLOUD_T = [("r", -60, -4, 120, 30, 15), ("c", -28, -6, 24), ("c", 4, -20, 30), ("c", 32, -6, 22)]


def cloud_layer(shape, fill, dy=0):
    out = []
    for sh in shape:
        if sh[0] == "r":
            out.append(rect(sh[1], sh[2] + dy, sh[3], sh[4], fill, rx=sh[5]))
        else:
            out.append(circle(sh[1], sh[2] + dy, sh[3], fill))
    return "".join(out)


def cloud(x, y, s=1.0, shape=CLOUD_T, fill=WHITE, shade="#E6E0F5", o=None, flip=False):
    return g(cloud_layer(shape, shade) + cloud_layer(shape, fill, -7), x, y, s, flip=flip, opacity=o)


def nimbus(x, y, s=1.0, expr="happy", rain=False):
    """Nimbus: la nube pequeña."""
    out = []
    if rain:
        for dx, dy in [(-52, 66), (-22, 90), (8, 62), (38, 88), (-38, 122), (-6, 114), (26, 128), (56, 118)]:
            out.append(drop(dx, dy, 0.9, "#A3CDF0"))
    out.append(cloud_layer(CLOUD_S, "#E4DCF7") + cloud_layer(CLOUD_S, WHITE, -7))
    if expr == "strain":
        out.append(path("M-23 -5 L-12 2 L-23 9", stroke=PLUM, sw=3) + path("M23 -5 L12 2 L23 9", stroke=PLUM, sw=3))
        out.append(circle(-35, 13, 10, BLUSH, op(0.9)) + circle(35, 13, 10, BLUSH, op(0.9)))
        out.append(path("M-8 17 Q-4 13 0 17 Q4 21 8 17", stroke=PLUM, sw=2.8))
        out.append(path("M68 -34 L80 -44 M74 -18 L88 -21 M58 -46 L62 -58", stroke="#A9BCD8", sw=3.2))
        out.append(drop(-80, -40, 0.75, "#B9DCF6"))
    elif expr == "sad":
        out.append(eye(-17, 4, 5.5, (0, 1)) + eye(17, 4, 5.5, (0, 1)))
        out.append(path("M-25 -9 L-11 -12", stroke=PLUM, sw=2.6) + path("M25 -9 L11 -12", stroke=PLUM, sw=2.6))
        out.append(blush(-33, 14, 7, 4.5) + blush(33, 14, 7, 4.5))
        out.append(frown(0, 17, 12, 2.8))
    elif expr == "joy":
        out.append(happy_eye(-17, 2, 13) + happy_eye(17, 2, 13))
        out.append(blush(-33, 13, 8, 5) + blush(33, 13, 8, 5))
        out.append(open_mouth(0, 11, 16))
    else:
        out.append(eye(-17, 2, 5.8) + eye(17, 2, 5.8))
        out.append(blush(-33, 13, 8, 5) + blush(33, 13, 8, 5))
        out.append(smile(0, 12, 14, 3))
    return g("".join(out), x, y, s)


def big_cloud(x, y, s=1.0, face="none", fill="#C9D3E6", shade="#AEBBD3", flip=False):
    """Nubes grandes de lluvia (Mamá Cúmulo cuando face='kind')."""
    out = [cloud_layer(CLOUD_B, shade), cloud_layer(CLOUD_B, fill, -9)]
    if face == "kind":
        out.append(happy_eye(-30, 8, 18, 3.6) + happy_eye(30, 8, 18, 3.6))
        out.append(blush(-56, 24, 12, 7) + blush(56, 24, 12, 7))
        out.append(smile(0, 24, 22, 3.6))
    elif face == "sleepy":
        out.append(calm_eye(-28, 8, 16, 3.4) + calm_eye(28, 8, 16, 3.4))
        out.append(blush(-52, 22, 11, 6) + blush(52, 22, 11, 6))
        out.append(smile(0, 24, 14, 3.2))
    return g("".join(out), x, y, s, flip=flip)


def rain_field(rng, x0, x1, y0, y1, count, fill="#A9CBEA", s=0.85):
    return "".join(drop(rng.uniform(x0, x1), rng.uniform(y0, y1), s, fill) for _ in range(count))


# --------------------------------------------------------------------- Pip

FOX = "#F4A06B"
FOX_D = "#E68E5C"
FOX_CREAM = "#FFF4E8"
FOX_PAW = "#D98763"
FOX_LIMB = "#EE9761"
EAR_PINK = "#F8C2B4"


def pip(x, y, s=1.0, flip=False, pose="sit", expr="happy", look=(0, 0), head_rot=0, holding="", lean=0):
    """Pip, el zorrito. Origen: entre las patas, a nivel del suelo."""
    o = []
    o.append('<g transform="rotate(32 62 -62)">' + ellipse(62, -62, 31, 62, FOX_CREAM) + ellipse(62, -50, 32, 51, FOX) + "</g>")
    o.append(ellipse(-32, -24, 20, 26, FOX_D) + ellipse(32, -24, 20, 26, FOX_D))
    o.append(ellipse(0, -54, 46, 52, FOX))
    o.append(ellipse(0, -46, 28, 38, FOX_CREAM))
    o.append(ellipse(-34, -7, 18, 9, FOX_PAW) + ellipse(34, -7, 18, 9, FOX_PAW))

    def leg(sx):
        return rect(sx * 19 - 7, -60, 14, 54, FOX_LIMB, rx=7) + ellipse(sx * 19, -7, 10, 7, FOX_PAW)

    def arm_hold(sx):
        return path(f"M{sx * 34} -84 Q{sx * 42} -66 {sx * 29} -60", stroke=FOX_LIMB, sw=15) + circle(sx * 28, -60, 8.5, FOX_PAW)

    if pose == "hold":
        o.append(holding + arm_hold(-1) + arm_hold(1))
    elif pose == "wave":
        o.append(leg(-1))
        o.append(path("M28 -84 Q56 -98 60 -130", stroke=FOX_LIMB, sw=15) + circle(60, -133, 9.5, FOX_PAW))
        o.append(path("M76 -150 Q84 -140 80 -128 M86 -160 Q98 -142 92 -124", stroke="#FFFFFF", sw=3, extra=op(0.8)))
    elif pose == "step":
        o.append(leg(-1))
        o.append(path("M19 -58 Q22 -40 34 -36", stroke=FOX_LIMB, sw=14) + circle(35, -35, 7.5, FOX_PAW))
    else:
        o.append(leg(-1) + leg(1))

    h = []
    for sx in (-1, 1):
        h.append(path(f"M{sx * 16} -150 L{sx * 42} -197 L{sx * 50} -128 Z", fill=FOX, stroke=FOX, sw=10))
        h.append(path(f"M{sx * 24} -150 L{sx * 41} -184 L{sx * 44} -142 Z", fill=EAR_PINK, stroke=EAR_PINK, sw=5))
    h.append(path("M-52 -122 C-56 -168 56 -168 52 -122 C60 -108 38 -92 0 -90 C-38 -92 -60 -108 -52 -122 Z", fill=FOX))
    h.append(path("M-54 -118 C-40 -110 -20 -124 0 -112 C20 -124 40 -110 54 -118 C55 -104 36 -91 0 -90 C-36 -91 -55 -104 -54 -118 Z",
                  fill=FOX_CREAM))
    if expr == "joy":
        h.append(happy_eye(-20, -131, 14, 3.2) + happy_eye(20, -131, 14, 3.2))
    else:
        h.append(eye(-20, -132, 6.4, look) + eye(20, -132, 6.4, look))
    if expr == "sad":
        h.append(path("M-29 -146 L-14 -149", stroke=PLUM, sw=2.6) + path("M29 -146 L14 -149", stroke=PLUM, sw=2.6))
    h.append(blush(-35, -114, 8, 5) + blush(35, -114, 8, 5))
    h.append(ellipse(0, -113, 6.8, 5, PLUM) + ellipse(-2, -115, 2, 1.2, WHITE, extra=op(0.7)))
    if expr == "curious":
        h.append(ellipse(0, -101, 3.6, 4.2, PLUM))
    elif expr == "joy":
        h.append(open_mouth(0, -106, 14))
    elif expr == "sad":
        h.append(frown(0, -103, 10, 2.6))
    else:
        h.append(path("M-8 -105 Q-4 -100 0 -106 Q4 -100 8 -105", stroke=PLUM, sw=2.6))
    head = "".join(h)
    if head_rot:
        head = rotated(head, head_rot, 0, -95)
    o.append(head)
    return g("".join(o), x, y, s, flip=flip, rot=lean)


# ----------------------------------------------------------------- Twinkle

STAR = "#FFE38A"
STAR_DIM = "#F3E2AE"


def star_points(R, r, k=5):
    pts = []
    for i in range(k * 2):
        a = -math.pi / 2 + i * math.pi / k
        rad = R if i % 2 == 0 else r
        pts.append(f"{n(round(rad * math.cos(a), 1))} {n(round(rad * math.sin(a), 1))}")
    return "M" + " L".join(pts) + " Z"


def twinkle(x, y, s=1.0, expr="happy", glow="normal", rot=0):
    """Twinkle, la estrellita. Origen: centro."""
    o = []
    radius, gop = {"dim": (72, 0.5), "normal": (100, 0.85), "big": (180, 1.0)}[glow]
    o.append(circle(0, 0, radius, url("glow"), op(gop)))
    color = STAR_DIM if expr == "cry" else STAR
    o.append(path(star_points(44, 22), fill=color, stroke=color, sw=14))
    o.append(ellipse(-15, -17, 6, 3.4, WHITE, rot=-50, extra=op(0.7)))
    if expr == "cry":
        o.append(eye(-10, 0, 4.4, (0, 1)) + eye(10, 0, 4.4, (0, 1)))
        o.append(path("M-16 -9 L-6 -12", stroke=PLUM, sw=2.4) + path("M16 -9 L6 -12", stroke=PLUM, sw=2.4))
        o.append(frown(0, 11, 9, 2.4))
        o.append(drop(-13, 13, 0.55, "#9FCDF2") + drop(14, 16, 0.45, "#9FCDF2"))
    elif expr == "bright":
        o.append(happy_eye(-10, 0, 10, 2.6) + happy_eye(10, 0, 10, 2.6))
        o.append(blush(-19, 8, 5, 3.2) + blush(19, 8, 5, 3.2))
        o.append(open_mouth(0, 7, 11))
        for a, d, r in [(-60, 78, 10), (20, 84, 8), (110, 80, 9), (190, 76, 7), (260, 86, 11), (330, 72, 6)]:
            ar = math.radians(a)
            o.append(sparkle(d * math.cos(ar), d * math.sin(ar), r, "#FFF8D6"))
    else:
        o.append(eye(-10, 0, 4.6) + eye(10, 0, 4.6))
        o.append(blush(-19, 8, 5, 3.2) + blush(19, 8, 5, 3.2))
        o.append(smile(0, 8, 10, 2.4))
    return g("".join(o), x, y, s, rot=rot)


# ----------------------------------------------------------- Abuelo Búho

OWL = "#B7A7D6"
OWL_D = "#9D8CC5"
OWL_L = "#ECE6F8"


def owl(x, y, s=1.0, flip=False):
    """El abuelo Búho. Origen: patas (sobre la rama)."""
    o = []
    for sx in (-1, 1):
        o.append(path(f"M{sx * 22} -150 L{sx * 46} -176 L{sx * 46} -132 Z", fill=OWL, stroke=OWL, sw=8))
    o.append(ellipse(0, -62, 46, 62, OWL))
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
        o.append(circle(sx * 21, -120, 16, WHITE) + circle(sx * 21, -119, 11, STAR) + circle(sx * 21, -119, 6.5, PLUM)
                 + circle(sx * 21 + 2.5, -122, 2.4, WHITE))
        brow = "".join(circle(sx * bx, by, br, WHITE) for bx, by, br in [(9, -142, 5), (18, -146, 6.5), (28, -145, 6), (37, -139, 4.6)])
        o.append(brow)
    o.append(blush(-40, -100, 7, 4.5) + blush(40, -100, 7, 4.5))
    o.append(path("M-7 -108 L7 -108 L0 -95 Z", fill="#F4A06B", stroke="#F4A06B", sw=4))
    for sx in (-1, 1):
        o.append(circle(sx * 8, -1, 4.4, "#F4A06B") + circle(sx * 15, 0, 4.4, "#F4A06B"))
    return g("".join(o), x, y, s, flip=flip)


# ----------------------------------------------------------- Daisy y flores

def daisy_head(expr="happy", petal="#FFFFFF", center="#FFD86B"):
    o = []
    for i in range(12):
        o.append(f'<ellipse cx="0" cy="-25" rx="8.5" ry="15" fill="{petal}" stroke="#E4DBEF" stroke-width="1.5" transform="rotate({i * 30})"/>')
    o.append(circle(0, 0, 17, center))
    if expr == "sad":
        o.append(calm_eye(-6, -2, 6, 2.2) + calm_eye(6, -2, 6, 2.2))
        o.append(frown(0, 6, 7, 2.2))
    else:
        o.append(eye(-6, -2, 2.9) + eye(6, -2, 2.9))
        o.append(blush(-11, 4, 3.4, 2.2, 0.9) + blush(11, 4, 3.4, 2.2, 0.9))
        o.append(smile(0, 4, 8, 2.2))
    return "".join(o)


def daisy(x, y, s=1.0, droopy=False):
    """Daisy, la margarita. Origen: base del tallo."""
    if not droopy:
        body = (path("M0 0 C-5 -40 5 -70 0 -96", stroke=STEM, sw=6)
                + leaf(0, -34, 34, -30) + leaf(0, -54, 30, -150)
                + g(daisy_head("happy"), 0, -104))
    else:
        dry_leaf, dry_vein = "#D3DDB0", "#BCCB98"
        body = (path("M0 0 C-2 -50 10 -92 40 -82", stroke=dry_vein, sw=6)
                + leaf(0, -28, 30, 35, dry_leaf, dry_vein) + leaf(0, -42, 26, 150, dry_leaf, dry_vein)
                + g(daisy_head("sad", "#F2ECDF", "#EBCB82"), 50, -62, rot=78))
    return g(body, x, y, s)


def flower(x, y, s=1.0, color="#F7B7C3", center="#FFE38A", h=36, droopy=False):
    if droopy:
        stem = path(f"M0 0 C0 {n(-h * 0.7)} 6 {n(-h)} 16 {n(-h * 0.9)}", stroke="#BCCB98", sw=4)
        petals = "".join(circle(7.5 * math.cos(math.radians(a)), 7.5 * math.sin(math.radians(a)), 6.5, color) for a in range(0, 360, 72))
        head = g(petals + circle(0, 0, 5, center), 19, -h * 0.72, rot=70)
        return g(stem + head, x, y, s)
    stem = path(f"M0 0 Q2 {n(-h * 0.5)} 0 {n(-h)}", stroke=STEM, sw=4)
    petals = "".join(circle(7.5 * math.cos(math.radians(a)), -h + 7.5 * math.sin(math.radians(a)), 7, color) for a in range(-90, 270, 72))
    return g(stem + leaf(1, -h * 0.4, 14, -35) + petals + circle(0, -h, 5, center), x, y, s)


def sunflower(x, y, h=230, s=1.0, tilt=0):
    o = [path(f"M0 0 C-8 {n(-h * 0.4)} 8 {n(-h * 0.7)} 0 {n(-h)}", stroke=STEM, sw=9)]
    o.append(leaf(0, -h * 0.36, 52, -28) + leaf(0, -h * 0.58, 44, -152))
    head = []
    for i in range(16):
        c = "#FFD66E" if i % 2 else "#FFE08A"
        head.append(f'<ellipse cx="0" cy="-38" rx="11" ry="24" fill="{c}" transform="rotate({n(i * 22.5)})"/>')
    head.append(circle(0, 0, 30, "#CFA27B") + circle(0, 0, 21, "#BF8F68"))
    for a in range(0, 360, 45):
        head.append(circle(12 * math.cos(math.radians(a)), 12 * math.sin(math.radians(a)), 2.2, "#A97A55"))
    o.append(g("".join(head), 0, -h, rot=tilt))
    return g("".join(o), x, y, s)


# ------------------------------------------------------------------- Benny

BUN = "#E9C9A5"
BUN_D = "#DDB58C"
BUN_L = "#FFF4E6"
BUN_PINK = "#F6B3C2"
NOSE = "#F08FA8"


def benny(x, y, s=1.0, flip=False, pose="stand", expr="happy", holding="", look=(0, 0), pal=None, mid="", face_extra=""):
    """Benny, el conejo. Origen: entre las patas, a nivel del suelo.

    pal cambia los colores (BUN, BUN_D, BUN_L); mid se dibuja bajo la cabeza y
    face_extra sobre la cara (lo usa la abuela para el chal y los lentes)."""
    BUN, BUN_D, BUN_L = pal or (globals()["BUN"], globals()["BUN_D"], globals()["BUN_L"])
    o = []
    o.append(g(ellipse(0, -40, 14, 44, BUN) + ellipse(0, -38, 7, 32, BUN_PINK), -20, -150, rot=-10))
    o.append(path("M8 -148 C12 -200 66 -204 84 -154 C88 -141 77 -131 69 -141 C58 -170 34 -174 26 -146 Z", fill=BUN))
    o.append(path("M17 -153 C22 -186 60 -190 74 -156 C63 -170 38 -172 27 -151 Z", fill=BUN_PINK))
    o.append(ellipse(0, -50, 40, 48, BUN))
    o.append(ellipse(0, -44, 26, 33, BUN_L))
    if pose == "hop":
        o.append(ellipse(-24, -8, 20, 9, BUN_L, rot=-18) + ellipse(24, -8, 20, 9, BUN_L, rot=18))
    else:
        o.append(ellipse(-22, -7, 21, 10, BUN_L) + ellipse(22, -7, 21, 10, BUN_L))
        o.append(ellipse(-24, -6, 6, 3.5, BUN_PINK, extra=op(0.8)) + ellipse(24, -6, 6, 3.5, BUN_PINK, extra=op(0.8)))

    def arm_side(sx):
        return ellipse(sx * 34, -56, 10, 19, BUN_D, rot=-sx * 15)

    def arm_up(sx):
        return path(f"M{sx * 30} -76 Q{sx * 48} -86 {sx * 54} -108", stroke=BUN_D, sw=15) + circle(sx * 55, -111, 8.5, BUN_L)

    if pose == "hold":
        o.append(holding)
        for sx in (-1, 1):
            o.append(path(f"M{sx * 32} -78 Q{sx * 32} -60 {sx * 14} -60", stroke=BUN_D, sw=15) + circle(sx * 13, -60, 8.5, BUN_L))
    elif pose == "hop":
        o.append(arm_up(-1) + arm_up(1))
    elif pose == "wave":
        o.append(arm_side(-1) + arm_up(1))
    elif pose == "plant":
        o.append(arm_side(-1))
        o.append(path("M30 -74 Q56 -62 62 -36", stroke=BUN_D, sw=15) + circle(62, -32, 8.5, BUN_L))
        o.append(ellipse(66, -14, 3.6, 5, "#B98B6B") + ellipse(60, 0, 3.6, 5, "#B98B6B", rot=30))
    else:
        o.append(arm_side(-1) + arm_side(1))

    o.append(mid)
    o.append(circle(0, -116, 44, BUN))
    o.append(circle(-14, -100, 15, BUN_L) + circle(14, -100, 15, BUN_L))
    if expr == "joy":
        o.append(happy_eye(-17, -124, 13, 3.2) + happy_eye(17, -124, 13, 3.2))
    else:
        o.append(eye(-17, -125, 6.2, look) + eye(17, -125, 6.2, look))
    o.append(blush(-31, -104, 7, 4.5) + blush(31, -104, 7, 4.5))
    for sx in (-1, 1):
        o.append(path(f"M{sx * 27} -104 L{sx * 45} -108 M{sx * 27} -99 L{sx * 45} -97", stroke=PLUM, sw=1.4, extra=op(0.35)))
    if expr == "joy":
        o.append(open_mouth(0, -99, 13))
    else:
        o.append(rect(-3.5, -98.5, 7, 6, WHITE, rx=1.5))
        o.append(path("M0 -103 L0 -99 M-7 -97 Q-3.5 -94 0 -99 Q3.5 -94 7 -97", stroke=PLUM, sw=2.4))
    o.append(ellipse(0, -107, 6, 4.4, NOSE))
    o.append(face_extra)
    return g("".join(o), x, y, s, flip=flip)


GRANNY = ("#E6DED6", "#D2C7BC", "#FBF7F2")


def grandma_bunny(x, y, s=1.0, flip=False, holding=""):
    """La abuela Bunny: misma forma que Benny, pelaje gris claro, chal y lentes."""
    shawl = (path("M-44 -86 Q0 -64 44 -86 L36 -46 Q0 -30 -36 -46 Z", fill="#CDBDF0", stroke="#CDBDF0", sw=6)
             + path("M-30 -44 L-32 -36 M-18 -38 L-19 -30 M-6 -35 L-6 -27 M6 -35 L6 -27 M18 -38 L19 -30 M30 -44 L32 -36",
                    stroke="#B8A6E6", sw=3)
             + circle(0, -70, 6, "#F6B8A8"))
    glasses = (circle(-17, -125, 11, "none", f' stroke="{PLUM}" stroke-width="2.4"')
               + circle(17, -125, 11, "none", f' stroke="{PLUM}" stroke-width="2.4"')
               + path("M-6 -126 Q0 -130 6 -126", stroke=PLUM, sw=2.4))
    pose = "hold" if holding else "stand"
    return benny(x, y, s, flip=flip, pose=pose, expr="happy", holding=holding, pal=GRANNY, mid=shawl, face_extra=glasses)


def watering_can(x, y, s=1.0, flip=False, pour=False):
    blue, blue_d = "#A9D4F5", "#8DC2EC"
    o = [path("M-24 -38 C-50 -40 -48 -10 -24 -12", stroke=blue_d, sw=7)]
    o.append(path("M20 -14 L56 -48", stroke=blue, sw=10))
    o.append(ellipse(59, -51, 7, 10, blue_d, rot=45))
    o.append(path("M-14 -44 C-10 -62 10 -62 14 -44", stroke=blue_d, sw=7))
    o.append(rect(-26, -46, 52, 46, blue, rx=11))
    o.append(rect(-26, -34, 52, 7, blue_d))
    o.append(ellipse(-12, -20, 4, 8, WHITE, extra=op(0.5)))
    if pour:
        o.append(drop(68, -36, 0.6, "#9CCBEF") + drop(76, -22, 0.6, "#9CCBEF") + drop(64, -16, 0.55, "#9CCBEF"))
    return g("".join(o), x, y, s, flip=flip)


# ------------------------------------------------------------------- Tilly

SHELL = "#9FD8BF"
SHELL_D = "#7DC2A4"
TURT = "#CDEBB8"
TURT_D = "#B5DCA0"


def hexagon(cx, cy, r, fill=SHELL_D):
    pts = " ".join(f"{n(round(cx + r * math.cos(math.pi / 3 * i + math.pi / 6), 1))},"
                   f"{n(round(cy + r * math.sin(math.pi / 3 * i + math.pi / 6), 1))}" for i in range(6))
    return f'<polygon points="{pts}" fill="{fill}" stroke="{fill}" stroke-width="5" opacity="0.6"/>'


def tilly(x, y, s=1.0, flip=False, expr="calm", nod=False):
    """Tilly, la tortuga (mira a la derecha). Origen: centro, a nivel del suelo."""
    o = [ellipse(-46, -12, 13, 13, TURT_D) + ellipse(30, -12, 13, 13, TURT_D)]
    o.append(path("M-70 -24 L-94 -16 L-68 -12 Z", fill=TURT, stroke=TURT, sw=6))
    o.append(ellipse(-16, -11, 13, 13, TURT) + ellipse(54, -11, 13, 13, TURT))
    face = (path("M44 -34 Q66 -40 84 -50", stroke=TURT, sw=24) + ellipse(98, -54, 27, 23, TURT))
    if expr == "calm":
        face += calm_eye(104, -61, 12, 2.8)
    else:
        face += eye(105, -61, 5.2)
    face += blush(103, -46, 6.5, 4) + path("M106 -44 Q114 -39 121 -47", stroke=PLUM, sw=2.6) + circle(121, -58, 1.4, PLUM)
    o.append(rotated(face, 14, 60, -38) if nod else face)
    o.append(path("M-76 -20 C-76 -104 76 -104 76 -20 Z", fill=SHELL))
    o.append(hexagon(0, -50, 16) + hexagon(-40, -38, 12) + hexagon(40, -38, 12) + hexagon(-22, -68, 7) + hexagon(22, -68, 7))
    o.append(path("M-52 -48 Q-44 -72 -20 -80", stroke=WHITE, sw=5, extra=op(0.45)))
    o.append(rect(-82, -26, 164, 14, SHELL_D, rx=7))
    return g("".join(o), x, y, s, flip=flip)


# -------------------------------------------------------------------- Milo

MOUSE = "#C3B9CF"
MOUSE_D = "#ABA0BC"
MOUSE_L = "#ECE7F1"


def milo(x, y, s=1.0, flip=False, expr="happy", body=True, holding="", pal=None):
    """Milo, el ratoncito. Origen: entre las patas, a nivel del suelo. pal = (MOUSE, MOUSE_D, MOUSE_L)."""
    MOUSE, MOUSE_D, MOUSE_L = pal or (globals()["MOUSE"], globals()["MOUSE_D"], globals()["MOUSE_L"])
    o = []
    if body:
        o.append(path("M16 -8 C46 -4 54 -36 38 -42 C27 -46 25 -28 36 -29", stroke=MOUSE_D, sw=4))
        o.append(ellipse(0, -27, 22, 27, MOUSE))
        o.append(ellipse(0, -23, 14, 17, MOUSE_L))
        o.append(ellipse(-10, -3, 9, 4.5, BUN_PINK) + ellipse(10, -3, 9, 4.5, BUN_PINK))
        if holding:
            o.append(holding + circle(-9, -34, 5.5, MOUSE_D) + circle(9, -34, 5.5, MOUSE_D))
        else:
            o.append(ellipse(-17, -30, 5, 10, MOUSE_D, rot=20) + ellipse(17, -30, 5, 10, MOUSE_D, rot=-20))
    for sx in (-1, 1):
        o.append(circle(sx * 21, -82, 15, MOUSE) + circle(sx * 21, -82, 9.5, BUN_PINK))
    o.append(circle(0, -62, 24, MOUSE))
    o.append(ellipse(0, -54, 12, 9, MOUSE_L))
    if expr == "joy":
        o.append(happy_eye(-9, -66, 9, 2.6) + happy_eye(9, -66, 9, 2.6))
    else:
        o.append(eye(-9, -66, 4.2) + eye(9, -66, 4.2))
    o.append(blush(-16, -55, 4.5, 3) + blush(16, -55, 4.5, 3))
    o.append(path("M-4 -51 Q-2 -48 0 -51 Q2 -48 4 -51", stroke=PLUM, sw=1.8))
    for sx in (-1, 1):
        o.append(path(f"M{sx * 10} -56 L{sx * 30} -60 M{sx * 10} -53 L{sx * 30} -51", stroke=PLUM, sw=1.2, extra=op(0.35)))
    o.append(circle(0, -57, 3.6, NOSE))
    return g("".join(o), x, y, s, flip=flip)


def milo_paws(x, y, s=1.0):
    return g(circle(-12, -38, 6.5, MOUSE_D) + circle(12, -38, 6.5, MOUSE_D), x, y, s)


# -------------------------------------------------------------- Cuervo

CROW = "#8A85A3"
CROW_D = "#736E8E"
BEAK = "#F7C873"


def crow(x, y, s=1.0, flip=False):
    o = [path("M-6 -14 L-8 0 M8 -14 L8 0", stroke=BEAK, sw=3)]
    o.append(path("M-26 -34 L-56 -26 L-50 -42 Z", fill=CROW_D, stroke=CROW_D, sw=6))
    o.append(ellipse(0, -36, 30, 23, CROW))
    o.append(ellipse(-6, -38, 20, 12, CROW_D, rot=-12))
    o.append(path("M18 -76 Q22 -86 28 -78", stroke=CROW, sw=4))
    o.append(circle(24, -60, 18, CROW))
    o.append(path("M38 -63 L55 -58 L38 -52 Z", fill=BEAK, stroke=BEAK, sw=3))
    o.append(eye(28, -64, 4.2))
    o.append(blush(30, -53, 4.5, 3, 0.8))
    return g("".join(o), x, y, s, flip=flip)


# ------------------------------------------------------------- comida y casa

def carrot(x, y, s=1.0, rot=0):
    o = [path("M0 -2 Q-12 -20 -8 -32 M0 -2 Q0 -22 4 -34 M0 -2 Q10 -18 15 -28", stroke=STEM, sw=5)]
    o.append(path("M-11 -2 C-9 18 -3 40 0 48 C3 40 9 18 11 -2 Z", fill="#F7A66E", stroke="#F7A66E", sw=4))
    o.append(path("M-7 12 L-1 14 M2 24 L7 22 M-4 33 L0 34", stroke="#E98E58", sw=2))
    return g("".join(o), x, y, s, rot=rot)


def strawberry(x, y, s=1.0, rot=0):
    o = [path("M0 15 C-15 7 -15 -10 -8 -12 C-4 -14 4 -14 8 -12 C15 -10 15 7 0 15 Z", fill="#F48FA0")]
    for sx, sy in [(-5, -4), (4, -5), (0, 3), (-6, 5), (6, 4), (0, 10)]:
        o.append(ellipse(sx, sy, 1.2, 1.8, "#FFF1BF"))
    o.append(path("M-9 -12 L-4 -9 L0 -14 L4 -9 L9 -12 L4 -16 L0 -15 L-4 -16 Z", fill=STEM, stroke=STEM, sw=2))
    return g("".join(o), x, y, s, rot=rot)


def tomato(x, y, s=1.0):
    return g(circle(0, 0, 13, "#F59A8B") + ellipse(-5, -5, 3.5, 2.2, WHITE, rot=-30, extra=op(0.6))
             + path("M-6 -11 L0 -8 L6 -11 L2 -13 L0 -17 L-2 -13 Z", fill=STEM, stroke=STEM, sw=2), x, y, s)


def cake(x, y, s=1.0):
    o = [ellipse(0, 0, 52, 11, WHITE) + ellipse(0, -1, 42, 7, "#F3EEF7")]
    o.append(rect(-34, -48, 68, 46, "#E9B98A", rx=8))
    o.append(rect(-34, -28, 68, 7, "#FFF6EA"))
    o.append(path("M-36 -44 Q-36 -54 -28 -54 L28 -54 Q36 -54 36 -44 L36 -40 Q31 -33 26 -40 Q20 -31 14 -40 Q7 -33 0 -40 "
                  "Q-7 -31 -14 -40 Q-20 -33 -26 -40 Q-31 -31 -36 -40 Z", fill="#FFF6EA"))
    o.append(carrot(0, -62, 0.42, rot=100))
    return g("".join(o), x, y, s)


def bowl(x, y, s=1.0, fill_items=""):
    return g(fill_items + path("M-34 -14 Q-32 14 0 14 Q32 14 34 -14 Z", fill="#CFE6F7") + ellipse(0, -14, 34, 6, "#B8D9F2"), x, y, s)


def house(x, y, s=1.0):
    o = [rect(46, -152, 18, 44, "#F4B4A2", rx=3)]
    o.append(rect(-70, -95, 140, 95, "#FFE49A", rx=8))
    o.append(path("M-86 -88 L0 -158 L86 -88 Z", fill="#FFB9A6", stroke="#FFB9A6", sw=12))
    o.append(circle(0, -118, 11, "#FFF6EA") + circle(0, -118, 7, "#D2E7F7"))
    o.append(rect(-15, -58, 30, 58, "#DDB58C", rx=13) + circle(8, -28, 2.6, "#BB9068"))
    for wx in (-56, 26):
        o.append(rect(wx, -76, 30, 28, "#D2E7F7", rx=6) + path(f"M{wx + 15} -76 L{wx + 15} -48 M{wx} -62 L{wx + 30} -62", stroke=WHITE, sw=3))
        o.append(rect(wx - 3, -48, 36, 7, "#F7C9B9", rx=3))
    return g("".join(o), x, y, s)


def fence(x0, x1, y, h=40, color="#F4E3CF"):
    o = [rect(x0, y - h * 0.72, x1 - x0, 6, color, rx=3), rect(x0, y - h * 0.32, x1 - x0, 6, color, rx=3)]
    px = x0 + 6
    while px <= x1 - 6:
        o.append(path(f"M{n(px - 6)} {n(y)} L{n(px - 6)} {n(y - h + 6)} L{n(px)} {n(y - h)} L{n(px + 6)} {n(y - h + 6)} L{n(px + 6)} {n(y)} Z",
                      fill=color, stroke=color, sw=3))
        px += 24
    return "".join(o)


def soil_row(x0, x1, y, h=26):
    w = x1 - x0
    return (path(f"M{n(x0)} {n(y)} Q{n(x0 + w * 0.08)} {n(y - h)} {n(x0 + w * 0.25)} {n(y - h)} L{n(x1 - w * 0.25)} {n(y - h)} "
                 f"Q{n(x1 - w * 0.08)} {n(y - h)} {n(x1)} {n(y)} Z", fill="#DCC2A6")
            + path(f"M{n(x0 + w * 0.15)} {n(y - h * 0.55)} L{n(x1 - w * 0.15)} {n(y - h * 0.55)}", stroke="#C9AB8C", sw=3))


def round_tree(x, y, s=1.0, leaf_c="#B4E2C6", shade="#9FD6B6"):
    canopy = [("c", 0, -70, 34), ("c", -24, -52, 26), ("c", 24, -52, 26)]
    return g(rect(-6, -40, 12, 40, "#D8BBA0", rx=4) + cloud_layer(canopy, shade, 5) + cloud_layer(canopy, leaf_c), x, y, s)


def sprout(x, y, s=1.0):
    return g(path("M0 0 L0 -14", stroke=STEM, sw=3.5) + leaf(0, -14, 14, -40) + leaf(0, -12, 12, -145), x, y, s)


# ------------------------------------------------- animales del bosque (Pip)

RAB = "#EEE9F3"
RAB_D = "#DCD4E6"
RAB_PINK = "#F6C1CD"


def rabbit(x, y, s=1.0, flip=False, expr="happy"):
    """Conejito del bosque (no es Benny). Mira a la derecha. Origen: patas."""
    o = [circle(-40, -26, 12, WHITE)]
    o.append(ellipse(-8, -34, 38, 33, RAB))
    o.append(ellipse(2, -6, 22, 8, RAB_D) + ellipse(26, -5, 11, 6, RAB))
    o.append(ellipse(14, -120, 10, 30, RAB, rot=-12) + ellipse(14, -118, 5, 20, RAB_PINK, rot=-12))
    o.append(ellipse(36, -116, 10, 28, RAB, rot=16) + ellipse(36, -114, 5, 18, RAB_PINK, rot=16))
    o.append(circle(24, -72, 28, RAB))
    if expr == "sleepy":
        o.append(calm_eye(14, -76, 10, 2.6) + calm_eye(34, -76, 10, 2.6))
        o.append(path("M48 -98 L58 -98 L48 -88 L58 -88", stroke="#CFC6E6", sw=2.6))
    elif expr == "joy":
        o.append(happy_eye(14, -76, 10, 2.6) + happy_eye(34, -76, 10, 2.6))
    else:
        o.append(eye(14, -76, 4.2) + eye(34, -76, 4.2))
    o.append(blush(6, -63, 5, 3.2) + blush(42, -63, 5, 3.2))
    o.append(ellipse(24, -66, 4, 3, NOSE))
    o.append(path("M24 -63 L24 -60 M19 -58 Q21.5 -56 24 -60 Q26.5 -56 29 -58", stroke=PLUM, sw=2))
    return g("".join(o), x, y, s, flip=flip)


FROG = "#A9DDA0"
FROG_D = "#8FCB88"
FROG_L = "#E2F4D4"


def frog(x, y, s=1.0, flip=False, expr="happy"):
    """Ranita verde. Origen: base (suelo o nenúfar)."""
    o = [ellipse(-26, -10, 16, 10, FROG_D) + ellipse(26, -10, 16, 10, FROG_D)]
    o.append(ellipse(0, -24, 30, 22, FROG))
    o.append(ellipse(0, -18, 18, 13, FROG_L))
    o.append(ellipse(-12, -3, 8, 4, FROG_D) + ellipse(12, -3, 8, 4, FROG_D))
    for sx in (-1, 1):
        o.append(circle(sx * 16, -44, 11, FROG) + circle(sx * 16, -45, 7.5, WHITE)
                 + circle(sx * 16, -44, 4.6, PLUM) + circle(sx * 16 + 1.6, -46, 1.6, WHITE))
    o.append(blush(-21, -29, 5, 3) + blush(21, -29, 5, 3))
    if expr == "joy":
        o.append(open_mouth(0, -32, 14))
    else:
        o.append(smile(0, -33, 20, 2.6, 0.3))
    return g("".join(o), x, y, s, flip=flip)


def lily_pad(x, y, s=1.0, water="#BFE0F5"):
    return g(ellipse(0, 0, 48, 14, "#8FCFA3") + path("M0 0 L44 -6 L40 6 Z", fill=water)
             + path("M-30 0 L-4 0 M-20 -7 L-4 -1 M-18 7 L-4 1", stroke="#7DBF93", sw=2), x, y, s)


SQ = "#DDA57E"
SQ_D = "#C88B63"
SQ_L = "#FFEBD9"


def squirrel(x, y, s=1.0, flip=False, rot=0):
    """Ardilla con bellota. Mira a la derecha. Origen: patas."""
    o = [ellipse(-26, -56, 22, 44, SQ_D, rot=-14) + circle(-16, -100, 19, SQ_D) + ellipse(-24, -56, 11, 30, "#D79A72", rot=-14)]
    o.append(ellipse(6, -30, 22, 28, SQ) + ellipse(11, -26, 13, 19, SQ_L))
    o.append(ellipse(0, -4, 12, 5, SQ_D) + ellipse(18, -4, 10, 5, SQ_D))
    for ex in (4, 26):
        o.append(path(f"M{ex - 6} -80 L{ex} -96 L{ex + 6} -80 Z", fill=SQ, stroke=SQ, sw=5))
    o.append(circle(15, -66, 18, SQ))
    o.append(eye(8, -69, 3.4) + eye(23, -69, 3.4))
    o.append(blush(3, -59, 4, 2.6) + blush(28, -59, 4, 2.6))
    o.append(circle(16, -61, 2.4, PLUM))
    o.append(ellipse(21, -40, 6.5, 7.5, "#D6AE78") + path("M14 -45 Q21 -52 28 -45 Z", fill="#A9825F", stroke="#A9825F", sw=3))
    o.append(circle(15, -38, 4.5, SQ_D) + circle(27, -38, 4.5, SQ_D))
    return g("".join(o), x, y, s, flip=flip, rot=rot)


def duck(x, y, s=1.0, flip=False, baby=False, swim=True):
    """Pato (mama blanca o patito amarillo). Mira a la derecha. Origen: línea del agua o suelo."""
    body, shade = ("#FFE89A", "#F5D676") if baby else ("#FFFDF6", "#E9E3D6")
    o = []
    if swim:
        o.append(path("M-34 0 C-38 -26 -8 -30 8 -22 C20 -18 30 -14 32 0 Z", fill=body))
        o.append(path("M-44 6 Q-34 1 -24 6 M18 6 Q28 1 38 6", stroke="#E3F2FC", sw=3))
    else:
        o.append(path("M-6 -4 L-6 4 L-12 6 M10 -4 L10 4 L4 6", stroke="#F7B267", sw=3.4))
        o.append(path("M-34 -12 C-38 -38 -8 -42 8 -34 C20 -30 32 -26 30 -12 C26 2 -30 2 -34 -12 Z", fill=body))
    dy = 0 if swim else -12
    o.append(path(f"M-32 {-8 + dy} L-46 {-20 + dy} L-28 {-16 + dy} Z", fill=body, stroke=body, sw=4))
    o.append(ellipse(-8, -12 + dy, 16, 8, shade, rot=-10))
    o.append(circle(22, -36 + dy, 14, body))
    o.append(path(f"M33 {-39 + dy} L46 {-35 + dy} L33 {-31 + dy} Z", fill="#F7B267", stroke="#F7B267", sw=3))
    o.append(eye(26, -40 + dy, 2.8))
    o.append(blush(24, -30 + dy, 3.6, 2.4))
    return g("".join(o), x, y, s, flip=flip)


def fish(x, y, s=1.0, rot=0):
    """Pez saltando. Origen: centro."""
    o = [path("M-18 0 L-36 -13 L-33 0 L-36 13 Z", fill="#98BBE2", stroke="#98BBE2", sw=4)]
    o.append(path("M-6 -10 Q4 -22 12 -10 Z", fill="#98BBE2"))
    o.append(ellipse(0, 0, 24, 12, "#AFCBEA") + ellipse(2, 4, 16, 5, "#D9E8F7"))
    o.append(eye(13, -3, 2.6) + path("M20 3 Q22 5 24 3", stroke=PLUM, sw=1.6))
    return g("".join(o), x, y, s, rot=rot)


BEAV = "#C9A07E"
BEAV_D = "#AD8364"
BEAV_L = "#EFDCC8"


def beaver(x, y, s=1.0, flip=False):
    """Castor. Mira a la derecha. Origen: patas."""
    o = [ellipse(-44, -10, 26, 11, "#9C7A62", rot=-14)
         + path("M-60 -12 L-30 -16 M-56 -4 L-30 -8 M-50 -20 L-40 0", stroke="#B89580", sw=1.6)]
    o.append(ellipse(-6, -34, 30, 33, BEAV) + ellipse(0, -28, 17, 23, BEAV_L))
    o.append(ellipse(-14, -4, 12, 6, BEAV_D) + ellipse(10, -4, 12, 6, BEAV_D))
    o.append(ellipse(-20, -42, 7, 13, BEAV_D, rot=20) + ellipse(16, -44, 7, 13, BEAV_D, rot=-20))
    o.append(circle(2, -94, 6, BEAV_D) + circle(30, -94, 6, BEAV_D))
    o.append(circle(16, -74, 24, BEAV))
    o.append(ellipse(17, -63, 12, 9, BEAV_L))
    o.append(rect(13, -58, 8, 9, WHITE, rx=2) + path("M17 -58 L17 -50", stroke="#E3DACE", sw=1.4))
    o.append(ellipse(17, -69, 5, 3.6, PLUM))
    o.append(eye(7, -80, 3.6) + eye(27, -80, 3.6))
    o.append(blush(1, -66, 4.5, 3) + blush(33, -66, 4.5, 3))
    return g("".join(o), x, y, s, flip=flip)


def log_bridge(x0, y0, x1, y1, w=20):
    """Tronco atravesado sobre el río."""
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    L = math.hypot(x1 - x0, y1 - y0)
    body = (rect(0, -w / 2, L, w, "#C9A98F", rx=w / 2) + path(f"M14 -2 L{n(L * 0.45)} -2 M{n(L * 0.55)} 4 L{n(L - 20)} 4",
                                                                   stroke="#B8977C", sw=2.4)
            + ellipse(L, 0, w * 0.32, w / 2, "#E8D3BC") + ellipse(L, 0, w * 0.16, w * 0.26, "#D7BFA4"))
    return f'<g transform="translate({n(x0)} {n(y0)}) rotate({n(ang)})">{body}</g>'


BEAR = "#B98F72"
BEAR_D = "#A47B60"
BEAR_L = "#E9D2BC"


def bear(x, y, s=1.0, flip=False, berries=False, expr="happy"):
    """Oso pardo sentado (de frente). Origen: entre las patas."""
    o = [ellipse(-34, -20, 24, 20, BEAR_D) + ellipse(34, -20, 24, 20, BEAR_D)]
    o.append(ellipse(0, -62, 54, 60, BEAR) + ellipse(0, -54, 33, 41, BEAR_L))
    o.append(ellipse(-38, -9, 15, 9, BEAR_L) + ellipse(38, -9, 15, 9, BEAR_L))
    if berries:
        o.append(path("M-48 -88 Q-46 -66 -16 -62", stroke=BEAR_D, sw=20) + path("M48 -88 Q46 -66 16 -62", stroke=BEAR_D, sw=20))
        for bx, by, c in [(-8, -70, "#B48DD6"), (6, -72, "#E58FA6"), (-1, -80, "#B48DD6"), (12, -82, "#B48DD6"), (-12, -81, "#E58FA6")]:
            o.append(circle(bx, by, 6, c) + circle(bx - 2, by - 2, 1.6, WHITE, op(0.7)))
    else:
        o.append(ellipse(-44, -64, 13, 26, BEAR_D, rot=16) + ellipse(44, -64, 13, 26, BEAR_D, rot=-16))
    for sx in (-1, 1):
        o.append(circle(sx * 32, -168, 15, BEAR) + circle(sx * 32, -168, 8, BEAR_L))
    o.append(circle(0, -138, 42, BEAR))
    o.append(ellipse(0, -122, 20, 15, BEAR_L))
    o.append(ellipse(0, -129, 7.5, 5.5, PLUM) + ellipse(-2, -131, 2, 1.2, WHITE, extra=op(0.7)))
    if expr == "joy":
        o.append(happy_eye(-16, -146, 11, 3) + happy_eye(16, -146, 11, 3))
        o.append(open_mouth(0, -119, 12))
    else:
        o.append(eye(-16, -146, 5.2) + eye(16, -146, 5.2))
        o.append(path("M-7 -118 Q-3.5 -114 0 -119 Q3.5 -114 7 -118", stroke=PLUM, sw=2.4))
    o.append(blush(-30, -124, 7, 4.5) + blush(30, -124, 7, 4.5))
    return g("".join(o), x, y, s, flip=flip)


def berry_bush(x, y, s=1.0):
    bush = [("c", -26, -20, 24), ("c", 0, -34, 30), ("c", 28, -20, 24)]
    o = [rect(-46, -20, 92, 20, "#93BBAE", rx=10), cloud_layer(bush, "#93BBAE", 4), cloud_layer(bush, "#A9CDBF")]
    for bx, by in [(-28, -26), (-10, -44), (8, -30), (26, -36), (34, -18), (-38, -12), (0, -14)]:
        o.append(circle(bx, by, 4.5, "#B48DD6"))
    return g("".join(o), x, y, s)


DEER = "#E3B793"
DEER_D = "#CFA07B"
DEER_L = "#FFF2E4"


def deer(x, y, s=1.0, flip=False):
    """Cierva amable (sin astas). Mira a la derecha. Origen: suelo, entre las patas."""
    o = []
    for lx in (-34, -20, 18, 32):
        o.append(rect(lx - 4.5, -64, 9, 62, DEER_D, rx=4.5) + ellipse(lx, -2, 6, 3.5, "#A98163"))
    o.append(ellipse(-50, -92, 8, 12, DEER_L, rot=-30))
    o.append(ellipse(0, -76, 50, 28, DEER) + ellipse(0, -64, 34, 12, DEER_L))
    for sx, sy in [(-22, -86), (-6, -92), (10, -86), (-30, -76), (2, -80)]:
        o.append(circle(sx, sy, 3.6, DEER_L))
    o.append(path("M30 -90 Q42 -118 50 -136", stroke=DEER, sw=24))
    o.append(ellipse(44, -172, 7, 16, DEER, rot=-38) + ellipse(44, -172, 3.5, 10, "#F6C9C2", rot=-38))
    o.append(ellipse(72, -172, 7, 16, DEER, rot=30) + ellipse(72, -172, 3.5, 10, "#F6C9C2", rot=30))
    o.append(ellipse(58, -150, 22, 19, DEER) + ellipse(74, -142, 13, 10, DEER_L))
    o.append(circle(84, -145, 4, PLUM))
    o.append(eye(58, -154, 4.2) + path("M53 -161 L50 -164 M57 -162 L56 -166", stroke=PLUM, sw=1.6))
    o.append(blush(62, -140, 5, 3))
    o.append(path("M74 -136 Q78 -133 82 -136", stroke=PLUM, sw=1.8))
    return g("".join(o), x, y, s, flip=flip)


FOREST_MOUSE = ("#D7C2A8", "#C2AA8E", "#F5EBDD")


# ------------------------------------------------------- naturaleza (Nimbus)

def mountain(cx, base, w, h, fill, snow=None, snow_frac=0.3):
    o = [path(f"M{n(cx - w / 2)} {n(base)} L{n(cx - 10)} {n(base - h + 12)} Q{n(cx)} {n(base - h)} {n(cx + 10)} {n(base - h + 12)} "
              f"L{n(cx + w / 2)} {n(base)} Z", fill=fill, stroke=fill, sw=6)]
    if snow:
        k = snow_frac
        lx, rx = cx - w / 2 * k, cx + w / 2 * k
        sy = base - h * (1 - k)
        o.append(path(f"M{n(cx - 10)} {n(base - h + 12)} Q{n(cx)} {n(base - h)} {n(cx + 10)} {n(base - h + 12)} L{n(rx)} {n(sy)} "
                      f"Q{n(rx - w * 0.04)} {n(sy + 12)} {n(cx + w * 0.05)} {n(sy - 2)} Q{n(cx)} {n(sy + 14)} {n(cx - w * 0.06)} {n(sy)} "
                      f"Q{n(lx + w * 0.03)} {n(sy + 12)} {n(lx)} {n(sy)} Z", fill=snow, stroke=snow, sw=4))
    return "".join(o)


def pine(x, y, s=1.0, c1="#9CCDB3", c2="#86BFA2"):
    o = [rect(-5, -18, 10, 18, "#C9A98F", rx=3)]
    for i, (w, top, bot) in enumerate([(46, -60, -14), (38, -88, -44), (28, -112, -72)]):
        o.append(path(f"M{-w} {bot} L0 {top} L{w} {bot} Z", fill=c1 if i % 2 == 0 else c2, stroke=c1 if i % 2 == 0 else c2, sw=8))
    return g("".join(o), x, y, s)


def rock(x, y, s=1.0, c="#CFC8DA", d="#BBB3C9"):
    return g(ellipse(0, -10, 26, 14, d) + ellipse(-3, -13, 22, 11, c) + ellipse(-9, -17, 6, 3, WHITE, extra=op(0.5)), x, y, s)


def garden_tree(x, y, s=1.0, lush=True):
    """Arbolito del jardín: hojas secas (lush=False) o verdes nuevas."""
    leaf_c, shade = ("#B4E2C6", "#9FD6B6") if lush else ("#E2C994", "#CFB27A")
    canopy = [("c", 0, -96, 40), ("c", -32, -74, 30), ("c", 32, -74, 30), ("c", -14, -120, 26), ("c", 18, -118, 26)]
    o = [rect(-8, -60, 16, 60, "#D2B296", rx=5), path("M0 -44 L-18 -70 M0 -54 L16 -76", stroke="#D2B296", sw=6)]
    o.append(cloud_layer(canopy, shade, 6) + cloud_layer(canopy, leaf_c))
    if lush:
        for lx, ly, r in [(-20, -100, -30), (14, -128, 20), (30, -84, 60), (-38, -70, -70), (4, -80, 10)]:
            o.append(leaf(lx, ly, 14, r, "#CDEFD8", "#A8DDB5"))
    else:
        for lx, ly in [(-26, -98), (10, -122), (26, -80), (-4, -76)]:
            o.append(path(f"M{lx - 5} {ly} L{lx + 5} {ly}", stroke="#C9A86C", sw=2))
        o.append(leaf(54, -30, 14, 30, "#DCBF86", "#C9A86C") + leaf(-50, -14, 13, 160, "#DCBF86", "#C9A86C")
                 + leaf(34, -6, 12, -20, "#DCBF86", "#C9A86C"))
    return g("".join(o), x, y, s)


# ------------------------------------------------------------- frutas (Benny)

def apple(x, y, s=1.0, color="#F28B82", rot=0):
    o = [path("M0 -12 C-8 -18 -20 -14 -20 -2 C-20 12 -10 20 0 16 C10 20 20 12 20 -2 C20 -14 8 -18 0 -12 Z", fill=color)]
    o.append(path("M0 -12 Q1 -18 3 -22", stroke="#A9825F", sw=2.6))
    o.append(leaf(3, -18, 13, -30, LEAF, STEM))
    o.append(ellipse(-9, -4, 3, 5.5, WHITE, rot=20, extra=op(0.55)))
    return g("".join(o), x, y, s, rot=rot)


def pear(x, y, s=1.0, rot=0):
    o = [path("M0 -22 C-7 -22 -8 -12 -10 -6 C-18 0 -18 18 0 18 C18 18 18 0 10 -6 C8 -12 7 -22 0 -22 Z", fill="#D8E79A")]
    o.append(path("M0 -22 Q0 -27 3 -30", stroke="#A9825F", sw=2.4) + leaf(2, -26, 11, -20, LEAF, STEM))
    o.append(ellipse(-6, 4, 2.6, 5, WHITE, rot=15, extra=op(0.5)))
    return g("".join(o), x, y, s, rot=rot)


def lemon(x, y, s=1.0, rot=0, color="#FFE58A"):
    o = [path("M-20 0 Q-18 -14 0 -14 Q18 -14 20 0 Q18 14 0 14 Q-18 14 -20 0 Z", fill=color, stroke=color, sw=3)]
    o.append(ellipse(-23, 0, 3.4, 3, color) + ellipse(23, 0, 3.4, 3, color))
    o.append(ellipse(-7, -5, 5, 2.4, WHITE, rot=-10, extra=op(0.55)))
    return g("".join(o), x, y, s, rot=rot)


def orange(x, y, s=1.0):
    return g(circle(0, 0, 16, "#FFC27A") + circle(-5, -5, 3.6, WHITE, op(0.5)) + circle(0, -14, 2, "#E8A55E")
             + leaf(1, -15, 12, -25, LEAF, STEM), x, y, s)


def cherries(x, y, s=1.0):
    return g(path("M-8 4 Q-6 -14 4 -24 M8 6 Q8 -10 4 -24", stroke="#8CCB9B", sw=2.4) + leaf(4, -24, 13, -10, LEAF, STEM)
             + circle(-9, 8, 8, "#E8707F") + circle(9, 10, 8, "#E8707F")
             + circle(-11, 5, 2.2, WHITE, op(0.6)) + circle(7, 7, 2.2, WHITE, op(0.6)), x, y, s)


def banana(x, y, s=1.0, rot=0):
    return g(path("M-26 -6 Q-2 22 26 -10 Q28 -14 24 -14 Q0 8 -22 -12 Q-28 -12 -26 -6 Z", fill="#FFE28A", stroke="#FFE28A", sw=3)
             + path("M-21 -8 Q0 10 22 -11", stroke="#F2CC66", sw=2) + circle(-26, -9, 2.6, "#A9825F") + circle(26, -12, 2.2, "#A9825F"),
             x, y, s, rot=rot)


def grapes(x, y, s=1.0):
    o = [path("M0 -22 Q2 -30 6 -32", stroke="#A9825F", sw=2.6), leaf(4, -28, 14, -25, LEAF, STEM)]
    for gx, gy in [(-10, -12), (0, -14), (10, -12), (-5, -2), (5, -2), (-10, 8), (0, 8), (10, 8), (-5, 18), (5, 18), (0, 27)]:
        o.append(circle(gx, gy, 6.6, "#B9A3DE") + circle(gx - 2, gy - 2, 1.8, WHITE, op(0.55)))
    return g("".join(o), x, y, s)


def watermelon_slice(x, y, s=1.0, rot=0):
    o = [path("M-30 0 A30 30 0 0 0 30 0 Z", fill="#9ED7AE"), path("M-26 0 A26 26 0 0 0 26 0 Z", fill="#F3FAE8"),
         path("M-23 0 A23 23 0 0 0 23 0 Z", fill="#F7A1AE")]
    for sx, sy in [(-12, 6), (0, 10), (12, 6), (-6, 15), (6, 15)]:
        o.append(ellipse(sx, sy, 1.6, 2.6, PLUM, extra=op(0.7)))
    return g("".join(o), x, y, s, rot=rot)


def blueberries(x, y, s=1.0):
    return g("".join(circle(bx, by, 5, "#8FA6D9") + circle(bx, by - 2.6, 1.4, "#6F86BE")
                     for bx, by in [(-6, 0), (5, -1), (0, -8), (-1, 7)]), x, y, s)


def basket(x, y, s=1.0, items=""):
    o = [path("M-30 -24 Q0 -58 30 -24", stroke="#D6B07E", sw=5), items]
    o.append(path("M-36 -22 L36 -22 L28 6 Q0 12 -28 6 Z", fill="#E8C795"))
    o.append(path("M-32 -12 L33 -12 M-30 -2 L31 -2 M-18 -22 L-15 8 M0 -22 L0 10 M18 -22 L15 8", stroke="#D6B07E", sw=2.4))
    o.append(rect(-38, -26, 76, 8, "#D6B07E", rx=4))
    return g("".join(o), x, y, s)


def fruit_tree(x, y, s=1.0, fruit="apple"):
    """Árbol frutal (manzano o limonero). Origen: base del tronco."""
    canopy = [("c", 0, -176, 62), ("c", -50, -144, 46), ("c", 50, -144, 46), ("c", -28, -210, 44), ("c", 30, -208, 44)]
    o = [rect(-9, -130, 18, 130, "#D2B296", rx=6), path("M0 -96 L-26 -126 M0 -110 L22 -134", stroke="#D2B296", sw=8)]
    o.append(cloud_layer(canopy, "#9FD6B6", 8) + cloud_layer(canopy, "#B4E2C6"))
    spots = [(-60, -150), (-30, -186), (2, -214), (36, -184), (62, -146), (-8, -152), (24, -140), (-40, -216), (44, -222)]
    for fx, fy in spots:
        o.append(apple(fx, fy, 0.62) if fruit == "apple" else lemon(fx, fy, 0.55, rot=-20))
    return g("".join(o), x, y, s)


def strawberry_plant(x, y, s=1.0, flowers=False, berries=True):
    o = []
    for rot, L in [(-150, 30), (-110, 34), (-70, 34), (-30, 30)]:
        o.append(leaf(0, -4, L, rot, "#9ED7AE", "#86C79A"))
    if flowers:
        for fx, fy in [(-14, -36), (12, -38)]:
            o.append("".join(circle(fx + 5 * math.cos(math.radians(a)), fy + 5 * math.sin(math.radians(a)), 4.4, WHITE)
                             for a in range(0, 360, 72)) + circle(fx, fy, 2.6, "#FFE38A"))
    if berries:
        o.append(strawberry(-18, -2, 0.75, 15) + strawberry(16, 0, 0.7, -20))
    return g("".join(o), x, y, s)


def lemon_sapling(x, y, s=1.0, bump=False):
    """Limonero bebé (ch1) o con un limoncito verde (ch2)."""
    o = [path("M0 0 C-2 -30 3 -60 0 -92", stroke="#C9A98F", sw=5)]
    for ly, L, rot in [(-38, 24, -30), (-52, 22, -150), (-66, 22, -35), (-78, 20, -145), (-92, 18, -80)]:
        o.append(leaf(0, ly, L, rot, "#B4E2C0", "#8CCB9B"))
    if bump:
        o.append(lemon(14, -58, 0.6, rot=30, color="#A9D46A"))
    return g("".join(o), x, y, s)


def seed_bag(x, y, s=1.0):
    """Bolsita de papel de la abuela con semillas."""
    o = [path("M-22 0 L-24 -46 L24 -46 L22 0 Z", fill="#EBD3AE")]
    o.append(path("M-24 -46 L-20 -54 L-12 -48 L-4 -55 L4 -48 L12 -55 L20 -48 L24 -46 Z", fill="#E0C49B"))
    o.append(apple(0, -22, 0.55) + path("M-14 -6 L14 -6", stroke="#D9BC92", sw=2))
    for sx, sy in [(30, -2), (36, 2), (26, 4)]:
        o.append(ellipse(sx, sy, 2.6, 3.6, "#B98B6B"))
    return g("".join(o), x, y, s)


def pitcher(x, y, s=1.0):
    """Jarra de limonada rosada."""
    o = [path("M18 -44 C34 -44 34 -16 18 -16", stroke="#E4F1FA", sw=5)]
    o.append(path("M-18 0 L-20 -52 L20 -52 L18 0 Z", fill="#E4F1FA"))
    o.append(path("M-17 -2 L-18 -36 L18 -36 L17 -2 Z", fill="#F9C3CF"))
    o.append(lemon(0, -40, 0.4, color="#FFE58A") + ellipse(-9, -24, 3, 9, WHITE, extra=op(0.5)))
    return g("".join(o), x, y, s)


# ----------------------------------------------------------------- archivos

def common_defs():
    return (f'<radialGradient id="{uid("glow")}"><stop offset="0" stop-color="#FFF8CF"/>'
            f'<stop offset="0.45" stop-color="#FFEBA6" stop-opacity="0.55"/><stop offset="1" stop-color="#FFE38A" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="{uid("soft")}"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/>'
            f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>')


def lin(name, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{uid(name)}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient>'


def write_svg(book, name, w, h, title, defs, body):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
           f'aria-labelledby="{uid("t")}" stroke-linecap="round" stroke-linejoin="round">'
           f'<title id="{uid("t")}">{title}</title><defs>{common_defs()}{defs}</defs>{body}</svg>\n')
    out = os.path.join(ROOT, "images", book, f"{name}.svg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    return out, len(doc.encode())


# ------------------------------------------------------------ Pip: escenas

def pip_cover():
    rng = random.Random(1)
    defs = lin("sky", [(0, "#B8ADE0"), (0.55, "#E2D8F5"), (1, "#FFDCCF")])
    o = [rect(0, 0, 600, 800, url("sky"))]
    o.append(starfield(rng, 30, 40, 560, 40, 440, avoid=[(440, 160, 100), (300, 420, 150)]))
    o.append(moon(440, 160, 50))
    o.append(path("M0 560 Q150 480 300 525 Q460 570 600 500 L600 800 L0 800 Z", fill="#CFE3DC"))
    o.append(path("M0 660 Q300 540 600 660 L600 800 L0 800 Z", fill="#B7D8CA"))
    for tx, ty in [(80, 680), (130, 720), (480, 690), (530, 730), (210, 760), (400, 770)]:
        o.append(tuft(tx, ty, 1.2, "#9CC9B5"))
    for fx, fy, c in [(110, 700, "#F7B7C3"), (500, 715, "#E4DCF7"), (170, 755, "#FFF1BF"), (450, 760, "#F7B7C3")]:
        o.append(flower(fx, fy, 1.1, c))
    o.append(pip(300, 650, 1.55, pose="hold", expr="joy", holding=twinkle(0, -60, 0.66, "happy", "normal")))
    for sx, sy, r in [(200, 430, 8), (410, 400, 10), (180, 520, 6), (430, 500, 7)]:
        o.append(sparkle(sx, sy, r, "#FFF6C8"))
    return defs, "".join(o)


def pip_ch1():
    rng = random.Random(11)
    defs = lin("sky", [(0, "#B5AADF"), (0.6, "#DED5F3"), (1, "#F7DCD8")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(starfield(rng, 28, 40, 760, 30, 290, avoid=[(120, 100, 70)]))
    o.append(moon(120, 100, 34))
    o.append(path("M0 360 Q200 300 420 345 Q620 385 800 330 L800 600 L0 600 Z", fill="#C9DFD8"))
    o.append(path("M0 440 Q400 380 800 440 L800 600 L0 600 Z", fill="#AFD2C2"))
    o.append(blades(rng, 50, 0, 540, 425, 470, 30, 70, ["#9CCAB5", "#A6D0BC", "#93C2AC"]))
    # el estanque con el nenúfar y la rana
    o.append(ellipse(660, 458, 118, 26, "#BFE0F5")
             + path("M580 452 Q598 448 616 452 M690 470 Q708 466 726 470", stroke="#E3F2FC", sw=3))
    o.append(lily_pad(612, 466, 0.5) + lily_pad(700, 462, 0.85))
    o.append(frog(700, 460, 0.62, expr="happy"))
    o.append(blade(548, 470, 40, -6, "#93C2AC") + blade(774, 466, 44, 8, "#9CCAB5") + blade(786, 470, 34, -4, "#A6D0BC"))
    for fx, fy in [(80, 470), (160, 455), (430, 450)]:
        o.append(flower(fx, fy, 1.0, "#FFFFFF", "#FFE38A", 40))
    o.append(twinkle(545, 512, 0.78, "cry", "dim", rot=18))
    o.append(rabbit(108, 552, 0.66, expr="sleepy"))
    o.append(milo(202, 560, 0.6, pal=FOREST_MOUSE))
    o.append(pip(330, 548, 1.2, pose="step", expr="curious", look=(3, 1), lean=5))
    o.append(blades(rng, 40, 0, 800, 560, 610, 30, 60, ["#93C2AC", "#8BBDA6", "#9CCAB5"]))
    o.append(blade(500, 548, 52, -6, "#93C2AC") + blade(592, 552, 46, 8, "#8BBDA6") + blade(572, 556, 40, -4, "#9CCAB5"))
    for fx, fy in [(60, 590), (240, 600), (700, 595), (760, 585)]:
        o.append(flower(fx, fy, 1.2, "#FFFFFF", "#FFE38A", 46))
    for fx, fy in [(440, 380), (690, 360), (230, 330), (520, 420)]:
        o.append(circle(fx, fy, 9, url("glow")) + circle(fx, fy, 2.4, "#FFF6C8"))
    return defs, "".join(o)


def pip_ch2():
    rng = random.Random(21)
    defs = lin("sky", [(0, "#C1B5E6"), (0.6, "#E6DCF6"), (1, "#FFE2D4")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(starfield(rng, 16, 300, 780, 30, 200, avoid=[(640, 150, 60)]))
    o.append(path("M330 440 Q470 380 560 210 Q620 110 690 210 Q760 320 800 360 L800 600 L330 600 Z", fill="#C2D8D2"))
    o.append(path("M600 168 Q610 230 580 290 Q560 340 600 400", stroke="#E3EEE9", sw=6, extra=' stroke-dasharray="2 14"'))
    o.append(sparkle(632, 150, 12, "#FFF6C8"))
    o.append(path("M0 420 Q200 390 420 425 Q620 455 800 420 L800 600 L0 600 Z", fill="#C8E3D6"))
    # orilla de enfrente: el oso con sus moras
    o.append(berry_bush(648, 446, 0.62))
    o.append(bear(728, 446, 0.4, berries=True))
    # el río con patos y un pez
    o.append(path("M0 470 C200 440 400 500 800 455 L800 505 C400 550 200 490 0 522 Z", fill="#BFE0F5"))
    o.append(path("M60 478 Q90 472 120 478 M420 500 Q450 494 480 500 M700 470 Q725 465 750 470", stroke="#E3F2FC", sw=3))
    o.append(duck(252, 503, 0.55) + duck(296, 506, 0.36, baby=True) + duck(326, 504, 0.34, baby=True))
    o.append(fish(372, 452, 0.62, rot=-35))
    o.append(drop(352, 480, 0.5, "#E3F2FC") + drop(392, 478, 0.45, "#E3F2FC") + drop(372, 486, 0.4, "#E3F2FC"))
    o.append(path("M0 525 C200 495 400 548 800 505 L800 600 L0 600 Z", fill="#B3D7C6"))
    # el tronco que empujó el castor
    o.append(log_bridge(590, 532, 668, 452, 18))
    o.append(beaver(712, 566, 0.56, flip=True))
    # el árbol del abuelo Búho, con la ardilla bajando por el tronco
    o.append(path("M108 548 C122 450 118 330 136 250 L178 250 C190 330 186 450 206 548 Z", fill="#C9A98F"))
    o.append(path("M92 556 Q116 546 122 516 L192 516 Q200 546 226 556 Z", fill="#C9A98F"))
    o.append(ellipse(160, 557, 82, 9, "#A3CBB8"))
    o.append(path("M168 342 C220 326 270 322 336 300", stroke="#C9A98F", sw=18))
    o.append(path("M150 300 Q138 330 150 360", stroke="#B8977C", sw=4))
    canopy = [("c", 150, 140, 92), ("c", 66, 190, 58), ("c", 236, 172, 60), ("c", 104, 80, 56), ("c", 200, 74, 56)]
    o.append(cloud_layer(canopy, "#93BBAE", 8) + cloud_layer(canopy, "#A9CDBF"))
    o.append(circle(120, 120, 6, "#C3DDD3") + circle(190, 160, 5, "#C3DDD3") + circle(80, 200, 5, "#C3DDD3"))
    o.append(squirrel(206, 327, 0.46))
    o.append(owl(286, 308, 0.74))
    for tx, ty in [(40, 560), (300, 575), (560, 590), (100, 562), (230, 566), (780, 575)]:
        o.append(tuft(tx, ty, 1.1, "#98C6B1"))
    o.append(pip(470, 578, 1.0, pose="hold", expr="happy", look=(-3, -3), head_rot=-9,
                 holding=twinkle(0, -60, 0.6, "happy", "normal")))
    for fx, fy in [(60, 470), (690, 385), (420, 360), (250, 420)]:
        o.append(circle(fx, fy, 9, url("glow")) + circle(fx, fy, 2.4, "#FFF6C8"))
    return defs, "".join(o)


def pip_ch3():
    rng = random.Random(31)
    defs = lin("sky", [(0, "#A99CD8"), (0.6, "#D7CCF0"), (1, "#F9D9D2")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(starfield(rng, 40, 30, 770, 25, 380, avoid=[(540, 170, 120), (300, 330, 110)]))
    o.append(path("M0 500 Q200 450 400 490 Q600 525 800 470 L800 600 L0 600 Z", fill="#CBE0D9"))
    o.append(path("M0 600 L0 520 Q300 400 600 470 Q700 492 800 520 L800 600 Z", fill="#B3D7C6"))
    for sx, sy, r in [(370, 300, 6), (410, 268, 7), (448, 236, 8), (485, 210, 6)]:
        o.append(sparkle(sx, sy, r, "#FFF6C8", 0.9))
    o.append(twinkle(545, 170, 1.0, "bright", "big", rot=-8))
    # todos los amigos de Pip en la cima
    o.append(deer(58, 496, 0.56))
    o.append(owl(742, 510, 0.34))
    o.append(squirrel(686, 494, 0.52, flip=True))
    o.append(duck(600, 474, 0.44, swim=False, flip=True) + duck(642, 484, 0.34, baby=True, swim=False, flip=True))
    o.append(bear(178, 470, 0.5, expr="joy"))
    o.append(frog(492, 454, 0.5, expr="joy"))
    o.append(milo(548, 462, 0.5, expr="joy", pal=FOREST_MOUSE))
    o.append(pip(290, 452, 1.15, pose="wave", expr="joy", head_rot=-6))
    o.append(rabbit(430, 450, 0.56, expr="joy", flip=True))
    for tx, ty in [(110, 545), (380, 470), (520, 500), (650, 525), (740, 565), (250, 520)]:
        o.append(tuft(tx, ty, 1.1, "#98C6B1"))
    for fx, fy, c in [(120, 560, "#F7B7C3"), (460, 500, "#FFF1BF"), (610, 530, "#E4DCF7"), (700, 560, "#F7B7C3")]:
        o.append(flower(fx, fy, 1.1, c))
    return defs, "".join(o)


# --------------------------------------------------------- Nimbus: escenas

def nimbus_cover():
    defs = lin("sky", [(0, "#BCDBF3"), (0.6, "#D8EAF8"), (1, "#EEF6FB")])
    o = [rect(0, 0, 600, 800, url("sky"))]
    o.append(cloud(120, 130, 1.0, o=0.9) + cloud(500, 200, 0.8, o=0.9, flip=True))
    o.append(rainbow(300, 470, 230, 14))
    o.append(cloud(78, 470, 1.0) + cloud(522, 470, 1.0, flip=True))
    o.append(path("M0 600 Q150 560 300 590 Q450 620 600 570 L600 800 L0 800 Z", fill="#CFEFE3"))
    o.append(path("M0 690 Q300 610 600 690 L600 800 L0 800 Z", fill="#B9E4D2"))
    o.append(nimbus(300, 330, 1.55, "happy", rain=False))
    for dx, dy in [(-40, 430), (10, 470), (60, 440), (-10, 520)]:
        o.append(drop(300 + dx, dy, 1.0, "#A3CDF0"))
    o.append(daisy(300, 720, 1.35))
    for fx, fy, c in [(120, 700, "#F7B7C3"), (180, 740, "#E4DCF7"), (440, 710, "#FFD9CC"), (500, 745, "#F7B7C3")]:
        o.append(flower(fx, fy, 1.2, c))
    for tx, ty in [(70, 720), (240, 760), (380, 765), (540, 720)]:
        o.append(tuft(tx, ty, 1.2, "#9FD6BF"))
    return defs, "".join(o)


def fields(clip_d, colors, x0=0, x1=800, y0=360, y1=600, step=46):
    clip = f'<clipPath id="{uid("fields")}"><path d="{clip_d}"/></clipPath>'
    bands = [path(clip_d, fill=colors[0])]
    i = 0
    for bx in range(x0 - 400, x1 + 400, step):
        bands.append(path(f"M{bx} {y1} L{bx + step / 2 + 220} {y0} L{bx + step + 220} {y0} L{bx + step / 2} {y1} Z",
                          fill=colors[1 + i % (len(colors) - 1)]))
        i += 1
    return clip, f'<g clip-path="{url("fields")}">' + "".join(bands) + "</g>"


def nimbus_ch1():
    rng = random.Random(41)
    defs = lin("sky", [(0, "#C5D4E9"), (0.65, "#DCE7F3"), (1, "#EEF3F7")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    clip, stripes = fields("M0 410 Q200 362 400 392 Q600 424 800 372 L800 600 L0 600 Z", ["#CFEFE3", "#BEE6D3", "#E6F2CB", "#CFEFE3"])
    defs += clip
    o.append(sun(716, 88, 30))
    # montañas detrás del bosque
    o.append(mountain(130, 400, 340, 190, "#C9C3E3", snow="#F6F3FC"))
    o.append(mountain(390, 400, 400, 236, "#BDB6DC", snow="#F6F3FC"))
    o.append(mountain(650, 400, 340, 128, "#CBC5E4"))
    o.append(path("M0 380 Q160 330 330 360 Q520 395 800 340 L800 420 L0 420 Z", fill="#D9EADF"))
    o.append(rain_field(rng, 130, 380, 210, 400, 26) + rain_field(rng, 420, 600, 190, 390, 20))
    o.append(stripes)
    # el río entre los campos
    o.append(path("M552 410 C530 446 600 470 548 516 C508 552 470 572 462 600 L570 600 C578 570 616 552 646 518 "
                  "C694 466 606 444 576 410 Z", fill="#BFE0F5"))
    o.append(path("M560 440 Q570 436 580 440 M560 530 Q575 524 590 530 M500 580 Q515 574 530 580", stroke="#E3F2FC", sw=3))
    # el bosque
    for px, py, ps, c1, c2 in [(30, 404, 0.62, "#9CCDB3", "#86BFA2"), (80, 398, 0.78, "#A6D3BB", "#8FC5A9"),
                               (138, 392, 0.66, "#9CCDB3", "#86BFA2"), (190, 392, 0.82, "#A6D3BB", "#8FC5A9"),
                               (246, 394, 0.64, "#9CCDB3", "#86BFA2"), (296, 398, 0.74, "#A6D3BB", "#8FC5A9")]:
        o.append(pine(px, py, ps, c1, c2))
    o.append(round_tree(112, 410, 0.7) + round_tree(222, 408, 0.6) + round_tree(330, 410, 0.62))
    o.append(big_cloud(250, 150, 0.95, "kind"))
    o.append(big_cloud(510, 128, 0.78, "sleepy", flip=True))
    o.append(nimbus(680, 292, 0.72, "strain"))
    for tx, ty in [(60, 560), (260, 585), (700, 570), (380, 590)]:
        o.append(tuft(tx, ty, 1.1, "#A7D9C3"))
    return defs, "".join(o)


def valley_backdrop():
    """Montaña nevada, lago y valle con rocas detrás del jardín (capítulos 2 y 3)."""
    o = [mountain(338, 414, 270, 118, "#D8D2EC")]
    o.append(mountain(168, 414, 390, 204, "#C9C3E3", snow="#FBFAFE"))
    o.append(ellipse(478, 400, 150, 16, "#A9D2F0") + path("M404 398 Q422 394 440 398 M500 402 Q518 398 536 402", stroke="#D6EBFA", sw=2.6))
    for rx, ry, rs in [(36, 418, 0.7), (78, 420, 0.5), (262, 416, 0.8), (300, 420, 0.55)]:
        o.append(rock(rx, ry, rs))
    return "".join(o)


def garden(lush, shadow=False):
    """Jardín compartido por los capítulos 2 y 3 de Nimbus."""
    o = []
    o.append(path("M0 420 Q400 388 800 420 L800 600 L0 600 Z", fill="#CFEFE3" if lush else "#E9E4C2"))
    o.append(house(640, 468, 1.0))
    o.append(path("M0 470 Q400 440 800 470 L800 600 L0 600 Z", fill="#BDE6D2" if lush else "#DEDAB4"))
    o.append(garden_tree(84, 512, 0.82, lush))
    o.append(fence(150, 520, 492, 38))
    o.append(ellipse(330, 545, 210, 34, "#D9BFA4" if lush else "#E2CDB2"))
    if not lush:
        o.append(path("M178 540 L198 548 L214 541 M262 560 L280 552 L298 560 L312 554 M386 536 L402 544 L420 538 "
                      "M448 556 L466 550 L480 558", stroke="#CBAE8C", sw=2.4))
    if shadow:
        o.append(ellipse(330, 548, 130, 20, PLUM, extra=op(0.07)))
    spots = [(180, 545, "#F7B7C3"), (230, 560, "#E4DCF7"), (270, 538, "#FFD9CC"), (410, 540, "#F7B7C3"),
             (450, 560, "#E4DCF7"), (490, 545, "#FFD9CC")]
    for fx, fy, c in spots:
        if lush:
            o.append(flower(fx, fy, 1.35, c, "#FFE38A", 40))
        else:
            o.append(flower(fx, fy, 1.35, {"#F7B7C3": "#E9CFC8", "#E4DCF7": "#DCD6E0", "#FFD9CC": "#EED8C4"}[c], "#E8D6A0", 40, droopy=True))
    o.append(daisy(330, 560, 1.25, droopy=not lush))
    for tx, ty in [(40, 575), (130, 592), (600, 585), (740, 570)]:
        o.append(tuft(tx, ty, 1.2, "#9FD6BF" if lush else "#CBB98E"))
    return "".join(o)


def nimbus_ch2():
    defs = lin("sky", [(0, "#CFE4F5"), (0.7, "#F3F1DC"), (1, "#FFF1C4")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(120, 105, 44))
    o.append(valley_backdrop())
    o.append(garden(lush=False, shadow=True))
    o.append(nimbus(330, 200, 1.0, "sad"))
    return defs, "".join(o)


def nimbus_ch3():
    rng = random.Random(61)
    defs = lin("sky", [(0, "#C2DFF5"), (0.7, "#E2F0FA"), (1, "#F1F8FC")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(690, 112, 40))
    o.append(cloud(640, 140, 0.9))
    o.append(valley_backdrop())
    o.append(rainbow(400, 470, 330, 16, 0.92))
    o.append(garden(lush=True))
    o.append(rain_field(rng, 250, 410, 300, 480, 14, "#A3CDF0", 0.8))
    o.append(nimbus(330, 200, 1.0, "joy", rain=True))
    for sx, sy in [(200, 500), (470, 505), (560, 520)]:
        o.append(sparkle(sx, sy, 7, WHITE, 0.9))
    return defs, "".join(o)


# ---------------------------------------------------------- Benny: escenas

def benny_cover():
    defs = lin("sky", [(0, "#CDEEDF"), (0.6, "#E6F7EE"), (1, "#F8FCF6")])
    o = [rect(0, 0, 600, 800, url("sky"))]
    o.append(sun(470, 120, 38))
    o.append(cloud(130, 140, 0.9) + cloud(330, 220, 0.6, o=0.9))
    o.append(path("M0 520 Q150 470 300 500 Q460 530 600 480 L600 800 L0 800 Z", fill="#D3F0E1"))
    o.append(fruit_tree(118, 640, 1.0, "apple") + fruit_tree(486, 640, 1.0, "lemon"))
    o.append(path("M0 650 Q300 590 600 650 L600 800 L0 800 Z", fill="#BCE5CF"))
    for sx, sy, ss in [(84, 722, 1.1), (520, 728, 1.1), (186, 768, 0.9), (420, 770, 0.9)]:
        o.append(strawberry_plant(sx, sy, ss))
    o.append(benny(300, 715, 1.55, pose="wave", expr="joy"))
    o.append(apple(386, 518, 1.35))  # la manzana en la pata levantada
    for tx, ty in [(40, 700), (140, 745), (470, 700), (565, 760)]:
        o.append(tuft(tx, ty, 1.3, "#9FD6BF"))
    return defs, "".join(o)


def benny_ch1():
    defs = lin("sky", [(0, "#D6F1E5"), (0.7, "#F1FAF4"), (1, "#FFF8F0")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(110, 100, 36))
    o.append(cloud(560, 110, 0.9) + cloud(320, 70, 0.6, o=0.85))
    o.append(round_tree(470, 352, 0.8) + round_tree(720, 346, 1.0) + round_tree(770, 344, 0.75))
    o.append(path("M0 360 Q200 320 420 350 Q620 378 800 335 L800 600 L0 600 Z", fill="#D5F0E2"))
    o.append(path("M0 410 Q400 380 800 410 L800 600 L0 600 Z", fill="#C2E8D4"))
    o.append(soil_row(80, 720, 448, 22))
    o.append(soil_row(40, 760, 500, 26))
    o.append(lemon_sapling(522, 494, 0.85))
    o.append(benny(300, 548, 1.1, pose="plant", expr="happy", look=(2, 2)))
    o.append(soil_row(0, 800, 572, 32))
    o.append(watering_can(440, 552, 0.95))
    o.append(tilly(660, 545, 0.85, flip=True, expr="calm"))
    o.append(seed_bag(172, 590, 1.05))
    for sx, sy in [(222, 540), (250, 546), (560, 542)]:
        o.append(ellipse(sx, sy, 3.6, 5, "#B98B6B"))
    for tx, ty in [(30, 600), (790, 598)]:
        o.append(tuft(tx, ty, 1.2, "#9FD6BF"))
    return defs, "".join(o)


def benny_ch2():
    defs = lin("sky", [(0, "#D2EFE2"), (0.7, "#EFF9F3"), (1, "#FFF8F0")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(680, 95, 38))
    o.append(cloud(170, 100, 0.85) + cloud(450, 70, 0.6, o=0.85))
    o.append(round_tree(60, 344, 1.0) + round_tree(110, 340, 0.75) + round_tree(520, 358, 0.8))
    o.append(path("M0 360 Q200 320 420 350 Q620 378 800 335 L800 600 L0 600 Z", fill="#D5F0E2"))
    o.append(path("M0 410 Q400 380 800 410 L800 600 L0 600 Z", fill="#C2E8D4"))
    o.append(soil_row(80, 720, 448, 22))
    for sx in range(150, 640, 62):
        o.append(sprout(sx, 438, 0.9))
    o.append(lemon_sapling(700, 444, 1.15, bump=True))
    o.append(soil_row(40, 760, 500, 26))
    for i, sx in enumerate(range(110, 720, 70)):
        if i % 2 == 0:
            o.append(strawberry_plant(sx, 492, 0.85, flowers=True, berries=False))
        else:
            o.append(sprout(sx, 488, 1.1))
    o.append(path("M290 540 Q300 528 310 540 M330 546 Q345 532 360 546", stroke="#9FD6BF", sw=3.5))
    o.append(benny(330, 500, 1.0, pose="hop", expr="joy"))
    o.append(soil_row(0, 800, 572, 32))
    for sx in range(60, 780, 80):
        o.append(sprout(sx, 556, 1.3))
    o.append(tilly(140, 560, 0.8, expr="calm", nod=True))
    o.append(leaf(640, 585, 120, -72, "#B4E2C0", "#8CCB9B"))
    o.append(milo(600, 545, 0.95, body=False))
    o.append(leaf(500, 578, 196, -8, "#9ED7AE", "#86C79A"))
    o.append(blueberries(600, 506, 0.9))
    o.append(milo_paws(600, 545, 0.95))
    return defs, "".join(o)


def benny_ch3():
    defs = lin("sky", [(0, "#FFDDBE"), (0.55, "#FFEFC8"), (1, "#FFF8EA")])
    defs += (f'<pattern id="{uid("check")}" width="40" height="40" patternUnits="userSpaceOnUse">'
             f'<rect width="40" height="40" fill="#FFF4EC"/><rect width="20" height="40" fill="#FFC6B4" opacity="0.6"/>'
             f'<rect width="40" height="20" fill="#FFC6B4" opacity="0.6"/></pattern>')
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(400, 214, 50))
    o.append(path("M0 330 Q200 300 420 325 Q620 350 800 315 L800 600 L0 600 Z", fill="#D9EDCB"))
    o.append(fruit_tree(96, 420, 0.86, "apple") + fruit_tree(704, 420, 0.86, "lemon"))
    o.append(path("M0 400 Q400 370 800 400 L800 600 L0 600 Z", fill="#CBE6BC"))
    o.append(path("M170 448 L630 448 L720 572 L80 572 Z", fill=url("check")))
    # la fruta sobre el mantel
    o.append(apple(338, 470, 0.9) + apple(366, 476, 0.8, "#B8DD8C") + pear(392, 468, 0.85))
    o.append(cherries(512, 466, 0.9))
    o.append(basket(596, 486, 0.82, orange(-16, -24, 0.9) + orange(10, -28, 0.9) + orange(0, -14, 0.85) + orange(22, -16, 0.8)))
    salad = (orange(-18, -18, 0.6) + strawberry(-2, -22, 0.7) + grapes(16, -20, 0.4)
             + banana(4, -12, 0.5, 10) + cherries(-14, -30, 0.5) + apple(14, -30, 0.45))
    o.append(bowl(452, 506, 1.35, salad))
    o.append(watermelon_slice(336, 548, 0.9, -8) + watermelon_slice(378, 556, 0.85, 10))
    o.append(pitcher(190, 532, 0.72))
    o.append(grandma_bunny(104, 548, 0.8))
    o.append(benny(268, 525, 0.9, pose="hold", expr="joy", holding=strawberry(0, -64, 1.2)))
    o.append(tilly(658, 552, 0.7, flip=True, expr="calm"))
    o.append(banana(566, 566, 0.75, -10))
    o.append(milo(520, 562, 0.9, expr="joy", holding=grapes(0, -40, 0.5)))
    for tx, ty in [(30, 590), (775, 595), (40, 470), (760, 470)]:
        o.append(tuft(tx, ty, 1.2, "#A9D29A"))
    return defs, "".join(o)


SCENES = [
    ("pip", "cover", 600, 800, "Pip the fox holding a glowing little star at night", pip_cover),
    ("pip", "ch1", 800, 600, "Pip finds a crying little star in the meadow, with a frog, a rabbit and a mouse", pip_ch1),
    ("pip", "ch2", 800, 600, "Pip and Twinkle by the river with Grandpa Owl, a squirrel, ducks, a fish, a beaver and a bear", pip_ch2),
    ("pip", "ch3", 800, 600, "Twinkle floats back up to the sky while Pip and his animal friends wave", pip_ch3),
    ("nimbus", "cover", 600, 800, "Nimbus the little cloud smiling over a rainbow and a daisy", nimbus_cover),
    ("nimbus", "ch1", 800, 600, "Big rain clouds over the mountains, the forest and the river while little Nimbus tries to rain", nimbus_ch1),
    ("nimbus", "ch2", 800, 600, "Nimbus finds a thirsty garden below a snowy mountain and a lake", nimbus_ch2),
    ("nimbus", "ch3", 800, 600, "Nimbus rains on the garden and a rainbow appears", nimbus_ch3),
    ("benny", "cover", 600, 800, "Benny the bunny holding a red apple between an apple tree and a lemon tree", benny_cover),
    ("benny", "ch1", 800, 600, "Benny plants fruit seeds and a baby lemon tree while Tilly the turtle walks by", benny_ch1),
    ("benny", "ch2", 800, 600, "Benny hops next to sprouts and strawberry flowers while Milo shares blueberries", benny_ch2),
    ("benny", "ch3", 800, 600, "Benny, Grandma, Tilly and Milo share a fruit picnic", benny_ch3),
]


def main():
    global _P
    for book, name, w, h, title, fn in SCENES:
        _P = f"{book}-{name}"
        defs, body = fn()
        out, size = write_svg(book, name, w, h, title, defs, body)
        print(f"{os.path.relpath(out, ROOT)}  {size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
