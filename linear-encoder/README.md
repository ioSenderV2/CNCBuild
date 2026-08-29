# Linear scale position feedback

Magnetic linear scales on each axis, read by AS5311 sensors, decoded to positions by an ESP32-S3, sent
over CAN to the Teensy, so grblHAL knows where each axis **actually** is. Status: **design only, nothing
built.**

| File | What it is |
|---|---|
| **[`design-can-position-feedback.md`](design-can-position-feedback.md)** | **Start here.** The whole design: scope, the sensors, the machine's layout, staleness, the CAN frame, grblHAL integration, failure modes, phasing, and the wiring (§14). |
| [`controller-board.md`](controller-board.md) | The 4-jack daughter board that sits over the ESP32 module: the no-magnetics rule, the mechanical envelope, and the 5 mm-pin / 14 mm-standoff problem. |
| [`sensor-board.md`](sensor-board.md) | The AS5311 board in the puck: what goes on each face, the passives, and the connector question the layout is waiting on. |
| [`hardware-esp32-s3-rs485-can.md`](hardware-esp32-s3-rs485-can.md) | The ESP32 module's 20-pin header map - **not documented on the Waveshare wiki**, only in the schematic. |
| [`kicad/controller-board/`](kicad/controller-board/) | KiCad project. Schematic drawn and verified against KiCad 10.0.5; **no layout yet**, and the symbols are placeholders to be swapped for real parts. |
| [`kicad/sensor-board/`](kicad/sensor-board/) | KiCad project. Schematic drawn and verified the same way; **no layout yet**, and the connector footprint is deliberately unresolved (see `sensor-board.md`). |
| [`../manufacturer-assets/`](../manufacturer-assets/index.html) | The AS5311 datasheet (rev 1.12) and the module schematic. **Untracked** - third-party documents in a public repo. The tracked `index.html` there records where each came from, including the browser-User-Agent trick both waveshare.com URLs need. |

The datasheets are **kept on disk on purpose**: the header map was extracted once, lost, and had to be
found again. A link is not a copy - but nor is someone else's document ours to republish, so the files
stay untracked and `../manufacturer-assets/index.html` records how to fetch each one.

## What is not here yet

- **Both PCB layouts.** Two schematics exist and both pass ERC, but nothing has been placed or routed,
  and every symbol is still a placeholder carrying the netlist rather than a real part.
- **The ESP32-S3 firmware**, and the grblHAL plugin at the other end of the CAN link.
- **The puck-mount mechanical drawings** - the 35 mm round, the 30 mm bore, and the anti-rotation
  fix that §1.4 leaves open.

An earlier note here said that when the first of these landed the work would probably want its own
repo, away from the firmware fork. That has happened: this **is** that repo.
