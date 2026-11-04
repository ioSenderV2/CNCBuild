# Sensor board

One per puck: the **AS5311 on the tape-facing side**, the RJ45 jack and every passive on the other.
**Three pucks - X, Y1, Y2.** The Z axis takes a different mount, yet to be designed: the magnetic
strip goes on the outside edge of the X carriage, and the sensor hangs over it on a bracket off
the side of the Z plate - 1/4" aluminum so it cannot flex, since it has to span 15.3 + 30 mm
between the Z plate's bottom face and the X carriage's top face. The design rationale for carrying
the chip rather than a breakout is in
[`design-can-position-feedback.md`](design-can-position-feedback.md) § *The sensor board: carry the
chip, not a breakout*; this file is the board itself.

Status: **laid out and routed, DRC clean with schematic parity; regrown to 35 mm 2026-11-04**
for the bored-rod mount below. The jack is the SMT CRJ068-1-SMT, which removed the through-hole
height problem entirely. `kicad/sensor-board/layout.py` regenerates all placement and copper.

Layout facts worth knowing:

- Every component sits inside the 27 mm bore circle; the jack body covers nearly all of
  it, so the top-side parts live in the thin crescents beyond its courtyard. **D1
  (SRV05-4) rides the bottom** south of the tape corridor - at 1.1 mm tall it is no
  prouder than the AS5311 itself - and **both test pads ride the bottom**, side by side
  in the north crescent, so the bench check is all one face: tape over the chip, probes
  on CLK and DO, everything in view at once.
- The mounting holes are **o3.2 at (0, +/-15.5) from center**, on the axis across the
  tape run, matching M3 taps centered in the rod's 4 mm wall. Past each hole only
  0.4 mm of board remains - snug the bolts, don't crank them.
- **The top copper pour stops at r 13.4**, inside the bore, so the rod's end face seats
  on bare FR4 - no grounded copper against the machine frame through worn mask. The
  bottom GND patch is notched away from where the south bolt head lands for the same
  reason, and the script's clearance checker enforces both.
- **One flat 3.3 V trace crosses the corridor on the tape-facing side** (and the chip's
  own escapes exit through it). Copper under mask is ~0.05 mm proud against the 1-2 mm
  gap; the corridor keep-out is about parts and protrusions, and nothing stands in it.
- **The MagINCn test pad was deleted at layout** - no room in the crescents, and this
  file already called that pad an optional judgement call. The TP3 reference now names
  the **ground test pad** instead, third in the bottom-side row.
- OSH Park sells boards in threes and the machine wants three pucks - one order covers it
  exactly. The Z sensor's board gets decided with its bracket.

## Assembly sequence

1. Paste and hot-plate the **AS5311 side** first, board flat on the plate. The chip reflows
   once; surface tension centers it on the pads, and the pads carry the Hall-array offset.
2. Flip, paste and reflow the **top passives** with the board sitting on a short metal pipe
   so the chip hangs clear of the plate. The pipe is mechanical clearance only - the copper
   pours still carry the heat everywhere, and the chip's joints re-melting while it hangs
   is normal double-sided reflow. Face the pipe end flat so the board sits level.
3. The **jack goes on last with the iron** - eight 1.27 mm pads and two shell tabs; the
   brass shell wants a big tip. Its plastic is the one part that minds a long hot soak,
   which is why it stays off the plate.

KiCad project: [`kicad/sensor-board/`](kicad/sensor-board/).

---

## The puck

- The board is a **35 mm diameter disc** - as large as it can be and still insert through the
  35 mm hole in each X end plate and in the X carriage plate.
- Across the tape-facing side runs an **8 mm keep-out strip**, full width: no copper, no parts,
  nothing proud - the tape corridor. The **AS5311 sits in the middle of it**, the only thing
  inside the strip.
- The **RJ45 stands vertically on the other side** and the chip's signals route to its 8 pins
  (cable pinout below).
- The board bolts to the end of a **35 mm solid aluminum rod bored with the 1-1/16" annular
  cutter (26.99 mm)**, which leaves a **4 mm wall**. Everything on the board lives inside the
  27 mm bore; the **outer 4 mm ring of the top face is the rod's seat** - bare FR4, nothing on
  it but the two mounting holes. The rod goes through the 35 mm plate hole.
- **Two o3.2 holes at +/-15.5 mm from center**, on the axis across the tape run, match **M3
  taps centered in the rod's wall**. The bolts come in from the tape side; a button head
  stands ~1.65 mm off that face, inside the 3.8 mm minimum between board face and beam face
  (1.2 chip + 1 minimum gap + 1.6 tape).
- Working distance at Y1: **39.3 mm from the X end plate face to the Y1 beam face** that
  carries the tape; the **tape is 1.6 mm thick** with its adhesive. The rod's length and
  retention set the sensor somewhere inside that.
- Measured on the beam: the tape's lane sits between **low-profile flange bolt heads, o14,
  3.0 mm tall at the center and 2.3 at the edge, 16 mm between heads**. Anything on the
  puck that comes within 3 mm of the beam face must stay inside that 16 mm window - which
  a 35 mm disc riding at tape height cannot. Gap-setting is therefore coupled to the
  design doc's riser proposal (tape in a milled trench on an aluminum bar that stands
  proud of the bolt heads); still OPEN.
- OPEN: the rod's **retention mechanism** - whatever it is, it must allow setting **1-2 mm of
  separation** between the AS5311 and the magnetic tape on the beam face between the rails.
- **The 35 mm hole is not symmetric in use** (seen on the drilled X end plate): the **forward
  third is a keep-out**, because the Z spacer plate covers it at the limit of travel. The cat6
  patch cable must exit through the **back half** of the opening and run to the backside of the
  X beam, entering the drag chain without interfering. Orient the puck's jack accordingly.
- **Y2's patch cable** runs along the underside of the X beam and joins Y1's at the other end,
  in the drag chain.

---

## The jack: Same Sky CRJ068-1-SMT

**SMT, vertical, 8P8C, reflow-mount, no magnetics - nothing penetrates the board**, so the
tape-facing side carries the AS5311 and nothing else. Drawing committed as
[`SameSky-CRJ068-1-SMT-RJ45-SMT-Vertical.pdf`](../manufacturer-assets/SameSky-CRJ068-1-SMT-RJ45-SMT-Vertical.pdf):
body 16.1 x 19.5, 13.0 tall, 8 gull-wing pads (1.27 pitch, 8.89 row), solder flange tabs
opposite, 0.1 mm standoff. It has a **brass shield shell; the shell's tabs get solder pads and
NO net**, so a shielded plug's screen still floats at this end - the unshielded rule's intent,
met by netlist instead of by part. The 69255-004LF stays the record of the through-hole
attempt below; it is no longer the plan.

## SUPERSEDED: The through-hole jack does not obviously fit

The tape-facing side has a hard height budget, and it is small:

| | |
|---|---|
| AS5311 package height, **A max** (datasheet rev 1.12 Fig 17, MO-153) | 1.20 mm |
| Air gap to the strip (§General Description, typ) | 0.30 mm |
| **Distance from the board's tape-facing face to the tape** | **1.50 mm** |

The chip is the lowest thing on that face by design - that is what the 0.3 mm gap *means*. So
**anything else protruding from that face must stand less than 1.50 mm**, and less than that again if
any clearance is wanted.

A through-hole jack protrudes on exactly that face. Two contributions, and neither is currently known
for the chosen part:

1. **Solder tails.** IPC-A-610 accepts 0.5-2.5 mm of lead protrusion; untrimmed THT tails through a
   1.6 mm board are typically 1.5-2.0 mm. At the top of that range the tails reach the tape before
   the chip does. Trimmed flush they might make it, but a solder fillet still stands ~0.3-0.5 mm and
   the result then depends on workmanship, on four boards, repeatably.
2. **Plastic board-lock pegs.** Many vertical RJ45 jacks snap through the board on moulded pegs that
   protrude 1.5-3 mm and **cannot be trimmed**. If `69255-004LF` has them, through-hole is decided:
   it does not fit.

**Neither number is in this repo.** `manufacturer-assets/index.html` records the `69255` drawing as
*not captured* - only DIM C (15.62 mm, the height above the PCB) was read off it by hand. Getting the
drawing and reading tail length and board-lock protrusion is the next action on this board.

### The ways out, cheapest first

| Option | Verdict |
|---|---|
| **A thicker PCB - 2.4 or 3.2 mm** | The tails are a fixed length; a thicker board swallows more of them, and can end them inside the barrel entirely. Costs nothing but a fab option, changes no other dimension, and keeps the chosen part. **Try this first** - but it needs the tail length to size, so it waits on the same drawing. |
| **An SMT 8P8C jack** | Nothing protrudes through at all, which removes the problem rather than budgeting for it. The constraint is availability: it must still be **unshielded, vertical, no magnetics**, and that is a narrower search than the through-hole version was. |
| **Trim the tails and verify** | Workable only if there are no board-lock pegs, and it makes every board depend on hand work at the one dimension that is not allowed to vary. Acceptable as a fallback, not as a plan. |
| **Move the jack off the tape centreline** | Does not work here. The cable comes up the middle of the puck and §1.4 wants the die centreline **on** the puck axis for anti-rotation, so both parts want the centre. |

The unshielded requirement is not negotiable in any of these: it is what keeps the cable screen
grounded at the controller end **only**, by construction rather than by remembering (§14).

## The passives

Everything here is on the jack side, so none of it competes for the height budget above.

| Ref | Value | Why |
|---|---|---|
| `R1` `R2` `R3` | **100R-220R** (range, not yet fixed) | Series at the source on `A`, `B`, `MagDECn`. One half of an RC whose other half is 330 pF-1 nF at the **controller** end - so the value gets picked with that cap, not before it. |
| `R4` | **0R link** | Ties `CSn` low. It **must** be low or the incremental outputs never turn on and the board measures dead - it has an internal ~50 kΩ pull-up. A link rather than a trace so it can be lifted for SSI readout later. |
| `C1` | 100 nF | Decoupling. |
| `C2` | 10 µF | Decoupling. Both belong at this end: 2.4 m of 24 AWG has enough R and L that a supply dip here is real. |
| `D1` | TVS array, 4 channel | On `A`, `B`, `MagDECn` and `+3V3`, on the **connector side** of the series resistors - this end gets handled, and the resistors then also limit current into the array. |

**No pull-ups on this board.** `MagDECn` is open-drain and its ~2.2 kΩ pull-up lives at the
controller, with the RC, so the long line is held stiffly where it is read.

Test pads: `TP1` `CLK`, `TP2` `DO`, `TP3` `GND` - the first two cost no GPIO and make the board
interrogable over SSI on the bench, which beats the two hardware flags as a diagnostic, and the
third is the probe's ground clip. All three sit in a row on the **tape-facing side**, north of the
corridor: wave the tape over the chip with the probes on, and the pads, the chip and the tape all
face you.

## Cable pinout - not a free choice

The same CAT5 run lands on the controller board, so this end must mirror
[`kicad/controller-board/netlist.txt`](kicad/controller-board/netlist.txt) exactly:

```
1 = A     2 = GND   3 = B        4 = +3V3
5 = GND   6 = GND   7 = MagDECn  8 = GND
```

Five signals over four pairs, nothing spare.

## Open

- **The connector.** Above. Blocks layout.
- **`R1`-`R3` value**, pending the controller-end cap.
- **`TP3` / MagINCn.** `MagDECn` alone is what the design carries - asserted ⟺ RED, a clean per-axis
  fault. `MagINCn` would add the YELLOW early warning, but the cable is full and §"Pin budget" parks
  that option on a wire-OR across all four axes into `IO1`/`IO2` off the SH1.0 connector. A test pad
  was put on `MagINCn` so the board does not foreclose it; **that was a judgement call, not something
  the design doc asked for**, and it was deleted at layout when the crescents ran out of room (the
  TP3 reference now names the ground test pad).
- **Package reference dimensions.** Figure 14's Hall-array dimensions were read off a rendered page. §"carry the
  chip" already says the reference edges deserve a second look before layout, and layout is exactly
  where they get used.
