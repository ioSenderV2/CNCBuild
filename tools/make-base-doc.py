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
        ("Leg foot spacer", v["FOOT_SPACER_H"], v["POST_W_Y"], 10, "offcut",
         "2 laminations each, all FIVE legs - glued to the inside of the outer "
         "lamination, closing the slot from the floor up to the lower rail. "
         f"Its {v['FOOT_SPACER_H']:g} is BASE_FLOOR_CLEAR, which is exactly "
         "what the slot leaves open down there. It is what the leg stands on"),
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


# ---- the five legs, strip by strip ------------------------------------------
# HIS ASK, 2026-10-15: show which four pieces make up each leg's lamination, and
# show WHICH BLOCKS IN THE SLOT COME BACK OUT. That second half is the one thing
# a parts list cannot say. Three of the blocks glued into a leg stay there for
# good and three come out at base assembly and are replaced by a rail or a wall,
# and they are the same 36 x 86 plywood as each other - so on the bench, with
# five legs lying there, nothing distinguishes a filler that is structure from a
# spacer that is scaffolding except this drawing.
#
# THE STACK IS NOT INVENTED AND IT IS NOT APPROXIMATE - it is how BASE_VOLUME_H
# is derived, read back the other way, so it sums to the leg's own length
# exactly and `leg_bands` asserts that it does:
#
#     100 foot spacer + 100 lower rail + 564 filler + 100 upper rail + 10 gap
#       = 874 = LEG_L_REAR, a rear corner leg
#     ... + 116 tenon = 990 = LEG_L_BOX, a leg the box lands on
#
# Colours are the 3D MODEL'S colours, deliberately: a reader with the model open
# should see the same brown leg, blue fore-aft rail and tan central wall here.
LEG_BROWN, REAR_BROWN = "#7A5230", "#8A5A2B"
RAIL_BLUE, WALL_TAN, BACK_ORANGE = "#3C7DA5", "#C9A66B", "#D4793B"
OPEN_GREY = "#f2f2f2"


def _tint(hexrgb, f=0.72):
    """Lighten a model colour, for a block that is only a PLACEHOLDER for it.

    A spacer is drawn in a washed-out version of what replaces it, so the
    drawing says "this becomes that" without a second legend to look up.
    """
    r, g, b = (int(hexrgb[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(int(c + (255 - c) * f) for c in (r, g, b))


def leg_bands(v, kind):
    """One leg's slot, floor up, as (code, height, piece, deep, fate, becomes).

    `fate` is the whole point: "stays" is glued in for good, "out" is a glue-up
    spacer that is removed at base assembly, "open" is slot that nothing ever
    fills. `becomes` names what takes an "out" band's place.

    Checked against the leg's own length, because this stack and LEG_L_BOX come
    from opposite directions and the only thing that proves they agree is the
    sum.
    """
    gm_h, gm_t, pwy = v["GRID_MEMBER_H"], v["GRID_MEMBER_T"], v["POST_W_Y"]
    deep_rear = pwy - v["T_BACK_WALL"]          # the back 18 is the back wall's
    foot = ("A", v["FOOT_SPACER_H"], "Leg foot spacer", pwy, "stays", "")
    gap = ("E", v["BASE_BOX_GAP"], "open &mdash; the gap under the box", pwy,
           "open", "")
    tenon = ("F", v["POST_TENON_L"], "open &mdash; through shoulder and tenon",
             pwy, "open", "")

    def rail(which):
        return ("B", gm_h, "Glue-up spacer", pwy, "out",
                f"the {which} fore-aft rail")

    if kind == "front":
        bands = [foot, rail("lower"),
                 ("C", v["BASE_VOLUME_H"], "Leg filler", pwy, "stays", ""),
                 rail("upper"), gap, tenon]
        total = v["LEG_L_BOX"]
    elif kind == "rear-corner":
        bands = [foot, rail("lower"),
                 ("C", v["BASE_VOLUME_H"], "Leg filler", deep_rear, "stays", ""),
                 rail("upper"), gap]
        total = v["LEG_L_REAR"]
    else:                                        # the rear centre leg
        bands = [foot,
                 ("D", v["WALL_H"], "Glue-up spacer", pwy, "out",
                  "the central wall in the front "
                  f"{deep_rear:g}, the back wall in the back "
                  f"{v['T_BACK_WALL']:g}"),
                 gap, tenon]
        total = v["LEG_L_BOX"]
    assert abs(sum(b[1] for b in bands) - total) < 1e-9, (
        f"{kind}: the slot stack sums to {sum(b[1] for b in bands):g} and the "
        f"leg is {total:g} - one of the two is wrong")
    return bands


def leg_kinds(v):
    """The five legs as the three kinds they actually come in.

    Named by where they stand, because that is how they get picked up off the
    bench. The box lands on front left, front right and back centre; the two
    rear corner legs carry the grids and the back wall and NOT the box.
    """
    pwy, bw, strip = v["POST_W_Y"], v["T_BACK_WALL"], v["LEG_STRIP"]
    return [
        ("front", "Front left, front right", 2, v["LEG_L_BOX"], LEG_BROWN,
         f"one {strip:g} &times; {v['TENON_CORNER']:g} tab, on the inner strip",
         f"ledged {v['T_BOX_LEDGE']:g} on the side face and the front face",
         f"front face of the INNER strip notched {bw:g} deep at both rail "
         f"bands, for the cross rail's outer lamination"),
        ("rear-corner", "Rear left, rear right", 2, v["LEG_L_REAR"], REAR_BROWN,
         "none &mdash; the box does not land on it", "no ledge",
         f"back face of the INNER strip rebated {bw:g} deep its whole height, "
         f"for the back wall"),
        ("rear-centre", "Back centre", 1, v["LEG_L_BOX"], LEG_BROWN,
         f"two {strip:g} &times; {v['TENON_CORNER']:g} tabs, "
         f"{v['GRID_MEMBER_T']:g} apart",
         f"ledged {v['T_BOX_LEDGE']:g} on the back face only",
         f"BOTH strips rebated {bw:g} deep their whole height &mdash; the back "
         f"wall runs straight through this leg"),
    ]


def leg_elevation_svg(v, s=0.165):
    """All five legs in one elevation, floor at the bottom, to one scale.

    WHY ONE DRAWING AND NOT FIVE: the band heights are the same across the
    legs, so five separate drawings would repeat one height axis five times and
    make the one real difference - the back centre leg carrying a wall where
    the others carry two rails and a filler - the hardest thing to see.

    A leg is drawn as its FOUR STRIPS: the outer pair full height, and the
    middle 36 drawn as the slot stack. Hatched, dashed-outline bands come out.
    """
    pwx, strip, gm_t = v["POST_W_X"], v["LEG_STRIP"], v["GRID_MEMBER_T"]
    kinds = leg_kinds(v)
    # NAMED FOR ITSELF, NOT FOR ITS KIND: a leg gets picked up off the bench by
    # where it stands, and "front, 2 off" is the one label that does not help
    # when four of the five look identical.
    names = ["Front left", "Front right", "Rear left", "Rear right",
             "Back centre"]
    legs = list(zip(names, [k for kind, _, n, *_ in kinds
                            for k in [kind] * n]))
    assert len(legs) == len(names), "five legs, and the kinds must cover them"

    # THE PITCH IS IN DRAWN UNITS, NOT IN MILLIMETRES OF LEG. Written as
    # pwx + 46 it spaced five 9-unit legs 118 units apart and they came out as
    # hairlines with a page of white between them.
    tall = max(v["LEG_L_BOX"], v["LEG_L_REAR"])
    pitch, pad_l, pad_r, pad_t, pad_b = pwx * s + 32, 15.0, 48.0, 13.0, 15.0
    w = pad_l + pitch * len(legs) + pad_r
    h = pad_t + tall * s + pad_b
    body = []

    # the height axis: every station a leg is set out from, and they are the
    # base's own elevation - the one table this document did not have
    def y_of(z):
        return pad_t + (tall - z) * s

    # THE STATION NAME GOES AT THE FAR RIGHT, NOT BESIDE THE NUMBER. Run
    # together as one string they were wider than the left margin and the
    # NUMBER is the half that got clipped - "upper grid under" printed with
    # nothing to say which height it was.
    #
    # AND THE TEXT IS PUSHED CLEAR OF ITS NEIGHBOUR. Two stations are
    # BASE_BOX_GAP apart, which at this scale is under two units, so 864 and
    # 874 printed on top of each other and neither could be read. The rule
    # stays on the station; only the label moves.
    stations = [(0, "floor"), (v["FOOT_SPACER_H"], "lower grid under"),
                (v["FOOT_SPACER_H"] + v["GRID_MEMBER_H"], "lower grid top"),
                (v["LEG_L_REAR"] - v["BASE_BOX_GAP"] - v["GRID_MEMBER_H"],
                 "upper grid under"),
                (v["LEG_L_REAR"] - v["BASE_BOX_GAP"], "upper grid top"),
                (v["LEG_L_REAR"], "box underside"),
                (v["LEG_L_BOX"], "leg top")]
    label_y, floor_y = {}, None
    for z, _ in sorted(stations, key=lambda p: -p[0]):      # top of the leg down
        y = y_of(z)
        if floor_y is not None and y < floor_y + 5.2:
            y = floor_y + 5.2
        label_y[z] = floor_y = y
    for z, what in stations:
        y = y_of(z)
        body.append(f'<line x1="{pad_l:.1f}" y1="{y:.1f}" '
                    f'x2="{w - pad_r + 6:.1f}" y2="{y:.1f}" stroke="#ccc" '
                    f'stroke-width="0.4" stroke-dasharray="2 2"/>')
        body.append(f'<text x="{pad_l - 1.5:.1f}" y="{label_y[z] + 1.7:.1f}" '
                    f'text-anchor="end" font-size="4.6" fill="#555">'
                    f'{z:g}</text>')
        body.append(f'<text x="{w - pad_r + 8:.1f}" y="{label_y[z] + 1.4:.1f}" '
                    f'font-size="3.8" fill="#888">{what}</text>')

    for i, (name, kind) in enumerate(legs):
        x0 = pad_l + i * pitch
        bands = leg_bands(v, kind)
        total = sum(b[1] for b in bands)
        top = y_of(total)
        # the two outer strips, full height, which is what makes them the pieces
        # that get trimmed to length and ledged
        for sx in (0.0, pwx - strip):
            body.append(
                f'<rect x="{x0 + sx * s:.2f}" y="{top:.2f}" '
                f'width="{strip * s:.2f}" height="{total * s:.2f}" '
                f'fill="{dict(((k, c) for k, _, _, _, c, *_ in kinds))[kind]}" '
                f'stroke="#333" stroke-width="0.4"/>')
        # the middle 36: the slot, band by band, floor up
        z = 0.0
        for code, hgt, piece, deep, fate, becomes in bands:
            y = y_of(z + hgt)
            fill, dash, edge = {
                "stays": ("#c8ab8c", "", "#333"),
                "out": (_tint(WALL_TAN if code == "D" else RAIL_BLUE), "3 2",
                        "#a00"),
                "open": (OPEN_GREY, "1 2", "#aaa"),
            }[fate]
            body.append(
                f'<rect x="{x0 + strip * s:.2f}" y="{y:.2f}" '
                f'width="{gm_t * s:.2f}" height="{hgt * s:.2f}" fill="{fill}" '
                f'stroke="{edge}" stroke-width="0.5"'
                + (f' stroke-dasharray="{dash}"/>' if dash else '/>'))
            if hgt * s > 5.5:
                body.append(
                    f'<text x="{x0 + (strip + gm_t / 2) * s:.2f}" '
                    f'y="{y + hgt * s / 2 + 1.7:.2f}" text-anchor="middle" '
                    f'font-size="4.8" font-weight="bold">{code}</text>')
            z += hgt
        body.append(f'<text x="{x0 + pwx * s / 2:.1f}" y="{h - 7:.1f}" '
                    f'text-anchor="middle" font-size="4.6">{name}</text>')
        body.append(f'<text x="{x0 + pwx * s / 2:.1f}" y="{h - 2.4:.1f}" '
                    f'text-anchor="middle" font-size="3.8" fill="#666">'
                    f'{total:g} long</text>')
    # FULL PAGE WIDTH, unlike the nest drawings: those are deliberately small
    # because a nest is read as a picture, and this one is read for its labels.
    # The viewBox units are what the font sizes are in, so the drawing has to
    # fill the 190mm or a 4.8 letter lands under a millimetre tall on paper.
    return (f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="100%" '
            f'style="max-width:100%">{"".join(body)}</svg>')


def leg_section_svg(v, kind, s=0.62):
    """One leg's cross-section: four strips of 18, the middle two left out.

    The elevation cannot show a notch or a rebate, because both are cut into a
    face rather than through the leg - so they are here, which is also where the
    four strips read as four pieces rather than as a 72 block.
    """
    pwx, pwy, strip = v["POST_W_X"], v["POST_W_Y"], v["LEG_STRIP"]
    gm_t, bw = v["GRID_MEMBER_T"], v["T_BACK_WALL"]
    colour = dict((k, c) for k, _, _, _, c, *_ in leg_kinds(v))[kind]
    pad, lab = 4.0, 7.0
    w, h = pwx * s + 2 * pad, pwy * s + 2 * pad + lab
    body = [f'<rect x="{pad:.1f}" y="{pad:.1f}" width="{pwx * s:.1f}" '
            f'height="{pwy * s:.1f}" fill="none" stroke="#999" '
            f'stroke-width="0.5" stroke-dasharray="2 2"/>']
    # WHICH STRIPS ARE CUT BACK, AND HOW FAR ACROSS THE LEG THE WALL REACHES.
    # "inner" is the strip nearer the machine's centreline and it is the only
    # one a front leg ever loses; at the back the wall runs THROUGH the slot as
    # well, so the rebate is one band across the leg rather than a bite out of
    # one strip. Drawn stopping at the outer strip, which is the rule: the
    # outermost lamination of every leg keeps its full POST_W_Y and covers the
    # wall's end grain.
    rebate = {"front": None,
              "rear-corner": (strip, pwx - strip),        # slot + inner strip
              "rear-centre": (0.0, pwx)}[kind]            # straight through
    for sx in (0.0, pwx - strip):
        body.append(
            f'<rect x="{pad + sx * s:.2f}" y="{pad:.2f}" '
            f'width="{strip * s:.2f}" height="{pwy * s:.2f}" '
            f'fill="{colour}" stroke="#222" stroke-width="0.6"/>')
    # the slot itself
    body.append(f'<rect x="{pad + strip * s:.2f}" y="{pad:.2f}" '
                f'width="{gm_t * s:.2f}" height="{pwy * s:.2f}" '
                f'fill="{OPEN_GREY}" stroke="#a00" stroke-width="0.6" '
                f'stroke-dasharray="3 2"/>')
    if rebate:
        rx0, rx1 = rebate
        body.append(
            f'<rect x="{pad + rx0 * s:.2f}" y="{pad:.2f}" '
            f'width="{(rx1 - rx0) * s:.2f}" height="{bw * s:.2f}" '
            f'fill="{BACK_ORANGE}" opacity="0.6" stroke="#a00" '
            f'stroke-width="0.6"/>')
        body.append(f'<text x="{pad + (rx0 + rx1) / 2 * s:.1f}" '
                    f'y="{pad + bw * s / 2 + 1.4:.1f}" text-anchor="middle" '
                    f'font-size="3.6" fill="#5a2a00">wall {bw:g}</text>')
    # WHERE THE TWO LEFT-OUT STRIPS WOULD HAVE BEEN. Without this line the
    # section shows two strips and a hole, and the leg reads as a 2-piece
    # lamination - which is the thing this chapter exists to correct.
    body.append(f'<line x1="{pad + (strip + gm_t / 2) * s:.2f}" '
                f'y1="{pad:.2f}" x2="{pad + (strip + gm_t / 2) * s:.2f}" '
                f'y2="{pad + pwy * s:.2f}" stroke="#bbb" stroke-width="0.4" '
                f'stroke-dasharray="1.5 1.5"/>')
    body.append(f'<text x="{pad + (strip + gm_t / 2) * s:.1f}" '
                f'y="{pad + pwy * s / 2 + 2:.1f}" text-anchor="middle" '
                f'font-size="5.5" fill="#a00">{gm_t:g}</text>')
    body.append(f'<text x="{w / 2:.1f}" y="{h - 2.2:.1f}" text-anchor="middle" '
                f'font-size="5">{pwx:g} &times; {pwy:g}</text>')
    # WHICH STRIP IS THE INNER ONE IS A SIDE-OF-THE-MACHINE FACT and it has to
    # be stated, but it is stated in the PROSE above these drawings: set as a
    # caption it was wider than the section itself and clipped at both ends.
    return (f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="100%" '
            f'style="max-width:{w * 2.1:.0f}px">{"".join(body)}</svg>')


def legs_html(v):
    """Chapter 4: the five legs, strip by strip."""
    kinds = leg_kinds(v)
    sections = "".join(
        # THE <br> IS LOAD-BEARING: an svg is inline, so without it the caption
        # and the drawing share a line box and the "72 x 86" lands on top of
        # the "2 off" text.
        f'<td style="text-align:center"><b>{label}</b><br>'
        f'<span class=s>{n} off, {total:g} long</span><br>'
        f'{leg_section_svg(v, kind)}</td>'
        for kind, label, n, total, _c, _t, _l, _f in kinds)
    faces = "".join(
        f"<tr><td><b>{label}</b></td><td>{tenon}</td><td>{ledge}</td>"
        f"<td class=s>{face}</td></tr>"
        for kind, label, n, total, _c, tenon, ledge, face in kinds)
    # ONE KEY ROW PER DISTINCT BAND, AND IT NAMES WHICH LEGS CARRY IT. The two
    # fillers differ only in depth - 86 against 68 - so a row that did not say
    # which legs it was for read as the same part listed twice with two sizes,
    # which is exactly the kind of row somebody cuts eight of.
    rows, order = {}, []
    for kind, label, *_ in kinds:
        for code, hgt, piece, deep, fate, becomes in leg_bands(v, kind):
            sig = (code, hgt, deep)
            if sig not in rows:
                order.append(sig)
                rows[sig] = [code, hgt, piece, deep, fate, becomes, []]
            if label not in rows[sig][6]:
                rows[sig][6].append(label)
    key = []
    for sig in order:
        code, hgt, piece, deep, fate, becomes, which = rows[sig]
        fate_txt = {
            "stays": "<b>stays</b> &mdash; glued in for good",
            "out": "<b class=bad>COMES OUT</b> at base assembly",
            "open": "nothing ever fills it",
        }[fate]
        legs = ("all five" if len(which) == len(kinds)
                else "; ".join(which).lower())
        key.append(
            f"<tr><td style='text-align:center'><b>{code}</b></td>"
            f"<td>{piece}</td><td class=n>{hgt:g}</td>"
            f"<td class=n>{deep:g}</td><td class=s>{legs}</td>"
            f"<td>{fate_txt}</td>"
            f"<td class=s>{becomes and 'replaced by ' + becomes}</td></tr>")
    return f"""
<h2>4 &mdash; The five legs, strip by strip</h2>
<p><b>Every leg is four strips of {v['LEG_STRIP']:g} laminated face to face
&mdash; {v['POST_W_X']:g} across &mdash; and the middle two are left out to make
a {v['GRID_MEMBER_T']:g} slot the full height of the leg.</b> The lamination runs
<b>across the machine</b>; the other way is the strip's own width, ripped at 90
and trimmed to {v['POST_W_Y']:g}.</p>
<p>🔴 <b>Three of the blocks in that slot come back OUT.</b> They are glue-up
spacers &mdash; they hold the slot open and stop the outer strips bowing in under
clamps, and at base assembly they are knocked out and a rail or a wall takes
their place. <b>They are the same {v['GRID_MEMBER_T']:g} plywood as the two that
stay</b>, so on the bench nothing tells them apart. <b>Cut each one from the
stock that will fill that slot and keep glue off it</b> &mdash; wax or tape.</p>
<table><tr><th>Leg</th><th>Tenon</th><th>Ledge</th><th>Cut into a face</th></tr>
{faces}</table>
<p>The sections, looking down on a leg with its <b>back face at the top and its
inner strip on the right</b> &mdash; mirror them for the leg on the other side
of the machine. <b>The dotted red column is the slot, and the faint line down
its middle is where the two left-out strips would have met</b> &mdash; it is two
strips wide because it is two strips, which is why the leg is four and not
three. The orange band is the
<b>back wall</b>, which at the rear runs through the slot as well as the inner
strip. <b>It stops at the outer strip</b> &mdash; the outermost lamination of
every leg stays its full {v['POST_W_Y']:g} and covers the wall's end grain, and
the front legs lose nothing at all.</p>
<table><tr>{sections}</tr></table>

<h3>The slot, floor up</h3>
<p>All five legs to one scale, floor at the bottom. The <b>stations down the left
are the base's own elevation</b>, and every leg is set out from them. A band with
a <b>dashed red outline is a spacer that comes out</b>; a solid one is glued in
for good; grey is slot that stays empty.</p>
{leg_elevation_svg(v)}
<table><tr><th></th><th>What is in the slot</th><th>Tall</th><th>Deep</th>
<th>In which legs</th><th>Fate</th><th></th></tr>{''.join(key)}</table>
<p><b>The stack sums to the leg, and that is the check</b>:
{v['FOOT_SPACER_H']:g} + {v['GRID_MEMBER_H']:g} + {v['BASE_VOLUME_H']:g} +
{v['GRID_MEMBER_H']:g} + {v['BASE_BOX_GAP']:g} = <b>{v['LEG_L_REAR']:g}</b>, a
rear corner leg, and {v['POST_TENON_L']:g} more of tenon makes
<b>{v['LEG_L_BOX']:g}</b> for a leg the box lands on. The back centre leg gets
there the other way: {v['FOOT_SPACER_H']:g} + {v['WALL_H']:g} +
{v['BASE_BOX_GAP']:g} + {v['POST_TENON_L']:g}. <b>If a leg does not add up, the
mortise heights will not agree across the five and the frame sits twisted.</b></p>
<p>🔴 <b>The back centre leg's slot carries the walls, not rails and a filler.</b>
The central wall fills the front {v['POST_W_Y'] - v['T_BACK_WALL']:g} of it and
runs {v['CENTRE_WALL_H']:g} tall, {v['WALL_H'] - v['CENTRE_WALL_H']:g} shy at the
top; the back wall fills the back {v['T_BACK_WALL']:g} for the full
{v['WALL_H']:g}. <b>So it takes one spacer, not two, and it gets no filler</b>
&mdash; the wall is already doing the filler's job, with a part that was going in
anyway.</p>
<p><b>In the two rear corner legs the back {v['T_BACK_WALL']:g} of the slot
belongs to the back wall over its whole height</b>, which is why their filler is
{v['POST_W_Y'] - v['T_BACK_WALL']:g} deep where the front legs' is
{v['POST_W_Y']:g}. <b>The spacers are the full {v['POST_W_Y']:g}</b>: at glue-up
nothing is in there yet, and a spacer that does not reach both faces is the one
that lets a strip bow.</p>
<p>OPEN: <b>Nothing packs the slot above the upper rail</b> &mdash; the top
{v['BASE_BOX_GAP']:g} of a rear leg, and {v['BASE_BOX_GAP'] + v['POST_TENON_L']:g}
on a leg with a tenon. It is slot by design, since the slot runs the full height
and passes through the shoulder and the tenon. Whether that length wants a
removable spacer at glue-up, purely to stop the outer strips bowing where the
ledge will be cut, is his call.</p>
"""


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
{legs_html(v)}
<h2>5 &mdash; How it goes together</h2>
<table>
<tr><th>Joint</th><th>How</th></tr>
<tr><td><b>Fore-aft rails to legs</b></td><td>They fill the legs' middle slot
&mdash; the two centre laminations. One slot per leg carries the lower rail, the
upper rail, the filler between them, and in the rear middle leg the central
wall</td></tr>
<tr><td><b>Front cross rails to legs</b></td><td>Outer {v['GRID_MEMBER_T'] / 2:g}
housed {v['GRID_MEMBER_T'] / 2:g} deep in the front faces of the legs' INNER
strips, stopping <b>one lamination short at each end</b> so each leg's outermost
strip covers its end grain; inner {v['GRID_MEMBER_T'] / 2:g} spanning between the
legs, housed in nothing</td></tr>
<tr><td>🔴 <b>Both ends of the base</b></td><td><b>The outermost lamination of
every leg stays its full {v['POST_W_Y']:g}</b>, and whatever runs along that face
&mdash; cross rail at the front, shear wall at the back &mdash; stops one strip
short and is covered by it. <b>No end grain shows on the base's outer
faces</b></td></tr>
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

<h2>6 &mdash; The two side openings</h2>
<p>Each side of the base is open between the grids. Standing at one side, the
rectangle is:</p>
<table>
<tr><th>Fore-aft</th><td><b>{v['BAY_OPEN_FORE_AFT']:g}</b> &mdash; rear leg's back
face to front leg's front face. <b>The rails take nothing off it</b>: they run
the full length inside the legs' slots, so it is the legs that bound it</td></tr>
<tr><th>Height</th><td><b>{v['BASE_VOLUME_H']:g}</b> &mdash; lower rail's top to
upper rail's underside</td></tr>
<tr><th>Depth in</th><td><b>{v['BAY_OPEN_DEPTH']:g}</b> &mdash; legs' inner faces
to the near face of the central wall</td></tr>
</table>
<p>🔴 <b>The central wall is a backstop, so these are two separate volumes and
not one through-space.</b> The back wall closes the rear face as well, so a
carcase goes in from the side only.</p>
<p>Keep the carcases removable: the bottom skin's sand ports drain downward and
have to be reachable.</p>

<h2>7 &mdash; Order</h2>
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
