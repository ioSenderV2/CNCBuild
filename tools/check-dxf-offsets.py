#!/usr/bin/env python3
"""Do the offsets PRINTED on each quote page match the holes in the DXF?

    python tools/check-dxf-offsets.py

Run after tools/dxf-preview.py; make-pdf.ps1 -Doc dxf runs it for you.

A WRONG NUMBER ON A SHOP DRAWING IS THE WORST THING THIS FOLDER CAN PRODUCE.
The picture is already drawn back from the written bytes so it cannot flatter
the writer, and this closes the same loop on the ordinate rows: it reads the
generated HTML back, pulls out the blue offset labels, and compares that set
against the circle centres parsed straight out of each DXF. Nothing here
shares a code path with the drawing, so a rounding or formatting slip between
a tick and its label has nowhere to hide.

What it does NOT check is whether the holes themselves are right - that is
make-dxf.py's tally against the shop pack, one step upstream.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "machine" / "drawings" / "dxf"

# dxf-preview has a hyphen in its name, so it cannot be imported by name
_spec = importlib.util.spec_from_file_location(
    "dxf_preview", ROOT / "tools" / "dxf-preview.py")
_dxfp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_dxfp)

# the X row is rotated upright; the Y column is plain and right-aligned
X_RE = re.compile(r'font-size="2\.1" fill="#06c" transform="rotate\(-90 '
                  r'[\d.]+ [\d.]+\)">([\d.]+)</text>')
Y_RE = re.compile(r'text-anchor="end" font-size="2\.1" fill="#06c">'
                  r'([\d.]+)</text>')


def main() -> int:
    bad = 0
    for g in _dxfp.GROUPS:
        page = SRC / g["out"]
        if not page.exists():
            print(f"{page.name} not written - run tools/dxf-preview.py first",
                  file=sys.stderr)
            return 1
        html = page.read_text(encoding="utf-8")
        # one <section> per drawing, after the intro
        sections = re.findall(r"<section>.*?</section>", html, re.S)[1:]
        if len(sections) != len(g["files"]):
            print(f"{page.name}: {len(sections)} drawing section(s) for "
                  f"{len(g['files'])} file(s)", file=sys.stderr)
            return 1
        for name, sec in zip(g["files"], sections):
            _lines, circles, _arcs, _texts = _dxfp.parse(SRC / name)
            want_x = {f"{v:g}" for v in {round(c[0], 2) for c in circles}}
            want_y = {f"{v:g}" for v in {round(c[1], 2) for c in circles}}
            got_x, got_y = set(X_RE.findall(sec)), set(Y_RE.findall(sec))
            for axis, got, want in (("X", got_x, want_x),
                                    ("Y", got_y, want_y)):
                if got != want:
                    bad += 1
                    print(f"{name}: the {axis} offsets printed do not match "
                          f"the holes", file=sys.stderr)
                    print(f"    only on the page: "
                          f"{sorted(got - want)}", file=sys.stderr)
                    print(f"    only in the DXF:  "
                          f"{sorted(want - got)}", file=sys.stderr)
    if bad:
        return 1
    print("every printed offset is a hole centre from its own DXF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
