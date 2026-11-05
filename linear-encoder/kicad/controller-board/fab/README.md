# Controller board — fabrication and assembly package

What to send a board house for a quote, and what to tell them to populate.

Regenerate everything here with `tools/export-fab.ps1`; do not hand-edit these files.

## Board

| | |
|---|---|
| Size | **66.5 × 22.0 mm** rectangle, 2.27 sq in |
| Layers | **2** |
| Thickness | **1.6 mm** (0.062 in) — not a free choice; the stack above the module depends on it |
| Copper | 1 oz is ample for ~90 mA |
| Quantity | **3 minimum** on the Advanced Circuits prototype deal |

## It fits the Advanced Circuits $33 prototype spec

Run `tools/check-4pcb-33.ps1` after any layout change. It measures the board and
the generated drill file, so it checks what will actually be sent.

| Their limit | This board |
|---|---|
| 2 layers, FR-4, 0.062 in, 1 oz | 2 layers, 1.6 mm |
| Min 0.006 in line/space | **0.0079 in** (0.2 mm) both |
| Min 0.010 in hole | **0.0118 in** (0.3 mm) |
| **Max 35 drilled holes per sq in** | **29.1** — 66 holes in 2.27 sq in |
| Max 60 sq in | 2.27 sq in |
| No blind/buried vias | all vias go F.Cu to B.Cu |
| No slots or overlapping drill hits | no oval drills; 0.25 mm minimum hole to hole |
| No internal routing, no scoring | outline is four lines, a plain rectangle |

Hole density is the only one with real margin to lose. It is 66 holes against a
budget of 79, and the stitching vias are the only discretionary holes on the board
— **adding stitching back is what will break it.**

Two ordering constraints that are not board properties: **one part number per order**,
so do not panelise, and **three boards minimum**.

Finish is their choice — lead-free HAL, or ENIG or silver at no extra charge.
Any of the three solders fine by hand.

## Assembly — bottom side only

**Populate the 19 passives on the bottom side. Nothing on the top side.**

| Populate | |
|---|---|
| C1–C12 | 1 nF, 0603 |
| C13 | 10 µF, 0805 |
| C14 | 100 nF, 0603 |
| R1–R4 | 2.2 kΩ, 0603 |
| R5 | 0 Ω, 0603 |

**Do NOT populate — these are fitted by hand afterwards:**

| Leave empty | |
|---|---|
| J1–J4 | RJ45 jacks, top side |
| J5 | 2×10 2.00 mm header, bottom side |

Tolerance and voltage rating are not critical anywhere on this board; house-standard
parts are fine unless the quote asks for specifics.

## Files

| File | |
|---|---|
| `controller-board-gerbers.zip` | Send this for the **bare-board** quote — gerbers, drill and drill map |
| `controller-board-assembly.zip` | Send this for the **assembly** quote — `ASSEMBLY.md`, BOM and centroid |
| `ASSEMBLY.md` | What to populate and what to leave off. The vendor-facing sheet |
| `gerbers/` | The bare-board files unzipped |
| `controller-board-bottom-pos.csv` | Pick-and-place centroid, bottom side, the 19 passives only |
| `controller-board-bom.csv` | Full BOM including the parts left unpopulated — see `ASSEMBLY.md` |

**Two zips, two quotes.** The gerber zip carries no BOM, no centroid and no
statement of which parts to leave off, so it cannot be quoted for assembly on its
own. Send both.

Re-running the export restamps the KiCad creation date in every gerber, so all
thirteen files show as modified even when no copper moved. Diff before assuming a
layout change: a real change shows more than the two `CreationDate` lines.

Gerbers, drill and centroid all share one origin: the **lower-left corner of the board**,
so centroid coordinates run 0–66.5 in X and 0–22 in Y.

The BOM lists J1–J5 because it is generated from the schematic. The assembly house
needs the two tables above, not the raw BOM.
