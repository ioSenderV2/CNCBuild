"""Silkscreen labels for the interface board - Rev B option 1 geometry.

Run with KiCad's bundled Python after route.py:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' silk.py

Owns ALL free board text and the IN/OUT divider: deletes every PCB_TEXT and
silk PCB_SHAPE, then adds the tables below. Function names only - no
connector types - per his instruction. The board reads top half MACHINE IN,
bottom half RP23 OUT, with a heavy divider line between (y 78.3, the strip
between corridor R's last lane and the output row's courtyards). Labels over
the lane corridors are fine: the vias are tented.
"""

import pcbnew

BOARD = r"C:\github\CNCBuild\wiring\kicad\interface-board\interface-board.kicad_pcb"

mm = pcbnew.FromMM

DIVIDER_Y = 105.8
DIVIDER_W = 0.5

# (text, x, y, size, rotation_degrees)
LABELS = [
    # axis columns - one label per column under the stacked pair
    ("X",   15.0, 38.4, 1.4, 0),
    ("Y1",  39.0, 38.4, 1.4, 0),
    ("Y2",  63.0, 38.4, 1.4, 0),
    ("Z",   87.0, 38.4, 1.4, 0),
    ("B",  111.0, 38.4, 1.4, 0),
    # stepper power row - the 36 V pair, one jack per axis
    ("36V",  15.0, 59.5, 0.9, 0),
    ("36V",  39.0, 59.5, 0.9, 0),
    ("36V",  63.0, 59.5, 0.9, 0),
    ("36V",  87.0, 59.5, 0.9, 0),
    ("36V", 111.0, 59.5, 0.9, 0),
    ("STEPPER 36V", 15.0, 44.0, 0.8, 0),
    # misc input row 3, labels between the rows
    ("CONTROL",    14.4, 81.65, 0.9, 0),
    ("TOOLSETTER", 38.9, 81.65, 0.9, 0),
    ("SPINDLE",    62.9, 81.65, 0.9, 0),
    ("3D PROBE",  109.5, 81.65, 0.9, 0),
    # misc input row 4, labels below
    ("TOUCH 1", 15.4, 96.3, 0.9, 0),
    ("TOUCH 2", 38.9, 96.3, 0.9, 0),
    ("MIST",    62.9, 96.3, 0.9, 0),
    ("FLOOD",   86.9, 96.3, 0.9, 0),
    ("UART1",  111.5, 96.3, 0.9, 0),
    # the halves, named
    ("MACHINE SIDE - IN", 65.5, 104.7, 1.2, 0),
    ("RP23 SIDE - OUT",   60.0, 119.1, 1.2, 0),
    # row A: ribbons, headers, 12 V
    ("RP23 J24 ALARMS",   20.3, 116.8, 0.9, 0),
    ("RP23 J20 STEPPERS", 56.0, 116.8, 0.9, 0),
    ("X",  31.5, 118.5, 0.9, 0),
    ("Y1", 36.1, 118.5, 0.9, 0),
    ("Y2", 78.6, 118.5, 0.9, 0),
    ("Z",  83.2, 118.5, 0.9, 0),
    ("B",  87.8, 118.5, 0.9, 0),
    ("TEENSY  G S D E", 33.8, 120.2, 0.9, 0),
    ("TEENSY  G S D E", 83.2, 120.2, 0.9, 0),
    ("12V IN",  105.0, 118.5, 0.9, 0),
    ("12V OUT", 117.5, 118.5, 0.9, 0),
    ("36V IN",  130.5, 118.5, 0.9, 0),
    # terminal block row - block names above
    ("CONTROL", 29.25, 127.65, 0.85, 0),
    ("LIMITS",  47.5, 127.65, 0.85, 0),
    ("PRB DR",  62.25, 127.65, 0.85, 0),
    ("SPINDLE", 75.25, 127.65, 0.85, 0),
    ("MIST",    87.75, 127.65, 0.85, 0),
    ("FLOOD",   96.75, 127.65, 0.85, 0),
    ("UART1",  115.81, 127.65, 0.85, 0),
    ("CNCBuild INTERFACE REV B", 86.5, 62.0, 1.2, 0),
]

# per-position signal names, rotated, above the output-row terminals
# anchor x of pad 1 -> (pitch, names)
TB_PINS = {
    24.0:  (3.5, ["CS", "FH", "ES", "SP"]),     # J36 control
    40.5:  (3.5, ["X", "Y1", "Y2", "Z", "B"]),  # J21 limits
    60.5:  (3.5, ["PRB", "DR"]),                # J23
    70.0:  (3.5, ["EN", "G", "G", "PWM"]),      # J22 spindle
    86.0:  (3.5, ["A", "B"]),                   # J34 mist
    95.0:  (3.5, ["A", "B"]),                   # J35 flood
    112.0: (2.54, ["TX", "RX", "3V3", "G"]),    # J37 uart - a 1x4 header now
}
TB_PIN_Y = 125.4          # just above the row B terminals

# the 36 V input block sits beside the 12 V pair, screws side by side
TB36 = (128.0, 115.4, 5.08, ["+", "-"])

# every 36 V connector stacks + over -, so the polarity marks stack too -
# a side-by-side pair would read as the wrong pin. x of each power jack.
PWR_JACKS = (15.0, 39.0, 63.0, 87.0, 111.0)
PWR_PLUS_Y, PWR_MINUS_Y = 48.0, 53.5

# parts whose reference text collides with the function labels: the ref moves
# onto the body center (visible bare, covered assembled - the label is what
# matters with the connector in place). Offset from footprint anchor, mm.
REF_ON_BODY = {
    "J11": (0.0, -0.9), "J12": (0.0, -0.9),
    "J13": (0.0, 3.25), "J14": (0.0, 3.25), "J30": (0.0, 3.25), "J31": (0.0, 3.25),
    "J15": (2.1, 3.25), "J32": (2.1, 3.25), "J33": (2.1, 3.25),
    "J21": (7.0, 0.1), "J22": (5.25, 0.1), "J23": (1.75, 0.1),
    "J34": (1.75, 0.1), "J35": (1.75, 0.1), "J36": (5.25, 0.1),
    # the stepper power row and its input block
    "J50": (0.0, 3.25), "J51": (0.0, 3.25), "J52": (0.0, 3.25),
    "J53": (0.0, 3.25), "J54": (0.0, 3.25), "J55": (2.85, 0.25),
    # J37 is the UART header, rotated 90: local (dx,dy) lands at board
    # (dy,-dx), so this puts the ref just south of the pin row
    "J37": (-2.3, 3.8),
    "J18": (2.85, 0.25), "J19": (2.85, 0.25),
}


def fix_refs():
    """Move the listed reference fields onto their part bodies by editing the
    board text: the (property "Reference" ... (at dx dy)) position is relative
    to the footprint, so the offsets in REF_ON_BODY go in verbatim."""
    import re
    with open(BOARD, encoding="utf-8") as f:
        text = f.read()
    for ref, (dx, dy) in REF_ON_BODY.items():
        pat = re.compile(
            r'(\(property "Reference" "' + ref + r'"\s*\n\s*\(at )[-0-9.]+ [-0-9.]+')
        text, n = pat.subn(lambda m: f"{m.group(1)}{dx} {dy}", text, count=1)
        if n != 1:
            raise RuntimeError(f"reference property for {ref} not found")
    with open(BOARD, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"moved {len(REF_ON_BODY)} reference fields onto their bodies.")


def main():
    board = pcbnew.LoadBoard(BOARD)

    for d in list(board.GetDrawings()):
        if d.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS) and \
                isinstance(d, (pcbnew.PCB_TEXT, pcbnew.PCB_SHAPE)):
            board.Remove(d)

    def add(text, x, y, size, rot):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        t.SetLayer(pcbnew.F_SilkS)
        t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
        t.SetTextThickness(mm(max(0.13, size * 0.15)))
        try:
            t.SetTextAngleDegrees(rot)
        except AttributeError:
            t.SetTextAngle(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
        board.Add(t)

    # the IN/OUT divider, interrupted where the IN banner text sits
    for (x1, x2) in ((6.0, 53.0), (78.5, 137.0)):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(mm(x1), mm(DIVIDER_Y)))
        s.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(DIVIDER_Y)))
        s.SetLayer(pcbnew.F_SilkS)
        s.SetWidth(mm(DIVIDER_W))
        board.Add(s)

    count = 0
    for (text, x, y, size, rot) in LABELS:
        add(text, x, y, size, rot)
        count += 1
    for (x0, (pitch, names)) in TB_PINS.items():
        for i, nm in enumerate(names):
            add(nm, x0 + pitch * i, TB_PIN_Y, 0.7, 90)
            count += 1
    tx, ty, tpitch, tnames = TB36
    for i, nm in enumerate(tnames):
        add(nm, tx + tpitch * i, ty, 0.9, 0)
        count += 1
    for jx in PWR_JACKS:
        add("+", jx - 3.3, PWR_PLUS_Y, 0.9, 0)
        add("-", jx - 3.3, PWR_MINUS_Y, 0.9, 0)
        count += 2

    pcbnew.SaveBoard(BOARD, board)
    print(f"placed {count} silk labels + divider. Saved.")
    # after the save: the reference fields are positioned text-level -
    # touching them through pcbnew's python crashes this build
    fix_refs()


if __name__ == "__main__":
    main()
