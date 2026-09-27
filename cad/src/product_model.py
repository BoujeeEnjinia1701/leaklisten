"""LeakListen product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the IP68 logger tube with filleted end plugs and
their parting grooves, owner and lithium warning label, teal name band, antenna gland, M12 panel
socket and a lit status light pipe; the main board, C-size cell and desiccant inside; the flat
LoRa antenna radome and its lead; the stainless hanger strap and lanyard; the sensor cable with
its knurled M12 plug; and the bead-blasted aluminium sensor puck with grip flutes, cable gland
and teal ring on its 42 mm pot magnet, with the piezo disc, seismic mass and preamplifier inside.
Context is compact: the cover frame edge with a slice of roof slab and street, and the top of
the gate valve bonnet with its spindle and square spindle cap. The chamber cover is left off so
the antenna shows; the main itself (about 520 mm further down) is not drawn.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, position and interface comes from PARAMS, derived() and site_context()
in model.py; axes as model.py (street surface Z = 0, chamber opening centred on X = Y = 0,
front is -Y). See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, derived

TITLE = "LeakListen: acoustic leak logger for water valve chambers"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); logger hanging from "
             "the cover frame at left, sensor puck on the valve spindle cap at right, cover lifted off"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): logger tube and end "
             "plugs, main board, C cell and desiccant, antenna, hanger strap, sensor cable, sensor puck, "
             "piezo and mass, preamplifier and pot magnet"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 18, "az": -35,
     "note": "Detail from the front right, slightly above (about 18 deg elevation): logger, antenna and "
             "hanger at left, sensor puck on its magnet at right, without the chamber; status light lit"},
]

# Colours (restrained product palette; kit accent)
C_TUBE = "#E6E8EA"
C_PLUG = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_LABEL = "#F4F4F2"
C_INK = "#2B2F36"
C_ALU = "#C3C8CE"
C_STEEL = "#9AA1A9"
C_SS = "#B8BEC6"
C_BRASS = "#C9A227"
C_PCB = "#166534"
C_CHIP = "#111827"
C_CELL = "#1E3A5F"
C_LED = "#22C55E"
C_DESIC = "#EDEDEA"
C_IRON = "#5E646B"
C_VALVE = "#3F5A73"
C_CONC = "#C9C5BD"
C_ASPH = "#4A4B50"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _smooth(points, n=3):
    """Chaikin corner cutting, endpoints kept: soft cable bends through the same route."""
    pts = [tuple(q) for q in points]
    for _ in range(n):
        new = [pts[0]]
        for a, c in zip(pts, pts[1:]):
            new.append(tuple(0.75 * a[i] + 0.25 * c[i] for i in range(3)))
            new.append(tuple(0.25 * a[i] + 0.75 * c[i] for i in range(3)))
        new.append(pts[-1])
        pts = new
    return pts


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _ring_on_cyl(x, y, z, r, h, arc_deg, face_deg, t=0.4):
    """Thin raised band on a vertical cylinder of radius r: arc `arc_deg` wide, centred on the
    direction `face_deg` (degrees from +X toward +Y), height h, thickness t."""
    band = _zcyl(x, y, z, r + t, h) - _zcyl(x, y, z, r - 0.5, h + 2)
    w = 2 * (r + 2) * math.sin(math.radians(min(arc_deg, 179) / 2))
    a = math.radians(face_deg)
    d = r + 2
    cut = Pos(x + math.cos(a) * d / 2, y + math.sin(a) * d / 2, z) * Rot(0, 0, face_deg) * Box(d + 2, w, h + 4)
    return band & cut


def product_parts(P=PARAMS):
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ logger (BOM 6, 7, 8, 11)
    lx, top, bot = P["logger_x"], P["logger_top_z"], D["logger_bot_z"]
    ro, ri = P["tube_od"] / 2, D["tube_id"] / 2
    pt = P["plug_t"]
    zin_top, zin_bot = top - pt, bot + pt
    EL = (-40, -40, 0)                              # logger body explode: slightly left, toward camera
    ETP = (EL[0], EL[1], 95)                        # top plug up
    EBP = (EL[0], EL[1], -95)                       # bottom plug down

    shell = _zcyl(lx, 0, (zin_top + zin_bot) / 2, ro, zin_top - zin_bot)
    shell -= _zcyl(lx, 0, (zin_top + zin_bot) / 2, ri, zin_top - zin_bot + 2)
    add("Logger tube (PVC)", shell, C_TUBE, "plastic", 6, "shell", EL)

    def plug(z0, z1, up):
        p = _zcyl(lx, 0, (z0 + z1) / 2, ro, z1 - z0)
        p = _fillet_try(p, _top(p) if up else _bottom(p), [4.0, 3.0, 2.0])
        # parting groove where the plug shoulder meets the tube, and an O-ring line
        zg = z0 + 1.0 if up else z1 - 1.0
        p -= _zcyl(lx, 0, zg, ro + 1, 1.0) - _zcyl(lx, 0, zg, ro - 0.6, 2.0)
        zo = z0 + 7.0 if up else z1 - 7.0
        p -= _zcyl(lx, 0, zo, ro + 1, 0.8) - _zcyl(lx, 0, zo, ro - 0.4, 2.0)
        return p

    add("Logger top plug", plug(zin_top, top, True), C_PLUG, "plastic", 6, "shell", ETP)
    add("Logger bottom plug", plug(bot, zin_bot, False), C_PLUG, "plastic", 6, "shell", EBP)

    # antenna and lanyard gland on the top plug (model.py: r 6, 12 mm tall)
    gl = _hex_z(lx, 0, top + 2.5, 14.0, 5.0) + _zcyl(lx, 0, top + 7.5, 6.0, 5.0)
    gl += Pos(lx, 0, top + 10.0) * Sphere(5.5) & _box(lx, 0, top + 12.0, 14, 14, 4.0)
    add("Antenna gland", gl, C_BLACK, "plastic", 6, "shell", ETP)

    # status light pipe on the top plug (appearance addition, see REVIEW.md)
    led = _zcyl(lx + 18, -8, top + 0.8, 3.0, 1.6) + Pos(lx + 18, -8, top + 1.6) * Sphere(2.6)
    led &= _zcyl(lx + 18, -8, top + 2.0, 4.0, 4.0)
    add("Status light pipe (lit)", led, C_LED, "emissive", 7, "shell", ETP)

    # M12 IP68 panel socket under the bottom plug (model.py: r 8, 15 mm)
    sk = _hex_z(lx, 0, bot - 2.5, 19.0, 5.0) + _zcyl(lx, 0, bot - 10.0, 8.0, 10.0)
    for k in range(5):
        sk -= _zcyl(lx, 0, bot - 6.5 - 1.8 * k, 8.5, 0.6) - _zcyl(lx, 0, bot - 6.5 - 1.8 * k, 7.5, 1.0)
    add("M12 panel socket", sk, C_SS, "metal", 6, "shell", EBP)

    # labels: teal name band and white owner and lithium warning label, facing front right
    face = -45.0
    band = _ring_on_cyl(lx, 0, top - pt - 14, ro, 8.0, 150, face)
    add("Logger name band", band, C_ACCENT, "painted", 6, "shell", EL)
    lab = _ring_on_cyl(lx, 0, (zin_top + zin_bot) / 2 + 10, ro, 70.0, 110, face, t=0.3)
    add("Owner and lithium warning label", lab, C_LABEL, "paper", 11, "shell", EL)
    a = math.radians(face)
    ux, uy = -math.sin(a), math.cos(a)                     # tangent direction on the label face
    nx_, ny_ = math.cos(a), math.sin(a)
    rr = ro + 0.45
    ink = []
    zc = (zin_top + zin_bot) / 2 + 10
    for dz, w, h, off in [(24, 30, 6, -4), (15, 36, 2.2, 0), (10, 30, 2.2, -3), (5, 34, 2.2, -1),
                          (-8, 14, 12, -13), (-5, 18, 2.2, 8), (-10, 18, 2.2, 8), (-24, 40, 2.0, 0)]:
        cxp = lx + nx_ * rr + ux * off
        cyp = ny_ * rr + uy * off
        ink.append(Pos(cxp, cyp, zc + dz) * Rot(0, 0, face + 90) * Box(w, 0.3, h))
    add("Label print", _union(ink), C_INK, "paper", 11, "shell", EL)

    # internals, as model.py
    bx, by, bz = P["board"]
    hd, hh = P["hlc"]
    EB = (-40 - 70, -40 - 60, 40)
    zb = zin_top - 4 - bz / 2
    pcb = _box(lx, -12.0 + by / 2 - 0.8, zb, bx, 1.6, bz)       # components face the front (-Y)
    add("Main board PCB", pcb, C_PCB, "plastic", 7, "internal", EB)
    y_c = -12.0 + by / 2 - 1.6
    mod = _box(lx, y_c - 1.5, zb + 30, 26, 3.0, 30)
    add("LoRaWAN module shield can", mod, C_SS, "metal", 7, "internal", EB)
    chips = (_box(lx - 6, y_c - 0.8, zb - 10, 12, 1.6, 12) + _box(lx + 10, y_c - 0.6, zb - 12, 6, 1.2, 8)
             + _box(lx, y_c - 1.0, zb - 38, 24, 2.0, 7) + _box(lx - 12, y_c - 0.7, zb + 5, 5, 1.4, 3))
    add("Main board components", chips, C_CHIP, "plastic", 7, "internal", EB)
    hlc = _zcyl(lx - 10.0, 8.0, zin_top - 4 - hh / 2, hd / 2, hh)
    hlc = _fillet_try(hlc, _bottom(hlc), [1.0, 0.5])
    add("Hybrid layer capacitor", hlc, C_CELL, "plastic", 7, "internal", EB)

    cd, ch = P["cell"]
    ccx, ccy, ccz = lx + 2.0, 11.0, zin_bot + 4 + ch / 2
    EC = (-40 - 60, -40 - 60, -45)
    cell = _zcyl(ccx, ccy, ccz, cd / 2, ch - 1.0)
    cell = _fillet_try(cell, cell.edges(), [1.2, 0.6])
    add("Primary cell, Li-SOCl2 C", cell, C_CELL, "plastic", 8, "internal", EC)
    caps = _zcyl(ccx, ccy, ccz + ch / 2 - 0.4, cd / 2 - 1.5, 0.8) + _zcyl(ccx, ccy, ccz - ch / 2 + 0.4, cd / 2 - 1.5, 0.8)
    caps += _zcyl(ccx, ccy, ccz + ch / 2 + 0.6, 4.0, 1.2)
    add("Cell terminals", caps, C_SS, "metal", 8, "internal", EC)
    cband = _zcyl(ccx, ccy, ccz + 6, cd / 2 + 0.2, 14) - _zcyl(ccx, ccy, ccz + 6, cd / 2 - 1, 16)
    add("Cell label band", cband, C_LABEL, "paper", 8, "internal", EC)

    dx_, dy_, dz_ = P["desiccant"]
    des = _box(lx - 8.0, -12.0, zin_bot + 4 + dz_ / 2, dx_, dy_, dz_)
    des = _fillet_try(des, des.edges(), [3.0, 2.0, 1.0])
    add("Desiccant pack", des, C_DESIC, "fabric", 11, "internal", (-40 - 150, -40 - 60, -45))

    # ------------------------------------------------------------ hanger and antenna (BOM 9, 10)
    x_edge = -P["frame_open"] / 2
    zf = -P["frame_depth"]
    w, t = P["strap_w"], P["strap_t"]
    EH = (-60, 0, 150)
    zp = zf + 10 - t / 2
    plate = _box(x_edge + P["strap_run"] / 2, 0, zp, P["strap_run"], w, t)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Z), [6.0, 4.0])
    hook_c = zf + 10 + (P["hook_h"] - 10) / 2 - 5
    hook = _box(x_edge - t / 2, 0, hook_c, t, w, P["hook_h"])
    hook = _fillet_try(hook, _top(hook).filter_by(Axis.Y), [0.7, 0.5])
    bend = Pos(x_edge - 0.01, 0, zp) * Rot(90, 0, 0) * (Cylinder(t, w) - Cylinder(0.01, w + 1))
    bend &= _box(x_edge - t / 2, 0, zp, t + 0.02, w + 1, 2 * t)
    strap = plate + hook
    try:
        s2 = strap + bend
        if s2.is_valid:
            strap = s2
    except Exception:
        pass
    strap -= _zcyl(x_edge + P["strap_run"] - 10, 0, zp, 2.2, 4.0)     # lanyard eye
    add("Hanger strap and hook (stainless)", strap, C_SS, "metal", 9, "shell", EH)
    rivets = _union(_zcyl(x_edge + 15 + 22 * k, sgn * 8, zp - t / 2 - 0.5, 2.2, 1.0)
                    for k in range(2) for sgn in (-1, 1))
    add("Strap rivets", rivets, C_STEEL, "metal", 9, "shell", EH)
    lan = _pipe([(x_edge + P["strap_run"] - 10, 0, zp - t / 2), (x_edge + P["strap_run"] - 10, 0, zp - 8),
                 (lx, 0, top + 12.0)], P["lanyard_d"] / 2)
    add("Stainless lanyard", lan, C_SS, "metal", 9, "shell", ETP)

    za = D["ant_z"]
    ax = x_edge + P["strap_run"] + P["ant_d"] / 2 - 10
    EA = (40, -30, 150)
    ant = _zcyl(ax, 0, za, P["ant_d"] / 2, P["ant_t"])
    ant = _fillet_try(ant, _bottom(ant), [4.0, 3.0, 2.0])
    ant = _fillet_try(ant, _top(ant), [1.5, 1.0])
    ant -= _zcyl(ax, 0, za - P["ant_t"] / 2, P["ant_d"] / 2 - 9, 1.2) - _zcyl(ax, 0, za - P["ant_t"] / 2, P["ant_d"] / 2 - 10, 2.0)
    add("Flat LoRa antenna radome", ant, C_PLUG, "plastic", 10, "shell", EA)
    dot = _zcyl(ax + 14, -12, za - P["ant_t"] / 2 - 0.2, 5.0, 0.4)
    add("Antenna mark", dot, C_ACCENT, "painted", 10, "shell", EA)
    lead = _pipe([(ax - 20, 0, za - P["ant_t"] / 2 + 1), (ax - 20, 0, za - P["ant_t"] / 2 - 8), (lx + 8, 0, top + 12.0)], 2.5)
    add("Antenna lead", lead, C_BLACK, "rubber", 10, "shell", ETP)

    # ------------------------------------------------------------ sensor cable (BOM 5)
    zt = D["puck_top_z"]
    zs = bot - 15.0 - P["m12_len"]
    ECB = (40, -20, -40)
    route = _smooth([(0, 0, zt + 12), (0, 0, zt + 40), (-60, 0, zt + 70), (lx + 30, 0, zs - 40),
                     (lx, 0, zs - 10), (lx, 0, zs + 1)])
    cable = _pipe([(0, 0, zt - 1)] + route, P["cable_d"] / 2)
    add("Sensor cable (PUR)", cable, C_BLACK, "rubber", 5, "shell", ECB)
    mb = _zcyl(lx, 0, zs + 14, P["m12_d"] / 2 - 2, 28)
    mb = _fillet_try(mb, _bottom(mb), [5.0, 4.0, 2.0])
    add("M12 plug overmold", mb, C_BLACK, "rubber", 5, "shell", ECB)
    nut = _zcyl(lx, 0, zs + P["m12_len"] - 8.5, P["m12_d"] / 2, 17)
    for k in range(18):
        a = 2 * math.pi * k / 18
        nut -= _zcyl(lx + math.cos(a) * P["m12_d"] / 2, math.sin(a) * P["m12_d"] / 2, zs + P["m12_len"] - 9.5, 1.0, 13)
    add("M12 coupling nut (knurled)", nut, C_SS, "metal", 5, "shell", ECB)

    # ------------------------------------------------------------ sensor puck (BOM 1 to 4)
    zc = P["cap_top_z"]
    pr = P["puck_d"] / 2
    zpb = D["puck_bot_z"]
    EPK = (170, -40, 0)
    body = _zcyl(0, 0, zpb + P["puck_h"] / 2, pr, P["puck_h"])
    body = _fillet_try(body, _top(body), [2.5, 2.0, 1.0])
    body = _fillet_try(body, _bottom(body), [0.8, 0.5])
    cav_h = P["puck_h"] - P["puck_base"] - 3.0
    body -= _zcyl(0, 0, zpb + P["puck_base"] + cav_h / 2, pr - P["puck_wall"], cav_h)
    for k in range(16):                                           # grip flutes on the lower half
        a = 2 * math.pi * k / 16
        body -= _zcyl(math.cos(a) * (pr + 0.6), math.sin(a) * (pr + 0.6), zpb + 14, 1.4, 18)
    body -= _zcyl(0, 0, zpb + 27, pr + 1, 0.8) - _zcyl(0, 0, zpb + 27, pr - 0.5, 2)   # lid seam line
    add("Sensor puck body (aluminium)", body, C_ALU, "metal", 1, "shell", EPK)
    ring = _zcyl(0, 0, zpb + 33, pr + 0.3, 4.0) - _zcyl(0, 0, zpb + 33, pr - 0.5, 6.0)
    add("Puck accent ring", ring, C_ACCENT, "painted", 1, "shell", EPK)
    pg = _hex_z(0, 0, zt + 2.5, 13.0, 5.0) + _zcyl(0, 0, zt + 7.5, 5.5, 5.0)
    pg = _fillet_try(pg, _top(pg), [1.5, 1.0])
    add("Puck cable gland", pg, C_SS, "metal", 1, "shell", EPK)

    zp0 = zpb + P["puck_base"]
    E3 = (170, -40, 105)
    piezo = _zcyl(0, 0, zp0 + P["piezo_t"] / 2, P["piezo_d"] / 2, P["piezo_t"])
    add("Piezo disc (brass backed)", piezo, C_BRASS, "metal", 3, "internal", (170, -40, 75))
    cer = _zcyl(0, 0, zp0 + P["piezo_t"] + 0.2, 10.0, 0.4)
    add("Piezo ceramic", cer, "#E7E2D6", "plastic", 3, "internal", (170, -40, 75))
    mass = _zcyl(0, 0, zp0 + P["piezo_t"] + P["mass_h"] / 2, P["mass_d"] / 2, P["mass_h"])
    mass = _fillet_try(mass, _top(mass), [1.0, 0.5])
    add("Seismic mass (brass)", mass, C_BRASS, "metal", 3, "internal", E3)
    px, py, pz = P["preamp"]
    zpa = zp0 + P["piezo_t"] + P["mass_h"] + 6 + pz / 2
    pa = _box(0, 0, zpa, px, py, pz)
    add("Charge preamplifier board", pa, C_PCB, "plastic", 4, "internal", (170, -40, 150))
    pac = _box(-3, 2, zpa + pz / 2 + 0.6, 7, 5, 1.2) + _box(6, -5, zpa + pz / 2 + 0.5, 4, 3, 1.0)
    add("Preamplifier components", pac, C_CHIP, "plastic", 4, "internal", (170, -40, 150))

    mag = _zcyl(0, 0, zc + P["magnet_h"] / 2, P["magnet_d"] / 2, P["magnet_h"])
    mag = _fillet_try(mag, _top(mag), [1.5, 1.0])
    mag = _fillet_try(mag, _bottom(mag), [0.8, 0.5])
    mag -= _zcyl(0, 0, zc + 0.4, P["magnet_d"] / 2 - 3.0, 0.8) - _zcyl(0, 0, zc + 0.4, P["magnet_d"] / 2 - 4.0, 2.0)
    add("Pot magnet, 42 mm", mag, C_STEEL, "metal", 2, "shell", (170, -40, -50))

    # ------------------------------------------------------------ context (existing assets, not in the BOM)
    s = P["cap_sq"]
    cap = _box(0, 0, zc - P["cap_h"] / 2, s, s, P["cap_h"])
    cap = _fillet_try(cap, cap.edges().filter_by(Axis.Z), [3.0, 2.0])
    cap = _fillet_try(cap, _top(cap), [1.5, 1.0])
    add("Valve spindle cap (existing)", cap, C_VALVE, "painted", None, "context", (0, 0, 0))
    z_bonnet = -570.0                                     # bonnet top, as cad/src/concept_media.py
    spindle = _zcyl(0, 0, (z_bonnet + zc - P["cap_h"]) / 2, 18.0, zc - P["cap_h"] - z_bonnet)
    add("Valve spindle (existing)", spindle, C_IRON, "metal", None, "context", (0, 0, 0))
    bon = _zcyl(0, 0, z_bonnet - 45, 75.0, 90.0)
    bon = _fillet_try(bon, _top(bon), [6.0, 4.0])
    bon += _hex_z(0, 0, z_bonnet + 6, 60.0, 12.0)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        bon += _zcyl(math.cos(a) * 52, math.sin(a) * 52, z_bonnet + 4, 7.5, 8.0)
    add("Gate valve bonnet top (existing)", bon, C_VALVE, "painted", None, "context", (0, 0, 0))

    fr = _box(x_edge - 30, 0, -P["frame_depth"] / 2, 60, 220, P["frame_depth"])
    fr -= _box(x_edge + 5, 0, -P["cover_t"] / 2 + 0.01, 70, 230, P["cover_t"])
    add("Cover frame edge (existing)", fr, C_IRON, "metal", None, "context", (0, 0, 0))
    slab = _box(x_edge - 30 - 55, 0, -130, 170, 220, 140)
    slab = _fillet_try(slab, _edges_x(slab), [1.5, 1.0])
    add("Chamber roof slab (section)", slab, C_CONC, "clay", None, "context", (0, 0, 0))
    road = _box(x_edge - 60 - 55, 0, -P["frame_depth"] / 2, 110, 220, P["frame_depth"])
    add("Street surface (section)", road, C_ASPH, "clay", None, "context", (0, 0, 0))
    return out


def _edges_x(s):
    return s.edges().filter_by(Axis.X)


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
