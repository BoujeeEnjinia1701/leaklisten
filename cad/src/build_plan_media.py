"""LeakListen prototype build plan pictures (LKL-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/LKL-DWG-101 to 109        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring (matplotlib)
Pass a single picture name (for example step-07 or LKL-DWG-104) to draw only that one.
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, site_context, zspan, boxspan  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
SC = site_context(P)
LX = P["logger_x"]
TOP, BOT = P["logger_top_z"], D["logger_bot_z"]
BZ = P["bar_z"]

COL = {"puck": "#0F766E", "magnet": "#B91C1C", "piezo": "#D4A017", "mass": "#A16207", "preamp": "#16A34A",
       "potting": "#1F2937", "cable": "#111827", "tube": "#0E7490", "plug": "#155E75", "orings": "#111827",
       "eyebolt": "#374151", "sma": "#CA8A04", "socket": "#4B5563", "chassis": "#94A3B8", "board": "#2563EB",
       "hlc": "#7C3AED", "cell": "#C2410C", "desiccant": "#E5E7EB", "outer": "#A8A29E", "inner": "#78716C",
       "feet": "#1F2937", "pin": "#DC2626", "bracket": "#57534E", "antenna": "#6D28D9", "lanyard": "#374151",
       "bolt": "#111827", "ctx": "#9CA3AF"}


def S(*keys):
    out = None
    for k in keys:
        out = C[k].shape if out is None else out + C[k].shape
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & boxspan(x0, x1, y0, y1, z0, z1)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def at_origin(shape, x=0.0, y=0.0, z=0.0):
    import build123d as b
    return b.Pos(-x, -y, -z) * shape


def lay_x(shape):
    """Turn a part that runs along Y so it runs along X (the front view then shows its length)."""
    import build123d as b
    return b.Rot(0, 0, -90) * shape


LOGGER_KEYS = ("tube", "botplug", "socket", "bot_orings", "topplug", "top_orings", "eyebolt", "sma", "lpipe", "screws_top",
               "screws_bot", "chassis", "standoffs", "board", "board_standoffs", "hlc", "desiccant", "cell")
PUCK_KEYS = ("puck", "magnet", "piezo", "mass", "preamp", "potting")
FEET_A = lambda: win(S("feet", "inserts"), -1000, 1000, -400, 0, -1000, 1000)  # noqa: E731
FEET_B = lambda: win(S("feet", "inserts"), -1000, 1000, 0, 400, -1000, 1000)  # noqa: E731


# ----------------------------------------------------------------- overview
def overview():
    parts = [
        part("Sensor puck body", S("puck"), COL["puck"], (90, 0, 0)),
        part("Seismic mass and piezo disc", S("piezo", "mass"), COL["piezo"], (90, 0, 75)),
        part("Preamplifier board", S("preamp"), COL["preamp"], (90, 0, 120)),
        part("Sensor cable with M12 plug", S("cable", "m12_plug"), COL["cable"], (0, 0, -170)),
        part("Pot magnet", S("magnet"), COL["magnet"], (90, 0, -70)),
        part("Logger tube", S("tube"), COL["tube"], (0, 0, 0)),
        part("Top end plug, eye bolt, SMA bulkhead, light pipe", S("topplug", "top_orings", "eyebolt", "sma", "lpipe", "screws_top"), COL["plug"], (0, 0, 150)),
        part("Bottom end plug and M12 socket", S("botplug", "bot_orings", "socket", "screws_bot"), COL["socket"], (0, 0, -120)),
        part("Internal chassis and standoffs", S("chassis", "standoffs", "board_standoffs"), COL["chassis"], (-170, 0, 0)),
        part("Main board and capacitor", S("board", "hlc"), COL["board"], (-170, -110, 0)),
        part("Primary cell", S("cell"), COL["cell"], (-170, 110, -20)),
        part("Desiccant pack", S("desiccant"), "#CBD5E1", (-170, 110, 60)),
        part("Neck bar, outer tube", S("bar_outer"), COL["outer"], (0, 0, 260)),
        part("Neck bar, inner tube and pin", S("bar_inner", "lockpin"), COL["inner"], (0, 120, 320)),
        part("Inserts and levelling feet", S("feet", "inserts"), COL["feet"], (0, 0, 380)),
        part("Antenna bracket and bolt", S("bracket", "bracket_bolt"), COL["bracket"], (0, 0, 440)),
        part("Flat antenna with its lead", S("antenna", "ant_nut", "ant_lead"), COL["antenna"], (100, 0, 540)),
        part("Lanyard with snap hook", S("lanyard"), COL["lanyard"], (120, 0, 120)),
    ]
    return bv.overview(parts, OUT / "overview.png", "LeakListen prototype: every component, pulled apart",
                       subtitle="Numbered in build order: sensor puck 1 to 5, logger 6 to 12, neck bar 13 to 18. Seen from the front right and above",
                       elev=20, azim=-55, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    from functools import partial
    CS = partial(bv.component_sheet, project="LeakListen", date=DATE)
    out = []
    zb = D["puck_bot_z"]
    cap = Part("Spindle cap", SC["cap"], COL["ctx"])
    jobs = []

    def job(no, fn):
        if only is None or only == no:
            jobs.append(fn)

    job("LKL-DWG-101", lambda: CS(
        Part("Sensor puck body", S("puck"), COL["puck"]), [part("p", S("magnet", "piezo", "mass", "preamp", "potting"), COL["ctx"]), cap],
        dwg_no="LKL-DWG-101", title="LeakListen sensor puck body: making sketch", material="Aluminium 6061 round bar, 45 mm",
        view_shape=at_origin(S("puck"), z=zb), inset_view=(20, -60),
        notes=["Turn from 45 mm 6061 bar: 40 mm diameter, 42 mm long.",
               "Base 8 mm thick. Centre drill and drill 5.0 mm, 8 mm deep, in the",
               "  bottom face; tap M6, 6 mm of full thread, for the magnet's stud.",
               "Lower bore 29 mm diameter, from the top of the base up 25 mm.",
               "Upper bore 32 mm diameter, from there to the top (9 mm): the",
               "  step between the bores carries the preamplifier board.",
               "Face the base inside flat and smooth (0.8 or better): the piezo",
               "  disc is bonded to it and the signal passes through it.",
               "Break all outside edges 0.5 mm. Bead blast if you can.",
               "Fit: magnet stud into the base with threadlocker; disc and mass on",
               "  the base; board on the step; potting above the board only.",
               "Check: the base face is flat; the M6 stud runs in by hand."]))

    job("LKL-DWG-102", lambda: CS(
        Part("Seismic mass", S("mass"), COL["mass"]), [part("p", win(S("puck", "preamp", "potting"), -50, 50, 0, 50, -600, 0) + S("piezo"), COL["ctx"])],
        dwg_no="LKL-DWG-102", title="LeakListen seismic mass: making sketch", material="Brass round bar CW614N, 20 mm",
        view_shape=at_origin(S("mass"), z=zb + P["puck_base"] + P["piezo_t"]), inset_view=(15, -80),
        notes=["Saw a 21 mm slice off 20 mm brass bar; face both ends to 20 mm long.",
               "The two end faces must be flat and parallel: face them in one setting",
               "  each, or lap them on fine paper on glass.",
               "Mass about 53 g; weigh it and write the figure down.",
               "Break the edges 0.3 mm; degrease with alcohol before bonding.",
               "Fit: bonded with a thin film of rigid epoxy on the brass face of the",
               "  piezo disc, centred, which is bonded to the puck base.",
               "Nothing else touches it: 4.5 mm side gap to the bore and 4.5 mm",
               "  up to the preamplifier board. No potting below the board.",
               "Check: 20 mm long, faces parallel within 0.05 mm."]))

    job("LKL-DWG-103", lambda: CS(
        Part("Logger tube", S("tube"), COL["tube"]), [part("p", S("topplug", "botplug", "eyebolt", "socket"), COL["ctx"])],
        dwg_no="LKL-DWG-103", title="LeakListen logger tube: making sketch", material="PVC pressure pipe 63 mm OD, 3 mm wall",
        view_shape=at_origin(S("tube"), x=LX, z=BOT + P["plug_flange"]), inset_view=(20, -60),
        notes=["Cut 232 mm off 63 x 3 mm PVC pressure pipe with a fine saw in a",
               "  mitre box; square the ends by sanding on a flat board.",
               "Chamfer the inside of both ends 1 mm x 30 degrees so the O-rings",
               "  slide in without cutting. Deburr inside and out.",
               "Six 4.5 mm screw holes, 4 mm from each end: three at each end,",
               "  120 degrees apart. Mark them with a paper wrap round the tube.",
               "Drill the holes with the plug fitted, so the plug can be drilled",
               "  3.3 mm and tapped M4 through the same holes (see the plugs).",
               "Fit: plug spigots slide in until the flanges sit on the tube ends;",
               "  both O-rings on each plug are inside, beyond the screws.",
               "Check: the ends are square; no scratches along the bore",
               "  in the 25 mm at each end where the O-rings seal."]))

    job("LKL-DWG-104", lambda: CS(
        Part("Top end plug", S("topplug"), COL["plug"]), [part("p", S("tube", "eyebolt", "sma", "lpipe", "standoffs", "chassis"), COL["ctx"])],
        dwg_no="LKL-DWG-104", title="LeakListen top end plug: making sketch", material="Acetal (POM) round bar, 65 mm",
        rev="P2", date="2026-10-02",
        revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC"),
                   ("P2", "Light pipe hole added (decision of 2026-10-02)", "2026-10-02", "AC")],
        view_shape=at_origin(S("topplug"), x=LX, z=TOP - 22), inset_view=(25, -60),
        notes=["Turn from 65 mm acetal bar: flange 63 mm diameter, 4 mm thick;",
               "  spigot 57 mm diameter (a light push fit in the tube), 18 mm long.",
               "Two O-ring grooves in the spigot, 2.5 mm wide, 1.8 mm deep, centred",
               "  10 and 15 mm below the flange, for 2.5 mm section O-rings.",
               "Eye bolt hole 6.5 mm on the axis, right through.",
               "SMA bulkhead hole 6.5 mm, 14 mm from the axis, right through;",
               "  check the size against the bulkhead's datasheet.",
               "Light pipe hole 3.0 mm, right through, 13 mm from the axis on the side",
               "  away from the SMA and 10 mm toward the right-hand standoff in the top view.",
               "Inner face: two M3 tapped holes 6 mm deep for the standoffs,",
               "  18 mm each side of the axis, 6 mm toward the side away from the SMA.",
               "Radial holes: drill 3.3 mm, tap M4, through the tube's holes,",
               "  4 mm below the flange, 120 degrees apart (one away from the SMA).",
               "Check: the plug pushes in by hand with O-rings greased."]))

    job("LKL-DWG-105", lambda: CS(
        Part("Bottom end plug", S("botplug"), COL["socket"]), [part("p", S("tube", "socket", "cell", "chassis"), COL["ctx"])],
        dwg_no="LKL-DWG-105", title="LeakListen bottom end plug: making sketch", material="Acetal (POM) round bar, 65 mm",
        view_shape=at_origin(S("botplug"), x=LX, z=BOT), inset_view=(-20, -60),
        notes=["Turn as the top plug: flange 63 mm x 4 mm, spigot 57 mm x 18 mm,",
               "  two O-ring grooves 2.5 x 1.8 mm, 10 and 15 mm above the flange.",
               "Centre hole: drill 14.5 mm and tap M16 x 1.5 right through, for",
               "  the front-mount M12 panel socket (check its thread first).",
               "Face the outside of the flange flat where the socket's O-ring sits.",
               "Radial holes: drill 3.3 mm, tap M4, through the tube's holes,",
               "  4 mm above the flange, 120 degrees apart.",
               "Fit: the socket screws in from outside with its O-ring under its",
               "  flange; its lock nut and the board lead are inside.",
               "Check: the socket seats flat; the plug pushes in by hand."]))

    job("LKL-DWG-106", lambda: CS(
        Part("Internal chassis", S("chassis"), COL["chassis"]), [part("p", S("topplug", "standoffs", "board", "cell", "hlc", "desiccant"), COL["ctx"])],
        dwg_no="LKL-DWG-106", title="LeakListen internal chassis: making sketch", material="PETG, 3D printed, 40 % infill",
        view_shape=at_origin(S("chassis"), x=LX, z=BOT + 40), inset_view=(20, 30),
        notes=["Print lying on its board face, with support under the 6 mm of the",
               "  top tab that stands out on that side. Spine 48 x 3 x 158 mm.",
               "Top tab 48 x 18 x 4 mm across the top of the spine, with two 3.2 mm",
               "  holes 18 mm each side of centre, 6 mm out on the board side:",
               "  M3 screws up through these (before the board goes on) into",
               "  the two M3 x 20 standoffs that hang it from the top plug.",
               "Clip face (dashed in the front view), from the top: two clips for",
               "  the 16 mm capacitor, 8 and 30 mm down; a 22 x 10 x 50 mm pocket",
               "  for the desiccant,",
               "  open at the top; at the bottom, two clips for the C cell, 10 and",
               "  40 mm up from the bottom edge. Clips wrap about 200 degrees.",
               "Board face: four 2.5 mm pilot holes for the board standoffs,",
               "  30 mm apart across and 100 mm apart down.",
               "Fit: the cell and capacitor snap into their clips.",
               "Check: it slides into the tube with 2.5 mm to spare all round."]))

    job("LKL-DWG-107", lambda: CS(
        Part("Neck bar, outer tube", S("bar_outer"), COL["outer"]), [part("p", S("bar_inner", "feet", "inserts", "bracket", "lockpin"), COL["ctx"])],
        dwg_no="LKL-DWG-107", title="LeakListen neck bar outer tube: making sketch", material="Aluminium square tube 20 x 20 x 1.5 mm, 6063",
        view_shape=lay_x(at_origin(S("bar_outer"), x=LX, y=P["bar_out_y0"], z=BZ)), inset_view=(25, -40),
        notes=["Cut 350 mm of 20 x 20 x 1.5 mm square tube; square and deburr.",
               "Measure from the foot end (the end that takes the fixed foot):",
               "  bracket bolt hole 5.5 mm at 130 mm, top and bottom walls;",
               "  locking pin hole 6.5 mm at 320 mm, top and bottom walls.",
               "Drill each pair straight through both walls in a drill stand so",
               "  the holes line up.",
               "Press a 20 x 20 tube insert with an M10 nut into the foot end.",
               "Fit: the inner tube slides into the other end with 0.5 mm",
               "  clearance; the pin goes through both tubes.",
               "Check: the inner tube slides the full length without binding."]))

    job("LKL-DWG-108", lambda: CS(
        Part("Neck bar, inner tube", S("bar_inner"), COL["inner"]), [part("p", S("bar_outer", "feet", "inserts", "lockpin"), COL["ctx"])],
        dwg_no="LKL-DWG-108", title="LeakListen neck bar inner tube: making sketch", material="Aluminium square tube 16 x 16 x 1.5 mm, 6063",
        view_shape=lay_x(at_origin(S("bar_inner"), x=LX, y=P["bar_in_y0"], z=BZ)), inset_view=(25, -40),
        notes=["Cut 350 mm of 16 x 16 x 1.5 mm square tube; square and deburr.",
               "Seven locking pin holes, 6.5 mm, through the top and bottom walls,",
               "  20 mm apart, the first 20 mm from the plain end (20 to 140 mm).",
               "Press a 16 x 16 tube insert with an M10 nut into the far end.",
               "Fit: slide into the outer tube; choose the hole that sets the bar",
               "  about 20 mm short of the neck width, fit the pin and R-clip,",
               "  then wind the feet out to take up the last 20 mm.",
               "With the 7 holes and about 30 mm of foot travel the bar spans",
               "  necks of about 570 to 710 mm (600 mm as drawn, hole 6 of 7).",
               "Check: the pin drops through both tubes at every hole."]))

    job("LKL-DWG-109", lambda: CS(
        Part("Antenna bracket", S("bracket"), COL["bracket"]), [part("p", S("bar_outer", "antenna", "bracket_bolt", "ant_nut"), COL["ctx"])],
        dwg_no="LKL-DWG-109", title="LeakListen antenna bracket: making sketch", material="Aluminium flat bar 40 x 3 mm, 6082",
        view_shape=at_origin(S("bracket"), x=LX, y=P["ant_y"], z=D["bar_top"]), inset_view=(30, -50),
        notes=["Cut 100 mm of 40 x 3 mm flat bar; round the corners 3 mm, deburr.",
               "On the centre line: bolt hole 5.5 mm, 15 mm from one end;",
               "  antenna stud hole 60 mm from the same end, sized to the antenna's",
               "  stud (16.5 mm for an M16 stud; check its datasheet).",
               "Fit: the bracket lies flat across the top of the outer tube, the",
               "  bolt hole over the tube; one M5 x 30 bolt through bracket and",
               "  tube, nyloc nut under the tube.",
               "The antenna sits on top, its stud through the large hole, nut",
               "  underneath; the antenna is 45 mm off the bar's centre line.",
               "Check: the antenna sits flat and the bracket cannot turn when",
               "  the bolt is tight (bracket edge against your thumb)."]))

    for j in jobs:
        out.append(j())
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []
    zb, zt = D["puck_bot_z"], D["puck_top_z"]
    J = {}
    J[1] = lambda: bv.joint([
        part("Spindle cap (existing)", win(SC["cap"], -40, 40, -40, 40, -500, -470), COL["ctx"]),
        part("Pot magnet and its M6 stud", S("magnet"), COL["magnet"]),
        part("Puck body (base tapped M6)", S("puck"), COL["puck"]),
        part("Piezo disc, bonded to the base", S("piezo"), COL["piezo"]),
        part("Seismic mass, bonded to the disc", S("mass"), COL["mass"]),
        part("Preamplifier board on the step", S("preamp"), COL["preamp"]),
        part("Potting, above the board only", S("potting"), "#475569"),
        part("Sensor cable", win(S("cable"), -30, 30, -30, 30, zb, zt + 25), COL["cable"])],
        OUT / "joint-01.png", "Joint 1: inside the sensor puck (cut in half)",
        subtitle="Only the base touches the disc; the mass stands free with 4.5 mm round it and above it",
        cut="+Y", elev=8, azim=-90, size=(8, 6.5))
    J[2] = lambda: bv.joint([
        part("Logger tube", win(S("tube"), LX - 40, LX + 40, -40, 40, TOP - 40, TOP), COL["tube"]),
        part("Top end plug", S("topplug"), COL["plug"]),
        part("O-rings (2)", S("top_orings"), COL["orings"]),
        part("Radial M4 screw", S("screws_top"), COL["bolt"]),
        part("M6 eye bolt", win(S("eyebolt"), LX - 40, LX + 40, -40, 40, TOP - 40, TOP + 40), COL["eyebolt"]),
        part("Standoff (to the chassis)", win(S("standoffs"), LX - 40, LX + 40, -40, 40, TOP - 40, TOP), COL["chassis"])],
        OUT / "joint-02.png", "Joint 2: top end plug in the tube (cut in half)",
        subtitle="Cut through the axis and one radial screw. The screw sits 4 mm in from the tube end, outboard of both O-rings",
        cut="+X", elev=12, azim=180, size=(8, 6.5))
    J[3] = lambda: bv.joint([
        part("Logger tube", win(S("tube"), LX - 40, LX + 40, -40, 40, BOT, BOT + 40), COL["tube"]),
        part("Bottom end plug", S("botplug"), COL["socket"]),
        part("O-rings (2)", S("bot_orings"), COL["orings"]),
        part("Radial M4 screw", S("screws_bot"), COL["bolt"]),
        part("M12 panel socket", S("socket"), "#D4A017"),
        part("Cable's M12 plug", win(S("m12_plug"), LX - 30, LX + 30, -30, 30, BOT - 40, BOT), COL["cable"])],
        OUT / "joint-03.png", "Joint 3: bottom end plug and M12 socket (cut in half)",
        subtitle="Cut through the axis and one radial screw. The socket screws in from outside; the cable plug screws onto it",
        cut="+X", elev=12, azim=180, size=(8, 6.5))
    J[4] = lambda: bv.joint([
        part("Internal chassis", S("chassis"), COL["chassis"]),
        part("Capacitor in two clips", S("hlc"), COL["hlc"]),
        part("Desiccant in its pocket", S("desiccant"), "#65A30D"),
        part("C cell in two clips", S("cell"), COL["cell"]),
        part("Standoffs (to the top plug)", S("standoffs"), COL["bolt"])],
        OUT / "joint-04.png", "Joint 4: cell, capacitor and desiccant on the chassis",
        subtitle="Seen from the front of the chassis (the side away from the board). The clips wrap about 200 degrees",
        elev=35, azim=100, size=(8, 6.5))
    yo = P["pin_y"]
    J[5] = lambda: bv.joint([
        part("Outer tube", win(S("bar_outer"), LX - 30, LX + 30, -40, 75, BZ - 30, BZ + 30), COL["outer"]),
        part("Inner tube", win(S("bar_inner"), LX - 30, LX + 30, -40, 110, BZ - 30, BZ + 30), "#475569"),
        part("Locking pin and R-clip", S("lockpin"), COL["pin"])],
        OUT / "joint-05.png", "Joint 5: neck bar, inner tube in the outer tube (cut in half)",
        subtitle="Cut along the bar and seen from the cut side. 0.5 mm sliding clearance; the pin passes through both tubes",
        cut="+X", elev=20, azim=200, size=(8, 6))
    J[6] = lambda: bv.joint([
        part("Chamber neck wall (existing)", win(SC["neck"], LX - 45, LX + 45, -316, -300, BZ - 45, BZ + 25), COL["ctx"]),
        part("Rubber pad on the M10 foot", win(S("feet"), LX, LX + 30, -310, -265, BZ - 30, BZ + 30), COL["feet"]),
        part("Tube insert with M10 nut", win(S("inserts"), LX, LX + 30, -310, -230, BZ - 30, BZ + 30), "#D4A017"),
        part("Outer tube", win(S("bar_outer"), LX, LX + 30, -300, -200, BZ - 30, BZ + 30), COL["outer"])],
        OUT / "joint-06.png", "Joint 6: fixed foot against the neck wall (bar cut in half)",
        subtitle="The foot screws into the insert in the tube end; at the other end the same foot is wound out to wedge the bar",
        elev=20, azim=140, size=(8, 6))
    ay = P["ant_y"]
    J[7] = lambda: bv.joint([
        part("Outer tube", win(S("bar_outer"), LX - 30, LX + 30, ay - 50, ay + 50, BZ - 30, BZ + 30), COL["outer"]),
        part("Antenna bracket", S("bracket"), COL["bracket"]),
        part("M5 bolt and nyloc nut", S("bracket_bolt"), COL["bolt"]),
        part("Flat antenna", S("antenna"), COL["antenna"]),
        part("Antenna stud nut", S("ant_nut"), "#111827")],
        OUT / "joint-07.png", "Joint 7: antenna bracket on the neck bar",
        subtitle="Seen from below and to the side. One bolt through the tube; the antenna stud nut is clear of the tube",
        elev=-25, azim=-60, size=(8, 6))
    J[8] = lambda: bv.joint([
        part("Outer tube", win(S("bar_outer"), LX - 30, LX + 30, -35, 35, BZ - 30, BZ + 30), COL["outer"]),
        part("Wire rope loop and snap hook", S("lanyard"), COL["lanyard"]),
        part("M6 eye bolt", S("eyebolt"), COL["eyebolt"]),
        part("Top end plug", win(S("topplug", "tube"), LX - 40, LX + 40, -40, 40, TOP - 25, TOP), COL["plug"]),
        part("SMA bulkhead and antenna lead", S("sma") + win(S("ant_lead"), LX - 40, LX + 60, -20, 40, TOP, TOP + 40), COL["sma"]),
        part("Status light pipe rod", win(S("lpipe"), LX - 40, LX + 40, -40, 40, TOP - 25, TOP), "#38BDF8")],
        OUT / "joint-08.png", "Joint 8: lanyard from the neck bar to the eye bolt",
        subtitle="The loop goes round the bar; the snap hook clips into the eye. The antenna lead plugs into the SMA bulkhead; the light pipe rod sits flush in the plug",
        elev=15, azim=-35, size=(8, 6.5))
    for n, fn in J.items():
        if only is None or only == f"joint-{n:02d}":
            out.append(fn())
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []
    zt = D["puck_top_z"]

    def st(n, done, new, title, sub, **kw):
        if only is None or only == f"step-{n:02d}":
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    puck = part("Puck body", S("puck"), COL["puck"])
    st(1, [puck], [mv(part("Piezo disc", S("piezo"), COL["piezo"]), (0, 0, 60)),
                   mv(part("Seismic mass", S("mass"), COL["mass"]), (0, 0, 110))],
       "piezo disc and seismic mass into the puck",
       "Thin film of rigid epoxy under the disc and under the mass, both centred; cure flat for 24 hours",
       elev=30, azim=-60)
    inner = [puck, part("Disc and mass", S("piezo", "mass"), COL["piezo"])]
    cable_end = win(S("cable"), -40, 40, -40, 40, zt - 20, zt + 30)
    st(2, inner, [mv(part("Preamplifier board", S("preamp"), COL["preamp"]), (0, 0, 60)),
                  mv(part("Cable end, soldered to the board", cable_end, COL["cable"]), (0, 0, 110))],
       "preamplifier board and cable",
       "Solder the disc leads and the cable to the board first, then lay the board on the step",
       elev=30, azim=-60, label_done=False)
    inner2 = inner + [part("Board", S("preamp"), COL["preamp"]), part("Cable", cable_end, COL["cable"])]
    st(3, inner2, [mv(part("Potting compound", S("potting"), "#475569"), (0, 0, 50))],
       "pot the top of the puck",
       "Pour to the rim, above the board only; nothing may run below the board onto the mass",
       elev=30, azim=-60, label_done=False)
    done_puck = inner2 + [part("Potting", S("potting"), "#475569")]
    st(4, done_puck, [mv(part("Pot magnet (keeper plate on)", S("magnet"), COL["magnet"]), (0, 0, -60))],
       "pot magnet onto the puck",
       "Medium threadlocker on the stud; screw in hand tight. Keep the keeper plate on",
       elev=-15, azim=-60, label_done=False)
    st(5, [part("Top end plug", S("topplug"), COL["plug"])],
       [mv(part("M6 eye bolt", S("eyebolt"), COL["eyebolt"]), (0, 0, 70)),
        mv(part("SMA bulkhead", S("sma"), COL["sma"]), (0, 0, 70)),
        mv(part("Light pipe rod", S("lpipe"), "#38BDF8"), (0, 0, 70)),
        mv(part("Standoffs (2)", S("standoffs"), COL["bolt"]), (0, 0, -50)),
        mv(part("O-rings (2), greased", S("top_orings"), COL["orings"]), (0, 0, -30))],
       "fit the top end plug",
       "Eye bolt with its sealing washer, nyloc nut inside; SMA bulkhead with its O-ring; light pipe rod glued in flush; standoffs into the inner face",
       elev=20, azim=-60, label_done=False)
    st(6, [part("Bottom end plug", S("botplug"), COL["socket"])],
       [mv(part("M12 panel socket", S("socket"), "#D4A017"), (0, 0, -60)),
        mv(part("O-rings (2), greased", S("bot_orings"), COL["orings"]), (0, 0, 40))],
       "fit the bottom end plug",
       "Socket in from outside with its O-ring, lock nut inside; O-rings in both grooves",
       elev=20, azim=-60, label_done=False)
    topset = [part("Top end plug with fittings", S("topplug", "eyebolt", "sma", "lpipe", "top_orings"), COL["plug"])]
    st(7, topset, [mv(part("Internal chassis and standoffs", S("chassis", "standoffs"), COL["chassis"]), (0, 0, -80))],
       "chassis onto the top plug",
       "Two M3 screws up through the chassis tab into the standoffs, before anything else goes on the chassis",
       elev=15, azim=-60, label_done=False)
    hung = topset + [part("Chassis", S("chassis", "standoffs"), COL["chassis"])]
    st(8, hung, [mv(part("Main board on four standoffs", S("board", "board_standoffs"), COL["board"]), (0, -70, 0)),
                 mv(part("Capacitor", S("hlc"), COL["hlc"]), (0, 60, 0)),
                 mv(part("Desiccant pack", S("desiccant"), "#65A30D"), (0, 130, 30)),
                 mv(part("C cell (fit last)", S("cell"), COL["cell"]), (0, 70, 0))],
       "electronics onto the chassis",
       "Board on the board face; capacitor, desiccant and cell into their clips; SMA pigtail to the board (stop point S2)",
       elev=15, azim=-60, label_done=False)
    st(9, [part("Logger tube", S("tube"), COL["tube"])],
       [mv(part("Bottom plug with socket", S("botplug", "socket", "bot_orings"), COL["socket"]), (0, 0, -80)),
        mv(part("Radial M4 screws (3)", S("screws_bot"), COL["bolt"]), (0, 0, -80))],
       "bottom plug into the tube",
       "Push in until the flange meets the tube end; three M4 screws through the tube into the plug",
       elev=15, azim=-60, label_done=False)
    st(10, [part("Tube with bottom plug", S("tube", "botplug", "socket", "bot_orings", "screws_bot"), COL["tube"])],
       [mv(part("Top plug with chassis", S("topplug", "eyebolt", "sma", "lpipe", "top_orings", "standoffs", "chassis", "board",
                                            "board_standoffs", "hlc", "desiccant", "cell"), COL["plug"]), (0, 0, 220)),
        mv(part("Radial M4 screws (3)", S("screws_top"), COL["bolt"]), (0, 0, 220))],
       "close the logger",
       "Plug in the socket lead, slide the chassis in, push the plug home; three M4 screws (stop point S3)",
       elev=15, azim=-60, label_done=False)
    st(11, [part("Outer tube", S("bar_outer"), COL["outer"])],
       [mv(part("Inner tube", S("bar_inner"), COL["inner"]), (0, 160, 0)),
        mv(part("Locking pin", S("lockpin"), COL["pin"]), (0, 0, 50)),
        mv(part("Fixed foot and insert", FEET_A(), COL["feet"]), (0, -60, 0)),
        mv(part("Adjusting foot and insert", FEET_B(), COL["feet"]), (0, 220, 0))],
       "assemble the neck bar",
       "Slide the inner tube in, pin it at the hole that suits the neck, screw both feet into the inserts",
       elev=25, azim=-40, label_done=False)
    bar = [part("Neck bar", S("bar_outer", "bar_inner", "lockpin", "feet", "inserts"), COL["outer"])]
    st(12, bar, [mv(part("Antenna bracket and M5 bolt", S("bracket", "bracket_bolt"), COL["bracket"]), (0, 0, 50)),
                 mv(part("Flat antenna and stud nut", S("antenna", "ant_nut"), COL["antenna"]), (0, 0, 110))],
       "antenna bracket and antenna onto the bar",
       "Bolt the bracket across the outer tube; antenna stud through the bracket, nut underneath",
       elev=25, azim=-40, label_done=False)
    bar2 = bar + [part("Bracket and antenna", S("bracket", "bracket_bolt", "antenna", "ant_nut"), COL["antenna"])]
    logger = part("Logger", S(*LOGGER_KEYS), COL["tube"])
    st(13, bar2, [mv(part("Lanyard", S("lanyard"), COL["lanyard"]), (60, 0, 0)), mv(logger, (0, 0, -100)),
                  mv(part("Antenna lead", S("ant_lead"), COL["antenna"]), (90, 0, 0))],
       "hang the logger and connect the antenna",
       "Loop the lanyard round the bar, clip the snap hook into the eye bolt, screw the lead onto the SMA bulkhead",
       elev=20, azim=-40, label_done=False)
    walls = win(SC["neck"], LX - 60, LX + 60, -360, 360, P["neck_bot"], -P["frame_depth"])
    up = (0, 0, 110)
    st(14, [part("Chamber neck walls (existing)", walls, COL["ctx"])],
       [mv(part("Neck bar", S("bar_outer", "bar_inner", "lockpin", "feet", "inserts", "bracket", "bracket_bolt", "lanyard"), COL["outer"]), up),
        mv(part("Antenna", S("antenna", "ant_nut", "ant_lead"), COL["antenna"]), up),
        mv(part("Logger", S(*LOGGER_KEYS), COL["tube"]), up)],
       "set the bar in the chamber neck",
       "From the surface: lower the set below the frame, fixed pad on one wall, wind the other foot out hand tight",
       elev=22, azim=-35, label_done=True)
    done_all = [part("Neck bar and logger", S("bar_outer", "bar_inner", "feet", "inserts", "bracket", "antenna", "lanyard", *LOGGER_KEYS), COL["outer"])]
    st(15, done_all, [mv(part("Sensor puck and magnet", S(*PUCK_KEYS), COL["puck"]), (0, 0, 150)),
                      mv(part("Sensor cable and M12 plug", S("cable", "m12_plug"), COL["cable"]), (0, 0, 150))],
       "sensor puck onto the spindle cap",
       "Keeper plate off at the cap; lower the puck onto the cap; screw the M12 plug onto the logger's socket",
       context=[part("Spindle cap (existing)", SC["cap"], COL["ctx"])], elev=22, azim=-35, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 6.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 66); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 64, "LeakListen prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 60.6, "No circuit board is laid out at this stage; the main board is bought or built on a carrier. Stranded copper; "
            "every joint soldered and sleeved.", fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/leaklisten", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color, fc="white"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc=fc, ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, RF = "#B91C1C", "#1D4ED8", "#6B7280", "#6D28D9"
    # sensor puck
    ax.add_patch(FancyBboxPatch((3, 10), 24, 41, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(4.5, 50.6, "In the sensor puck (potted)", fontsize=8, color=MUT, va="top")
    blk(6, 33, 18, 12, "Piezo disc", "under the 53 g mass;\ntwo leads, 0.25 mm²", "#D4A017")
    blk(6, 15, 18, 12, "Preamplifier board", "charge stage and 40 dB;\nround, 31 mm", "#16A34A")
    wire([(15, 33), (15, 27)], GRY, 1.2); lab(15.6, 30, "disc leads, short, twisted", GRY)
    # cable
    wire([(24, 21), (42, 21)], INK, 3.0); lab(32.6, 24.2, "2 m sensor cable", INK, "center")
    lab(32.6, 17.0, "4 cores and shield:\nsupply, ground,\nsignal, spare", MUT, "center")
    # logger
    ax.add_patch(FancyBboxPatch((40, 8.5), 77, 45.5, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(41.5, 52.8, "In the logger", fontsize=8, color=MUT, va="top")
    blk(43, 15, 12, 12, "M12 socket", "in the bottom\nplug", "#4B5563")
    blk(64, 13, 28, 32, "Main board", "STM32WL LoRaWAN module,\n24-bit audio ADC, clock,\nfuse and reverse\nprotection, status LED\n(light pipe to the\ntop plug)", "#2563EB")
    blk(100, 39, 15, 10, "SMA bulkhead", "in the top plug;\nlead outside", RF)
    blk(100, 26, 15, 9, "Capacitor", "about 0.1 F", "#7C3AED")
    blk(100, 11, 15, 11, "C cell", "Li-SOCl2, 3.6 V;\n2-pin plug", "#C2410C")
    wire([(55.3, 21), (64, 21)], INK, 2.0); lab(59.6, 23.4, "4-pin lead", INK, "center")
    wire([(92.3, 44), (99.7, 44)], RF, 1.4); lab(96, 46.4, "u.FL pigtail", RF, "center")
    wire([(99.7, 30.5), (92.3, 30.5)], RED); lab(96, 32.9, "0.5 mm²", RED, "center")
    wire([(99.7, 16.5), (92.3, 16.5)], RED); lab(96, 18.9, "0.5 mm²", RED, "center")
    ax.text(3, 6.2, "Safety: the cell stays unplugged until stop point S2. Never charge a lithium thionyl chloride cell;",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 4.0, "the board's fuse and reverse protection come before everything else on the cell lead.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(2, 57.6, "Red: power. Purple: radio. Grey: sensor signal. Black: sensor cable and its lead.", fontsize=7.6, color=MUT, va="top")
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "wiring"]
    for a in args:
        if a == "overview":
            print(overview())
        elif a == "wiring":
            print(wiring())
        elif a == "sheets":
            print(sheets())
        elif a == "joints":
            print(joints())
        elif a == "steps":
            print(steps())
        elif a.startswith("LKL-DWG-"):
            print(sheets(a))
        elif a.startswith("joint-"):
            print(joints(a))
        elif a.startswith("step-"):
            print(steps(a))
