#!/usr/bin/env python3
"""The base nest places nothing twice, nothing off the sheet, nothing missing.

    python tools/check-cutlist-nest.py

A band packer written by hand can overlap two pieces or run one past the
sheet's edge and the drawing still looks plausible - the rectangles are small
and a few millimetres of overlap is invisible at 1:14. So the three things
that would make the nest a lie get checked:

  - every piece in the cutlist is placed exactly once;
  - no two placed pieces overlap, kerf included;
  - every piece lies inside the sheet's usable area.

Exit 0 when the nest is sound, 1 on the first failure, naming the pieces.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from dims import Registry                                    # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "cutdoc", HERE / "make-cutlist-doc.py")
cutdoc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cutdoc)
boxdoc = cutdoc.boxdoc


def overlaps(a, b, slack=1e-6):
    ax, ay, aw, ah, _ = a
    bx, by, bw, bh, _ = b
    return (ax < bx + bw - slack and bx < ax + aw - slack
            and ay < by + bh - slack and by < ay + ah - slack)


def main():
    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate", file=sys.stderr)
        return 2
    v = {s: reg.value(s) for s in reg.order}

    gs = cutdoc.groups(v)
    five, fours, u48, u55 = cutdoc.nest(v, gs)

    want = {}
    for gname, _q, _w, rows in gs:
        for name, _a, _b, q, _n in rows:
            want["%s / %s" % (gname, name)] = want.get(
                "%s / %s" % (gname, name), 0) + q

    got, bad = {}, []
    sheets = [("1 (5 x 5)", five[0], u55)] + [
        ("%d (4 x 8)" % i, placed, u48)
        for i, (placed, _l) in enumerate(fours, start=2)]

    for label, placed, (uw, ul) in sheets:
        for p in placed:
            got[p[4]] = got.get(p[4], 0) + 1
            x, y, w, h, name = p
            if x < -1e-6 or y < -1e-6 or x + w > uw + 1e-6 or y + h > ul + 1e-6:
                bad.append("sheet %s: %s runs off the sheet - %.1f,%.1f "
                           "%.1fx%.1f in %gx%g"
                           % (label, name, x, y, w, h, uw, ul))
        for i in range(len(placed)):
            for j in range(i + 1, len(placed)):
                if overlaps(placed[i], placed[j]):
                    bad.append("sheet %s: %s overlaps %s"
                               % (label, placed[i][4], placed[j][4]))

    for name, n in sorted(want.items()):
        if got.get(name, 0) != n:
            bad.append("%s: cutlist wants %d, nest places %d"
                       % (name, n, got.get(name, 0)))
    for name in sorted(got):
        if name not in want:
            bad.append("%s: placed but not in the cutlist" % name)

    if bad:
        print("NEST IS NOT SOUND:")
        for b in bad[:20]:
            print("   ", b)
        if len(bad) > 20:
            print("    ... and %d more" % (len(bad) - 20))
        return 1

    print("nest sound: %d pieces, %d sheet(s), no overlap, nothing off-sheet"
          % (sum(want.values()), len(sheets)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
