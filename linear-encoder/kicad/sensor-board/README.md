# Sensor board - KiCad

Schematic for the board described in [`../../sensor-board.md`](../../sensor-board.md).

| File | |
|---|---|
| `sensor-board.kicad_sch` | The schematic. Symbols are **embedded** (`lib_symbols`), so it needs no external libraries. |
| `sensor-board.kicad_pro` | Project wrapper. |
| `netlist.txt` | The connection list, generated from the same source as the schematic. |
| `generate.py` | The seed that produced the first version. See the warning below. |

> 🔴 **`generate.py` is already a SEED, not the source of truth - as of 2026-08-29.**
> It took one `kicad-cli sch erc` run: the tool **re-saves the schematic**, upgrading it from the
> `version 20231120` header the script writes to KiCad 10's own format (and to CRLF, which
> `.gitattributes` normalises back to LF on commit). Nobody opened Eeschema; running the checks was
> enough. **Re-running `generate.py` now overwrites whatever KiCad wrote, including any layout or
> hand edits.** Treat the `.kicad_sch` as the live document, keep the script as the record of how the
> netlist was derived, and if the design changes, edit in Eeschema and update `netlist.txt` to match.
>
> Connectivity was re-checked **after** the upgrade: all 12 nets and every node still identical, and
> all 9 `no_connect` markers intact. The format change carried the design across without loss.

## Status: verified against KiCad 10.0.5

Checked with `kicad-cli`, not just written and hoped for:

| Check | Result |
|---|---|
| Parses / loads | **Yes** - `sch erc` and `sch export netlist` both succeed |
| Netlist matches `netlist.txt` | **Exactly.** All 12 connected nets, every node identical, nothing extra or missing |
| `no_connect` coverage | **9 pins - 1, 6, 7, 10, 11, 15, 16, 17, 20** - exactly the datasheet's NC list plus Index and PWM |
| ERC violations | **12**, all one warning type - see below |

Reproduce with:

```
kicad-cli sch erc --severity-all --output erc-report.txt sensor-board.kicad_sch
kicad-cli sch export netlist --format kicadsexpr --output kicad-export.net sensor-board.kicad_sch
```

### The 12 violations are all expected

Every one is `lib_symbol_issues`: *"The current configuration does not include the symbol library
'cnc'"*. The symbols are embedded in the file rather than coming from a configured library, so KiCad
notes it. Nothing is broken - and as on the controller board the warning is arguably useful, because
those symbols **are** placeholders.

## Symbols are placeholders - swap before layout

`cnc:AS5311`, `cnc:RJ45_8_UNSHLD`, `cnc:TVS_4`, `cnc:R`, `cnc:C`, `cnc:TP` are minimal rectangles with
correct pin numbering and, on the AS5311, correct pin names from datasheet Table 1. Enough to carry
the netlist; not real parts. Before layout:

- **The RJ45 footprint is the open question, not a detail.** Unshielded, vertical, no magnetics - and
  whether it can be through-hole at all is unresolved. `../../sensor-board.md` has the height budget
  and the options. **Do not lay this board out until that is settled**, because it decides the part.
- **The AS5311 footprint is the one dimension that matters.** The datasheet's recommended land
  pattern is A 7.00, B 5.00, C 0.38, D 0.65, E 6.23 mm (rev 1.12 §9.1, Fig 18). What actually decides
  accuracy is the **Hall array position relative to the mounting datum**, from Figure 14 - and that
  figure was read off a rendered page, so confirm the reference edges first.
- Expect a "no power source" ERC complaint once real power symbols are used: `+3V3` arrives through
  a passive connector pin, which is honest for a board at the end of a cable. A `PWR_FLAG` settles it.

## How it is drawn

**Connections are by net label on a short stub at each pin**, not point-to-point wires - the same
convention as the controller board, for the same reason. It reads as a fan-out list, which is what
the board is.

Net names ending `_SRC` are the chip side of a series resistor; the bare name is the cable side. So
`A_SRC` is `U1` pin 4, `A` is what reaches the jack.
