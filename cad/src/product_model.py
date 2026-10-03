"""LeakListen product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders, updated 2026-10-02 to the constructable design
(LKL-DDR-003): the IP68 logger, a PVC tube closed by two flanged turned acetal plugs with O-rings
and three radial M4 screws each; owner and lithium warning label and teal name band; on the top
plug an M6 eye bolt, an IP67 SMA bulkhead and a 3 mm clear status light pipe rod (lit); under the
bottom plug an M12 panel socket. Inside: the printed chassis hung on two standoffs from the top
plug, carrying the main board on four short standoffs, the hybrid layer capacitor, the C-size cell
and the desiccant pack. The telescopic aluminium neck bar with its levelling feet, pin and
antenna bracket, the wire rope lanyard with its snap hook and the flat LoRa antenna on the bar.
The sensor cable with its knurled M12 plug and the bead-blasted aluminium puck on its 42 mm pot
magnet, with the piezo disc, seismic mass, round preamplifier board on its step and the potting.
Context is compact: the cover frame edge with a slice of roof slab and street, a patch of chamber
neck wall behind each bar foot, and the top of the gate valve bonnet with its spindle and cap. The
chamber cover is left off so the antenna shows; the main itself (about 520 mm further down) is not
drawn. APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, position and interface comes from PARAMS, derived() and build_components()
in model.py (plain parts are the model.py shapes themselves); axes as model.py (street surface
Z = 0, chamber opening centred on X = Y = 0, front is -Y). See docs/REVIEW.md, sessions 2026-09-26
and 2026-10-02.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, build_components, derived

TITLE = "LeakListen: acoustic leak logger for water valve chambers"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); logger hanging from "
             "the neck bar below the cover frame, sensor puck on the valve spindle cap at right, cover lifted off"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): logger tube and end "
             "plugs, chassis, main board, C cell and desiccant, antenna, neck bar and lanyard, sensor cable, sensor puck, "
             "piezo and mass, preamplifier and pot magnet"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 18, "az": -35,
     "note": "Detail from the front right, slightly above (about 18 deg elevation): logger, antenna and "
             "neck bar at left, sensor puck on its magnet at right, without the chamber; status light lit"},
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
    MC = build_components(P)                       # model.py components, used as they are where they are plain
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    def mc(key):
        return MC[key].shape

    # ------------------------------------------------------------ logger (BOM 6, 7, 8, 11, 12, 13)
    lx, top, bot = P["logger_x"], P["logger_top_z"], D["logger_bot_z"]
    ro, ri = P["tube_od"] / 2, D["tube_id"] / 2
    pf, pt = P["plug_flange"], P["plug_t"]
    t0, t1 = bot + pf, top - pf                     # tube ends, flanges outside them (model.py)
    EL = (-40, -40, 0)                              # logger body explode: slightly left, toward camera
    ETP = (EL[0], EL[1], 95)                        # top plug and its fittings up
    EBP = (EL[0], EL[1], -95)                       # bottom plug down

    shell = _zcyl(lx, 0, (t0 + t1) / 2, ro, t1 - t0)
    shell -= _zcyl(lx, 0, (t0 + t1) / 2, ri, t1 - t0 + 2)
    for z_, scr in ((t1 - P["screw_z"], True), (t0 + P["screw_z"], True)):
        for a in P["screw_ang"]:
            shell -= Pos(lx, 0, z_) * Rot(0, 0, a) * Pos(ro - 1.5, 0, 0) * Rot(0, 90, 0) * Cylinder(2.0, 5.0)
    add("Logger tube (PVC)", shell, C_TUBE, "plastic", 6, "shell", EL)

    def plug(end):
        """Flanged turned plug: 63 mm flange 4 mm thick and a 57 mm spigot 18 mm long, two O-ring grooves."""
        if end > 0:
            f0, f1, s0, s1 = t1, top, t1 - pt, t1
        else:
            f0, f1, s0, s1 = bot, t0, t0, t0 + pt
        fl = _zcyl(lx, 0, (f0 + f1) / 2, ro, f1 - f0)
        fl = _fillet_try(fl, _top(fl) if end > 0 else _bottom(fl), [2.5, 2.0, 1.0])
        sp = _zcyl(lx, 0, (s0 + s1) / 2, ri, s1 - s0)
        for dz, cs in zip(P["oring_z"], P["oring_cs"]):
            zc_ = (t1 - dz) if end > 0 else (t0 + dz)
            sp -= _zcyl(lx, 0, zc_, ri + 1, cs) - _zcyl(lx, 0, zc_, ri - 1.8, cs + 2)
        pl = fl + sp
        z_ = (t1 - P["screw_z"]) if end > 0 else (t0 + P["screw_z"])
        for a in P["screw_ang"]:
            pl -= Pos(lx, 0, z_) * Rot(0, 0, a) * Pos(ri - 1.0, 0, 0) * Rot(0, 90, 0) * Cylinder(1.7, 8.0)
        return pl

    tp = plug(+1)
    tp -= _zcyl(lx, 0, (top + t1 - pt) / 2, 3.0, top - t1 + pt + 2)                     # eye bolt hole
    tp -= _zcyl(lx, 14.0, (top + t1 - pt) / 2, 3.2, top - t1 + pt + 2)                  # SMA hole
    lpx, lpy = P["lpipe_xy"]
    tp -= _zcyl(lx + lpx, lpy, (top + t1 - pt) / 2, P["lpipe_d"] / 2, top - t1 + pt + 2)    # light pipe hole
    add("Logger top plug (acetal)", tp, C_PLUG, "plastic", 6, "shell", ETP)
    add("Logger bottom plug (acetal)", plug(-1) - _zcyl(lx, 0, (bot + t0 + pt) / 2, 8.0, t0 + pt - bot + 2), C_PLUG, "plastic", 6, "shell", EBP)
    add("Plug O-rings, top", mc("top_orings"), C_BLACK, "rubber", 6, "internal", ETP)
    add("Plug O-rings, bottom", mc("bot_orings"), C_BLACK, "rubber", 6, "internal", EBP)
    add("Radial M4 screws, top", mc("screws_top"), C_STEEL, "metal", 6, "shell", ETP)
    add("Radial M4 screws, bottom", mc("screws_bot"), C_STEEL, "metal", 6, "shell", EBP)

    # top plug fittings (LKL-DDR-003 P3): M6 eye bolt, IP67 SMA bulkhead, status light pipe rod
    add("M6 eye bolt (stainless)", mc("eyebolt"), C_SS, "metal", 13, "shell", ETP)
    add("SMA bulkhead (IP67)", mc("sma"), C_BRASS, "metal", 13, "shell", ETP)
    add("Status light pipe rod (lit)", mc("lpipe"), C_LED, "emissive", 7, "shell", ETP)

    # M12 IP68 panel socket under the bottom plug (model.py: 15 mm below the flange)
    sk = _hex_z(lx, 0, bot - 2.5, 19.0, 5.0) + _zcyl(lx, 0, bot - 10.0, 8.0, 10.0)
    for k in range(5):
        sk -= _zcyl(lx, 0, bot - 6.5 - 1.8 * k, 8.5, 0.6) - _zcyl(lx, 0, bot - 6.5 - 1.8 * k, 7.5, 1.0)
    add("M12 panel socket", sk, C_SS, "metal", 6, "shell", EBP)

    # labels: teal name band and white owner and lithium warning label, facing front right
    face = -45.0
    zin_top, zin_bot = t1, t0
    band = _ring_on_cyl(lx, 0, t1 - 14, ro, 8.0, 150, face)
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

    # internals (P1, P6 of LKL-DDR-003): printed chassis on two standoffs from the top plug, main board on
    # four short standoffs, capacitor, desiccant and cell in clips, all as model.py
    ECH = (-100, -100, 40)
    add("Internal chassis (printed)", mc("chassis"), "#0F766E", "plastic", 12, "internal", ECH)
    add("Chassis standoffs (2)", mc("standoffs"), C_BRASS, "metal", 12, "internal", (ECH[0], ECH[1], 70))
    bb = mc("board").bounding_box()
    zb_top, zb_bot = bb.max.Z, bb.min.Z
    y_pcb = bb.max.Y                                       # board plane against its standoffs
    pcb = _box(lx, y_pcb - 0.8, (zb_top + zb_bot) / 2, P["board"][0], 1.6, zb_top - zb_bot)
    add("Main board PCB", pcb, C_PCB, "plastic", 7, "internal", ECH)
    y_c = y_pcb - 1.6
    mod = _box(lx, y_c - 1.5, zb_top - 30, 26, 3.0, 30)
    add("LoRaWAN module shield can", mod, C_SS, "metal", 7, "internal", ECH)
    chips = (_box(lx - 6, y_c - 0.8, zb_top - 70, 12, 1.6, 12) + _box(lx + 10, y_c - 0.6, zb_top - 80, 6, 1.2, 8)
             + _box(lx, y_c - 1.0, zb_top - 95, 24, 2.0, 7) + _box(lx - 12, y_c - 0.7, zb_top - 50, 5, 1.4, 3))
    add("Main board components", chips, C_CHIP, "plastic", 7, "internal", ECH)
    add("Board standoffs (4)", mc("board_standoffs"), C_ALU, "plastic", 12, "internal", ECH)
    hlc = mc("hlc")
    hlc = _fillet_try(hlc, _bottom(hlc), [1.0, 0.5])
    add("Hybrid layer capacitor", hlc, C_CELL, "plastic", 7, "internal", (-100, -60, 70))
    cell = mc("cell")
    cb = cell.bounding_box()
    ccx, ccy = (cb.min.X + cb.max.X) / 2, (cb.min.Y + cb.max.Y) / 2
    cd = P["cell"][0]
    cell = _fillet_try(cell, cell.edges(), [1.2, 0.6])
    EC = (-100, -40, -45)
    add("Primary cell, Li-SOCl2 C", cell, C_CELL, "plastic", 8, "internal", EC)
    cband = _zcyl(ccx, ccy, cb.min.Z + 28, cd / 2 + 0.2, 14) - _zcyl(ccx, ccy, cb.min.Z + 28, cd / 2 - 1, 16)
    add("Cell label band", cband, C_LABEL, "paper", 8, "internal", EC)
    des = _fillet_try(mc("desiccant"), mc("desiccant").edges(), [3.0, 2.0, 1.0])
    add("Desiccant pack", des, C_DESIC, "fabric", 11, "internal", (-100, 40, -45))

    # ------------------------------------------------------------ neck bar, lanyard and antenna (BOM 9, 10)
    EH = (-60, 0, 150)
    add("Neck bar outer tube", mc("bar_outer"), C_ALU, "metal", 9, "shell", EH)
    add("Neck bar inner tube", mc("bar_inner"), C_ALU, "metal", 9, "shell", (EH[0], EH[1] + 60, EH[2]))
    add("Tube end inserts with M10 nuts", mc("inserts"), C_STEEL, "metal", 9, "shell", EH)
    add("Levelling feet with rubber pads", mc("feet"), "#2E3338", "rubber", 9, "shell", EH)
    add("Locking pin with R-clip", mc("lockpin"), C_SS, "metal", 9, "shell", (EH[0], EH[1], EH[2] + 40))
    add("Antenna bracket (aluminium flat bar)", mc("bracket"), C_ALU, "metal", 9, "shell", (EH[0], EH[1], EH[2] + 40))
    add("M5 bolt and nyloc nut", mc("bracket_bolt"), C_STEEL, "metal", 9, "shell", (EH[0], EH[1], EH[2] + 40))
    add("Wire rope lanyard with snap hook", mc("lanyard"), C_SS, "metal", 9, "shell", (0, 0, 120))

    za = D["ant_z"]
    ax, ay = lx + P["ant_off"], P["ant_y"]
    EA = (40, -30, EH[2] + 90)
    ant = _zcyl(ax, ay, za, P["ant_d"] / 2, P["ant_t"])
    ant = _fillet_try(ant, _bottom(ant), [4.0, 3.0, 2.0])
    ant = _fillet_try(ant, _top(ant), [1.5, 1.0])
    add("Flat LoRa antenna radome", ant, C_PLUG, "plastic", 10, "shell", EA)
    dot = _zcyl(ax + 14, ay - 12, za + P["ant_t"] / 2 + 0.1, 5.0, 0.3)
    add("Antenna mark", dot, C_ACCENT, "painted", 10, "shell", EA)
    add("Antenna stud nut", mc("ant_nut"), C_STEEL, "metal", 10, "shell", (EA[0], EA[1], EA[2] - 40))
    add("Antenna lead with SMA plug", mc("ant_lead"), C_BLACK, "rubber", 10, "shell", ETP)

    # ------------------------------------------------------------ sensor cable (BOM 5)
    zt = D["puck_top_z"]
    zs = bot - 15.0 - P["m12_len"]
    ECB = (40, -20, -40)
    zp1 = D["puck_bot_z"] + P["puck_base"] + P["puck_step"] + P["preamp_t"]
    pts = [(0, 0, zp1), (0, 0, zt + 31), (-70, 0, zt + 41), (-130, 0, zt - 44), (-165, 0, zt - 104),
           (lx, 0, zs - 35), (lx, 0, zs)]
    cable = _pipe(_smooth(pts, 2), P["cable_d"] / 2)
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
    z_base = zpb + P["puck_base"]
    z_step = z_base + P["puck_step"]
    r_up = pr - P["puck_wall"]
    body = _zcyl(0, 0, zpb + P["puck_h"] / 2, pr, P["puck_h"])
    body = _fillet_try(body, _top(body), [2.5, 2.0, 1.0])
    body = _fillet_try(body, _bottom(body), [0.8, 0.5])
    body -= _zcyl(0, 0, (z_base + z_step) / 2, P["puck_bore_low"] / 2, z_step - z_base)    # lower bore
    body -= _zcyl(0, 0, (z_step + zt + 1) / 2, r_up, zt + 1 - z_step)                      # upper bore, open top
    for k in range(16):                                           # grip flutes on the lower half
        a = 2 * math.pi * k / 16
        body -= _zcyl(math.cos(a) * (pr + 0.6), math.sin(a) * (pr + 0.6), zpb + 14, 1.4, 18)
    add("Sensor puck body (aluminium)", body, C_ALU, "metal", 1, "shell", EPK)
    ring = _zcyl(0, 0, zpb + 33, pr + 0.3, 4.0) - _zcyl(0, 0, zpb + 33, pr - 0.5, 6.0)
    add("Puck accent ring", ring, C_ACCENT, "painted", 1, "shell", EPK)
    pot = mc("potting")
    add("Potting above the board", pot, "#262A30", "rubber", 11, "shell", (170, -40, 190))

    E3 = (170, -40, 105)
    piezo = mc("piezo")
    add("Piezo disc (brass backed)", piezo, C_BRASS, "metal", 3, "internal", (170, -40, 75))
    cer = _zcyl(0, 0, z_base + P["piezo_t"] + 0.2, 10.0, 0.4)
    add("Piezo ceramic", cer, "#E7E2D6", "plastic", 3, "internal", (170, -40, 75))
    mass = mc("mass")
    mass = _fillet_try(mass, _top(mass), [1.0, 0.5])
    add("Seismic mass (brass)", mass, C_BRASS, "metal", 3, "internal", E3)
    pa = mc("preamp")
    add("Charge preamplifier board (round, on the step)", pa, C_PCB, "plastic", 4, "internal", (170, -40, 150))
    pac = _box(-4, 4, zp1 + 0.6, 7, 5, 1.2) + _box(5, -6, zp1 + 0.5, 4, 3, 1.0)
    add("Preamplifier components", pac, C_CHIP, "plastic", 4, "internal", (170, -40, 150))

    mag = _zcyl(0, 0, zc + P["magnet_h"] / 2, P["magnet_d"] / 2, P["magnet_h"])
    mag = _fillet_try(mag, _top(mag), [1.5, 1.0])
    mag = _fillet_try(mag, _bottom(mag), [0.8, 0.5])
    mag -= _zcyl(0, 0, zc + 0.4, P["magnet_d"] / 2 - 3.0, 0.8) - _zcyl(0, 0, zc + 0.4, P["magnet_d"] / 2 - 4.0, 2.0)
    add("Pot magnet, 42 mm", mag, C_STEEL, "metal", 2, "shell", (170, -40, -50))

    # ------------------------------------------------------------ context (existing assets, not in the BOM)
    s = P["cap_sq"]
    x_edge = -P["frame_open"] / 2
    half = P["frame_open"] / 2
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
    # chamber neck wall behind each foot of the neck bar (section patches, so the feet are not in mid air)
    walls = _union([_box(lx, sy * (half + 10), P["bar_z"], 140, 20, 150) for sy in (-1, 1)])
    add("Chamber neck wall at the bar feet (section)", walls, C_CONC, "clay", None, "context", (0, 0, 0))
    return out


def _edges_x(s):
    return s.edges().filter_by(Axis.X)


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:40s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
