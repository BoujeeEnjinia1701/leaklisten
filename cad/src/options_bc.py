"""LeakListen concept options B and C as detailed parts (kit 1.9, D3), beside option A in model.py.

Option B, hydrant cap hydrophone: a stainless blind cap bolted to a hydrant outlet flange carries a hydrophone in the
water column; the logger lies in two omega clips on the cap; a mast carries the flat antenna to 20 mm under the cover.
Option C, ground spike geophone: a stainless spike in the verge carries a geophone to 0.5 m depth; the logger stands in
a flush HDPE ground box with its antenna under the lid.
Both use the logger electronics of option A (lkl_logger.logger_parts). Dimensions below are first-order estimates for
the concept comparison, not design values; the hydrant outlet and the soil are assumed, to assess with a partner utility.
"""
from __future__ import annotations

import math

import build123d as b
import cad_parts as cp
import lkl_logger as LG
from lkl_parts import (mk, fuse, tube, path, smooth, zspan, box, boxspan, hexprism, ring, put, pan_screw, socket_screw,
                       washer_od, oring_installed, xcyl)

LOC = b.Location
PL = b.Plane


def frame(origin, x_dir, z_dir):
    return LOC(PL(origin=origin, x_dir=x_dir, z_dir=z_dir))


def gpt(fr, x, y, z):
    """Global point of a local point under Location fr."""
    return (fr * b.Pos(x, y, z)).position


def moved(parts, fr, tag=""):
    """Move a list of part dicts (built in a local frame) by a Location."""
    out = []
    for q in parts:
        r = dict(q)
        r["shape"] = fr * q["shape"]
        out.append(r)
    return out


def local_p(p):
    """PARAMS for building the logger in its own frame: axis through the origin, top flange at z = 0."""
    q = dict(p)
    q["logger_x"], q["logger_top_z"] = 0.0, 0.0
    return q


def plug_local(p, D):
    """M12 plug overmould and coupling nut on the logger socket in the local logger frame, and the z of the plug's end."""
    bot = -p["logger_len"]
    z_nut_top = bot - 5.0
    zs_bot = z_nut_top - p["m12_len"]
    body = cp.break_edges(zspan(0, 0, zs_bot, z_nut_top - 17.0, p["m12_d"] / 2 - 2.0), 3.0)
    nut = ring(0, 0, z_nut_top - 17.0, z_nut_top, 6.0, p["m12_d"] / 2)
    for k in range(18):
        a = 2 * math.pi * k / 18
        nut = nut - zspan(math.cos(a) * p["m12_d"] / 2, math.sin(a) * p["m12_d"] / 2, z_nut_top - 15.5, z_nut_top - 1.5, 0.9)
    return [mk("m12_plug", "M12 plug overmould", body, "pu_black", "bought", 5),
            mk("m12_plug", "M12 coupling nut, knurled", cp.break_edges(nut, 0.4), "stainless", "bought", 5)], zs_bot


def sma_plug_local(p):
    top = 0.0
    sma_y = 14.0
    plug = ring(0, sma_y, top + 4.5, top + 15, 3.175, 4.5) + zspan(0, sma_y, top + 15, top + 16, 4.5) + zspan(0, sma_y, top + 16, top + 27, 2.5)
    return cp.break_edges(plug, 0.3)


def omega_clip(R, width, tag, z_at):
    """Omega pipe clip in a local frame: tube axis along Z through the origin, base plane at x = -R - 1 (feet),
    band over the +X side. Returns (clip shape, [(y, x) screw centres])."""
    t = 1.0
    z0, z1 = z_at - width / 2, z_at + width / 2
    arc = ring(0, 0, z0, z1, R, R + t) & boxspan(0, R + 2, -R - 2, R + 2, z0, z1)
    walls = [boxspan(-R, 0, s * R, s * (R + t) if s > 0 else s * (R + t), z0, z1) for s in (1, -1)]
    feet = [boxspan(-R - t, -R, (R + t) if s > 0 else -(R + t + 14), (R + t + 14) if s > 0 else -(R + t), z0, z1) for s in (1, -1)]
    shp = arc
    for w in walls + feet:
        shp = shp + w
    sc = []
    for s in (1, -1):
        yc = s * (R + t + 7.5)
        shp = shp - b.Pos(-R - t / 2, yc, z_at) * b.Rot(0, 90, 0) * b.Cylinder(2.75, 3.0)
        sc.append(yc)
    return shp, sc


def clip_set(p, fr, z_list, base_cuts, L=12):
    """Omega clips on the logger (local frame fr maps local x to 'away from the base'); returns parts and the cutters
    (tapped holes) for the base part, in global coordinates."""
    R = p["tube_od"] / 2
    out, cuts = [], []
    for i, zc in enumerate(z_list):
        shp, ys = omega_clip(R, 20.0, i, zc)
        out.append(mk("clip", f"Omega clip 63 mm, stainless band {i + 1}", fr * cp.break_edges(shp, 0.2), "stainless", "bought", 6))
        for j, yc in enumerate(ys):
            scr = pan_screw(5, L, 9.0, 3.3)
            sh = fr * b.Pos(-R, yc, zc) * b.Rot(0, 90, 0) * scr
            out.append(mk("clip_screw", f"M5x{L} pan head screw, clip {i + 1} foot {j + 1}", sh, "stainless", "fastener", 6))
            cuts.append(fr * b.Pos(-R - 1.0 - (L - 1.0) / 2 - 0.2, yc, zc) * b.Rot(0, 90, 0) * b.Cylinder(2.6, L - 1.0 + 0.4))
    return out, cuts


def antenna_stack(p, back=15.0):
    """Flat antenna on a 100 x 40 x 3 bracket lying on a horizontal surface at z = 0 (local), M5 bolt at the local origin,
    antenna centre 45 mm along +X. Returns parts and the local point of the antenna stud's bottom."""
    bw_, bt_, bl_ = p["ant_bracket"]
    axx = p["ant_off"]
    cx = -back + bl_ / 2
    br = cp.sheet(bl_, bw_, bt_, holes=[(0 - cx, 0, 5.5), (axx - cx, 0, 16.0)], r_corner=4.0, edge=0.5)
    parts = [mk("bracket", "Antenna bracket, 40 x 3 aluminium flat", b.Pos(cx, 0, 0) * br, "aluminium", "made", 9)]
    body = b.Pos(axx, 0, bt_ + p["ant_t"] / 2) * b.Cylinder(p["ant_d"] / 2, p["ant_t"])
    ant = cp.break_edges(body, 2.0) + zspan(axx, 0, -11, bt_, 8.0)
    parts.append(mk("antenna", "Flat LoRa antenna with centre stud", ant, "antenna_white", "bought", 10))
    parts.append(mk("ant_nut", "Antenna stud nut", hexprism(axx, 0, -6, 0, 24.0) - zspan(axx, 0, -7, 1, 8.0), "stainless", "fastener", 10))
    return parts, (axx, 0.0, -11.0)


# ======================================================================================================== option B
PB = {"flange_r": 105.0, "flange_t": 16.0, "stub_r": 45.0, "stub_ri": 32.0, "stub_len": 180.0,
      "z_flange_top": -320.0, "gasket_t": 3.0, "cap_t": 16.0, "pcd": 170.0, "bolt_d": 12,
      "sleeve_ro": 10.0, "sleeve_ri": 6.0, "collar_r": 14.0, "tip_len": 40.0,
      "logger_x": 52.0, "clip_y": (-35.0, 35.0), "mast_x": -60.0, "mast_side": 20.0, "mast_wall": 1.5}


def components_B(p):
    D = {}
    zf = PB["z_flange_top"]
    ff = zf - PB["flange_t"]
    cap_bot = zf + PB["gasket_t"]
    cap_top = cap_bot + PB["cap_t"]
    rf = PB["flange_r"]
    r_pcd = PB["pcd"] / 2
    bpos = [(r_pcd * math.cos(math.radians(a)), r_pcd * math.sin(math.radians(a))) for a in (45, 135, 225, 315)]
    out = []
    add = lambda *a, **k: out.append(mk(*a, **k))

    # ---- existing hydrant outlet (context): flange with four M12 holes and a stub pipe
    fl = zspan(0, 0, ff, zf, rf) - zspan(0, 0, ff - 1, zf + 1, PB["stub_ri"])
    fl = fl + ring(0, 0, ff - PB["stub_len"], ff, PB["stub_ri"], PB["stub_r"])
    for x, y in bpos:
        fl = fl - zspan(x, y, ff - 1, zf + 1, 7.0)
    add("hydrant", "Hydrant outlet flange and stub (existing)", fl, "mild_steel", "context")

    # ---- cap, gasket, sleeve bore and O-ring groove
    cap = cp.break_edges(zspan(0, 0, cap_bot, cap_top, rf), 1.0)
    cap = cap - zspan(0, 0, cap_bot - 1, cap_top + 1, PB["sleeve_ro"])
    cap = cap - ring(0, 0, cap_bot + 4, cap_bot + 6.5, PB["sleeve_ro"] - 0.1, PB["sleeve_ro"] + 1.6)
    for x, y in bpos:       # countersunk M12 holes: cone 24 mm at the top face, 12 mm shank
        cone = b.Pos(x, y, cap_top - 3.5) * b.Cone(6.0, 12.0, 7.0)
        cap = cap - cone - zspan(x, y, cap_bot - 1, cap_top, 6.0)
    # tapped M8 holes for the mast foot and M5 holes for the clip feet are added below
    gasket = ring(0, 0, zf, cap_bot, PB["stub_ri"] + 6, rf - 12)
    gasket = gasket - zspan(0, 0, zf - 1, cap_bot + 1, PB["sleeve_ro"])
    for x, y in bpos:
        gasket = gasket - zspan(x, y, zf - 1, cap_bot + 1, 7.0)
    add("gasket", "Cap gasket, EPDM 3 mm", gasket, "epdm", "bought", 6)
    for i, (x, y) in enumerate(bpos):
        # countersunk head, shank through cap, gasket (gasket is clear of the bolts) and flange, washer and nut below
        csk = b.Pos(x, y, cap_top - 3.5) * b.Cone(6.0, 12.0, 7.0) + zspan(x, y, ff - 12, cap_top - 7.0, 6.0)
        add("csk", f"M12 countersunk screw {i + 1} (ISO 10642)", csk, "stainless", "fastener", 6)
        add("csk", f"M12 washer {i + 1} (ISO 7089)", b.Pos(x, y, ff - 2.5) * cp.washer(12), "stainless", "fastener", 6)
        add("csk", f"M12 hex nut {i + 1} (ISO 4032)", b.Pos(x, y, ff - 2.5 - 10.8) * cp.hex_nut(12), "stainless", "fastener", 6)

    # ---- hydrophone: sleeve with collar, potted piezo tube, retaining nut, O-ring, gland, preamp, cable
    ro, ri = PB["sleeve_ro"], PB["sleeve_ri"]
    z_tip = cap_bot - PB["tip_len"]
    z_col = cap_top
    sleeve = zspan(0, 0, z_tip, z_col + 70.0, ro) + zspan(0, 0, z_col, z_col + 6.0, PB["collar_r"])
    sleeve = sleeve - zspan(0, 0, z_tip + 3.0, z_col + 71.0, ri)
    sleeve = cp.break_edges(sleeve, 0.5)
    add("sleeve", "Hydrophone sleeve, 316 stainless", sleeve, "stainless", "made", 6)
    add("sleeve_oring", "O-ring 20 x 3 (nitrile)", oring_installed(0, 0, cap_bot + 5.25, ro, ro + 1.5, 2.5), "nitrile", "bought", 6)
    add("sleeve_nut", "Retaining nut, 316 stainless", hexprism(0, 0, z_col + 6.0, z_col + 16.0, 30.0) - zspan(0, 0, z_col, z_col + 17, ro), "stainless", "fastener", 6)
    piezo = zspan(0, 0, z_tip + 6.0, z_tip + 26.0, 5.8) - zspan(0, 0, z_tip + 5.0, z_tip + 27.0, 3.5)
    add("piezo", "Piezoceramic tube 11.6 x 7 x 20", cp.break_edges(piezo, 0.2), "ceramic_piezo", "bought", 3)
    pot = zspan(0, 0, z_tip + 3.0, z_tip + 36.0, ri) - zspan(0, 0, z_tip + 2.0, z_tip + 37.0, 5.8) + zspan(0, 0, z_tip + 6.0, z_tip + 26.0, 3.5)
    pot = pot - zspan(0, 0, z_tip + 6.0, z_tip + 26.0, 3.5) + zspan(0, 0, z_tip + 6.0, z_tip + 26.0, 3.5) if False else \
        (zspan(0, 0, z_tip + 3.0, z_tip + 36.0, ri) - zspan(0, 0, z_tip + 6.0, z_tip + 26.0, 5.8)) + zspan(0, 0, z_tip + 6.0, z_tip + 26.0, 3.5)
    add("potting", "Polyurethane potting in the tip", pot, "pu_black", "made", 11)
    pa_z = z_tip + 40.0
    pre = cp.break_edges(zspan(0, 0, pa_z, pa_z + 1.6, 5.4), 0.15) + zspan(1.5, 1.0, pa_z - 0.8, pa_z, 1.2) + zspan(-2.0, -1.0, pa_z - 0.6, pa_z, 1.0)
    add("preamp", "Hydrophone preamplifier board", pre, "fr4_green", "bought", 4)
    gl = zspan(0, 0, z_col + 70.0, z_col + 82.0, 9.0) + hexprism(0, 0, z_col + 70.0, z_col + 76.0, 19.0)
    gl = cp.break_edges(gl, 0.6) - zspan(0, 0, z_col + 69.0, z_col + 83.0, 3.2)
    add("gland", "Cable gland PG7, brass", gl, "brass", "bought", 6)

    # ---- mast foot plate with a mast welded on, top plate, antenna bracket and antenna
    mx, ms, mw = PB["mast_x"], PB["mast_side"], PB["mast_wall"]
    pt = 5.0
    plate = cp.sheet(60, 60, pt, holes=[(0, -22, 6.6), (0, 22, 6.6)], r_corner=5.0, edge=0.5)
    plate = b.Pos(mx, 0, cap_top) * plate
    for y in (-22, 22):
        cap = cap - zspan(mx, y, cap_top - 12.0, cap_top + 1, 3.1)
    add("foot", "Mast foot plate, 60 x 60 x 5 stainless", plate, "stainless", "made", 9)
    z_ant_top = -40.0 - 20.0
    z_bracket = z_ant_top - p["ant_t"] - p["ant_bracket"][1]
    z_mast_top = z_bracket - 4.0                            # top plate 4 mm under the bracket
    mast = b.Pos(mx, 0, cap_top + pt) * cp.shs(ms, mw, z_mast_top - cap_top - pt)
    add("mast", "Antenna mast, 20 x 20 x 1.5 aluminium", mast, "aluminium", "made", 9)
    tp = cp.sheet(ms + 4, ms + 4, 4.0, holes=[(0, 0, 5.5)], r_corner=2.0, edge=0.4)
    add("mast_top", "Mast top plate, 24 x 24 x 4 aluminium", b.Pos(mx, 0, z_mast_top) * tp, "aluminium", "made", 9)
    leg = 3.0
    bead = cp.weld_fillet(ms, leg)
    for k in range(4):
        base = b.Rot(0, 0, 90 * k) * b.Pos(-ms / 2, ms / 2, 0) * bead               # on the mast side face, above the plate
        add("weld", f"Fillet weld, mast to foot plate {k + 1}", b.Pos(mx, 0, cap_top + pt) * base, "stainless", "weld", 9)
    for k in range(4):
        base = b.Rot(0, 0, 90 * k) * b.Pos(-ms / 2, ms / 2, 0) * bead.mirror(b.Plane.XY)   # under the top plate
        add("weld", f"Fillet weld, mast to top plate {k + 1}", b.Pos(mx, 0, z_mast_top) * base, "aluminium", "weld", 9)
    for i, y in enumerate((-22, 22)):
        add("foot_screw", f"M6x16 pan head screw, foot plate {i + 1}", b.Pos(mx, y, cap_top + pt) * pan_screw(6, 16, 12.0, 3.6), "stainless", "fastener", 9)
    fr_ant = b.Pos(mx, 0, z_bracket)
    ant_parts, stud_loc = antenna_stack(p)
    out += moved(ant_parts, fr_ant)
    stud_bottom = tuple(gpt(fr_ant, *stud_loc))
    # M5 bolt through bracket and top plate, nut and washers inside the mast
    for nm, shp in cp.hex_bolt_set(5, p["ant_bracket"][1] + 4.0):
        add("bracket_bolt", nm + " (bracket)", b.Pos(mx, 0, z_bracket + p["ant_bracket"][1]) * shp, "stainless", "fastener", 9)

    # ---- logger lying on two omega clips on the cap; axis along Y, top (eye bolt) toward -Y, SMA bulkhead on top
    lp = local_p(p)
    lg = LG.logger_parts(lp, D, 0.0, 0.0)
    R = p["tube_od"] / 2
    x_c = PB["logger_x"]
    z_L = cap_top + 1.0 + R + 1.0
    y_top = -p["logger_len"] / 2
    fr = frame((x_c, y_top, z_L), (0, 0, 1), (0, -1, 0))        # local z -> global -Y, local x -> global +Z, local y -> global +X
    # NB local x -> +Z means the base (local -x) is below: correct. local y = z cross x = (0,-1,0)x(0,0,1) = (-1,0,0)
    lgp = moved(lg, fr)
    plug, zs_bot = plug_local(lp, D)
    lgp += moved(plug, fr)
    zc_local = [(-y_top) * -1 for _ in ()]
    clip_z = [-(p["logger_len"] / 2 + y) for y in PB["clip_y"]]     # local z of each clip (negative, below the top flange)
    cl, cuts = clip_set(lp, fr, clip_z, None)
    out += lgp + cl
    for c in cuts:
        cap = cap - c
    add("cap", "Hydrant cap, 316 stainless, 210 x 16", cap, "stainless", "made", 6)

    # ---- hydrophone cable to the logger's M12 socket, antenna lead to the SMA plug
    smap = moved([mk("ant_lead", "SMA plug", sma_plug_local(lp), "pu_black", "bought", 10)], fr)[0]
    p_end = gpt(fr, 0, 14.0, 27.0)                              # end of the SMA plug boot, global
    p_m12 = gpt(fr, 0, 0, zs_bot)
    cab_pts = [(0, 0, cap_top + 82.0), (0, 0, cap_top + 95.0), (25, -40, cap_top + 60.0), (x_c, -50, z_L - 40), (x_c, p_m12.Y - 38, z_L - 12),
               (x_c, p_m12.Y - 38, z_L)]
    cab_pts[-2] = (x_c, p_m12.Y + 38.0, z_L - 12)
    cab_pts[-1] = (x_c, p_m12.Y + 3.0, z_L)
    cab_pts = [(0, 0, cap_top + 82.0), (0, 0, cap_top + 96.0), (0, 20, cap_top + 110.0), (30, 120, cap_top + 90.0), (x_c, p_m12.Y + 60.0, z_L + 5.0),
               (x_c, p_m12.Y + 3.0, z_L)]
    add("cable", "Hydrophone cable, PU 6 mm", cp.rope(smooth(cab_pts, 2), 6.0), "pu_black", "bought", 5)
    ax_c, ay_c, az_c = stud_bottom
    lead_pts = [(ax_c, ay_c, az_c), (ax_c, ay_c, az_c - 60), (ax_c + 10, -60.0, cap_top + 160.0), (x_c, p_end.Y - 40.0, z_L + 14 + 40), (x_c, p_end.Y - 20.0, z_L + 14), (x_c, p_end.Y, z_L + 14)]
    add("ant_lead", "Antenna lead", fuse([smap["shape"], path(smooth(lead_pts, 1), 2.5)]), "pu_black", "bought", 10)
    return out


# ======================================================================================================== option C
PC = {"box": (420.0, 300.0, 520.0), "wall": 10.0, "lip": 30.0, "lip_t": 10.0, "lid_t": 20.0,
      "spike_x": 330.0, "spike_r": 11.0, "spike_len": 420.0, "z_head_top": -41.0,
      "plate": (110.0, 330.0, 8.0), "ptop": -30.0, "logger_top": -95.0, "xp": -100.0, "zg": -30.0}


def components_C(p):
    D = {}
    bx, by, bz = PC["box"]
    wt = PC["wall"]
    out = []
    add = lambda *a, **k: out.append(mk(*a, **k))
    zg, xp, ptop = PC["zg"], PC["xp"], PC["ptop"]

    # ---- ground box: open top, outward lip, 10 mm walls (HDPE moulding), lid on the lip
    outer = boxspan(-bx / 2, bx / 2, -by / 2, by / 2, -bz, 0)
    inner = boxspan(-bx / 2 + wt, bx / 2 - wt, -by / 2 + wt, by / 2 - wt, -bz + wt, 1)
    gb = cp.break_edges(outer - inner, 2.0)
    lipw = PC["lip"]
    lip = boxspan(-bx / 2 - lipw, bx / 2 + lipw, -by / 2 - lipw, by / 2 + lipw, -PC["lip_t"], 0) - boxspan(-bx / 2 + wt, bx / 2 - wt, -by / 2 + wt, by / 2 - wt, -PC["lip_t"] - 1, 1)
    gb = gb + cp.break_edges(lip, 1.5)
    lid_pts = [(sx * (bx / 2 + lipw / 2), sy * (by / 4)) for sx in (-1, 1) for sy in (-1, 1)]
    for x, y in lid_pts:
        gb = gb - zspan(x, y, -PC["lip_t"], 1, 5.0)
    gx = bx / 2
    gb = gb - xcyl(gx - wt - 1, gx + 1, 0, zg, 6.5)           # gland hole, M16 class
    yw = by / 2 - wt
    pw, ph, pt = PC["plate"]
    plate_holes = [(xp + sx * 44, ptop - 25.0 if sz > 0 else ptop - ph + 25.0) for sx in (-1, 1) for sz in (1, -1)]
    for x, z in plate_holes:
        gb = gb - b.Pos(x, yw + 4.5, z) * b.Rot(90, 0, 0) * b.Cylinder(3.05, 9.0)
    lid = cp.break_edges(boxspan(-bx / 2 - lipw, bx / 2 + lipw, -by / 2 - lipw, by / 2 + lipw, 0, PC["lid_t"]), 2.0)
    lid = lid - fuse([zspan(x, y, -1, PC["lid_t"] + 1, 5.5) for x, y in lid_pts])
    add("lid", "Ground box lid, HDPE 20 mm", lid, "hdpe_box", "made", 6)
    for i, (x, y) in enumerate(lid_pts):
        for nm, shp in [("M10x35 hex bolt (ISO 4017)", b.Pos(x, y, PC["lid_t"] + 2.0) * cp.hex_bolt(10, 35)),
                        ("M10 washer (ISO 7089)", b.Pos(x, y, PC["lid_t"]) * cp.washer(10))]:
            add("lid_bolt", f"{nm} {i + 1}", shp, "stainless", "fastener", 6)

    # ---- back plate on the rear wall, M6 screws into the wall, logger on two omega clips
    zc_pl = ptop - ph / 2
    plate = b.Pos(xp, yw, zc_pl) * (b.Rot(90, 0, 0) * cp.sheet(pw, ph, pt, holes=[(x - xp, z - zc_pl, 6.6) for x, z in plate_holes], r_corner=4.0, edge=0.6))
    lp = local_p(p)
    lg = LG.logger_parts(lp, D, 0.0, 0.0)
    R = p["tube_od"] / 2
    y_c = (yw - pt) - R - 1.0
    fr = frame((xp, y_c, PC["logger_top"]), (0, -1, 0), (0, 0, 1))      # local z -> +Z, local x -> -Y, local y -> +X
    lgp = moved(lg, fr)
    plug, zs_bot = plug_local(lp, D)
    lgp += moved(plug, fr)
    LS = 7
    cl, cuts = clip_set(lp, fr, [-60.0, -180.0], None, L=LS)
    for c_ in cuts:
        plate = plate - c_
    plate = plate - zspan(xp, yw - 4.0, ptop - 8.0, ptop + 1, 2.6)           # bracket screw, tapped in the top edge
    add("plate", "Back plate, 110 x 330 x 8 aluminium", plate, "aluminium", "made", 9)
    for i, (x, z) in enumerate(plate_holes):
        add("plate_screw", f"M6x16 pan head screw, back plate {i + 1}", b.Pos(x, yw - pt, z) * b.Rot(90, 0, 0) * pan_screw(6, 16, 12.0, 3.6), "stainless", "fastener", 9)
    out += lgp + cl

    # ---- antenna on a bracket bolted to the top edge of the back plate, under the lid
    fr_ant = frame((xp, yw - 4.0, ptop), (0, -1, 0), (0, 0, 1))
    ant_parts, stud_loc = antenna_stack(p, back=3.5)
    out += moved(ant_parts, fr_ant)
    stud = gpt(fr_ant, *stud_loc)
    add("bracket_bolt", "M5x10 pan head screw (bracket)", b.Pos(xp, yw - 4.0, ptop + p["ant_bracket"][1]) * pan_screw(5, 10, 9.0, 3.3), "stainless", "fastener", 9)
    sma = moved([mk("ant_lead", "SMA plug", sma_plug_local(lp), "pu_black", "bought", 10)], fr)[0]
    sx0, sy0 = xp + 14.0, y_c
    ztop_sma = PC["logger_top"] + 27.0
    lead = [(sx0, sy0, ztop_sma - 1.0), (sx0, sy0, ztop_sma + 5.0), (xp + 8.0, (sy0 + stud.Y) / 2, (ztop_sma + stud.Z) / 2 + 2.0), (stud.X, stud.Y, stud.Z - 1.2)]
    add("ant_lead", "Antenna lead", fuse([sma["shape"], path(smooth(lead, 1), 2.5)]), "pu_black", "bought", 10)

    # ---- spike, geophone housing and cable
    sx = PC["spike_x"]
    sr = PC["spike_r"]
    z_top = PC["z_head_top"]
    z_cap = z_top - 5.0
    z_tube0 = z_cap - 50.0
    z_plate = z_tube0 - 4.0
    z_bar_bot = z_plate - PC["spike_len"]
    bar = zspan(sx, 0, z_bar_bot, z_plate, sr)
    tip = zspan(sx, 0, z_bar_bot - 12.0, z_bar_bot, sr) + b.Pos(sx, 0, z_bar_bot - 12.0 - 20.0) * b.Cone(0.8, sr, 40.0)
    add("spike", "Spike, 22 mm stainless round bar", cp.break_edges(bar, 0.6), "stainless", "made", 9)
    add("spike", "Spike tip, 316 stainless", cp.break_edges(tip, 0.3), "stainless", "made", 9)
    add("spike", "Housing base plate, 46 x 4 stainless", cp.break_edges(zspan(sx, 0, z_plate, z_tube0, 23.0), 0.6), "stainless", "made", 9)
    ht = b.Pos(sx, 0, z_tube0) * cp.round_tube(40.0, 5.0, z_cap - z_tube0)
    for k in range(3):
        a = math.radians(30 + 120 * k)
        ht = ht - zspan(sx + 17.5 * math.cos(a), 17.5 * math.sin(a), z_cap - 10.0, z_cap + 1.0, 2.0)
    add("housing", "Geophone housing tube, 40 x 5 stainless", ht, "stainless", "made", 9)
    hcap = cp.break_edges(zspan(sx, 0, z_cap + 1.0, z_top, 21.0), 0.6) - zspan(sx, 0, z_cap - 1, z_top + 1, 4.0)
    for k in range(3):
        a = math.radians(30 + 120 * k)
        hcap = hcap - zspan(sx + 17.5 * math.cos(a), 17.5 * math.sin(a), z_cap, z_top + 1, 2.25)
    add("housing", "Housing cap, 42 x 5 stainless", hcap, "stainless", "made", 9)
    for k in range(3):
        a = math.radians(30 + 120 * k)
        add("housing_screw", f"M4x14 socket screw, housing cap {k + 1}", b.Pos(sx + 17.5 * math.cos(a), 17.5 * math.sin(a), z_top) * socket_screw(4, 14), "stainless", "fastener", 9)
    gk = ring(sx, 0, z_cap, z_cap + 1.0, 15.0, 20.0)
    for k in range(3):
        a = math.radians(30 + 120 * k)
        gk = gk - zspan(sx + 17.5 * math.cos(a), 17.5 * math.sin(a), z_cap - 1, z_cap + 2, 2.25)
    add("housing_gasket", "Housing cap gasket, EPDM 1 mm", gk, "epdm", "bought", 6)
    geo = cp.break_edges(zspan(sx, 0, z_tube0, z_tube0 + 32.0, 12.5), 1.0)
    add("geophone", "Geophone element 4.5 Hz, 25 mm", geo, "mild_steel", "bought", 3)
    gl = cp.break_edges(zspan(sx, 0, z_top, z_top + 12.0, 6.0), 0.6) - zspan(sx, 0, z_top - 1, z_top + 13, 3.2)
    add("gland", "Cable gland PG7, housing cap", gl, "brass", "bought", 6)
    # wall gland: body through the wall, dome outside, nut inside
    body = xcyl(gx - wt - 12.0, gx, 0, zg, 6.5)
    body = body + xcyl(gx, gx + 14.0, 0, zg, 9.0)
    body = cp.break_edges(body - xcyl(gx - wt - 13.0, gx + 15.0, 0, zg, 3.2), 0.5)
    add("gland", "Cable gland M16, wall", body, "brass", "bought", 6)
    nut = put(hexprism(0, 0, 0, 8.0, 19.0), (gx - wt, 0, zg), "-x") - xcyl(gx - wt - 9, gx - wt + 1, 0, zg, 6.5)
    add("gland", "Gland nut, inside", nut, "brass", "fastener", 6)
    # cable: geophone to gland (outside) and gland to logger plug (inside), one run
    z_end = zs_bot
    pm = gpt(fr, 0, 0, zs_bot)
    cab = [(sx, 0, z_top + 12.0), (sx, 0, z_top + 20.0), (sx - 30.0, 0, zg + 8.0), (gx + 40.0, 0, zg), (gx - wt - 40.0, 0, zg),
           (120.0, 20.0, -150.0), (xp + 60.0, y_c - 20.0, pm.Z - 70.0), (xp, y_c, pm.Z - 30.0), (xp, y_c, pm.Z - 3.0)]
    add("cable", "Geophone cable, PU 6 mm", cp.rope(smooth(cab, 1), 6.0), "pu_black", "bought", 5)
    add("box", "Ground box, HDPE moulding 10 mm wall", gb, "hdpe_box", "made", 6)
    return out


def components(option):
    from model import PARAMS
    p = dict(PARAMS)
    return {"B": components_B, "C": components_C}[option](p)
