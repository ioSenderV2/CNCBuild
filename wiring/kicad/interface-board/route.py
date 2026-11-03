"""Channel router for the interface board.

Run with KiCad's bundled Python:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' route.py

Owns ALL copper on this board (there is no hand routing): deletes every track,
via and zone, then regenerates:

  - every non-GND net as escape -> vertical drop -> horizontal lane -> entry,
    verticals on F.Cu, horizontal lanes on B.Cu, a via at each layer change;
  - GND as full-board pours on both layers (thermal relief on the pads).

Corridors (board 220 x 95 at origin 5,5; connector rows at y = 22 / 52 / ~83):
  A: y 33..45      lanes for row-1 columns whose straight drop is blocked by row 2
                   (J1, J6, J2, J7); they travel east to a staging highway at the
                   right board edge and descend there
  B: y 59.6..79.2  one lane per net, the main east-west channel
  C: y 90.9..98.6  lanes serving the back pad row (y=85) of the ribbon headers,
                   reached through crossing columns in the two gaps east of each

Every emitted segment and via is clearance-checked against every pad (NPTH pegs
included) and all other-net copper before the board is saved; a violation aborts
the save and prints the geometry. kicad-cli DRC remains the real gate.
"""

import sys

import pcbnew

BOARD = r"C:\github\CNCBuild\wiring\kicad\interface-board\interface-board.kicad_pcb"

SIG_W = 0.3       # signal track width, mm
PWR_W = 0.6       # +12V track width
CLEAR = 0.22      # gap demanded between copper of different nets (DRC default is 0.2)
VIA_SIZE = 0.6
VIA_DRILL = 0.3

A_LANES = (33.2, 45.0, 0.8)
B_LANES = (59.6, 79.2, 0.675)
C_LANES = (90.9, 98.6, 0.7)

STAGE_X_START = 212.4   # right-edge highway where corridor-A nets descend
STAGE_PITCH = 0.7

PWR_LANE_Y = 80.1       # +12V gets its own lane below the block - it is wider

# candidate crossing columns from corridor B down to corridor C, in the pad-free
# gaps east of J16 and J17; each is checked against already-routed verticals
C_COLS = [99.7, 100.4, 101.1, 102.4, 104.35, 105.0, 106.9, 107.6, 109.4,
          119.3, 120.3, 123.3, 124.3, 127.6, 128.6, 130.0, 131.0]

LEFT_REFS = {"J1", "J6", "J2", "J7"}   # row-1 parts whose drop is blocked by row 2
ROW3_REFS = {"J16", "J17", "J18", "J19", "J21", "J22", "J23"}

mm = pcbnew.FromMM


def to_mm(v):
    return pcbnew.ToMM(v)


def pad_radius(pad):
    try:
        sz = pad.GetSize()
    except TypeError:
        sz = pad.GetSize(pcbnew.PADSTACK.ALL_LAYERS)
    return max(to_mm(sz.x), to_mm(sz.y)) / 2.0


class Router:
    def __init__(self, board):
        self.board = board
        self.segs = []      # (x1, y1, x2, y2, width, layer, netname)
        self.vias = []      # (x, y, netname)
        self.pads = []      # (x, y, radius, netname or None for NPTH, ref)
        self.reserved_x = []   # columns the row-3 pad entries will descend in
        for fp in board.GetFootprints():
            ref = fp.GetReference()
            for pad in fp.Pads():
                pos = pad.GetPosition()
                name = pad.GetNetname() if pad.GetNumber() else None
                self.pads.append((to_mm(pos.x), to_mm(pos.y), pad_radius(pad), name, ref))
                if ref in ROW3_REFS and name not in (None, "GND"):
                    self.reserved_x.append(to_mm(pos.x))

    def seg(self, x1, y1, x2, y2, net, layer, width=SIG_W):
        if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
            return
        self.segs.append((x1, y1, x2, y2, width, layer, net))

    def via(self, x, y, net):
        self.vias.append((x, y, net))

    # ---- geometry helpers ----
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

    def _path_clear(self, pts, net, width):
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            for (px, py, pr, pname, ref) in self.pads:
                if pname == net and pname is not None:
                    continue
                if self._pt_seg_dist(px, py, x1, y1, x2, y2) - pr - width / 2.0 < CLEAR:
                    return False
        return True

    def escape_down(self, x, y, exit_y, net, width):
        """Leave a pad field downward, the whole run to exit_y checked against
        every pad; jogs sideways 45 deg first when the straight drop is blocked.
        Emits the copper, returns the x it descends on."""
        for dx in (0.0, 1.1, -1.1, 2.1, -2.1, 2.8, -2.8, 3.6, -3.6):
            xc = x + dx
            if any(abs(xc - rx) < 0.55 for rx in self.reserved_x):
                continue
            jog_y = y + abs(dx)
            pts = [(x, y)] + ([(xc, jog_y)] if dx else []) + [(xc, exit_y)]
            if self._path_clear(pts, net, width):
                for i in range(len(pts) - 1):
                    self.seg(*pts[i], *pts[i + 1], net, pcbnew.F_Cu, width)
                return xc
        raise RuntimeError(f"no escape from ({x:.2f},{y:.2f}) net {net}")

    # ---- final check ----
    def check(self):
        problems = []
        for (x1, y1, x2, y2, w, layer, net) in self.segs:
            for (px, py, pr, pname, ref) in self.pads:
                if pname == net and pname is not None:
                    continue
                d = self._pt_seg_dist(px, py, x1, y1, x2, y2) - pr - w / 2.0
                if d < CLEAR - 0.03:
                    problems.append(
                        f"seg {net} ({x1:.2f},{y1:.2f})-({x2:.2f},{y2:.2f}) vs pad {ref}/{pname} "
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
            for (px, py, pr, pname, ref) in self.pads:
                if pname == vnet and pname is not None:
                    continue
                d = ((vx - px) ** 2 + (vy - py) ** 2) ** 0.5 - pr - VIA_SIZE / 2.0
                if d < CLEAR - 0.03:
                    problems.append(f"via {vnet} ({vx:.2f},{vy:.2f}) vs pad {ref}/{pname} gap {d:.3f}")
            for (x1, y1, x2, y2, w, layer, net) in self.segs:
                if net == vnet:
                    continue
                d = self._pt_seg_dist(vx, vy, x1, y1, x2, y2) - w / 2.0 - VIA_SIZE / 2.0
                if d < CLEAR - 0.03:
                    problems.append(f"via {vnet} ({vx:.2f},{vy:.2f}) vs seg {net} gap {d:.3f}")
        for i in range(len(self.vias)):
            for j in range(i + 1, len(self.vias)):
                a, b = self.vias[i], self.vias[j]
                if a[2] == b[2]:
                    continue
                d = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 - VIA_SIZE
                if d < CLEAR - 0.03:
                    problems.append(f"via {a[2]} ({a[0]:.2f},{a[1]:.2f}) vs via {b[2]} ({b[0]:.2f},{b[1]:.2f}) gap {d:.3f}")
        return problems

    # ---- emit ----
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


class Lanes:
    def __init__(self, start, stop, pitch):
        self.next = start
        self.stop = stop
        self.pitch = pitch

    def take(self):
        y = self.next
        if y > self.stop + 1e-9:
            raise RuntimeError("corridor out of lanes")
        self.next = round(self.next + self.pitch, 3)
        return y


def collect_nets(board):
    nets = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        for pad in fp.Pads():
            if not pad.GetNumber():
                continue
            name = pad.GetNetname()
            if not name or name == "GND":
                continue
            p = pad.GetPosition()
            nets.setdefault(name, []).append((ref, pad.GetNumber(), to_mm(p.x), to_mm(p.y)))
    return nets


def row_split(board):
    """For J16/J17: midpoint y separating the lane-facing pad row from the back row."""
    split = {}
    for fp in board.GetFootprints():
        if fp.GetReference() in ("J16", "J17"):
            ys = [to_mm(p.GetPosition().y) for p in fp.Pads()]
            split[fp.GetReference()] = (min(ys) + max(ys)) / 2.0
    return split


def strip_copper(path):
    """Delete all top-level (segment/(via/(zone blocks from the board file -
    done at text level because board.Remove over SWIG segfaults on teardown."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    out = []
    i = 0
    n = len(text)
    while i < n:
        is_item = False
        for key in ("\t(segment", "\t(via", "\t(zone"):
            if text.startswith(key, i):
                is_item = True
                break
        if is_item:
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


def main():
    strip_copper(BOARD)
    board = pcbnew.LoadBoard(BOARD)

    r = Router(board)
    nets = collect_nets(board)
    split = row_split(board)

    a_lanes = Lanes(*A_LANES)
    b_lanes = Lanes(*B_LANES)
    c_lanes = Lanes(*C_LANES)

    stage = [STAGE_X_START]

    def next_stage():
        x = stage[0]
        stage[0] = round(x + STAGE_PITCH, 3)
        return x

    c_cols = sorted(C_COLS)
    c_used = []

    def col_free(cx):
        """No already-routed vertical copper within reach in the B->C span."""
        for (x1, y1, x2, y2, w, layer, net) in r.segs:
            if abs(x1 - x2) > 0.01:
                continue
            if max(y1, y2) < 56 or min(y1, y2) > 99:
                continue
            if abs(x1 - cx) < 0.3 + w / 2.0 + CLEAR:
                return False
        return True

    def c_cross_x(near_x):
        free = [c for c in c_cols if c not in c_used and col_free(c)]
        if not free:
            raise RuntimeError("crossing columns exhausted")
        x = min(free, key=lambda c: abs(c - near_x))
        c_used.append(x)
        return x

    back_jobs = []   # (netname, b_lane, x, y, width) - routed after all escapes exist
    net_lane = {}    # net -> its B lane, for the tie pass at the end

    for name in sorted(nets):
        pads = sorted(nets[name], key=lambda p: (p[2], p[3]))
        is_pwr = name == "+12V"
        width = SIG_W
        b_lane = PWR_LANE_Y if is_pwr else b_lanes.take()
        net_lane[name] = b_lane

        for (ref, num, x, y) in pads:
            if ref in ROW3_REFS:
                if ref in split and y > split[ref]:
                    back_jobs.append((name, b_lane, x, y, width))
                else:
                    r.via(x, b_lane, name)
                    r.seg(x, b_lane, x, y, name, pcbnew.F_Cu,
                          PWR_W if is_pwr else width)
                continue
            if ref in LEFT_REFS:
                al = a_lanes.take()
                ex = r.escape_down(x, y, al, name, width)
                sx = next_stage()
                r.via(ex, al, name)
                r.seg(ex, al, sx, al, name, pcbnew.B_Cu, width)
                r.via(sx, al, name)
                r.seg(sx, al, sx, b_lane, name, pcbnew.F_Cu, width)
                r.via(sx, b_lane, name)
            else:
                ex = r.escape_down(x, y, b_lane, name, width)
                r.via(ex, b_lane, name)

    # back pad rows next, so crossing columns can dodge every routed vertical
    for (name, b_lane, x, y, width) in back_jobs:
        gx = c_cross_x(x)
        cl = c_lanes.take()
        r.via(gx, b_lane, name)
        r.seg(gx, b_lane, gx, cl, name, pcbnew.F_Cu, width)
        r.via(gx, cl, name)
        r.seg(gx, cl, x, cl, name, pcbnew.B_Cu, width)
        r.via(x, cl, name)
        r.seg(x, cl, x, y, name, pcbnew.F_Cu, width)

    # lane ties last, when every via that must sit on a lane exists
    for name, b_lane in net_lane.items():
        xs = [v[0] for v in r.vias if v[2] == name and abs(v[1] - b_lane) < 1e-6]
        if len(xs) >= 2:
            r.seg(min(xs), b_lane, max(xs), b_lane, name, pcbnew.B_Cu,
                  PWR_W if name == "+12V" else SIG_W)

    # ---------- GND pours, both layers ----------
    gnd = board.FindNet("GND").GetNetCode()
    for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
        z = pcbnew.ZONE(board)
        z.SetLayer(layer)
        z.SetNetCode(gnd)
        chain = pcbnew.SHAPE_LINE_CHAIN()
        for (px, py) in ((5, 5), (225, 5), (225, 100), (5, 100)):
            chain.Append(mm(px), mm(py))
        chain.SetClosed(True)
        z.Outline().AddOutline(chain)
        try:
            z.SetLocalClearance(mm(0.3))
        except TypeError:
            pass
        z.SetMinThickness(mm(0.25))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(mm(0.4))
        z.SetThermalReliefSpokeWidth(mm(0.5))
        board.Add(z)

    problems = r.check()
    if problems:
        print(f"{len(problems)} clearance problem(s); NOT saved:")
        for p in problems[:40]:
            print(" ", p)
        sys.exit(1)

    r.emit()
    pcbnew.SaveBoard(BOARD, board)
    print(f"routed {len(nets)} nets: {len(r.segs)} segments, {len(r.vias)} vias, "
          f"2 GND pours (unfilled - run kicad-cli pcb drc --refill-zones --save-board). Saved.")


if __name__ == "__main__":
    main()
