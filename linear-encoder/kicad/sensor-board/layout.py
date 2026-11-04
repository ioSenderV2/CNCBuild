"""Placement and routing for the sensor puck.

Run with KiCad's bundled Python:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' layout.py          (layout + route + save)
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' layout.py dump     (placement only, print pads)

Owns the whole board: places every footprint, draws the 30 mm circular outline
and the tape-corridor marks, strips and regenerates all copper.

Geometry (board center C = (100,100); the tape runs along x):
  - The tape corridor is the 8 mm band |y-100| <= 4, bottom side: nothing there
    but the AS5311 (and flat copper). Its edges are drawn on B.SilkS.
  - U1 sits on the BOTTOM at exactly C: the footprint's origin is the Hall
    array center, so the array lands on the puck axis.
  - J1 stands on the TOP at C, signal pads east (x+9.15), floating shield
    flange west. The 4 mm screw holes are at (100, 100+/-11).
  - D1 (TVS) sits on the BOTTOM south of the corridor - at 1.1 mm tall it is
    no prouder than the AS5311 itself.
  - Passives and test pads on TOP: series Rs south, decoupling and R4 north.
  - U1 escapes run on B.Cu out of the corridor to vias; input lanes to the
    series Rs on B.Cu south; the A/B/MagDECn and +3V3 runs are F.Cu.

Checked like route.py: every segment and via against every pad and all
other-net copper before saving. kicad-cli DRC is the real gate.
"""

import sys

import pcbnew

BOARD = r"C:\github\CNCBuild\linear-encoder\kicad\sensor-board\sensor-board.kicad_pcb"

CX, CY = 100.0, 100.0
R_EDGE = 15.0
SIG_W = 0.25
CLEAR = 0.2
VIA_SIZE = 0.6
VIA_DRILL = 0.3

mm = pcbnew.FromMM


def to_mm(v):
    return pcbnew.ToMM(v)


# The jack body is 16.1 x 19.5 on a 30 mm disc: every top-side part lives in
# the thin crescents beyond its courtyard (|y-100| > 8.6). D1 rides the bottom.
PLACE = {
    # ref: (x, y, rot, back?)
    "U1":  (100.0, 100.0, 180, True),
    "J1":  (100.0, 100.0, 0, False),
    "D1":  (106.8, 107.3, 0, True),     # bottom, south of the corridor - 1.1mm tall, same budget as the chip
    "R1":  (100.0, 110.95, 0, False),   # A      (horizontal, pad1 west feed, pad2 east out)
    "R2":  (100.0, 112.45, 0, False),   # B
    "R3":  (100.0, 109.45, 0, False),   # MagDECn
    "R4":  (99.5, 90.3, 0, False),      # CSn tie (pad1 west = CSn)
    "C1":  (92.9, 90.3, 180, False),    # pad1 east = +3V3
    "C2":  (96.2, 90.3, 180, False),
    "TP1": (88.0, 94.9, 0, False),      # CLK - west sliver, clear of the jack courtyard
    "TP2": (87.9, 100.6, 0, False),     # DO
    "MH1": (104.5, 89.0, 0, False),     # 4mm screws into the printed tube, flanking the corridor
    "MH2": (94.0, 110.8, 0, False),
}


class Router:
    def __init__(self, board):
        self.board = board
        self.segs = []
        self.vias = []
        self.pads = []
        for fp in board.GetFootprints():
            ref = fp.GetReference()
            for pad in fp.Pads():
                pos = pad.GetPosition()
                bb = pad.GetBoundingBox()
                hw = to_mm(bb.GetWidth()) / 2.0
                hh = to_mm(bb.GetHeight()) / 2.0
                name = pad.GetNetname() if pad.GetNumber() else None
                self.pads.append((to_mm(pos.x), to_mm(pos.y), hw, hh, name, ref,
                                  pad.GetNumber()))

    def pad(self, ref, num):
        for (x, y, hw, hh, name, pref, pnum) in self.pads:
            if pref == ref and pnum == str(num):
                return (x, y)
        raise RuntimeError(f"pad {ref}.{num} not found")

    @staticmethod
    def _nearest_on_seg(px, py, x1, y1, x2, y2):
        dx, dy = x2 - x1, y2 - y1
        ll = dx * dx + dy * dy
        if ll == 0:
            return (x1, y1)
        t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / ll))
        return (x1 + t * dx, y1 + t * dy)

    @classmethod
    def _rect_seg_dist(cls, px, py, hw, hh, x1, y1, x2, y2):
        nx, ny = cls._nearest_on_seg(px, py, x1, y1, x2, y2)
        ddx = max(abs(nx - px) - hw, 0.0)
        ddy = max(abs(ny - py) - hh, 0.0)
        return (ddx * ddx + ddy * ddy) ** 0.5

    def seg(self, x1, y1, x2, y2, net, layer, width=SIG_W):
        if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
            return
        self.segs.append((x1, y1, x2, y2, width, layer, net))

    def path(self, pts, net, layer, width=SIG_W):
        for i in range(len(pts) - 1):
            self.seg(*pts[i], *pts[i + 1], net, layer, width)

    def via(self, x, y, net):
        self.vias.append((x, y, net))

    @staticmethod
    def _pt_seg_dist(px, py, x1, y1, x2, y2):
        dx, dy = x2 - x1, y2 - y1
        ll = dx * dx + dy * dy
        if ll == 0:
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
        t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / ll))
        cx, cy = x1 + t * dx, y1 + t * dy
        return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5

    @classmethod
    def _seg_seg_dist(cls, a, b):
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b

        def ccw(ax, ay, bx, by, cx, cy):
            return (cy - ay) * (bx - ax) - (by - ay) * (cx - ax)

        d1 = ccw(bx1, by1, bx2, by2, ax1, ay1)
        d2 = ccw(bx1, by1, bx2, by2, ax2, ay2)
        d3 = ccw(ax1, ay1, ax2, ay2, bx1, by1)
        d4 = ccw(ax1, ay1, ax2, ay2, bx2, by2)
        if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
            return 0.0
        return min(
            cls._pt_seg_dist(ax1, ay1, *b), cls._pt_seg_dist(ax2, ay2, *b),
            cls._pt_seg_dist(bx1, by1, *a), cls._pt_seg_dist(bx2, by2, *a))

    def check(self):
        problems = []
        pad_layers = {}
        for fp in self.board.GetFootprints():
            for pad in fp.Pads():
                layers = frozenset(l for l in (pcbnew.F_Cu, pcbnew.B_Cu) if pad.IsOnLayer(l))
                pad_layers[(fp.GetReference(), pad.GetNumber())] = layers
        for (x1, y1, x2, y2, w, layer, net) in self.segs:
            for (px, py, hw, hh, pname, ref, pnum) in self.pads:
                if pname == net and pname is not None:
                    continue
                pl = pad_layers.get((ref, pnum))
                if pl is not None and layer not in pl:
                    continue   # pad has no copper on this layer
                d = self._rect_seg_dist(px, py, hw, hh, x1, y1, x2, y2) - w / 2.0
                if d < CLEAR - 0.03:
                    problems.append(
                        f"seg {net} [{('F' if layer==pcbnew.F_Cu else 'B')}] "
                        f"({x1:.2f},{y1:.2f})-({x2:.2f},{y2:.2f}) vs pad {ref}.{pnum}/{pname} "
                        f"({px:.2f},{py:.2f}) gap {d:.3f}")
        for i in range(len(self.segs)):
            for j in range(i + 1, len(self.segs)):
                a, b = self.segs[i], self.segs[j]
                if a[6] == b[6] or a[5] != b[5]:
                    continue
                d = self._seg_seg_dist(a[:4], b[:4]) - a[4] / 2.0 - b[4] / 2.0
                if d < CLEAR - 0.03:
                    problems.append(
                        f"seg {a[6]} ({a[0]:.2f},{a[1]:.2f})-({a[2]:.2f},{a[3]:.2f}) vs "
                        f"seg {b[6]} ({b[0]:.2f},{b[1]:.2f})-({b[2]:.2f},{b[3]:.2f}) gap {d:.3f}")
        for (vx, vy, vnet) in self.vias:
            for (px, py, hw, hh, pname, ref, pnum) in self.pads:
                if pname == vnet and pname is not None:
                    continue
                ddx = max(abs(vx - px) - hw, 0.0)
                ddy = max(abs(vy - py) - hh, 0.0)
                d = (ddx * ddx + ddy * ddy) ** 0.5 - VIA_SIZE / 2.0
                if d < CLEAR - 0.03:
                    problems.append(f"via {vnet} ({vx:.2f},{vy:.2f}) vs pad {ref}.{pnum} gap {d:.3f}")
            for (x1, y1, x2, y2, w, layer, net) in self.segs:
                if net == vnet:
                    continue
                d = self._pt_seg_dist(vx, vy, x1, y1, x2, y2) - w / 2.0 - VIA_SIZE / 2.0
                if d < CLEAR - 0.03:
                    problems.append(f"via {vnet} ({vx:.2f},{vy:.2f}) vs seg {net} "
                                    f"({x1:.2f},{y1:.2f})-({x2:.2f},{y2:.2f}) gap {d:.3f}")
        for i in range(len(self.vias)):
            for j in range(i + 1, len(self.vias)):
                a, b = self.vias[i], self.vias[j]
                if a[2] == b[2]:
                    continue
                d = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 - VIA_SIZE
                if d < CLEAR - 0.03:
                    problems.append(f"via {a[2]} vs via {b[2]} gap {d:.3f}")
        # board edge: everything inside r 14.3
        for (x1, y1, x2, y2, w, layer, net) in self.segs:
            for (px, py) in ((x1, y1), (x2, y2)):
                rr = ((px - CX) ** 2 + (py - CY) ** 2) ** 0.5
                if rr > R_EDGE - 0.7:
                    problems.append(f"seg {net} endpoint ({px:.2f},{py:.2f}) r={rr:.2f} too close to edge")
        return problems

    def netcode(self, name):
        net = self.board.FindNet(name)
        if net is None:
            raise RuntimeError(f"net {name} not on board")
        return net.GetNetCode()

    def emit(self):
        for (x1, y1, x2, y2, w, layer, net) in self.segs:
            t = pcbnew.PCB_TRACK(self.board)
            t.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
            t.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
            t.SetWidth(mm(w))
            t.SetLayer(layer)
            t.SetNetCode(self.netcode(net))
            self.board.Add(t)
        for (x, y, net) in self.vias:
            v = pcbnew.PCB_VIA(self.board)
            v.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
            v.SetDrill(mm(VIA_DRILL))
            try:
                v.SetWidth(mm(VIA_SIZE))
            except TypeError:
                v.SetWidth(pcbnew.PADSTACK.ALL_LAYERS, mm(VIA_SIZE))
            v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
            v.SetNetCode(self.netcode(net))
            self.board.Add(v)


def strip_copper_and_graphics(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    out = []
    i = 0
    n = len(text)
    while i < n:
        hit = False
        for key in ("\t(segment", "\t(via", "\t(zone", "\t(gr_line", "\t(gr_circle",
                    "\t(gr_rect", "\t(gr_arc", "\t(gr_text"):
            if text.startswith(key, i):
                hit = True
                break
        if hit:
            depth = 0
            j = i
            while j < n:
                c = text[j]
                if c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            i = j + 1
            if i < n and text[i] == "\n":
                i += 1
            continue
        out.append(text[i])
        i += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("".join(out))


def place(board):
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref not in PLACE:
            continue
        (x, y, rot, back) = PLACE[ref]
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        if back and fp.GetLayer() != pcbnew.B_Cu:
            fp.Flip(pcbnew.VECTOR2I(mm(x), mm(y)), True)
        if not back and fp.GetLayer() != pcbnew.F_Cu:
            fp.Flip(pcbnew.VECTOR2I(mm(x), mm(y)), True)
        fp.SetOrientationDegrees(rot)
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref in ("J1", "D1"):
            # GND pads that sit where thermal spokes starve connect solid
            for pad in fp.Pads():
                if pad.GetNetname() == "GND":
                    try:
                        pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
                    except AttributeError:
                        pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
        if ref.startswith("MH"):
            # bare holes: shrink the ring to the drill so neither copper nor a
            # mask aperture reaches near the board edge, and keep the pour off
            for pad in fp.Pads():
                try:
                    pad.SetSize(pcbnew.VECTOR2I(mm(4.2), mm(4.2)))
                except TypeError:
                    pad.SetSize(pcbnew.PADSTACK.ALL_LAYERS, pcbnew.VECTOR2I(mm(4.2), mm(4.2)))
                pad.SetLocalClearance(mm(0.7))


def graphics(board):
    # circular outline
    c = pcbnew.PCB_SHAPE(board)
    c.SetShape(pcbnew.SHAPE_T_CIRCLE)
    c.SetCenter(pcbnew.VECTOR2I(mm(CX), mm(CY)))
    c.SetEnd(pcbnew.VECTOR2I(mm(CX + R_EDGE), mm(CY)))
    c.SetLayer(pcbnew.Edge_Cuts)
    c.SetWidth(mm(0.1))
    board.Add(c)
    # tape corridor marks on the bottom silk
    for dy in (-4.0, 4.0):
        half = (R_EDGE ** 2 - dy ** 2) ** 0.5 - 0.6
        ln = pcbnew.PCB_SHAPE(board)
        ln.SetShape(pcbnew.SHAPE_T_SEGMENT)
        ln.SetStart(pcbnew.VECTOR2I(mm(CX - half), mm(CY + dy)))
        ln.SetEnd(pcbnew.VECTOR2I(mm(CX + half), mm(CY + dy)))
        ln.SetLayer(pcbnew.B_SilkS)
        ln.SetWidth(mm(0.2))
        board.Add(ln)


def main():
    dump = len(sys.argv) > 1 and sys.argv[1] == "dump"
    strip_copper_and_graphics(BOARD)
    board = pcbnew.LoadBoard(BOARD)
    place(board)
    graphics(board)

    r = Router(board)
    if dump:
        for (x, y, rad, name, ref, num) in sorted(r.pads, key=lambda p: (p[4], p[5])):
            print(f"{ref}.{num:>2}  ({x:7.3f},{y:7.3f}) r={rad:.2f}  {name}")
        pcbnew.SaveBoard(BOARD, board)
        print("placed + outline only. Saved.")
        return

    F = pcbnew.F_Cu
    B = pcbnew.B_Cu

    # ---------------- bottom: U1 escapes west, vias outside the corridor ------
    # south row signals turn west under the chip's own quadrant, then drop on
    # F.Cu down the west flank to the series Rs in the south sliver
    r.path([(100.11, 103), (100.11, 104.5), (97.6, 104.5), (97.6, 104.7)], "B_SRC", B)
    r.via(97.6, 104.7, "B_SRC")
    r.path([(100.76, 103), (100.76, 105.0), (98.6, 105.0), (98.6, 105.3)], "A_SRC", B)
    r.via(98.6, 105.3, "A_SRC")
    r.path([(101.41, 103), (101.41, 105.7), (99.3, 105.7)], "MAGD_SRC", B)
    r.via(99.3, 105.7, "MAGD_SRC")


    r.path([(98.16, 103), (98.16, 103.95), (97.51, 103.95)], "GND", B)
    r.path([(97.51, 103), (97.51, 103.95)], "GND", B)
    r.path([(97.51, 103.95), (96.6, 103.95), (96.3, 104.9)], "GND", B)
    r.via(96.3, 104.9, "GND")

    r.path([(97.51, 97), (97.51, 96.1), (95.8, 96.1), (95.8, 96.35)], "DO", B)
    r.via(95.8, 96.35, "DO")
    # (TP3 / MagINCn deleted - the crescents have no room and the doc calls it optional)
    r.path([(98.16, 97), (98.16, 95.5)], "CLK", B)
    r.via(98.16, 95.5, "CLK")
    r.path([(98.81, 97), (98.81, 94.9)], "CSN", B)
    r.via(98.81, 94.9, "CSN")
    r.path([(102.06, 97), (102.06, 95.6), (101.41, 95.6)], "+3V3", B)
    r.path([(101.41, 97), (101.41, 95.0)], "+3V3", B)
    r.via(101.41, 95.0, "+3V3")

    # D1 taps (bottom). D1 pads: row1 y106.2: 1=A(105.85) 5=GND(106.8) 2=B(107.75);
    # row2 y108.4: 3=MagDECn(105.85) 4=+3V3(106.8) nc(107.75)
    r.via(105.85, 104.445, "A")        # on A's entry run, straight above D1.1
    r.path([(105.85, 104.445), (105.85, 106.2)], "A", B)
    # B taps from its own bottom-side east run (below); MagDECn taps from a via
    # on its output run; +3V3 dives from its north via and crosses the corridor
    # once as a flat trace down the chip's east flank
    r.via(103.5, 109.45, "MAGD")
    r.path([(103.5, 109.45), (105.85, 109.45), (105.85, 108.4)], "MAGD", B)
    r.path([(101.41, 95.0), (103.8, 95.0), (103.8, 107.3), (106.8, 107.3),
            (106.8, 107.75)], "+3V3", B)
    # D1's GND pin stitches straight up to the top pour; the bottom GND patch
    # connects through the pad itself
    r.path([(106.8, 106.2), (106.8, 105.1)], "GND", B)
    r.via(106.8, 105.1, "GND")
    r.via(100.0, 113.6, "GND")   # second stitch out on the open south rim

    # B's east journey runs on the bottom so the top pour stays in one piece;
    # the TVS channel taps straight off its diagonal
    r.via(101.9, 112.45, "B")
    r.path([(101.9, 112.45), (105.35, 112.45), (111.3, 106.5), (111.3, 105.65)], "B", B)
    r.path([(108.9, 108.9), (108.9, 106.2), (107.75, 106.2)], "B", B)
    r.via(111.3, 105.65, "B")

    # ---------------- top: west-flank feeds down to the series Rs -------------
    r.path([(97.6, 104.7), (97.8, 104.9), (97.8, 112.45), (99.225, 112.45)], "B_SRC", F)
    r.path([(98.6, 105.3), (98.35, 105.55), (98.35, 110.95), (99.225, 110.95)], "A_SRC", F)
    r.path([(99.3, 105.7), (99.3, 109.45)], "MAGD_SRC", F)   # lands on R3.1 from above

    # outputs east: MagDECn north across the corridor, A to J1.1, B around the rim
    r.path([(100.775, 109.45), (105.1, 109.45), (105.1, 105.2)], "MAGD", F)
    r.path([(105.1, 105.2), (104.9, 105.2)], "MAGD", F)
    r.path([(105.1, 105.2), (105.1, 96.825), (109.15, 96.825)], "MAGD", F)
    r.path([(100.775, 110.95), (105.8, 110.95), (105.8, 104.445),
            (109.15, 104.445)], "A", F)
    r.path([(100.775, 112.45), (101.9, 112.45)], "B", F)
    r.path([(111.3, 105.65), (111.3, 101.905), (109.3, 101.905)], "B", F)

    # DO / CLK to the test pads, both skirting the jack's west shield flange
    r.path([(95.8, 96.35), (95.8, 96.65), (87.9, 96.65), (87.9, 100.6)], "DO", F)
    r.path([(98.16, 95.5), (98.16, 94.3), (88.0, 94.3), (88.0, 94.9)], "CLK", F)
    # CSn to R4
    r.path([(98.81, 94.9), (98.81, 91.0), (98.725, 91.0), (98.725, 90.3)], "CSN", F)
    # +3V3: north over the parts to the decoupling pair, east run to J1.4 + tap
    r.path([(101.41, 95.0), (101.41, 89.2), (93.675, 89.2), (93.675, 90.3)], "+3V3", F)
    r.path([(96.975, 89.2), (96.975, 90.3)], "+3V3", F)
    r.path([(101.41, 95.0), (101.41, 94.8), (112.1, 94.8), (112.1, 100.635),
            (109.3, 100.635)], "+3V3", F)
    r.path([(112.1, 100.635), (112.1, 106.6)], "+3V3", F)

    # ---------------- GND pours: full top, small bottom patch under D1 --------
    # The corridor stays bare on the bottom; the south patch gives D1's GND pin
    # its copper and stitches to the top pour through one via.
    import math
    gnd = board.FindNet("GND").GetNetCode()

    def gnd_zone(layer, points):
        z = pcbnew.ZONE(board)
        z.SetLayer(layer)
        # SetLayer alone does not update a zone's layer SET in this build
        ls = pcbnew.LSET()
        ls.AddLayer(layer)
        z.SetLayerSet(ls)
        z.SetNetCode(gnd)
        chain = pcbnew.SHAPE_LINE_CHAIN()
        for (px, py) in points:
            chain.Append(mm(px), mm(py))
        chain.SetClosed(True)
        z.Outline().AddOutline(chain)
        try:
            z.SetLocalClearance(mm(0.25))
        except TypeError:
            pass
        z.SetMinThickness(mm(0.2))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(mm(0.35))
        z.SetThermalReliefSpokeWidth(mm(0.4))
        board.Add(z)

    gnd_zone(pcbnew.F_Cu,
             [(CX + 14.6 * math.cos(k * math.pi / 18), CY + 14.6 * math.sin(k * math.pi / 18))
              for k in range(36)])
    gnd_zone(pcbnew.B_Cu, [(99.5, 104.7), (110.6, 104.7), (110.6, 110.8),
                           (105.5, 113.9), (99.6, 113.9), (99.5, 110.5)])

    problems = r.check()
    if problems:
        print(f"{len(problems)} clearance problem(s); NOT saved:")
        for p in problems[:40]:
            print(" ", p)
        sys.exit(1)

    r.emit()
    pcbnew.SaveBoard(BOARD, board)
    print(f"puck routed: {len(r.segs)} segments, {len(r.vias)} vias, top GND pour "
          f"(unfilled - kicad-cli drc --refill-zones --save-board). Saved.")


if __name__ == "__main__":
    main()
