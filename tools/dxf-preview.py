#!/usr/bin/env python3
"""Draw the quote DXFs into three quote requests, one part per sheet.

    python tools/dxf-preview.py

Writes one HTML per group in GROUPS below, into machine/drawings/dxf/;
make-pdf.ps1 prints them.

IT PARSES THE WRITTEN BYTES, not make-dxf.py's own data. That is the whole
value: a mistake in the writer shows up here as a wrong picture instead of
agreeing with itself. What these pages show is what the shop receives.

THREE REQUESTS, NOT ONE, AND EACH IS SELF-CONTAINED. They go to shops
separately, so neither the how-to-read notes nor the quoting instructions can
be shared between them - every file carries a full copy. Quoting one group does
not require the others to be in the envelope.

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

# THE SPLIT IS HIS, BY WHAT GETS QUOTED TOGETHER - not by material, which is
# why groups 2 and 3 are both 6061 and go out separately: the fins are being
# sent on their own to price one part. Every DXF in the folder must appear
# in exactly one group; main() fails if one is missing or named twice, so a
# ninth drawing cannot drop silently out of all three requests.
GROUPS = [
    {
        "out": "quote-1-steel.html",
        "title": "Waterjet quote - steel plates",
        "lead": "Three drawings, all <b>steel</b>: the rear plate, the two "
                "side plates, and the three nut sole plates. The rear and "
                "side plate material is <b>supplied</b>; the sole plates are "
                "cut from <b>1/4in HR A36 the shop supplies</b>.",
        "files": ["1-back-plate.dxf", "2-side-plates.dxf",
                  "3-sole-plates.dxf"],
    },
    # THE X BACK JOINING PLATE HAD ITS OWN REQUEST and does not any more - he
    # machined it at home, 2026-10-23, and its drawing left the folder with it.
    {
        "out": "quote-2-front-fins.html",
        "title": "Waterjet quote - Y front fins",
        "lead": "One drawing, <b>6061</b>: the <b>two Y front fins</b>, both "
                "out of one square of plate.",
        "files": ["4-front-fins.dxf"],
    },
    {
        "out": "quote-3-x-end-plates.html",
        "title": "Waterjet quote - X gantry end plates",
        "lead": "Two drawings in <b>6061</b>: the two <b>X gantry end "
                "plates</b>, each with its doubler nested in the strip "
                "beside it. <b>All material is supplied</b> and the outline "
                "drawn is the piece handed over, so the job is the holes and "
                "the profiles cut out of each piece.",
        "files": ["5-x-end-plate-left.dxf", "6-x-end-plate-right.dxf"],
    },
]

PAGE_W, PAGE_H = 272.0, 180.0        # mm of usable letter landscape
SCALES = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]


def parse(path: Path):
    toks = path.read_text(encoding="ascii").splitlines()
    lines, circles, arcs, texts, i = [], [], [], [], 0
    while i < len(toks) - 1:
        if toks[i].strip() == "0" and toks[i + 1].strip() in (
                "LINE", "CIRCLE", "ARC", "TEXT"):
            kind = toks[i + 1].strip()
            d, j = {}, i + 2
            while j < len(toks) - 1 and toks[j].strip() != "0":
                d[toks[j].strip()] = toks[j + 1].strip()
                j += 2
            if kind == "LINE":
                lines.append(((float(d["10"]), float(d["20"])),
                              (float(d["11"]), float(d["21"])),
                              d.get("8", "")))
            elif kind == "CIRCLE":
                circles.append((float(d["10"]), float(d["20"]),
                                float(d["40"]) * 2))
            elif kind == "ARC":
                arcs.append((float(d["10"]), float(d["20"]), float(d["40"]),
                             float(d["50"]), float(d["51"]), d.get("8", "")))
            else:
                texts.append((float(d["10"]), float(d["20"]),
                              float(d["40"]), d.get("1", ""),
                              d.get("8", "")))
            i = j
        else:
            i += 2
    return lines, circles, arcs, texts


def arc_ends(cx, cy, r, a0, a1):
    """The two endpoints and the sweep, R12's arc being always CCW a0 -> a1."""
    sweep = (a1 - a0) % 360.0 or 360.0
    p0 = (cx + r * math.cos(math.radians(a0)),
          cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)),
          cy + r * math.sin(math.radians(a1)))
    return p0, p1, sweep


def open_ends(lines, arcs):
    """Endpoints that do not meet exactly one other endpoint.

    AN OPEN PROFILE IS THE FAILURE THAT MATTERS AND IT IS INVISIBLE AT 1:5. A
    gap of a hundredth where an arc meets its line looks like a closed part on
    paper, and the shop's software either refuses the file or quietly cuts the
    hole as an open path. Every outline here is closed by construction, so each
    endpoint must be shared by exactly two entities - no more, no less.

    COUNTED BY LAYER. A profile closes within its own layer, and the stock
    outline on the end plates shares its lower-left corner with the plate cut
    out of it - counted together that corner meets three other ends and reads
    as a defect when both shapes are perfectly closed.
    """
    pts = [(p, seg[2]) for seg in lines for p in seg[:2]]
    pts += [(p, a[5]) for a in arcs for p in arc_ends(*a[:5])[:2]]
    seen = {}
    for (x, y), layer in pts:
        k = (layer, round(x, 6), round(y, 6))
        seen[k] = seen.get(k, 0) + 1
    return sorted((x, y) for (_, x, y), n in seen.items() if n != 2)


def extent(lines, circles, arcs):
    xs = [p[0] for seg in lines for p in seg[:2]] + [c[0] for c in circles]
    ys = [p[1] for seg in lines for p in seg[:2]] + [c[1] for c in circles]
    for cx, cy, r, a0, a1, _layer in arcs:
        for p in arc_ends(cx, cy, r, a0, a1)[:2]:
            xs.append(p[0])
            ys.append(p[1])
    return min(xs), max(xs), min(ys), max(ys)


def spread(pos: list, lo: float, hi: float, sep: float):
    """Label positions that do not collide, each as near its tick as it can be.

    THE TICK STAYS ON THE HOLE AND ONLY THE LABEL MOVES, which is what the
    leader line is for. Neighbouring hole centres come as close as 1.0 mm on
    paper - the two ø9 rows flanking the beam seam are 5 mm apart on a 1:5
    part - and a label is 2.4 mm wide, so a row of labels sitting on their own
    coordinates would overlap into mush exactly where the reader most needs to
    tell two holes apart.

    A single left-to-right push, then a clamp back from the far end if the
    block ran off the paper. Where there is room nothing moves at all, so the
    common case stays a straight tick with the number directly above it.

    Returns the positions and whether the row is too crowded to separate even
    using the whole band - the caller says so rather than printing a row that
    is quietly illegible.
    """
    if not pos:
        return [], False
    out = list(pos)
    for i in range(1, len(out)):
        out[i] = max(out[i], out[i - 1] + sep)
    if out[-1] > hi:
        out = [p - (out[-1] - hi) for p in out]
        for i in range(len(out) - 2, -1, -1):
            out[i] = min(out[i], out[i + 1] - sep)
    if out[0] < lo:
        n = len(out)
        if n > 1 and (hi - lo) / (n - 1) < sep:
            return out, True
        step = (hi - lo) / (n - 1) if n > 1 else 0.0
        out = [lo + step * i for i in range(n)]
    return out, False


def cutouts(lines, arcs):
    """Bounding box of each shape on the HOLES layer that is not a circle.

    A SLOT HAS NO CENTRE TO PUT IN AN ORDINATE ROW, so the rows below are
    built from circles only - and the back plate's two cut-outs would then be
    the one feature on the one page with no position on it at all. They get
    their extents instead, which is what a cut needs anyway.

    Shapes are separated by walking connected endpoints; the profiles are
    closed, which open_ends has already proved by the time this runs.
    """
    segs = [(seg[0], seg[1]) for seg in lines if seg[2] == "HOLES"]
    segs += [(arc_ends(*a[:5])[0], arc_ends(*a[:5])[1])
             for a in arcs if a[5] == "HOLES"]
    boxes = []
    while segs:
        pts = list(segs.pop(0))
        moved = True
        while moved:
            moved = False
            for s in list(segs):
                for p in s:
                    if any(abs(p[0] - q[0]) < 1e-6 and abs(p[1] - q[1]) < 1e-6
                           for q in pts):
                        pts += list(s)
                        segs.remove(s)
                        moved = True
                        break
                else:
                    continue
                break
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        boxes.append((min(xs), max(xs), min(ys), max(ys)))
    return sorted(boxes)


def page(path: Path, bad: list, toc: list) -> str:
    lines, circles, arcs, texts = parse(path)
    x0, x1, y0, y1 = extent(lines, circles, arcs)
    for p in open_ends(lines, arcs):
        bad.append(f"{path.name}: {p} does not close")
    w, h = x1 - x0, y1 - y0
    pad = 26.0                                   # mm for dimensions and labels

    title = next((t[3] for t in texts if "QTY " in t[3]), path.stem)
    # THE LAYER SAYS WHICH TEXT IS PART OF THE PICTURE. A label on PARTS belongs
    # on the drawing - the sole plates name each profile and give its length, and
    # a page of three identical-looking Ts is not reviewable without them. A line
    # on NOTES is the title block and reads better as prose above the figure. The
    # first cut of this told them apart by where they sat, which cannot work: the
    # title block's bottom line and a part label both land a few mm over the top
    # of the extent, so one band either swallowed the labels or drew the notes
    # across the part's top edge.
    notes = [t[3] for t in texts
             if "QTY " not in t[3] and not t[3].startswith("HOLES ")
             and t[4] != "PARTS"]

    # THE TITLE BLOCK IS PART OF THE PAGE AND MUST BE COUNTED, which the first
    # cut of this did not do - it sized the drawing against the full 180 mm,
    # so every part spilled onto a second sheet with its heading left behind on
    # the first. A drawing whose title is on another page is not a drawing.
    # Heading, one line per note, the holes line, a cut-outs line where there
    # is one, the caption, and the gap down to the figure.
    nlines = len(notes) + 1 + (1 if any("cut-out" in t[3] for t in texts)
                               else 0)
    header = 9.0 + 4.3 * nlines + 6.5
    # 16.1 above for the X offsets, about 10 below for the width dimension.
    VPAD = 27.0

    def below(s):
        """Paper mm of PART LABEL hanging under the part, at scale s.

        The end plates name themselves below their own bottom edge, where the
        overall width dimension also goes - and the two were printed on top of
        each other. The dimension moves down past the label, so the page has
        to budget for it before the scale is picked.
        """
        return max([0.0] + [(y0 - t[1] + t[2]) / s for t in texts
                            if t[4] == "PARTS" and t[1] < y0])

    scale = next((s for s in SCALES
                  if w / s + pad <= PAGE_W
                  and header + h / s + VPAD + below(s) <= PAGE_H), 10)

    def X(v):
        return (v - x0) / scale + pad * 0.62

    def Y(v):
        return (y1 - v) / scale + pad * 0.62

    g = []
    # THE STOCK OUTLINE IS NOT A CUT LINE, so it must not look like one: it is
    # the piece he hands over, drawn to show the waste the extra parts come out
    # of. Dashed and grey, where every cut path is solid black.
    for a, b, layer in lines:
        dash = ' stroke-dasharray="2.2 1.6"' if layer == 'STOCK' else ''
        col = '#999' if layer == 'STOCK' else '#111'
        g.append(f'<line x1="{X(a[0]):.2f}" y1="{Y(a[1]):.2f}" '
                 f'x2="{X(b[0]):.2f}" y2="{Y(b[1]):.2f}" '
                 f'stroke="{col}" stroke-width="0.5"{dash}/>')
    # SVG's arc sweep flag is in SCREEN space, and Y is flipped here, so a
    # counterclockwise DXF arc is a clockwise SVG one: sweep-flag 0, not 1.
    for cx, cy, r, a0, a1, _layer in arcs:
        p0, p1, sweep = arc_ends(cx, cy, r, a0, a1)
        g.append(f'<path d="M {X(p0[0]):.2f} {Y(p0[1]):.2f} '
                 f'A {r / scale:.3f} {r / scale:.3f} 0 '
                 f'{1 if sweep > 180 else 0} 0 '
                 f'{X(p1[0]):.2f} {Y(p1[1]):.2f}" '
                 f'fill="none" stroke="#111" stroke-width="0.5"/>')
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

    for tx, ty_, th, s, layer in texts:
        if layer != "PARTS":
            continue
        g.append(f'<text x="{X(tx):.2f}" y="{Y(ty_):.2f}" '
                 f'font-size="{max(th / scale, 2.4):.2f}" fill="#444">'
                 f'{s}</text>')

    # overall dimensions, outside the part - and below any label hanging under
    # it, which is what below() reserved the room for
    bx = X(x1) + 5
    by = max([Y(y0) + 5] + [Y(t[1]) + 1.6 for t in texts
                            if t[4] == "PARTS" and t[1] < y0])
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

    # --- where the holes are: the origin, then X across the top, Y down the
    # left. THE NUMBERS ARE THE PARSED CIRCLE CENTRES, so a row cannot
    # disagree with the holes drawn beside it - the same reason this whole
    # page is redrawn from the written bytes instead of from make-dxf's data.
    if round(x0, 6) or round(y0, 6):
        bad.append(f"{path.name}: geometry starts at ({x0:g}, {y0:g}), not "
                   f"the origin - the origin dot would be in the wrong place")
    g.append(f'<circle cx="{X(0.0):.2f}" cy="{Y(0.0):.2f}" r="1.1" '
             f'fill="#c00"/>')
    g.append(f'<text x="{X(0.0) - 1.6:.2f}" y="{Y(0.0) + 4.2:.2f}" '
             f'text-anchor="end" font-size="2.6" fill="#c00">0,0</text>')

    OFS, LBL = 2.1, 2.6          # font size, and the room one label needs
    crowded = False

    xs = sorted({round(c[0], 2) for c in circles})
    lx, over = spread([X(v) for v in xs], 2.0, PAGE_W - 2.0, LBL)
    crowded = crowded or over
    # START THE ROW ABOVE ANY PART LABEL, not at the part's top edge. The sole
    # plates name each of the three profiles just over that edge, and ticks
    # taken from the edge upward ruled straight through the words.
    top = min([Y(y1)] + [Y(t[1]) - t[2] / scale - 0.8 for t in texts
                         if t[4] == "PARTS" and t[1] + t[2] > y1])
    for v, p in zip(xs, lx):
        g.append(f'<line x1="{X(v):.2f}" y1="{top:.2f}" x2="{X(v):.2f}" '
                 f'y2="{top - 2.6:.2f}" stroke="#06c" stroke-width="0.25"/>')
        g.append(f'<line x1="{X(v):.2f}" y1="{top - 2.6:.2f}" x2="{p:.2f}" '
                 f'y2="{top - 4.6:.2f}" stroke="#06c" stroke-width="0.18"/>')
        g.append(f'<text x="{p:.2f}" y="{top - 5.4:.2f}" font-size="{OFS}" '
                 f'fill="#06c" transform="rotate(-90 {p:.2f} '
                 f'{top - 5.4:.2f})">{v:g}</text>')

    ys = sorted({round(c[1], 2) for c in circles})
    ly, over = spread([Y(v) for v in reversed(ys)], 2.0, PAGE_H - 2.0, LBL)
    crowded = crowded or over
    left = X(x0)
    for v, p in zip(reversed(ys), ly):
        g.append(f'<line x1="{left:.2f}" y1="{Y(v):.2f}" '
                 f'x2="{left - 2.6:.2f}" y2="{Y(v):.2f}" stroke="#06c" '
                 f'stroke-width="0.25"/>')
        g.append(f'<line x1="{left - 2.6:.2f}" y1="{Y(v):.2f}" '
                 f'x2="{left - 4.6:.2f}" y2="{p:.2f}" stroke="#06c" '
                 f'stroke-width="0.18"/>')
        g.append(f'<text x="{left - 5.4:.2f}" y="{p + 0.75:.2f}" '
                 f'text-anchor="end" font-size="{OFS}" fill="#06c">'
                 f'{v:g}</text>')

    if crowded:
        bad.append(f"{path.name}: the offset rows cannot be separated - "
                   f"{len(xs)} X and {len(ys)} Y values do not fit the page")

    bom = " &middot; ".join(f"{n} &times; &oslash;{d:g} mm "
                            f"({d / 25.4:.3f} in)"
                            for d, n in sorted(sizes.items()))
    # a cut-out is drawn as lines, not a circle, so it is not in `sizes` - take
    # the count off the file's own HOLES line rather than re-deriving it
    cut = next((t[3] for t in texts if "cut-out" in t[3]), "")
    if cut:
        bom += " &middot; <b>" + cut.split("+", 1)[1].strip() + "</b>"
    svg_w, svg_h = PAGE_W, max(h / scale + VPAD + below(scale), 60)
    toc.append({
        "file": path.name,
        "title": title,
        "stock": next((t for t in notes if t.startswith(("STOCK ", "MATERIAL "))),
                      ""),
        "bom": bom,
        "size": f"{w:g} &times; {h:g}",
    })
    # The cut-outs are lines and arcs, so they are in neither ordinate row -
    # give their extents, which is what a cut needs in any case.
    boxes = cutouts(lines, arcs)
    cutline = ""
    if boxes:
        cutline = ('<p class=n><b>Cut-outs</b> ' + " &middot; ".join(
            f"X {a:g} to {b:g}, Y {c:g} to {d:g}" for a, b, c, d in boxes)
            + '</p>')

    return (f'<section><h2>{title}</h2>'
            + "".join(f"<p class=n>{t}</p>" for t in notes)
            + f'<p class=n><b>Holes</b> {bom}</p>'
            + cutline
            + f'<p class=s>Drawn at 1:{scale:g} from the DXF itself &middot; '
              f'{path.name} &middot; offsets are HOLE CENTRES from the red '
              f'0,0 dot - X across the top, Y down the left side</p>'
            + f'<svg viewBox="0 0 {svg_w:.1f} {svg_h:.1f}" '
              f'width="{svg_w:.0f}mm">{"".join(g)}</svg></section>')


def intro(toc: list, group: dict) -> str:
    """The front page: what the request is, what is in it, how to read it.

    EVERY FIGURE HERE COMES OFF THE PARSED FILES, not from a list written
    beside them - the contents table cannot disagree with the drawings it
    indexes, because it is built from the same bytes on the same pass. Only the
    title and the lead sentence come from GROUPS.
    """
    rows = "".join(
        f'<tr><td class=f>{t["file"]}</td><td>{t["title"]}</td>'
        f'<td class=t>{t["stock"]}</td><td class=t>{t["size"]} mm</td>'
        f'<td class=t>{t["bom"]}</td></tr>' for t in toc)
    return f'''<section><h1>{group["title"]}</h1>
<p class=lead>{group["lead"]} <b>Every drawing is a separate DXF</b> and the
file name is printed on its page.</p>

<h2>What is in it</h2>
<table class=toc>
<tr><th>File</th><th>Part</th><th>Material</th><th>Overall</th><th>Holes</th></tr>
{rows}
</table>

<h2>How to read the drawings</h2>
<ul>
<li><b>Units are millimetres</b> and the origin is the lower-left corner of
every drawing, marked with a <b>red dot</b>. Inch equivalents are printed
alongside for reference only &mdash; work to the millimetre figures.</li>
<li><b>Hole offsets from that origin are printed on each page</b> &mdash; the
<b>X</b> values across the top, the <b>Y</b> values down the left side, each on
a leader from its own tick. They are there to read the drawing by; the
<b>DXF is the authority</b> and the offsets are taken from it.</li>
<li><b>R12 DXF, lines, circles and arcs only.</b> No polylines, no splines, no
blocks. Outlines are closed.</li>
<li><b>Layers:</b> OUTLINE is the cut profile, HOLES are the holes, NOTES and
PARTS are text and are not to be cut.</li>
<li><b>Where a drawing says STOCK, the material is supplied</b> and the outline
drawn IS that piece &mdash; the job is the holes, and any excess falls outside
them. Where it says MATERIAL, the shop supplies the plate and the outline is
the part to cut.</li>
<li><b>Holes called out as edge-bored are not drawn.</b> They run into a part's
end face rather than through it, and are drilled here.</li>
<li><b>Where two parts share one piece</b>, both are drawn in position on it
with the kerf allowed between them.</li>
</ul>

<h2>What would help on the quote</h2>
<ul>
<li>Price <b>per drawing</b>, and separately the material where you are
supplying it.</li>
<li>Say if any hole is <b>below your minimum for the thickness</b> &mdash; a
pilot that gets opened out here is fine, and so is a scribed mark, so tell us
which you would rather cut.</li>
<li>Note any outline you would rather nest differently. Nesting is yours to
choose; the drawings do not assume one.</li>
</ul>
</section>'''


def shell(title: str, body: str) -> str:
    return (
        "<!DOCTYPE html><html lang=en><head><meta charset=utf-8>"
        f"<title>CNCBuild &mdash; {title}</title><style>"
        "@page{size:letter landscape;margin:10mm}"
        "body{font:10pt 'Segoe UI',sans-serif;color:#111;margin:0}"
        "section{page-break-after:always;padding:0 0 4mm}"
        "section:last-child{page-break-after:auto}"
        "h1{font-size:19pt;margin:0 0 2mm}"
        "h2{font-size:13pt;margin:0 0 1mm}"
        "section h2{margin-top:5mm}section:first-child h2:first-of-type"
        "{margin-top:3mm}"
        "p.lead{margin:0 0 3mm;font-size:10pt}"
        "table.toc{border-collapse:collapse;width:100%;font-size:8.5pt;"
        "margin:0 0 2mm}"
        "table.toc th{text-align:left;border-bottom:1px solid #111;"
        "padding:1mm 2mm 1mm 0}"
        "table.toc td{border-bottom:1px solid #ddd;padding:1mm 2mm 1mm 0;"
        "vertical-align:top}"
        "td.f{font-family:ui-monospace,Consolas,monospace;white-space:nowrap}"
        "td.t{font-size:8pt;color:#333}"
        "ul{margin:0 0 3mm;padding-left:5mm;font-size:9.5pt}"
        "li{margin:0 0 1.2mm}"
        "p.n{margin:0 0 1mm;font-size:9pt}"
        "p.s{margin:0 0 2mm;font-size:8pt;color:#555}"
        "svg{display:block}</style></head><body>" + body + "</body></html>")


def main() -> int:
    files = sorted(SRC.glob("*.dxf"))
    if not files:
        print("no DXFs; run tools/make-dxf.py first", file=sys.stderr)
        return 1

    # EVERY DRAWING IN EXACTLY ONE REQUEST. A new DXF that nobody added to a
    # group would otherwise be quoted by nobody, and the only symptom would be
    # a part that never arrives.
    grouped = [f for g in GROUPS for f in g["files"]]
    have = {f.name for f in files}
    missing = sorted(have - set(grouped))
    unknown = sorted(set(grouped) - have)
    twice = sorted({f for f in grouped if grouped.count(f) > 1})
    if missing or unknown or twice:
        print("GROUPS does not match the folder:", file=sys.stderr)
        for f in missing:
            print(f"    {f} is in no group - add it to GROUPS", file=sys.stderr)
        for f in unknown:
            print(f"    {f} is grouped but not written", file=sys.stderr)
        for f in twice:
            print(f"    {f} is in more than one group", file=sys.stderr)
        return 1

    for g in GROUPS:
        bad: list[str] = []
        toc: list = []
        body = "".join(page(SRC / f, bad, toc) for f in g["files"])
        if bad:
            print("OPEN PROFILE - these cannot go to the shop:",
                  file=sys.stderr)
            for b in bad:
                print("    " + b, file=sys.stderr)
            return 1
        out = SRC / g["out"]
        out.write_text(shell(g["title"], intro(toc, g) + body),
                       encoding="utf-8", newline="")
        print(f"{len(g['files'])} part(s), every profile closing -> "
              f"{out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
