#!/usr/bin/env python3
"""Fail if a registry note that CHANGED is carrying history.

    python tools/check-note-history.py            # against HEAD
    python tools/check-note-history.py HEAD~3     # against another rev

A note says what the number is, what forces it, and what breaks if it moves.
What it used to be is not information - the value is in the registry and the
change is in git, and a reader working from the sheet does not need either.

ONLY CHANGED AND NEW NOTES ARE CHECKED. The existing corpus is full of this
and rewriting it wholesale is not the point; the point is that the next note
written does not add more. So this is a ratchet, not an audit.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REL = "dimensions/registry.toml"

# Each is a phrase that only appears when a note is narrating its own past.
MARKERS = [
    r"\d{4}-\d{2}-\d{2}",
    r"\bused to\b", r"\bit was\b", r"\bthey were\b", r"\bwas stale\b",
    r"\bwent stale\b", r"\bcame down from\b", r"\bcame to\b",
    r"\bthis note said\b", r"\bit read\b", r"\bhad been\b", r"\bformerly\b",
    r"\bpreviously\b", r"\bwas recorded\b", r"\bno longer reads\b",
    r"\buntil the\b", r"\bwas pinned at\b", r"\bhas been\b",
]
RX = [re.compile(m, re.I) for m in MARKERS]

BLOCK = re.compile(r'^sym = "([A-Z0-9_]+)"', re.M)


def notes(text: str) -> dict[str, str]:
    """sym -> note, for every [[dim]] in a registry's text."""
    out, syms = {}, list(BLOCK.finditer(text))
    for i, m in enumerate(syms):
        end = syms[i + 1].start() if i + 1 < len(syms) else len(text)
        chunk = text[m.start():end]
        n = re.search(r'^note = "(.*)"$', chunk, re.M)
        out[m.group(1)] = n.group(1) if n else ""
    return out


def main() -> int:
    rev = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    try:
        was = subprocess.run(["git", "show", f"{rev}:{REL}"], cwd=ROOT,
                             capture_output=True, text=True, check=True,
                             encoding="utf-8").stdout
    except subprocess.CalledProcessError:
        print(f"cannot read {REL} at {rev}", file=sys.stderr)
        return 2

    before = notes(was)
    after = notes((ROOT / REL).read_text(encoding="utf-8"))

    hits = []
    for sym, note in after.items():
        if before.get(sym) == note:
            continue                       # untouched; not this tool's business
        for rx in RX:
            m = rx.search(note)
            if m:
                i = max(0, m.start() - 40)
                hits.append((sym, m.group(0), note[i:m.end() + 40]))
                break

    changed = sum(1 for s, n in after.items() if before.get(s) != n)
    if hits:
        print(f"HISTORY IN {len(hits)} CHANGED NOTE(S) - a note says what the "
              f"number is, not what it was:", file=sys.stderr)
        for sym, hit, ctx in hits:
            print(f"    {sym}: '{hit}'", file=sys.stderr)
            print(f"        ...{ctx}...", file=sys.stderr)
        return 1
    print(f"{changed} note(s) changed against {rev}, none narrating its own "
          f"past")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
