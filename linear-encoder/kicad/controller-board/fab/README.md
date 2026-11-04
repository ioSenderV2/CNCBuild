# Controller board — fabrication and assembly package

What to send a board house for a quote, and what to tell them to populate.

Regenerate everything here with `tools/export-fab.ps1`; do not hand-edit these files.

## Board

| | |
|---|---|
| Size | **66.5 × 22.0 mm** rectangle |
| Layers | **2** |
| Thickness | **1.6 mm** — not a free choice; the stack above the module depends on it |
| Quantity | *set at quote* |

Everything below is inside standard spec at every house — no fine-feature surcharge
should apply:

| Constraint | Design value |
|---|---|
| Minimum trace width | 0.2 mm |
| Minimum clearance | 0.2 mm |
| Minimum drill | 0.3 mm |
| Minimum annular ring | 0.15 mm |
| Copper to board edge | 0.5 mm |

Not fixed by the design — choose at quote: copper weight (1 oz is ample for ~90 mA),
surface finish, solder mask and silkscreen colour.

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
| `controller-board-gerbers.zip` | Upload this for the bare-board quote — gerbers, drill and drill map |
| `gerbers/` | The same files unzipped |
| `controller-board-bottom-pos.csv` | Pick-and-place centroid, bottom side, the 19 passives only |
| `controller-board-bom.csv` | Full BOM including the parts left unpopulated — see the tables above |

Gerbers, drill and centroid all share one origin: the **lower-left corner of the board**,
so centroid coordinates run 0–66.5 in X and 0–22 in Y.

The BOM lists J1–J5 because it is generated from the schematic. The assembly house
needs the two tables above, not the raw BOM.
