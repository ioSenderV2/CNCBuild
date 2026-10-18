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

# THE PART DATA LIVES IN ONE PLACE and this document borrows it. The cutlist
# tool owns groups() - what gets made, under the assembly it belongs to - and
# the sheet layout stays over there. A second copy of the list here is exactly
# the duplicate that drifts.
_cspec = importlib.util.spec_from_file_location(
    "cutdoc", HERE / "make-cutlist-doc.py")
cutdoc = importlib.util.module_from_spec(_cspec)
_cspec.loader.exec_module(cutdoc)

OUT = HERE.parent / "machine" / "drawings" / "base-construction.html"
SHEETS = boxdoc.SHEETS

ON_5x5 = "5 x 5"                  # the two central wall laminations, and only those

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
        # NO GAP BAND: this leg STOPS at the upper grid's top. The gap is air
        # between the grid and the box, and on the three legs the box lands on
        # it is leg material because they carry on up through it - here there
        # is no leg above the grid at all, which is the whole point of the
        # three-point mount.
        bands = [foot, rail("lower"),
                 ("C", v["BASE_VOLUME_H"], "Leg filler", deep_rear, "stays", ""),
                 rail("upper")]
        total = v["LEG_L_REAR"]
    elif kind == "front-centre":
        # THE WALL FILLS THE WHOLE SLOT ABOVE THE FOOT SPACER, and there is no
        # gap band and no tenon: this leg stops at the upper grid's top like a
        # rear corner one, because the box must not land on it.
        bands = [foot,
                 ("D", v["WALL_H"], "Glue-up spacer", pwy, "out",
                  f"the central wall, all {pwy:g} of the slot's depth")]
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
    """The six legs as the four kinds they actually come in.

    Named by where they stand, because that is how they get picked up off the
    bench. The box lands on front left, front right and back centre; the two
    rear corner legs and the front centre one carry the grids and the walls
    and NOT the box.

    THE FRONT CENTRE LEG IS WHAT HOLDS THE CENTRAL WALL'S FRONT END - his, and
    it replaced a pair of bolted cheeks that did the same job with a notch in
    every piece. A leg does it with no notch anywhere: the wall slides into its
    slot exactly as it does at the back, and the cross rail's housed outer
    lamination covers the wall's end the way the back wall covers the other.
    """
    pwy, bw, strip = v["POST_W_Y"], v["T_BACK_WALL"], v["LEG_STRIP"]
    return [
        ("front", "Front left, front right", 2, v["LEG_L_BOX"], LEG_BROWN,
         f"one {strip:g} &times; {v['TENON_CORNER']:g} tab, on the inner strip",
         f"ledged {v['T_BOX_LEDGE']:g} on the side face and the front face",
         f"front face of the INNER strip notched {bw:g} deep for the cross "
         f"rail's outer lamination &mdash; and the notch runs on UP from the "
         f"upper rail to the top of the tenon, so no ear is left standing "
         f"over the rail"),
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
        ("front-centre", "Front centre", 1, v["LEG_L_REAR"], REAR_BROWN,
         "none &mdash; the box does not land on it", "no ledge",
         f"BOTH strips notched {bw:g} deep at each grid for the cross rail's "
         f"outer lamination &mdash; that rail runs straight through this leg, "
         f"the same way the back wall runs through the back centre one"),
    ]


def leg_elevation_svg(v, s=0.165):
    """All six legs in one elevation, floor at the bottom, to one scale.

    WHY ONE DRAWING AND NOT FIVE: the band heights are the same across the
    legs, so five separate drawings would repeat one height axis five times and
    make the one real difference - the back centre leg carrying a wall where
    the others carry two rails and a filler - the hardest thing to see.

    A leg is drawn as its FOUR STRIPS: the outer pair, each to ITS OWN top,
    and the middle 36 drawn as the slot stack. Hatched, dashed-outline bands
    come out. The outer pair is drawn in leg_faces order - the outboard strip
    on the left, the inner one on the right - and they are not always the same
    height: a front leg's outboard strip stops at the shoulder.
    """
    pwx, strip, gm_t = v["POST_W_X"], v["LEG_STRIP"], v["GRID_MEMBER_T"]
    kinds = leg_kinds(v)
    # NAMED FOR ITSELF, NOT FOR ITS KIND: a leg gets picked up off the bench by
    # where it stands, and "front, 2 off" is the one label that does not help
    # when four of the five look identical.
    names = ["Front left", "Front right", "Rear left", "Rear right",
             "Back centre", "Front centre"]
    legs = list(zip(names, [k for kind, _, n, *_ in kinds
                            for k in [kind] * n]))
    assert len(legs) == len(names), "the names and the kinds must cover the same legs"

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
                # OFF LEG_BELOW_BOX, NOT OFF A LEG. These are elevations of
                # the base, and a rear corner leg stops BASE_BOX_GAP below the
                # box - reading them off that leg put every one of them 10 low
                # the moment the leg was corrected.
                (v["LEG_BELOW_BOX"] - v["BASE_BOX_GAP"] - v["GRID_MEMBER_H"],
                 "upper grid under"),
                (v["LEG_BELOW_BOX"] - v["BASE_BOX_GAP"], "upper grid top"),
                (v["LEG_BELOW_BOX"], "box underside"),
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
        # THE TWO OUTER STRIPS ARE NOT THE SAME HEIGHT, and the tops come from
        # leg_faces so this drawing cannot disagree with the quarter-turn one.
        # They were both drawn at the leg's full length, which is right for a
        # rear corner and for the back centre leg and WRONG for a front leg:
        # there the side ledge is 42 deep across an 18 outer strip, so it
        # swallows that strip whole and its top face IS the bearing shoulder.
        # The front elevation showed it running past the shoulder to the leg
        # top, against the profile view's 874, which is the one that was right.
        for sx, (_which, s_top, _cuts) in zip((0.0, pwx - strip),
                                              leg_faces(v, kind)):
            body.append(
                f'<rect x="{x0 + sx * s:.2f}" y="{y_of(s_top):.2f}" '
                f'width="{strip * s:.2f}" height="{s_top * s:.2f}" '
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


def leg_faces(v, kind):
    """The two outer laminations of one leg, as finished shapes.

    Each is returned as (which, top, cuts) where a cut is (points, label) and
    the points outline material TAKEN OFF the face, in the leg's own frame: x
    is fore-and-aft with the machine's FRONT at 0 and the back at POST_W_Y, y
    is height off the floor. The piece is what is left of POST_W_Y x top once
    they come out.

    ONE OUTLINE PER CONTIGUOUS REMOVAL, which is why these are polygons and
    not rectangles. On a front leg the ledge sits directly on top of the
    notch, and drawn as two rectangles they shared an edge and printed a
    double dashed line across the shoulder - where the reader is trying to
    see one step.

    EVERY FIGURE IS A REGISTRY SYMBOL. The ledge depth, the tab, the rebate
    and the notch are each stated once in the dimensions and read here - this
    function decides nothing, it only says which of them lands on which strip.
    """
    pwy, strip, ledge = v["POST_W_Y"], v["LEG_STRIP"], v["T_BOX_LEDGE"]
    bw, tenon = v["T_BACK_WALL"], v["POST_TENON_L"]
    box, rear = v["LEG_L_BOX"], v["LEG_L_REAR"]
    rail_under = rear - v["BASE_BOX_GAP"] - v["GRID_MEMBER_H"]

    shoulder = box - tenon
    if kind == "front":
        # THE SIDE LEDGE SWALLOWS THE OUTER STRIP WHOLE: it is 42 deep across
        # a leg whose outer lamination is 18, so above the shoulder there is
        # no outer strip left to draw. Its top face IS the bearing shoulder.
        #
        # On the inner strip the notch for the cross rail's outer lamination
        # runs up from the rail and the front ledge continues off the top of
        # it, so the two come off as one L down the leg's front face.
        tab = pwy - v["TENON_CORNER_Y"]
        return [
            ("outer", shoulder, []),
            ("inner", box, [
                ([(0, rail_under), (bw, rail_under), (bw, shoulder),
                  (tab, shoulder), (tab, box), (0, box)],
                 f"ledge {ledge:g} &middot; notch {bw:g}, front face"),
            ]),
        ]
    if kind == "rear-corner":
        return [
            ("outer", rear, []),
            ("inner", rear, [
                ([(pwy - bw, 0), (pwy, 0), (pwy, rear), (pwy - bw, rear)],
                 f"rebate {bw:g}, back face, full height"),
            ]),
        ]
    if kind == "front-centre":
        # BOTH STRIPS THE SAME, and both notched where the cross rail passes.
        # The rail is continuous through this leg, so unlike a front CORNER
        # leg there is no outermost strip left whole to cover its end grain -
        # there is no end grain here, the rail runs on.
        lo_a, lo_b = v["FOOT_SPACER_H"], v["FOOT_SPACER_H"] + v["GRID_MEMBER_H"]
        hi_b = rear
        hi_a = rear - v["GRID_MEMBER_H"]
        return [
            (which, rear, [
                ([(0, lo_a), (bw, lo_a), (bw, lo_b), (0, lo_b)],
                 f"notch {bw:g}, front face, at the lower grid"),
                ([(0, hi_a), (bw, hi_a), (bw, hi_b), (0, hi_b)],
                 f"notch {bw:g}, front face, at the upper grid"),
            ]) for which in ("outer", "inner")
        ]
    # the back centre leg: ledged on its back face only, so BOTH strips stand
    # proud and the full-height slot makes the tenon a pair of tabs. The
    # ledge is deeper than the rebate and sits on top of it - one L again.
    return [
        (which, box, [
            ([(pwy - bw, 0), (pwy, 0), (pwy, box), (pwy - ledge, box),
              (pwy - ledge, shoulder), (pwy - bw, shoulder)],
             f"ledge {ledge:g} &middot; rebate {bw:g}, back face"),
        ]) for which in ("outer", "inner")
    ]


def shoulder_of(v, kind):
    """Where the tenon starts on this kind of leg - its top if it has none."""
    if kind in ("rear-corner", "front-centre"):
        return v["LEG_L_REAR"]
    return v["LEG_L_BOX"] - v["POST_TENON_L"]


def inside(px, pz, pts):
    """Is this point inside the polygon - the usual ray cast."""
    hit = False
    for (ax, az), (bx, bz) in zip(pts, pts[1:] + pts[:1]):
        if (az > pz) != (bz > pz) and \
                px < ax + (pz - az) / (bz - az) * (bx - ax):
            hit = not hit
    return hit


def leg_faces_svg(v, s=0.165):
    """The same elevation, each leg turned a quarter turn about its own axis.

    WHY IT EXISTS: the slot elevation looks at the leg's 72 face, so both
    outer laminations are seen EDGE ON and every cut into a face - the tenon
    tab, the cross rail's notch, the back wall's rebate - is invisible. Turned
    90 degrees each lamination shows its POST_W_Y face, which is the face all
    of those are cut into.

    WHY THE TWO ARE DRAWN SIDE BY SIDE rather than one behind the other: at a
    quarter turn the inner strip stands directly behind the outer one and
    hides it, and the two are not the same shape in any of the three kinds of
    leg. His, and it is the whole reason for the drawing.

    Same scale and the same height stations as the slot elevation, so the two
    read against each other.
    """
    pwy = v["POST_W_Y"]
    kinds = leg_kinds(v)
    names = ["Front left", "Front right", "Rear left", "Rear right",
             "Back centre", "Front centre"]
    legs = list(zip(names, [k for kind, _, n, *_ in kinds
                            for k in [kind] * n]))

    tall = max(v["LEG_L_BOX"], v["LEG_L_REAR"])
    face_pitch = pwy * s + 10               # the two faces of one leg
    leg_pitch = 2 * face_pitch + 16         # and the gap to the next leg
    pad_l, pad_r, pad_t, pad_b = 15.0, 48.0, 13.0, 21.0
    w = pad_l + leg_pitch * len(legs) + pad_r
    h = pad_t + tall * s + pad_b
    body = []

    def y_of(z):
        return pad_t + (tall - z) * s

    stations = [(0, "floor"), (v["FOOT_SPACER_H"], "lower grid under"),
                (v["FOOT_SPACER_H"] + v["GRID_MEMBER_H"], "lower grid top"),
                # OFF LEG_BELOW_BOX, NOT OFF A LEG. These are elevations of
                # the base, and a rear corner leg stops BASE_BOX_GAP below the
                # box - reading them off that leg put every one of them 10 low
                # the moment the leg was corrected.
                (v["LEG_BELOW_BOX"] - v["BASE_BOX_GAP"] - v["GRID_MEMBER_H"],
                 "upper grid under"),
                (v["LEG_BELOW_BOX"] - v["BASE_BOX_GAP"], "upper grid top"),
                (v["LEG_BELOW_BOX"], "box underside"),
                (v["LEG_L_BOX"], "leg top")]
    # the same push-apart the slot elevation uses, for the two stations that
    # are BASE_BOX_GAP apart and would otherwise print on each other
    label_y, floor_y = {}, None
    for z, _ in sorted(stations, key=lambda p: -p[0]):
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

    colour = dict((k, c) for k, _, _, _, c, *_ in kinds)
    for i, (name, kind) in enumerate(legs):
        for j, (which, top, cuts) in enumerate(leg_faces(v, kind)):
            x0 = pad_l + i * leg_pitch + j * face_pitch
            body.append(
                f'<rect x="{x0:.2f}" y="{y_of(top):.2f}" '
                f'width="{pwy * s:.2f}" height="{top * s:.2f}" '
                f'fill="{colour[kind]}" stroke="#333" stroke-width="0.5"/>')
            for pts, _label in cuts:
                d = " ".join(f'{x0 + px * s:.2f},{y_of(pz):.2f}'
                             for px, pz in pts)
                body.append(
                    f'<polygon points="{d}" fill="#fff" stroke="#a00" '
                    f'stroke-width="0.5" stroke-dasharray="2.5 1.5"/>')
            # NAME THE TAB, which is the thing the ledge leaves standing and
            # the reason a leg the box lands on is drawn at all. Anything
            # still solid above the shoulder is tab.
            if top > shoulder_of(v, kind):
                sh = shoulder_of(v, kind)
                solid = [x for x in range(0, int(pwy))
                         if not any(inside(x + 0.5, (sh + top) / 2, pts)
                                    for pts, _ in cuts)]
                if solid:
                    body.append(
                        f'<text x="{x0 + (solid[0] + solid[-1]) / 2 * s:.2f}" '
                        f'y="{y_of((sh + top) / 2) + 1.4:.2f}" '
                        f'text-anchor="middle" font-size="3.4" '
                        f'fill="#333">tab</text>')
            body.append(f'<text x="{x0 + pwy * s / 2:.1f}" '
                        f'y="{h - 13.5:.1f}" text-anchor="middle" '
                        f'font-size="4.0" fill="#444">{which}</text>')
        xc = pad_l + i * leg_pitch + face_pitch
        body.append(f'<text x="{xc:.1f}" y="{h - 7.6:.1f}" '
                    f'text-anchor="middle" font-size="4.6">{name}</text>')
        notes = [lab for _w, _t, cuts in leg_faces(v, kind)
                 for _pts, lab in cuts]
        body.append(f'<text x="{xc:.1f}" y="{h - 2.6:.1f}" '
                    f'text-anchor="middle" font-size="3.4" fill="#666">'
                    f'{" &middot; ".join(dict.fromkeys(notes)) or "no cuts"}'
                    f'</text>')
    # FRONT OF THE MACHINE TO THE LEFT on every face, so the notch and the
    # rebate land on opposite sides of the drawing and cannot be confused.
    body.append(f'<text x="{pad_l:.1f}" y="{pad_t - 4.5:.1f}" '
                f'font-size="3.8" fill="#888">front of the machine to the '
                f'LEFT, back to the right &mdash; each face {pwy:g} wide'
                f'</text>')
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
    # (across the leg from, to, WHICH FACE, what sits in it). The face matters:
    # the two rear kinds take the back wall in their BACK face, and the front
    # centre leg takes the cross rail's outer lamination in its FRONT one.
    rebate = {"front": None,
              "rear-corner": (strip, pwx - strip, "back", "wall"),
              "rear-centre": (0.0, pwx, "back", "wall"),
              "front-centre": (0.0, pwx, "front", "rail")}[kind]
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
        rx0, rx1, face, what = rebate
        ry = pad if face == "back" else pad + (pwy - bw) * s
        body.append(
            f'<rect x="{pad + rx0 * s:.2f}" y="{ry:.2f}" '
            f'width="{(rx1 - rx0) * s:.2f}" height="{bw * s:.2f}" '
            f'fill="{BACK_ORANGE}" opacity="0.6" stroke="#a00" '
            f'stroke-width="0.6"/>')
        body.append(f'<text x="{pad + (rx0 + rx1) / 2 * s:.1f}" '
                    f'y="{ry + bw * s / 2 + 1.4:.1f}" text-anchor="middle" '
                    f'font-size="3.6" fill="#5a2a00">{what} {bw:g}</text>')
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


def parts_html(v):
    """Chapter 1: what gets made, under the assembly it belongs to.

    The rows come from make-cutlist-doc.py's groups(), which is the one place
    the part data lives. THE SHEET LAYOUT IS NOT HERE - it is read standing at
    a sheet, where this is read standing at the frame.
    """
    rows, total = [], 0
    for gname, qty, why, pieces in cutdoc.groups(v):
        n = sum(p[3] for p in pieces)
        total += n
        rows.append(
            f'<tr class="g"><td colspan="4"><b>{gname}</b>'
            + (f' &mdash; {qty} of them' if qty > 1 else '')
            + f'<div class="why">{why}</div></td></tr>')
        for name, a, b, q, note in pieces:
            rows.append(f'<tr><td>{name}</td>'
                        f'<td class=n>{a:g} &times; {b:g}</td>'
                        f'<td class=n><b>{q}</b></td>'
                        f'<td class=s>{note}</td></tr>')
    return f"""
<h2>1 &mdash; Parts</h2>
<p><b>{total} pieces of {v['T_BB_SKIN_BOT']:g} mm Baltic birch</b>, grouped the
way the base goes together &mdash; <b>a group here is one assembly</b> and
carries everything that goes into it, so the legs bring their own fillers and
foot spacers and the rails bring the caster blocks that bear on them.</p>
<p><b>Leg strips are ripped at {cutdoc.STRIP_W:g} and trimmed to
{v['POST_W_Y']:g} once the lamination is dry</b>, so everything cut from strip
stock is listed at {cutdoc.STRIP_W:g} wide. <b>Every
{v['GRID_MEMBER_T']:g} member is two laminations</b>, listed here as the
{v['T_BB_SKIN_BOT']:g} pieces that actually get cut &mdash; the
{v['GRID_MEMBER_T']:g} is not a choice, it is what fills a leg's slot.</p>
<p><b>The glue-up spacers are not a part.</b> One set holds a leg's slot open
while it is clamped and comes straight back out for the next leg, so it is one
set off rail offcut, waxed or taped.</p>
<table><tr><th>Piece</th><th class=n>Size</th><th class=n>Qty</th>
<th>Notes</th></tr>
{''.join(rows)}</table>
<p><b>Which sheet each piece comes off is a separate document</b> &mdash;
<a href="base-cutlist.html">base-cutlist.html</a>.</p>
"""


def legs_html(v):
    """Chapter 4: the six legs, strip by strip."""
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
        legs = ("all six" if len(which) == len(kinds)
                else "; ".join(which).lower())
        key.append(
            f"<tr><td style='text-align:center'><b>{code}</b></td>"
            f"<td>{piece}</td><td class=n>{hgt:g}</td>"
            f"<td class=n>{deep:g}</td><td class=s>{legs}</td>"
            f"<td>{fate_txt}</td>"
            f"<td class=s>{becomes and 'replaced by ' + becomes}</td></tr>")
    return f"""
<h2>4 &mdash; The six legs, strip by strip</h2>
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
<p>All six legs to one scale, floor at the bottom. The <b>stations down the left
are the base's own elevation</b>, and every leg is set out from them. A band with
a <b>dashed red outline is a spacer that comes out</b>; a solid one is glued in
for good; grey is slot that stays empty.</p>
{leg_elevation_svg(v)}
<p>The same legs <b>turned a quarter turn</b>, so each outer lamination shows
the {v['POST_W_Y']:g} face instead of its edge &mdash; which is the face the
tenon, the notch and the rebate are all cut into. <b>The two are drawn side by
side because at a quarter turn one stands behind the other</b>, and they are
not the same shape. A <b>dashed red outline is material taken off</b>.</p>
{leg_faces_svg(v)}
<table><tr><th></th><th>What is in the slot</th><th>Tall</th><th>Deep</th>
<th>In which legs</th><th>Fate</th><th></th></tr>{''.join(key)}</table>
<p><b>The stack sums to the leg, and that is the check</b>:
{v['FOOT_SPACER_H']:g} + {v['GRID_MEMBER_H']:g} + {v['BASE_VOLUME_H']:g} +
{v['GRID_MEMBER_H']:g} = <b>{v['LEG_L_REAR']:g}</b>, a rear corner leg, which
stops level with the upper grid's top. <b>The {v['BASE_BOX_GAP']:g} gap is air,
not leg</b> &mdash; only a leg the box lands on carries on through it, to the
box underside at {v['LEG_BELOW_BOX']:g}, and {v['POST_TENON_L']:g} more of
tenon makes <b>{v['LEG_L_BOX']:g}</b>. The back centre leg gets
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


# ---- the shoulder, top down -------------------------------------------------
# HIS ASK: show the three legs the box lands on from above, and show HOW THE
# SHOULDER GETS CUT. It is one cut repeated - a band the width of the wall taken
# off the top of every outward-facing face, down to the shoulder - and what is
# left standing is the tenon. Nothing is laid out as a tenon: the tenon is a
# RESIDUE, which is why a full-height slot could pass straight through it
# without anybody having to redraw anything.
#
# THE GEOMETRY IS THE MODEL'S, NOT A RECONSTRUCTION. make-3d.py gives each post
# as (un-ledged band, full section), and the two agree: the 42 band off a front
# leg's side face swallows the whole outer strip plus 24 of slot, so the only
# material left inside the band is the inner strip - 18 x 44, one tab. On the
# back centre leg the band comes off the back face alone, so both strips stand
# and the slot leaves 36 between them.
SHOULDER_TONGUE, SHOULDER_SKIN = "#e7d2a8", "#cfe0ee"
TENON_BROWN, SPACER_PINK = "#9C6B3C", "#f6d8de"


def shoulder_legs(v):
    """The three legs the box lands on: which faces are ledged, and the residue.

    `ledged` is the set of leg-local faces the band comes off, drawn with the
    machine's left at the left and the box's FRONT at the bottom. `inner` says
    which strip is the one nearer the machine's centreline, because that is the
    strip the tab is on and it swaps sides between the two front legs.
    """
    return [
        ("Front left", {"left", "front"}, "right",
         f"one tab, on the strip nearer the machine's centre"),
        ("Front right", {"right", "front"}, "left",
         f"the same leg mirrored &mdash; the tab swaps sides"),
        ("Back centre", {"back"}, None,
         f"two tabs, {v['GRID_MEMBER_T']:g} apart, one on each strip"),
    ]


SHOULDER_S = 1.15                    # one scale for the plan and the section


def _shoulder_w(v):
    """The plan's drawn width, which the section matches.

    THE TWO DRAWINGS MUST SHARE A viewBox WIDTH. Rendered at width 100% the
    browser stretches each to the page, so a narrower viewBox is drawn LARGER -
    the section came out at four times the plan's scale with its labels
    overlapping, which looked like a font bug and was a units bug.
    """
    return 15.0 + (v["POST_W_X"] * SHOULDER_S + 44) * 3


def shoulder_plan_svg(v, s=SHOULDER_S):
    """All three in one plan, to one scale, so the mirroring is visible.

    Drawn as: the leg's full 72 x 86 outline, the two strips and the slot, the
    LEDGE BAND shaded in its two jobs - the outer 24 the tongue bears on and the
    inner 18 the bottom skin bears on - and whatever stands inside the band
    hatched as the tenon.
    """
    pwx, pwy, strip = v["POST_W_X"], v["POST_W_Y"], v["LEG_STRIP"]
    gm_t, ledge, tong = v["GRID_MEMBER_T"], v["T_BOX_LEDGE"], v["T_BOX_TONGUE"]
    gap = v["TENON_SPACER_GAP"]
    skin = ledge - tong                      # the inner 18 of the 42
    stand = pwx - ledge                      # 30 across, on a leg ledged in X
    legs = shoulder_legs(v)
    pad_l, pad_t, pad_b, pitch = 15.0, 22.0, 28.0, pwx * s + 44
    w, h = _shoulder_w(v), pad_t + pwy * s + pad_b
    body = []

    for i, (name, ledged, inner, _note) in enumerate(legs):
        ox = pad_l + i * pitch
        oy = pad_t

        def px(x):
            return ox + x * s

        def py(y):
            return oy + y * s

        # the ledge bands, outer 24 then inner 18, one per ledged face. Drawn
        # FIRST so the strips and the slot sit over them and a reader sees
        # which of the two the shoulder actually is.
        for face in sorted(ledged):
            for depth0, depth1, fill in ((0.0, tong, SHOULDER_TONGUE),
                                         (tong, ledge, SHOULDER_SKIN)):
                if face == "left":
                    r = (depth0, 0.0, depth1 - depth0, pwy)
                elif face == "right":
                    r = (pwx - depth1, 0.0, depth1 - depth0, pwy)
                elif face == "front":
                    r = (0.0, pwy - depth1, pwx, depth1 - depth0)
                else:                                            # back
                    r = (0.0, depth0, pwx, depth1 - depth0)
                body.append(
                    f'<rect x="{px(r[0]):.2f}" y="{py(r[1]):.2f}" '
                    f'width="{r[2] * s:.2f}" height="{r[3] * s:.2f}" '
                    f'fill="{fill}" stroke="none"/>')

        # the two strips and the slot, over the shading
        for sx in (0.0, pwx - strip):
            body.append(f'<rect x="{px(sx):.2f}" y="{py(0):.2f}" '
                        f'width="{strip * s:.2f}" height="{pwy * s:.2f}" '
                        f'fill="none" stroke="#333" stroke-width="0.6"/>')
        body.append(f'<rect x="{px(strip):.2f}" y="{py(0):.2f}" '
                    f'width="{gm_t * s:.2f}" height="{pwy * s:.2f}" '
                    f'fill="#fff" stroke="#a00" stroke-width="0.6" '
                    f'stroke-dasharray="3 2"/>')
        body.append(f'<text x="{px(strip + gm_t / 2):.1f}" '
                    f'y="{py(pwy / 2):.1f}" text-anchor="middle" '
                    f'font-size="5" fill="#a00">{gm_t:g}</text>')

        # WHAT STANDS: the un-ledged band intersected with the strips, which is
        # the tenon. Computed rather than stated, so it cannot disagree with
        # the bands drawn above it.
        bx0 = ledge if "left" in ledged else 0.0
        bx1 = pwx - ledge if "right" in ledged else pwx
        by0 = ledge if "back" in ledged else 0.0
        by1 = pwy - ledge if "front" in ledged else pwy
        for sx0, sx1 in ((0.0, strip), (pwx - strip, pwx)):
            tx0, tx1 = max(sx0, bx0), min(sx1, bx1)
            if tx1 - tx0 < 1e-9:
                continue
            body.append(
                f'<rect x="{px(tx0):.2f}" y="{py(by0):.2f}" '
                f'width="{(tx1 - tx0) * s:.2f}" height="{(by1 - by0) * s:.2f}" '
                f'fill="{TENON_BROWN}" stroke="#222" stroke-width="0.7"/>')
            body.append(
                f'<text x="{px((tx0 + tx1) / 2):.1f}" '
                f'y="{py((by0 + by1) / 2) + 1.6:.1f}" text-anchor="middle" '
                f'font-size="4.6" fill="#fff" font-weight="bold">'
                f'{tx1 - tx0:g}&#215;{by1 - by0:g}</text>')
            # THE SPACER FILLS THE REST OF THE BAND. On a front leg the band is
            # POST_W_X - T_BOX_LEDGE across and the tab is one strip of it; the
            # rest is slot, and that is the gap to the web. Drawn against the
            # tab's outer face, which is whichever side the ledge is on.
            if ledged & {"left", "right"}:
                gx0 = tx0 - gap if "left" in ledged else tx1
                body.append(
                    f'<rect x="{px(gx0):.2f}" y="{py(by0):.2f}" '
                    f'width="{gap * s:.2f}" height="{(by1 - by0) * s:.2f}" '
                    f'fill="{SPACER_PINK}" stroke="#a00" stroke-width="0.7"/>')
                body.append(
                    f'<text x="{px(gx0 + gap / 2):.1f}" '
                    f'y="{py((by0 + by1) / 2) + 1.4:.1f}" text-anchor="middle" '
                    f'font-size="4" fill="#a00" '
                    f'transform="rotate(-90 {px(gx0 + gap / 2):.1f} '
                    f'{py((by0 + by1) / 2) + 1.4:.1f})">spacer {gap:g}</text>')

        # the outline last, so it is unbroken
        body.append(f'<rect x="{px(0):.2f}" y="{py(0):.2f}" '
                    f'width="{pwx * s:.2f}" height="{pwy * s:.2f}" '
                    f'fill="none" stroke="#111" stroke-width="1"/>')

        # WHICH FACES THE BAND COMES OFF, marked on the faces themselves - the
        # one fact a reader needs before picking the leg up, and the one that
        # differs between the three.
        for face in sorted(ledged):
            if face == "left":
                tx, ty, rot = px(-3.5), py(pwy / 2), -90
            elif face == "right":
                tx, ty, rot = px(pwx + 7), py(pwy / 2), -90
            elif face == "front":
                tx, ty, rot = px(pwx / 2), py(pwy) + 8, 0
            else:
                tx, ty, rot = px(pwx / 2), py(0) - 4, 0
            body.append(
                f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" '
                f'font-size="4.4" fill="#a00"'
                + (f' transform="rotate({rot} {tx:.1f} {ty:.1f})"' if rot else '')
                + f'>ledged {ledge:g}</text>')

        body.append(f'<text x="{px(pwx / 2):.1f}" y="{pad_t - 13:.1f}" '
                    f'text-anchor="middle" font-size="6" '
                    f'font-weight="bold">{name}</text>')
        body.append(f'<text x="{px(pwx / 2):.1f}" y="{h - 7:.1f}" '
                    f'text-anchor="middle" font-size="4.4" fill="#555">'
                    f'{pwx:g} &times; {pwy:g}, front at the bottom</text>')
    # NO KEY INSIDE THE DRAWING. Set as a row of three it landed one swatch
    # under each leg and read as three per-leg captions. The colours are named
    # in the prose instead, where a swatch can sit in the sentence that
    # explains it.
    assert skin == v["T_BB_SKIN_BOT"], "the inner band is the bottom skin's own 18"
    return (f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="100%" '
            f'style="max-width:100%">{"".join(body)}</svg>')


def shoulder_section_svg(v, s=SHOULDER_S):
    """The depth of the cut, in section through a front leg, TO SCALE both ways.

    The plan says where the band is; this says how deep and what comes down on
    it. They are the two halves of one cut and a reader needs both before
    reaching for a saw - so they are drawn to ONE scale, in one viewBox width.
    """
    pwx, strip, ledge = v["POST_W_X"], v["LEG_STRIP"], v["T_BOX_LEDGE"]
    tong, skin, tl = v["T_BOX_TONGUE"], v["T_BB_SKIN_BOT"], v["POST_TENON_L"]
    cav, hc = 100.0, v["TENON_HOLE_CLEAR"]
    pad_l, pad_t = 15.0, 10.0
    below = 40.0                               # how much leg to show under it
    w = _shoulder_w(v)
    pad_r = w - pad_l - (pwx + 34) * s
    h = pad_t + (tl + below) * s + 10
    body = []

    def px(x):
        return pad_l + x * s

    def py(z):                                 # z measured UP from the shoulder
        return pad_t + (tl - z) * s

    # the leg under the shoulder: two strips with the slot void between them
    for sx in (0.0, pwx - strip):
        body.append(f'<rect x="{px(sx):.2f}" y="{py(0):.2f}" '
                    f'width="{strip * s:.2f}" height="{below * s:.2f}" '
                    f'fill="#7A5230" stroke="#222" stroke-width="0.6"/>')
    body.append(f'<text x="{px(pwx / 2):.1f}" y="{py(0) + below * s / 2:.1f}" '
                f'text-anchor="middle" font-size="4.2" fill="#a00">slot</text>')
    # the tenon standing out of the inner strip
    body.append(f'<rect x="{px(pwx - strip):.2f}" y="{py(tl):.2f}" '
                f'width="{strip * s:.2f}" height="{tl * s:.2f}" '
                f'fill="{TENON_BROWN}" stroke="#222" stroke-width="0.7"/>')
    # the shoulder itself, drawn as the line the band leaves
    body.append(f'<line x1="{px(0):.2f}" y1="{py(0):.2f}" '
                f'x2="{px(pwx - strip):.2f}" y2="{py(0):.2f}" stroke="#111" '
                f'stroke-width="1.1"/>')
    # what lands on it: the tongue on the outer 24, the bottom skin on the
    # inner 18 and running inboard past the tenon through its own hole
    # The tongue runs on up past the top skin; drawn to the leg's top and no
    # further, because above that it is the box's business and not this cut's.
    body.append(f'<rect x="{px(0):.2f}" y="{py(tl):.2f}" '
                f'width="{tong * s:.2f}" height="{tl * s:.2f}" '
                f'fill="{SHOULDER_TONGUE}" stroke="#444" stroke-width="0.5"/>')
    body.append(f'<text x="{px(tong / 2):.1f}" y="{py(tl / 2):.1f}" '
                f'text-anchor="middle" font-size="4" fill="#5a4a20" '
                f'transform="rotate(-90 {px(tong / 2):.1f} {py(tl / 2):.1f})">'
                f'tongue {tong:g}</text>')
    body.append(f'<rect x="{px(tong):.2f}" y="{py(skin):.2f}" '
                f'width="{(pwx - strip - hc - tong) * s:.2f}" '
                f'height="{skin * s:.2f}" fill="{SHOULDER_SKIN}" stroke="#444" '
                f'stroke-width="0.5"/>')
    body.append(f'<rect x="{px(pwx + hc):.2f}" y="{py(skin):.2f}" '
                f'width="{(34 - hc) * s:.2f}" height="{skin * s:.2f}" '
                f'fill="{SHOULDER_SKIN}" stroke="#444" stroke-width="0.5"/>')
    body.append(f'<text x="{px(pwx + 18):.1f}" y="{py(skin / 2) + 1.4:.1f}" '
                f'text-anchor="middle" font-size="4" fill="#2a4458">'
                f'bottom skin</text>')
    # SAME LABEL COLLISION AS THE ELEVATION: the leg top and the top skin's
    # underside are TENON_HOLE_CLEAR x 2 apart, which is a millimetre of drawing.
    # The rule stays on its height; only the text is pushed clear.
    marks = [(skin + cav, f"top skin underside at {skin + cav:g} &mdash; the "
                          f"leg stops {skin + cav - tl:g} shy of it"),
             (tl, "leg top"),
             (skin, f"bottom skin {skin:g} rests on it"),
             (0, f"the shoulder &mdash; cut {tl:g} down from the leg's top")]
    prev = None
    for z, txt in marks:
        y = py(z)
        ty = y if prev is None else max(y, prev + 5.2)
        prev = ty
        body.append(f'<line x1="{px(0) - 3:.2f}" y1="{y:.2f}" '
                    f'x2="{w - pad_r + 4:.2f}" y2="{y:.2f}" stroke="#bbb" '
                    f'stroke-width="0.4" stroke-dasharray="2 2"/>')
        body.append(f'<text x="{w - pad_r + 6:.1f}" y="{ty + 1.4:.1f}" '
                    f'font-size="4.4" fill="#444">{txt}</text>')
    return (f'<svg viewBox="0 0 {w:.1f} {h:.1f}" width="100%" '
            f'style="max-width:100%">{"".join(body)}</svg>')


def ends_html(v):
    """Chapter 5b: how the central wall is held at both ends.

    IT USED TO BE A DRAWING OF NOTCHES. The wall took two at each end and the
    front end was a pair of bolted cheeks either side of it; the sixth leg
    removed all of that, so what is left to say is short and there is no
    profile to draw - the piece is a plain rectangle.
    """
    return f"""
<h2>5b &mdash; The central wall, at both ends</h2>
<p><b>The same joint twice.</b> The wall slides into a leg's slot at each end
&mdash; the back centre leg at the rear, the front centre leg at the front
&mdash; and is bolted through with {v['CENTRE_WALL_BOLT_COUNT']:g} bolts a side
on the {v['CENTRE_WALL_BOLT_PITCH']:g} quarter points of the clear band.</p>
<p>🔴 <b>The wall is a plain rectangle: {v['CENTRE_WALL_L']:g} &times;
{v['CENTRE_WALL_H']:g}, no notches anywhere.</b> It used to take two at the
front, to clear a cross rail lamination that ran past it. <b>With a leg there
that lamination butts the leg instead</b>, in two spans, so nothing crosses the
wall and there is nothing to cut.</p>
<p><b>No end grain shows at either end, and for the same reason both times:</b>
the piece running straight through that leg covers it &mdash; the back wall at
the rear, the front cross rail's housed outer lamination at the front. The wall
stops {v['GRID_MEMBER_T'] / 2:g} shy of the front plane, which is exactly that
housing's depth.</p>
<table><tr><th></th><th></th></tr>
<tr><td><b>Front centre leg</b></td><td>{v['LEG_L_REAR']:g} tall, the same as a
rear corner leg &mdash; <b>no tenon, so the box must not land on it</b>. Both
strips notched {v['T_BACK_WALL']:g} deep at each grid in the front face, where
the cross rail's outer lamination runs through</td></tr>
<tr><td><b>No filler</b></td><td>the wall fills this leg's slot, the same as at
the back centre leg</td></tr>
<tr><td><b>What it cost</b></td><td>the front cross rails' inner lamination
becomes <b>two spans of {v['RAIL_CROSS_INNER_SPAN']:g}</b> per grid instead of
one piece of {v['RAIL_CROSS_INNER_L']:g}</td></tr>
</table>
"""


def casters_html(v):
    """Chapter 5a: the six leveling casters and the fork channel."""
    gap = v["BASE_FLOOR_CLEAR"] - v["CASTER_H"]
    margin = (v["BAY_OPEN_FORE_AFT"] - v["FORK_CHANNEL_W"]) / 2
    return f"""
<h2>5a &mdash; The casters and the fork channel</h2>
<p><b>{v['CASTER_COUNT']:g} leveling casters, one per leg, all of them INSIDE the
{v['BASE_FLOOR_CLEAR']:g} floor clearance rather than under the legs</b> &mdash;
which is what keeps the base's height exactly as drawn. Four sit beside a corner
leg under the lower fore-aft rail. <b>The fifth sits on the central shear wall's
bottom edge, BEHIND the front centre leg</b> &mdash; neither centre leg has a
fore-aft rail of its own, so a lamination each side of the wall's bottom band
brings it out to {v['POST_W_X']:g} and the plate lands on that.</p>
<p><b>Five casters, six legs.</b> The two centre legs share this one between
them, so the back centre leg has none.</p>
<table><tr><th></th><th></th></tr>
<tr><td><b>Plate</b></td><td>{v['CASTER_PLATE']:g} square, four holes at 7
&mdash; which is why the lower rails are brought out to {v['POST_W_X']:g}</td></tr>
<tr><td><b>Overall height</b></td><td>{v['CASTER_H']:g}, plate face to the
bottom of the wheel</td></tr>
<tr><td><b>Leveling travel</b></td><td>{v['CASTER_LEVEL_TRAVEL']:g} &mdash; the
whole leveling authority of the base</td></tr>
</table>
<p>🔴 <b>Every caster sits on a drop block, and the block's thickness is cut to
fit.</b> {v['CASTER_H']:g} in a {v['BASE_FLOOR_CLEAR']:g} band leaves
<b>{gap:.1f}</b> between the wheel and the floor, and
{v['CASTER_LEVEL_TRAVEL']:g} of foot cannot make that up. The block brings the
wheel just below the leg bottoms. <b>Measure the slab under the six positions and
cut the six blocks so they land within a couple of mm of each other</b> &mdash;
the {v['CASTER_LEVEL_TRAVEL']:g} trims what is left.</p>
<p><b>A block is a shim in compression</b>, not a hanger: the structure bears
down on it and the caster bears up, so its screws locate it and carry nothing.
Four bear on a <b>lower rail's underside</b>, hard against a corner leg's face;
the fifth on the <b>central wall's bottom edge</b>. Nothing passes under a leg's
foot &mdash; the legs fill the band, which is what lets all five caster plates sit on
one plane.</p>
<p><b>The machine stands on the feet.</b> There is not enough travel to lift the
wheels clear and set the legs back down, so the leg bottoms hang a few mm off the
floor either way.</p>
<p><b>Level on three</b> &mdash; the two <b>REAR</b> corners and the front
centre. <b>The two front corners come down to touch</b>, not to lift: they
carry nothing standing, and they are what stops the thing tipping about a line
from a rear corner to the front centre.</p>
<p>🔴 <b>The trio changed when the fifth caster moved behind the front centre
leg.</b> It used to be the two FRONT corners and a centre caster near the back.
Level on the two front corners now and all three points sit in a line across
the front, which defines no plane at all &mdash; the base would rock about
it.</p>
<p><b>The fork channel is {v['FORK_CHANNEL_W']:g} wide, centred in the
{v['BAY_OPEN_FORE_AFT']:g} opening</b>, with a guard rail each side screwed under
the lower grid. That leaves <b>{margin:.0f}</b> at each end of the opening, which
is where the casters and their blocks sit. Each rail is a <b>dressed 2x3 on
edge</b>, hanging <b>{v['GUARD_RAIL_DROP']:g}</b> below the grid and leaving
<b>{v['BASE_FLOOR_CLEAR'] - v['GUARD_RAIL_DROP']:g}</b> under itself.</p>
<p>🔴 <b>Both ends run under a lower fore-aft rail and are screwed up into
it.</b> That is the anchorage, and it is what takes a sideways hit from a fork.
Each rail is <b>{v['GUARD_RAIL_L']:g}</b> &mdash; one lamination short at each
end, so it covers the fore-aft rail's inner three strips, <b>54</b> of overlap,
and its own ends sit 18 in from the base's outer faces. <b>The central wall
catches it again at mid-span</b>, which halves the length it has to resist a hit
over. They keep
the jack centred and stop a fork ever reaching a caster, and they are <b>guides
and not bearing surfaces</b>: as the jack lifts, the forks rise inside the
channel until they bear on the grid's underside.</p>
"""


def shoulder_html(v):
    """Chapter 5: top down on the three legs the box lands on."""
    rows = "".join(
        f"<tr><td><b>{name}</b></td>"
        f"<td>{'the side face and the front face' if 'front' in ledged else 'the back face only'}</td>"
        f"<td>{note}</td></tr>"
        for name, ledged, inner, note in shoulder_legs(v))
    return f"""
<h2>5 &mdash; Top down on the three legs the box lands on</h2>
<p><b>One cut, repeated: a band {v['T_BOX_LEDGE']:g} wide is taken off the top of
every outward-facing face, down to the shoulder. What is left standing is the
tenon.</b> Nothing is set out as a tenon &mdash; the tenon is what the band does
not reach, which is why the slot can run straight through it.</p>
<table><tr><th>Leg</th><th>Faces the band comes off</th><th>What stands</th></tr>
{rows}</table>
<p>🔴 <b>The {v['T_BOX_LEDGE']:g} is not one number, it is two jobs side by
side</b>, and that is why it is {v['T_BOX_LEDGE']:g}:
<span style="background:{SHOULDER_TONGUE};padding:0 3px">the outer
<b>{v['T_BOX_TONGUE']:g}</b></span> is where the tongue stands, directly on the
leg and not on the box, and
<span style="background:{SHOULDER_SKIN};padding:0 3px">the inner
<b>{v['T_BOX_LEDGE'] - v['T_BOX_TONGUE']:g}</b></span> is where the bottom skin
rests. <b>So the band is as wide as the wall that lands on it.</b> On the plans
below those are the two shades of the cut-away band, and
<span style="background:{TENON_BROWN};color:#fff;padding:0 3px">what is left
standing</span> is the tenon.</p>
{shoulder_plan_svg(v)}
<p><b>On a front leg the band off the side face swallows the whole outer strip
and {v['T_BOX_TONGUE']:g} of the slot</b>, so the only material left inside the
band is the inner strip &mdash; <b>one tab,
{v['LEG_STRIP']:g} &times; {v['TENON_CORNER']:g}</b>. On the back centre leg the
band comes off the back face alone, both strips stand, and the slot leaves
<b>{v['GRID_MEMBER_T']:g} between the two tabs</b>. That island bears nothing,
since it sits over the slot.</p>
<p>🔴 <b>The tenon carries nothing.</b> Every bit of vertical load is on the
shoulder, and the tenon is location only. <b>Which is why the slot passing
through it costs nothing</b> &mdash; a tenon is whichever strips stand inside
the band, never the leg's full width.</p>

<h3>A {v['TENON_SPACER_GAP']:g} spacer on each front tenon</h3>
<p><b>{v['TENON_SPACER_GAP']:g} &times; {v['TENON_CORNER_Y']:g} &times;
{v['POST_TENON_L']:g}, glued to the OUTER face of the tab</b>, out of
{v['TENON_SPACER_GAP']:g} Baltic birch scrap. <b>The two front legs only</b>
&mdash; the back centre leg's tabs butt the back wall's web with no gap at
all.</p>
<p>🔴 <b>Without it the box is located on a face and not on a corner.</b> A front
tab butts the front perimeter web with nothing to spare and has
<b>{v['TENON_SPACER_GAP']:g} of air to the side web</b>. Fill that, and the
composite tenon's outer face lands <b>on</b> the side web's inner face, so the
box's tongue corner is held both ways.</p>
<p>🔴 <b>Put another way, the spacer makes the composite tenon fill the whole
un-ledged band.</b> That band is {v['POST_W_X']:g} &minus;
{v['T_BOX_LEDGE']:g} = <b>{v['POST_W_X'] - v['T_BOX_LEDGE']:g}</b> across, the
tab is the one {v['LEG_STRIP']:g} of it that is solid, and the other
<b>{v['TENON_SPACER_GAP']:g} is slot</b> &mdash; which is the gap. <b>And the
band's inner edge IS the web's inner face</b>, because the ledge is as wide as
the wall and the leg's outer face is flush with the wall's. So filling the band
and landing on the web are the same thing.</p>
<p><b>Where the {v['TENON_SPACER_GAP']:g} comes from the long way round</b>, which
is the answer to why it is not {v['LEG_STRIP']:g}: the leg's outer face stands
flush with the
<b>tongue's</b> outer face, and the tongue is {v['T_BOX_TONGUE']:g} where every
other lamination is {v['LEG_STRIP']:g}. So the leg and its slot sit
{v['T_BOX_TONGUE'] - v['LEG_STRIP']:g} further outboard than an all-{v['LEG_STRIP']:g}
wall would put them: <b>{v['LEG_STRIP']:g} + {v['GRID_MEMBER_T']:g}</b> of leg
against <b>{v['T_BOX_TONGUE']:g} + {v['T_BOX_WALL_WEB']:g}</b> of wall leaves
<b>{v['TENON_SPACER_GAP']:g}</b>. <b>It moves if any of those four do.</b></p>
<p>🔴 <b>So no tenon cut in the bottom skin is a hole.</b> Each one reaches an
edge, which makes every one of them a saw cut. The two front tenons take a
<b>corner</b>, in from it to the tenon's two inboard faces plus the
{v['TENON_HOLE_CLEAR']:g} a side; the back centre's pair take <b>one notch out
of the back edge</b>, the island between them bearing nothing since it sits over
the leg's own slot. <b>The band of skin that goes with each cut is all under a
perimeter web</b>, with a {v['T_BOX_TONGUE']:g} lamination standing outside it,
so none of it shows.</p>

<h3>How deep, and what lands on it</h3>
{shoulder_section_svg(v)}
<p><b>Cut all six legs to {v['POST_W_X']:g} &times; {v['POST_W_Y']:g} first,
then cut the shoulders.</b> The two front legs are the same leg mirrored, so
trimmed to one size their tenon holes are identical and come off one setup, and
the back centre one differs only in standing the full {v['POST_W_X']:g} wide.</p>
<p>🔴 <b>Square faces matter more here than the width.</b> The shoulder is a
cross-cut and the wall lands directly over it, so a face out of square puts the
bearing on an edge instead of on a face.</p>
<p><b>Keep the holes {v['TENON_HOLE_CLEAR']:g} generous a side</b> &mdash;
{v['LEG_STRIP'] + 2 * v['TENON_HOLE_CLEAR']:g} &times;
{v['TENON_CORNER'] + 2 * v['TENON_HOLE_CLEAR']:g}. Trimming the legs to one size
makes them identical, not the assembly easy: a loaded box still has to be
lowered onto three tenons.</p>
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

    OUT.write_text(render(v), encoding="utf-8")
    print("wrote", OUT.relative_to(HERE.parent))
    return 0


def render(v):
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
<p><b>Two grids that locate and constrain all six legs</b>, three of which the
box lands on. <b>It is built BEFORE the box, and the legs before it</b> &mdash;
the box cannot be lowered onto tenons that are not located yet. All sizes in mm,
all generated from the dimension registry.</p>

<div class="note"><b>The sheet layout is its own document</b> &mdash; <a href="base-cutlist.html">base-cutlist.html</a>, which shows which sheet each piece comes off. <b>The parts are here</b>, in chapter 1, because they are read standing at the frame rather than at a sheet.</div>

{parts_html(v)}
{legs_html(v)}
{shoulder_html(v)}
{casters_html(v)}
{ends_html(v)}
<h2>6 &mdash; How it goes together</h2>
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

<h2>7 &mdash; The two side openings</h2>
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

<h2>8 &mdash; Order</h2>
<ol>
<li><b>Laminate all six legs, with a spacer in every slot.</b> Cut each spacer
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
twisted &mdash; lay them all up on one flat surface with the spacers set off a
single stop.</p>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
