"""LeakListen general arrangement sheet LKL-DWG-001, Rev P5 (TRL 3, constructable design, LKL-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/LKL-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is LKL-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-25"
DATE4 = "2026-10-01"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right"), dims=True):
    """Repeat Sheet.add_ortho's layout arithmetic (kit 1.7) to find the box (x, y, w, h) that each
    view's geometry occupies on the sheet."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    vb = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = vb["front"]; tw, th = vb["top"]; rw, rh = vb["right"]
    dl = 11 if dims else 0
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    cells = {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
             "right": (ax + colw + gap, front_y, k * rw, row_h)}
    out = {}
    for n, (x, y, w, h) in cells.items():
        vw, vh = vb[n][0] - 0.35, vb[n][1] - 0.35
        out[n] = (x + (w - k * vw) / 2, y + (h - k * vh) / 2, k * vw, k * vh)
    return out


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly(with_site=True)
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="LeakListen", title="General arrangement, logger installed", dwg_no="LKL-DWG-001", rev="P5",
              author="Amish Chadha", date="2026-10-02", scale=None, theme="technical",
              material="PVC, aluminium, stainless; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "42 mm pot magnet (LKL-DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC"),
                         ("P4", "Constructable design: neck bar, end plugs, chassis (LKL-DDR-003)", DATE4, "AC"),
                         ("P5", "Status light pipe added to the top plug (decision of 2026-10-02)", "2026-10-02", "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    lx = P["logger_x"]
    top, bot = P["logger_top_z"], D["logger_bot_z"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zs = Z(0)
    L.append(f'<line x1="{x - 4:.2f}" y1="{zs:.2f}" x2="{x + w + 4:.2f}" y2="{zs:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L.append(_t(x + w + 4, zs - 1, "STREET", 2.0, 600, MUTED, "end"))
    xl0 = X(bb.min.X) - 14
    for i, (zz, label) in enumerate(((top, f"{-top:.0f}"), (bot, f"{-bot:.0f}"), (P["cap_top_z"], f"{-P['cap_top_z']:.0f} cap top"))):
        xd = xl0 - 6 * i
        L += [ext(X(lx - P["tube_od"] / 2) if zz != P["cap_top_z"] else X(-P["cap_sq"] / 2), Z(zz), xd - 1, Z(zz))]
        L += dim_v(xd, zs, Z(zz), label)
    xl = X(lx + P["tube_od"] / 2) + 12
    L += dim_v(xl, Z(top), Z(bot), f"{P['logger_len']:.0f}", side=1.8)
    L += leader(X(15), Z(D["puck_bot_z"] + 25), X(40), Z(-300), "SENSOR PUCK")
    L += leader(X(-P["frame_open"] / 2 - 45), Z(-45), X(-P["frame_open"] / 2 - 45) + 6, Z(70), "COVER FRAME (EXISTING)")
    L += leader(X(-100), Z(-427), X(-60), Z(-560), "CABLE SHOWN DIRECT; 2 m FITTED")


    # top view (from +Z): X to the right, Y up the sheet; logger to spindle offset
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    yt = Yt(150)
    L += [ext(Xt(0), Yt(P["cap_sq"] / 2), Xt(0), yt - 1)]
    L += dim_h(Xt(lx), Xt(0), yt, f"{-lx:.0f}")

    # right view (from +X): logger diameter
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    r = P["tube_od"] / 2
    zd = (top + bot) / 2
    dy = 0.0
    L += dim_h(Yr(-r) + dy, Yr(r) + dy, Zr(zd), "")
    ay_ = P["ant_y"]
    L += leader(Yr(ay_ - 20), Zr(D["ant_z"] + 4), Yr(ay_ - 60), Zr(60), "FLAT ANTENNA ON ITS BRACKET")
    L += leader(Yr(200), Zr(P["bar_z"]), Yr(150), Zr(25), "NECK BAR, FEET ON THE NECK WALLS")
    L.append(_t(Yr(r) + dy + 6, Zr(zd) + 0.8, f"{P['tube_od']:.0f} OD", 2.3, 400, INK, "start", mono=True))

    s._layers += L
    s.add_svg(views["iso"], 276, 48, 140, 88, label="Isometric view", sublabel="Not to scale; spindle cap and frame edge grey context")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Logger PVC tube {P['tube_od']:.0f} OD x {P['tube_wall']:.0f} wall, flanged acetal end plugs; {P['logger_len']:.0f} flange to flange, {D['overall_len']:.0f} with socket and eye bolt",
        f"Sensor puck {P['puck_d']:.0f} x {P['puck_h']:.0f} aluminium on a {P['magnet_d']:.0f} mm pot magnet (keeper plate in transport); stack {D['sensor_stack_h']:.0f}",
        f"Seismic mass brass {P['mass_d']:.0f} x {P['mass_h']:.0f} on a 27 mm piezo disc (compression)",
        f"Spindle cap {P['cap_sq']:.0f} square, top {-P['cap_top_z']:.0f} below street (example site)",
        f"Neck bar {P['bar_out'][0]:.0f} and {P['bar_in'][0]:.0f} square aluminium tube, rubber feet on the neck walls; lanyard {P['lanyard_d']:.0f}",
        f"Flat antenna {P['ant_d']:.0f} dia on a bracket on the bar, {D['ant_gap']:.0f} gap below the {P['cover_t']:.0f} cover",
        "Top plug: eye bolt, SMA bulkhead and a 3 mm status light pipe rod",
        "Sensor cable 2 m, M12 IP68; reaches caps to about 2.2 m deep",
        "No chamber entry; nothing touches drinking water",
    ], x=276, y=158, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "LKL-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
