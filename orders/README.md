# Orders

One row per order. **The PDFs sit in this folder on his disk and are not in git** - an
invoice carries a name, a home address, an email and sometimes an order-access link, and
this repo is public. Drop the PDF here, add the row; `.gitignore` keeps the file out.

| Date | Vendor | Order | What | Total | For | PDF (local only) |
|---|---|---|---|---|---|---|
| 2026-11-02 | Mouser | web 40971389, sales 282784271 | Molex Mini-Fit Jr headers: 10x 39-31-0027, 10x 46999-0621, 10x 39-29-9027 | $36.58 | [interface board](../wiring/kicad/interface-board/README.md) | `282784271.pdf` |
| 2026-11-03 | Mouser | web 40971773, sales 282784945 | 20x Molex 39-30-1039 3P header, 10x 85508-5001 RJ45 jack | $75.23 | [interface board](../wiring/kicad/interface-board/README.md) | `282784945.pdf` |
| 2026-11-03 | OSH Park | xPBWS3rt | Interface board Rev A, 3 boards, $152.95 + $12.00 FedEx 2 Day | $164.95 | [interface board](../wiring/kicad/interface-board/README.md) | `oshpark-order-invoice-xPBWS3rt.pdf` |
| 2026-11-04 | OSH Park | nonwzU9u | Sensor board, 6 boards (2 sets of 3), $18.90 + $8.60 USPS Priority | $27.50 | [sensor board](../linear-encoder/sensor-board.md) | `oshpark-order-invoice-nonwzU9u.pdf` |
| 2026-11-04 | Digi-Key | 102688952 (from the export's filename) | 4x Sullins NPPN102AFCN-RC 2x10 socket, 2.0 mm (S5750-10-ND), $6.24 subtotal | $16.50 delivered, per the controller board notes | [CAN controller board](../linear-encoder/controller-board.md) socket bench test | `DK_PRODUCTS_102688952.csv` |
| 2026-11-13 | Mouser | web 41109063, sales 282984374 | Extras of the same headers: 20x 46999-0621, 25x 39-29-9027, 25x 39-30-1039 | $59.13 | [interface board](../wiring/kicad/interface-board/README.md) | `282984374.pdf` |
| 2026-11-14 | Mouser | web 41110345 | Phoenix Contact: 24x PT 4-QUATTRO (3211797), 4x FBS 10-6 bridge (3030271), 5x D-PT 4-QUATTRO end cover (3208979), 3x ATP-ST QUATTRO partition plate (3030815), 2x CLIPFIX 35 end bracket (3022218) | $163.30 | 36 V distribution on the DIN rail beside the XDR | `Order_41110345.pdf` |

Mouser files its PDFs under the **sales** order number; the project's notes quote the
**web** order number. Both are in the Order column.

SETTLED: **THE QUANTITIES ARE DOUBLED ON PURPOSE - his, 2026-11-14.** The Mega V gets
converted to the same wiring setup before he sells it, so the 2026-11-13 header order and
the Phoenix order each cover two machines: 24 PT 4-QUATTRO is 12 per machine, and 4 FBS
10-6 is one per 36 V leg per machine.

## Mouser parts across all four orders

| Part | Orders | Total bought |
|---|---|---|
| Molex 46999-0621 | 40971389 (10), 41109063 (20) | 30 |
| Molex 39-29-9027 | 40971389 (10), 41109063 (25) | 35 |
| Molex 39-30-1039 | 40971773 (20), 41109063 (25) | 45 |
| Molex 39-31-0027 | 40971389 (10) | 10 |
| Molex 85508-5001 | 40971773 (10) | 10 |

FLAG: **46999-0621 IS A 2-CIRCUIT HEADER BY MOLEX'S OWN DRAWING - and this file said the
opposite for an hour on 2026-11-14.** Sales drawing 55660021-SD sheet 3, matte tin, 94V-0
natural: **46999-0621 = 5566-02A2MS-210, 2 circuits**; the 4-circuit in that column is
**46999-0502**. That matches Mouser's "Dual Row, 2 Pos., 94V-0, Matte Tin" word for word.
The 2x2 reading came from Mouser's product photo, which is marked "for reference only" -
a signal, not the part. 30 are bought; if the drawing is right, **no 4-circuit header has
been ordered** and the interface board needs three per board (J15, J32, J33). The bag
settles it: two pins or four.

The two OSH Park invoices were committed beside their gerbers until 2026-11-14 and were
moved here that day. They are still in the git history before that date.
