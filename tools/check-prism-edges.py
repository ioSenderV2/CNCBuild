#!/usr/bin/env python3
"""Does the model draw any edge that is not on a part?

WHY THIS EXISTS. On 2026-10-11 he hid the top skin, looked into the torsion box
and saw a line running clean across the inside, from the back of one front tenon
to the back of the other. Hovering it changed nothing, because it was not a part
at all: three.js's EdgesGeometry, given an extruded shape with holes, draws the
cap triangulator's SEAMS as though they were edges of the solid. The bottom skin
has three tenon holes, and the triangulator had joined two of them.

An invented edge is worse than a missing one. It reads as a joint, a seam or a
score line that somebody might then go and cut.

So the generator draws a prism's outline from its own profile, and this checks
the result the only way that means anything: every segment the page draws must
lie ALONG a real outline edge, or be one of the uprights joining the two ends of
the extrusion. Anything else is invented.

    python tools/check-prism-edges.py

Exit 0 if every segment is accounted for, 1 if any is not, 2 if node or the page
is missing. The shipped prismEdges() is lifted out of the generated page, so
this tests what ships rather than a copy of it.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = ROOT / "machine" / "drawings" / "Interactive_Model.html"
THREE = ROOT / "machine" / "drawings" / "vendor" / "three.min.js"

HARNESS = r"""
const vm = require('vm');
const sandbox = { window: {}, self: {}, console };
sandbox.window = sandbox;
vm.runInNewContext(DATA.three, sandbox);
const THREE = sandbox.THREE || sandbox.window.THREE;

const mid = [0, 0, 0];
const ctx = { THREE, mid, console };
vm.runInNewContext(DATA.fn + '; globalThis.__f = prismEdges;', ctx);
const prismEdges = ctx.__f;

// positions are float32, so at 1200 mm the round trip is worth about 1e-4
const TOL = 0.01;
function onSegment(p, a, b) {          // is p on the segment a-b?
  const vx = b[0] - a[0], vy = b[1] - a[1];
  const wx = p[0] - a[0], wy = p[1] - a[1];
  const L = Math.hypot(vx, vy);
  if (L < 1e-9) return false;
  // 🔴 A DISTANCE, NOT A CROSS PRODUCT. Comparing the raw cross against a fixed
  // tolerance scales with the coordinates: at the bottom skin's 1200 mm the
  // float32 round trip alone blows past 1e-4, and the checker then calls every
  // real edge invented. It did, on all five prisms.
  if (Math.abs(vx * wy - vy * wx) / L > TOL) return false;
  // 🔴 AND THE PARAMETER'S TOLERANCE SCALES WITH THE EDGE TOO. A fixed 1e-6 on
  // t is a tolerance of 1e-6 * L in millimetres, so on the spindle clamp's 3 mm
  // arc facets the float32 round trip put t at -6e-6 and the checker called 70
  // real edges invented. The same mistake twice in one function, once on the
  // distance and once on the parameter.
  const t = (vx * wx + vy * wy) / (L * L);
  const tEps = TOL / L;
  return t >= -tEps && t <= 1 + tEps;
}

const out = [];
for (const p of DATA.parts) {
  if (p.t !== 'prism') continue;
  const xy = (p.pl === 'xy');
  const d = p.yb - p.ya;
  const loops = [p.profile].concat(p.holes || []);
  const a = prismEdges(p).attributes.position.array;

  // undo the turn the xy prisms get, so everything is back in the shape's own
  // plane with the extrusion along the third axis
  const back = v => (xy ? [v[0], -v[2], v[1]] : [v[0], v[1], v[2]]);

  let bad = 0, total = 0;
  for (let i = 0; i < a.length; i += 6) {
    total++;
    const P = back([a[i], a[i + 1], a[i + 2]]);
    const Q = back([a[i + 3], a[i + 4], a[i + 5]]);
    const flat = Math.abs(P[2] - Q[2]) < TOL;
    let okSeg = false;
    if (flat) {
      // must lie along one edge of one loop, at one end of the extrusion
      const atEnd = Math.abs(P[2]) < TOL || Math.abs(P[2] - d) < TOL;
      if (atEnd) {
        for (const lp of loops) {
          for (let k = 0; k < lp.length && !okSeg; k++) {
            const s = lp[k], e = lp[(k + 1) % lp.length];
            if (onSegment(P, s, e) && onSegment(Q, s, e)) okSeg = true;
          }
          if (okSeg) break;
        }
      }
    } else {
      // an upright: same point in the plane, spanning the extrusion
      const samePoint = Math.abs(P[0] - Q[0]) < TOL && Math.abs(P[1] - Q[1]) < TOL;
      const spans = Math.abs(Math.abs(P[2] - Q[2]) - d) < TOL;
      if (samePoint && spans) {
        for (const lp of loops)
          for (const v of lp)
            if (Math.abs(v[0] - P[0]) < TOL && Math.abs(v[1] - P[1]) < TOL) okSeg = true;
      }
    }
    if (!okSeg) bad++;
  }
  out.push({ n: p.n, holes: (p.holes || []).length, total: total, bad: bad });
}
console.log(JSON.stringify(out));
"""


def main():
    if not PAGE.exists() or not THREE.exists():
        print("the model is not built - run tools/make-3d.py first", file=sys.stderr)
        return 2
    node = shutil.which("node")
    if not node:
        print("node is not on PATH, so the shipped code cannot be run."
              " THIS IS NOT A PASS.", file=sys.stderr)
        return 2

    html = PAGE.read_text(encoding="utf-8")
    parts = json.loads(re.search(r"const PARTS=(\[.*?\]), GROUPS=", html, re.S).group(1))
    fn = re.search(r"function prismEdges\(p\)\{[\s\S]*?\n\}", html).group(0)
    data = json.dumps({"parts": parts, "fn": fn,
                       "three": THREE.read_text(encoding="utf-8")})

    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "h.js"
        f.write_text("const DATA=" + data + ";\n" + HARNESS, encoding="utf-8")
        r = subprocess.run([node, str(f)], capture_output=True,
                           encoding="utf-8", errors="replace")
    if r.returncode:
        print("node failed:\n" + (r.stderr or "")[:2000], file=sys.stderr)
        return 2

    rows = json.loads(r.stdout.strip().splitlines()[-1])
    bad = 0
    for row in rows:
        mark = "ok   " if row["bad"] == 0 else "FAIL "
        if row["bad"]:
            bad += 1
        print(f"  {mark} {row['n']:16s} {row['holes']} hole(s)  "
              f"{row['total']:4d} segments, {row['bad']} not on the part")
    print(f"\n{len(rows)} prism(s), {bad} drawing an edge that is not there")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
