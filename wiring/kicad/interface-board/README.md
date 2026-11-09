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
| `interface-board.kicad_pcb` | **REV B, this branch: 133 x 132 mm, FOUR layers** - F.Cu signal, In1.Cu solid GND plane, In2.Cu solid +12V plane, B.Cu signal, plus the 36 V pours. 27.2 sq in. **Top half MACHINE IN, bottom half RP23 OUT.** The lid gets cut to match the board. The four M3 holes are **at the corners** - 22,4 / 125,4 / 5,127.3 / 127,127.3 from the top-left; [`../../../machine/drawings/board-mounting.html`](../../../machine/drawings/board-mounting.html) is the drilling drawing and regenerates from this file. **main still holds Rev A** (210 x 94, 2 layers) - the boards in hand. |
| `interface-board.pretty/` | Project footprints for the two parts KiCad's libraries lack: the 85508 jack and the 3P single-row header, both taken from the committed Molex drawings. |
| `route.py` | Regenerates ALL copper from the placed footprints - the Rev B rewrite of the channel router. Owns every track on the board; re-run it after moving a part, then refill zones via the DRC command below. GND and +12V are inner-plane zones and route themselves (every pad on both nets is through-hole); signals run as F.Cu verticals into three packed B.Cu lane corridors. Verticals cross a connector row on searched columns, 0.70 mm apart - track-past-via, not just track-track - with jogs in the gap above the row. |
| `fab/oshpark/` | Manufacturing outputs for **OSH Park**: gerbers (Protel extensions), Excellon drill, and `interface-board-oshpark.zip` - the one file their upload takes. Board is 210 x 94, 2 layers; their standard 1.6 mm matches the 85508 jack's 1.57 tooling. **Rev A ordered 2026-11-03**, OSH Park order xPBWS3rt, $164.95 for 3 with FedEx 2 Day - this zip is what was uploaded; invoice alongside. Regenerate after any board change with the two kicad-cli export commands, then re-zip. |
| `fab/oshpark-revb/` | **Rev B manufacturing outputs - FOR A QUOTE, NOT AN ORDER.** `interface-board-revb-oshpark.zip` is the single file their upload takes: 13 files, all four copper layers (`.gtl` `.g1` `.g2` `.gbl`), masks, silks, `.gm1` outline and the Excellon drill. The drill **map** is written alongside but deliberately kept **out of the zip** - it is a `.gbr` and their uploader can mistake it for a copper layer. Outline measured from the plotted gerber: **133.00 x 132.00 mm, 27.2 sq in.** Regenerate after any board change. **Rev A's order record in `fab/oshpark/` is not touched by this.** |
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
| 2x Mini-Fit Jr 2P - touch probes | TB 2P 5.08 - 12 V IN, TB 2P 5.08 - 12 V OUT to the RP23, TB 2P 5.08 - **36 V IN from the supply** - the three cabinet feeds side by side |
| **5x Mini-Fit Jr 2P - stepper power**, one per axis under its limit connector: where the **18/2** motor supply cable terminates. Pin 1 **+36 V**, pin 2 **return** | |
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

🔴 **THE 36 V PAIR IS ISOLATED AND MUST STAY THAT WAY.** `+36V` and `36V_RET`
touch nothing else on the board - not GND, not +12V. That is the same rule the
12 V supply exists to protect: tying the motor return to logic ground throws away
the drives' measured per-signal isolation. **The 36 V return is not a ground.**

**The 36 V bus is copper pours, not traces, and that is what set the board size.**
The supply is 600 W at 36 V - **16.5 A across all axes**, nameplate, see
[`../../breakout-box.md`](../../breakout-box.md) - and 16.5 A wants about 10 mm of
1 oz copper per leg. Under the limit row **both legs are on B.Cu**, stacked, because
F.Cu in that band belongs to the five signal bundle streets that have to cross it;
down the east edge **+36V takes F.Cu and 36V_RET takes B.Cu** in one 10.2 mm channel,
stitched with 20 vias where +36V changes layer. [`route.py`](route.py) owns all of it.

**J20 is a skipped reference.** On this bench "J20" means the RP23's stepper header;
two J20s in one enclosure invites miswiring.

## Status: verified against KiCad 10.0.5

| Check | Result |
|---|---|
| ERC, error severity | **0 violations** |
| `netlist.txt` | **All 44 nets**, planes included, written straight from the kicad-cli export. FLAG: **this is no longer an independent check.** It was one while `generate.py` produced both; now that KiCad owns the schematic the file can only be derived from it, so it is documentation, not corroboration. |
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
   | 2P dual row (J13, J14, J30, J31, **J50-J54 stepper power**) | Molex **39-29-9027** - 2 ckt vertical with peg, tin, 10 ordered 2026-11-02, Mouser order 40971389 (the same order's 39-31-0027 is 10 spare 2-ckt without peg - they also fit these footprints). The four probe/mist/flood positions carry signal; **the five power positions carry 5 A each** - Mini-Fit Jr is rated 9 A on 18 AWG, so the part is the same and the crimp terminal is what must suit the wire | 9 |
   | 3.5 mm TB 2P (J23, J34, J35) | KF350-class screw block, 4Ucon pattern - **to order** | 3 |
   | 3.5 mm TB 4P (J22, J36) | same family - **to order** | 2 |
   | 3.5 mm TB 5P (J21) | same family - **to order** | 1 |
   | Pin header 1x04 2.54 mm (J40-J44, J37 UART1 out) | any breakaway header - **to order or from stock** | 6 |

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

## Rev B - designed on this branch, 2026-11-09

**His call, 2026-11-09: "proceed with this alternate design and see how it shakes out."**
This branch is that design, done: placed, routed, ERC/DRC clean, silkscreened, mounting
sheet regenerated. 🔴 **THE FAB STILL WAITS** until Rev A's lessons are in - no order goes
out on the back of this branch alone.

### What it came out as

| | |
|---|---|
| **Board** | **133 x 132 mm, 4 layers** - 27.2 sq in, ~$272 at his $10/sq in 4-layer rate, against Rev A's $153. Inside his 160 mm square. It was 121 x 104.5 / ~$196 before the stepper power row; **the extra 27.5 mm of height is the 36 V bus band and the extra 12 mm of width is its east channel** - see the 36 V note above for why that copper has to be that wide. |
| **The halves** | **Top half MACHINE IN** (jacks + limit 3Ps, the stepper power row, then the misc inputs), **bottom half RP23 OUT** (ribbons + Teensy headers + the three power-input blocks, then the signal TBs on the bottom edge, field wiring off the south side). A heavy silk divider with MACHINE SIDE - IN / RP23 SIDE - OUT names them - one silk color is all OSH Park prints, so the zoning does what color coding would have. |
| **Stepper power** | Five Mini-Fit Jr 2P under the limit connectors, one per axis, for the 18/2 motor supply cables; the 36 V input block sits with the 12 V pair. Isolated `+36V` / `36V_RET`, bussed on pours - see the 36 V note above. |
| **Stackup** | F.Cu signal / In1.Cu **solid GND plane** / In2.Cu **solid +12V plane** / B.Cu signal. Every GND and +12V pad is through-hole, so **both nets routed themselves** - zero GND or 12 V copper on the signal layers. That plane pair is what deleted Rev A's 24 mm corridor. |
| **What bought the clean halves** | Jack pitch opens 18 -> 24 mm, and each column's five nets (LIM, STEP, EN, DIR, AL) drop in **one bundle street** east of the column. The misc inputs tile one per inter-bundle zone, so no fixed vertical ever pierces a connector. The first Rev B cut proved the packed version of this order unroutable - 25 verticals cannot pierce two Mini-Fit rows at 18 mm pitch - which is why that cut interleaved the rows; the wider pitch is what undoes it. |
| **Zone balance** | Control 2x2 sits in the X column's zone and the 3D probe 3P in the B column's zone - a 2x2 beside the UART 2x2 outruns the crossing columns one zone can hold. Row B follows its sources: CONTROL, LIMITS, PRB/DR, SPINDLE, MIST, FLOOD, UART, west to east. |

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

**Rev B lands at 27.2 sq in: ~$272 against Rev A's $153.** Three choices, each his and
each made with the price in front of him:

| Cut | sq in | ~cost | What bought it |
|---|---|---|---|
| Packed, rows interleaved | 17.3 | $173 | the first attempt |
| Clean IN / OUT halves | 19.6 | $196 | 24 mm jack pitch, so every vertical gets a street |
| **Plus stepper power** | **27.2** | **$272** | the 36 V band and its east channel |

FLAG: **THE COMMITTED INVOICE CANNOT SERVE AS RATE EVIDENCE.**
`fab/oshpark/oshpark-order-invoice-xPBWS3rt.pdf` is **image-only** - there is no extractable
text in it, so no rate or line item can be read back out. It records that the order happened,
not what it cost per unit area. **A text PDF or a saved quote page would.**

### Still open before any Rev B order

1. **Rev A's lessons.** He is wiring Rev A now; whatever that run teaches goes in before
   gerbers are cut. Nothing in `fab/` describes Rev B - the zip there is Rev A's order.
2. **Lid cutout and mounting.** 133 x 132 against Rev A's 210 x 94, M3 at the four
   corners - 22,4 / 125,4 / 5,127.3 / 127,127.3 - the regenerated
   [`board-mounting.html`](../../../machine/drawings/board-mounting.html) has the drawing.
3. **4-layer gerber export.** When fab is called: the two kicad-cli export commands now need
   In1.Cu and In2.Cu in the layer list, and a fresh zip - do not overwrite `fab/oshpark/`,
   that is Rev A's order record.
4. 🔴 **THE 36 V INPUT BLOCK'S RATING IS NOT CHECKED, AND IT IS THE ONE PART THE BOARD
   COPPER CANNOT RESCUE.** J55 is the same CUI TB007-508 5.08 mm family as the 12 V pair,
   chosen for consistency, not for current. **A 5.08 mm screw block is typically rated
   10-15 A and takes 14 AWG at best, against a 16.5 A supply.** The pours are sized for the
   full 16.5 A; the block may not be, and neither may the wire from the supply. Settle one
   of: a bigger block, a fuse ahead of it that the copper is then sized against, or a
   measured figure for what the five drives actually draw together.
