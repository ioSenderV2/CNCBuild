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

## OPEN: Star the 48 V returns

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

The part fitted is an **SN04-N** (Haldzemo, 4-pack). **SN04-N2, the NC variant, was ordered
2026-10-12 and arrives Wednesday 2026-10-14** to replace it - see the fail-direction section below.
Every row of this table except the output sense is common to both parts. Datasheet in
[`../manufacturer-assets/`](../manufacturer-assets/) - read off the drawing, not the listing:

| | |
|---|---|
| Supply | 6-36 V DC. **12 V is inside range** |
| Output | **NPN.** Open collector - "switched negative". **Normally open as fitted; normally closed once the N2 parts go in** |
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

### OPEN: Do not copy the datasheet's MCU circuit

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

### OPEN: The 1.2 m captive cable does not reach

Each sensor ships with **1.2 m** of moulded-on lead. That is the axis end to somewhere near the
axis end - not to the breakout box. Every limit needs a junction near its sensor, and that junction
is then in the drag chain's environment. Not yet designed.

## The fail-closed conflict is resolved by buying the NC part

SETTLED: **SN04-N2 ORDERED 2026-10-12, ARRIVING WEDNESDAY 2026-10-14** - his purchase, and it closes
the conflict that stood here. The sensors fitted today are **normally open**, while
[`design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md) §3 settles the
limit sense as **NC** on an argument that is entirely about fail direction:

| | NPN-NC (ordered) | NPN-NO (fitted today) |
|---|---|---|
| Broken signal wire | reads **triggered** - stops | reads clear - **drives on** |
| Dead sensor / no 12 V | reads **triggered** - stops | reads clear - **drives on** |
| Connector pulled | reads **triggered** - stops | reads clear - **drives on** |

The series runs N (NPN NO) / N2 (NPN NC) / P (PNP NO) / P2 (PNP NC), and the N2 is a drop-in: same
body, same bracket, same captive cable, same wire colours. Swapping restores fail-closed and changes
nothing else in this document - no pinout, no pull-up, no connector.

FLAG: **THE SWAP IS NOT DONE BY THE PARCEL ARRIVING, AND UNTIL IT IS THE MACHINE IS THE NO COLUMN.**
Four sensors have to come off, go back on and be re-tested. `$5` inverts the sense in firmware so
either part *works* and homing will look correct either way - which is exactly why the swap cannot
be confirmed by homing alone. **Pull one limit conductor and confirm the machine faults.** That is
the only check that tells the two parts apart, and it is a commissioning measurement, not a
decision: it belongs in [`../commissioning/`](../commissioning/) once taken.

**It also restores a property the DB37 was getting for free and then lost.** With NC limits, pulling
the interconnect faults the machine; with NO it does not. See
[`db37-axis-interconnect.md`](db37-axis-interconnect.md).

## Sensor response latency

**500 Hz** response frequency is a **2 ms** worst case before the output moves. At the 16 k rapid
the encoder design doc uses for its own latency argument - 267 mm/s - the axis travels about
**0.53 mm** in that window, before anything downstream has been told.

Recorded because this repo cares about where travel numbers come from. It is not an objection: the
sensor is the backstop, and 0.5 mm of it is the cost.

## The drives are IG57, and the stepper run is Cat 6 plus 18/2

FLAG: **THIS SECTION WAS WRITTEN ABOUT THE HBT57C AND THOSE ARE THE MEGA V'S DRIVES, NOT THIS
MACHINE'S** - corrected by him on 2026-10-12. Four **IG57** all-in-one closed-loop steppers, 2.2 N·m,
**DC 24-50 V**. The part and everything known about it is
[`ig57-drives.md`](ig57-drives.md); this section is only what the *cabinet* has to do about them.

The drive is at the motor, so what leaves this box per axis is logic plus motor supply and never motor
phases. **His cabling, 2026-10-12: one Cat 6 patch cable per stepper, each of PU, DR, EN and AL as a
plus/minus pair in its own twist - plus on the striped conductor, minus on the solid - and 18/2
shielded for the 48 V, sized for the drive's 5 A.** The drive presents these on two separate terminal
blocks, a 2P for the 48 V and a small-gauge block of five signal pairs of which four are used.

FLAG: **THAT REPLACES THE 6-PIN SHELL ON THIS PAGE, BUT THIS PAGE'S OPTO ASSUMPTION WAS RIGHT.** The
four minus legs are commoned inside the drive - the seller's word, 2026-10-12 - which is the
common-cathode arrangement the open items below had assumed. So **one isolated common per drive**,
with the isolation sitting between each drive and the controller. What changes is the connector, the
conductor count and that the 48 V no longer shares a shell with the signals.

**The star rule above still applies and is now easier to honour**: the 48 V runs on its own shielded
cable, so no signal reference shares a conductor with chopped motor current by construction. See
[`ig57-drives.md`](ig57-drives.md).

### OPEN: Keep AL per axis in the cabling, whatever the firmware does today

grblHAL has **$744 / $745** and raises **Alarm 17, motor fault**, and the core defines *per-axis*
fault inputs - but the Teensy driver implements only a **single combined** motor-fault pin across
every board map, so four separate AL conductors are ahead of the firmware and would be wire-ORed into
one input today. Keeping them separate is still right: the wiring is nearly free during a build,
expensive to retrofit, and per-axis needs only a board-map edit later. With AL on its own pair per
stepper that wiring is already done.

### FLAG: An alarm output that fails open is not a guard, whichever drive it is

If the drive's alarm is an open-collector output then **a drive with no power, or a broken alarm wire,
reads exactly like a healthy drive**. It becomes a real guard only paired with a
**driver-power-present** input: *power present AND no alarm* = healthy, neither half sufficient.

This is about fail direction rather than about a part, which is why it survived the change of drive
intact. **There is still no pin allocated for the power-present signal** - it is a candidate for the
seven spares in [`db37-axis-interconnect.md`](db37-axis-interconnect.md). OPEN: Whether the IG57's
alarm is in fact open collector is not established - see [`ig57-drives.md`](ig57-drives.md).

Same failure direction as the limit sensors above, and worth holding both in mind together: until the
NC sensors are fitted and an alarm guard exists, **two of the three things that are supposed to stop
this machine fail silent.**

### Do not daisy-chain the 48 V

Each drive's 48 V runs from the PSU as its own leg, in parallel, never chained from one drive to the
next. A chained rail makes both over- and under-voltage trips likelier at the far end, and the IG57's
input range tops out at **50 V** against a 48 V rail - so there is less to give away here than there
was on the drives this page used to describe.

So the star rule above is **not only about the returns**: the 48 V positive is a per-drive leg too.
Never verified against how the machine is actually wired today.

## Open items
1. **Controller draw on the 5 V rail.** The buck is rated 3 A; the actual draw, and the gauge of the
   5 V pair, are not established. Both are needed before the drop across that run means anything.
2. **Which rail the limit pull-up goes to.** Follows from the controller board's input stage - 3.3 V
   direct, or 5 V if its inputs are buffered. The breakout box has 5 V but not 3.3 V, so this also
   decides whether the resistor sits in the breakout box or at the controller.
3. **48 V against the IG57's 50 V input ceiling.** This item read "48 V against a 55 V over-voltage
   trip" until 2026-10-12 and that was the Mega V's drive. The listing gives the IG57 as 24-50 V, and
   the **trip point is a different number from the top of the range and is not known** - so the
   headroom for regeneration on decel is somewhere between about 2 V and unknown, not the 7 V this
   item used to assert. See [`ig57-drives.md`](ig57-drives.md). The Mega V's clean regen history was
   accumulated on different drives with a higher ceiling and **does not transfer**. Also see the
   supply question in [`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md).
4. **Peak current per axis.** The IG57 is rated **5 A**; the drag-chain run length is unrecorded, so
   the drop is uncomputed. The 48 V now runs on **18/2 shielded** rather than in a six-way shell.
5. **Confirm the opto commoning with a meter, not with the seller.** The IG57's inputs are plus/minus
   pairs, so they are opto inputs, and the seller says the four minus legs are commoned inside the
   drive - which is what this page had assumed. **That makes it a claim rather than a datum, and it
   is the assumption everything else here rests on.** Continuity between PU- and DR- at the drive's
   terminal block, powered off, settles it in under a minute. Worth the minute: a vendor answered the
   Mega V's equivalent question both ways in one message.
6. **EN polarity and whether EN clears a fault.** Both were live questions on the Mega V's drives and
   neither answer transfers. An opto input where floating means no current can be described two
   opposite ways in one manual, so **measure, do not reason** - and establish separately whether a
   fault clears by power cycle only or by a signal on enable, because that decides whether the
   cabinet needs the drives' 48 V switchable independently of the controller. That is cheap now and
   expensive later.
7. **The limit sensor junction.** See the 1.2 m cable above - needed per axis, not yet designed.
8. **Target plates.** 4 mm non-shielded sensing means something ferrous has to come within 4 mm at
   each end of travel. Not yet specified.
9. **No IG57 documentation is committed.** Everything known about the drive is off a retail listing.
   Per this repo's datasheets-committed rule the manual or datasheet belongs in
   [`../manufacturer-assets/`](../manufacturer-assets/), and **items 3, 5 and 6 above cannot be
   closed without it** - between them they decide the rail voltage, the grounding scheme and whether
   the cabinet needs switched motor power.
