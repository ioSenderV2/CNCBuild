# Interface board - KiCad

The termination board that replaces the DB37 breakout: machine cables in through the
enclosure lid, RP23U5XBB controller fed out the other side. All connectors, no actives -
the 12 V arrives regulated from **its own mains-fed 12 V supply**, on the fourth pair off
the E-stop contactor's block. See
[`../../cabinet-power-and-grounding.md`](../../cabinet-power-and-grounding.md).

> FLAG: **NOT a 36 V -> 12 V buck.** This line said so until 2026-11-05 and it was wrong
> in a way nothing on the board shows: a buck off the motor rail ties logic ground to the
> motor return and throws away the drives' measured per-signal isolation. The board's
> 5.08 mm terminal block does not care where the 12 V comes from, so **nothing ordered is
> affected** - only what gets wired into it.

| File | |
|---|---|
| `interface-board.kicad_sch` | The schematic. Symbols are **embedded** (`lib_symbols`), so it needs no external libraries. |
| `interface-board.kicad_pcb` | The board: **210 x 94 mm**, two layers, GND pour both sides, four M3 mounting holes. The lid gets cut to match the board. FLAG: **this line read 220 x 95 and the fab line below read 210 x 94** - Edge.Cuts measures 210 x 94, so the fab line was right. NOTE: **the holes are NOT in the corners** - they are at 4,4 / 204,4 / 3.2,45 / 206,66 from the top-left, which is why [`../../../machine/drawings/board-mounting.html`](../../../machine/drawings/board-mounting.html) exists. |
| `interface-board.pretty/` | Project footprints for the two parts KiCad's libraries lack: the 85508 jack and the 3P single-row header, both taken from the committed Molex drawings. |
| `route.py` | Regenerates ALL copper (tracks, vias, GND pours) from the placed footprints - a channel router. Owns every track on the board; re-run it after moving a part, then refill zones via the DRC command below. |
| `fab/oshpark/` | Manufacturing outputs for **OSH Park**: gerbers (Protel extensions), Excellon drill, and `interface-board-oshpark.zip` - the one file their upload takes. Board is 210 x 94, 2 layers; their standard 1.6 mm matches the 85508 jack's 1.57 tooling. **Rev A ordered 2026-11-03**, OSH Park order xPBWS3rt, $164.95 for 3 with FedEx 2 Day - this zip is what was uploaded; invoice alongside. Regenerate after any board change with the two kicad-cli export commands, then re-zip. |
| `silk.py` | Regenerates every free silkscreen label (function names, per-terminal signal names). Owns all board text - edit its tables, not the board. |
| `interface-board.kicad_pro` | Project wrapper. |
| `netlist.txt` | The connection list, generated from the same source as the schematic. |
| `generate.py` | **The seed that produced the first version - not the live source once KiCad has touched the file.** See the warning below. |

> FLAG: **`generate.py` is a SEED, not the source of truth once the schematic has been
> opened and re-saved by KiCad.** Re-running it overwrites hand edits and layout work.
> Same rule as the two linear-encoder boards. If the design changes, edit in Eeschema
> and update `netlist.txt` to match.

## What is on it

| Machine side (top-entry, through the lid) | Controller side |
|---|---|
| 5x RJ45 vertical, one cat6 per stepper - column order **X, Y1, Y2, Z, B**, each with its limit 3P stacked below it | 2x10 IDC ribbon to RP23 **J20** (pin-for-pin), right end of the board |
| Mini-Fit Jr 3P - 3D probe (12 V), 3P - toolsetter (12 V) | 2x3 IDC ribbon to RP23 **J24** servo alarms, left end |
| 2x Mini-Fit Jr 2P - touch probes | TB 2P 5.08 - 12 V IN from buck, TB 2P 5.08 - 12 V OUT to the RP23 |
| 2x Mini-Fit Jr 2P - mist, flood | 3.5 mm TBs, one position per signal with silk names: limits 5P, spindle 4P, probe + door 2P |
| Mini-Fit Jr 4P - spindle (Enable, GND, GND, 0-10 V) | 3.5 mm TBs passing the new inputs through: mist 2P, flood 2P, control 4P, UART1 4P |
| Mini-Fit Jr 4P - cycle start / feed hold / e-stop / spare | 5x 2.54 mm header, **GND / Step / Dir / Enable** per axis - jumper to a Teensy T41U5XBB instead of the ribbon |
| Mini-Fit Jr 4P - UART1 for CAN, **TX / RX / 3.3V / GND** | |

**Y1 drives the controller's Y, Y2 drives A.** The three touch/3D probe signals are
wired-OR onto one PROBE net; the toolsetter goes to DOOR. Mist, flood, control and
UART1 pass straight through, connector to terminal block, position for position.

**RJ45 pin map** (striped conductor = signal, solid = return):
1 Step, 3 Enable, 5 Dir, 7 Alarm; evens GND. Step and Alarm sit on opposite edges of
the jack - Step is the aggressor and Alarm feeds EStop. Signals on odds is correct on
the twists by construction: in T568 every odd pin's twist partner is an even pin.

**"Evens GND" does not say WHICH even pin, and that is where a split pair comes from.**
The twists are **1-2, 3-6, 4-5, 7-8**. So each signal's return leg must land on its
own twist partner: Step 1-2, Enable **3-6**, Dir **5-4**, Alarm 7-8. Wiring it as the
numbers read - 3 with 4, 5 with 6 - puts Enable and Dir in each other's twists. The
board cannot catch it, because all four evens are the same GND net: it passes
continuity and works, and costs only signal integrity. Drive-end terminals and the
reasoning are in [`../../ig57-drives.md`](../../ig57-drives.md).

**3P pin order**: 1 = 12 V, 2 = signal, 3 = GND - matches the SN04's brown/black/blue.

**J20 is a skipped reference.** On this bench "J20" means the RP23's stepper header;
two J20s in one enclosure invites miswiring.

## Status: verified against KiCad 10.0.5

| Check | Result |
|---|---|
| ERC, error severity | **0 violations** |
| Netlist matches `netlist.txt` | **Exactly** - all 31 nets, node for node, from the kicad-cli export |
| PCB DRC with schematic parity, error severity | **0 violations, 0 unconnected, 0 parity issues** |

Reproduce with:

```
kicad-cli sch erc --severity-error --exit-code-violations interface-board.kicad_sch
kicad-cli sch export netlist --format kicadsexpr --output kicad-export.net interface-board.kicad_sch
kicad-cli pcb drc --schematic-parity --severity-error --exit-code-violations --refill-zones --save-board interface-board.kicad_pcb
```

## Open items

1. **J17 alarm pin -> RP23 LED mapping.** All five alarm pins join one net on the RP23,
   so the wiring works regardless; which pin lights which axis LED is unlabelled in the
   RP23 schematic. Read the board silkscreen when making the ribbon.
2. **Footprints.** All 35 assigned and the board is placed and routed. The IDC headers
   are the standard shrouded 2.54 mm pattern (any vendor fits); the signal terminal
   blocks are 3.5 mm on the 4Ucon pattern (KF350 class fits), the 12 V pair 5.08 mm on
   the CUI TB007-508 pattern (KF301 class fits). Board-side parts:

   | Position | Part | Qty |
   |---|---|---|
   | RJ45 vertical (J1-J5) | Molex **85508-5001** - top entry, THT, Cat5e, shielded (tab to GND; the patch cables are UTP so it carries nothing), no magnetics, 16.85 mm tall. 10 ordered 2026-11-03, Mouser order 40971773. NOT the sensor board's jack - that stays the unshielded 69255-004LF, whose end must float | 5 |
   | 3P single row (J6-J12) | Molex **39-30-1039** - 5566, vertical, peg lock. 20 ordered 2026-11-03, Mouser order 40971773 | 7 |
   | 4P dual row 2x2 (J15, J32, J33) | Molex **46999-0621** - 2x2 vertical, tin, 10 ordered 2026-11-02, Mouser order 40971389 | 3 |
   | 2P dual row (J13, J14, J30, J31) | Molex **39-29-9027** - 2 ckt vertical with peg, tin, 10 ordered 2026-11-02, Mouser order 40971389 (the same order's 39-31-0027 is 10 spare 2-ckt without peg - they also fit these footprints) | 4 |
   | 3.5 mm TB 2P (J23, J34, J35) | KF350-class screw block, 4Ucon pattern - **to order** | 3 |
   | 3.5 mm TB 4P (J22, J36, J37) | same family - **to order** | 3 |
   | 3.5 mm TB 5P (J21) | same family - **to order** | 1 |
   | Pin header 1x04 2.54 mm (J40-J44) | any breakaway header - **to order or from stock** | 5 |

   Cable-end housings (5557, take the 5556 terminals already in stock): 3P single row
   **39-01-4031**, 4P single row **39-01-4041**, 2P dual row **39-01-2025** family.
   There is no 2P in the 5566 single-row range - it starts at 3 circuits, which is why
   the touch probes are dual-row and self-key by shape against the 3P sockets.
3. **RP23 header state, from his board in hand:** J24 already carries a bare 2x3 header;
   J20 is open with plenty of room, so it gets a **shrouded** 2x10 (Digi-Key: CNC Tech /
   On Shore class, 2.54 mm vertical THT). The alarm ribbon's RP23 end therefore lands on
   an unkeyed header - mark pin 1 against the silkscreen; this board's J17 can still be
   shrouded so the interface end is foolproof.

---

## Rev B target - the shape any future board takes

**His, 2026-11-09, and it is a TARGET, not work in progress.** Rev A is fabbed and in hand;
he runs it, collects whatever else wants changing, and a Rev B goes out smaller. **Nothing
here is scheduled. Do not start the rewrite below until a Rev B is actually called.**

### The layout he wants

| | |
|---|---|
| **The misc 3P and 4P connectors** - probe, toolsetter, UART, spindle control, everything that is **not** a stepper | come **down and left, underneath the stepper jacks**, out of the top-right |
| **The controller outputs along the bottom** | become **two rows**, stacked under the rest - taller is fine if it buys shorter |
| **Board width** | **180 mm or less**, against today's 210 |
| **Layer count** | **4 is acceptable.** "Smaller is better" |

### Why the empty middle is not waste

🔴 **THAT BAND IS THE ROUTER'S CORRIDOR, AND IT EXISTS BECAUSE THE BOARD IS 2 LAYER.**
[`route.py`](route.py) owns every piece of copper here and names it in its own docstring:
*"Corridor B (y 40..64): horizontal lanes, interval-packed so short nets share a lane."*
Every signal from the top connectors reaches the bottom connectors through horizontal lanes
on B.Cu, and those lanes need that height. **Fill the middle with connectors on 2 layers and
the copper has nowhere to go.**

✅ **SO 4 LAYERS IS THE ENABLER, NOT A SIDE EFFECT - his instinct was right and the two asks
are one ask.** A dedicated ground plane and a power plane free both outer layers for signal,
the corridor collapses, and the height comes out. **Packing it tighter and shrinking it are
the same change, and neither works on 2 layers.**

### 🔴 180 WIDE DOES NOT SAVE MONEY. AREA DOES.

**OSH Park prices by the square inch**, so width alone is the wrong target:

| | sq in |
|---|---|
| Today, 210 x 94 | **30.6** |
| 180 x 94 | **26.2** - only **14% less** |

**At roughly double the rate for 4 layers, a 180 x 94 four-layer board costs MORE than the
2-layer board he already has.** To come back cheaper on 4 layers the board has to lose about
**half** its area, not a seventh - call it **under 15 sq in**, which is something like
180 x 54 or 150 x 65.

✅ **AND THAT IS REACHABLE, BECAUSE THE SAVING IS IN THE HEIGHT.** The corridor is what 4
layers deletes, so the target to design against is **a square-inch number, with the height as
the variable** - not the 180 width.

FLAG: **THE RATES ARE NOT READ FROM A QUOTE.** The **2 layer $5 per sq in** is corroborated
by arithmetic against his own order: 30.6 sq in at $5 is **$152.99**, and the order came to
**$164.95** with FedEx 2 Day, leaving **$11.96** of shipping. That fit is close enough to
trust. **The 4 layer rate is recalled, not verified** - price the real outline on their site
before committing, and check whether a smaller 4 layer board still takes the standard service
rather than a different tier.

FLAG: **THE COMMITTED INVOICE CANNOT SERVE AS THAT EVIDENCE.**
`fab/oshpark/oshpark-order-invoice-xPBWS3rt.pdf` is **image-only** - there is no extractable
text in it, so no rate or line item can be read back out. It records that the order happened,
not what it cost per unit area. **A text PDF or a saved quote page would.**

### What the work actually is

**Moving the footprints is the easy half.** `route.py` regenerates all copper from their
positions, so there is no hand routing to redo.

🔴 **THE ROUTER IS THE JOB.** Its topology is hard-coded to the current arrangement - five
axis columns across the top, the rest in two brick-staggered rows to the right, corridor B at
y 40..64, the Teensy headers standing at x 150..166, one bottom row. **Every one of those
stops being true**, and a 4 layer version needs new layer assignments on top of it. Budget a
router rewrite, not a parameter change.

NOTE: **And [`../../../machine/drawings/board-mounting.html`](../../../machine/drawings/board-mounting.html)
regenerates itself** - it reads this board's outline, courtyards and mounting holes straight
from the PCB, so it follows a Rev B without being touched. Run `tools/make-board-sheet.py`.
