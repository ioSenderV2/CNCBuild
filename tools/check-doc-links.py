#!/usr/bin/env python3
"""Audit every link in the generated HTML documents: no dead anchors, no dead paths.

    check-doc-links.py          audit whatever md2html.py has written
    check-doc-links.py --build  render first, then audit

WHY THIS EXISTS
---------------
A dead link renders exactly like a live one. There is no error, no missing image, no gap in
the page - the words are underlined and blue and go nowhere, and the only way to find out is
to click it.

Two kinds go wrong, and both were found the day the wiring document was added, 2026-11-07:

  A DEAD PATH, from a heading that was renamed without its links.
  `db37-axis-interconnect.md` pointed at `#the-connector-fails-in-the-right-direction`; the
  heading had become "The connector fails safe again once the NC sensors go in". That link
  was also dead in VS Code and on GitHub, and had been for as long as the rename.

  A DEAD ANCHOR, from the chapter-namespacing in md2html's slugger. On a multi-chapter
  document every heading id is prefixed with its chapter slug, so a bare `#anchor` written in
  the markdown - correct in VS Code, correct on GitHub - pointed at nothing in the printed
  document. rebase() now prefixes bare anchors with the chapter being rendered; this script is
  what proves it, and what will notice if that ever regresses.

WHAT IT DOES NOT CHECK
----------------------
External http(s) links. They need the network, they fail for reasons that are not this
repo's, and a check that goes amber on somebody else's outage gets ignored.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Every document md2html.py writes. A new DOCS entry needs its output added here.
DOCS = [
    "docs/build-document.html",
    "docs/design-record.html",
    "docs/steel-prep.html",
    "docs/wiring-document.html",
]

HREF_RE = re.compile(r'href="([^"]+)"')
ID_RE = re.compile(r'id="([^"]+)"')


def audit(rel: str) -> tuple[int, int, int]:
    """Audit one document. Returns (hrefs, dangling anchors, broken paths)."""
    path = ROOT / rel
    if not path.exists():
        print(f"  {rel:30} NOT BUILT - run md2html.py, or --build")
        return (0, 0, 0)

    html = path.read_text(encoding="utf-8")
    anchors = set(ID_RE.findall(html))
    hrefs = sorted(set(HREF_RE.findall(html)))

    # Every document lives in docs/ now, and each one's links resolve from its own
    # directory - which this already did generically when steel-prep was the outlier.
    base = path.parent

    dangling: list[str] = []
    broken: list[str] = []
    for href in hrefs:
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in anchors:
                dangling.append(href)
            continue
        target = href.split("#")[0]
        if target and not (base / target).exists():
            broken.append(href)

    flag = "" if not (dangling or broken) else "   <-- PROBLEM"
    print(f"  {rel:30} {len(hrefs):4} links   "
          f"dangling {len(dangling)}   broken {len(broken)}{flag}")
    for href in dangling:
        print(f"      DEAD ANCHOR  {href}")
    for href in broken:
        print(f"      DEAD PATH    {href}")

    return (len(hrefs), len(dangling), len(broken))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true",
                    help="run md2html.py first, so the audit is of current output")
    args = ap.parse_args()

    if args.build:
        rc = subprocess.run([sys.executable, str(ROOT / "tools" / "md2html.py")],
                            cwd=ROOT).returncode
        if rc:
            print("md2html.py failed - nothing audited")
            return rc
        print()

    print("Links in the generated documents:")
    totals = [audit(rel) for rel in DOCS]
    links = sum(t[0] for t in totals)
    bad = sum(t[1] + t[2] for t in totals)

    print(f"\n{links} link(s) across {len(DOCS)} document(s), {bad} problem(s)")
    if bad:
        print("A dead link renders exactly like a live one. Fix the source .md, not the HTML.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
