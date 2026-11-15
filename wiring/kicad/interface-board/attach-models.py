"""Attaches Molex's own 3D models to the connectors KiCad has none for - Rev B.

Run with KiCad's bundled Python, from anywhere, then make-mech.py:
  python attach-models.py

His, 2026-11-14: he downloaded the four STEP files from Molex (AP214) so the
board's STEP export carries real connector heights for the enclosure's lid.

THE MODELS ARE NOT IN THIS REPO. They are Molex's, and they sit untracked in
manufacturer-assets/3d/<part>/ with the datasheets. A clone without them still
opens and still passes DRC - the 3D view and the STEP just lack those parts.

  footprint                  Molex part    on the board
  RJ45 85508-5001            85508-5001    J1-J5
  Mini-Fit Jr 5566-03A3 1x3  39-30-1039    J6-J12
  Mini-Fit Jr 5566-02A2 2x1  39-29-9027    J13 J14 J30 J31 J18 J19
  Mini-Fit Jr 5566-04A2 2x2  39-29-9047    J15 J32 J33

HOW EACH WAS ALIGNED - measured, not eyeballed. Every model stands along its
own +Y, so each is turned -90 about X to stand on the board. Slicing the model
just under its housing gives its pins and pegs as islands, and those were
matched to the footprint's pads and peg holes:

  RJ45        pins, pegs and shield tabs land on the pads as drawn; the board
              plane is 8.6 below the model's origin
  2x1, 2x2    the model's first pin row is 0.65 off its origin, pegs put it
              the right way round; board plane 12.8 below the origin
  1x3         the model is the footprint turned half a turn - its two pegs
              are not symmetric, which settles it - and its pin row is 0.85
              off the origin; board plane at the origin

The offsets below are in KiCad's model frame, millimetres. make-mech.py's STEP
is the check: export one connector and measure where it landed.

Re-runnable: it replaces whatever model the listed footprints carry.
"""

import sys
from pathlib import Path

import pcbnew

HERE = Path(__file__).resolve().parent
BOARD = str(HERE / "interface-board.kicad_pcb")
MODELS = HERE.parent.parent.parent / "manufacturer-assets" / "3d"
KIPATH = "${KIPRJMOD}/../../../manufacturer-assets/3d/"

# footprint name -> (model file under 3d/, offset xyz, rotation xyz)
ATTACH = {
    "RJ45_Molex_85508-5001_Vertical":
        ("855085001/0855085001.stp", (0.0, 0.0, 8.6), (-90, 0, 0)),
    "Molex_Mini-Fit_Jr_5566-03A3_1x03_P4.20mm_Vertical":
        ("39301039/0039301039.stp", (0.0, 0.85, 0.0), (-90, 0, 180)),
    "Molex_Mini-Fit_Jr_5566-02A2_2x01_P4.20mm_Vertical":
        ("39299027/39299027.stp", (0.0, -0.65, 12.8), (-90, 0, 0)),
    "Molex_Mini-Fit_Jr_5566-04A2_2x02_P4.20mm_Vertical":
        ("39299047/39299047.stp", (0.0, -0.65, 12.8), (-90, 0, 0)),
}


def main():
    board = pcbnew.LoadBoard(BOARD)
    done = {}
    for fp in board.GetFootprints():
        name = fp.GetFPID().GetLibItemName().wx_str()
        if name not in ATTACH:
            continue
        rel, off, rot = ATTACH[name]
        if not (MODELS / rel).is_file():
            raise RuntimeError(f"model not found: {MODELS / rel}")
        models = fp.Models()
        models.clear()
        m = pcbnew.FP_3DMODEL()
        m.m_Filename = KIPATH + rel
        m.m_Offset = pcbnew.VECTOR3D(*off)
        m.m_Rotation = pcbnew.VECTOR3D(*rot)
        m.m_Scale = pcbnew.VECTOR3D(1, 1, 1)
        m.m_Show = True
        models.push_back(m)
        done.setdefault(name, []).append(fp.GetReference())
    missing = [n for n in ATTACH if n not in done]
    if missing:
        raise RuntimeError(f"no footprint on the board named {missing}")
    pcbnew.SaveBoard(BOARD, board)
    for name, refs in done.items():
        print(f"{ATTACH[name][0]:28} -> {', '.join(sorted(refs, key=lambda r: int(r[1:])))}")
    print("Saved - now make-mech.py.")


if __name__ == "__main__":
    main()
    sys.exit(0)
