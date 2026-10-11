#!/usr/bin/env python3
"""Generate machine/drawings/model-3d.html from the dimension registry.

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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dims import Registry  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "machine" / "drawings" / "model-3d.html"
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
    "Stepper motor": "NEMA 23",
    "Interposer": "interposer bar, Sheet 6 - three the same",
    "Front strip": "front joining strip, ordered as 1/8in 6061 flat bar",
    "Fender washer": "plain M8 fender washer, under the acorn nut",
    "Acorn nut": "M8 acorn nut, on the tongue bolt's outboard end",
    "Rail counterbore": "counterbore in the rail, for an M5 x 16 rail bolt",
    "Z spacer": "spacer bar, sandwiched between the bearing blocks and the Z plate",
    "Y nut doubler": "doubler on the X end plate's outboard face, carrying the Y nut sole bracket",
    "X nut doubler": "doubler on the carriage plate's back face, carrying the X sole plate",
    "Shelf bar": "the bar the X beam's underside rests on",
    "BF12 tongue": "the tongue that carries the X axis BF12, on the MIN X end plate only",
}

# The fasteners. Lengths are quoted ONLY where the registry carries one -
# BOLT_BACK_Y, BOLT_FRONT_STRIP, BOLT_Z_NUT - and the rest say so.
M8_HEAD = "M8 x 1.25 flanged button head, hex socket in the dome"
D_SIDE_BOLT = M8_HEAD + " - 10 mm, with a plain washer, into a slide-in T-nut (BOLT_BACK_Y)"
D_STRIP_BOLT = M8_HEAD + " - 10 mm, A4/316, into a slide-in T-nut (BOLT_FRONT_STRIP)"
D_BEAM_END = M8_HEAD + " - into the extrusion's lengthwise corner bore. LENGTH NOT RECORDED"
D_TNUT = M8_HEAD + " - into a slide-in T-nut in the beam's slot. LENGTH NOT RECORDED"
D_SHELF_V = M8_HEAD + " - up into the beam's underside slot. LENGTH NOT RECORDED"
D_SHELF_H = M8_HEAD + " - into a BLIND tap in the X end plate. LENGTH NOT RECORDED"
D_TONGUE = M8_HEAD + " - through plate and tongue to a fender washer and an acorn nut. LENGTH NOT RECORDED"
D_M5_PLATE = "M5 x 0.8 socket cap, tapped into the plate. LENGTH NOT RECORDED"
D_M5_BAR = "M5 x 0.8 socket cap, up out of the casting into the tapped bar. LENGTH NOT RECORDED"
D_M5_END = "M5 x 0.8 socket cap into a tapped end face. LENGTH NOT RECORDED"
D_M5_EDGE = "M5 x 0.8 socket cap into the doubler's tapped top edge. LENGTH NOT RECORDED"
D_M5_NUT = "M5 x 0.8 x 16 socket cap into the ball nut housing, 9.65 mm engaged (BOLT_Z_NUT)"


def main() -> int:
    reg = Registry()
    reg.evaluate_all()
    if reg.errors:
        print("registry does not evaluate; fix that first", file=sys.stderr)
        return 2
    v = {s: reg.value(s) for s in reg.order}

    P = []  # parts: name, group, colour, [x0,y0,z0], [x1,y1,z1]

    # WHICH CARRIAGES A PART RIDES ON - "" for the frame, "Y" for the gantry,
    # "YX" for the X carriage, "YXZ" for the Z carriage. It is set as a cursor
    # across the sections below rather than passed at 60 call sites, and a call
    # may override it with k=. The display groups cannot serve: a bolt is in
    # "bolts" whether it rides the gantry or sits in the torsion box, and
    # "drive" holds both the screws, which never move, and the nuts, which do.
    ride = [""]

    def box(name, group, colour, x0, y0, z0, x1, y1, z1, d="", k=None):
        P.append({"n": name, "g": group, "c": colour, "t": "box", "d": d,
                  "k": ride[0] if k is None else k,
                  "p": [min(x0, x1), min(y0, y1), min(z0, z1)],
                  "q": [max(x0, x1), max(y0, y1), max(z0, z1)]})

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

    def prism(name, group, colour, profile, ya, yb, holes=None, d="", k=None):
        """An X-Z profile extruded along fore-aft. The fins are not boxes.

        p/q stay the bounding box so the camera framing and the interference
        check keep working; the check is then CONSERVATIVE on a prism, which is
        the safe direction - it may flag a touch that the real taper clears.
        """
        xs = [pt[0] for pt in profile]
        zs = [pt[1] for pt in profile]
        P.append({"n": name, "g": group, "c": colour, "t": "prism", "d": d,
                  "k": ride[0] if k is None else k,
                  "profile": profile, "holes": holes or [],
                  "ya": min(ya, yb), "yb": max(ya, yb),
                  "p": [min(xs), min(ya, yb), min(zs)],
                  "q": [max(xs), max(ya, yb), max(zs)]})

    W = v["MACHINE_OUTER_W"]         # 1211.238, side plate face to side plate face
    D = v["BOX_FORE_AFT"]            # 1156.35
    TT = v["T_BOX_TONGUE"]           # 19
    SKIN = v["T_BB_SKIN"]            # 19

    # ---- torsion box -----------------------------------------------------
    box("Torsion box", "box", 0xC9A227, 0, 0, -v["BOX_THK"], W, D, 0)
    tz0, tz1 = -(v["BOX_THK"] - SKIN), v["BOX_TONGUE_PROUD"]
    box("Back tongue", "box", 0xA07B16, -TT, -TT, tz0, W + TT, 0, tz1)
    for x0 in (-TT, W):
        box("Side tongue", "box", 0xA07B16,
            x0, v["SIDE_TONGUE_START"], tz0, x0 + TT, v["SIDE_TONGUE_END"], tz1)

    # ---- the plates that stand on the skin -------------------------------
    # ITS LEFT EDGE IS ON THE Y1 EXTRUSION'S OUTBOARD FACE, not on the side
    # plate's - his, 2026-10-10 - and it is drawn at the length it was BOUGHT,
    # REAR_PLATE_L_ORDERED, rather than at the flush envelope MACHINE_OUTER_W. The
    # side plate at each end is outboard of it, and the far end runs past the
    # machine's outer width by whatever the delivered piece gives.
    rpx = v["Y1_EXT_FACE_X"]
    box("Rear plate", "plates", 0x8899AA, rpx, 0, 0,
        rpx + v["REAR_PLATE_L_ORDERED"], v["T_REAR_PLATE"], v["REAR_PLATE_W"])

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
        wa, wb = outer + sgn * wo, outer + sgn * (wo + ww)
        prism("Front fin", "plates", 0x6FA8DC,
              [[outer, 0], [outer + sgn * fb, 0],
               [outer + sgn * ft, h], [outer, h]],
              y1, y1 + v["T_FIN"],
              holes=[[[wa, wz0], [wb, wz0], [wb, wz1], [wa, wz1]]])

    # ---- the interposer, under each beam and out through the window -------
    # Four M8 into slide-in T-nuts hold each bar on, at Sheet 6's two rows
    # measured from the bar's OUTBOARD end and on the extrusion's own two slot
    # centrelines across the 60. There is no third row: the bar slides back
    # along the beam to seat the screw's journal in the casting, which brings
    # the casting's footprint over the bar's first 72.5.
    ip_t = v["T_INTERPOSER"]
    ip_rows = (v["INTERPOSER_BOLT_ROW_1"], v["INTERPOSER_BOLT_ROW_2"])
    ip_slots = (v["RAIL_SLOT_INSET"], v["RAIL_SLOT_INSET"] + v["SLOT_GRID"])

    def interposer_bolts(along, across0, outb, along_axis, seat, up):
        """outb is the bar's outboard end; the rows run back from it. seat is
        the bar's face away from the beam, up the way the head stands off it."""
        for r in ip_rows:
            for s in ip_slots:
                a, c = outb - along * r, across0 + s
                cx, cy = (c, a) if along_axis == "y" else (a, c)
                cyl("Flange head", "bolts", 0x3C4248, cx, cy,
                    seat, seat + up * v["FLANGE_HEAD_H"],
                    v["FLANGE_HEAD_D"] / 2, seg=12, d=D_TNUT)
                cyl("Interposer bolt", "bolts", 0x3C4248, cx, cy,
                    seat, seat - up * ip_t,
                    v["BEAM_BOLT_CLEARANCE"] / 2 - 0.5, seg=10, d=D_TNUT)

    ip_front = y1 + v["T_FIN"] + v["INTERPOSER_PROUD"]
    for x0 in (lx0, rx0):
        box("Interposer", "ybeams", 0xC0652A, x0, ip_front - v["INTERPOSER_L"],
            ybot - ip_t, x0 + v["INTERPOSER_W"], ip_front, ybot)
        # it HANGS under the beam, so these drive upward and the heads are below
        interposer_bolts(+1, x0, ip_front, "y", ybot - ip_t, -1)

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
            x0, xep_back, xep_bot, x0 + xep_t, xep_front, xb_top)
        # It runs the plate's FULL 154 fore-aft, not DOUBLER_H - the four
        # stations D1-D4 that bolt it on are spread across that 154, and so
        # are the sole bracket's two rows. DOUBLER_H is its 45 UP the plate,
        # the offcut width, and it had been standing in for both.
        box("Y nut doubler", "gantry", 0xB06000,
            x0 - v["T_DOUBLER"] if x0 < xb_x0 else x0 + xep_t, xep_back,
            xep_bot,
            x0 if x0 < xb_x0 else x0 + xep_t + v["T_DOUBLER"],
            xep_front, xep_bot + v["DOUBLER_H"])

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
                    outer, outer + faceward * v["FLANGE_HEAD_H"],
                    v["FLANGE_HEAD_D"] / 2, axis="x", seg=12, d=D_BEAM_END)
                cyl("X end plate bolt", "bolts", 0x3C4248, xep_back + by, bz,
                    outer, outer - faceward * xep_t,
                    v["BEAM_BOLT_CLEARANCE"] / 2 - 0.5, axis="x", seg=10,
                    d=D_BEAM_END)

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
                bar_bottom, bar_bottom - v["FLANGE_HEAD_H"],
                v["FLANGE_HEAD_D"] / 2, seg=12, d=D_SHELF_V)
            cyl("Shelf bolt", "bolts", 0x3C4248, bar_mid, xep_back + sy,
                bar_bottom, bar_top, shank8, seg=10, d=D_SHELF_V)
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
                bar_out, bar_out + inb * v["FLANGE_HEAD_H"],
                v["FLANGE_HEAD_D"] / 2, axis="x", seg=12, d=D_SHELF_H)
            cyl("Shelf bolt", "bolts", 0x3C4248,
                xep_back + v["SHELF_HORIZ_Y"], hz, bar_out, plate_mid, shank8,
                axis="x", seg=10, d=D_SHELF_H)

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

    # Two clamps, CLAMP_CENTRES apart about the Z plate's mid-height, each
    # CLAMP_AXIAL tall and CLAMP_W across, reaching from the plate's face past
    # the bore so the barrel passes through them.
    for cz in (block_mid - v["CLAMP_CENTRES"] / 2, block_mid + v["CLAMP_CENTRES"] / 2):
        box("Spindle clamp", "z", 0x5E6B75,
            zp_cx - v["CLAMP_W"] / 2, zp_front, cz - v["CLAMP_AXIAL"] / 2,
            zp_cx + v["CLAMP_W"] / 2, sp_axis + r + 8, cz + v["CLAMP_AXIAL"] / 2)

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
    # BF12 seats on the rear plate, but THE SCREW STOPS SCREW_END_IN_BF12
    # SHORT OF IT - the bearing is centred in the block and the journal has to
    # straddle the bearing, which centres the journal too.
    bf12_y = v["T_REAR_PLATE"]
    y_lo = bf12_y + v["SCREW_END_IN_BF12"]
    y_hi = y_lo + v["SCREW_OAL_LONG"]
    for x0 in (lx0, rx0):
        cx = x0 + v["EXT_W"] / 2
        ride[0] = ""
        screw("y", cx, y_axis_z, y_lo, v["SCREW_OAL_LONG"], bf_low=True)
        support("bf12", "y", cx, y_axis_z, bf12_y, +1, y_seat_z, -1)
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
        cast_in = y_hi - v["SCREW_JOURNAL_CAST"]
        support("casting", "y", cx, y_axis_z, cast_in, +1, y_seat_z, -1)
        rails("y", cx, cast_in + v["BK12_L"], +1, y_seat_z, -1)
        motor("y", cx, y_axis_z, cast_in + v["CASTING_FOOTPRINT_L"], +1)
        # Six M5 up out of the casting into the tapped bar - Sheet 6's C1-C6,
        # three rows back from the casting's MOTOR end on the same two columns
        # BF12 uses. The head is under the casting, which is as deep as the
        # wing at the bearing end and as the rails further forward.
        motor_end = cast_in + v["CASTING_FOOTPRINT_L"]
        for r, d, c in casting_rows(cx):
            cyl("Casting bolt head", "bolts", 0x3C4248, c, motor_end - r,
                y_seat_z - d, y_seat_z - d - v["M5_HEAD_H"],
                v["M5_HEAD_D"] / 2, seg=12, d=D_M5_BAR)
            cyl("Casting bolt", "bolts", 0x3C4248, c, motor_end - r,
                y_seat_z - d, y_seat_z + ip_t, 2.5, seg=10, d=D_M5_BAR)

        # ---- the Y nut sole bracket, under the X end plate at this end ----
        # The nut hangs below the beam with its face DOWN, so the bracket lies
        # under it and bolts UP - into the nut at the tip, and into the END
        # FACES of the X end plate and its doubler at the root. Its top is put
        # on the NUT'S face rather than on the plate's bottom edge, so that if
        # XEP_CUT ever drifts off XEP_H again the plate shows it instead of the
        # bracket quietly missing the nut.
        inner = xb_x0 if x0 == lx0 else xb_x1       # the plate face it starts at
        out = -1 if x0 == lx0 else +1               # and which way it reaches
        face_z = y_axis_z - v["NUT_AXIS_TO_FACE"]
        ride[0] = "Y"            # it hangs off the X end plate
        tip = inner + out * v["SOLE_BRACKET_L"]
        box("Y sole bracket", "gantry", 0xC9A227,
            min(inner, tip), xep_back, face_z - v["T_SOLE_BRACKET"],
            max(inner, tip), xep_front, face_z)

        # Twelve M5 up through it: R5-R8 into the end plate's end face, R1-R4
        # into the doubler's behind it, then four into the nut on its own
        # pattern. ASSUMPTION: the root bolts are drawn BOLT_Z_NUT long like
        # the nut ones - no length is given for them.
        nut_mid = (y_lo + y_hi) / 2
        cols = [(inner + out * v["ROOT_BOLT_X_ENDPLATE"], j) for j in range(4)]
        cols += [(inner + out * v["ROOT_BOLT_X_DOUBLER"], j) for j in range(4)]
        pts = [(bx, xep_back + v["ROOT_BOLT_Y_FIRST"] + j * v["ROOT_BOLT_Y_PITCH"],
                D_M5_END) for bx, j in cols]
        for bx in (v["NUT_BOLT_X_NEAR"], v["NUT_BOLT_X_FAR"]):
            for dy in (-v["NUT_PATTERN_Y"] / 2, +v["NUT_PATTERN_Y"] / 2):
                pts.append((inner + out * bx, nut_mid + dy, D_M5_NUT))
        for bx, by, det in pts:
            cyl("Y sole bolt head", "bolts", 0x3C4248, bx, by,
                face_z - v["T_SOLE_BRACKET"],
                face_z - v["T_SOLE_BRACKET"] - v["M5_HEAD_H"],
                v["M5_HEAD_D"] / 2, seg=12, d=det)
            cyl("Y sole bolt", "bolts", 0x3C4248, bx, by,
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
                v["M5_HEAD_D"] / 2, axis="x", seg=12, d=D_M5_PLATE)
            cyl("BF12 bolt", "bolts", 0x3C4248, xep_back + by, xep_bot + bz,
                tongue_out, bf12_x + v["T_BF12_BLOCK"], 2.5, axis="x", seg=10,
                d=D_M5_PLATE)
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
    interposer_bolts(+1, xep_back, x_ip_out, "x", x_seat_z, +1)
    support("casting", "x", x_axis_y, x_axis_z, x_cast_in, +1, x_seat_z, +1)
    rails("x", x_axis_y, x_cast_in + v["BK12_L"], +1, x_seat_z, +1)
    motor("x", x_axis_y, x_axis_z, x_cast_in + v["CASTING_FOOTPRINT_L"], +1)
    # the same six, but this casting sits ON its bar so they drive downward
    for r, d, c in casting_rows(x_axis_y):
        cyl("Casting bolt head", "bolts", 0x3C4248, x_ip_out - r, c,
            x_seat_z + d, x_seat_z + d + v["M5_HEAD_H"],
            v["M5_HEAD_D"] / 2, seg=12, d=D_M5_BAR)
        cyl("Casting bolt", "bolts", 0x3C4248, x_ip_out - r, c,
            x_seat_z + d, x_seat_z - ip_t, 2.5, seg=10, d=D_M5_BAR)

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
            v["M5_HEAD_D"] / 2, axis="y", seg=12, d=D_M5_PLATE)
        cyl("BF12 bolt", "bolts", 0x3C4248, bx, bf12_z + v["T_BF12_BLOCK"] / 2,
            cp_back, cp_front + v["BF12_WING_H"], 2.5, axis="y", seg=10,
            d=D_M5_PLATE)
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
            v["M5_HEAD_D"] / 2, axis="y", seg=12, d=D_M5_PLATE)
        cyl("Casting bolt", "bolts", 0x3C4248, c, z_motor_end - r,
            cp_front + d, cp_back, 2.5, axis="y", seg=10, d=D_M5_PLATE)

    # ---- linear rails and bearing blocks ---------------------------------
    # Rails sit on their beam's face at RAIL_LOW_Z / RAIL_HIGH_Z; the block
    # envelopes the rail and stands RAIL_STACK off the face, which is the
    # measured figure the whole machine's offsets are built on.
    ride[0] = ""
    rw, st, bw, bl = v["RAIL_W"], v["RAIL_STACK"], v["BLOCK_W"], v["BLOCK_BUTTED"]
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
                box(f"{along} block", "motion", BC, face, bfrom[1], z - bw / 2,
                    face + d * st, bto[1], z + bw / 2, k=bk)
            else:                                   # stack grows along fore-aft
                box(f"{along} rail", "motion", RC, bfrom[0], face, z - rw / 2,
                    bto[0], face + d * rw, z + rw / 2, k=rk)
                box(f"{along} block", "motion", BC, bfrom[1], face, z - bw / 2,
                    bto[1], face + d * st, z + bw / 2, k=bk)

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
        box("Z block", "motion", BC, xc - bw / 2, cp_front, block_mid - bl / 2,
            xc + bw / 2, cp_front + st, block_mid + bl / 2, k="YXZ")
        # The spacer bar is SANDWICHED between the blocks and the Z plate - one per
        # rail, each spanning that rail's two blocks. The model had the gap but
        # nothing in it until he spotted the omission, 2026-10-03.
        box("Z spacer", "z", 0xBFC7CE,
            xc - v["SPACER_W"] / 2, cp_front + st, block_mid - v["SPACER_L"] / 2,
            xc + v["SPACER_W"] / 2, cp_front + st + v["SPACER_T"],
            block_mid + v["SPACER_L"] / 2, k="YXZ")

    # ---- the 45 mm front joining strips, Sheet 8 --------------------------
    # One per beam, across the seam, SITTING IN THE GAP BETWEEN THE TWO BEARING
    # BLOCK ROWS. That is the fit FRONT_STRIP_W exists to make: the blocks reach
    # to seam +/- 23, the strip to seam +/- 22.5, so it clears by half a
    # millimetre each side. The interference check is what proves it.
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
    hd, hh = v["FLANGE_HEAD_D"] / 2, v["FLANGE_HEAD_H"]
    BOLT = 0x3C4248
    rows = [v["SIDE_TSLOT_ROW_1"] + i * v["SLOT_GRID"] for i in range(4)]
    stations = [v["SIDE_TONGUE_START"] + v["TSLOT_X_FIRST"] + i * v["TSLOT_X_PITCH"]
                for i in range(int(v["TSLOT_X_COUNT"]))]

    for face, d in ((0.0, -1), (W, +1)):            # side plates, heads outboard
        for st in stations:
            for z in rows:
                cyl("Flange head", "bolts", BOLT, st, z, face, face + d * hh,
                    hd, axis="x", seg=12, d=D_SIDE_BOLT)

    # THE RP_ COLUMNS ARE SHEET 7 COORDINATES, measured from the plate's left edge,
    # which sits on the Y1 extrusion's outboard face - so the machine X is each of
    # them plus Y1_EXT_FACE_X.
    rp0 = v["Y1_EXT_FACE_X"]
    for col in (rp0 + v["RP_A_COL_1"],
                rp0 + v["RP_A_COL_1"] + v["EXT_W"] - 2 * v["EXT_BORE_INSET"],
                rp0 + v["RP_A_COL_3"], rp0 + v["RP_A_COL_4"]):   # heads backward
        for z in rows:
            cyl("Flange head", "bolts", BOLT, col, z, 0.0, -hh, hd, axis="y",
                seg=12, d=D_BEAM_END)

    # The BF12 bolts, four per Y beam. THEY RUN FORWARD, NOT BACKWARD - his,
    # 2026-10-10: the rear plate is TAPPED M5 and the bolt is driven from the
    # block side, so the head seats on BF12's own outer face and the bolt ends
    # FLUSH with the plate's back face. From behind, the plate shows four tapped
    # holes per beam and nothing proud. The block hangs upside down with its base
    # level with the interposer's underside, which is what puts the rows at 165
    # and 147. Head drawn as the M5 socket cap he is using, M5_HEAD_D / _H.
    bf12_face = v["T_REAR_PLATE"] + v["T_BF12_BLOCK"]       # BF12's outer face
    for col in (rp0 + v["RP_F_COL_1"], rp0 + v["RP_F_COL_2"],
                rp0 + v["RP_F_COL_3"], rp0 + v["RP_F_COL_4"]):
        for z in (v["BF12_ROW1_Y"], v["BF12_ROW2_Y"]):
            cyl("BF12 bolt head", "bolts", BOLT, col, z,
                bf12_face, bf12_face + v["M5_HEAD_H"], v["M5_HEAD_D"] / 2,
                axis="y", seg=12, d=D_M5_PLATE)
            cyl("BF12 bolt", "bolts", BOLT, col, z, 0.0, bf12_face, 2.5,
                axis="y", seg=10, d=D_M5_PLATE)

    # The eight M5 through the X sole plate, all driven DOWNWARD from above -
    # his reason for putting the plate on top in the first place: the bolts stay
    # reachable during assembly. Four at the root tap into the doubler's top
    # edge, four further out tap into the ball nut housing. Head proud on the
    # plate's top face, shank BOLT_Z_NUT down from under it, which crosses the
    # 6.35 plate and leaves Y_NUT_BOLT_ENGAGE in the part below.
    sole_top = x_nut_face + v["T_SOLE_BRACKET"]
    sole_bolts = [(cp_x0 + v["ROOT_BOLT_Y_FIRST"] + i * v["ROOT_BOLT_Y_PITCH"],
                   cp_back - v["X_SOLE_ROOT_ROW"], D_M5_EDGE) for i in range(4)]
    x_nut_mid = (x_lo + x_hi) / 2
    for ry in (v["X_NUT_BOLT_NEAR"], v["X_NUT_BOLT_FAR"]):
        for dx in (-v["NUT_PATTERN_Y"] / 2, +v["NUT_PATTERN_Y"] / 2):
            sole_bolts.append((x_nut_mid + dx, cp_back - ry, D_M5_NUT))
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
                    seg=12, d=D_BEAM_END)

    # the strips' own two rows, which land in the slots flanking each seam
    for face, d in ((lx0 + v["EXT_W"], +1), (rx0, -1)):
        for st in [y0 + x for x in strip_x]:
            for z in (y_seam - v["RAIL_SLOT_INSET"], y_seam + v["RAIL_SLOT_INSET"]):
                cyl("Flange head", "bolts", BOLT, st, z,
                    face + d * st_t, face + d * (st_t + hh), hd, axis="x",
                    seg=12, d=D_STRIP_BOLT)
    for st in [xb_x0 + x for x in strip_x]:
        for z in (x_seam - v["RAIL_SLOT_INSET"], x_seam + v["RAIL_SLOT_INSET"]):
            cyl("Flange head", "bolts", BOLT, st, z,
                xbeam_front + st_t, xbeam_front + st_t + hh, hd, axis="y",
                seg=12, d=D_STRIP_BOLT, k="Y")

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

    def bolt_stack(axis, c0, c1, head_face, far_face, out):
        """head_face is the plate's inboard face, far_face the tongue's outer."""
        cyl("Tongue bolt head", "bolts", BOLT, c0, c1,
            head_face, head_face - out * v["FLANGE_HEAD_H"],
            v["FLANGE_HEAD_D"] / 2, axis=axis, seg=12, d=D_TONGUE)
        cyl("Tongue bolt", "bolts", BOLT, c0, c1, head_face, far_face,
            SHANK, axis=axis, seg=10, d=D_TONGUE)
        cyl("Fender washer", "bolts", WASH, c0, c1,
            far_face, far_face + out * WT, WD, axis=axis, seg=14)
        cyl("Acorn nut", "bolts", ACORN, c0, c1,
            far_face + out * WT, far_face + out * (WT + AH), AD, axis=axis, seg=6)

    # the back tongue laps the rear plate from BEHIND, so these drive -y
    for i in range(8):
        # Sheet 7 coordinates, so off the plate's left edge like the RP_ columns
        x = rp0 + v["XBOX_X_FIRST"] + i * v["XBOX_PITCH"]
        bolt_stack("y", x, v["XBOX_ROW_Y"], v["T_REAR_PLATE"], -TT, -1)

    # each side tongue laps its plate from OUTBOARD
    side_st = [v["SIDE_TONGUE_START"] + v["TSLOT_X_FIRST"] + i * v["TSLOT_X_PITCH"]
               for i in range(int(v["TSLOT_X_COUNT"]))]
    for head_face, far_face, out in ((sp, -TT, -1), (W - sp, W + TT, +1)):
        for st in side_st:
            bolt_stack("x", st, v["BOX_TONGUE_BOLT_Y"], head_face, far_face, out)

    # ---- rail counterbores ------------------------------------------------
    # Drilled into the rail's EXPOSED face and running RAIL_CBORE_DEPTH back
    # toward the beam, so they are drawn as dark cylinders sunk into the rail.
    # No boolean subtraction here - the model is solids - so the pair is allowed
    # to interpenetrate on purpose and says so in ALLOWED.
    cb_r, cb_d = v["RAIL_CBORE_D"] / 2, v["RAIL_CBORE_DEPTH"]
    cb_f, cb_p = v["RAIL_CBORE_FIRST"], v["RAIL_CBORE_PITCH"]
    HOLE = 0x22262A
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
    #       front: their front edge, 5 from the front fin's back face
    #   X   either way: the Z PLATE's edge, 5 from the inside face of the X end
    #       plate at that end. The Z plate and not the carriage plate because it
    #       is the wider of the two, Z_PLATE_W against XEP_W.
    #   Z   down: the nut's lower end, 5 above BF12's upper face
    #       up: THE Z TOP STOP BLOCK IS NOT IN THE MODEL. Sheet 3c dimensions it
    #       - 50 x 25.4 x 45 off 1in 6061, stop face at X 310 up the carriage
    #       plate - but it has no registry symbols, and nothing here is placed
    #       from a number typed in this file. So the up stop is pinned at the
    #       drawn pose and says so on the page rather than guessing one.
    jog = {
        "Y": [round(v["T_REAR_PLATE"] + 5 - xep_back, 2),
              round((y1 - 5) - xep_front, 2), ""],
        "X": [round((xb_x0 + 5) - (zp_cx - v["Z_PLATE_W"] / 2), 2),
              round((xb_x1 - 5) - (zp_cx + v["Z_PLATE_W"] / 2), 2), ""],
        "Z": [round((bf12_z + v["T_BF12_BLOCK"] + 5) - (z_nut_mid - v["NUT_OAL"] / 2), 2),
              0.0, "UP STOP NOT MODELLED - the Z top stop block has no registry "
                   "symbols, so the up limit is the drawn pose"],
    }

    groups = {
        "box": "Torsion box and tongues",
        "bolts": "M8 flange bolt heads",
        "motion": "Rails and bearing blocks",
        "plates": "Rear, side and fin plates",
        "ybeams": "Y beams",
        "drive": "Ball screws, nuts and steppers",
        "gantry": "X gantry",
        "z": "Z carriage and spindle",
    }
    facts = [
        ("Machine width", W), ("Box fore-aft", D), ("Box thickness", v["BOX_THK"]),
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

    three = VENDOR.read_text(encoding="utf-8")
    html = (HTML.replace("__PARTS__", json.dumps(P))
                .replace("__GROUPS__", json.dumps(groups))
                .replace("__ASSUMPTIONS__", json.dumps(ASSUMPTIONS))
                .replace("__FACTS__", json.dumps([[a, round(b, 2)] for a, b in facts]))
                .replace("__JOG__", json.dumps(jog)))
    # last, and not via str.replace on the whole document: three.min.js contains
    # backslash escapes that a replacement template would eat.
    i = html.index("__THREE__")
    html = html[:i] + three + html[i + len("__THREE__"):]
    OUT.write_text(html, encoding="utf-8")
    kb = len(html.encode("utf-8")) / 1024
    print(f"wrote {OUT.relative_to(ROOT)} - {len(P)} parts, {kb:.0f} KB, self-contained")
    for a, b in facts:
        print(f"  {a:22} {b:10.2f}")
    print("\njog limits, as an offset from the drawn pose:")
    for ax, (lo_, hi_, warn) in jog.items():
        print(f"  {ax}  {lo_:+9.2f} to {hi_:+9.2f}   travel {hi_ - lo_:8.2f}"
              + ("   " + warn.split(" - ")[0] if warn else ""))
    return report_overlaps(P)


# Pairs that SHOULD interpenetrate, with the reason. Everything else that
# overlaps is a real interference and gets printed.
ALLOWED = {
    frozenset({"Torsion box", "Back tongue"}),      # laminated to the wall
    frozenset({"Torsion box", "Side tongue"}),
    frozenset({"Back tongue", "Side tongue"}),      # meet at the corner
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
    frozenset({"Rear plate", "BF12 bolt"}),
    # the same joint on the X tongue and on the Z carriage plate
    frozenset({"BF12 tongue", "BF12 bolt"}),
    frozenset({"X end plate", "BF12 bolt"}),
    frozenset({"X carriage plate", "BF12 bolt"}),
    frozenset({"BF12 boss", "BF12 bolt"}),
    frozenset({"BF12 wing", "BF12 bolt"}),
    frozenset({"Back tongue", "Tongue bolt"}),
    frozenset({"Side plate", "Tongue bolt"}),
    frozenset({"Side tongue", "Tongue bolt"}),
    # barrel, nose, shaft and nut are one spindle drawn as four cylinders
    frozenset({"Spindle barrel", "Spindle nose"}),
    frozenset({"Spindle nose", "Spindle shaft"}),
    frozenset({"Spindle shaft", "Collet nut"}),
    frozenset({"Spindle clamp", "Spindle barrel"}),  # a clamp WRAPS the barrel
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
    # The Y sole bracket laps the end plate and doubler end faces and the nut's
    # face, and its twelve bolts cross it into all three. Only the shanks are
    # listed; the heads hang below the bracket and clash with nothing.
    frozenset({"Y sole bracket", "X end plate"}),
    frozenset({"Y sole bracket", "Y nut doubler"}),
    frozenset({"Y sole bracket", "Nut bolt face"}),
    frozenset({"Y sole bracket", "Y sole bolt"}),
    frozenset({"X end plate", "Y sole bolt"}),
    frozenset({"Y nut doubler", "Y sole bolt"}),
    frozenset({"Ball nut", "Y sole bolt"}),
    frozenset({"Nut bolt face", "Y sole bolt"}),
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


def through_hole(a, b) -> bool:
    """A part passing THROUGH a cut-out is not an interference.

    The prism's p/q is its bounding box, which knows nothing about the window in
    it, so the interposer running out through the fin reads as a solid clash.
    This resolves it properly rather than by adding the pair to ALLOWED: the
    other part has to sit INSIDE the hole in both axes. Move the interposer and
    it is flagged again, which is the whole point of the check.
    """
    for prism_, other in ((a, b), (b, a)):
        for hp in prism_.get("holes", []):
            hx = [pt[0] for pt in hp]
            hz = [pt[1] for pt in hp]
            # Same 0.05 slack the overlap test uses. Needed, not cosmetic: the
            # window's edge and the beam's face are both 1208.575 but are reached
            # by different routes, so an exact compare fails on one fin and not
            # the other.
            e = 0.05
            if (min(hx) - e <= other["p"][0] and other["q"][0] <= max(hx) + e
                    and min(hz) - e <= other["p"][2] and other["q"][2] <= max(hz) + e):
                return True
    return False


def report_overlaps(P) -> int:
    """Solid-body interference check - the one thing a box model can prove.

    It cannot tell you a part is in the RIGHT place. It can tell you two parts
    are in the SAME place, which is the failure a dimension change causes and
    the eye misses on a shaded render.
    """
    bad = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            a, b = P[i], P[j]
            # A LINE HAS NO VOLUME. The thread is drawn over the screw's own
            # cylinder, and that cylinder is what the check already tests, so
            # including the helix would only re-flag the screw's own envelope.
            if a["t"] == "helix" or b["t"] == "helix":
                continue
            if frozenset({a["n"], b["n"]}) in ALLOWED:
                continue
            ov = [min(a["q"][k], b["q"][k]) - max(a["p"][k], b["p"][k]) for k in range(3)]
            if all(o > 0.05 for o in ov) and not through_hole(a, b):
                bad.append((a["n"], b["n"], ov))
    if not bad:
        print("\ninterference check: clean - no two parts occupy the same space")
        return 0
    print(f"\ninterference check: {len(bad)} OVERLAP(S)")
    for n1, n2, ov in bad:
        print(f"  {n1} <-> {n2}   by {ov[0]:.2f} x {ov[1]:.2f} x {ov[2]:.2f} mm")
    return 0


HTML = r"""<!doctype html>
<meta charset="utf-8"><title>CNC assembly - generated from the dimension registry</title>
<style>
 html,body{margin:0;height:100%;background:#1a1d21;color:#ddd;
   font:13px/1.5 "Segoe UI",system-ui,sans-serif;overflow:hidden}
 #c{position:fixed;inset:0}
 .panel{position:fixed;background:#23272dEE;border:1px solid #3a4048;border-radius:6px;padding:10px 12px}
 #ui{top:12px;left:12px;max-width:280px}
 #info{bottom:12px;left:12px;max-width:430px;font-size:11.5px;color:#aab}
 #info summary{cursor:pointer;color:#e8b64c;font-weight:600;list-style:none}
 #info summary::-webkit-details-marker{display:none}
 #info summary::before{content:'show  ';color:#8fd}
 #info[open] summary::before{content:'hide  '}
 #info .body{margin-top:8px}
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
 #jogro{margin-top:8px;font-size:11.5px}
 #jogro .ax{color:#e8b64c;font-weight:600}
 #jogro .stop{color:#e8613d;font-weight:600}
 #jogro .hint{color:#8a929b;font-size:11px}
 #jogro .warn{color:#e8b64c}
 #jogro table{margin:2px 0 0}
 #jogro td.v{text-align:right;color:#8fd;padding-right:8px}
</style>
<canvas id="c"></canvas>
<div id="tip"></div>
<div class="panel" id="ui"><h1>CNC assembly</h1>
<div id="btnrow"><button id="partsbtn">Show parts</button><button id="statsbtn">Show dimensions</button></div>
<div id="toggles" hidden></div><table id="facts" hidden></table>
<div id="jogro"></div></div>
<details class="panel" id="info"><summary>How this was built, and what is assumed</summary><div class="body" id="infobody"></div></details>
<script>__THREE__</script>
<script>
const PARTS=__PARTS__, GROUPS=__GROUPS__, ASSUMPTIONS=__ASSUMPTIONS__, FACTS=__FACTS__;
const JOG=__JOG__;

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
    // profile is machine X-Z, extruded along fore-aft. Extrude runs along three's
    // +Z, so the mesh is built at the origin and then shifted to the right depth.
    const sh=new THREE.Shape();
    p.profile.forEach((pt,i)=>i?sh.lineTo(pt[0]-mid[0],pt[1]-mid[2]):sh.moveTo(pt[0]-mid[0],pt[1]-mid[2]));
    sh.closePath();
    (p.holes||[]).forEach(hp=>{
      const hs=new THREE.Path();
      hp.forEach((pt,i)=>i?hs.lineTo(pt[0]-mid[0],pt[1]-mid[2]):hs.moveTo(pt[0]-mid[0],pt[1]-mid[2]));
      hs.closePath(); sh.holes.push(hs);
    });
    geom=new THREE.ExtrudeGeometry(sh,{depth:p.yb-p.ya,bevelEnabled:false});
    ctr=[0,0,-(p.yb-mid[1])];
  }else{
    const s=[0,1,2].map(i=>Math.max(p.q[i]-p.p[i],0.4));
    geom=new THREE.BoxGeometry(s[0],s[2],s[1]);
    ctr=[(p.p[0]+p.q[0])/2-mid[0],(p.p[2]+p.q[2])/2-mid[2],-((p.p[1]+p.q[1])/2-mid[1])];
  }
  const g=new THREE.Mesh(geom,new THREE.MeshLambertMaterial({color:p.c,side:THREE.DoubleSide}));
  g.position.set(ctr[0],ctr[1],ctr[2]);
  const e=new THREE.LineSegments(new THREE.EdgesGeometry(g.geometry),
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
let az=-0.72, el=0.42, dist=span*1.75, down=null, mode=null;
const tgt=new THREE.Vector3(0,0,0);
function place(){
  cam.position.set(tgt.x+dist*Math.cos(el)*Math.sin(az),
                   tgt.y+dist*Math.sin(el),
                   tgt.z+dist*Math.cos(el)*Math.cos(az));
  cam.lookAt(tgt);
}
addEventListener('pointerdown',e=>{
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
const ENDS={Y:['back','front'],X:['right','left'],Z:['down','up']};
const j1=n=>(n<0?'':'+')+(Math.round(n*10)/10).toFixed(1);

function applyJog(){
  GY.position.z=-JOGPOS.Y;        // machine +Y is forward, which is three's -Z
  GX.position.x=JOGPOS.X;
  GZ.position.y=JOGPOS.Z;
  // the raycaster reads matrixWorld, and a hover can land before the next draw
  scene.updateMatrixWorld(true);
  const rows=['X','Y','Z'].map(ax=>{
    const L=JOG[ax], p=JOGPOS[ax], e=ENDS[ax];
    const hit=p<=L[0]+1e-6?e[0]:p>=L[1]-1e-6?e[1]:'';
    // A pinned end is not a stop, and must not read as one.
    const say=hit?(L[2]&&hit===e[1]
      ?' &middot; <span class="warn">PINNED, no '+e[1]+' stop modelled</span>'
      :' &middot; <span class="stop">AT THE '+hit.toUpperCase()+' STOP</span>'):'';
    return '<tr><td class="ax">'+ax+'</td><td class="v">'+j1(p)+'</td>'+
      '<td>'+j1(p-L[0])+' to '+e[0]+', '+j1(L[1]-p)+' to '+e[1]+say+
      '</td></tr>';
  }).join('');
  const warn=['X','Y','Z'].filter(ax=>JOG[ax][2]).map(ax=>JOG[ax][2]);
  document.getElementById('jogro').innerHTML=
    '<span class="hint">JOG: left/right = X, AS THE OPERATOR SEES THEM standing at the '+
    'front - so left is max X, and the opening view, which is from behind, shows it '+
    'mirrored. Up/down = fore-aft, PgUp/PgDn = Z. '+
    '10 mm a press, Shift 1 mm, Ctrl 50 mm. Home recentres all three.</span>'+
    '<table>'+rows+'</table>'+
    (warn.length?'<span class="warn">'+warn.join('<br>')+'</span>':'');
}

addEventListener('keydown',e=>{
  if(e.key==='Home'){JOGPOS.X=JOGPOS.Y=JOGPOS.Z=0;e.preventDefault();applyJog();draw();return;}
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
addEventListener('pointermove',e=>{
  if(down){tip.style.display='none';return;}
  ray.setFromCamera({x:e.clientX/innerWidth*2-1,y:-(e.clientY/innerHeight)*2+1},cam);
  // THE RAYCASTER DOES NOT TEST .visible, so a part in a hidden group is still
  // hit - take the first intersection that is actually on the screen.
  const h=ray.intersectObjects(PICK,false).find(x=>x.object.visible);
  if(!h){tip.style.display='none';return;}
  const p=h.object.userData.part;
  tip.innerHTML='<b class="w">'+p.n+'</b><br>'+(p.d?p.d+'<br>':'')+
    '<span class="dim">'+sizeOf(p)+' &middot; '+(GROUPS[p.g]||p.g)+'</span>';
  tip.style.display='block';
  const w=tip.offsetWidth, th=tip.offsetHeight;
  tip.style.left=Math.max(6,Math.min(e.clientX+14,innerWidth-w-8))+'px';
  tip.style.top=(e.clientY+18+th>innerHeight?Math.max(6,e.clientY-th-12):e.clientY+18)+'px';
});

function resize(){const w=innerWidth,h=innerHeight;rend.setPixelRatio(devicePixelRatio);rend.setSize(w,h);cam.aspect=w/h;cam.updateProjectionMatrix();draw();}
function draw(){rend.render(scene,cam);}
addEventListener('resize',resize);

const VIEWS={iso:[-0.72,0.42],front:[Math.PI,0.06],back:[0,0.06],
             left:[-Math.PI/2,0.06],right:[Math.PI/2,0.06],top:[0,1.44]};
const vb=document.createElement('div'); vb.style.margin='2px 0 8px';
for(const k in VIEWS){
  const b=document.createElement('button'); b.textContent=k;
  b.style.cssText='margin:2px 4px 0 0;background:#2f353d;color:#cde;border:1px solid #454c55;'+
                  'border-radius:4px;padding:2px 7px;cursor:pointer;font:11px inherit';
  b.onclick=()=>{[az,el]=VIEWS[k];tgt.set(0,0,0);place();draw();};
  vb.appendChild(b);
}
document.getElementById('ui').insertBefore(vb,document.getElementById('btnrow'));
const t=document.getElementById('toggles');
for(const k in GROUPS){
  const l=document.createElement('label');
  l.innerHTML='<input type="checkbox" checked>'+GROUPS[k];
  l.firstChild.onchange=e=>{(byGroup[k]||[]).forEach(m=>m.visible=e.target.checked);draw();};
  t.appendChild(l);
}
document.getElementById('facts').innerHTML=
  FACTS.map(f=>'<tr><td>'+f[0]+'</td><td class="n">'+f[1]+'</td></tr>').join('');
document.getElementById('infobody').innerHTML=
  '<b class="w">Generated from dimensions/registry.toml by tools/make-3d.py.</b> '+
  'Every box is placed from a registry value. <b class="w">LEFT DRAG PANS, MIDDLE DRAG ORBITS</b>, scroll zooms, a view button recentres, and <b class="w">HOVER NAMES THE PART</b> under the cursor. '+
  '<b class="w">THE CURSOR KEYS JOG THE CARRIAGES</b> - left/right the X carriage, up/down the gantry fore-aft, PgUp/PgDn the Z axis, Home back to the drawn pose. Each axis stops 5 mm short of the part it would hit.<br>'+
  'Pose: the drawn pose is mid travel on all three axes.<br><b class="w">Placements ASSUMED, not derived:</b>'+
  '<ul>'+ASSUMPTIONS.map(a=>'<li>'+a+'</li>').join('')+'</ul>';

const BTN='margin:8px 6px 0 0;background:#2f353d;color:#cde;border:1px solid #454c55;'+
          'border-radius:4px;padding:3px 9px;cursor:pointer;font:11.5px inherit';
const sb=document.getElementById('statsbtn'), ft2=document.getElementById('facts');
const pb=document.getElementById('partsbtn'), tg=document.getElementById('toggles');
sb.style.cssText=BTN; pb.style.cssText=BTN;
sb.onclick=()=>{ft2.hidden=!ft2.hidden;sb.textContent=ft2.hidden?'Show dimensions':'Hide dimensions';};
pb.onclick=()=>{tg.hidden=!tg.hidden;pb.textContent=tg.hidden?'Show parts':'Hide parts';};

applyJog(); place(); resize();
</script>
"""

if __name__ == "__main__":
    raise SystemExit(main())
