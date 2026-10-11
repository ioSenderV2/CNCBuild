#!/usr/bin/env python3
"""Does the viewer's live clash check agree with the generator's?

🔴 WHY THIS EXISTS. The interference check in tools/make-3d.py is the one the
repo trusts, and the interactive model now runs a SECOND copy of it in
JavaScript so the red boxes follow the carriages as you jog. Two
implementations of one check is exactly the arrangement that drifts: a pair
added to ALLOWED in Python, a slack value changed in one and not the other, and
the page then shows a clean machine while the console says otherwise.

So this lifts the JavaScript out of the generated page - between the
CLASH-CHECK-BEGIN and CLASH-CHECK-END markers, so it is the SHIPPED code and
not a copy of it - runs it under node at the drawn pose and at all eight corners
of travel, and compares the answer with Python's own at the same poses.

    python tools/check-clash-js.py

Exit 0 if every pose agrees, 1 if any does not, 2 if node or the page is
missing. No third-party imports.
"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = ROOT / "machine" / "drawings" / "Interactive_Model.html"


def load_generator():
    """tools/make-3d.py, imported despite the hyphen in its name."""
    spec = importlib.util.spec_from_file_location("make3d", HERE / "make-3d.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lift(page_text, name):
    """One __NAME__ value out of the generated page, as Python data."""
    m = re.search(r"const PARTS=(\[.*?\]), GROUPS=", page_text, re.S)
    if name == "PARTS":
        return json.loads(m.group(1))
    m = re.search(r"const ALLOWED=(\[.*?\]), BITE=(\[.*?\]);", page_text, re.S)
    return json.loads(m.group(1) if name == "ALLOWED" else m.group(2))


def main():
    if not PAGE.exists():
        print(f"{PAGE.name} is not built - run tools/make-3d.py first",
              file=sys.stderr)
        return 2
    node = shutil.which("node")
    if not node:
        print("node is not on PATH, so the shipped JavaScript cannot be run."
              " THIS IS NOT A PASS.", file=sys.stderr)
        return 2

    page = PAGE.read_text(encoding="utf-8")
    js = page[page.index("// CLASH-CHECK-BEGIN"):page.index("// CLASH-CHECK-END")]
    parts = lift(page, "PARTS")

    mod = load_generator()
    # The same eight corners the envelope sweep uses, plus the drawn pose.
    jog = {"X": [0, 0], "Y": [0, 0], "Z": [0, 0]}
    m = re.search(r"const JOG=(\{.*?\}), TIP=", page, re.S)
    raw = json.loads(m.group(1))
    jog = {k: [raw[k][0], raw[k][1]] for k in ("X", "Y", "Z")}
    poses = [(0.0, 0.0, 0.0)]
    for x in jog["X"]:
        for y in jog["Y"]:
            for z in jog["Z"]:
                poses.append((float(x), float(y), float(z)))

    harness = (
        "const PARTS=" + json.dumps(parts) + ";\n"
        "const ALLOWED=" + json.dumps(lift(page, "ALLOWED")) + ";\n"
        "const BITE=" + json.dumps(lift(page, "BITE")) + ";\n"
        + js + "\n"
        "const POSES=" + json.dumps([list(p) for p in poses]) + ";\n"
        "console.log(JSON.stringify(POSES.map(o=>clashesAt(o)"
        # A PAIR IS UNORDERED, so both sides name it alphabetically before
        # comparing. Without this the broad-phase sort in the page - which
        # changes only which of the two is seen first - reads as nine
        # disagreements, and a check that cries wolf gets switched off.
        ".map(c=>[c.a<c.b?c.a:c.b,c.a<c.b?c.b:c.a,"
        "c.ov.map(v=>Math.round(v*1000)/1000),c.bite])"
        ".sort())));\n")

    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "harness.js"
        f.write_text(harness, encoding="utf-8")
        r = subprocess.run([node, str(f)], capture_output=True,
                           encoding="utf-8", errors="replace")
    if r.returncode:
        print("node failed:\n" + (r.stderr or "")[:2000], file=sys.stderr)
        return 2
    got = json.loads(r.stdout)

    bites = {frozenset(b) for b in lift(page, "BITE")}
    bad = 0
    for pose, js_rows in zip(poses, got):
        py = sorted([min(a, b), max(a, b), [round(o, 3) for o in ov],
                     frozenset({a, b}) in bites]
                    for a, b, ov in mod.overlaps_at(parts, pose))
        js = sorted(js_rows)
        tag = ("drawn pose" if pose == (0.0, 0.0, 0.0)
               else f"X{pose[0]:+8.1f} Y{pose[1]:+8.1f} Z{pose[2]:+8.1f}")
        if py == js:
            print(f"  agree  {tag:34s} {len(py)} overlap(s)")
            continue
        bad += 1
        print(f"  🔴 DIFFER {tag}")
        for row in [r for r in py if r not in js]:
            print(f"       python only: {row}")
        for row in [r for r in js if r not in py]:
            print(f"       page only:   {row}")

    print(f"\n{len(poses)} pose(s) checked, {bad} disagreement(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
