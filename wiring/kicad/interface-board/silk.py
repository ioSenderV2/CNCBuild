"""Silkscreen labels for the interface board - Rev B option 1 geometry.

Run with KiCad's bundled Python after route.py, from anywhere - the board is
found beside this file:
  Windows  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' silk.py
  macOS    /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 silk.py

Owns ALL free board text and the IN/OUT divider: deletes every PCB_TEXT and
silk PCB_SHAPE, then adds the tables below. Function names only - no
connector types - per his instruction. The board reads top half MACHINE IN,
bottom half RP23 OUT, with a heavy divider line between (y 76.7, the strip
between corridor R's last lane and the output row's courtyards). Labels over
the lane corridors are fine: the vias are tented.
"""

from pathlib import Path

import pcbnew

BOARD = str(Path(__file__).resolve().parent / "interface-board.kicad_pcb")

mm = pcbnew.FromMM

DIVIDER_Y = 76.7          # above the output row's reference fields, which
                          # sit around y 78.1 and the line used to cross
DIVIDER_W = 0.5

# (text, x, y, size, rotation_degrees)
LABELS = [
    # axis columns - one label per column under the stacked pair
    ("X",   15.0, 38.4, 1.4, 0),
    ("Y1",  39.0, 38.4, 1.4, 0),
    ("Y2",  63.0, 38.4, 1.4, 0),
    ("Z",   87.0, 38.4, 1.4, 0),
    ("B",  111.0, 38.4, 1.4, 0),
    # misc input row 3, labels between the rows
    ("CONTROL",    14.4, 54.15, 0.9, 0),
    ("TOOLSETTER", 38.9, 54.15, 0.9, 0),
    # SPINDLE until Rev C: the connector feeds the VFD's control terminals and
    # the label now says so - his, 2026-11-25
    ("VFD",        62.9, 54.15, 0.9, 0),
    ("3D PROBE",  109.5, 54.15, 0.9, 0),
    # the radiator fan header stands in the Z column's zone of row 3 - the
    # top half, because its lead comes in through the lid like a machine cable
    ("RAD FAN",    86.7, 54.15, 0.9, 0),
    # the Rev C alarm-OR jumpers, one on each axis's AL street in the strip
    # between rows 3 and 4 - a letter under each, the story told once. All
    # five shunts tie the drives' assert-on-fault alarms together and J17
    # pin 1 is the single output for the Teensy's motor-fault input.
    ("X OR", 47.9, 42.4, 0.7, 0),
    ("Y OR", 50.8, 54.2, 0.7, 0),
    ("A OR", 78.9, 42.4, 0.7, 0),
    ("Z OR", 92.5, 42.4, 0.7, 0),
    ("B OR", 118.9, 42.4, 0.7, 0),
    ("ALARM WIRE-OR - 5 SHUNTS = ONE ALARM OUT ON J17 PIN 1", 65.5, 67.4, 0.7, 0),
    # misc input row 4, labels below
    ("TOUCH 1", 15.4, 68.8, 0.9, 0),
    ("TOUCH 2", 38.9, 68.8, 0.9, 0),
    ("MIST",    62.9, 68.8, 0.9, 0),
    ("FLOOD",   86.9, 68.8, 0.9, 0),
    ("UART1",  111.5, 68.8, 0.9, 0),
    # the halves, named
    ("MACHINE SIDE - IN", 65.5, 75.5, 1.2, 0),
    ("RP23 SIDE - OUT",   60.0, 91.6, 1.2, 0),
    # row A: ribbons, headers, 12 V. The label LEADS with this board's own
    # reference: on Rev A the bold destination labels got read as the part's
    # reference - J16/J17 sat small at the board edge - and it cost a false
    # alarm probing the wrong pad. The part name comes first now.
    ("J17 - RP23 J24 ALARMS",   20.3, 89.3, 0.9, 0),
    ("J16 - RP23 J20 STEPPERS", 56.0, 89.3, 0.9, 0),
    # machine name = controller name. The headers run in column order, which
    # in controller letters is X Y A Z B - not the controller's own X Y Z A B
    # - because Y1 drives Y and Y2 drives A. Jumper by the label, not by
    # position, and the label now says both.
    ("X",    31.5, 91, 0.8, 0),
    ("Y1=Y", 36.1, 91, 0.8, 0),
    ("Y2=A", 78.6, 91, 0.8, 0),
    ("Z",    83.2, 91, 0.8, 0),
    ("B",    87.8, 91, 0.8, 0),
    ("TEENSY  G S D E", 33.8, 92.7, 0.9, 0),
    ("TEENSY  G S D E", 83.2, 92.7, 0.9, 0),
    # 12 V IN stays a Mini-Fit; 12 V OUT became a row-B terminal block in
    # Rev C and the UART1 header stands in its old spot
    ("12V IN",  98.5, 91, 0.9, 0),
    ("+ TOP  - BOTTOM", 98.5, 92.7, 0.8, 0),
    ("UART1", 112.1, 91, 0.9, 0),
    # J37's pin names, east of the pads (the jog columns run there - silk
    # over copper, a warning the board already carries 41 of)
    ("TX",  114.6, 81.10, 0.7, 0),
    ("RX",  114.6, 83.64, 0.7, 0),
    ("3V3", 114.9, 86.18, 0.7, 0),
    ("G",   114.6, 88.72, 0.7, 0),
    # the case fan header, east end of row A - bottom half, it never leaves
    # the enclosure
    ("CASE FAN", 121.6, 91, 0.8, 0),
    # terminal block row - block names above. SPINDLE reads VFD since Rev C,
    # and the east slot is the 12 V OUT block that took the UART header's place
    ("CONTROL", 29.25, 100.15, 0.85, 0),
    ("LIMITS",  47.5, 100.15, 0.85, 0),
    ("PRB DR",  62.25, 100.15, 0.85, 0),
    ("VFD",     75.25, 100.15, 0.85, 0),
    ("MIST",    87.75, 100.15, 0.85, 0),
    ("FLOOD",   96.75, 100.15, 0.85, 0),
    ("12V OUT", 106.75, 100.15, 0.85, 0),
    # the title gave its place in row 3 to the radiator fan header and stacks
    # in the south-west corner, over the S corridor (vias are tented)
    ("CNCBuild",  13.0, 93.2, 0.9, 0),
    ("INTERFACE", 13.0, 95.1, 0.9, 0),
    ("REV B",     13.0, 97.0, 0.9, 0),
]

# per-position signal names, rotated, above the output-row terminals
# anchor x of pad 1 -> (pitch, names)
TB_PINS = {
    24.0:  (3.5, ["CS", "FH", "ES", "SP"]),     # J36 control
    # J21 limits land on the controller too, so they carry the same mapping
    40.5:  (3.5, ["X", "Y1=Y", "Y2=A", "Z", "B"]),
    60.5:  (3.5, ["PRB", "DR"]),                # J23
    # the fourth terminal is the 0-10 V speed command and says so since
    # Rev C - PWM was never the signal there
    70.0:  (3.5, ["EN", "G", "G", "0-10V"]),    # J22 VFD
    86.0:  (3.5, ["A", "B"]),                   # J34 mist
    95.0:  (3.5, ["A", "B"]),                   # J35 flood
    105.0: (3.5, ["+12V", "G"]),                # J19 12 V OUT, the Rev C TB
}
TB_PIN_Y = 97.9           # just above the row B terminals

# parts whose reference text collides with the function labels: the ref moves
# onto the body center (visible bare, covered assembled - the label is what
# matters with the connector in place). Offset from footprint anchor, mm.
REF_ON_BODY = {
    "J11": (0.0, -0.9), "J12": (0.0, -0.9),
    "J13": (0.0, 3.25), "J14": (0.0, 3.25), "J30": (0.0, 3.25), "J31": (0.0, 3.25),
    "J15": (2.1, 3.25), "J32": (2.1, 3.25), "J33": (2.1, 3.25),
    "J21": (7.0, 0.1), "J22": (5.25, 0.1), "J23": (1.75, 0.1),
    "J34": (1.75, 0.1), "J35": (1.75, 0.1), "J36": (5.25, 0.1),
    # J37 stands vertical in row A since Rev C - ref in the strip under the
    # divider, where J40-J44 carry theirs
    "J37": (0.0, -2.38),
    "J18": (0.0, 3.25),
    # J19 is the Rev C 12 V OUT terminal block - same offset as its row-B kin
    "J19": (1.75, 0.1),
    # the alarm-OR jumpers: ref between the two pads, under the shunt. The
    # third value forces the text horizontal whatever the part's rotation.
    "JP1": (1.27, 0.0, 0), "JP2": (1.27, 0.0, 0), "JP3": (1.27, 0.0, 0),
    "JP4": (-1.45, 0.0, 0), "JP5": (1.27, 0.0, 0),
    # the radiator fan header stands on end, rotated -90: local (dx,dy) lands
    # at board (-dy,dx), so this puts the ref east of the body, mid-height
    "J60": (3.8, -5.5),
    # the case fan header stands on end, rotated +90: local (dx,dy) lands at
    # board (dy,-dx). His, 2026-11-14: its ref goes ABOVE the header, in the
    # strip under the divider where J40-J44 carry theirs - same height (board
    # y 78.07), centred on the body, and turned horizontal (the third value
    # is the text angle). It was hidden for a day on the wrong belief that no
    # side had room; the strip above was never tried.
    "J61": (10.13, 0.4, 0),
}


def fix_refs():
    """Move the listed reference fields onto their part bodies by editing the
    board text: the (property "Reference" ... (at dx dy)) position is relative
    to the footprint, so the offsets in REF_ON_BODY go in verbatim."""
    import re
    with open(BOARD, encoding="utf-8") as f:
        text = f.read()
    for ref, spec in REF_ON_BODY.items():
        dx, dy = spec[0], spec[1]
        angle = f" {spec[2]}" if len(spec) > 2 else None
        # the optional (hide yes) line is dropped: every ref listed here shows
        pat = re.compile(
            r'(\(property "Reference" "' + ref + r'"\s*\n\s*\(at )[-0-9.]+ [-0-9.]+( [-0-9.]+)?'
            r'(\)\s*\n\s*\(layer "[^"]*"\)\n)(?:\s*\(hide yes\)\n)?')
        text, n = pat.subn(
            lambda m: f"{m.group(1)}{dx} {dy}{angle if angle is not None else (m.group(2) or '')}{m.group(3)}",
            text, count=1)
        if n != 1:
            raise RuntimeError(f"reference property for {ref} not found")
    with open(BOARD, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"placed {len(REF_ON_BODY)} reference fields.")


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
    for (x1, x2) in ((6.0, 53.0), (78.5, 125.0)):
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
            add(nm, x0 + pitch * i, TB_PIN_Y, 0.8, 90)
            count += 1

    pcbnew.SaveBoard(BOARD, board)
    print(f"placed {count} silk labels + divider. Saved.")
    # after the save: the reference fields are positioned text-level -
    # touching them through pcbnew's python crashes this build
    fix_refs()


if __name__ == "__main__":
    main()
