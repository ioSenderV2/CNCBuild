"""The board as mechanical drawings, for laying out the enclosure - Rev B.

Run with KiCad's bundled Python, from anywhere:
  python make-mech.py

His, 2026-11-14: a DXF of the board's perimeter, its mounting holes and every
connector's outline, to import into Fusion and lay out the openings in the top
of the enclosure. And a STEP of the whole board, for the heights a DXF has not.

Writes, beside this script in mech/:

  interface-board-revb.dxf    flat, millimetres, seen from the component side
  interface-board-revb.step   the board with its connectors standing on it

THE DXF'S ORIGIN IS THE BOARD'S BOTTOM-LEFT CORNER, X RIGHT, Y UP - every
coordinate is positive, which is what a Fusion sketch wants. The mounting
sheet measures from the TOP-left corner with y down, so x agrees and
y here = board height - y there.

ITS LAYERS, so each can be switched off at import:

  BOARD            the perimeter
  HOLES            the four mounting holes, circles at the drilled diameter
  BODY_TOP         one closed rectangle per connector ABOVE the divider - the
                   machine-side group, the ones the lid opens onto
  BODY_BOTTOM      the same for the group below it, internal to the case
  FAB_DETAIL       the footprints' own fabrication drawings, line for line -
                   latches, pin-1 chamfers, screw heads. Reference only
  COURTYARD        body plus KiCad's clearance margin. Reference only
  REFS             each connector's reference, as text at its body's centre

BODY_* IS THE BOUNDING RECTANGLE OF THE FABRICATION OUTLINE, not the outline
itself: a Mini-Fit's drawing carries its latch as a bump, and a rectangle that
takes the bump in is the one an opening has to clear. It is the HEADER on the
board. THE MATING PLUG IS BIGGER and is not on this board - size an opening
from the plug, and use this for where its centre goes.

The STEP's origin is the same corner, and the board's top face is at z 1.6.
The Molex connectors stand on it from Molex's own models, which attach-models.py
aligns and which live UNTRACKED in manufacturer-assets/3d/ - without them those
parts are simply absent. The terminal blocks have no model at all. The script
lists what is absent each run. The STEP is not tracked - regenerate it.
"""

import math
import subprocess
import sys
from pathlib import Path

import pcbnew

HERE = Path(__file__).resolve().parent
BOARD = HERE / "interface-board.kicad_pcb"
OUT = HERE / "mech"
DXF = OUT / "interface-board-revb.dxf"
STEP = OUT / "interface-board-revb.step"

# silk.py's divider line: connectors above it are the machine-side group
DIVIDER_Y = 76.7

KICAD_CLI = (
    "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
    r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
)

LAYERS = {              # name -> AutoCAD colour index
    "BOARD": 7, "HOLES": 1, "BODY_TOP": 3, "BODY_BOTTOM": 5,
    "FAB_DETAIL": 8, "COURTYARD": 6, "REFS": 2,
}

mm = pcbnew.ToMM


class Dxf:
    """A minimal R12 ASCII DXF: LINE, CIRCLE, ARC and TEXT on named layers."""

    def __init__(self):
        self.ents = []

    def line(self, layer, a, b):
        if abs(a[0] - b[0]) < 1e-6 and abs(a[1] - b[1]) < 1e-6:
            return
        self.ents.append(f"0\nLINE\n8\n{layer}\n10\n{a[0]:.4f}\n20\n{a[1]:.4f}\n30\n0.0\n"
                         f"11\n{b[0]:.4f}\n21\n{b[1]:.4f}\n31\n0.0\n")

    def rect(self, layer, x0, y0, x1, y1):
        p = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            self.line(layer, p[i], p[(i + 1) % 4])

    def circle(self, layer, c, r):
        self.ents.append(f"0\nCIRCLE\n8\n{layer}\n10\n{c[0]:.4f}\n20\n{c[1]:.4f}\n30\n0.0\n40\n{r:.4f}\n")

    def arc(self, layer, start, mid, end):
        """Through three points. DXF arcs run counter-clockwise from the first
        angle to the second, so the ends swap when start-mid-end is clockwise."""
        (ax, ay), (bx, by), (cx, cy) = start, mid, end
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < 1e-9:
            self.line(layer, start, end)
            return
        ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay)
              + (cx * cx + cy * cy) * (ay - by)) / d
        uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx)
              + (cx * cx + cy * cy) * (bx - ax)) / d
        r = math.hypot(ax - ux, ay - uy)
        ccw = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) > 0
        s, e = (start, end) if ccw else (end, start)
        a0 = math.degrees(math.atan2(s[1] - uy, s[0] - ux)) % 360
        a1 = math.degrees(math.atan2(e[1] - uy, e[0] - ux)) % 360
        self.ents.append(f"0\nARC\n8\n{layer}\n10\n{ux:.4f}\n20\n{uy:.4f}\n30\n0.0\n40\n{r:.4f}\n"
                         f"50\n{a0:.4f}\n51\n{a1:.4f}\n")

    def text(self, layer, c, height, s):
        # 72/73 = centred both ways on the second alignment point
        self.ents.append(f"0\nTEXT\n8\n{layer}\n10\n{c[0]:.4f}\n20\n{c[1]:.4f}\n30\n0.0\n40\n{height}\n"
                         f"1\n{s}\n72\n1\n73\n2\n11\n{c[0]:.4f}\n21\n{c[1]:.4f}\n31\n0.0\n")

    def write(self, path):
        # R12 carries no units: the numbers are millimetres, say so at import
        out = ["0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n0\nENDSEC\n",
               "0\nSECTION\n2\nTABLES\n"
               "0\nTABLE\n2\nLTYPE\n70\n1\n0\nLTYPE\n2\nCONTINUOUS\n70\n0\n3\nSolid line\n"
               "72\n65\n73\n0\n40\n0.0\n0\nENDTAB\n",
               "0\nTABLE\n2\nSTYLE\n70\n1\n0\nSTYLE\n2\nSTANDARD\n70\n0\n40\n0.0\n41\n1.0\n50\n0.0\n"
               "71\n0\n42\n1.0\n3\ntxt\n4\n\n0\nENDTAB\n",
               f"0\nTABLE\n2\nLAYER\n70\n{len(LAYERS)}\n"]
        for name, colour in LAYERS.items():
            out.append(f"0\nLAYER\n2\n{name}\n70\n0\n62\n{colour}\n6\nCONTINUOUS\n")
        out.append("0\nENDTAB\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n")
        out.extend(self.ents)
        out.append("0\nENDSEC\n0\nEOF\n")
        with open(path, "w", encoding="ascii", newline="\n") as f:
            f.write("".join(out))


def draw_shape(dxf, layer, g, T):
    """One PCB_SHAPE onto a layer. Returns the points it spans, for the bbox."""
    sh = g.GetShape()
    if sh == pcbnew.SHAPE_T_SEGMENT:
        a, b = T(g.GetStart()), T(g.GetEnd())
        dxf.line(layer, a, b)
        return [a, b]
    if sh == pcbnew.SHAPE_T_RECT:
        pts = [T(p) for p in g.GetRectCorners()]
        for i in range(4):
            dxf.line(layer, pts[i], pts[(i + 1) % 4])
        return pts
    if sh == pcbnew.SHAPE_T_CIRCLE:
        c, r = T(g.GetCenter()), mm(g.GetRadius())
        dxf.circle(layer, c, r)
        return [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]
    if sh == pcbnew.SHAPE_T_ARC:
        a, m, b = T(g.GetStart()), T(g.GetArcMid()), T(g.GetEnd())
        dxf.arc(layer, a, m, b)
        return [a, m, b]
    raise RuntimeError(f"shape type {sh} on {layer} is not handled")


def make_dxf():
    board = pcbnew.LoadBoard(str(BOARD))
    edges = [d for d in board.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts]
    if len(edges) != 1 or edges[0].GetShape() != pcbnew.SHAPE_T_RECT:
        raise RuntimeError("Edge.Cuts is expected to be one rectangle")
    e = edges[0]
    x0, x1 = sorted((mm(e.GetStart().x), mm(e.GetEnd().x)))
    y0, y1 = sorted((mm(e.GetStart().y), mm(e.GetEnd().y)))
    w, h = x1 - x0, y1 - y0

    def T(p):                       # board -> DXF: bottom-left origin, y up
        return (mm(p.x) - x0, y1 - mm(p.y))

    dxf = Dxf()
    dxf.rect("BOARD", 0, 0, w, h)

    holes, bodies = [], []
    for fp in sorted(board.GetFootprints(), key=lambda f: f.GetReference()):
        ref = fp.GetReference()
        if ref.startswith("MH"):
            pad = next(iter(fp.Pads()))
            c, dia = T(pad.GetPosition()), mm(pad.GetDrillSize().x)
            dxf.circle("HOLES", c, dia / 2)
            holes.append((ref, c, dia))
            continue
        pts = []
        for g in fp.GraphicalItems():
            if g.GetClass() != "PCB_SHAPE":
                continue
            if g.GetLayer() == pcbnew.F_Fab:
                pts += draw_shape(dxf, "FAB_DETAIL", g, T)
            elif g.GetLayer() == pcbnew.F_CrtYd:
                draw_shape(dxf, "COURTYARD", g, T)
        if not pts:
            raise RuntimeError(f"{ref} has no fabrication outline")
        bx0, bx1 = min(p[0] for p in pts), max(p[0] for p in pts)
        by0, by1 = min(p[1] for p in pts), max(p[1] for p in pts)
        top = mm(fp.GetPosition().y) < DIVIDER_Y
        dxf.rect("BODY_TOP" if top else "BODY_BOTTOM", bx0, by0, bx1, by1)
        dxf.text("REFS", ((bx0 + bx1) / 2, (by0 + by1) / 2), 1.2, ref)
        bodies.append((ref, top, bx0, by0, bx1, by1))

    OUT.mkdir(exist_ok=True)
    dxf.write(DXF)
    print(f"{DXF.name}: board {w:g} x {h:g} mm, {len(holes)} holes, "
          f"{sum(1 for b in bodies if b[1])} bodies above the divider, "
          f"{sum(1 for b in bodies if not b[1])} below.")
    for ref, c, dia in holes:
        print(f"  {ref}  {c[0]:7.2f} {c[1]:7.2f}  dia {dia:g}")
    for ref, top, bx0, by0, bx1, by1 in bodies:
        print(f"  {ref:4} {'top   ' if top else 'bottom'} x {bx0:7.2f}..{bx1:7.2f}  y {by0:7.2f}..{by1:7.2f}"
              f"   {bx1 - bx0:5.2f} x {by1 - by0:5.2f}")
    no_model = [fp.GetReference() for fp in board.GetFootprints()
                if not fp.GetReference().startswith("MH") and len(fp.Models()) == 0]
    return x0, y1, sorted(no_model)


def make_step(ox, oy, no_model):
    cli = next((p for p in KICAD_CLI if Path(p).is_file()), None)
    if cli is None:
        raise RuntimeError("kicad-cli not found - add its path to KICAD_CLI")
    r = subprocess.run(
        [cli, "pcb", "export", "step", "--force", "--subst-models", "--no-dnp",
         "--user-origin", f"{ox}x{oy}mm", "-o", str(STEP), str(BOARD)],
        capture_output=True, text=True)
    tail = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
    # a model the footprint names but KiCad does not ship is a line of its own
    unfound = sorted(ln.split(" for ")[-1].rstrip(".") for ln in tail if "Could not add 3D model" in ln)
    if r.returncode != 0 or not STEP.is_file():
        raise RuntimeError("STEP export failed:\n" + "\n".join(tail[-10:]))
    print(f"{STEP.name}: {STEP.stat().st_size / 1e6:.1f} MB.")
    if no_model:
        print(f"  ABSENT - footprint names no 3D model: {', '.join(no_model)}")
    if unfound:
        print(f"  ABSENT - KiCad ships no such model: {', '.join(unfound)}")


if __name__ == "__main__":
    ox, oy, no_model = make_dxf()
    make_step(ox, oy, no_model)
    sys.exit(0)
