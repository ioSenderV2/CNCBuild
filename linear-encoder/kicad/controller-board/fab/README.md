# Controller board — fabrication and assembly package

What to send for quotes, split by vendor. Two packages are built from one plot
pass, so they cannot drift apart.

Regenerate everything here with `tools/export-fab.ps1`; do not hand-edit anything
under `fab/` except this file and `ASSEMBLY.md`.

## Board

| | |
|---|---|
| Size | **70.0 × 28.0 mm** rectangle, 3.04 sq in |
| Layers | **2** |
| Thickness | **1.6 mm** (0.062 in) — not a free choice; the stack above the module depends on it |
| Copper | 1 oz is ample for ~90 mA |
| Drill | 89 holes, min 0.3 mm, all round — no slots, no blind/buried vias |
| Line/space | 0.2 mm both |

## OSH Park — bare boards

Upload **`oshpark/controller-board-gerbers.zip`**. OSH Park does no assembly, so
that zip is the whole package; they also accept the KiCad board file
(`../controller-board.kicad_pcb`) directly, which is even less to go wrong.
Boards come in multiples of three.

## PCBWay — boards plus assembly

The `pcbway/` folder holds the four pieces their quote flow asks for:

| File | |
|---|---|
| `controller-board-gerbers.zip` | The board quote — gerbers, drill and drill map |
| `controller-board-bom-smd.csv` | **SMD parts only** — the 18 passives they populate. The through-hole connectors (J1–J5) are deliberately absent: customer-fitted |
| `controller-board-centroid.csv` | Pick-and-place, bottom side, their column names, same 18 parts |
| `ASSEMBLY.md` | The populate / do-not-populate sheet in prose |

No manufacturer part numbers are given: tolerance and voltage rating are not
critical anywhere on this board, so their house-standard 0603/0805 stock is fine
— the BOM says so in its Description column.

## Assembly — bottom side only

**All 18 placed parts are on the bottom side. Nothing is placed on the top side.**

| Populate | |
|---|---|
| C1–C12 | 1 nF, 0603 |
| C13 | 10 µF, 0805 |
| C14 | 100 nF, 0603 |
| R1–R4 | 2.2 kΩ, 0603 |

**Do NOT populate — fitted by hand afterwards:** J1–J4 (RJ45 jacks, top side)
and J5 (2×10 2.00 mm header, bottom side).

## Files at the root of fab/

| File | |
|---|---|
| `controller-board-gerbers.zip` | The vendor-neutral bare-board zip (same bytes as both vendor copies) |
| `controller-board-assembly.zip` | `ASSEMBLY.md` + full BOM + centroid, for any other assembly quote |
| `controller-board-bom.csv` | Full BOM including J1–J5, straight from the schematic |
| `controller-board-bottom-pos.csv` | Centroid in KiCad's own column names |
| `gerbers/` | The bare-board files unzipped |

For the record: the board also still clears the Advanced Circuits $33 prototype
spec — `tools/check-4pcb-33.ps1` measures the board and drill file and passes
everything — should that route ever be wanted again.

Re-running the export restamps the KiCad creation date in every gerber, so all
the files show as modified even when no copper moved. Diff before assuming a
layout change: a real change shows more than the two `CreationDate` lines.

Gerbers, drill and centroid all share one origin: the **lower-left corner of the
board**, so centroid coordinates run 0–70 in X and 0–28 in Y.
