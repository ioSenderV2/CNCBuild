# -*- coding: utf-8 -*-
"""Generate sensor-board.kicad_sch (KiCad 10) for the CNCBuild AS5311 sensor board.

One of these sits in each puck: AS5311 on the tape-facing side, RJ45 jack and passives on
the other. The cable pinout is NOT a free choice here - it must mirror the controller board
exactly (see ../controller-board/netlist.txt), because it is the same CAT5 run:

    1 = A    2 = GND   3 = B      4 = +3V3
    5 = GND  6 = GND   7 = MagDECn   8 = GND

Same drawing convention as the controller board: connections are made by NET LABEL on a
short wire stub at each pin, not by point-to-point wires. Electrically identical for
netlist/ERC purposes and far less error-prone to generate.
"""
import uuid, io, os

OUT = os.path.dirname(os.path.abspath(__file__))
U = lambda: str(uuid.uuid4())


def f(v):
    return str(int(v)) if float(v) == int(v) else ("%.4f" % v).rstrip('0').rstrip('.')


# --------------------------------------------------------------- symbol geometry
# KiCad convention: a pin's `at` IS its connection point, and `rot` points FROM that
# point TOWARD the body. Symbol space is Y-up; the sheet is Y-down, so py is mirrored
# when the symbol is placed.
COL_Y = [11.43, 8.89, 6.35, 3.81, 1.27, -1.27, -3.81, -6.35, -8.89, -11.43]
RJ_Y = [8.89, 6.35, 3.81, 1.27, -1.27, -3.81, -6.35, -8.89]
TVS_Y = [5.08, 2.54, 0, -2.54]
FONT = '(effects (font (size 1.27 1.27)))'

# AS5311, TSSOP-20. DIP numbering runs counterclockwise: 1..10 down the left side,
# 11..20 up the right. Names come from the datasheet Table 1 (rev 1.12, p.4).
AS_NAMES = {1: "NC", 2: "MagINCn", 3: "MagDECn", 4: "A", 5: "B", 6: "NC", 7: "Index",
            8: "VSS", 9: "Prog", 10: "NC", 11: "NC", 12: "DO", 13: "CLK", 14: "CSn",
            15: "PWM", 16: "NC", 17: "NC", 18: "VDD3V3", 19: "VDD5V", 20: "NC"}


def as5311_pins():
    out = []
    for i, y in enumerate(COL_Y):                 # 1..10 down the left
        out.append((str(i + 1), -7.62, y, 0))
    for i, y in enumerate(reversed(COL_Y)):       # 11..20 up the right
        out.append((str(i + 11), 7.62, y, 180))
    return out


def rj_pins():
    # Plastic, UNSHIELDED jack: no shield tab, so no SH pin. That is the whole point -
    # with nothing to bond to, the cable screen floats at this end by construction.
    return [(str(i + 1), -7.62, y, 0) for i, y in enumerate(RJ_Y)]


def tvs_pins():
    out = [(str(i + 1), -6.35, y, 0) for i, y in enumerate(TVS_Y)]
    out.append(("5", 0, -7.62, 90))
    return out


RC_PINS = [("1", 0, 3.81, 270), ("2", 0, -3.81, 90)]
TP_PINS = [("1", 0, -3.81, 90)]


def lib_symbol(name, bodyrect, pins, ref, val, hide_names=False, names=None):
    x0, y0, x1, y1 = bodyrect
    s = []
    s.append('  (symbol "%s" (pin_names (offset 0.254)%s) (exclude_from_sim no) (in_bom yes) (on_board yes)'
             % (name, ' hide' if hide_names else ''))
    s.append('    (property "Reference" "%s" (at 0 %s 0) %s)' % (ref, f(y1 + 2.54), FONT))
    s.append('    (property "Value" "%s" (at 0 %s 0) %s)' % (val, f(y0 - 2.54), FONT))
    s.append('    (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
    s.append('    (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
    s.append('    (symbol "%s_0_1"' % name.split(":")[-1])
    s.append('      (rectangle (start %s %s) (end %s %s) (stroke (width 0.254) (type default)) (fill (type background)))'
             % (f(x0), f(y0), f(x1), f(y1)))
    s.append('    )')
    s.append('    (symbol "%s_1_1"' % name.split(":")[-1])
    for num, px, py, rot in pins:
        pname = (names or {}).get(int(num) if num.isdigit() else num, num)
        s.append('      (pin passive line (at %s %s %d) (length 2.54) (name "%s" %s) (number "%s" %s))'
                 % (f(px), f(py), rot, pname, FONT, num, FONT))
    s.append('    )')
    s.append('  )')
    return "\n".join(s)


LIBS = [
    lib_symbol("cnc:AS5311", (-5.08, -12.7, 5.08, 12.7), as5311_pins(), "U", "AS5311", names=AS_NAMES),
    lib_symbol("cnc:RJ45_8_UNSHLD", (-5.08, -10.16, 5.08, 10.16), rj_pins(), "J", "RJ45_unshielded_no_magnetics"),
    lib_symbol("cnc:TVS_4", (-3.81, -7.62, 3.81, 7.62), tvs_pins(), "D", "TVS_array_4ch"),
    lib_symbol("cnc:R", (-1.016, -2.54, 1.016, 2.54), RC_PINS, "R", "R", hide_names=True),
    lib_symbol("cnc:C", (-1.016, -2.54, 1.016, 2.54), RC_PINS, "C", "C", hide_names=True),
    lib_symbol("cnc:TP", (-1.016, -1.016, 1.016, 1.016), TP_PINS, "TP", "TestPoint", hide_names=True),
]
SYM_PINS = {"cnc:AS5311": as5311_pins(), "cnc:RJ45_8_UNSHLD": rj_pins(), "cnc:TVS_4": tvs_pins(),
            "cnc:R": RC_PINS, "cnc:C": RC_PINS, "cnc:TP": TP_PINS}

SHEET_UUID = U()
body, wires, labels, noconns = [], [], [], []

GRID = 1.27


def snap(v):
    """Placement origins must land on the 1.27 mm connection grid. Every pin offset and stub
    length in this file is already a multiple of 1.27, so snapping the origin puts every
    endpoint on-grid. KiCad flags off-grid endpoints because they can silently fail to
    connect once the sheet is edited by hand."""
    return round(v / GRID) * GRID


def place(lib, ref, val, x, y, conns, nc=()):
    x, y = snap(x), snap(y)
    # Pin numbers in the symbol tables are STRINGS; the conns dicts below are written with
    # integer keys for readability. Normalise, or every integer key silently fails to match
    # and the schematic comes out with symbols and no connections.
    conns = dict((str(k), v) for k, v in conns.items())
    nc = set(str(n) for n in nc)
    pins = SYM_PINS[lib]
    b = []
    b.append('  (symbol (lib_id "%s") (at %s %s 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)'
             % (lib, f(x), f(y)))
    b.append('    (uuid "%s")' % U())
    b.append('    (property "Reference" "%s" (at %s %s 0) (effects (font (size 1.27 1.27)) (justify left)))'
             % (ref, f(x + 7), f(y - 16)))
    b.append('    (property "Value" "%s" (at %s %s 0) (effects (font (size 1.27 1.27)) (justify left)))'
             % (val, f(x + 7), f(y - 13.5)))
    for num, px, py, rot in pins:
        b.append('    (pin "%s" (uuid "%s"))' % (num, U()))
    b.append('    (instances (project "sensor-board" (path "/%s" (reference "%s") (unit 1))))'
             % (SHEET_UUID, ref))
    b.append('  )')
    body.append("\n".join(b))

    for num, px, py, rot in pins:
        if num in nc:
            # Deliberately unused pin. A no_connect marker states the intent and turns an
            # ERC error into a recorded decision.
            noconns.append('  (no_connect (at %s %s) (uuid "%s"))'
                           % (f(x + px), f(y - py), U()))
            continue
        if num not in conns:
            continue
        ax, ay = x + px, y - py            # mirror Y: symbol is Y-up, sheet is Y-down
        dx = {0: -1, 180: 1, 90: 0, 270: 0}[rot]
        dy = {0: 0, 180: 0, 90: 1, 270: -1}[rot]
        ex, ey = ax + dx * 3.81, ay + dy * 3.81
        wires.append('  (wire (pts (xy %s %s) (xy %s %s)) (stroke (width 0) (type default)) (uuid "%s"))'
                     % (f(ax), f(ay), f(ex), f(ey), U()))
        just = "right" if dx < 0 else "left"
        labels.append('  (label "%s" (at %s %s 0) (effects (font (size 1.27 1.27)) (justify %s bottom)) (uuid "%s"))'
                      % (conns[num], f(ex), f(ey), just, U()))


# --------------------------------------------------------------- the design
#
# Series resistor value: the design doc gives a RANGE (100-220 Ohm, §"Series 100-220 Ohm at
# the AS5311 output"), paired with 330 pF-1 nF at the controller end. The exact value is one
# half of an RC that is chosen with the other half, so it is left as the range rather than
# invented here. Pick it when the controller-end cap is fixed, and update netlist.txt.
RSER = "100R-220R TBD"

# U1 - the sensor. NC pins per datasheet Table 1: 1, 6, 10, 11, 16, 17, 20 "must be left
# unconnected". Index (7) and PWM (15) are real outputs this design does not use.
AS = {2: "MAGI", 3: "MAGD_SRC", 4: "A_SRC", 5: "B_SRC",
      8: "GND", 9: "GND", 12: "DO", 13: "CLK", 14: "CSN",
      18: "+3V3", 19: "+3V3"}
place("cnc:AS5311", "U1", "AS5311  (tape-facing side)", 90, 120, AS,
      nc=(1, 6, 7, 10, 11, 15, 16, 17, 20))

# J1 - the cable. Pinout mirrors the controller board exactly.
RJ = {1: "A", 2: "GND", 3: "B", 4: "+3V3", 5: "GND", 6: "GND", 7: "MAGD", 8: "GND"}
place("cnc:RJ45_8_UNSHLD", "J1", "RJ45 - UNSHIELDED, NO MAGNETICS", 210, 120, RJ)

# Series resistors at the source, one per outgoing signal.
place("cnc:R", "R1", RSER, 150, 95, {1: "A_SRC", 2: "A"})
place("cnc:R", "R2", RSER, 150, 120, {1: "B_SRC", 2: "B"})
place("cnc:R", "R3", RSER, 150, 145, {1: "MAGD_SRC", 2: "MAGD"})

# CSn must be LOW to enable the incremental outputs, and it has an internal ~50k pull-up.
# Through a link rather than a hard trace, so it can be lifted for SSI readout later.
place("cnc:R", "R4", "0R link - CSn low", 90, 175, {1: "CSN", 2: "GND"})

# Decoupling, at this end because the cable is 2.4 m of 24 AWG.
place("cnc:C", "C1", "100n", 40, 150, {1: "+3V3", 2: "GND"})
place("cnc:C", "C2", "10u", 60, 150, {1: "+3V3", 2: "GND"})

# TVS on the connector side of the series resistors - this end gets handled, and the
# resistors then also limit current into the array.
place("cnc:TVS_4", "D1", "TVS array 4ch", 250, 120,
      {1: "A", 2: "B", 3: "MAGD", 4: "+3V3", 5: "GND"})

# Test pads. CLK and DO cost no GPIO and turn the board into something you can interrogate
# over SSI on the bench - absolute position within the pole pair plus the status word.
place("cnc:TP", "TP1", "CLK", 130, 185, {1: "CLK"})
place("cnc:TP", "TP2", "DO", 145, 185, {1: "DO"})
place("cnc:TP", "TP3", "MagINCn", 160, 185, {1: "MAGI"})

TEXT = ('  (text "Sensor board  -  AS5311 -> unshielded RJ45 (NO MAGNETICS).  One per puck.'
        '\\nCable pinout mirrors the controller board. Rationale: linear-encoder/sensor-board.md"'
        ' (at 20 18 0) (effects (font (size 2.2 2.2)) (justify left)) (uuid "%s"))' % U())

doc = ['(kicad_sch (version 20231120) (generator "eeschema") (generator_version "8.0")',
       '  (uuid "%s")' % SHEET_UUID,
       '  (paper "A3")',
       '  (lib_symbols',
       "\n".join(LIBS),
       '  )',
       TEXT,
       "\n".join(body),
       "\n".join(wires),
       "\n".join(labels),
       "\n".join(noconns),
       '  (sheet_instances (path "/" (page "1")))',
       ')', '']

if not os.path.isdir(OUT):
    os.makedirs(OUT)
io.open(os.path.join(OUT, "sensor-board.kicad_sch"), "w", encoding="utf-8", newline="\n").write("\n".join(doc))

pro = ('{\n  "board": {},\n  "meta": {"filename": "sensor-board.kicad_pro", "version": 1},\n'
       '  "schematic": {},\n  "sheets": [["%s", "Root"]]\n}\n' % SHEET_UUID)
io.open(os.path.join(OUT, "sensor-board.kicad_pro"), "w", encoding="utf-8", newline="\n").write(pro)

# ---- authoritative netlist, independent of whether KiCad parses the schematic
nets = {}


def add(net, ref, pin):
    nets.setdefault(net, []).append("%s.%s" % (ref, pin))


for p, n in AS.items():
    add(n, "U1", p)
for p, n in RJ.items():
    add(n, "J1", p)
for ref, a, b_ in (("R1", "A_SRC", "A"), ("R2", "B_SRC", "B"), ("R3", "MAGD_SRC", "MAGD")):
    add(a, ref, 1)
    add(b_, ref, 2)
add("CSN", "R4", 1)
add("GND", "R4", 2)
for ref in ("C1", "C2"):
    add("+3V3", ref, 1)
    add("GND", ref, 2)
for p, n in {1: "A", 2: "B", 3: "MAGD", 4: "+3V3", 5: "GND"}.items():
    add(n, "D1", p)
for ref, n in (("TP1", "CLK"), ("TP2", "DO"), ("TP3", "MAGI")):
    add(n, ref, 1)

lines = ["Sensor board - net list",
         "generated from the same source as the schematic",
         "=" * 60, ""]
for n in sorted(nets, key=lambda s: (s in ("GND", "+3V3"), s)):
    lines.append("%-9s %s" % (n, "  ".join(sorted(set(nets[n])))))
lines += ["",
          "Cable pinout (must match ../controller-board/netlist.txt):",
          "  1=A  2=GND  3=B  4=+3V3  5=GND  6=GND  7=MagDECn  8=GND",
          "",
          "Not connected on U1: 1, 6, 10, 11, 16, 17, 20 (datasheet: must be left",
          "unconnected), plus 7 (Index) and 15 (PWM), which this design does not use."]
io.open(os.path.join(OUT, "netlist.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

print("wrote to", OUT)
print("symbols=%d  stubs=%d  labels=%d  no_connects=%d  nets=%d"
      % (len(body), len(wires), len(labels), len(noconns), len(nets)))
