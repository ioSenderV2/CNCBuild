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

# HIS STOCK, given 2026-10-16. (file, title, sheet, stock L, stock W, thickness,
# material, how many pieces the one drawing is for)
SETUPS = [
    ('1-back-plate', 'Y rear plate', 's7', 1211.0, 302.0, 6.19,
     'steel', 1),
    ('2-side-plates', 'Y outboard / side plate', 's9', 1000.0, 302.0, 3.39,
     'steel', 2),
    ('3-x-back-joiner', 'X back joining plate', 's10', 1000.0, 120.0, 6.42,
     '6061', 1),
    ('4-inside-joiners', 'Inside joining strip', 's8', 1000.0, 50.0, 3.0,
     '6061', 3),
    ('5-front-fins', 'Y front fin', 's1a', 302.0, 302.0, 10.0,
     '6061', 2),
]

FIN_BASE, FIN_TOP, FIN_H = 200.0, 100.0, 301.625
FIN_GAP = 1.0           # between the two nested fins

# THE ONE SETUP WHERE THE SHOP SUPPLIES THE METAL - his, 2026-10-16. So there is
# no stock rectangle: these are three part profiles cut from the shop's own
# plate, and the material goes on the drawing as a note for them to quote rather
# than as an outline he hands over. Everything about the shape comes out of the
# registry, which is why it is read rather than written down here again.
#   (sheet, title, the symbol for its root-to-tip length, its base depth)
SOLE_PARTS = [
    ('s5', 'Y nut sole bracket', 'SOLE_BRACKET_L', 'SOLE_BASE_D', 2),
    ('s11', 'X nut sole plate', 'X_SOLE_BRACKET_L', 'T_X_ENDPLATE', 1),
]
SOLE_FILE = '6-sole-plates'
SOLE_MATERIAL = '1/4in HR A36 STEEL - SHOP TO SUPPLY'
SOLE_GAP = 12.0         # between the three profiles on the one drawing


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


def holes_for(src, sheet):
    """(x, y, diameter) for every drilled hole on a sheet.

    Each row is an X list crossed with a Y list - that is how these tables are
    built and what the Qty column already counts. A row whose diameter is not a
    plain number is a cut-out and is handled separately.
    """
    out, cutouts = [], []
    for name, blk in re.findall(PLATE_RE, src, re.S):
        if name != sheet:
            continue
        for t in re.findall(SCHED_RE, blk, re.S):
            hdr = [text_of(x) for x in re.findall(r'<th[^>]*>(.*?)</th>', t, re.S)]
            if 'o' not in hdr:
                continue
            dcol = hdr.index('o')
            for r in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
                if '<th' in r or 'TOTAL' in r:
                    continue
                c = [text_of(x) for x in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
                if len(c) <= dcol:
                    continue
                dia = c[dcol].strip()
                xs, ys = numbers(c[3]), numbers(c[4])
                if not re.match(r'^\d+(\.\d+)?$', dia):
                    # a cut-out: the X cell holds pairs, the Y cell one pair
                    for i in range(0, len(xs), 2):
                        cutouts.append((xs[i], xs[i + 1], ys[0], ys[1]))
                    continue
                for x in xs:
                    for y in ys:
                        out.append((x, y, float(dia)))
    return out, cutouts


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


def poly(pts, layer):
    out = []
    for i in range(len(pts)):
        out += line(pts[i], pts[(i + 1) % len(pts)], layer)
    return out


def both_units(mm):
    return f'{mm:g} mm ({mm / MM_IN:.3f} in)'


def build(name, title, sheet, L, W, T, material, qty, src):
    ents, holes, cutouts = [], *holes_for(src, sheet)
    fins = sheet == 's1a'

    if fins:
        # two nested head to tail, the straight outboard edge on the outside
        a = [(0, 0), (FIN_BASE, 0), (FIN_TOP, FIN_H), (0, FIN_H)]
        dx = FIN_BASE + FIN_TOP + FIN_GAP
        b = [(dx - x, FIN_H - y) for x, y in a]
        for pts in (a, b):
            ents += poly(pts, 'OUTLINE')
        for x, y, d in holes:
            ents += circle(x, y, d, 'HOLES')
            ents += circle(dx - x, FIN_H - y, d, 'HOLES')
        used = dx
    else:
        ents += poly([(0, 0), (L, 0), (L, W), (0, W)], 'OUTLINE')
        for x, y, d in holes:
            ents += circle(x, y, d, 'HOLES')
        for x0, x1, y0, y1 in cutouts:
            ents += poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 'HOLES')
        used = L

    n = len(holes) * (2 if fins else 1)
    sizes = {}
    for _, _, d in holes:
        sizes[d] = sizes.get(d, 0) + (2 if fins else 1)
    bom = ' '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes))

    ty = W + 14
    ents += text(0, ty + 20, 7, f'{title.upper()}  -  QTY {qty}', 'NOTES')
    ents += text(0, ty + 10, 5,
                 f'STOCK {both_units(L)} x {both_units(W)} x '
                 f'{both_units(T)} {material}', 'NOTES')
    ents += text(0, ty, 5, f'HOLES {bom}'
                 + (f'  +{len(cutouts)} cut-out' if cutouts else ''), 'NOTES')
    ents += text(0, ty - 10, 5, 'UNITS mm  -  ORIGIN LOWER LEFT', 'NOTES')

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
        holes, cutouts = holes_for(src, sheet)
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

    path = os.path.join(OUT, SOLE_FILE + '.dxf')
    with open(path, 'w', encoding='ascii', newline='\r\n') as fh:
        fh.write('\n'.join(dxf_head() + ents + dxf_tail()) + '\n')
    return n, used, tall, sizes, per_sheet


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
        if t['ti'] == 0:
            out[t['sheet']] = {float(k): v for k, v in t['own'].items()}
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

    print('STOCK IS HIS, holes are the shop pack\'s\n')
    total, bad = 0, []
    for name, title, sheet, L, W, T, mat, qty in SETUPS:
        n, nc, used, sizes = build(name, title, sheet, L, W, T, mat, qty, src)
        total += n
        per_part = {d: c // (2 if sheet == 's1a' else 1)
                    for d, c in sizes.items()}
        if per_part != expect.get(sheet):
            bad.append(f'{sheet}: this file {per_part} against the tally '
                       f'{expect.get(sheet)}')
        spare = (302.0 - used) if sheet == 's1a' else (L - used)
        print(f'  {name:18s} sheet {sheet:4s} {n:3d} hole(s)'
              + (f' + {nc} cut-out(s)' if nc else '')
              + f'   {", ".join(f"{sizes[d]}x o{d:g}" for d in sorted(sizes))}')
        if sheet == 's1a':
            print(f'  {"":18s} nest {used:g} across a {302:g} square, '
                  f'{spare:g} spare')

    n, used, tall, sizes, per_sheet = build_sole(src, reg)
    total += n
    for sheet, got in per_sheet.items():
        if got != expect.get(sheet):
            bad.append(f'{sheet}: this file {got} against the tally '
                       f'{expect.get(sheet)}')
    print(f'  {SOLE_FILE:18s} sheets '
          + '+'.join(s for s, *_ in SOLE_PARTS)
          + f' {n:3d} hole(s)   '
          + ', '.join(f'{sizes[d]}x o{d:g}' for d in sorted(sizes)))
    print(f'  {"":18s} 3 profiles over {used:g} x {tall:g}, '
          f'NO STOCK - the shop supplies the plate')

    if bad:
        print('\nHOLE COUNTS DISAGREE WITH tools/build-hole-tally.py:',
              file=sys.stderr)
        for b in bad:
            print('    ' + b, file=sys.stderr)
        return 1
    print(f'\n{len(SETUPS) + 1} file(s), {total} hole(s), '
          f'every count agreeing with the tally -> '
          f'{os.path.relpath(OUT, os.path.dirname(HERE))}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
