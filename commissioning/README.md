# Commissioning measurements

**Measured from the machine.** This folder outranks any configuration file - see the standing rule in the
[root README](../README.md).

**Recorded so far:** [`masses.md`](masses.md) - the four moving assemblies, weighed 2026-09-26, and
[`base-as-built.md`](base-as-built.md) - the base's measured width, wall, tenon span and the bottom
skin's dry fit. **The remaining base parts get cut to that file, not to the registry.**

**Do first:** [`bench-session.md`](bench-session.md) - it needs no machine, and it is the only item
here that gets harder once the build moves on.

Nothing else has been recorded. What needs measuring, and why it matters:

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

## Rail voltage, and what the drives draw

PROCEDURE: **[`bench-session.md`](bench-session.md)** - the full procedure, and **it needs no
assembled axis**. Four motors loose on the bench answer the supply-sizing question, the power-on
inrush question, whether the alarm really asserts when healthy, and how a fault clears.

**Do it before the plates are machined.** An uncoupled motor is the best test rig this build will
have and it exists now; provoking a fault later means moving a gantry to do it.

It also settles a figure that is a **setting rather than a property**: the motor supply's output is
variable, so its 36 V is exactly the kind of number the $130 fault above was. Measured at a drive's
own terminals, not read off the supply's label.

## Stiffness and lost motion

PROCEDURE: **[`stiffness-test.md`](stiffness-test.md)** - the full procedure. Push the spindle nose with a
known force and read six indicator positions, so the deflection can be attributed to a subassembly
rather than lumped into one number.

**It settles the 1/4" vs 3/8" X beam plate choice**, which was decided on the *claim* that the Z
assembly is the largest compliance in the stack. It also gives the gantry's torsional stiffness, which
cannot be computed - 8020 do not publish J - and the lost motion, which matters more than either.

## Squaring and backlash

Y1/Y2 squaring is `Y_AUTO_SQUARE`, so it is set at homing; a loose Y pinion set screw has caused a real
squaring fault before. Record measurements here when taken.
