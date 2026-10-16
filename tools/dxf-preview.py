#!/usr/bin/env python3
"""Draw the quote DXFs into one reviewable page, one part per sheet.

    python tools/dxf-preview.py

Writes machine/drawings/dxf/preview.html; make-pdf.ps1 prints it.

IT PARSES THE WRITTEN BYTES, not make-dxf.py's own data. That is the whole
value: a mistake in the writer shows up here as a wrong picture instead of
agreeing with itself. What this page shows is what the shop receives.

To scale, with the scale stated, the outline dimensioned and every hole size
called out. Letter landscape - a 1211 part at 1:5 is 242 mm, which fits the
printable width with room for the dimension lines.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "machine" / "drawings" / "dxf"
OUT = SRC / "preview.html"

PAGE_W, PAGE_H = 272.0, 180.0        # mm of usable letter landscape
SCALES = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]


def parse(path: Path):
    toks = path.read_text(encoding="ascii").splitlines()
    lines, circles, texts, i = [], [], [], 0
    while i < len(toks) - 1:
        if toks[i].strip() == "0" and toks[i + 1].strip() in (
                "LINE", "CIRCLE", "TEXT"):
            kind = toks[i + 1].strip()
            d, j = {}, i + 2
            while j < len(toks) - 1 and toks[j].strip() != "0":
                d[toks[j].strip()] = toks[j + 1].strip()
                j += 2
            if kind == "LINE":
                lines.append(((float(d["10"]), float(d["20"])),
                              (float(d["11"]), float(d["21"]))))
            elif kind == "CIRCLE":
                circles.append((float(d["10"]), float(d["20"]),
                                float(d["40"]) * 2))
            else:
                texts.append((float(d["10"]), float(d["20"]),
                              float(d["40"]), d.get("1", "")))
            i = j
        else:
            i += 2
    return lines, circles, texts


def extent(lines, circles):
    xs = [p[0] for seg in lines for p in seg] + [c[0] for c in circles]
    ys = [p[1] for seg in lines for p in seg] + [c[1] for c in circles]
    return min(xs), max(xs), min(ys), max(ys)


def page(path: Path) -> str:
    lines, circles, texts = parse(path)
    x0, x1, y0, y1 = extent(lines, circles)
    w, h = x1 - x0, y1 - y0
    pad = 26.0                                   # mm for dimensions and labels
    scale = next((s for s in SCALES
                  if w / s + pad <= PAGE_W and h / s + pad <= PAGE_H), 10)

    title = next((t[3] for t in texts if " - QTY" in t[3]), path.stem)
    # the file's own HOLES line is dropped: the one below is counted from the
    # circles actually in the file and carries both units
    notes = [t[3] for t in texts
             if " - QTY" not in t[3] and not t[3].startswith("HOLES ")]

    def X(v):
        return (v - x0) / scale + pad * 0.62

    def Y(v):
        return (y1 - v) / scale + pad * 0.62

    g = []
    for a, b in lines:
        g.append(f'<line x1="{X(a[0]):.2f}" y1="{Y(a[1]):.2f}" '
                 f'x2="{X(b[0]):.2f}" y2="{Y(b[1]):.2f}" '
                 f'stroke="#111" stroke-width="0.5"/>')
    sizes = {}
    for cx, cy, d in circles:
        sizes[d] = sizes.get(d, 0) + 1
        r = max(d / 2 / scale, 0.45)
        g.append(f'<circle cx="{X(cx):.2f}" cy="{Y(cy):.2f}" r="{r:.2f}" '
                 f'fill="none" stroke="#c00" stroke-width="0.35"/>')
        g.append(f'<line x1="{X(cx) - r - 0.7:.2f}" y1="{Y(cy):.2f}" '
                 f'x2="{X(cx) + r + 0.7:.2f}" y2="{Y(cy):.2f}" '
                 f'stroke="#c00" stroke-width="0.12"/>')
        g.append(f'<line x1="{X(cx):.2f}" y1="{Y(cy) - r - 0.7:.2f}" '
                 f'x2="{X(cx):.2f}" y2="{Y(cy) + r + 0.7:.2f}" '
                 f'stroke="#c00" stroke-width="0.12"/>')

    # overall dimensions, outside the part
    bx, by = X(x1) + 5, Y(y0) + 5
    g.append(f'<line x1="{X(x0):.2f}" y1="{by:.2f}" x2="{X(x1):.2f}" '
             f'y2="{by:.2f}" stroke="#06c" stroke-width="0.3"/>')
    g.append(f'<text x="{(X(x0) + X(x1)) / 2:.2f}" y="{by + 3.4:.2f}" '
             f'text-anchor="middle" font-size="3" fill="#06c">{w:g} mm '
             f'({w / 25.4:.3f} in)</text>')
    # ROTATED, because set horizontally it ran off the page on the long parts:
    # the label is about 25 mm of text and the widest part leaves under 10.
    g.append(f'<line x1="{bx:.2f}" y1="{Y(y1):.2f}" x2="{bx:.2f}" '
             f'y2="{Y(y0):.2f}" stroke="#06c" stroke-width="0.3"/>')
    my = (Y(y0) + Y(y1)) / 2
    g.append(f'<text x="{bx + 3.2:.2f}" y="{my:.2f}" text-anchor="middle" '
             f'font-size="3" fill="#06c" '
             f'transform="rotate(-90 {bx + 3.2:.2f} {my:.2f})">'
             f'{h:g} mm ({h / 25.4:.3f} in)</text>')

    bom = " &middot; ".join(f"{n} &times; &oslash;{d:g} mm "
                            f"({d / 25.4:.3f} in)"
                            for d, n in sorted(sizes.items()))
    # a cut-out is drawn as lines, not a circle, so it is not in `sizes` - take
    # the count off the file's own HOLES line rather than re-deriving it
    cut = next((t[3] for t in texts if "cut-out" in t[3]), "")
    if cut:
        bom += " &middot; <b>" + cut.split("+", 1)[1].strip() + "</b>"
    svg_w, svg_h = PAGE_W, max(h / scale + pad * 1.4, 60)
    return (f'<section><h2>{title}</h2>'
            + "".join(f"<p class=n>{t}</p>" for t in notes)
            + f'<p class=n><b>Holes</b> {bom}</p>'
            + f'<p class=s>Drawn at 1:{scale:g} from the DXF itself &middot; '
              f'{path.name}</p>'
            + f'<svg viewBox="0 0 {svg_w:.1f} {svg_h:.1f}" '
              f'width="{svg_w:.0f}mm">{"".join(g)}</svg></section>')


def main() -> int:
    files = sorted(SRC.glob("*.dxf"))
    if not files:
        print("no DXFs; run tools/make-dxf.py first", file=sys.stderr)
        return 1
    body = "".join(page(f) for f in files)
    OUT.write_text(
        "<!DOCTYPE html><html lang=en><head><meta charset=utf-8>"
        "<title>CNCBuild &mdash; quote DXF preview</title><style>"
        "@page{size:letter landscape;margin:10mm}"
        "body{font:10pt 'Segoe UI',sans-serif;color:#111;margin:0}"
        "section{page-break-after:always;padding:0 0 4mm}"
        "section:last-child{page-break-after:auto}"
        "h2{font-size:13pt;margin:0 0 1mm}"
        "p.n{margin:0 0 1mm;font-size:9pt}"
        "p.s{margin:0 0 2mm;font-size:8pt;color:#555}"
        "svg{display:block}</style></head><body>" + body + "</body></html>",
        encoding="utf-8", newline="")
    print(f"{len(files)} part(s) -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
