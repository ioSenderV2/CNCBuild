"""Channel router for the interface board - Rev B, 4 layers.

Run with KiCad's bundled Python:
  & 'C:\\Program Files\\KiCad\\10.0\\bin\\python.exe' route.py

Owns ALL copper on this board (there is no hand routing): strips every track,
via and zone from the file, then regenerates:

  - F.Cu: vertical escapes and short jogs only;
  - In1.Cu: solid GND plane (every GND pad is through-hole, so GND needs no
    routing at all - thermal relief on the plane);
  - In2.Cu: solid +12V plane (same trick: the seven Mini-Fit pin 1s and both
    5.08 blocks' pin 1s tap it directly);
  - B.Cu: horizontal lanes, interval-packed, in three corridors.

Topology (board 105 x 104 at origin 5,5), top to bottom:
  - Five axis columns: RJ45 (y=16, 18 mm pitch) over its limit 3P (y=31).
    The jack's four signals thread past the 3P in the fixed JACK_CHANNELS,
    exactly as Rev A.
  - Corridor R (y 37.4..47.0): STEP / DIR / AL lanes. The jack verticals drop
    STRAIGHT into it - they cross no other connector row, which is the whole
    point of this row order (Rev A's misc-under-the-jacks arrangement was
    proven unroutable: 25 fixed verticals cannot pierce two Mini-Fit rows).
  - Row A (y 47.8..59.0): alarm + stepper ribbons, Teensy headers, 12 V blocks.
  - Corridor S (y 59.6..66.4): EN lanes (header pin 4 and the ribbon back row
    are served from below) and the LIM westward shift.
  - Misc rows 3 and 4 (y 67..92.5): probe, door, spindle, control, touch
    probes, mist, flood, UART - "down and left, underneath the stepper jacks".
  - Corridor S2 (y 92.9..99.8): every terminal-block net; misc pads drop in
    from above, TB pads rise from below.
  - Row B (y 100.3..108.3): the signal TBs on the bottom edge, wires south.

Only the five LIM nets cross connector rows at all: row A on searched columns,
then misc rows 3+4 through the far-left street (x ~6..9) after a westward
lane in corridor S, then corridor S2 east to the LIMITS block.

A vertical crosses a connector row at a column found by search: full-row
clear of pads and pegs, 0.70 mm from every other claimed column (0.70 covers
track-past-via), jogging in the corridor above the row when its x is blocked.
Dest-side via columns are pre-claimed so later crossers keep that distance.

Every emitted segment and via is clearance-checked against every pad (NPTH
pegs included) and all other-net copper before the board is saved; a violation
aborts the save and prints the geometry. kicad-cli DRC remains the real gate.
"""

import sys

import pcbnew

BOARD = r"C:\github\CNCBuild\wiring\kicad\interface-board\interface-board.kicad_pcb"

SIG_W = 0.3
CLEAR = 0.22
CLEAR_RUN = 0.205         # runtime search tolerance: candidates sit at exact
                          # boundaries and float noise must not reject them;
                          # the final check() and kicad-cli DRC stay the gates
VIA_SIZE = 0.6
VIA_DRILL = 0.3
COL_SEP = 0.70            # column-to-column: track past a via on an adjacent lane

R_LANES = (37.45, 46.95, 0.675)    # STEP / DIR / AL
S_LANES = (59.60, 66.35, 0.675)    # EN + LIM westward shift
S2_LANES = (92.95, 99.75, 0.675)   # every TB net + LIM eastward return
PACK_MARGIN = 3.0

X_MIN, X_MAX = 5.65, 111.35

# jack ref -> (prox 3P ref, column center x); channels as Rev A
AXIS = {"J1": ("J6", 21.0), "J2": ("J7", 39.0), "J3": ("J8", 57.0),
        "J4": ("J9", 75.0), "J5": ("J10", 93.0)}
JACK_CHANNELS = {"1": (-6.5, 22.5), "3": (1.9, 23.54), "5": (6.15, 23.02), "7": (9.9, 22.5)}
PIN1_SIDESTEP = 0.945

# Teensy headers: ref -> x; pad y from placement. Split 2+3 around the EN/LIM
# crossing windows - a contiguous header train walls those nets out of row A -
# and placed so hx+1.22 / hx-2.28 clear every jack-channel column by >= 0.67.
HDR = {"J40": 27.9, "J41": 32.4, "J42": 74.4, "J43": 80.7, "J44": 86.2}
HDR_STEP_DX = 1.22        # drop column east of the header, jog west into pad 2
HDR_DIR_DX = -2.28        # drop column west, jog east into pad 3
HDR_Y = {"1": 49.55, "2": 52.09, "3": 54.63, "4": 57.17}

RIBBON_N_Y = 51.45        # ribbon front row (served from corridor R above)
RIBBON_S_Y = 53.99        # ribbon back row (EN rises from corridor S below;
                          # J17's AL_Z / AL_B thread from R between front pads)
THREAD_JOG_Y = 52.72      # between the two ribbon pad rows
TB_Y = 104.22             # row B terminal block pads

LIM_STREET = [6.2, 6.9, 7.6, 8.3, 9.0]   # far-left columns through both misc rows

# obstacle rows a vertical must cross on one clear column
# (name, y0, y1, jog band above it on F.Cu, or None = must pass as-is)
BAND_DEFS = [
    ("ROW2", 24.0, 36.8, None),
    ("ROWA", 47.75, 59.05, (37.55, 46.80)),
    ("MISC34", 67.0, 92.5, (59.70, 66.25)),
    ("MISC4", 80.4, 92.5, (79.90, 81.00)),   # jog strip: below the row-3 pegs
                                             # (y<=79.7), above the row-4 pads

]

mm = pcbnew.FromMM


def to_mm(v):
    return pcbnew.ToMM(v)


def frange(a, b, step):
    out = []
    x = a
    while x <= b + 1e-9:
        out.append(round(x, 3))
        x += step
    return out


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
        for fp in board.GetFootprints():
            ref = fp.GetReference()
            for pad in fp.Pads():
                pos = pad.GetPosition()
                name = pad.GetNetname() if pad.GetNumber() else None
                pr = pad_radius(pad)
                if name is None:
                    pr += 0.06   # NPTH: hole-clearance rule is 0.25, not CLEAR
                self.pads.append((to_mm(pos.x), to_mm(pos.y), pr, name, ref))

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

    def path_blocker(self, pts, net, width, layer):
        """First thing that blocks this path, as text - or None if clear."""
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            for (px, py, pr, pname, ref) in self.pads:
                if pname == net and pname is not None:
                    continue
                if self._pt_seg_dist(px, py, x1, y1, x2, y2) - pr - width / 2.0 < CLEAR_RUN:
                    return f"pad {ref}/{pname} ({px:.2f},{py:.2f})"
            for (sx1, sy1, sx2, sy2, w, slayer, sname) in self.segs:
                if sname == net or slayer != layer:
                    continue
                if self._seg_seg_dist((x1, y1, x2, y2), (sx1, sy1, sx2, sy2)) \
                        - width / 2.0 - w / 2.0 < CLEAR_RUN:
                    return f"seg {sname} ({sx1:.2f},{sy1:.2f})-({sx2:.2f},{sy2:.2f})"
            for (vx, vy, vname) in self.vias:
                if vname == net:
                    continue
                if self._pt_seg_dist(vx, vy, x1, y1, x2, y2) - VIA_SIZE / 2.0 - width / 2.0 < CLEAR_RUN:
                    return f"via {vname} ({vx:.2f},{vy:.2f})"
        return None

    def path_clear(self, pts, net, width, layer):
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            for (px, py, pr, pname, ref) in self.pads:
                if pname == net and pname is not None:
                    continue
                if self._pt_seg_dist(px, py, x1, y1, x2, y2) - pr - width / 2.0 < CLEAR_RUN:
                    return False
            for (sx1, sy1, sx2, sy2, w, slayer, sname) in self.segs:
                if sname == net or slayer != layer:
                    continue
                if self._seg_seg_dist((x1, y1, x2, y2), (sx1, sy1, sx2, sy2)) \
                        - width / 2.0 - w / 2.0 < CLEAR_RUN:
                    return False
            for (vx, vy, vname) in self.vias:
                if vname == net:
                    continue
                if self._pt_seg_dist(vx, vy, x1, y1, x2, y2) - VIA_SIZE / 2.0 - width / 2.0 < CLEAR_RUN:
                    return False
        return True

    def via_clear(self, x, y, net):
        for (sx1, sy1, sx2, sy2, w, slayer, sname) in self.segs:
            if sname == net:
                continue
            if self._pt_seg_dist(x, y, sx1, sy1, sx2, sy2) - VIA_SIZE / 2.0 - w / 2.0 < CLEAR_RUN:
                return False
        for (px, py, pr, pname, ref) in self.pads:
            if pname == net and pname is not None:
                continue
            if ((x - px) ** 2 + (y - py) ** 2) ** 0.5 - pr - VIA_SIZE / 2.0 < CLEAR_RUN:
                return False
        for (vx, vy, vname) in self.vias:
            if vname == net:
                continue
            if ((x - vx) ** 2 + (y - vy) ** 2) ** 0.5 - VIA_SIZE < CLEAR_RUN:
                return False
        return True

    def emit_pts(self, pts, net, layer, width=SIG_W):
        for i in range(len(pts) - 1):
            self.seg(*pts[i], *pts[i + 1], net, layer, width)

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


class Band:
    """One connector row. A vertical crosses it on a column clear of every pad
    and peg for the full row height, COL_SEP from every other claimed column."""

    def __init__(self, name, y0, y1, jog):
        self.name = name
        self.y0 = y0
        self.y1 = y1
        self.jog = jog
        self.blocked = []
        self.cols = []

    def build(self, pads):
        raw = sorted((px - pr, px + pr) for (px, py, pr, pname, ref) in pads
                     if py + pr > self.y0 and py - pr < self.y1)
        merged = []
        for lo, hi in raw:
            if merged and lo <= merged[-1][1] + 0.74:
                merged[-1][1] = max(merged[-1][1], hi)
            else:
                merged.append([lo, hi])
        self.blocked = [(lo, hi) for lo, hi in merged]

    def ok(self, x):
        if not (X_MIN <= x <= X_MAX):
            return False
        for (lo, hi) in self.blocked:
            if lo - 0.365 < x < hi + 0.365:
                return False
        for c in self.cols:
            if abs(x - c) < COL_SEP - 0.005:
                return False
        return True

    def candidates(self, x, limit=8, prefer=None):
        if prefer is None:
            prefer = x
        cand = set()
        for (lo, hi) in self.blocked:
            cand.add(round(lo - 0.38, 3))
            cand.add(round(hi + 0.38, 3))
        for c in self.cols:
            cand.add(round(c - COL_SEP, 3))
            cand.add(round(c + COL_SEP, 3))
        valid = sorted((c for c in cand if self.ok(c) and abs(c - x) < 16.0),
                       key=lambda c: abs(c - prefer))
        out = [x] if self.ok(x) else []
        return out + [c for c in valid if abs(c - x) > 1e-6][:limit]

    def claim(self, x):
        self.cols.append(x)

    def col_ok(self, x):
        return all(abs(x - c) >= COL_SEP - 0.005 for c in self.cols)

    def crossed_by(self, y_from, y_to):
        return y_from <= self.y0 and y_to >= self.y1


def route_down(r, bands, x, y, stop_y, net, width=SIG_W, prefer=None):
    """Vertical from (x, y) down to (xf, stop_y) on F.Cu, jogging above any
    band that blocks the current column. Claims every band column it uses.
    `prefer` biases the candidate order (e.g. LIM pulls west, toward its
    street, so it does not steal the one window its column's EN net needs).
    Returns the point list, or None."""
    crossing = [b for b in bands if b.crossed_by(y, stop_y)]

    def attempt(pts, cx, idx):
        if idx == len(crossing):
            tail = pts + [(cx, stop_y)]
            if r.path_clear(tail[-2:], net, width, pcbnew.F_Cu):
                return tail
            return None
        b = crossing[idx]
        for xc in b.candidates(cx, prefer=prefer):
            if abs(xc - cx) < 1e-6:
                res = attempt(pts, cx, idx + 1)
                if res:
                    b.claim(cx)
                    return res
            else:
                if b.jog is None:
                    continue
                for jy in reversed(frange(*b.jog, 0.52)):
                    if jy <= pts[-1][1] + 0.2:
                        continue
                    hop = [pts[-1], (cx, jy), (xc, jy)]
                    if not r.path_clear(hop, net, width, pcbnew.F_Cu):
                        continue
                    res = attempt(pts + [(cx, jy), (xc, jy)], xc, idx + 1)
                    if res:
                        b.claim(xc)
                        return res
        return None

    res = attempt([(x, y)], x, 0)
    if res is None:
        print(f"-- route_down failed: net {net} from ({x:.2f},{y:.2f}) to {stop_y}")
        for b in crossing:
            print(f"   {b.name} candidates: {b.candidates(x)}")
            for xc in b.candidates(x)[:4]:
                if abs(xc - x) < 1e-6:
                    blk = r.path_blocker([(x, y), (x, stop_y)], net, width, pcbnew.F_Cu)
                    print(f"     straight {xc}: {blk}")
                elif b.jog:
                    for jy in frange(*b.jog, 0.45):
                        blk = r.path_blocker([(x, y), (x, jy), (xc, jy)], net,
                                             width, pcbnew.F_Cu)
                        tblk = r.path_blocker([(xc, jy), (xc, stop_y)], net,
                                              width, pcbnew.F_Cu)
                        print(f"     xc {xc} jy {jy}: hop {blk} / tail {tblk}")
    return res


def descend_from_pad(r, bands, x, y, stop_y, net, below_block):
    """Leave a pad (diagonal sidestep if its own footprint blocks the straight
    drop) and descend to stop_y, retrying other sidesteps when the descent
    cannot clear the rows below. A source INSIDE a band still respects and
    claims that band's columns. Returns the full point list."""
    if below_block:
        dxs = (2.1, -2.1, 2.8, -2.8, 3.4, -3.4, 4.2, -4.2, 4.9, -4.9,
               5.6, -5.6, 6.3, -6.3)
    else:
        dxs = (0.0, 1.1, -1.1, 2.1, -2.1, 2.8, -2.8, 3.4, -3.4)
    inside = [b for b in bands if b.y0 < y < b.y1]
    for dx in dxs:
        if dx == 0.0:
            nx, ny, pre = x, y, [(x, y)]
        else:
            nx, ny = x + dx, y + abs(dx)
            pre = [(x, y), (nx, ny)]
            if not r.path_clear(pre, net, SIG_W, pcbnew.F_Cu):
                continue
        if any(not b.col_ok(nx) for b in inside):
            continue
        pts = route_down(r, bands, nx, ny, stop_y, net)
        if pts:
            for b in inside:
                b.claim(pts[-1][0])
            return pre[:-1] + pts
    raise RuntimeError(f"no descent from pad ({x:.2f},{y:.2f}) net {net}")


class PackedLanes:
    """First-fit interval packing: nets whose x spans don't overlap share a lane."""

    def __init__(self, start, stop, pitch):
        self.start = start
        self.stop = stop
        self.pitch = pitch
        self.lanes = []

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


def add_zone(board, netname, layer):
    net = board.FindNet(netname)
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNetCode(net.GetNetCode())
    chain = pcbnew.SHAPE_LINE_CHAIN()
    for (px, py) in ((5, 5), (112, 5), (112, 109), (5, 109)):
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


def main():
    strip_copper(BOARD)
    board = pcbnew.LoadBoard(BOARD)
    r = Router(board)

    bands = {name: Band(name, y0, y1, jog) for (name, y0, y1, jog) in BAND_DEFS}
    for b in bands.values():
        b.build(r.pads)
    band_list = [bands[n] for n in ("ROW2", "ROWA", "MISC34", "MISC4")]

    fp_pads = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        for pad in fp.Pads():
            if not pad.GetNumber():
                continue
            p = pad.GetPosition()
            fp_pads.setdefault(ref, {})[pad.GetNumber()] = (
                to_mm(p.x), to_mm(p.y), pad.GetNetname())

    # dest-side via columns, pre-claimed so crossers keep COL_SEP from them,
    # and the fixed horizontal entry jogs (header pads 2/3, the J17 threads)
    # blocked outright - a crossing column through a jog's x-span collides
    # with it no matter which corridor it jogged in
    for ref, hx in HDR.items():
        bands["ROWA"].claim(hx + HDR_STEP_DX)
        bands["ROWA"].claim(hx + HDR_DIR_DX)
        bands["ROWA"].blocked.append((hx - abs(HDR_DIR_DX) - 0.155,
                                      hx + HDR_STEP_DX + 0.155))
    for num, (px, py, pname) in fp_pads["J17"].items():
        if pname != "GND" and py > 53.0:
            bands["ROWA"].claim(px + 1.27)          # AL_Z / AL_B threads
            bands["ROWA"].blocked.append((px - 0.16, px + 1.43))
    tb_xs = []
    for ref in ("J21", "J22", "J23", "J34", "J35", "J36", "J37"):
        for num, (px, py, pname) in fp_pads[ref].items():
            if pname != "GND":
                tb_xs.append(px)
    for c in tb_xs:
        bands["MISC34"].claim(c)
        bands["MISC4"].claim(c)
    for c in LIM_STREET:
        bands["MISC4"].claim(c)   # keep misc-row-3 escapes off the LIM street
                                  # (only LIM crosses MISC34, so no claim there)

    r_lanes = PackedLanes(*R_LANES)
    s_lanes = PackedLanes(*S_LANES)
    s2_lanes = PackedLanes(*S2_LANES)

    nets = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        for pad in fp.Pads():
            if not pad.GetNumber():
                continue
            name = pad.GetNetname()
            if not name or name in ("GND", "+12V"):
                continue
            p = pad.GetPosition()
            nets.setdefault(name, []).append(
                (ref, pad.GetNumber(), to_mm(p.x), to_mm(p.y)))

    def corridor_of(net):
        fam = net.split("_")[0]
        if fam in ("STEP", "DIR", "AL"):
            return "R"
        if fam in ("EN", "LIM"):
            return "S"
        return "S2"

    # deepest source pad first: a bottom-row Mini-Fit pin is hemmed in by its
    # neighbors' escapes, so it picks its exit before they wall it off
    tb_refs = {"J21", "J22", "J23", "J34", "J35", "J36", "J37"}

    def src_depth(n):
        ys = [p[3] for p in nets[n] if p[0] not in tb_refs]
        return max(ys) if ys else 0.0

    order = sorted(nets, key=lambda n: (
        corridor_of(n),
        -src_depth(n) if corridor_of(n) == "S2" else 0.0,
        min(p[2] for p in nets[n])))
    lanes_for = {"R": r_lanes, "S": s_lanes, "S2": s2_lanes}
    stop_at = {"R": R_LANES[0], "S": S_LANES[0], "S2": S2_LANES[0]}
    lim_street = list(LIM_STREET)

    for name in order:
        cor = corridor_of(name)

        # --- LIM: row 2 pad -> row A crossing -> corridor S, lane west to the
        # far-left street, down through both misc rows, corridor S2 east, up
        # into the LIMITS block ---------------------------------------------
        if name.startswith("LIM"):
            (ref3p, num, x, y) = [p for p in nets[name] if p[0].startswith("J") and p[1] == "2"
                                  and p[0] in ("J6", "J7", "J8", "J9", "J10")][0]
            (reftb, numtb, tx, ty) = [p for p in nets[name] if p[0] == "J21"][0]
            pts = route_down(r, [bands["ROWA"]], x, y, S_LANES[0], name,
                             prefer=x - 4.0)
            if pts is None:
                raise RuntimeError(f"LIM descent failed for {name}")
            street = lim_street.pop(0)
            s_lane = s_lanes.take(street, pts[-1][0])
            r.emit_pts(pts + [(pts[-1][0], s_lane)], name, pcbnew.F_Cu)
            r.via(pts[-1][0], s_lane, name)
            r.seg(street, s_lane, pts[-1][0], s_lane, name, pcbnew.B_Cu)
            r.via(street, s_lane, name)
            pts2 = route_down(r, [bands["MISC34"]], street, s_lane, S2_LANES[0], name)
            if pts2 is None:
                raise RuntimeError(f"LIM street descent failed for {name}")
            s2_lane = s2_lanes.take(min(street, tx), max(street, tx))
            r.emit_pts(pts2 + [(pts2[-1][0], s2_lane)], name, pcbnew.F_Cu)
            r.via(pts2[-1][0], s2_lane, name)
            r.seg(min(pts2[-1][0], tx), s2_lane, max(pts2[-1][0], tx), s2_lane,
                  name, pcbnew.B_Cu)
            r.via(tx, s2_lane, name)
            r.seg(tx, s2_lane, tx, ty, name, pcbnew.F_Cu)
            continue

        lanes = lanes_for[cor]
        stop_y = stop_at[cor]
        sources = []
        dests = []

        for (ref, num, x, y) in sorted(nets[name], key=lambda p: (p[2], p[3])):
            if ref in AXIS:
                col = AXIS[ref][1]
                dx, jog_y = JACK_CHANNELS[num]
                cx = col + dx
                pre = []
                sx = x
                if num == "1":
                    sx = x + PIN1_SIDESTEP
                    pre.append((x, y))
                    y = y + PIN1_SIDESTEP
                pre += [(sx, y), (sx, jog_y), (cx, jog_y)]
                crossed = [bands["ROW2"]] if cor == "R" else \
                          [bands["ROW2"], bands["ROWA"]]
                pts = route_down(r, crossed, cx, jog_y, stop_y, name)
                if pts is None:
                    raise RuntimeError(f"jack descent failed: {name} from {ref}")
                sources.append((pre[:-1] + pts, pts[-1][0]))
            elif ref in ("J11", "J12", "J13", "J14", "J30", "J31",
                         "J15", "J32", "J33"):
                own = fp_pads[ref]
                below = any(abs(ox - x) < 1.0 and oy > y + 1.0
                            for (ox, oy, on) in own.values())
                pts = descend_from_pad(r, [bands["MISC4"]], x, y, stop_y,
                                       name, below)
                sources.append((pts, pts[-1][0]))
            elif ref in HDR:
                hx = HDR[ref]
                if num == "2":
                    dests.append(("hdr_step", hx))
                elif num == "3":
                    dests.append(("hdr_dir", hx))
                elif num == "4":
                    dests.append(("hdr_en", hx))
            elif ref == "J16":
                dests.append(("rib_north" if y < 53.0 else "rib_south_rise", x))
            elif ref == "J17":
                dests.append(("rib_north" if y < 53.0 else "rib_thread", x))
            elif ref in ("J21", "J22", "J23", "J34", "J35", "J36", "J37"):
                dests.append(("tb_rise", x))
            else:
                raise RuntimeError(f"no routing rule for {ref} net {name}")

        xs = [vx for (_, vx) in sources]
        for kind, data in dests:
            if kind == "hdr_step":
                xs.append(data + HDR_STEP_DX)
            elif kind == "hdr_dir":
                xs.append(data + HDR_DIR_DX)
            elif kind == "rib_thread":
                xs.append(data + 1.27)
            else:
                xs.append(data)
        lane_y = lanes.take(min(xs), max(xs))

        for (pts, vx) in sources:
            r.emit_pts(pts + [(vx, lane_y)], name, pcbnew.F_Cu)
            r.via(vx, lane_y, name)

        for kind, data in dests:
            if kind == "hdr_step":
                cx = data + HDR_STEP_DX
                r.via(cx, lane_y, name)
                r.emit_pts([(cx, lane_y), (cx, HDR_Y["2"]), (data, HDR_Y["2"])],
                           name, pcbnew.F_Cu)
            elif kind == "hdr_dir":
                cx = data + HDR_DIR_DX
                r.via(cx, lane_y, name)
                r.emit_pts([(cx, lane_y), (cx, HDR_Y["3"]), (data, HDR_Y["3"])],
                           name, pcbnew.F_Cu)
            elif kind == "hdr_en":
                r.via(data, lane_y, name)
                r.emit_pts([(data, lane_y), (data, HDR_Y["4"])], name, pcbnew.F_Cu)
            elif kind == "rib_north":
                r.via(data, lane_y, name)
                r.emit_pts([(data, lane_y), (data, RIBBON_N_Y)], name, pcbnew.F_Cu)
            elif kind == "rib_south_rise":
                r.via(data, lane_y, name)
                r.emit_pts([(data, lane_y), (data, RIBBON_S_Y)], name, pcbnew.F_Cu)
            elif kind == "rib_thread":
                tx = data + 1.27
                r.via(tx, lane_y, name)
                r.emit_pts([(tx, lane_y), (tx, THREAD_JOG_Y),
                            (data, THREAD_JOG_Y), (data, RIBBON_S_Y)],
                           name, pcbnew.F_Cu)
            elif kind == "tb_rise":
                r.via(data, lane_y, name)
                r.emit_pts([(data, lane_y), (data, TB_Y)], name, pcbnew.F_Cu)

        lane_xs = [vx for (vx, vy, vn) in r.vias
                   if vn == name and abs(vy - lane_y) < 1e-6]
        if len(lane_xs) >= 2:
            r.seg(min(lane_xs), lane_y, max(lane_xs), lane_y, name,
                  pcbnew.B_Cu, SIG_W)

    # planes: GND on In1, +12V on In2 - every pad of both nets is through-hole
    add_zone(board, "GND", pcbnew.In1_Cu)
    add_zone(board, "+12V", pcbnew.In2_Cu)

    problems = r.check()
    if problems:
        print(f"{len(problems)} clearance problem(s); NOT saved:")
        for p in problems[:40]:
            print(" ", p)
        sys.exit(1)

    r.emit()
    pcbnew.SaveBoard(BOARD, board)
    print(f"routed {len(nets)} nets: {len(r.segs)} segments, {len(r.vias)} vias, "
          f"{len(r_lanes.lanes)} R lanes, {len(s_lanes.lanes)} S lanes, "
          f"{len(s2_lanes.lanes)} S2 lanes, GND plane In1, +12V plane In2 "
          f"(unfilled - kicad-cli drc --refill-zones --save-board). Saved.")


if __name__ == "__main__":
    main()
