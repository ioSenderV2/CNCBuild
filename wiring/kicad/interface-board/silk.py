"""Silkscreen labels for the interface board.

Run with KiCad's bundled Python after route.py:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' silk.py

Owns ALL free board text: deletes every PCB_TEXT on the silk layers, then adds
the labels from the tables below. Function names only - no connector types -
per his instruction. Signal names sit under each terminal position, rotated.
"""

import pcbnew

BOARD = r"C:\github\CNCBuild\wiring\kicad\interface-board\interface-board.kicad_pcb"

mm = pcbnew.FromMM

# (text, x, y, size, rotation_degrees)
LABELS = [
    # axis columns - one label per column under the stacked pair
    ("X",  21.0, 37.6, 2.0, 0),
    ("Y1", 41.0, 37.6, 2.0, 0),
    ("Y2", 61.0, 37.6, 2.0, 0),
    ("Z",  81.0, 37.6, 2.0, 0),
    ("B", 101.0, 37.6, 2.0, 0),
    # upper input row
    ("MIST",   123.0, 18.8, 1.2, 0),
    ("TOUCH 1", 137.0, 18.8, 1.2, 0),
    ("FLOOD",  156.0, 18.8, 1.2, 0),
    ("TOUCH 2", 175.0, 18.8, 1.2, 0),
    # lower input row
    ("3D PROBE",  117.5, 35.0, 1.2, 0),
    ("TOOLSETTER", 133.0, 37.2, 1.2, 0),
    ("SPINDLE",   149.6, 36.4, 1.2, 0),
    ("CONTROL",   168.1, 36.4, 1.2, 0),
    ("UART1",     186.6, 36.4, 1.2, 0),
    # terminal block row - block names above
    ("12V IN",  27.5, 77.7, 1.2, 0),
    ("12V OUT", 43.5, 77.7, 1.2, 0),
    ("LIMITS",  64.6, 77.7, 1.2, 0),
    ("SPINDLE", 83.0, 77.7, 1.2, 0),
    ("PROBE DOOR", 95.3, 77.7, 1.0, 0),
    ("MIST",   106.0, 77.7, 1.2, 0),
    ("FLOOD",  115.9, 77.7, 1.2, 0),
    ("CONTROL", 128.4, 77.7, 1.2, 0),
    ("UART1",  144.0, 77.7, 1.2, 0),
    # Teensy headers
    ("TEENSY  G S D E", 163.2, 66.0, 1.0, 0),
    ("X",  154.0, 81.6, 1.0, 0),
    ("Y1", 158.6, 81.6, 1.0, 0),
    ("Y2", 163.2, 81.6, 1.0, 0),
    ("Z",  167.8, 81.6, 1.0, 0),
    ("B",  172.4, 81.6, 1.0, 0),
    # ribbons
    ("RP23 J24 ALARMS", 13.5, 90.6, 1.0, 0),
    ("RP23 J20 STEPPERS", 196.0, 90.6, 1.2, 0),
    ("CNCBuild INTERFACE REV A", 107.5, 44.6, 1.5, 0),
]

# per-position signal names, rotated, under the terminal blocks
TB_PINS = {
    57.6: ["X", "Y1", "Y2", "Z", "B"],          # J21 limits, pitch 3.5
    77.7: ["EN", "G", "G", "PWM"],              # J22 spindle
    93.6: ["PRB", "DR"],                        # J23
    104.3: ["A", "B"],                          # J34 mist
    114.1: ["A", "B"],                          # J35 flood
    122.9: ["CS", "FH", "ES", "SP"],            # J36 control
    138.8: ["TX", "RX", "3V3", "G"],            # J37 uart
}


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
            add(nm, x0 + 3.5 * i, 90.9, 0.8, 90)
            count += 1

    pcbnew.SaveBoard(BOARD, board)
    print(f"placed {count} silk labels. Saved.")


if __name__ == "__main__":
    main()
