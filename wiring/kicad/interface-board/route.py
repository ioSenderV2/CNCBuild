"""Channel router for the interface board.

Run with KiCad's bundled Python:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' route.py

Owns ALL copper on this board (there is no hand routing): strips every track,
via and zone from the file, then regenerates:

  - every non-GND net as escape -> vertical drop -> horizontal lane -> entry,
    verticals on F.Cu, horizontal lanes on B.Cu, a via at each layer change;
  - GND as full-board pours on both layers (thermal relief on the pads).

Topology (board 200 x 94 at origin 5,5):
  - Five axis columns across the top: RJ45 (anchor y=16) with its limit 3P
    stacked below (y=31). The jack's four signals thread past the 3P in fixed
    channels per pin - see JACK_CHANNELS - meeting in a mini-corridor between
    jack and 3P at staggered heights chosen so no two jogs cross.
  - The rest of the inputs sit to the right in two brick-staggered rows and
    escape straight down (search jogs around pegs where needed).
  - Corridor B (y 40..64): horizontal lanes, interval-packed so short nets
    share a lane. +12V runs on its own lane below the block at y 66.5.
  - Teensy headers J40-J44 stand vertically at x 150..166: STEP/DIR leave on
    short stubs then rise to their lanes; EN drops to corridor C.
  - Bottom row: J17 ribbon far left, 12V + signal terminal blocks, then the
    Teensy headers and the J16 ribbon. Ribbon back rows (y 82.54) are served
    from corridor C (y 89.8..94) through crossing columns between the headers.

Every emitted segment and via is clearance-checked against every pad (NPTH pegs
included) and all other-net copper before the board is saved; a violation aborts
the save and prints the geometry. kicad-cli DRC remains the real gate.
"""

import sys

import pcbnew

BOARD = r"C:\github\CNCBuild\wiring\kicad\interface-board\interface-board.kicad_pcb"

SIG_W = 0.3
PWR_W = 0.6       # +12V lane tie and 12V terminal entries
CLEAR = 0.22
VIA_SIZE = 0.6
VIA_DRILL = 0.3

BAND_EXIT = 38.0          # y where the input band's escapes end
B_LANES = (40.0, 64.0, 0.675)
PWR_LANE_Y = 66.5
C_LANES = (89.8, 94.0, 0.7)
PACK_MARGIN = 3.0         # x separation between nets sharing a lane

# axis columns: jack ref -> (prox ref, column center x)
AXIS = {"J1": ("J6", 21.0), "J2": ("J7", 41.0), "J3": ("J8", 61.0),
        "J4": ("J9", 81.0), "J5": ("J10", 101.0)}
# jack pad -> (x offset from column center, jog y); a farther rightward channel
# jogs higher so no two jogs cross, levels 0.52 apart, and every channel clears
# the 3P pads and pegs below. Pin 1 first sidesteps the jack's own left peg.
JACK_CHANNELS = {"1": (-6.5, 22.5), "3": (1.9, 23.54), "5": (6.15, 23.02), "7": (9.9, 22.5)}
PIN1_SIDESTEP = 0.945

BAND_RIGHT = {"J11", "J12", "J13", "J14", "J15", "J30", "J31", "J32", "J33"}
DUPONT = {"J40", "J41", "J42", "J43", "J44"}
DUPONT_STUB = 1.9   # wide enough that the GND pads above keep two thermal spokes
ROW3_TB = {"J18", "J19", "J21", "J22", "J23", "J34", "J35", "J36", "J37"}
RIBBONS = {"J16", "J17"}

# crossing columns from corridor B down to corridor C: two beside J17 for the
# left-end alarms, the rest in the gaps between the Teensy headers and east of
# them; col_free() rejects any that an escape already descended in
C_COLS = [19.5, 20.3, 175.2, 176.1, 177.0, 177.9, 178.8, 179.7]

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
        self.reserved_x = []
        for fp in board.GetFootprints():
            ref = fp.GetReference()
            for pad in fp.Pads():
                pos = pad.GetPosition()
                name = pad.GetNetname() if pad.GetNumber() else None
                self.pads.append((to_mm(pos.x), to_mm(pos.y), pad_radius(pad), name, ref))
                if ref in (ROW3_TB | RIBBONS) and name not in (None, "GND"):
                    self.reserved_x.append(to_mm(pos.x))

    def seg(self, x1, y1, x2, y2, net, layer, width=SIG_W):
        if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
            return
        self.segs.append((x1, y1, x2, y2, width, layer, net))

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

    def _path_clear(self, pts, net, width):
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            for (px, py, pr, pname, ref) in self.pads:
                if pname == net and pname is not None:
                    continue
                if self._pt_seg_dist(px, py, x1, y1, x2, y2) - pr - width / 2.0 < CLEAR:
                    return False
            for (sx1, sy1, sx2, sy2, w, layer, sname) in self.segs:
                if sname == net or layer != pcbnew.F_Cu:
                    continue
                if self._seg_seg_dist((x1, y1, x2, y2), (sx1, sy1, sx2, sy2)) \
                        - width / 2.0 - w / 2.0 < CLEAR:
                    return False
            for (vx, vy, vname) in self.vias:
                if vname == net:
                    continue
                if self._pt_seg_dist(vx, vy, x1, y1, x2, y2) - VIA_SIZE / 2.0 - width / 2.0 < CLEAR:
                    return False
        # the terminal via of the path must clear other nets' copper too
        ex, ey = pts[-1]
        for (sx1, sy1, sx2, sy2, w, layer, sname) in self.segs:
            if sname == net or layer != pcbnew.F_Cu:
                continue
            if self._pt_seg_dist(ex, ey, sx1, sy1, sx2, sy2) - VIA_SIZE / 2.0 - w / 2.0 < CLEAR:
                return False
        for (px, py, pr, pname, ref) in self.pads:
            if pname == net and pname is not None:
                continue
            if ((ex - px) ** 2 + (ey - py) ** 2) ** 0.5 - pr - VIA_SIZE / 2.0 < CLEAR:
                return False
        return True

    def escape_down(self, x, y, exit_y, net, width):
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
                    problems.append(f"via {vnet} ({vx:.2f},{vy:.2f}) vs seg {net} "
                                    f"({x1:.2f},{y1:.2f})-({x2:.2f},{y2:.2f}) gap {d:.3f}")
        for i in range(len(self.vias)):
            for j in range(i + 1, len(self.vias)):
                a, b = self.vias[i], self.vias[j]
                if a[2] == b[2]:
                    continue
                d = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 - VIA_SIZE
                if d < CLEAR - 0.03:
                    problems.append(f"via {a[2]} ({a[0]:.2f},{a[1]:.2f}) vs via {b[2]} "
                                    f"({b[0]:.2f},{b[1]:.2f}) gap {d:.3f}")
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


class PackedLanes:
    """First-fit interval packing: nets whose x spans don't overlap share a lane."""

    def __init__(self, start, stop, pitch):
        self.start = start
        self.stop = stop
        self.pitch = pitch
        self.lanes = []   # list of interval lists

    def take(self, x_min, x_max):
        iv = (x_min - PACK_MARGIN, x_max + PACK_MARGIN)
        for i, occupied in enumerate(self.lanes):
            if all(iv[1] <= lo or iv[0] >= hi for (lo, hi) in occupied):
                occupied.append(iv)
                return round(self.start + i * self.pitch, 3)
        y = self.start + len(self.lanes) * self.pitch
        if y > self.stop + 1e-9:
            raise RuntimeError("corridor out of lanes")
        self.lanes.append([iv])
        return round(y, 3)


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


def strip_copper(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    out = []
    i = 0
    n = len(text)
    while i < n:
        hit = False
        for key in ("\t(segment", "\t(via", "\t(zone"):
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
    split = {}
    for fp in board.GetFootprints():
        if fp.GetReference() in RIBBONS:
            ys = [to_mm(p.GetPosition().y) for p in fp.Pads()]
            split[fp.GetReference()] = (min(ys) + max(ys)) / 2.0
    return split


def main():
    strip_copper(BOARD)
    board = pcbnew.LoadBoard(BOARD)

    r = Router(board)
    nets = collect_nets(board)
    split = row_split(board)

    # the Teensy headers' GND pins sit too tight for two thermal spokes
    # (pin 2 below, stub channels either side) - connect those solid instead
    for fp in board.GetFootprints():
        if fp.GetReference() in DUPONT:
            for pad in fp.Pads():
                if pad.GetNumber() == "1":
                    try:
                        pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
                    except AttributeError:
                        pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)

    b_lanes = PackedLanes(*B_LANES)
    c_lanes = Lanes(*C_LANES)

    c_free = sorted(C_COLS)
    c_used = []

    def col_free(cx):
        for (x1, y1, x2, y2, w, layer, net) in r.segs:
            if abs(x1 - x2) > 0.01 or layer != pcbnew.F_Cu:
                continue
            if max(y1, y2) < 39 or min(y1, y2) > 95:
                continue
            if abs(x1 - cx) < 0.3 + w / 2.0 + CLEAR:
                return False
        return True

    def c_cross_x(near_x):
        avail = [c for c in c_free if c not in c_used and col_free(c)]
        if not avail:
            raise RuntimeError("crossing columns exhausted")
        x = min(avail, key=lambda c: abs(c - near_x))
        c_used.append(x)
        return x

    # route +12V last so its dedicated lane ties after all sources exist;
    # otherwise alphabetical: deterministic
    names = sorted(n for n in nets if n != "+12V") + ["+12V"]

    back_jobs = {}   # net -> list of (x, y, kind) back-row pads; kind 'rib' or 'dup'
    net_lane = {}

    for name in names:
        pads = sorted(nets[name], key=lambda p: (p[2], p[3]))
        is_pwr = name == "+12V"
        width = SIG_W
        xs_span = [p[2] for p in pads]
        b_lane = PWR_LANE_Y if is_pwr else b_lanes.take(min(xs_span) - 15, max(xs_span) + 15)
        net_lane[name] = b_lane

        for (ref, num, x, y) in pads:
            if ref in AXIS:
                col = AXIS[ref][1]
                dx, jog_y = JACK_CHANNELS[num]
                cx = col + dx
                sx = x
                if num == "1":   # sidestep the jack's own left peg first
                    sx = x + PIN1_SIDESTEP
                    r.seg(x, y, sx, y + PIN1_SIDESTEP, name, pcbnew.F_Cu, width)
                    y = y + PIN1_SIDESTEP
                r.seg(sx, y, sx, jog_y, name, pcbnew.F_Cu, width)
                r.seg(sx, jog_y, cx, jog_y, name, pcbnew.F_Cu, width)
                r.seg(cx, jog_y, cx, b_lane, name, pcbnew.F_Cu, width)
                r.via(cx, b_lane, name)
            elif ref in {v[0] for v in AXIS.values()} or ref in BAND_RIGHT:
                # the whole run down to the lane is searched, so a jog also
                # dodges copper already standing in the corridor
                ex = r.escape_down(x, y, b_lane, name, width)
                r.via(ex, b_lane, name)
            elif ref in DUPONT:
                if num == "2":        # STEP: stub east, rise to lane
                    r.seg(x, y, x + DUPONT_STUB, y, name, pcbnew.F_Cu, width)
                    r.seg(x + DUPONT_STUB, y, x + DUPONT_STUB, b_lane, name, pcbnew.F_Cu, width)
                    r.via(x + DUPONT_STUB, b_lane, name)
                elif num == "3":      # DIR: stub west, rise to lane
                    r.seg(x, y, x - DUPONT_STUB, y, name, pcbnew.F_Cu, width)
                    r.seg(x - DUPONT_STUB, y, x - DUPONT_STUB, b_lane, name, pcbnew.F_Cu, width)
                    r.via(x - DUPONT_STUB, b_lane, name)
                elif num == "4":      # EN: drops to corridor C with the ribbon back row
                    back_jobs.setdefault(name, []).append((x, y, "dup"))
            elif ref in RIBBONS:
                if y > split[ref]:
                    back_jobs.setdefault(name, []).append((x, y, "rib"))
                else:
                    r.via(x, b_lane, name)
                    r.seg(x, b_lane, x, y, name, pcbnew.F_Cu, width)
            elif ref in ROW3_TB:
                w2 = PWR_W if is_pwr else width
                r.via(x, b_lane, name)
                r.seg(x, b_lane, x, y, name, pcbnew.F_Cu, w2)
            else:
                raise RuntimeError(f"no routing rule for {ref}")

    # corridor C: one lane and one B->C crossing per net with back-row pads
    for name, jobs in back_jobs.items():
        b_lane = net_lane[name]
        cl = c_lanes.take()
        gx = c_cross_x(sum(j[0] for j in jobs) / len(jobs))
        r.via(gx, b_lane, name)
        r.seg(gx, b_lane, gx, cl, name, pcbnew.F_Cu, SIG_W)
        r.via(gx, cl, name)
        for (x, y, kind) in jobs:
            r.via(x, cl, name)
            r.seg(x, cl, x, y, name, pcbnew.F_Cu, SIG_W)
        xs = [gx] + [j[0] for j in jobs]
        r.seg(min(xs), cl, max(xs), cl, name, pcbnew.B_Cu, SIG_W)

    # lane ties, after every via that must sit on a lane exists
    for name, b_lane in net_lane.items():
        xs = [v[0] for v in r.vias if v[2] == name and abs(v[1] - b_lane) < 1e-6]
        if len(xs) >= 2:
            r.seg(min(xs), b_lane, max(xs), b_lane, name, pcbnew.B_Cu,
                  PWR_W if name == "+12V" else SIG_W)

    # GND pours, both layers
    gnd = board.FindNet("GND").GetNetCode()
    for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
        z = pcbnew.ZONE(board)
        z.SetLayer(layer)
        z.SetNetCode(gnd)
        chain = pcbnew.SHAPE_LINE_CHAIN()
        for (px, py) in ((5, 5), (215, 5), (215, 99), (5, 99)):
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
    lanes_used = len(b_lanes.lanes)
    print(f"routed {len(nets)} nets on {lanes_used} packed lanes: {len(r.segs)} segments, "
          f"{len(r.vias)} vias, 2 GND pours (unfilled - kicad-cli drc --refill-zones --save-board). Saved.")


if __name__ == "__main__":
    main()
