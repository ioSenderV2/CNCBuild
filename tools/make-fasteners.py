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
import re
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
        # 🔴 A T-NUT GIVES TNUT_THREAD_M8 WHATEVER THE BOLT IS. Reporting
        # length-minus-grip for one overstates the engagement badly - a 50 bolt
        # read as 24.6 engaged when the nut can only hold 6, with the rest
        # standing through into the slot. So cap it, and carry the remainder as
        # `past` so a bolt running deep into a slot is visible rather than
        # flattered into looking well engaged.
        past = None
        if eng is not None and j.get("into") == "t-nut":
            # A PRONGED T-NUT IN PLYWOOD IS NOT A SLIDE-IN EXTRUSION T-NUT.
            # The fin angle's give 10, the extrusion's give 6, so a joint
            # may name its own symbol rather than take the default.
            cap = v.get(j.get("tnut_thread", "TNUT_THREAD_M8"), 6.0)
            if eng > cap:
                past, eng = eng - cap, cap
        rows.append(dict(j, grip=grip, grip_txt=grip_txt, eng=eng, past=past))

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
        pa = f"  +{r['past']:g} past" if r.get("past") else ""
        print(f"  {r['id']:22s} {sz:6s} {r.get('count','?'):>4} {L:>6s} "
              f"{g:>7s} {e:>7s}{pa}")

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

    # THE BUY LIST IS GROUPED BY THREAD SIZE - his call 2026-10-11, and it is
    # how hardware is actually bought: you stand at one drawer for M5 and
    # another for M8, not at a list sorted by joint. Bolts, T-nuts, washers and
    # nuts for a size all sit together, because forgetting the T-nuts is a
    # second trip and nothing else in the repo totals them.
    buy = {}

    def add(size, item, n):
        buy.setdefault(size, {})
        buy[size][item] = buy[size].get(item, 0) + n

    for r in rows:
        n = r.get("count", 0)
        if "size" not in r:
            continue
        sz = r["size"]
        if r.get("length") is not None:
            add(sz, f"bolt M{sz} x {r['length']:g}", n)
        if r.get("into") == "t-nut":
            add(sz, f"T-nut M{sz}", n)
        for e in r.get("extras", []):
            m = re.match(r'M(\d+)\s+(.*)', e)
            add(int(m.group(1)) if m else sz, m.group(2) if m else e, n)

    print("\n  WHAT TO BUY, by thread size")
    for sz in sorted(buy):
        print(f"\n   --- M{sz} ---")
        for item in sorted(buy[sz], key=lambda i: (not i.startswith("bolt"), i)):
            print(f"      {item:24s} {buy[sz][item]:4d}")

    print(f"\n  {len(rows)} joints, {total_pcs} pieces")
    print(f"  🔴 {len(missing)} joints have NO LENGTH recorded")
    if nosize:
        print(f"  ⚠️  {len(nosize)} have no SIZE either: "
              + ", ".join(r['id'] for r in nosize))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows, missing, total_pcs, buy),
                   encoding="utf-8")
    print("\nwrote", OUT.relative_to(HERE.parent))
    return 0


def render(rows, missing, total_pcs, buy):
    tables = []
    for sz in sorted(buy):
        rws = "".join(
            f"<tr><td>{i}</td><td class=n>{buy[sz][i]}</td></tr>"
            for i in sorted(buy[sz], key=lambda i: (not i.startswith("bolt"), i)))
        tables.append(
            f'<div class="buy"><h3>M{sz}</h3><table>'
            f"<tr><th>Item</th><th class=n>Off</th></tr>{rws}</table></div>")
    buytables = "".join(tables)
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
 .buys {{ display: flex; gap: 8mm; flex-wrap: wrap; align-items: flex-start; }}
 .buy table {{ width: auto; }}
 .buy h3 {{ font-size: 11pt; margin: 2mm 0 1mm; }}
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

<div class="buys">{buytables}</div>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
