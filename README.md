# CNCBuild

The machine: a **Mega V XL**, and everything about building, wiring, configuring and instrumenting it.

Written down because these facts kept getting re-derived in conversation - travels, plate dimensions,
what shares a drag chain, which stored setting disagreed with the machine. A firmware fork's scratch
folder was the wrong home for them.

| Folder | What is in it |
|---|---|
| [`machine/`](machine/) | The build itself: extrusions, rails, screws, plates, and the mechanical decisions with their reasons |
| [`linear-encoder/`](linear-encoder/) | Magnetic linear scales + AS5311 + ESP32-S3 → CAN → grblHAL. The most developed subsystem; design complete, nothing built |
| [`commissioning/`](commissioning/) | Measurements taken **from the machine** - travels, squaring, tape extents. The authority when the config disagrees |

## What lives elsewhere

| | Where | Why |
|---|---|---|
| grblHAL firmware + the CAN plugin | `stevenrwood/iMXRT1062`, branch `srw/local-build-config` | It is firmware and needs that build tree |
| ioSender (the sender application) | `ioSenderV2/ioSender` | Its own product |

## A standing rule for this repo

**The machine is the authority, not the configuration.** `$130` once read 889 mm against a real 860 mm,
because a catalog preset overwrote a measured value - which quietly cost soft-limit protection until it
was found by accident. Anything in `commissioning/` is measured; anything quoted from a config file is
labelled as such.

Datasheets are **committed, not linked**. The ESP32 module's header pinout was extracted once, lost, and
had to be recovered from a schematic - and both of that vendor's URLs refuse a plain fetch. A link is not
a copy.
