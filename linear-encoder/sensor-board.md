# Sensor board

One per puck: the **AS5311 on the tape-facing side**, the RJ45 jack and every passive on the other.
Four of them (three now, Z later - §11.9), panelised. The design rationale for carrying the chip
rather than a breakout is in
[`design-can-position-feedback.md`](design-can-position-feedback.md) § *The sensor board: carry the
chip, not a breakout*; this file is the board itself.

Status: **schematic drawn and verified, 2026-08-29. No layout. The connector footprint is open** -
see below, because it is the one thing that can force a different part.

KiCad project: [`kicad/sensor-board/`](kicad/sensor-board/).

---

## ⚠️ The through-hole jack does not obviously fit

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

Test pads: `TP1` `CLK`, `TP2` `DO` - they cost no GPIO and make the board interrogable over SSI on
the bench, which beats the two hardware flags as a diagnostic.

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
  the design doc asked for**, and it is free to delete.
- **Package datums.** Figure 14's Hall-array dimensions were read off a rendered page. §"carry the
  chip" already says the reference edges deserve a second look before layout, and layout is exactly
  where they get used.
