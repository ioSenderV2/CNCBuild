#!/usr/bin/env python3
"""CNCBuild dimension registry - evaluate, check, and export.

The registry (dimensions/registry.toml) is AUTHORITATIVE FOR VALUES. The machine/*.md
files stay authoritative for reasoning. This tool is what makes that claim mean
something rather than being a note nobody enforces.

    dims.py check            evaluate everything; non-zero exit on any error
    dims.py table            print every symbol, value and provenance
    dims.py deps SYM         what depends on SYM, transitively - run this BEFORE
                             changing a primitive
    dims.py open             every OPEN symbol, i.e. every value that must not be cut to
    dims.py fusion [-o F]    Fusion 360 parameters CSV
    dims.py md [-o F]        generated markdown table for the prose to link to

Why `deps` exists: on 2026-10-02 two numbers in the prose were found to have been
computed from sources that later moved - the shelf's rear bolt, keyed off a beam face
that went flush, and a "1.8 mm proud" figure keyed off an M8 column that had been
corrected from 20 to 35. Neither had any link back to its source. `deps` is that link.

No third-party imports: stdlib only, so it runs wherever Python 3.11+ does.
"""

from __future__ import annotations

import argparse
import ast
import csv
import operator
import sys
import tomllib
from pathlib import Path

# The notes are full of emoji markers and they reach stdout in `table`, `deps` and
# `open`. On a default Windows console that is cp1252 and the print RAISES, so a
# single marker in one note kills the whole report partway through - `deps` died on
# FLANGE_HEAD_D on 2026-10-08 and reported nothing at all. Reconfigure rather than
# strip: the markers are load-bearing in the prose. Same fix as tools/audit-prose.py.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "dimensions" / "registry.toml"

PROVENANCE = {"measured", "part", "vendor", "nominal", "derived", "OPEN"}

# Provenance that means "this number is not confirmed on the real thing". The repo's
# standing rule is that the machine is the authority, so these are called out loudly.
UNCONFIRMED = {"nominal", "OPEN"}

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


class RegistryError(Exception):
    pass


def _eval_node(node: ast.AST, resolve) -> float:
    """Evaluate one node of an expression. Deliberately not eval(): the registry is a
    data file, and a data file should not be able to execute anything."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, resolve)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise RegistryError(f"non-numeric constant {node.value!r}")
    if isinstance(node, ast.Name):
        return resolve(node.id)
    if isinstance(node, ast.BinOp):
        op = _BINOPS.get(type(node.op))
        if op is None:
            raise RegistryError(f"operator {type(node.op).__name__} not allowed")
        return op(_eval_node(node.left, resolve), _eval_node(node.right, resolve))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        v = _eval_node(node.operand, resolve)
        return v if isinstance(node.op, ast.UAdd) else -v
    raise RegistryError(f"expression node {type(node).__name__} not allowed")


def refs(expr: str) -> set[str]:
    return {n.id for n in ast.walk(ast.parse(expr, mode="eval")) if isinstance(n, ast.Name)}


class Registry:
    def __init__(self, path: Path = REGISTRY):
        self.path = path
        with path.open("rb") as fh:
            raw = tomllib.load(fh)
        self.meta = raw.get("meta", {})
        self.dims: dict[str, dict] = {}
        self.order: list[str] = []
        self.errors: list[str] = []

        for d in raw.get("dim", []):
            sym = d.get("sym")
            if not sym:
                self.errors.append(f"an entry has no `sym`: {d}")
                continue
            if sym in self.dims:
                self.errors.append(f"{sym}: defined twice")
                continue
            has_v, has_e = "value" in d, "expr" in d
            if has_v == has_e:
                self.errors.append(f"{sym}: needs exactly one of `value` or `expr`")
                continue
            if has_e:
                d.setdefault("provenance", "derived")
            p = d.get("provenance")
            if p not in PROVENANCE:
                self.errors.append(f"{sym}: provenance {p!r} not one of {sorted(PROVENANCE)}")
            if has_e and p != "derived":
                self.errors.append(f"{sym}: has `expr` so provenance must be 'derived', not {p!r}")
            if not (sym[0].isalpha() and all(c.isalnum() or c == "_" for c in sym)):
                self.errors.append(f"{sym}: not a Fusion-safe identifier")
            d.setdefault("unit", self.meta.get("units", "mm"))
            self.dims[sym] = d
            self.order.append(sym)

        self._values: dict[str, float] = {}
        self._resolving: list[str] = []

    def value(self, sym: str) -> float:
        if sym in self._values:
            return self._values[sym]
        if sym not in self.dims:
            raise RegistryError(f"undefined symbol {sym}")
        if sym in self._resolving:
            cycle = " -> ".join(self._resolving[self._resolving.index(sym):] + [sym])
            raise RegistryError(f"circular definition: {cycle}")
        d = self.dims[sym]
        self._resolving.append(sym)
        try:
            if "value" in d:
                v = float(d["value"])
            else:
                v = _eval_node(ast.parse(d["expr"], mode="eval"), self.value)
        finally:
            self._resolving.pop()
        self._values[sym] = v
        return v

    def evaluate_all(self) -> list[str]:
        """Resolve every symbol. Returns the error list (also appended to self.errors)."""
        for sym in self.order:
            try:
                self.value(sym)
            except RegistryError as e:
                self.errors.append(f"{sym}: {e}")
            except ZeroDivisionError:
                self.errors.append(f"{sym}: division by zero")
        return self.errors

    def direct_dependents(self, sym: str) -> list[str]:
        out = []
        for other, d in self.dims.items():
            if "expr" in d and sym in refs(d["expr"]):
                out.append(other)
        return out

    def all_dependents(self, sym: str) -> list[str]:
        seen, stack = set(), [sym]
        while stack:
            for dep in self.direct_dependents(stack.pop()):
                if dep not in seen:
                    seen.add(dep)
                    stack.append(dep)
        return sorted(seen)

    def fmt(self, sym: str) -> str:
        v = self.value(sym)
        return f"{v:g}" if abs(v - round(v, 4)) < 1e-9 else f"{v:.4f}"


def _load(strict: bool = True) -> Registry:
    reg = Registry()
    reg.evaluate_all()
    if reg.errors and strict:
        print("REGISTRY ERRORS:", file=sys.stderr)
        for e in reg.errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    return reg


def cmd_check(_args) -> int:
    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("FAIL")
        for e in reg.errors:
            print(f"  {e}")
        return 1
    unconfirmed = [s for s in reg.order if reg.dims[s]["provenance"] in UNCONFIRMED]
    print(f"OK - {len(reg.order)} symbols resolve, no cycles, no undefined references.")
    if unconfirmed:
        print(f"\n{len(unconfirmed)} NOT confirmed on the real part - do not cut to these:")
        for s in unconfirmed:
            d = reg.dims[s]
            print(f"  [{d['provenance']:7}] {s:28} = {reg.fmt(s):>10} {d['unit']}")
    return 0


def cmd_table(_args) -> int:
    reg = _load()
    print(f"{'SYMBOL':30} {'VALUE':>10} {'UNIT':5} {'PROVENANCE':11} NOTE")
    print("-" * 110)
    for s in reg.order:
        d = reg.dims[s]
        note = d.get("note", "")
        if "expr" in d:
            note = f"= {d['expr']}" + (f"  |  {note}" if note else "")
        print(f"{s:30} {reg.fmt(s):>10} {d['unit']:5} {d['provenance']:11} {note[:60]}")
    return 0


def cmd_deps(args) -> int:
    reg = _load()
    sym = args.symbol
    if sym not in reg.dims:
        print(f"undefined symbol {sym}", file=sys.stderr)
        return 1
    d = reg.dims[sym]
    print(f"{sym} = {reg.fmt(sym)} {d['unit']}  [{d['provenance']}]")
    if d.get("note"):
        print(f"  {d['note']}")
    if "expr" in d:
        print(f"\n  built from: {d['expr']}")
    deps = reg.all_dependents(sym)
    if not deps:
        print("\nNothing depends on this. Changing it is local.")
        return 0
    print(f"\nCHANGING {sym} RE-DERIVES {len(deps)}:")
    direct = set(reg.direct_dependents(sym))
    for dep in deps:
        mark = "*" if dep in direct else " "
        print(f"  {mark} {dep:28} = {reg.fmt(dep):>10}   {reg.dims[dep].get('expr','')}")
    print("\n  (* = directly)")
    print("\nNow grep the prose for every number above - the registry owns the value,")
    print("the .md files quote it, and nothing enforces the quote.")
    return 0


def cmd_open(_args) -> int:
    reg = _load()
    rows = [s for s in reg.order if reg.dims[s]["provenance"] in UNCONFIRMED]
    if not rows:
        print("Nothing unconfirmed.")
        return 0
    for s in rows:
        d = reg.dims[s]
        print(f"[{d['provenance']:7}] {s:28} = {reg.fmt(s):>10} {d['unit']}")
        if d.get("note"):
            print(f"              {d['note']}")
        dependents = reg.all_dependents(s)
        if dependents:
            print(f"              feeds: {', '.join(dependents)}")
    return 0


def cmd_fusion(args) -> int:
    """Fusion 360: Modify > Change Parameters > Import.

    Columns are name, unit, expression, comment. Fusion has shipped variations on
    whether a header row is accepted, so --header is there if yours wants one.
    VERIFY THE IMPORT rather than trusting this - if Fusion rejects the file, the
    header is the first thing to try either way.
    """
    reg = _load()
    out = Path(args.output) if args.output else ROOT / "dimensions" / "fusion-parameters.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if args.header:
            w.writerow(["Name", "Unit", "Expression", "Comment"])
        for s in reg.order:
            d = reg.dims[s]
            unit = d["unit"]
            if unit == "kg":
                continue  # Fusion parameters are lengths here; mass is not one
            comment = d.get("note", "")
            comment = f"[{d['provenance']}] {comment}".strip()
            # Export every symbol as a plain number, NOT as its expression. Fusion would
            # happily take the expression, but then two systems would own the same
            # derivation and they would drift - which is the exact failure this registry
            # exists to stop. The registry derives; Fusion consumes.
            w.writerow([s, unit, reg.fmt(s), comment[:250]])
    n = sum(1 for s in reg.order if reg.dims[s]["unit"] != "kg")
    print(f"wrote {out}  ({n} parameters)")
    print("Fusion: Modify > Change Parameters > Import. Re-run and re-import after any")
    print("registry change - Fusion holds a COPY, so it goes stale like anything else.")
    return 0


def cmd_md(args) -> int:
    reg = _load()
    out = Path(args.output) if args.output else ROOT / "dimensions" / "VALUES.md"
    lines = [
        "# Dimension values - GENERATED, DO NOT EDIT",
        "",
        "Generated by `tools/dims.py md` from [`registry.toml`](registry.toml), which is",
        "**authoritative for values**. Edit the registry, regenerate this.",
        "",
        "The `machine/*.md` files stay authoritative for **reasoning** - why a number is what",
        "it is, what it trades against, what was rejected. This table is only *what the numbers*",
        "*are*. If a number in prose disagrees with this table, the prose is stale.",
        "",
        f"Registry updated: **{reg.meta.get('updated','unknown')}**",
        "",
        "| Symbol | Value | Provenance | Built from | Note |",
        "|---|---|---|---|---|",
    ]
    for s in reg.order:
        d = reg.dims[s]
        note = (d.get("note", "") or "").replace("|", "\\|")
        expr = d.get("expr", "")
        flag = " 🔴" if d["provenance"] == "OPEN" else (" ⚠️" if d["provenance"] == "nominal" else "")
        lines.append(
            f"| **{s}**{flag} | {reg.fmt(s)} {d['unit']} | {d['provenance']} | {expr} | {note} |"
        )
    lines += [
        "",
        "## Not confirmed on the real part",
        "",
        "🔴 **OPEN** values are placeholders and **must not be cut to.** ⚠️ **nominal** values are",
        "catalogue figures not yet checked against the part - the class that produced three wrong",
        "numbers in one session on 2026-10-02.",
        "",
    ]
    for s in reg.order:
        d = reg.dims[s]
        if d["provenance"] in UNCONFIRMED:
            deps = reg.all_dependents(s)
            lines.append(
                f"- **{s}** ({d['provenance']}) = {reg.fmt(s)} {d['unit']}"
                + (f" - feeds {len(deps)}: {', '.join(deps)}" if deps else " - nothing depends on it")
            )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="evaluate everything; non-zero exit on error").set_defaults(fn=cmd_check)
    sub.add_parser("table", help="print every symbol").set_defaults(fn=cmd_table)
    sub.add_parser("open", help="every unconfirmed value").set_defaults(fn=cmd_open)
    d = sub.add_parser("deps", help="what depends on a symbol")
    d.add_argument("symbol")
    d.set_defaults(fn=cmd_deps)
    f = sub.add_parser("fusion", help="Fusion 360 parameters CSV")
    f.add_argument("-o", "--output")
    f.add_argument("--header", action="store_true", help="emit a header row")
    f.set_defaults(fn=cmd_fusion)
    m = sub.add_parser("md", help="generated markdown table")
    m.add_argument("-o", "--output")
    m.set_defaults(fn=cmd_md)
    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
