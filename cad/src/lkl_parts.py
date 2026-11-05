"""LeakListen repo-specific CAD helpers beside .kit/cad_parts.py (kit 1.9).

Small solids and fasteners the parts library does not have (socket and pan head screws, hex standoffs,
R-clips, compressed O-rings, PCB assemblies), custom materials for plastics and electronics, and the plain
build123d helpers that cad/src/model.py has always used (zspan, boxspan, hexprism, ring, ...).
All sizes in millimetres. Nothing here is a design dimension: those live in model.PARAMS.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / ".kit")]
import build123d as b  # noqa: E402
import cad_parts as cp  # noqa: E402

# ---------------------------------------------------------------------------------------------------------
# Materials the library lacks (name -> (colour, render class photoreal.py knows, density kg/m3)).
# They are added to cad_parts.MATERIALS when this module is imported, so cad_check.py and the renderers see them.
# ---------------------------------------------------------------------------------------------------------
EXTRA_MATERIALS = {
    "pvc_grey":     ("#D8DADC", "plastic_tank", 1400),     # PVC-U pressure pipe
    "acetal_black": ("#2B2F36", "hdpe", 1410),             # turned POM-C plugs
    "petg_teal":    ("#0F766E", "plastic_tank", 1270),     # printed chassis
    "nylon_white":  ("#EDEDE8", "plastic_tank", 1140),     # nylon standoffs, inserts
    "acrylic_clear": ("#DDE6EA", "clear", 1190),           # light pipe rod
    "nitrile":      ("#151617", "rubber", 1200),           # O-rings
    "fr4_green":    ("#166534", "painted", 1850),          # printed circuit boards
    "ic_black":     ("#111827", "matte_black", 1800),      # chips and connectors
    "ndfeb":        ("#6B7280", "metal", 7500),            # neodymium magnet
    "li_cell":      ("#1E3A5F", "plastic_tank", 3300),     # C cell (can and contents, mass from catalogue 90 g)
    "capacitor":    ("#1E3A5F", "plastic_tank", 2200),     # hybrid layer capacitor
    "epoxy_potting": ("#1F2937", "matte_black", 1100),     # potting compound
    "pu_black":     ("#1C1F24", "rubber", 1100),           # polyurethane cable jackets and potting
    "antenna_white": ("#E9EAEC", "plastic_tank", 1100),    # flat antenna radome
    "desiccant_pouch": ("#EDEDEA", "fabric", 700),         # silica gel pouch
    "ceramic_piezo": ("#C9C5BD", "painted_white", 7600),   # PZT ceramic
    "hdpe_box":     ("#2B4A43", "hdpe", 950),
}
for _k, _v in EXTRA_MATERIALS.items():
    cp.MATERIALS.setdefault(_k, _v)


def mk(key, name, shape, material, kind="made", bom=None, **kw):
    """cad_parts.part() with a short key (the name the build plan pictures and the product model use)."""
    p = cp.part(name, shape, material, kind=kind, bom=bom, **kw)
    p["key"] = key
    return p


# ---------------------------------------------------------------------------------------------------------
# Plain build123d helpers (as cad/src/model.py has always had them)
# ---------------------------------------------------------------------------------------------------------
def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def tube(a, c, r):
    """Solid rod of radius r between two 3D points."""
    a, c = b.Vector(*a), b.Vector(*c)
    v = c - a
    return b.Solid.make_cylinder(r, v.length, b.Plane(origin=a, z_dir=v.normalized()))


def path(points, r, joints=True):
    """Polyline rod with a ball at each bend so it reads as one cable."""
    s = fuse(tube(a, c, r) for a, c in zip(points, points[1:]))
    if joints:
        for q in points[1:-1]:
            s = s + b.Pos(*q) * b.Sphere(r)
    return s


def smooth(points, n=2):
    """Chaikin corner cutting, end points kept: a soft cable bend through the same route."""
    pts = [tuple(q) for q in points]
    for _ in range(n):
        new = [pts[0]]
        for a, c in zip(pts, pts[1:]):
            new.append(tuple(0.75 * a[i] + 0.25 * c[i] for i in range(3)))
            new.append(tuple(0.25 * a[i] + 0.75 * c[i] for i in range(3)))
        new.append(pts[-1])
        pts = new
    return pts


def zcyl(x, y, z, r, h):
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def zspan(x, y, z0, z1, r):
    return zcyl(x, y, (z0 + z1) / 2, r, abs(z1 - z0))


def ycyl(x, y0, y1, z, r):
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, abs(y1 - y0))


def xcyl(x0, x1, y, z, r):
    return b.Pos((x0 + x1) / 2, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, abs(x1 - x0))


def box(x, y, z, sx, sy, sz):
    return b.Pos(x, y, z) * b.Box(sx, sy, sz)


def boxspan(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def hexprism(x, y, z0, z1, af):
    """Hexagon, across flats af, between heights z0 < z1."""
    return b.Pos(x, y, z0) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), amount=abs(z1 - z0))


def ring(x, y, z0, z1, ri, ro):
    return zspan(x, y, z0, z1, ro) - zspan(x, y, z0 - 1, z1 + 1, ri)


def soften(shape, r=0.4):
    """cad_parts.break_edges with a quiet fallback (returns the shape unchanged if no edge break is possible)."""
    return cp.break_edges(shape, r)


# ---------------------------------------------------------------------------------------------------------
# Placing library parts (built along +Z, head or top at z = 0) on any axis
# ---------------------------------------------------------------------------------------------------------
_TURN = {"+z": b.Rot(0, 0, 0), "-z": b.Rot(180, 0, 0), "+x": b.Rot(0, 90, 0), "-x": b.Rot(0, -90, 0),
         "+y": b.Rot(-90, 0, 0), "-y": b.Rot(90, 0, 0)}


def put(shape, xyz, direction="+z", spin=0.0):
    """Place a shape built along +Z so that its +Z points along `direction`, origin at xyz."""
    return b.Pos(*xyz) * _TURN[direction] * b.Rot(0, 0, spin) * shape


def radial(shape, cx, cy, z, r, ang_deg):
    """Place a +Z-built shape at radius r, angle ang (degrees from +X) about a vertical axis through (cx, cy), with its
    +Z pointing radially outward."""
    a = math.radians(ang_deg)
    return b.Pos(cx + r * math.cos(a), cy + r * math.sin(a), z) * b.Rot(0, 0, ang_deg) * b.Rot(0, 90, 0) * shape


# ---------------------------------------------------------------------------------------------------------
# Fasteners the library does not have
# ---------------------------------------------------------------------------------------------------------
def pan_screw(d, length, head_d, head_k, recess=True):
    """Pan-head machine screw (ISO 7045 style): head on top (z 0 to head_k), shank from z 0 down to -length,
    rounded head, cross-slot drawn as a hex socket recess."""
    head = b.Pos(0, 0, head_k / 2) * b.Cylinder(head_d / 2, head_k)
    head = cp.break_edges(head, min(head_k * 0.35, 0.8))
    if recess:
        head = head - b.Pos(0, 0, head_k) * b.extrude(b.RegularPolygon(d * 0.45, 6), amount=-head_k * 0.55)
    shank = b.Pos(0, 0, -length / 2) * b.Cylinder(d / 2, length)
    try:
        shank = b.chamfer(shank.edges().sort_by(b.Axis.Z)[0], d * 0.1)
    except Exception:
        pass
    return head + shank


def socket_screw(d, length):
    """ISO 4762 socket head cap screw Md x length: head on top, shank down."""
    dk = {3: 5.5, 4: 7.0, 5: 8.5, 6: 10.0, 8: 13.0}[d]
    k = d
    head = cp.break_edges(b.Pos(0, 0, k / 2) * b.Cylinder(dk / 2, k), 0.3)
    head = head - b.Pos(0, 0, k) * b.extrude(b.RegularPolygon(d * 0.55, 6), amount=-k * 0.6)
    shank = b.Pos(0, 0, -length / 2) * b.Cylinder(d / 2, length)
    try:
        shank = b.chamfer(shank.edges().sort_by(b.Axis.Z)[0], d * 0.1)
    except Exception:
        pass
    return head + shank


def hex_standoff(af, length, thread_d, stud_len, bore_depth):
    """Male-female hex standoff: hex body of `length` from z = 0 up, a threaded stud of stud_len below z = 0,
    a tapped bore at the top (drawn as a plain hole of the thread diameter)."""
    body = hexprism(0, 0, 0, length, af)
    stud = b.Pos(0, 0, -stud_len / 2) * b.Cylinder(thread_d / 2, stud_len)
    hole = b.Pos(0, 0, length - bore_depth / 2) * b.Cylinder(thread_d / 2, bore_depth)
    return (body - hole) + stud


def washer_od(d_in, d_out, t):
    """Plain ring washer from z = 0 to t."""
    return b.extrude(b.Sketch() + b.Circle(d_out / 2) - b.Circle(d_in / 2), t)


def oring_installed(cx, cy, zc, r_in, r_out, width):
    """An O-ring as installed, squeezed to fill its groove: a ring r_in..r_out, `width` high, edges rounded."""
    return cp.break_edges(ring(cx, cy, zc - width / 2, zc + width / 2, r_in, r_out), min(0.5, (r_out - r_in) / 3))


def r_clip(x_pin, y_pin, z_pin, pin_d, hole_axis="x"):
    """R-clip (hairpin cotter) through a cross hole of a pin: a straight leg through the hole, a second leg
    outside the pin, joined by a bend. Wire 1.5 mm. hole_axis x: the hole runs along X at (y_pin, z_pin)."""
    r = 0.75
    off = pin_d / 2 + r + 1.2
    pts = [(x_pin - 8, y_pin, z_pin), (x_pin + 7, y_pin, z_pin), (x_pin + 7, y_pin + off, z_pin), (x_pin - 3, y_pin + off, z_pin)]
    return cp.rope(pts, 2 * r)


def pcb(w, h, t, holes=(), r_corner=2.0):
    """Printed circuit board w (X) x h (Z) x t, centred on X = 0 and Z = 0, occupying Y from -t to 0.
    holes [(x, z, d)] measured from the centre."""
    holes_xy = [(x, z, d) for x, z, d in holes]      # sheet() y is the board's Z after the turn
    return b.Rot(90, 0, 0) * cp.sheet(w, h, t, holes=holes_xy, r_corner=r_corner, edge=0.15)


def smd(x, y, z, sx, sy, sz):
    """A surface-mount component body."""
    return cp.break_edges(box(x, y, z, sx, sy, sz), min(0.15, min(sx, sy, sz) / 4))
