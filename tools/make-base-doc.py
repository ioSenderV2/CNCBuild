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
        ("Shear wall, central", v["CENTRE_WALL_L"], v["WALL_H"], 2,
         f"2 laminations - it fills the rear middle leg's slot, so it is "
         f"{gm_t:g}. Notched at BOTH front corners, {gm_t:g} across by "
         f"{gm_h:g} up"),
        ("Leg filler, front legs", v["BASE_VOLUME_H"], v["POST_W_Y"], 4,
         "2 laminations each, 2 legs - it closes the slot between the grids"),
        ("Leg filler, rear legs", v["BASE_VOLUME_H"],
         v["POST_W_Y"] - v["T_BACK_WALL"], 4,
         "2 laminations each, 2 legs - shallower, because the back wall takes "
         f"the slot's back {v['T_BACK_WALL']:g}"),
    ]


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
    summary = []
    pieces = [(n, lng, shrt, qty, v["T_BB_SKIN_BOT"]) for n, lng, shrt, qty, _ in to_cut]
    for label, sw, sl in SHEETS:
        places, fail = boxdoc.pack(pieces, sw, sl)
        if places is None:
            print(f"  {label}: DOES NOT FIT - {fail}")
            summary.append((label, None, fail))
            continue
        n = max(p[0] for p in places) + 1
        tight, part = boxdoc.tightest(pieces, sw, sl)
        print(f"  {label} ({sw:g} x {sl:g}) : {n} sheet(s)   tightest "
              f"{tight:.2f} spare  ({part})")
        summary.append((label, n, None))
    print()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(all_parts, summary, v), encoding="utf-8")
    print("wrote", OUT.relative_to(HERE.parent))
    return 0


def render(rows, summary, v):
    pr = "".join(
        f"<tr><td>{n}</td><td class=n>{lng:g}</td><td class=n>{shrt:g}</td>"
        f"<td class=n>{qty}</td><td class=s>{note}</td></tr>"
        for n, lng, shrt, qty, note in rows)
    sh = "".join(
        f"<tr><td>{label}</td><td>{f'{n} sheet(s)' if n else f'<b class=bad>will not fit</b> &mdash; {fail}'}</td></tr>"
        for label, n, fail in summary)
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
<table><tr><th>Sheet</th><th>Needs</th></tr>{sh}</table>
<p>🔴 <b>Three sheets, and it is the walls that decide it &mdash; not waste,
geometry.</b> Each wall is {v['WALL_H']:g} wide, so it has to lie with its length
along the sheet. <b>Two of them want {v['CENTRE_WALL_L'] * 2:g} of a
2435 sheet and come up 47 short</b>, and the back wall will not share either, by
29. So each of the three wall pieces takes its own sheet &mdash; and the
{1216 - v['WALL_H']:g} &times; 2435 left beside each one is where every rail and
filler comes from, which is why three sheets covers the whole base.</p>
<p>The figure to know if this is ever re-cut: <b>two walls share a sheet only if
they come under about 1216 long</b>, and the central one is
{v['CENTRE_WALL_L']:g}.</p>

<h2>3 &mdash; How it goes together</h2>
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

<h2>4 &mdash; Order</h2>
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
