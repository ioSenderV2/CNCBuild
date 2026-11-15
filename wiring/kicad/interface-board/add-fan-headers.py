"""Adds two 12 V fan headers to the interface board - Rev B, 2026-11-14.

Run with KiCad's bundled Python, from anywhere:
  python add-fan-headers.py

His, 2026-11-14: two fan headers, both always-on 12 V.

  J60  RAD FAN   the external fan on the radiator the coolant runs through on
                 its way back to the reservoir
  J61  CASE FAN  a 40 mm Noctua inside the 3D printed case that holds this
                 board stacked on the RP23

Both are the standard 4-pin PC fan header (Molex 47053-1000 class, KiCad's
FanPinHeader_1x04), which takes a 3-pin or a 4-pin fan plug and keys either:

  pin 1 GND    pin 2 +12 V    pin 3 tach - not connected    pin 4 PWM - not connected

A 4-pin PWM fan with pin 4 open runs at full speed, which is what always-on
means. Nothing on this board switches or reads a fan - it has no actives.

WHERE THEY GO - his, 2026-11-14: one in each half, because the halves are
what the case's lid does and does not open onto.

  J60 RAD FAN, TOP HALF. The lid's hole shows the machine-side connectors, and
      the radiator fan's lead comes in through it like every other machine
      cable. It takes the Z column's zone in input row 3, the one inter-bundle
      zone that held no connector - only the board's title, which silk.py moves.
  J61 CASE FAN, BOTTOM HALF. The Noctua is inside the case and its lead never
      leaves it. It stands at the east end of row A, beside the 12 V pair.
      There were 6.75 mm between 12 V OUT's courtyard and the board edge and
      this part's courtyard is 7.1, so 12 V OUT SLIDES 0.4 mm WEST - into the
      0.5 that separated it from 12 V IN, leaving 0.1 - and the header then
      sits 0.06 inside the edge. PIN 1 IS AT THE BOTTOM on this one, which
      puts the footprint's locating hole on the west side, away from the edge.
      TWO THINGS TRIED FIRST: sliding BOTH 12 V connectors a full millimetre
      does not route - it moves 12 V IN's pad onto the only row-A column the
      Z axis's LIM has, between that connector's peg and the flood block's
      via. And leaving them alone hangs this courtyard 0.34 over the edge,
      which the mounting sheet's own check refuses, rightly.

Both stand on end. GND and +12 V are the two inner planes and every pad here
is through-hole, so the headers route themselves: route.py lays no track for
them. J61 does sit on the two columns the B axis's LIM and EN used to drop
through row A on; route.py finds them new ones.

Two steps, schematic as text and board through pcbnew, then route.py, silk.py.
ONE-SHOT: it refuses a board that already has a J60.
"""

import re
import sys
import uuid
from pathlib import Path

import pcbnew

HERE = Path(__file__).resolve().parent
BOARD = str(HERE / "interface-board.kicad_pcb")
SCH = HERE / "interface-board.kicad_sch"

FP_NAME = "FanPinHeader_1x04_P2.54mm_Vertical"
FP_LIBS = (
    "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Connector.pretty",
    r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Connector.pretty",
)

# ref -> (value, schematic x, y, board pin-1 x, y, rotation)
# rotation -90: pins run DOWN the board from pin 1.  +90: UP from pin 1.
FANS = {
    "J60": ("FAN 4P - radiator fan, 12 V", 299.72, 300.99, 87.0, 42.3, -90),
    "J61": ("FAN 4P - case fan, 12 V",     299.72, 340.36, 122.1, 88.2, 90),
}
# 12 V OUT gives the case fan its room: ref -> new x
SLIDE_X = {"J19": 112.1}
PIN_NETS = {"1": "GND", "2": "+12V"}     # 3 tach and 4 PWM stay unconnected

# the schematic template: J37, a 1x4 whose four pins end 6.35 west of its
# anchor at 2.54 pitch, each with a label sitting on the pin end
TEMPLATE_REF = "J37"
PIN_DX = -6.35
PIN_DY = (-3.81, -1.27, 1.27, 3.81)


def top_level_spans(text):
    spans, depth, start, in_str, esc = [], 0, None, False, False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "(":
            depth += 1
            if depth == 2:
                start = i
        elif ch == ")":
            if depth == 2:
                spans.append((start, i + 1))
            depth -= 1
    return spans


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def add_to_schematic():
    with open(SCH, encoding="utf-8", newline="") as f:
        text = f.read()
    if '(property "Reference" "J60"' in text:
        print("schematic: J60 already there - skipped.")
        return
    spans = top_level_spans(text)
    tmpl = None
    for (a, b) in spans:
        item = text[a:b]
        if item.startswith("(symbol") and f'(property "Reference" "{TEMPLATE_REF}"' in item:
            tmpl = item
    if tmpl is None:
        raise RuntimeError(f"template symbol {TEMPLATE_REF} not found")
    m = re.search(r"\(at ([-0-9.]+) ([-0-9.]+) 0\)", tmpl)
    tx, ty = float(m.group(1)), float(m.group(2))
    tmpl_value = re.search(r'\(property "Value" "([^"]*)"', tmpl).group(1)
    tmpl_fp = re.search(r'\(property "Footprint" "([^"]*)"', tmpl).group(1)

    new = []
    for ref, (value, sx, sy, _bx, _by, _rot) in FANS.items():
        dx, dy = sx - tx, sy - ty

        def shift(mm_):
            return f"(at {fmt(float(mm_.group(1)) + dx)} {fmt(float(mm_.group(2)) + dy)} {mm_.group(3)})"

        sym = re.sub(r"\(at ([-0-9.]+) ([-0-9.]+) (\d+)\)", shift, tmpl)
        sym = sym.replace(f'"{TEMPLATE_REF}"', f'"{ref}"')
        sym = sym.replace(f'"{tmpl_value}"', f'"{value}"')
        sym = sym.replace(f'"{tmpl_fp}"', f'"Connector:{FP_NAME}"')
        sym = re.sub(r'\(uuid "[^"]*"\)', lambda _m: f'(uuid "{uuid.uuid4()}")', sym)
        new.append("\t" + sym + "\n")

        px = sx + PIN_DX
        for pin, pdy in zip("1234", PIN_DY):
            at = f"{fmt(px)} {fmt(sy + pdy)}"
            if pin in PIN_NETS:
                new.append(
                    f'\t(global_label "{PIN_NETS[pin]}"\n\t\t(shape passive)\n\t\t(at {at} 180)\n'
                    f"\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n"
                    f"\t\t\t(justify right bottom)\n\t\t)\n"
                    f'\t\t(uuid "{uuid.uuid4()}")\n\t)\n')
            else:
                new.append(f'\t(no_connect\n\t\t(at {at})\n\t\t(uuid "{uuid.uuid4()}")\n\t)\n')

    # insert ahead of (sheet_instances, which KiCad keeps after the items
    anchor = text.index("\t(sheet_instances")
    text = text[:anchor] + "".join(new) + text[anchor:]
    with open(SCH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"schematic: added {', '.join(FANS)} - pin 1 GND, pin 2 +12V, pins 3 and 4 no-connect.")


def add_to_board():
    board = pcbnew.LoadBoard(BOARD)
    if board.FindFootprintByReference("J60") is not None:
        raise RuntimeError("J60 is already on this board")
    lib = next((p for p in FP_LIBS if Path(p).is_dir()), None)
    if lib is None:
        raise RuntimeError("KiCad's Connector.pretty not found - add its path to FP_LIBS")

    for ref, x in SLIDE_X.items():
        f = board.FindFootprintByReference(ref)
        f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), f.GetPosition().y))

    for ref, (value, _sx, _sy, bx, by, rot) in FANS.items():
        fp = pcbnew.FootprintLoad(lib, FP_NAME)
        fp.SetReference(ref)
        fp.SetValue(value)
        fp.SetFPID(pcbnew.LIB_ID("Connector", FP_NAME))
        board.Add(fp)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(bx), pcbnew.FromMM(by)))
        fp.SetOrientationDegrees(rot)
        for pad in fp.Pads():
            net = PIN_NETS.get(pad.GetNumber())
            if net:
                code = board.FindNet(net)
                if code is None:
                    raise RuntimeError(f"net {net} not on board")
                pad.SetNet(code)
            elif pad.GetNumber():
                # the schematic gives an unconnected pin a net of its own, and
                # the parity check wants the pad to carry it by name
                ni = pcbnew.NETINFO_ITEM(board, f"unconnected-({ref}-Pad{pad.GetNumber()})")
                board.Add(ni)
                pad.SetNet(ni)
    pcbnew.SaveBoard(BOARD, board)
    print(f"board: placed {', '.join(FANS)}. Saved - now route.py, then silk.py.")


if __name__ == "__main__":
    add_to_schematic()
    add_to_board()
    sys.exit(0)
