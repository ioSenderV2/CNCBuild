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

PACK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'machine', 'drawings', 'shop-pack.html')


def text_of(html):
    """Strip tags and normalise the entities the pack actually uses."""
    t = re.sub(r'<[^>]+>', '', html)
    for ent, ch in (('&ndash;', '-'), ('&#8211;', '-'), ('&mdash;', '-'),
                    ('&hellip;', '...'), ('&nbsp;', ' '), ('&amp;', '&')):
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


def covered(ref, tags):
    """A row ref may be tagged as a whole ("K1-K6") or by its parts ("TS1" + "TS2")."""
    if ref in tags:
        return True
    parts = [p.strip() for p in ref.split(',') if p.strip()]
    return len(parts) > 1 and all(p in tags for p in parts)


def main():
    src = io.open(PACK, encoding='utf-8').read()
    sheets = re.findall(r'<div class="plate pg-(s[0-9a-z]+)">(.*?)(?=\n<div class="plate )',
                        src, re.S)
    if not sheets:
        print('no sheets found - has the pack structure changed?')
        return 1

    bad = 0
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
    if bad:
        print('%d refs appear in a schedule but nowhere on their drawing.' % bad)
        return 1
    print('Every schedule ref is tagged on its drawing.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
