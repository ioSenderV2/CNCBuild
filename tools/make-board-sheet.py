#!/usr/bin/env python3
"""One-page mounting drawing: the interface board beside the RP23.

    make-board-sheet.py            write machine/drawings/board-mounting.html
    make-board-sheet.py --check    build and report, write nothing

WHAT IT IS FOR
--------------
Drilling the plate the two boards bolt to, and knowing which lead goes in which
jack. It shows both outlines to scale, every mounting hole with its coordinate,
and a rectangle per connector labelled with conductor count and purpose.

WHY IT IS GENERATED AND NOT DRAWN
---------------------------------
Every number about the interface board comes out of
`wiring/kicad/interface-board/interface-board.kicad_pcb`. Hand-drawing it would
make a second source of truth that goes stale the first time a connector moves -
which is the failure STATUS.md and INDEX.md are generated to avoid. Re-run this
after any board change.

The RP23's figures are HIS, 2026-11-08 - 38 mm square, M3 on a 34 mm square at
the corners - because that board is not in this repo. They are stated once, at
RP23 below, and nothing derives them.

TWO THINGS THIS GOT WRONG FIRST, kept so they are not repeated:

  A FOOTPRINT'S `at` IS NOT ITS BODY CENTRE, and body sizes are not guessable.
  The first version placed rectangles from the anchor and assumed each part's
  size; five connectors came out hanging off the board. The rectangles are now
  the parts' real F.CrtYd courtyards, rotated by the footprint angle and offset
  by its position.

  MOUNTING HOLES HAVE NO COURTYARD, so filtering footprints by courtyard drops
  them silently - and they are the whole point of the sheet. They are read
  separately, and the script refuses to write unless it finds exactly four.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PCB = ROOT / "wiring" / "kicad" / "interface-board" / "interface-board.kicad_pcb"
OUT = ROOT / "machine" / "drawings" / "board-mounting.html"

# His, 2026-11-08. Not in this repo, so stated rather than read.
RP, RPSQ = 38.0, 34.0
GAP = 30.0

EDGE_PATS = (
    r'\(gr_line\s*\(start ([-\d.]+) ([-\d.]+)\)\s*\(end ([-\d.]+) ([-\d.]+)\)(.*?)\)\s*\(uuid',
    r'\(gr_rect\s*\(start ([-\d.]+) ([-\d.]+)\)\s*\(end ([-\d.]+) ([-\d.]+)\)(.*?)\)\s*\(uuid',
)

WHAT = {
    "J1": ("X stepper", "8", "step/dir/en/alarm, Cat 6"),
    "J2": ("Y1 stepper", "8", "step/dir/en/alarm, Cat 6"),
    "J3": ("Y2 stepper", "8", "step/dir/en/alarm, Cat 6"),
    "J4": ("Z stepper", "8", "step/dir/en/alarm, Cat 6"),
    "J5": ("B stepper", "8", "step/dir/en/alarm, Cat 6"),
    "J6": ("X limit", "3", "12 V / signal / GND"),
    "J7": ("Y1 limit", "3", "12 V / signal / GND"),
    "J8": ("Y2 limit", "3", "12 V / signal / GND"),
    "J9": ("Z limit", "3", "12 V / signal / GND"),
    "J10": ("B limit", "3", "12 V / signal / GND"),
    "J11": ("Probe", "3", "12 V / PROBE / GND"),
    "J12": ("Door / toolsetter", "3", "12 V / DOOR / GND"),
    "J13": ("Probe 2", "2", "PROBE / GND"),
    "J14": ("Probe 3", "2", "PROBE / GND"),
    "J15": ("Spindle", "4", "enable / GND / GND / 0-10 V"),
    "J16": ("to RP23 J20", "2x10", "step, dir, enable - five axes"),
    "J17": ("to RP23 J24", "2x3", "alarms - five axes"),
    "J18": ("12 V in", "2", "+12 V / GND"),
    "J19": ("12 V out", "2", "+12 V / GND"),
    "J21": ("Limits out", "5", "LIM X Y1 Y2 Z B"),
    "J22": ("Spindle out", "4", "enable / GND / 0-10 V"),
    "J23": ("Probe + door", "2", "PROBE / DOOR"),
    "J30": ("Mist", "2", "dry contact"),
    "J31": ("Flood", "2", "dry contact"),
    "J32": ("Control", "4", "cycle start / hold / estop / spare"),
    "J33": ("UART1", "4", "TX / RX / 3V3 / GND"),
    "J34": ("Mist out", "2", "dry contact"),
    "J35": ("Flood out", "2", "dry contact"),
    "J36": ("Control out", "4", "cycle start / hold / estop / spare"),
    "J37": ("UART1 out", "4", "TX / RX / 3V3 / GND"),
    "J40": ("X Teensy jumper", "4", "GND / step / dir / enable"),
    "J41": ("Y1 Teensy jumper", "4", "GND / step / dir / enable"),
    "J42": ("Y2 Teensy jumper", "4", "GND / step / dir / enable"),
    "J43": ("Z Teensy jumper", "4", "GND / step / dir / enable"),
    "J44": ("B Teensy jumper", "4", "GND / step / dir / enable"),
    "J50": ("X stepper power", "2", "+36 V / return, 18/2"),
    "J51": ("Y1 stepper power", "2", "+36 V / return, 18/2"),
    "J52": ("Y2 stepper power", "2", "+36 V / return, 18/2"),
    "J53": ("Z stepper power", "2", "+36 V / return, 18/2"),
    "J54": ("B stepper power", "2", "+36 V / return, 18/2"),
    "J55": ("36 V in", "2", "+36 V / return, from the supply"),
}


def jnum(ref: str) -> int:
    return int(re.sub(r"\D", "", ref) or 0)


def read_board(src: str):
    """Board origin and size, from Edge.Cuts."""
    xs, ys = [], []
    for pat in EDGE_PATS:
        for m in re.finditer(pat, src, re.S):
            if "Edge.Cuts" in m.group(5):
                xs += [float(m.group(1)), float(m.group(3))]
                ys += [float(m.group(2)), float(m.group(4))]
    if not xs:
        sys.exit("no Edge.Cuts geometry found - nothing written")
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)


def read_parts(src: str, ox: float, oy: float):
    """Placed courtyards for connectors, and mounting hole centres."""
    fp, mh = {}, {}
    for m in re.finditer(r'\(footprint "([^"]+)"(.*?)\n\t\)\n', src, re.S):
        body = m.group(2)
        at = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', body)
        ref = re.search(r'\(property "Reference" "([^"]+)"', body)
        if not (at and ref):
            continue
        name = ref.group(1)
        cx, cy = float(at.group(1)) - ox, float(at.group(2)) - oy

        if name.startswith("MH"):
            mh[name] = (cx, cy)
            continue

        pts = []
        for pat in (r'\(fp_line\s*\(start ([-\d.]+) ([-\d.]+)\)\s*\(end ([-\d.]+) ([-\d.]+)\)(.*?)\)\s*\(uuid',
                    r'\(fp_rect\s*\(start ([-\d.]+) ([-\d.]+)\)\s*\(end ([-\d.]+) ([-\d.]+)\)(.*?)\)\s*\(uuid'):
            for g in re.finditer(pat, body, re.S):
                if "F.CrtYd" in g.group(5):
                    pts += [(float(g.group(1)), float(g.group(2))),
                            (float(g.group(3)), float(g.group(4)))]
        if not pts:
            continue
        rot = math.radians(float(at.group(3) or 0))
        c, s = math.cos(-rot), math.sin(-rot)
        gx = [cx + (px * c - py * s) for px, py in pts]
        gy = [cy + (px * s + py * c) for px, py in pts]
        fp[name] = {"x": min(gx), "y": min(gy),
                    "w": max(gx) - min(gx), "h": max(gy) - min(gy),
                    "cx": cx, "cy": cy}
    return fp, mh


def hole(x: float, y: float, label: bool = True) -> str:
    s = (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.6" class="mh"/>'
         f'<line x1="{x-3.6:.2f}" y1="{y:.2f}" x2="{x+3.6:.2f}" y2="{y:.2f}" class="cl"/>'
         f'<line x1="{x:.2f}" y1="{y-3.6:.2f}" x2="{x:.2f}" y2="{y+3.6:.2f}" class="cl"/>')
    if label:
        s += f'<text x="{x:.2f}" y="{y-4.8:.2f}" class="hl">{x:.1f}, {y:.1f}</text>'
    return s


def build() -> tuple[str, dict, dict, float, float]:
    src = PCB.read_text(encoding="utf-8")
    ox, oy, bw, bh = read_board(src)
    fp, mh = read_parts(src, ox, oy)

    if len(mh) != 4:
        sys.exit(f"expected 4 mounting holes, found {len(mh)} - nothing written")
    missing = sorted(set(WHAT) - set(fp), key=jnum)
    if missing:
        sys.exit(f"on the sheet but not on the board: {missing} - nothing written")

    off = [r for r in WHAT
           if fp[r]["x"] < -0.05 or fp[r]["y"] < -0.05
           or fp[r]["x"] + fp[r]["w"] > bw + 0.05
           or fp[r]["y"] + fp[r]["h"] > bh + 0.05]
    if off:
        sys.exit(f"courtyards off the board outline: {off} - nothing written")

    parts, rows = [], []
    for ref in sorted(WHAT, key=jnum):
        v = fp[ref]
        parts.append(
            f'<rect x="{v["x"]:.2f}" y="{v["y"]:.2f}" width="{v["w"]:.2f}" '
            f'height="{v["h"]:.2f}" class="jk"/>'
            f'<text x="{v["cx"]:.2f}" y="{v["y"] + v["h"]/2 + 1.1:.2f}" class="jr">{ref}</text>')
        what, n, carries = WHAT[ref]
        rows.append(f"<tr><td><b>{ref}</b></td><td>{what}</td><td class='n'>{n}</td>"
                    f"<td>{carries}</td><td class='n'>{v['cx']:.1f}, {v['cy']:.1f}</td></tr>")

    inset = (RP - RPSQ) / 2
    rpx = bw + GAP
    total = rpx + RP
    holes = "".join(hole(x, y) for _r, (x, y) in sorted(mh.items()))
    rp_holes = "".join(hole(rpx + inset + dx*RPSQ, inset + dy*RPSQ, False)
                       for dx in (0, 1) for dy in (0, 1))
    mh_list = ", ".join(f"<b>{r}</b> {x:.1f}, {y:.1f}" for r, (x, y) in sorted(mh.items()))
    near = min(min(x, y, bw - x, bh - y) for x, y in mh.values())

    html = f"""<!doctype html>
<meta charset="utf-8">
<title>CNCBuild - interface board and RP23 mounting</title>
<style>
  @page {{ size: letter landscape; margin: 7mm; }}
  body {{ font: 9pt/1.25 "Segoe UI", system-ui, sans-serif; color:#111; margin:0 auto; max-width:277mm; }}
  h1 {{ font-size:13pt; margin:0 0 0.5mm; }}
  .sub {{ color:#555; margin:0 0 2mm; font-size:8.2pt; }}
  table {{ border-collapse:collapse; width:100%; font-size:6.2pt; }}
  th,td {{ border:1px solid #aaa; padding:0.25mm 0.9mm; text-align:left; }}
  th {{ background:#eee; }} td.n {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
  .cols {{ column-count:4; column-gap:3mm; margin-top:1.2mm; }}
  .note {{ border-left:3px solid #c00; background:#fdf0f0; padding:1.4mm 2mm; margin:1.4mm 0; font-size:7.8pt; }}
  svg {{ width:100%; height:auto; }}
  .bd {{ fill:#eef3fa; stroke:#111; stroke-width:0.7; }}
  .jk {{ fill:#fff; stroke:#b06000; stroke-width:0.35; }}
  .jr {{ font:2.7px "Segoe UI",sans-serif; fill:#b06000; text-anchor:middle; }}
  .mh {{ fill:#fff; stroke:#c00; stroke-width:0.7; }}
  .cl {{ stroke:#c00; stroke-width:0.3; }}
  .hl {{ font:2.5px "Segoe UI",sans-serif; fill:#c00; text-anchor:middle; }}
  .dim {{ stroke:#06c; stroke-width:0.3; }}
  .dt {{ font:3.2px "Segoe UI",sans-serif; fill:#06c; text-anchor:middle; }}
  .ttl {{ font:4.2px "Segoe UI",sans-serif; fill:#111; font-weight:bold; }}
</style>

<h1>Interface board and RP23 &mdash; mounting</h1>
<p class="sub"><b>Outline, mounting holes and every connector read from interface-board.kicad_pcb;
the connector rectangles are the parts' real courtyards.</b> RP23 figures his, 2026-11-08.
Drawn to scale. <b>All coordinates are millimetres from each board's own top-left corner.</b>
Regenerate with tools/make-board-sheet.py after any board change.</p>

<svg viewBox="-13 -15 {total + 26:.0f} {bh + 32:.0f}" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="{bw:.2f}" height="{bh:.2f}" class="bd"/>
  <text x="1" y="-3.5" class="ttl">INTERFACE BOARD &#8212; {bw:.0f} &#215; {bh:.0f}</text>
  {''.join(parts)}
  {holes}
  <line x1="0" y1="{bh+6:.2f}" x2="{bw:.2f}" y2="{bh+6:.2f}" class="dim"/>
  <text x="{bw/2:.2f}" y="{bh+10:.2f}" class="dt">{bw:.0f}</text>
  <line x1="-6" y1="0" x2="-6" y2="{bh:.2f}" class="dim"/>
  <text x="-9.5" y="{bh/2:.2f}" class="dt" transform="rotate(-90 -9.5 {bh/2:.2f})">{bh:.0f}</text>

  <rect x="{rpx:.2f}" y="0" width="{RP}" height="{RP}" class="bd"/>
  <text x="{rpx+1:.2f}" y="-3.5" class="ttl">RP23 &#8212; {RP:.0f} &#215; {RP:.0f}</text>
  {rp_holes}
  <line x1="{rpx:.2f}" y1="{RP+6:.2f}" x2="{rpx+RP:.2f}" y2="{RP+6:.2f}" class="dim"/>
  <text x="{rpx+RP/2:.2f}" y="{RP+10:.2f}" class="dt">{RP:.0f}</text>
  <line x1="{rpx+inset:.2f}" y1="{RP+14:.2f}" x2="{rpx+inset+RPSQ:.2f}" y2="{RP+14:.2f}" class="dim"/>
  <text x="{rpx+RP/2:.2f}" y="{RP+18:.2f}" class="dt">{RPSQ:.0f} square, M3</text>
  <text x="{rpx+RP/2:.2f}" y="{RP+23:.2f}" class="dt">{inset:.0f} in from each edge</text>
</svg>

<div class="note">
<b>The interface board's four &oslash;3.2 holes are NOT a rectangle &mdash; drill from these four
numbers, never by symmetry:</b> {mh_list}.
<b>The RP23's four M3 ARE a true {RPSQ:.0f} square</b>, {inset:.0f} mm in from each edge of its {RP:.0f}.
<br><br>
<b>Every interface board hole is about 4 mm from an edge and the closest is {near:.1f}.</b> A standoff
whose flange is wider than roughly {2*near:.0f} mm will overhang there. <b>Check the standoff against
this before drilling the plate</b>, not after.
</div>

<div class="cols">
<table>
<tr><th>Ref</th><th>What</th><th>Cond</th><th>Carries</th><th>x, y</th></tr>
{chr(10).join(rows)}
</table>
</div>
"""
    return html, fp, mh, bw, bh


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="build and report, write nothing")
    args = ap.parse_args()

    html, fp, mh, bw, bh = build()
    print(f"interface board {bw:.0f} x {bh:.0f}, "
          f"{len(WHAT)} connectors, {len(mh)} mounting holes")
    for r, (x, y) in sorted(mh.items()):
        print(f"  {r}  {x:6.1f}, {y:5.1f}   nearest edge "
              f"{min(x, y, bw - x, bh - y):4.1f}")
    if args.check:
        print("  --check: nothing written")
        return 0
    OUT.write_text(html, encoding="utf-8")
    print(f"  wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
