#!/usr/bin/env python3
"""Every Ref in a hole schedule must appear on that sheet's drawing.

A schedule row says "drill K1-K6 at X 360, 373, 403" and the drawing shows six circles.
Nothing connects the two unless the drawing carries the tag, and the reader is left
matching coordinates by eye. This checks the connection exists.

The rule: for each sheet, every Ref in its <table class="sched"> must appear as a
<text class="ref"> tag somewhere in that same sheet's SVG.

    python tools/check-shop-pack-refs.py

Exit 0 when every sheet is covered, 1 when any ref is untagged.
"""
import io
import os
import re
import sys

try:
    unichr
except NameError:   # py3
    unichr = chr

PACK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'machine', 'drawings', 'shop-pack.html')


def text_of(html):
    """Strip tags and resolve entities, so a character count is a character count."""
    t = re.sub(r'<[^>]+>', '', html)
    t = re.sub(r'&#(\d+);', lambda m: unichr(int(m.group(1))), t)
    for ent, ch in (('&ndash;', '-'), ('&mdash;', '-'), ('&hellip;', '...'),
                    ('&nbsp;', ' '), ('&amp;', '&'), ('&times;', '*'),
                    ('&oslash;', 'o'), ('&middot;', '.'), ('&rarr;', '>'),
                    ('&minus;', '-'), ('&plus;', '+'), ('&rsquo;', "'"),
                    ('&apos;', "'"), ('&quot;', '"'), ('&lt;', '<'), ('&gt;', '>')):
        t = t.replace(ent, ch)
    return ' '.join(t.split())


def refs_in_schedules(block):
    """First cell of every data row in every table.sched on this sheet."""
    out = []
    for table in re.findall(r'<table class="sched">(.*?)</table>', block, re.S):
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.S):
            if '<th' in row:
                continue
            cell = re.match(r'\s*<td[^>]*>(.*?)</td>', row, re.S)
            if cell:
                ref = text_of(cell.group(1))
                if ref:
                    out.append(ref)
    return out


def tags_in_drawing(block):
    return [text_of(t) for t in re.findall(r'<text class="ref"[^>]*>(.*?)</text>', block, re.S)]


def expand(ref):
    """The members a row ref stands for.

    Schedules write ranges two ways and a drawing may tag either the range as a whole
    or every hole in it:
        X1-X16   -> X1 X2 ... X16        (numeric tail)
        R1a-g    -> R1a R1b ... R1g      (letter tail, prefix carried)
        TS1, TS2 -> TS1 TS2              (comma list)
    """
    parts = [p.strip() for p in ref.split(',') if p.strip()]
    if len(parts) > 1:
        return parts

    m = re.match(r'^([A-Za-z]+)(\d+)-(?:\1)?(\d+)$', ref)
    if m:
        pre, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
        if lo <= hi:
            return ['%s%d' % (pre, i) for i in range(lo, hi + 1)]

    m = re.match(r'^([A-Za-z]+\d+)([a-z])-(?:\1)?([a-z])$', ref)
    if m:
        pre, lo, hi = m.group(1), m.group(2), m.group(3)
        if lo <= hi:
            return ['%s%s' % (pre, chr(c)) for c in range(ord(lo), ord(hi) + 1)]

    return [ref]


def covered(ref, tags):
    """Tagged as the whole range, or with every member tagged individually."""
    if ref in tags:
        return True
    members = expand(ref)
    return len(members) > 1 and all(m in tags for m in members)


# Rough advance width per character, as a fraction of font-size, for the sans-serif
# these sheets render in. Deliberately a little low so the check warns rather than nags.
GLYPH = 0.50
FONT = {'q': 8.0, 'lbl': 8.0, 'dim': 7.0, 'ref': 8.5}


def clipped_text(block):
    """Text that runs outside its own viewBox.

    This has bitten three sheets already and it is invisible when it happens - the
    line does not truncate with an ellipsis, it simply is not on the page, and the
    legend above it still reads as complete.
    """
    out = []
    # a page may hold several drawings - sheet 2 carries 2a, 2b, 2c and 2d - and each
    # has its own viewBox, so every svg is measured against its own box
    for svg in re.findall(r'<svg .*?</svg>', block, re.S):
        out.extend(_clipped_in_svg(svg))
    return out


def _clipped_in_svg(block):
    vb = re.search(r'<svg viewBox="\s*(-?[\d.]+)\s+(-?[\d.]+)\s+([\d.]+)\s+([\d.]+)"', block)
    if not vb:
        return []
    x0, y0, w, h = [float(g) for g in vb.groups()]
    out = []
    for m in re.finditer(r'<text class="([a-z]+)"([^>]*)>(.*?)</text>', block, re.S):
        cls, attrs, body = m.group(1), m.group(2), text_of(m.group(3))
        xm = re.search(r'\bx="(-?[\d.]+)"', attrs)
        ym = re.search(r'\by="(-?[\d.]+)"', attrs)
        if not xm or not ym:
            continue
        x, yy = float(xm.group(1)), float(ym.group(1))
        width = len(body) * GLYPH * FONT.get(cls, 8.0)
        if 'text-anchor="middle"' in attrs:
            lo, hi = x - width / 2.0, x + width / 2.0
        elif 'text-anchor="end"' in attrs:
            lo, hi = x - width, x
        else:
            lo, hi = x, x + width
        why = []
        if hi > x0 + w:
            why.append('%.0f past the right edge' % (hi - (x0 + w)))
        if lo < x0:
            why.append('%.0f past the left edge' % (x0 - lo))
        if yy > y0 + h:
            why.append('%.0f below the bottom' % (yy - (y0 + h)))
        if yy < y0:
            why.append('%.0f above the top' % (y0 - yy))
        if why:
            # the Windows console is cp1252, and a warning triangle must not be the
            # thing that stops a check from reporting
            safe = body[:46].encode('ascii', 'replace').decode('ascii')
            out.append((safe, ', '.join(why)))
    return out


def main():
    src = io.open(PACK, encoding='utf-8').read()
    sheets = re.findall(r'<div class="plate pg-(s[0-9a-z]+)">(.*?)(?=\n<div class="plate )',
                        src, re.S)
    if not sheets:
        print('no sheets found - has the pack structure changed?')
        return 1

    bad = 0
    clip = 0
    for name, block in sheets:
        for body, why in clipped_text(block):
            clip += 1
            print('sheet %-6s OFF THE DRAWING (%s): %s' % (name[1:], why, body))
    if clip:
        print()

    for name, block in sheets:
        refs = refs_in_schedules(block)
        if not refs:
            continue
        tags = tags_in_drawing(block)
        missing = [r for r in refs if not covered(r, tags)]
        label = 'sheet ' + name[1:]
        if missing:
            bad += len(missing)
            print('%-12s %2d of %2d refs NOT on the drawing: %s'
                  % (label, len(missing), len(refs), ', '.join(missing)))
        else:
            print('%-12s all %2d refs tagged' % (label, len(refs)))

    print()
    if clip:
        print('%d lines of text fall outside their viewBox and will not print.' % clip)
    if bad:
        print('%d refs appear in a schedule but nowhere on their drawing.' % bad)
    if bad or clip:
        return 1
    print('Every schedule ref is tagged on its drawing, and no text falls off a sheet.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
