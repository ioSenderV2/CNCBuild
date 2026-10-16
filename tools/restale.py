#!/usr/bin/env python3
"""Find prose still quoting a symbol's OLD value, and cite the symbol instead.

    restale.py --since BEFORE.json           report
    restale.py --since BEFORE.json --apply   write it

WHY THIS IS SAFE WHERE A GENERAL SWEEP IS NOT. tools/sweep-prose.py has to guess
whether a literal means a given symbol, and guesses wrong about one time in
five. This does not guess: it is given a snapshot of the registry from before a
change, and looks only for literals equal to the value a symbol USED to have, on
a line that names it. A number equal to the old value of the very symbol the
sentence is about is not a coincidence - it is the copy that went stale when the
symbol moved, which is the failure the whole registry exists to prevent.

Replacing it with {{SYMBOL}} does not just fix today's value; it stops that line
needing to be found again.

MAKE THE SNAPSHOT BEFORE EDITING THE REGISTRY:
    python tools/restale.py --snapshot before.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from dims import Registry                                    # noqa: E402
import importlib.util                                        # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "auditprose", HERE / "audit-prose.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

ROOT = HERE.parent

# ONLY FILES THE SUBSTITUTION PASS READS. md2html.py and status.py run prose
# through tools/subst.py, and make-pdf.ps1 prints the shop pack from a
# substituted copy - so all three can carry symbols. Anywhere else the braces
# would print.
#
# ARCHIVE IS EXCLUDED ON PURPOSE. Those files record what was computed at the
# time; replacing their figures with today's rewrites the record rather than
# correcting it.
SCAN = ["machine/*.md", "commissioning/*.md", "wiring/*.md",
        "machine/drawings/shop-pack.html"]
WINDOW = 6

# 🔴 NEVER INSIDE A SCHEDULE'S NUMERIC CELL. Those are machining coordinates,
# and tools/build-hole-tally.py reads them as numbers - a symbol there breaks
# the tally and the counts that gate the pack. A coordinate with no symbol
# behind it is a real problem, but it is audit-prose's --uncaptured problem,
# not this one.
CELL = re.compile(r'<td class="n"[^>]*>.*?</td>', re.S)

# file:line that must keep its literal, with the reason. A number can equal a
# symbol's old value and still not be a citation of it - most often because the
# sentence is about what a figure USED to be.
KEEP = {
    "machine/open-items.md:120": "3.429 is the 10 gauge NOMINAL the sentence "
                                 "is contrasting, not the measured thickness",
    "machine/open-items.md:121": "the sentence is about the envelope GROWING "
                                 "to that figure, which is history",
    "machine/gantry-beam-joint.md:389": "the row's 4.97 and 2.67 are computed "
                                        "FROM this 3.429 and are literals too - "
                                        "fixing one leaves the row wrong and "
                                        "looking right",
    "machine/spoilboard.md:160": "the 8.72, 1202.52 and 1006.35 on this line "
                                 "are computed from it and are literals too",
}


def fmt(x):
    return f"{x:g}"


def near(line, at):
    before = re.findall(r"[a-z]{3,}", line[:at].lower())[-WINDOW:]
    after = re.findall(r"[a-z]{3,}", line[at:].lower())[:WINDOW]
    return set(before) | set(after)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--since")
    ap.add_argument("--snapshot")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    reg = Registry()
    reg.evaluate_all()
    now = {s: reg.value(s) for s in reg.order}

    if a.snapshot:
        Path(a.snapshot).write_text(json.dumps(now, indent=0), encoding="utf-8")
        print(f"snapshot of {len(now)} symbols -> {a.snapshot}")
        return 0
    if not a.since:
        print("need --since BEFORE.json or --snapshot OUT.json", file=sys.stderr)
        return 2

    before = json.loads(Path(a.since).read_text(encoding="utf-8"))
    moved = {s: (before[s], now[s]) for s in now
             if s in before and abs(now[s] - before[s]) > 1e-9}
    if not moved:
        print("nothing moved since that snapshot")
        return 0
    print(f"{len(moved)} symbol(s) moved; looking for prose still on the old "
          f"value\n")

    names = {s: audit.name_words(s) for s in moved}
    # old value as it would have been written, -> symbols that had it
    old_lit = {}
    for s, (b, _) in moved.items():
        old_lit.setdefault(fmt(b), []).append(s)

    hits, files = 0, sorted({p for pat in SCAN for p in ROOT.glob(pat)})
    for f in files:
        text = f.read_text(encoding="utf-8")
        out, changed = [], False
        for ln, line in enumerate(text.split("\n"), 1):
            cells = [m.span() for m in CELL.finditer(line)]
            new, last = [], 0
            for m in re.finditer(r"(?<![\w.\-{])(\d{1,5}(?:\.\d{1,4})?)"
                                 r"(?![\w.]|\s*\}\})", line):
                if any(a <= m.start() and m.end() <= b for a, b in cells):
                    continue                    # a machining coordinate
                lit = fmt(float(m.group(1)))
                cands = old_lit.get(lit, [])
                if not cands:
                    continue
                close = near(line, m.start())
                fit = [s for s in cands if names[s] and names[s] & close]
                if len(fit) != 1:
                    continue
                where = f"{f.relative_to(ROOT).as_posix()}:{ln}"
                if where in KEEP:
                    print(f"  KEPT {where}  {m.group(1)}  -  {KEEP[where]}")
                    continue
                sym = fit[0]
                new.append(line[last:m.start()])
                new.append("{{" + sym + "}}")
                last = m.end()
                changed = True
                hits += 1
                print(f"  {f.relative_to(ROOT).as_posix()}:{ln}  "
                      f"{m.group(1)} was {sym}, now {fmt(now[sym])}")
                print(f"      {line.strip()[:104]}")
            new.append(line[last:])
            out.append("".join(new))
        if a.apply and changed:
            f.write_text("\n".join(out), encoding="utf-8", newline="")

    print(f"\n{hits} stale quotation(s)"
          f"{' rewritten' if a.apply else ' (dry run)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
