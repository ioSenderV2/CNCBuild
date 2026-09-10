# The DB37 axis interconnect

The per-axis back-panel connections live in a **remote breakout box**, not on the controller box.
One **1.5 m DB37 cable** carries every axis signal between the two.

**DB37 female at both boxes**, so the cable is male-male. That is deliberate: a symmetric M-M lead
cannot be plugged in the wrong way round, and there is only one cable to get wrong.

Settled 2026-09-10. The pinout below is a decision, not a measurement - nothing here has been built
or metered yet.

## Six conductors per axis

| | Direction | Notes |
|---|---|---|
| **Step** | controller → driver | The fast edge. The only real aggressor on the cable |
| **Dir** | controller → driver | |
| **EN** | controller → driver | Per axis, not commoned across drivers |
| **GND** | shared | The commoned cathode rail - see below |
| **AL** | driver → controller | Closed-loop driver alarm |
| **Limit** | switch → controller | **NC.** See [fail-closed](#the-connector-fails-in-the-right-direction) |

The driver's Step/Dir/EN inputs are **opto pairs wired common-cathode (sinking)**: the `-` side of
each opto is tied to the shared GND and the controller sources current into the `+` side. That is
what makes a single GND per axis sufficient - it is not just a return, it is the reference the
optos are commoned to.

## The pinout

Five axis blocks. Four are in use (X, Y, A, Z); **B is wired and unused**, so a fifth motor channel
costs a plug, not a re-terminate.

Five blocks of six is **30 pins of 37**, leaving **7 spare**.

### Row A - pins 1-19

| Axis | Step | Dir | EN | GND | AL | Limit |
|---|---|---|---|---|---|---|
| **X** | 1 | 2 | 3 | 4 | 5 | 6 |
| **Y** | 7 | 8 | 9 | 10 | 11 | 12 |
| **A** (Y2, M3) | 13 | 14 | 15 | 16 | 17 | 18 |

Pin **19** - spare

### Row B - pins 20-37

| Axis | Step | Dir | EN | GND | AL | Limit |
|---|---|---|---|---|---|---|
| **Z** | 20 | 21 | 22 | 23 | 24 | 25 |
| **B** (M4, reserved) | 26 | 27 | 28 | 29 | 30 | 31 |

Pins **32-37** - spare

## Why the map looks like this

### One contiguous block per axis

Each axis is an unbroken run of six pins, so one field cable maps to one range. It is wired in
order, labelled in order, and fault-found with a meter by counting rather than by reading a table.
Any scheme that interleaved axes would trade that away for a noise margin this run does not need.

### GND at position 4

With **one** shared return per axis its position is a compromise, and putting it in the middle
minimises the worst-case loop area for any signal in the block. It also lands between the three
driven outputs and the two sensed inputs.

This is a second-order effect at 1.5 m behind a shield. It is done because it is free, not because
it is load-bearing.

### One GND per axis, and what it trades

The alternative - a return conductor adjacent to every signal - would have used all 37 pins and
left nothing for a fifth axis. **The fifth axis won.** The shield and the short run are doing the
noise work here; the returns are doing the referencing.

Chosen deliberately, so it does not want re-arguing. What it costs is documented below.

### ⚠️ Two Step/Limit adjacencies, known and accepted

The DB37's rows are staggered - **pin 20 sits physically between pins 1 and 2** - so a block in row
B straddles two blocks in row A. Physical neighbours are diagonal, not numeric.

That leaves two places where a fast output sits next to a high-impedance input:

| | is physically next to | |
|---|---|---|
| Pin 25 - **Z Limit** | ↔ | Pin 7 - **Y Step** |
| Pin 31 - **B Limit** | ↔ | Pin 13 - **A Step** |

With 30 of 37 pins spoken for there is no slack to guard both, and shuffling the map to dodge them
would cost the contiguous-block property that makes it wirable. Written down because a phantom hard
limit on Z or B is the failure this would produce, and it reads exactly like a mechanical fault -
which sends you to the gantry instead of to the cable.

**B is unused, so in practice only the Z one is live.**

## The cable

The cable decides whether this works. Ordering by pin count alone is how it goes wrong.

- **Straight-through, pin 1 ↔ pin 1.** Some DB37 M-M leads are wired crossover. Verify from the
  datasheet, not the listing title.
- **Overall braid shield, bonded to the metal backshell** at both ends. Both boxes share a safety
  earth, so a chassis-to-chassis bond over 1.5 m is what you want - not a single-ended shield.
- Not ribbon.

## The connector fails in the right direction

The limit switches are **NC** - settled in
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md),
§3, *Fail-closed versus fail-open*.

So pulling the DB37 opens every limit at once and the machine faults. Concentrating all four axes
into a single connector would be a real objection if the limits were NO; with NC it is the correct
direction to fail, and the same argument that kept the switches applies to the connector carrying
them.

## ⚠️ Open

Not guessed. Each needs an answer off the bench before the box is built.

1. **Controller-side source current.** Common-cathode means the controller *sources* the opto
   current, typically 8-16 mA per input. What buffers the Teensy's 3.3 V pins has not been checked.
   The failure signature is Step working at low feed and dropping pulses at high - meter it before
   trusting it.
2. **What physically terminates in the breakout box per axis.** One connector carrying all six, or
   the driver signals and the limit switch arriving on separate cables? Decides the box's front
   panel.
3. **Where the drivers sit.** The DB37 carries controller↔driver logic, which puts the drivers at
   the machine end rather than in the controller box - stated here as the reading, not as a fact.
4. **Spare pin allocation.** Seven pins (19, 32-37) are unassigned. Probe, spindle and E-stop have
   not been considered against them.
