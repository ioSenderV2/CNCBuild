# Commissioning measurements

**Measured from the machine.** This folder outranks any configuration file - see the standing rule in the
[root README](../README.md).

Nothing has been recorded yet. What needs measuring, and why it matters:

## Travels, per axis

Jog to each hard stop and read the position. Do **not** take these from `$130`/`$131`/`$132`: `$130` read
**889 mm against a real 860 mm** because a catalog preset overwrote the measured value, and the
disagreement went unnoticed while soft-limit protection was quietly absent.

| Axis | Travel | Measured on | Notes |
|---|---|---|---|
| X | | | |
| Y | | | |
| A | | | |
| Z | | | |

## Tape extents, per axis

Needed before cutting magnetic tape, which is one-shot PSA. The tape must span the range the **sensor
bore** sweeps - not the extrusion, not the plate - and the bore may not be centred on its plate, which
shifts the tape's *start* as well as its length.

1. Jog to one hard stop; mark the extrusion at the sensor bore's centreline.
2. Jog to the other stop; mark again.
3. Cut and lay mark-to-mark plus ~10 mm beyond each end.

| Axis | Mark A | Mark B | Tape cut | Laid on |
|---|---|---|---|---|
| X | | | | |
| Y | | | | |
| A | | | | |
| Z | | | | |

Budget: 3 m in stock, three long axes plus Z. **No long run can be recut** - cut the long axes first and
err long rather than short.

## Squaring and backlash

Y1/Y2 squaring is `Y_AUTO_SQUARE`, so it is set at homing; a loose Y pinion set screw has caused a real
squaring fault before. Record measurements here when taken.
