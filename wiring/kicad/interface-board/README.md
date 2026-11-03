# Interface board - KiCad

The termination board that replaces the DB37 breakout: machine cables in through the
enclosure lid, RP23U5XBB controller fed out the other side. All connectors, no actives -
the 12 V arrives regulated from the existing 36 V -> 12 V buck in the same enclosure.

| File | |
|---|---|
| `interface-board.kicad_sch` | The schematic. Symbols are **embedded** (`lib_symbols`), so it needs no external libraries. |
| `interface-board.kicad_pcb` | The board: 220 x 95 mm, two layers, GND pour both sides, M3 mounting holes in the corners. The lid gets cut to match the board. |
| `interface-board.pretty/` | Project footprints for the two parts KiCad's libraries lack: the 85508 jack and the 3P single-row header, both taken from the committed Molex drawings. |
| `route.py` | Regenerates ALL copper (tracks, vias, GND pours) from the placed footprints - a channel router. Owns every track on the board; re-run it after moving a part, then refill zones via the DRC command below. |
| `fab/oshpark/` | Manufacturing outputs for **OSH Park**: gerbers (Protel extensions), Excellon drill, and `interface-board-oshpark.zip` - the one file their upload takes. Board is 210 x 94, 2 layers; their standard 1.6 mm matches the 85508 jack's 1.57 tooling. Regenerate after any board change with the two kicad-cli export commands, then re-zip. |
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
the jack - Step is the aggressor and Alarm feeds EStop.

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
