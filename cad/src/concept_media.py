"""LeakListen concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
The LeakListen parts come from cad/src/model.py (PARAMS, build_parts); the street, soil,
chamber, main and valve are context. Figures on the sheet and in the flow diagram come from
docs/04-calcs/sizing.py (LKL-CAL-001). Not for fabrication.

Coordinates in mm. Street surface at Z = 0, water main along X at Z = -1000, chamber
opening centered on X = 0, Y = 0. The street, soil and chamber are context (hero only) and
are shown in section: everything in front of the plane Y = -250 is removed so the inside of
the valve chamber can be seen. Existing utility assets (pipe, valve) are grey with no BOM number.
"""
import sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[2] / ".kit"), str(Path(__file__).resolve().parent)]
from build123d import Box, Cylinder, Compound, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure
from model import PARAMS as MP, site_context  # noqa: E402
import build123d as _b  # noqa: E402

# An exactly axis-aligned viewpoint makes the hidden-line pass crawl on a many-part model (hours); tilt every
# viewpoint by 0.006 deg (invisible on the sheet).
_orig_ptv = _b.Compound.project_to_viewport


def _ptv(self, origin, up=(0, 0, 1), look_at=None, *a, **k):
    o = _b.Vector(*origin)
    la = _b.Vector(*look_at) if look_at is not None else _b.Vector(0, 0, 0)
    e = (o - la).length * 1e-4
    o = _b.Vector(o.X + (e if abs(o.X - la.X) < 1e-6 else 0), o.Y + (e if abs(o.Y - la.Y) < 1e-6 else 0), o.Z + (e if abs(o.Z - la.Z) < 1e-6 else 0))
    return _orig_ptv(self, (o.X, o.Y, o.Z), up, look_at, *a, **k)


_b.Compound.project_to_viewport = _ptv

# ---------------- key dimensions ----------------
PIPE_Z = -1000.0          # main axis depth (about 0.9 m cover to crown)
PIPE_OD = 170.0           # DN150 ductile iron, about 170 mm OD
CH_X, CH_Y, CH_D = 1000.0, 800.0, 1300.0   # chamber inner size and depth below surface
WALL = 150.0
OPEN = 600.0              # clear opening under the cover
SECTION_Y = -250.0        # context is cut here so the chamber interior shows

CONCRETE = "#B8B2A7"
SOIL = "#8B6B4A"
ASPHALT = "#3F3F46"
IRON = "#6B7280"
ASSET = "#9CA3AF"


def rod(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def keep_back(shape):
    """Section the context: keep only Y >= SECTION_Y."""
    big = 10000.0
    return shape & (Pos(0, SECTION_Y + big / 2, 0) * Box(big, big, big))


# ---------------- context: street, soil, chamber, cover (hero only) ----------------
soil = Pos(0, 375, -800) * Box(2400, 1250, 1500)
outer = Pos(0, 0, -750) * Box(CH_X + 2 * WALL, CH_Y + 2 * WALL, 1400)      # Z -1450 to -50
cavity = Pos(0, 0, -750) * Box(CH_X, CH_Y, 1100)                            # Z -1300 to -200
shaft = Pos(0, 0, -120) * Box(OPEN, OPEN, 170)                              # opening in the roof slab
soil = soil - outer - shaft
chamber = outer - cavity - shaft
road = (Pos(0, 375, -25) * Box(2400, 1250, 50)) - (Pos(0, 0, -25) * Box(OPEN + 120, OPEN + 120, 60))
frame = (Pos(0, 0, -30) * Box(OPEN + 120, OPEN + 120, 60)) - (Pos(0, 0, -30) * Box(OPEN, OPEN, 70))
lid = Pos(0, 0, -20) * Box(OPEN - 6, OPEN - 6, 40)
pipe_buried = (Pos(0, 0, PIPE_Z) * Rot(0, 90, 0) * Cylinder(PIPE_OD / 2, 2440)) - \
              (Pos(0, 0, PIPE_Z) * Box(CH_X - 2, 400, 400))

person = human_figure(1750, x=820, y=520, z=0)

context = [
    Part("Street surface", keep_back(road), ASPHALT),
    Part("Soil (section)", keep_back(soil), SOIL),
    Part("Valve chamber, concrete (section)", keep_back(chamber), CONCRETE),
    Part("Cover frame", keep_back(frame), IRON),
    Part("Chamber cover", keep_back(lid), "#52525B"),
    Part("Buried main", keep_back(pipe_buried), ASSET),
    person,
]

# ---------------- existing assets in the chamber (no BOM number) ----------------
pipe = Pos(0, 0, PIPE_Z) * Rot(0, 90, 0) * (Cylinder(PIPE_OD / 2, CH_X - 4) - Cylinder(PIPE_OD / 2 - 12, CH_X))
flanges = (Pos(-150, 0, PIPE_Z) * Rot(0, 90, 0) * Cylinder(140, 24)
           + Pos(150, 0, PIPE_Z) * Rot(0, 90, 0) * Cylinder(140, 24))
body = Pos(0, 0, PIPE_Z) * Box(280, 210, 260)
bonnet = Pos(0, 0, PIPE_Z + 130 + 150) * Cylinder(75, 300)
spindle = Pos(0, 0, -575) * Cylinder(18, 150)
valve = flanges + body + bonnet + spindle

# ---------------- LeakListen parts (from the kit 1.9 detailed model, option A, LKL-DDR-003 constructable design) ----------------
from model import components  # noqa: E402

cap = site_context(MP)["cap"]
assert MP["cap_top_z"] == -480.0  # the context valve spindle above is drawn for this cap height
_OPT_A = [q for q in components("A") if q["kind"] != "context"]


def bom_group(*lines, keys=None):
    """One shape from every part of option A on the given BOM lines (and, if keys is given, with those keys)."""
    kids = [q["shape"] for q in _OPT_A if q["bom"] in lines and (keys is None or q["key"] in keys)]
    return Compound(children=kids) if kids else None


parts = [
    Part("Valve spindle cap (existing)", cap, "#4B5563"),
    Part("Sensor puck body", bom_group(1), "#0F766E", 1, (170, 0, 20)),
    Part(f"Pot magnet, {MP['magnet_d']:.0f} mm", bom_group(2), "#B91C1C", 2, (170, 0, -50)),
    Part("Piezo disc and seismic mass", bom_group(3), "#D4A017", 3, (170, 0, 95)),
    Part("Charge preamplifier", bom_group(4), "#16A34A", 4, (170, 0, 140)),
    Part("Sensor cable, M12 IP68", bom_group(5), "#111827", 5, (60, 0, -40)),
    Part("Logger housing, IP68", bom_group(6), "#0E7490", 6, (-150, 0, 0)),
    Part("Main board, LoRaWAN", bom_group(7), "#2563EB", 7, (100, -90, 30)),
    Part("Primary cell, Li-SOCl2 C", bom_group(8), "#C2410C", 8, (100, 90, -40)),
    Part("Neck bar hanger and lanyard", bom_group(9), "#A16207", 9, (0, 0, 230)),
    Part("Flat LoRa antenna", bom_group(10), "#7C3AED", 10, (150, 0, 420)),
    Part("Desiccant and potting", bom_group(11), "#E5E7EB", None, (100, 90, 60)),
    Part("Internal chassis", bom_group(12), "#94A3B8", 12, (100, 0, 0)),
    Part("Eye bolt and SMA bulkhead", bom_group(13), "#374151", 13, (-150, 0, 90)),
]

# The existing main and valve are shown in the hero only, so the exploded view and cutaway frame the logger
context += [Part("Water main in chamber (existing)", pipe, ASSET), Part("Gate valve (existing)", valve, IRON)]

# render_all's cutaway cutter is centered on Z = 0 and sized from the largest part, so the logger
# parts are lifted 400 mm for the kit media; the hero below uses the true street coordinates.
def lift(ps):
    return [Part(p.name, Pos(0, 0, 400) * p.shape, p.color, p.bom, p.explode, p.alpha) for p in ps]


lifted, lifted_context = lift(parts), lift(context)

render_all(
    lifted, project="LeakListen", title="Clamp-on acoustic leak logger concept", dwg_no="LKL-DWG-010",
    key_figures=["Magnet-on piezo sensor, 53 g seismic mass; about 1.0 ug/rtHz",
                 "Listens 02:00 to 04:00; 12 x 20 s windows a night",
                 "About 1.2 mAh/day; C cell life 10 years or more",
                 "One 24-byte LoRaWAN summary a night; raw audio stays on device",
                 "Hears about 185 m on iron (estimate); hydrophone variant for plastic",
                 "Hangs from a neck bar; placed from the surface; about $142 in parts"],
    scale_figure=False, context=lifted_context,
    flow={"title": "nightly data flow per logger, kB (LKL-CAL-001 estimates: 240 s at 8 kS/s, 16 bit; 12 spectra of 64 bands)", "unit": "kB",
          "stages": [("Pipe vibration", "5 Hz to 2 kHz"),
                     ("Sampled audio", 3840), ("Band spectra", 1.5),
                     ("Nightly summary", 0.024), ("Trend and leak flag", "on server or TwinKit")],
          "losses": [(1, "Raw samples deleted on device", 3838)]},
)

# Hero with a plain-language note (the default note would list every context part by name)
from concept import _render  # noqa: E402
hero_parts = [Part(p.name, keep_back(p.shape), p.color, p.bom, p.explode, p.alpha) if p.bom == 9 else p for p in parts]  # bar sectioned
_render(hero_parts + context, Path("media") / "hero.png", title="LeakListen",
        note="Grey figure: 1.75 m person for scale. Street, soil and valve chamber shown in section.")
