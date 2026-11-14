# Orders

One row per order. **The PDFs sit in this folder on his disk and are not in git** - an
invoice carries a name, a home address, an email and sometimes an order-access link, and
this repo is public. Drop the PDF here, add the row; `.gitignore` keeps the file out.

| Date | Vendor | Order | What | For | PDF (local only) |
|---|---|---|---|---|---|
| 2026-11-02 | Mouser | 40971389 | Molex Mini-Fit Jr headers: 10x 46999-0621 (2x2), 10x 39-29-9027 (2P with peg), 10x 39-31-0027 (2P no peg) | [interface board](../wiring/kicad/interface-board/README.md) | not saved |
| 2026-11-03 | Mouser | 40971773 | 10x Molex 85508-5001 RJ45 jack, 20x 39-30-1039 3P header | [interface board](../wiring/kicad/interface-board/README.md) | not saved |
| 2026-11-03 | OSH Park | xPBWS3rt | Interface board Rev A, 3 boards, $152.95 + $12.00 FedEx 2 Day = $164.95 | [interface board](../wiring/kicad/interface-board/README.md) | `oshpark-order-invoice-xPBWS3rt.pdf` |
| 2026-11-04 | OSH Park | nonwzU9u | Sensor board, 6 boards (2 sets of 3), $18.90 + $8.60 USPS Priority = $27.50 | [sensor board](../linear-encoder/sensor-board.md) | `oshpark-order-invoice-nonwzU9u.pdf` |
| 2026-11-14 | not recorded | not recorded | Phoenix Contact PT 4-QUATTRO (3211797) terminal blocks and FBS bridges - quantities not recorded | 36 V distribution on the DIN rail beside the XDR | not saved |

The two OSH Park invoices were committed beside their gerbers until 2026-11-14 and were
moved here that day. They are still in the git history before that date.
