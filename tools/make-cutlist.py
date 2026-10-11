#!/usr/bin/env python3
"""The torsion box cut list, generated from the registry.

WHY THIS IS GENERATED AND NOT TYPED: every part below is a plywood piece whose
size depends on thicknesses that are still NOMINAL - the sheets have not been
micced. When they are, the registry changes and this regenerates. A typed list
would be stale the moment a sheet measured 18.4 instead of 19, and the places it
would be wrong are the notch fits and the wall, which are the two that matter.

It also answers the sheet-size question, because that is not eyeballable: the
skins are BOX_W x BOX_FORE_AFT and BOX_W is within 8 mm of a 4-foot sheet.

    python tools/make-cutlist.py

Writes machine/drawings/box-cutlist.html and prints the sheet summary.
No third-party imports, same as every other tool here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dims import Registry                                    # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "machine" / "drawings" / "box-cutlist.html"

# Sheet sizes to test, in mm. The two Baltic birch formats he asked about.
SHEETS = [
    ("4 x 8", 1219.2, 2438.4),
    ("5 x 5", 1524.0, 1524.0),
]

# How much is lost to a saw cut. 3 mm is a thin-kerf blade and the honest
# figure for a track saw; it is applied between parts, not around the sheet.
KERF = 3.0
# Trim taken off the factory edges before anything is cut to size.
EDGE_TRIM = 6.0


def parts(v):
    """Every plywood piece in the box, as (name, long, short, qty, thickness).

    Each size is an expression over registry symbols, never a literal - that is
    the whole point of generating this. Where a part's size equals a cavity
    dimension the symbol is used directly so the two cannot drift.
    """
    W, D = v["BOX_W"], v["BOX_FORE_AFT"]
    web, rib = v["T_BOX_WALL_WEB"], v["T_BB_RIB"]
    t_out = v["T_BOX_TONGUE"]
    h_cav = v["BOX_RIB_H"]
    return [
        # --- the two skins ------------------------------------------------
        ("Top skin", W, D, 1, v["T_BB_SKIN_TOP"]),
        ("Bottom skin", W, D, 1, v["T_BB_SKIN_BOT"]),

        # --- the outer laminations ----------------------------------------
        # Each side is ONE piece cut full depth and full height, with the proud
        # part sawn off forward of SIDE_LAM_PROUD_CUT - so it is ordered at the
        # TALL height even though most of its length finishes flush.
        ("Side lamination", v["SIDE_LAM_L"], v["TONGUE_FULL_H"], 2, t_out),
        # The back and front run the full OUTER width: they lap the side pieces'
        # end grain, so they cover the box plus both side laminations.
        ("Back lamination", W + 2 * t_out, v["TONGUE_FULL_H"], 1, t_out),
        ("Front cap", W + 2 * t_out, v["BOX_FRONT_CAP_H"], 1, t_out),

        # --- the inner webs, between the skins ------------------------------
        ("Web, back and front", W, h_cav, 2, web),
        ("Web, sides", D - 2 * web, h_cav, 2, web),

        # --- the egg crate ---------------------------------------------------
        ("Rib, fore-aft", D - 2 * web, h_cav, int(v["BOX_RIBS_FORE_AFT"]), rib),
        ("Rib, across", W - 2 * web, h_cav, int(v["BOX_RIBS_ACROSS"]), rib),
        ("Back tenon block", v["BACK_TENON_BLOCK_L"], h_cav, 2, rib),
    ]


def pack(pieces, sw, sl):
    """Shelf-pack onto sheets, longest piece first. Returns (sheets, fits).

    🔴 IT IS AN UPPER BOUND, NOT AN OPTIMUM. Shelf packing lays parts in rows
    and never backfills, so a real nest beats it. That is the right error to
    make here: a cut list that says three sheets and needs two wastes money,
    one that says two and needs three stops the build.
    """
    usable_w, usable_l = sw - 2 * EDGE_TRIM, sl - 2 * EDGE_TRIM
    flat = []
    for name, a, b, qty, _t in pieces:
        for _ in range(qty):
            flat.append((name, max(a, b), min(a, b)))
    # SORT BY THE SHORT SIDE, DESCENDING - this is first-fit-decreasing-height
    # and the sort key is the whole algorithm. Sorting by the LONG side instead
    # cost a whole sheet of 25 mm: it laid the thin laminations down first and
    # then had no depth left for the 1210-deep skin.
    flat.sort(key=lambda p: (-p[2], -p[1]))

    for name, lng, shrt in flat:
        # A piece must fit some way round on a bare sheet at all. REPORT THE
        # SHORTFALL, not just the refusal: "4 mm over" is a decision he can
        # make - a sheet may run oversize, or the trim can be skipped on one
        # edge - where a bare "will not fit" is not.
        if not ((lng <= usable_l and shrt <= usable_w)
                or (lng <= usable_w and shrt <= usable_l)):
            over = min(max(lng - usable_l, shrt - usable_w),
                       max(lng - usable_w, shrt - usable_l))
            return None, f"{name}, over by {over:.2f}"

    sheets = 1
    rows = []                                       # (depth, remaining_width) per row
    sheet_depth_used = 0.0
    for name, lng, shrt in flat:
        placed = False
        for i, (depth, rem) in enumerate(rows):
            if shrt <= depth and lng + KERF <= rem:
                rows[i] = (depth, rem - lng - KERF)
                placed = True
                break
        if placed:
            continue
        if sheet_depth_used + shrt + KERF <= usable_w:
            rows.append((shrt, usable_l - lng - KERF))
            sheet_depth_used += shrt + KERF
        else:
            sheets += 1
            rows = [(shrt, usable_l - lng - KERF)]
            sheet_depth_used = shrt + KERF
    return sheets, None


def main():
    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        return 2
    v = {s: reg.value(s) for s in reg.order}

    all_parts = parts(v)
    by_t = {}
    for p in all_parts:
        by_t.setdefault(round(p[4], 3), []).append(p)

    print("TORSION BOX CUT LIST\n")
    rows_html = []
    for t in sorted(by_t, reverse=True):
        print(f"  --- {t:g} mm ---")
        for name, a, b, qty, _ in by_t[t]:
            print(f"    {name:22s} {a:9.2f} x {b:7.2f}   x{qty}")
            rows_html.append((t, name, a, b, qty))
        print()

    print("SHEETS NEEDED, per thickness (shelf-packed, an UPPER bound)\n")
    summary = []
    for label, sw, sl in SHEETS:
        print(f"  {label} ({sw:g} x {sl:g})")
        total = 0
        ok = True
        for t in sorted(by_t, reverse=True):
            n, fail = pack(by_t[t], sw, sl)
            if n is None:
                print(f"    {t:g} mm : DOES NOT FIT - {fail}")
                ok = False
                summary.append((label, t, None, fail))
            else:
                print(f"    {t:g} mm : {n} sheet(s)")
                total += n
                summary.append((label, t, n, None))
        print(f"    total   : {total} sheet(s)" if ok else "    total   : n/a")
        print()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows_html, summary, v), encoding="utf-8")
    print("wrote", OUT.relative_to(HERE.parent))
    return 0


def render(rows, summary, v):
    th = []
    last_t = None
    for t, name, a, b, qty in rows:
        if t != last_t:
            th.append(f'<tr class="grp"><td colspan="4">{t:g} mm</td></tr>')
            last_t = t
        th.append(f"<tr><td>{name}</td><td class=n>{a:.1f}</td>"
                  f"<td class=n>{b:.1f}</td><td class=n>{qty}</td></tr>")
    sh = []
    for label, t, n, fail in summary:
        cell = f"{n} sheet(s)" if n else f'<b class="bad">will not fit</b> &mdash; {fail}'
        sh.append(f"<tr><td>{label}</td><td class=n>{t:g} mm</td><td>{cell}</td></tr>")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>CNCBuild &mdash; Torsion Box Cut List</title>
<style>
 @page {{ size: letter portrait; margin: 14mm; }}
 body {{ font: 10.5pt "Segoe UI", sans-serif; color: #111; max-width: 190mm; }}
 h1 {{ font-size: 15pt; margin: 0 0 2mm; }}
 h2 {{ font-size: 12pt; margin: 7mm 0 2mm; border-bottom: 1px solid #bbb; }}
 table {{ border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; }}
 td, th {{ border: 1px solid #ccc; padding: 1.4mm 2.2mm; }}
 th {{ background: #eee; text-align: left; }}
 td.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
 tr.grp td {{ background: #f3f3f3; font-weight: 600; }}
 .bad {{ color: #a00; }}
 .note {{ background: #fff8e1; border-left: 3px solid #e0a800;
          padding: 2mm 3mm; margin: 3mm 0; }}
</style></head><body>
<h1>Torsion box &mdash; cut list</h1>
<p>Box <b>{v['BOX_W']:.2f}</b> across by <b>{v['BOX_FORE_AFT']:.0f}</b> front to back,
<b>{v['BOX_THK']:.0f}</b> deep. All sizes in mm.</p>

<div class="note"><b>Cut the rib notches to the sheet in hand, not to the number
in this table.</b> The plywood thicknesses here are nominal until the sheets are
micced; a sheet sold as 19 commonly measures 18.2&ndash;18.5. Test-cut on scrap
from the same sheet.</div>

<h2>Parts</h2>
<table><tr><th>Part</th><th>Long</th><th>Short</th><th>Off</th></tr>
{''.join(th)}</table>

<h2>Sheets</h2>
<p>Shelf-packed with a {KERF:g} mm kerf and {EDGE_TRIM:g} mm trimmed off each
factory edge. <b>This is an upper bound</b> &mdash; parts are laid in rows and
never backfilled, so a real nest does better.</p>
<table><tr><th>Sheet</th><th>Thickness</th><th>Needs</th></tr>
{''.join(sh)}</table>

<h2>Notches</h2>
<p>Egg crate, continuous both ways, half-depth notches at every crossing.
Notch depth <b>exactly half</b> &mdash; a set cut slightly deep sits low and
loses contact with a skin along its whole length. The fit is a slip fit, not a
clearance: too tight splits the rib, too loose leaves no glue line.</p>
<p>Notch the bottom edge of every rib where it meets the bottom skin, roughly
20 &times; 15, so the sand can migrate between cells.</p>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
