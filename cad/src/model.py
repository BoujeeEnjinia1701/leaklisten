"""LeakListen parametric model (build123d), kit 1.9 interface, detail level D3 (LKL-DDR-003 constructable design).

Run from the repo root:  python cad/src/model.py          (prints part counts and mass per option)
                         python cad/src/model.py --check  (constructability checks on option A)
                         python cad/src/model.py --stl    (STL for the chosen option's assembly and its groups)
STEP files and the fidelity report come from  python .kit/cad_check.py --export  (cad/fidelity.json).

Kit 1.9 interface (STANDARDS section 24):
    PARAMS      every main dimension of the chosen design (option A); docs/04-calcs/sizing.py reads it
    OPTIONS     key -> name of every concept option; each is modelled to D3
    PRINCIPLES  key -> one-line working principle
    CHOSEN      the option the drawing, BOM and build plan describe (the design as it stood before kit 1.8)
    components(option)   list of cad_parts.part() dicts

Axes: the street surface is Z = 0 and the chamber opening is centred on X = Y = 0. The example site is a DN150 gate
valve whose square spindle cap top sits 480 mm below the street; the cover frame's clear opening is 600 mm square and
the chamber neck continues it down to 230 mm below the street.

Option A (current design, LKL-DDR-003): magnet-on piezo accelerometer on the valve spindle cap, logger hung under the
cover from a telescopic neck bar on a wire rope lanyard, flat antenna on the bar. Options B (hydrant cap hydrophone)
and C (ground spike geophone) are in options_bc.py and share the logger electronics (lkl_logger.py). Main dimensions
and interfaces only; tolerances are TRL 4 work.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]
import build123d as b  # noqa: E402
import cad_parts as cp  # noqa: E402
from lkl_parts import (mk, fuse, tube, path, smooth, zcyl, zspan, ycyl, xcyl, box, boxspan, hexprism, ring, put,  # noqa: E402,F401
                       r_clip, pan_screw)
import lkl_logger as LG  # noqa: E402

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
    # 7 status light pipe: clear acrylic rod from 1.5 mm above the main board's top edge, through the
    #   top plug, flush with its top face (lit for a brief blink at power-up or magnet swipe)
    "lpipe_d": 3.0, "lpipe_xy": (10.0, -13.0), "lpipe_gap": 1.5,
}

BOM = {  # BOM line: name
    1: "Sensor puck body", 2: "Pot magnet", 3: "Piezo disc and seismic mass", 4: "Charge preamplifier",
    5: "Sensor cable", 6: "Logger housing", 7: "Main board", 8: "Primary cell", 9: "Neck bar hanger",
    10: "Flat LoRa antenna", 11: "Desiccant and consumables", 12: "Internal chassis", 13: "Top plug fittings",
}

OPTIONS = {"A": "Magnet-on contact sensor", "B": "Hydrant cap hydrophone", "C": "Ground spike geophone"}
PRINCIPLES = {
    "A": "A magnet-on piezo accelerometer on the valve spindle cap hears pipe-wall vibration; the logger hangs under the cover.",
    "B": "A hydrophone in a hydrant outlet cap hears leak sound in the water itself; the logger is clamped beside the hydrant.",
    "C": "A geophone on a stainless spike in the verge hears leak noise through the soil; the logger sits in a flush ground box.",
}
CHOSEN = "A"
OPTION_VIEWS = {  # render elevation, azimuth; scale reference "none" (a 1.75 m person would dwarf a 0.3 m logger)
    "A": {"el": 24, "az": -50, "scale": "none"},
    "B": {"el": 24, "az": -50, "scale": "none"},
    "C": {"el": 24, "az": -50, "scale": "none"},
}
# Parts that are designed to touch (name fragments); the interference check ignores these pairs.
ALLOWED_CONTACTS = []


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
    d["bar_span"] = p["frame_open"]
    d["bar_overlap"] = p["bar_out_y0"] + p["bar_out"][2] - p["bar_in_y0"]
    return d


# ------------------------------------------------------------------ site (existing assets, context parts)
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
    cover = boxspan(-half - 28, half + 28, -half - 28, half + 28, -p["cover_t"], -0.5)
    nb = p["neck_bot"]
    neck = boxspan(-half - 120, half + 120, -half - 120, half + 120, nb, -fd) - boxspan(-half, half, -half, half, nb - 1, -fd + 1)
    return {"cap": cap, "frame": frame, "cover": cover, "neck": neck, "D": D}


def context_parts(p=PARAMS):
    sc = site_context(p)
    return [mk("cap", "Valve spindle cap (existing)", sc["cap"], "mild_steel", "context"),
            mk("frame", "Cover frame edge (existing)", sc["frame"], "mild_steel", "context"),
            mk("neck", "Chamber neck (existing)", sc["neck"], "concrete", "context")]


# ------------------------------------------------------------------ option A: neck bar, antenna, lanyard
def bar_parts(p, D):
    out = []
    add = lambda *a, **k: out.append(mk(*a, **k))
    lx, top = p["logger_x"], p["logger_top_z"]
    so_, wo, lo = p["bar_out"]
    si_, wi, li = p["bar_in"]
    bzc = p["bar_z"]
    half = p["frame_open"] / 2
    pd, pdt = p["pad"]
    yo0, yo1 = p["bar_out_y0"], p["bar_out_y0"] + lo
    yi0, yi1 = p["bar_in_y0"], p["bar_in_y0"] + li
    pin_y = p["pin_y"]
    ay = p["ant_y"]
    ax = lx + p["ant_off"]
    zb_top = bzc + so_ / 2

    def vhole(y, d, h=40.0):
        return zspan(lx, y, bzc - h / 2, bzc + h / 2, d / 2)

    outer = put(cp.shs(so_, wo, lo), (lx, yo0, bzc), "+y")
    outer = outer - vhole(pin_y, 6.5) - vhole(ay, 5.5)
    inner = put(cp.shs(si_, wi, li), (lx, yi0, bzc), "+y")
    for n in range(-5, 2):                                    # adjustment holes at 20 mm pitch
        inner = inner - vhole(pin_y + 20 * n, 6.5)
    add("bar_outer", "Neck bar outer tube, 20 x 20 x 1.5 aluminium", outer, "aluminium", "made", 9)
    add("bar_inner", "Neck bar inner tube, 16 x 16 x 1.5 aluminium", inner, "aluminium", "made", 9)

    def insert(y_face, direction, side, wall):
        """Nylon end insert: plug 15 mm into the tube, 2 mm flange outside, 10 mm centre hole for the foot stud."""
        inn = side - 2 * wall - 0.4
        plug = put(cp.break_edges(box(0, 0, 7.5, inn, inn, 15.0), 1.5), (lx, y_face, bzc), direction)
        fl = put(cp.break_edges(box(0, 0, -1.0, side, side, 2.0), 0.6), (lx, y_face, bzc), direction)
        s = plug + fl
        return s - put(b.Pos(0, 0, 0) * b.Cylinder(5.0, 40.0), (lx, y_face, bzc), direction)

    add("inserts", "Tube end insert, outer tube (nylon)", insert(yo0, "+y", so_, wo), "nylon_white", "bought", 9)
    add("inserts", "Tube end insert, inner tube (nylon)", insert(yi1, "-y", si_, wi), "nylon_white", "bought", 9)
    # levelling feet: M10 stud, jam nut and rubber pad at each end
    ya0, ya1 = -half + pdt, yo0 + 15
    yb0, yb1 = yi1 - 15, half - pdt
    add("feet", "Levelling foot stud M10 (outer tube end)", put(cp.round_bar(10, ya1 - ya0, 0.8), (lx, ya0, bzc), "+y"), "stainless", "bought", 9)
    add("feet", "Levelling foot stud M10 (inner tube end)", put(cp.round_bar(10, yb1 - yb0, 0.8), (lx, yb0, bzc), "+y"), "stainless", "bought", 9)
    add("feet", "Rubber pad 40 x 8 (outer tube end)", put(cp.break_edges(b.Cylinder(pd / 2, pdt, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN)), 1.5), (lx, -half, bzc), "+y"),
        "epdm", "bought", 9)
    add("feet", "Rubber pad 40 x 8 (inner tube end)", put(cp.break_edges(b.Cylinder(pd / 2, pdt, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN)), 1.5), (lx, half - pdt, bzc), "+y"),
        "epdm", "bought", 9)
    add("feet", "M10 jam nut (ISO 4032), outer end", put(cp.hex_nut(10), (lx, yo0 - 2.0 - 8.4, bzc), "+y"), "stainless", "fastener", 9)
    add("feet", "M10 jam nut (ISO 4032), inner end", put(cp.hex_nut(10), (lx, yi1 + 2.0, bzc), "+y"), "stainless", "fastener", 9)
    # locking pin with R-clip
    grip = so_
    pin = put(cp.clevis_pin(6, grip), (lx, pin_y, zb_top))
    add("lockpin", "Locking pin 6 mm (ISO 2341 B)", pin, "stainless", "bought", 9)
    add("lockpin", "R-clip", r_clip(lx, pin_y, zb_top - grip - 6.0, 6.0), "stainless", "fastener", 9)
    # antenna bracket across the top of the outer tube, M5 bolt through the tube
    bw_, bt_, bl_ = p["ant_bracket"]
    bracket = cp.sheet(bl_, bw_, bt_, holes=[(lx - (lx - 15 + bl_ / 2), 0, 5.5), (ax - (lx - 15 + bl_ / 2), 0, 16.0)], r_corner=4.0, edge=0.5)
    bracket = b.Pos(lx - 15 + bl_ / 2, ay, zb_top) * bracket
    add("bracket", "Antenna bracket, 40 x 3 aluminium flat", bracket, "aluminium", "made", 9)
    for nm, shp in cp.hex_bolt_set(5, bt_ + so_):
        kind = "fastener"
        add("bracket_bolt", nm.replace("hex bolt", "bolt") + " (bracket)", b.Pos(lx, ay, zb_top + bt_) * shp, "stainless", kind, 9)
    # flat antenna on its stud
    ant_z0 = zb_top + bt_
    body = b.Pos(ax, ay, ant_z0 + p["ant_t"] / 2) * b.Cylinder(p["ant_d"] / 2, p["ant_t"])
    body = cp.break_edges(body, 2.0)
    ant = body + zspan(ax, ay, zb_top - 11, ant_z0, 8.0)
    add("antenna", "Flat LoRa antenna with centre stud", ant, "antenna_white", "bought", 10)
    nut = hexprism(ax, ay, zb_top - 6, zb_top, 24.0) - zspan(ax, ay, zb_top - 7, zb_top + 1, 8.0)
    add("ant_nut", "Antenna stud nut", nut, "stainless", "fastener", 10)
    # antenna lead with SMA plug
    sma_y = 14.0
    pts = [(ax, ay, zb_top - 11), (ax, ay, zb_top - 30), (lx + 40, -100, bzc - 30), (lx + 5, sma_y, top + 50),
           (lx, sma_y, top + 32), (lx, sma_y, top + 27)]
    lead = path(smooth(pts, 1), 2.5)
    plug_ = ring(lx, sma_y, top + 4.5, top + 15, 3.175, 4.5) + zspan(lx, sma_y, top + 15, top + 16, 4.5) + zspan(lx, sma_y, top + 16, top + 27, 2.5)
    add("ant_lead", "Antenna lead with SMA plug", cp.break_edges(plug_, 0.3) + lead, "pu_black", "bought", 10)
    # lanyard: wire rope loop round the outer tube at y = 0, tail down to a ferrule and the snap link on the eye bolt
    rr = p["lanyard_d"] / 2
    e = so_ / 2 + rr
    loop = path([(lx - e, 0, bzc - e), (lx - e, 0, bzc + e), (lx + e, 0, bzc + e), (lx + e, 0, bzc - e), (lx - e, 0, bzc - e)], rr)
    z_tail = bzc - e - 25.0
    tail = tube((lx, 0, bzc - e), (lx, 0, z_tail), rr)
    zc_eye = top + 15.5
    z_link = zc_eye + 10.0
    stem = tube((lx, 0, z_link + 4.0), (lx, 0, z_tail), rr)
    link = b.Pos(lx, 0, z_link) * b.Rot(0, 90, 0) * b.Torus(5.0, 1.2)
    add("lanyard", "Lanyard, 3 mm stainless wire rope", loop + tail, "stainless", "bought", 9)
    ferrule = zspan(lx, 0, z_tail - 7.0, z_tail + 7.0, 3.0) - stem - tail
    add("lanyard", "Swaged ferrule", ferrule, "zinc_plated", "bought", 9)
    add("lanyard", "Snap link on the eye bolt", stem + link, "stainless", "bought", 9)
    return out


def components_A(p=PARAMS):
    D = derived(p)
    lx, top = p["logger_x"], p["logger_top_z"]
    parts = LG.puck_parts(p, D) + LG.cable_parts(p, D, lx, top) + LG.logger_parts(p, D, lx, top) + bar_parts(p, D)
    return parts + context_parts(p)


_CACHE = {}


def components(option):
    """Parts of a concept option as cad_parts.part() dicts (cached; shapes are shared, copy before changing them)."""
    if option not in _CACHE:
        if option == "A":
            _CACHE[option] = components_A()
        else:
            import options_bc
            _CACHE[option] = options_bc.components(option)
    return list(_CACHE[option])


# ------------------------------------------------------------------ compatibility for the sheets, build plan and media scripts
@dataclass
class Comp:
    """One group of parts sharing a key (the key is what the build plan pictures and the sizing note call it)."""
    name: str
    shape: object
    bom: int | None
    kind: str
    density: float = 0.0


_DENS = {"puck": 2.70, "tube": 1.40, "botplug": 1.41, "topplug": 1.41, "eyebolt": 0.0, "lpipe": 1.19, "potting": 1.10,
         "chassis": 1.27 * 0.6, "bar_outer": 2.70, "bar_inner": 2.70, "inserts": 1.2, "bracket": 2.70}


def build_components(p=PARAMS):
    """Every component of option A in installed position, keyed by short name (parts that share a key are one entry)."""
    groups = {}
    for q in components_A(p) if p is not PARAMS else components("A"):
        if q["kind"] == "context":
            continue
        groups.setdefault(q["key"], []).append(q)
    C = {}
    for k, ps in groups.items():
        shp = ps[0]["shape"] if len(ps) == 1 else b.Compound(children=[q["shape"] for q in ps])
        C[k] = Comp(ps[0]["name"], shp, ps[0]["bom"], ps[0]["kind"], _DENS.get(k, 0.0))
    return C


class _Lazy(dict):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def __missing__(self, k):
        self[k] = self.fn(k)
        return self[k]


def build_parts(p=PARAMS):
    """{BOM line: solid}. Line 2 is the catalogue envelope of the pot magnet (cylinder and stud) because its mass is
    a catalogue figure; the other lines are the fused model parts."""
    def make(k):
        if k == 2:
            D = derived(p)
            sd, sl = p["stud"]
            zc, zb = p["cap_top_z"], D["puck_bot_z"]
            return zspan(0, 0, zc, zb, p["magnet_d"] / 2) + zspan(0, 0, zb, zb + sl, sd / 2)
        return fuse([q["shape"] for q in components("A") if q["bom"] == k and q["kind"] != "context"])
    return _Lazy(make)


def component_masses(p=PARAMS):
    """Mass in kg per BOM line for the made parts with a density in _DENS (volume from the model)."""
    C = build_components(p)
    m = {}
    for k, c in C.items():
        if c.bom and c.density:
            m[c.bom] = m.get(c.bom, 0.0) + c.shape.volume * 1e-3 * c.density / 1000
    return m


GROUPS = {
    "sensor-puck": ("puck", "magnet", "piezo", "mass", "preamp", "potting"),
    "logger": ("tube", "botplug", "socket", "bot_orings", "topplug", "top_orings", "eyebolt", "sma", "lpipe", "screws_top",
               "screws_bot", "chassis", "standoffs", "board", "board_standoffs", "hlc", "desiccant", "cell"),
    "neck-bar": ("bar_outer", "bar_inner", "inserts", "feet", "lockpin", "bracket", "bracket_bolt", "antenna", "ant_nut",
                 "lanyard", "ant_lead"),
}


def assembly(p=PARAMS, with_site=False):
    kids = [q["shape"] for q in components("A") if with_site or q["kind"] != "context"]
    return b.Compound(children=kids)


def logger(p=PARAMS):
    C = build_components(p)
    return b.Compound(children=[C[k].shape for k in GROUPS["logger"]])


def sensor_puck(p=PARAMS):
    C = build_components(p)
    return b.Compound(children=[C[k].shape for k in GROUPS["sensor-puck"]])


# ------------------------------------------------------------------ constructability checks (option A)
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch or must stay apart. Returns (description, overlap mm3, gap mm, expectation, ok)."""
    parts = components("A")
    by = {}
    for q in parts:
        by.setdefault(q["key"], []).append(q["shape"])
    S = lambda *ks: fuse([s for k in ks for s in by[k]])  # noqa: E731
    sc = site_context(p)
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 5.0 and (gp < 0.25 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    chk("Magnet on the spindle cap", S("magnet"), sc["cap"], "touch")
    chk("Magnet stud in the puck base", S("magnet"), S("puck"), "touch")
    chk("Piezo on the puck base", S("piezo"), S("puck"), "touch")
    chk("Seismic mass on the piezo", S("mass"), S("piezo"), "touch")
    chk("Seismic mass clear of the puck bore wall", S("mass"), S("puck"), 0.5)
    chk("Seismic mass clear of the preamplifier", S("mass"), S("preamp"), 2.0)
    chk("Preamplifier on the step", S("preamp"), S("puck"), "touch")
    chk("Potting on the preamplifier", S("potting"), S("preamp"), "touch")
    chk("Potting clear of the seismic mass", S("potting"), S("mass"), 2.0)
    chk("Cable through the potting", S("cable"), S("potting"), "touch")
    chk("Top plug spigot in the tube", S("topplug"), S("tube"), "touch")
    chk("Bottom plug spigot in the tube", S("botplug"), S("tube"), "touch")
    chk("Radial screws clear of the O-rings", S("screws_top", "screws_bot"), S("top_orings", "bot_orings"), 1.0)
    chk("Eye bolt in the top plug", S("eyebolt"), S("topplug"), "touch")
    chk("Eye bolt clear of the SMA bulkhead", S("eyebolt"), S("sma"), 1.0)
    chk("M12 socket in the bottom plug", S("socket"), S("botplug"), "touch")
    chk("M12 plug on the socket", S("m12_plug"), S("socket"), "touch")
    chk("Standoffs on the top plug", S("standoffs"), S("topplug"), "touch")
    chk("Light pipe clear of the board", S("lpipe"), S("board"), 1.0)
    chk("Chassis clear of the tube bore", S("chassis"), S("tube"), 0.5)
    chk("Board clear of the tube bore", S("board"), S("tube"), 1.0)
    chk("Capacitor, cell and desiccant clear of the tube bore", S("hlc", "cell", "desiccant"), S("tube"), 0.5)
    chk("Inner tube in the outer tube (sliding fit)", S("bar_inner"), S("bar_outer"), 0.4)
    chk("Feet against the neck walls", S("feet"), sc["neck"], "touch")
    chk("Neck bar clear of the cover frame", S("bar_outer", "bar_inner"), sc["frame"], 5.0)
    chk("Antenna clear of the cover", S("antenna"), sc["cover"], 10.0)
    logger_all = S(*GROUPS["logger"])
    chk("Logger clear of the neck bar", logger_all, S("bar_outer", "bar_inner"), 40.0)
    chk("Logger clear of the neck walls", logger_all, sc["neck"], 40.0)
    chk("Sensor cable clear of the logger tube", S("cable"), S("tube", "botplug"), 5.0)
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


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    if "--stl" in sys.argv:
        from build123d import export_stl
        out = HERE.parent / "stl"
        out.mkdir(exist_ok=True)
        C = build_components()
        sets = {"leaklisten-assembly": [c.shape for c in C.values()]}
        sets.update({k: [C[n].shape for n in v] for k, v in GROUPS.items()})
        for name, shapes in sets.items():
            export_stl(b.Compound(children=shapes), str(out / f"{name}.stl"), tolerance=0.15, angular_tolerance=0.4)
            print("wrote", name)
        sys.exit(0)
    for o in OPTIONS:
        try:
            ps = [q for q in components(o) if q["kind"] != "context"]
        except Exception as ex:   # noqa: BLE001
            print(o, "not available:", ex)
            continue
        print(f"option {o} {OPTIONS[o]}: {len(ps)} parts, mass {sum(cp.mass_kg(q) for q in ps):.2f} kg")
