# -*- coding: utf-8 -*-
"""Generate interface-board.kicad_sch (KiCad 10) - the termination board that replaces the
DB37 breakout. SEED, run once: after KiCad has opened and re-saved the schematic, KiCad owns
it and re-running this overwrites hand edits (same rule as the other two boards).

Machine side (all connectors top-entry, exposed through the enclosure lid):
  5x RJ45 vertical     - one cat6 per stepper, column order X, Y1, Y2, Z, B
  5x Mini-Fit Jr 3P    - one prox per axis, paired next to its RJ45
  1x Mini-Fit Jr 3P    - 3D probe        (12V, NO signal -> PROBE)
  1x Mini-Fit Jr 3P    - toolsetter      (12V, NO signal -> DOOR)
  2x Mini-Fit Jr 2P    - touch probes    (NO signal -> PROBE, wired-OR)
  1x Mini-Fit Jr 4P    - spindle         (Enable, GND, GND, 0-10V)

Controller side (RP23U5XBB V2.02 - pin maps read from its schematic, committed in
manufacturer-assets/RP23U5XBB-V2.02-Schematic.pdf):
  2x10 IDC  - ribbon to RP23 J20, mirrored pin-for-pin
  2x3  IDC  - ribbon to RP23 J24 servo alarm header, per-axis parallel
  screw terminal blocks: 12V in (from the 36V->12V buck), 12V out (to the RP23's
  power inputs), 5P limits, 4P spindle, 2P probe+door

Axis mapping: the Y1 jack drives the controller's Y, the Y2 jack drives A.

RJ45 pin map (HIS CONVENTION striped = signal, solid = return; pair picks are mine):
  1 STEP  2 GND   3 EN   4 GND   5 DIR   6 GND   7 AL   8 GND
  (orange pair = Step, green = Enable, blue = Dir, brown = Alarm; Step and Alarm
  land on opposite edges of the jack - Step is the aggressor, Alarm feeds EStop)

3P pin order (mine, matches SN04 lead colours brown/black/blue): 1 = 12V, 2 = signal, 3 = GND.

Board is fully passive - connectors and copper only. Every signal class already crosses an
opto at one end or the other, and the 12V rail arrives regulated from the existing buck.

Same drawing convention as the other boards: connections are net labels on short wire
stubs, not point-to-point wires.
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
FONT = '(effects (font (size 1.27 1.27)))'

RJ_Y = [8.89, 6.35, 3.81, 1.27, -1.27, -3.81, -6.35, -8.89]


def rj_pins():
    return [(str(i + 1), -7.62, y, 0) for i, y in enumerate(RJ_Y)]


def conn_1xn_pins(n):
    top = (n - 1) * 1.27
    return [(str(i + 1), -6.35, top - i * 2.54, 0) for i in range(n)]


def conn_2xn_oe_pins(n):
    # Odd/even numbering, the KiCad Conn_02xNN_Odd_Even convention and the RP23's:
    # odds down one column, evens down the other, row by row.
    top = (n - 1) * 1.27
    out = []
    for i in range(n):
        y = top - i * 2.54
        out.append((str(2 * i + 1), -7.62, y, 0))
        out.append((str(2 * i + 2), 7.62, y, 180))
    return out


def lib_symbol(name, bodyrect, pins, ref, val, hide_names=True):
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
        s.append('      (pin passive line (at %s %s %d) (length 2.54) (name "%s" %s) (number "%s" %s))'
                 % (f(px), f(py), rot, num, FONT, num, FONT))
    s.append('    )')
    s.append('  )')
    return "\n".join(s)


def body_1xn(n):
    half = (n - 1) * 1.27 + 2.54
    return (-3.81, -half, 3.81, half)


def body_2xn(n):
    half = (n - 1) * 1.27 + 2.54
    return (-5.08, -half, 5.08, half)


LIBS = [
    lib_symbol("cnc:RJ45_8", (-5.08, -10.16, 5.08, 10.16), rj_pins(), "J", "RJ45_vertical"),
    lib_symbol("cnc:CONN_1x02", body_1xn(2), conn_1xn_pins(2), "J", "CONN_2P"),
    lib_symbol("cnc:CONN_1x03", body_1xn(3), conn_1xn_pins(3), "J", "CONN_3P"),
    lib_symbol("cnc:CONN_1x04", body_1xn(4), conn_1xn_pins(4), "J", "CONN_4P"),
    lib_symbol("cnc:TB_1x02", body_1xn(2), conn_1xn_pins(2), "J", "TB_2P"),
    lib_symbol("cnc:TB_1x04", body_1xn(4), conn_1xn_pins(4), "J", "TB_4P"),
    lib_symbol("cnc:TB_1x05", body_1xn(5), conn_1xn_pins(5), "J", "TB_5P"),
    lib_symbol("cnc:CONN_2x10_OE", body_2xn(10), conn_2xn_oe_pins(10), "J", "IDC_2x10"),
    lib_symbol("cnc:CONN_2x03_OE", body_2xn(3), conn_2xn_oe_pins(3), "J", "IDC_2x3"),
]
SYM_PINS = {"cnc:RJ45_8": rj_pins(),
            "cnc:CONN_1x02": conn_1xn_pins(2), "cnc:CONN_1x03": conn_1xn_pins(3),
            "cnc:CONN_1x04": conn_1xn_pins(4),
            "cnc:TB_1x02": conn_1xn_pins(2), "cnc:TB_1x04": conn_1xn_pins(4),
            "cnc:TB_1x05": conn_1xn_pins(5),
            "cnc:CONN_2x10_OE": conn_2xn_oe_pins(10), "cnc:CONN_2x03_OE": conn_2xn_oe_pins(3)}

SHEET_UUID = U()
body, wires, labels, noconns = [], [], [], []

GRID = 1.27


def snap(v):
    """Placement origins must land on the 1.27 mm connection grid - every pin offset and
    stub length here is already a multiple of 1.27, so snapping the origin puts every
    endpoint on-grid."""
    return round(v / GRID) * GRID


def place(lib, ref, val, x, y, conns):
    x, y = snap(x), snap(y)
    conns = dict((str(k), v) for k, v in conns.items())
    pins = SYM_PINS[lib]
    b = []
    b.append('  (symbol (lib_id "%s") (at %s %s 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)'
             % (lib, f(x), f(y)))
    b.append('    (uuid "%s")' % U())
    b.append('    (property "Reference" "%s" (at %s %s 0) (effects (font (size 1.27 1.27)) (justify left)))'
             % (ref, f(x - 3.81), f(y - 16.5)))
    b.append('    (property "Value" "%s" (at %s %s 0) (effects (font (size 1.27 1.27)) (justify left)))'
             % (val, f(x - 3.81), f(y - 14)))
    for num, px, py, rot in pins:
        b.append('    (pin "%s" (uuid "%s"))' % (num, U()))
    b.append('    (instances (project "interface-board" (path "/%s" (reference "%s") (unit 1))))'
             % (SHEET_UUID, ref))
    b.append('  )')
    body.append("\n".join(b))

    for num, px, py, rot in pins:
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
# (net suffix, panel label). Y1 jack -> controller Y, Y2 jack -> controller A.
AXES = [("X", "X"), ("Y", "Y1"), ("A", "Y2"), ("Z", "Z"), ("B", "B")]

NETS_BY_REF = {}  # ref -> {pin: net}, collected for the authoritative netlist


def rec(ref, conns):
    NETS_BY_REF[ref] = dict((str(k), v) for k, v in conns.items())
    return conns


# Machine side - five column pairs, one row per axis.
for i, (q, lab) in enumerate(AXES):
    y = 45 + i * 45
    rj = {1: "STEP_" + q, 2: "GND", 3: "EN_" + q, 4: "GND",
          5: "DIR_" + q, 6: "GND", 7: "AL_" + q, 8: "GND"}
    place("cnc:RJ45_8", "J%d" % (i + 1), "RJ45 vert - %s stepper" % lab,
          60, y, rec("J%d" % (i + 1), rj))
    px = {1: "+12V", 2: "LIM_" + q, 3: "GND"}
    place("cnc:CONN_1x03", "J%d" % (i + 6), "Mini-Fit 3P - %s prox" % lab,
          125, y, rec("J%d" % (i + 6), px))

# Probe family and spindle, bottom row.
place("cnc:CONN_1x03", "J11", "Mini-Fit 3P - 3D probe",
      60, 272, rec("J11", {1: "+12V", 2: "PROBE", 3: "GND"}))
place("cnc:CONN_1x03", "J12", "Mini-Fit 3P - toolsetter",
      125, 272, rec("J12", {1: "+12V", 2: "DOOR", 3: "GND"}))
place("cnc:CONN_1x02", "J13", "Mini-Fit 2P - touch probe 1",
      185, 272, rec("J13", {1: "PROBE", 2: "GND"}))
place("cnc:CONN_1x02", "J14", "Mini-Fit 2P - touch probe 2",
      240, 272, rec("J14", {1: "PROBE", 2: "GND"}))
place("cnc:CONN_1x04", "J15", "Mini-Fit 4P - spindle",
      300, 272, rec("J15", {1: "SPIN_EN", 2: "GND", 3: "GND", 4: "SPIN_PWM"}))

# Controller side. J16 mirrors RP23 J20 pin-for-pin (1:1 ribbon, pin 1 to pin 1).
J20_MAP = {}
for i, q in enumerate(("X", "Y", "Z", "A", "B")):   # RP23 J20 axis order, X at pin 1
    J20_MAP[4 * i + 1] = "DIR_" + q
    J20_MAP[4 * i + 2] = "EN_" + q
    J20_MAP[4 * i + 3] = "STEP_" + q
    J20_MAP[4 * i + 4] = "GND"
place("cnc:CONN_2x10_OE", "J16", "IDC 2x10 - ribbon to RP23 J20",
      330, 70, rec("J16", J20_MAP))

# J17 mirrors RP23 J24: GND on pin 2, five alarm inputs on 1,3,4,5,6. All five join one
# net on the RP23, so which pin is which axis only decides which of its LEDs lights -
# that mapping is not labelled in the RP23 schematic; read the silkscreen when wiring.
place("cnc:CONN_2x03_OE", "J17", "IDC 2x3 - ribbon to RP23 J24 alarms",
      330, 130, rec("J17", {1: "AL_X", 2: "GND", 3: "AL_Y",
                            4: "AL_Z", 5: "AL_A", 6: "AL_B"}))

# Terminal blocks. J20 is deliberately skipped as a reference - on this bench "J20"
# means the RP23's stepper header, and two J20s in one enclosure invites miswiring.
place("cnc:TB_1x02", "J18", "TB 2P - 12V IN from buck",
      240, 45, rec("J18", {1: "+12V", 2: "GND"}))
place("cnc:TB_1x02", "J19", "TB 2P - 12V OUT to RP23",
      240, 80, rec("J19", {1: "+12V", 2: "GND"}))
place("cnc:TB_1x05", "J21", "TB 5P - limits to RP23",
      240, 120, rec("J21", {1: "LIM_X", 2: "LIM_Y", 3: "LIM_A",
                            4: "LIM_Z", 5: "LIM_B"}))
place("cnc:TB_1x04", "J22", "TB 4P - spindle to RP23",
      240, 165, rec("J22", {1: "SPIN_EN", 2: "GND", 3: "GND", 4: "SPIN_PWM"}))
place("cnc:TB_1x02", "J23", "TB 2P - probe + door to RP23",
      240, 205, rec("J23", {1: "PROBE", 2: "DOOR"}))

TEXT = ('  (text "Interface board - terminates the machine cables, feeds the RP23U5XBB.'
        '\\nColumn pairs X Y1 Y2 Z B; Y1 -> controller Y, Y2 -> controller A.'
        '\\nRJ45: 1 Step, 3 En, 5 Dir, 7 AL (striped = signal), evens GND.'
        '\\n3P: 1 = 12V, 2 = signal, 3 = GND (SN04: brown / black / blue).'
        '\\nPassive - no actives, 12V arrives regulated from the existing buck."'
        ' (at 20 14 0) (effects (font (size 2.2 2.2)) (justify left)) (uuid "%s"))' % U())

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
       '  (sheet_instances (path "/" (page "1")))',
       ')', '']

if not os.path.isdir(OUT):
    os.makedirs(OUT)
io.open(os.path.join(OUT, "interface-board.kicad_sch"), "w", encoding="utf-8", newline="\n").write("\n".join(doc))

pro = ('{\n  "board": {},\n  "meta": {"filename": "interface-board.kicad_pro", "version": 1},\n'
       '  "schematic": {},\n  "sheets": [["%s", "Root"]]\n}\n' % SHEET_UUID)
io.open(os.path.join(OUT, "interface-board.kicad_pro"), "w", encoding="utf-8", newline="\n").write(pro)

# ---- authoritative netlist, independent of whether KiCad parses the schematic
nets = {}
for ref, conns in NETS_BY_REF.items():
    for p, n in conns.items():
        nets.setdefault(n, []).append("%s.%s" % (ref, p))

lines = ["Interface board - net list",
         "generated from the same source as the schematic",
         "=" * 60, ""]
for n in sorted(nets, key=lambda s: (s in ("GND", "+12V"), s)):
    lines.append("%-10s %s" % (n, "  ".join(sorted(set(nets[n])))))
lines += ["",
          "J16 ribbon is 1:1 to RP23 J20 (odds Dir/Step, evens Enable, 4/8/12/16/20 GND, X at pin 1).",
          "J17 ribbon is 1:1 to RP23 J24 (alarms on 1,3,4,5,6; GND on 2). Which alarm pin",
          "  lights which RP23 LED is unlabelled in its schematic - electrically one net.",
          "J20 is a skipped reference: on this bench J20 means the RP23's stepper header.",
          "RJ45 pin/pair and 3P pin-order assignments are recorded in the sheet text."]
io.open(os.path.join(OUT, "netlist.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

print("wrote to", OUT)
print("symbols=%d  stubs=%d  labels=%d  nets=%d"
      % (len(body), len(wires), len(labels), len(nets)))
