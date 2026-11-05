# Controller board — assembly instructions

Board: **controller-board**, 66.5 × 22.0 mm, 2 layers, 1.6 mm.

## Populate the bottom side only

All nineteen parts are on the **bottom** side. Nothing is placed on the top side.

| Designators | Value | Package | Qty |
|---|---|---|---|
| C1–C12 | 1 nF | 0603 | 12 |
| C13 | 10 µF | 0805 | 1 |
| C14 | 100 nF | 0603 | 1 |
| R1–R4 | 2.2 kΩ | 0603 | 4 |
| R5 | 0 Ω | 0603 | 1 |

Tolerance and voltage rating are not critical anywhere on this board. House-standard
parts are fine; please quote with your own stock.

## Do not populate

| Designators | Part | |
|---|---|---|
| J1, J2, J3, J4 | RJ45 jack, top side | fitted by the customer |
| J5 | 2×10 2.00 mm header, bottom side | fitted by the customer |

These five are hand-soldered after delivery. Leave the pads bare — no parts, no
paste needed on the top side.

## Files

| File | |
|---|---|
| `controller-board-bom.csv` | Bill of materials. It lists J1–J5 as well, because it comes from the schematic — use the two tables above, not the raw BOM. |
| `controller-board-bottom-pos.csv` | Pick-and-place centroid. Contains only the nineteen parts to be placed. |

Centroid coordinates are in millimetres from the **lower-left corner of the board**,
X running 0–66.5 and Y running 0–22. The gerbers and drill file sent for the board
quote share that same origin, and include the paste layers.
