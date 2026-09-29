# The remote breakout box

Every per-axis connection terminates here rather than on the controller box's back panel. The
controller box keeps the logic and nothing else - it does not even hold its own supply.

Settled 2026-09-10. Decisions, not measurements; nothing has been built or metered.

## What is in it

| | |
|---|---|
| **48 V, 600 W** power supply | Motor power. 12.5 A across all axes |
| **12 V, 3 A** buck | Limit sensors, and the relays in the controller box |
| **5 V, 3 A** buck | The controller box's logic supply |
| **DB37 breakout board** | Fans the [DB37 interconnect](db37-axis-interconnect.md) out to the back-panel connectors |

**The boxes share a common ground.** The 5 V and 12 V returns, the DB37 per-axis GNDs and the 48 V
return are all one node - which is what makes a single GND per axis in the DB37 sufficient, and
also what makes the next section matter.

## ⚠️ Star the 48 V returns

**The one wiring order that decides whether the signals are clean.**

Each axis's GND sits in the same 6-pin shell as its 48 V, so that conductor carries motor return
current - several amps, chopped by the drive - and it is *also* the reference the drive's optos are
commoned to.

- **Right:** every stepper GND lands on the **PSU negative terminal directly**. Motor current never
  crosses the signal reference.
- **Wrong:** the stepper GNDs daisy-chain through the DB37 breakout board's ground terminals. Then
  the IR drop from every axis's motor current appears as common mode on Step, Dir, AL and Limit.

Same parts, same cost, same afternoon. Only the order the rings go onto the stud differs. Written
down because the wrong version works fine on the bench with the motors idle.

For contrast, the controller's 5 V return *does* run in parallel with the five DB37 GND pins, and
that is fine: at plausible gauges it puts the two ground nodes tens of millivolts apart, against an
opto threshold of about 1.2 V. Not worth engineering around.

## Back panel - Molex Mini-Fit Jr, panel-mount female

Two connectors per axis.

### Stepper, 6P

**AL, EN, Step, Dir, 48 V, GND** - on **18 AWG**, 6 conductor.

The steppers are **integrated closed-loop units**: the drive is at the motor, so what leaves the box
is logic plus motor supply, not motor phases.

> **If the steppers were ordinary open-loop motors**, the drivers would sit in the breakout box and
> this same 6P shell would carry **AL, EN, A+, A−, B+, B−** - phases, not logic. Recorded because
> the connector count and the cable are identical, so a future swap looks like a drop-in and is not
> one: it moves the switching currents out onto the drag-chain cable.

### Limit, 3P

**12 V, Limit, GND** - three-wire inductive proximity sensor, powered from the 12 V buck.

The part is an **SN04-N** (Haldzemo, 4-pack). Datasheet in
[`../manufacturer-assets/`](../manufacturer-assets/) - read off the drawing, not the listing:

| | |
|---|---|
| Supply | 6-36 V DC. **12 V is inside range** |
| Output | **NPN, normally open.** Open collector - "switched negative" |
| Max load | 300 mA |
| Response frequency | **500 Hz** |
| Detect range | 0-4 mm, non-shielded |
| Captive cable | **1.2 m** |
| Protection | IP67 |

Wire colours: **brown = +V, black = output, blue = 0 V.**

**There is no internal pull-up.** The datasheet's terminal drawing puts the load between black and
+V, and the NPN configuration page draws the output as a plain switch to 0 V. So the black wire is
free to be pulled up to whatever rail the controller wants - which matters, because of the next
part.

### ⚠️ Do not copy the datasheet's MCU circuit

Page 3 of the datasheet shows the sensor driven into an Arduino as: **1 kΩ pull-up to +12 V**, then
a **3.3 kΩ / 2.2 kΩ divider**, giving the **0-4.8 V** the drawing labels. That is sized for a 5 V
Arduino.

**4.8 V into a Teensy 4.1 pin destroys it** - the iMXRT1062 is a 3.3 V part and is not 5 V tolerant.

Since the output is open collector with no internal pull-up, the whole divider is unnecessary:
**pull the black wire up to the controller's own logic rail and stop.** No 12 V ever appears on the
signal, and there is nothing to get the ratio wrong on. Use **1 kΩ-2.2 kΩ** rather than an MCU
internal pull-up - the run is a drag-chain cable plus 1.5 m of DB37, and a 20-50 kΩ internal
pull-up leaves it high-impedance next to Y Step
([see the adjacency](db37-axis-interconnect.md#-two-steplimit-adjacencies-known-and-accepted)).
The sensor sinks 300 mA, so the resistor value is not remotely a constraint.

### ⚠️ The 1.2 m captive cable does not reach

Each sensor ships with **1.2 m** of moulded-on lead. That is the axis end to somewhere near the
axis end - not to the breakout box. Every limit needs a junction near its sensor, and that junction
is then in the drag chain's environment. Not yet designed.

## ⚠️ NPN-NO conflicts with the fail-closed argument

The sensors fitted are **normally open**. [`design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md)
§3 settles the limit sense as **NC**, and the whole of its argument is fail direction:

| | NPN-NC | NPN-NO (fitted) |
|---|---|---|
| Broken signal wire | reads **triggered** - stops | reads clear - **drives on** |
| Dead sensor / no 12 V | reads **triggered** - stops | reads clear - **drives on** |
| Connector pulled | reads **triggered** - stops | reads clear - **drives on** |

Recorded as fitted, not re-argued. `$5` inverts the sense in firmware so either part *works*; no
setting recovers the fail direction. The consequence is written here so it is a known property of
the machine rather than something discovered during a crash.

**It also removes a property the DB37 was getting for free.** With NC limits, pulling the
interconnect faulted the machine. With NO it does not.

**The drop-in NC part exists.** The same body, bracket, cable and wire colours are sold as
**SN04-N2** - the series runs N (NPN NO) / N2 (NPN NC) / P (PNP NO) / P2 (PNP NC). Recorded so the
option is known, not to reopen the choice: swapping restores fail-closed and changes nothing else
in this document.

## Sensor response latency

**500 Hz** response frequency is a **2 ms** worst case before the output moves. At the 16 k rapid
the encoder design doc uses for its own latency argument - 267 mm/s - the axis travels about
**0.53 mm** in that window, before anything downstream has been told.

Recorded because this repo cares about where travel numbers come from. It is not an objection: the
sensor is the backstop, and 0.5 mm of it is the cost.

## The drives are HBT57C - and three things follow

Added 2026-09-29, from notes written in an ioSender session on 2026-09-26. **Not yet folded in
properly** - the full HBT57C material (LED fault codes, the ENA-reset question, $744/$745) is
scheduled to land in this folder and has not. Until it does, the memory note is the fuller source.

**TOSEASTARS HBT57C**, 57 frame / NEMA 23, 24-55 V DC, 36 V recommended. The manual is not in
[`../manufacturer-assets/`](../manufacturer-assets/) yet, which this repo's own rule says it should
be.

### ⚠️ AL has no pull-up today, which is why it has never asserted

Pins 11/12 are **AL+ / AL-**, open collector, max pull-up 24 V / 100 mA. AL+ is the collector and
AL- the emitter, so it is a **floating switch** - tying AL- to the shared GND at the connector is
what makes the single-GND scheme on this page work for it.

**An open collector with nothing pulling it up never shows a level.** There is no pull-up in the
build today, and that alone accounts for the alarm never having been seen to work. It needs one,
and — exactly as for the limit sensors above — **not the manual's 24 V / 2 kΩ near a Teensy pin.**

### ⚠️ AL fails open, so it is not a guard on its own

Fault means the transistor conducts and the line goes low. But **a drive with no power, or a broken
AL wire, leaves the transistor off** - the pull-up wins, the line reads high, and that reads as
*healthy*. A dead or unplugged drive looks fine.

It becomes a real guard only when paired with a **driver-power-present** input: *power present AND
no alarm* = healthy. Neither half is sufficient. **There is no pin allocated for that signal** -
it is a candidate for the seven spares in
[`db37-axis-interconnect.md`](db37-axis-interconnect.md).

This is the same failure direction as the NO limit sensors above. Two of the three things that are
supposed to stop this machine currently fail silent.

### ⚠️ Do not daisy-chain the 48 V

The manual is explicit: *"parallel connection should be adopted at the power supply, and chain
connection from one driver to another is not allowed."* A chained rail makes both over- and
under-voltage trips far likelier at the far end.

So the star rule above is **not only about the returns** - the 48 V positive runs from the PSU to
each drive as its own leg too. Never verified against how the machine is actually wired today.

### Note on the five AL pins

grblHAL has **$744 / $745** and raises **Alarm 17, motor fault**, and the core defines *per-axis*
fault inputs. But the Teensy driver implements only a **single combined** motor-fault pin across
every board map - so five separate AL conductors are ahead of the firmware, and today they would
have to be wire-ORed into one input.

Keeping them separate in the connector is still the right call: the wiring is nearly free during a
build and impossible to retrofit cheaply, and per-axis needs only a board-map edit later. Recorded
so the gap is not mistaken for a wiring error.

## ⚠️ Open

1. **Controller draw on the 5 V rail.** The buck is rated 3 A; the actual draw, and the gauge of the
   5 V pair, are not established. Both are needed before the drop across that run means anything.
2. **Which rail the limit pull-up goes to.** Follows from the controller board's input stage - 3.3 V
   direct, or 5 V if its inputs are buffered. The breakout box has 5 V but not 3.3 V, so this also
   decides whether the resistor sits in the breakout box or at the controller.
3. **48 V against a 55 V over-voltage trip.** The drives trip on over-voltage at a figure the manual
   states three ways; the memory note says design to **55 V**. A 48 V rail leaves about **7 V** of
   headroom for regeneration on decel. No regen fault has ever been observed - but it is not
   recorded what supply voltage that history was accumulated at, and 48 V is a swap-in. Establish
   the present rail voltage before treating the clean history as applying.
4. **Peak current per axis on 18 AWG.** 18 AWG is about 21 mΩ/m; the drag-chain run length and the
   drive's peak draw are both unrecorded, so the drop is uncomputed.
5. **Where the drives' opto commons sit.** The HBT57C signal pins are **pairs** - PUL+/PUL-,
   DIR+/DIR-, EN+/EN-, AL+/AL-. The six-wire scheme on this page ties all four minus legs to the
   shared GND at the connector, which is standard common-cathode practice and is what the AL
   wire-OR already does. **It is still an assumption**, and it is the one everything else here
   rests on. Confirm against the manual once that is committed.
6. **EN polarity.** Genuinely ambiguous in the manual - the FAQ says a low enable prevents motion
   and that it should be "pulled high or not connected", but it is an opto input where floating
   means no current. **Measure, do not reason.** The manual also recommends leaving EN
   unconnected, so they are probably floating on the machine today.
7. **The limit sensor junction.** See the 1.2 m cable above - needed per axis, not yet designed.
8. **Target plates.** 4 mm non-shielded sensing means something ferrous has to come within 4 mm at
   each end of travel. Not yet specified.
9. **The HBT57C manual is not committed.** Per this repo's datasheets-committed rule it belongs in
   [`../manufacturer-assets/`](../manufacturer-assets/), and several items above cannot be closed
   without it.
