#!/usr/bin/env python3
"""Replace prose literals that match a registry symbol with {{SYMBOL}}.

    sweep-prose.py              report what it would change, touch nothing
    sweep-prose.py --apply      write it
    sweep-prose.py --file F     one file

THE FAILURE IT ENDS: a number written into prose is a COPY. It reads like a
fact, nothing cross-checks it, and when the symbol it came from moves the copy
keeps the old value. tools/subst.py already renders {{SYMBOL}} at build time and
fails on a symbol that does not exist - what was missing is anything that turns
the existing literals INTO symbols.

IT ONLY TOUCHES THE UNAMBIGUOUS ONES. A literal is converted when, and only
when, EXACTLY ONE symbol both equals it and is named by the words around it -
the same name gate tools/audit-prose.py uses, for the same reason: without it a
bare 30 matches a dozen symbols and the sweep becomes a random edit. Anything
with two candidates or none is listed, not changed.

NEVER TOUCHED: fenced code, URLs, dates, footnote markers, table rules, a number
already inside braces, and the figures in generated files.
"""
from __future__ import annotations

import argparse
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
SCAN = ["machine/*.md", "commissioning/*.md", "wiring/*.md"]
EPS = 1e-6

# A line this matches is left alone outright.
SKIP_LINE = re.compile(r"https?://|\b\d{4}-\d{2}-\d{2}\b|^\s*\|?\s*[-:| ]+\s*\|?\s*$")
# and a literal already in braces, or one that is part of a bigger token
BRACED = re.compile(r"\{\{[^}]*\}\}")
NUM = re.compile(r"(?<![\w.\-{])(\d{1,5}(?:\.\d{1,4})?)(?![\w.]|-\w|\s*\}\})")


def candidates(reg, vals):
    """value -> [symbols with that value], for the live symbols only."""
    out = {}
    for s in reg.order:
        if reg.dims[s].get("retired"):
            continue
        out.setdefault(round(vals[s], 6), []).append(s)
    return out


def line_words(line):
    return set(re.findall(r"[a-z]{3,}", line.lower()))


# How many words either side of the literal the symbol has to be named within.
# THE WHOLE LINE IS TOO WIDE A WINDOW. audit-prose gates on the line because a
# person then reads the line and decides; an edit cannot. On a line reading
# "a 48 V rail is at the top of the lowest stated range, with about 2 V to the
# alarm" the word rail sits ten words from the 2 and matched CASTING_RAIL_BOLTS,
# which is a wrong edit that reads as a right one.
WINDOW = 5


def near_words(line, at):
    """The words within WINDOW either side of a position in the line."""
    before = re.findall(r"[a-z]{3,}", line[:at].lower())[-WINDOW:]
    after = re.findall(r"[a-z]{3,}", line[at:].lower())[:WINDOW]
    return set(before) | set(after)


def sweep_text(text, by_value, names, path):
    """Returns (new text, [converted], [ambiguous], [ungated])."""
    done, amb, ungated = [], [], []
    out_lines, fenced = [], False
    for ln, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out_lines.append(line)
            continue
        if fenced or SKIP_LINE.search(line):
            out_lines.append(line)
            continue
        words = line_words(line)
        spans = [m.span() for m in BRACED.finditer(line)]

        def guarded(a, b):
            return any(s <= a and b <= e for s, e in spans)

        new, last = [], 0
        for m in NUM.finditer(line):
            a, b = m.span()
            if guarded(a, b):
                continue
            lit = round(float(m.group(1)), 6)
            # ONLY DISTINCTIVE VALUES. A bare 1, 2, 3 or 60 matches a dozen
            # symbols by coincidence and is never the kind of number that goes
            # quietly stale; 1210.47 and 301.625 are. Requiring three digits or
            # a decimal point is what separates a dimension from a count.
            if lit < 100 and float(m.group(1)) == int(float(m.group(1))):
                continue
            syms = by_value.get(lit, [])
            if not syms:
                continue
            close = near_words(line, a)
            hit = [s for s in syms if names[s] and names[s] & close]
            if len(hit) == 1:
                new.append(line[last:a])
                new.append("{{" + hit[0] + "}}")
                last = b
                done.append((path, ln, m.group(1), hit[0], line.strip()[:96]))
            elif len(hit) > 1:
                amb.append((path, ln, m.group(1), hit, line.strip()[:96]))
            else:
                ungated.append((path, ln, m.group(1), syms, line.strip()[:96]))
        new.append(line[last:])
        out_lines.append("".join(new))
    return "\n".join(out_lines), done, amb, ungated


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--file")
    ap.add_argument("--show", choices=["done", "amb", "ungated", "all"],
                    default="done")
    a = ap.parse_args()

    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        return 2
    vals = {s: reg.value(s) for s in reg.order}
    by_value = candidates(reg, vals)
    names = {s: audit.name_words(s) for s in reg.order}

    files = ([ROOT / a.file] if a.file
             else sorted(p for pat in SCAN for p in ROOT.glob(pat)))
    D, A, U = [], [], []
    for f in files:
        text = f.read_text(encoding="utf-8")
        new, d, amb, ung = sweep_text(text, by_value, names,
                                      f.relative_to(ROOT).as_posix())
        D += d; A += amb; U += ung
        if a.apply and new != text:
            f.write_text(new, encoding="utf-8", newline="")

    if a.show in ("done", "all"):
        for p, ln, lit, sym, ctx in D:
            print(f"  {p}:{ln}  {lit} -> {sym}\n      {ctx}")
    if a.show in ("amb", "all"):
        print("\nAMBIGUOUS - two or more symbols fit, left alone:")
        for p, ln, lit, syms, ctx in A:
            print(f"  {p}:{ln}  {lit}  {', '.join(syms)}\n      {ctx}")
    if a.show in ("ungated", "all"):
        print("\nVALUE MATCHES BUT THE LINE DOES NOT NAME IT, left alone:")
        for p, ln, lit, syms, ctx in U:
            print(f"  {p}:{ln}  {lit}  {', '.join(syms[:4])}\n      {ctx}")

    print(f"\n{len(D)} converted{'' if a.apply else ' (dry run)'}, "
          f"{len(A)} ambiguous, {len(U)} value-only across {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
