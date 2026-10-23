#!/usr/bin/env python3
"""Is anything actually standing on each of the three mount points?

FLAG: WHY THIS EXISTS, AND IT IS THE INVERSE OF THE CLASH CHECK. The
interference check finds solids that overlap and must not. Nothing looked for
the opposite - surfaces that MUST meet and do not - and that is the gap the
front centre leg fell through.

What happened: the bottom skin's front tenon cut was opened out to the skin's
front edge, and the clause that justified it tested the band of skin being
removed against whether it would SHOW ("it is all under the front perimeter
web, so none of it shows"). Nobody asked what that band was BEARING. It was the
skin over the front centre leg's shoulder. Meanwhile SHOULDER_MID went on
computing 864 mm2 from the LEG's own geometry - tabs x strip x ledge band - and
a derived figure cannot notice that the sheet above it was cut away. The two
parts have no dependency between them in the registry, so nothing went stale,
nothing flagged, and the number was quoted as "about 1 MPa, a figure to know
rather than a problem" while in the part it bore on air. It was found by eye at
assembly, after the leg was built.

The information was in the model the whole time: the skin is drawn as a prism
with all three tenon cuts spliced out of its outline, so the hole was there to
be seen. Nothing was asking the question.

🔴 AND IT DOES NOT ASSUME WHICH PART LANDS ON A SHOULDER. The first draft of
this check asked whether the BOTTOM SKIN covered each shoulder, and reported
all three bearing on nothing - because at the two rear corners it is the
perimeter wall's tongue that lands on the ledge, not the skin, which butts the
tongue's inner face. Writing the supported part into the check is the same
mistake one layer up: it tests the answer you expected instead of the question.
So it takes EVERY part whose underside is at the shoulder plane and does not
belong to the post itself, and asks what they cover between them.

    python tools/check-bearing.py

Exit 0 if every mount point bears, 1 if any does not or disagrees with the
registry, 2 if the page is missing. No third-party imports.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = ROOT / "machine" / "drawings" / "Interactive_Model.html"

# Faces are coincident by construction, so the tolerance is for float noise in
# the generator's arithmetic and nothing else.
TOL = 0.05

# A post is "Post, rear left" and its pieces are named off it - "Post, rear
# left, inner strip", "Post, rear left tenon tab". Two words after the comma.
POST = re.compile(r"^Post, [a-z]+ [a-z]+")

# The dark colour make-3d gives a sunk hole or pocket, which it draws as a
# solid so the viewer shows it. Kept in step with HOLE there.
HOLE = 0x22262A

# WHICH REGISTRY SYMBOL CLAIMS A POST'S BEARING AREA, where one does. PRINTED
# BESIDE THE DRAWN FIGURE AND NOT ENFORCED, deliberately: a symbol's area and
# the area the model shows bearing are two different questions, and SHOULDER_MID
# is the standing example - it computes the leg's ledge band, which is still 864
# whatever happens to the sheet above it. Making a disagreement fatal would wedge
# every build on a number already FLAGged as superseded. Making it VISIBLE every
# run is what was missing.
CLAIMED = {
    "Post, front centre": "SHOULDER_MID",
}

# A MOUNT POINT CARRIED BY SOMETHING THE MODEL DOES NOT DRAW, with the reason
# and where it is written down. Same arrangement as ALLOWED in the clash check:
# an exception that is declared and reasoned beats one that is silent, and an
# EMPTY DICT IS THE STATE TO AIM AT - every entry is a part the model is
# missing, so drawing the part is the fix and the entry only stops the check
# crying wolf until then.
BEARS_ELSEWHERE = {}


def load_registry():
    """tools/dims.py, imported for the claimed areas."""
    spec = importlib.util.spec_from_file_location("dims", HERE / "dims.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._load()


def lift_parts(page_text):
    """The PARTS list out of the generated page - the SHIPPED geometry, the
    same source the clash check reads."""
    m = re.search(r"const PARTS=(\[.*?\]), GROUPS=", page_text, re.S)
    if not m:
        raise SystemExit("PARTS is not in the page - the generator's output "
                         "shape changed and this check has to follow it")
    return json.loads(m.group(1))


def footprint(part):
    """A part's plan shape as rings: (outline, holes), in machine x and y.

    A box is its rectangle. An xy prism is its real outline, which is the
    whole point here - the skin's tenon cuts are spliced into that outline and
    a bounding box would claim them back.
    """
    if part.get("t") == "prism" and part.get("pl") == "xy":
        return part["profile"], (part.get("holes") or [])
    x0, y0 = part["p"][0], part["p"][1]
    x1, y1 = part["q"][0], part["q"][1]
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], []


def in_ring(ring, px, py):
    """Crossing number. The outlines here are rectilinear and every test point
    is a cell CENTRE, so a point never lands on an edge."""
    c = False
    n = len(ring)
    for i in range(n):
        ax, ay = ring[i]
        bx, by = ring[(i + 1) % n]
        if (ay > py) != (by > py):
            if ax + (py - ay) * (bx - ax) / (by - ay) > px:
                c = not c
    return c


def covers(shapes, px, py):
    return any(in_ring(o, px, py) and not any(in_ring(h, px, py) for h in hs)
               for o, hs in shapes)


def walk(rect, shapes, blockers, want_cover):
    """Area of `rect` that is clear of `blockers`, and either covered by one of
    `shapes` or not, as asked.

    EXACT RATHER THAN SAMPLED, because every outline here is rectilinear:
    cutting the rectangle on every x and y that appears in any shape or blocker
    leaves cells that are each wholly in or wholly out, so the cell centres
    decide it with no quantisation at all.
    """
    x0, y0, x1, y1 = rect
    xs, ys = {x0, x1}, {y0, y1}
    rings = [r for o, hs in shapes for r in [o] + list(hs)]
    rings += [[[bx0, by0], [bx1, by0], [bx1, by1], [bx0, by1]]
              for bx0, by0, bx1, by1 in blockers]
    for ring in rings:
        for px, py in ring:
            if x0 < px < x1:
                xs.add(px)
            if y0 < py < y1:
                ys.add(py)
    xs, ys = sorted(xs), sorted(ys)

    area = 0.0
    for i in range(len(xs) - 1):
        cx = (xs[i] + xs[i + 1]) / 2
        for j in range(len(ys) - 1):
            cy = (ys[j] + ys[j + 1]) / 2
            if any(bx0 <= cx <= bx1 and by0 <= cy <= by1
                   for bx0, by0, bx1, by1 in blockers):
                continue
            if want_cover and not covers(shapes, cx, cy):
                continue
            area += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return area


def post_of(name):
    m = POST.match(name)
    return m.group(0) if m else None


def main():
    if not PAGE.exists():
        print(f"{PAGE.name} is not built - run tools/make-3d.py first",
              file=sys.stderr)
        return 2
    parts = lift_parts(PAGE.read_text(encoding="utf-8"))

    posts = sorted({post_of(p["n"]) for p in parts if post_of(p["n"])})
    if not posts:
        print("no posts in the model - the naming changed and this check has "
              "to follow it", file=sys.stderr)
        return 2

    # THE SHOULDER PLANE IS PER POST AND COMES OFF THE PARTS, not off the
    # registry: it is the surface the question is about, and a figure fetched
    # from elsewhere could disagree with what is drawn. The tenon tabs STAND on
    # the shoulder, so a post's plane is where ITS OWN tabs' undersides are -
    # and every mount point has one by definition, because a post without a tab
    # is not a mount point.
    #
    # 🔴 ONE PLANE ACROSS THE MODEL IS WRONG, AND IT WAS WRONG HERE. The front
    # centre leg's ledges are cut SHOULDER_MID_DROP lower than the other two,
    # so a single plane taken over all the tabs missed both rear posts and
    # reported them bearing on nothing. A figure that is shared only because
    # nothing has differed yet is not a shared figure.
    bad = []
    reg = None
    for post in posts:
        tabs = [p for p in parts
                if post_of(p["n"]) == post and "tenon tab" in p["n"]]
        if not tabs:
            print(f"  {post}: no tenon tab, so it is not a mount point\n")
            continue
        plane = min(p["p"][2] for p in tabs)

        # 🔴 A VOID IS NOT SUPPORT. Holes and pockets are drawn as solids in
        # the dark HOLE colour so they read in the viewer - the sand ports
        # through the bottom skin are two dozen of them at exactly the rear
        # posts' plane. Counting one as something a post bears on is the same
        # error this check exists to find, arriving from the other side.
        landing = [p for p in parts
                   if not post_of(p["n"]) and p.get("c") != HOLE
                   and abs(p["p"][2] - plane) <= TOL]

        rects, blockers = [], []
        for p in parts:
            if p.get("t") != "box" or post_of(p["n"]) != post:
                continue
            r = (p["p"][0], p["p"][1], p["q"][0], p["q"][1])
            if abs(p["q"][2] - plane) <= TOL:
                rects.append(r)              # a face AT the shoulder
            elif abs(p["p"][2] - plane) <= TOL:
                blockers.append(r)           # a tab or spacer standing ON it
        if not rects:
            print(f"  {post}: nothing reaches the shoulder plane\n")
            bad.append((post, "nothing reaches the shoulder plane"))
            continue

        shapes = [footprint(p) for p in landing]
        available = sum(walk(r, [], blockers, False) for r in rects)
        bears = sum(walk(r, shapes, blockers, True) for r in rects)
        pct = 100 * bears / available if available else 0.0
        on = sorted({p["n"] for p in landing
                     for r in rects if walk(r, [footprint(p)], blockers, True) > TOL})

        print(f"  {post}   shoulder plane z = {plane:g}")
        print(f"      shoulder drawn   {available:9.1f} mm2")
        print(f"      borne on         {bears:9.1f} mm2   ({pct:.0f}%)")
        if on:
            print(f"      carried by       {', '.join(on)}")

        excuse = BEARS_ELSEWHERE.get(post)
        if bears <= TOL:
            if excuse:
                print(f"      BEARS ELSEWHERE: {excuse}")
            else:
                print("      🔴 BEARS ON NOTHING")
                bad.append((post, "nothing in the model lands on this shoulder"))
        claim = CLAIMED.get(post)
        if claim:
            reg = reg or load_registry()
            want = reg.value(claim)
            print(f"      {claim} claims  {want:9.1f} mm2")
            if abs(want - bears) > 1.0:
                print(f"      NOT FATAL, BUT READ IT: the symbol computes the "
                      f"LEG's ledge band and the model shows what lands on it. "
                      f"They differ by {abs(want - bears):.1f} mm2.")
        print()

    if bad:
        print("BEARING CHECK FAILED")
        for post, why in bad:
            print(f"  {post}: {why}")
        return 1
    print("Every mount point bears, or says in writing what carries it instead.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
