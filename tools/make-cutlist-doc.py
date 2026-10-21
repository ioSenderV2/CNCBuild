#!/usr/bin/env python3
"""The base's cutlist and its sheet layout, as their own document.

    python tools/make-cutlist-doc.py

Writes machine/drawings/base-cutlist.html.

WHY IT IS SEPARATE from base-construction.html: that document is about how the
base GOES TOGETHER, and a cutlist is read at a different moment, by somebody
standing at a sheet rather than at the frame. They were one document and the
nest pages sat in the middle of the assembly order.

EACH GROUP IS AN ASSEMBLY GROUP - his. A group therefore carries every piece
that goes INTO that assembly, internals included, rather than every piece that
happens to share a shape: the rear corner legs' fillers and foot spacers are
listed under the legs, the caster blocks under the two things they bear on.

NOTHING IS TREATED AS ALREADY CUT. The sheet count is worked out from zero.

THE ONE FIXED SHEET IS HIS: one 5 x 5 carries the two central shear wall
laminations and nothing else, because at CENTRE_WALL_H both come off one.
"""
from __future__ import annotations

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

OUT = HERE.parent / "machine" / "drawings" / "base-cutlist.html"

STRIP_W = 90.0          # a leg strip is RIPPED at 90 and trimmed to 86 dry

# How much of a band's depth a piece must use before it may ride in that band
# rather than wait for one of its own. See the fill loop in bands() for what
# this is worth - at 1.0 nothing shares a band with anything shorter, at 0.0
# the first deep band swallows the width every later piece needed.
BAND_FILL = 0.7
SHEET_48 = ("4 x 8", 1219.2, 2438.4)
SHEET_55 = ("5 x 5", 1524.0, 1524.0)


def groups(v):
    """His assembly groups, each with every piece that goes into it.

    Sizes are registry values, never literals. A piece that is one lamination
    of a 36 member is listed at 18, because that is what gets cut.
    """
    gm_h = v["GRID_MEMBER_H"]
    shoulder = v["LEG_L_BOX"] - v["POST_TENON_L"]
    return [
        ("Front corner legs", 2,
         "They carry no tenon and the box must NOT land on them: each stops "
         "level with the upper grid's top, and the front cross rail's outer "
         "lamination is housed in the inner strip at each grid.",
         [("Leg strip", v["LEG_L_SHORT"], STRIP_W, 4,
           f"2 per leg. Inner strip takes an {v['T_BACK_WALL']:g} x "
           f"{v['GRID_MEMBER_H']:g} notch in its front edge at each grid; the "
           "outboard strip stays whole"),
          ("Leg filler", v["BASE_VOLUME_H"], STRIP_W, 4,
           f"2 per leg, closing the slot between the grids, "
           f"{v['POST_W_Y']:g} deep"),
          ("Foot spacer", v["FOOT_SPACER_H"], STRIP_W, 4,
           "2 per leg, closing the slot from the floor up to the lower rail. "
           "It is what the leg stands on")]),
        ("Three bearing legs", 3,
         "The box lands on these and nowhere else. TWO KINDS UNDER ONE "
         "HEADING: a rear corner leg is ledged on two faces, so its outboard "
         "strip stops at the shoulder and its tenon is one tab on the inner "
         "strip; the front centre leg is ledged on its front face only, so "
         "both strips run full length and the slot splits its tenon into two "
         "tabs.",
         [("Leg strip, full length", v["LEG_L_BOX"], STRIP_W, 4,
           "both strips of the front centre leg, and the INNER strip of each "
           "rear leg"),
          ("Leg strip, rear outboard", shoulder, STRIP_W, 2,
           "one per rear leg, and it is shorter: the side ledge is "
           f"{v['T_BOX_LEDGE']:g} deep across an {v['LEG_STRIP']:g} strip, so "
           "it swallows that strip whole and its top face IS the bearing "
           "shoulder"),
          ("Leg filler, rear legs", v["BASE_VOLUME_H"], STRIP_W, 4,
           f"2 per rear leg. Trim to "
           f"{v['POST_W_Y'] - v['T_BACK_WALL']:g} deep - the back wall takes "
           "the slot's back 18. The front centre leg gets none, the central "
           "wall fills its slot"),
          ("Foot spacer", v["FOOT_SPACER_H"], STRIP_W, 6,
           "2 per leg, all three"),
          ("Tenon corner spacer", v["POST_TENON_L"], v["TENON_CORNER_Y"], 2,
           f"the two REAR legs, and it is {v['TENON_SPACER_GAP']:g} stock, "
           "not 18 - glued to the OUTER face of the tenon tab")]),
        ("Back centre leg", 1,
         "What holds the central wall's back end, and the back wall runs "
         "straight through it. No tenon, so it stops level with the upper "
         "grid's top like the front corner pair. It takes NO FILLER, because "
         "the wall fills its slot.",
         [("Leg strip", v["LEG_L_SHORT"], STRIP_W, 2,
           f"BOTH rebated {v['T_BACK_WALL']:g} deep their whole height in the "
           "BACK face, for the back wall running through"),
          ("Foot spacer", v["FOOT_SPACER_H"], STRIP_W, 2,
           "closing the slot from the floor up to the lower rail")]),
        ("Lower fore-aft rails", 2,
         "Four laminations, not two: the inner pair passes through the legs' "
         "slot and a pad is added each side, butting the leg's face because "
         "it cannot pass through. The pads are what the caster plates bolt "
         "into.",
         [("Rail lamination", v["RAIL_FORE_AFT_L"], gm_h, 4,
           "2 per rail, filling the legs' "
           f"{v['GRID_MEMBER_T']:g} slot"),
          ("Outer pad", v["RAIL_LOWER_PAD_L"], gm_h, 4,
           "one each side of each rail, bringing it out to "
           f"{v['POST_W_X']:g} so all four bolts of a "
           f"{v['CASTER_PLATE_L']:g} x {v['CASTER_PLATE_W']:g} caster plate "
           "land in solid rail, the plate standing 7 proud each side"),
          ("Caster plate", v["CASTER_PLATE_L"], v["CASTER_PLATE_W"], 4,
           "one per corner caster, bearing on the rail's underside and butted "
           f"against a corner leg's face. {v['CASTER_PLATE_T']:g} THICK, all "
           "five the same piece - the caster's own plate bolts to it")]),
        ("Upper fore-aft rails", 2,
         "Two laminations only - the pads are what feed the casters and "
         "there are none up here.",
         [("Rail lamination", v["RAIL_FORE_AFT_L"], gm_h, 4, "2 per rail")]),
        ("Front cross rail, lower", 1,
         "One rail, two laminations doing different jobs.",
         [("Outer, housed in the legs", v["RAIL_CROSS_OUTER_L"], gm_h, 1,
           "full width, housed 18 deep in the front faces of the legs' inner "
           "strips, and it stops one lamination short at each end so the "
           "outermost strip covers its end grain"),
          ("Inner, in two spans", v["RAIL_CROSS_INNER_SPAN"], gm_h, 2,
           "TWO pieces, not one: the front centre leg stands in the middle of "
           "this lamination's run, so each piece goes from a corner leg to "
           "that leg. Housed in nothing - it butts a leg's face at each "
           "end")]),
        ("Front cross rail, upper", 1,
         "The same two pieces again.",
         [("Outer, housed in the legs", v["RAIL_CROSS_OUTER_L"], gm_h, 1,
           "as the lower"),
          ("Inner, in two spans", v["RAIL_CROSS_INNER_SPAN"], gm_h, 2,
           "as the lower")]),
        ("Rear shear wall", 1,
         "It replaces the back cross rails at BOTH grids, so it must not be "
         "cut into strips - and it is glued and screwed to all three rear "
         "legs, which is what makes the back a single assembly.",
         [("Wall, one sheet", v["BACK_WALL_L"], v["WALL_H"], 1,
           "CUT TO THE SHEET: its length is the sheet's full usable width, so "
           "the two cuts that trim the long edges are its two ends. It stops "
           f"{v['BASE_BOX_GAP']:g} shy of the box")]),
        ("Central shear wall", 1,
         "Two laminations filling both centre legs' slots, dry-fitted and "
         "bolted. It ties the front and back assemblies together with the "
         "fore-aft rails.",
         [("Wall lamination", v["CENTRE_WALL_L"], v["CENTRE_WALL_H"], 2,
           "a plain rectangle, no notches anywhere - the front cross rail's "
           "inner lamination butts the front centre leg in two spans instead "
           "of running past the wall"),
          ("Lower band pad", v["CENTRE_WALL_PAD_L"], gm_h, 2,
           "one each side, flush with the wall's bottom edge. It brings the "
           f"wall out to {v['POST_W_X']:g} for the centre caster's plate, and "
           "its top edge is level with the lower grid's top"),
          ("Caster plate", v["CASTER_PLATE_L"], v["CASTER_PLATE_W"], 1,
           "the fifth plate, bearing on this wall's bottom edge and butted "
           "against the back of the front centre leg")]),
    ]


# ---------------------------------------------------------------- the nest

def bands(pieces, usable_l, usable_w, reserve_first=None):
    """Left-loaded bands: fill across the width, then step along the length.

    NOT A PACKER'S NEST, DELIBERATELY. A packer sorts by area and scatters
    pieces down a sheet to save a few millimetres; what is wanted is each
    sheet loaded from ONE END so the remainder is one whole offcut rather than
    a fringe of strips. So pieces go down in the order given, a band is as
    deep as the longest piece in it, and a band closes when the next piece
    will not fit across what is left of the width.

    `reserve_first` is a piece that must have a band of its own with nothing
    beside it - the rear shear wall, whose length IS the sheet's usable width
    and so leaves no room for a neighbour.

    Returns (placed, leftover_length) where placed is
    [(x, y, w, h, name)] with y along the sheet's LENGTH.
    """
    k = boxdoc.KERF
    placed, y = [], 0.0

    def fits(length):
        return y + length <= usable_l + 1e-9

    if reserve_first is not None:
        name, lng, wide = reserve_first
        if not (wide <= usable_l + 1e-9 and lng <= usable_w + 1e-9):
            raise SystemExit("%s does not fit a bare sheet" % name)
        placed.append((0.0, y, lng, wide, name))
        y += wide + k

    queue = list(pieces)
    while queue:
        # open a band on the longest piece still waiting that will fit
        lead = next((i for i, p in enumerate(queue) if fits(p[1])), None)
        if lead is None:
            return placed, usable_l - y, queue
        name, lng, wide = queue.pop(lead)
        band_h, x = lng, 0.0
        placed.append((x, y, wide, band_h, name))
        x += wide + k
        # fill across the width - but only with pieces that nearly FILL the
        # band's depth. A band costs its leader's whole length, so a piece
        # much shorter than that spends full width to use part of the depth
        # and the difference is dead. One 564 filler riding in an 864 band
        # that way cost a whole fourth sheet: it took the width a leg strip
        # wanted, and the eighth filler then had no band deep enough left.
        # Below the threshold a piece waits and leads a band of its own, where
        # its own kind packs beside it at full efficiency.
        i = 0
        while i < len(queue):
            n2, l2, w2 = queue[i]
            if (l2 >= BAND_FILL * band_h and l2 <= band_h + 1e-9
                    and x + w2 <= usable_w + 1e-9):
                placed.append((x, y, w2, l2, n2))
                x += w2 + k
                queue.pop(i)
            else:
                i += 1
        y += band_h + k
    return placed, usable_l - y, []


def nest(v, gs):
    """The three sheets, and which pieces fall on each.

    ORDER IS THE WHOLE DESIGN HERE: the wall takes its reserved band, then the
    long rail-width pieces, then the leg strips and the short stuff, so the
    offcut that survives is at one end and in one piece.
    """
    trim = boxdoc.EDGE_TRIM
    _n48, w48, l48 = SHEET_48
    _n55, w55, l55 = SHEET_55
    uw48, ul48 = w48 - 2 * trim, l48 - 2 * trim
    uw55, ul55 = w55 - 2 * trim, l55 - 2 * trim

    flat = []
    for gname, _qty, _why, rows in gs:
        for name, a, b, q, _note in rows:
            for _ in range(q):
                flat.append(("%s / %s" % (gname, name), a, b))

    def take(pred):
        got = [p for p in flat if pred(p)]
        for p in got:
            flat.remove(p)
        return got

    # the 5 x 5, and only the two wall laminations
    wall_lams = take(lambda p: p[0].endswith("Wall lamination"))
    s55, left55, over55 = bands(wall_lams, ul55, uw55)
    if over55:
        raise SystemExit("the 5 x 5 will not take both wall laminations")

    # THE 4 x 8s GO THROUGH make-box-doc.py's GUILLOTINE PACKER, not through
    # bands(). Bands load from one end and leave the remainder in one piece,
    # which is what he wants - but this set is mixed enough that bands cost a
    # WHOLE EXTRA SHEET for it, and the sheet is the expensive thing. Measured:
    # the guillotine packs it on two, bands wanted three plus a near-empty one.
    # bands() is kept for the 5 x 5, where two pieces make the question moot.
    #
    # WHAT IS GIVEN UP, and it is worth saying: the offcut is no longer a
    # single rectangle. A nest placed by hand can have both - that is how the
    # old one did it - and this is the honest machine answer rather than a
    # claim to match it.
    counted = {}
    for name, a, b in flat:
        counted[(name, a, b)] = counted.get((name, a, b), 0) + 1
    pieces = [(n, a, b, q, "") for (n, a, b), q in counted.items()]
    flat.clear()
    out, err = boxdoc.pack(pieces, w48, l48)
    if err:
        raise SystemExit("a 4 x 8 will not take it: %s" % err)

    # AXES SWAP ON THE WAY IN, and the nest checker is what caught it missing.
    # boxdoc.pack works with x along the sheet's LENGTH and y across its WIDTH;
    # everything here is the other way round, x across the width and y along
    # the length, because that is how these sheets are drawn. Taken straight,
    # a 1223 rail came back at x 765.6 on a 1216-wide sheet - off the edge, and
    # the drawing looked plausible.
    sheets = []
    for si in range(max(p[0] for p in out) + 1):
        placed = [(fy, fx, h, w, name)
                  for s_i, fx, fy, w, h, name in out if s_i == si]
        used = max(y + ph for _x, y, _pw, ph, _n in placed)
        sheets.append((placed, ul48 - used))
    return (s55, left55), sheets, (uw48, ul48), (uw55, ul55)


# ---------------------------------------------------------------- rendering

def sheet_svg(placed, usable_w, usable_l, left, s=0.072):
    """One sheet, pieces drawn where they fall, offcut shaded."""
    pad = 16.0
    w = pad * 2 + usable_w * s
    h = pad * 2 + usable_l * s
    out = [f'<rect x="{pad}" y="{pad}" width="{usable_w * s:.1f}" '
           f'height="{usable_l * s:.1f}" fill="#fff" stroke="#111" '
           f'stroke-width="1"/>']
    if left > 1:
        out.append(f'<rect x="{pad}" y="{pad + (usable_l - left) * s:.1f}" '
                   f'width="{usable_w * s:.1f}" height="{left * s:.1f}" '
                   f'fill="#eef3ee" stroke="#9b9" stroke-width="0.6" '
                   f'stroke-dasharray="4 3"/>')
        out.append(f'<text x="{pad + usable_w * s / 2:.1f}" '
                   f'y="{pad + (usable_l - left / 2) * s:.1f}" '
                   f'text-anchor="middle" font-size="7" fill="#476">'
                   f'{left:.0f} x {usable_w:.0f} past the last cut</text>')
    for x, y, pw, ph, name in placed:
        short = name.split(" / ")[-1]
        out.append(f'<rect x="{pad + x * s:.2f}" y="{pad + y * s:.2f}" '
                   f'width="{pw * s:.2f}" height="{ph * s:.2f}" '
                   f'fill="#dfe8f4" stroke="#36506e" stroke-width="0.5"/>')
        if pw * s > 7 and ph * s > 16:
            out.append(
                f'<text x="{pad + (x + pw / 2) * s:.2f}" '
                f'y="{pad + (y + ph / 2) * s:.2f}" text-anchor="middle" '
                f'font-size="5.2" transform="rotate(-90 '
                f'{pad + (x + pw / 2) * s:.2f} '
                f'{pad + (y + ph / 2) * s:.2f})">{short}</text>')
    return (f'<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w * 1.6:.0f}" '
            f'style="max-width:100%">{"".join(out)}</svg>')


def render(v, gs, five, fours, u48, u55):
    s55, left55 = five
    rows = []
    total = 0
    for gname, qty, why, pieces in gs:
        n = sum(p[3] for p in pieces)
        total += n
        rows.append(
            f'<tr class="g"><td colspan="4"><b>{gname}</b>'
            + (f' &mdash; {qty} of them' if qty > 1 else '')
            + f'<div class="why">{why}</div></td></tr>')
        for name, a, b, q, note in pieces:
            rows.append(
                f'<tr><td>{name}</td>'
                f'<td class="n">{a:g} &times; {b:g}</td>'
                f'<td class="n"><b>{q}</b></td>'
                f'<td class="note">{note}</td></tr>')

    sheet_blocks = [
        '<h2>Sheet 1 &mdash; 5 &times; 5, the central wall and nothing else</h2>'
        '<p>Both laminations come off one sheet, which is the reason the '
        f'central wall is cut {v["WALL_H"] - v["CENTRE_WALL_H"]:g} shorter '
        'than the rear one.</p>'
        + sheet_svg(s55, u55[0], u55[1], left55)]
    for i, (placed, left) in enumerate(fours, start=2):
        sheet_blocks.append(
            f'<h2>Sheet {i} &mdash; 4 &times; 8</h2>'
            + sheet_svg(placed, u48[0], u48[1], left))

    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>CNCBuild &mdash; Base cutlist and sheet layout</title>
<style>
 @page {{ size: letter portrait; margin: 14mm; }}
 body {{ font: 10.5pt/1.4 "Segoe UI", system-ui, sans-serif; color: #111;
        max-width: 190mm; margin: 0 auto; }}
 h1 {{ font-size: 19pt; margin: 0 0 1mm; }}
 h2 {{ font-size: 13pt; margin: 7mm 0 1mm; border-bottom: 2px solid #111;
       padding-bottom: 1mm; page-break-after: avoid; }}
 .sub {{ color: #555; margin: 0 0 4mm; }}
 table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt;
          margin: 2mm 0 4mm; }}
 th, td {{ border: 1px solid #999; padding: 1.3mm 2mm; text-align: left;
           vertical-align: top; }}
 td.n {{ text-align: right; white-space: nowrap; }}
 td.note {{ color: #444; font-size: 9pt; }}
 tr.g td {{ background: #eef1f5; }}
 .why {{ color: #444; font-weight: 400; font-size: 9pt; margin-top: 0.7mm; }}
 .box {{ border: 1px solid #c9c9c9; border-left: 5px solid #555;
         background: #fafafa; padding: .7rem .9rem; margin: 3mm 0; }}
 svg {{ margin: 2mm 0 4mm; }}
</style>
</head><body>

<h1>Base &mdash; sheet layout</h1>
<p class="sub"><b>{total} pieces off {1 + len(fours)} sheets of
{v["T_BB_SKIN_BOT"]:g} mm Baltic birch.</b> Millimetres throughout. <b>Which
sheet each piece comes off</b>, and nothing else &mdash; the parts list is
chapter 1 of <a href="base-construction.html">base-construction.html</a>.</p>

<div class="box">
<b>Leg strips are ripped at {STRIP_W:g} and trimmed to {v["POST_W_Y"]:g} once
the lamination is dry</b>, so every piece cut from strip stock &mdash; fillers
and foot spacers included &mdash; is listed at {STRIP_W:g} wide.
<br><br>
<b>The glue-up spacers are not in this list.</b> One set holds a leg's slot
open while it is clamped and comes straight back out to be used on the next
leg, so it is one set cut from rail offcut, waxed or taped, not a part of the
base.
<br><br>
<b>Kerf {boxdoc.KERF:g}, edge trim {boxdoc.EDGE_TRIM:g}</b> &mdash; one pass
off a factory edge and nothing more, so a usable 4 &times; 8 is
{u48[0]:g} &times; {u48[1]:g}.
</div>

<p><b>The parts list is not here</b> &mdash; it is chapter 1 of
<a href="base-construction.html">base-construction.html</a>, grouped by
assembly, because that is where it gets read. <b>This document is the sheets</b>:
which one each piece comes off.</p>

<h2>How it divides across the sheets</h2>
<p><b>Packed for the fewest sheets, not for a tidy offcut.</b> Loading each
sheet from one end keeps the remainder in a single piece, which is worth having
&mdash; but on this mix it cost <b>a whole extra sheet</b>, and the sheet is the
expensive thing. So the placements below are the packer's, the offcut comes back
as several pieces rather than one, and <b>a nest you place by hand can beat both</b>.</p>
<p>&#128308; <b>The rear shear wall takes a band of its own with nothing beside
it.</b> Its {v["BACK_WALL_L"]:g} length IS the sheet's usable width, so there
is no room for a neighbour and its two ends are the trim cuts.</p>

{''.join(sheet_blocks)}

</body></html>
'''


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

    gs = groups(v)
    five, fours, u48, u55 = nest(v, gs)
    OUT.write_text(render(v, gs, five, fours, u48, u55), encoding="utf-8")

    pieces = sum(p[3] for _g, _q, _w, rows in gs for p in rows)
    print("OK  %s  %d pieces, %d sheet(s): one %s and %d x %s"
          % (OUT.name, pieces, 1 + len(fours), SHEET_55[0], len(fours),
             SHEET_48[0]))
    for i, (placed, left) in enumerate(fours, start=2):
        print("    sheet %d: %2d pieces, %.0f x %.0f past the last cut"
              % (i, len(placed), left, u48[0]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
