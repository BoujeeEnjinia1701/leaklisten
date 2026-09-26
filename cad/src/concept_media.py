"""LeakListen concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Street surface at Z = 0, water main along X at Z = -1000, chamber
opening centered on X = 0, Y = 0. The street, soil and chamber are context (hero only) and
are shown in section: everything in front of the plane Y = -250 is removed so the inside of
the valve chamber can be seen. Existing utility assets (pipe, valve) are grey with no BOM number.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure

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
cap = Pos(0, 0, -490) * Box(50, 50, 20)          # square spindle cap, top at Z = -480

# ---------------- LeakListen parts ----------------
# 2 Pot magnet, 32 mm, on the spindle cap
magnet = Pos(0, 0, -474) * Cylinder(16, 12)
# 1 Sensor puck: aluminium body, 40 mm dia x 34 mm, hollow for the piezo and preamp
puck = Pos(0, 0, -451) * (Cylinder(20, 34) - Pos(0, 0, 3) * Cylinder(16, 26))
# 3 Piezo disc and seismic mass, bonded to the puck base
piezo = Pos(0, 0, -461) * (Cylinder(14, 2) + Pos(0, 0, 3.5) * Cylinder(9, 5))
# 4 Charge preamplifier board in the puck
preamp = Pos(0, 0, -447) * Box(22, 22, 3)
# 5 Sensor cable, 2 m, shielded, M12 IP68 plug at the logger (shown shortened)
LX = -200.0               # logger hangs on the -X side of the opening, clear of the street slab in the hero view
cable = (rod((0, 0, -434), (0, 0, -380), 3.5) + rod((0, 0, -380), (-60, 0, -350), 3.5)
         + rod((-60, 0, -350), (-175, 0, -350), 3.5) + rod((-175, 0, -350), (LX, 0, -330), 3.5))
# 6 Logger housing: 63 mm PVC tube with sealed end caps, hangs under the cover frame
logger = Pos(LX, 0, -210) * (Cylinder(31.5, 240) - Cylinder(27, 222))
# 7 Main board: STM32WL LoRaWAN module, 24-bit ADC, hybrid capacitor
board = Pos(LX, 0, -165) * Box(38, 8, 110)
# 8 Primary cell: Li-SOCl2 C size, 3.6 V
cell = Pos(LX - 1, 13, -265) * Cylinder(13, 50)
desiccant = Pos(LX, -12, -265) * Box(22, 10, 50)
# 9 Hanger: stainless strap hooked over the cover frame
hanger = (Pos(LX - 60, 0, -50) * Box(80, 30, 6)          # plate under the frame flange
          + Pos(LX - 97, 0, -25) * Box(6, 30, 56)          # hook over the frame
          + rod((LX - 20, 0, -53), (LX, 0, -90), 3))       # lanyard to the logger cap
# 10 Antenna: flat LoRa antenna on the hanger plate, just below the cover
antenna = Pos(LX - 50, 0, -60) * Rot(180, 0, 0) * Cylinder(35, 12)
antenna_lead = rod((LX - 30, 0, -66), (LX - 8, 0, -90), 2.5)

parts = [
    Part("Valve spindle cap (existing)", cap, "#4B5563"),
    Part("Sensor puck body", puck, "#0F766E", 1, (150, 0, 20)),
    Part("Pot magnet, 32 mm", magnet, "#B91C1C", 2, (150, 0, -40)),
    Part("Piezo disc and seismic mass", piezo, "#D4A017", 3, (150, 0, 95)),
    Part("Charge preamplifier", preamp, "#16A34A", 4, (150, 0, 135)),
    Part("Sensor cable, M12 IP68", cable, "#111827", 5, (60, 0, 0)),
    Part("Logger housing, IP68", logger, "#0E7490", 6, (-120, 0, 0)),
    Part("Main board, LoRaWAN", board, "#2563EB", 7, (110, 0, 60)),
    Part("Primary cell, Li-SOCl2 C", cell, "#C2410C", 8, (-120, 0, -170)),
    Part("Desiccant pack", desiccant, "#E5E7EB", None, (-60, 0, -170)),
    Part("Hanger strap and hook", hanger, "#A16207", 9, (-80, 0, 260)),
    Part("Flat LoRa antenna", antenna, "#7C3AED", 10, (120, 0, 200)),
    Part("Antenna lead", antenna_lead, "#111827", None, (120, 0, 200)),
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
    key_figures=["Magnet-on piezo sensor; 5 Hz to 2 kHz band (target)",
                 "Listens 02:00 to 04:00; 12 x 20 s windows a night",
                 "About 1 mAh/day; C cell life about 10 years (estimate)",
                 "One LoRaWAN summary a night; raw audio stays on device",
                 "Installed from the surface; no chamber entry",
                 "About $108 in parts (indicative)"],
    scale_figure=False, context=lifted_context,
    flow={"title": "nightly data flow per logger, kB (estimates: 240 s at 8 kS/s, 16 bit; 12 spectra of 64 bands)", "unit": "kB",
          "stages": [("Pipe vibration", "5 Hz to 2 kHz"),
                     ("Sampled audio", 3840), ("Band spectra", 1.5),
                     ("Nightly summary", 0.05), ("Trend and leak flag", "on server or TwinKit")],
          "losses": [(1, "Raw samples deleted on device", 3838)]},
)

# Hero with a plain-language note (the default note would list every context part by name)
from concept import _render  # noqa: E402
_render(parts + context, Path("media") / "hero.png", title="LeakListen",
        note="Grey figure: 1.75 m person for scale. Street, soil and valve chamber shown in section.")
