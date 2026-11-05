"""LeakListen product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is (kit 1.9 detailed model of option A, 72 parts:
PVC tube, turned plugs with O-rings and radial screws, M12 socket and plug, printed chassis, board, cell, capacitor,
desiccant, eye bolt, SMA bulkhead, light pipe, neck bar with feet and pin, antenna, lanyard, sensor puck with magnet,
piezo, mass, preamplifier and potting). Added to them are two appearance parts only, a teal name band and the
owner and lithium warning label on the tube (no dimension changes). The site is added as context parts.

The hero is a site render inside the valve chamber: the whole model is lifted 1300 mm so that the chamber floor is
ground level (model z = 0, concrete, rendered by .kit/photoreal.py as an outdoor scene). Walls, roof slab, street and
soil are cut away on the camera side (the front and the right of the chamber) and named "(site)" so the camera frames
the logger, the bar and the sensor. The main, valve and spindle stand on the floor. No person is shown in the hero
because a 1.75 m person does not stand in a 1.3 m deep chamber; the studio view gives the scale by its own dimensions.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the product), "context" (the chamber and valve, site render only).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

import build123d as b  # noqa: E402
import cad_parts as cp  # noqa: E402
import model as M  # noqa: E402
from lkl_parts import boxspan, zspan, ring, xcyl, mk  # noqa: E402

TITLE = "LeakListen: acoustic leak logger for water valve chambers"
SHIFT = 1300.0        # mm: the chamber floor (model z = -1300) becomes ground level z = 0

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=45,-60", "--lens=50"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 24, "az": -40, "args": _SITE,
     "note": "Site render inside a valve chamber, in section, from the front right and above (about 24 deg elevation): "
             "the logger hanging from the neck bar under the cover frame with the flat antenna on the bar, the sensor puck on "
             "its magnet on the spindle cap of a gate valve; chamber walls, roof slab and street cut away on the camera side; "
             "no person (the chamber is 1.3 m deep)"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 24, "az": -40,
     "note": "Studio render from the front right and above (about 24 deg elevation): logger tube with its teal band and "
             "warning label, turned end plugs, eye bolt, SMA bulkhead and status light, neck bar with antenna and lanyard, "
             "sensor cable and the sensor puck on its pot magnet"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 22, "az": -55,
     "note": "Exploded view from the front right and above (about 22 deg elevation): tube and end plugs, chassis, main "
             "board, C cell and desiccant, neck bar and lanyard, antenna, sensor cable and the sensor puck with piezo, "
             "mass, preamplifier and pot magnet"},
    {"name": "detail", "groups": ["shell"], "explode": False, "el": 18, "az": -35,
     "note": "Detail from the front right, slightly above (about 18 deg elevation): the logger with its label, plugs "
             "and fittings, the neck bar and antenna, and the sensor puck on its magnet"},
]

# Explode vectors by part key (mm), as the old appearance model: toward the camera, plugs and fittings along the axis
_EL = (-40, -40, 0)
_ETP = (-40, -40, 95)
_EBP = (-40, -40, -95)
_EXPLODE = {
    "tube": _EL, "topplug": _ETP, "top_orings": _ETP, "screws_top": _ETP, "eyebolt": _ETP, "eye_washer": _ETP, "eye_nut": _ETP,
    "sma": _ETP, "sma_nut": _ETP, "lpipe": _ETP, "ant_lead": _ETP,
    "botplug": _EBP, "bot_orings": _EBP, "screws_bot": _EBP, "socket": _EBP, "socket_nut": _EBP,
    "chassis": (-100, -100, 40), "standoffs": (-100, -100, 70), "board": (-100, -100, 40), "board_standoffs": (-100, -100, 40),
    "hlc": (-100, -60, 70), "cell": (-100, -40, -45), "desiccant": (-100, 40, -45),
    "bar_outer": (-60, 0, 150), "bar_inner": (-60, 60, 150), "inserts": (-60, 0, 150), "feet": (-60, 0, 150),
    "lockpin": (-60, 0, 190), "bracket": (-60, 0, 190), "bracket_bolt": (-60, 0, 190), "lanyard": (0, 0, 120),
    "antenna": (40, -30, 240), "ant_nut": (40, -30, 200),
    "cable": (40, -20, -40), "m12_plug": (40, -20, -40),
    "puck": (170, -40, 0), "magnet": (170, -40, -50), "magnet_core": (170, -40, -50),
    "piezo": (170, -40, 75), "mass": (170, -40, 105), "preamp": (170, -40, 150), "potting": (170, -40, 190),
}


def _band(x, y, z, r, h, arc_deg, face_deg, t):
    """Thin raised band on a vertical cylinder of radius r: arc `arc_deg` wide centred on `face_deg`."""
    band = ring(x, y, z - h / 2, z + h / 2, r - 0.3, r + t)
    if arc_deg >= 359:
        return band
    w = 2 * (r + 2) * math.sin(math.radians(min(arc_deg, 179) / 2))
    a = math.radians(face_deg)
    d = r + 2
    cut = b.Pos(x + math.cos(a) * d / 2, y + math.sin(a) * d / 2, z) * b.Rot(0, 0, face_deg) * b.Box(d + 2, w, h + 4)
    return band & cut


def site():
    """Valve chamber in section and the valve it serves, original model coordinates (street z = 0)."""
    out = []
    ctx = lambda n, sh, mat: out.append(cp.part(f"{n} (site)", sh, mat, kind="context", group="context"))
    ctx("Chamber floor slab", boxspan(-650, 650, -550, 550, -1450, -1300), "concrete")
    ctx("Chamber back wall", boxspan(-650, 650, 400, 550, -1450, -200), "concrete")
    ctx("Chamber left wall", boxspan(-650, -500, -550, 550, -1450, -200), "concrete")
    slab = boxspan(-650, -300, -550, 550, -200, -50) + boxspan(-300, 420, 300, 550, -200, -50) \
        + boxspan(-650, -70, -550, -300, -200, -50)
    ctx("Roof slab", slab, "concrete")
    ctx("Street surface left", boxspan(-1100, -360, -700, 700, -50, 0), "asphalt" if "asphalt" in cp.MATERIALS else "concrete")
    ctx("Street surface back", boxspan(-360, 700, 300, 700, -50, 0), "asphalt" if "asphalt" in cp.MATERIALS else "concrete")
    ctx("Soil beside the chamber", boxspan(-1100, -650, -700, 700, -1450, -50) + boxspan(-650, 700, 550, 700, -1450, -50), "soil")
    # the main and the gate valve (existing), standing on the floor
    pz = -1000.0
    pipe = b.Pos(0, 0, pz) * b.Rot(0, 90, 0) * (b.Cylinder(85, 1120) - b.Cylinder(73, 1130))
    ctx("Water main", pipe, "mild_steel")
    for sx in (-1, 1):
        ctx(f"Pipe flange {'right' if sx > 0 else 'left'}", b.Pos(sx * 150, 0, pz) * b.Rot(0, 90, 0) * (b.Cylinder(140, 24) - b.Cylinder(74, 26)), "mild_steel")
        ctx(f"Pipe support {'right' if sx > 0 else 'left'}", boxspan(sx * 350 - 100, sx * 350 + 100, -130, 130, -1310, pz - 82), "concrete")
    ctx("Valve body", b.Pos(0, 0, pz) * b.Box(280, 210, 260), "mild_steel")
    ctx("Valve bonnet", b.Pos(0, 0, pz + 130 + 150) * b.Cylinder(75, 300), "mild_steel")
    ctx("Valve spindle", zspan(0, 0, -570, -500, 18), "mild_steel")
    for q in M.context_parts():                       # spindle cap and cover frame edge, as the model has them
        if q["key"] in ("cap", "frame"):
            ctx(q["name"].replace(" (existing)", ""), q["shape"], "mild_steel")
    return out


def product_parts(P=M.PARAMS):
    D = M.derived(P)
    out = []
    for q in M.components(M.CHOSEN):
        if q["kind"] == "context":
            continue
        r = dict(q)
        r["group"] = "shell"
        r["explode"] = tuple(float(v) for v in _EXPLODE.get(q["key"], (0, 0, 0)))
        out.append(r)
    lx, top = P["logger_x"], P["logger_top_z"]
    ro = P["tube_od"] / 2
    t1 = top - P["plug_flange"]
    face = -45.0
    zc = (top + D["logger_bot_z"]) / 2 + 10
    out.append(cp.part("Logger name band", _band(lx, 0, t1 - 14, ro, 8.0, 360, face, 0.5), "petg_teal", kind="made", bom=None,
                       group="shell", explode=_EL))
    out.append(cp.part("Owner and lithium warning label", _band(lx, 0, zc, ro, 70.0, 110, face, 0.3), "label", kind="made",
                       bom=None, group="shell", explode=_EL))
    return [dict(p, shape=b.Pos(0, 0, SHIFT) * p["shape"]) for p in out + site()]


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name'][:46]:46s} {p['group']:8s} {p['material']:14s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
