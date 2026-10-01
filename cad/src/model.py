"""LeakListen parametric model (build123d), TRL 3, constructable design (LKL-DDR-003).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    leaklisten-assembly.step / .stl   the whole set as installed in the example valve chamber
    logger.step / .stl                logger tube, end plugs, fittings, chassis and electronics
    sensor-puck.step / .stl           puck body, pot magnet, piezo disc and mass, preamplifier, potting
    neck-bar.step / .stl              neck bar hanger, antenna bracket, antenna and lanyard
and prints the constructability checks (python cad/src/model.py --check prints them only).

Axes: the street surface is Z = 0 and the chamber opening is centred on X = Y = 0, as in
cad/src/concept_media.py. The example site is a DN150 gate valve whose square spindle cap top
sits 480 mm below the street. The cover frame's clear opening is 600 mm square and the chamber
neck (the opening through the roof slab) continues it down to 230 mm below the street.

Revised 2026-10-01 under Amish's 2026-09-30 instruction to make the design physically buildable
(LKL-DDR-003, "Design for construction"). The concept hung the logger from a stainless strap
"hooked over the cover frame", but the hook had nothing to hook over: the cover sits on the
frame's seat, so a strap there would sit under the cover and rock it. The constructable design:
    a telescopic aluminium neck bar wedged across the chamber neck below the frame by two rubber
    levelling feet; the logger hangs from it on a wire rope lanyard and the flat antenna sits on
    a bracket on top of it, 20 mm under the cover;
    flanged, turned acetal end plugs with two O-rings each, held in the PVC tube by three radial
    screws outboard of the O-rings;
    an M6 eye bolt (lanyard) and an IP67 SMA bulkhead (antenna) on the top plug, in place of the
    one "antenna and lanyard gland";
    a printed internal chassis on two standoffs from the top plug, carrying the board, the cell
    and capacitor in snap clips and the desiccant in a pocket, so the electronics lift out with
    the top plug;
    a puck body with an 8 mm base tapped M6 for the magnet's stud, and a stepped bore whose step
    carries a round preamplifier board clear of the seismic mass, potted above the board only.
Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS feed
docs/04-calcs/sizing.py (LKL-CAL-001), drawing LKL-DWG-001 (cad/src/sheets.py), the concept
media (cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site interface (existing assets, grey; not in the BOM)
    "frame_open": 600.0,            # clear opening of the cover frame, square
    "frame_depth": 60.0,            # frame depth below the street; the neck starts below it
    "cover_t": 40.0,                # cover thickness; underside at -cover_t, on the frame seat
    "neck_bot": -230.0,             # bottom of the chamber neck (roof slab soffit)
    "cap_top_z": -480.0,            # top of the valve spindle cap (example site)
    "cap_sq": 50.0, "cap_h": 20.0,  # square spindle cap
    # 1 sensor puck body (aluminium): diameter, height, top bore wall, base, lower bore diameter,
    #   height of the step (above the base) that carries the preamplifier board
    "puck_d": 40.0, "puck_h": 42.0, "puck_wall": 4.0, "puck_base": 8.0, "puck_bore_low": 29.0,
    "puck_step": 25.0,
    # 2 pot magnet: 42 mm, about 600 N rated (LKL-DDR-002); M6 stud cut to 6 mm, into the base
    "magnet_d": 42.0, "magnet_h": 12.0, "magnet_rated_n": 600.0, "stud": (6.0, 6.0),
    # 3 piezo disc and seismic mass; 4 preamplifier, round board on the step
    "piezo_d": 27.0, "piezo_t": 0.5, "mass_d": 20.0, "mass_h": 20.0,
    "preamp_d": 31.0, "preamp_t": 1.6,
    "preamp": (22.0, 22.0, 1.6),    # concept board size, kept for cad/src/product_model.py only
    # 5 sensor cable: 4-core shielded PUR, M12 plug at the logger end
    "cable_d": 6.0, "cable_len": 2000.0, "m12_d": 20.0, "m12_len": 45.0,
    # 6 logger housing: PVC pipe (OD, wall); overall length flange to flange; end plug flange
    #   thickness and spigot length; O-ring grooves and radial screws, measured from the tube end
    "tube_od": 63.0, "tube_wall": 3.0, "logger_len": 240.0, "plug_flange": 4.0, "plug_t": 18.0,
    "oring_z": (10.0, 15.0), "oring_cs": (2.5, 1.8), "screw_z": 4.0, "screw_ang": (30.0, 150.0, 270.0),
    "logger_x": -200.0, "logger_top_z": -180.0,
    # 7 main board and hybrid layer capacitor; 8 C-size cell; 11 desiccant
    "board": (38.0, 8.0, 110.0), "hlc": (16.0, 30.0),
    "cell": (26.2, 50.0),
    "desiccant": (22.0, 10.0, 50.0),
    # 12 internal chassis (printed): spine width and thickness; standoff length to the top plug
    "spine": (48.0, 3.0), "chassis_standoff": 20.0,
    # 9 neck bar: outer and inner aluminium square tube (side, wall, length); centre height;
    #   rubber levelling foot pad (diameter, thickness); locking pin position along the bar
    "bar_out": (20.0, 1.5, 350.0), "bar_in": (16.0, 1.5, 350.0), "bar_z": -85.0,
    "pad": (40.0, 8.0), "bar_out_y0": -280.0, "bar_in_y0": -80.0, "pin_y": 40.0,
    # 10 flat LoRa antenna (diameter, thickness) on a bracket (width, thickness, length) on the bar,
    #   its centre offset from the bar axis and its position along the bar
    "ant_d": 70.0, "ant_t": 12.0, "ant_bracket": (40.0, 3.0, 100.0), "ant_off": 45.0, "ant_y": -150.0,
    "lanyard_d": 3.0,
    # concept hanger, kept only so cad/src/product_model.py (appearance model, now stale) still runs
    "strap_w": 30.0, "strap_t": 1.5, "strap_run": 80.0, "hook_h": 56.0, "ant_gap": 8.0,
}

BOM = {  # BOM line: name
    1: "Sensor puck body", 2: "Pot magnet", 3: "Piezo disc and seismic mass", 4: "Charge preamplifier",
    5: "Sensor cable", 6: "Logger housing", 7: "Main board", 8: "Primary cell", 9: "Neck bar hanger",
    10: "Flat LoRa antenna", 11: "Desiccant and consumables", 12: "Internal chassis", 13: "Top plug fittings",
}


@dataclass
class Comp:
    """One component: a single made or bought piece (or a matched set of fixings)."""
    name: str
    shape: object
    bom: int | None
    kind: str           # "made", "bought" or "fixing"
    density: float = 0  # g/cm3 for the mass estimate; 0 = not counted from volume


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    ri = p["tube_od"] / 2 - p["tube_wall"]
    top = p["logger_top_z"]
    L = p["logger_len"]
    pf, pt = p["plug_flange"], p["plug_t"]
    zb = p["cap_top_z"] + p["magnet_h"]
    d = {
        "tube_id": 2 * ri,
        "tube_len": L - 2 * pf,
        "free_len": L - 2 * (pf + pt),
        "logger_bot_z": top - L,
        "logger_vol_l": math.pi * (p["tube_od"] / 2) ** 2 * L / 1e6,
        "puck_bot_z": zb,
        "puck_top_z": zb + p["puck_h"],
        "sensor_stack_h": p["magnet_h"] + p["puck_h"],
        "bar_top": p["bar_z"] + p["bar_out"][0] / 2,
        "bar_bot": p["bar_z"] - p["bar_out"][0] / 2,
        "ant_z": p["bar_z"] + p["bar_out"][0] / 2 + p["ant_bracket"][1] + p["ant_t"] / 2,
        "board_fits": p["board"][0] <= 2 * math.sqrt(ri ** 2 - (p["board"][1] / 2) ** 2),
        "cell_fits": p["cell"][0] <= 2 * ri,
        "eye_top": top + 28.0,
        "overall_len": L + 15.0 + 28.0,     # M12 socket below, eye bolt above
    }
    d["ant_gap"] = -p["cover_t"] - (d["ant_z"] + p["ant_t"] / 2)
    pad_t = p["pad"][1]
    d["bar_span"] = p["frame_open"]
    d["bar_overlap"] = p["bar_out_y0"] + p["bar_out"][2] - p["bar_in_y0"]
    return d


def _b3d():
    import build123d as b
    return b


def tube(a, c, r):
    """Solid rod of radius r between two 3D points."""
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    v = c - a
    return b.Solid.make_cylinder(r, v.length, b.Plane(origin=a, z_dir=v.normalized()))


def path(points, r, joints=True):
    """Polyline rod with a ball at each bend so it reads as one cable."""
    b = _b3d()
    s = fuse(tube(a, c, r) for a, c in zip(points, points[1:]))
    if joints:
        for q in points[1:-1]:
            s = s + b.Pos(*q) * b.Sphere(r)
    return s


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def zcyl(x, y, z, r, h):
    """Cylinder on a vertical axis, centred at (x, y, z)."""
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def zspan(x, y, z0, z1, r):
    return zcyl(x, y, (z0 + z1) / 2, r, abs(z1 - z0))


def ycyl(x, y0, y1, z, r):
    b = _b3d()
    return b.Pos(x, (y0 + y1) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(r, abs(y1 - y0))


def box(x, y, z, sx, sy, sz):
    b = _b3d()
    return b.Pos(x, y, z) * b.Box(sx, sy, sz)


def boxspan(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def hexprism(x, y, z0, z1, af):
    """Hexagon nut or head, across flats af, between heights z0 < z1."""
    b = _b3d()
    return b.Pos(x, y, z0) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), amount=abs(z1 - z0))


def ring(x, y, z0, z1, ri, ro):
    return zspan(x, y, z0, z1, ro) - zspan(x, y, z0 - 1, z1 + 1, ri)


def sqtube_y(x, y0, y1, z, side, wall):
    return boxspan(x - side / 2, x + side / 2, y0, y1, z - side / 2, z + side / 2) - \
        boxspan(x - side / 2 + wall, x + side / 2 - wall, y0 - 1, y1 + 1, z - side / 2 + wall, z + side / 2 - wall)


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Every component in installed position, keyed by a short name, in build order."""
    b = _b3d()
    D = derived(p)
    C = {}

    def add(key, name, shape, bom, kind, density=0.0):
        C[key] = Comp(name, shape, bom, kind, density)

    # --- sensor puck on the spindle cap (axis X = Y = 0)
    zc = p["cap_top_z"]
    zb = D["puck_bot_z"]
    zt = D["puck_top_z"]
    ro = p["puck_d"] / 2
    r_up = ro - p["puck_wall"]
    r_lo = p["puck_bore_low"] / 2
    z_base = zb + p["puck_base"]
    z_step = z_base + p["puck_step"]
    sd, sl = p["stud"]
    puck = zspan(0, 0, zb, zt, ro) - zspan(0, 0, z_base, z_step, r_lo) - zspan(0, 0, z_step, zt + 1, r_up) \
        - zspan(0, 0, zb - 1, zb + sl, sd / 2)
    add("puck", "Sensor puck body", puck, 1, "made", 2.70)
    magnet = zspan(0, 0, zc, zb, p["magnet_d"] / 2) + zspan(0, 0, zb, zb + sl, sd / 2)
    add("magnet", f"Pot magnet, {p['magnet_d']:.0f} mm, with M6 stud", magnet, 2, "bought", 0)
    add("piezo", "Piezo disc", zspan(0, 0, z_base, z_base + p["piezo_t"], p["piezo_d"] / 2), 3, "bought", 0)
    zm0 = z_base + p["piezo_t"]
    add("mass", "Seismic mass, brass", zspan(0, 0, zm0, zm0 + p["mass_h"], p["mass_d"] / 2), 3, "made", 0)
    zp1 = z_step + p["preamp_t"]
    add("preamp", "Charge preamplifier board", zspan(0, 0, z_step, zp1, p["preamp_d"] / 2), 4, "bought", 0)
    # --- sensor cable: from the preamplifier up through the potting to the logger's M12 socket
    lx, top = p["logger_x"], p["logger_top_z"]
    bot = D["logger_bot_z"]
    rc = p["cable_d"] / 2
    zs_top = bot - 15.0
    zs_bot = zs_top - p["m12_len"]
    pts = [(0, 0, zp1), (0, 0, zt + 31), (-70, 0, zt + 41), (-130, 0, zt - 44), (-165, 0, zt - 104),
           (lx, 0, zs_bot - 35), (lx, 0, zs_bot)]
    cable = path(pts, rc)
    add("cable", "Sensor cable", cable, 5, "bought", 0)
    potting = zspan(0, 0, zp1, zt, r_up) - zspan(0, 0, zp1 - 1, zt + 1, rc)
    add("potting", "Potting above the board", potting, 11, "fixing", 1.10)
    add("m12_plug", "M12 plug on the cable", zspan(lx, 0, zs_bot, zs_top, p["m12_d"] / 2), 5, "bought", 0)

    # --- logger (axis X = logger_x, Y = 0)
    R = p["tube_od"] / 2
    ri = D["tube_id"] / 2
    pf, pt = p["plug_flange"], p["plug_t"]
    t0, t1 = bot + pf, top - pf                               # tube ends
    tube_s = zspan(lx, 0, t0, t1, R) - zspan(lx, 0, t0 - 1, t1 + 1, ri)
    oc, od = p["oring_cs"]

    def plug(end):
        """end = +1 top plug (flange up), -1 bottom plug (flange down)."""
        if end > 0:
            f0, f1, s0, s1 = t1, top, t1 - pt, t1
        else:
            f0, f1, s0, s1 = bot, t0, t0, t0 + pt
        body = zspan(lx, 0, f0, f1, R) + zspan(lx, 0, s0, s1, ri)
        rings = None
        for dz in p["oring_z"]:
            zc_ = (t1 - dz) if end > 0 else (t0 + dz)
            g = ring(lx, 0, zc_ - oc / 2, zc_ + oc / 2, ri - od, ri + 1)
            body = body - g
            o = ring(lx, 0, zc_ - oc / 2, zc_ + oc / 2, ri - od, ri)
            rings = o if rings is None else rings + o
        return body, rings, (t1 - p["screw_z"]) if end > 0 else (t0 + p["screw_z"])

    def radial_screws(zs):
        out = None
        for a in p["screw_ang"]:
            c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
            shank = tube((lx + c * (ri - 8), s * (ri - 8), zs), (lx + c * R, s * R, zs), 2.0)
            head = tube((lx + c * R, s * R, zs), (lx + c * (R + 2.5), s * (R + 2.5), zs), 3.5)
            sc = shank + head
            out = sc if out is None else out + sc
        return out

    topplug, top_orings, zs_t = plug(+1)
    botplug, bot_orings, zs_b = plug(-1)
    scr_t, scr_b = radial_screws(zs_t), radial_screws(zs_b)
    tube_s = tube_s - scr_t - scr_b
    # top plug fittings: M6 eye bolt on the axis, SMA bulkhead 14 mm toward +Y
    pin = t1 - pt                                             # inner face of the top plug
    eye = zspan(lx, 0, pin - 8, top, 3.0) + zspan(lx, 0, top, top + 3, 8.0) \
        + hexprism(lx, 0, pin - 5, pin, 10.0)
    tor = b.Pos(lx, 0, top + 15.5) * b.Rot(90, 0, 0) * (b.Cylinder(12.5, 5.0) - b.Cylinder(7.5, 6.0))   # the eye
    eye = eye + tor
    sma_y = 14.0
    sma = zspan(lx, sma_y, pin - 15, pin, 5.0) + zspan(lx, sma_y, pin, top, 3.2) + hexprism(lx, sma_y, top, top + 3, 8.0) \
        + zspan(lx, sma_y, top + 3, top + 15, 3.2)
    topplug = topplug - zspan(lx, 0, pin - 1, top + 1, 3.0) - zspan(lx, sma_y, pin - 1, top + 1, 3.2) - scr_t
    botplug = botplug - scr_b
    # bottom plug: front-mount M12 socket (M16 thread through the plug)
    sock = zspan(lx, 0, bot - 15, bot, 8.0) + zspan(lx, 0, bot, t0 + pt, 8.0) + zspan(lx, 0, t0 + pt, t0 + pt + 12, 7.0)
    botplug = botplug - zspan(lx, 0, bot - 1, t0 + pt + 1, 8.0)

    add("tube", "Logger tube, PVC", tube_s, 6, "made", 1.40)
    add("botplug", "Bottom end plug", botplug, 6, "made", 1.41)
    add("socket", "M12 panel socket", sock, 6, "bought", 0)
    add("bot_orings", "O-rings, bottom plug", bot_orings, 6, "fixing", 0)
    add("topplug", "Top end plug", topplug, 6, "made", 1.41)
    add("top_orings", "O-rings, top plug", top_orings, 6, "fixing", 0)
    add("eyebolt", "M6 eye bolt", eye, 13, "bought", 7.9)
    add("sma", "SMA bulkhead", sma, 13, "bought", 0)
    add("screws_top", "Radial screws, top", scr_t, 6, "fixing", 0)
    add("screws_bot", "Radial screws, bottom", scr_b, 6, "fixing", 0)

    # --- internal chassis (printed), hung from the top plug on two standoffs
    sw, st = p["spine"]
    SO_Y = -6.0                                               # standoff line, on the board side of the spine
    sy0, sy1 = -st, 0.0
    so = p["chassis_standoff"]
    sp_top = pin - so
    sp_bot = bot + pf + pt + 18.0
    spine = boxspan(lx - sw / 2, lx + sw / 2, sy0, sy1, sp_bot, sp_top)
    # capacitor clip, desiccant pocket, cell clips (all on the +Y face of the spine)
    hd, hh = p["hlc"]
    cap_c = (lx - 12.0, hd / 2 + 1.5)
    z_cap1 = sp_top - 8.0
    cap_s = zspan(cap_c[0], cap_c[1], z_cap1 - hh, z_cap1, hd / 2)
    clip = None
    for zz in (z_cap1 - 8, z_cap1 - hh + 8):
        c_ = ring(cap_c[0], cap_c[1], zz - 3, zz + 3, hd / 2, hd / 2 + 1.5) & boxspan(lx - 40, lx + 40, -1, cap_c[1] + 3, zz - 4, zz + 4)
        clip = c_ if clip is None else clip + c_
    ddx, ddy, ddz = p["desiccant"]
    dx0 = lx - 1.0
    dz1 = sp_top - 8.0
    des = boxspan(dx0, dx0 + ddx, 1.5, 1.5 + ddy, dz1 - ddz, dz1)
    pocket = boxspan(dx0 - 1.5, dx0 + ddx + 1.5, 0, 1.5 + ddy + 1.5, dz1 - ddz - 1.5, dz1 - 10) - \
        boxspan(dx0, dx0 + ddx, 0.01, 1.5 + ddy, dz1 - ddz, dz1)
    cd, ch = p["cell"]
    cell_c = (lx, cd / 2 + 1.5)
    z_cell0 = sp_bot + 5.0
    cell = zspan(cell_c[0], cell_c[1], z_cell0, z_cell0 + ch, cd / 2)
    cclips = None
    for zz in (z_cell0 + 10, z_cell0 + ch - 10):
        c_ = ring(cell_c[0], cell_c[1], zz - 4, zz + 4, cd / 2, cd / 2 + 2) & boxspan(lx - 40, lx + 40, -1, cell_c[1] + 2.5, zz - 5, zz + 5)
        cclips = c_ if cclips is None else cclips + c_
    tab = boxspan(lx - sw / 2, lx + sw / 2, -9.0, 9.0, sp_top - 4.0, sp_top)       # top tab the standoffs screw to
    tab = tab - zspan(lx - 18, SO_Y, sp_top - 5, sp_top + 1, 1.6) - zspan(lx + 18, SO_Y, sp_top - 5, sp_top + 1, 1.6)
    chassis = spine + tab + clip + pocket + cclips
    add("chassis", "Internal chassis, printed", chassis, 12, "made", 1.27 * 0.6)
    stand = zspan(lx - 18, SO_Y, sp_top, pin, 2.5) + zspan(lx + 18, SO_Y, sp_top, pin, 2.5) \
        + zspan(lx - 18, SO_Y, pin, pin + 6, 1.5) + zspan(lx + 18, SO_Y, pin, pin + 6, 1.5) \
        + zspan(lx - 18, SO_Y, sp_top - 4, sp_top, 1.6) + zspan(lx + 18, SO_Y, sp_top - 4, sp_top, 1.6) \
        + zspan(lx - 18, SO_Y, sp_top - 6, sp_top - 4, 2.75) + zspan(lx + 18, SO_Y, sp_top - 6, sp_top - 4, 2.75)  # M3 screws up through the tab
    C["topplug"].shape = C["topplug"].shape - zspan(lx - 18, SO_Y, pin - 1, pin + 6, 1.5) - zspan(lx + 18, SO_Y, pin - 1, pin + 6, 1.5)
    add("standoffs", "Chassis standoffs (2)", stand, 12, "fixing", 0)
    # main board on four short standoffs on the -Y face
    bx, by, bz = p["board"]
    bz1 = sp_top - 8.0
    board = boxspan(lx - bx / 2, lx + bx / 2, sy0 - 3 - by, sy0 - 3, bz1 - bz, bz1)
    bst = None
    for xx in (-15, 15):
        for zz in (bz1 - 5, bz1 - bz + 5):
            s_ = boxspan(lx + xx - 2.5, lx + xx + 2.5, sy0 - 3, sy0, zz - 2.5, zz + 2.5)
            bst = s_ if bst is None else bst + s_
    add("board", "Main board", board, 7, "bought", 0)
    add("board_standoffs", "Board standoffs (4)", bst, 12, "fixing", 0)
    add("hlc", "Hybrid layer capacitor", cap_s, 7, "bought", 0)
    add("desiccant", "Desiccant pack", des, 11, "bought", 0)
    add("cell", "Primary cell, C size", cell, 8, "bought", 0)

    # --- neck bar hanger, across the neck along Y at x = logger_x
    so_, wo, lo = p["bar_out"]
    si_, wi, li = p["bar_in"]
    bzc = p["bar_z"]
    half = p["frame_open"] / 2
    pd, pdt = p["pad"]
    yo0, yo1 = p["bar_out_y0"], p["bar_out_y0"] + lo
    yi0, yi1 = p["bar_in_y0"], p["bar_in_y0"] + li
    pin_y = p["pin_y"]
    pin_hole_o = zspan(lx, pin_y, bzc - 20, bzc + 20, 3.25)
    outer = sqtube_y(lx, yo0, yo1, bzc, so_, wo) - pin_hole_o
    inner = sqtube_y(lx, yi0, yi1, bzc, si_, wi)
    for n in range(-5, 2):                                   # adjustment holes at 20 mm pitch
        inner = inner - zspan(lx, pin_y + 20 * n, bzc - 20, bzc + 20, 3.25)
    # tube inserts with M10 nuts (outer tube's -Y end, inner tube's +Y end), studs, rubber pads
    ins_o = boxspan(lx - so_ / 2, lx + so_ / 2, yo0 - 2, yo0, bzc - so_ / 2, bzc + so_ / 2) + \
        boxspan(lx - so_ / 2 + wo, lx + so_ / 2 - wo, yo0, yo0 + 15, bzc - so_ / 2 + wo, bzc + so_ / 2 - wo)
    ins_i = boxspan(lx - si_ / 2, lx + si_ / 2, yi1, yi1 + 2, bzc - si_ / 2, bzc + si_ / 2) + \
        boxspan(lx - si_ / 2 + wi, lx + si_ / 2 - wi, yi1 - 15, yi1, bzc - si_ / 2 + wi, bzc + si_ / 2 - wi)
    stud_a = ycyl(lx, -half + pdt, yo0 + 15, bzc, 5.0)
    stud_b = ycyl(lx, yi1 - 15, half - pdt, bzc, 5.0)
    ins_o, ins_i = ins_o - stud_a, ins_i - stud_b
    pads = ycyl(lx, -half, -half + pdt, bzc, pd / 2) + ycyl(lx, half - pdt, half, bzc, pd / 2)
    add("bar_outer", "Neck bar, outer tube", outer, 9, "made", 2.70)
    add("bar_inner", "Neck bar, inner tube", inner, 9, "made", 2.70)
    add("inserts", "Tube end inserts with M10 nuts (2)", ins_o + ins_i, 9, "bought", 1.2)
    add("feet", "Levelling feet, M10, rubber pad (2)", pads + stud_a + stud_b, 9, "bought", 0)
    lockpin = zspan(lx, pin_y, bzc - so_ / 2 - 4, bzc + so_ / 2, 3.0) + zspan(lx, pin_y, bzc + so_ / 2, bzc + so_ / 2 + 2, 5.0)
    add("lockpin", "Locking pin with R-clip", lockpin, 9, "fixing", 0)
    # antenna bracket across the top of the outer tube, antenna on it, one M5 bolt through the tube
    bw_, bt_, bl_ = p["ant_bracket"]
    ay = p["ant_y"]
    zb_top = bzc + so_ / 2
    ax = lx + p["ant_off"]
    bracket = boxspan(lx - 15, lx - 15 + bl_, ay - bw_ / 2, ay + bw_ / 2, zb_top, zb_top + bt_)
    bolt = zspan(lx, ay, bzc - so_ / 2 - 6, zb_top + bt_, 2.5) + zspan(lx, ay, zb_top + bt_, zb_top + bt_ + 3, 4.5) \
        + hexprism(lx, ay, bzc - so_ / 2 - 5, bzc - so_ / 2, 8.0)
    ant_z0 = zb_top + bt_
    ant_stud = zspan(ax, ay, zb_top - 11, ant_z0, 8.0)
    ant_nut = hexprism(ax, ay, zb_top - 6, zb_top, 24.0) - zspan(ax, ay, zb_top - 7, zb_top + 1, 8.0)
    bracket = bracket - zspan(lx, ay, zb_top - 1, zb_top + bt_ + 1, 2.5) - zspan(ax, ay, zb_top - 1, zb_top + bt_ + 1, 8.0)
    outer = C["bar_outer"].shape - zspan(lx, ay, bzc - 20, bzc + 20, 2.5)
    C["bar_outer"].shape = outer
    antenna = zspan(ax, ay, ant_z0, ant_z0 + p["ant_t"], p["ant_d"] / 2) + ant_stud
    add("bracket", "Antenna bracket", bracket, 9, "made", 2.70)
    add("bracket_bolt", "M5 bolt and nyloc nut", bolt, 9, "fixing", 0)
    add("antenna", "Flat LoRa antenna with stud", antenna, 10, "bought", 0)
    add("ant_nut", "Antenna stud nut", ant_nut, 10, "fixing", 0)
    # antenna lead: stud bottom, down and across to the SMA plug on the top plug
    sma_top = top + 15
    lead_pts = [(ax, ay, zb_top - 11), (ax, ay, zb_top - 30), (lx + 40, -100, bzc - 30), (lx + 5, sma_y, top + 50),
                (lx, sma_y, top + 32), (lx, sma_y, sma_top + 12)]
    lead = path(lead_pts, 2.5) + zspan(lx, sma_y, sma_top, sma_top + 12, 4.0)
    add("ant_lead", "Antenna lead with SMA plug", lead, 10, "bought", 0)
    # lanyard: wire rope loop round the outer tube at y = 0, tail down to a snap hook on the eye bolt
    rr = p["lanyard_d"] / 2
    e = so_ / 2 + rr
    loop = path([(lx - e, 0, bzc - e), (lx - e, 0, bzc + e), (lx + e, 0, bzc + e), (lx + e, 0, bzc - e), (lx - e, 0, bzc - e)], rr)
    tail = tube((lx, 0, bzc - e), (lx, 0, bzc - e - 25), rr)
    hook = zspan(lx, 0, D["eye_top"], bzc - e - 25, 2.5)
    add("lanyard", "Lanyard with snap hook", loop + tail + hook, 9, "bought", 0)
    return C


def site_context(p=PARAMS):
    """Existing spindle cap, cover frame edge, cover and chamber neck (grey); not in the BOM."""
    D = derived(p)
    s = p["cap_sq"]
    cap = box(0, 0, p["cap_top_z"] - p["cap_h"] / 2, s, s, p["cap_h"])
    half = p["frame_open"] / 2
    fd = p["frame_depth"]
    x_edge = -half
    frame = box(x_edge - 30, 0, -fd / 2, 60, 120, fd)
    frame -= box(x_edge - 30 + 15, 0, -p["cover_t"] / 2 + 0.01, 31, 130, p["cover_t"])     # cover seat, 30 mm ledge
    cover = boxspan(-half - 28, half + 28, -half - 28, half + 28, -p["cover_t"], -0.5)   # rests on the seat ledge
    nb = p["neck_bot"]
    neck = boxspan(-half - 120, half + 120, -half - 120, half + 120, nb, -fd) - boxspan(-half, half, -half, half, nb - 1, -fd + 1)
    return {"cap": cap, "frame": frame, "cover": cover, "neck": neck, "D": D}


def build_parts(p=PARAMS):
    """Return {BOM line: solid} (fixings counted with the line they belong to)."""
    C = build_components(p)
    out = {}
    for c in C.values():
        if c.bom:
            out[c.bom] = c.shape if c.bom not in out else out[c.bom] + c.shape
    return out


GROUPS = {
    "sensor-puck": ("puck", "magnet", "piezo", "mass", "preamp", "potting"),
    "logger": ("tube", "botplug", "socket", "bot_orings", "topplug", "top_orings", "eyebolt", "sma", "screws_top",
               "screws_bot", "chassis", "standoffs", "board", "board_standoffs", "hlc", "desiccant", "cell"),
    "neck-bar": ("bar_outer", "bar_inner", "inserts", "feet", "lockpin", "bracket", "bracket_bolt", "antenna", "ant_nut",
                 "lanyard"),
}


def assembly(p=PARAMS, with_site=False):
    b = _b3d()
    C = build_components(p)
    kids = [c.shape for c in C.values()]
    if with_site:
        sc = site_context(p)
        kids += [sc["cap"], sc["frame"]]
    return b.Compound(children=kids)


def logger(p=PARAMS):
    b = _b3d()
    C = build_components(p)
    return b.Compound(children=[C[k].shape for k in GROUPS["logger"]])


def sensor_puck(p=PARAMS):
    b = _b3d()
    C = build_components(p)
    return b.Compound(children=[C[k].shape for k in GROUPS["sensor-puck"]])


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch or must stay apart. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    sc = site_context(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    # sensor puck
    chk("Magnet on the spindle cap", S("magnet"), sc["cap"], "touch")
    chk("Magnet and its stud in the puck base", S("magnet"), S("puck"), "touch")
    chk("Piezo disc on the puck base", S("piezo"), S("puck"), "touch")
    chk("Seismic mass on the piezo disc", S("mass"), S("piezo"), "touch")
    wall = S("puck") - zspan(0, 0, -1000, derived(p)["puck_bot_z"] + p["puck_base"], 30)
    chk("Seismic mass clear of the puck bore wall", S("mass"), wall, 2.0)
    chk("Piezo disc clear of the lower bore wall", S("piezo"), wall, 0.5)
    chk("Seismic mass clear of the preamplifier", S("mass"), S("preamp"), 2.0)
    chk("Preamplifier on the step", S("preamp"), S("puck"), "touch")
    chk("Potting on the preamplifier", S("potting"), S("preamp"), "touch")
    chk("Potting clear of the seismic mass", S("potting"), S("mass"), 2.0)
    chk("Cable through the potting", S("cable"), S("potting"), "touch")
    # logger housing
    for k in ("topplug", "botplug"):
        chk(f"{C[k].name} spigot in the tube", S(k), S("tube"), "touch")
    chk("O-rings in the tube (top)", S("top_orings"), S("tube"), "touch")
    chk("O-rings in the tube (bottom)", S("bot_orings"), S("tube"), "touch")
    chk("Radial screws in the tube and top plug", S("screws_top"), S("topplug"), "touch")
    chk("Radial screws in the tube and bottom plug", S("screws_bot"), S("botplug"), "touch")
    chk("Radial screws clear of the top O-rings", S("screws_top"), S("top_orings"), 1.0)
    chk("Radial screws clear of the bottom O-rings", S("screws_bot"), S("bot_orings"), 1.0)
    chk("Eye bolt in the top plug", S("eyebolt"), S("topplug"), "touch")
    chk("SMA bulkhead in the top plug", S("sma"), S("topplug"), "touch")
    chk("Eye bolt clear of the SMA bulkhead", S("eyebolt"), S("sma"), 1.0)
    chk("Radial screws clear of the SMA bulkhead", S("screws_top"), S("sma"), 1.0)
    chk("M12 socket in the bottom plug", S("socket"), S("botplug"), "touch")
    chk("M12 plug on the socket", S("m12_plug"), S("socket"), "touch")
    # chassis and electronics
    chk("Standoffs on the top plug", S("standoffs"), S("topplug"), "touch")
    chk("Standoffs on the chassis", S("standoffs"), S("chassis"), "touch")
    chk("Standoffs clear of the eye bolt nut", S("standoffs"), S("eyebolt"), 1.0)
    chk("Standoffs clear of the SMA bulkhead", S("standoffs"), S("sma"), 1.0)
    chk("Chassis clear of the tube bore", S("chassis"), S("tube"), 0.5)
    chk("Chassis clear of the eye bolt and SMA", S("chassis"), S("eyebolt") + S("sma"), 2.0)
    chk("Chassis clear of the bottom plug and socket", S("chassis"), S("botplug") + S("socket"), 3.0)
    chk("Board on its standoffs", S("board"), S("board_standoffs"), "touch")
    chk("Board standoffs on the chassis", S("board_standoffs"), S("chassis"), "touch")
    chk("Board clear of the tube bore", S("board"), S("tube"), 1.0)
    chk("Board clear of the chassis screw heads", S("board"), S("standoffs"), 1.0)
    chk("Board clear of the top plug fittings", S("board"), S("eyebolt") + S("sma") + S("topplug"), 2.0)
    chk("Capacitor in its clips", S("hlc"), S("chassis"), "touch")
    chk("Cell in its clips", S("cell"), S("chassis"), "touch")
    chk("Desiccant in its pocket", S("desiccant"), S("chassis"), "touch")
    for k in ("hlc", "cell", "desiccant"):
        chk(f"{C[k].name} clear of the tube bore", S(k), S("tube"), 0.5)
    chk("Cell clear of the capacitor and desiccant", S("cell"), S("hlc") + S("desiccant"), 5.0)
    chk("Capacitor clear of the desiccant", S("hlc"), S("desiccant"), 1.0)
    chk("Cell clear of the bottom plug and socket", S("cell"), S("botplug") + S("socket"), 5.0)
    # neck bar
    chk("Inner tube in the outer tube (sliding fit)", S("bar_inner"), S("bar_outer"), 0.4)
    chk("Locking pin through both tubes", S("lockpin"), S("bar_inner"), 0.2)
    chk("Locking pin head on the outer tube", S("lockpin"), S("bar_outer"), "touch")
    chk("Inserts in the tube ends", S("inserts"), S("bar_outer"), "touch")
    chk("Feet screwed into the inserts", S("feet"), S("inserts"), "touch")
    chk("Feet against the neck walls", S("feet"), sc["neck"], "touch")
    chk("Neck bar clear of the cover frame", S("bar_outer") + S("bar_inner"), sc["frame"], 5.0)
    chk("Neck bar clear of the neck walls (only the feet touch)", S("bar_outer") + S("bar_inner"), sc["neck"], 5.0)
    chk("Antenna bracket on the outer tube", S("bracket"), S("bar_outer"), "touch")
    chk("Bracket bolt through the bracket and tube", S("bracket_bolt"), S("bracket"), "touch")
    chk("Bracket bolt nut on the tube", S("bracket_bolt"), S("bar_outer"), "touch")
    chk("Antenna on the bracket", S("antenna"), S("bracket"), "touch")
    chk("Antenna stud nut under the bracket", S("ant_nut"), S("bracket"), "touch")
    chk("Antenna stud nut clear of the tube", S("ant_nut"), S("bar_outer"), 3.0)
    chk("Antenna clear of the cover", S("antenna"), sc["cover"], 10.0)
    chk("Antenna clear of the frame", S("antenna"), sc["frame"], 10.0)
    chk("Antenna lead clear of the neck bar", S("ant_lead"), S("bar_outer") + S("bar_inner") + S("bracket"), 2.0)
    chk("Antenna lead clear of the lanyard", S("ant_lead"), S("lanyard"), 2.0)
    chk("Antenna lead on the SMA bulkhead", S("ant_lead"), S("sma"), "touch")
    chk("Lanyard loop round the outer tube", S("lanyard"), S("bar_outer"), "touch")
    chk("Snap hook on the eye bolt", S("lanyard"), S("eyebolt"), "touch")
    # logger and cable in the chamber
    logger_all = fuse(S(k) for k in GROUPS["logger"])
    chk("Logger clear of the neck bar", logger_all, S("bar_outer") + S("bar_inner"), 40.0)
    chk("Logger clear of the neck walls", logger_all, sc["neck"], 40.0)
    chk("Sensor cable clear of the logger tube", S("cable"), S("tube") + S("botplug"), 5.0)
    chk("Sensor cable clear of the spindle cap", S("cable"), sc["cap"], 5.0)
    chk("Sensor puck clear of the logger", fuse(S(k) for k in GROUPS["sensor-puck"]), logger_all, 50.0)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:58s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def component_masses(p=PARAMS):
    """Mass in kg per BOM line: solids with a density from their volume, the rest from catalogue figures."""
    C = build_components(p)
    m = {}
    for c in C.values():
        if c.bom and c.density:
            m[c.bom] = m.get(c.bom, 0.0) + c.shape.volume * 1e-3 * c.density / 1000
    return m


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    groups = {"leaklisten-assembly": [c.shape for c in C.values()]}
    groups.update({k: [C[n].shape for n in v] for k, v in GROUPS.items()})
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
    D = derived()
    print(f"logger {PARAMS['tube_od']:.0f} x {PARAMS['logger_len']:.0f} mm flange to flange, tube {D['tube_len']:.0f} mm, "
          f"bore {D['tube_id']:.0f} mm, free length {D['free_len']:.0f} mm; {D['overall_len']:.0f} mm with socket and eye bolt")
    print(f"sensor stack {D['sensor_stack_h']:.0f} mm on the cap; antenna {D['ant_gap']:.0f} mm under the cover; "
          f"neck bar tube overlap {D['bar_overlap']:.0f} mm")
    print_checks()
