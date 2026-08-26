# -*- coding: utf-8 -*-
"""Generate controller-board.kicad_sch (KiCad 8) for the CNCBuild encoder controller board.

Connections are made by NET LABEL on a short wire stub at each pin, not by point-to-point
wires. That is electrically identical for netlist/ERC purposes and far less error-prone to
generate than routing 40-odd nets by computed coordinates.
"""
import uuid, io, os

OUT = r"c:\github\CNCBuild\linear-encoder\kicad\controller-board"
U = lambda: str(uuid.uuid4())


def f(v):
    return str(int(v)) if float(v) == int(v) else ("%.4f" % v).rstrip('0').rstrip('.')


# --------------------------------------------------------------- symbol geometry
# KiCad convention: a pin's `at` IS its connection point, and `rot` points FROM that
# point TOWARD the body. Symbol space is Y-up; the sheet is Y-down, so py is mirrored
# when the symbol is placed.
HDR_Y = [11.43, 8.89, 6.35, 3.81, 1.27, -1.27, -3.81, -6.35, -8.89, -11.43]
RJ_Y = [8.89, 6.35, 3.81, 1.27, -1.27, -3.81, -6.35, -8.89]
FONT = '(effects (font (size 1.27 1.27)))'


def hdr_pins():
    out = []
    for row, y in enumerate(HDR_Y):
        out.append((str(row * 2 + 1), -5.08, y, 0))
        out.append((str(row * 2 + 2), 5.08, y, 180))
    return out


def rj_pins():
    out = [(str(i + 1), -7.62, y, 0) for i, y in enumerate(RJ_Y)]
    out.append(("SH", 0, -12.7, 90))
    return out


RC_PINS = [("1", 0, 3.81, 270), ("2", 0, -3.81, 90)]


def lib_symbol(name, bodyrect, pins, ref, val, hide_names=False):
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


LIBS = [
    lib_symbol("cnc:HDR_2x10", (-2.54, -12.7, 2.54, 12.7), hdr_pins(), "J", "Conn_02x10_2.00mm"),
    lib_symbol("cnc:RJ45_8", (-5.08, -12.7, 5.08, 11.43), rj_pins(), "J", "RJ45_no_magnetics"),
    lib_symbol("cnc:R", (-1.016, -2.54, 1.016, 2.54), RC_PINS, "R", "R", hide_names=True),
    lib_symbol("cnc:C", (-1.016, -2.54, 1.016, 2.54), RC_PINS, "C", "C", hide_names=True),
]
SYM_PINS = {"cnc:HDR_2x10": hdr_pins(), "cnc:RJ45_8": rj_pins(),
            "cnc:R": RC_PINS, "cnc:C": RC_PINS}

SHEET_UUID = U()
body, wires, labels, noconns = [], [], [], []

GRID = 1.27


def snap(v):
    """Placement origins must land on the 1.27 mm connection grid. Every pin offset and stub
    length in this file is already a multiple of 1.27, so snapping the origin puts every
    endpoint on-grid. KiCad flags off-grid endpoints because they can silently fail to
    connect when the schematic is later edited by hand."""
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
    b.append('    (instances (project "controller-board" (path "/%s" (reference "%s") (unit 1))))'
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
# Module header P1. Pins 2 (5V), 5/7 (UART) and 6/8 (USB) deliberately unconnected.
HDR = {1: "+3V3", 3: "GND", 4: "GND",
       9: "IO3", 11: "IO4", 13: "IO5", 15: "IO6", 17: "IO7", 19: "IO8",
       20: "IO9", 18: "IO10", 16: "IO11", 14: "IO12", 12: "IO13", 10: "IO14"}
place("cnc:HDR_2x10", "J5", "P1 2.00mm 2x10", 60, 150, HDR, nc=(2, 5, 6, 7, 8))

AXES = [("J1", "X", "IO3", "IO4", "IO5", 45),
        ("J2", "Y", "IO6", "IO7", "IO8", 110),
        ("J3", "A", "IO9", "IO10", "IO11", 175),
        ("J4", "Z", "IO12", "IO13", "IO14", 240)]

caps = []
for i, (ref, axis, a, b_, mag, y) in enumerate(AXES):
    place("cnc:RJ45_8", ref, "RJ45 %s - NO MAGNETICS" % axis, 170, y,
          {1: a, 2: "GND", 3: b_, 4: "+3V3", 5: "GND", 6: "GND", 7: mag, 8: "GND", "SH": "SHLD"})
    place("cnc:R", "R%d" % (i + 1), "2k2", 225, y, {1: "+3V3", 2: mag})
    for j, net in enumerate((a, b_, mag)):
        caps.append((net, 265 + j * 22, y))

for k, (net, cx, cy) in enumerate(caps):
    place("cnc:C", "C%d" % (k + 1), "1n", cx, cy, {1: net, 2: "GND"})

place("cnc:R", "R5", "0R shield link", 60, 250, {1: "SHLD", 2: "GND"})

TEXT = ('  (text "Controller board  -  4x shielded RJ45 (NO MAGNETICS) -> ESP32-S3-RS485-CAN P1'
        '\\nConnected by net label. Rationale and mechanical envelope: linear-encoder/controller-board.md"'
        ' (at 20 18 0) (effects (font (size 2.2 2.2)) (justify left)) (uuid "%s"))' % U())

doc = ['(kicad_sch (version 20231120) (generator "eeschema") (generator_version "8.0")',
       '  (uuid "%s")' % SHEET_UUID,
       '  (paper "A2")',
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
io.open(os.path.join(OUT, "controller-board.kicad_sch"), "w", encoding="utf-8", newline="\n").write("\n".join(doc))

pro = ('{\n  "board": {},\n  "meta": {"filename": "controller-board.kicad_pro", "version": 1},\n'
       '  "schematic": {},\n  "sheets": [["%s", "Root"]]\n}\n' % SHEET_UUID)
io.open(os.path.join(OUT, "controller-board.kicad_pro"), "w", encoding="utf-8", newline="\n").write(pro)

# ---- authoritative netlist, independent of whether KiCad parses the schematic
nets = {}


def add(net, ref, pin):
    nets.setdefault(net, []).append("%s.%s" % (ref, pin))


for p, n in HDR.items():
    add(n, "J5", p)
for i, (ref, axis, a, b_, mag, y) in enumerate(AXES):
    for p, n in {1: a, 2: "GND", 3: b_, 4: "+3V3", 5: "GND", 6: "GND",
                 7: mag, 8: "GND", "SH": "SHLD"}.items():
        add(n, ref, p)
    add("+3V3", "R%d" % (i + 1), 1)
    add(mag, "R%d" % (i + 1), 2)
for k, (net, cx, cy) in enumerate(caps):
    add(net, "C%d" % (k + 1), 1)
    add("GND", "C%d" % (k + 1), 2)
add("SHLD", "R5", 1)
add("GND", "R5", 2)

lines = ["Controller board - net list", "generated from the same source as the schematic", "=" * 60, ""]
for n in sorted(nets, key=lambda s: (s in ("GND", "+3V3", "SHLD"), s)):
    lines.append("%-8s %s" % (n, "  ".join(sorted(set(nets[n])))))
lines += ["", "Not connected on P1: 2 (5V), 5/7 (UART TXD/RXD), 6/8 (USB D+/D-)."]
io.open(os.path.join(OUT, "netlist.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

print("wrote to", OUT)
print("symbols=%d  stubs=%d  labels=%d  no_connects=%d  nets=%d" % (len(body), len(wires), len(labels), len(noconns), len(nets)))
