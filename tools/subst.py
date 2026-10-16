#!/usr/bin/env python3
"""Resolve {{SYMBOL}} in the prose to the registry's value.

    subst.py --check        every .md under machine/ and wiring/; exit 1 on a
                            symbol the registry does not have

THE POINT: a number written into prose is a COPY, and copies go stale. Fifteen
places said "the 1210.73 mm rear plate" - a figure that was neither the plate's
length nor the envelope - and nothing failed, because nothing was checking. Write
{{REAR_PLATE_L_ORDERED}} instead and the number lives in exactly one place.

WHY IT FAILS RATHER THAN WARNS: audit-prose.py already reports prose that
disagrees with the registry and is deliberately kept out of the default run,
because its hits need judgement. This needs none - a symbol either exists or it
does not - so it can be a gate, and a gate is the only kind of check that stops
a stale number reaching a document.

STDLIB ONLY, because status.py imports it and status.py must run on a bare
Python: STATUS.md and INDEX.md gate correctness.

WHAT IT COSTS: the raw .md on GitHub shows the symbol rather than the number.
The rendered documents - which are what anybody builds from - show the number.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

# {{SYMBOL}}, with optional spaces. Nothing else in the prose looks like this -
# the existing style cites a symbol as bare text, which this leaves alone.
SUB_RE = re.compile(r"\{\{\s*([A-Z][A-Z0-9_]*)\s*\}\}")

_VALUES: dict[str, float] | None = None


def values() -> dict[str, float]:
    """The registry, evaluated once per process."""
    global _VALUES
    if _VALUES is None:
        from dims import Registry
        reg = Registry()
        reg.evaluate_all()
        if reg.errors:
            raise SystemExit("registry does not evaluate; fix that first")
        _VALUES = {s: reg.value(s) for s in reg.order}
    return _VALUES


def fmt(x: float) -> str:
    """A value as the prose wants to read it - no trailing zeros, no unit.

    The unit stays in the prose because that is where it reads naturally: "the
    plate is {{REAR_PLATE_L_ORDERED}} mm long" rather than a unit the registry
    would have to agree about.
    """
    return f"{x:g}"


def resolve(text: str, where: str = "") -> tuple[str, list[str]]:
    """Substitute every {{SYMBOL}}. Returns the text and any unknown symbols."""
    v = values()
    unknown: list[str] = []

    def one(m: re.Match) -> str:
        sym = m.group(1)
        if sym not in v:
            unknown.append(f"{where}: {{{{{sym}}}}} is not in the registry"
                           if where else sym)
            return m.group(0)
        return fmt(v[sym])

    return SUB_RE.sub(one, text), unknown


def read(path: Path) -> str:
    """read_text plus substitution, for the tools that consume the prose.

    Raises on an unknown symbol: a document that prints {{TYPO}} has already
    failed and printing it anyway is the thing this exists to prevent.
    """
    text, unknown = resolve(path.read_text(encoding="utf-8"),
                            str(path.relative_to(ROOT)))
    if unknown:
        raise SystemExit("\n".join(["unknown symbol in prose:"] + unknown))
    return text


def render_file(src: Path, dst: Path) -> int:
    """Substitute one file into another, for a document printed directly.

    machine/drawings/shop-pack.html is hand-authored and goes straight to the
    printer, so it cannot be rendered through md2html the way the prose is.
    make-pdf.ps1 prints a substituted copy of it instead, which is what lets
    the pack cite symbols without the braces reaching paper.
    """
    text, unknown = resolve(src.read_text(encoding="utf-8"), str(src))
    if unknown:
        print("\n".join(["unknown symbol in prose:"] + unknown),
              file=sys.stderr)
        return 1
    dst.write_text(text, encoding="utf-8", newline="")
    n = len(SUB_RE.findall(src.read_text(encoding="utf-8")))
    print(f"{n} substitution(s): {src.name} -> {dst.name}")
    return 0


def main() -> int:
    if len(sys.argv) == 4 and sys.argv[1] == "--render":
        return render_file(Path(sys.argv[2]), Path(sys.argv[3]))
    files = sorted(list((ROOT / "machine").rglob("*.md"))
                   + list((ROOT / "wiring").rglob("*.md")))
    used: dict[str, int] = {}
    bad: list[str] = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        for m in SUB_RE.finditer(text):
            used[m.group(1)] = used.get(m.group(1), 0) + 1
        _, unknown = resolve(text, str(f.relative_to(ROOT)))
        bad += unknown
    total = sum(used.values())
    print(f"{total} substitution(s) across {len(files)} file(s), "
          f"{len(used)} distinct symbol(s)")
    # "??" and not values()[sym]: the listing runs BEFORE the verdict, so an
    # unknown symbol reached this loop and raised a KeyError - the report
    # crashing instead of reporting the thing it exists to report.
    for sym in sorted(used):
        known = values().get(sym)
        print(f"    {sym:28s} x{used[sym]:<3} = "
              f"{fmt(known) if known is not None else '?? NOT IN REGISTRY'}")
    if bad:
        print("\nUNKNOWN:", file=sys.stderr)
        for b in bad:
            print(f"    {b}", file=sys.stderr)
        return 1
    print("\nEvery symbol resolves.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
