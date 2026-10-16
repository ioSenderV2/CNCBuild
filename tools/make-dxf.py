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

DXF R12 ASCII, LINE and CIRCLE only. No splines, no polylines, no blocks: every
machine shop's software reads R12, and an outline made of lines cannot be
misread the way a fitted curve can.
"""
from __future__ import annotations

import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(HERE, '..', 'machine', 'drawings', 'shop-pack.html')
OUT = os.path.join(HERE, '..', 'machine', 'drawings', 'dxf')

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
     'steel', 1),
    ('4-inside-joiners', 'Inside joining strip', 's8', 1000.0, 50.0, 3.0,
     'steel', 3),
    ('5-front-fins', 'Y front fin', 's1a', 302.0, 302.0, 12.13,
     '6061', 2),
]

FIN_BASE, FIN_TOP, FIN_H = 200.0, 100.0, 301.625
FIN_GAP = 1.0           # between the two nested fins


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
    with open(PACK, encoding='utf-8') as fh:
        src = fh.read()
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
    if bad:
        print('\nHOLE COUNTS DISAGREE WITH tools/build-hole-tally.py:',
              file=sys.stderr)
        for b in bad:
            print('    ' + b, file=sys.stderr)
        return 1
    print(f'\n{len(SETUPS)} file(s), {total} hole(s), '
          f'every count agreeing with the tally -> '
          f'{os.path.relpath(OUT, os.path.dirname(HERE))}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
