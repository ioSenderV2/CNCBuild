# Controller board — fabrication and assembly package

What to send a board house for a quote, and what to tell them to populate.

Regenerate everything here with `tools/export-fab.ps1`; do not hand-edit these files.

## Board

| | |
|---|---|
| Size | **66.5 × 28.0 mm** rectangle, 2.89 sq in |
| Layers | **2** |
| Thickness | **1.6 mm** (0.062 in) — not a free choice; the stack above the module depends on it |
| Copper | 1 oz is ample for ~90 mA |
| **Plated slots** | **3**, each 1.6 × 2.6 mm, between the RJ45 jacks — each takes two adjacent shield tabs. **The fab must do plated slots.** |

## The Advanced Circuits $33 prototype deal no longer fits

`tools/check-4pcb-33.ps1` (run it after any layout change) passes everything
except **No slots: FAIL — 3 oval drills.** The 2026-11-19 re-layout to
through-hole 85508 jacks at butted pitch forces adjacent shield tabs to share a
plated slot, and the $33 spec excludes slots outright. For the record, the rest
of the spec still clears: 0.2 mm line/space, 0.3 mm min hole, 89 holes = 30.8
per sq in against 35, plain rectangular outline, through vias only.

**The board needs a fab that does plated slots** (OSH Park does, and the board
already meets their 0.38 mm copper-to-edge). Vendor not yet chosen — his call.

## Assembly — bottom side only

**Populate the 18 passives on the bottom side. Nothing on the top side.**

| Populate | |
|---|---|
| C1–C12 | 1 nF, 0603 |
| C13 | 10 µF, 0805 |
| C14 | 100 nF, 0603 |
| R1–R4 | 2.2 kΩ, 0603 |

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
| `controller-board-bottom-pos.csv` | Pick-and-place centroid, bottom side, the 18 passives only |
| `controller-board-bom.csv` | Full BOM including the parts left unpopulated — see `ASSEMBLY.md` |

**Two zips, two quotes.** The gerber zip carries no BOM, no centroid and no
statement of which parts to leave off, so it cannot be quoted for assembly on its
own. Send both.

Re-running the export restamps the KiCad creation date in every gerber, so all
thirteen files show as modified even when no copper moved. Diff before assuming a
layout change: a real change shows more than the two `CreationDate` lines.

Gerbers, drill and centroid all share one origin: the **lower-left corner of the board**,
so centroid coordinates run 0–66.5 in X and 0–28 in Y.

The BOM lists J1–J5 because it is generated from the schematic. The assembly house
needs the two tables above, not the raw BOM.
