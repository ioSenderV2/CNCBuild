#!/usr/bin/env python3
"""Trade jargon does not belong in this repo's prose - the guard.

The standing rule (working-rules, and the hub's rule 15: on a repeat, write a
guard): these documents exist so someone can build and wire the machine WITHOUT
hidden knowledge. A word that means something to a machinist or an electrician
and nothing to anyone else is hidden knowledge. He has named the offenders as
they appeared, and each one goes in BANNED when he does:

    "datum"      -> name the actual reference ("the bottom edge")
    "3 off"      -> QTY 3
    "FG"         -> the earth-symbol terminal (allowed only beside its own
                    translation, "frame ground", because reading a datasheet
                    next to the panel needs the mapping once)

    python tools/check-jargon.py

Exit 1 on any hit, so regen.ps1 treats it like the other checkers. Generated
files are skipped - fix the source, regenerate.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent

# (pattern, what to write instead). Each pattern is tried per line.
# "N off" as a quantity: "three off," / "2 off)" - but NOT the preposition
# ("2 off the 1225", "55 off the beam"), which a following article betrays.
QTY_OFF = re.compile(
    r"(?<![\d.])\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+off\b"
    r"(?!\s+(the|each|its|his|a|an|one|every|either|both|that|this|those|these|it|"
    r"centre|center|and)\b)",
    re.IGNORECASE,
)
BANNED = [
    (QTY_OFF, "quantity: write QTY N, not 'N off'"),
    (re.compile(r"\bdatum\b", re.IGNORECASE), "name the real reference edge or face, not 'datum'"),
    (re.compile(r"\bFG\b"), "the earth-symbol terminal; FG only beside its translation"),
]

# Generated outputs duplicate their sources; .history is VS Code's, archive is frozen.
SKIP = re.compile(r"^(STATUS\.md|INDEX\.md|dimensions/VALUES\.md|docs/registry\.html|"
                  r"docs/(build-document|design-record|wiring-document)\.html|"
                  r"docs/drawings/(base-construction|torsion-box-construction|base-cutlist|"
                  r"fasteners|board-mounting|Interactive_Model)\.html|"
                  r"machine/archive/|\.history/|docs/drawings/vendor/)")


def main() -> int:
    files = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "*.md", "*.html", "*.toml"],
        capture_output=True, text=True).stdout.split()
    hits = 0
    for rel in files:
        if SKIP.match(rel):
            continue
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pat, fix in BANNED:
                m = pat.search(line)
                if not m:
                    continue
                if pat.pattern.startswith(r"\bFG\b") and "frame ground" in line:
                    continue
                print(f"  {rel}:{lineno}: '{m.group(0)}' - {fix}")
                print(f"      {line.strip()[:140]}")
                hits += 1
    if hits:
        print(f"\n{hits} jargon hit(s) - the documents are for building without hidden knowledge.")
        return 1
    print("no trade jargon in the prose")
    return 0


if __name__ == "__main__":
    sys.exit(main())
