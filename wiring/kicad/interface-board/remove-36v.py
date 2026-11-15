"""Takes the 36 V off the interface board - Rev B strip-down, 2026-11-14.

Run with KiCad's bundled Python, from anywhere:
  python remove-36v.py

His call, 2026-11-14: stepper power is distributed on the DIN rail beside the
XDR (Phoenix PT 4-QUATTRO blocks), not on this board. What that removes:

  - J50..J54, the five Mini-Fit 2P stepper power jacks, and J55, the 2x2 input;
  - the +36V and 36V_RET nets, so every pour and the stitched east channel;
  - 27.5 mm of height (the power band) and 12 mm of width (the east channel).

Three things happen here, in this order, and route.py / silk.py do the rest:

  1. SCHEMATIC, as text: the six symbols, their fourteen labels and any wire
     that ends on one of those labels. Text-level because the schematic is not
     reachable from pcbnew, and a removal is safe to do by span.
  2. BOARD: the six footprints go; everything below the limit row moves up by
     27.5; the two east mounting holes come in with the edge.
  3. BOARD OUTLINE: Edge.Cuts is redrawn at 121 x 104.5.

Kept as the record of how the board got from 133 x 132 back to 121 x 104.5,
the way swap-power-connectors.py records the step that went the other way.
ONE-SHOT: it refuses to run on a board that has no J50.
"""

import re
from pathlib import Path

import pcbnew

HERE = Path(__file__).resolve().parent
BOARD = str(HERE / "interface-board.kicad_pcb")
SCH = HERE / "interface-board.kicad_sch"

GONE_REFS = {"J50", "J51", "J52", "J53", "J54", "J55"}
GONE_NETS = {"+36V", "36V_RET"}

SHIFT_BELOW_Y = 37.0      # the limit row ends at 36.8; everything under it moves
SHIFT = -27.5             # the power band's height
EDGE = (5.0, 5.0, 126.0, 109.5)
# the east holes were at x 130 and 132, outside the new edge. 122.3 keeps a
# 6 mm screw head 0.7 inside the edge and off the B jack's body (courtyard
# ends at 119.59); the B column's bundle street shares that x but only starts
# at y 20.7, well under the hole.
HOLES = {"MH2": (122.3, 9.0), "MH4": (122.3, 104.8)}
# the UART header's pin 4 sat at x 119.62, under where MH4 has to go. It
# slides west into the gap the narrower board leaves beside the flood block
# (courtyard ends 101.14), which is what frees the corner for the hole.
SLIDE_X = {"J37": 105.0}

mm = pcbnew.FromMM


def top_level_spans(text):
    """(start, end) of every direct child of the root s-expression."""
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


def strip_schematic():
    with open(SCH, encoding="utf-8", newline="") as f:
        text = f.read()
    spans = top_level_spans(text)
    at = re.compile(r"\(at ([-0-9.]+) ([-0-9.]+)")
    xy = re.compile(r"\(xy ([-0-9.]+) ([-0-9.]+)\)")

    drop, label_pts = [], set()
    for (a, b) in spans:
        item = text[a:b]
        if item.startswith("(label "):
            name = re.match(r'\(label "([^"]*)"', item).group(1)
            if name in GONE_NETS:
                drop.append((a, b))
                label_pts.add(at.search(item).groups())
        elif item.startswith("(symbol"):
            m = re.search(r'\(property "Reference" "([^"]*)"', item)
            if m and m.group(1) in GONE_REFS:
                drop.append((a, b))
    wires = 0
    for (a, b) in spans:
        item = text[a:b]
        if item.startswith("(wire") and any(p in label_pts for p in xy.findall(item)):
            drop.append((a, b))
            wires += 1

    syms = sum(1 for (a, b) in drop if text[a:b].startswith("(symbol"))
    labels = sum(1 for (a, b) in drop if text[a:b].startswith("(label "))
    if syms == 0 and labels == 0:
        print("schematic: no 36 V parts left - already stripped.")
        return
    if syms != len(GONE_REFS):
        raise RuntimeError(f"expected {len(GONE_REFS)} symbols, found {syms}")

    for (a, b) in sorted(drop, reverse=True):
        # take the item's own line start and trailing newline with it
        while a > 0 and text[a - 1] in " \t":
            a -= 1
        if text[b:b + 1] == "\n":
            b += 1
        text = text[:a] + text[b:]
    with open(SCH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"schematic: removed {syms} symbols, {labels} labels, {wires} wires.")


def strip_board():
    board = pcbnew.LoadBoard(BOARD)
    if board.FindFootprintByReference("J50") is None:
        raise RuntimeError("no J50 on this board - the 36 V is already off it")

    # the copper is left alone: route.py strips every track, via and zone
    # from the file as text before it rebuilds them, and walking tracks
    # through this build's python bindings fails outright.
    # MOVES FIRST, REMOVALS LAST, and nothing held across a Remove(): this
    # build's bindings hand back untyped objects for anything fetched before
    # a footprint is taken off the board.
    moved = 0
    for f in board.GetFootprints():
        ref = f.GetReference()
        if ref in GONE_REFS:
            continue
        p = f.GetPosition()
        if ref in HOLES:
            x, y = HOLES[ref]
            f.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        elif pcbnew.ToMM(p.y) > SHIFT_BELOW_Y:
            x = mm(SLIDE_X[ref]) if ref in SLIDE_X else p.x
            f.SetPosition(pcbnew.VECTOR2I(x, p.y + mm(SHIFT)))
            moved += 1

    for d in list(board.GetDrawings()):
        if d.GetLayer() == pcbnew.Edge_Cuts:
            board.Remove(d)
    x0, y0, x1, y1 = EDGE
    r = pcbnew.PCB_SHAPE(board)
    r.SetShape(pcbnew.SHAPE_T_RECT)
    r.SetStart(pcbnew.VECTOR2I(mm(x0), mm(y0)))
    r.SetEnd(pcbnew.VECTOR2I(mm(x1), mm(y1)))
    r.SetLayer(pcbnew.Edge_Cuts)
    r.SetWidth(mm(0.1))
    board.Add(r)

    for ref in sorted(GONE_REFS):
        board.Remove(board.FindFootprintByReference(ref))

    pcbnew.SaveBoard(BOARD, board)
    print(f"board: removed {len(GONE_REFS)} footprints, moved {moved} up by "
          f"{-SHIFT}, holes {sorted(HOLES)} brought in, outline "
          f"{x1 - x0} x {y1 - y0}. Saved - now route.py, then silk.py.")


if __name__ == "__main__":
    strip_schematic()
    strip_board()
