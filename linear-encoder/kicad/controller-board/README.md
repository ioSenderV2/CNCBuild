# Controller board - KiCad

Schematic for the daughter board described in [`../../controller-board.md`](../../controller-board.md).

| File | |
|---|---|
| `controller-board.kicad_sch` | The schematic. Symbols are **embedded** (`lib_symbols`), so it needs no external libraries. |
| `controller-board.kicad_pro` | Project wrapper. |
| `netlist.txt` | The connection list, generated from the same source as the schematic. |
| `generate.py` | **The seed that produced the first version - not the live source any more.** See the warning below before re-running it. |

> 🔴 **`generate.py` is now a SEED, not the source of truth.**
> The schematic has since been **opened and re-saved by KiCad 10**, which upgraded the file format and
> may carry hand edits and layout work. **Re-running `generate.py` overwrites all of that.** Treat the
> `.kicad_sch` as the live document from here on; keep `generate.py` only as the record of how the
> netlist was derived, and if the design changes, edit in Eeschema and update `netlist.txt` to match.

## Status: verified against KiCad 10.0.5

Opened and checked with `kicad-cli`, not just written and hoped for:

| Check | Result |
|---|---|
| Parses / loads | **Yes** - `kicad-cli sch erc` and `sch export netlist` both succeed |
| Netlist matches `netlist.txt` | **Exactly.** All 15 nets, 0 mismatches, no extra or missing nodes - re-checked after KiCad re-saved the file, so connectivity survived the format upgrade |
| ERC violations | **22**, all one warning type - see below |

Reproduce with:

```
kicad-cli sch erc --severity-all --output erc-report.txt controller-board.kicad_sch
kicad-cli sch export netlist --format kicadsexpr --output kicad-export.net controller-board.kicad_sch
```

### The 22 remaining warnings are expected

All are `lib_symbol_issues`: *"The current configuration does not include the symbol library 'cnc'"*.
The symbols are embedded in the file rather than coming from a configured library, so KiCad notes it.
Nothing is broken - and the warning is arguably useful, because those symbols **are** placeholders.

An earlier run had 134 violations. The other 112 were real and are fixed:

- **107 x `endpoint_off_grid`** - placement origins were not multiples of 1.27 mm, so every pin and
  stub sat off the connection grid. Connections still resolved, but off-grid endpoints can silently
  fail to connect once a human edits the sheet. `generate.py` now snaps origins.
- **5 x `pin_not_connected`** - header pins 2 (5V), 5/7 (UART) and 6/8 (USB), which are deliberately
  unused. Now carry `no_connect` markers, which turns an error into a recorded decision.

## How it is drawn

**Connections are by net label on a short stub at each pin**, not point-to-point wires - electrically
identical for netlist and ERC purposes, and far less error-prone to generate than routing 40-odd nets
by computed coordinates. It reads as a fan-out list rather than a picture of wires, which is what the
board actually is.

## Symbols are placeholders - swap before layout

`cnc:RJ45_8`, `cnc:HDR_2x10`, `cnc:R`, `cnc:C` are minimal rectangles with correct pin numbering:
enough to carry the netlist, not real parts. Before layout, replace them with manufacturer symbols and
footprints - in particular:

- the RJ45: **shielded, NO integrated magnetics** (see the warning at the top of `controller-board.md`);
- the 2x10 header: **2.00 mm pitch**, not 2.54 mm.

`J1..J4` are X, Y, A, Z in that order; `J5` is the header to the module's `P1`.

Expect a "no power source" ERC complaint once real power symbols are used - 3V3 arrives through a
passive header pin, which is honest for a daughter board. A `PWR_FLAG` on `+3V3` and `GND` settles it.
