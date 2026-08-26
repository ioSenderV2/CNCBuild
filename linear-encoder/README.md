# Linear scale position feedback

Magnetic linear scales on each axis, read by AS5311 sensors, decoded to positions by an ESP32-S3, sent
over CAN to the Teensy, so grblHAL knows where each axis **actually** is. Status: **design only, nothing
built.**

| File | What it is |
|---|---|
| **[`design-can-position-feedback.md`](design-can-position-feedback.md)** | **Start here.** The whole design: scope, the sensors, the machine's layout, staleness, the CAN frame, grblHAL integration, failure modes, phasing, and the wiring (§14). |
| [`hardware-esp32-s3-rs485-can.md`](hardware-esp32-s3-rs485-can.md) | The ESP32 module's 20-pin header map - **not documented on the Waveshare wiki**, only in the schematic. |
| [`../manufacturer-assets/`](../manufacturer-assets/index.html) | The AS5311 datasheet (rev 1.12) and the module schematic. **Untracked** - third-party documents in a public repo. The tracked `index.html` there records where each came from, including the browser-User-Agent trick both waveshare.com URLs need. |

The datasheets are **kept on disk on purpose**: the header map was extracted once, lost, and had to be
found again. A link is not a copy - but nor is someone else's document ours to republish, so the files
stay untracked and `../manufacturer-assets/index.html` records how to fetch each one.

## What is not here yet

The ESP32-S3 firmware, the two PCB projects (the sensor board and the 4-jack controller board) and the
mechanical drawings for the puck mount. **When the first of those lands, this probably wants its own
repo** - only the grblHAL plugin genuinely belongs in this firmware tree, and this one is a fork with a
submodule web that made it awkward enough to migrate once already. Design docs are cheap to keep beside
the plugin; a KiCad project and a second firmware are not.
