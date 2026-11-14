# Interface board - KiCad

The termination board that replaces the DB37 breakout: machine cables in through the
enclosure lid, RP23U5XBB controller fed out the other side. All connectors, no actives -
the 12 V arrives regulated from **its own mains-fed 12 V supply**, on the fourth pair off
the E-stop contactor's block. See
[`../../cabinet-power-and-grounding.md`](../../cabinet-power-and-grounding.md).

> FLAG: **NOT a 36 V -> 12 V buck.** This line said so until 2026-11-05 and it was wrong
> in a way nothing on the board shows: a buck off the motor rail ties logic ground to the
> motor return and throws away the drives' measured per-signal isolation. The board's
> 12 V input connector does not care where the 12 V comes from, so **nothing ordered is
> affected** - only what gets wired into it.

| File | |
|---|---|
| `interface-board.kicad_sch` | The schematic. Symbols are **embedded** (`lib_symbols`), so it needs no external libraries. |
| `interface-board.kicad_pcb` | **REV B, this branch: 121 x 104.5 mm, FOUR layers** - F.Cu signal, In1.Cu solid GND plane, In2.Cu solid +12V plane, B.Cu signal. 19.6 sq in. **Top half MACHINE IN, bottom half RP23 OUT.** **No 36 V on it** - stripped 2026-11-14, see below. The lid gets cut to match the board. The four M3 holes are **at the corners** - 22,4 / 117.3,4 / 5,99.8 / 117.3,99.8 from the top-left; [`../../../docs/drawings/board-mounting.html`](../../../docs/drawings/board-mounting.html) is the drilling drawing and regenerates from this file. **main still holds Rev A** (210 x 94, 2 layers) - the boards in hand. |
| `interface-board.pretty/` | Project footprints for the two parts KiCad's libraries lack: the 85508 jack and the 3P single-row header, both taken from the committed Molex drawings. |
| `route.py` | Regenerates ALL copper from the placed footprints - the Rev B rewrite of the channel router. Owns every track on the board; re-run it after moving a part, then refill zones via the DRC command below. GND and +12V are inner-plane zones and route themselves (every pad on both nets is through-hole); signals run as F.Cu verticals into packed B.Cu lane corridors. **Finds the board beside itself** - it carried a hard-coded Windows path until 2026-11-14 and now runs from either machine. Verticals cross a connector row on searched columns, 0.70 mm apart - track-past-via, not just track-track - with jogs in the gap above the row. |
| `fab/oshpark/` | Manufacturing outputs for **OSH Park**: gerbers (Protel extensions), Excellon drill, and `interface-board-oshpark.zip` - the one file their upload takes. Board is 210 x 94, 2 layers; their standard 1.6 mm matches the 85508 jack's 1.57 tooling. **Rev A ordered 2026-11-03**, OSH Park order xPBWS3rt, $164.95 for 3 with FedEx 2 Day - this zip is what was uploaded; invoice alongside. Regenerate after any board change with the two kicad-cli export commands, then re-zip. |
| `fab/oshpark-revb/` | **Rev B manufacturing outputs - FOR A QUOTE, NOT AN ORDER.** `interface-board-revb-oshpark.zip` is the single file their upload takes: 13 files, all four copper layers (`.gtl` `.g1` `.g2` `.gbl`), masks, silks, `.gm1` outline and the Excellon drill. The drill **map** is written alongside but deliberately kept **out of the zip** - it is a `.gbr` and their uploader can mistake it for a copper layer. Outline read from the plotted gerber: **x 5..126 by y 5..109.5 - 121.00 x 104.50 mm, 19.6 sq in.** Regenerate after any board change **with `make-fab-revb.ps1`**, which keeps the refill and the map-exclusion from being forgotten. **Rev A's order record in `fab/oshpark/` is not touched by this.** |
| `silk.py` | Regenerates every free silkscreen label (function names, per-terminal signal names). Owns all board text - edit its tables, not the board. |
| `interface-board.kicad_pro` | Project wrapper. |
| `netlist.txt` | The connection list. **Generated from the routed board by `make-netlist.py`** - not hand-kept, and not from the seed. |
| `make-netlist.py` | Writes `netlist.txt` from the board. Run after any net change. |
| `make-fab-revb.ps1` | Builds the whole Rev B quote package - DRC with refill, both exports, the zip. Refuses to build if DRC is not clean. Run this rather than the export commands by hand. |
| `swap-power-connectors.py` | Placed the three cabinet power feeds as Mini-Fit Jr. Kept because it carries the courtyard arithmetic for row A, which is the tightest row on the board. The 36 V one of the three has since gone. |
| `remove-36v.py` | **The strip-down, 2026-11-14**: took J50-J55 and both 36 V nets off the schematic and the board, moved everything under the limit row up 27.5 mm, brought the east mounting holes in and redrew the outline. One-shot - it refuses a board with no J50. Kept as the record. |
| `generate.py` | **The seed that produced the first version - not the live source once KiCad has touched the file.** See the warning below. |

> FLAG: **`generate.py` is a SEED, not the source of truth once the schematic has been
> opened and re-saved by KiCad.** Re-running it overwrites hand edits and layout work.
> Same rule as the two linear-encoder boards. If the design changes, edit in Eeschema.
>
> FLAG: **AND `netlist.txt` IS NO LONGER ITS OUTPUT.** It used to be, which meant the
> only way to refresh the netlist was to run the seed - which would have destroyed the
> board. So it was hand-edited instead, and had already lost its trailer that way.
> `make-netlist.py` now derives it from the routed board, and
> `drc --schematic-parity` is what makes "from the board" and "from the schematic" the
> same statement.

## What is on it

| Machine side (top-entry, through the lid) | Controller side |
|---|---|
| 5x RJ45 vertical, one cat6 per stepper - column order **X, Y1, Y2, Z, B**, each with its limit 3P stacked below it | 2x10 IDC ribbon to RP23 **J20** (pin-for-pin), middle of row A |
| Mini-Fit Jr 3P - 3D probe (12 V), 3P - toolsetter (12 V) | 2x3 IDC ribbon to RP23 **J24** servo alarms, west end of row A |
| 2x Mini-Fit Jr 2P - touch probes | Mini-Fit Jr 2P - 12 V IN, Mini-Fit Jr 2P - 12 V OUT to the RP23 - both latched, so a pulled feed has no bare conductor |
| 2x Mini-Fit Jr 2P - mist, flood | 3.5 mm TBs, one position per signal with silk names: limits 5P, spindle 4P, probe + door 2P |
| Mini-Fit Jr 4P - spindle (Enable, GND, GND, 0-10 V) | 3.5 mm TBs passing the new inputs through: mist 2P, flood 2P, control 4P; UART1 leaves on a **1x4 2.54 mm header** - dupont jumpers straight to the RP23's 4-pin UART header |
| Mini-Fit Jr 4P - cycle start / feed hold / e-stop / spare | 5x 2.54 mm header, **GND / Step / Dir / Enable** per axis - jumper to a Teensy T41U5XBB instead of the ribbon |
| Mini-Fit Jr 4P - UART1 for CAN, **TX / RX / 3.3V / GND** | |

**Y1 drives the controller's Y, Y2 drives A.** The three touch/3D probe signals are
wired-OR onto one PROBE net; the toolsetter goes to DOOR. Mist, flood, control and
UART1 pass straight through, connector to output terminal, position for position -
UART1's output being the 1x4 header rather than a screw block.

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

🔴 **THERE IS NO 36 V ON THIS BOARD - his, 2026-11-14.** Stepper power is distributed on
the DIN rail beside the supply, on Phoenix PT 4-QUATTRO blocks, and the 18/2 motor supply
cables land there. This board carries logic and 12 V only. Three things decided it, in the
order they turned up:

- **The supply grew to 26.6 A** (XDR-960-36) under pours sized for 16.5.
- **The input connector could never carry it.** Molex PS-5556-001 table 3: a 4-circuit
  Mini-Fit Jr is **8 A per circuit** on 16 or 18 AWG with brass terminals, 7 A with phosphor
  bronze - so the doubled legs were 16 A, not the 18 this file claimed. And drawing
  55660021-SD note 10: **"parts are not designed for current sharing"**, which is what
  doubling a leg is.
- **45 cm2 of 36 V pour sat 0.2 mm over the logic planes** - roughly 0.9 nF between the
  motor bus and logic ground, calculated not measured, on a board whose whole point is
  keeping the two apart.

The rule the pours were built around still stands, and is now kept by absence: **the motor
return is not a ground and never meets logic GND on this board.**

**THIS BOARD HAS NO PE CONNECTION AT ALL, AND THAT IS DELIBERATE.** There is no earth
or chassis net on it - 42 nets, none of them PE - **all four mounting holes are
unplated NPTH with no net**, and its enclosure is 3D printed, so there is no chassis
to bond. **Its GND arrives on one pad, J18.2 of the 12 V IN connector**, and leaves on
J19.2 to the RP23. The In1 plane distributes it from there.

✅ **THE TWO RULES ARE THE SAME RULE: SEPARATE EVERYWHERE, JOINED AT ONE POINT.** Logic
GND and the 36 V return do meet - **back at the cabinet's PE bar**, which carries
*12 V supply 0 V* and *motor supply 0 V* as two of its eight named conductors, see
[`../../cabinet-power-and-grounding.md`](../../cabinet-power-and-grounding.md).
**That bar is the single point, and the board staying isolated is what keeps it
single.** A second meeting anywhere - a jumper here, a shared terminal out at a
drive - turns one bond into a loop and puts chopped motor return current through
the logic ground plane. 🔴 **So do not "helpfully" tie the motor return to GND anywhere** - not at a drive, not
at the DIN blocks.

**J20 is a skipped reference.** On this bench "J20" means the RP23's stepper header;
two J20s in one enclosure invites miswiring.

## Status: verified against KiCad 10.0.8, 2026-11-14

| Check | Result |
|---|---|
| ERC | **0 errors.** 58 warnings, every one a library-not-configured notice - the symbols and footprints are embedded, so they carry nothing |
| `netlist.txt` | **All 42 nets**, planes included, written straight from the kicad-cli export. FLAG: **this is no longer an independent check.** It was one while `generate.py` produced both; now that KiCad owns the schematic the file can only be derived from it, so it is documentation, not corroboration. |
| PCB DRC with schematic parity, **all severities** | **0 errors, 0 unconnected, 0 parity issues.** 73 warnings: 41 silk over copper, 5 jack pin-1 dots near the top edge, 27 library notices. FLAG: **this row said "0 parity issues" while 178 were being hidden.** It was run at error severity, and every pad on the board was a net-name *warning*: the schematic's labels were local, so its nets were `/STEP_X` against the board's `STEP_X`. Connectivity matched; the names did not, and a real mismatch would have been one more warning in the pile. **The labels are global now and the mounting holes are marked board-only, so the count is a true zero** - run it at all severities to keep it that way |

Reproduce with:

```
kicad-cli sch erc --severity-error --exit-code-violations interface-board.kicad_sch
kicad-cli sch export netlist --format kicadsexpr --output kicad-export.net interface-board.kicad_sch
kicad-cli pcb drc --schematic-parity --severity-all --refill-zones --save-board interface-board.kicad_pcb
```

## Open items

1. **J17 alarm pin -> RP23 LED mapping.** All five alarm pins join one net on the RP23,
   so the wiring works regardless; which pin lights which axis LED is unlabelled in the
   RP23 schematic. Read the board silkscreen when making the ribbon.
2. **Footprints.** All 35 assigned and the board is placed and routed. The IDC headers
   are the standard shrouded 2.54 mm pattern (any vendor fits); the signal terminal
   blocks are 3.5 mm on the 4Ucon pattern (KF350 class fits), and the **two 12 V feeds** -
   in and out - are **Mini-Fit Jr** like the signal connectors. Board-side parts:

   | Position | Part | Qty |
   |---|---|---|
   | RJ45 vertical (J1-J5) | Molex **85508-5001** - top entry, THT, Cat5e, shielded (tab to GND; the patch cables are UTP so it carries nothing), no magnetics, 16.85 mm tall. 10 ordered 2026-11-03, Mouser order 40971773. NOT the sensor board's jack - that stays the unshielded 69255-004LF, whose end must float | 5 |
   | 3P single row (J6-J12) | Molex **39-30-1039** - 5566, vertical, peg lock. 20 ordered 2026-11-03, Mouser order 40971773 | 7 |
   | 4P dual row 2x2 (J15, J32, J33) | Bought as Molex **46999-0621**, 10 on 2026-11-02 (Mouser 40971389) and 20 more on 2026-11-13. FLAG: **Molex drawing 55660021-SD sheet 3 lists 46999-0621 as 5566-02A2MS-210 - 2 circuits, not 2x2.** The 4-circuit in that plating is 46999-0502 (Mouser minimum 4800 - his, 2026-11-14); plain tin is 39-29-9047. These three positions use the 04A2 footprint, peg holes 13.60 apart, and a 2-circuit part's pegs are 9.40 apart - it will not seat. He checks the parts when order 41109063 lands | 3 |
   | 2P dual row (J13, J14, J30, J31, **J18 12 V in, J19 12 V out**) | Molex **39-29-9027** - 2 ckt vertical with peg, tin. 10 ordered 2026-11-02 (Mouser 40971389), 25 more 2026-11-13; the first order's 39-31-0027 is 10 spare 2-ckt without peg, which also fit these footprints. The peg is worth keeping on the two feeds that get unplugged | 6 |
   | 3.5 mm TB 2P (J23, J34, J35) | KF350-class screw block, 4Ucon pattern - **to order** | 3 |
   | 3.5 mm TB 4P (J22, J36) | same family - **to order** | 2 |
   | 3.5 mm TB 5P (J21) | same family - **to order** | 1 |
   | Pin header 1x04 2.54 mm (J40-J44, J37 UART1 out) | any breakaway header - **to order or from stock** | 6 |

   Cable-end housings (5557, take the 5556 terminals already in stock): 3P single row
   **39-01-4031**, 4P single row **39-01-4041**, 2P dual row **39-01-2025** family.
   There is no 2P in the 5566 single-row range - it starts at 3 circuits, which is why
   the touch probes are dual-row and self-key by shape against the 3P sockets.

   NOTE: **THE TWO 12 V FEEDS NEED CABLE-END HOUSINGS, WHICH SCREW BLOCKS DID NOT** - two
   more 2P dual-row. That is the whole ordering consequence of the connector change.
3. **RP23 header state, from his board in hand:** J24 already carries a bare 2x3 header;
   J20 is open with plenty of room, so it gets a **shrouded** 2x10 (Digi-Key: CNC Tech /
   On Shore class, 2.54 mm vertical THT). The alarm ribbon's RP23 end therefore lands on
   an unkeyed header - mark pin 1 against the silkscreen; this board's J17 can still be
   shrouded so the interface end is foolproof.

---

## Rev B - designed on this branch, 2026-11-09; 36 V stripped 2026-11-14

**His call, 2026-11-09: "proceed with this alternate design and see how it shakes out."**
This branch is that design: placed, routed, ERC/DRC clean, silkscreened, mounting sheet
regenerated. 🔴 **THE FAB STILL WAITS** until Rev A's lessons are in - no order goes out on
the back of this branch alone.

### What it came out as

| | |
|---|---|
| **Board** | **121 x 104.5 mm, 4 layers** - 19.6 sq in, ~$196 at his $10/sq in 4-layer rate, against Rev A's $153. It was 133 x 132 / ~$272 with the stepper power row; taking the 36 V off gave back **27.5 mm of height** (the bus band) and **12 mm of width** (its east channel). |
| **The halves** | **Top half MACHINE IN** (jacks + limit 3Ps, then the misc inputs), **bottom half RP23 OUT** (ribbons + Teensy headers + the two 12 V feeds, then the signal TBs on the bottom edge, field wiring off the south side). A heavy silk divider with MACHINE SIDE - IN / RP23 SIDE - OUT names them - one silk color is all OSH Park prints, so the zoning does what color coding would have. |
| **Stepper power** | **Not here.** DIN rail, beside the supply - see the 36 V note above. |
| **Stackup** | F.Cu signal / In1.Cu **solid GND plane** / In2.Cu **solid +12V plane** / B.Cu signal. Every GND and +12V pad is through-hole, so **both nets routed themselves** - zero GND or 12 V copper on the signal layers. That plane pair is what deleted Rev A's 24 mm corridor. |
| **What bought the clean halves** | Jack pitch opens 18 -> 24 mm, and each column's five nets (LIM, STEP, EN, DIR, AL) drop in **one bundle street** east of the column. The misc inputs tile one per inter-bundle zone, so no fixed vertical ever pierces a connector. The first Rev B cut proved the packed version of this order unroutable - 25 verticals cannot pierce two Mini-Fit rows at 18 mm pitch - which is why that cut interleaved the rows; the wider pitch is what undoes it. |
| **Zone balance** | Control 2x2 sits in the X column's zone and the 3D probe 3P in the B column's zone - a 2x2 beside the UART 2x2 outruns the crossing columns one zone can hold. Row B follows its sources: CONTROL, LIMITS, PRB/DR, SPINDLE, MIST, FLOOD, UART, west to east. |
| **Mounting holes** | All four at the corners. The UART output header slid 7 mm west along row B to free the south-east one. |

### Cost, against his settled rates

SETTLED: **THE RATES ARE HIS, OFF OSH PARK, 2026-11-09.**

| Prototype service | Rate | Ships |
|---|---|---|
| **2 layer** | **$5 / sq in** | **9-12 days** |
| **4 layer** | **$10 / sq in** | **9-14 days** |

✅ **NO BARGAIN TIER IS LOST BY GOING TO 4 LAYERS - that was the open worry and it is closed.**
Both are the **same prototype service**. The whole cost of the fourth and fifth copper layers
is **double the rate and up to two more days**; there is no minimum area to clear and no
different class of service to fall into.

NOTE: **And the 2 layer rate checks against his own order** - 30.6 sq in at $5 is **$152.99**,
the order came to **$164.95** with FedEx 2 Day, leaving **$11.96** of shipping.

**Rev B lands at 19.6 sq in: ~$196 against Rev A's $153.** How it got there:

| Cut | sq in | ~cost | What bought it |
|---|---|---|---|
| Packed, rows interleaved | 17.3 | $173 | the first attempt |
| Clean IN / OUT halves | 19.6 | $196 | 24 mm jack pitch, so every vertical gets a street |
| Plus stepper power | 27.2 | $272 | the 36 V band and its east channel - **withdrawn 2026-11-14** |
| **36 V back off** | **19.6** | **$196** | DIN rail distribution, his, 2026-11-14 |

FLAG: **THE COMMITTED INVOICE CANNOT SERVE AS RATE EVIDENCE.**
`fab/oshpark/oshpark-order-invoice-xPBWS3rt.pdf` is **image-only** - there is no extractable
text in it, so no rate or line item can be read back out. It records that the order happened,
not what it cost per unit area. **A text PDF or a saved quote page would.**

### Still open before any Rev B order

1. **Rev A's lessons.** He is wiring Rev A now; whatever that run teaches goes in before
   gerbers are cut. Nothing in `fab/` describes Rev B - the zip there is Rev A's order.
2. **Lid cutout and mounting.** 121 x 104.5 against Rev A's 210 x 94, M3 at the four
   corners - 22,4 / 117.3,4 / 5,99.8 / 117.3,99.8 - the regenerated
   [`board-mounting.html`](../../../docs/drawings/board-mounting.html) has the drawing.
3. **4-layer gerber export.** Done for the quote - `fab/oshpark-revb/` holds the package and
   the zip. Regenerate it after any board change, and **do not overwrite `fab/oshpark/`**,
   which is Rev A's order record.
4. SETTLED: **the 36 V input and the supply that outgrew it - both closed by taking the 36 V off the board, his, 2026-11-14.** The history, shortest form: a 5.08 screw block, then Mini-Fit Jr with doubled legs so a pulled feed had no bare conductor, then an XDR-960-36 at 26.6 A against pours sized for 16.5 and a connector good for 16. Distribution is on the DIN rail now, and what bounds the fault current there is a cabinet question, in [`../../cabinet-power-and-grounding.md`](../../cabinet-power-and-grounding.md).
