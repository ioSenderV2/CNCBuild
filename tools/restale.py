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

# A SECOND KEY, file:LITERAL rather than file:line, for a number that collides with
# a symbol's old value ANYWHERE in a file that is not about that symbol at all.
# Line keys rot: anything inserted above shifts them silently, and the entry then
# whitelists an innocent line while the real one fires again. These do not move.
# Use this form only where the file genuinely never cites the symbol - a coincidence
# of digits, not a judgement about staleness.
KEEP_LITERAL = {
    "wiring/db37-axis-interconnect.md:20": "a DB37 PIN NUMBER. The line says "
                                           "'block in row', which is what drags "
                                           "a block symbol into range",
    "machine/gantry-beam-joint.md:20": "the extrusion's slot centrelines are "
                                       "20 / 60 / 100 - a profile feature, and "
                                       "this file never cites a rail inset",
    "machine/spoilboard.md:20": "SPOIL_BOLT_INSET is its own 20, named on the "
                                "line, and has nothing to do with the Z rails",
    "machine/drawings/shop-pack.html:20": "RAIL_W - the HGR20 rail is 20 WIDE, "
                                          "and the sheet says so next to its "
                                          "400 length. Not a rail inset",
    "machine/drawings/shop-pack.html:5.2": "the front tally groups holes BY "
                                           "DRILL SIZE, so its 5.2 is a count "
                                           "key rather than a citation - and "
                                           "the region is generated by "
                                           "build-hole-tally.py, so a hand "
                                           "edit there is overwritten anyway",
    "machine/tramming.md:0.5": "M8 in a 9 mm clearance hole gives 0.5 of "
                               "radial float - its own arithmetic, named on "
                               "the line, and nothing to do with the Z plate",
    "machine/assembly.md:20": "RAIL_W again - '20 of rail' is the rail's own "
                              "section in a stack-up. An HGR20 is 20 wide and "
                              "Z_RAIL_INSET was 20 until the pitch was chosen, "
                              "so these two collide across the whole repo",
    "machine/loads-and-plate-thicknesses.md:154": "the Mega V's own 154 x 310 "
                                                  "carriage plate, quoted as the "
                                                  "comparison this build moved away "
                                                  "from - a different machine",
}


def fmt(x):
    return f"{x:g}"


def near(line, at):
    before = re.findall(r"[a-z]{3,}", line[:at].lower())[-WINDOW:]
    after = re.findall(r"[a-z]{3,}", line[at:].lower())[:WINDOW]
    return set(before) | set(after)


def from_git(rev):
    """The registry's values as of a commit, so no snapshot has to be taken.

    A snapshot you must remember to take before editing is a step that gets
    skipped on the day it matters. git already holds the previous registry, so
    this evaluates THAT and diffs against the working tree.
    """
    import subprocess
    import tempfile
    rel = "dimensions/registry.toml"
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{rel}"],
                       capture_output=True)
    if r.returncode != 0:
        print(f"cannot read {rel} at {rev}: "
              f"{r.stderr.decode(errors='replace').strip()}", file=sys.stderr)
        return None
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "registry.toml"
        p.write_bytes(r.stdout)
        try:
            old = Registry(p)
            old.evaluate_all()
        except Exception as exc:
            print(f"the registry at {rev} does not evaluate: {exc}",
                  file=sys.stderr)
            return None
        if old.errors:
            print(f"the registry at {rev} does not evaluate", file=sys.stderr)
            return None
        return {s: old.value(s) for s in old.order}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--since")
    ap.add_argument("--since-git", metavar="REV", nargs="?", const="HEAD",
                    help="previous values from a committed registry.toml; "
                         "no snapshot to remember to take")
    ap.add_argument("--snapshot")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--gate", action="store_true",
                    help="exit non-zero if any prose is still on an old value")
    a = ap.parse_args()

    reg = Registry()
    reg.evaluate_all()
    now = {s: reg.value(s) for s in reg.order}

    if a.snapshot:
        Path(a.snapshot).write_text(json.dumps(now, indent=0), encoding="utf-8")
        print(f"snapshot of {len(now)} symbols -> {a.snapshot}")
        return 0
    if a.since_git:
        before = from_git(a.since_git)
        if before is None:
            return 2
    elif a.since:
        before = json.loads(Path(a.since).read_text(encoding="utf-8"))
    else:
        print("need --since-git [REV], --since FILE or --snapshot OUT",
              file=sys.stderr)
        return 2
    moved = {s: (before[s], now[s]) for s in now
             if s in before and abs(now[s] - before[s]) > 1e-9}
    if not moved:
        print("nothing moved since that snapshot")
        return 0
    print(f"{len(moved)} symbol(s) moved; looking for prose still on the old "
          f"value\n")

    names = {s: audit.name_words(s) for s in moved}
    # old value as it would have been written, -> symbols that had it
    #
    # 🔴 AN OLD VALUE OF ZERO IS NEVER A CITATION. A symbol sitting at 0 is an
    # OPEN placeholder - nothing in prose was ever quoting it - and a bare 0 is
    # in every stroke-width, coordinate and count on the page, so the moment
    # such a symbol gets a real value this tool reports the whole file. It fired
    # three times on shop-pack.html's SVG the day BASE_BOLT_WASHER went 0 to 25,
    # and all three were rects. Skipped rather than KEEPed one line at a time,
    # because the next placeholder to be filled would do it again somewhere new.
    old_lit = {}
    for s, (b, _) in moved.items():
        if abs(b) < 1e-9:
            continue
        old_lit.setdefault(fmt(b), []).append(s)

    hits, files = 0, sorted({p for pat in SCAN for p in ROOT.glob(pat)})
    for f in files:
        text = f.read_text(encoding="utf-8")
        out, changed = [], False
        for ln, line in enumerate(text.split("\n"), 1):
            cells = [m.span() for m in CELL.finditer(line)]
            new, last = [], 0
            # 🔴 A NUMBER GLUED TO A HYPHEN AND A WORD IS PART OF A NAME, not a
            # citation: 25-series extrusion, 30-6060, 2x3. The leading lookbehind
            # already refused a hyphen BEFORE the digits and the trailing one did
            # not, so "25-series" matched and the day BASE_BOLT_WASHER went 25 to
            # 24 it was reported as stale prose in three-point-mount.md - on a
            # line whose subject is which extrusion NOT to rebuild the base in.
            # The name words matched only because that line says "base".
            # A FRACTION IS NOT TWO NUMBERS. The day TT_BED_BAR_T went 5 to 10.6
            # this reported the 5 in `5/8" aluminium bar` on the Z spacer bar
            # sheet - a part with no connection to the bed at all, matched
            # because that line also says "bar". --apply would have written
            # 10.6/8". This repo quotes imperial fractions constantly, so a
            # numerator or denominator is excluded outright: a digit touching a
            # slash is part of a fraction or a path, never a quoted value.
            for m in re.finditer(r"(?<![\w.\-{/])(\d{1,5}(?:\.\d{1,4})?)"
                                 r"(?![\w./]|-\w|\s*\}\})", line):
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
                rel = f.relative_to(ROOT).as_posix()
                where = f"{rel}:{ln}"
                if where in KEEP:
                    print(f"  KEPT {where}  {m.group(1)}  -  {KEEP[where]}")
                    continue
                by_lit = f"{rel}:{m.group(1)}"
                if by_lit in KEEP_LITERAL:
                    print(f"  KEPT {where}  {m.group(1)}  -  {KEEP_LITERAL[by_lit]}")
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

    if a.gate and hits:
        print(f"\n{hits} line(s) still quote a value the registry has moved "
              f"away from.\nRun: python tools/restale.py --since-git --apply",
              file=sys.stderr)
        return 1
    print(f"\n{hits} stale quotation(s)"
          f"{' rewritten' if a.apply else ' (dry run)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
