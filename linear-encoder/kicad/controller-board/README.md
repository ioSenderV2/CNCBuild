# Controller board - KiCad

Schematic for the daughter board described in [`../../controller-board.md`](../../controller-board.md).

| File | |
|---|---|
| `controller-board.kicad_sch` | The schematic. Symbols are **embedded** (`lib_symbols`), so it needs no external libraries. |
| `controller-board.kicad_pro` | Project wrapper. |
| `netlist.txt` | **The authoritative connection list.** Generated from the same source data as the schematic. |

## ⚠️ Status: generated, NOT opened in KiCad

KiCad was not installed on the machine that produced this, so **nobody has yet confirmed the file opens.**
It is well-formed (balanced s-expressions, 22 symbols, 85 wire/label pairs) and its labels match
`netlist.txt` net-for-net, but that is structural verification, not "Eeschema loads it".

**First job when KiCad is installed:** open it, and run `kicad-cli sch erc controller-board.kicad_sch`.
If it will not load, `netlist.txt` carries the whole design and redrawing it by hand is an hour's work.

## How it is drawn

**Connections are by net label on a short stub at each pin**, not point-to-point wires. That is
electrically identical for netlist and ERC purposes, and it is far less error-prone to generate than
routing 40-odd nets by computed coordinates. It reads as a fan-out list rather than a picture of wires -
deliberate, given the design is literally a fan-out.

Expect ERC to complain that no net has a power **source** (the 3V3 comes in through a passive header
pin). That is the schematic being honest about a daughter board, not a fault. Add a `PWR_FLAG` on
`+3V3` and `GND` to silence it.

## Symbols are placeholders

`cnc:RJ45_8`, `cnc:HDR_2x10`, `cnc:R`, `cnc:C` are minimal rectangles with correctly numbered pins -
enough to carry the netlist, not a substitute for real library parts. **Before layout, swap them for
the actual manufacturer symbols and footprints**, in particular:

- the RJ45 - **shielded, no magnetics** (see the warning in `controller-board.md`), and
- the 2x10 **2.00 mm** female header, not 2.54 mm.

`J1..J4` are X, Y, A, Z in that order; `J5` is the header to the module's `P1`.
