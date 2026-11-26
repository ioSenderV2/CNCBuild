"""Rev C changes 1, 3 and 4 onto the schematic and board - 2026-11-26.

Run with KiCad's bundled Python, from anywhere:
  Windows  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' rev-c-changes.py

The four changes recorded in this folder's README, Rev C section; change 2
(the VFD silk labels) lives in silk.py's tables, not here:

  1. J19 (12 V OUT) stops being a Mini-Fit Jr and becomes a 3.5 mm 2P terminal
     block on the bottom edge, in the exact slot J37 vacates. J37 (UART1 out,
     1x4) moves up to J19's old spot at the east end of row A, rotated 90 -
     from lying along the TB row to standing in row A like the Teensy headers.
  3. The SPIN_PWM net renames to SPIN_0_10V - the signal was always the 0-10 V
     speed command - in the schematic's two global labels and the board's net
     table. netlist.txt follows via make-netlist.py.
  4. The alarm wire-OR jumpers: five 1x2s JP1-JP5, ONE IN EACH AXIS COLUMN'S
     ZONE, in the free strip between input rows 3 and 4, each 2.5 mm WEST of
     its column's bundle streets. Pin 1 carries that axis's AL net and
     reaches the AL street through a short B.Cu stub ending in a via placed
     on the street line itself - a via fits the 0.70 mm bundle pitch where a
     1.7 mm pad does not. Pin 2 of every jumper is AL_X - the rail - one
     B.Cu run across the top half (nothing else uses B.Cu above corridor R),
     jogging over each foreign stub on the way east. All five shunts fitted
     ties the five alarms together and J17 pin 1 (AL_X) is the one output
     for the Teensy's single motor-fault input; shunts off, the straight
     ribbon to the RP23 behaves as today. Measured 2026-11-25: these drives'
     alarms assert on fault, so the parallel OR is the correct combination.

     Board order west to east is X, Y, A, Z, B - the same "machine name =
     controller name" order the Teensy headers carry, because Y1 drives Y
     and Y2 drives A. route.py emits the stubs, vias and rail.

     THREE PLACEMENTS WERE TRIED FIRST AND FAILED IN ROUTING, kept here so
     nobody re-walks them: a clustered field in row A's open middle (x
     44-57) with straight drops from corridor R walls the ROWA jog corridor
     shut - EN_Y and LIM_Y's fixed streets could no longer jog around it;
     the same field fed by a nested comb starves the mid-board S-corridor
     descents (SPIN, MIST), because that zone is the ONLY crossing pool
     between the J41 header block and the J16 ribbon, whose lane-via rows
     make every jog across its columns collide; and pin 1 sitting DIRECTLY
     on the AL street breaks the neighboring DIR street - 0.70 mm away, a
     1.7 mm pad eats it.

ONE-SHOT: refuses a schematic or board that already carries JP1.
After it: route.py, silk.py, then the DRC with parity, then make-netlist.py.
"""

import re
import sys
import uuid
from pathlib import Path

import pcbnew

HERE = Path(__file__).resolve().parent
BOARD = str(HERE / "interface-board.kicad_pcb")
SCH = HERE / "interface-board.kicad_sch"

FP_LIBS_ROOT = (
    r"C:\Program Files\KiCad\10.0\share\kicad\footprints",
    "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints",
)

TB_LIB = "TerminalBlock_4Ucon"
TB_FP = "TerminalBlock_4Ucon_1x02_P3.50mm_Horizontal"
JP_LIB = "Connector_PinHeader_2.54mm"
JP_FP = "PinHeader_1x02_P2.54mm_Vertical"

J19_TB_POS = (105.0, 104.47)          # J37's vacated row-B slot
J37_POS = (112.1, 81.1)               # J19's old row-A anchor, now vertical
J37_PADS = {"1": (112.1, 81.10), "2": (112.1, 83.64),
            "3": (112.1, 86.18), "4": (112.1, 88.72)}

# Pads live in the strip between input rows 3 and 4 - EXCEPT JP1, which
# stacks a row higher, directly above JP2: the X zone's y 53-55 strip is the
# CONTROL quartet's ROW4 jog corridor (Rev B's FEED_HOLD ran straight through
# the spot), so the X jumper's stub runs west on B.Cu to the AL_X street
# instead. route.py owns the stubs, tap vias and rail.
JPS = [  # ref, x, pin-1 y, pin-1 net. VERTICAL: pin 1 on top, the AL_X rail
    # pad 2.54 below it. The pockets dodge, by measured coordinates: the
    # connector courtyards, the 3 mm NPTH pegs of the 3P Mini-Fits (which
    # want 2.6 mm from any plated hole), the ROW4 jog corridor at y 53-55
    # where the CONTROL and SPIN jogs weave, the bundle streets, and the
    # J60 fan's pad column. Horizontal jumpers in the inter-row strip and
    # street-straddling pads were both tried and both failed routing.
    ("JP1", 47.9, 44.50, "AL_X"),
    ("JP2", 47.9, 52.90, "AL_Y"),
    ("JP3", 78.9, 44.50, "AL_A"),
    ("JP4", 92.5, 44.50, "AL_Z"),
    ("JP5", 118.9, 44.50, "AL_B"),
]

J19_VALUE = "TB 2P - 12V OUT to RP23"
J37_VALUE = "header 1x4 - UART1 out to RP23"

# schematic template: J13, a cnc:CONN_1x02 - pins end 6.35 west of the anchor
# at +/-1.27 (pin 1 the upper one in sheet coordinates)
TEMPLATE_REF = "J13"
PIN_DX = -6.35
PIN_DY = {"1": -1.27, "2": 1.27}
JP_SCH = {  # ref -> sheet anchor
    "JP1": (299.72, 380.99), "JP2": (299.72, 400.99), "JP3": (299.72, 420.99),
    "JP4": (299.72, 440.99), "JP5": (299.72, 460.99),
}
JP_NET = {ref: net for (ref, _x, _y, net) in JPS}


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


def span_of_ref(text, ref):
    for (a, b) in top_level_spans(text):
        item = text[a:b]
        if item.startswith("(symbol") and f'(property "Reference" "{ref}"' in item:
            return a, b
    raise RuntimeError(f"symbol {ref} not found in schematic")


def edit_schematic():
    with open(SCH, encoding="utf-8", newline="") as f:
        text = f.read()
    if '"JP1"' in text:
        raise RuntimeError("schematic already carries JP1 - one-shot, not run twice")

    n = text.count("SPIN_PWM")
    if n != 2:
        raise RuntimeError(f"expected exactly 2 SPIN_PWM in schematic, found {n}")
    text = text.replace("SPIN_PWM", "SPIN_0_10V")

    # J19: Mini-Fit 2P symbol becomes the TB 2P - same pin geometry, so its
    # +12V / GND labels stay where they are
    a, b = span_of_ref(text, "J19")
    j19 = text[a:b]
    for old, new in (
        ('(lib_id "cnc:CONN_1x02")', '(lib_id "cnc:TB_1x02")'),
        ('"Mini-Fit 2P - 12V OUT to RP23"', f'"{J19_VALUE}"'),
        ('"Connector_Molex:Molex_Mini-Fit_Jr_5566-02A2_2x01_P4.20mm_Vertical"',
         f'"{TB_LIB}:{TB_FP}"'),
    ):
        if old not in j19:
            raise RuntimeError(f"J19 edit anchor missing: {old}")
        j19 = j19.replace(old, new, 1)
    text = text[:a] + j19 + text[b:]

    # J37: value only - the move is board-side
    a, b = span_of_ref(text, "J37")
    j37 = text[a:b]
    if '"TB 4P - UART1 out"' not in j37:
        raise RuntimeError("J37 value anchor missing")
    j37 = j37.replace('"TB 4P - UART1 out"', f'"{J37_VALUE}"', 1)
    text = text[:a] + j37 + text[b:]

    # the five jumpers, cloned from J13 the way add-fan-headers.py cloned J37
    a, b = span_of_ref(text, TEMPLATE_REF)
    tmpl = text[a:b]
    m = re.search(r"\(at ([-0-9.]+) ([-0-9.]+) 0\)", tmpl)
    tx, ty = float(m.group(1)), float(m.group(2))
    tmpl_value = re.search(r'\(property "Value" "([^"]*)"', tmpl).group(1)
    tmpl_fp = re.search(r'\(property "Footprint" "([^"]*)"', tmpl).group(1)

    new = []
    for ref, x, _py, top_net in JPS:
        sx, sy = JP_SCH[ref]
        dx, dy = sx - tx, sy - ty

        def shift(mm_):
            return (f"(at {fmt(float(mm_.group(1)) + dx)} "
                    f"{fmt(float(mm_.group(2)) + dy)} {mm_.group(3)})")

        sym = re.sub(r"\(at ([-0-9.]+) ([-0-9.]+) (\d+)\)", shift, tmpl)
        sym = sym.replace(f'"{TEMPLATE_REF}"', f'"{ref}"')
        axis = top_net.split("_")[1]
        sym = sym.replace(f'"{tmpl_value}"',
                          f'"jumper - AL_{axis} onto the alarm-OR rail"')
        sym = sym.replace(f'"{tmpl_fp}"', f'"{JP_LIB}:{JP_FP}"')
        sym = re.sub(r'\(uuid "[^"]*"\)', lambda _m: f'(uuid "{uuid.uuid4()}")', sym)
        new.append("\t" + sym + "\n")

        for pin, net in (("1", top_net), ("2", "AL_X")):
            at = f"{fmt(sx + PIN_DX)} {fmt(sy + PIN_DY[pin])}"
            new.append(
                f'\t(global_label "{net}"\n\t\t(shape passive)\n\t\t(at {at} 180)\n'
                f"\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n"
                f"\t\t\t(justify right bottom)\n\t\t)\n"
                f'\t\t(uuid "{uuid.uuid4()}")\n\t)\n')

    anchor = text.index("\t(sheet_instances")
    text = text[:anchor] + "".join(new) + text[anchor:]
    with open(SCH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("schematic: SPIN_PWM -> SPIN_0_10V, J19 -> TB 2P, J37 revalued, "
          "JP1-JP5 added with their labels.")


def rename_net_on_board_text():
    with open(BOARD, encoding="utf-8", newline="") as f:
        text = f.read()
    n = text.count("SPIN_PWM")
    if n == 0:
        raise RuntimeError("no SPIN_PWM on the board - already renamed?")
    text = text.replace("SPIN_PWM", "SPIN_0_10V")
    with open(BOARD, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"board text: SPIN_PWM -> SPIN_0_10V ({n} occurrences).")


def lib_dir(name):
    for root in FP_LIBS_ROOT:
        p = Path(root) / f"{name}.pretty"
        if p.is_dir():
            return str(p)
    raise RuntimeError(f"{name}.pretty not found under KiCad's footprint roots")


def pad_mm(fp):
    out = {}
    for pad in fp.Pads():
        if pad.GetNumber():
            p = pad.GetPosition()
            out[pad.GetNumber()] = (round(pcbnew.ToMM(p.x), 3),
                                    round(pcbnew.ToMM(p.y), 3))
    return out


def place(fp, x, y, rot):
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    fp.SetOrientationDegrees(rot)


def expect(fp, want, what):
    got = pad_mm(fp)
    for num, (ex, ey) in want.items():
        gx, gy = got[num]
        if abs(gx - ex) > 0.01 or abs(gy - ey) > 0.01:
            raise RuntimeError(
                f"{what}: pad {num} at ({gx},{gy}), wanted ({ex},{ey}) - "
                f"rotation convention differs, fix the rot constant")


def set_net(board, pad, name):
    net = board.FindNet(name)
    if net is None:
        raise RuntimeError(f"net {name} not on board")
    pad.SetNet(net)


def edit_board():
    board = pcbnew.LoadBoard(BOARD)
    if board.FindFootprintByReference("JP1") is not None:
        raise RuntimeError("JP1 is already on this board - one-shot, not run twice")

    # J19: the Mini-Fit goes, the TB arrives in J37's old slot
    old = board.FindFootprintByReference("J19")
    if old is None:
        raise RuntimeError("J19 not found")
    board.Remove(old)
    tb = pcbnew.FootprintLoad(lib_dir(TB_LIB), TB_FP)
    tb.SetReference("J19")
    tb.SetValue(J19_VALUE)
    tb.SetFPID(pcbnew.LIB_ID(TB_LIB, TB_FP))
    board.Add(tb)
    place(tb, *J19_TB_POS, 0)
    expect(tb, {"1": J19_TB_POS}, "J19 TB")
    set_net(board, [p for p in tb.Pads() if p.GetNumber() == "1"][0], "+12V")
    set_net(board, [p for p in tb.Pads() if p.GetNumber() == "2"][0], "GND")

    # J37 stands up in row A
    j37 = board.FindFootprintByReference("J37")
    place(j37, *J37_POS, 0)
    expect(j37, J37_PADS, "J37")
    j37.SetValue(J37_VALUE)

    # the jumpers, one per axis street. Pin 1 lands exactly on the street;
    # the rotation that puts pin 2 on the rail side is found by trying both.
    jp_lib = lib_dir(JP_LIB)
    for ref, x, py, top_net in JPS:
        fp = pcbnew.FootprintLoad(jp_lib, JP_FP)
        fp.SetReference(ref)
        axis = top_net.split("_")[1]
        fp.SetValue(f"jumper - AL_{axis} onto the alarm-OR rail")
        fp.SetFPID(pcbnew.LIB_ID(JP_LIB, JP_FP))
        board.Add(fp)
        want = {"1": (x, py), "2": (x, py + 2.54)}
        placed = False
        for rot in (0, 180):
            place(fp, x, py, rot)
            got = pad_mm(fp)
            if all(abs(got[n][0] - w[0]) < 0.01 and abs(got[n][1] - w[1]) < 0.01
                   for n, w in want.items()):
                placed = True
                break
        if not placed:
            expect(fp, want, ref)   # raises with the real coordinates
        set_net(board, [p for p in fp.Pads() if p.GetNumber() == "1"][0], top_net)
        set_net(board, [p for p in fp.Pads() if p.GetNumber() == "2"][0], "AL_X")

    pcbnew.SaveBoard(BOARD, board)
    print("board: J19 is the TB in row B, J37 stands at the east end of row A, "
          "JP1-JP5 placed. Saved - now route.py, then silk.py.")


if __name__ == "__main__":
    edit_schematic()
    rename_net_on_board_text()
    edit_board()
    sys.exit(0)
