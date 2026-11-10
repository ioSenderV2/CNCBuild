"""Regenerate netlist.txt from the LIVE board.

Run with KiCad's bundled Python:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' make-netlist.py

Why this exists: netlist.txt used to fall out of generate.py, and generate.py is a
SEED - it still writes the Rev A schematic and running it would destroy the hand
work KiCad now owns. So the file was being hand-edited after every change, which is
how a connection list quietly goes stale. It is now derived from the board instead,
and the board is checked against the schematic by

  kicad-cli pcb drc --schematic-parity ...

on every turn. Zero parity issues is what makes "from the board" and "from the
schematic" the same statement.

Lock pegs and mounting holes carry no pad number and no net, and are skipped.
"""

import pcbnew

BOARD = r"C:\github\CNCBuild\wiring\kicad\interface-board\interface-board.kicad_pcb"
OUT = r"C:\github\CNCBuild\wiring\kicad\interface-board\netlist.txt"


def main():
    board = pcbnew.LoadBoard(BOARD)

    nets = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        for pad in fp.Pads():
            num, net = pad.GetNumber(), pad.GetNetname()
            if not num or not net:
                continue
            nets.setdefault(net, set()).add("%s.%s" % (ref, num))

    lines = ["Interface board - net list",
             "generated from the routed board by make-netlist.py; the board is",
             "checked against the schematic by kicad-cli pcb drc --schematic-parity",
             "=" * 60, ""]
    for n in sorted(nets):
        lines.append("%-10s %s" % (n, "  ".join(sorted(nets[n]))))

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote %s: %d nets, %d pads"
          % (OUT, len(nets), sum(len(v) for v in nets.values())))


main()
