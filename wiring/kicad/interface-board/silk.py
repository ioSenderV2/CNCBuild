"""Silkscreen labels for the interface board - Rev B geometry.

Run with KiCad's bundled Python after route.py:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' silk.py

Owns ALL free board text: deletes every PCB_TEXT on the silk layers, then adds
the labels from the tables below. Function names only - no connector types -
per his instruction. Signal names sit above each terminal position, rotated
(the blocks sit on the bottom edge now, so there is no room below them).
Labels over the lane corridors are fine: the vias are tented.
"""

import pcbnew

BOARD = r"C:\github\CNCBuild\wiring\kicad\interface-board\interface-board.kicad_pcb"

mm = pcbnew.FromMM

# (text, x, y, size, rotation_degrees)
LABELS = [
    # axis columns - one label per column under the stacked pair
    ("X",  21.0, 38.4, 1.4, 0),
    ("Y1", 39.0, 38.4, 1.4, 0),
    ("Y2", 57.0, 38.4, 1.4, 0),
    ("Z",  75.0, 38.4, 1.4, 0),
    ("B",  93.0, 38.4, 1.4, 0),
    # row A: ribbons, Teensy headers, 12 V blocks
    ("RP23 J24 ALARMS", 20.25, 58.5, 0.9, 0),
    ("RP23 J20 STEPPERS", 55.0, 58.3, 0.9, 0),
    ("X",  27.9, 59.9, 0.9, 0),
    ("Y1", 32.4, 59.9, 0.9, 0),
    ("Y2", 74.4, 59.9, 0.9, 0),
    ("Z",  80.7, 59.9, 0.9, 0),
    ("B",  86.2, 59.9, 0.9, 0),
    ("TEENSY  G S D E", 36.0, 61.6, 0.9, 0),
    ("TEENSY  G S D E", 80.4, 61.6, 0.9, 0),
    ("12V IN",  93.6, 60.4, 1.0, 0),
    ("12V OUT", 105.5, 60.4, 1.0, 0),
    # misc row 3, labels above each connector
    ("3D PROBE",   15.0, 66.6, 1.0, 0),
    ("TOOLSETTER", 30.0, 66.6, 1.0, 0),
    ("SPINDLE",    47.1, 66.6, 1.0, 0),
    ("CONTROL",    65.6, 66.6, 1.0, 0),
    # misc row 4, labels below each connector (corridor S2, vias tented)
    ("TOUCH 1", 19.0, 93.6, 0.9, 0),
    ("TOUCH 2", 33.5, 93.6, 0.9, 0),
    ("MIST",    48.0, 93.6, 0.9, 0),
    ("FLOOD",   62.5, 93.6, 0.9, 0),
    ("UART1",   82.1, 93.6, 0.9, 0),
    # terminal block row - block names above
    ("LIMITS",     16.0, 100.0, 0.9, 0),
    ("PRB DR",     31.25, 100.0, 0.8, 0),
    ("SPINDLE",    44.75, 100.0, 0.9, 0),
    ("MIST",       57.75, 100.0, 0.9, 0),
    ("FLOOD",      66.95, 100.0, 0.9, 0),
    ("CONTROL",    79.25, 100.0, 0.9, 0),
    ("UART1",      96.25, 100.0, 0.9, 0),
    ("CNCBuild INTERFACE REV B", 46.0, 63.4, 1.4, 0),
]

# per-position signal names, rotated, above the terminal blocks
# anchor x of pad 1 -> names; pitch 3.5
TB_PINS = {
    9.0:  ["X", "Y1", "Y2", "Z", "B"],          # J21 limits
    29.5: ["PRB", "DR"],                        # J23
    39.5: ["EN", "G", "G", "PWM"],              # J22 spindle
    56.0: ["A", "B"],                           # J34 mist
    65.2: ["A", "B"],                           # J35 flood
    74.0: ["CS", "FH", "ES", "SP"],             # J36 control
    91.0: ["TX", "RX", "3V3", "G"],             # J37 uart
}


# parts whose reference text collides with the function labels: the ref moves
# onto the body center (visible bare, covered assembled - the label is what
# matters with the connector in place). Offset from footprint anchor, mm.
REF_ON_BODY = {
    "J11": (0.0, -0.9), "J12": (0.0, -0.9),
    "J13": (0.0, 3.25), "J14": (0.0, 3.25), "J30": (0.0, 3.25), "J31": (0.0, 3.25),
    "J15": (2.1, 3.25), "J32": (2.1, 3.25), "J33": (2.1, 3.25),
    "J21": (7.0, 0.1), "J22": (5.25, 0.1), "J23": (1.75, 0.1),
    "J34": (1.75, 0.1), "J35": (1.75, 0.1), "J36": (5.25, 0.1), "J37": (5.25, 0.1),
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
        if isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS):
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

    count = 0
    for (text, x, y, size, rot) in LABELS:
        add(text, x, y, size, rot)
        count += 1
    for (x0, names) in TB_PINS.items():
        for i, nm in enumerate(names):
            add(nm, x0 + 3.5 * i, 97.6, 0.7, 90)
            count += 1

    pcbnew.SaveBoard(BOARD, board)
    print(f"placed {count} silk labels. Saved.")
    # after the save: the reference fields are positioned text-level -
    # touching them through pcbnew's python crashes this build
    fix_refs()


if __name__ == "__main__":
    main()
