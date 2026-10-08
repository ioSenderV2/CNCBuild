# CNCBuild

The machine, and everything about building, wiring, configuring and instrumenting it. Gantry beams are
**stacked pairs of 8020 `30-6060`** on HGR20 rails and 1605 ball screws.

Written down because these facts kept getting re-derived in conversation - travels, plate dimensions,
what shares a drag chain, which stored setting disagreed with the machine. A firmware fork's scratch
folder was the wrong home for them.

| Folder | What is in it |
|---|---|
| [`machine/`](machine/) | The build itself: extrusions, rails, screws, plates, and the mechanical decisions with their reasons |
| [`linear-encoder/`](linear-encoder/) | Magnetic linear scales + AS5311 + ESP32-S3 → CAN → grblHAL. The most developed subsystem; design complete, nothing built |
| [`commissioning/`](commissioning/) | Measurements taken **from the machine** - travels, squaring, tape extents. The authority when the config disagrees |
| [`wiring/`](wiring/) | How the boxes connect - the DB37 between the controller box and the remote axis breakout box |

## Generated views - regenerate, never edit

Three files are built from the prose rather than maintained beside it, because a
hand-maintained summary drifts from what it summarises. That is not hypothetical here: on
2026-10-02 two settled decisions were relitigated, both because a pointer had gone stale.

| Build it with | What you get |
|---|---|
| `python tools/status.py all` | [`STATUS.md`](STATUS.md) - every open item, harvested from the ✅ ⚠️ 🔴 ❌ markers in the prose. [`INDEX.md`](INDEX.md) - every heading in the repo |
| `tools\make-pdf.ps1` | **`build-document.pdf`** - the whole mechanical design as one printable file: the thirteen `machine/*.md` files in reading order, a clickable contents, all fifteen photographs embedded with their captions, and links into the shop pack. ~4.4 MB, 97 pages. **Untracked** - rebuild it, do not commit it |

**If a generated file and a `.md` file disagree, the `.md` file wins** and the generated copy
is stale. The PDF needs two packages - `python -m pip install markdown pillow` - the first to
render the prose, the second to scale the photographs to print size on the way in (22.9 MB of
originals become 4.4 MB of PDF, still over 300 dpi at the size they are printed; the originals
in `machine/photos/` are never touched). `status.py` is stdlib-only on purpose, because it
gates correctness and the PDF does not.

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
