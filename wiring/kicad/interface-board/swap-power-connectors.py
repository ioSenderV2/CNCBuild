"""One-shot: the three cabinet power feeds move from 5.08 mm screw blocks to Mini-Fit Jr.

Run with KiCad's bundled Python:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' swap-power-connectors.py

Why: unplugging a screw block leaves bare conductors on the end of a live-ish cable.
A Mini-Fit Jr is a latched, shrouded connector, so a disconnected feed is insulated -
his call 2026-11-09, and it makes all three cabinet feeds the same family as the five
stepper power jacks on the row above.

J55 goes to FOUR circuits, not two: the supply is 600 W at 36 V - 16.5 A across all
axes, nameplate, breakout-box.md - and Mini-Fit Jr is 9 A per circuit on 18 AWG, so
one circuit per leg does not carry the feed. Pins 1+2 are both +36V and pins 3+4 are
both 36V_RET, one row per leg, two crimps per leg in the cable.

Positions are set by courtyard, west to east, against J44's east edge at x 89.615 and
the board edge at 138.05 - the 4P body is 17.69 mm wide and only just fits, which is
why the 36 V input sits where it does rather than deeper into the east power channel.

Placement only. route.py owns every track, via and zone and is run after this.
"""

import pcbnew

BOARD = r"C:\github\CNCBuild\wiring\kicad\interface-board\interface-board.kicad_pcb"
LIB = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector_Molex.pretty"

MF2 = "Molex_Mini-Fit_Jr_5566-02A2_2x01_P4.20mm_Vertical"
MF4 = "Molex_Mini-Fit_Jr_5566-04A2_2x02_P4.20mm_Vertical"

ROW_Y = 108.6             # pad 1 row; pad 2 row is +5.5, pegs +5.04

# PACKED EAST, AND THE REASON IS ROW A'S CROSSINGS, NOT TIDINESS. Each 2P part
# blocks three x columns - pad plus two 3 mm NPTH lock pegs - where the screw
# block it replaces blocked two narrow ones. The first cut sat J18 at x 97 and
# FLOOD_B had no descent left between J44's pads (east edge 88.65) and J18's
# west peg. So the three are shoved as far east as the 4P's body allows and the
# recovered width all goes into that one gap.
SWAP = (
    ("J18", MF2, 98.5, {"1": "+12V", "2": "GND"},
     "Mini-Fit 2P - 12V IN from buck"),
    ("J19", MF2, 112.5, {"1": "+12V", "2": "GND"},
     "Mini-Fit 2P - 12V OUT to RP23"),
    ("J55", MF4, 126.5, {"1": "+36V", "2": "+36V", "3": "36V_RET", "4": "36V_RET"},
     "Mini-Fit 4P - 36V IN from supply, legs doubled"),
)


def main():
    board = pcbnew.LoadBoard(BOARD)
    mm = pcbnew.ToMM

    # Look everything up BEFORE mutating: GetPosition() on a footprint read back
    # after a Remove/Add returns an untyped SWIG object and blows up on .x.
    found = {}
    for ref, _, _, _, _ in SWAP:
        old = board.FindFootprintByReference(ref)
        if old is None:
            raise SystemExit("no footprint %s on the board" % ref)
        found[ref] = (old, old.GetPath(),
                      str(old.GetFPIDAsString()).split(":")[-1],
                      mm(old.GetX()), mm(old.GetY()))

    for ref, fpname, x, nets, value in SWAP:
        old, path, oldname, oldx, oldy = found[ref]
        print("%-5s was %-56s at (%.3f, %.3f)" % (ref, oldname, oldx, oldy))
        board.Remove(old)

        new = pcbnew.FootprintLoad(LIB, fpname)
        if new is None:
            raise SystemExit("library has no %s" % fpname)
        new.SetReference(ref)
        new.SetValue(value)
        new.SetPath(path)
        board.Add(new)
        new.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(ROW_Y)))

        for pad in new.Pads():
            want = nets.get(pad.GetNumber())
            if want is None:
                continue                      # the two NPTH lock pegs
            net = board.FindNet(want)
            if net is None:
                raise SystemExit("board has no net %s" % want)
            pad.SetNet(net)

        cy = new.GetCourtyard(pcbnew.F_CrtYd).BBox()
        print("      now %-56s at (%.3f, %.3f)  courtyard x %.3f .. %.3f  y %.3f .. %.3f"
              % (fpname, x, ROW_Y, mm(cy.GetLeft()), mm(cy.GetRight()),
                 mm(cy.GetTop()), mm(cy.GetBottom())))
        for pad in sorted(new.Pads(), key=lambda p: p.GetNumber()):
            if not pad.GetNumber():
                continue
            print("        pad %-2s (%.3f, %.3f) net=%s"
                  % (pad.GetNumber(), mm(pad.GetX()), mm(pad.GetY()),
                     pad.GetNetname()))

    pcbnew.SaveBoard(BOARD, board)
    print("saved")


main()
