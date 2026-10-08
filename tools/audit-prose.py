#!/usr/bin/env python3
"""Find prose numbers that have drifted away from the dimension registry.

The failure this catches is specific and has happened repeatedly: a number is
written into prose, the registry symbol it came from is later corrected, and the
prose keeps the old value. It still reads like a fact. Nothing cross-checks it.

So this does NOT try to find every number. It flags NEAR MISSES - a literal that
is close to a registry value but not equal to it - and only on a line that is
actually TALKING about that quantity, judged by the symbol's own name words. The
name gate is what makes the report readable: without it the same scan returns a
few hundred hits, nearly all of them two different quantities that happen to sit
close together.

    python tools/audit-prose.py               # default tolerance
    python tools/audit-prose.py --tol 2       # widen it
    python tools/audit-prose.py --sym T_FIN   # one symbol
    python tools/audit-prose.py --loose       # drop the name gate, see everything
    python tools/audit-prose.py --uncaptured  # the other direction, see below

Exit code is always 0: this is a report, not a gate. Every line needs judgement,
because a near miss is sometimes two real numbers and sometimes a stale one.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dims import Registry  # noqa: E402

# The prose is full of emoji markers and they reach stdout in the context lines. On a
# default Windows console that is cp1252 and the print RAISES, killing the report
# partway through with a traceback - so the findings after the first marker were simply
# never seen. Reconfigure rather than strip: the markers are load-bearing in the prose.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent
SCAN = ["machine/**/*.md", "machine/**/*.html", "commissioning/**/*.md", "*.md"]

# Rebuilt from the prose, so a hit here is a duplicate of one in the source file.
GENERATED = {"STATUS.md", "INDEX.md", "VALUES.md", "README.md"}

NUM = re.compile(r"(?<![\w.\-])(\d{1,5}(?:\.\d{1,3})?)(?![\w.]|-\w)")
SKIP_LINE = re.compile(r"https?://|\bcommit\b|\d{4}-\d{2}-\d{2}", re.I)

# Name words too common to identify a quantity on their own.
GENERIC = {
    "the", "and", "for", "min", "max", "first", "low", "high", "top", "bot",
    "plate", "bolt", "hole", "face", "edge", "row", "col", "len", "asbuilt",
    "asfound", "geom", "pair", "span", "range", "per", "100", "kg", "deg",
}
# Name fragments that do not appear in prose in that form.
SYNONYM = {
    "ext": "extrusion", "xep": "end plate", "bb": "baltic birch",
    "xbox": "torsion", "assy": "assembl", "thk": "thick", "sym": "",
    "inset": "inset", "stack": "stack",
}


def name_words(sym: str) -> set[str]:
    out = set()
    for raw in sym.lower().split("_"):
        w = SYNONYM.get(raw, raw)
        if not w or w in GENERIC or len(w) < 3:
            continue
        out.add(w)
    return out


def strip_markup(text: str) -> str:
    """HTML prose only: an SVG is coordinates, and a tag attribute is not a claim.

    Line numbers are preserved - every removal is replaced by its own newlines -
    so a reported line still points at the right place in the file.
    """
    def blank(m):
        return "\n" * m.group(0).count("\n")

    text = re.sub(r"<svg.*?</svg>", blank, text, flags=re.S)
    text = re.sub(r"<style.*?</style>", blank, text, flags=re.S)
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    text = re.sub(r"<sup class=\"f\">[\d.]+</sup>", "", text)      # footnote refs
    text = re.sub(r"^<p><b>[\d.]+</b>", "<p>", text, flags=re.M)   # footnote numbers
    text = re.sub(r"<[^>]+>", " ", text)
    return text.replace("&times;", "x").replace("&mdash;", "-").replace("&nbsp;", " ")


SCHED_CELL = re.compile(r'<td class="n"[^>]*>(.*?)</td>', re.S)
SHEET_ID = re.compile(r'<h[23][^>]*>\s*(Sheet\s*[\w.]+)', re.I)


def covered(lit: float, values: set[float], pitches: set[float], tol: float) -> bool:
    """Is this literal backed by the registry, directly or as a grid station?

    A row of holes on a pitch is ONE fact, not four. 32 / 62 / 92 / 122 is a
    first station and a 30 pitch, both of which are symbols; minting four more
    symbols for the stations would pad the registry without adding a thing that
    could go stale independently. So a literal also counts as covered when it is
    first + n x pitch for a small n.

    Only symbols whose NAME carries PITCH are allowed as the step. Letting any
    value act as a step makes almost everything 'covered' by coincidence.
    """
    if any(abs(lit - v) <= tol for v in values):
        return True
    for base in values:
        for p in pitches:
            for n in range(1, 8):
                if abs(lit - (base + n * p)) <= tol:
                    return True
    return False


def uncaptured(values: set[float], tol: float, pitches: set[float] | None = None) -> int:
    """The other direction: a number that gets DRILLED and has no symbol behind it.

    Scans the shop pack's hole schedules only - the numeric cells, which are the
    coordinates a person takes to a mill. A value with no registry symbol within
    `tol` is not necessarily wrong, but nothing in the repo can re-derive it, so
    when an upstream dimension moves it will not move with it. That is exactly
    how the rear plate's X values went stale.
    """
    f = ROOT / "machine" / "drawings" / "shop-pack.html"
    text = f.read_text(encoding="utf-8")
    sheet, hits = "?", 0
    seen = set()
    for m in re.finditer(r'<h[23][^>]*>.*?</h[23]>|<td class="n"[^>]*>.*?</td>', text, re.S):
        chunk = m.group(0)
        s = SHEET_ID.search(chunk)
        if s:
            sheet = s.group(1)
            continue
        plain = re.sub(r"<[^>]+>", " ", chunk)
        for lit in {round(float(x), 4) for x in NUM.findall(plain)}:
            if lit < 10 or (sheet, lit) in seen:
                continue
            if covered(lit, values, pitches or set(), tol):
                continue
            seen.add((sheet, lit))
            hits += 1
            print(f"{sheet:>10}  {lit:>10}  no registry symbol within {tol}")
    print(f"\n{hits} drilled value(s) with nothing in the registry behind them.")
    return hits


def load():
    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        for e in reg.errors:
            print("  ", e, file=sys.stderr)
        raise SystemExit(2)
    rows = []
    for sym in reg.order:
        # NOT dims[sym]["value"] - that key exists only on literal symbols, so
        # reading it drops every derived one, which is most of the registry.
        # The first cut of this tool did exactly that and reported a clean sweep.
        try:
            v = reg.value(sym)
        except Exception:
            continue
        rows.append((sym, round(float(v), 4), name_words(sym)))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tol", type=float, default=1.0)
    ap.add_argument("--sym")
    ap.add_argument("--min", type=float, default=10.0,
                    help="ignore literals below this; small integers are counts, not dimensions")
    ap.add_argument("--loose", action="store_true", help="drop the name gate")
    ap.add_argument("--uncaptured", action="store_true",
                    help="opposite direction: drilled coordinates with no registry symbol behind them")
    args = ap.parse_args()

    rows = load()
    if args.uncaptured:
        uncaptured(
            {v for _, v, _ in rows},
            0.05,                       # absorbs documented roundings: 20.5 for 20.545
            {v for s_, v, _ in rows if "PITCH" in s_},
        )
        return 0
    if args.sym:
        rows = [r for r in rows if args.sym.upper() in r[0]]
        if not rows:
            print(f"no such symbol: {args.sym}", file=sys.stderr)
            return 2
    exact = {v for _, v, _ in rows}

    files = []
    for pat in SCAN:
        files.extend(sorted(ROOT.glob(pat)))

    hits = 0
    for f in files:
        if f.name in GENERATED:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if f.suffix == ".html":
            text = strip_markup(text)
        rel = f.relative_to(ROOT).as_posix()
        for n, line in enumerate(text.splitlines(), 1):
            if SKIP_LINE.search(line):
                continue
            low = line.lower()
            for m in NUM.finditer(line):
                lit = round(float(m.group(1)), 4)
                if lit < args.min or lit in exact:
                    continue
                for sym, v, words in rows:
                    d = abs(lit - v)
                    if not (0 < d <= args.tol):
                        continue
                    if not args.loose and not (words and any(w in low for w in words)):
                        continue
                    hits += 1
                    ctx = line.strip()
                    if len(ctx) > 120:
                        s = max(0, m.start() - 55)
                        ctx = "..." + line[s:s + 120].strip() + "..."
                    print(f"{rel}:{n}  {lit} vs {v}  {sym}  d={d:g}")
                    print(f"    {ctx}")
                    break

    print(f"\n{hits} near miss(es), tol={args.tol}"
          f"{'' if args.loose else ', name-gated'}. Each needs judgement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
