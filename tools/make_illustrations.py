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


RAINBOW = ["#F7B7C3", "#FFD3B0", "#FFF0B5", "#CFEFE3", "#C6E0F5", "#DCD2F3"]


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


def benny(x, y, s=1.0, flip=False, pose="stand", expr="happy", holding="", look=(0, 0)):
    """Benny, el conejo. Origen: entre las patas, a nivel del suelo."""
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
    return g("".join(o), x, y, s, flip=flip)


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


def milo(x, y, s=1.0, flip=False, expr="happy", body=True, holding=""):
    """Milo, el ratoncito. Origen: entre las patas, a nivel del suelo."""
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
    o.append(blades(rng, 70, 0, 800, 425, 470, 30, 70, ["#9CCAB5", "#A6D0BC", "#93C2AC"]))
    for fx, fy in [(80, 470), (160, 455), (690, 465), (740, 480), (430, 450)]:
        o.append(flower(fx, fy, 1.0, "#FFFFFF", "#FFE38A", 40))
    o.append(twinkle(565, 505, 0.78, "cry", "dim", rot=18))
    o.append(pip(300, 548, 1.2, pose="step", expr="curious", look=(3, 1), lean=5))
    o.append(blades(rng, 40, 0, 800, 560, 610, 30, 60, ["#93C2AC", "#8BBDA6", "#9CCAB5"]))
    o.append(blade(520, 548, 52, -6, "#93C2AC") + blade(612, 552, 46, 8, "#8BBDA6") + blade(592, 556, 40, -4, "#9CCAB5"))
    for fx, fy in [(60, 590), (220, 600), (700, 595), (760, 585)]:
        o.append(flower(fx, fy, 1.2, "#FFFFFF", "#FFE38A", 46))
    for fx, fy in [(420, 380), (690, 360), (210, 330), (630, 420)]:
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
    o.append(path("M0 470 C200 440 400 500 800 455 L800 505 C400 550 200 490 0 522 Z", fill="#BFE0F5"))
    o.append(path("M60 478 Q90 472 120 478 M300 490 Q330 484 360 490 M560 478 Q590 472 620 478 M700 470 Q725 465 750 470",
                  stroke="#E3F2FC", sw=3))
    for sx, sy, rx in [(470, 498, 26), (560, 486, 24), (650, 476, 22), (735, 468, 20)]:
        o.append(ellipse(sx, sy + 4, rx, 9, "#B9AFCB") + ellipse(sx, sy, rx, 9, "#DCD4E6"))
    o.append(path("M0 525 C200 495 400 548 800 505 L800 600 L0 600 Z", fill="#B3D7C6"))
    o.append(path("M108 548 C122 450 118 330 136 250 L178 250 C190 330 186 450 206 548 Z", fill="#C9A98F"))
    o.append(path("M92 556 Q116 546 122 516 L192 516 Q200 546 226 556 Z", fill="#C9A98F"))
    o.append(ellipse(160, 557, 82, 9, "#A3CBB8"))
    o.append(path("M168 342 C220 326 270 322 336 300", stroke="#C9A98F", sw=18))
    o.append(path("M150 300 Q138 330 150 360", stroke="#B8977C", sw=4))
    canopy = [("c", 150, 140, 92), ("c", 66, 190, 58), ("c", 236, 172, 60), ("c", 104, 80, 56), ("c", 200, 74, 56)]
    o.append(cloud_layer(canopy, "#93BBAE", 8) + cloud_layer(canopy, "#A9CDBF"))
    o.append(circle(120, 120, 6, "#C3DDD3") + circle(190, 160, 5, "#C3DDD3") + circle(80, 200, 5, "#C3DDD3"))
    o.append(owl(286, 308, 0.74))
    for tx, ty in [(40, 560), (300, 575), (720, 560), (560, 590), (100, 562), (222, 566)]:
        o.append(tuft(tx, ty, 1.1, "#98C6B1"))
    o.append(pip(460, 578, 1.0, pose="hold", expr="happy", look=(-3, -3), head_rot=-9,
                 holding=twinkle(0, -60, 0.6, "happy", "normal")))
    for fx, fy in [(60, 470), (690, 385), (380, 360), (250, 420)]:
        o.append(circle(fx, fy, 9, url("glow")) + circle(fx, fy, 2.4, "#FFF6C8"))
    return defs, "".join(o)


def pip_ch3():
    rng = random.Random(31)
    defs = lin("sky", [(0, "#A99CD8"), (0.6, "#D7CCF0"), (1, "#F9D9D2")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(starfield(rng, 44, 30, 770, 25, 430, avoid=[(540, 170, 120), (300, 330, 110)]))
    o.append(path("M0 500 Q200 450 400 490 Q600 525 800 470 L800 600 L0 600 Z", fill="#CBE0D9"))
    o.append(path("M0 600 L0 520 Q300 400 600 470 Q700 492 800 520 L800 600 Z", fill="#B3D7C6"))
    for i, (sx, sy, r) in enumerate([(370, 300, 6), (410, 268, 7), (448, 236, 8), (485, 210, 6)]):
        o.append(sparkle(sx, sy, r, "#FFF6C8", 0.9))
    o.append(twinkle(545, 170, 1.0, "bright", "big", rot=-8))
    o.append(pip(290, 452, 1.15, pose="wave", expr="joy", head_rot=-6))
    for tx, ty in [(80, 540), (150, 520), (430, 470), (520, 500), (650, 520), (740, 560)]:
        o.append(tuft(tx, ty, 1.1, "#98C6B1"))
    for fx, fy, c in [(120, 540, "#F7B7C3"), (470, 490, "#FFF1BF"), (600, 515, "#E4DCF7"), (700, 545, "#F7B7C3")]:
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
    o.append(path("M0 380 Q160 330 330 360 Q520 395 800 340 L800 420 L0 420 Z", fill="#D9EADF"))
    o.append(rain_field(rng, 130, 380, 210, 400, 26) + rain_field(rng, 420, 600, 190, 390, 20))
    o.append(stripes)
    o.append(big_cloud(250, 150, 0.95, "kind"))
    o.append(big_cloud(510, 128, 0.78, "sleepy", flip=True))
    o.append(nimbus(680, 292, 0.72, "strain"))
    for tx, ty in [(60, 560), (260, 585), (520, 570), (730, 580)]:
        o.append(tuft(tx, ty, 1.1, "#A7D9C3"))
    return defs, "".join(o)


def garden(lush, shadow=False):
    """Jardín compartido por los capítulos 2 y 3 de Nimbus."""
    o = []
    o.append(path("M0 420 Q400 388 800 420 L800 600 L0 600 Z", fill="#CFEFE3" if lush else "#E9E4C2"))
    o.append(house(640, 468, 1.0))
    o.append(path("M0 470 Q400 440 800 470 L800 600 L0 600 Z", fill="#BDE6D2" if lush else "#DEDAB4"))
    o.append(fence(150, 520, 492, 38))
    o.append(ellipse(330, 545, 210, 34, "#D9BFA4" if lush else "#E2CDB2"))
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
    for tx, ty in [(40, 560), (110, 590), (600, 585), (740, 570)]:
        o.append(tuft(tx, ty, 1.2, "#9FD6BF" if lush else "#CBCC9E"))
    return "".join(o)


def nimbus_ch2():
    defs = lin("sky", [(0, "#CFE4F5"), (0.7, "#F3F1DC"), (1, "#FFF1C4")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(120, 105, 44))
    o.append(garden(lush=False, shadow=True))
    o.append(nimbus(330, 200, 1.0, "sad"))
    return defs, "".join(o)


def nimbus_ch3():
    rng = random.Random(61)
    defs = lin("sky", [(0, "#C2DFF5"), (0.7, "#E2F0FA"), (1, "#F1F8FC")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(690, 112, 40))
    o.append(cloud(640, 140, 0.9))
    o.append(rainbow(400, 470, 330, 16, 0.9))
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
    o.append(sun(470, 130, 40))
    o.append(cloud(130, 150, 0.9) + cloud(380, 230, 0.6, o=0.9))
    o.append(path("M0 520 Q150 470 300 500 Q460 530 600 480 L600 800 L0 800 Z", fill="#D3F0E1"))
    o.append(sunflower(110, 640, 300, tilt=-10) + sunflower(500, 650, 330, tilt=12) + sunflower(200, 600, 220, 0.85, tilt=-4)
             + sunflower(410, 600, 250, 0.8, tilt=8))
    o.append(path("M0 650 Q300 590 600 650 L600 800 L0 800 Z", fill="#BCE5CF"))
    o.append(benny(300, 715, 1.55, pose="hold", expr="joy", holding=carrot(30, -82, 1.0, rot=40)))
    for tx, ty in [(70, 700), (130, 750), (470, 705), (540, 750)]:
        o.append(tuft(tx, ty, 1.3, "#9FD6BF"))
    for fx, fy, c in [(100, 735, "#FFF1BF"), (500, 730, "#F7B7C3"), (210, 770, "#E4DCF7"), (400, 772, "#FFD9CC")]:
        o.append(flower(fx, fy, 1.1, c))
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
    o.append(benny(300, 548, 1.1, pose="plant", expr="happy", look=(2, 2)))
    o.append(soil_row(0, 800, 572, 32))
    o.append(watering_can(440, 552, 0.95))
    o.append(tilly(650, 545, 0.85, flip=True, expr="calm"))
    for sx, sy in [(200, 538), (240, 544), (520, 542)]:
        o.append(ellipse(sx, sy, 3.6, 5, "#B98B6B"))
    for tx, ty in [(30, 600), (790, 598)]:
        o.append(tuft(tx, ty, 1.2, "#9FD6BF"))
    return defs, "".join(o)


def benny_ch2():
    defs = lin("sky", [(0, "#D2EFE2"), (0.7, "#EFF9F3"), (1, "#FFF8F0")])
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(680, 95, 38))
    o.append(cloud(170, 100, 0.85) + cloud(450, 70, 0.6, o=0.85))
    o.append(round_tree(60, 344, 1.0) + round_tree(110, 340, 0.75) + round_tree(560, 358, 0.8))
    o.append(path("M0 360 Q200 320 420 350 Q620 378 800 335 L800 600 L0 600 Z", fill="#D5F0E2"))
    o.append(path("M0 410 Q400 380 800 410 L800 600 L0 600 Z", fill="#C2E8D4"))
    o.append(soil_row(80, 720, 448, 22))
    for sx in range(150, 680, 62):
        o.append(sprout(sx, 438, 0.9))
    o.append(soil_row(40, 760, 500, 26))
    for sx in range(110, 720, 70):
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
    o.append(milo_paws(600, 545, 0.95))
    return defs, "".join(o)


def benny_ch3():
    defs = lin("sky", [(0, "#FFDDBE"), (0.55, "#FFEFC8"), (1, "#FFF8EA")])
    defs += (f'<pattern id="{uid("check")}" width="40" height="40" patternUnits="userSpaceOnUse">'
             f'<rect width="40" height="40" fill="#FFF4EC"/><rect width="20" height="40" fill="#FFC6B4" opacity="0.6"/>'
             f'<rect width="40" height="20" fill="#FFC6B4" opacity="0.6"/></pattern>')
    o = [rect(0, 0, 800, 600, url("sky"))]
    o.append(sun(660, 250, 54))
    o.append(path("M0 330 Q200 300 420 325 Q620 350 800 315 L800 600 L0 600 Z", fill="#D9EDCB"))
    for sx, h, t, sc in [(70, 290, -8, 1.0), (180, 250, 4, 0.9), (560, 240, -4, 0.85), (730, 300, 10, 1.0), (320, 230, 6, 0.75)]:
        o.append(sunflower(sx, 420, h, sc, tilt=t))
    o.append(path("M0 400 Q400 370 800 400 L800 600 L0 600 Z", fill="#CBE6BC"))
    o.append(path("M170 448 L630 448 L720 572 L80 572 Z", fill=url("check")))
    o.append(benny(220, 520, 0.92, pose="hold", expr="joy", holding=strawberry(0, -64, 1.2)))
    o.append(cake(400, 500, 1.0))
    o.append(bowl(500, 478, 0.9, strawberry(-14, -18, 0.9) + strawberry(6, -22, 0.9, 20) + strawberry(20, -14, 0.8, -15)))
    o.append(tomato(300, 470, 1.0) + tomato(322, 476, 0.85))
    o.append(tilly(600, 548, 0.72, flip=True, expr="calm"))
    o.append(milo(450, 556, 0.95, expr="joy", holding=strawberry(0, -36, 0.7)))
    o.append(crow(700, 472, 0.85, flip=True))
    for tx, ty in [(40, 590), (770, 595), (60, 470)]:
        o.append(tuft(tx, ty, 1.2, "#A9D29A"))
    return defs, "".join(o)


SCENES = [
    ("pip", "cover", 600, 800, "Pip the fox holding a glowing little star at night", pip_cover),
    ("pip", "ch1", 800, 600, "Pip finds a crying little star in the meadow", pip_ch1),
    ("pip", "ch2", 800, 600, "Pip and Twinkle ask Grandpa Owl the way to the tallest hill", pip_ch2),
    ("pip", "ch3", 800, 600, "Twinkle floats back up to the sky while Pip waves", pip_ch3),
    ("nimbus", "cover", 600, 800, "Nimbus the little cloud smiling over a rainbow and a daisy", nimbus_cover),
    ("nimbus", "ch1", 800, 600, "Big rain clouds over the fields while little Nimbus tries to rain", nimbus_ch1),
    ("nimbus", "ch2", 800, 600, "Nimbus finds a thirsty garden next to a little yellow house", nimbus_ch2),
    ("nimbus", "ch3", 800, 600, "Nimbus rains on the garden and a rainbow appears", nimbus_ch3),
    ("benny", "cover", 600, 800, "Benny the bunny holding a carrot among sunflowers", benny_cover),
    ("benny", "ch1", 800, 600, "Benny plants tiny seeds while Tilly the turtle walks by", benny_ch1),
    ("benny", "ch2", 800, 600, "Benny hops next to the first sprouts while Milo peeks from a leaf", benny_ch2),
    ("benny", "ch3", 800, 600, "Benny, Tilly, Milo and a crow share a picnic in the garden", benny_ch3),
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
