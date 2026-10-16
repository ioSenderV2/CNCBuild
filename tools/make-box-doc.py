#!/usr/bin/env python3
"""Torsion Box Construction - the whole build of the box, generated from the registry.

It was the cut list alone and the cut list is now its first chapter - his call
2026-10-15, because the sheet sizes turned out to be the smallest part of what the
sheet has to say. The chapters:

    1  Parts            every plywood piece, sized off the registry
    2  Sheets           what it takes, and the nesting drawn to scale
    3  Notches          the sliding-miter-saw procedure and what a millimetre costs
    4  Sand ports       the grid from above, dimensioned
    5  Glue up          the six joints, what each carries, and the order
    6  Not on this list

WHY THIS IS GENERATED AND NOT TYPED: every part is a plywood piece whose size
depends on the sheet thicknesses, and this is exactly what it was written for -
the sheets were micced on 2026-10-13 and came back 24 and 18 against the nominal
25 and 19 the registry had carried. One number each in registry.toml and every
part here followed. A typed list would have been wrong in the notch fits and in
the wall, which are the two that matter.

It also answers the sheet-size question, because that is not eyeballable: the
skins are BOX_W x BOX_FORE_AFT and BOX_W is within 8 mm of a 4-foot sheet.

    python tools/make-box-doc.py [--kerf 1.6] [--trim 1.6] [--sheet "4 x 8"]

Writes machine/drawings/torsion-box-construction.html and prints the summary.
No third-party imports, same as every other tool here.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dims import Registry                                    # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "machine" / "drawings" / "torsion-box-construction.html"

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
        # whole rather than divided out: a notch offset of 697.944 cannot be read
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


def plan_svg(v, ports):
    """Top-down plan of the grid with the bottom skin's ports, dimensioned.

    Drawn in MILLIMETRES - the viewBox is the part - so every coordinate below
    is the real figure and there is no scale factor to get wrong. Y runs down
    the page the same way it runs forward on the machine, so the rear plate is
    at the top of the drawing.
    """
    W = v["BOX_W"]
    web, rib, r = v["T_BOX_WALL_WEB"], v["T_BB_RIB"], v["SAND_PORT_D"] / 2
    starts = [web + s for s in
              (v["BOX_BAY_W_END"] + i * (v["BOX_BAY_W"] + rib) for i in range(4))]
    M = 150                                      # room for the dimension chains
    g = [f'<rect x="0" y="0" width="{W:g}" height="{W:g}" fill="#fbfbf8" '
         f'stroke="#333" stroke-width="2"/>']

    # the four perimeter webs, then the ribs: same layout both ways
    for x, y, w, h in ((0, 0, W, web), (0, W - web, W, web),
                       (0, 0, web, W), (W - web, 0, web, W)):
        g.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" '
                 f'fill="#d8d2c4" stroke="#333" stroke-width="1.5"/>')
    for s in starts:
        g.append(f'<rect x="{s:g}" y="{web:g}" width="{rib:g}" '
                 f'height="{W - 2 * web:g}" fill="#e8e0cc" stroke="#333" '
                 f'stroke-width="1.5"/>')
        g.append(f'<rect x="{web:g}" y="{s:g}" width="{W - 2 * web:g}" '
                 f'height="{rib:g}" fill="#e8e0cc" stroke="#333" '
                 f'stroke-width="1.5"/>')

    # the tee track bed's front edge - what puts the front row on the apron
    bed = v["TT_BED_Y0"] + v["TT_BED_FORE_AFT"]
    g.append(f'<line x1="0" y1="{bed:g}" x2="{W:g}" y2="{bed:g}" stroke="#c00" '
             f'stroke-width="3" stroke-dasharray="26 14"/>')
    g.append(f'<text x="{W - 10:g}" y="{bed - 14:g}" text-anchor="end" '
             f'font-size="26" fill="#c00">tee track bed ends {bed:g} - the row '
             f'below it is on the apron</text>')

    # ---- the three tenon holes, and the legs under them ------------------
    # Same rectangles tools/make-3d.py cuts out of the bottom skin, built from
    # the same symbols: the hole is the tenon plus TENON_HOLE_CLEAR a side, and
    # the post around it is bigger than its hole because the ledge is cut on the
    # OUTWARD faces - which is why the leg centres are not the hole centres.
    ledge, hc = v["T_BOX_LEDGE"], v["TENON_HOLE_CLEAR"]
    tcy, tb, pwx = v["TENON_CORNER_Y"], v["TENON_BACK_DEPTH"], v["POST_W_X"]
    # FLAG: THE LEG IS POST_W_X ACROSS AND THE TAB IS LEG_STRIP - this read
    # web + TENON_CORNER_X, which drew each front leg 60 wide with an 18 hole
    # sitting against the web's inner face. It was right while the corner tenon
    # was a solid 30 standing at that face; the full-height slot moved the tab
    # out to the INNER STRIP and make-3d.py was corrected for it and this was
    # not. The leg centres come off these rectangles, so the front-leg span was
    # being drawn 12 long as well.
    strip, gap = v["LEG_STRIP"], v["TENON_SPACER_GAP"]
    beyond = pwx - ledge                         # 30, the un-ledged band
    legs = [
        ("front left", (web - ledge, web + beyond,
                        W - web - tcy, W - web + ledge),
         [(web + beyond - strip, web + beyond, W - web - tcy, W - web)],
         "left"),
        ("front right", (W - web - beyond, W - web + ledge,
                         W - web - tcy, W - web + ledge),
         [(W - web - beyond, W - web - beyond + strip,
           W - web - tcy, W - web)], "right"),
        ("back centre", (W / 2 - pwx / 2, W / 2 + pwx / 2, web - ledge, web + tb),
         [(W / 2 - pwx / 2, W / 2 - pwx / 2 + strip, web, web + tb),
          (W / 2 + pwx / 2 - strip, W / 2 + pwx / 2, web, web + tb)], None),
    ]
    centres = []
    for nm, (px0, px1, py0, py1), tabs, corner in legs:
        g.append(f'<rect x="{px0:g}" y="{py0:g}" width="{px1 - px0:g}" '
                 f'height="{py1 - py0:g}" fill="none" stroke="#06c" '
                 f'stroke-width="2.5" stroke-dasharray="20 12"/>')
        if corner:
            # A CORNER, NOT A HOLE - his, 2026-10-15. The cut runs out to both
            # of the skin's edges, so the outer web-width of skin goes with it
            # and nothing wraps the corner. Drawn as the opening plus the two
            # pieces standing in it: the tab, and the spacer that fills the gap
            # to the web.
            tx0, tx1, ty0, ty1 = tabs[0]
            sx0, sx1 = ((tx0 - gap, tx0) if corner == "left"
                        else (tx1, tx1 + gap))
            ox0 = 0 if corner == "left" else min(tx0, sx0) - hc
            ox1 = max(tx1, sx1) + hc if corner == "left" else W
            g.append(f'<rect x="{ox0:g}" y="{ty0 - hc:g}" '
                     f'width="{ox1 - ox0:g}" height="{W - (ty0 - hc):g}" '
                     f'fill="#cfe0f5" stroke="#06c" stroke-width="3"/>')
            g.append(f'<rect x="{sx0:g}" y="{ty0:g}" width="{gap:g}" '
                     f'height="{ty1 - ty0:g}" fill="#f6d8de" stroke="#a00" '
                     f'stroke-width="2"/>')
            g.append(f'<rect x="{tx0:g}" y="{ty0:g}" width="{tx1 - tx0:g}" '
                     f'height="{ty1 - ty0:g}" fill="#c9a66b" stroke="#333" '
                     f'stroke-width="2"/>')
        else:
            for tx0, tx1, ty0, ty1 in tabs:
                g.append(f'<rect x="{tx0 - hc:g}" y="{ty0 - hc:g}" '
                         f'width="{tx1 - tx0 + 2 * hc:g}" '
                         f'height="{ty1 - ty0 + 2 * hc:g}" fill="#cfe0f5" '
                         f'stroke="#06c" stroke-width="3"/>')
        cx, cy = (px0 + px1) / 2, (py0 + py1) / 2
        centres.append((cx, cy))
        g.append(f'<line x1="{cx - 26:g}" y1="{cy:g}" x2="{cx + 26:g}" '
                 f'y2="{cy:g}" stroke="#06c" stroke-width="2"/>')
        g.append(f'<line x1="{cx:g}" y1="{cy - 26:g}" x2="{cx:g}" '
                 f'y2="{cy + 26:g}" stroke="#06c" stroke-width="2"/>')

    # the three leg-to-leg spans, on the centres
    (flx, fly), (frx, fry), (bcx, bcy) = centres
    g.append(f'<line x1="{flx:g}" y1="{fly + 100:g}" x2="{frx:g}" '
             f'y2="{fry + 100:g}" stroke="#06c" stroke-width="2.5"/>')
    g.append(f'<text x="{(flx + frx) / 2:g}" y="{fly + 140:g}" '
             f'text-anchor="middle" font-size="32" fill="#06c">'
             f'{v["POST_SPAN_FRONT"]:g} front leg to front leg</text>')
    g.append(f'<line x1="{frx + 100:g}" y1="{bcy:g}" x2="{frx + 100:g}" '
             f'y2="{fry:g}" stroke="#06c" stroke-width="2.5"/>')
    g.append(f'<text x="{frx + 118:g}" y="{(bcy + fry) / 2:g}" font-size="32" '
             f'fill="#06c">{v["POST_SPAN_FORE_AFT"]:g} front to back</text>')
    g.append(f'<line x1="{bcx:g}" y1="{bcy:g}" x2="{flx:g}" y2="{fly:g}" '
             f'stroke="#06c" stroke-width="1.5" stroke-dasharray="14 10"/>')
    g.append(f'<text x="{(bcx + flx) / 2 - 20:g}" y="{(bcy + fly) / 2:g}" '
             f'text-anchor="end" font-size="30" fill="#06c">'
             f'{v["POST_SPAN_DIAG"]:.1f} back to each front</text>')

    for cy in ports:
        for cx in ports:
            g.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="#fff" '
                     f'stroke="#c00" stroke-width="3"/>')
            g.append(f'<line x1="{cx - r - 10:g}" y1="{cy:g}" '
                     f'x2="{cx + r + 10:g}" y2="{cy:g}" stroke="#c00" '
                     f'stroke-width="1.5"/>')
            g.append(f'<line x1="{cx:g}" y1="{cy - r - 10:g}" x2="{cx:g}" '
                     f'y2="{cy + r + 10:g}" stroke="#c00" stroke-width="1.5"/>')

    # ONE dimension chain, along the top, and a note that it serves both ways.
    # The box is square and the grid is identical in X and Y, so a second chain
    # down the side would be the same five numbers twice.
    dy = -70
    g.append(f'<line x1="0" y1="{dy:g}" x2="{W:g}" y2="{dy:g}" stroke="#444" '
             f'stroke-width="2"/>')
    edges = [0] + list(ports) + [W]
    for p in edges:
        g.append(f'<line x1="{p:g}" y1="{dy - 18:g}" x2="{p:g}" '
                 f'y2="{dy + 18:g}" stroke="#444" stroke-width="2"/>')
        if p not in (0, W):
            # leader down to the port it dimensions, so the chain cannot be
            # read against the wrong column
            g.append(f'<line x1="{p:g}" y1="{dy:g}" x2="{p:g}" '
                     f'y2="{ports[0]:g}" stroke="#888" stroke-width="1" '
                     f'stroke-dasharray="8 8"/>')
    for a, b in zip(edges, edges[1:]):
        g.append(f'<text x="{(a + b) / 2:g}" y="{dy - 26:g}" '
                 f'text-anchor="middle" font-size="30">{b - a:g}</text>')
    g.append(f'<text x="{W / 2:g}" y="{dy - 80:g}" text-anchor="middle" '
             f'font-size="32" font-weight="600">port centres - THE SAME IN BOTH '
             f'DIRECTIONS</text>')

    # the three figures that are not in the chain
    g.append(f'<text x="{web + 12:g}" y="{W + 48:g}" font-size="28">'
             f'web and ribs {rib:g} - bays {v["BOX_BAY_W_END"]:g} at the ends, '
             f'{v["BOX_BAY_W"]:g} between - ports &#216;{v["SAND_PORT_D"]:g} '
             f'through the bottom skin, one per bay, {len(ports) ** 2} of '
             f'them</text>')
    g.append(f'<text x="0" y="{dy - 80:g}" font-size="28" fill="#555">back</text>')
    g.append(f'<text x="0" y="{W + 100:g}" font-size="28" fill="#555">front - '
             f'apron beyond</text>')

    return (f'<svg viewBox="{-M:g} {-M - 90:g} {W + 2 * M:g} {W + 2 * M + 90:g}" '
            f'width="100%" style="max-width:185mm">{"".join(g)}</svg>')


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

    rib, half, web = v["T_BB_RIB"], v["BOX_RIB_H"] / 2, v["T_BOX_WALL_WEB"]
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
<title>CNCBuild &mdash; Torsion Box Construction</title>
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
 ol.toc {{ margin: 2mm 0 5mm; padding-left: 6mm; }}
 ol.toc a {{ color: #06c; }}
</style></head><body>
<h1>Torsion Box Construction</h1>
<p>Box <b>{v['BOX_W']:.0f}</b> square by <b>{v['BOX_THK']:.0f}</b> deep. All sizes
in mm. <b>Every figure on this sheet is generated from the dimension registry</b>
&mdash; if one disagrees with the registry, this sheet is stale and gets rebuilt
rather than edited.</p>
<ol class="toc">
<li><a href="#parts">Parts</a></li>
<li><a href="#sheets">Sheets</a> and <a href="#nesting">nesting</a></li>
<li><a href="#notches">Notches</a></li>
<li><a href="#ports">Sand ports</a></li>
<li><a href="#glue">Glue up</a></li>
<li><a href="#not-here">Not on this list</a></li>
</ol>

<div class="note"><b>These are the sheets in hand</b> &mdash; {v['T_BB_SKIN_TOP']:g} and
{v['T_BB_SKIN_BOT']:g}, micced to five thousandths. Sheet sold at a nominal
commonly runs under and varies between sheets, so <b>still test-cut one notch on
scrap from the same sheet</b> before cutting the set.</div>

<h2 id="parts">1 &mdash; Parts</h2>
<table><tr><th>Part</th><th>Long</th><th>Short</th><th>Off</th></tr>
{''.join(th)}</table>

<h2 id="sheets">2 &mdash; Sheets</h2>
<p>Guillotine-packed with a <b>{KERF:g} mm</b> kerf and <b>{EDGE_TRIM:g} mm</b> off
each factory edge &mdash; a Festool track saw on Baltic birch, which is all that
gets removed. <b>The counts are an upper bound</b>: offcuts are never merged
back together, so a careful nest can still do better.</p>
<table><tr><th>Sheet</th><th>Thickness</th><th>Needs</th></tr>
{''.join(sh)}</table>

<h2 id="nesting">Nesting &mdash; {drawn}</h2>
<p>To scale, sheet length left to right. The dashed red line is the
<b>{EDGE_TRIM:g} mm</b> off each factory edge; everything sits inside it.
Offcut is whatever stays white.</p>
{''.join(ns)}

<h2 id="notches">3 &mdash; Notches</h2>
<p>Egg crate, continuous both ways, half-depth notches at every crossing. Every
notch is <b>{rib:g} wide</b> and <b>{half:g} deep</b>, and <b>all eight ribs are
the same part</b> &mdash; same length, same four offsets.</p>

<h3>Cut all eight at once, on the sliding miter saw</h3>
<p>Stack the eight ribs face to face <b>on edge</b> &mdash; {rib * 8:g} across
&mdash; clamp them as one block, set the depth stop to <b>{half:g}</b>, and
nibble each notch out in overlapping slides. Four notch positions, six or seven
passes each.</p>
<ol>
<li><b>Register the ends against a stop block, and do not unclamp until all four
notches are cut.</b> The stack is one part for as long as it is clamped; the
moment a rib shifts, that rib's notches move and nothing tells you.</li>
<li><b>A sacrificial piece of the same stock on each face of the stack.</b> It
takes the blade's exit tear-out, and it gives the clamps something to crush
instead of a finished rib.</li>
<li><b>Plywood sub-base on the saw table</b>, so the {half:g} is measured from a
continuous flat surface and not across the saw's own kerf slot.</li>
<li><b>Tall fence.</b> The ribs stand {v['BOX_RIB_H']:g} on edge, which is taller
than the saw's own fence.</li>
<li><b>Cut a test notch in an offcut first and try a real rib in it.</b> That
sets the width &mdash; nibbling means {rib:g} is where you <i>stop</i>, so it is
the one thing on this page that does not depend on a blade being the right
thickness. Check the same test notch for a <b>flat floor</b>: the cut must be
{half:g} deep all the way across, and a floor that comes out dished means the
blade is dropping rather than sliding through the cut.</li>
<li><b>Overlap each pass by about a millimetre</b> and the floor needs no
cleanup.</li>
</ol>
<p>Set the depth stop against a <b>test cut that you then measure</b>, not off the
screw.</p>
<p><b>Prove the depth on a practice pair first.</b> Cut two offcuts the way the
eight will be cut, flip one, turn it 90&deg; and cross them at <b>every</b>
station &mdash; <b>pressed flat against the reference</b>, because a released rib
bows enough to lift a station off the table and show a step that is not in the
part. Pressed flat, a correct pair reads even at every station: both bottom edges
down, both top edges flush, notch floors just meeting.</p>
<p>Notch depth <b>half, and err over rather than under</b>. The fit across the
notch is a slip fit, not a clearance: too tight splits the rib, too loose leaves
no glue line.</p>
<p><b>The notches are the layout</b> &mdash; a rib sits where the mating rib's
notch puts it, not at a measured position &mdash; so of the four ways to be a
millimetre out, only one touches the structure:</p>
<table>
<tr><th>Error</th><th>What happens</th></tr>
<tr><td><b>A position off by 1, on all eight</b></td><td>Nothing jams. The eight
are identical, so the grid stays self-consistent and that rib line lands 1 off
the drawing. Bays go {bay + 1:g} and {bay - 1:g}</td></tr>
<tr><td><b>One rib of the eight off</b></td><td>That rib will not drop in &mdash;
pare or recut it. This is what the stop block and the do-not-unclamp rule are
for</td></tr>
<tr><td><b>A notch too wide by 1</b></td><td>Slop at every crossing, so the grid
stops holding itself square. Square it on the reference before the skins go on.
<b>Too narrow splits a rib</b></td></tr>
<tr><td><b>A notch too deep by 1</b></td><td><b>Harmless, and the side to err
on.</b> The rib stands on the bottom skin so it cannot sink - both edges still
reach both skins, and all that is lost is notch floor to notch floor, which
carries nothing</td></tr>
<tr><td>&#128308; <b>A notch too shallow by 1</b></td><td><b>The only structural
one.</b> It holds its mating rib up off the bottom skin, so the top skin bears on
that set and sits clear of the rest of the grid</td></tr>
<tr><td><b>A step that closes when you press the rib flat</b></td><td>Not an
error - the rib's own bow lifting it off the reference. Check every station
pressed flat, and measure depth on a <b>released</b> rib, never on the clamped
stack</td></tr>
</table>
<p><b>So the figure to get right at setup is the depth stop &mdash; and only in
one direction.</b> The stop block's position is forgiving, over-depth is
forgiving, under-depth is not. <b>Aim half a millimetre over</b> and let the
rib's bow live inside it.</p>
<p><b>Cut all eight from the same edge, then turn four of them over.</b> One
direction has to be notched from the top edge and the other from the bottom, and
that costs nothing here because the notch is <i>exactly</i> half of
{v['BOX_RIB_H']:g}: a rib turned upside down is a rib notched from the other
edge. The offsets do not care either &mdash; the run is symmetric end to end, so
a rib fitted backwards still fits.</p>
<p>So the eight stay one part right through the notching, and the only cut that
tells a rib which way up it goes is the <b>sand relief at the bottom edge</b>,
done afterwards on whichever edge ends up down.</p>
{''.join(nt)}
<p>Notch the bottom edge of every rib where it meets the bottom skin, roughly
20 &times; 15, so the sand can migrate between cells.</p>

<h2 id="ports">4 &mdash; Sand ports</h2>
<p><b>{v['SAND_PORT_D']:g} through both skins, {len(ports)} &times; {len(ports)} =
{len(ports) ** 2} in each</b>, one centred in every bay. Centres from the skin's
edge, <b>the same figures in X and Y</b> &mdash; the box is square and the grid is
the same both ways:</p>
<table><tr><th>Port</th>{''.join(f'<th>{i + 1}</th>' for i in range(len(ports)))}</tr>
<tr><td>Centre</td>{''.join(f'<td class=n>{p:g}</td>' for p in ports)}</tr></table>

<h3>The grid from above, with the bottom skin's ports</h3>
{plan_svg(v, ports)}
<p><b>The steps are not equal</b> &mdash; {v['SAND_PORT_STEP_END']:g} at each end of
the row and {v['SAND_PORT_STEP']:g} through the middle, because the end bays are
wider. Walking it as a constant pitch puts the far port in the wrong place.</p>
<p>The bottom port takes a <b>rubber plug fitted from below with a pull tab
underneath</b> &mdash; nothing goes in from above and nothing is attached to it.
Pull it to drain, push it back to seal. The sand bearing on one plug is only
<b>{v['SAND_PORT_PLUG_LOAD'] * 1000:.0f} grams</b>, so friction is all it needs.
<b>Fill through the top ports once, at assembly, before the bed goes down</b>:
the bed cannot come out of the assembled machine.</p>
<p>The tee track bed covers all but the <b>front row</b> of five, which lands on
the open apron. <b>{v['T_APRON_SKIN']:g} Baltic birch over the apron on
double-sided tape</b> covers those &mdash; a cover, not structure, so it comes off
the day a port is used.</p>

<h2 id="glue">5 &mdash; Glue up</h2>
<p><b>Six joints, and only the first two carry the sandwich.</b></p>
<table>
<tr><th>Joint</th><th>Where</th><th>What it carries</th></tr>
<tr><td><b>Rib edge to skin</b></td><td>every rib's top edge to the top skin and
bottom edge to the bottom skin, the full {v['BOX_CAVITY_W']:g} &times; {rib:g} of
each, both ends of all eight</td><td><b>This is the box.</b> The skins are the
flanges and the ribs carry shear between them. Starve it anywhere and the section
is locally gone</td></tr>
<tr><td><b>Web edge to skin</b></td><td>the four perimeter webs, same joint, top
and bottom edges</td><td>the same, round the perimeter</td></tr>
<tr><td><b>Notch cheek to rib face</b></td><td>the sixteen crossings, face to
face, {rib:g} wide &times; {half:g} deep on each side of every notch</td><td>the
<b>two-way plate action</b> &mdash; the reason this is an egg crate and not
blocking. Face-to-face plywood, the strong orientation</td></tr>
<tr><td><b>Tongue to web face</b></td><td>the outer lamination glued flat to the
inner web over the whole {v['TONGUE_FULL_H']:g} height and full length, back and
both sides, and the front cap doing the same</td><td>makes the
{v['T_BOX_WALL']:g} wall one piece, which is what lets the standing plates bolt
through it in bearing. The biggest area in the box</td></tr>
<tr><td><b>Tongue to skin end grain</b></td><td>the tongue caps the end grain of
both skins rather than standing on them</td><td>closes the edge; not a load
path</td></tr>
<tr><td><b>Rib end to web face</b></td><td>each rib's {rib:g} &times;
{v['BOX_RIB_H']:g} end butting a perimeter web's inner face, sixteen of
them</td><td><b>Weak by nature</b> &mdash; plywood edge onto face &mdash; and
nothing relies on it. It is the joint the blocking scheme would have had at
<i>every</i> junction, which is why blocking was rejected</td></tr>
</table>
<p><b>Two things that look like joints and are not.</b> <b>Notch floor to notch
floor</b> &mdash; no glue reaches it and nothing asks it to carry anything, which
is why over-depth there is free. And <b>the post tenons</b>, which are not glued
at all: the box is lowered onto three tenons and the shoulder carries it.</p>

<h3>Dominos &mdash; where they go, and where they must not</h3>
<table>
<tr><th>Where</th><th></th></tr>
<tr><td><b>The four web corners</b></td><td><b>Two each, eight in all.</b> That
butt has nothing else locating it &mdash; a side web's end against the back or
front web's inner face &mdash; and it is where racking shows before the skins go
on. Two stop rotation as well as sliding; one does not</td></tr>
<tr><td><b>The outer laminations</b></td><td><b>A few per side.</b> The tongue is
a {v['TONGUE_FULL_H']:g} &times; full-length face glue-up with no mechanical
location at all, it floats on the glue, and it has to finish flush with the top
skin. Same for the front cap. Screws from the inside do the same job</td></tr>
<tr><td>🔴 <b>NOT in the rib ends</b></td><td><b>Over-constraint, not cost.</b>
Every rib is already located twice &mdash; the notches fix it against every
crossing rib, the bottom skin fixes its height &mdash; so pinning both ends into
the webs is a third constraint that has to agree with the first two to a fraction
of a millimetre, sixteen rib ends against sixteen crossings, with nowhere for the
disagreement to go. A rib end that lands half a millimetre shy is invisible and
harmless now; with a Domino in it, it is a part that will not seat. And that joint
carries nothing</td></tr>
</table>
<p><b>Cutter size and depth are a shop choice, but two things bound it:</b> the
mortise in the web's <b>end</b> has the whole length behind it, while the one in
the mating web's <b>face</b> is cutting into {web:g} of thickness &mdash; so keep
that side shallow and leave material behind it, because the tongue glues to that
outer face. And the two depths together have to exceed the tenon's length.</p>

<h3>The order, and why the top stays loose</h3>
<p>🔴 <b>The top skin is not glued until the whole machine is proven.</b>
Everything up to the top goes together permanently, the top is laid in on
<b>four temporary screws</b>, and the box is <b>not sealed</b> until the entire
assembly &mdash; the CNC on top of it included &mdash; has been verified.</p>
<ol>
<li><b>Dry-assemble the grid on the flat reference</b> &mdash; four ribs one way,
four the other, into the perimeter webs. Press every crossing flat and check it
seats. An egg crate self-jigs, so this is also the squareness check.</li>
<li><b>Glue the egg crate and the perimeter webs as one assembly</b>, two Dominos
at each corner.</li>
<li><b>Glue and screw the bottom skin on</b>, still on the reference. Its four
tenon holes are already cut.</li>
<li><b>When it is dry, flip the box</b> so the bottom is down and the open side
is up. Nothing goes into the post tenons</li>
<li><b>Glue the outer laminations on</b>, on their own pins, the tongues capping
the bottom skin's end grain and standing proud of where the top skin will sit.
<b>Pull each lamination down with 1&frac12;" countersunk screws from inside the
cavity</b>, through the {web:g} web into the {v['T_BOX_TONGUE']:g} tongue &mdash;
that is the clamping pressure while the glue dries, on all four walls, and the
cavity is open at this stage which is what makes driving them easy.
<b>Nothing longer</b>: head flush with the web, 38.1 leaves <b>3.9</b> before the
tongue's outer face, which is the face the standing plates bolt against, and a
1&frac34;" comes through it by 2.5</li>
<li><b>Lay the top skin in on four temporary screws. DO NOT GLUE IT.</b> It drops
between the tongues, which stand {v['BOX_TONGUE_PROUD']:g} proud of it.</li>
<li><b>Build the machine on it and verify the whole assembly.</b> Everything above
the box stays reversible while the top is only screwed.</li>
<li><b>Only then seal it</b>: fit the fin angles' T-nuts into the top skin from
underneath, glue the top on and clamp it hard onto the rib edges. Screws through
the skin into the ribs give uniform pressure and can stay in; the 52 inch
parallel clamps go across the top, <b>one over each rib</b>, so the pressure lands
on structure and not on unsupported skin.</li>
<li><b>Sand last</b>, through the top ports.</li>
</ol>
<p><b>The T-nuts stop being a trap.</b> They still have to go in before the top
skin is <b>glued</b>, but with the top only screwed they can be fitted any time up
to that &mdash; lift it, drop them in, put it back. That was the one step in this
build with no way back.</p>

<h2 id="not-here">6 &mdash; Not on this list</h2>
<p><b>The five legs, and they come FIRST.</b> The base holds the three
load-bearing legs in position, so it is built before the box and the legs before
it. Each leg is laminated from <b>{v['T_BB_SKIN_BOT']:g} mm strips 4 ft long</b>,
trimmed square after the glue dries and cut to length off the standing base. They
come off a <b>second sheet of {v['T_BB_SKIN_BOT']:g}</b> &mdash; so the box and
its legs together are one sheet of {v['T_BB_SKIN_TOP']:g} and <b>two</b> of
{v['T_BB_SKIN_BOT']:g}, not the two sheets the Sheets chapter counts for the box
alone. Each leg finishes <b>{v['POST_W_X']:g} across the machine by {v['POST_W_Y']:g}
fore and aft</b> &mdash; the {v['POST_W_X']:g} is the lamination, and it runs
across the machine so the base's fore-aft rails can pass through the leg as a
through tenon left open at glue-up.</p>
<p><b>The two blocks beside the back centre tenon.</b> They are location pieces
inside the box, carry no load, and their thickness is free &mdash; so they come
out of the scrap bin rather than off a sheet. They must be <b>{v['BOX_RIB_H']:.0f}
tall</b> like a rib so both skins glue to them, and no thicker than
<b>{v['BACK_TENON_BLOCK_T_MAX']:.1f}</b>, which is the clear space each side of
the tenon.</p>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
