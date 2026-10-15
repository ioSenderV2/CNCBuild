#!/usr/bin/env python3
"""Base Construction - every piece of the base, generated from the registry.

The torsion box has its own document; this is the part that holds it up, and it
comes FIRST: the base locates the three legs the box lands on, so it is built
before the box and the legs before it.

    python tools/make-base-doc.py [--kerf 1.6] [--trim 1.6]

Writes machine/drawings/base-construction.html and prints the sheet summary.

WHY IT SHARES make-box-doc's PACKER rather than carrying its own: the two
documents answer the same question about the same sheets, and a second copy of a
guillotine packer is a second thing to be wrong. Imported by path because the
module name has a hyphen in it.

MATERIAL ALREADY COMMITTED, his 2026-10-15: one sheet of 18 is bought and cut
into 20 strips of 90, which is exactly the five legs. What this list counts is
everything else.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from dims import Registry                                    # noqa: E402

_spec = importlib.util.spec_from_file_location("boxdoc", HERE / "make-box-doc.py")
boxdoc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(boxdoc)

OUT = HERE.parent / "machine" / "drawings" / "base-construction.html"
SHEETS = boxdoc.SHEETS

# His, 2026-10-15: the legs are already cut, so they are listed for the record
# but they are NOT in the sheet count - that sheet is spent.
STRIPS_CUT = 20
ON_5x5 = "5 x 5"                  # the two central wall laminations, and only those


def parts(v):
    """Every piece of the base, as (name, long, short, qty, sheet, note).

    Sizes are registry expressions, never literals. Where a piece is one
    lamination of a 36 member it is listed as 18, because that is what gets cut.

    `sheet` is WHICH SHEET IT COMES OFF - his nest, 2026-10-15, not the packer's.
    A piece marked "cut" or "offcut" needs no sheet at all.
    """
    t = v["T_BB_SKIN_BOT"]                      # 18, the sheet everything is
    gm_h, gm_t = v["GRID_MEMBER_H"], v["GRID_MEMBER_T"]
    return [
        ("Leg strip, box legs", v["LEG_L_BOX"], 90, 12, "cut",
         "4 per leg, 3 legs - laminate then trim to "
         f"{v['POST_W_X']:g} x {v['POST_W_Y']:g}"),
        ("Leg strip, rear corner legs", v["LEG_L_REAR"], 90, 8, "cut",
         "4 per leg, 2 legs - same trim, no tenon"),
        ("Shear wall, back", v["BACK_WALL_L"], v["WALL_H"], 1, "1",
         f"ONE sheet {t:g} thick - it replaces the back cross rails at both "
         "grids, so it must not be cut into strips"),
        ("Rail, front cross - outer", v["RAIL_CROSS_OUTER_L"], gm_h, 2, "1",
         "one per grid, FULL WIDTH - this is the half housed in the legs"),
        ("Rail, front cross - inner", v["RAIL_CROSS_INNER_L"], gm_h, 2, "1",
         "one per grid - it spans between the front legs and is housed in "
         "nothing"),
        ("Rail, fore-aft", v["RAIL_FORE_AFT_L"], gm_h, 8, "2",
         f"2 laminations each, 4 rails - it fills the legs' {gm_t:g} slot"),
        ("Shear wall, central", v["CENTRE_WALL_L"], v["CENTRE_WALL_H"], 2, "3",
         f"2 laminations - it fills the rear middle leg's slot, so it is "
         f"{gm_t:g}. Notched at BOTH front corners, {gm_t / 2:g} across by "
         f"{gm_h:g} up. Cut {v['WALL_H'] - v['CENTRE_WALL_H']:g} shorter than "
         f"the back wall so both come off ONE 5 x 5"),
        ("Leg filler", v["BASE_VOLUME_H"], v["POST_W_Y"], 8, "offcut",
         f"2 laminations each, 4 legs - {v['POST_W_Y']:g} deep in the front "
         f"legs and {v['POST_W_Y'] - v['T_BACK_WALL']:g} in the rear ones. "
         "HIS, and it costs no sheet: the leg strips are already 90 wide and "
         "long enough to give these out of what is left past the leg lengths"),
    ]


# Which sheet is which, and his reason for each. Sheets 1 and 2 are deliberately
# loaded on the LEFT ONLY so the right of each stays one whole offcut rather
# than a fringe of strips - that is worth more than a tighter nest.
SHEET_PLAN = [
    ("0", "4 x 8", "20 leg strips - ALREADY CUT, and the fillers and spacers "
                   "come out of what is left"),
    ("1", "4 x 8", "the back wall and both front cross rails"),
    ("2", "4 x 8", "the eight fore-aft rail laminations"),
    ("3", "5 x 5", "both central wall laminations"),
]


def layout(v, num, sw, sl):
    """HIS nest, placed explicitly rather than packed.

    A packer optimises for area and will scatter pieces down a sheet to save a
    few millimetres; he wants each sheet loaded from the LEFT so what is left is
    one whole offcut. On sheet 1 the packer put the two inner rails out at
    x 1260 and left 60 of length - the same pieces stacked under the outer rails
    leave 1176 in one piece. So the placements are stated, and checked instead.

    Returns [(sheet, x, y, w, h, name)] in the packer's own format, with x along
    the sheet's LENGTH, both measured from inside the trim.
    """
    k, usable_w = boxdoc.KERF, sw - 2 * boxdoc.EDGE_TRIM
    gm_h = v["GRID_MEMBER_H"]
    out, y = [], 0.0

    def row(name, w, h, n=1, x=0.0):
        nonlocal y
        for _ in range(n):
            out.append((0, x, y, w, h, name))
            y += h + k

    if num == "0":
        for i in range(STRIPS_CUT):
            out.append((0, i * (90 + k), 0.0, 90.0, usable_w, "Leg strip"))
    elif num == "1":
        row("Shear wall, back", v["BACK_WALL_L"], v["WALL_H"])
        row("Rail, front cross - outer", v["RAIL_CROSS_OUTER_L"], gm_h, 2)
        row("Rail, front cross - inner", v["RAIL_CROSS_INNER_L"], gm_h, 2)
    elif num == "2":
        row("Rail, fore-aft", v["RAIL_FORE_AFT_L"], gm_h, 8)
    elif num == "3":
        row("Shear wall, central", v["CENTRE_WALL_L"], v["CENTRE_WALL_H"], 2)

    # CHECKED, because a stated nest has no packer to prove it fits. Bounds
    # first, then every pair - the whole point of writing the placements down
    # is that the arithmetic can be wrong and look fine on a drawing.
    usable_l = sl - 2 * boxdoc.EDGE_TRIM
    for _, x, yy, w, h, name in out:
        assert x + w <= usable_l + 1e-9 and yy + h <= usable_w + 1e-9, (
            f"sheet {num}: {name} at {x:.1f},{yy:.1f} runs off a "
            f"{usable_l:.1f} x {usable_w:.1f} sheet")
    for i, (_, ax, ay, aw, ah, an) in enumerate(out):
        for _, bx, by, bw, bh, bn in out[i + 1:]:
            if ax < bx + bw - 1e-9 and bx < ax + aw - 1e-9 \
               and ay < by + bh - 1e-9 and by < ay + ah - 1e-9:
                raise AssertionError(f"sheet {num}: {an} overlaps {bn}")
    return out


def notches(v, name, L, H):
    """Notch rectangles in a piece's OWN coordinates, L along, H across.

    Only the central wall carries any: everything else on these sheets is a
    plain rectangle, because the legs' housings and rebates are cut after
    lamination and never appear on a sheet.
    """
    if not name.startswith("Shear wall, central"):
        return []
    n, d = v["GRID_MEMBER_T"] / 2, v["GRID_MEMBER_H"]
    return [(L - n, 0, n, d), (L - n, H - d, n, d)]      # both front corners


def nest_svg(v, places, sw, sl, colours, s=0.105):
    """Same picture as the box document's, with the notches dotted on.

    A notch is drawn rather than left to the parts table because it is the one
    thing on a cut list that is easy to forget until the piece is already cut -
    and it is at the END of the longest piece on the sheet.
    """
    by_sheet = {}
    for sheet, x, y, w, h, name in places:
        by_sheet.setdefault(sheet, []).append((x, y, w, h, name))
    out = []
    for sheet in sorted(by_sheet):
        pw, ph, t = sl * s, sw * s, boxdoc.EDGE_TRIM * s
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
            # the piece's own L is whichever of w/h is its long side as cut
            L, H = (w, h) if w >= h else (h, w)
            for nx, ny, nw, nh in notches(v, name, L, H):
                # map part coords onto the sheet, allowing for the packer
                # having turned the piece to make it fit
                ax, ay, aw, ah = ((nx, ny, nw, nh) if w >= h
                                  else (ny, nx, nh, nw))
                body.append(
                    f'<rect x="{px + ax * s:.2f}" y="{py + ay * s:.2f}" '
                    f'width="{aw * s:.2f}" height="{ah * s:.2f}" fill="none" '
                    f'stroke="#c00" stroke-width="0.8" stroke-dasharray="3 2"/>')
            if hh > 9 and ww > 40:
                body.append(
                    f'<text x="{px + ww / 2:.1f}" y="{py + hh / 2 + 2.6:.1f}" '
                    f'text-anchor="middle" font-size="7">{name}'
                    f'<tspan font-size="5.5" fill="#555">  {w:.0f}&#215;{h:.0f}'
                    f'</tspan></text>')
        out.append((sheet + 1,
                    f'<svg viewBox="0 0 {pw:.1f} {ph:.1f}" width="100%" '
                    f'style="max-width:{pw:.0f}px">{"".join(body)}</svg>'))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--kerf", type=float, default=boxdoc.KERF)
    ap.add_argument("--trim", type=float, default=boxdoc.EDGE_TRIM)
    a = ap.parse_args()
    boxdoc.KERF, boxdoc.EDGE_TRIM = a.kerf, a.trim

    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        return 2
    v = {s: reg.value(s) for s in reg.order}

    all_parts = parts(v)

    print("BASE CONSTRUCTION\n")
    for name, lng, shrt, qty, sheet, _ in all_parts:
        where = {"cut": "already cut", "offcut": "from the leg offcut"}.get(
            sheet, f"sheet {sheet}")
        print(f"  {name:30s} {lng:8.0f} x {shrt:6.0f}   x{qty:<3} {where}")
    print(f"\n  {STRIPS_CUT} leg strips are ALREADY CUT from a sheet of "
          f"{v['T_BB_SKIN_BOT']:g} - that sheet is spent, and the fillers come "
          f"out of what is left past the leg lengths.\n")

    print(f"SHEETS - kerf {boxdoc.KERF:g}, edge trim {boxdoc.EDGE_TRIM:g}\n")
    # ONE PACK PER NAMED SHEET, not one pack across all of them. The nest is
    # HIS, 2026-10-15, and packing each sheet alone is what keeps the right of
    # sheets 1 and 2 as a single whole offcut instead of a fringe of strips.
    summary, nests = [], []
    t = v["T_BB_SKIN_BOT"]
    sizes = {label: (sw, sl) for label, sw, sl in SHEETS}
    colours = {p[0]: boxdoc.PALETTE[i % len(boxdoc.PALETTE)]
               for i, p in enumerate(all_parts)}
    colours["Leg strip"] = boxdoc.PALETTE[2]
    for num, size, why in SHEET_PLAN:
        sw, sl = sizes[size]
        places = layout(v, num, sw, sl)
        used = max(x + w for _, x, _, w, _, _ in places)
        left = sl - 2 * boxdoc.EDGE_TRIM - used
        print(f"  sheet {num} ({size}, {sw:g} x {sl:g}): {why}")
        print(f"      {left:.0f} of length left whole")
        summary.append((num, size, why, left, None))
        nests += [(f"Sheet {num} &mdash; {size}", svg)
                  for _, svg in nest_svg(v, places, sw, sl, colours)]
    print()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(all_parts, summary, v, nests), encoding="utf-8")
    print("wrote", OUT.relative_to(HERE.parent))
    return 0


def render(rows, summary, v, nests):
    where = {"cut": "<b>already cut</b>", "offcut": "<b>leg offcut</b>"}
    pr = "".join(
        f"<tr><td>{n}</td><td class=n>{lng:g}</td><td class=n>{shrt:g}</td>"
        f"<td class=n>{qty}</td><td>{where.get(sheet, f'sheet {sheet}')}</td>"
        f"<td class=s>{note}</td></tr>"
        for n, lng, shrt, qty, sheet, note in rows)
    sh = "".join(
        f"<tr><td><b>{num}</b></td><td>{size}</td><td>{why}</td>"
        f"<td class=n>{f'{left:.0f}' if bad is None else '&mdash;'}</td>"
        f"<td class=s>{'' if bad is None else f'<b class=bad>{bad}</b>'}</td></tr>"
        for num, size, why, left, bad in summary)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>CNCBuild &mdash; Base Construction</title>
<style>
 @page {{ size: letter portrait; margin: 14mm; }}
 body {{ font: 10.5pt "Segoe UI", sans-serif; color: #111; max-width: 190mm; }}
 h1 {{ font-size: 15pt; margin: 0 0 2mm; }}
 h2 {{ font-size: 12pt; margin: 7mm 0 2mm; border-bottom: 1px solid #bbb; }}
 table {{ border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; }}
 td, th {{ border: 1px solid #ccc; padding: 1.4mm 2.2mm; vertical-align: top; }}
 th {{ background: #eee; text-align: left; }}
 td.n {{ text-align: right; font-variant-numeric: tabular-nums; }}
 td.s {{ font-size: 9pt; color: #444; }}
 .bad {{ color: #a00; }}
 .note {{ background: #fff8e1; border-left: 3px solid #e0a800;
          padding: 2mm 3mm; margin: 3mm 0; }}
</style></head><body>
<h1>Base Construction</h1>
<p><b>Two grids that locate and constrain all five legs</b>, three of which the
box lands on. <b>It is built BEFORE the box, and the legs before it</b> &mdash;
the box cannot be lowered onto tenons that are not located yet. All sizes in mm,
all generated from the dimension registry.</p>

<div class="note"><b>One sheet of {v['T_BB_SKIN_BOT']:g} is already cut into
{20} strips of 90</b>, which is exactly the five legs. <b>That sheet is spent</b>
and the sheet count below is for everything else. <b>The offcut past the leg
lengths is the test material and the slot spacers</b> &mdash; a spacer cut from
the stock that will fill the slot is a slot that fits by construction.</div>

<h2>1 &mdash; Parts</h2>
<table><tr><th>Piece</th><th>Long</th><th>Short</th><th>Off</th><th>From</th>
<th>Notes</th></tr>
{pr}</table>
<p><b>Every 36 member is two laminations of {v['T_BB_SKIN_BOT']:g}</b>, listed
here as the {v['T_BB_SKIN_BOT']:g} pieces that actually get cut. The
{v['GRID_MEMBER_T']:g} is not a choice &mdash; it is what fills a leg's slot,
which is the middle two laminations of a four-strip leg.</p>

<h2>2 &mdash; Three sheets</h2>
<p><b>Each piece is assigned to a named sheet, and each sheet is packed on its
own.</b> Sheets 1 and 2 are loaded from the <b>left only</b>, so what is left of
each stays <b>one whole offcut</b> rather than a fringe of strips &mdash; worth
more than a tighter nest.</p>
<table><tr><th>Sheet</th><th>Size</th><th>Carrying</th>
<th>Length left whole</th><th></th></tr>{sh}</table>
<p>🔴 <b>The two central laminations come off ONE 5 &times; 5, and that is what
cutting them {v['WALL_H'] - v['CENTRE_WALL_H']:g} shorter than the back wall
buys.</b> A 5 &times; 5 trims to <b>1520.8</b>, and with the
<b>{boxdoc.KERF:g}</b> kerf between the two pieces each may be at most
<b>759.6</b> tall. At the back wall's {v['WALL_H']:g} they would take two sheets;
at {v['CENTRE_WALL_H']:g} they take one. <b>Four off would have missed it by
0.4</b> &mdash; the kerf is the whole margin there.</p>
<p><b>Anything else that turns out to be wanted comes out of sheet 3's waste</b>
&mdash; his call. Worth knowing when reaching for it: sheet 3 leaves
<b>298 &times; 1521</b>, where <b>sheet 2 leaves 1212 &times; 1216</b> and sheet 1
<b>1176 &times; 1216</b>, so sheet 3's is the one to spend and the other two are
the ones to keep whole.</p>
<p><b>Sheet 0 is the one already cut</b>, drawn so the record is complete: 20
strips of 90 taken across its width, leaving <b>605</b> of length. That remainder
is the test material, the slot spacers and all eight leg fillers.</p>

<h2>3 &mdash; The cuts, sheet by sheet</h2>
<p>To scale, sheet length left to right. The dashed red border is the
<b>{boxdoc.EDGE_TRIM:g}</b> off each factory edge; everything sits inside it, and
offcut is whatever stays white. <b>Every sheet is loaded from the left</b>, so
the white is one piece. <b>Notches are drawn as dotted rectangles</b> &mdash;
they are the one thing on a cut list easy to miss until the piece is already cut,
and here they sit at the far END of the longest piece on sheet 3.</p>
<p>These placements are <b>stated, not packed</b>, and they are <b>checked</b>:
every piece is tested against the sheet's usable size and against every other
piece, so a nest that does not fit fails the build rather than printing.</p>
{''.join(f'<h3>{n}</h3>{svg}' for n, svg in nests)}

<h2>4 &mdash; How it goes together</h2>
<table>
<tr><th>Joint</th><th>How</th></tr>
<tr><td><b>Fore-aft rails to legs</b></td><td>They fill the legs' middle slot
&mdash; the two centre laminations. One slot per leg carries the lower rail, the
upper rail, the filler between them, and in the rear middle leg the central
wall</td></tr>
<tr><td><b>Front cross rails to legs</b></td><td>Outer {v['GRID_MEMBER_T'] / 2:g}
housed in a notch in the legs' front faces, full width; inner
{v['GRID_MEMBER_T'] / 2:g} spanning between them, housed in nothing</td></tr>
<tr><td><b>Fore-aft meets cross, inside a leg</b></td><td><b>The cross rail
wins</b> and the fore-aft rails butt its inner face. The cross rail has to be
continuous: the central wall's notch rides over it</td></tr>
<tr><td><b>Central wall at the front</b></td><td>Notched at <b>both</b> front
corners, {v['GRID_MEMBER_T']:g} across by {v['GRID_MEMBER_H']:g} up, one per
grid. The lower notch sits on its rail; two long screws through each rail into
the wall's end</td></tr>
<tr><td><b>Central wall at the back</b></td><td>It slides into the rear middle
leg's slot &mdash; the space its own two laminations would have filled</td></tr>
<tr><td><b>Back wall</b></td><td>In a full-height rebate
{v['T_BACK_WALL']:g} deep in the rear legs, but <b>only in the strips it passes
through</b>. Each corner leg's outermost lamination stays its full
{v['POST_W_Y']:g}, and the wall stops one lamination short at each end so its end
grain butts the back of it</td></tr>
</table>
<p>🔴 <b>One rule covers all of it: every rail stays whole and whatever meets it
gives way.</b> The only cutting a rail ever takes is screw holes.</p>

<h2>5 &mdash; Order</h2>
<ol>
<li><b>Laminate all five legs, with a spacer in every slot.</b> Cut each spacer
from the stock that will fill that slot, wax or tape it so it does not glue in,
and run it the full depth so the outer strips cannot bow inward under clamps.</li>
<li><b>Trim the legs to {v['POST_W_X']:g} &times; {v['POST_W_Y']:g}</b> after the
glue dries, and cut them to length &mdash; <b>measuring from the mortise</b>, not
from an end, so the floor end takes the error.</li>
<li><b>Cut the ledges and tenons</b> on the three box legs.</li>
<li><b>Build the two grids around the legs</b>, then the two shear walls.</li>
<li><b>Only then the box.</b></li>
</ol>
<p><b>The mortise heights have to agree across the legs</b> or the frame sits
twisted &mdash; lay all five up on one flat surface with the spacers set off a
single stop.</p>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
