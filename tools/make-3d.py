#!/usr/bin/env python3
"""Generate machine/drawings/Interactive_Model.html from the dimension registry.

Every box in the model is placed from registry values, not from numbers typed
here. That is the whole point: if a dimension moves and a part stops fitting,
the model shows it as a visible gap or overlap rather than hiding it. Re-run
this after any registry change.

    python tools/make-3d.py

Where a placement could NOT be derived, it is listed in ASSUMPTIONS below and
printed on the page itself, so nobody mistakes a guess for a dimension.
"""
from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dims import Registry  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "machine" / "drawings" / "Interactive_Model.html"
VENDOR = ROOT / "machine" / "drawings" / "vendor" / "three.min.js"

# ---------------------------------------------------------------- the frame
#
#   X  across the machine, 0 at the rear plate's LEFT end  (= outer left face)
#   Y  fore-aft,           0 at the torsion box's BACK edge, +Y forward
#   Z  up,                 0 at the torsion box's TOP SKIN
#
# Three.js is Y-up, so the writer swaps: three(x, z, y).

ASSUMPTIONS = [
    "THE GANTRY IS PARKED AT MID TRAVEL ON ALL THREE AXES, so that it hides nothing "
    "on the rear plate or the beams. It is a viewing position and not a machine "
    "position: no axis has a home or a park figure in the registry. Y runs between "
    "the end plate's back edge level with the beam's back end and its front face "
    "level with the front end; X between the carriage butted against either end "
    "plate; Z over the 400 rail, with the Z plate centred on the butted block pair "
    "because the plate's offset along the spacers is not dimensioned.",
    "The front fin's taper is drawn with a VERTICAL FRONT EDGE and the 200-to-100 "
    "taper on its back. Sheet 1 gives the widths, not which edge is square.",
    "The box tongue is drawn from the bottom skin's top face up, 179 tall, to land "
    "at the 60 proud the registry gives. torsion-box.md says 180.",
    "THE BALL NUTS ARE DRAWN AT MID TRAVEL. None of the three axes has a home or "
    "park position in the registry, so the nut is put halfway along its screw. Where a "
    "nut sits is therefore the one thing in the drive train NOT to read off this model.",
    "THE CASTINGS' RAILS ARE DRAWN SOLID. The real casting is open between the two "
    "rails that join its screw end to its motor plate. Solid is the conservative way "
    "round for an interference check - a clearance the model SHOWS is real, one it "
    "denies may not be.",
    "THE X AND Z CASTINGS ARE PLACED BY THEIR SCREW. The bearing end is set where the "
    "screw's long journal ends and the rest follows, so the motor's position is a "
    "consequence of the 1000 screw rather than a figure anyone chose. THE TWO Y "
    "CASTINGS ARE NOT: they are placed by the interposer's leading edge, which their "
    "motor frame's 5 mm lip sits on.",
    "NO BASE OR LEGS - deliberately out of scope. The box sits on the ground plane.",
]

# What the hover says about a part, keyed by the name it is drawn under. ONLY
# WHAT THE REGISTRY OR A VENDOR PAGE ALREADY SAYS goes in here - a tooltip that
# invents a spec is worse than one that says nothing, because it reads as though
# somebody checked. Where a fastener's length is genuinely not recorded, the
# string says so rather than guessing a size that would then get ordered.
#
# A call site may pass d= instead, and that wins. It has to for the fasteners:
# "Flange head" is drawn at six different joints and they are not all one bolt.
DETAIL = {
    "Y beam": "30-6060 aluminium extrusion",
    "X beam": "30-6060 aluminium extrusion",
    "Y rail": "HGR20 linear rail",
    "X rail": "HGR20 linear rail",
    "Z rail": "HGR20 linear rail",
    "Y block": "HGH20 bearing block",
    "X block": "HGH20 bearing block",
    "Z block": "HGH20 bearing block",
    "Ball screw": "1605 ball screw, 16 diameter and 5 lead, right-hand - all four "
                  "axes are the same part, only the length differs",
    "Ball screw thread": "the thread's turns at the 5 mm lead, drawn as a line at the "
                         "crest. The groove's section is not dimensioned in the repo",
    "Screw journal": "the screw's journal, into a bearing at each end",
    "Ball nut": "DSG1605 housed ball nut - the same part on all four axes",
    "Nut bolt face": "the nut housing's mounting flat, 4 x M5 tapped INTO the housing",
    "BF12 wing": "BF12 bearing support - one part, drawn as a wing plus a boss",
    "BF12 boss": "BF12 bearing support - one part, drawn as a wing plus a boss",
    "Casting wing": "the cast stepper mount's bearing end",
    "Casting boss": "the cast stepper mount's bearing end",
    "Casting rails": "the cast stepper mount, DRAWN SOLID - the real casting is open here",
    "Motor plate": "the casting's motor plate",
    # HIS OWN WORDING FOR THE PART, 2026-10-11 - the motor carries its driver,
    # which is why MOTOR_BODY_L is 94 and not a plain NEMA 23's length.
    "Stepper motor": "All in one Closed Loop NEMA 23 stepper, 2.2N.m 5A 24-50VDC",
    "Interposer": "interposer bar - three the same",
    "Front strip": "front joining strip, ordered as 1/8in 6061 flat bar",
    "Fender washer": "plain M8 fender washer, under the acorn nut",
    "Acorn nut": "M8 acorn nut, on the tongue bolt's outboard end",
    "Rail counterbore": "counterbore in the rail, for an M5 x 16 rail bolt",
    "Z spacer": "spacer bar, sandwiched between the bearing blocks and the Z plate",
    "Y nut doubler": "doubler on the X end plate's outboard face, carrying the Y nut sole plate",
    "X nut doubler": "doubler on the carriage plate's back face, carrying the X sole plate",
    "Shelf bar": "the bar the X beam's underside rests on",
    "BF12 tongue": "the tongue that carries the X axis BF12, on the MIN X end plate only",
}

# WHICH SHOP PACK SHEET MAKES A PART, by the name it is drawn under. Only parts
# that get MADE are here: a bought rail, a bought clamp and a stepper have no
# sheet, and the absence is the information. Checked against the pack itself at
# generation time, so a renumbered sheet is an error here and not a wrong label
# on the page.
#
# Two parts are drawn twice under one name and their sheets differ by hand, so
# those are passed at the call site instead: the fins are Sheets 1a and 1b, and
# the X end plates are 2a with the min X one also carrying 2b's tongue.
SHEETS = {
    "Shelf bar": "2c",
    "Y nut doubler": "2d",
    "X nut doubler": "2d",
    "BF12 tongue": "2b",
    "X carriage plate": "3a",
    "Z spacer": "3b",
    "Z stop block": "3c",
    "Z plate": "4",
    "Y sole plate": "5",
    "Interposer": "6",
    "Rear plate": "7",
    "Front strip": "8",
    "Side plate": "9",
    "X sole plate": "5",
}
SHOP_PACK = ROOT / "machine" / "drawings" / "shop-pack.html"


def sheet_note(label):
    return "SHOP PACK: Sheet " + label


def check_sheets(extra):
    """Every sheet named here has to exist in the pack. Nothing else in this
    script can tell the difference between a right and a wrong sheet number,
    and a wrong one on a hover is worse than none - it sends somebody to the
    wrong drawing."""
    import re
    pack = SHOP_PACK.read_text(encoding="utf-8")
    # THE ANCHORS AND NOT THE PROSE. The pack says "Sheet 1 gives the widths"
    # in running text, which made two sheets that do not exist look as though
    # they did. One anchor does not match its own number: 2a is sheet-2.
    have = {{"2": "2a"}.get(x, x)
            for x in re.findall(r'id="sheet-([0-9]+[a-z]?)"', pack)}
    want = set(SHEETS.values()) | set(extra)
    missing = sorted(want - have)
    if missing:
        raise SystemExit("sheet(s) named by the model but not in the shop pack: "
                         + ", ".join(missing))
    return sorted(have - want)


# The fasteners.
#
# FLAG: A BOLT'S LENGTH IS READ OUT OF dimensions/fasteners.toml, BY JOINT ID. It
# used to be typed here, and every one of these strings said LENGTH NOT RECORDED
# because that was true when they were written - the schedule did not exist yet.
# It does now, and the model went on telling anyone who hovered a bolt that
# nobody knew how long it was while the schedule said 35. His catch, 2026-10-11.
#
# A site that names no joint still gets LENGTH NOT RECORDED, and that is now a
# REAL answer rather than a stale one: it means the schedule has no entry for
# that joint. A site that names a joint the schedule does not have fails the
# build, so a renamed id cannot quietly go back to saying nothing is known.
_JOINTS = {j["id"]: j for j in tomllib.loads(
    (ROOT / "dimensions" / "fasteners.toml").read_text(encoding="utf-8"))["joint"]}


# What the two helpers have handed out. Membership, not pattern matching: a
# tooltip is derived if it CAME FROM HERE, which is the only form of that
# question with a reliable answer.
DERIVED_HEAD, DERIVED_LEN = set(), set()


def _keep_head(t):
    DERIVED_HEAD.add(t)
    return t


def _keep_len(t):
    DERIVED_LEN.add(t)
    return t


def blen(jid):
    """' - M8 x 35' for a joint in the schedule, from the schedule."""
    if jid is None:
        return _keep_len(" - LENGTH NOT RECORDED - no entry in the schedule")
    j = _JOINTS.get(jid)
    if j is None:
        raise SystemExit(f"a tooltip names the joint {jid!r}, which is not in "
                         f"dimensions/fasteners.toml")
    if j.get("length") is None:
        return _keep_len(" - LENGTH NOT RECORDED - the schedule has none")
    return _keep_len(f" - M{j['size']:g} x {j['length']:g}")


# FLAG: THE HEAD IS DESCRIBED FROM THE SCHEDULE TOO, not from a constant. There
# was one M8_HEAD string saying "flanged button head" and it prefixed every M8
# tooltip, including the shelf bar's socket-head pair - so the same tooltip said
# flanged button head at the front and socket at the back. His catch came from
# the other end of the same fault: the spindle clamp's bolts reported themselves
# as flange because the GROUP was called "M8 flange bolt heads".
HEAD_PROSE = {
    "flange": "flanged button head, hex socket in the dome",
    "flange, low profile": "LOW PROFILE flanged button head, hex socket in the dome",
    "socket": "socket head cap",
    "socket, counterbored": "socket head cap, counterbored",
}


def M8_HEAD(jid):
    """What the head IS, in words, for the joint the schedule names.

    FLAG: EVERY BOLT TOOLTIP COMES THROUGH HERE AND THROUGH blen(). They record
    what they hand out, and check_tips() at the end of main() fails the build if
    any part in the bolts group carries text that did not come from them. The
    sweep that was supposed to make the tooltips derive from the schedule
    converted the shared helpers and left the call sites that spell their text
    out inline, so the fin angle bolts went on saying nothing about their head
    while the strip bolts said it - his catch, 2026-10-11. A sweep nobody can
    check is a sweep that will be incomplete again.
    """
    j = _JOINTS.get(jid) if jid else None
    if j is None:
        return _keep_head("NOT IN THE FASTENER SCHEDULE, so neither the head "
                          "nor the length below is from it")
    pitch = {3: "0.5", 4: "0.7", 5: "0.8", 6: "1.0", 8: "1.25"}.get(j.get("size"), "")
    size = f"M{j['size']:g}" + (f" x {pitch}" if pitch else "")
    kind = HEAD_PROSE.get(j.get("head"))
    return _keep_head(f"{size} {kind}" if kind else f"{size}, HEAD NOT RECORDED")
def D_SIDE_BOLT(jid):
    return M8_HEAD(jid) + " - with a plain washer, into a slide-in T-nut" + blen(jid)


def D_STRIP_BOLT(jid):
    return M8_HEAD(jid) + " - A4/316, into a slide-in T-nut" + blen(jid)
def D_BEAM_END(jid):
    return M8_HEAD(jid) + " - into the extrusion's lengthwise corner bore" + blen(jid)


def D_TNUT(jid):
    return M8_HEAD(jid) + " - into a slide-in T-nut in the beam's slot" + blen(jid)


def D_SHELF_V(jid):
    return M8_HEAD(jid) + " - up into the beam's underside slot" + blen(jid)


def D_SHELF_H(jid):
    return M8_HEAD(jid) + " - into a BLIND tap in the X end plate" + blen(jid)


def D_TONGUE(jid):
    return (M8_HEAD(jid) + " - through plate and tongue to a fender washer and an "
            "acorn nut" + blen(jid))


def D_M5_PLATE(jid):
    return M8_HEAD(jid) + " - tapped into the plate" + blen(jid)


def D_M5_BAR(jid):
    return M8_HEAD(jid) + " - up out of the casting into the tapped bar" + blen(jid)


def D_M5_END(jid):
    return M8_HEAD(jid) + " - into a tapped end face" + blen(jid)


def D_M5_EDGE(jid):
    return M8_HEAD(jid) + " - into the doubler's tapped top edge" + blen(jid)


def D_M5_NUT(jid):
    return M8_HEAD(jid) + " - into the ball nut housing" + blen(jid)


def main() -> int:
    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        return 2
    v = {s: reg.value(s) for s in reg.order}

    P = []  # parts: name, group, colour, [x0,y0,z0], [x1,y1,z1]
    # A SUNK HOLE OR POCKET, dark. Defined here rather than beside the rail
    # counterbores that first used it: the spoilboard draws holes long before
    # the rails do, and a colour constant is not a rail detail.
    HOLE = 0x22262A

    # WHICH CARRIAGES A PART RIDES ON - "" for the frame, "Y" for the gantry,
    # "YX" for the X carriage, "YXZ" for the Z carriage. It is set as a cursor
    # across the sections below rather than passed at 60 call sites, and a call
    # may override it with k=. The display groups cannot serve: a bolt is in
    # "bolts" whether it rides the gantry or sits in the torsion box, and
    # "drive" holds both the screws, which never move, and the nuts, which do.
    ride = [""]

    def box(name, group, colour, x0, y0, z0, x1, y1, z1, d="", k=None, u=None):
        # u is a UNIT ID for one part that has to be drawn as several boxes -
        # the tee track bed's flats are slices of one 250 panel, not parts. A
        # click in the viewer takes the whole unit, because hiding one flat of a
        # panel is not a thing anybody wants to do.
        b = {"n": name, "g": group, "c": colour, "t": "box", "d": d,
             "k": ride[0] if k is None else k,
             "p": [min(x0, x1), min(y0, y1), min(z0, z1)],
             "q": [max(x0, x1), max(y0, y1), max(z0, z1)]}
        if u:
            b["u"] = u
        P.append(b)

    def cyl(name, group, colour, cx, cy, z0, z1, r, axis="z", seg=36, d="",
            k=None):
        """A cylinder along one axis. The spindle is round and a box misrepresents
        its clearance - at 45 degrees a box corner sticks out r*(sqrt2-1) further.
        Bolt heads are round for the same reason and are drawn with few segments.

        cx, cy are the two coordinates the axis does NOT run along, in machine
        order: for axis 'z' that is (x, y), for 'x' it is (y, z), for 'y' (x, z).
        """
        lo, hi = min(z0, z1), max(z0, z1)
        if axis == "z":
            p, q = [cx - r, cy - r, lo], [cx + r, cy + r, hi]
        elif axis == "x":
            p, q = [lo, cx - r, cy - r], [hi, cx + r, cy + r]
        else:
            p, q = [cx - r, lo, cy - r], [cx + r, hi, cy + r]
        P.append({"n": name, "g": group, "c": colour, "t": "cyl", "ax": axis,
                  "cx": cx, "cy": cy, "r": r, "z0": lo, "z1": hi, "seg": seg,
                  "d": d, "k": ride[0] if k is None else k,
                  "p": p, "q": q})

    def helix(name, group, colour, cx, cy, z0, z1, r, axis, lead, d="", k=None):
        """The thread, as ONE RIGHT-HAND POLYLINE at the crest radius.

        Not a solid and not a swept ridge. The ball groove's section is not
        dimensioned anywhere in the repo, so a ridge would be invented metal;
        what a line can carry honestly is WHERE the turns are, which is the
        lead. cx, cy and axis follow cyl's convention exactly.

        It therefore has no volume, stays out of the interference check, and
        leaves the screw's envelope as the cylinder underneath it.
        """
        lo, hi = min(z0, z1), max(z0, z1)
        if axis == "z":
            p, q = [cx - r, cy - r, lo], [cx + r, cy + r, hi]
        elif axis == "x":
            p, q = [lo, cx - r, cy - r], [hi, cx + r, cy + r]
        else:
            p, q = [cx - r, lo, cy - r], [cx + r, hi, cy + r]
        P.append({"n": name, "g": group, "c": colour, "t": "helix", "ax": axis,
                  "cx": cx, "cy": cy, "r": r, "z0": lo, "z1": hi, "lead": lead,
                  "d": d, "k": ride[0] if k is None else k, "p": p, "q": q})

    def prism(name, group, colour, profile, ya, yb, holes=None, d="", k=None,
              plane="xz"):
        """A profile extruded along the axis it does not lie in.

        plane "xz" is a section across the machine and up, extruded along
        FORE-AFT - the fins. plane "xy" is a section across the machine and
        OUT from the Z plate, extruded along Z - the spindle clamps, whose
        shape lives in that plane and whose bore runs along the extrusion.

        p/q stay the bounding box so the camera framing keeps working. The
        interference check no longer settles for that: where a prism is in the
        pair it re-tests against this profile, because on a tapered part the
        box claims metal the part does not have.
        """
        us = [pt[0] for pt in profile]
        vs = [pt[1] for pt in profile]
        lo, hi = min(ya, yb), max(ya, yb)
        if plane == "xz":
            p, q = [min(us), lo, min(vs)], [max(us), hi, max(vs)]
        else:
            p, q = [min(us), min(vs), lo], [max(us), max(vs), hi]
        P.append({"n": name, "g": group, "c": colour, "t": "prism", "d": d,
                  "k": ride[0] if k is None else k, "pl": plane,
                  "profile": profile, "holes": holes or [],
                  "ya": lo, "yb": hi, "p": p, "q": q})

    W = v["MACHINE_OUTER_W"]         # 1211.238, side plate face to side plate face
    # 🔴 THE BOX IS NOT THE ENVELOPE. BOX_W was an alias of MACHINE_OUTER_W until
    # the grid went to whole millimetres, and is a chosen 1211 since - so every
    # part whose position is set by the BOX (skins, webs, ribs, legs, the base,
    # the walls) uses this, and only the machine's own parts use W. Drawing the
    # box at the envelope put it 0.238 wide, which is where the back tenon
    # block's 0.12 overlap came from: the blocks are placed off BOX_W in the
    # registry and the tenon they flank was placed off W here.
    BW = v["BOX_W"]                  # 1211, the skins' actual width
    D = v["BOX_FORE_AFT"]            # 1156.35
    TT = v["T_BOX_TONGUE"]           # 19
    # THE TOP SKIN, which is the one this is used for - the back and side tongues
    # reach down to its underside. 25 since 2026-10-11, and the underside does NOT
    # move with it: BOX_THK grows by the same 6, so -(BOX_THK - SKIN) is still -119.
    SKIN = v["T_BB_SKIN_TOP"]        # 25

    # ---- torsion box -----------------------------------------------------
    # DRAWN AS ITS REAL PARTS since 2026-10-11, not as one solid: he needs to
    # hide the top skin and look at the bay layout and the tenon placement. So
    # the top skin is its OWN GROUP and toggles alone.
    #
    # The z stack, and it closes on BOX_THK exactly:
    #   0 to -T_BB_SKIN_TOP          the top skin            (25)
    #   -25 to -125                  the cavity, ribs and webs stand here (100)
    #   -125 to -144                 the bottom skin         (19)
    skin_bot_top = -(v["BOX_THK"] - v["T_BB_SKIN_BOT"])   # -125
    cav_z0, cav_z1 = skin_bot_top, -SKIN                  # -125 .. -25
    web = v["T_BOX_WALL_WEB"]

    box("Top skin", "topskin", 0xC9A227, 0, 0, -SKIN, BW, D, 0,
        d="25 Baltic birch - hide this group to see the bays and tenons")

    # ---- the three posts, and the tenon holes they need in the bottom skin --
    # THE GEOMETRY CLOSES AND IT IS WORTH SAYING WHY, because it is the check
    # that the 44 ledge is right: the ledges are cut on the OUTWARD-facing
    # faces, so a post's outer face lands FLUSH WITH THE TONGUE'S OUTER FACE at
    # -T_BOX_TONGUE, the 44 wall (25 tongue + 19 web) sits squarely on the 44
    # shoulder, and the tenon occupies from the web's inner face inboard. No
    # number was chosen to make that happen.
    # SETTLED: THE FRONT WALL AND THE TWO FRONT POSTS STAND AT THE BOX'S FRONT EDGE
    # AND MOVE WITH IT - his, 2026-10-11, closing BOX_FRONT_WALL_AT. Each front
    # post therefore reaches D - web + ledge, 25 past the skin's front edge,
    # exactly as it reaches 25 past the side edge at x = -25. Everything below
    # is written off D, so the posts follow the front face for free - which
    # matters because the apron depth is a REMAINDER now, so the front edge
    # moves whenever the box is resized. It moved 53.65 forward the same day.
    #
    # NOTE: It also keeps the front tenons in a real corner, snug against both
    # perimeter walls - the property TENON_CORNER's note leans on.
    #
    # OPEN: The model still draws no FRONT TONGUE, only the back and side ones.
    # VALUES.md on BOX_FRONT_OVERHANG says the front has none: the box runs
    # past the fins and four L-brackets per fin tie it down. The front WALL is
    # here; a front tongue standing 60 proud is not, and that is on purpose.
    ledge = v["T_BOX_LEDGE"]
    # The leg is 72 x 86 since 2026-10-15, not square, so the corner tenon has
    # its own figure on each axis: tcx across the machine, tcy fore and aft.
    tcx, tcy = v["TENON_CORNER_X"], v["TENON_CORNER_Y"]
    tb, pwx = v["TENON_BACK_DEPTH"], v["POST_W_X"]
    # The grid member's section, needed up here because the leg's SLOT is the
    # same 36: a rail fills it, which is the whole joint.
    gm_h, gm_t = v["GRID_MEMBER_H"], v["GRID_MEMBER_T"]
    housed = gm_t / 2                        # the cross rail's outer 18
    # The tenon is POST_TENON_L long from the shoulder, which leaves it shy of
    # the top skin's underside by whatever that length does not reach. Derived
    # and not stated: it was a literal 1.0 while the bottom skin was 19, and the
    # measured 18 made the real clearance 0 until POST_TENON_L came down to 116.
    post_top = -v["BOX_THK"] + v["POST_TENON_L"]
    # THE LEGS RUN TO THE FLOOR NOW, not to a drawing stub. The floor's Z comes
    # off SURFACE_H, which is a PLACEHOLDER - see its note. POST_STUB_L is left
    # in the registry as the old drawing length and is no longer used here.
    floor_z = -v["BOX_THK"] - v["LEG_BELOW_BOX"]
    post_bot = floor_z
    # The two grids' Z bands, needed up here because the legs are NOTCHED to
    # house the cross rails and the notch only exists where a rail is.
    grid_hi_top = -v["BOX_THK"] - v["BASE_BOX_GAP"]
    grid_lo_bot = floor_z + v["BASE_FLOOR_CLEAR"]
    rail_bands = ((grid_lo_bot, grid_lo_bot + gm_h),
                  (grid_hi_top - gm_h, grid_hi_top))
    ledge_z = -v["BOX_THK"]          # the shoulder IS the bottom skin's underside
    hc = v["TENON_HOLE_CLEAR"]
    pwy = v["POST_W_Y"]

    # Each post: (tenon rect, full-section rect) in machine x/y. The two REAR
    # CORNER legs carry no tenon - the box lands on three legs only - so they
    # have no entry here and are drawn with the base below.
    # The first rect is the leg's UN-LEDGED region - what stands proud of the
    # shoulder before the slot is taken out of it. NOT the tenon: with a
    # full-height slot the tenon is whichever STRIPS fall inside this band.
    beyond = pwx - ledge                     # 30 across, on a leg ledged in X
    posts = [
        ("Post, front left", (web, web + beyond, D - web - tcy, D - web),
         (web - ledge, web + beyond, D - web - tcy, D - web + ledge)),
        ("Post, front right", (BW - web - beyond, BW - web, D - web - tcy, D - web),
         (BW - web - beyond, BW - web + ledge, D - web - tcy, D - web + ledge)),
        ("Post, back centre", (BW / 2 - pwx / 2, BW / 2 + pwx / 2, web, web + tb),
         (BW / 2 - pwx / 2, BW / 2 + pwx / 2, web - ledge, web + tb)),
    ]
    # A LEG IS DRAWN AS ITS TWO OUTER STRIPS, NOT AS A SOLID. The middle two
    # laminations are a SLOT, and everything fore-aft lives in it: a rail at each
    # grid, the filler between them, and in the rear middle leg the shear wall.
    # Drawn solid, every one of those sat inside the leg with coincident faces -
    # which is what put the striped z-fighting patch on the front leg in his
    # screenshot, and it also hid the joint this model exists to show.
    strip = (pwx - gm_t) / 2             # one outer strip, 18 of the 72

    def leg_strips(nm, group, colour, px0, px1, py0, py1, z0, z1, notch, d=""):
        """Both outer strips of a leg, with its outer face cut back.

        FRONT legs lose `housed` where a cross rail is AND EVERYWHERE ABOVE THE
        TOP ONE, so the face comes out as the Z segments below the upper rail
        band only - the housing runs clear up to the top of the tenon. REAR legs
        lose it over the WHOLE height - his, 2026-10-15 - because the back shear
        wall sits in the same rebate, and the band then carries the wall over
        most of its height and the rails' outer laminations at the two grids.
        """
        back = notch.startswith("back")
        # NAMED BY WHICH SIDE OF THE MACHINE THEY ARE ON, not by whether they
        # come first: on a right-hand leg px0 is the one nearer the centre, so
        # naming the pair outer-then-inner got it backwards over there.
        for sx0 in (px0, px1 - strip):
            side = ("inner"
                    if abs(sx0 + strip / 2 - BW / 2) < abs(px0 + px1 - BW) / 2
                    else "outer")
            # ONLY THE INNER STRIP IS EVER CUT BACK - his, 2026-10-15, and it is
            # ONE RULE AT BOTH ENDS OF THE BASE: the OUTERMOST lamination of
            # every leg stays its full POST_W_Y, and whatever runs along that
            # face - the cross rail at the front, the shear wall at the back -
            # stops one strip short and is covered by it. The back centre leg is
            # the exception, because the wall passes right through it.
            nearer = abs(sx0 + strip / 2 - BW / 2) < abs(px0 + px1 - BW) / 2
            if not (notch == "back-both" or nearer):
                box(f"{nm}, {side} strip", group, colour,
                    sx0, py0, z0, sx0 + strip, py1, z1, d=d)
                continue
            by_a, by_b = (py0 + housed, py1) if back else (py0, py1 - housed)
            box(f"{nm}, {side} strip", group, colour,
                sx0, by_a, z0, sx0 + strip, by_b, z1, d=d)
            if back:
                continue                 # the rebate runs the full height
            # 🔴 NO SEGMENT ABOVE THE TOP RAIL BAND - his, from the model:
            # "that little ear that sticks out over where the front rail comes
            # in should go away, so the cutout for the rail is all the way up to
            # the top of the tenon". It was BASE_BOX_GAP tall, 18 deep and 18
            # wide, standing over the rail's housing with the shoulder cut away
            # right above it. The list simply STOPS at the top band rather than
            # closing on z1: with z1 on the end, [0::2]/[1::2] pairs one last
            # gap from the top band up to the leg's top, and that gap is the ear.
            edges = [z0] + [z for band in rail_bands for z in band]
            for za, zb in zip(edges[0::2], edges[1::2]):
                if zb - za < 1e-9:
                    continue
                box(f"{nm}, {side} strip at the housing", group, colour,
                    sx0, py1 - housed, za, sx0 + strip, py1, zb,
                    d=f"the {housed:g} the cross rail is housed into - present "
                      f"only where there is no rail")

    holes_xy = []
    corner_notch = {}            # front leg -> the skin corner it opens out to
    back_notch = []              # the back centre's, out to the BACK edge
    leg_rects = []
    for nm, (tx0, tx1, ty0, ty1), (px0, px1, py0, py1) in posts:
        leg_strips(nm, "legs", 0x7A5230, px0, px1, py0, py1, post_bot, ledge_z,
                   "back-both" if "back" in nm else "front",
                   d=f"{strip:g} of a {pwx:g} x {pwy:g} laminated leg - the two "
                     f"middle laminations are the slot. The shoulder bears the box")
        leg_rects.append((px0, px1, py0, py1))
        # THE SLOT RUNS FULL HEIGHT, so it passes through the tenon as well: a
        # tenon tab is a STRIP's top, never the leg's. A strip standing inside
        # the leg's outward ledge has a tab; one swallowed by the ledge has none.
        # So a corner leg has ONE tab and the back centre leg has TWO, with 36 of
        # slot between them.
        for sx0 in (px0, px1 - strip):
            if not (tx0 - 1e-9 <= sx0 and sx0 + strip <= tx1 + 1e-9):
                continue                       # this strip is inside the ledge
            box(nm + " tenon tab", "legs", 0x9C6B3C,
                sx0, ty0, ledge_z, sx0 + strip, ty1, post_top,
                d=f"{strip:g} x {ty1 - ty0:g} - location only, it carries no "
                  f"vertical load. All of that is on the shoulder")
            if "back" in nm:
                # 🔴 ONE SLOT SPANNING BOTH TABS, NOT TWO - his, 2026-10-15,
                # and it is the file's own advice taken: the island between the
                # tabs BEARS NOTHING, because it sits over the leg's slot. So
                # there is nothing to be gained by cutting round it and a
                # straight cut to gain, which is why it is one opening the
                # width of the pair plus TENON_HOLE_CLEAR a side. Appended
                # once, after the tabs, rather than per tab.
                continue
            # ---- the two FRONT tabs: a spacer, and a corner instead of a hole
            # 🔴 A SPACER ON THE TAB'S OUTER FACE - his, 2026-10-15, and the
            # reason is the one worth keeping: WITHOUT IT THE BOX IS LOCATED ON
            # A FACE AND NOT ON A CORNER. The tab butts the front web with
            # nothing to spare and has TENON_SPACER_GAP of air to the side web,
            # so the corner is captured one way only. Fill that gap and the
            # composite tenon's outer face lands ON the side web's inner face.
            #
            # DRAWN AT THE GAP, NOT AT THE STOCK. T_TENON_SPACER mikes at 12.003
            # on his 12 scrap - 0.003 over, which is the glue line and not
            # geometry. The measurement is recorded on that symbol; the model
            # draws the hole it fills.
            gap = v["TENON_SPACER_GAP"]
            left = sx0 + strip / 2 < BW / 2          # which way is OUTBOARD
            sp0 = sx0 - gap if left else sx0 + strip
            box(nm + " tenon corner spacer", "legs", 0xB5894F,
                sp0, ty0, ledge_z, sp0 + gap, ty1, post_top,
                d=f"{gap:g} x {ty1 - ty0:g} x {post_top - ledge_z:g}, from 12 "
                  f"scrap - glued to the OUTER face of the tenon so the "
                  f"composite lands on the web's inner face. It locates the "
                  f"box's tongue CORNER, not just a face")
            # 🔴 AND THE SKIN TAKES A CORNER, NOT A HOLE - his, same day. A
            # closed rectangle leaves the outer 18 of skin wrapped around the
            # corner between the tenon and the skin's own edge; he wants that
            # 18 gone and the cutout open to both edges, all of it covered by
            # the 24 laminations. So this corner is spliced out of the skin's
            # OUTLINE rather than added to `holes_xy`: a hole whose edge lands
            # on the outline is not a hole, and the triangulator's seams are
            # exactly what check-prism-edges.py exists to catch.
            inx = (sx0 + strip + hc) if left else (sx0 - hc)
            corner_notch["left" if left else "right"] = (inx, ty0 - hc)

        if "back" in nm:
            # 🔴 AND IT OPENS TO THE BACK EDGE TOO - his, 2026-10-15, on seeing
            # the detail: as a closed rectangle in the field of the sheet it
            # needed a start hole and a jigsaw. The skin left between it and
            # the edge was T_BOX_WALL_WEB less the clearance, and ALL of that
            # sits under the back perimeter web with the back tongue outside
            # it, so none of it shows. Opened out, every one of the three
            # tenon cuts is a saw cut from an edge.
            back_notch.append((px0 - hc, px1 + hc, ty1 + hc))

    # The outline, anticlockwise from the back left, with ALL THREE tenon cuts
    # spliced out of it: along the back edge and into the back centre's notch,
    # up the right edge into that corner, forward and across the front edge to
    # the other corner, and back out to the left edge. NOTHING is a hole in this
    # skin any more, which is the point - every cut reaches an edge, so every
    # cut is a saw cut.
    nl, nr = corner_notch.get("left"), corner_notch.get("right")
    outline = [[0, 0]]
    for bx0, bx1, by in sorted(back_notch):
        outline += [[bx0, 0], [bx0, by], [bx1, by], [bx1, 0]]
    outline += [[BW, 0]]
    outline += ([[BW, nr[1]], [nr[0], nr[1]], [nr[0], D]] if nr else [[BW, D]])
    outline += ([[nl[0], D], [nl[0], nl[1]], [0, nl[1]]] if nl else [[0, D]])
    prism("Bottom skin", "box", 0xB08A1E,
          outline, skin_bot_top, -v["BOX_THK"],
          holes=holes_xy, plane="xy",
          d="19 Baltic birch, resting on the three post shoulders. NONE of the "
            "three tenon cuts is a hole: the two front ones take a corner and "
            "the back centre's takes a notch out of the back edge, so every one "
            "of them is a saw cut and the skin under the webs goes with it")

    # ---- the base: two grids holding five legs ---------------------------
    # HIS SPEC 2026-10-15, and the definition is the point: the base is not a
    # table that happens to have legs, it is TWO GRIDS whose job is holding five
    # legs in position - three of which the box lands on.
    #
    # 🔴 THE UPPER GRID MUST NEVER TOUCH THE BOX. BASE_BOX_GAP is the whole
    # three-point mount: the box contacts three leg tops and nothing else, and
    # the moment the grid touches it there is a fourth and fifth contact point
    # and the failure is SILENT - nothing shows but the Y beams going out of
    # coplanar. The gap is drawn so the model shows it rather than implying it.
    grid_hi_top = -v["BOX_THK"] - v["BASE_BOX_GAP"]
    grid_lo_bot = floor_z + v["BASE_FLOOR_CLEAR"]
    grids = (("upper", grid_hi_top - gm_h, grid_hi_top),
             ("lower", grid_lo_bot, grid_lo_bot + gm_h))

    # The two REAR CORNER legs. They carry no tenon - the box lands on three
    # legs only - so they stop at the box's underside and hold up the grids and
    # the back shear wall. Drawn at the same stations as the front pair.
    # FLAG: THEIR X SPAN IS THE LEG'S OWN WIDTH, not the corner tenon's. It was
    # written as web + tcx back when tcx happened to be 30 and the sum happened
    # to land right; when the full-height slot took the corner tenon to 18 these
    # two legs quietly became 60 wide.
    for nm, x0, x1 in (("Leg, rear left", web - ledge, web - ledge + pwx),
                       ("Leg, rear right", BW - web + ledge - pwx, BW - web + ledge)):
        leg_strips(nm, "legs", 0x8A5A2B, x0, x1, web - ledge, web + tb,
                   floor_z, -v["BOX_THK"], "back-inner",
                   d=f"{strip:g} of a {pwx:g} x {pwy:g} laminated leg - it carries "
                     f"the grids and the back shear wall, NOT the box")
        leg_rects.append((x0, x1, web - ledge, web + tb))

    # Grid members, on edge: TWO fore-aft rails and TWO cross rails, a plain
    # rectangle. FLAG: THERE IS NO CENTRE FORE-AFT RAIL - his correction
    # 2026-10-15, and it is the right one: the central SHEAR WALL is the
    # centreline fore-aft member, and standing the full BASE_VOLUME_H between
    # the grids it is a far deeper beam than a gm_h rail could ever be. A rail
    # there would be a second member doing a job already done, in the one place
    # the wall has to pass.
    #
    # The fore-aft rails run FULL LENGTH because they pass THROUGH the legs as a
    # through tenon left open at glue-up. The cross rails run BETWEEN them: a
    # cross rail cannot also pass through a leg at the same height, because the
    # leg has one slot and the fore-aft rail is in it.
    bx0, bx1 = web - ledge, BW - web + ledge          # the base's outer envelope
    by0, by1 = web - ledge, D - web + ledge
    housed = gm_t / 2                                # the rail's outer 18
    # THE CROSS RAILS ARE THE CONTINUOUS ONES AT A CORNER - his, 2026-10-15. Each
    # runs the base's full width with its OUTER 18 housed in a notch in the legs'
    # outer faces (the back of the rear legs, the front of the front legs) and
    # its INNER 18 spanning between them. So the fore-aft rails butt their inner
    # faces rather than crossing them, which is what stops two rails wanting the
    # same space inside a leg.
    #
    # The leg notches are not drawn, for the same reason the rib notches are not:
    # an 18-deep housing removes no envelope, and drawing it would only clutter
    # the one view that shows the frame's layout.
    # EVERY PIECE ITS OWN COLOUR - his, 2026-10-15, so the boundaries read in a
    # frame where almost everything is the same 36 of the same plywood. The
    # wall's lip is the ONE exception: it shares the wall's colour because it is
    # the same sheet, not a separate piece.
    # The fore-aft rails sit IN THE LEGS' SLOT, which is the middle 36 of a leg -
    # NOT at the base's outer edge. Drawn at the edge they ran through the legs'
    # outer strips instead of between them.
    for which, z0, z1 in grids:
        for x0, x1 in ((bx0 + strip, bx0 + strip + gm_t),
                       (bx1 - strip - gm_t, bx1 - strip)):
            box(f"Grid rail, fore-aft ({which})", "rails", 0x3C7DA5,
                x0, by0 + housed, z0, x1, by1 - housed, z1,
                d=f"{gm_t:g} x {gm_h:g} on edge - it fills the legs' middle slot "
                  f"and butts the cross rails' inner faces")
        # A CROSS RAIL IS ITS TWO LAMINATIONS DOING DIFFERENT JOBS - his catch
        # on the model, 2026-10-15. The OUTER 18 runs the full width, through the
        # notch in every leg it passes. The INNER 18 only spans BETWEEN the legs:
        # it is not housed and it does not pass through anything. Drawn as one
        # 36 block it ran the whole rail through the legs, which is not the joint.
        # ONLY THE FRONT HAS A CROSS RAIL. At the back the shear wall replaces
        # them at both grids - his, 2026-10-15 - so there is nothing to draw
        # there but the wall, which runs continuously past both grid levels.
        for nm, y0, side in (("front", by1 - gm_t, "front"),):
            box(f"Grid rail, {nm} outer lamination ({which})", "rails", 0x3F8F5B,
                bx0 + strip, y0 if nm == "back" else y0 + housed, z0,
                bx1 - strip, y0 + housed if nm == "back" else y0 + gm_t, z1,
                d=f"{housed:g} x {gm_h:g} - the half housed in the legs. It "
                  f"stops one lamination short at each end, so the legs' "
                  f"outermost strips cover its end grain")
            on_this_side = sorted(r for r in leg_rects
                                  if (r[2] <= by0 + 1e-9) == (side == "rear"))
            spans = [bx0] + [x for r in on_this_side for x in (r[0], r[1])] + [bx1]
            for xa, xb in zip(spans[0::2], spans[1::2]):
                if xb - xa < 1e-9:
                    continue
                box(f"Grid rail, {nm} inner lamination ({which})", "rails", 0x2F6F47,
                    xa, y0 if nm == "front" else y0 + housed, z0,
                    xb, y0 + housed if nm == "front" else y0 + gm_t, z1,
                    d=f"{housed:g} x {gm_h:g} - it spans BETWEEN the legs and is "
                      f"not housed in any of them")

    # ---- the lower rails' outer pads, the casters and the fork channel -----
    # THE LOWER fore-aft rails are FOUR laminations, not two. The inner pair
    # passes through the legs' slot; these two cannot, so they butt a leg's face
    # at each end. They bring the rail out to POST_W_X so a caster's plate lands
    # on a full face. The upper grid keeps two.
    # A LAMINATION EACH SIDE OF THE CENTRAL WALL'S BOTTOM BAND, flush with its
    # bottom edge. It brings the wall out to POST_W_X so the centre caster's
    # plate lands on a full face, and its TOP EDGE is level with the lower
    # grid's top - a ledger down the centreline for a shelf or a cabinet.
    # It runs from the back centre leg's front face to the front cross rail.
    for sx0 in (BW / 2 - pwx / 2, BW / 2 + gm_t / 2):
        box("Wall pad, central - lower band", "walls", 0xD9BE8A,
            sx0, by0 + pwy, grid_lo_bot,
            sx0 + strip, by1 - gm_t, grid_lo_bot + gm_h,
            d=f"{strip:g} x {gm_h:g} x {v['CENTRE_WALL_PAD_L']:g}, flush with "
              f"the wall's bottom - it carries the centre caster's plate and "
              f"its top edge is a ledger level with the lower grid")

    cp, ch = v["CASTER_PLATE"], v["CASTER_H"]
    blk = v["CASTER_BLOCK_MIN"]
    pad_y0, pad_y1 = by0 + pwy, by1 - pwy          # between the legs' faces
    for x0, x1 in ((bx0 + strip, bx0 + strip + gm_t),
                   (bx1 - strip - gm_t, bx1 - strip)):
        for px0, px1 in ((x0 - strip, x0), (x1, x1 + strip)):
            box("Rail pad, lower fore-aft", "rails", 0x4E97C4,
                px0, pad_y0, grid_lo_bot, px1, pad_y1, grid_lo_bot + gm_h,
                d=f"{strip:g} x {gm_h:g} x {pad_y1 - pad_y0:g} - it butts a "
                  f"leg's face at each end and brings the rail out to "
                  f"{pwx:g}, which is what a caster plate lands on")

    # SIX LEVELLING CASTERS, all of them INSIDE the floor clearance rather than
    # under the legs, which is what keeps the base's height as drawn. Four
    # beside the corner legs under the lower rail, two straddling the back
    # centre leg - that one has no fore-aft rail and a single caster under it
    # would put its adjuster behind the leg.
    #
    # DRAWN AS THE ENVELOPE AND NOT AS A CASTER: the listing gives the plate,
    # the overall height and the travel, and nothing about the body, the wheel's
    # width or its offset. What is drawn is what is known.
    def caster(cx0, cy0, note):
        box("Caster block", "rails", 0x8C6A3F,
            cx0, cy0, grid_lo_bot - blk, cx0 + cp, cy0 + cp, grid_lo_bot,
            d=f"the drop block, drawn at its minimum {blk:g}. CUT TO FIT: it "
              f"has to put the wheel below the leg bottoms, and the six of "
              f"them are what level the base against the slab")
        box("Levelling caster", "rails", 0x999999,
            cx0, cy0, grid_lo_bot - blk - ch, cx0 + cp, cy0 + cp,
            grid_lo_bot - blk,
            d=f"{cp:g} plate, {ch:g} overall, "
              f"{v['CASTER_LEVEL_TRAVEL']:g} of levelling travel, 50 nylon "
              f"wheel. Drawn as its envelope - {note}")

    half = (cp - pwx) / 2                      # the plate stands 0.5 proud
    for lx0, lx1, ly0, ly1 in leg_rects:
        if abs(lx0 - (BW - pwx) / 2) < 1e-9:           # the back centre leg
            # ON THE CENTRAL WALL, just forward of the leg: that leg has no
            # fore-aft rail, and the wall's bottom band is brought out to
            # POST_W_X by a lamination each side.
            caster(lx0 - half, ly1,
                   "on the central wall's bottom edge, forward of the back "
                   "centre leg")
        else:
            cy0 = ly1 if ly0 <= by0 + 1e-9 else ly0 - cp
            caster(lx0 - half, cy0, "under the lower rail, hard against the "
                                    "leg's face")

    # TWO GUARD RAILS, a dressed 2x3 each, hanging below the lower grid and
    # FORK_CHANNEL_W apart. They keep the jack centred and stop a fork reaching
    # a caster. GUIDES AND NOT BEARING SURFACES: as the jack lifts, the forks
    # rise inside the channel until they bear on the grid's underside.
    chan_c = (pad_y0 + pad_y1) / 2
    for gy0 in (chan_c - v["FORK_CHANNEL_W"] / 2 - v["GUARD_RAIL_T"],
                chan_c + v["FORK_CHANNEL_W"] / 2):
        box("Fork guard rail", "rails", 0xB07A3C,
            bx0 + strip, gy0, grid_lo_bot - v["GUARD_RAIL_DROP"],
            bx1 - strip, gy0 + v["GUARD_RAIL_T"], grid_lo_bot,
            d=f"dressed 2x3, hanging {v['GUARD_RAIL_DROP']:g} below the grid "
              f"and leaving {v['BASE_FLOOR_CLEAR'] - v['GUARD_RAIL_DROP']:g} "
              f"under it. The two are {v['FORK_CHANNEL_W']:g} apart, which is "
              f"the channel the forks run in. BOTH ENDS RUN UNDER A LOWER "
              f"FORE-AFT RAIL and are screwed up into it - that is what takes "
              f"a sideways hit - and the central wall catches it at mid-span")

    # The two shear walls, a T in plan: the centreline one runs back to the back
    # centre leg, which is the box's own rear support, so the wall lands under
    # the load it braces. They are what leaves the left and right volumes open.
    # THE CENTRELINE WALL RUNS THE BASE'S WHOLE HEIGHT - his, 2026-10-15: it
    # starts at the BOTTOM of the lower grid, where a centre rail would have
    # been, and goes all the way up to the top of the upper one. That is why
    # there is no centre rail at either level: the wall IS the centreline member
    # at both grids and everything between them.
    #
    # It is NOTCHED AT ITS FRONT LOWER CORNER to go over the front rail - gm_t
    # across by gm_h up, so the notch shoulder sits on the rail's top edge and
    # the wall's end face finishes flush with the rail's outer face. Drawn as
    # the body plus the lip over the rail, which is what the notch leaves.
    sw_z0, sw_z1 = grid_lo_bot, grid_hi_top
    # THE BACK WALL IS ONE SHEET, NOT TWO, and it lives in the same full-height
    # rebate as the back rails' outer laminations - so it is drawn in the Z
    # segments between them. A shear panel is governed by its edge fastening
    # rather than its thickness, which is why 18 does the job here while the
    # central wall is 36 for the geometric reason that it has to fill a slot.
    # 🔴 IT IS ONE CONTINUOUS SHEET and that is why it owns the rebate outright:
    # a shear panel cut into three horizontal strips by the rails is no longer a
    # shear panel. So the wall fills the back 18 from the lower grid up to
    # BASE_BOX_GAP shy of the box, and the back cross rails present only their
    # INNER lamination, butting it.
    bw = v["T_BACK_WALL"]
    box("Shear wall, back", "walls", 0xD4793B,
        bx0 + strip, by0, sw_z0, bx1 - strip, by0 + bw, sw_z1,
        d=f"{bw:g} thick, ONE sheet - IT REPLACES THE BACK CROSS RAILS at both "
          f"grids. It stops one lamination short at each end so its end grain "
          f"butts the back of the outer lamination, and {v['BASE_BOX_GAP']:g} "
          f"shy of the box. Glue plus screws at about 150 all the way round")
    # IT STOPS SHORT AT BOTH ENDS so no end grain shows: the back wall covers it
    # at the rear, the front cross rail's OUTER lamination covers it at the
    # front. So the front notches only have to clear the rail's INNER lamination
    # and are half as deep as they were.
    # CUT SHORTER THAN THE BACK WALL, and the reason is a sheet rather than the
    # structure: at CENTRE_WALL_H both of its laminations come off one 5 x 5,
    # where at the back wall's height they take two. The difference comes off
    # the TOP, where the wall is free and nothing bears on it.
    box("Shear wall, centreline", "walls", 0xC9A66B,
        BW / 2 - gm_t / 2, by0 + bw, sw_z0,
        BW / 2 + gm_t / 2, by1 - gm_t, sw_z0 + v["CENTRE_WALL_H"],
        d="fore-aft on the centreline, the base's full height, from the front "
          "back to the back centre leg - which is the box's own rear support, "
          "so it lands under the load it braces")
    # TWO NOTCHES, ONE AT EACH FRONT CORNER - his, 2026-10-15. The front 36 is
    # wanted by the wall and by a front cross rail at BOTH grids, so the wall is
    # notched gm_t x gm_h at the bottom front and again at the top front. What
    # is left between them is this lip, which is exactly BASE_VOLUME_H tall.
    box("Shear wall lip, between the front rails", "walls", 0xC9A66B,
        BW / 2 - gm_t / 2, by1 - gm_t, grid_lo_bot + gm_h,
        BW / 2 + gm_t / 2, by1 - housed, grid_hi_top - gm_h,
        d=f"what the two front notches leave, each {housed:g} across now - it "
          f"stops at the cross rails' OUTER lamination, which covers its end "
          f"grain. The lower notch SITS ON its rail, and the two cheeks "
          f"capture it either side")

    # THE FRONT END IS A SOCKET, NOT TWO SCREWS - his. A pair of cheeks glued
    # and screwed to the BACK faces of both inner front cross rail laminations
    # straddle the wall, so 18 + gm_t + 18 is POST_W_X and the front end is the
    # same captured, bolted joint as the back centre leg's slot: same grip,
    # same bolt, same three-at-a-quarter-point pattern.
    #
    # 🔴 IT STOPS AT grid_hi_top LIKE EVERYTHING ELSE AT THIS END. A cheek
    # proud of the upper grid's top is a fourth contact under the box and the
    # three-point mount stops being determinate - the failure nothing shows but
    # the two Y beams drifting out of coplanar.
    cheek_t, cheek_w = v["CENTRE_WALL_CHEEK_T"], v["CENTRE_WALL_CHEEK_W"]
    cheek_front = by1 - gm_t                 # the inner lamination's back face
    for side, x0 in (("left", BW / 2 - gm_t / 2 - cheek_t),
                     ("right", BW / 2 + gm_t / 2)):
        box(f"Centre wall front cheek, {side}", "walls", 0xB08D57,
            x0, cheek_front - cheek_w, sw_z0,
            x0 + cheek_t, cheek_front, sw_z1,
            d=f"{cheek_t:g} x {cheek_w:g} x {v['CENTRE_WALL_CHEEK_H']:g}, "
              f"glued and screwed to the BACK of both inner front cross rail "
              f"laminations - it laps the full {gm_h:g} of each. With its pair "
              f"it makes a {cheek_t:g} + {gm_t:g} + {cheek_t:g} socket, the "
              f"leg's own {v['POST_W_X']:g}, and the wall is bolted through it "
              f"on the same pattern as the back centre leg")

    # FILLER BLOCKS in the four CORNER legs' slots, between the grids - his,
    # 2026-10-15. The slot is full height and carries a rail at each grid, so
    # without these the leg is two 18 planks BASE_VOLUME_H tall joined only top
    # and bottom, and two unconnected planks buckle independently where a
    # built-up section does not. Out of the leftover strip material.
    #
    # The rear middle leg gets none: the central wall is in its slot already,
    # which is the same job done by a part that was going in anyway.
    # A FILLER IS PART OF ITS LEG, SO IT TAKES THAT LEG'S COLOUR - his,
    # 2026-10-15. It goes in at the leg's own glue-up and is never a separate
    # part on the bench, so giving it one of its own said otherwise.
    all_legs = [(r, 0x7A5230 if i < 3 else 0x8A5A2B)
                for i, r in enumerate(leg_rects)]
    corner_legs = [(r, c) for i, (r, c) in enumerate(all_legs) if i != 2]

    # A SPACER AT THE FOOT OF ALL FIVE, glued to the inside of the outer
    # lamination - his, 2026-10-15. The slot runs the leg's full height, so
    # below the lower grid exactly BASE_FLOOR_CLEAR of it is open, and this
    # fills it. Without it a leg stands on the floor as two 18 strips with a 36
    # gap between them.
    for (px0, px1, py0, py1), leg_colour in all_legs:
        box("Leg foot spacer", "legs", leg_colour,
            px0 + (pwx - gm_t) / 2, py0, floor_z,
            px0 + (pwx - gm_t) / 2 + gm_t, py1, floor_z + v["FOOT_SPACER_H"],
            d=f"{gm_t:g} x {py1 - py0:g} x {v['FOOT_SPACER_H']:g} - it closes "
              f"the slot from the floor up to the lower rail, and it is what "
              f"the leg actually stands on")
    slot_in = (pwx - gm_t) / 2               # the slot is the middle two strips
    for (px0, px1, py0, py1), leg_colour in corner_legs:
        # IN A REAR LEG THE FILLER STOPS AT THE REBATE. The back shear wall runs
        # through the slot's back `housed`, so a filler cut to the leg's full
        # depth sits inside the wall - which is exactly what the clash list
        # reported, 36 x 18 x 564, once per rear corner leg.
        fy0 = py0 + housed if py0 <= by0 + 1e-9 else py0
        box("Leg filler block", "legs", leg_colour,
            px0 + slot_in, fy0, grid_lo_bot + gm_h,
            px0 + slot_in + gm_t, py1, grid_hi_top - gm_h,
            d=f"{gm_t:g} x {py1 - fy0:g}, {v['BASE_VOLUME_H']:g} tall "
              f"- it closes the leg's slot between the grids so the two outer "
              f"strips act as one section")

    # ---- the perimeter inner webs ----------------------------------------
    # The INNER lamination of each wall, between the skins. It stays 19 while
    # the outer lamination went to 25: it is a perimeter rib and carries shear.
    # FLAG: WHERE IT SITS IS THE OPEN QUESTION - see BOX_WALL_STANDS_ON. Drawn
    # INBOARD of the skin edge, which is what this model already implied and
    # what the post arithmetic above closes on.
    for x0, y0, x1, y1 in ((0, 0, BW, web), (0, D - web, BW, D),
                           (0, web, web, D - web), (BW - web, web, BW, D - web)):
        box("Perimeter web", "grid", 0xA8822C, x0, y0, cav_z0, x1, y1, cav_z1,
            d="19 inner wall lamination - a perimeter rib, carries shear")

    # ---- the egg crate ----------------------------------------------------
    # CONTINUOUS BOTH WAYS, half-depth notches at every crossing - settled
    # 2026-09-30, and the notches are not drawn: a half-depth notch removes no
    # envelope and drawing it would only hide the bay layout he wants to see.
    #
    # OPEN: THE COUNTS ARE PROVISIONAL. torsion-box.md still lists the grid
    # spacing as open, and BOX_RIBS_FORE_AFT's note carries why four and not
    # five: an odd count puts a rib ON the centreline, where the back tenon is.
    def rib_centres(n, bay, end, lo):
        """Centres of n ribs, from lo, with END bays outside and `bay` between.

        The five bays are NOT equal since 2026-10-14: the inner ones are pinned
        whole millimetres so a tape can walk them, and the remainder goes to the
        two end bays, which keeps every notch offset a whole number. Symmetric,
        so the middle bay still centres on the machine centreline.
        """
        return [lo + end + v["T_BB_RIB"] / 2 + i * (bay + v["T_BB_RIB"])
                for i in range(int(n))]

    # ---- the two blocks beside the back centre tenon ----------------------
    # THE ONLY TENON THAT WANTS THEM: the front corner tenons are snug into the
    # box corners and located by both perimeter walls for free, while this one
    # has the back wall behind it and nothing either side.
    #
    # NOTE: FOR LOCATION, NOT BEARING - the tenon carries no vertical load, all of
    # it is on the shoulder, so these only stop the box walking across.
    #
    # They run forward from the back web to the first across-rib, so each is
    # captured at both ends rather than floating. BACK_TENON_BLOCK_L's note
    # records that the length is his to shorten; the position is settled.
    for bx, sgn_b in ((v["BACK_TENON_BLOCK_X1"], -1), (v["BACK_TENON_BLOCK_X2"], +1)):
        box("Back tenon block", "grid", 0xC2A23F,
            bx, web, cav_z0, bx + sgn_b * v["T_BB_RIB"],
            web + v["BACK_TENON_BLOCK_L"], cav_z1,
            d="location only - the back centre tenon is the one with no wall "
              "either side")

    bw, bf = v["BOX_BAY_W"], v["BOX_BAY_FORE_AFT"]
    ew, ef = v["BOX_BAY_W_END"], v["BOX_BAY_FORE_AFT_END"]
    half = v["T_BB_RIB"] / 2
    desc = f"{v['T_BB_RIB']:g} x {v['BOX_RIB_H']:g}, continuous"
    for cx_ in rib_centres(v["BOX_RIBS_FORE_AFT"], bw, ew, web):
        box("Rib, fore-aft", "grid", 0xD4B24A, cx_ - half, web, cav_z0,
            cx_ + half, D - web, cav_z1, d=desc)
    for cy_ in rib_centres(v["BOX_RIBS_ACROSS"], bf, ef, web):
        box("Rib, across", "grid", 0xD4B24A, web, cy_ - half, cav_z0,
            BW - web, cy_ + half, cav_z1, d=desc)

    # THE TONGUE COVERS THE END GRAIN OF BOTH SKINS - his, 2026-10-11 - so it
    # runs the box's full thickness and stands BOX_TONGUE_PROUD above the top
    # skin: -BOX_THK to +60, which is TONGUE_FULL_H = 204 tall.
    #
    # FLAG: IT USED TO READ -(BOX_THK - SKIN) AND THAT BECAME WRONG ON 2026-10-11.
    # With both skins at 19 that expression gave -119, which WAS the bottom
    # skin's top face, so the tongue stood on it as the prose said. When the
    # top skin went to 25 the expression still gave -119 BY COINCIDENCE - 144
    # less 25 - while the bottom skin's top face moved to -125, leaving the
    # tongue floating 6 above it. A formula that reached for the BOTTOM skin
    # through the TOP skin's symbol only worked while the two were equal.
    tz0, tz1 = -v["BOX_THK"], v["BOX_TONGUE_PROUD"]
    # THE BACK AND FRONT LAP THE SIDES, which is the file's original corner.
    # NOTE: IT WAS REVERSED FOR ONE COMMIT on 2026-10-11 - his preference, the
    # side lapping the back - and reverted the same day for money: a 1235 side
    # will not sit beside the top skin on a 4 x 8 where a 1203.65 one will, and
    # that is a whole sheet of 25 mm at $245. The reversal also drove the side
    # through the rear plate's right end, which overhangs the box by 2.66;
    # SIDE_TONGUE_START's 6.35 exists to clear that plate.
    #
    # THE BACK AND FRONT ARE EACH CUT IN TWO PIECES, butted at mid-length, and
    # they are DRAWN as two - his, 2026-10-11: the model should show what he is
    # building. A butt joint removes no envelope, so this changes no clearance;
    # what it changes is that the seam is there to see and the hover says which
    # half you are on.
    #
    # The joint is sound because the wall is two laminations: the inner web
    # behind it is one continuous piece, so the butt is staggered against solid
    # material. It also lands over the back centre post, so both halves are
    # supported AT the joint rather than it floating between supports. See
    # BACK_LAM_PIECE_L.
    # The joint is at the long piece's end, NOT at the box's middle: the
    # lamination is an odd length and the split goes on a whole millimetre, so
    # the two pieces are 1 apart and the butt sits 0.5 off centre.
    lam_mid = -TT + v["BACK_LAM_PIECE_L"]
    D_LAM_PIECE = (" - ONE OF TWO PIECES, butted just off the box's middle. The "
                   "whole thick sheet fits one 4 x 8 this way and will not at "
                   "full width; the inner web behind the joint is continuous and "
                   "the back centre post sits under it")
    for x0, x1 in ((-TT, lam_mid), (lam_mid, W + TT)):
        box("Back tongue", "tongues", 0xA07B16, x0, -TT, tz0, x1, 0, tz1,
            d=f"{x1 - x0:g} long, {v['T_BOX_TONGUE']:g} thick" + D_LAM_PIECE)
    # EACH SIDE IS ONE BOARD WITH A STEP IN ITS TOP EDGE, and it is split here
    # along the TOP SKIN'S TOP FACE rather than across the board at the saw cut:
    # the full-length piece is what the board is, and the proud band is what
    # stands above the skin behind SIDE_LAM_PROUD_CUT. Split the other way it
    # drew a butt joint at 1006 that does not exist.
    for x0 in (-TT, W):
        box("Side lamination", "tongues", 0xA07B16,
            x0, v["SIDE_TONGUE_START"], tz0, x0 + TT, D, 0,
            d=f"ONE board, {v['SIDE_LAM_L']:.2f} long and "
              f"{v['TONGUE_FULL_H']:g} tall as cut. This is the part of it "
              f"that runs the box's full depth, flush with the top skin")
        box("Side lamination, proud band", "tongues", 0xA07B16,
            x0, v["SIDE_TONGUE_START"], 0, x0 + TT,
            v["SIDE_LAM_PROUD_CUT"], tz1,
            d=f"the same board's top {v['BOX_TONGUE_PROUD']:g}, standing proud "
              f"behind the saw cut at {v['SIDE_LAM_PROUD_CUT']:.2f}. Forward of "
              f"that it is sawn away so the apron stays clear - there is NO "
              f"joint there")

    # ---- the tee track bed -----------------------------------------------
    # The four Mega V tee track plates, 20 thick, BEDDED DIRECTLY ON THE TOP SKIN.
    # The Mega V carries them on three 2040s laid flat at 500 mm centres and the
    # board springs under the cutter because of it; on a continuous skin they are
    # supported everywhere and the 2040s have no job left. So z runs 0 to 20 and
    # there is nothing under them - see machine/spoilboard.md.
    #
    # They run ACROSS the machine at 1193.8, which is SHORTER than the 1204.38
    # between the side plates' inside faces, so TT_BED_SPACER sits at each end
    # rather than the plates being cut. The MDF above them is NOT drawn: it is
    # sacrificial, it gets skimmed, and its thickness is a choice at build time.
    #
    # The fore-aft placement is a PLACEHOLDER - TT_BED_Y0's note says so.
    # THE SLOTS ARE DRAWN AS THE FLATS BETWEEN THEM, with a bar under each slot
    # carrying the plate's bottom 6 across. The flats give the top face and the
    # 8 mm openings exactly; the bar is TT_BED_T - TT_SLOT_DEPTH thick, so the
    # slot reads as the 10 deep pocket it is instead of a hole through the plate -
    # it was a through gap until he gave the depth and the box's top skin showed
    # through every slot from above. THE UNDERCUT IS STILL NOT A FIGURE WE HAVE,
    # so the lips that make it a tee slot are not drawn and the pocket is plain.
    #
    # His breakdown of the 250: 2 x 16 end flats + 7 x 22 inner flats + 8 x 8
    # slots. TT_PLATE_W_CHECK sums it and closes on TT_BED_PLATE_W exactly.
    bed_x0 = v["T_SIDE_PLATE"] + v["TT_BED_SPACER"]
    bed_x1 = bed_x0 + v["TT_BED_L"]
    bed_y0, bed_pw = v["TT_BED_Y0"], v["TT_BED_PLATE_W"]
    n_slots, sw = int(v["TT_SLOTS"]), v["TT_SLOT_W"]
    for i in range(int(v["TT_BED_PLATES"])):
        py0 = bed_y0 + i * bed_pw
        # Walk the plate's depth: end flat, then slot / inner flat alternating,
        # then the far end flat. The cursor is what guarantees the flats and the
        # slots cannot drift apart - there is no second expression for either.
        y = py0
        runs = [v["TT_END_FLAT"]]
        for j in range(n_slots):
            runs.append(("slot", sw))
            runs.append(v["TT_MID_FLAT"] if j < n_slots - 1 else v["TT_END_FLAT"])
        slot_floor = v["TT_BED_T"] - v["TT_SLOT_DEPTH"]
        for run in runs:
            if isinstance(run, tuple):
                # a slot: the plate's bottom 6 runs on under it
                box("Tee track slot bottom", "bed", 0xB0B6BC, bed_x0, y, 0,
                    bed_x1, y + run[1], slot_floor,
                    d="the floor of an 8 x 10 slot - the plate's bottom "
                      f"{slot_floor:g} carrying on under the gap. The undercut "
                      "that makes it a tee slot is not a figure we have",
                    u=f"bed{i}")
                y += run[1]
                continue
            box("Tee track flat", "bed", 0xB0B6BC, bed_x0, y, 0,
                bed_x1, y + run, v["TT_BED_T"],
                d="16 thick, bedded on the skin - the gaps are the 8 mm slots, "
                  "10 deep, whose undercut is not a figure we have",
                u=f"bed{i}")
            y += run
        # Belt and braces: the walk has to land exactly on the plate's far edge.
        if abs(y - (py0 + bed_pw)) > 1e-6:
            print(f"tee track plate {i}: flats and slots sum to {y - py0}, "
                  f"not {bed_pw}", file=sys.stderr)
            return 2
    # ---- the MDF spoilboard over the aluminium ---------------------------
    # TWO SHEETS OF 25 ULTRA LITE MDF, his 2026-10-11, which is what makes the
    # bed a work surface the tool can actually reach: the tip floor is 45.2 above
    # the box's top skin and a fresh surface here is SPOIL_SURFACE = 66, so the
    # machine can skim its own board. The upper sheet is the sacrificial one.
    #
    # THE SHEET IS SMALLER THAN THE ALUMINIUM UNDER IT and that is his call: it
    # only has to cover the range the tool can reach. FLUSH WITH THE BED'S FRONT
    # EDGE, SPOIL_BACK_SHY off the rear plate, SPOIL_SIDE_SHY off each side
    # plate's inside face - his, 2026-10-11.
    #
    # It also settles a clash the full footprint had: eight tongue bolt heads
    # stand 4 mm proud of the bed's back edge, up at z 21.35 to 38.65, straight
    # through the lower sheet. 200 of setback leaves them in clear air.
    mdf_t = v["MDF_LAYER_T"]
    bed_y1 = bed_y0 + int(v["TT_BED_PLATES"]) * bed_pw
    mdf_x0 = v["T_SIDE_PLATE"] + v["SPOIL_SIDE_SHY"]
    mdf_x1 = W - v["T_SIDE_PLATE"] - v["SPOIL_SIDE_SHY"]
    mdf_y0 = v["T_REAR_PLATE"] + v["SPOIL_BACK_SHY"]
    for i in range(int(v["MDF_LAYERS"])):
        z0 = v["TT_BED_T"] + i * mdf_t
        top = i == int(v["MDF_LAYERS"]) - 1
        box("MDF sacrificial sheet" if top else "MDF sheet", "spoil", 0xC2A878,
            mdf_x0, mdf_y0, z0, mdf_x1, bed_y1, z0 + mdf_t,
            d=f"{mdf_t:g} ultra lite MDF" + (
               f" - the sacrificial sheet, surfaced in place. A fresh surface is "
               f"{v['SPOIL_SURFACE']:g} above the box's top skin and the tool tip "
               f"floor is 45.2, so the machine can skim it"
               if top else " - the lower sheet, held down by tee nuts in the track"))

    # ---- the four T-bolts that hold the MDF down -------------------------
    # HIS SCHEME, 2026-10-11: drill 8 through both sheets at the four corners,
    # counterbore from the top for the washer and nut, drop the T-bolts in the
    # holes, set the sandwich on the aluminium, turn each bolt so its T lines
    # up with the slot, let it drop and tighten.
    #
    # THE HOLES HAVE TO LAND ON REAL SLOT CENTRES, so they are worked out from
    # the slot walk above rather than from a pitch - and then CHECKED. His rule
    # is "20 in from the front corner, then back in multiples of 30 while
    # staying 20 clear of the back edge", and he is right that a multiple of 30
    # only walks slots WITHIN one 250 panel: across a join the step is 40. It
    # happens to close here because 25 x 30 is also 3 x 250, the same slot three
    # panels along. That coincidence is exactly the kind that stops holding
    # quietly when a number moves, so the assert below is not decoration.
    slot_centres = []
    for i in range(int(v["TT_BED_PLATES"])):
        y = bed_y0 + i * bed_pw + v["TT_END_FLAT"]
        for j in range(n_slots):
            slot_centres.append(y + sw / 2)
            y += sw + (v["TT_MID_FLAT"] if j < n_slots - 1 else 0)

    bolt_front_y = bed_y1 - v["SPOIL_BOLT_INSET"]
    bolt_back_y = v["SPOIL_BOLT_BACK_Y"]
    for label, by in (("front", bolt_front_y), ("back", bolt_back_y)):
        off = min(abs(c - by) for c in slot_centres)
        if off > 1e-6:
            print(f"the {label} T-bolt row at {by:.3f} is not on a slot centre "
                  f"- nearest is {off:.3f} away. Move SPOIL_BOLT_INSET or "
                  f"SPOIL_BOLT_BACK_Y onto the grid.", file=sys.stderr)
            return 2
    if bolt_back_y - mdf_y0 < v["SPOIL_BOLT_INSET"]:
        print(f"the back T-bolt row is {bolt_back_y - mdf_y0:.1f} from the "
              f"MDF's back edge, inside the {v['SPOIL_BOLT_INSET']:g} he set",
              file=sys.stderr)
        return 2

    # The thread tops out at the work surface; the nut and its washer sit in a
    # counterbore below it, because the sacrificial sheet gets skimmed and a nut
    # proud of the surface is what the cutter finds.
    thread_top = v["TT_BED_T"] + v["SPOIL_BOLT_RISE"]
    cbore_z = v["SPOIL_CBORE_Z"]
    wash_r, nut_r = v["M8_WASHER_D"] / 2, v["ACORN_NUT_D"] / 2
    D_TBOLT = (M8_HEAD(None) + " - M8 drop-in T-bolt, the T drops into the "
               "slot and turns to "
               "catch. " + str(v["SPOIL_BOLT_RISE"]) + " of thread above the "
               "aluminium puts its top level with the work surface. \u26a0 THE "
               "RISE IS HIS PICK, NOT A MEASUREMENT - see open-items.md. The T "
               "itself is not drawn: its size is not a figure we have")
    for bx in (mdf_x0 + v["SPOIL_BOLT_INSET"], mdf_x1 - v["SPOIL_BOLT_INSET"]):
        for by in (bolt_back_y, bolt_front_y):
            # the clearance hole through both sheets, and the counterbore over it
            cyl("Spoilboard bolt hole", "spoil", HOLE, bx, by,
                v["TT_BED_T"], cbore_z, v["BEAM_BOLT_CLEARANCE"] / 2,
                seg=12, d="8 through both sheets, drilled before the sandwich "
                          "goes down")
            cyl("Spoilboard counterbore", "spoil", HOLE, bx, by,
                cbore_z, v["SPOIL_SURFACE"], wash_r, seg=16,
                d="sunk to clear the washer and bring the nut below the "
                  "surface - the floor is at " + f"{cbore_z:g}" + ", which is "
                  "the surface less the nut and the washer")
            # the bolt, from inside the slot up to the surface
            cyl("Spoilboard T-bolt", "spoil", 0x8A939B, bx, by,
                v["TT_BED_T"] - v["TT_SLOT_DEPTH"], thread_top,
                v["TT_BED_END_BOLT"] * 0.8, seg=12, d=D_TBOLT)
            cyl("Spoilboard washer", "spoil", 0x9AA3AB, bx, by,
                cbore_z, cbore_z + v["M8_WASHER_T"], wash_r, seg=20,
                d="plain M8 flat washer - his, 2026-10-11, over the fender "
                  "this was first drawn with: it bears on MDF in a counterbore, "
                  "not on a face that could pull through")
            cyl("Spoilboard nut", "spoil", 0x5A6068, bx, by,
                cbore_z + v["M8_WASHER_T"], v["SPOIL_SURFACE"], nut_r,
                seg=6, d="plain M8 nut, finishing level with the surface at "
                         "worst - it must never stand proud of a sheet the "
                         "machine skims")

    # THE TT_BED_SPACER GAP AT EACH END IS NOT DRAWN, and that is right rather
    # than missing: it is taken up by a WASHER STACK ON EACH BOLT - his, 2026-10-11
    # - so there is no part with a footprint here to draw. It was briefly modelled
    # as a 5.29 x 1000 x 16 bar at each end, which both invented a part and implied
    # a flat bar in a thickness nobody stocks.

    # ---- the front cap and the two side caps ------------------------------
    # The front has NO TONGUE: this cap is the same 25 stock and the same 44
    # wall section as the other three sides, but it stops FLUSH with the top
    # skin instead of standing BOX_TONGUE_PROUD above it - his, 2026-10-11, so
    # the apron stays a clear work surface.
    #
    # SETTLED: IT CLOSES ON THE POST WITHOUT ANYTHING BEING CHOSEN: the front post's
    # full section reaches D - web + ledge = 1235, and the cap occupies D to
    # D + 25 = 1210 to 1235. The 44 wall is web (1191..1210) plus cap
    # (1210..1235), landing squarely on the 44 shoulder, exactly as at the sides.
    #
    # The front fin overhangs outboard by FIN_PROUD where the side lamination
    # runs flush with the skin, and lands on its top edge rather than hanging in
    # midair - his words. That stretch is part of the side lamination itself,
    # drawn with it above.
    cap_t = v["T_BOX_FRONT_CAP"]
    cap_z0 = -v["BOX_FRONT_CAP_H"]
    # Two pieces, the same as the back and for the same reason.
    for x0, x1 in ((-cap_t, lam_mid), (lam_mid, W + cap_t)):
        box("Front cap", "tongues", 0xA07B16, x0, D, cap_z0, x1, D + cap_t, 0,
            d=f"{x1 - x0:g} long, {cap_t:g} thick, flush with "
              f"the top skin - the front has no tongue" + D_LAM_PIECE)
    # FLAG: THERE IS NO SEPARATE SIDE CAP. Each side's outer lamination is ONE
    # piece, SIDE_LAM_L long and TONGUE_FULL_H tall, with the proud portion
    # forward of SIDE_LAM_PROUD_CUT sawn away - it is drawn with the tongues
    # above, split along the top skin's face so no joint appears at the cut.

    # ---- the plates that stand on the skin -------------------------------
    # ITS LEFT EDGE IS ON THE Y1 EXTRUSION'S OUTBOARD FACE, not on the side
    # plate's - his, 2026-10-10 - and it is drawn at the length it was BOUGHT,
    # REAR_PLATE_L_ORDERED, rather than at the flush envelope MACHINE_OUTER_W. The
    # side plate at each end is outboard of it, and the far end runs past the
    # machine's outer width by whatever the delivered piece gives.
    #
    # IT CARRIES THE TWO WINDOWS NOW - his flip, 2026-10-13. The casting and
    # interposer pass through the REAR plane, which is the thing the 2026-10-02
    # arrangement had stopped happening and is why one monolithic rear plate
    # became practical in the first place. It stays monolithic: the windows are
    # 60.5 apertures in a 1210.73 plate, nowhere near its ends.
    #
    # Each window's OUTBOARD edge lands on its Y beam's outer face, which is the
    # same rule the fin's window followed - the casting is centred on the beam
    # at either end, so the station is the beam's and not the plate's.
    rpx = v["Y1_EXT_FACE_X"]
    # FLAG: THE TWO WINDOWS MIRROR, they do not repeat. Each one's OUTBOARD edge
    # is on its own beam's outer face, and Y1's outer face is its low-X side
    # while Y2's is its high-X side. Drawing both from the low-X side puts Y2's
    # window 0.5 out - WINDOW_W is 60.5 over a 60 casting, so the clash check
    # cannot see it and it would have reached the sheet as a real offset.
    # EACH WINDOW IS A T, and it hangs from the BEAM'S UNDERSIDE rather than
    # standing on a bottom edge: the full-width opening runs WINDOW_H down from
    # there, and PROBE_NOTCH_W carries on PROBE_NOTCH_H below it. The notch
    # clears the back of the proximity probe body, and it is also how the
    # casting and interposer go in - through the window from behind, BK12 end
    # first. PROBE_NOTCH_R is NOT DRAWN, the same call as SOLE_FILLET_R: a
    # polygon approximation of it would then disagree with the sheet.
    _rp_top = v["Y_BEAM_UNDERSIDE"]
    _rp_mid = v["WINDOW_BOTTOM_Y"]
    _rp_bot = v["PROBE_NOTCH_BOTTOM_Y"]
    _y1x = v["Y1_EXT_FACE_X"]
    _y2x = _y1x + v["Y2_EXT_FACE_X"] - v["EXT_W"]
    _nin = (v["WINDOW_W"] - v["PROBE_NOTCH_W"]) / 2
    rp_wins = [[[xa, _rp_top], [xb, _rp_top], [xb, _rp_mid],
                [xb - _nin, _rp_mid], [xb - _nin, _rp_bot],
                [xa + _nin, _rp_bot], [xa + _nin, _rp_mid], [xa, _rp_mid]]
               for xa, xb in ((_y1x, _y1x + v["WINDOW_W"]),
                              (_y2x + v["EXT_W"] - v["WINDOW_W"],
                               _y2x + v["EXT_W"]))]
    prism("Rear plate", "plates", 0x8899AA,
          [[rpx, 0], [rpx + v["REAR_PLATE_L_ORDERED"], 0],
           [rpx + v["REAR_PLATE_L_ORDERED"], v["REAR_PLATE_W"]],
           [rpx, v["REAR_PLATE_W"]]],
          0, v["T_REAR_PLATE"], holes=rp_wins, d=sheet_note("7"))

    sp = v["T_SIDE_PLATE"]
    y0, y1 = v["SIDE_TONGUE_START"], v["SIDE_TONGUE_END"]
    for x0 in (0.0, W - sp):
        box("Side plate", "plates", 0x8899AA, x0, y0, 0, x0 + sp, y1, v["SIDE_PLATE_H"])

    # ---- Y beams ---------------------------------------------------------
    # The beam's height comes from the FIN, not the side plate: the window's top
    # edge is the beam's underside. 182 + 120 lands on FIN_STOCK's measured 302,
    # which is the cross-check that this chain closes.
    ybot = v["Y_BEAM_UNDERSIDE"]
    ytop = ybot + v["BEAM_H"]
    # Y2_EXT_FACE_X IS A SHEET 7 COORDINATE, off the Y1 extrusion's outboard face,
    # so the machine X adds Y1_EXT_FACE_X the same way the RP_ columns do.
    lx0 = v["Y1_EXT_FACE_X"]
    rx0 = lx0 + v["Y2_EXT_FACE_X"] - v["EXT_W"]
    for x0 in (lx0, rx0):
        box("Y beam", "ybeams", 0x4A7DB5, x0, y0, ybot, x0 + v["EXT_W"], y1, ytop)

    # ---- front fins ------------------------------------------------------
    # They CAP THE Y BEAM'S FRONT END - plane normal to fore-aft, like the rear
    # plate does at the back - and the taper faces INBOARD, so the outboard edge
    # is square. Corrected 2026-10-03; the first model had them on the beams'
    # sides, which is the wrong plane entirely.
    fb, ft, h = v["FIN_BASE_W"], v["FIN_TOP_W"], v["FIN_STOCK"]
    wo, ww = v["WINDOW_OUTB_DRAWN"], v["WINDOW_W"]
    wz0, wz1 = v["WINDOW_Z_LOW"], v["WINDOW_Z_LOW"] + v["WINDOW_H"]
    for outer, sgn in ((0 - v["FIN_PROUD"], +1), (W + v["FIN_PROUD"], -1)):
        # The window's outboard edge lands on the Y beam's OUTER FACE - 3.175 and
        # 1208.575 - which is what Sheet 1 says it is aligned to, and the check
        # that WINDOW_OUTB_DRAWN's 20 is right where the measured 19 is not.
        # NO WINDOW IN THE FIN ANY MORE - his flip, 2026-10-13. It moved to the
        # rear plate with the casting, and the fin instead carries BF12's four
        # tapped M5. The plate is SOLID here: the holes are tapped and the bolts
        # are drawn through them, which the pair list covers.
        # 1a is the Y1 end, 1b the Y2 end - and the pack calls Y1 the left,
        # which is the left of a view taken from BEHIND, the frame X runs in.
        prism("Front fin", "plates", 0x6FA8DC,
              [[outer, 0], [outer + sgn * fb, 0],
               [outer + sgn * ft, h], [outer, h]],
              y1, y1 + v["T_FIN"],
              d=sheet_note("1a" if sgn > 0 else "1b"))

    # ---- the angle that ties each front fin down --------------------------
    # ONE 170 piece per fin, in FRONT of it - 2026-10-11. In front because the
    # tee track bed's front edge and the fin's back face are BOTH at 1006.35,
    # leaving zero room behind; the bed decision the same day closed that space.
    #
    # It starts FLUSH WITH THE BOX'S SIDE EDGE and runs inboard, not flush with
    # the fin: the fin stands FIN_PROUD outboard, so an angle on the fin's edge
    # would have its first 16.571 hanging in air with no skin to bolt into.
    #
    # The 170 is his, measured off the fin's tapered edge at the leg's top and
    # rounded - it finishes 0.17 inside the taper and reads flush. That tightness
    # is the point: the failure here is cosmetic, and margin would show as a step.
    #
    # OPEN: FIN_ANGLE_T is a NOMINAL - the piece has not been calipered. It feeds
    # nothing; it is here so the angle is not a zero-thickness plane.
    at = v["FIN_ANGLE_T"]
    aleg, alen = v["FIN_ANGLE_LEG"], v["FIN_ANGLE_L"]
    fin_front = y1 + v["T_FIN"]
    for xa, sgn in ((0.0, +1), (W, -1)):
        xb = xa + sgn * alen
        lo, hi = min(xa, xb), max(xa, xb)
        # vertical leg, against the fin's front face
        box("Fin angle", "plates", 0x9AA5B1, lo, fin_front, 0,
            hi, fin_front + at, aleg,
            d="40 x 40, 170 long - two M8 into TAPPED holes in the fin at Y 20")
        # horizontal leg, on the top skin
        box("Fin angle", "plates", 0x9AA5B1, lo, fin_front + at, 0,
            hi, fin_front + aleg, at,
            d="three bolts into pronged T-NUTS in the top skin - fitted from "
              "underneath BEFORE the skin is glued")
        # T1 and T2 - the two M8 through the angle's VERTICAL leg into the fin's
        # TAPPED holes at FIN_BRACKET_BOLT_Y. Their X comes off the FIN's own
        # outboard edge, confirmed by him 2026-10-11, which is FIN_PROUD outside
        # the box edge - so T1 ends up only FIN_ANGLE_T1_END from the angle's
        # near end, a known thin spot recorded rather than designed away.
        fin_edge = xa - sgn * v["FIN_PROUD"]
        for bolt_x in (v["FIN_TONGUE_BOLT_1"], 170.0):
            cyl("Fin T bolt", "bolts", 0xC8CDD3,
                fin_edge + sgn * bolt_x, v["FIN_BRACKET_BOLT_Y"],
                fin_front + at, fin_front + at + v["FLANGE_LOW_H"],
                v["FLANGE_LOW_D"] / 2, axis="y",
                d=M8_HEAD("fin-to-angle") + " - into a TAPPED hole in the "
                  "fin, no nut, because the tee track bed is hard against the "
                  "fin's back face" + blen("fin-to-angle"))

        # The LOW PROFILE M8 flange heads - 13.75 across and only 3 proud,
        # which is why
        # they suit a bracket out on the apron where anything tall catches a
        # workpiece. NOT M8_HEAD_D's plain hex, which is a different fastener.
        #
        # THE EXTRUSION COMES WITHOUT HOLES, so this is a pattern he drills:
        # THREE at 30, 85 and 140 from the near end - his, 2026-10-11, cutting
        # four down as unnecessary over 170. Measured from the end that starts
        # flush with the box's side edge, so the right-hand angle mirrors.
        # The margins match at 30 and the middle lands on the centre;
        # FIN_ANGLE_BOLT_END_MARGIN is the symbol that holds that closed.
        bp, b1 = v["FIN_ANGLE_BOLT_PITCH"], v["FIN_ANGLE_BOLT_FIRST"]
        by = fin_front + at + (aleg - at) / 2        # centred in the free leg
        for i in range(int(v["FIN_ANGLE_SKIN_FIX"])):
            cyl("Fin angle bolt", "bolts", 0xC8CDD3,
                xa + sgn * (b1 + i * bp), by, at,
                at + v["FLANGE_LOW_H"], v["FLANGE_LOW_D"] / 2,
                d=M8_HEAD("fin-angle-to-skin") + " - into a pronged T-nut in "
                  "the top skin" + blen("fin-angle-to-skin"))

    # ---- the interposer, under each beam and out through the window -------
    # Four M8 into slide-in T-nuts hold each bar on, at Sheet 6's two rows
    # measured from the bar's OUTBOARD end and on the extrusion's own two slot
    # centrelines across the 60. There is no third row: the bar slides back
    # along the beam to seat the screw's journal in the casting, which brings
    # the casting's footprint over the bar's first 72.5.
    ip_t = v["T_INTERPOSER"]
    ip_rows = (v["INTERPOSER_BOLT_ROW_1"], v["INTERPOSER_BOLT_ROW_2"])
    ip_slots = (v["RAIL_SLOT_INSET"], v["RAIL_SLOT_INSET"] + v["SLOT_GRID"])

    def interposer_bolts(along, across0, outb, along_axis, seat, up, jid):
        """outb is the bar's outboard end; the rows run back from it. seat is
        the bar's face away from the beam, up the way the head stands off it."""
        for r in ip_rows:
            for s in ip_slots:
                a, c = outb - along * r, across0 + s
                cx, cy = (c, a) if along_axis == "y" else (a, c)
                cyl("Flange head", "bolts", 0x3C4248, cx, cy,
                    seat, seat + up * v["FLANGE_NORMAL_H"],
                    v["FLANGE_NORMAL_D"] / 2, seg=12, d=D_TNUT(jid))
                cyl("Interposer bolt", "bolts", 0x3C4248, cx, cy,
                    seat, seat - up * ip_t,
                    v["BEAM_BOLT_CLEARANCE"] / 2 - 0.5, seg=10, d=D_TNUT(jid))

    # ITS OUTBOARD END IS THE REAR ONE NOW. INTERPOSER_PROUD is measured past
    # the rear plate's INSIDE face, going back, so the bar's outboard end lands
    # at T_REAR_PLATE less that - which is negative, i.e. behind the plate's
    # outer face, exactly as the casting's motor end is.
    ip_rear = v["T_REAR_PLATE"] - v["INTERPOSER_PROUD"]
    for x0 in (lx0, rx0):
        box("Interposer", "ybeams", 0xC0652A, x0, ip_rear,
            ybot - ip_t, x0 + v["INTERPOSER_W"], ip_rear + v["INTERPOSER_L"], ybot)
        # it HANGS under the beam, so these drive upward and the heads are below
        interposer_bolts(-1, x0, ip_rear, "y", ybot - ip_t, -1,
                         "y-interposer-to-beam")

    # ---- X gantry, at Y home ---------------------------------------------
    # EVERYTHING FROM HERE RIDES THE Y CARRIAGE until the cursor says otherwise.
    ride[0] = "Y"
    xep_t = v["T_X_ENDPLATE"]
    xb_x0 = lx0 + v["EXT_W"] + v["RAIL_STACK"] + xep_t
    xb_x1 = xb_x0 + v["BEAM_LEN"]
    # MID TRAVEL ON ALL THREE AXES, so nothing on the rear plate or the beams is
    # hidden behind the gantry. Y runs from the end plate's back edge level with
    # the beam's back end to its front face level with the front end.
    xep_back = (y0 + (y1 - v["XEP_W"])) / 2
    xep_front = xep_back + v["XEP_W"]
    xb_top = ytop + v["XEP_TOP_ABOVE_BEAM"]
    xb_bot = xb_top - v["BEAM_H"]
    box("X beam", "gantry", 0x4A7DB5, xb_x0, xep_back, xb_bot,
        xb_x1, xep_back + v["EXT_W"], xb_top)
    # The plate is drawn at XEP_CUT, what Sheet 2a actually cuts, not at XEP_H,
    # which is only the floor it has to beat. Its TOP is fixed at the X beam's
    # upper extrusion, so the extra 7.5 hangs DOWN as spare metal.
    xep_bot = xb_top - v["XEP_CUT"]
    for x0 in (xb_x0 - xep_t, xb_x1):
        box("X end plate", "gantry", 0x6FA8DC,
            x0, xep_back, xep_bot, x0 + xep_t, xep_front, xb_top,
            # 2a is both plates; 2b is the min X one, which carries the tongue
            d=sheet_note("2a and 2b" if x0 < xb_x0 else "2a"))
        # It runs the plate's FULL 154 fore-aft, not DOUBLER_H - the four
        # stations D1-D4 that bolt it on are spread across that 154. DOUBLER_H
        # is its 45 UP the plate, the offcut width.
        #
        # ITS END FACE IS THE NUT PLANE, NOT THE PLATE'S BOTTOM EDGE. The plate
        # reaches XEP_SOLE_TAB further down so the sole plate's base has a face
        # to butt, so the block starts DOUBLER_BOTTOM_X up from xep_bot - and
        # that is the whole 10 mm of difference the joint was changed for.
        doub_bot = xep_bot + v["DOUBLER_BOTTOM_X"]
        box("Y nut doubler", "gantry", 0xB06000,
            x0 - v["T_DOUBLER"] if x0 < xb_x0 else x0 + xep_t, xep_back,
            doub_bot,
            x0 if x0 < xb_x0 else x0 + xep_t + v["T_DOUBLER"],
            xep_front, doub_bot + v["DOUBLER_H"])

        # ---- four M8 into the X beam's TOP extrusion end bores ----------
        # The plate bolts to the beam's end, and the bores are EXT_BORE_INSET
        # in from each of the four faces - so fore-aft they are XEP_BOLT_REAR
        # and _FRONT off the plate's back edge, and in Z the same inset down
        # from the beam's top and up from the top extrusion's own bottom. Head
        # on the plate's OUTBOARD face, shank through the plate into the bore.
        # They clear the Y bearing blocks, which stop at the upper rail.
        outer = x0 if x0 < xb_x0 else x0 + xep_t
        faceward = -1 if x0 < xb_x0 else +1
        for by in (v["XEP_BOLT_REAR"], v["XEP_BOLT_FRONT"]):
            for bz in (xb_top - v["EXT_BORE_INSET"],
                       xb_top - v["EXT_W"] + v["EXT_BORE_INSET"]):
                cyl("Flange head", "bolts", 0x3C4248, xep_back + by, bz,
                    outer, outer + faceward * v["FLANGE_NORMAL_H"],
                    v["FLANGE_NORMAL_D"] / 2, axis="x", seg=12,
                    d=D_BEAM_END("xep-to-xbeam"))
                cyl("X end plate bolt", "bolts", 0x3C4248, xep_back + by, bz,
                    outer, outer - faceward * xep_t,
                    v["BEAM_BOLT_CLEARANCE"] / 2 - 0.5, axis="x", seg=10,
                    d=D_BEAM_END("xep-to-xbeam"))

        # ---- the shelf bar, carrying the X beam off this plate ----------
        # It stands INBOARD off the plate's face with the beam's underside
        # resting on its top, 60 fore-aft so it covers the beam's footprint
        # exactly. Two M8 up into the extrusion's two underside slots, two
        # more horizontally into the bar's side through the plate - those are
        # BLIND-tapped, because through-drilling would break out where the
        # lower Y bearing block sits.
        inb = +1 if x0 < xb_x0 else -1
        bar_face = x0 + xep_t if x0 < xb_x0 else x0
        bar_top = ytop + v["SHELF_BAR_TOP"]
        bar_bottom = ytop + v["SHELF_BAR_BOTTOM"]
        box("Shelf bar", "gantry", 0x7E6B8F,
            bar_face, xep_back, bar_bottom,
            bar_face + inb * v["SHELF_BAR_W"], xep_back + v["SHELF_BAR_L"], bar_top)
        bar_mid = bar_face + inb * v["SHELF_BAR_W"] / 2
        shank8 = v["BEAM_BOLT_CLEARANCE"] / 2 - 0.5
        for sy in (v["SHELF_VERT_REAR"], v["SHELF_VERT_FRONT"]):
            cyl("Shelf bolt head", "bolts", 0x3C4248, bar_mid, xep_back + sy,
                bar_bottom, bar_bottom - v["M8_HEAD_H"],
                v["M8_HEAD_D"] / 2, seg=12, d=D_SHELF_V("shelf-bar-vertical"))
            cyl("Shelf bolt", "bolts", 0x3C4248, bar_mid, xep_back + sy,
                bar_bottom, bar_top, shank8, seg=10, d=D_SHELF_V("shelf-bar-vertical"))
        # The horizontal pair are driven from the BAR side, head on the bar's
        # inboard face and the shank running back through it into the plate.
        # They cannot come the other way: Sheet 2a's H1 and H2 are blind-
        # tapped precisely because through-drilling breaks out on the plate's
        # outboard face, and that is where the lower Y bearing block sits -
        # the model showed the head inside the block when it was drawn that
        # way round.
        # ASSUMPTION: drawn to the plate's mid-thickness. The registry gives
        # the stations but no blind-tap depth.
        plate_mid = (x0 + x0 + xep_t) / 2
        bar_out = bar_face + inb * v["SHELF_BAR_W"]
        for sz in (v["SHELF_HORIZ_Z_LOW"], v["SHELF_HORIZ_Z_HIGH"]):
            hz = bar_bottom + sz
            cyl("Shelf bolt head", "bolts", 0x3C4248,
                xep_back + v["SHELF_HORIZ_Y"], hz,
                bar_out, bar_out + inb * v["FLANGE_LOW_H"],
                v["FLANGE_LOW_D"] / 2, axis="x", seg=12,
                d=D_SHELF_H("shelf-bar-horizontal"))
            cyl("Shelf bolt", "bolts", 0x3C4248,
                xep_back + v["SHELF_HORIZ_Y"], hz, bar_out, plate_mid, shank8,
                axis="x", seg=10, d=D_SHELF_H("shelf-bar-horizontal"))

    # THE BF12 TONGUE, on the MIN X plate only - the operator's right, and the
    # left of a view taken from behind the machine. It carries on past the 2a
    # outline to TONGUE_TOP, 60 wide fore-aft so it sits over the beam, and BF12
    # bolts to its inboard face. The check that it is in the right place: the
    # sheet puts the first BF12 row at TONGUE_BF12_ROW1 up from the plate's
    # bottom, which lands at the beam top plus the interposer plus BF12's own 7.
    box("BF12 tongue", "gantry", 0x6FA8DC,
        xb_x0 - xep_t, xep_back, xb_top,
        xb_x0, xep_back + v["EXT_W"], xb_top + v["TONGUE_H"])

    # ---- X carriage, at mid travel ----------------------------------------
    ride[0] = "YX"
    # The X rails sit RAIL_LOW_Z up the beam's front face; Sheet 3 puts the lower
    # block row's centre 46 up the carriage plate, so the plate's bottom follows.
    xbeam_front = xep_back + v["EXT_W"]
    cp_bot = xb_bot + v["RAIL_LOW_Z"] - 46.0
    # X 0 is the rear plate's left as seen FROM BEHIND, so the operator standing at
    # the front has it on their right, and X HOME - the operator's left - is MAX X
    # in this frame rather than min. It matters for reading the view even with the
    # carriage parked in the middle.
    cp_x1 = (xb_x0 + v["XEP_W"] + xb_x1) / 2
    cp_x0 = cp_x1 - v["XEP_W"]
    # The plate bolts to the BLOCKS, so it stands RAIL_STACK off the beam's face -
    # not on it. Caught by the interference check on 2026-10-03, which had the X
    # rail passing straight through the plate; everything on the Z axis moved
    # forward 30 with it.
    cp_back = xbeam_front + v["RAIL_STACK"]
    box("X carriage plate", "z", 0xD98E04, cp_x0, cp_back, cp_bot,
        cp_x1, cp_back + v["T_X_CARRIAGE_PLATE"], cp_bot + 407.0)

    # ---- the X nut doubler and sole plate, on the plate's BACK face --------
    # The X ball nut sits above the beam BEHIND this plate, so the doubler
    # stands off the plate's back face and the sole plate laps from its top
    # edge out over the nut.
    #
    # BOTH ARE ANCHORED TO THE X BEAM'S TOP, not to the carriage plate's
    # bottom - his, 2026-10-10. The nut's face is 55 above the beam top, ten
    # of interposer, twenty-five to the casting's bore, twenty from the bore
    # to the nut's face, and the 45 doubler hangs from that, which lands its
    # bottom edge 10 above the beam top. The upper bearing blocks stand 10
    # proud of the beam top as well, so THE DOUBLER RESTS ON THEIR SIDES -
    # fine, because both parts are fixed by the same carriage plate.
    #
    # Referenced this way they meet the nut by construction. The registry
    # reaches the same two planes from the carriage plate's bottom, at
    # X_DOUBLER_BOTTOM and X_NUT_FACE_Z, and those run through a measured
    # X_BEAM_TOP_XC of 167 where the model's rails and blocks put the beam top
    # 151 above that edge - see the open item; nothing here resolves it.
    #
    # ASSUMPTION: both are drawn the carriage plate's own 154 across. The
    # sheets give their lengths and rows, not a width.
    x_nut_face = (xb_top + v["T_INTERPOSER"] + v["CASTING_AXIS_ABOVE_FOOT"]
                  + v["NUT_AXIS_TO_FACE"])
    box("X nut doubler", "gantry", 0xB06000,
        cp_x0, cp_back - v["T_DOUBLER"], x_nut_face - v["DOUBLER_H"],
        cp_x1, cp_back, x_nut_face)
    # X_SOLE_BRACKET_L is measured from the carriage plate's back face, so it
    # covers the doubler's 12.19 and then SOLE_REACH of free span to the nut.
    box("X sole plate", "gantry", 0xC9A227,
        cp_x0, cp_back - v["X_SOLE_BRACKET_L"], x_nut_face,
        cp_x1, cp_back, x_nut_face + v["T_SOLE_BRACKET"])

    # ---- Z plate and spindle, at Z max -----------------------------------
    ride[0] = "YXZ"
    cp_front = cp_back + v["T_X_CARRIAGE_PLATE"]
    rail_top = cp_bot + 407.0 - 7.0
    block_mid = (rail_top + cp_bot + 7.0) / 2            # mid travel, as above
    zp_back = cp_front + v["RAIL_STACK"] + v["SPACER_T"]
    zp_cx = (cp_x0 + cp_x1) / 2
    box("Z plate", "z", 0xD98E04,
        zp_cx - v["Z_PLATE_W"] / 2, zp_back, block_mid - v["Z_PLATE_L"] / 2,
        zp_cx + v["Z_PLATE_W"] / 2, zp_back + v["T_Z_PLATE"],
        block_mid + v["Z_PLATE_L"] / 2)

    # The spindle axis is CLAMP_BORE_OFFSET off the Z plate's FRONT face - that
    # term is what makes SPINDLE_OFFSET add up from the carriage plate.
    zp_front = zp_back + v["T_Z_PLATE"]
    sp_axis = zp_front + v["CLAMP_BORE_OFFSET"]
    r = v["SPINDLE_D"] / 2
    bar_bot = block_mid - v["SPINDLE_BARREL_L"] / 2
    cyl("Spindle barrel", "z", 0x9AA3AB, zp_cx, sp_axis,
        bar_bot, bar_bot + v["SPINDLE_BARREL_L"], r)
    # The nose: a SPINDLE_NOSE_D boss stepping out of the barrel as far as the
    # shoulder, then the shaft the collet nut screws onto. Neither was drawn and
    # the view showed the barrel ending in air above the nut. The nut OVERLAPS
    # the shaft - it seats where the thread starts, not at the shoulder.
    shoulder = bar_bot - v["SPINDLE_SHOULDER_DROP"]
    cyl("Spindle nose", "z", 0x9AA3AB, zp_cx, sp_axis,
        shoulder, bar_bot, v["SPINDLE_NOSE_D"] / 2)
    cyl("Spindle shaft", "z", 0x8A9097, zp_cx, sp_axis,
        shoulder - v["SPINDLE_SHAFT_L"], shoulder, v["SPINDLE_SHAFT_D"] / 2)
    nut_end = bar_bot - v["SPINDLE_COLLET_END"]
    cyl("Collet nut", "z", 0x2E2E2E, zp_cx, sp_axis,
        nut_end, nut_end + v["SPINDLE_NUT_L"], v["SPINDLE_NUT_D"] / 2)

    # The tool, for the view only. It hangs TOOL_L out of the collet nut's face
    # on the spindle axis, and ITS TIP IS WHAT THE DRO READS - the one point on
    # the machine an operator actually cares about. Stickout, not a cutter's
    # overall length: how much of a real tool is in the collet is not something
    # the model can know.
    tool_tip = nut_end - v["TOOL_L"]
    cyl("Tool", "z", 0xE8B64C, zp_cx, sp_axis, tool_tip, nut_end,
        v["TOOL_D"] / 2, seg=16,
        d="a stand-in cutter, 1/4in by 2in of stickout - NOT a machine dimension")

    # Two clamps, CLAMP_CENTRES apart about the Z plate's mid-height. Each is a
    # STEPPED SECTION, not a block - his, 2026-10-10: a middle that stands
    # CLAMP_MID_OUT off the plate with a CLAMP_TOP_W face on top and a fall away
    # each side, and a shoulder either side standing CLAMP_SHOULDER_OUT, which
    # is what the four M8 go through. The section lies across the machine and
    # out from the plate, and the bore runs along the extrusion, so the barrel
    # passes through a real hole rather than through declared metal.
    # IT IS SLIT DOWN ONE SIDE ONLY - the operator's right, which is the LOW X
    # side of this frame because X is measured from behind. So the clamp is one
    # C-shaped piece: the slit runs in from that edge at CLAMP_GAP_START,
    # CLAMP_GAP_W open with the bolts slack, and meets the bore. The bore is
    # therefore not an enclosed hole; it is part of the outline, reached
    # through the slit, which is what lets the jaw close on the barrel.
    import math as _math
    cl_half, sh_in = v["CLAMP_W"] / 2, v["CLAMP_MID_W"] / 2
    sh_half, step = v["CLAMP_SHOULDER_W"] / 2, v["CLAMP_STEP_OUT"]
    top_half, sh_out = v["CLAMP_TOP_W"] / 2, v["CLAMP_SHOULDER_OUT"]
    mid_out, bore_r = v["CLAMP_MID_OUT"], v["SPINDLE_D"] / 2
    g0 = zp_front + v["CLAMP_GAP_START"]
    g1 = g0 + v["CLAMP_GAP_W"]

    def _slit_x(y):
        """Where the slit's edge at height y meets the bore."""
        dy = y - sp_axis
        return zp_cx - _math.sqrt(max(bore_r ** 2 - dy ** 2, 0.0))

    # The bore, traced the LONG way round from the slit's upper lip to its
    # lower one, so the short way - the slit itself - is left open.
    a_top = _math.atan2(g1 - sp_axis, _slit_x(g1) - zp_cx)
    a_bot = _math.atan2(g0 - sp_axis, _slit_x(g0) - zp_cx) - 2 * _math.pi
    n = 48
    bore_arc = [[zp_cx + bore_r * _math.cos(a_top + (a_bot - a_top) * i / n),
                 sp_axis + bore_r * _math.sin(a_top + (a_bot - a_top) * i / n)]
                for i in range(n + 1)]

    # CLAMP_W at the face for CLAMP_STEP_OUT, then in to CLAMP_SHOULDER_W the
    # rest of the way up - his calipers, 2026-10-10. The slit is above the step,
    # so it starts from the narrower part of the side.
    clamp_profile = (
        [[zp_cx - cl_half, zp_front], [zp_cx + cl_half, zp_front],
         [zp_cx + cl_half, zp_front + step], [zp_cx + sh_half, zp_front + step],
         [zp_cx + sh_half, zp_front + sh_out], [zp_cx + sh_in, zp_front + sh_out],
         [zp_cx + top_half, zp_front + mid_out], [zp_cx - top_half, zp_front + mid_out],
         [zp_cx - sh_in, zp_front + sh_out], [zp_cx - sh_half, zp_front + sh_out],
         [zp_cx - sh_half, g1], [_slit_x(g1), g1]]
        + bore_arc
        + [[_slit_x(g0), g0], [zp_cx - sh_half, g0],
           [zp_cx - sh_half, zp_front + step], [zp_cx - cl_half, zp_front + step]])

    for cz in (block_mid - v["CLAMP_CENTRES"] / 2, block_mid + v["CLAMP_CENTRES"] / 2):
        prism("Spindle clamp", "z", 0x5E6B75, clamp_profile,
              cz - v["CLAMP_AXIAL"] / 2, cz + v["CLAMP_AXIAL"] / 2, plane="xy",
              d="bolts to the Z plate face, " + str(v["CLAMP_MID_OUT"]) +
                " out at the middle and " + str(v["CLAMP_SHOULDER_OUT"]) +
                " at the shoulders, slit on the operator's right")
        # Four M8 x 90 a clamp, on Sheet 4's M1-M8 pattern: CLAMP_BOLT_PITCH_W
        # across CENTRED ON THE CLAMP - not centred in the shoulder, which is
        # the reading that put it 2.5 out - and CLAMP_BOLT_EDGE in from each
        # end of the 55. Head proud of the shoulder, shank through it and
        # CLAMP_BOLT_ENGAGE into the plate.
        for bx in (zp_cx - v["CLAMP_BOLT_PITCH_W"] / 2,
                   zp_cx + v["CLAMP_BOLT_PITCH_W"] / 2):
            for bz in (cz - v["CLAMP_AXIAL"] / 2 + v["CLAMP_BOLT_EDGE"],
                       cz + v["CLAMP_AXIAL"] / 2 - v["CLAMP_BOLT_EDGE"]):
                cyl("Clamp bolt head", "bolts", 0x3C4248, bx, bz,
                    zp_front + sh_out, zp_front + sh_out + v["M8_HEAD_H"],
                    v["M8_HEAD_D"] / 2, axis="y", seg=12,
                    d=M8_HEAD("spindle-clamp") + " - head proud of the "
                      "shoulder" + blen("spindle-clamp"))
                cyl("Clamp bolt", "bolts", 0x3C4248, bx, bz,
                    zp_front + sh_out,
                    zp_front + sh_out - v["BOLT_SPINDLE_CLAMP"], 4.0,
                    axis="y", seg=10,
                    d=M8_HEAD("spindle-clamp") + " - " +
                      str(v["CLAMP_SHOULDER_OUT"]) + " of clamp then " +
                      str(v["CLAMP_BOLT_ENGAGE"]) + " tapped into the Z plate" +
                      blen("spindle-clamp"))

    # ---- ball screws, nuts, BF12 and the stepper castings -----------------
    # Four identical 1605 screws, each running from a BF12 at one end to a cast
    # stepper frame at the other, carrying a nut that something bolts to.
    #
    # Neither support is a block. Both are a tall centre boss holding the
    # bearing with a LOWER WING either side, and the mounting bolts go through
    # the wings - so each is drawn as two parts. One box would put a 43 boss
    # across the full 60 width and show the tongue fouling metal that is not
    # there.
    ride[0] = ""
    SCR, JRN = v["SCREW_D"] / 2, v["SCREW_JOURNAL_D"] / 2
    JB, JC = v["SCREW_JOURNAL_BF"], v["SCREW_JOURNAL_CAST"]
    STEEL, DARK, SUP = 0xB9C0C7, 0x8A9097, 0x7E6B8F
    THREAD = 0x444C54        # the thread line, dark against the steel
    NUTC, MOT = 0xC06000, 0x3C4248

    def screw(axis, c0, c1, lo, oal, bf_low):
        """lo to lo+oal along `axis`. The journals are drawn at their real 10,
        which is what makes the length visibly land inside its two supports."""
        a, b = (JB, JC) if bf_low else (JC, JB)
        cyl("Screw journal", "drive", DARK, c0, c1, lo, lo + a, JRN, axis)
        cyl("Ball screw", "drive", STEEL, c0, c1, lo + a, lo + oal - b, SCR, axis)
        # The threaded span runs between the two journals, so its length is the
        # overall less SCREW_BARE_TOTAL - which is what SCREW_THREAD_LONG and
        # SCREW_THREAD_Z already say, reached here from the other direction.
        helix("Ball screw thread", "drive", THREAD, c0, c1,
              lo + a, lo + oal - b, SCR, axis, v["SCREW_LEAD"])
        cyl("Screw journal", "drive", DARK, c0, c1, lo + oal - b, lo + oal, JRN, axis)

    def span(axis, along0, along1, c0lo, c0hi, c1lo, c1hi):
        """A box given as (along the screw) x (the other two), in machine order."""
        if axis == "y":
            return (c0lo, along0, c1lo, c0hi, along1, c1hi)
        if axis == "x":
            return (along0, c0lo, c1lo, along1, c0hi, c1hi)
        return (c0lo, c1lo, along0, c0hi, c1hi, along1)

    def support(kind, axis, c0, c1, inner, grow, seat, up):
        """BF12 or the casting's screw end, as wing + boss.

        inner is the face the screw enters, grow is +1/-1 along the screw, and
        up is +1/-1 for which way the part stands off its seating plane.
        """
        if kind == "bf12":
            depth, w, bw = v["T_BF12_BLOCK"], v["BF12_W"], v["BF12_BOSS_W"]
            wh, bh = v["BF12_WING_H"], v["BF12_H"]
        else:
            depth, w, bw = v["BK12_L"], v["CASTING_FOOTPRINT_W"], v["CASTING_BOSS_W"]
            wh, bh = v["CASTING_WING_H"], v["CASTING_BOSS_H"]
        a0, a1 = sorted((inner, inner + grow * depth))
        for name, half, h in (("wing", w / 2, wh), ("boss", bw / 2, bh)):
            s0, s1 = sorted((seat, seat + up * h))
            lbl = ("BF12 " if kind == "bf12" else "Casting ") + name
            box(lbl, "drive", SUP, *span(axis, a0, a1, c0 - half, c0 + half, s0, s1))

    def nut(axis, c0, c1, mid, face_dir):
        """The ball nut, its bolting face NUT_AXIS_TO_FACE off the axis."""
        h = v["NUT_AXIS_TO_FACE"]
        a0, a1 = mid - v["NUT_OAL"] / 2, mid + v["NUT_OAL"] / 2
        box("Ball nut", "drive", NUTC,
            *span(axis, a0, a1, c0 - v["NUT_W"] / 2, c0 + v["NUT_W"] / 2,
                  c1 - h, c1 + h))
        # the bolting face, drawn thin so it is obvious which side bolts
        f = c1 + face_dir * h
        box("Nut bolt face", "drive", 0xE08A2E,
            *span(axis, a0, a1, c0 - v["NUT_FACE_X"] / 2, c0 + v["NUT_FACE_X"] / 2,
                  min(f, f - face_dir * 2), max(f, f - face_dir * 2)))

    def rails(axis, c0, start, grow, seat, up):
        """The open rails joining the casting's screw end to its motor plate.

        Drawn SOLID, which is conservative: the real casting is open between
        them. A clearance the model shows is therefore real; one it denies may
        not be.

        THEY RUN FROM THE SEATING PLANE, not from the screw axis. The whole of
        CASTING_FOOTPRINT_L is bolted face - Sheet 3a's K1-K6 are spread across
        all 72.5 of it - so the casting is flat against the interposer for its
        full length. Drawing them centred on the axis left them floating 10
        below it, which is what the view showed.
        """
        n = v["CASTING_FOOTPRINT_L"] - v["BK12_L"]
        a0, a1 = sorted((start, start + grow * n))
        w = v["CASTING_FOOTPRINT_W"] / 2
        s0, s1 = sorted((seat, seat + up * v["CASTING_RAIL_H"]))
        box("Casting rails", "drive", SUP,
            *span(axis, a0, a1, c0 - w, c0 + w, s0, s1))

    def cast_jid(depth):
        """Which schedule entry a casting bolt belongs to, by the depth
        casting_rows hands back: the rails row is one joint, the two rows in the
        wing another, and they are 35 and 45 long."""
        return ("casting-rails" if abs(depth - v["CASTING_RAIL_H"]) < 1e-9
                else "casting-block")

    def casting_rows(c0):
        """The casting's six mounting points, as (row offset from its motor end,
        how deep the casting is there, column coordinate). The rows nearer the
        bearing end are in the WING, which is taller than the rails."""
        rails_len = v["CASTING_FOOTPRINT_L"] - v["BK12_L"]
        half = (v["BF12_COL_OUTB"] - v["BF12_COL_INB"]) / 2
        for r in (v["CASTING_BOLT_ROW_1"], v["CASTING_BOLT_ROW_2"],
                  v["CASTING_BOLT_ROW_3"]):
            d = v["CASTING_RAIL_H"] if r < rails_len else v["CASTING_WING_H"]
            for c in (c0 - half, c0 + half):
                yield r, d, c

    def motor(axis, c0, c1, plate_at, grow):
        """The casting's motor plate and the NEMA 23 hanging off it."""
        t, fw = v["MOTOR_FRAME_T"], v["MOTOR_FRAME_W"] / 2
        bl, bs = v["MOTOR_BODY_L"], v["MOTOR_BODY_SQ"] / 2
        p0, p1 = sorted((plate_at, plate_at + grow * t))
        box("Motor plate", "drive", SUP,
            *span(axis, p0, p1, c0 - fw, c0 + fw, c1 - fw, c1 + fw))
        m0, m1 = sorted((plate_at + grow * t, plate_at + grow * (t + bl)))
        box("Stepper motor", "drive", MOT,
            *span(axis, m0, m1, c0 - bs, c0 + bs, c1 - bs, c1 + bs))

    # ------------------------------------------------ Y1 and Y2
    y_axis_z = ybot - v["Y_SCREW_BELOW_BEAM"]
    y_seat_z = ybot - ip_t                      # the interposer's underside
    # THE Y DRIVE IS AT THE REAR - his, 2026-10-13. BF12 now face-mounts into
    # the FRONT FIN's inner face and the casting, interposer and motor are at
    # the back, which is the reverse of 2026-10-02. Everything below is the
    # same chain running the other way: BF12 still stops the screw
    # SCREW_END_IN_BF12 short of the plate, because the bearing is centred in
    # the block and the journal has to straddle it.
    bf12_y = v["SIDE_TONGUE_END"]               # the fin's INNER face
    y_hi = v["SCREW_FRONT_END_Y"]
    y_lo = v["SCREW_REAR_END_Y"]
    for x0 in (lx0, rx0):
        cx = x0 + v["EXT_W"] / 2
        ride[0] = ""
        # bf_low is FALSE now: the BF journal is at the HIGH end of the screw.
        screw("y", cx, y_axis_z, y_lo, v["SCREW_OAL_LONG"], bf_low=False)
        support("bf12", "y", cx, y_axis_z, bf12_y, -1, y_seat_z, -1)
        # ASSUMPTION: the nut is drawn at mid travel - it has no home position
        ride[0] = "Y"            # the nut is bolted to the gantry
        nut("y", cx, y_axis_z, (y_lo + y_hi) / 2, -1)
        ride[0] = ""
        # THE CASTING IS PLACED BY ITS SCREW AND THE INTERPOSER FOLLOWS IT -
        # his, 2026-10-10, and it is the bar's second job: besides giving
        # K1-K6 something solid to land in, it slides along the beam to meet
        # whatever the screw dictates. So the bore takes the inner BK12_L of
        # the long journal, the thread runs to the casting's face, and the
        # remaining 24.5 stands out for the coupler - the same as X and Z.
        # The interposer's leading edge is reached independently, off the fin
        # through INTERPOSER_PROUD, so if the two ever stop agreeing the lip
        # lifts off the bar in the view instead of the drift hiding.
        cast_in = v["CASTING_INBOARD_Y"]
        support("casting", "y", cx, y_axis_z, cast_in, -1, y_seat_z, -1)
        rails("y", cx, cast_in - v["BK12_L"], -1, y_seat_z, -1)
        motor("y", cx, y_axis_z, cast_in - v["CASTING_FOOTPRINT_L"], -1)
        # Six M5 up out of the casting into the tapped bar - Sheet 6's C1-C6,
        # three rows back from the casting's MOTOR end on the same two columns
        # BF12 uses. The head is under the casting, which is as deep as the
        # wing at the bearing end and as the rails further forward.
        motor_end = cast_in - v["CASTING_FOOTPRINT_L"]
        for r, d, c in casting_rows(cx):
            cyl("Casting bolt head", "bolts", 0x3C4248, c, motor_end + r,
                y_seat_z - d, y_seat_z - d - v["M5_HEAD_H"],
                v["M5_HEAD_D"] / 2, seg=12, d=D_M5_BAR(cast_jid(d)))
            cyl("Casting bolt", "bolts", 0x3C4248, c, motor_end + r,
                y_seat_z - d, y_seat_z + ip_t, 2.5, seg=10, d=D_M5_BAR(cast_jid(d)))

        # ---- the nut sole plate, under the X end plate at this end --------
        # The nut hangs below the beam with its face DOWN, so the plate lies
        # under it and bolts UP - into the nut at the tip and into the DOUBLER'S
        # end face at the root, and into nothing else. The end plate carries on
        # XEP_SOLE_TAB past that face and the base BUTTS it. Its top is put on
        # the NUT'S face rather than on the plate's bottom edge, so a cut that
        # drifts off XEP_H shows as the plate moving, not as this quietly
        # missing the nut.
        inner = xb_x0 if x0 == lx0 else xb_x1       # the end plate's INNER face
        out = -1 if x0 == lx0 else +1               # and which way it reaches
        root = inner + out * v["T_X_ENDPLATE"]      # its OUTER face: the root
        face_z = y_axis_z - v["NUT_AXIS_TO_FACE"]
        ride[0] = "Y"            # it hangs off the X end plate
        # IT IS A STEEL T, drawn as a PRISM rather than a box for the reason
        # prism()'s own docstring gives: a box claims metal the part has not
        # got, and at the tip that misreads how crowded this end is.
        #
        # The base stays FULL WIDTH for SOLE_BASE_D, which is the doubler's end
        # face and the whole of what the four root bolts land on. The stem then
        # runs straight out at SOLE_STEM_W, covering the nut's face.
        #
        # THE BASE'S REAR FACE IS THE LIMIT SENSOR'S TARGET: a full-width flat,
        # square to the direction of travel, which is what settled the T over a
        # taper - an angled face is a trip point that drifts with standoff.
        #
        # SOLE_FILLET_R is NOT DRAWN. The stem-to-base corner is square here;
        # the radius lives in the registry and on the sheet, because a polygon
        # approximation of it would then disagree with both.
        tip = root + out * v["SOLE_BRACKET_L"]
        seat = root + out * v["SOLE_BASE_D"]
        y_mid = (xep_back + xep_front) / 2
        t_half = v["SOLE_STEM_W"] / 2
        prism("Y sole plate", "gantry", 0xC9A227,
              [[root, xep_back], [seat, xep_back],
               [seat, y_mid - t_half], [tip, y_mid - t_half],
               [tip, y_mid + t_half], [seat, y_mid + t_half],
               [seat, xep_front], [root, xep_front]],
              face_z - v["T_SOLE_BRACKET"], face_z, plane="xy")

        # Eight M5 up through it: R1-R4 into the doubler's end face, then four
        # into the nut on its own pattern. Nothing goes into the end plate -
        # the base butts its strip instead. ASSUMPTION: the root bolts are
        # drawn BOLT_Z_NUT long like the nut ones; no length is given for them.
        nut_mid = (y_lo + y_hi) / 2
        cols = [(root + out * v["ROOT_BOLT_X_DOUBLER"], j) for j in range(4)]
        pts = [(bx, xep_back + v["ROOT_BOLT_Y_FIRST"] + j * v["ROOT_BOLT_Y_PITCH"],
                D_M5_END("sole-to-doubler")) for bx, j in cols]
        for bx in (v["NUT_BOLT_X_NEAR"], v["NUT_BOLT_X_FAR"]):
            for dy in (-v["NUT_PATTERN_Y"] / 2, +v["NUT_PATTERN_Y"] / 2):
                pts.append((root + out * bx, nut_mid + dy, D_M5_NUT("sole-to-nut")))
        for bx, by, det in pts:
            cyl("Y sole plate bolt head", "bolts", 0x3C4248, bx, by,
                face_z - v["T_SOLE_BRACKET"],
                face_z - v["T_SOLE_BRACKET"] - v["M5_HEAD_H"],
                v["M5_HEAD_D"] / 2, seg=12, d=det)
            cyl("Y sole plate bolt", "bolts", 0x3C4248, bx, by,
                face_z - v["T_SOLE_BRACKET"],
                face_z - v["T_SOLE_BRACKET"] + v["BOLT_Z_NUT"], 2.5, seg=10,
                d=det)

    # ------------------------------------------------ X, on TOP of its beam
    # The X screw, its supports, its bar and its motor are all carried by the X
    # beam, so they ride Y and not X. Only the nut rides X.
    ride[0] = "Y"
    x_seat_z = xb_top + ip_t
    x_axis_z = x_seat_z + v["SCREW_AXIS_H"]
    x_axis_y = xep_back + v["EXT_W"] / 2
    # THE STEPPER IS AT MAX X and BF12 at min - his, 2026-10-10. Seen from BEHIND
    # the machine, which is the frame X 0 is measured in, that puts the motor on
    # the RIGHT and the tongue plate on the left. It was the other way round.
    bf12_x = xb_x0                              # BF12 on the left plate's tongue
    x_lo = bf12_x + v["SCREW_END_IN_BF12"]      # the screw stops short of it
    x_hi = x_lo + v["SCREW_OAL_LONG"]
    screw("x", x_axis_y, x_axis_z, x_lo, v["SCREW_OAL_LONG"], bf_low=True)
    support("bf12", "x", x_axis_y, x_axis_z, bf12_x, +1, x_seat_z, +1)
    # Four M5 hold it to the tongue, the same joint as the rear plate's: the
    # TONGUE is tapped, the bolt is driven from the block side, and its end
    # finishes flush with the tongue's outboard face. Rows TONGUE_BF12_ROW1
    # and _ROW2 up from the plate's bottom edge, columns BF12_COL_INB/_OUTB
    # from its back edge - the same two columns the casting uses.
    tongue_out = bf12_x - xep_t
    for bz in (v["TONGUE_BF12_ROW1"], v["TONGUE_BF12_ROW2"]):
        for by in (v["BF12_COL_INB"], v["BF12_COL_OUTB"]):
            cyl("BF12 bolt head", "bolts", 0x3C4248,
                xep_back + by, xep_bot + bz,
                bf12_x + v["T_BF12_BLOCK"],
                bf12_x + v["T_BF12_BLOCK"] + v["M5_HEAD_H"],
                v["M5_HEAD_D"] / 2, axis="x", seg=12,
                d=D_M5_PLATE("bf12-to-x-tongue"))
            cyl("BF12 bolt", "bolts", 0x3C4248, xep_back + by, xep_bot + bz,
                tongue_out, bf12_x + v["T_BF12_BLOCK"], 2.5, axis="x", seg=10,
                d=D_M5_PLATE("bf12-to-x-tongue"))
    ride[0] = "YX"
    nut("x", x_axis_y, x_axis_z, (x_lo + x_hi) / 2, +1)
    ride[0] = "Y"
    # THE CASTING'S BORE SITS AT THE INNER END OF THE LONG JOURNAL. The journal is
    # SCREW_JOURNAL_CAST, 54.5, because the coupler lives on it as well as the
    # bearing - so the bore takes the inner BK12_L of it and the remaining 24.5
    # stands out the far side for the coupler. Drawn the other way round, 24.5 of
    # BARE SHAFT showed between the thread and the casting; the thread runs all
    # the way to the casting's face. His catch, 2026-10-10.
    x_cast_in = x_hi - v["SCREW_JOURNAL_CAST"]
    # THE X INTERPOSER, on top of the beam under the casting. It is what lifts
    # this end by T_INTERPOSER and so puts the tongue's BF12 rows where
    # TONGUE_BF12_ROW1 has them. IT IS THE SAME 150 BAR AS Y - Sheet 6 makes
    # three of them - running back from the casting's outboard end, so it
    # overhangs the beam's end the way the Y bar runs out through the fin.
    # Drawn at the casting's own 72.5 until 2026-10-10, which left it with
    # nowhere to put its T-nut bolts.
    x_ip_out = x_cast_in + v["CASTING_FOOTPRINT_L"]
    box("Interposer", "gantry", 0xC0652A,
        x_ip_out - v["INTERPOSER_L"], xep_back, xb_top,
        x_ip_out, xep_back + v["EXT_W"], x_seat_z)
    # this one SITS ON the beam, so its bolts drive down and the heads are up
    interposer_bolts(+1, xep_back, x_ip_out, "x", x_seat_z, +1,
                     "x-interposer-to-beam")
    support("casting", "x", x_axis_y, x_axis_z, x_cast_in, +1, x_seat_z, +1)
    rails("x", x_axis_y, x_cast_in + v["BK12_L"], +1, x_seat_z, +1)
    motor("x", x_axis_y, x_axis_z, x_cast_in + v["CASTING_FOOTPRINT_L"], +1)
    # the same six, but this casting sits ON its bar so they drive downward
    for r, d, c in casting_rows(x_axis_y):
        cyl("Casting bolt head", "bolts", 0x3C4248, x_ip_out - r, c,
            x_seat_z + d, x_seat_z + d + v["M5_HEAD_H"],
            v["M5_HEAD_D"] / 2, seg=12, d=D_M5_BAR(cast_jid(d)))
        cyl("Casting bolt", "bolts", 0x3C4248, x_ip_out - r, c,
            x_seat_z + d, x_seat_z - ip_t, 2.5, seg=10, d=D_M5_BAR(cast_jid(d)))

    # ------------------------------------------------ Z, up the carriage plate
    # Carried by the X carriage plate, so the Z screw and its ends ride X.
    ride[0] = "YX"
    # No interposer here, which is why the Z nut face sits 45 off the plate
    # where the beams get 55.
    z_axis_y = cp_front + v["SCREW_AXIS_H"]
    bf12_z = cp_bot
    z_lo = bf12_z + v["SCREW_END_IN_BF12"]
    z_hi = z_lo + v["SCREW_OAL_Z"]
    screw("z", zp_cx, z_axis_y, z_lo, v["SCREW_OAL_Z"], bf_low=True)
    support("bf12", "z", zp_cx, z_axis_y, bf12_z, +1, cp_front, +1)
    # Sheet 3a's F1 and F2, and there are only two of them. Here the screw runs
    # ALONG the plate rather than through it, so the block stands off its face
    # and the bolts cross its wings fore-aft instead of its 20. Mid-block along
    # the screw, and either side of the plate's centre by half the column pitch
    # BF12_COL_INB/_OUTB give.
    f_half = (v["BF12_COL_OUTB"] - v["BF12_COL_INB"]) / 2
    for bx in (zp_cx - f_half, zp_cx + f_half):
        cyl("BF12 bolt head", "bolts", 0x3C4248,
            bx, bf12_z + v["T_BF12_BLOCK"] / 2,
            cp_front + v["BF12_WING_H"],
            cp_front + v["BF12_WING_H"] + v["M5_HEAD_H"],
            v["M5_HEAD_D"] / 2, axis="y", seg=12, d=D_M5_PLATE(None))
        cyl("BF12 bolt", "bolts", 0x3C4248, bx, bf12_z + v["T_BF12_BLOCK"] / 2,
            cp_back, cp_front + v["BF12_WING_H"], 2.5, axis="y", seg=10,
            d=D_M5_PLATE(None))
    z_nut_mid = (z_lo + z_hi) / 2
    ride[0] = "YXZ"
    nut("z", zp_cx, z_axis_y, z_nut_mid, +1)
    ride[0] = "YX"
    # Same as X: the bore takes the INNER BK12_L of the long journal so the
    # thread runs to the casting's face, and the remaining 24.5 stands out the
    # far side for the coupler.
    z_cast_in = z_hi - v["SCREW_JOURNAL_CAST"]
    support("casting", "z", zp_cx, z_axis_y, z_cast_in, +1, cp_front, +1)
    rails("z", zp_cx, z_cast_in + v["BK12_L"], +1, cp_front, +1)
    motor("z", zp_cx, z_axis_y, z_cast_in + v["CASTING_FOOTPRINT_L"], +1)
    # and here the casting stands off the carriage plate's face, so the six run
    # fore-aft into the plate rather than up or down into a bar
    z_motor_end = z_cast_in + v["CASTING_FOOTPRINT_L"]
    for r, d, c in casting_rows(zp_cx):
        cyl("Casting bolt head", "bolts", 0x3C4248, c, z_motor_end - r,
            cp_front + d, cp_front + d + v["M5_HEAD_H"],
            v["M5_HEAD_D"] / 2, axis="y", seg=12, d=D_M5_PLATE(None))
        cyl("Casting bolt", "bolts", 0x3C4248, c, z_motor_end - r,
            cp_front + d, cp_back, 2.5, axis="y", seg=10, d=D_M5_PLATE(None))

    # ---- the Z top stop block, Sheet 3c ----------------------------------
    # It bolts to the carriage plate's front face and the Z ball nut lands on
    # its LOWER face, which is the stop. The screw runs on past it through the
    # \u00f822 bore - not drawn, because the model has no boolean subtraction, so
    # the screw passing through the block is declared in ALLOWED instead.
    #
    # The sheet reaches the bore at Z_STOP_BORE_OUT, 25 out from the plate face;
    # the model reaches the screw axis independently through SCREW_AXIS_H, also
    # 25. They agree, which is the check that the block is on the screw.
    ride[0] = "YX"                  # bolted to the carriage plate
    zs_out = cp_front + v["Z_STOP_OUT"]
    zs_bot = cp_bot + v["Z_STOP_FACE_X"]
    box("Z stop block", "z", 0xC9A227,
        zp_cx - v["Z_STOP_W"] / 2, cp_front, zs_bot,
        zp_cx + v["Z_STOP_W"] / 2, zs_out, zs_bot + v["Z_STOP_T"],
        d="1in 6061 - the Z nut lands on its lower face. SACRIFICIAL: replace it "
          "and its bolts if it is ever used")
    # TS1 and TS2: M5 x 50 counterbored Z_STOP_CBORE_DEPTH from the outer face,
    # so the shank starts at the counterbore floor and runs its full 50 - which
    # ends BOLT_Z_STOP - (Z_STOP_OUT - Z_STOP_CBORE_DEPTH) inside the plate.
    zs_floor = zs_out - v["Z_STOP_CBORE_DEPTH"]
    for sx in (zp_cx - (v["Z_STOP_W"] / 2 - v["Z_STOP_BOLT_INSET"]),
               zp_cx + (v["Z_STOP_W"] / 2 - v["Z_STOP_BOLT_INSET"])):
        sz = zs_bot + v["Z_STOP_BOLT_Z"]
        cyl("Z stop bolt head", "bolts", 0x3C4248, sx, sz,
            zs_floor, zs_floor + v["M5_HEAD_H"], v["M5_HEAD_D"] / 2,
            axis="y", seg=12,
            d=M8_HEAD(None) + " - M5 x 0.8 x 50 socket cap from BOLT_Z_STOP, "
              "counterbored 6 deep" + blen(None))
        cyl("Z stop bolt", "bolts", 0x3C4248, sx, sz,
            zs_floor, zs_floor - v["BOLT_Z_STOP"], 2.5, axis="y", seg=10,
            d=M8_HEAD(None) + " - M5 x 0.8 x 50 from BOLT_Z_STOP, 39 of block "
              "then 11 into the carriage plate" + blen(None))
    ride[0] = ""

    # ---- linear rails and bearing blocks ---------------------------------
    # Rails sit on their beam's face at RAIL_LOW_Z / RAIL_HIGH_Z; the block
    # envelopes the rail and stands RAIL_STACK off the face, which is the
    # measured figure the whole machine's offsets are built on.
    ride[0] = ""
    rw, st, bw, bl = v["RAIL_W"], v["RAIL_STACK"], v["BLOCK_W"], v["BLOCK_BUTTED"]
    # FLAG: THE BLOCK DOES NOT REACH THE FACE. Its side wings stop BLOCK_FACE_CLEAR
    # short of it - 4.2, his gauge-block measurement 2026-10-11 - and that gap is
    # what the front strips run through. Drawn as a solid box from the face, the
    # model reported six clashes against the strips that do not exist on the
    # machine. The relief is drawn rather than the pair being declared allowed,
    # so a strip thicker than 4.2 still gets caught.
    bfc = v["BLOCK_FACE_CLEAR"]
    RC, BC = 0x7E8C99, 0xE04F3D

    def rail_and_blocks(axis, face, d, zc, along, bfrom, bto, rk="", bk=""):
        """axis: which coordinate the stack grows along; d: +1 / -1.

        rk and bk are what the rail and the blocks ride on, and they are never
        the same thing: the rail belongs to whatever it is bolted to and the
        blocks to the carriage that slides on it.
        """
        for z in zc:
            if axis == "x":
                box(f"{along} rail", "motion", RC, face, bfrom[0], z - rw / 2,
                    face + d * rw, bto[0], z + rw / 2, k=rk)
                box(f"{along} block", "motion", BC, face + d * bfc, bfrom[1],
                    z - bw / 2, face + d * st, bto[1], z + bw / 2, k=bk)
            else:                                   # stack grows along fore-aft
                box(f"{along} rail", "motion", RC, bfrom[0], face, z - rw / 2,
                    bto[0], face + d * rw, z + rw / 2, k=rk)
                box(f"{along} block", "motion", BC, bfrom[1], face + d * bfc,
                    z - bw / 2, bto[1], face + d * st, z + bw / 2, k=bk)

    # Y: on each beam's INNER face, blocks carried by the X end plate
    gb = (xep_back, xep_back + bl)
    rail_and_blocks("x", lx0 + v["EXT_W"], +1, [ybot + v["RAIL_LOW_Z"], ybot + v["RAIL_HIGH_Z"]],
                    "Y", (y0, gb[0]), (y1, gb[1]), rk="", bk="Y")
    rail_and_blocks("x", rx0, -1, [ybot + v["RAIL_LOW_Z"], ybot + v["RAIL_HIGH_Z"]],
                    "Y", (y0, gb[0]), (y1, gb[1]), rk="", bk="Y")
    # X: on the X beam's FRONT face, blocks carried by the carriage plate
    # The butted pair is BLOCK_BUTTED = 154.18 against a 154 plate, so it is
    # CENTRED on the plate and the 0.09 that hangs over each end is end cap.
    bo = (bl - v["XEP_W"]) / 2
    rail_and_blocks("y", xbeam_front, +1, [xb_bot + v["RAIL_LOW_Z"], xb_bot + v["RAIL_HIGH_Z"]],
                    "X", (xb_x0, cp_x0 - bo), (xb_x1, cp_x1 + bo), rk="Y", bk="YX")
    # Z: vertical, on the carriage plate's front face
    for xc in (zp_cx - v["Z_RAIL_COL"], zp_cx + v["Z_RAIL_COL"]):
        box("Z rail", "motion", RC, xc - rw / 2, cp_front, cp_bot + 7,
            xc + rw / 2, cp_front + rw, cp_bot + 7 + v["Z_RAIL_L"], k="YX")
        box("Z block", "motion", BC, xc - bw / 2, cp_front + bfc,
            block_mid - bl / 2,
            xc + bw / 2, cp_front + st, block_mid + bl / 2, k="YXZ")
        # The spacer bar is SANDWICHED between the blocks and the Z plate - one per
        # rail, each spanning that rail's two blocks. The model had the gap but
        # nothing in it until he spotted the omission, 2026-10-03.
        box("Z spacer", "z", 0xBFC7CE,
            xc - v["SPACER_W"] / 2, cp_front + st, block_mid - v["SPACER_L"] / 2,
            xc + v["SPACER_W"] / 2, cp_front + st + v["SPACER_T"],
            block_mid + v["SPACER_L"] / 2, k="YXZ")

    # ---- the 45 mm front joining strips, Sheet 8 --------------------------
    # One per beam, across the seam, RUNNING UNDER BOTH BEARING BLOCK ROWS.
    # OPEN: THIS COMMENT DESCRIBED THE OLD 45 STRIP until 2026-10-11 - one that sat
    # BETWEEN the rows with half a millimetre either side - and the registry had
    # moved to 50.8 on 2026-10-09 without it. At 50.8 the strip is wider than the
    # block gap ON PURPOSE and passes 2.4 under each block, which buys about ten
    # millimetres of fore-aft tolerance instead of about nothing; see
    # FRONT_STRIP_W. What makes it fit is BLOCK_FACE_CLEAR, the 4.2 under the
    # block's wings, against the strip's 3.175.
    sw, st_t = v["FRONT_STRIP_W"], v["T_FRONT_STRIP"]
    strip_x = [v["TSLOT_X_FIRST"] + i * v["TSLOT_X_PITCH"]
               for i in range(int(v["TSLOT_X_COUNT"]))]
    y_seam = ybot + v["EXT_W"]
    for face, d in ((lx0 + v["EXT_W"], +1), (rx0, -1)):     # Y beams, inner faces
        box("Front strip", "plates", 0xB8C2CB, face, y0, y_seam - sw / 2,
            face + d * st_t, y1, y_seam + sw / 2)
    x_seam = xb_bot + v["EXT_W"]
    box("Front strip", "plates", 0xB8C2CB, xb_x0, xbeam_front, x_seam - sw / 2,
        xb_x1, xbeam_front + st_t, x_seam + sw / 2, k="Y")

    # ---- M8 flange bolt heads -------------------------------------------
    # Only where the position is unambiguous from the registry: the four T-slot
    # rows on each side plate, the rear plate's sixteen A-holes, and each fin's
    # eight into the beam's end bores. All three sets land on the SAME four
    # heights, 197 / 227 / 257 / 287, because all three are the extrusion's own
    # slot grid off Y_BEAM_UNDERSIDE - so if they do not line up in the view,
    # something upstream has moved.
    # 2.5 is the TOTAL proud height: these are flanged button heads with a hex
    # socket in the middle of the dome, so nothing sits above it. Drawn flat,
    # because the dome's fall to under 1 at the rim is a millimetre of relief.
    hd, hh = v["FLANGE_NORMAL_D"] / 2, v["FLANGE_NORMAL_H"]
    # FLAG: THE STRIP BOLTS ARE A DIFFERENT HEAD AND THE MODEL DREW THEM AS THIS
    # ONE. FLANGE_LOW_D exists because the AS5311 puck has to pass between the
    # two head rows - at 17.5 the channel is 12.5 and the puck does not fit, at
    # 13.75 it is 16.25 and it does. Drawing the big head there contradicted the
    # symbol that was created for the clearance. Caught 2026-10-11 when he gave
    # the head type for every joint.
    ld, lh = v["FLANGE_LOW_D"] / 2, v["FLANGE_LOW_H"]
    BOLT = 0x3C4248
    rows = [v["SIDE_TSLOT_ROW_1"] + i * v["SLOT_GRID"] for i in range(4)]
    stations = [v["SIDE_TONGUE_START"] + v["TSLOT_X_FIRST"] + i * v["TSLOT_X_PITCH"]
                for i in range(int(v["TSLOT_X_COUNT"]))]

    for face, d in ((0.0, -1), (W, +1)):            # side plates, heads outboard
        for st in stations:
            for z in rows:
                cyl("Flange head", "bolts", BOLT, st, z, face, face + d * hh,
                    hd, axis="x", seg=12, d=D_SIDE_BOLT("y-back-plate"))

    # THE RP_ COLUMNS ARE SHEET 7 COORDINATES, measured from the plate's left edge,
    # which sits on the Y1 extrusion's outboard face - so the machine X is each of
    # them plus Y1_EXT_FACE_X.
    rp0 = v["Y1_EXT_FACE_X"]
    for col in (rp0 + v["RP_A_COL_1"],
                rp0 + v["RP_A_COL_1"] + v["EXT_W"] - 2 * v["EXT_BORE_INSET"],
                rp0 + v["RP_A_COL_3"], rp0 + v["RP_A_COL_4"]):   # heads backward
        for z in rows:
            cyl("Flange head", "bolts", BOLT, col, z, 0.0, -hh, hd, axis="y",
                seg=12, d=D_BEAM_END("rear-plate-to-beam-ends"))

    # The BF12 bolts, four per Y beam - AT THE FIN NOW, not the rear plate, and
    # they run BACKWARD out of it. His flip, 2026-10-13. The fin is TAPPED M5
    # and the bolt is driven from the block side, so the head seats on BF12's
    # own rearward face and the bolt runs forward into the fin. The block still
    # hangs upside down with its base level with the interposer's underside,
    # which is what puts the rows at 165 and 147 - that chain is beam-referenced
    # and did not move. Head drawn as the M5 socket cap he is using.
    #
    # FLAG: M5 x 30 ENDS FLUSH, where in the X tongue the same bolt stops 2.19
    # short. BF12_BODY_AT_BOLT is 20, so a 30 engages 10, and T_FIN is 10 - it
    # is a tapped-through hole, 2 x D in aluminium, finishing level with the
    # fin's outboard face. His call, 2026-10-13: the same fastener as X's.
    #
    # OPEN: THE COLUMNS ARE STILL NAMED RP_F_COL_*. They are the right machine X
    # either way, because the beams did not move and the columns are set by
    # them - but the name says rear plate and the holes are in the fin now.
    bf12_face = v["SIDE_TONGUE_END"] - v["T_BF12_BLOCK"]    # BF12's rear face
    fin_outer = v["SIDE_TONGUE_END"] + v["T_FIN"]
    for col in (rp0 + v["RP_F_COL_1"], rp0 + v["RP_F_COL_2"],
                rp0 + v["RP_F_COL_3"], rp0 + v["RP_F_COL_4"]):
        for z in (v["BF12_ROW1_Y"], v["BF12_ROW2_Y"]):
            cyl("BF12 bolt head", "bolts", BOLT, col, z,
                bf12_face, bf12_face - v["M5_HEAD_H"], v["M5_HEAD_D"] / 2,
                axis="y", seg=12, d=D_M5_PLATE("bf12-to-rear-plate"))
            cyl("BF12 bolt", "bolts", BOLT, col, z, bf12_face, fin_outer, 2.5,
                axis="y", seg=10, d=D_M5_PLATE("bf12-to-rear-plate"))

    # The eight M5 through the X sole plate, all driven DOWNWARD from above -
    # his reason for putting the plate on top in the first place: the bolts stay
    # reachable during assembly. Four at the root tap into the doubler's top
    # edge, four further out tap into the ball nut housing. Head proud on the
    # plate's top face, shank BOLT_Z_NUT down from under it, which crosses the
    # 6.35 plate and leaves Y_NUT_BOLT_ENGAGE in the part below.
    sole_top = x_nut_face + v["T_SOLE_BRACKET"]
    sole_bolts = [(cp_x0 + v["ROOT_BOLT_Y_FIRST"] + i * v["ROOT_BOLT_Y_PITCH"],
                   cp_back - v["X_SOLE_ROOT_ROW"], D_M5_EDGE(None)) for i in range(4)]
    x_nut_mid = (x_lo + x_hi) / 2
    for ry in (v["X_NUT_BOLT_NEAR"], v["X_NUT_BOLT_FAR"]):
        for dx in (-v["NUT_PATTERN_Y"] / 2, +v["NUT_PATTERN_Y"] / 2):
            sole_bolts.append((x_nut_mid + dx, cp_back - ry, D_M5_NUT("sole-to-nut")))
    for bx, by, det in sole_bolts:
        cyl("X sole bolt head", "bolts", BOLT, bx, by,
            sole_top, sole_top + v["M5_HEAD_H"], v["M5_HEAD_D"] / 2, seg=12,
            d=det, k="YX")
        cyl("X sole bolt", "bolts", BOLT, bx, by,
            sole_top, sole_top - v["BOLT_Z_NUT"], 2.5, seg=10, d=det, k="YX")

    for outer, sgn in ((0 - v["FIN_PROUD"], +1), (W + v["FIN_PROUD"], -1)):
        for c in (v["FIN_COL_OUTB"], v["FIN_COL_INB"]):   # fins, heads forward
            for z in rows:
                cyl("Flange head", "bolts", BOLT, outer + sgn * c, z,
                    y1 + v["T_FIN"], y1 + v["T_FIN"] + hh, hd, axis="y",
                    seg=12, d=D_BEAM_END("fin-to-beam-end"))

    # the strips' own two rows, which land in the slots flanking each seam
    for face, d in ((lx0 + v["EXT_W"], +1), (rx0, -1)):
        for st in [y0 + x for x in strip_x]:
            for z in (y_seam - v["RAIL_SLOT_INSET"], y_seam + v["RAIL_SLOT_INSET"]):
                cyl("Flange head", "bolts", BOLT, st, z,
                    face + d * st_t, face + d * (st_t + lh), ld, axis="x",
                    seg=12, d=D_STRIP_BOLT("front-strip"))
    for st in [xb_x0 + x for x in strip_x]:
        for z in (x_seam - v["RAIL_SLOT_INSET"], x_seam + v["RAIL_SLOT_INSET"]):
            cyl("Flange head", "bolts", BOLT, st, z,
                xbeam_front + st_t, xbeam_front + st_t + lh, ld, axis="y",
                seg=12, d=D_STRIP_BOLT("front-strip"), k="Y")

    # ---- the tongue bolts, through plate and tongue into an acorn nut -----
    # Twenty-two of them: eight through the rear plate into the back tongue and
    # seven through each outboard plate into its side tongue. The stack runs
    # flange head on the INBOARD face, shank through plate and tongue, fender
    # washer, acorn nut outboard - head inside so one wrench sits on the nut in
    # the open while the bolt is driven from within.
    WD, WT = v["FENDER_WASHER_D"] / 2, v["FENDER_WASHER_T"]
    AD, AH = v["ACORN_NUT_D"] / 2, v["ACORN_NUT_H"]
    SHANK = v["BEAM_BOLT_CLEARANCE"] / 2 - 0.5        # the M8 itself, not its hole
    WASH, ACORN = 0x9AA3AB, 0x5A6068

    def bolt_stack(axis, c0, c1, head_face, far_face, out, jid):
        """head_face is the plate's inboard face, far_face the tongue's outer."""
        cyl("Tongue bolt head", "bolts", BOLT, c0, c1,
            head_face, head_face - out * v["FLANGE_NORMAL_H"],
            v["FLANGE_NORMAL_D"] / 2, axis=axis, seg=12, d=D_TONGUE(jid))
        cyl("Tongue bolt", "bolts", BOLT, c0, c1, head_face, far_face,
            SHANK, axis=axis, seg=10, d=D_TONGUE(jid))
        cyl("Fender washer", "bolts", WASH, c0, c1,
            far_face, far_face + out * WT, WD, axis=axis, seg=14)
        cyl("Acorn nut", "bolts", ACORN, c0, c1,
            far_face + out * WT, far_face + out * (WT + AH), AD, axis=axis, seg=6)

    # the back tongue laps the rear plate from BEHIND, so these drive -y
    for i in range(8):
        # Sheet 7 coordinates, so off the plate's left edge like the RP_ columns
        x = rp0 + v["XBOX_X_FIRST"] + i * v["XBOX_PITCH"]
        bolt_stack("y", x, v["XBOX_ROW_Y"], v["T_REAR_PLATE"], -TT, -1,
                       "rear-plate-to-tongue")

    # each side tongue laps its plate from OUTBOARD
    side_st = [v["SIDE_TONGUE_START"] + v["TSLOT_X_FIRST"] + i * v["TSLOT_X_PITCH"]
               for i in range(int(v["TSLOT_X_COUNT"]))]
    for head_face, far_face, out in ((sp, -TT, -1), (W - sp, W + TT, +1)):
        for st in side_st:
            bolt_stack("x", st, v["BOX_TONGUE_BOLT_Y"], head_face, far_face,
                       out, "side-plate-to-tongue")

    # ---- rail counterbores ------------------------------------------------
    # Drilled into the rail's EXPOSED face and running RAIL_CBORE_DEPTH back
    # toward the beam, so they are drawn as dark cylinders sunk into the rail.
    # No boolean subtraction here - the model is solids - so the pair is allowed
    # to interpenetrate on purpose and says so in ALLOWED.
    cb_r, cb_d = v["RAIL_CBORE_D"] / 2, v["RAIL_CBORE_DEPTH"]
    cb_f, cb_p = v["RAIL_CBORE_FIRST"], v["RAIL_CBORE_PITCH"]
    n_beam = int(round(v["RAIL_CBORE_N_BEAM"]))
    n_z = int(round(v["RAIL_CBORE_N_Z"]))

    for face, d in ((lx0 + v["EXT_W"], +1), (rx0, -1)):          # Y rails
        for z in (ybot + v["RAIL_LOW_Z"], ybot + v["RAIL_HIGH_Z"]):
            for i in range(n_beam):
                cyl("Rail counterbore", "motion", HOLE, y0 + cb_f + i * cb_p, z,
                    face + d * rw, face + d * (rw - cb_d), cb_r, axis="x", seg=10)
    for z in (xb_bot + v["RAIL_LOW_Z"], xb_bot + v["RAIL_HIGH_Z"]):   # X rails
        for i in range(n_beam):
            cyl("Rail counterbore", "motion", HOLE, xb_x0 + cb_f + i * cb_p, z,
                xbeam_front + rw, xbeam_front + rw - cb_d, cb_r, axis="y",
                seg=10, k="Y")
    for xc in (zp_cx - v["Z_RAIL_COL"], zp_cx + v["Z_RAIL_COL"]):     # Z rails
        for i in range(n_z):
            cyl("Rail counterbore", "motion", HOLE, xc,
                cp_bot + 7 + cb_f + i * cb_p,
                cp_front + rw, cp_front + rw - cb_d, cb_r, axis="y", seg=10,
                k="YX")

    # ---- the T-slots on the beams' top and bottom faces ------------------
    # Two per face, on the same two centrelines the bolt rows already use -
    # RAIL_SLOT_INSET and one SLOT_GRID further in, so 15 and 45 across the 60.
    # Sunk TSLOT_DEPTH to the slot floor and TSLOT_MOUTH_W across the mouth.
    #
    # THE MOUTH AND THE DEPTH ONLY. The lips, the undercut behind them and the
    # corner bores are not drawn - the registry has the lip's thickness but not
    # its reach, so a full section would be invented rather than placed. What
    # this gives is where a slot IS, which is what a bolt column has to land in.
    #
    # Drawn the way the rail counterbores are, as a dark solid sunk into the
    # face, because the model has no boolean subtraction. The pair is allowed to
    # interpenetrate on purpose and says so in ALLOWED.
    D_SLOT = ("T-slot on the 30-6060 - " + str(v["TSLOT_MOUTH_W"]) + " across the "
              "mouth, " + str(v["TSLOT_DEPTH"]) + " to the floor. The lips and the "
              "undercut behind them are not drawn")
    mw, td = v["TSLOT_MOUTH_W"] / 2, v["TSLOT_DEPTH"]
    slots = (v["RAIL_SLOT_INSET"], v["RAIL_SLOT_INSET"] + v["SLOT_GRID"])

    for x0 in (lx0, rx0):                       # the two Y beams, frame
        for sc in slots:
            c = x0 + sc
            for face, into in ((ytop, -1), (ybot, +1)):
                box("Beam T-slot", "ybeams", HOLE, c - mw, y0, face,
                    c + mw, y1, face + into * td, d=D_SLOT, k="")
    for sc in slots:                            # the X beam, which rides Y
        c = xep_back + sc
        for face, into in ((xb_top, -1), (xb_bot, +1)):
            box("Beam T-slot", "gantry", HOLE, xb_x0, c - mw, face,
                xb_x1, c + mw, face + into * td, d=D_SLOT, k="Y")

    # ---- jog limits ------------------------------------------------------
    # HIS, 2026-10-10, and every one of them is a 5 mm standoff off a part this
    # model already places - so each limit moves if the part it is measured from
    # moves, the same way everything else here does.
    #
    #   Y   back: the X end plates' back edge, 5 from the rear plate's front face
    #       front: THE Z PLATE's front face, 5 from the front fin's back face -
    #       his, 2026-10-10. It was the end plate's front edge, which is 6.6
    #       behind the Z plate, so the plate itself went 1.6 INTO the fin at
    #       full forward travel with Z down. The envelope sweep found it; the
    #       limit now rides on the part that gets there first.
    #   X   either way: the Z PLATE's edge, 5 from the inside face of the X end
    #       plate at that end. The Z plate and not the carriage plate because it
    #       is the wider of the two, Z_PLATE_W against XEP_W.
    #   Z   down: the nut's lower end, 5 above BF12's upper face
    #       up: the nut's upper end, 5 below the stop block's lower face - the
    #       face the nut would land on if it ever got there.
    jog = {
        "Y": [round(v["T_REAR_PLATE"] + 5 - xep_back, 2),
              round((y1 - 5) - zp_front, 2), ""],
        "X": [round((xb_x0 + 5) - (zp_cx - v["Z_PLATE_W"] / 2), 2),
              round((xb_x1 - 5) - (zp_cx + v["Z_PLATE_W"] / 2), 2), ""],
        "Z": [round((bf12_z + v["T_BF12_BLOCK"] + 5) - (z_nut_mid - v["NUT_OAL"] / 2), 2),
              round((zs_bot - 5) - (z_nut_mid + v["NUT_OAL"] / 2), 2), ""],
    }

    # WHERE HOME IS: the back left corner, top of travel - his, 2026-10-10, and
    # the same corner the Mega V homes to. Left is the operator's left, which is
    # MAX machine X; back is MIN fore-aft; top is the up stop. Each one is an end
    # of travel the model already works out, so home moves if a stop moves.
    home = {"X": jog["X"][1], "Y": jog["Y"][0], "Z": jog["Z"][1]}

    groups = {
        "box": "Torsion box: bottom skin",
        # THEIR OWN CHECKBOX - his, off the Parts dialog. The four 24 pieces are
        # what covers every joint at the box's edge: hide them and the tenons,
        # the skin's corners and the shoulder are all visible at once, and with
        # them in the box group that meant hiding the bottom skin as well.
        "tongues": "Torsion box: the 24 outer laminations",
        "topskin": "Torsion box: TOP SKIN (hide to see the bays)",
        "grid": "Torsion box: ribs and perimeter webs",
        "legs": "Legs: all five, with their tenons and fillers",
        "rails": "Base: the grid rails",
        "walls": "Base: the two shear walls",
        "bed": "Tee track bed",
        "spoil": "MDF spoilboard (hide to see the track)",
        # FLAG: NOT "M8 flange bolt heads", WHICH IS WHAT IT SAID. The hover line
        # ends with the part's group, so every socket-head bolt in the model was
        # reporting itself as a flange one - he caught it on the spindle clamp's
        # M8 x 90, whose own text has always said socket head cap. The group was
        # named when it held nothing else; it now holds M4 and M5 socket heads,
        # two M8 socket joints, acorn nuts, washers and the spoilboard T-bolts.
        "bolts": "Bolts, nuts and washers",
        "motion": "Rails and bearing blocks",
        "plates": "Rear, side and fin plates",
        "ybeams": "Y beams",
        "drive": "Ball screws, nuts and steppers",
        "gantry": "X gantry",
        "z": "Z carriage and spindle",
    }
    # Where the tool tip sits at the drawn pose, in machine coordinates. The DRO
    # adds the jog offsets to it, which is all a DRO is here.
    tip = [round(zp_cx, 3), round(sp_axis, 3), round(tool_tip, 3)]

    facts = [
        ("Machine width", W), ("Box fore-aft", D), ("Box thickness", v["BOX_THK"]),
        ("Tee track bed top", v["TT_BED_T"]),
        ("Y beam underside", ybot), ("Y beam top", ytop),
        ("X beam top", xb_top), ("Collet nut tip", bar_bot - v["SPINDLE_COLLET_END"]),
    ]
    # three.js goes INLINE rather than being referenced. The model is a thing that
    # gets sent to people, and a two-file page arrives broken the moment the vendor
    # folder is left behind - a blank window with nothing to say why. One file costs
    # about 600 KB and cannot be separated from the thing it needs.
    # Anything no call site described gets the table's line for its name. Parts
    # with neither keep an empty string and the hover then shows name and size
    # only, which is still better than nothing and is honest about the rest.
    for p in P:
        if not p.get("d"):
            p["d"] = DETAIL.get(p["n"], "")
        if p["n"] in SHEETS:
            p["d"] = ((p["d"] + " \u00b7 ") if p["d"] else "") + sheet_note(SHEETS[p["n"]])
    # FLAG: EVERY BOLT TOOLTIP MUST HAVE COME FROM THE SCHEDULE HELPERS, and this
    # is what proves it rather than a sweep somebody believed. A part in the
    # bolts group has to carry one of the strings M8_HEAD() handed out AND one
    # of blen()'s - membership, not pattern matching. Nuts and washers are
    # exempt: they are not bolts and have no length of their own.
    EXEMPT = {"Acorn nut", "Fender washer", "Spoilboard washer",
              "Spoilboard nut", "Spoilboard counterbore", "Spoilboard bolt hole"}
    typed = []
    for q in P:
        if q["g"] != "bolts" or q["n"] in EXEMPT:
            continue
        d = q.get("d", "")
        if not (any(h in d for h in DERIVED_HEAD)
                and any(L in d for L in DERIVED_LEN)):
            typed.append(q["n"])
    if typed:
        names = sorted(set(typed))
        print(f"{len(typed)} bolt(s) carry a tooltip that did not come from the "
              f"fastener schedule: {', '.join(names)}", file=sys.stderr)
        return 2

    unused = check_sheets(("1a", "1b", "2a", "2b"))

    # FLAG: A BOLT THE SCHEDULE HAS NEVER HEARD OF IS A BOLT NOBODY ORDERS. Now
    # that the tooltips read their length out of fasteners.toml, the ones that
    # come back empty are a list of real joints missing from it - so say so on
    # every run rather than leaving it to whoever happens to hover one.
    gaps = {}
    for q in P:
        if "no entry in the fastener schedule" in q.get("d", ""):
            if "head" not in q["n"]:
                gaps[q["n"]] = gaps.get(q["n"], 0) + 1
    if gaps:
        print("")
        print(f"{sum(gaps.values())} bolts are drawn that the "
              f"fastener schedule has no entry for:")
        for n in sorted(gaps):
            print(f"  {n:24s} {gaps[n]:3d}")

    three = VENDOR.read_text(encoding="utf-8")
    html = (HTML.replace("__PARTS__", json.dumps(P))
                .replace("__GROUPS__", json.dumps(groups))
                .replace("__ASSUMPTIONS__", json.dumps(ASSUMPTIONS))
                .replace("__FACTS__", json.dumps([[a, round(b, 2)] for a, b in facts]))
                .replace("__JOG__", json.dumps(jog))
                .replace("__TIP__", json.dumps(tip))
                .replace("__HOME__", json.dumps(home))
                # THE PAGE DOES NOT GET ITS OWN EXCLUSION LIST. The live clash
                # check in the viewer is a port of the one above, and the thing
                # that would rot first is two copies of ALLOWED drifting apart -
                # so the page is handed THIS one. Same for the bite pairs.
                .replace("__ALLOWED__", json.dumps(
                    sorted(sorted(f) for f in ALLOWED if len(f) == 2)))
                .replace("__BITE__", json.dumps(
                    sorted(sorted(f) for f in BITE))))
    # last, and not via str.replace on the whole document: three.min.js contains
    # backslash escapes that a replacement template would eat.
    i = html.index("__THREE__")
    html = html[:i] + three + html[i + len("__THREE__"):]
    OUT.write_text(html, encoding="utf-8")
    kb = len(html.encode("utf-8")) / 1024
    print(f"wrote {OUT.relative_to(ROOT)} - {len(P)} parts, {kb:.0f} KB, self-contained")
    for a, b in facts:
        print(f"  {a:22} {b:10.2f}")
    print(f"\n{len(SHEETS) + 4} shop pack sheets are named on hover"
          + (f"; NOT MODELLED: Sheet {', Sheet '.join(unused)}" if unused else ""))
    print(f"\ntool tip at the drawn pose: X {tip[0]:.2f}  fore-aft {tip[1]:.2f}  "
          f"Z {tip[2]:.2f}")
    print("\nhome is the back left corner at the top of travel, where the DRO "
          "reads zero:")
    print(f"  from the drawn pose that is X {home['X']:+.2f}  Y {home['Y']:+.2f}  "
          f"Z {home['Z']:+.2f}")
    print("\njog limits, as an offset from the drawn pose:")
    for ax, (lo_, hi_, warn) in jog.items():
        print(f"  {ax}  {lo_:+9.2f} to {hi_:+9.2f}   travel {hi_ - lo_:8.2f}"
              + ("   " + warn.split(" - ")[0] if warn else ""))
    rc = report_overlaps(P)
    return rc or sweep_envelope(P, jog, home)


# Pairs that SHOULD interpenetrate, with the reason. Everything else that
# overlaps is a real interference and gets printed.
# FLAG: THE TOOL IN THE SACRIFICIAL SHEET IS NOT A FAULT, IT IS THE JOB. The
# spoilboard exists to be cut into, so a tool-in-MDF overlap is reported as a
# BITE and drawn in a different colour from a clash. Only the MDF is listed:
# the tool reaching the ALUMINIUM would be a real fault and must stay red.
BITE = {
    frozenset({"Tool", "MDF sacrificial sheet"}),
    frozenset({"Tool", "MDF sheet"}),
}

ALLOWED = {
    # The spoilboard's four T-bolts: the shank crosses both MDF sheets and the
    # nut and washer sit in a counterbore that is DRAWN AS A SOLID rather than
    # subtracted from the board, so every one of these pairs is a part sharing
    # space with the hole it lives in. Declared rather than left to clutter the
    # clash list red.
    frozenset({"Spoilboard T-bolt", "MDF sheet"}),
    frozenset({"Spoilboard T-bolt", "MDF sacrificial sheet"}),
    frozenset({"Spoilboard T-bolt", "Spoilboard bolt hole"}),
    frozenset({"Spoilboard T-bolt", "Spoilboard counterbore"}),
    frozenset({"Spoilboard T-bolt", "Spoilboard washer"}),
    frozenset({"Spoilboard T-bolt", "Spoilboard nut"}),
    frozenset({"Spoilboard T-bolt", "Tee track flat"}),
    frozenset({"Spoilboard T-bolt", "Tee track slot bottom"}),
    frozenset({"Spoilboard bolt hole", "MDF sheet"}),
    frozenset({"Spoilboard bolt hole", "MDF sacrificial sheet"}),
    frozenset({"Spoilboard counterbore", "MDF sacrificial sheet"}),
    frozenset({"Spoilboard counterbore", "MDF sheet"}),
    frozenset({"Spoilboard counterbore", "Spoilboard washer"}),
    frozenset({"Spoilboard counterbore", "Spoilboard nut"}),
    frozenset({"Spoilboard washer", "MDF sacrificial sheet"}),
    frozenset({"Spoilboard nut", "MDF sacrificial sheet"}),
    frozenset({"Spoilboard washer", "MDF sheet"}),
    frozenset({"Spoilboard nut", "MDF sheet"}),
    # THE EGG CRATE IS HALF-DEPTH NOTCHED AT EVERY CROSSING - settled
    # 2026-09-30 - and the notches are deliberately not drawn: a half-depth
    # notch removes no envelope, and drawing sixteen of them would clutter the
    # bay layout the interior was decomposed to show. So every crossing reads
    # as a 19 x 19 x 100 overlap, and all sixteen are intentional.
    #
    # FLAG: THE PRICE IS NAMED RATHER THAN HIDDEN: this pair is now blind, so if a
    # rib ever moves onto a POST it will not be caught here. The checks that
    # still bite are rib-against-tenon and rib-against-web, both left live.
    frozenset({"Rib, fore-aft", "Rib, across"}),

    # The perimeter web is one lamination of a wall whose other lamination is
    # the tongue. They are laminated face to face, so they touch by design.
    frozenset({"Perimeter web", "Back tongue"}),
    frozenset({"Perimeter web", "Side lamination"}),
    frozenset({"Perimeter web", "Side lamination, proud band"}),
    frozenset({"Perimeter web", "Rib, fore-aft"}),  # ribs die into the webs
    frozenset({"Perimeter web", "Rib, across"}),
    frozenset({"Perimeter web", "Back tenon block"}),   # it dies into the web
    frozenset({"Back tenon block", "Rib, across"}),     # and into the first rib
    frozenset({"Back tenon block", "Post, back centre tenon"}),  # it beds against it

    # Each post is drawn as a tenon standing out of a full-section stub - one
    # part, two boxes, the same convention as the BF12 wing and boss below.
    frozenset({"Post, front left", "Post, front left tenon"}),
    frozenset({"Post, front right", "Post, front right tenon"}),
    frozenset({"Post, back centre", "Post, back centre tenon"}),
    # The post's outer face is FLUSH with the tongue's outer face and the 44
    # wall lands on the 44 shoulder - that is the whole ledge detail, so the
    # wall standing on the shoulder is contact by design, not a clash.
    frozenset({"Post, front left", "Side lamination"}),
    frozenset({"Post, front left", "Back tongue"}),
    frozenset({"Post, front right", "Side lamination"}),
    frozenset({"Post, front right", "Back tongue"}),
    frozenset({"Post, back centre", "Back tongue"}),
    frozenset({"Post, front left", "Perimeter web"}),
    frozenset({"Post, front right", "Perimeter web"}),
    frozenset({"Post, back centre", "Perimeter web"}),

    frozenset({"Back tongue", "Side lamination"}),       # meet at the corner
    frozenset({"Back tongue", "Side lamination, proud band"}),
    # The front cap is the front's wall lamination - it laminates to the web and
    # bears on the post shoulder exactly as the tongues do.
    frozenset({"Front cap", "Side lamination"}),    # meet at the front corner
    frozenset({"Front cap", "Perimeter web"}),
    frozenset({"Front cap", "Post, front left"}),
    frozenset({"Front cap", "Post, front right"}),
    # One board with a step: the full-depth piece and the proud band above it.
    frozenset({"Side lamination", "Side lamination, proud band"}),
    # One part drawn as two boxes, the same convention as the BF12 wing/boss.
    frozenset({"Fin angle", "Fin angle"}),
    frozenset({"Fin angle", "Front fin"}),          # it bolts to its face
    frozenset({"Fin angle bolt", "Fin angle"}),     # the head sits on the leg
    frozenset({"Fin T bolt", "Fin angle"}),         # head on the vertical leg
    frozenset({"Fin T bolt", "Front fin"}),         # it threads into the fin
    frozenset({"X beam", "X end plate"}),           # plate laps the beam's end
    frozenset({"X end plate", "Y nut doubler"}),    # doubler bolts to its face
    frozenset({"X carriage plate", "Z plate"}),     # modelled without the spacers

    # The drive train is mostly parts that pass through each other by design.
    # A screw inside its own nut is not a clash, and neither is a journal
    # inside the bearing that holds it. Declaring them is the price of having
    # the check mean something when a motor DOES foul a fin.
    frozenset({"Ball screw", "Ball nut"}),          # the nut runs on it
    frozenset({"Ball screw", "BF12 wing"}),         # thread reaches into the bore
    frozenset({"Ball screw", "BF12 boss"}),
    frozenset({"Ball screw", "Casting wing"}),
    frozenset({"Ball screw", "Casting boss"}),
    frozenset({"Screw journal", "BF12 wing"}),      # journal in its bearing
    frozenset({"Screw journal", "BF12 boss"}),
    frozenset({"Screw journal", "Casting wing"}),
    frozenset({"Screw journal", "Casting boss"}),
    # The Y casting is placed by the interposer and the screw by the rear plate,
    # so the journal runs 2.5 past the bore into the open coupler space between
    # the rails. The rails are DRAWN SOLID, which is what makes that read as a
    # clash; on the real casting it is where the coupler goes.
    frozenset({"Screw journal", "Casting rails"}),
    # each support is ONE part drawn as two boxes - a boss standing out of a wing
    frozenset({"BF12 wing", "BF12 boss"}),
    frozenset({"Casting wing", "Casting boss"}),
    # and the nut's bolting face is a face of the nut, not a separate part
    frozenset({"Ball nut", "Nut bolt face"}),
    # the casting carries its motor plate, which carries the motor
    frozenset({"Casting wing", "Motor plate"}),
    frozenset({"Casting boss", "Motor plate"}),
    frozenset({"Motor plate", "Stepper motor"}),

    # Every tongue bolt passes through a o9 clearance hole in its plate and
    # another in the tongue. The plates are drawn as solid boxes, so the check
    # sees a shank in metal. Only the SHANK is listed here - the head, washer
    # and acorn nut sit proud of their faces and clash with nothing, which is
    # the check confirming the stack is the right way round.
    frozenset({"Rear plate", "Tongue bolt"}),
    # The four BF12 bolts per beam run through the block's wing and THREAD INTO
    # the rear plate, ending flush with its back face. Both solids therefore have
    # a bolt inside them on purpose. Only the shank is listed: the head stands
    # proud of BF12's outer face and clashes with nothing, which is the check
    # confirming the stack is the right way round.
    # SINCE THE FLIP IT IS THE FIN THEY THREAD INTO, not the rear plate - and
    # the M5 x 30 ends FLUSH with the fin's outboard face rather than stopping
    # short, because T_FIN is 10 and the bolt engages exactly 10.
    frozenset({"Front fin", "BF12 bolt"}),
    frozenset({"Rear plate", "BF12 bolt"}),
    # the same joint on the X tongue and on the Z carriage plate
    frozenset({"BF12 tongue", "BF12 bolt"}),
    frozenset({"X end plate", "BF12 bolt"}),
    frozenset({"X carriage plate", "BF12 bolt"}),
    frozenset({"BF12 boss", "BF12 bolt"}),
    frozenset({"BF12 wing", "BF12 bolt"}),
    frozenset({"Back tongue", "Tongue bolt"}),
    frozenset({"Side plate", "Tongue bolt"}),
    frozenset({"Side lamination", "Tongue bolt"}),
    frozenset({"Side lamination, proud band", "Tongue bolt"}),
    # barrel, nose, shaft and nut are one spindle drawn as four cylinders
    frozenset({"Spindle barrel", "Spindle nose"}),
    frozenset({"Spindle nose", "Spindle shaft"}),
    frozenset({"Spindle shaft", "Collet nut"}),
    frozenset({"Spindle clamp", "Spindle barrel"}),  # a clamp WRAPS the barrel
    # Four M8 x 90 a clamp: 80 through the shoulder and 10 into the plate, which
    # is CLAMP_SHOULDER_OUT and CLAMP_BOLT_ENGAGE coming back out of the model.
    # Only the shank is listed - the heads stand proud of the shoulder and clash
    # with nothing, which is the check that they are the right way round.
    frozenset({"Spindle clamp", "Clamp bolt"}),
    frozenset({"Z plate", "Clamp bolt"}),
    frozenset({"Spindle clamp", "Z plate"}),         # bolts to its face
    frozenset({"Y rail", "Y block"}),               # a block WRAPS its rail
    frozenset({"X rail", "X block"}),
    frozenset({"Z rail", "Z block"}),
    frozenset({"X carriage plate", "Z rail"}),      # rail bolts to its face
    frozenset({"X carriage plate", "Z block"}),
    frozenset({"X carriage plate", "X block"}),     # carriage hangs off these
    # The shelf bar is bolted to the end plate's face and the beam sits on it,
    # so it touches both. Its four bolts cross the plate and the bar.
    # the four M8 that bolt each end plate to the beam's top extrusion
    frozenset({"X end plate", "X end plate bolt"}),
    frozenset({"X beam", "X end plate bolt"}),
    # the four T-nut bolts on each interposer bar, shank through the bar and
    # on into the extrusion's slot
    frozenset({"Interposer", "Interposer bolt"}),
    # the casting's own six, up through it into the bar - or into the carriage
    # plate on Z - so they sit inside both parts on purpose
    frozenset({"Interposer", "Casting bolt"}),
    frozenset({"Casting wing", "Casting bolt"}),
    frozenset({"Casting rails", "Casting bolt"}),
    frozenset({"Casting boss", "Casting bolt"}),
    frozenset({"X carriage plate", "Casting bolt"}),
    frozenset({"Y beam", "Interposer bolt"}),
    frozenset({"X beam", "Interposer bolt"}),
    frozenset({"Shelf bar", "X end plate"}),
    frozenset({"Shelf bar", "X beam"}),
    frozenset({"Shelf bar", "Shelf bolt"}),
    frozenset({"X end plate", "Shelf bolt"}),
    frozenset({"X beam", "Shelf bolt"}),
    # The Y sole plate laps the doubler's end face and the nut's face, and its
    # eight bolts cross it into both. Only the shanks are listed; the heads hang
    # below the plate and clash with nothing. It also BUTTS the end plate's
    # strip, which is a touching face rather than an overlap - listed because
    # two coplanar faces still register.
    frozenset({"Y sole plate", "X end plate"}),
    frozenset({"Y sole plate", "Y nut doubler"}),
    frozenset({"Y sole plate", "Nut bolt face"}),
    frozenset({"Y sole plate", "Y sole plate bolt"}),
    frozenset({"Y nut doubler", "Y sole plate bolt"}),
    frozenset({"Ball nut", "Y sole plate bolt"}),
    frozenset({"Nut bolt face", "Y sole plate bolt"}),
    # The doubler is bolted flat to the plate's back face and the sole plate
    # lands on the doubler's top edge and on the nut's bolting face - those are
    # the same plane, which is the whole point of X_NUT_FACE_Z.
    frozenset({"X carriage plate", "X nut doubler"}),
    frozenset({"X nut doubler", "X sole plate"}),
    # The eight sole-plate bolts cross the plate and thread into the part under
    # it - the doubler's tapped top edge at the root, the nut housing further
    # out. Only the shank is listed; the heads stand proud of the plate.
    frozenset({"X sole plate", "X sole bolt"}),
    frozenset({"X nut doubler", "X sole bolt"}),
    frozenset({"Ball nut", "X sole bolt"}),
    frozenset({"Nut bolt face", "X sole bolt"}),
    frozenset({"X sole plate", "Nut bolt face"}),
    frozenset({"X carriage plate", "X sole plate"}),
    # The doubler's bottom edge rests on the SIDES of the upper bearing blocks,
    # which stand 10 proud of the beam top - both parts are fixed by the same
    # carriage plate, so a touch there is the design and not a clash.
    frozenset({"X block", "X nut doubler"}),
    frozenset({"X end plate", "Y block"}),          # end plate hangs off these
    # Kept for when the carriage is parked at either end rather than mid travel:
    # butted against the end plate, the block pair is BLOCK_BUTTED 154.18 against
    # a 154 plate, so 0.09 of END CAP touches at each end. The caps are seals and
    # carry nothing; x-gantry-end-plates.md settled that. A touch of exactly this
    # size is the design.
    frozenset({"X end plate", "X block"}),
    frozenset({"Front strip", "Flange head"}),      # head seats on the strip
    frozenset({"Side plate", "Flange head"}),
    frozenset({"Rear plate", "Flange head"}),
    frozenset({"Front fin", "Flange head"}),
    # The strip bolt's flange RIM passes under the bearing block's overhang, and
    # that is measured on a real beam with rails and blocks fitted - the block has
    # BLOCK_OVERHANG_CLEAR of relief underneath that this model does not draw,
    # because its blocks are plain solids. See STRIP_STACK for the caveat: the
    # measurement was taken with a 4 mm plate, not the specified 6.35.
    frozenset({"Y block", "Flange head"}),
    frozenset({"X block", "Flange head"}),
    # A counterbore is a HOLE IN the rail, drawn as a solid because the model has
    # no boolean subtraction. It also passes under a bearing block wherever one
    # happens to sit over it, which is normal.
    # The Z top stop block. The screw runs THROUGH it, down the \u00f822 bore, and
    # the two M5 x 50 cross it into the carriage plate - 39 of block and 11 of
    # plate, which is the sheet's own arithmetic read back off the model. The
    # head sits 5 down inside a 6 counterbore, so it clashes with the block too
    # and with nothing else, which is the check that the counterbore is deep
    # enough to bury it.
    frozenset({"Ball screw", "Z stop block"}),
    frozenset({"Z stop block", "Z stop bolt"}),
    frozenset({"Z stop block", "Z stop bolt head"}),
    frozenset({"X carriage plate", "Z stop bolt"}),

    # A slot is a VOID IN the beam, drawn as a solid for want of boolean
    # subtraction - the same licence the rail counterbores take.
    frozenset({"Y beam", "Beam T-slot"}),
    frozenset({"X beam", "Beam T-slot"}),
    frozenset({"Y rail", "Rail counterbore"}),
    frozenset({"X rail", "Rail counterbore"}),
    frozenset({"Z rail", "Rail counterbore"}),
    frozenset({"Y block", "Rail counterbore"}),
    frozenset({"X block", "Rail counterbore"}),
    frozenset({"Z block", "Rail counterbore"}),
}


# Which two coordinates a prism's profile lives in, and which it extrudes
# along. Everything below reads the profile through this rather than assuming
# the fins' plane.
PLANE_AXES = {"xz": (0, 2), "xy": (0, 1)}


def through_hole(a, b) -> bool:
    """A part passing THROUGH a cut-out is not an interference.

    The prism's p/q is its bounding box, which knows nothing about the window in
    it, so the interposer running out through the fin reads as a solid clash.
    This resolves it properly rather than by adding the pair to ALLOWED: the
    other part has to sit INSIDE the hole in both axes. Move the interposer and
    it is flagged again, which is the whole point of the check.
    """
    for prism_, other in ((a, b), (b, a)):
        i, j = PLANE_AXES[prism_.get("pl", "xz")]
        for hp in prism_.get("holes", []):
            hx = [pt[0] for pt in hp]
            hz = [pt[1] for pt in hp]
            # Same 0.05 slack the overlap test uses. Needed, not cosmetic: the
            # window's edge and the beam's face are both 1208.575 but are reached
            # by different routes, so an exact compare fails on one fin and not
            # the other.
            e = 0.05
            if (min(hx) - e <= other["p"][i] and other["q"][i] <= max(hx) + e
                    and min(hz) - e <= other["p"][j] and other["q"][j] <= max(hz) + e):
                return True
    return False


def shifted(p, off):
    """One part moved by the jog, according to the carriages it rides on."""
    k = p.get("k", "")
    d = (off[0] if "X" in k else 0.0,
         off[1] if "Y" in k else 0.0,
         off[2] if "Z" in k else 0.0)
    if d == (0.0, 0.0, 0.0):
        return p
    if p.get("holes"):
        # through_hole() reads a prism's window in absolute coordinates, so a
        # prism that ever rides a carriage would take its window with it and
        # this would quietly stop working. Nothing rides today; say so loudly
        # if that changes rather than reporting a clearance that is not there.
        raise SystemExit("a prism with a window now rides a carriage - "
                         "through_hole() has to move its holes too")
    q = dict(p)
    q["p"] = [p["p"][i] + d[i] for i in range(3)]
    q["q"] = [p["q"][i] + d[i] for i in range(3)]
    return q


def overlaps_at(P, off=(0.0, 0.0, 0.0)):
    """Every pair of solids sharing space, with the carriages at one position."""
    Q = [shifted(p, off) for p in P]
    bad = []
    for i in range(len(Q)):
        for j in range(i + 1, len(Q)):
            a, b = Q[i], Q[j]
            # A LINE HAS NO VOLUME. The thread is drawn over the screw's own
            # cylinder, and that cylinder is what the check already tests, so
            # including the helix would only re-flag the screw's own envelope.
            if a["t"] == "helix" or b["t"] == "helix":
                continue
            if frozenset({a["n"], b["n"]}) in ALLOWED:
                continue
            ov = [min(a["q"][k], b["q"][k]) - max(a["p"][k], b["p"][k]) for k in range(3)]
            if (all(o > 0.05 for o in ov) and not through_hole(a, b)
                    and not prism_misses(a, b)):
                if a["t"] == "prism" or b["t"] == "prism":
                    ov = list(ov)
                    ov[0] = prism_bite(a, b)      # the real width, not the box
                bad.append((a["n"], b["n"], ov))
    return bad


def _rect_hits_poly(poly, x0, x1, z0, z1) -> bool:
    """Does the axis-aligned rectangle touch the polygon? Three ways it can."""
    def inside(px, pz):                      # crossing number, polygon in X-Z
        c = False
        n = len(poly)
        for i in range(n):
            ax, az = poly[i]
            bx, bz = poly[(i + 1) % n]
            if (az > pz) != (bz > pz):
                xx = ax + (pz - az) * (bx - ax) / (bz - az)
                if xx > px:
                    c = not c
        return c

    for px, pz in poly:                      # a corner of the part inside
        if x0 - 0.05 <= px <= x1 + 0.05 and z0 - 0.05 <= pz <= z1 + 0.05:
            return True
    for px in (x0, x1):                      # a corner of the rectangle inside
        for pz in (z0, z1):
            if inside(px, pz):
                return True
    for i in range(len(poly)):               # or an edge crossing an edge
        ax, az = poly[i]
        bx, bz = poly[(i + 1) % len(poly)]
        for _ in range(1):
            # the segment against the four sides of the rectangle
            for cx, cz, dx_, dz_ in ((x0, z0, x1, z0), (x1, z0, x1, z1),
                                     (x1, z1, x0, z1), (x0, z1, x0, z0)):
                d1 = (bx - ax) * (cz - az) - (bz - az) * (cx - ax)
                d2 = (bx - ax) * (dz_ - az) - (bz - az) * (dx_ - ax)
                d3 = (dx_ - cx) * (az - cz) - (dz_ - cz) * (ax - cx)
                d4 = (dx_ - cx) * (bz - cz) - (dz_ - cz) * (bx - cx)
                if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
                    return True
    return False


def prism_bite(a, b):
    """How wide the overlap really is across a prism, measured on its section.

    The caller prints the bounding box extents, and on a tapered part that
    number is too big - on a fin the box claims the 100 mm the taper removes.
    This walks the shared height and returns the widest run of REAL metal.
    """
    worst = 0.0
    for prism_, other in ((a, b), (b, a)):
        if prism_.get("t") != "prism":
            continue
        pts = prism_["profile"]
        # ai / aj and NOT i / j: the sampling loop below uses i, and naming the
        # axis index the same thing made it read the part's z as its x.
        ai, aj = PLANE_AXES[prism_.get("pl", "xz")]
        zs = [q[1] for q in pts]
        z0 = max(prism_["p"][aj], other["p"][aj], min(zs))
        z1 = min(prism_["q"][aj], other["q"][aj], max(zs))
        if z1 <= z0:
            continue
        for i in range(201):
            z = z0 + (z1 - z0) * i / 200
            # the section's x span at this height, from the edges it crosses
            xs = []
            for j in range(len(pts)):
                ax, az = pts[j]
                bx, bz = pts[(j + 1) % len(pts)]
                if az == bz:
                    continue
                if min(az, bz) - 1e-9 <= z <= max(az, bz) + 1e-9:
                    xs.append(ax + (z - az) * (bx - ax) / (bz - az))
            if len(xs) < 2:
                continue
            lo = max(min(xs), other["p"][ai])
            hi = min(max(xs), other["q"][ai])
            worst = max(worst, hi - lo)
    return worst


def prism_misses(a, b) -> bool:
    """A PRISM IS NOT ITS BOUNDING BOX, and on the fins the difference is the
    whole part: the taper runs 200 down to 100 on the INBOARD face, which is
    exactly where the Z assembly comes past. Comparing boxes claimed 100 mm of
    metal that is not there and reported two clashes against air.

    So where one of the pair is a prism, the overlap is re-tested against the
    real section. The fore-aft overlap is already established by the caller.
    """
    for prism_, other in ((a, b), (b, a)):
        if prism_.get("t") != "prism":
            continue
        i, j = PLANE_AXES[prism_.get("pl", "xz")]
        x0 = max(prism_["p"][i], other["p"][i])
        x1 = min(prism_["q"][i], other["q"][i])
        z0 = max(prism_["p"][j], other["p"][j])
        z1 = min(prism_["q"][j], other["q"][j])
        if not _rect_hits_poly(prism_["profile"], x0, x1, z0, z1):
            return True
    return False


def report_overlaps(P) -> int:
    """Solid-body interference check - the one thing a box model can prove.

    It cannot tell you a part is in the RIGHT place. It can tell you two parts
    are in the SAME place, which is the failure a dimension change causes and
    the eye misses on a shaded render.
    """
    bad = overlaps_at(P)
    if not bad:
        print("\ninterference check: clean - no two parts occupy the same space")
        return 0
    print(f"\ninterference check: {len(bad)} OVERLAP(S)")
    for n1, n2, ov in bad:
        print(f"  {n1} <-> {n2}   by {ov[0]:.2f} x {ov[1]:.2f} x {ov[2]:.2f} mm")
    return 0


def sweep_envelope(P, jog, home) -> int:
    """THE CORNERS, NOT JUST THE MIDDLE.

    The pose the model is drawn at is mid travel, and a clash that only happens
    at an end of travel is invisible there. Worse, the ones worth finding need
    TWO axes at once - the Z assembly can only reach a front fin with X at an
    end AND Y fully forward - so sweeping one axis at a time would not find them
    either. Eight corners is the smallest set that contains every such pair.

    It cannot prove the inside of the envelope is clear. Every part here is a
    box or a cylinder travelling in a straight line, so for any two of them the
    overlap is largest at an extreme of each axis - but the castings' rails are
    drawn SOLID and a prism's bounding box is bigger than the prism, so this is
    conservative rather than exact, the same way the drawn-pose check is.
    """
    base = {frozenset({n1, n2}) for n1, n2, _ in overlaps_at(P)}
    print(f"\nenvelope sweep: the same check at the 8 corners of travel. "
          f"{len(base)} pair(s) already overlap at the drawn pose and are not "
          f"repeated below.")
    found = {}
    for jx in jog["X"][:2]:
        for jy in jog["Y"][:2]:
            for jz in jog["Z"][:2]:
                dro = (home["X"] - jx, home["Y"] - jy, jz - home["Z"])
                label = f"X {dro[0]:+8.1f}  Y {dro[1]:+8.1f}  Z {dro[2]:+8.1f}"
                new = [b for b in overlaps_at(P, (jx, jy, jz))
                       if frozenset({b[0], b[1]}) not in base]
                if not new:
                    print(f"  {label}   clear")
                    continue
                print(f"  {label}   {len(new)} NEW")
                for n1, n2, ov in new:
                    print(f"      {n1} <-> {n2}   by "
                          f"{ov[0]:.2f} x {ov[1]:.2f} x {ov[2]:.2f} mm")
                    key = frozenset({n1, n2})
                    found[key] = max(found.get(key, 0), min(ov))
    if found:
        print(f"\n  {len(found)} distinct pair(s) foul somewhere in the envelope:")
        for k, worst in sorted(found.items(), key=lambda kv: -kv[1]):
            print(f"    {' <-> '.join(sorted(k))}   worst bite {worst:.2f} mm")
    else:
        print("  nothing new at any corner.")
    return 0


HTML = r"""<!doctype html>
<meta charset="utf-8"><title>CNC assembly - generated from the dimension registry</title>
<style>
 html,body{margin:0;height:100%;background:#1a1d21;color:#ddd;
   font:13px/1.5 "Segoe UI",system-ui,sans-serif;overflow:hidden}
 #c{position:fixed;inset:0}
 .panel{position:fixed;background:#23272dEE;border:1px solid #3a4048;border-radius:6px;padding:10px 12px}
 /* THE CONTROLS ARE A ROW ACROSS THE TOP OF THE WINDOW, not one Menu button -
    his, 2026-10-11. Everything that used to sit at the top of the window is
    pushed below the bar, so the bar never covers a readout. */
 #bar{top:0;left:0;right:0;display:flex;flex-wrap:wrap;gap:6px;align-items:center;
   padding:7px 10px;border:none;border-bottom:1px solid #3a4048;border-radius:0;z-index:10}
 #bar h1{margin:0 10px 0 2px}
 .mwrap{position:relative;display:inline-block}
 .drop{position:absolute;top:calc(100% + 6px);left:0;border:1px solid #3a4048;
   border-radius:5px;background:#1d2126;padding:3px 0;min-width:190px;z-index:11}
 #facts{top:56px;left:12px;max-width:280px;margin-top:0}
 h1{font-size:14px;margin:0 0 8px}
 label{display:block;cursor:pointer;padding:1px 0}
 input{vertical-align:-2px;margin-right:6px}
 table{border-collapse:collapse;font-size:11.5px;margin-top:8px}
 td{padding:1px 10px 1px 0}
 td.n{text-align:right;color:#8fd}
 b.w{color:#e8b64c}
 ul{margin:4px 0 0;padding-left:16px}
 li{margin:3px 0}
 #tip{position:fixed;display:none;max-width:300px;z-index:9;pointer-events:none;
   background:#0e1114F2;border:1px solid #4a515a;border-radius:4px;padding:6px 9px;
   font-size:11.5px;line-height:1.45;color:#dde}
 #tip .dim{color:#8fd}
 /* The two readouts share one row at the top right. Travel is the left of
    the pair, so when the DRO is switched off it falls into the DRO's place
    without anything having to measure or move. */
 #topright{position:fixed;top:56px;right:12px;display:flex;gap:10px;align-items:flex-start}
 #topright .panel{position:static}
 #jogro h2{font-size:11px;margin:0 0 4px;color:#e8b64c;letter-spacing:.06em}
 #jogro table{font:13px/1.35 "Consolas",ui-monospace,monospace;border-collapse:collapse;margin:0}
 #jogro td{padding:0 2px}
 #jogro td.ax{color:#e8b64c;padding-right:4px}
 #jogro td.e{text-align:right;color:#8a929b}
 #jogro td.v{text-align:right;color:#8fd}
 #jogro td.v.stop{color:#e8613d}
 #jogro td.br,#jogro td.d{color:#5c646d}
 button{background:#2f353d;color:#cde;border:1px solid #454c55;border-radius:4px;
   padding:3px 10px;cursor:pointer;font:11.5px inherit}
 button:hover{background:#39414a}
 button.on{background:#3d4a39;border-color:#5a6b53;color:#dfe}
 .mrow{padding:3px 10px;cursor:pointer;white-space:nowrap}
 .mrow:hover{background:#2f353d}
 /* One row per group, the box in its own column so the names line up. */
 table.ptable{margin:0;font-size:12px}
 table.ptable td{padding:2px 10px 2px 0;cursor:pointer;white-space:nowrap}
 table.ptable td:first-child{padding:2px 2px 2px 8px}
 table.ptable tr:hover{background:#2f353d}
 #dro{min-width:150px}
 #dro h2{font-size:11px;margin:0 0 4px;color:#e8b64c;letter-spacing:.06em}
 #dro table{font:15px/1.35 "Consolas",ui-monospace,monospace;border-collapse:collapse}
 #dro td.ax{color:#e8b64c;padding-right:10px}
 #dro td.v{text-align:right;color:#8fd}
 #dro .frame{margin-top:6px;font-size:10.5px;color:#8a929b;max-width:200px;white-space:normal}
 #clashlist{top:56px;left:12px;max-width:260px;max-height:70vh;overflow-y:auto;font-size:11.5px}
 #clashlist h2{font-size:11px;margin:0 0 6px;color:#ff6b5a;letter-spacing:.06em}
 .cl{border-left:3px solid #ff2b2b;padding:2px 0 2px 7px;margin:0 0 6px;color:#cdd}
 .cl.bite{border-left-color:#25c08a}
 button.alarm{background:#5a2a2a;border-color:#8a4040;color:#fee}
 #help,#about{top:56px;left:50%;transform:translateX(-50%);max-width:520px;font-size:12px}
 #about{max-height:78vh;overflow-y:auto}
 #help h2,#about h2{font-size:12.5px;margin:0 0 6px;color:#e8b64c}
 #help b,#about b{color:#e8b64c}
 #help .close,#about .close{float:right;cursor:pointer;color:#8fd}
 #help table{border-collapse:collapse}
 #help td{padding:1px 12px 1px 0;vertical-align:top}
 #help td:first-child{white-space:nowrap}
</style>
<canvas id="c"></canvas>
<div id="tip"></div>
<div class="panel" id="bar"><h1>CNC assembly</h1></div>
<table class="panel" id="facts" hidden></table>
<div id="topright"><div class="panel" id="jogro" hidden></div>
<div class="panel" id="dro"></div></div>
<div class="panel" id="clashlist" hidden></div>
<div class="panel" id="help" hidden></div>
<div class="panel" id="about" hidden></div>
<script>__THREE__</script>
<script>
const PARTS=__PARTS__, GROUPS=__GROUPS__, ASSUMPTIONS=__ASSUMPTIONS__, FACTS=__FACTS__;
const JOG=__JOG__, TIP=__TIP__, HOME=__HOME__;
const ALLOWED=__ALLOWED__, BITE=__BITE__;

const scene=new THREE.Scene(); scene.background=new THREE.Color(0x1a1d21);
const cam=new THREE.PerspectiveCamera(42,1,10,20000);
const rend=new THREE.WebGLRenderer({canvas:document.getElementById('c'),antialias:true});
scene.add(new THREE.HemisphereLight(0xffffff,0x40454d,1.05));
const key=new THREE.DirectionalLight(0xffffff,0.75); key.position.set(1,2,1.4); scene.add(key);

// Centre everything on the machine so the orbit pivot is sensible.
let lo=[1e9,1e9,1e9], hi=[-1e9,-1e9,-1e9];
PARTS.forEach(p=>{for(let i=0;i<3;i++){lo[i]=Math.min(lo[i],p.p[i]);hi[i]=Math.max(hi[i],p.q[i]);}});
const mid=[0,1,2].map(i=>(lo[i]+hi[i])/2);
const span=Math.max(hi[0]-lo[0],hi[1]-lo[1],hi[2]-lo[2]);

// machine (x,y,z) -> three (x, z, -y); three's Y is up, and fore-aft runs to -Z
// THE THREE CARRIAGES, NESTED THE WAY THE MACHINE IS: Z rides on X, X rides on
// Y. So one translation per group is enough - moving the gantry carries the X
// carriage and everything on the Z axis with it, without touching their own
// offsets. A part's k says which group it belongs in; the frame goes in the
// scene and never moves.
const GY=new THREE.Group(), GX=new THREE.Group(), GZ=new THREE.Group();
scene.add(GY); GY.add(GX); GX.add(GZ);
const RIDE={Y:GY,YX:GX,YXZ:GZ};
const byGroup={}, PICK=[];
// A PRISM'S OUTLINE IS DRAWN FROM ITS OWN PROFILE, not from EdgesGeometry.
// 🔴 EdgesGeometry on an extruded shape WITH HOLES draws the cap triangulator's
// seams as if they were real edges. On the bottom skin that put a line straight
// across the inside of the box, 1087 mm from the back of one front tenon hole
// to the back of the other - he spotted it with the top skin switched off, and
// the tooltip did not change over it because an edge overlay is not a part.
// Measured in node against this very three.js: four such segments, two on each
// face, at exactly y 1148, which is the tenon line.
//
// The loops ARE the outline, so drawing them needs no triangulator and cannot
// invent an edge: each loop twice, once at each end of the extrusion, plus one
// upright at every vertex.
function prismEdges(p){
  const xy=(p.pl==='xy');
  const u=pt=>pt[0]-mid[0], w=pt=>xy?(pt[1]-mid[1]):(pt[1]-mid[2]);
  const d=p.yb-p.ya, v=[];
  for(const lp of [p.profile].concat(p.holes||[])){
    for(let i=0;i<lp.length;i++){
      const a=lp[i], b=lp[(i+1)%lp.length];
      v.push(u(a),w(a),0, u(b),w(b),0);     // this end
      v.push(u(a),w(a),d, u(b),w(b),d);     // the far end
      v.push(u(a),w(a),0, u(a),w(a),d);     // and the corner between them
    }
  }
  const g=new THREE.BufferGeometry();
  g.setAttribute('position',new THREE.Float32BufferAttribute(v,3));
  // the same turn the mesh gets, because this rides on the mesh
  if(xy)g.rotateX(-Math.PI/2);
  return g;
}

for(const p of PARTS){
  let geom, ctr;
  if(p.t==='helix'){
    // ONE RIGHT-HAND POLYLINE at the crest, over the plain cylinder. Drawn
    // 0.05 clear of the surface on purpose: exactly on it z-fights with it,
    // and 0.05 out puts the near side cleanly in front while the cylinder
    // still hides the far side, which is what makes it read as a thread.
    //
    // Machine X / fore-aft / Z is right-handed and the mapping into three's
    // frame is a rotation, so a right-hand helix stays right-hand on screen.
    // The ONE exception is a screw along fore-aft: there cyl's (cx,cy) order
    // swaps two axes rather than rotating them, so the angle runs backwards
    // and has to be negated to keep the hand right.
    const turns=(p.z1-p.z0)/p.lead, segs=Math.max(8,Math.round(turns*24));
    const R=p.r+0.05, hand=(p.ax==='y')?-1:1, pts=[];
    for(let i=0;i<=segs;i++){
      const f=i/segs, a=2*Math.PI*turns*f*hand, L=p.z0+(p.z1-p.z0)*f;
      const u=p.cx+R*Math.cos(a), w=p.cy+R*Math.sin(a);
      if(p.ax==='x')      pts.push(new THREE.Vector3(L-mid[0], w-mid[2], -(u-mid[1])));
      else if(p.ax==='y') pts.push(new THREE.Vector3(u-mid[0], w-mid[2], -(L-mid[1])));
      else                pts.push(new THREE.Vector3(u-mid[0], L-mid[2], -(w-mid[1])));
    }
    const ln=new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),
                            new THREE.LineBasicMaterial({color:p.c}));
    (RIDE[p.k]||scene).add(ln);
    // It toggles with its group, but it is NOT in PICK - hovering the screw
    // should report the screw, not a line lying on its surface.
    (byGroup[p.g]=byGroup[p.g]||[]).push(ln);
    continue;
  }
  if(p.t==='cyl'){
    geom=new THREE.CylinderGeometry(p.r,p.r,p.z1-p.z0,p.seg||36);
    const m=(p.z0+p.z1)/2;
    if(p.ax==='x'){      // machine X: cx is fore-aft, cy is height
      geom.rotateZ(Math.PI/2); ctr=[m-mid[0],p.cy-mid[2],-(p.cx-mid[1])];
    }else if(p.ax==='y'){ // machine fore-aft: cx is across, cy is height
      geom.rotateX(Math.PI/2); ctr=[p.cx-mid[0],p.cy-mid[2],-(m-mid[1])];
    }else{
      ctr=[p.cx-mid[0],m-mid[2],-(p.cy-mid[1])];
    }
  }else if(p.t==='prism'){
    // Two planes. "xz" is a section across and up, extruded along fore-aft -
    // the fins. "xy" is across and OUT from the Z plate, extruded along Z -
    // the spindle clamps. Either way the profile is built in the shape's own
    // plane and the mesh is then turned to stand the right way up.
    const xy=(p.pl==='xy');
    const u=pt=>pt[0]-mid[0], w=pt=>xy?(pt[1]-mid[1]):(pt[1]-mid[2]);
    const sh=new THREE.Shape();
    p.profile.forEach((pt,i)=>i?sh.lineTo(u(pt),w(pt)):sh.moveTo(u(pt),w(pt)));
    sh.closePath();
    (p.holes||[]).forEach(hp=>{
      const hs=new THREE.Path();
      hp.forEach((pt,i)=>i?hs.lineTo(u(pt),w(pt)):hs.moveTo(u(pt),w(pt)));
      hs.closePath(); sh.holes.push(hs);
    });
    geom=new THREE.ExtrudeGeometry(sh,{depth:p.yb-p.ya,bevelEnabled:false});
    if(xy){
      // the shape's second axis is machine fore-aft, which is three's -Z, and
      // the extrusion is machine Z, which is three's +Y
      geom.rotateX(-Math.PI/2);
      ctr=[0,p.ya-mid[2],0];
    }else{
      ctr=[0,0,-(p.yb-mid[1])];
    }
  }else{
    const s=[0,1,2].map(i=>Math.max(p.q[i]-p.p[i],0.4));
    geom=new THREE.BoxGeometry(s[0],s[2],s[1]);
    ctr=[(p.p[0]+p.q[0])/2-mid[0],(p.p[2]+p.q[2])/2-mid[2],-((p.p[1]+p.q[1])/2-mid[1])];
  }
  const g=new THREE.Mesh(geom,new THREE.MeshLambertMaterial({color:p.c,side:THREE.DoubleSide}));
  g.position.set(ctr[0],ctr[1],ctr[2]);
  const e=new THREE.LineSegments(
    p.t==='prism'?prismEdges(p):new THREE.EdgesGeometry(g.geometry),
    new THREE.LineBasicMaterial({color:0x000000,opacity:0.35,transparent:true}));
  g.add(e); (RIDE[p.k]||scene).add(g);
  g.userData.part=p; PICK.push(g);
  (byGroup[p.g]=byGroup[p.g]||[]).push(g);
}

// ground plane at the box's underside
const gy=lo[2]-mid[2];
const grid=new THREE.GridHelper(span*2.2, 22, 0x44505c, 0x2b3139); grid.position.y=gy; scene.add(grid);

// --- orbit and pan: written out rather than pulled from a second CDN file --
// LEFT DRAG PANS, MIDDLE DRAG ORBITS. His call - on a model this size you spend
// far more time sliding across it than swinging around it, and the left button
// is the one your hand is already on.
let az=-2.42, el=0.42, dist=span*1.75, down=null, mode=null;
const tgt=new THREE.Vector3(0,0,0);
function place(){
  cam.position.set(tgt.x+dist*Math.cos(el)*Math.sin(az),
                   tgt.y+dist*Math.sin(el),
                   tgt.z+dist*Math.cos(el)*Math.cos(az));
  cam.lookAt(tgt);
}
const onPanel=e=>!!(e.target.closest&&e.target.closest('.panel'));
addEventListener('pointerdown',e=>{
  if(onPanel(e))return;              // a click on the UI is not a drag on the model
  // A MODIFIED LEFT CLICK HIDES WHAT IS UNDER THE CURSOR - his, 2026-10-11.
  // It swallows the left button's own drag, so the model does not pan as the
  // part goes. Show all parts brings every one of them back.
  if(e.button===0&&(e.ctrlKey||e.shiftKey)){
    hideAt(e); e.preventDefault(); return;
  }
  if(e.button!==0&&e.button!==1)return;
  if(e.button===1)e.preventDefault();          // middle-click autoscroll
  down=[e.clientX,e.clientY]; mode=e.button===0?'pan':'orbit';});
addEventListener('pointerup',()=>{down=null;mode=null;});
addEventListener('pointercancel',()=>{down=null;mode=null;});
addEventListener('pointermove',e=>{if(!down)return;
  const dx=e.clientX-down[0], dy=e.clientY-down[1];
  if(mode==='orbit'){
    az-=dx*0.006; el=Math.max(-1.45,Math.min(1.45,el+dy*0.006));
  }else{
    // world units per pixel at the pivot's depth, so the model tracks the cursor
    const k=2*dist*Math.tan(cam.fov*Math.PI/360)/innerHeight;
    const right=new THREE.Vector3(), up=new THREE.Vector3();
    cam.matrixWorld.extractBasis(right,up,new THREE.Vector3());
    tgt.addScaledVector(right,-dx*k).addScaledVector(up,dy*k);
  }
  down=[e.clientX,e.clientY]; place(); draw();});
addEventListener('wheel',e=>{e.preventDefault();dist=Math.max(span*0.25,Math.min(span*6,dist*(1+Math.sign(e.deltaY)*0.11)));place();draw();},{passive:false});

// --- jog: the cursor keys drive the three carriages ---------------------
// Machine axes, not screen directions: X is measured across the machine FROM
// BEHIND, fore-aft is +Y toward the operator, Z is up. The limits come from the
// generator, each one a 5 mm standoff off a part the model already places.
const JOGPOS={Y:0,X:0,Z:0};
// LEFT AND RIGHT ARE NOT THE SIGN OF MACHINE X. X is measured across the
// machine FROM BEHIND, so on screen +X runs to the LEFT - his, 2026-10-10.
const KEYS={ArrowLeft:['X',+1],ArrowRight:['X',-1],
            ArrowUp:['Y',-1],ArrowDown:['Y',+1],
            PageUp:['Z',+1],PageDown:['Z',-1]};
// Each pair is [what the low end of the offset is called, what the high end is].
// X reads reversed for the same reason the keys do.
// What the DRO reads for one axis at a given jog offset. X and Y are home
// MINUS current because both home ends sit at the high end of their machine
// axis; Z is the other way about. Home therefore always reads zero.
const axisDro=(ax,j)=>ax==='Z'?j-HOME.Z:HOME[ax]-j;
const j1=n=>String(Math.round(n*10)/10);

function applyJog(){
  GY.position.z=-JOGPOS.Y;        // machine +Y is forward, which is three's -Z
  GX.position.x=JOGPOS.X;
  GZ.position.y=JOGPOS.Z;
  // the raycaster reads matrixWorld, and a hover can land before the next draw
  scene.updateMatrixWorld(true);
  // ONE LINE PER AXIS, IN THE SAME NUMBERS THE DRO SHOWS: where home is, where the tool
  // is now, and where the far stop is. Home is always the zero, so the first
  // figure is always 0 and the last is the travel, signed the way that axis
  // runs. Reading the same numbers as the DRO is the point - a position you
  // cannot compare against the travel is just another number.
  const rows=['X','Y','Z'].map(ax=>{
    const L=JOG[ax], home=HOME[ax];
    const far=(Math.abs(L[0]-home)<1e-6)?L[1]:L[0];
    const cur=axisDro(ax,JOGPOS[ax]), end=axisDro(ax,far);
    const atStop=Math.abs(cur)<1e-6||Math.abs(cur-end)<1e-6;
    return '<tr><td class="ax">'+ax+'</td><td class="br">[</td>'+
      '<td class="e">0</td><td class="d">...</td>'+
      '<td class="v'+(atStop?' stop':'')+'">'+j1(cur)+'</td>'+
      '<td class="d">...</td><td class="e">'+j1(end)+'</td><td class="br">]</td></tr>';
  }).join('');
  // THE DRO IS THE TOOL TIP, MEASURED FROM HOME - zero in the back left corner
  // at the top of travel, and from there X runs POSITIVE to the right while Y
  // and Z run NEGATIVE, which is how the Mega V reads. His, 2026-10-10.
  //
  // X and Y are home MINUS current because both home ends are at the high end
  // of their machine axis: left is max machine X and back is min fore-aft, and
  // fore-aft runs forward, so moving forward has to come out negative.
  const v2=n=>(n<0?'-':'')+Math.abs(n).toFixed(2);
  document.getElementById('dro').innerHTML='<h2>DRO</h2><table>'+
    [['X',axisDro('X',JOGPOS.X)],['Y',axisDro('Y',JOGPOS.Y)],['Z',axisDro('Z',JOGPOS.Z)]]
      .map(r=>'<tr><td class="ax">'+r[0]+'</td><td class="v">'+v2(r[1])+'</td></tr>').join('')+
    '</table>';
  jogro.innerHTML='<h2>TRAVEL</h2><table>'+rows+'</table>';
  paintClashes();   // the carriages moved, so the answer may have
}

addEventListener('keydown',e=>{
  // HOME GOES HOME - the back left corner at the top of travel, where the DRO
  // reads zero. It used to return to the drawn pose, which is mid travel.
  if(e.key==='Home'){
    JOGPOS.X=HOME.X; JOGPOS.Y=HOME.Y; JOGPOS.Z=HOME.Z;
    e.preventDefault(); applyJog(); draw(); return;}
  const k=KEYS[e.key]; if(!k)return;
  e.preventDefault();
  const ax=k[0], L=JOG[ax];
  const step=(e.shiftKey?1:e.ctrlKey?50:10)*k[1];
  JOGPOS[ax]=Math.max(L[0],Math.min(L[1],JOGPOS[ax]+step));
  applyJog(); draw();
});

// --- hover: say what the part under the cursor IS -----------------------
// The one place the model says what a part is rather than where it is. The
// fastener lines carry a designation only where the registry has one and say
// LENGTH NOT RECORDED where it does not - see DETAIL in tools/make-3d.py.
const ray=new THREE.Raycaster(), tip=document.getElementById('tip');
const f2=n=>Math.round(n*100)/100;
function sizeOf(p){
  if(p.t==='cyl')
    return '&oslash;'+f2(2*p.r)+' x '+f2(p.z1-p.z0)+' mm long, along '+(p.ax||'z').toUpperCase();
  return f2(p.q[0]-p.p[0])+' x '+f2(p.q[1]-p.p[1])+' x '+f2(p.q[2]-p.p[2])+
         ' mm (X x fore-aft x Z)';
}
// THE RAYCASTER DOES NOT TEST .visible, so a part in a hidden group is still
// hit - take the first intersection that is actually on the screen. Both the
// hover and Ctrl+click go through here, so they can never disagree about which
// part is under the cursor.
function pickAt(e){
  ray.setFromCamera({x:e.clientX/innerWidth*2-1,y:-(e.clientY/innerHeight)*2+1},cam);
  return ray.intersectObjects(PICK,false).find(x=>x.object.visible);
}
// WHAT A MODIFIED CLICK HIDES - his, 2026-10-11:
//   Shift        the part alone, its fasteners left standing, which is how you
//                see whether a bolt fouls something once the metal is out of
//                the way
//   Ctrl         the part AND the fasteners that hold it
//   Ctrl + Shift the whole group the part belongs to, box unticked to match
// A part that has to be drawn as several boxes carries a unit id - the tee
// track bed's flats are slices of one 250 panel, not parts - and the whole
// unit goes together.
function unitMeshes(m){
  const u=m.userData.part.u;
  return u?PICK.filter(x=>x.userData.part.u===u):[m];
}
// A fastener is a part in the bolts group, and the ones holding this part are
// the ones its metal touches. Tested in WORLD space with a 0.3 mm skin: a bolt
// head sits ON a face rather than inside it, and the part and the fastener can
// ride different carriages.
function fastenersOn(ms){
  scene.updateMatrixWorld(true);
  const near=ms.map(m=>new THREE.Box3().setFromObject(m).expandByScalar(0.3));
  return PICK.filter(x=>x.userData.part.g==='bolts'&&ms.indexOf(x)<0&&
    near.some(b=>b.intersectsBox(new THREE.Box3().setFromObject(x))));
}
function hideAt(e){
  const h=pickAt(e); if(!h)return;
  const p=h.object.userData.part;
  if(e.ctrlKey&&e.shiftKey){
    GON[p.g]=false; if(gbox[p.g])gbox[p.g].checked=false;
  }else{
    let ms=unitMeshes(h.object);
    if(e.ctrlKey)ms=ms.concat(fastenersOn(ms));
    ms.forEach(x=>{x.userData.hid=true;});
  }
  applyVis(); tip.style.display='none';
}
addEventListener('pointermove',e=>{
  if(down||onPanel(e)){tip.style.display='none';return;}
  const h=pickAt(e);
  if(!h){tip.style.display='none';return;}
  const p=h.object.userData.part;
  tip.innerHTML='<b class="w">'+p.n+'</b><br>'+(p.d?p.d+'<br>':'')+
    '<span class="dim">'+sizeOf(p)+' &middot; '+(GROUPS[p.g]||p.g)+'</span>';
  tip.style.display='block';
  const w=tip.offsetWidth, th=tip.offsetHeight;
  tip.style.left=Math.max(6,Math.min(e.clientX+14,innerWidth-w-8))+'px';
  tip.style.top=(e.clientY+18+th>innerHeight?Math.max(6,e.clientY-th-12):e.clientY+18)+'px';
});

// --- the live clash check, ported from tools/make-3d.py ---------------
// CLASH-CHECK-BEGIN
// FLAG: THIS IS A SECOND IMPLEMENTATION OF A CHECK THAT ALREADY EXISTS, which is
// a thing this repo is right to be suspicious of. Three guards: the exclusion
// list and the bite list are HANDED OVER from the generator rather than
// retyped; every helper below is a line-for-line port with the same 0.05
// slack; and tools/check-clash-js.py lifts this function out of the generated
// page and runs it under node against the Python answer at the drawn pose and
// all eight corners of travel. If they ever disagree, that script says so.
const PLANE_AXES={xz:[0,2],xy:[0,1]};
const ALLOW=new Set(ALLOWED.map(x=>x[0]+'|'+x[1]));
const BITES=new Set(BITE.map(x=>x[0]+'|'+x[1]));
const pairKey=(a,b)=>a<b?a+'|'+b:b+'|'+a;

function shiftPart(p,off){
  const k=p.k||'';
  const d=[k.indexOf('X')>=0?off[0]:0,
           k.indexOf('Y')>=0?off[1]:0,
           k.indexOf('Z')>=0?off[2]:0];
  if(!d[0]&&!d[1]&&!d[2])return p;
  const q=Object.create(p);
  q.p=[p.p[0]+d[0],p.p[1]+d[1],p.p[2]+d[2]];
  q.q=[p.q[0]+d[0],p.q[1]+d[1],p.q[2]+d[2]];
  return q;
}

function rectHitsPoly(poly,x0,x1,z0,z1){
  const inside=(px,pz)=>{
    let c=false;
    for(let i=0;i<poly.length;i++){
      const [ax,az]=poly[i], [bx,bz]=poly[(i+1)%poly.length];
      if((az>pz)!==(bz>pz)){
        const xx=ax+(pz-az)*(bx-ax)/(bz-az);
        if(xx>px)c=!c;
      }
    }
    return c;
  };
  for(const [px,pz] of poly)
    if(x0-0.05<=px&&px<=x1+0.05&&z0-0.05<=pz&&pz<=z1+0.05)return true;
  for(const px of [x0,x1])for(const pz of [z0,z1])if(inside(px,pz))return true;
  for(let i=0;i<poly.length;i++){
    const [ax,az]=poly[i], [bx,bz]=poly[(i+1)%poly.length];
    for(const [cx,cz,dx_,dz_] of [[x0,z0,x1,z0],[x1,z0,x1,z1],
                                  [x1,z1,x0,z1],[x0,z1,x0,z0]]){
      const d1=(bx-ax)*(cz-az)-(bz-az)*(cx-ax);
      const d2=(bx-ax)*(dz_-az)-(bz-az)*(dx_-ax);
      const d3=(dx_-cx)*(az-cz)-(dz_-cz)*(ax-cx);
      const d4=(dx_-cx)*(bz-cz)-(dz_-cz)*(bx-cx);
      if(((d1>0)!==(d2>0))&&((d3>0)!==(d4>0)))return true;
    }
  }
  return false;
}

// A part passing THROUGH a cut-out is not an interference.
function throughHole(a,b){
  for(const [pr,other] of [[a,b],[b,a]]){
    const [i,j]=PLANE_AXES[pr.pl||'xz'], e=0.05;
    for(const hp of (pr.holes||[])){
      const hx=hp.map(t=>t[0]), hz=hp.map(t=>t[1]);
      if(Math.min(...hx)-e<=other.p[i]&&other.q[i]<=Math.max(...hx)+e
       &&Math.min(...hz)-e<=other.p[j]&&other.q[j]<=Math.max(...hz)+e)return true;
    }
  }
  return false;
}

// A PRISM IS NOT ITS BOUNDING BOX - on the fins the taper is the whole part.
function prismMisses(a,b){
  for(const [pr,other] of [[a,b],[b,a]]){
    if(pr.t!=='prism')continue;
    const [i,j]=PLANE_AXES[pr.pl||'xz'];
    const x0=Math.max(pr.p[i],other.p[i]), x1=Math.min(pr.q[i],other.q[i]);
    const z0=Math.max(pr.p[j],other.p[j]), z1=Math.min(pr.q[j],other.q[j]);
    if(!rectHitsPoly(pr.profile,x0,x1,z0,z1))return true;
  }
  return false;
}

// How wide the overlap really is across a prism, measured on its section.
function prismBite(a,b){
  let worst=0;
  for(const [pr,other] of [[a,b],[b,a]]){
    if(pr.t!=='prism')continue;
    const pts=pr.profile, [ai,aj]=PLANE_AXES[pr.pl||'xz'];
    const zs=pts.map(t=>t[1]);
    const z0=Math.max(pr.p[aj],other.p[aj],Math.min(...zs));
    const z1=Math.min(pr.q[aj],other.q[aj],Math.max(...zs));
    if(z1<=z0)continue;
    for(let i=0;i<=200;i++){
      const z=z0+(z1-z0)*i/200, xs=[];
      for(let j=0;j<pts.length;j++){
        const [ax,az]=pts[j], [bx,bz]=pts[(j+1)%pts.length];
        if(az===bz)continue;
        if(Math.min(az,bz)-1e-9<=z&&z<=Math.max(az,bz)+1e-9)
          xs.push(ax+(z-az)*(bx-ax)/(bz-az));
      }
      if(xs.length<2)continue;
      const lo=Math.max(Math.min(...xs),other.p[ai]);
      const hi=Math.min(Math.max(...xs),other.q[ai]);
      worst=Math.max(worst,hi-lo);
    }
  }
  return worst;
}

// Every pair of solids sharing space, with the carriages where they are now.
function clashesAt(off){
  // SORTED BY MACHINE X AND THE INNER LOOP BREAKS - 779 parts is 303k pairs,
  // which measured 17 ms a pass, and this runs on every jog keypress. Sorting
  // on one axis and stopping as soon as a part starts beyond the current one's
  // far face skips only pairs that CANNOT overlap, so the answer is identical -
  // tools/check-clash-js.py is what proves that, at nine poses.
  const Q=PARTS.filter(p=>p.t!=='helix').map(p=>shiftPart(p,off));
  Q.sort((u,w)=>u.p[0]-w.p[0]);
  const out=[];
  for(let i=0;i<Q.length;i++){
    const a=Q[i];
    for(let j=i+1;j<Q.length;j++){
      const b=Q[j];
      if(b.p[0]>=a.q[0]-0.05)break;     // and so does everything after it
      if(a.q[1]-b.p[1]<=0.05||b.q[1]-a.p[1]<=0.05)continue;
      if(a.q[2]-b.p[2]<=0.05||b.q[2]-a.p[2]<=0.05)continue;
      const k=pairKey(a.n,b.n);
      if(ALLOW.has(k))continue;
      if(throughHole(a,b)||prismMisses(a,b))continue;
      const ov=[0,1,2].map(t=>Math.min(a.q[t],b.q[t])-Math.max(a.p[t],b.p[t]));
      if(a.t==='prism'||b.t==='prism')ov[0]=prismBite(a,b);
      out.push({a:a.n,b:b.n,ov:ov,bite:BITES.has(k),
                lo:[0,1,2].map(t=>Math.max(a.p[t],b.p[t])),
                hi:[0,1,2].map(t=>Math.min(a.q[t],b.q[t]))});
    }
  }
  return out;
}
// CLASH-CHECK-END

// --- drawing what the check found -------------------------------------
// RED IS A CLASH, GREEN IS A BITE. The tool in the sacrificial sheet is the
// machine doing its job and must not read as a fault; everything else in red
// is two solids in the same space. The boxes are drawn WITHOUT depth testing
// on purpose - a clash is usually buried inside the parts that cause it, and a
// marker you can only see by hiding the machine is a marker you will not see.
const clashGrp=new THREE.Group(); scene.add(clashGrp);
let clashOn=false, clashBtn=null, clashList=null, CLASHES=[];
const f1=n=>Math.round(n*100)/100;

function paintClashes(){
  while(clashGrp.children.length){
    const m=clashGrp.children.pop(); m.geometry.dispose(); clashGrp.remove(m);
  }
  CLASHES=clashesAt([JOGPOS.X,JOGPOS.Y,JOGPOS.Z]);
  for(const c of CLASHES){
    const s=[0,1,2].map(t=>Math.max(c.hi[t]-c.lo[t],0.3));
    const m=new THREE.Mesh(new THREE.BoxGeometry(s[0],s[2],s[1]),
      new THREE.MeshBasicMaterial({color:c.bite?0x25c08a:0xff2b2b,
        transparent:true,opacity:0.55,depthTest:false}));
    m.position.set((c.lo[0]+c.hi[0])/2-mid[0],(c.lo[2]+c.hi[2])/2-mid[2],
                   -((c.lo[1]+c.hi[1])/2-mid[1]));
    m.renderOrder=999;
    clashGrp.add(m);
  }
  clashGrp.visible=clashOn;
  const hard=CLASHES.filter(c=>!c.bite).length, bite=CLASHES.length-hard;
  if(clashBtn){
    clashBtn.textContent='Clashes ('+hard+(bite?' + '+bite+' bite':'')+')';
    clashBtn.classList.toggle('alarm',hard>0);
    clashBtn.classList.toggle('on',clashOn);
  }
  if(clashList){
    clashList.innerHTML=CLASHES.length
      ? '<h2>'+(hard?'CLASHES':'NO CLASH')+'</h2>'+CLASHES.map(c=>
          '<div class="cl'+(c.bite?' bite':'')+'"><b>'+c.a+'</b> &amp; <b>'+c.b+
          '</b><br>'+(c.bite?'cuts ':'overlaps ')+f1(c.ov[0])+' x '+f1(c.ov[1])+
          ' x '+f1(c.ov[2])+' mm'+(c.bite?' - the job, not a fault':'')+'</div>'
        ).join('')
      : '<h2>NO CLASH</h2><div class="cl">Nothing shares space at this position.</div>';
    clashList.hidden=!clashOn;
  }
}

function resize(){const w=innerWidth,h=innerHeight;rend.setPixelRatio(devicePixelRatio);rend.setSize(w,h);cam.aspect=w/h;cam.updateProjectionMatrix();draw();}
function draw(){rend.render(scene,cam);}
addEventListener('resize',resize);

// ISO LOOKS FROM THE FRONT AND THE OPERATOR'S RIGHT - his, 2026-10-10. The
// azimuth is the old one swung round behind-to-front: cos(az) negative puts the
// camera forward of the machine, sin(az) negative puts it on the MIN X side,
// which is the operator's right when they are standing at the front.
// LEFT AND RIGHT ARE AS THE OPERATOR SEES THEM, standing at the front - so the
// Left view looks from the MAX X side. They were the other way round, which was
// the same mix-up the jog keys had.
const VIEWS={iso:[-2.42,0.42],front:[Math.PI,0.06],back:[0,0.06],
             left:[Math.PI/2,0.06],right:[-Math.PI/2,0.06],top:[0,1.44]};

// --- a row of buttons across the top, each one its own drop ------------
const bar=document.getElementById('bar');
const facts=document.getElementById('facts'), dro=document.getElementById('dro');
const help=document.getElementById('help'), about=document.getElementById('about');
const jogro=document.getElementById('jogro');
clashList=document.getElementById('clashlist');

function mrow(label,parent){
  const d=document.createElement('div');
  d.className='mrow'; d.textContent=label;
  parent.appendChild(d); return d;
}
const DROPS=[];
function closeDrops(){DROPS.forEach(d=>{d.hidden=true;});}
function bbtn(label,title){
  const b=document.createElement('button');
  b.textContent=label; if(title)b.title=title;
  bar.appendChild(b); return b;
}
// A button with a panel under it. Opening one shuts the others, so there is
// never more than one drop over the model.
function bdrop(label,title){
  const w=document.createElement('span'); w.className='mwrap';
  const b=document.createElement('button'); b.textContent=label+' ▾';
  if(title)b.title=title;
  const d=document.createElement('div'); d.className='drop'; d.hidden=true;
  w.appendChild(b); w.appendChild(d); bar.appendChild(w);
  b.onclick=()=>{const shut=d.hidden; closeDrops(); d.hidden=!shut;};
  DROPS.push(d); return d;
}
// A button that stands for a thing being on or off, lit while it is on.
function btoggle(label,on,fn,title){
  const b=bbtn(label,title); let v=on;
  const paint=()=>{b.classList.toggle('on',v); fn(v);};
  b.onclick=()=>{v=!v; paint();};
  paint(); return b;
}

const vdrop=bdrop('View','Swing the camera to a square-on view');
[['ISO','iso'],['Left','left'],['Right','right'],
 ['Front','front'],['Back','back'],['Top','top']].forEach(v=>{
  mrow(v[0],vdrop).onclick=()=>{[az,el]=VIEWS[v[1]];tgt.set(0,0,0);place();draw();
    closeDrops();};
});

// WHAT IS VISIBLE HAS TWO SWITCHES, and a part needs both: its group's check box
// and its own. Ctrl+click clears a part's own switch; turning a group back on
// therefore does NOT resurrect a part that was hidden one at a time. Only Show
// all parts clears both.
const GON={}, gbox={};
function applyVis(){
  PICK.forEach(m=>{m.visible=GON[m.userData.part.g]!==false&&!m.userData.hid;});
  draw();
}
const pdrop=bdrop('Parts','Show or hide a whole group of parts');
const ptab=document.createElement('table'); ptab.className='ptable';
pdrop.appendChild(ptab);
for(const k in GROUPS){
  GON[k]=true;
  const tr=ptab.insertRow(), c1=tr.insertCell(), c2=tr.insertCell();
  const cb=document.createElement('input'); cb.type='checkbox'; cb.checked=true;
  cb.onchange=()=>{GON[k]=cb.checked; applyVis();};
  c1.appendChild(cb); c2.textContent=GROUPS[k];
  // the name is part of the switch, not a label beside it
  c2.onclick=()=>{cb.checked=!cb.checked; cb.onchange();};
  gbox[k]=cb;
}

bbtn('Show all parts',
     'Shows all the parts again - including the ones hidden with Ctrl+click on a part')
  .onclick=()=>{
    for(const k in GON){GON[k]=true; gbox[k].checked=true;}
    PICK.forEach(m=>{m.userData.hid=false;});
    applyVis();
  };

// THE CLASH BUTTON CARRIES THE COUNT, so the answer is on the bar without
// turning anything on. It re-runs on every jog - that is the whole point of
// checking live rather than shipping the drawn pose's answer.
clashBtn=bbtn('Clashes',
  'Red where two solids share space, green where the tool is cutting the '
  +'sacrificial sheet. Re-checked every time you jog.');
clashBtn.onclick=()=>{clashOn=!clashOn; paintClashes(); draw();};

btoggle('DRO',true,v=>{dro.hidden=!v;});               // ON by default - his
btoggle('Travel',false,v=>{jogro.hidden=!v;});
btoggle('Dimensions',false,v=>{facts.hidden=!v;});

bbtn('Help').onclick=()=>{help.hidden=false;about.hidden=true;closeDrops();};
// The assumptions used to sit in a panel along the bottom of the window. They
// are still ON THE PAGE, which is the point of them - a guess has to be visible
// as a guess - but behind a button instead of taking up the window.
bbtn('How this was built').onclick=()=>{about.hidden=false;help.hidden=true;closeDrops();};

addEventListener('pointerdown',e=>{
  if(!bar.contains(e.target)) closeDrops();
},true);
addEventListener('keydown',e=>{
  if(e.key==='Escape'){closeDrops();help.hidden=true;about.hidden=true;}});

help.innerHTML=
  '<span class="close">close</span><h2>Driving the model</h2><table>'+
  '<tr><td><b>Left drag</b></td><td>pans</td></tr>'+
  '<tr><td><b>Middle drag</b></td><td>orbits</td></tr>'+
  '<tr><td><b>Scroll</b></td><td>zooms</td></tr>'+
  '<tr><td><b>Hover</b></td><td>names the part under the cursor and gives its size</td></tr>'+
  '<tr><td><b>Shift + left click</b></td><td>hides the part under the cursor and '+
  'leaves its fasteners standing</td></tr>'+
  '<tr><td><b>Ctrl + left click</b></td><td>hides the part <i>and</i> the fasteners '+
  'that hold it</td></tr>'+
  '<tr><td><b>Ctrl + Shift + left click</b></td><td>hides the whole group the part '+
  'belongs to</td></tr>'+
  '<tr><td></td><td><b>Show all parts</b> brings every one of them back</td></tr>'+
  '<tr><td><b>Left / Right</b></td><td>jog the X carriage - as the operator sees them, '+
  'standing at the front, so Left runs toward max X</td></tr>'+
  '<tr><td><b>Up / Down</b></td><td>jog the gantry back and forward</td></tr>'+
  '<tr><td><b>PgUp / PgDn</b></td><td>jog the Z axis up and down</td></tr>'+
  '<tr><td><b>Shift / Ctrl</b></td><td>1 mm and 50 mm a press, instead of 10</td></tr>'+
  '<tr><td><b>Home</b></td><td>all three axes back to the drawn pose</td></tr>'+
  '<tr><td><b>Esc</b></td><td>shuts this and any open drop</td></tr></table>'+
  '<p><b>Clashes</b> on the bar counts every pair of solids sharing space '+
  '<i>at the position you are jogged to</i>, and re-checks on every jog. Red is '+
  'a clash; green is the tool cutting the sacrificial sheet, which is the job '+
  'rather than a fault. The boxes draw through the machine on purpose - a clash '+
  'is usually buried inside the parts that cause it.</p>'+
  '<p>Each axis stops 5 mm short of the part it would otherwise hit, and the panel on '+
  'the left says how far is left to run. The DRO is the <b>tool tip</b>.</p>';
help.querySelector('.close').onclick=()=>{help.hidden=true;};

facts.innerHTML=FACTS.map(f=>'<tr><td>'+f[0]+'</td><td class="n">'+f[1]+'</td></tr>').join('');
about.innerHTML=
  '<span class="close">close</span><h2>How this was built</h2>'+
  '<b>Generated from dimensions/registry.toml by tools/make-3d.py.</b> '+
  'Every box is placed from a registry value, so a dimension that moves shows up here '+
  'as a gap or an overlap instead of being quietly absorbed. The model opens at mid '+
  'travel on all three axes; Home drives to the back left corner at the top of travel, '+
  'where the DRO reads zero.'+
  '<h2>Placements assumed, not derived</h2>'+
  '<ul>'+ASSUMPTIONS.map(a=>'<li>'+a+'</li>').join('')+'</ul>';
about.querySelector('.close').onclick=()=>{about.hidden=true;};

applyJog(); place(); resize();
</script>
"""

if __name__ == "__main__":
    raise SystemExit(main())
