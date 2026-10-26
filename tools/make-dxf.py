#!/usr/bin/env python3
"""One DXF per quote setup, for the laser/waterjet house.

    python tools/make-dxf.py

Writes machine/drawings/dxf/*.dxf. HIS STOCK SIZES, not the registry's part
sizes: he is supplying the material, so the outline is the piece he hands over
and any excess falls past the holes rather than being trimmed off a drawing.

The holes come from the shop pack's own schedules, which is the only place they
are written down once. Every schedule on these five sheets is a cross product of
its X list and its Y list, so that is how they are read, and the generated count
is checked against tools/build-hole-tally.py's independent count of the same
tables - if those two disagree the parse is wrong and the run fails.

DXF R12 ASCII, LINE, CIRCLE and ARC only. No splines, no polylines, no blocks:
every machine shop's software reads R12, and an outline made of lines cannot be
misread the way a fitted curve can. The ARC is there for the sole plates' two
fillets and is as old as the format.

The pack is read through tools/subst.py, so a schedule cell may cite a registry
symbol and the coordinate that reaches the DXF is still a number. Reading the
raw file instead would silently parse '{{ROOT_BOLT_X_DOUBLER}}' as no X at all
and write a part with holes missing.
"""
from __future__ import annotations

import math
import os
import re
import sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(HERE, '..', 'machine', 'drawings', 'shop-pack.html')
OUT = os.path.join(HERE, '..', 'machine', 'drawings', 'dxf')

sys.path.insert(0, HERE)
import subst                                                     # noqa: E402
from dims import Registry                                        # noqa: E402

MM_IN = 25.4
PLATE_RE = r'<div class="plate pg-(s[0-9a-z]+)">(.*?)(?=\n<div class="plate )'
SCHED_RE = r'<table class="sched">(.*?)</table>'

# THE FOLDER'S ORDER IS HIS, and the numeric prefix comes from position in this
# list rather than being part of a name: the three STEEL jobs first, then the
# aluminium joiners, then the fins, then the end plates. Renaming a file is
# therefore a matter of moving its line.
#
#   kind 'stock' - he supplies the piece, so the outline IS the stock and the
#                  job is holes. payload: (sheet, L, W, thickness, material,
#                  how many pieces the one drawing is for)
#   kind 'fins'  - one profile on its own square, cut twice
#   kind 'sole'  - profiles only, the shop supplies the plate
#   kind 'xep'   - an end plate with its doubler in the strip beside it
ORDER = [
    ('back-plate', 'stock', ('Y rear plate', 's7', 1211.0, 302.0, 6.19,
                             'steel', 1)),
    ('side-plates', 'stock', ('Y outboard / side plate', 's9', 1000.0, 302.0,
                              3.45, 'steel', 2)),
    ('sole-plates', 'sole', None),
    # The three INSIDE JOINING STRIPS were here and are not quoted: he drilled
    # them by hand. Sheet s8 still specifies the part - it just does not go out.
    # THE X BACK JOINING PLATE WENT THE SAME WAY, 2026-10-23: machined at home
    # and installed on the beam, so it has no drawing in the folder either.
    # Sheet s10 still specifies it. All six bolt-on plates are done.
    # THE SQUARE IS FIN_STOCK, A MEASURED 302 - the Nones are filled in build().
    # His instruction: IGNORE THE 11 7/8in THE LISTING PROMISED and use the 302
    # he reads off the piece with a precision ruler. FIN_TOP_Z arrives at the
    # same 302 off the beam top, from a different direction entirely.
    #   THE SQUARE IS STILL NOMINAL ON THE DRAWING: each fin's base edge indexes
    # on a real plate edge, opposite edges, so any shortfall lands in the gap
    # rather than on a base. His call - a fin a hair narrow is acceptable, a
    # base edge off the plate is not.
    ('front-fins', 'fins', ('Y front fin', 's1a', None, None, 10.0,
                            '6061', 2)),
    ('x-end-plate-left', 'xep', ('X gantry end plate, LEFT-HAND', 0,
                                 'XEP_CUT')),
    ('x-end-plate-right', 'xep', ('X gantry end plate, RIGHT-HAND with the '
                                  'tongue', 1, 'XEP_STOCK_L')),
    #   kind 'doubler' - the three doubler blanks on one sheet, holes only
    ('doublers', 'doubler', None),
    # THE X CARRIAGE PLATE JOINED THE WATERJET LIST, 2026-10-26 - it was on the
    # mill trip and came off it when the fins' minimum order left room. Sheet
    # s3a's stock line is the piece he hands over, so it is the same 'stock'
    # kind as the steel plates: the outline registers, the job is the holes.
    # 12.7 IS THE NOMINAL and T_X_CARRIAGE_PLATE still carries CALIPER IT - the
    # end plates' half-inch stock came in at 12.19. Nothing on the drawing
    # depends on it; it is a note for the shop.
    ('x-carriage-plate', 'stock', ('X carriage plate', 's3a', 407.0, 154.0,
                                   12.7, '6061', 1)),
]


def filename(slug):
    """1-back-plate, 2-side-plates, ... - the prefix is the position."""
    return f'{[s for s, _, _ in ORDER].index(slug) + 1}-{slug}'


# THE FIN'S THREE DIMENSIONS COME FROM THE REGISTRY, read in build(). They were
# hardcoded here as 200, 100 and 301.625, and the height is how the divergence
# showed itself: tools/make-3d.py has always taken the fin's height from
# FIN_STOCK, so the 3D model stood the fin as tall as its square while this
# writer drew it 0.375 shorter. Two tools, one part, two heights.

# THE ONE SETUP WHERE THE SHOP SUPPLIES THE METAL - his, 2026-10-16. So there is
# no stock rectangle: these are three part profiles cut from the shop's own
# plate, and the material goes on the drawing as a note for them to quote rather
# than as an outline he hands over. Everything about the shape comes out of the
# registry, which is why it is read rather than written down here again.
# ONE PART, THREE COPIES - Y1, Y2 and the X carriage. They were two drawings
# while the Y pair bolted into a plate's and a doubler's stacked end faces and
# so ran 12.19 longer; the Y joint is the X one inverted now and every
# coordinate agrees, which SOLE_SAME_AS_X_CHECK holds to.
#   (sheet, title, the symbol for its root-to-tip length, its base depth, copies)
SOLE_PARTS = [
    ('s5', 'Nut sole plate', 'SOLE_BRACKET_L', 'SOLE_BASE_D', 3),
]
SOLE_MATERIAL = '1/4in HR A36 STEEL - SHOP TO SUPPLY'
SOLE_GAP = 12.0         # between the three profiles on the one drawing

# THE TWO X END PLATES, each with its own doubler nested beside it - his,
# 2026-10-16: one 300 x 200 piece per plate. The plate is XEP_W wide out of the
# 200, which leaves a strip down one side, and DOUBLER_H is 45 precisely
# because that is what the strip holds. The doubler runs along the strip.
#   The titles, table indexes and length symbols live in ORDER.
XEP_DOUBLER_TI = 3      # Sheet 2d's schedule, the fourth in the same div
XEP_KERF = 1.0          # between the plate and the doubler in the strip


def text_of(html):
    t = re.sub(r'<[^>]+>', '', html)
    t = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), t)
    for ent, ch in (('&ndash;', '-'), ('&mdash;', '-'), ('&nbsp;', ' '),
                    ('&times;', '*'), ('&oslash;', 'o'), ('&rarr;', '->')):
        t = t.replace(ent, ch)
    return ' '.join(t.split())


def numbers(cell):
    """Every number in a cell, in order. '50, 200, 350' and '15, 45' alike."""
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', cell)]


def cols(hdr):
    """(Qty, X, Y) column indices, BY HEADER NAME and not by position.

    These used to be hardcoded 2, 3 and 4, which held only while every
    schedule carried the same seven columns in the same order. Dropping one
    column from the pack would then have shifted X and Y under the reader
    without any error: the cells still parse as numbers, so the DXF would come
    out wrong rather than refusing to build. The header is the contract.
    """
    # MATCH THE FIRST WORD, not the whole cell. An X or Y header carries the
    # edge it is measured from - "X across, from the outboard edge" - so an
    # equality test finds nothing and silently falls back to a position.
    def find(key, default):
        for i, h in enumerate(hdr):
            if h.split()[:1] == [key]:
                return i
        return default

    return tuple(find(k, d) for k, d in (('Qty', 2), ('X', 3), ('Y', 4)))


def holes_for(src, sheet, ti=None):
    """(x, y, diameter) for every drilled hole on a sheet.

    Each row is an X list crossed with a Y list - that is how these tables are
    built and what the Qty column already counts. A row whose diameter is not a
    plain number is a cut-out and is handled separately.

    `ti` PICKS ONE SCHEDULE OUT OF A SHEET THAT HOLDS SEVERAL. Sheets 2a, 2b, 2c
    and 2d all live in one pg-s2 div, so without it the two end plates would
    each come back carrying the other's holes and the shelf bar's as well - the
    same index build-hole-tally.py keys its PARTS map on.
    """
    out, cutouts, edge, merges = [], [], {}, []
    for name, blk in re.findall(PLATE_RE, src, re.S):
        if name != sheet:
            continue
        for i, t in enumerate(re.findall(SCHED_RE, blk, re.S)):
            if ti is not None and i != ti:
                continue
            hdr = [text_of(x) for x in re.findall(r'<th[^>]*>(.*?)</th>', t, re.S)]
            if 'o' not in hdr:
                continue
            dcol = hdr.index('o')
            qcol, xcol, ycol = cols(hdr)
            for tag, r in re.findall(r'(<tr[^>]*>)(.*?)</tr>', t, re.S):
                if '<th' in r or 'TOTAL' in r:
                    continue
                # AN EDGE-BORED HOLE IS NOT A WATERJET FEATURE. The jet cuts
                # through the face; a hole run into a part's end face cannot be
                # made that way at all. The pack marks those rows, so they are
                # taken out of the drawing and returned separately - the count
                # check then still reconciles against the sheet's own total.
                c = [text_of(x) for x in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
                if len(c) <= dcol:
                    continue
                dia = c[dcol].strip()
                if 'class="edge"' in tag:
                    # Its X cell is a DEPTH, not a coordinate, so there is
                    # nothing to cross against Y - take the Qty column, which
                    # is what the tally counts off too.
                    if re.match(r'^\d+(\.\d+)?$', dia):
                        edge[float(dia)] = (edge.get(float(dia), 0)
                                            + int(numbers(c[qcol])[0]))
                    continue
                xs, ys = numbers(c[xcol]), numbers(c[ycol])
                if not re.match(r'^\d+(\.\d+)?$', dia):
                    # a cut-out: the X cell holds pairs, the Y cell one pair.
                    # NOT `i` - that is the table index the ti filter reads.
                    #
                    # A ROW MARKED 'merge' IS NOT ITS OWN OPENING. The rear
                    # plate's probe notch is scheduled separately because it
                    # has its own dimensions, but it is cut as one path with
                    # the window above it - drawn as two rectangles the shop
                    # would get a line straight across the notch's mouth.
                    tgt = merges if 'class="merge"' in tag else cutouts
                    for k in range(0, len(xs), 2):
                        tgt.append((xs[k], xs[k + 1], ys[0], ys[1]))
                    continue
                for x in xs:
                    for y in ys:
                        out.append((x, y, float(dia)))
    return out, cutouts, edge, merges


def notched_window(w, n, r, layer='HOLES'):
    """One closed path: a rectangular opening with a notch off its bottom edge.

    w and n are (x0, x1, ylo, yhi). The notch's top IS the window's bottom, so
    the shared edge is not drawn - that line would be cut straight across the
    notch's mouth. Four arcs, radius r:

      - at the notch's MOUTH the metal forms a protruding corner, so the arc
        breaks that corner off and its centre sits in the metal;
      - at the notch's BOTTOM the metal wraps around the end of the notch, so
        the arc is a fillet into the metal and its centre sits in the void.
        That pair is the one that matters - this plate is a shear panel.
    """
    x0, x1, y0, y1 = w[0], w[1], w[2], w[3]
    a, b, ny0 = n[0], n[1], n[2]
    ents = []
    for p, q in (((x0, y1), (x1, y1)),            # top
                 ((x1, y1), (x1, y0)),            # far side
                 ((x1, y0), (b + r, y0)),         # bottom, past the notch
                 ((b, y0 - r), (b, ny0 + r)),     # notch, far side
                 ((b - r, ny0), (a + r, ny0)),    # notch bottom
                 ((a, ny0 + r), (a, y0 - r)),     # notch, near side
                 ((a - r, y0), (x0, y0)),         # bottom, near the notch
                 ((x0, y0), (x0, y1))):           # near side
        ents += line(p, q, layer)
    # mouth corners: centre in the metal, the quarter nearest the corner
    ents += arc(b + r, y0 - r, r, 90, 180, layer)
    ents += arc(a - r, y0 - r, r, 0, 90, layer)
    # notch bottom: centre in the void, the quarter nearest the corner
    ents += arc(b - r, ny0 + r, r, 270, 360, layer)
    ents += arc(a + r, ny0 + r, r, 180, 270, layer)
    return ents


# ---- DXF R12 -------------------------------------------------------------
def dxf_head():
    return ['0', 'SECTION', '2', 'ENTITIES']


def dxf_tail():
    return ['0', 'ENDSEC', '0', 'EOF']


def line(a, b, layer):
    return ['0', 'LINE', '8', layer,
            '10', f'{a[0]:.4f}', '20', f'{a[1]:.4f}', '30', '0.0',
            '11', f'{b[0]:.4f}', '21', f'{b[1]:.4f}', '31', '0.0']


def circle(x, y, d, layer):
    return ['0', 'CIRCLE', '8', layer,
            '10', f'{x:.4f}', '20', f'{y:.4f}', '30', '0.0',
            '40', f'{d / 2:.4f}']


def arc(x, y, r, a0, a1, layer):
    """R12 ARC. ALWAYS COUNTERCLOCKWISE from code 50 to code 51 - the format has
    no direction flag, so swapping the two angles draws the other three quarters
    of the circle rather than reversing the same arc."""
    return ['0', 'ARC', '8', layer,
            '10', f'{x:.4f}', '20', f'{y:.4f}', '30', '0.0',
            '40', f'{r:.4f}', '50', f'{a0:.4f}', '51', f'{a1:.4f}']


def text(x, y, h, s, layer):
    return ['0', 'TEXT', '8', layer,
            '10', f'{x:.4f}', '20', f'{y:.4f}', '30', '0.0',
            '40', f'{h:.2f}', '1', s]


def poly(pts, layer, close=True):
    """The run of edges through pts, closed back to the first unless told not.

    close=False IS FOR A SHARED EDGE, which the two front fins have: the second
    fin's taper is the first fin's taper, so its outline is drawn as an open run
    and the segment it is missing is the one already in the file.
    """
    out = []
    for i in range(len(pts) - (0 if close else 1)):
        out += line(pts[i], pts[(i + 1) % len(pts)], layer)
    return out


def both_units(mm):
    return f'{mm:g} mm ({mm / MM_IN:.3f} in)'


def build(name, title, sheet, L, W, T, material, qty, src, reg):
    ents, holes, cutouts, _edge, merges = [], *holes_for(src, sheet)
    fins = sheet == 's1a'

    if fins:
        L = W = reg.value('FIN_STOCK')
        base, top = reg.value('FIN_BASE_W'), reg.value('FIN_TOP_W')
        # BOTH FINS OUT OF ONE SQUARE, HEAD TO TAIL, ON ONE SHARED DIAGONAL.
        # The second fin is the first ROTATED 180 degrees about the square's
        # centre, which is what the two halves are: assembly.md says rotations
        # of each other and not mirrors, so left and right come off one profile
        # and the pair tiles the square with no waste.
        #
        # THE TAPER IS A SINGLE CUT SERVING BOTH PARTS, and that is only true
        # because base plus top closes on the square EXACTLY and the fin stands
        # as tall as the square. Break either and the two tapers stop being the
        # same line: at a 100 top they sit 2 mm apart with a sliver of 10 mm
        # plate between two separate passes, and at a fin shorter than its
        # square they are skew rather than parallel. The rotation maps the
        # diagonal onto itself, which is what SHARED_TAPER_CHECK holds to.
        ents += poly([(0, 0), (W, 0), (W, L), (0, L)], 'STOCK')
        profile = [(0, 0), (base, 0), (top, L), (0, L)]
        rot = [(W - x, L - y) for x, y in profile]
        if abs((base + top) - W) > 1e-6:
            raise SystemExit(
                f'{name}: the fins do not share one taper - base {base:g} plus '
                f'top {top:g} is {base + top:g} against a {W:g} square. '
                f'Either close it, or the drawing needs two tapers and a web '
                f'the shop has agreed to.')
        if sorted(profile[1:3]) != sorted(rot[1:3]):
            raise SystemExit(f'{name}: the rotated taper is not the same line')
        # THE TAPER GOES IN THE FILE ONCE, AND IT GOES IN LAST.
        #
        # ONCE, because drawing both profiles whole would put the shared segment
        # in twice, exactly overlapping, and a CAM package that takes the file
        # at its word cuts it twice - a second pass down an open kerf, which is
        # how an edge gets washed out.
        #
        # LAST, because it is the ONLY cut that separates the two parts. Until
        # it runs the plate is one piece and everything is held; the moment it
        # runs, both halves are loose and can tip or shift. So the order in the
        # file is holes, then the two perimeters, then the diagonal - and the
        # same order is stated in plain words on the drawing, because entity
        # order in a DXF is a HINT and not a contract. The operator programs
        # the machine; the note is what he reads.
        #
        # profile[1] -> profile[2] IS the taper, so rot's copy is rot[1] ->
        # rot[2]. Starting each open run at index 2 walks the other three edges
        # and leaves the shared one out of both.
        for x, y, d in holes:
            ents += circle(x, y, d, 'HOLES')
            ents += circle(W - x, L - y, d, 'HOLES')
        ents += poly(profile[2:] + profile[:2], 'OUTLINE', close=False)
        ents += poly(rot[2:] + rot[:2], 'OUTLINE', close=False)
        ents += line(profile[1], profile[2], 'OUTLINE')
        used = base + top
    else:
        ents += poly([(0, 0), (L, 0), (L, W), (0, W)], 'OUTLINE')
        for x, y, d in holes:
            ents += circle(x, y, d, 'HOLES')
        for cut in cutouts:
            x0, x1, y0, y1 = cut
            # a notch scheduled on its own row still belongs to this opening if
            # it hangs off the bottom edge, inside the span - the rear plate's
            # probe notch is the one, and PROBE_NOTCH_R rounds the four corners
            notch = next((m for m in merges
                          if abs(m[3] - y0) < 1e-6 and x0 <= m[0] and m[1] <= x1),
                         None)
            if notch:
                ents += notched_window(cut, notch, reg.value('PROBE_NOTCH_R'))
            else:
                ents += poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 'HOLES')
        if len(merges) != sum(
                1 for c in cutouts
                if any(abs(m[3] - c[2]) < 1e-6 and c[0] <= m[0] and m[1] <= c[1]
                       for m in merges)):
            raise SystemExit(f'{name}: a merge row found no window to join')
        used = L

    n = len(holes)
    sizes = {}
    for _, _, d in holes:
        sizes[d] = sizes.get(d, 0) + 1
    bom = ' '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes))

    ty = W + 14
    ents += text(0, ty + 20, 7, f'{title.upper()}  -  QTY {qty}', 'NOTES')
    ents += text(0, ty + 10, 5,
                 f'STOCK {both_units(L)} x {both_units(W)} x '
                 f'{both_units(T)} {material}', 'NOTES')
    ents += text(0, ty, 5, f'HOLES {bom}'
                 + ('  PER PART, BOTH PARTS DRAWN' if fins else '')
                 + (f'  +{len(cutouts)} cut-out' if cutouts else ''), 'NOTES')
    ents += text(0, ty - 10, 5, 'UNITS mm  -  ORIGIN LOWER LEFT', 'NOTES')
    if fins:
        ents += text(0, ty - 20, 5,
                     'BOTH PARTS NEST IN THE ONE SQUARE, HEAD TO TAIL.  THE '
                     'TAPER IS ONE SHARED CUT - NOT TWO', 'NOTES')
        ents += text(0, ty - 60, 5,
                     'CUT ORDER:  HOLES FIRST, THEN BOTH PERIMETERS, THEN THE '
                     'SHARED DIAGONAL LAST', 'NOTES')
        ents += text(0, ty - 70, 5,
                     'THE DIAGONAL IS THE CUT THAT PARTS THEM - UNTIL IT RUNS '
                     'THE PLATE IS ONE PIECE AND NOTHING CAN SHIFT', 'NOTES')
        ents += text(0, ty - 30, 5,
                     'THE KERF COMES OFF BOTH PARTS AT THE TAPER.  THAT IS '
                     'ACCEPTED - DO NOT ADD A WEB BETWEEN THEM', 'NOTES')
        ents += text(0, ty - 40, 5,
                     'THE SQUARE IS NOMINAL.  INDEX EACH PART\'S WIDE BASE '
                     'EDGE ON A REAL PLATE EDGE, OPPOSITE EDGES', 'NOTES')
        ents += text(0, ty - 50, 5,
                     'ANY SHORTFALL IN THE PLATE COMES OFF THE TAPERED ENDS, '
                     'NOT OFF A BASE EDGE', 'NOTES')

    path = os.path.join(OUT, name + '.dxf')
    with open(path, 'w', encoding='ascii', newline='\r\n') as fh:
        fh.write('\n'.join(dxf_head() + ents + dxf_tail()) + '\n')
    return n, len(cutouts), used, sizes


def sole_T(ox, L, D, W, S, R):
    """One sole plate's T profile, root along the bottom.

    DXF x is the part's WIDTH (machine Y, across the 154) and DXF y is its
    LENGTH (machine X, root to tip), so the drawing stands up the way Sheets 5
    and 11 draw it. Returns the entities and the two fillet centres.

    The stem is CENTRED on the root, which is Y 77 on both sheets - the plate's
    own fore-aft mid. The two re-entrant corners carry SOLE_FILLET_R, and the
    straight edges stop at the tangent points rather than running into it.
    """
    lo, hi = (W - S) / 2, (W + S) / 2          # the stem's two sides, 57 and 97
    ents = []
    for a, b in (((ox, 0), (ox + W, 0)),               # the root face
                 ((ox + W, 0), (ox + W, D)),           # base, far end
                 ((ox + W, D), (ox + hi + R, D)),      # base top, past the stem
                 ((ox + hi, D + R), (ox + hi, L)),     # stem, far side
                 ((ox + hi, L), (ox + lo, L)),         # the tip
                 ((ox + lo, L), (ox + lo, D + R)),     # stem, near side
                 ((ox + lo - R, D), (ox, D)),          # base top, near the stem
                 ((ox, D), (ox, 0))):                  # base, near end
        ents += line(a, b, 'OUTLINE')
    ents += arc(ox + hi + R, D + R, R, 180, 270, 'OUTLINE')
    ents += arc(ox + lo - R, D + R, R, 270, 360, 'OUTLINE')
    return ents


DOUBLER_GAP = 14.0      # between the three blanks on the one drawing


def build_doubler(name, src, reg):
    """The three doubler blocks on one drawing, BLANKS AND HOLES.

    THEY LOST THEIR DRAWING WHEN THE END PLATES BECAME FINISHED PARTS. Each
    doubler used to be nested in the strip beside its plate, so taking the nest
    off the end plate drawings took the only picture of their hole positions
    with it - and the blanks are sawn but not drilled. Sheet 2's schedule still
    specified them the whole time; this puts them back on a sheet of their own.

    THE OUTLINE IS REFERENCE, NOT A CUT LINE, same as the end plates: the blanks
    exist. Drawn 154 along the sheet's X and 45 up its Y, which is the turn the
    strip version used, so the schedule's X and Y swap here - its X reads up the
    45 and its Y along the 154.
    """
    W, H = reg.value('XEP_W'), reg.value('DOUBLER_H')
    t = reg.value('T_DOUBLER')

    holes, cutouts, edge, _m = holes_for(src, 's2', XEP_DOUBLER_TI)
    if cutouts:
        raise SystemExit(f'{name}: a cut-out on a doubler is not drawn')

    ents, oy, sizes, n = [], 0.0, {}, 0
    for i in range(3):
        ents += poly([(0, oy), (W, oy), (W, oy + H), (0, oy + H)], 'STOCK')
        for x, y, d in holes:
            ents += circle(y, oy + x, d, 'HOLES')
            sizes[d] = sizes.get(d, 0) + 1
            n += 1
        oy += H + DOUBLER_GAP

    tall = oy - DOUBLER_GAP
    bom = ' '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes))
    ty = tall + 24
    ents += text(0, ty + 20, 7, 'DOUBLER BLOCKS  -  QTY 3', 'NOTES')
    ents += text(0, ty + 10, 5,
                 f'PART {both_units(W)} x {both_units(H)} x {both_units(t)} '
                 f'6061  -  ALREADY SAWN TO SIZE', 'NOTES')
    ents += text(0, ty, 5, f'HOLES {bom}  -  PER BLOCK, ALL THREE DRAWN',
                 'NOTES')
    ents += text(0, ty - 10, 5,
                 'UNITS mm  -  ORIGIN LOWER LEFT OF EACH BLOCK  -  THE '
                 'OUTLINE IS REFERENCE, NOT A CUT LINE', 'NOTES')
    nedge = sum(edge.values())
    if nedge:
        ents += text(0, ty - 20, 5,
                     f'{nedge} EDGE-BORED HOLE(S) PER BLOCK ARE NOT DRAWN - '
                     f'they run into an end face and are drilled there',
                     'NOTES')

    check = {}
    for _, _, d in holes:
        check[d] = check.get(d, 0) + 1
    for d, c in edge.items():
        check[d] = check.get(d, 0) + c

    path = os.path.join(OUT, name + '.dxf')
    with open(path, 'w', encoding='ascii', newline='\r\n') as fh:
        fh.write('\n'.join(dxf_head() + ents + dxf_tail()) + '\n')
    return n, sizes, check, W, tall


def build_sole(src, reg):
    """The three nut sole plates on one drawing, PROFILES AND NO STOCK.

    The shop supplies this plate, so there is no rectangle to cut them out of -
    the outline on the page IS the part. Three of them side by side on their
    roots, which is also the order the sheets read.
    """
    W = reg.value('XEP_W')
    S = reg.value('SOLE_STEM_W')
    R = reg.value('SOLE_FILLET_R')
    T = reg.value('T_SOLE_BRACKET')

    ents, ox, tall, per_sheet, sizes, n = [], 0.0, 0.0, {}, {}, 0
    for sheet, title, l_sym, d_sym, copies in SOLE_PARTS:
        L, D = reg.value(l_sym), reg.value(d_sym)
        holes, cutouts, _edge, _m = holes_for(src, sheet)
        if cutouts:
            raise SystemExit(f'{sheet}: a cut-out on a sole plate is not drawn')
        for _ in range(copies):
            ents += sole_T(ox, L, D, W, S, R)
            for x, y, d in holes:
                ents += circle(ox + y, x, d, 'HOLES')
                sizes[d] = sizes.get(d, 0) + 1
                n += 1
            # LAYER 'PARTS', not 'NOTES': three Ts that look alike are not
            # reviewable without a name on each, so dxf-preview draws this one
            # on the figure, and it tells it from the title block by the layer
            ents += text(ox + 4, L + 6, 4.5, f'{title.upper()}  {L:g} LONG',
                         'PARTS')
            ox += W + SOLE_GAP
            tall = max(tall, L)
        per_sheet[sheet] = {}
        for _, _, d in holes:
            per_sheet[sheet][d] = per_sheet[sheet].get(d, 0) + 1

    used = ox - SOLE_GAP
    bom = ' '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes))
    ty = tall + 24
    ents += text(0, ty + 20, 7, 'NUT SOLE PLATES  -  QTY 3', 'NOTES')
    ents += text(0, ty + 10, 5, f'MATERIAL {both_units(T)} {SOLE_MATERIAL}',
                 'NOTES')
    ents += text(0, ty, 5, f'HOLES {bom}  -  ALL THROUGH', 'NOTES')
    ents += text(0, ty - 10, 5,
                 f'PROFILE TO CUT, NO STOCK OUTLINE  -  FILLETS R{R:g}  -  '
                 f'UNITS mm', 'NOTES')

    path = os.path.join(OUT, filename('sole-plates') + '.dxf')
    with open(path, 'w', encoding='ascii', newline='\r\n') as fh:
        fh.write('\n'.join(dxf_head() + ents + dxf_tail()) + '\n')
    return n, used, tall, sizes, per_sheet


def build_xep(name, title, ti, l_sym, src, reg):
    """One X end plate, FINISHED SIZE, holes only.

    BOTH PLATES ARE ALREADY CUT and their doubler blocks are already sawn out of
    them - his, 2026-10-24. So there is no stock rectangle, no profile to cut and
    no doubler nested in a strip: the part exists, and the only job left on it is
    the holes. The outline is drawn on the STOCK layer, which the preview dashes,
    because it is there to register the holes against and NOT to be cut.

    MIRRORED IN Y. His instruction: as the nest was drawn, the origin corner fell
    on the edge his bandsaw made when the doubler strip came off, and the holes
    have to be laid out from a FACTORY edge. Flipping about the horizontal axis
    moves the origin to the uncut long edge. The reference edge is called out in
    words on the drawing, so a flip in the wrong direction shows up on the print
    instead of in the metal - which on a part that cannot be re-cut is the whole
    precaution.
    """
    L = reg.value(l_sym)
    pw = reg.value('XEP_W')
    cut_y, cut_x = reg.value('CORNER_CUT_Y'), reg.value('CORNER_CUT_X_END')
    t = reg.value('T_X_ENDPLATE')

    def fy(y):
        """Mirror about the plate's own mid-height."""
        return pw - y

    ents = []
    ents += poly([(0, fy(0)), (L, fy(0)), (L, fy(cut_y)), (cut_x, fy(pw)),
                  (0, fy(pw))], 'STOCK')

    sizes, n = {}, 0
    holes, cutouts, edge, _m = holes_for(src, 's2', ti)
    if cutouts:
        raise SystemExit(f'{name}: a cut-out on an end plate is not drawn')
    for x, y, d in holes:
        ents += circle(x, fy(y), d, 'HOLES')
        sizes[d] = sizes.get(d, 0) + 1
        n += 1

    ents += text(0, -16, 4.5, f'{title.upper()} - {L:g} LONG', 'PARTS')

    bom = ' '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes))
    ty = pw + 14
    ents += text(0, ty + 20, 7, f'{title.upper()}  -  QTY 1', 'NOTES')
    ents += text(0, ty + 10, 5,
                 f'PART {both_units(L)} x {both_units(pw)} x '
                 f'{both_units(t)} 6061  -  ALREADY CUT TO SIZE', 'NOTES')
    ents += text(0, ty, 5, f'HOLES {bom}', 'NOTES')
    ents += text(0, ty - 10, 5,
                 'UNITS mm  -  ORIGIN LOWER LEFT  -  THE OUTLINE IS '
                 'REFERENCE, NOT A CUT LINE', 'NOTES')
    ents += text(0, ty - 20, 5,
                 'ORIGIN IS ON THE FACTORY LONG EDGE - the UNCUT one, NOT the '
                 'sawn edge the doubler came off', 'NOTES')
    nedge = sum(edge.values())
    if nedge:
        ents += text(0, ty - 30, 5,
                     f'{nedge} EDGE-BORED HOLE(S) ARE NOT DRAWN - they run '
                     f'into an end face and are drilled here', 'NOTES')

    # what the sheet's own total counts, which includes the edge rows
    check = dict(sizes)
    for d, c in edge.items():
        check[d] = check.get(d, 0) + c

    path = os.path.join(OUT, name + '.dxf')
    with open(path, 'w', encoding='ascii', newline='\r\n') as fh:
        fh.write('\n'.join(dxf_head() + ents + dxf_tail()) + '\n')
    return n, sizes, check


def tally_counts():
    """What build-hole-tally.py counts on each sheet, per drill size.

    A SECOND READER OF THE SAME TABLES. It walks the schedules for its own
    reasons and counts off the Qty column; this file reads the X and Y columns
    and crosses them. If the two disagree, one of them has misread a cell, and
    the whole point of a hole drawing is that it has not.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'bht', os.path.join(HERE, 'build-hole-tally.py'))
    bht = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bht)
    with open(PACK, encoding='utf-8') as fh:
        src = bht.strip_sheet_totals(fh.read())
    _, _, _, tables = bht.collect(src)
    out = {}
    for t in tables:
        # KEYED BY (sheet, table index), because pg-s2 holds four schedules and
        # the two end plates and the doubler are three of them.
        out[(t['sheet'], t['ti'])] = {float(k): v
                                      for k, v in t['own'].items()}
    return out


def main():
    # THROUGH subst, so a schedule cell may cite a registry symbol - see the
    # module docstring. It raises on an unknown one rather than writing a part
    # with a hole quietly missing.
    src = subst.read(Path(PACK).resolve())
    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print('registry does not evaluate; fix that first', file=sys.stderr)
        return 2
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    expect = tally_counts()

    # Anything from an earlier order would otherwise sit in the folder under its
    # old number and reach the shop as a ninth drawing.
    keep = {filename(s) + '.dxf' for s, _, _ in ORDER}
    for f in sorted(os.listdir(OUT)):
        if f.endswith('.dxf') and f not in keep:
            os.remove(os.path.join(OUT, f))
            print(f'  removed {f}, not in this order')

    print('STOCK IS HIS, holes are the shop pack\'s\n')
    total, bad = 0, []
    for slug, kind, payload in ORDER:
        name = filename(slug)

        if kind in ('stock', 'fins'):
            title, sheet, L, W, T, mat, qty = payload
            n, nc, used, sizes = build(name, title, sheet, L, W, T, mat, qty,
                                       src, reg)
            per_part = dict(sizes)
            if per_part != expect.get((sheet, 0)):
                bad.append(f'{name}: this file {per_part} against the tally '
                           f'{expect.get((sheet, 0))}')
            print(f'  {name:20s} sheet {sheet:4s} {n:3d} hole(s)'
                  + (f' + {nc} cut-out(s)' if nc else '')
                  + '   ' + ', '.join(f'{sizes[d]}x o{d:g}'
                                      for d in sorted(sizes)))
            if kind == 'fins':
                sq = reg.value('FIN_STOCK')
                print(f'  {"":20s} BOTH fins nested in one {sq:g} square, '
                      f'{n * 2} holes drawn, ONE shared taper - '
                      f'{reg.value("FIN_BASE_W"):g} base + '
                      f'{reg.value("FIN_TOP_W"):g} top closes on it')

        elif kind == 'sole':
            n, used, tall, sizes, per_sheet = build_sole(src, reg)
            for sheet, got in per_sheet.items():
                if got != expect.get((sheet, 0)):
                    bad.append(f'{name}: this file {got} against the tally '
                               f'{expect.get((sheet, 0))}')
            print(f'  {name:20s} sheet '
                  + '+'.join(s for s, *_ in SOLE_PARTS)
                  + f'   {n:3d} hole(s)   '
                  + ', '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes)))
            print(f'  {"":20s} 3 profiles over {used:g} x {tall:g}, '
                  f'NO STOCK - the shop supplies the plate')

        elif kind == 'doubler':
            n, sizes, got, w, tall = build_doubler(name, src, reg)
            if got != expect.get(('s2', XEP_DOUBLER_TI)):
                bad.append(f'{name}: this file {got} against the tally '
                           f'{expect.get(("s2", XEP_DOUBLER_TI))}')
            print(f'  {name:20s} sheet s2/{XEP_DOUBLER_TI}  {n:3d} hole(s)   '
                  + ', '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes)))
            print(f'  {"":20s} 3 blanks over {w:g} x {tall:g}, holes only - '
                  f'they are already sawn')

        else:                                               # 'xep'
            title, ti, l_sym = payload
            n, sizes, plate = build_xep(name, title, ti, l_sym, src, reg)
            if plate != expect.get(('s2', ti)):
                bad.append(f'{name} plate: this file {plate} against the '
                           f'tally {expect.get(("s2", ti))}')
            print(f'  {name:20s} sheet s2/{ti}  {n:3d} hole(s)   '
                  + ', '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes)))
            print(f'  {"":20s} finished size, holes only, MIRRORED IN Y - '
                  f'origin on the factory long edge')

        total += n

    if bad:
        print('\nHOLE COUNTS DISAGREE WITH tools/build-hole-tally.py:',
              file=sys.stderr)
        for b in bad:
            print('    ' + b, file=sys.stderr)
        return 1
    print(f'\n{len(ORDER)} file(s), {total} hole(s), '
          f'every count agreeing with the tally -> '
          f'{os.path.relpath(OUT, os.path.dirname(HERE))}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
