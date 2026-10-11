#!/usr/bin/env python3
"""The fastener schedule, from dimensions/fasteners.toml and the registry.

IT ANSWERS ONE QUESTION FIRST: how many joints have no length recorded. That was
asked on 2026-10-11 and could not be answered, because nothing listed the joints
- the registry was full of BOLT_* POSITIONS and had almost no LENGTHS.

The length is the figure that gets guessed at the bench, and guessing it has
already gone wrong twice here: an M8 x 25 that engaged 4 mm because a T-nut's
thread sits in the BOTTOM of a 25 skin, and a fin bolt that had to be 16 not 15.
Both were caught by working the grip stack by hand. This does that arithmetic.

    python tools/make-fasteners.py          # report + write the page
    python tools/make-fasteners.py --gaps   # just the joints missing a length

Writes machine/drawings/fasteners.html. No third-party imports.
"""
import argparse
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dims import Registry                                    # noqa: E402

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "dimensions" / "fasteners.toml"
OUT = HERE.parent / "machine" / "drawings" / "fasteners.html"

# What each destination gives you, and how far a bolt may safely run past it.
# 🔴 THESE ARE NOT ENGAGEMENT FIGURES AND MUST NOT BE READ AS ONE. They say
# whether running long is HARMLESS or DAMAGING, which is the half of the
# question a length table usually omits:
#   tapped - into a tapped hole in a part; running long may protrude somewhere
#   t-nut  - a through-threaded T-nut; a long bolt simply sticks out the back
#   nut    - a plain nut on the far side; length only has to reach
#   bore   - into an extrusion's lengthwise corner bore; deep, forgiving
#   wood   - a screw into timber
LONG_IS = {
    "tapped": "may protrude - check what is behind it",
    "t-nut": "harmless, the T-nut is through-threaded",
    "nut": "harmless, it just stands proud of the nut",
    "bore": "harmless, the bore is deep",
    "wood": "n/a",
}


def grip_of(j, v):
    """The stack a bolt crosses before it meets thread, from registry symbols."""
    syms = j.get("grip")
    if not syms:
        return None, None
    total = 0.0
    parts = []
    for s in syms:
        if s not in v:
            return None, f"unknown symbol {s}"
        total += v[s]
        parts.append(f"{s} {v[s]:g}")
    return total, " + ".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gaps", action="store_true",
                    help="list only the joints with no length recorded")
    a = ap.parse_args()

    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        return 2
    v = {s: reg.value(s) for s in reg.order}

    joints = tomllib.loads(SRC.read_text(encoding="utf-8"))["joint"]

    rows = []
    for j in joints:
        grip, grip_txt = grip_of(j, v)
        L = j.get("length")
        eng = (L - grip) if (L is not None and grip is not None) else None
        rows.append(dict(j, grip=grip, grip_txt=grip_txt, eng=eng))

    missing = [r for r in rows if r.get("length") is None]
    nosize = [r for r in rows if "size" not in r]
    total_pcs = sum(r.get("count", 0) for r in rows)

    if a.gaps:
        print(f"{len(missing)} of {len(rows)} joints have NO LENGTH recorded\n")
        for r in missing:
            sz = f"M{r['size']}" if "size" in r else "size unknown"
            print(f"  {r['id']:24s} {sz:14s} x{r.get('count','?'):<4} {r['what']}")
            if r.get("grip_txt"):
                print(f"  {'':24s} grip {r['grip']:g} = {r['grip_txt']}")
        return 0

    print("FASTENER SCHEDULE\n")
    print(f"{'joint':24s} {'size':6s} {'off':>4s} {'len':>6s} {'grip':>7s} {'eng':>7s}")
    for r in rows:
        sz = f"M{r['size']}" if "size" in r else "?"
        L = f"{r['length']:g}" if r.get("length") is not None else "--"
        g = f"{r['grip']:g}" if r.get("grip") is not None else ""
        e = f"{r['eng']:g}" if r.get("eng") is not None else ""
        print(f"  {r['id']:22s} {sz:6s} {r.get('count','?'):>4} {L:>6s} {g:>7s} {e:>7s}")

    # 🔴 ENGAGEMENT IS THE CHECK, and it caught two errors in the joints file the
    # first time it ran. Both were the same mistake: a TAPPED part listed in the
    # GRIP as well, so the bolt was counted as crossing the very thing it threads
    # into and engagement came out 0. A length table that cannot do this
    # arithmetic is just a list of numbers somebody typed.
    thin = [r for r in rows
            if r.get("eng") is not None and r["eng"] < r.get("size", 8)]
    if thin:
        print("\n  \U0001F534 ENGAGEMENT UNDER ONE DIAMETER - check these:")
        for r in thin:
            tail = ("   (zero or negative - is a tapped part listed in the grip?)"
                    if r["eng"] <= 0 else "")
            print(f"     {r['id']:24s} engages {r['eng']:g} "
                  f"on M{r.get('size', '?')}{tail}")

    # T-NUTS ARE A SEPARATE BUY AND THE SAME COUNT AS THE BOLTS. Forgetting
    # them is a trip to the supplier, and nothing else in the repo totals them -
    # his 2026-10-11 reminder that 102 rail bolts also means 102 T-nuts.
    tnuts = {}
    for r in rows:
        if r.get("into") == "t-nut" and "size" in r:
            tnuts[r["size"]] = tnuts.get(r["size"], 0) + r.get("count", 0)
    if tnuts:
        print("\n  T-nuts needed, same count as the bolts:")
        for sz in sorted(tnuts):
            print(f"     M{sz}: {tnuts[sz]}")

    # THE BUY LIST, by size and length. The schedule is read joint by joint at
    # the bench and size by size at the counter, and those are different sorts.
    buy = {}
    for r in rows:
        if "size" in r and r.get("length") is not None:
            buy[(r["size"], r["length"])] = (
                buy.get((r["size"], r["length"]), 0) + r.get("count", 0))
    print("\n  Bolts to buy:")
    for (sz, L) in sorted(buy):
        print(f"     M{sz} x {L:g}: {buy[(sz, L)]}")

    print(f"\n  {len(rows)} joints, {total_pcs} pieces")
    print(f"  🔴 {len(missing)} joints have NO LENGTH recorded")
    if nosize:
        print(f"  ⚠️  {len(nosize)} have no SIZE either: "
              + ", ".join(r['id'] for r in nosize))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows, missing, total_pcs, tnuts, buy),
                   encoding="utf-8")
    print("\nwrote", OUT.relative_to(HERE.parent))
    return 0


def render(rows, missing, total_pcs, tnuts, buy):
    bl = [f"M{sz} &times; {L:g}" for (sz, L) in sorted(buy)]
    bn = [buy[k] for k in sorted(buy)]
    tl = [f"M{sz} T-nut" for sz in sorted(tnuts)]
    tn = [tnuts[k] for k in sorted(tnuts)]
    pair = []
    for i in range(max(len(bl), len(tl))):
        a = f"<td>{bl[i]}</td><td class=n>{bn[i]}</td>" if i < len(bl) else "<td></td><td></td>"
        b = f"<td>{tl[i]}</td><td class=n>{tn[i]}</td>" if i < len(tl) else "<td></td><td></td>"
        pair.append(f"<tr>{a}{b}</tr>")
    rowspair = "".join(pair)
    tr = []
    for r in rows:
        sz = f"M{r['size']}" if "size" in r else '<b class="bad">?</b>'
        L = (f"<b>{r['length']:g}</b>" if r.get("length") is not None
             else '<b class="bad">not recorded</b>')
        g = f"{r['grip']:g}" if r.get("grip") is not None else "&mdash;"
        e = f"{r['eng']:g}" if r.get("eng") is not None else "&mdash;"
        tr.append(
            f"<tr><td>{r['what']}<br><span class=s>{r.get('note','')}</span></td>"
            f"<td class=n>{sz}</td><td class=n>{r.get('count','?')}</td>"
            f"<td class=n>{L}</td><td class=n>{g}</td><td class=n>{e}</td>"
            f"<td>{LONG_IS.get(r.get('into',''), '')}</td></tr>")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>CNCBuild &mdash; Fastener Schedule</title>
<style>
 @page {{ size: letter landscape; margin: 12mm; }}
 body {{ font: 9.5pt "Segoe UI", sans-serif; color: #111; }}
 h1 {{ font-size: 14pt; margin: 0 0 2mm; }}
 table {{ border-collapse: collapse; width: 100%; margin: 3mm 0; }}
 td, th {{ border: 1px solid #ccc; padding: 1.2mm 2mm; vertical-align: top; }}
 th {{ background: #eee; text-align: left; }}
 td.n {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
 .bad {{ color: #a00; }}
 .s {{ color: #666; font-size: 8pt; }}
 .note {{ background: #fff8e1; border-left: 3px solid #e0a800; padding: 2mm 3mm; }}
</style></head><body>
<h1>Fastener schedule</h1>
<p>{len(rows)} joints, {total_pcs} pieces.
<b class="bad">{len(missing)} joints have no length recorded.</b></p>

<div class="note"><b>Grip is what the bolt crosses before it meets thread</b>, summed
from registry symbols &mdash; so it moves when they do. <b>Engagement is length
minus grip.</b> A blank grip means the stack is not in the file yet; nothing here
is inferred, because the two length errors this repo has already made were both
inferences that read as facts.</div>

<table>
<tr><th>Joint</th><th>Size</th><th>Off</th><th>Length</th><th>Grip</th>
<th>Engages</th><th>If it runs long</th></tr>
{''.join(tr)}
</table>

<h2>What to buy</h2>
<p>🔴 <b>T-nuts are a separate line and the same count as the bolts.</b> Nothing
else in the repo totals them, and forgetting them is a trip to the supplier.
⚠️ These totals cover only the joints with a count recorded &mdash; the Z rails
are a different kit and their hole count is not known yet.</p>

<table style="width:auto">
<tr><th>Bolts</th><th class=n>Off</th><th>T-nuts</th><th class=n>Off</th></tr>
{rowspair}
</table>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
