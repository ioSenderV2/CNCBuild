# Interface board - KiCad

The termination board that replaces the DB37 breakout: machine cables in through the
enclosure lid, RP23U5XBB controller fed out the other side. All connectors, no actives -
the 12 V arrives regulated from the existing 36 V -> 12 V buck in the same enclosure.

| File | |
|---|---|
| `interface-board.kicad_sch` | The schematic. Symbols are **embedded** (`lib_symbols`), so it needs no external libraries. |
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
| 5x RJ45 vertical, one cat6 per stepper - column order **X, Y1, Y2, Z, B** | 2x10 IDC ribbon to RP23 **J20** (pin-for-pin) |
| 5x Mini-Fit Jr 3P, one prox per axis, paired beside its RJ45 | 2x3 IDC ribbon to RP23 **J24** servo alarms, per-axis parallel |
| Mini-Fit Jr 3P - 3D probe (12 V) | TB 2P - 12 V IN from buck |
| Mini-Fit Jr 3P - toolsetter (12 V) | TB 2P - 12 V OUT to the RP23's power inputs |
| 2x Mini-Fit Jr 2P - touch probes | TB 5P - limits |
| Mini-Fit Jr 4P - spindle (Enable, GND, GND, 0-10 V) | TB 4P - spindle, TB 2P - probe + door |

**Y1 drives the controller's Y, Y2 drives A.** The three touch/3D probe signals are
wired-OR onto one PROBE net; the toolsetter goes to DOOR.

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

Reproduce with:

```
kicad-cli sch erc --severity-error --exit-code-violations interface-board.kicad_sch
kicad-cli sch export netlist --format kicadsexpr --output kicad-export.net interface-board.kicad_sch
```

## Open items

1. **J17 alarm pin -> RP23 LED mapping.** All five alarm pins join one net on the RP23,
   so the wiring works regardless; which pin lights which axis LED is unlabelled in the
   RP23 schematic. Read the board silkscreen when making the ribbon.
2. **Footprints.** Schematic only so far; the connector parts are picked, the IDC
   shrouded headers and terminal block pitch still are not. Board-side parts:

   | Position | Part | Qty |
   |---|---|---|
   | RJ45 vertical (J1-J5) | Amphenol **69255-004LF** - same jack as the sensor board, unshielded, no magnetics, drawing notes in manufacturer-assets | 5 |
   | 3P single row (J6-J12) | Molex **39-30-1039** - 5566, vertical, peg lock. **Not in the 2026-11-02 Mouser order** | 7 |
   | 4P dual row 2x2 (J15) | Molex **46999-0621** - 2x2 vertical, tin, 10 ordered 2026-11-02, Mouser order 40971389 | 1 |
   | 2P dual row (J13, J14) | Molex **39-29-9027** (with peg) and **39-31-0027** (no peg) - both 2 ckt vertical, tin, 10 of each ordered 2026-11-02, Mouser order 40971389 | 2 |

   Cable-end housings (5557, take the 5556 terminals already in stock): 3P single row
   **39-01-4031**, 4P single row **39-01-4041**, 2P dual row **39-01-2025** family.
   There is no 2P in the 5566 single-row range - it starts at 3 circuits, which is why
   the touch probes are dual-row and self-key by shape against the 3P sockets.
3. **The RP23's J20 and J24 headers ship unpopulated** - a 2x10 and a 2x3 get soldered
   onto the controller as part of this build.
