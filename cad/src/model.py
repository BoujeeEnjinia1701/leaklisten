"""LeakListen parametric model (build123d), TRL 3, massing-plus level of detail (42 mm magnet per LKL-DDR-002).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    leaklisten-assembly.step / .stl   logger, hanger, antenna, cable and sensor puck as installed
    logger.step / .stl                IP68 logger tube with end plugs, board, cell and desiccant
    sensor-puck.step / .stl           aluminium puck, pot magnet, piezo disc and mass, preamplifier

Axes: the street surface is Z = 0 and the chamber opening is centered on X = Y = 0, as in
cad/src/concept_media.py. The example site is a DN150 gate valve whose square spindle cap
top sits 480 mm below the street (PARAMS["cap_top_z"]). The logger hangs on the -X side of
the opening from a stainless strap hooked over the cover frame; the flat antenna sits just
under the cover. The sensor cable is 2 m long; the model shows only the direct run.
Main dimensions and interfaces only. Not fabrication detail; not for fabrication. The same
PARAMS feed docs/04-calcs/sizing.py (LKL-CAL-001) and drawing LKL-DWG-001 (cad/src/sheets.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site interface (existing assets, grey; not in the BOM)
    "frame_open": 600.0,            # clear opening of the cover frame
    "frame_depth": 60.0,            # frame seat depth below the street
    "cover_t": 40.0,                # cover thickness; underside at -cover_t
    "cap_top_z": -480.0,            # top of the valve spindle cap (example site)
    "cap_sq": 50.0, "cap_h": 20.0,  # square spindle cap
    # 1 sensor puck body (aluminium), 3 piezo disc and seismic mass, 4 preamplifier
    "puck_d": 40.0, "puck_h": 42.0, "puck_wall": 4.0, "puck_base": 3.0,
    "piezo_d": 27.0, "piezo_t": 0.5, "mass_d": 20.0, "mass_h": 20.0,
    "preamp": (22.0, 22.0, 1.6),
    # 2 pot magnet: 42 mm, about 600 N rated (LKL-DDR-002; was 32 mm, 290 N at TRL 3 v0.1)
    "magnet_d": 42.0, "magnet_h": 12.0, "magnet_rated_n": 600.0,
    # 5 sensor cable: 4-core shielded PUR, M12 plug at the logger end
    "cable_d": 6.0, "cable_len": 2000.0, "m12_d": 20.0, "m12_len": 45.0,
    # 6 logger housing: PVC tube with two O-ring plugs (flush, so the OD stays the tube OD)
    "tube_od": 63.0, "tube_wall": 3.0, "logger_len": 240.0, "plug_t": 18.0,
    "logger_x": -200.0, "logger_top_z": -90.0,
    # 7 main board and hybrid layer capacitor; 8 C-size cell; 11 desiccant
    "board": (38.0, 8.0, 110.0), "hlc": (16.0, 30.0),
    "cell": (26.2, 50.0),
    "desiccant": (22.0, 10.0, 50.0),
    # 9 hanger strap, 1.5 mm stainless, 30 mm wide, and lanyard
    "strap_w": 30.0, "strap_t": 1.5, "strap_run": 80.0, "hook_h": 56.0, "lanyard_d": 3.0,
    # 10 flat antenna disc and 1 m lead
    "ant_d": 70.0, "ant_t": 12.0, "ant_gap": 8.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    ri = p["tube_od"] / 2 - p["tube_wall"]
    free_len = p["logger_len"] - 2 * p["plug_t"]
    top = p["logger_top_z"]
    d = {
        "tube_id": 2 * ri,
        "free_len": free_len,
        "logger_bot_z": top - p["logger_len"],
        "logger_vol_l": math.pi * (p["tube_od"] / 2) ** 2 * p["logger_len"] / 1e6,
        "puck_bot_z": p["cap_top_z"] + p["magnet_h"],
        "puck_top_z": p["cap_top_z"] + p["magnet_h"] + p["puck_h"],
        "sensor_stack_h": p["magnet_h"] + p["puck_h"],
        "ant_z": -p["cover_t"] - p["ant_gap"] - p["ant_t"] / 2,
        "strap_len": p["strap_run"] + p["hook_h"] + 2 * p["frame_depth"],
        "board_fits": p["board"][0] <= 2 * math.sqrt(ri ** 2 - (p["board"][1] / 2) ** 2),
        "cell_fits": p["cell"][0] <= 2 * ri,
    }
    # straight-line cable run from the puck to the logger's bottom plug
    dx = p["logger_x"] - 0.0
    dz = d["logger_bot_z"] - d["puck_top_z"]
    d["cable_direct"] = math.hypot(dx, dz)
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


def path(points, r):
    return fuse(tube(a, c, r) for a, c in zip(points, points[1:]))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def zcyl(x, y, z, r, h):
    """Cylinder on a vertical axis, centered at (x, y, z)."""
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def box(x, y, z, sx, sy, sz):
    b = _b3d()
    return b.Pos(x, y, z) * b.Box(sx, sy, sz)


def build_parts(p=PARAMS):
    """Return {bom_line: solid} for BOM lines 1 to 11, in installed position."""
    D = derived(p)
    parts = {}
    # --- sensor stack on the spindle cap (axis X = Y = 0)
    zc = p["cap_top_z"]
    parts[2] = zcyl(0, 0, zc + p["magnet_h"] / 2, p["magnet_d"] / 2, p["magnet_h"])
    zb = D["puck_bot_z"]
    shell = zcyl(0, 0, zb + p["puck_h"] / 2, p["puck_d"] / 2, p["puck_h"])
    cav_h = p["puck_h"] - p["puck_base"] - 3.0              # 3 mm potted lid
    shell = shell - zcyl(0, 0, zb + p["puck_base"] + cav_h / 2, p["puck_d"] / 2 - p["puck_wall"], cav_h)
    parts[1] = shell
    zp = zb + p["puck_base"]
    parts[3] = (zcyl(0, 0, zp + p["piezo_t"] / 2, p["piezo_d"] / 2, p["piezo_t"])
                + zcyl(0, 0, zp + p["piezo_t"] + p["mass_h"] / 2, p["mass_d"] / 2, p["mass_h"]))
    px, py, pz = p["preamp"]
    parts[4] = box(0, 0, zp + p["piezo_t"] + p["mass_h"] + 6 + pz / 2, px, py, pz)
    # --- logger tube and contents (axis X = logger_x)
    lx, top, bot = p["logger_x"], p["logger_top_z"], D["logger_bot_z"]
    ro, ri = p["tube_od"] / 2, D["tube_id"] / 2
    L = p["logger_len"]
    housing = zcyl(lx, 0, (top + bot) / 2, ro, L) - zcyl(lx, 0, (top + bot) / 2, ri, L - 2 * p["plug_t"])
    housing += zcyl(lx, 0, bot - 7.5, 8.0, 15.0)            # M12 IP68 panel socket
    housing += zcyl(lx, 0, top + 6.0, 6.0, 12.0)            # antenna and lanyard gland
    parts[6] = housing
    zin_top, zin_bot = top - p["plug_t"], bot + p["plug_t"]
    bx, by, bz = p["board"]
    hd, hh = p["hlc"]
    parts[7] = (box(lx, -12.0, zin_top - 4 - bz / 2, bx, by, bz)
                + zcyl(lx - 10.0, 8.0, zin_top - 4 - hh / 2, hd / 2, hh))
    cd, ch = p["cell"]
    parts[8] = zcyl(lx + 2.0, 13.0 - 2.0, zin_bot + 4 + ch / 2, cd / 2, ch)
    dx_, dy_, dz_ = p["desiccant"]
    parts[11] = box(lx - 8.0, -12.0, zin_bot + 4 + dz_ / 2, dx_, dy_, dz_)
    # --- sensor cable: puck top to the logger's bottom socket (direct run shown), with M12 plug
    zt = D["puck_top_z"]
    r = p["cable_d"] / 2
    zs = bot - 15.0 - p["m12_len"]
    cable = path([(0, 0, zt), (0, 0, zt + 40), (-60, 0, zt + 70), (lx + 30, 0, zs - 40), (lx, 0, zs - 10), (lx, 0, zs)], r)
    cable += zcyl(lx, 0, zs + p["m12_len"] / 2, p["m12_d"] / 2, p["m12_len"])
    parts[5] = cable
    # --- hanger: plate under the frame seat, hook over the frame edge, lanyard to the top gland
    x_edge = -p["frame_open"] / 2
    zf = -p["frame_depth"]
    w, t = p["strap_w"], p["strap_t"]
    plate = box(x_edge + p["strap_run"] / 2, 0, zf + 10 - t / 2, p["strap_run"], w, t)
    hook = box(x_edge - t / 2, 0, zf + 10 + (p["hook_h"] - 10) / 2 - 5, t, w, p["hook_h"])
    lanyard = tube((x_edge + p["strap_run"] - 10, 0, zf + 10 - t), (lx, 0, top + 12.0), p["lanyard_d"] / 2)
    parts[9] = plate + hook + lanyard
    # --- flat antenna disc below the plate, lead down to the top gland
    za = D["ant_z"]
    ax = x_edge + p["strap_run"] + p["ant_d"] / 2 - 10
    antenna = zcyl(ax, 0, za, p["ant_d"] / 2, p["ant_t"])
    antenna += tube((ax - 20, 0, za - p["ant_t"] / 2), (lx + 8, 0, top + 12.0), 2.5)
    parts[10] = antenna
    return parts


def site_context(p=PARAMS):
    """Existing spindle cap and cover frame edge (grey on the drawing); not in the BOM."""
    D = derived(p)
    s = p["cap_sq"]
    cap = box(0, 0, p["cap_top_z"] - p["cap_h"] / 2, s, s, p["cap_h"])
    x_edge = -p["frame_open"] / 2
    frame = box(x_edge - 30, 0, -p["frame_depth"] / 2, 60, 120, p["frame_depth"])
    frame -= box(x_edge + 5, 0, -p["cover_t"] / 2 + 0.01, 70, 130, p["cover_t"])     # cover seat
    cover = box(x_edge + 60, 0, -p["cover_t"] / 2, 120, 120, p["cover_t"] - 0.5)
    return {"cap": cap, "frame": frame, "cover": cover, "D": D}


def assembly(p=PARAMS, with_site=False):
    b = _b3d()
    parts = build_parts(p)
    kids = [parts[k] for k in sorted(parts)]
    if with_site:
        sc = site_context(p)
        kids += [sc["cap"], sc["frame"]]
    return b.Compound(children=kids)


def logger(p=PARAMS):
    b = _b3d()
    parts = build_parts(p)
    return b.Compound(children=[parts[k] for k in (6, 7, 8, 11)])


def sensor_puck(p=PARAMS):
    b = _b3d()
    parts = build_parts(p)
    return b.Compound(children=[parts[k] for k in (1, 2, 3, 4)])


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    D = derived()
    for name, shape in (("leaklisten-assembly", assembly()), ("logger", logger()), ("sensor-puck", sensor_puck())):
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm, volume {shape.volume / 1e3:.1f} cm3")
    print(f"logger {PARAMS['tube_od']:.0f} x {PARAMS['logger_len']:.0f} mm, bore {D['tube_id']:.0f} mm, "
          f"free length {D['free_len']:.0f} mm; board fits {D['board_fits']}, cell fits {D['cell_fits']}")
    print(f"sensor stack {D['sensor_stack_h']:.0f} mm on the cap; direct cable run {D['cable_direct']:.0f} mm "
          f"of {PARAMS['cable_len']:.0f} mm")
