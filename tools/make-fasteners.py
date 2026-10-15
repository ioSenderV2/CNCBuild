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
# FLAG: THESE ARE NOT ENGAGEMENT FIGURES AND MUST NOT BE READ AS ONE. They say
# whether running long is HARMLESS or DAMAGING, which is the half of the
# question a length table usually omits:
#   tapped - into a tapped hole in a part; running long may protrude somewhere
#   t-nut  - a through-threaded T-nut; a long bolt simply sticks out the back
#   nut    - a plain nut on the far side; length only has to reach
#   bore   - into an extrusion's lengthwise corner bore; deep, forgiving
#   wood   - a screw into timber
#   acorn  - a CLOSED nut; past its depth the bolt lands on the dome
LONG_IS = {
    "tapped": "may protrude - check what is behind it",
    "t-nut": "harmless, the T-nut is through-threaded",
    "nut": "harmless, it just stands proud of the nut",
    "bore": "harmless, the bore is deep",
    "wood": "n/a",
    "acorn": "DAMAGING - it bottoms on the dome and never clamps",
}


# THE SECOND VIEW: BY WHAT YOU ARE BUILDING, not by what you are buying - his
# list, 2026-10-11, and this is the order he gave it in. The buy list answers
# "what do I order"; this answers "what do I need in front of me to assemble
# ONE thing", which is the question you have at the bench with a sub-assembly
# on the mat.
#
# A joint names its own share of each group in `groups`, as [name, count]
# pairs, because a joint usually spans two sides - the fourteen side plate
# bolts are seven on Y1 and seven on Y2. FLAG: THE PAIRS DO NOT HAVE TO SUM TO THE
# JOINT'S COUNT. What is left over is reported as unassigned, so a joint that
# belongs partly to something he has not named stays VISIBLE rather than being
# forced into the nearest group - which is how a wrong assignment would get
# into a shop sheet and be read as settled.
GROUPS = [
    "Interposer/stepper assembly/BF12 for X",
    "Interposer/stepper assembly/BF12 for Y1",
    "Interposer/stepper assembly/BF12 for Y2",
    "X inside joiner plate",
    "Y1 inside joiner plate",
    "Y2 inside joiner plate",
    "Y1 Side Plate",
    "Y2 Side Plate",
    "Backplate",
    "Y1 Front fin",
    "Y2 Front fin",
    "Left X endplate",
    "Right X endplate",
    "X carriage plate",
    "Z plate",
]


# A TOTAL OF WHAT, is the question a single number cannot answer here. A joint
# of 42 M8 bolts is 42 bolts AND 42 T-nuts, so one figure for "M8 fasteners"
# either double-counts the bolts or loses the nuts - and the T-nuts are the line
# that gets forgotten. So the totals carry the four kinds separately and sum
# them, and every item in the buy list sorts into exactly one of them.
KINDS = ("bolt", "t-nut", "washer", "nut")


def kind_of(item):
    low = item.lower()
    if low.startswith("bolt"):
        return "bolt"
    if low.startswith("t-nut"):
        return "t-nut"
    if "washer" in low:
        return "washer"
    return "nut"      # acorn nuts, and anything else named in `extras`


def kinds(items):
    """{bolt/t-nut/washer/nut: n, all: n} for one size's buy list."""
    out = {k: 0 for k in KINDS}
    for item, n in items.items():
        out[kind_of(item)] += n
    out["all"] = sum(out[k] for k in KINDS)
    return out


def by_group(rows):
    """{group: [(row, count), ...]}, plus what each joint left unassigned."""
    out = {g: [] for g in GROUPS}
    loose = []
    for r in rows:
        n = r.get("count", 0)
        placed = 0
        for g, c in r.get("groups", []):
            # FLAG: ONE T-NUT PER BOLT, ON THE SAME LINE AS THE BOLT - his,
            # 2026-10-11. The buy list totals them for the order; what this view
            # has to answer is what goes on the mat for ONE assembly, and a
            # T-slot bolt without its nut is a trip back to the drawer.
            if g not in out:
                out.setdefault(g, [])     # an unknown name must still show up
            out[g].append((r, c))
            placed += c
        if placed > n:
            print(f"  \U0001F534 {r['id']}: groups sum to {placed}, "
                  f"more than its count of {n}", file=sys.stderr)
        if placed < n:
            loose.append((r, n - placed))
    return out, loose


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
        # FLAG: A T-NUT GIVES TNUT_THREAD_M8 WHATEVER THE BOLT IS. Reporting
        # length-minus-grip for one overstates the engagement badly - a 50 bolt
        # read as 24.6 engaged when the nut can only hold 6, with the rest
        # standing through into the slot. So cap it, and carry the remainder as
        # `past` so a bolt running deep into a slot is visible rather than
        # flattered into looking well engaged.
        past = None
        # FLAG: AN ACORN NUT IS THE ONE DESTINATION WHERE RUNNING LONG IS FATAL.
        # It gives ACORN_NUT_THREAD of thread and will swallow ACORN_NUT_DEPTH
        # of bolt; a bolt that wants more than the depth lands on the closed
        # dome and the joint NEVER CLAMPS, however hard the nut is turned. Both
        # figures are his, measured off two brands in hand on 2026-10-11 - the
        # question Sheet 7's footnote 7.9 asked. Engagement is capped the same
        # way a T-nut's is, and `over` carries what will not fit.
        over = None
        if eng is not None and j.get("into") == "acorn":
            depth = v.get("ACORN_NUT_DEPTH")
            thread = v.get("ACORN_NUT_THREAD", eng)
            if depth is not None and eng > depth:
                over = eng - depth
            eng = min(eng, thread)
        if eng is not None and j.get("into") == "t-nut":
            # A PRONGED T-NUT IN PLYWOOD IS NOT A SLIDE-IN EXTRUSION T-NUT.
            # The fin angle's give 10, the extrusion's give 6, so a joint
            # may name its own symbol rather than take the default.
            cap = v.get(j.get("tnut_thread", "TNUT_THREAD_M8"), 6.0)
            if eng > cap:
                past, eng = eng - cap, cap
        rows.append(dict(j, grip=grip, grip_txt=grip_txt, eng=eng, past=past,
                         over=over))

    # A joint at count 0 is RETIRED - kept in the schedule so it does not look
    # forgotten, but it has no size or length to be missing and reporting it as
    # a gap is noise that makes the real gaps harder to see.
    live = [r for r in rows if r.get("count", 0) > 0]
    missing = [r for r in live if r.get("length") is None]
    nosize = [r for r in live if "size" not in r]
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
    print(f"{'joint':24s} {'size':6s} {'off':>4s} {'len':>6s} {'head':18s} "
          f"{'grip':>7s} {'eng':>7s}")
    for r in rows:
        sz = f"M{r['size']}" if "size" in r else "?"
        L = f"{r['length']:g}" if r.get("length") is not None else "--"
        g = f"{r['grip']:g}" if r.get("grip") is not None else ""
        e = f"{r['eng']:g}" if r.get("eng") is not None else ""
        pa = f"  +{r['past']:g} past" if r.get("past") else ""
        print(f"  {r['id']:22s} {sz:6s} {r.get('count','?'):>4} {L:>6s} "
              f"{r.get('head','?'):18s} {g:>7s} {e:>7s}{pa}")

    # FLAG: ENGAGEMENT IS THE CHECK, and it caught two errors in the joints file the
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

    # FLAG: BOTTOMING IS A DIFFERENT FAULT FROM THIN ENGAGEMENT and gets its own
    # list: a thin joint holds less than you wanted, a bottomed one holds
    # NOTHING. It is also the quiet one - the nut spins up tight against the
    # dome and feels exactly like a joint that is clamped.
    deep = [r for r in rows if r.get("over")]
    if deep:
        print("\n  \U0001F534 BOTTOMS OUT IN THE ACORN NUT - the bolt is too long:")
        for r in deep:
            print(f"     {r['id']:24s} wants {r['length'] - r['grip']:g} of "
                  f"nut, it takes {v['ACORN_NUT_DEPTH']:g} - "
                  f"{r['over']:g} too long")

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
            # FLAG: THE HEAD IS PART OF THE PART, so it belongs on the line you
            # order from - his spec, 2026-10-11. An M8 x 10 in normal flange and
            # an M8 x 10 in low profile are different bolts, and totalling them
            # together is how one of the two never gets bought.
            head = r.get("head")
            add(sz, f"bolt M{sz} x {r['length']:g}"
                    + (f", {head}" if head else " (HEAD NOT RECORDED)"), n)
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
        k = kinds(buy[sz])
        print(f"      {'M%d, ALL PIECES' % sz:24s} {k['all']:4d}"
              f"   ({k['bolt']} bolts, {k['t-nut']} T-nuts, "
              f"{k['washer']} washers, {k['nut']} nuts)")

    print("\n  FASTENER TOTALS, by thread size")
    print(f"      {'size':6s} {'bolts':>6s} {'T-nuts':>7s} {'washers':>8s} "
          f"{'nuts':>5s} {'all':>6s}")
    grand = {k: 0 for k in KINDS + ("all",)}
    for sz in sorted(buy):
        k = kinds(buy[sz])
        for n in grand:
            grand[n] += k[n]
        print(f"      {'M%d' % sz:6s} {k['bolt']:>6d} {k['t-nut']:>7d} "
              f"{k['washer']:>8d} {k['nut']:>5d} {k['all']:>6d}")
    print(f"      {'ALL':6s} {grand['bolt']:>6d} {grand['t-nut']:>7d} "
          f"{grand['washer']:>8d} {grand['nut']:>5d} {grand['all']:>6d}")
    if nosize:
        extra = sum(r.get("count", 0) for r in nosize)
        print(f"      OPEN: {extra} more pieces have NO SIZE and are not in the "
              f"totals: " + ", ".join(r['id'] for r in nosize))

    groups, loose = by_group(rows)
    print("\n  BY FUNCTION GROUP - what to have in front of you for one assembly")
    for g in [x for x in GROUPS if groups.get(x)] + \
             [x for x in groups if x not in GROUPS]:
        print(f"\n   --- {g} ---")
        for r, c in groups[g]:
            L = f"M{r['size']} x {r['length']:g}" if r.get("length") else "?"
            print(f"      {L:14s} {c:>4}   {r['what']}")
            if r.get("into") == "t-nut":
                print(f"      {'T-nut M%d' % r['size']:14s} {c:>4}   "
                      f"for the line above")
    if loose:
        print("\n  OPEN: NOT IN ANY GROUP - these have no home in the list yet:")
        for r, c in loose:
            print(f"      {r['id']:24s} {c:>4} of {r.get('count','?')}")

    print(f"\n  {len(rows)} joints, {total_pcs} pieces")
    print(f"  FLAG: {len(missing)} joints have NO LENGTH recorded")
    if nosize:
        print(f"  OPEN: {len(nosize)} have no SIZE either: "
              + ", ".join(r['id'] for r in nosize))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows, missing, total_pcs, buy, groups, loose, nosize),
                   encoding="utf-8")
    print("\nwrote", OUT.relative_to(HERE.parent))
    return 0


def render(rows, missing, total_pcs, buy, groups, loose, nosize):
    # One card per function group, in his order, each one a pick list for a
    # single sub-assembly. Same data as the schedule above it, cut the other way.
    cards = []
    for g in [x for x in GROUPS if groups.get(x)] + \
             [x for x in groups if x not in GROUPS]:
        rws = "".join(
            (f"<tr><td>{('M%d x %g' % (r['size'], r['length'])) if r.get('length') else '?'}"
             f"{(', ' + r['head']) if r.get('head') else ''}"
             f"</td><td class=n>{c}</td><td>{r['what']}</td></tr>"
             + (f"<tr><td>T-nut M{r['size']}</td><td class=n>{c}</td>"
                f"<td class=s>one per bolt, for the line above</td></tr>"
                if r.get("into") == "t-nut" else ""))
            for r, c in groups[g])
        n = sum(c for _, c in groups[g])
        cards.append(
            f'<div class="buy"><h3>{g}</h3><table>'
            f"<tr><th>Bolt</th><th class=n>Qty</th><th>Joint</th></tr>{rws}"
            f'<tr><td><b>bolts</b></td><td class=n><b>{n}</b></td>'
            f'<td class=s>T-nuts are the lines above, not counted here</td></tr>'
            f"</table></div>")
    looserows = "".join(
        f"<tr><td>{r['id']}</td><td class=n>{c} of {r.get('count','?')}</td>"
        f"<td>{r['what']}</td></tr>" for r, c in loose)
    grouped = (
        '<h2>By function group</h2><p>What to have in front of you to build '
        '<b>one</b> sub-assembly. Same bolts as the schedule above, cut the '
        'other way.</p>'
        f'<div class="buys">{"".join(cards)}</div>'
        + (f'<div class="note"><b>Not in any group yet.</b> These are not '
           f'missing from the schedule - they are in it, and they have no home '
           f'in the group list. Shown rather than filed under the nearest '
           f'plausible heading.<table><tr><th>Joint</th><th class=n>Qty</th>'
           f"<th>What</th></tr>{looserows}</table></div>" if loose else ""))

    tables = []
    for sz in sorted(buy):
        rws = "".join(
            f"<tr><td>{i}</td><td class=n>{buy[sz][i]}</td></tr>"
            for i in sorted(buy[sz], key=lambda i: (not i.startswith("bolt"), i)))
        k = kinds(buy[sz])
        rws += (f'<tr class="tot"><td><b>M{sz}, all pieces</b></td>'
                f'<td class=n><b>{k["all"]}</b></td></tr>')
        tables.append(
            f'<div class="buy"><h3>M{sz}</h3><table>'
            f"<tr><th>Item</th><th class=n>Qty</th></tr>{rws}</table></div>")
    buytables = "".join(tables)

    # THE SUMMARY IS THE WHOLE ORDER ON ONE LINE PER SIZE. The per-size tables
    # above are what you tick off at the drawer; this is what you check a
    # delivery against, and the column that matters is the T-nut one.
    srows = []
    grand = {x: 0 for x in KINDS + ("all",)}
    for sz in sorted(buy):
        k = kinds(buy[sz])
        for n in grand:
            grand[n] += k[n]
        srows.append(f"<tr><td><b>M{sz}</b></td>"
                     + "".join(f"<td class=n>{k[x]}</td>" for x in KINDS)
                     + f"<td class=n><b>{k['all']}</b></td></tr>")
    srows.append('<tr class="tot"><td><b>COMBINED</b></td>'
                 + "".join(f"<td class=n><b>{grand[x]}</b></td>" for x in KINDS)
                 + f"<td class=n><b>{grand['all']}</b></td></tr>")
    nosize_pcs = sum(r.get("count", 0) for r in nosize)
    summary = (
        '<h3>Totals by thread size</h3>'
        '<table style="width:auto">'
        '<tr><th>Size</th><th class=n>Bolts</th><th class=n>T-nuts</th>'
        '<th class=n>Washers</th><th class=n>Nuts</th><th class=n>All pieces</th></tr>'
        + "".join(srows) + '</table>'
        + (f'<p class=s>OPEN: a further <b>{nosize_pcs}</b> pieces have no size '
           f'recorded and are in none of these figures &mdash; '
           + ", ".join(r['what'] for r in nosize) + '.</p>' if nosize else ''))
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
            f"<td class=n>{L}</td><td>{r.get('head') or 'not recorded'}</td>"
            f"<td class=n>{g}</td><td class=n>{e}</td>"
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
 tr.tot td {{ background: #f2f2f2; border-top: 1.4px solid #111; }}
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
<tr><th>Joint</th><th>Size</th><th>Qty</th><th>Length</th><th>Head</th><th>Grip</th>
<th>Engages</th><th>If it runs long</th></tr>
{''.join(tr)}
</table>

<h2>What to buy</h2>
<p>FLAG: <b>T-nuts are a separate line and the same count as the bolts.</b> Nothing
else in the repo totals them, and forgetting them is a trip to the supplier.
OPEN: These totals cover only the joints with a count recorded &mdash; the Z rails
are a different kit and their hole count is not known yet.</p>

<div class="buys">{buytables}</div>

{summary}

{grouped}
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
