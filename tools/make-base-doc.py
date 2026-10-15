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
    """Every piece of the base, as (name, long, short, qty, note).

    Sizes are registry expressions, never literals. Where a piece is one
    lamination of a 36 member it is listed as 18, because that is what gets cut.
    """
    t = v["T_BB_SKIN_BOT"]                      # 18, the sheet everything is
    gm_h, gm_t = v["GRID_MEMBER_H"], v["GRID_MEMBER_T"]
    strip = v["LEG_STRIP"]
    return [
        ("Leg strip, box legs", v["LEG_L_BOX"], 90, 12,
         "4 per leg, 3 legs - laminate then trim to "
         f"{v['POST_W_X']:g} x {v['POST_W_Y']:g}"),
        ("Leg strip, rear corner legs", v["LEG_L_REAR"], 90, 8,
         "4 per leg, 2 legs - same trim, no tenon"),
        ("Rail, fore-aft", v["RAIL_FORE_AFT_L"], gm_h, 8,
         f"2 laminations each, 4 rails - it fills the legs' {gm_t:g} slot"),
        ("Rail, front cross - outer", v["RAIL_CROSS_OUTER_L"], gm_h, 2,
         "one per grid, FULL WIDTH - this is the half housed in the legs"),
        ("Rail, front cross - inner", v["RAIL_CROSS_INNER_L"], gm_h, 2,
         "one per grid - it spans between the front legs and is housed in "
         "nothing"),
        ("Shear wall, back", v["BACK_WALL_L"], v["WALL_H"], 1,
         f"ONE sheet {t:g} thick - it replaces the back cross rails at both "
         "grids, so it must not be cut into strips"),
        ("Shear wall, central", v["CENTRE_WALL_L"], v["CENTRE_WALL_H"], 2,
         f"2 laminations - it fills the rear middle leg's slot, so it is "
         f"{gm_t:g}. Notched at BOTH front corners, {gm_t / 2:g} across by "
         f"{gm_h:g} up. Cut {v['WALL_H'] - v['CENTRE_WALL_H']:g} shorter than "
         f"the back wall so both come off ONE 5 x 5"),
        ("Leg filler, front legs", v["BASE_VOLUME_H"], v["POST_W_Y"], 4,
         "2 laminations each, 2 legs - it closes the slot between the grids"),
        ("Leg filler, rear legs", v["BASE_VOLUME_H"],
         v["POST_W_Y"] - v["T_BACK_WALL"], 4,
         "2 laminations each, 2 legs - shallower, because the back wall takes "
         f"the slot's back {v['T_BACK_WALL']:g}"),
    ]


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
    # The legs are already cut from a sheet that is spent, so they are shown
    # and then set aside - counting them again would ask for a sheet he has.
    to_cut = [p for p in all_parts if not p[0].startswith("Leg strip")]

    print("BASE CONSTRUCTION\n")
    for name, lng, shrt, qty, _ in all_parts:
        print(f"  {name:30s} {lng:8.0f} x {shrt:6.0f}   x{qty}")
    print(f"\n  {STRIPS_CUT} leg strips are ALREADY CUT from a sheet of "
          f"{v['T_BB_SKIN_BOT']:g} - that sheet is spent.\n")

    print(f"SHEETS FOR THE REST - kerf {boxdoc.KERF:g}, edge trim "
          f"{boxdoc.EDGE_TRIM:g} (guillotine-packed, an UPPER bound)\n")
    # EACH PIECE IS ASSIGNED TO A SHEET SIZE, not packed against both - his
    # plan, 2026-10-15: the two central laminations come off one 5 x 5, which is
    # what shrinking them by 6 bought, and everything else off 4 x 8s.
    summary, nests = [], []
    t = v["T_BB_SKIN_BOT"]
    groups = {}
    for n, lng, shrt, qty, _ in to_cut:
        groups.setdefault(ON_5x5 if n.startswith("Shear wall, central")
                          else "4 x 8", []).append((n, lng, shrt, qty, t))
    colours = {p[0]: boxdoc.PALETTE[i % len(boxdoc.PALETTE)]
               for i, p in enumerate(to_cut)}
    for label, sw, sl in SHEETS:
        pieces = groups.get(label)
        if not pieces:
            continue
        places, fail = boxdoc.pack(pieces, sw, sl)
        if places is None:
            print(f"  {label}: DOES NOT FIT - {fail}")
            summary.append((label, None, fail, []))
            continue
        n = max(p[0] for p in places) + 1
        tight, part = boxdoc.tightest(pieces, sw, sl)
        print(f"  {label} ({sw:g} x {sl:g}) : {n} sheet(s)   tightest "
              f"{tight:.2f} spare  ({part})")
        summary.append((label, n, None, [p[0] for p in pieces]))
        nests += [(f"{label}, sheet {i}", svg)
                  for i, svg in nest_svg(v, places, sw, sl, colours)]
    print()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(all_parts, summary, v, nests), encoding="utf-8")
    print("wrote", OUT.relative_to(HERE.parent))
    return 0


def render(rows, summary, v, nests):
    pr = "".join(
        f"<tr><td>{n}</td><td class=n>{lng:g}</td><td class=n>{shrt:g}</td>"
        f"<td class=n>{qty}</td><td class=s>{note}</td></tr>"
        for n, lng, shrt, qty, note in rows)
    sh = "".join(
        f"<tr><td>{label}</td>"
        f"<td>{f'{n} sheet(s)' if n else f'<b class=bad>will not fit</b> &mdash; {fail}'}</td>"
        f"<td class=s>{', '.join(sorted(set(names)))}</td></tr>"
        for label, n, fail, names in summary)
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
<table><tr><th>Piece</th><th>Long</th><th>Short</th><th>Off</th><th>Notes</th></tr>
{pr}</table>
<p><b>Every 36 member is two laminations of {v['T_BB_SKIN_BOT']:g}</b>, listed
here as the {v['T_BB_SKIN_BOT']:g} pieces that actually get cut. The
{v['GRID_MEMBER_T']:g} is not a choice &mdash; it is what fills a leg's slot,
which is the middle two laminations of a four-strip leg.</p>

<h2>2 &mdash; Sheets for the rest</h2>
<p><b>Each piece is assigned to a sheet size rather than packed against both.</b></p>
<table><tr><th>Sheet</th><th>Needs</th><th>Carrying</th></tr>{sh}</table>
<p>🔴 <b>The two central laminations come off ONE 5 &times; 5, and that is what
cutting them {v['WALL_H'] - v['CENTRE_WALL_H']:g} shorter than the back wall
buys.</b> A 5 &times; 5 trims to <b>1520.8</b>, and with the
<b>{boxdoc.KERF:g}</b> kerf between the two pieces each may be at most
<b>759.6</b> tall. At the back wall's {v['WALL_H']:g} they take two sheets; at
{v['CENTRE_WALL_H']:g} they take one, with 1.6 to spare. <b>Four would have
missed it by 0.4</b> &mdash; the kerf is the whole margin here.</p>
<p>On the 4 &times; 8 it is the back wall that sets the count: it is
{v['WALL_H']:g} wide so it lies along the sheet, and nothing else that long will
share the remaining {2435 - v['BACK_WALL_L']:g}. <b>The fore-aft rails and the
rest come out of the {1216 - v['WALL_H']:g} &times; 2435 beside it.</b></p>

<h2>3 &mdash; The cuts, sheet by sheet</h2>
<p>To scale, sheet length left to right. The dashed red
border is the <b>{boxdoc.EDGE_TRIM:g}</b> off each factory edge; everything sits
inside it, and offcut is whatever stays white. <b>Notches are drawn as dotted
rectangles</b> &mdash; they are the one thing on a cut list that is easy to miss
until the piece is already cut, and on this sheet they sit at the far END of the
longest piece.</p>
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
