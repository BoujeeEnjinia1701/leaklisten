"""The LeakListen logger and sensor puck as detailed parts (kit 1.9, D3), shared by every concept option.

logger_parts(p, lx, top)   PVC tube, two turned plugs with compressed O-rings, six radial M4 screws, M12 panel socket,
                           eye bolt, SMA bulkhead, light pipe, printed chassis on two hex standoffs, main board with its
                           components on four nylon standoffs, hybrid layer capacitor, C cell, desiccant pouch.
puck_parts(p)              sensor puck on a 42 mm pot magnet: puck body, magnet cup and ring, piezo, mass, preamplifier
                           board, potting, cable and M12 plug.
Every part is a cad_parts.part() dict with an extra "key" (see lkl_parts.mk). Axes as model.py: street surface Z = 0,
logger vertical at (lx, 0).
"""
from __future__ import annotations

import math

import build123d as b
import cad_parts as cp
from lkl_parts import (mk, fuse, zspan, zcyl, boxspan, box, hexprism, ring, smooth, put, radial, pan_screw,
                       socket_screw, hex_standoff, oring_installed, pcb, smd, washer_od, tube)


def logger_parts(p, D, lx, top, with_eye=True):
    """Parts of the logger hanging with its top flange at z = top and its axis at (lx, 0)."""
    L = p["logger_len"]
    bot = top - L
    R = p["tube_od"] / 2
    ri = R - p["tube_wall"]
    pf, pt = p["plug_flange"], p["plug_t"]
    t0, t1 = bot + pf, top - pf
    pin = t1 - pt                                           # inner face of the top plug
    out = []
    add = lambda *a, **k: out.append(mk(*a, **k))

    # ---- tube (BOM 6): 63 x 3 PVC pipe, ends broken, six 4.5 mm radial holes
    tb = b.Pos(lx, 0, t0) * cp.round_tube(p["tube_od"], p["tube_wall"], t1 - t0)
    tb = cp.break_edges(tb, 0.6)
    zs_t, zs_b = t1 - p["screw_z"], t0 + p["screw_z"]
    for zz in (zs_t, zs_b):
        for a in p["screw_ang"]:
            ar = math.radians(a)
            tb = tb - tube((lx + (R - 4) * math.cos(ar), (R - 4) * math.sin(ar), zz),
                           (lx + (R + 2) * math.cos(ar), (R + 2) * math.sin(ar), zz), 2.25)
    add("tube", "Logger tube, PVC-U 63 x 3", tb, "pvc_grey", "made", 6)

    # ---- plugs (BOM 6): turned acetal, flange 4 mm, spigot 18 mm, two O-ring grooves
    def plug(end):
        if end > 0:
            f0, f1, s0, s1 = t1, top, pin, t1
        else:
            f0, f1, s0, s1 = bot, t0, t0, t0 + pt
        fl = zspan(lx, 0, f0, f1, R)
        fl = cp.break_edges(fl, 0.8)
        sp = zspan(lx, 0, s0, s1, ri)
        body = fl + sp
        rings = []
        for dz, oc, od in zip(p["oring_z"], p["oring_cs"], (1.8, 1.8)):
            zc_ = (t1 - dz) if end > 0 else (t0 + dz)
            body = body - ring(lx, 0, zc_ - oc / 2, zc_ + oc / 2, ri - od, ri + 1)
            rings.append(oring_installed(lx, 0, zc_, ri - od, ri, oc))
        zsc = zs_t if end > 0 else zs_b
        for a in p["screw_ang"]:       # tapped M4 holes: the screw's own volume
            ar = math.radians(a)
            body = body - tube((lx + (ri - 8) * math.cos(ar), (ri - 8) * math.sin(ar), zsc),
                               (lx + R * math.cos(ar), R * math.sin(ar), zsc), 2.0)
        return body, rings

    tp, t_or = plug(+1)
    bp, b_or = plug(-1)
    sma_y = 14.0
    lpx, lpy = p["lpipe_xy"]
    tp = tp - zspan(lx, 0, pin - 1, top + 1, 3.2) - zspan(lx, sma_y, pin - 1, top + 1, 3.25) \
        - zspan(lx + lpx, lpy, pin - 1, top + 1, p["lpipe_d"] / 2 + 0.05)
    for xx in (-18, 18):                                      # M3 tapped holes for the standoff studs
        tp = tp - zspan(lx + xx, -6.0, pin - 1, pin + 6, 1.5)
    bp = bp - zspan(lx, 0, bot - 1, t0 + pt + 1, 8.0)
    add("topplug", "Top end plug, acetal", tp, "acetal_black", "made", 6)
    add("botplug", "Bottom end plug, acetal", bp, "acetal_black", "made", 6)
    for i, o in enumerate(t_or):
        add("top_orings", f"O-ring {i + 1}, top plug (nitrile)", o, "nitrile", "bought", 6)
    for i, o in enumerate(b_or):
        add("bot_orings", f"O-ring {i + 1}, bottom plug (nitrile)", o, "nitrile", "bought", 6)

    # ---- six radial M4 pan head screws (BOM 6)
    for key, zz, tag in (("screws_top", zs_t, "top"), ("screws_bot", zs_b, "bottom")):
        for a in p["screw_ang"]:
            add(key, f"M4x11 pan head screw, {tag} plug, {a:.0f} deg", radial(pan_screw(4, 11, 7.0, 2.5), lx, 0, zz, R, a),
                "stainless", "fastener", 6)

    # ---- M12 A-coded panel socket in the bottom plug (BOM 6): body in an M16 hole, hex nut inside, M12 thread outside
    sock = zspan(lx, 0, bot - 15, bot, 6.0) + zspan(lx, 0, bot, t0 + pt + 8, 8.0) + hexprism(lx, 0, bot - 1.0, bot, 19.0)
    sock = sock - zspan(lx, 0, bot - 16, bot - 6, 3.5)
    sock = cp.break_edges(sock, 0.3)
    add("socket", "M12 panel socket, front mount", sock, "stainless", "bought", 6)
    add("socket_nut", "M16 panel nut", hexprism(lx, 0, t0 + pt, t0 + pt + 4, 22.0) - zspan(lx, 0, t0 + pt - 1, t0 + pt + 5, 8.0),
        "stainless", "fastener", 6)

    # ---- eye bolt (BOM 13): sealing washer, ring bolt, nut
    add("eye_washer", "Bonded sealing washer M6", b.Pos(lx, 0, top) * washer_od(6.4, 14.0, 1.0), "epdm", "fastener", 13)
    shank_bot = pin - 8
    eye = zspan(lx, 0, shank_bot, top + 1.0, 3.0) + zspan(lx, 0, top + 1.0, top + 4.0, 7.0)
    eye = eye + b.Pos(lx, 0, top + 15.5) * b.Rot(90, 0, 0) * b.Torus(10.0, 2.5)
    eye = eye + zspan(lx, 0, top + 4.0, top + 7.0, 3.0)
    add("eyebolt", "M6 eye bolt, stainless", eye, "stainless", "bought", 13)
    add("eye_nut", "M6 hex nut (ISO 4032)", put(cp.hex_nut(6), (lx, 0, pin - 5.2)), "stainless", "fastener", 13)

    # ---- SMA bulkhead (BOM 13): barrel through the plug, hex flange outside, nut inside, solder cup behind
    sma = zspan(lx, sma_y, top, top + 15, 3.175) + hexprism(lx, sma_y, top + 0.5, top + 3.5, 8.0) \
        + zspan(lx, sma_y, pin - 15, pin - 2.5, 2.5) + zspan(lx, sma_y, pin - 2.5, top, 3.175)
    sma = sma - zspan(lx, sma_y, top + 6, top + 16, 1.6)
    add("sma", "SMA bulkhead, IP67", sma, "brass", "bought", 13)
    add("sma_nut", "SMA panel nut", hexprism(lx, sma_y, pin - 2.5, pin, 8.0) - zspan(lx, sma_y, pin - 3, pin + 1, 3.175),
        "brass", "fastener", 13)

    # ---- light pipe (BOM 7): 3 mm clear acrylic rod, flush with the top plug
    bz1 = pin - 20.0 - 8.0                                   # main board top edge (chassis spine top less 8)
    lp = zspan(lx + lpx, lpy, bz1 + p["lpipe_gap"], top, p["lpipe_d"] / 2)
    add("lpipe", "Status light pipe rod, acrylic", cp.break_edges(lp, 0.15), "acrylic_clear", "bought", 7)

    # ---- printed chassis on two hex standoffs (BOM 12)
    sw, st = p["spine"]
    SO_Y = -6.0
    so = p["chassis_standoff"]
    sp_top = pin - so
    sp_bot = bot + pf + pt + 18.0
    spine = boxspan(lx - sw / 2, lx + sw / 2, -st, 0.0, sp_bot, sp_top)
    hd, hh = p["hlc"]
    cap_c = (lx - 12.0, hd / 2 + 1.5)
    z_cap1 = sp_top - 8.0
    clip = None
    for zz in (z_cap1 - 8, z_cap1 - hh + 8):
        c_ = ring(cap_c[0], cap_c[1], zz - 3, zz + 3, hd / 2, hd / 2 + 1.5) & boxspan(lx - 40, lx + 40, -1, cap_c[1] + 3, zz - 4, zz + 4)
        clip = c_ if clip is None else clip + c_
    ddx, ddy, ddz = p["desiccant"]
    dx0 = lx - 1.0
    dz1 = sp_top - 8.0
    pocket = boxspan(dx0 - 1.5, dx0 + ddx + 1.5, 0, 1.5 + ddy + 1.5, dz1 - ddz - 1.5, dz1 - 10) - \
        boxspan(dx0, dx0 + ddx, 0.01, 1.5 + ddy, dz1 - ddz, dz1)
    cd, ch = p["cell"]
    cell_c = (lx, cd / 2 + 1.5)
    z_cell0 = sp_bot + 5.0
    cclips = None
    for zz in (z_cell0 + 10, z_cell0 + ch - 10):
        c_ = ring(cell_c[0], cell_c[1], zz - 4, zz + 4, cd / 2, cd / 2 + 2) & boxspan(lx - 40, lx + 40, -1, cell_c[1] + 2.5, zz - 5, zz + 5)
        cclips = c_ if cclips is None else cclips + c_
    tab = boxspan(lx - sw / 2, lx + sw / 2, -9.0, 9.0, sp_top - 4.0, sp_top)
    for xx in (-18, 18):
        tab = tab - zspan(lx + xx, SO_Y, sp_top - 5, sp_top + 1, 1.6)
    # four M3 bosses' clearance: thread-forming screws bite the 3 mm spine, holes drawn at the screw size
    bz_top = sp_top - 8.0
    bx, by, bz = p["board"]
    screw_pos = [(-15, bz_top - 5), (15, bz_top - 5), (-15, bz_top - bz + 5), (15, bz_top - bz + 5)]
    chassis = spine + tab + clip + pocket + cclips
    for xx, zz in screw_pos:
        chassis = chassis - b.Pos(lx + xx, -1.5, zz) * b.Rot(90, 0, 0) * b.Cylinder(1.5, 3.0)
    add("chassis", "Internal chassis, printed PETG", cp.break_edges(chassis, 0.3), "petg_teal", "made", 12)
    for i, xx in enumerate((-18, 18)):
        sd = put(hex_standoff(5.5, so, 3.0, 6.0, 5.0), (lx + xx, SO_Y, pin), "-z")
        add("standoffs", f"M3x20 hex standoff {i + 1}", sd, "aluminium", "bought", 12)
        add("standoffs", f"M3x8 socket screw, chassis {i + 1}",
            put(socket_screw(3, 8), (lx + xx, SO_Y, sp_top - 4.0), "-z"), "stainless", "fastener", 12)

    # ---- main board (BOM 7): 1.6 mm PCB on four nylon standoffs, components on the far face
    pc = b.Pos(lx, -6.0, bz_top - bz / 2) * pcb(bx, bz, 1.6, [(xx, zz - (bz_top - bz / 2), 3.2) for xx, zz in screw_pos])
    pc = b.Pos(0, 0, 0) * pc
    y0c = -6.0 - 1.6                                          # component face
    comp = [smd(lx, y0c - 1.5, bz_top - 20, 22, 3.0, 30),     # LoRaWAN module under its shield can
            smd(lx - 8, y0c - 0.5, bz_top - 55, 8, 1.0, 8), smd(lx + 8, y0c - 0.4, bz_top - 55, 6, 0.8, 6),
            smd(lx, y0c - 0.4, bz_top - 70, 10, 0.8, 5), smd(lx - 10, y0c - 0.4, bz_top - 82, 5, 0.8, 3),
            smd(lx + 10, y0c - 0.4, bz_top - 82, 5, 0.8, 3),
            smd(lx, y0c - 3.0, bz_top - bz + 14, 12, 6.0, 8)]  # 4-pin plug connector for the socket
    xtal = zspan(lx + 6, y0c - 1.0, bz_top - 45, bz_top - 40, 1.5)
    led = zspan(lx + lpx, lpy, bz_top - 3.0, bz_top + 0.5, 1.5)
    lead = b.Pos(lx + lpx, (lpy + y0c) / 2, bz_top - 3.0) * b.Rot(90, 0, 0) * b.Cylinder(0.3, abs(lpy - y0c))
    pc = pc + fuse(comp) + xtal + led + lead
    add("board", "Main board assembly, LoRaWAN", pc, "fr4_green", "bought", 7)
    bst = None
    for i, (xx, zz) in enumerate(screw_pos):
        s_ = b.Pos(lx + xx, -4.5, zz) * b.Rot(90, 0, 0) * (b.Cylinder(2.5, 3.0) - b.Cylinder(1.5, 3.2))
        add("board_standoffs", f"M3x3 nylon standoff {i + 1}", s_, "nylon_white", "bought", 12)
        add("board_standoffs", f"M3x8 pan head screw, board {i + 1}",
            put(pan_screw(3, 8, 6.0, 1.8), (lx + xx, y0c, zz), "-y"), "stainless", "fastener", 12)

    # ---- capacitor, desiccant, cell
    cap_s = zspan(cap_c[0], cap_c[1], z_cap1 - hh, z_cap1, hd / 2)
    add("hlc", "Hybrid layer capacitor 16 x 30", cp.break_edges(cap_s, 0.8), "capacitor", "bought", 7)
    des = box(dx0 + ddx / 2, 1.5 + ddy / 2, dz1 - ddz / 2, ddx, ddy, ddz)
    add("desiccant", "Silica gel pouch 10 g", cp.break_edges(des, 2.0), "desiccant_pouch", "bought", 11)
    can = zspan(cell_c[0], cell_c[1], z_cell0, z_cell0 + ch - 1.0, cd / 2)
    can = cp.break_edges(can, 0.8) + zspan(cell_c[0], cell_c[1], z_cell0 + ch - 1.0, z_cell0 + ch, 4.0)
    add("cell", "Primary cell, Li-SOCl2 C size", can, "li_cell", "bought", 8)
    return out


def puck_parts(p, D):
    """Sensor puck on the valve spindle cap (axis X = Y = 0): BOM 1 to 5 and the potting (line 11)."""
    out = []
    add = lambda *a, **k: out.append(mk(*a, **k))
    zc = p["cap_top_z"]
    zb = D["puck_bot_z"]
    zt = D["puck_top_z"]
    ro = p["puck_d"] / 2
    r_up = ro - p["puck_wall"]
    r_lo = p["puck_bore_low"] / 2
    z_base = zb + p["puck_base"]
    z_step = z_base + p["puck_step"]
    sd, sl = p["stud"]
    puck = cp.break_edges(zspan(0, 0, zb, zt, ro), 0.5)
    puck = puck - zspan(0, 0, z_base, z_step, r_lo) - zspan(0, 0, z_step, zt + 1, r_up) - zspan(0, 0, zb - 1, zb + sl, sd / 2)
    add("puck", "Sensor puck body, aluminium 6061", puck, "aluminium", "made", 1)
    # pot magnet (BOM 2): steel pot with centre pole and M6 stud, NdFeB ring in the pot
    mh = p["magnet_h"]
    rm = p["magnet_d"] / 2
    pot = zspan(0, 0, zc, zb, rm) - zspan(0, 0, zc - 1, zc + mh - 3.0, rm - 3.0) + zspan(0, 0, zc, zb, 6.0) \
        + zspan(0, 0, zb, zb + sl, sd / 2)
    add("magnet", "Pot magnet 42 mm, steel pot and M6 stud", cp.break_edges(pot, 0.4), "zinc_plated", "bought", 2)
    mring = ring(0, 0, zc + 0.5, zc + mh - 3.0, 6.0, rm - 3.5)
    add("magnet_core", "Pot magnet NdFeB ring", cp.break_edges(mring, 0.3), "ndfeb", "bought", 2)
    # piezo (BOM 3): brass disc with a solder tab, PZT ceramic on it, then the seismic mass
    pz = p["piezo_t"]
    brass = zspan(0, 0, z_base, z_base + pz / 2, p["piezo_d"] / 2) + boxspan(p["piezo_d"] / 2 - 1, p["piezo_d"] / 2 + 0.8, -1.5, 1.5, z_base, z_base + pz / 2)
    add("piezo", "Piezo disc, brass backing", brass, "brass", "bought", 3)
    cer = cp.break_edges(zspan(0, 0, z_base + pz / 2, z_base + pz, 10.0), 0.05)
    add("piezo", "Piezo ceramic, PZT 20 mm", cer, "ceramic_piezo", "bought", 3)
    mass = cp.break_edges(zspan(0, 0, z_base + pz, z_base + pz + p["mass_h"], p["mass_d"] / 2), 0.3)
    add("mass", "Seismic mass, brass 20 x 20", mass, "brass", "made", 3)
    # preamplifier board (BOM 4): round 31 mm board on the puck step, components on the underside
    zp1 = z_step + p["preamp_t"]
    pb = zspan(0, 0, z_step, zp1, p["preamp_d"] / 2)
    under = fuse([smd(-6, 0, z_step - 0.4, 5, 4, 0.8), smd(5, 3, z_step - 0.4, 4, 3, 0.8), smd(4, -4, z_step - 0.7, 6, 5, 1.4),
                  zspan(-4, 7, z_step - 1.5, z_step, 1.6)])
    pad = zspan(0, 0, zp1, zp1 + 0.1, 2.5)
    add("preamp", "Charge preamplifier board", cp.break_edges(pb, 0.15) + under + pad, "fr4_green", "bought", 4)
    potting = zspan(0, 0, zp1 + 0.1, zt, r_up) - zspan(0, 0, zp1, zt + 1, p["cable_d"] / 2)
    add("potting", "Potting above the board", potting, "epoxy_potting", "made", 11)
    # cable and M12 plug (BOM 5)
    return out


def cable_parts(p, D, lx, top):
    """Sensor cable from the preamplifier to the logger's M12 socket, plug overmould and coupling nut (BOM 5)."""
    out = []
    add = lambda *a, **k: out.append(mk(*a, **k))
    bot = top - p["logger_len"]
    zt = D["puck_top_z"]
    zb = D["puck_bot_z"]
    zp1 = zb + p["puck_base"] + p["puck_step"] + p["preamp_t"] + 0.1
    z_nut_top = bot - 5.0                                      # coupling nut engaged 10 mm on the socket thread
    zs_bot = z_nut_top - p["m12_len"]
    rc = p["cable_d"] / 2
    pts = [(0, 0, zp1), (0, 0, zt + 31), (-70, 0, zt + 41), (-130, 0, zt - 44), (-165, 0, zt - 104),
           (lx, 0, zs_bot - 38), (lx, 0, zs_bot - rc)]
    cable = cp.rope(smooth(pts, 2), p["cable_d"])
    add("cable", "Sensor cable, 4-core PUR, 2 m", cable, "pu_black", "bought", 5)
    body = cp.break_edges(zspan(lx, 0, zs_bot, z_nut_top - 17.0, p["m12_d"] / 2 - 2.0), 3.0)
    add("m12_plug", "M12 plug overmould", body, "pu_black", "bought", 5)
    nut = ring(lx, 0, z_nut_top - 17.0, z_nut_top, 6.0, p["m12_d"] / 2)
    for k in range(18):
        a = 2 * math.pi * k / 18
        nut = nut - zspan(lx + math.cos(a) * p["m12_d"] / 2, math.sin(a) * p["m12_d"] / 2, z_nut_top - 15.5, z_nut_top - 1.5, 0.9)
    add("m12_plug", "M12 coupling nut, knurled", cp.break_edges(nut, 0.4), "stainless", "bought", 5)
    return out
