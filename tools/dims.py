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
import re
import sys
import tomllib
from pathlib import Path

# The notes are full of emoji markers and they reach stdout in `table`, `deps` and
# `open`. On a default Windows console that is cp1252 and the print RAISES, so a
# single marker in one note kills the whole report partway through - `deps` died on
# FLANGE_NORMAL_D on 2026-10-08 and reported nothing at all. Reconfigure rather than
# strip: the markers are load-bearing in the prose. Same fix as tools/audit-prose.py.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "dimensions" / "registry.toml"

PROVENANCE = {"measured", "part", "vendor", "nominal", "derived", "alias",
              "pinned", "OPEN"}

# FLAG: PINNED IS NOT DERIVED - his call, 2026-10-11. 51 symbols carry a literal
# value while having come out of a calculation, and XEP_W says what that means:
# "set by BLOCK_BUTTED at 154.18, rounded down. NOT RE-DERIVED." The difference
# is the whole point of `deps`: a derived number FOLLOWS its source when the
# source moves, and a pinned one does not. Calling both derived is how a number
# goes stale without anything noticing - which is the exact failure that made
# this registry exist. Pinned says: this came from somewhere, go and re-check it
# by hand if that somewhere moves.

# FLAG: AN ALIAS IS A RENAME, NOT A CALCULATION - his call, 2026-10-11, after
# RAIL_LOW_Z read as "derived from RAIL_SLOT_INSET" when both are 15 and nothing
# happens in between. 31 of the registry's symbols are one symbol pointing
# straight at another, and calling that derived hides the single most useful
# thing about it: there is no arithmetic to check, only a question of whether
# the two still MEAN the same thing. It is assigned mechanically - a bare name
# is an alias, anything else is derived - so it cannot be got wrong by hand.

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


def is_alias(expr: str) -> bool:
    """Is this expression nothing but another symbol's name?

    That is a RENAME, and it is worth telling apart from a calculation: there is
    no arithmetic in it to be wrong, only the question of whether the two still
    mean the same thing. The day the answer is no, the alias has to become a
    value or an expression - and the thing that would hide that day coming is
    exactly how alike the two look.
    """
    try:
        return isinstance(ast.parse(expr, mode="eval").body, ast.Name)
    except SyntaxError:
        return False


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
        # FLAG: RETIRED IS A FLAG, NOT A PROVENANCE - his, 2026-10-11. The two
        # answer different questions: provenance is where the number came from,
        # retired is whether anything still wants it. FIN_KERF is nominal AND
        # retired, and folding one into the other would lose that it was never
        # confirmed either. Kept rather than deleted because a retired symbol is
        # usually the only record of a reversal - FIN_KERF is why FIN_TOP_W
        # reads 100 again rather than 99.625.
        self.retired: list[str] = []

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
                d["provenance"] = "alias" if is_alias(d["expr"]) else "derived"
            p = d.get("provenance")
            if p not in PROVENANCE:
                self.errors.append(f"{sym}: provenance {p!r} not one of {sorted(PROVENANCE)}")
            # A `value` cannot be derived or an alias: both of those mean the
            # number is computed from another symbol every time it is read. A
            # value that CAME from a calculation is `pinned`.
            if not has_e and p in ("derived", "alias"):
                self.errors.append(
                    f"{sym}: provenance {p!r} is for an `expr`; a literal value "
                    f"that came out of a calculation is 'pinned'")
            if not (sym[0].isalpha() and all(c.isalnum() or c == "_" for c in sym)):
                self.errors.append(f"{sym}: not a Fusion-safe identifier")
            d.setdefault("unit", self.meta.get("units", "mm"))
            if d.get("retired"):
                self.retired.append(sym)
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

    def check_retired(self) -> list[str]:
        """A retired symbol that something still derives from is not retired.

        This is the whole value of the flag: it is a claim that nothing wants
        this number any more, and a claim that can be checked is worth more than
        a note saying the same thing - the note cannot notice when it stops
        being true.
        """
        for sym in self.retired:
            users = self.direct_dependents(sym)
            if users:
                self.errors.append(
                    f"{sym}: marked retired, but {', '.join(users)} still "
                    f"derive(s) from it")
        return self.errors

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
    reg.check_retired()
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
    unconfirmed = [s for s in reg.order
                   if reg.dims[s]["provenance"] in UNCONFIRMED
                   and not reg.dims[s].get("retired")]
    print(f"OK - {len(reg.order)} symbols resolve, no cycles, no undefined references.")
    if reg.retired:
        print(f"{len(reg.retired)} retired and kept for the record: "
              + ", ".join(reg.retired))
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
    # A RETIRED SYMBOL IS NOT A THING TO CUT TO, so it does not belong in a
    # list of numbers nobody has confirmed - nobody is going to use it at all.
    rows = [s for s in reg.order
            if reg.dims[s]["provenance"] in UNCONFIRMED
            and not reg.dims[s].get("retired")]
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
        flag = " FLAG:" if d["provenance"] == "OPEN" else (" OPEN:" if d["provenance"] == "nominal" else "")
        lines.append(
            f"| **{s}**{flag} | {reg.fmt(s)} {d['unit']} | {d['provenance']} | {expr} | {note} |"
        )
    lines += [
        "",
        "## Not confirmed on the real part",
        "",
        "FLAG: **OPEN** values are placeholders and **must not be cut to.** OPEN: **nominal** values are",
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



# A SYMBOL NAME, for turning mentions in prose into links. Conservative on
# purpose: underscores and digits are part of a name, so the boundaries have to
# exclude them or TT_BED_T would match inside TT_BED_TOP.
_SYM_RE = re.compile(r"(?<![A-Za-z0-9_])([A-Z][A-Z0-9_]{2,})(?![A-Za-z0-9_])")


def _sections(path: Path) -> dict[str, str]:
    """{symbol: the section heading it sits under}, read from the RAW file.

    tomllib throws comments away, and the registry's structure lives entirely in
    them - 84 headings written as `# ---- the front fin`. Parsing the text is the
    only way to keep that structure, and it is why this reads the file a second
    time rather than using the loaded table.
    """
    out, current = {}, "unsectioned"
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#\s*-{3,}\s*(.+?)\s*$", line)
        if m:
            current = m.group(1)
            continue
        m = re.match(r'^sym = "([^"]+)"', line)
        if m:
            out[m.group(1)] = current
    return out


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _attr(s: str) -> str:
    """FLAG: FOR AN ATTRIBUTE VALUE, WHICH NEEDS THE QUOTES TOO. _esc was used for
    both and does not touch them, so the one registry note that quotes him -
    SCREW_AXIS_H, carrying footnote 3.8's "25 for the casting's axis" - closed
    its own data-note early and left the rest of the sentence parsed as junk
    attributes on the card."""
    return _esc(s).replace('"', "&quot;")


def cmd_html(args) -> int:
    reg = _load()
    out = Path(args.output) if args.output else ROOT / "dimensions" / "registry.html"
    sect = _sections(reg.path)
    known = set(reg.dims)

    def link(text: str) -> str:
        """Every mention of a symbol becomes a jump to its card."""
        return _SYM_RE.sub(
            lambda m: (f'<a href="#{m.group(1)}">{m.group(1)}</a>'
                       if m.group(1) in known else m.group(1)),
            _esc(text))

    # one ordered bucket per heading, in the order the registry introduces them
    order, buckets = [], {}
    for s in reg.order:
        g = sect.get(s, "unsectioned")
        if g not in buckets:
            buckets[g] = []
            order.append(g)
        buckets[g].append(s)

    counts = {}
    for s in reg.order:
        p = reg.dims[s]["provenance"]
        counts[p] = counts.get(p, 0) + 1

    def slug(g):
        return re.sub(r"[^a-z0-9]+", "-", g.lower()).strip("-")

    cards = []
    for g in order:
        gid = slug(g)
        rows = []
        for s in buckets[g]:
            d = reg.dims[s]
            prov = d["provenance"]
            used = reg.direct_dependents(s)
            expr = ""
            if d.get("expr"):
                # ANOTHER NAME FOR THE SAME NUMBER reads differently from a sum,
                # and the card should say which it is at a glance.
                lbl = "another name for" if prov == "alias" else "built from"
                expr = (f'<div class="r"><b>{lbl}</b> '
                        f'<code>{link(d["expr"])}</code></div>')
            src = (f'<div class="r"><b>source</b> {link(d["source"])}</div>'
                   if d.get("source") else "")
            usedby = ("" if not used else
                      '<div class="r"><b>used by</b> '
                      + ", ".join(f'<a href="#{u}">{u}</a>' for u in used)
                      + "</div>")
            note = (f'<div class="n">{link(d.get("note", ""))}</div>'
                    if d.get("note") else "")
            ret = bool(d.get("retired"))
            tag = '<span class="retired-tag">retired</span>' if ret else ""
            rows.append(
                f'<div class="sym p-{prov}{" retired" if ret else ""}" id="{s}" '
                f'data-sym="{s.lower()}" '
                f'data-prov="{prov}" data-retired="{"1" if ret else ""}" '
                f'data-note="{_attr(d.get("note","")).lower()}">'
                f'<div class="hd"><a class="name" href="#{s}">{s}</a>'
                f'<span class="val">{reg.fmt(s)} {d["unit"]}</span>'
                f'<span class="prov">{prov}</span>{tag}</div>'
                f"{expr}{usedby}{src}{note}</div>")
        cards.append(
            f'<section id="{gid}"><h2>{_esc(g)}</h2>{"".join(rows)}</section>')

    toc = "".join(
        f'<a href="#{slug(g)}">{_esc(g)}<span>{len(buckets[g])}</span></a>'
        for g in order)
    chips = "".join(
        f'<button type="button" class="chip" data-prov="{p}">{p} '
        f'<span>{counts[p]}</span></button>' for p in sorted(counts))
    nret = sum(1 for s in reg.order if reg.dims[s].get("retired"))
    if nret:
        chips += (f'<button type="button" class="chip" data-retired="1">retired '
                  f'<span>{nret}</span></button>')

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CNCBuild &mdash; the dimension registry</title>
<style>
 :root {{ color-scheme: light dark; }}
 * {{ box-sizing: border-box; }}
 body {{ margin: 0; font: 14px/1.5 "Segoe UI", system-ui, sans-serif;
   color: #1b1f23; background: #f6f7f8; }}
 header {{ position: sticky; top: 0; z-index: 5; background: #fffffff2;
   border-bottom: 1px solid #d8dde2; padding: 10px 16px;
   backdrop-filter: blur(6px); }}
 h1 {{ font-size: 15px; margin: 0 0 8px; }}
 h1 small {{ font-weight: normal; color: #5b646d; }}
 #q {{ width: min(420px, 60vw); padding: 6px 10px; font: inherit;
   border: 1px solid #c3cbd2; border-radius: 6px; }}
 .chip {{ font: inherit; font-size: 12.5px; padding: 4px 10px; margin-left: 6px;
   border: 1px solid #c3cbd2; border-radius: 999px; background: #fff;
   cursor: pointer; }}
 .chip.on {{ background: #2e7fae; border-color: #2e7fae; color: #fff; }}
 .chip.on span {{ color: #d6e9f6; }}
 .chip span {{ color: #5b646d; }}
 .hint {{ font-size: 11.5px; color: #6b747c; margin-top: 6px; }}
 .wrap {{ display: flex; align-items: flex-start; gap: 20px; padding: 16px; }}
 nav {{ position: sticky; top: 86px; flex: 0 0 240px; max-height: 80vh;
   overflow-y: auto; font-size: 12.5px; }}
 nav a {{ display: flex; justify-content: space-between; gap: 8px;
   padding: 2px 6px; color: #2b333a; text-decoration: none; border-radius: 4px; }}
 nav a:hover {{ background: #e7ebef; }}
 nav a.cur {{ background: #dce9f6; color: #0b3f6e; font-weight: 600; }}
 nav a span {{ color: #8a939b; }}
 main {{ flex: 1 1 auto; min-width: 0; }}
 section {{ margin: 0 0 22px; }}
 h2 {{ font-size: 13px; text-transform: uppercase; letter-spacing: .07em;
   color: #5b646d; margin: 0 0 8px; padding-bottom: 4px;
   border-bottom: 1px solid #dfe4e8; }}
 .sym {{ background: #fff; border: 1px solid #e1e6ea; border-left: 4px solid #c3cbd2;
   border-radius: 6px; padding: 8px 12px; margin: 0 0 8px;
   /* FLAG: THE HEADER IS STICKY, so an anchor jump lands the card UNDERNEATH it
      and it looks like the link did nothing. This is the room it needs. */
   scroll-margin-top: 104px; }}
 section {{ scroll-margin-top: 104px; }}
 .sym:target {{ border-color: #d99; box-shadow: 0 0 0 3px #f6dede; }}
 /* A jump inside the same screenful moves nothing, so the landing is what has
    to be visible rather than the scroll. */
 .sym.flash {{ animation: flash 1.1s ease-out; }}
 @keyframes flash {{
   from {{ background: #fdf0c8; box-shadow: 0 0 0 4px #f5d98a; }}
   to {{ background: #fff; box-shadow: 0 0 0 4px #fff0; }}
 }}
 .hd {{ display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }}
 .name {{ font-weight: 700; font-family: Consolas, ui-monospace, monospace;
   color: #11181f; text-decoration: none; }}
 .val {{ font-family: Consolas, ui-monospace, monospace; color: #0a6b4e;
   font-weight: 700; }}
 .prov {{ font-size: 11px; text-transform: uppercase; letter-spacing: .05em;
   color: #5b646d; border: 1px solid #d8dde2; border-radius: 999px;
   padding: 0 7px; }}
 .r {{ font-size: 12.5px; color: #39424a; margin-top: 3px; }}
 .r b {{ color: #5b646d; font-weight: 600; }}
 .n {{ font-size: 12.5px; color: #39424a; margin-top: 5px; }}
 code {{ font-family: Consolas, ui-monospace, monospace; }}
 a {{ color: #0b5fa5; }}
 /* FLAG: PROVENANCE IS THE WHOLE POINT OF THE REGISTRY, so it is the one thing
    carried in colour: measured and part are his, derived follows from them,
    nominal is a catalogue figure nobody has put a caliper on. */
 .p-measured {{ border-left-color: #2e9e6b; }}
 .p-part {{ border-left-color: #2e7fae; }}
 .p-derived {{ border-left-color: #b9c0c7; }}
 .p-alias {{ border-left-color: #8d7bb5; }}
 /* PINNED CAME OUT OF A CALCULATION AND THEN STOPPED FOLLOWING IT, which is
    worth seeing at a glance next to a derived one that still does. */
 .p-pinned {{ border-left-color: #c77d3f; }}
 /* A retired symbol is kept for the record only, so it reads as paper. */
 .sym.retired {{ opacity: .62; border-left-color: #9aa3ab;
   border-style: dashed; }}
 .retired-tag {{ font-size: 11px; text-transform: uppercase;
   letter-spacing: .05em; color: #fff; background: #9aa3ab;
   border-radius: 999px; padding: 0 7px; }}
 .p-nominal {{ border-left-color: #d9a406; }}
 .p-OPEN {{ border-left-color: #d64545; }}
 .hide {{ display: none; }}
 /* FLAG: PRESS AND HOLD A SYMBOL LINK TO PEEK AT IT - his, 2026-10-11. Following
    the link answers "what is that?" by throwing away where you were, which on a
    page whose whole point is cross-references is the wrong trade. */
 #peek {{ position: fixed; z-index: 20; max-width: 420px; pointer-events: none;
   background: #fff; border: 1px solid #b9c0c7; border-left: 4px solid #8d7bb5;
   border-radius: 6px; padding: 8px 12px; box-shadow: 0 6px 24px #0003;
   font-size: 12.5px; }}
 #peek .hd {{ margin-bottom: 3px; }}
 #peek[hidden] {{ display: none; }}
 @media (prefers-color-scheme: dark) {{
   body {{ color: #dfe4e8; background: #16191c; }}
   header {{ background: #1c2024f2; border-color: #2c3237; }}
   .sym {{ background: #1c2024; border-color: #2c3237; }}
   @keyframes flash {{
     from {{ background: #3d3621; box-shadow: 0 0 0 4px #6b5b22; }}
     to {{ background: #1c2024; box-shadow: 0 0 0 4px #1c20240; }}
   }}
   nav a {{ color: #c3cbd2; }} nav a:hover {{ background: #252a2f; }}
   nav a.cur {{ background: #1d3450; color: #cfe4fb; }}
   .name {{ color: #eaeef2; }} .val {{ color: #5fd3a3; }}
   .r, .n {{ color: #b4bdc5; }} a {{ color: #6cb6f5; }}
   #q, .chip {{ background: #1c2024; color: inherit; border-color: #39414a; }}
 }}
 @media (max-width: 760px) {{ nav {{ display: none; }} .wrap {{ padding: 10px; }} }}
</style></head><body>
<header>
  <h1>The dimension registry
    <small>&mdash; {len(reg.order)} symbols, generated from registry.toml by
    tools/dims.py html. Registry updated {reg.meta.get("updated", "unknown")}.</small></h1>
  <input id="q" type="search" placeholder="filter by symbol or note&hellip;" autofocus>
  {chips}
  <span id="n" class="chip" style="cursor:default"></span>
  <div class="hint">Chips show <b>only</b> what you pick &mdash; click one to
    isolate it, click more to add, click again to drop. None picked shows
    everything. <b>Press and hold</b> a symbol link to peek at it &mdash;
    letting go leaves you exactly where you were. <b>Ctrl+click</b> goes
    there.</div>
</header>
<div id="peek" hidden></div>
<div class="wrap">
  <nav>{toc}</nav>
  <main>{"".join(cards)}</main>
</div>
<script>
// Filter on the symbol name AND the note, because half of what this file is for
// lives in the notes - searching "acorn" has to find ACORN_NUT_DEPTH and every
// entry that talks about one.
const syms=[...document.querySelectorAll('.sym')], q=document.getElementById('q');
// FLAG: THE CHIPS SELECT, THEY DO NOT EXCLUDE - his, 2026-10-11, off how he
// actually uses the page: hide everything, then turn one back on. Subtractive
// chips make that six clicks and this makes it one. An EMPTY selection means
// show everything, so the same click that isolates a provenance also clears it.
const only=new Set();
let onlyRetired=false;
function apply(){{
  const t=q.value.trim().toLowerCase();
  let n=0;
  for(const s of syms){{
    const hit=(!t||s.dataset.sym.includes(t)||s.dataset.note.includes(t))
            && (only.size===0||only.has(s.dataset.prov))
            && (!onlyRetired||s.dataset.retired==='1');
    s.classList.toggle('hide',!hit);
    if(hit)n++;
  }}
  for(const sec of document.querySelectorAll('section'))
    sec.classList.toggle('hide',!sec.querySelector('.sym:not(.hide)'));
  const pick=[...only].sort();
  if(onlyRetired)pick.push('retired');
  document.getElementById('n').textContent=
    n+' shown'+(pick.length?' · only '+pick.join(', '):'');
}}
q.addEventListener('input',apply);
// addEventListener rather than .onclick, and the counter NAMES what is filtered
// out - so if a click ever appears to do nothing again, the counter says which
// half failed: unchanged text means the handler never ran, changed text with
// nothing hidden means the CSS did not take.
const rchip=document.querySelector('.chip[data-retired]');
if(rchip)rchip.addEventListener('click',()=>{{
  onlyRetired=!onlyRetired;
  rchip.classList.toggle('on',onlyRetired);
  apply();
}});
for(const c of document.querySelectorAll('.chip[data-prov]')){{
  c.addEventListener('click',()=>{{
    const p=c.dataset.prov;
    only.has(p)?only.delete(p):only.add(p);
    for(const o of document.querySelectorAll('.chip[data-prov]'))
      o.classList.toggle('on',only.has(o.dataset.prov));
    apply();
  }});
}}
apply();

// --- the left index follows the right pane ----------------------------
// Scrolling the symbols moves the highlight, and the index scrolls itself so
// the current section stays visible - his, 2026-10-11, and the reason is that
// an index you have to hunt in is not an index.
const links=new Map();
for(const a of document.querySelectorAll('nav a'))
  links.set(a.getAttribute('href').slice(1),a);

function mark(id){{
  if(!id||!links.has(id))return;
  for(const a of links.values())a.classList.remove('cur');
  const a=links.get(id);
  a.classList.add('cur');
  const nav=a.parentElement, r=a.getBoundingClientRect(),
        nr=nav.getBoundingClientRect();
  if(r.top<nr.top||r.bottom>nr.bottom)
    nav.scrollTop+=r.top-nr.top-nr.height/3;
}}

// The section whose top is nearest the top of the viewport and still above it -
// a plain scroll handler rather than IntersectionObserver, because sections here
// are tall enough that several are on screen at once and "the one I am in" is
// the last one I passed.
const secs=[...document.querySelectorAll('section')];
function spy(){{
  let cur=null;
  for(const sec of secs){{
    if(sec.classList.contains('hide'))continue;
    if(sec.getBoundingClientRect().top<=120)cur=sec.id;
  }}
  mark(cur||(secs.find(x=>!x.classList.contains('hide'))||{{}}).id);
}}
addEventListener('scroll',spy,{{passive:true}});
spy();

// Clicking a symbol - or landing on one from a link in a note - moves the index
// with it, which a plain #anchor jump does not do.
//
// FLAG: AND IT CLEARS THE FILTERS IF THE TARGET IS HIDDEN. Isolate one provenance,
// click a link in a note to something of another, and the jump lands on a card
// with display:none - the page does not move and the link looks broken. The
// filter is a view, the link is an intent, and the intent wins.
function land(){{
  const el=document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if(!el||!el.classList.contains('sym'))return;
  if(el.classList.contains('hide')){{
    only.clear(); q.value=''; onlyRetired=false;
    for(const o of document.querySelectorAll('.chip'))
      o.classList.remove('on');
    apply();
    el.scrollIntoView();
  }}
  const sec=el.closest('section');
  if(sec)mark(sec.id);
  el.classList.remove('flash');
  void el.offsetWidth;            // restart the animation on a repeat click
  el.classList.add('flash');
}}
addEventListener('hashchange',land);
if(location.hash)land();

// --- press and hold a symbol link to peek ------------------------------
// FLAG: FOLLOWING A LINK ANSWERS "WHAT IS THAT?" BY LOSING WHERE YOU WERE, and on
// a page that is mostly cross-references that is the wrong trade - his, and he
// is right. Mouse down shows the card, mouse up puts it away, and a plain click
// still navigates for when that IS what you want.
const peek=document.getElementById('peek');

// Is this a link to a SYMBOL CARD? The section index uses #anchors too and must
// go on behaving like an ordinary link - none of what follows applies to it.
function symLink(t){{
  const a=t&&t.closest&&t.closest('a[href^="#"]');
  if(!a)return null;
  const el=document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
  return el&&el.classList.contains('sym')?a:null;
}}

function showPeek(id,x,y){{
  const el=document.getElementById(id);
  if(!el||!el.classList.contains('sym'))return;
  peek.innerHTML=el.innerHTML;
  peek.hidden=false;
  // clamp into the window, and prefer below-right of the cursor
  const w=peek.offsetWidth,h=peek.offsetHeight;
  peek.style.left=Math.max(6,Math.min(x+14,innerWidth-w-8))+'px';
  peek.style.top=(y+18+h>innerHeight?Math.max(6,y-h-12):y+18)+'px';
}}
const hidePeek=()=>{{peek.hidden=true;}};
addEventListener('pointerdown',e=>{{
  const a=symLink(e.target);
  // FLAG: CTRL IS THE ONE THAT GOES THERE. A plain press peeks and the peek dies
  // on release, leaving you exactly where you were - his, 2026-10-11. The first
  // cut navigated on release, which is the opposite of a peek.
  if(!a||e.ctrlKey||e.metaKey)return;
  showPeek(decodeURIComponent(a.getAttribute('href').slice(1)),
           e.clientX,e.clientY);
}});
addEventListener('pointerup',hidePeek);

// BOTH CASES PREVENT THE BROWSER'S OWN NAVIGATION: a plain click would follow
// the anchor and lose your place, and a Ctrl+click would open a NEW TAB, which
// on a page this size is worse than either. So the page navigates itself.
addEventListener('click',e=>{{
  const a=symLink(e.target);
  if(!a)return;
  e.preventDefault();
  hidePeek();
  if(!(e.ctrlKey||e.metaKey))return;          // plain click peeked, nothing else
  const id=decodeURIComponent(a.getAttribute('href').slice(1));
  if(location.hash.slice(1)===id)land();      // already there: just flash it
  else location.hash='#'+id;                  // explicit: do not lean on the
                                              // browser normalising it
}});
addEventListener('pointercancel',hidePeek);
addEventListener('scroll',hidePeek,{{passive:true}});
</script>
</body></html>
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} - {len(reg.order)} symbols in "
          f"{len(order)} sections")
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
    hh = sub.add_parser("html", help="browsable registry page")
    hh.add_argument("-o", "--output")
    hh.set_defaults(fn=cmd_html)
    m = sub.add_parser("md", help="generated markdown table")
    m.add_argument("-o", "--output")
    m.set_defaults(fn=cmd_md)
    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
