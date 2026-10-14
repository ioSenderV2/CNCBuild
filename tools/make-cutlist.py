#!/usr/bin/env python3
"""The torsion box cut list and sheet nesting, generated from the registry.

WHY THIS IS GENERATED AND NOT TYPED: every part below is a plywood piece whose
size depends on the sheet thicknesses, and this is exactly what it was written
for - the sheets were micced on 2026-10-13 and came back 24 and 18 against the
nominal 25 and 19 the registry had carried. One number each in registry.toml and
every part here followed. A typed list would have been wrong in the notch fits
and in the wall, which are the two that matter.

It also answers the sheet-size question, because that is not eyeballable: the
skins are BOX_W x BOX_FORE_AFT and BOX_W is within 8 mm of a 4-foot sheet.

    python tools/make-cutlist.py [--kerf 1.6] [--trim 1.6] [--sheet "4 x 8"]

Writes machine/drawings/box-cutlist.html and prints the sheet summary.
No third-party imports, same as every other tool here.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dims import Registry                                    # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "machine" / "drawings" / "box-cutlist.html"

# Sheet sizes to test, in mm. The two Baltic birch formats he asked about.
#
# SETTLED: THE 4 x 8 IS A TRUE 48 x 96 FROM CROSSCUT - his, 2026-10-11, from having
# bought sheet goods there before. That matters more than it looks: the skins
# clear the sheet's WIDTH by only 6.00 after his trim, so a board arriving
# undersize is the one thing that breaks this plan. It is his supplier and his
# experience, so it is recorded as fact rather than carried as a risk.
SHEETS = [
    ("4 x 8", 1219.2, 2438.4),
    ("5 x 5", 1524.0, 1524.0),
]

# HIS NUMBERS, 2026-10-11, and they are the whole answer to the sheet-size
# question. A Festool track saw takes 1.6 off a Baltic birch factory edge and
# that is ALL he removes - he does not trim an allowance on top of the kerf.
#
# FLAG: THESE WERE 3.0 AND 6.0 FOR ONE COMMIT AND BOTH WERE INVENTED. On that pair
# a 4 x 8 sheet came out 2.8 SHORT of the skins and the tool reported 5 x 5 as
# required. It is not: the 6 was a trim allowance nobody had asked for, and it
# alone decided the answer. Defaults are his practice now, and both are
# overridable so the next question of this kind gets tested, not argued.
KERF = 1.6
EDGE_TRIM = 1.6

# One colour per part name, so a piece is recognisable across sheets.
PALETTE = ["#cfe3f7", "#d8efd4", "#fbe3cd", "#e8dcf2", "#fdf0c4",
           "#d6eef0", "#f6d8de", "#dfe3e8", "#e9f0cf", "#f2ded0"]


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
        # FLAG: THE BACK AND FRONT ARE EACH CUT IN TWO - his call 2026-10-11, and
        # it is what puts the whole 25 mm on ONE sheet instead of two. At full
        # length neither will sit beside the top skin on a 4 x 8; at half they
        # both will. Splitting only one of them does not do it.
        # The two halves are 1 apart, not equal: the lamination is an odd length
        # and the joint goes on a whole millimetre rather than on 0.5 - his
        # instruction 2026-10-14. Listed separately so the saw gets both figures.
        ("Back lamination, long half", v["BACK_LAM_PIECE_L"],
         v["TONGUE_FULL_H"], 1, t_out),
        ("Back lamination, short half", v["BACK_LAM_PIECE_SHORT"],
         v["TONGUE_FULL_H"], 1, t_out),
        ("Front cap, long half", v["FRONT_CAP_PIECE_L"],
         v["BOX_FRONT_CAP_H"], 1, t_out),
        ("Front cap, short half", v["FRONT_CAP_PIECE_SHORT"],
         v["BOX_FRONT_CAP_H"], 1, t_out),

        # --- the inner webs, between the skins ------------------------------
        ("Web, back and front", W, h_cav, 2, web),
        ("Web, sides", D - 2 * web, h_cav, 2, web),

        # --- the egg crate ---------------------------------------------------
        ("Rib, fore-aft", D - 2 * web, h_cav, int(v["BOX_RIBS_FORE_AFT"]), rib),
        ("Rib, across", W - 2 * web, h_cav, int(v["BOX_RIBS_ACROSS"]), rib),
        # FLAG: THE TWO BACK TENON BLOCKS ARE NOT HERE ON PURPOSE - they come from
        # his scrap bin, 2026-10-11. They were the ONLY parts on a second sheet
        # of 19 mm, 1% used: a $245 board for 0.044 m2 of location blocking that
        # carries no load and whose thickness is free up to
        # BACK_TENON_BLOCK_T_MAX. Leaving them on the list bought nothing and
        # cost a sheet.
    ]


def notch_svg(length, starts, rib, h, s=0.15):
    """The rib drawn to scale with its notches, cut from the TOP edge here.

    True scale in both directions - no exaggeration - because the point of the
    picture is to see at a glance that the notches are evenly spaced and that
    the end bays are bigger than the gaps between them. A stretched drawing
    would hide exactly the error it is there to catch.
    """
    W, H = length * s, h * s
    body = [f'<rect x="0" y="0" width="{W:.1f}" height="{H:.1f}" '
            f'fill="#f3f7fb" stroke="#333" stroke-width="0.4"/>']
    for st in starts:
        body.append(f'<rect x="{st * s:.2f}" y="0" width="{rib * s:.2f}" '
                    f'height="{H / 2:.2f}" fill="#fff" stroke="#333" '
                    f'stroke-width="0.3"/>')
    return (f'<svg viewBox="-1 -1 {W + 2:.1f} {H + 2:.1f}" width="100%" '
            f'style="max-width:180mm">{"".join(body)}</svg>')


def notch_runs(v):
    """The notch positions along each rib, as (part, length, bay, [starts]).

    A rib is notched where the ribs of the OTHER direction cross it, so the run
    is bay, notch, bay, notch ... bay - and the bay at each end is what holds the
    rib off the perimeter web. Positions are measured from the END OF THE PIECE,
    which is the inside face of the web it butts, so the same tape reading works
    on either end: the run is symmetric.

    It ASSERTS the run closes on the piece length. That is the whole reason this
    is generated: if a bay or a thickness moves and the arithmetic stops closing,
    the build fails here rather than on the bench with a set of ribs cut.
    """
    web, rib = v["T_BOX_WALL_WEB"], v["T_BB_RIB"]
    runs = []
    for part, length, bay, end, n in (
        ("Rib, fore-aft", v["BOX_FORE_AFT"] - 2 * web, v["BOX_BAY_FORE_AFT"],
         v["BOX_BAY_FORE_AFT_END"], int(v["BOX_RIBS_ACROSS"])),
        ("Rib, across", v["BOX_W"] - 2 * web, v["BOX_BAY_W"],
         v["BOX_BAY_W_END"], int(v["BOX_RIBS_FORE_AFT"])),
    ):
        starts = [end + k * (bay + rib) for k in range(n)]
        closes = starts[-1] + rib + end
        assert abs(closes - length) < 1e-6, (
            f"{part}: {n} notches, {end:.3f} end bays and {bay:.3f} inner, run "
            f"to {closes:.3f} on a {length:.3f} piece - the grid no longer closes")
        # HIS INSTRUCTION 2026-10-14, and it is the reason the bays are pinned
        # whole rather than divided out: a dado offset of 697.944 cannot be read
        # off a rule marked in millimetres. If a bay or a thickness ever moves
        # and puts a fraction back into a start, the build fails HERE.
        off = [s for s in starts if abs(s - round(s)) > 1e-9]
        assert not off, (
            f"{part}: notch starts not on whole millimetres - {off}")
        runs.append((part, length, bay, end, starts))
    return runs


def pack(pieces, sw, sl):
    """Guillotine-pack onto sheets. Returns (placements, failure).

    A placement is (sheet, x, y, w, h, name), x along the sheet's LENGTH and y
    across its WIDTH, both from the trimmed corner. Returning placements rather
    than a count is what lets the nesting be DRAWN - a count can be believed or
    not, a picture can be checked.

    FLAG: IT WAS SHELF PACKING AND SHELF PACKING GOT A REAL ANSWER WRONG. Shelves
    run the full width of the sheet, so the skin - 1210 deep on a 1216 sheet -
    consumed a whole shelf and everything after it went to a second sheet. But
    the skin only uses 1211 of the shelf's 2435 LENGTH, and the 1222 x 1216
    region beside it holds six wall pieces stacked. The tool said two sheets of
    25 mm where one does, on a sheet costing $245.

    So: FREE RECTANGLES, split guillotine-style after each placement. Still not
    optimal - it never merges free rectangles back together - but it sees the
    space beside a tall part, which shelves cannot.
    """
    usable_w, usable_l = sw - 2 * EDGE_TRIM, sl - 2 * EDGE_TRIM
    flat = []
    for name, a, b, qty, _t in pieces:
        for _ in range(qty):
            flat.append((name, max(a, b), min(a, b)))
    # Biggest first by area: a guillotine packer wants the awkward parts placed
    # while the sheet is still whole.
    flat.sort(key=lambda p: -(p[1] * p[2]))

    for name, lng, shrt in flat:
        # A piece must fit some way round on a bare sheet at all. REPORT THE
        # SHORTFALL, not just the refusal: "over by 2.8" is a decision he can
        # make - a sheet may run oversize - where a bare "will not fit" is not.
        if not ((lng <= usable_l and shrt <= usable_w)
                or (lng <= usable_w and shrt <= usable_l)):
            over = min(max(lng - usable_l, shrt - usable_w),
                       max(lng - usable_w, shrt - usable_l))
            return None, f"{name}, over by {over:.2f}"

    out = []
    sheets = [[(0.0, 0.0, usable_l, usable_w)]]      # free rects per sheet
    for name, lng, shrt in flat:
        best = None                                  # (sheet, rect idx, w, h)
        for si, free in enumerate(sheets):
            for ri, (fx, fy, fw, fh) in enumerate(free):
                for w, h in ((lng, shrt), (shrt, lng)):
                    if w <= fw + 1e-9 and h <= fh + 1e-9:
                        # SHORTEST LEFTOVER SIDE: prefer the rect that leaves
                        # the least awkward offcut, not the first that fits.
                        waste = min(fw - w, fh - h)
                        if best is None or waste < best[0]:
                            best = (waste, si, ri, w, h)
        if best is None:
            sheets.append([(0.0, 0.0, usable_l, usable_w)])
            si, ri = len(sheets) - 1, 0
            w, h = (lng, shrt) if lng <= usable_l else (shrt, lng)
        else:
            _waste, si, ri, w, h = best
        fx, fy, fw, fh = sheets[si].pop(ri)
        out.append((si, fx, fy, w, h, name))
        # Guillotine split: the strip to the right of the piece, and the strip
        # above the whole rect. Kerf comes off both new rects.
        if fw - w - KERF > 0:
            sheets[si].append((fx + w + KERF, fy, fw - w - KERF, h))
        if fh - h - KERF > 0:
            sheets[si].append((fx, fy + h + KERF, fw, fh - h - KERF))
    return out, None


def tightest(pieces, sw, sl):
    """The least spare any part has against the sheet's NARROW dimension.

    PASS/FAIL IS NOT ENOUGH HERE. The skins clear a 4 ft sheet by a few
    millimetres, so whether that sheet arrives on size matters more than the
    sheet count does - and a number he can check against the delivered board is
    the only form of that warning worth printing.
    """
    usable_w, usable_l = sw - 2 * EDGE_TRIM, sl - 2 * EDGE_TRIM
    best, who = None, ""
    for name, a, b, qty, _t in pieces:
        lng, shrt = max(a, b), min(a, b)
        spare = max(usable_w - shrt if lng <= usable_l else -1e9,
                    usable_w - lng if shrt <= usable_l else -1e9)
        if best is None or spare < best:
            best, who = spare, name
    return best, who


def nest_svg(places, sw, sl, colours, s=0.105):
    """One SVG per sheet, to scale, sheet length running left to right.

    THE TRIM BORDER IS DRAWN as a dashed line inside the sheet edge, because the
    whole 4 x 8 answer turns on how much comes off those edges - a nesting
    picture that hid it would hide the one assumption worth seeing.
    """
    by_sheet = {}
    for sheet, x, y, w, h, name in places:
        by_sheet.setdefault(sheet, []).append((x, y, w, h, name))
    svgs = []
    for sheet in sorted(by_sheet):
        pw, ph, t = sl * s, sw * s, EDGE_TRIM * s
        body = [f'<rect x="0" y="0" width="{pw:.1f}" height="{ph:.1f}" '
                f'fill="#fcfcfc" stroke="#777"/>',
                f'<rect x="{t:.1f}" y="{t:.1f}" width="{pw - 2 * t:.1f}" '
                f'height="{ph - 2 * t:.1f}" fill="none" stroke="#c00" '
                f'stroke-dasharray="4 3" stroke-width="0.7"/>']
        for x, y, w, h, name in sorted(by_sheet[sheet], key=lambda p: (p[1], p[0])):
            px, py, ww, hh = t + x * s, t + y * s, w * s, h * s
            body.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{ww:.1f}" '
                        f'height="{hh:.1f}" fill="{colours[name]}" '
                        f'stroke="#333" stroke-width="0.6"/>')
            if hh > 9 and ww > 40:
                body.append(
                    f'<text x="{px + ww / 2:.1f}" y="{py + hh / 2 + 2.6:.1f}" '
                    f'text-anchor="middle" font-size="7">{name}'
                    f'<tspan font-size="5.5" fill="#555">  {w:.0f}&#215;{h:.0f}'
                    f'</tspan></text>')
        svgs.append((sheet + 1,
                     f'<svg viewBox="0 0 {pw:.1f} {ph:.1f}" width="100%" '
                     f'style="max-width:{pw:.0f}px">{"".join(body)}</svg>'))
    return svgs


def sand_ports(v):
    """Centres of the sand ports, one per bay, as a list along one edge.

    Both skins get the same grid and the box is square, so one row of figures
    serves X and Y on both parts. The steps are not equal - the end bays are
    wider - which is exactly the kind of thing that gets walked as a constant
    pitch by hand and comes out wrong at the far end.
    """
    first, step, end = (v["SAND_PORT_FIRST"], v["SAND_PORT_STEP"],
                        v["SAND_PORT_STEP_END"])
    n = int(v["BOX_RIBS_FORE_AFT"]) + 1
    at, pos = [first], first
    for i in range(n - 1):
        pos += end if i in (0, n - 2) else step
        at.append(pos)
    # The row is symmetric about the cavity's centre, so the last port must sit
    # as far in from the far edge as the first does from the near one.
    assert abs((v["BOX_W"] - at[-1]) - first) < 1e-6, (
        f"sand ports run {at} on a {v['BOX_W']:g} skin - not symmetric")
    off = [p for p in at if abs(p * 2 - round(p * 2)) > 1e-9]
    assert not off, f"sand port centres not on a half millimetre - {off}"
    return at


def main():
    global KERF, EDGE_TRIM
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--kerf", type=float, default=KERF,
                    help=f"saw kerf between parts, mm (default {KERF})")
    ap.add_argument("--trim", type=float, default=EDGE_TRIM,
                    help=f"taken off each factory edge, mm (default {EDGE_TRIM})")
    ap.add_argument("--sheet", default="4 x 8",
                    help='which sheet size to DRAW the nesting for')
    a = ap.parse_args()
    KERF, EDGE_TRIM = a.kerf, a.trim

    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        return 2
    v = {s: reg.value(s) for s in reg.order}

    all_parts = parts(v)
    colours = {p[0]: PALETTE[i % len(PALETTE)] for i, p in enumerate(all_parts)}
    by_t = {}
    for p in all_parts:
        by_t.setdefault(round(p[4], 3), []).append(p)

    print("TORSION BOX CUT LIST\n")
    rows_html = []
    for t in sorted(by_t, reverse=True):
        print(f"  --- {t:g} mm ---")
        for name, aa, bb, qty, _ in by_t[t]:
            print(f"    {name:22s} {aa:9.2f} x {bb:7.2f}   x{qty}")
            rows_html.append((t, name, aa, bb, qty))
        print()

    print(f"SHEETS NEEDED - kerf {KERF:g}, edge trim {EDGE_TRIM:g} "
          f"(guillotine-packed, an UPPER bound)\n")
    summary, nests = [], []
    for label, sw, sl in SHEETS:
        print(f"  {label} ({sw:g} x {sl:g})")
        total, ok = 0, True
        for t in sorted(by_t, reverse=True):
            places, fail = pack(by_t[t], sw, sl)
            if places is None:
                print(f"    {t:g} mm : DOES NOT FIT - {fail}")
                ok = False
                summary.append((label, t, None, fail))
                continue
            n = max(p[0] for p in places) + 1
            tight, part = tightest(by_t[t], sw, sl)
            print(f"    {t:g} mm : {n} sheet(s)   tightest {tight:.2f} spare"
                  f"  ({part})")
            total += n
            summary.append((label, t, n, None))
            if label == a.sheet:
                for num, svg in nest_svg(places, sw, sl, colours):
                    nests.append((t, num, svg))
        print(f"    total   : {total} sheet(s)" if ok else "    total   : n/a")
        print()

    runs = notch_runs(v)
    print(f"NOTCHES - {v['T_BB_RIB']:g} wide, "
          f"{v['BOX_RIB_H'] / 2:g} deep, from each end of the piece\n")
    for part, length, bay, end, starts in runs:
        print(f"  {part:16s} {length:7.0f} long, {end:g} end bays, "
              f"{bay:g} inner")
        print("    starts  " + "  ".join(f"{s:6.0f}" for s in starts))
    print()

    ports = sand_ports(v)
    print(f"SAND PORTS - {v['SAND_PORT_D']:g} through both skins, "
          f"{len(ports)} x {len(ports)} = {len(ports) ** 2} per skin\n")
    print("  centres, same in X and Y  "
          + "  ".join(f"{p:g}" for p in ports) + "\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows_html, summary, nests, a.sheet, v, runs, ports),
                   encoding="utf-8")
    print("wrote", OUT.relative_to(HERE.parent))
    return 0


def render(rows, summary, nests, drawn, v, runs, ports):
    th, last_t = [], None
    for t, name, a, b, qty in rows:
        if t != last_t:
            th.append(f'<tr class="grp"><td colspan="4">{t:g} mm</td></tr>')
            last_t = t
        th.append(f"<tr><td>{name}</td><td class=n>{a:.1f}</td>"
                  f"<td class=n>{b:.1f}</td><td class=n>{qty}</td></tr>")
    sh = []
    for label, t, n, fail in summary:
        cell = (f"{n} sheet(s)" if n
                else f'<b class="bad">will not fit</b> &mdash; {fail}')
        sh.append(f"<tr><td>{label}</td><td class=n>{t:g} mm</td><td>{cell}</td></tr>")
    ns = [f'<div class="nest"><h3>{t:g} mm &mdash; sheet {num}</h3>{svg}</div>'
          for t, num, svg in nests]

    rib, half = v["T_BB_RIB"], v["BOX_RIB_H"] / 2
    nt = []
    for part, length, bay, end, starts in runs:
        hd = "".join(f"<th>{i + 1}</th>" for i in range(len(starts)))
        st = "".join(f"<td class=n>{s:g}</td>" for s in starts)
        en = "".join(f"<td class=n>{s + rib:g}</td>" for s in starts)
        nt.append(
            f"<h3>{part} &mdash; {length:g} long, {len(starts)} notches</h3>"
            f"{notch_svg(length, starts, rib, v['BOX_RIB_H'])}"
            f"<table><tr><th>Notch</th>{hd}</tr>"
            f"<tr><td>Start</td>{st}</tr>"
            f"<tr><td>End</td>{en}</tr></table>"
            f"<p>Bay at each end <b>{end:g}</b>, the three between notches "
            f"<b>{bay:g}</b>. Notch <b>{rib:g}</b> wide, <b>{half:g}</b> deep. "
            f"Every figure a whole millimetre.</p>")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>CNCBuild &mdash; Torsion Box Cut List</title>
<style>
 @page {{ size: letter portrait; margin: 14mm; }}
 body {{ font: 10.5pt "Segoe UI", sans-serif; color: #111; max-width: 190mm; }}
 h1 {{ font-size: 15pt; margin: 0 0 2mm; }}
 h2 {{ font-size: 12pt; margin: 7mm 0 2mm; border-bottom: 1px solid #bbb; }}
 h3 {{ font-size: 10pt; margin: 4mm 0 1mm; color: #444; }}
 table {{ border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; }}
 td, th {{ border: 1px solid #ccc; padding: 1.4mm 2.2mm; }}
 th {{ background: #eee; text-align: left; }}
 td.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
 tr.grp td {{ background: #f3f3f3; font-weight: 600; }}
 .bad {{ color: #a00; }}
 .note {{ background: #fff8e1; border-left: 3px solid #e0a800;
          padding: 2mm 3mm; margin: 3mm 0; }}
 .nest {{ page-break-inside: avoid; margin: 0 0 4mm; }}
</style></head><body>
<h1>Torsion box &mdash; cut list</h1>
<p>Box <b>{v['BOX_W']:.2f}</b> across by <b>{v['BOX_FORE_AFT']:.0f}</b> front to
back, <b>{v['BOX_THK']:.0f}</b> deep. All sizes in mm.</p>

<div class="note"><b>These are the sheets in hand</b> &mdash; {v['T_BB_SKIN_TOP']:g} and
{v['T_BB_SKIN_BOT']:g}, micced to five thousandths. Sheet sold at a nominal
commonly runs under and varies between sheets, so <b>still test-cut one notch on
scrap from the same sheet</b> before cutting the set.</div>

<h2>Parts</h2>
<table><tr><th>Part</th><th>Long</th><th>Short</th><th>Off</th></tr>
{''.join(th)}</table>

<h2>Sheets</h2>
<p>Guillotine-packed with a <b>{KERF:g} mm</b> kerf and <b>{EDGE_TRIM:g} mm</b> off
each factory edge &mdash; a Festool track saw on Baltic birch, which is all that
gets removed. <b>The counts are an upper bound</b>: offcuts are never merged
back together, so a careful nest can still do better.</p>
<table><tr><th>Sheet</th><th>Thickness</th><th>Needs</th></tr>
{''.join(sh)}</table>

<h2>Nesting &mdash; {drawn}</h2>
<p>To scale, sheet length left to right. The dashed red line is the
<b>{EDGE_TRIM:g} mm</b> off each factory edge; everything sits inside it.
Offcut is whatever stays white.</p>
{''.join(ns)}

<h2>Sand ports</h2>
<p><b>{v['SAND_PORT_D']:g} through both skins, {len(ports)} &times; {len(ports)} =
{len(ports) ** 2} in each</b>, one centred in every bay. Centres from the skin's
edge, <b>the same figures in X and Y</b> &mdash; the box is square and the grid is
the same both ways:</p>
<table><tr><th>Port</th>{''.join(f'<th>{i + 1}</th>' for i in range(len(ports)))}</tr>
<tr><td>Centre</td>{''.join(f'<td class=n>{p:g}</td>' for p in ports)}</tr></table>
<p><b>The steps are not equal</b> &mdash; {v['SAND_PORT_STEP_END']:g} at each end of
the row and {v['SAND_PORT_STEP']:g} through the middle, because the end bays are
wider. Walking it as a constant pitch puts the far port in the wrong place.</p>
<p>The bottom port takes a rubber cork with <b>{v['SAND_PORT_CHAIN_L']:g}</b> of
<b>stainless or brass</b> chain, fitted <b>before the top skin goes on</b>. Fill
through the top: fish the chain up with a magnet on a rod, tape it to the skin,
pour the bay full, untape and let it fall on the sand. Drain by pushing the cork
<b>up from below with a stick</b>, and reseat it from above with a
<b>{v['SAND_PORT_DOWEL']:g}</b> dowel.</p>
<p>The tee track bed covers all but the <b>front row</b> of five, which lands on
the open apron. <b>{v['T_APRON_SKIN']:g} Baltic birch over the apron on
double-sided tape</b> covers those &mdash; a cover, not structure, so it comes off
the day a port is used.</p>

<h2>Not on this list</h2>
<p><b>The two blocks beside the back centre tenon.</b> They are location pieces
inside the box, carry no load, and their thickness is free &mdash; so they come
out of the scrap bin rather than off a sheet. They must be <b>{v['BOX_RIB_H']:.0f}
tall</b> like a rib so both skins glue to them, and no thicker than
<b>{v['BACK_TENON_BLOCK_T_MAX']:.1f}</b>, which is the clear space each side of
the tenon.</p>

<h2>Notches</h2>
<p>Egg crate, continuous both ways, half-depth notches at every crossing. Every
notch is <b>{rib:g} wide</b> and <b>{half:g} deep</b>, and all the ribs of one
direction are identical &mdash; so the saw is set once per direction and the
whole set runs through it.</p>
<p>Notch depth <b>exactly half</b> &mdash; a set cut slightly deep sits low and
loses contact with a skin along its whole length. The fit is a slip fit, not a
clearance: too tight splits the rib, too loose leaves no glue line.</p>
<p><b>One direction is notched from the top edge and the other from the bottom</b>,
and whichever way round you choose, keep it the same for every rib in that
direction. Positions below are from either end of the piece &mdash; the run is
symmetric, so a rib fitted backwards still fits.</p>
{''.join(nt)}
<p>Notch the bottom edge of every rib where it meets the bottom skin, roughly
20 &times; 15, so the sand can migrate between cells.</p>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
