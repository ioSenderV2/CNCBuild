# The remote breakout box

Every per-axis connection terminates here rather than on the controller box's back panel. The
controller box keeps the logic and nothing else - it does not even hold its own supply.

Settled 2026-09-10. Decisions, not measurements; nothing has been built or metered.

## What is in it

| | |
|---|---|
| **36 V, 600 W** power supply | Motor power. **16.5 A across all axes.** Nameplate, 2026-10-12 - mains 220 V at 3.5 A. SETTLED at 36 V, the TST57 manual's recommended voltage - see [`ig57-drives.md`](ig57-drives.md) |
| **12 V, 3 A** buck | Limit sensors, and the relays in the controller box |
| **5 V, 3 A** buck | The controller box's logic supply |
| **DB37 breakout board** | Fans the [DB37 interconnect](db37-axis-interconnect.md) out to the back-panel connectors |

**The boxes share a common ground.** The 5 V and 12 V returns and the DB37 per-axis GNDs are one
node, which is what makes a single GND per axis in the DB37 sufficient.

## Star the motor returns - the reason changed, the rule did not

FLAG: **THE ORIGINAL REASON FOR THIS SECTION IS GONE, AND THE RULE SURVIVES ON A WEAKER ONE.** It was
written when each axis's GND sat in the same 6-pin shell as its motor supply, so one conductor
carried chopped motor current **and** served as the drive's opto reference. **Two measurements since
have removed that:** the motor supply now runs on its own 18/2 shielded cable, and the drives' opto
minus legs are **independent and isolated** - measured 2026-10-12, see
[`ig57-drives.md`](ig57-drives.md). There is no longer a conductor doing both jobs.

**So what is left is the ordinary rule, and it still holds:**

- **Right:** every drive's supply return lands on the **PSU negative terminal directly**.
- **Wrong:** the returns daisy-chain from drive to drive, or through the breakout board's ground
  terminals. Then each drive sees the IR drop of every drive downstream of it on its own supply.

Same parts, same cost, same afternoon - only the order the rings go onto the stud differs. It is now
about **supply quality at each drive** rather than about signal integrity, which matters because the
drives alarm on both over- and under-voltage.

NOTE: **The isolation is what demoted this from critical to ordinary**, and it is worth seeing why:
with the opto minus legs independent, no amount of IR drop on a motor return appears as common mode
on Step or Dir, because those signals do not reference it at all.

## Back panel - Molex Mini-Fit Jr, panel-mount female

Two connectors per axis.

### SUPERSEDED: Stepper, 6P

FLAG: **THIS CONNECTOR IS NOT WHAT THE STEPPER RUN USES.** Kept for the open-loop note below, which is
still worth having. The stepper run is now **Cat 6 for the four signal pairs plus 18/2 shielded for
the motor supply** - see [`ig57-drives.md`](ig57-drives.md).

**AL, EN, Step, Dir, motor supply, GND** - on **18 AWG**, 6 conductor.

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

### SETTLED: The alarm fails the right way on this drive, and no power-present partner is needed

**The IG57's alarm output is normally closed by default and asserts when the drive is HEALTHY** - the
TST57 manual's §7.3, see [`ig57-drives.md`](ig57-drives.md). An unpowered drive, a broken alarm wire
or a pulled connector all stop the assertion, so all three read as a fault.

FLAG: **THIS PAGE PREVIOUSLY SAID THE OPPOSITE AND IT WAS RIGHT ABOUT A DIFFERENT DRIVE.** The Mega
V's alarm asserted on fault, so it needed a **driver-power-present** partner to become a real guard -
*power present AND no alarm* = healthy. **That partner is not needed here**: asserting when healthy
already carries the power-present information, because a drive with no power cannot assert anything.
The spare pin that was being reserved for it in
[`db37-axis-interconnect.md`](db37-axis-interconnect.md) is freed.

FLAG: **SO THE WIRE-OR BECOMES A SERIES CHAIN.** Four alarms that assert on fault parallel together;
four that assert when healthy go in **series**, and any one dropping out breaks it. Wiring it as a
parallel OR out of habit produces a guard that reads healthy when every drive is dead.

OPEN: **Confirm the sense with a meter before relying on it** - power one drive with nothing wrong
and see whether the output is asserted. The manual is machine-translated and "normally closed by
default, and output when normal" is one sentence carrying the whole guard.

**It is an open collector - 30 V and 50 mA maximum - so it still needs a pull-up**, and that pull-up
can now be **3.3 V**, keeping the whole path on one logic level. Do not pull it to 24 V.

With this and the NC limit sensors on order, the two things that were failing silent on this machine
are both addressed - which is worth saying, because this page spent a long time recording that they
were not.

### Do not daisy-chain the motor supply

Each drive's supply runs from the PSU as its own leg, in parallel, never chained from one drive to
the next. A chained rail makes both over- and under-voltage trips likelier at the far end.

NOTE: **At 36 V the under-voltage end is the one to watch, not the over-voltage end.** The manual
warns that below 24 V the drive can alarm on an unstable supply and suggests a bulk capacitor at the
input. A 36 V rail has plenty of room above and a chained return eats into the room below, so the
per-drive leg is still the right build - the reason has just swapped ends.

So the star rule above is **not only about the returns**: the supply positive is a per-drive leg too.
Never verified against how the machine is actually wired today.

## Open items
1. **Controller draw on the 5 V rail.** The buck is rated 3 A; the actual draw, and the gauge of the
   5 V pair, are not established. Both are needed before the drop across that run means anything.
2. **Which rail the limit pull-up goes to.** Follows from the controller board's input stage - 3.3 V
   direct, or 5 V if its inputs are buffered. The breakout box has 5 V but not 3.3 V, so this also
   decides whether the resistor sits in the breakout box or at the controller.
3. SETTLED: ~~**The rail voltage.**~~ **36 V, his decision 2026-10-12** - the TST57 manual's
   recommended voltage, and it leaves the Mega V's 48 V supply where it is. At 48 V the rail would
   have sat at the manual's lowest stated maximum with about 2 V for regeneration on decel against a
   drive that alarms and stops mid-job. See [`ig57-drives.md`](ig57-drives.md). OPEN: **the supply's
   wattage is not recorded**, so the current across all four axes is not either.
4. **Peak current per axis.** The IG57 is rated **5 A** phase current; the drag-chain run length is
   unrecorded, so the drop is uncomputed. The supply now runs on **18/2 shielded** rather than in a
   six-way shell. NOTE: the manual says supply input current is **smaller** than phase current and
   declines to give a figure, so this is a clamp-meter reading rather than arithmetic.
5. SETTLED: ~~**Confirm the opto commoning.**~~ **MEASURED 2026-10-12: no continuity between any of
   the minus signals, so they are INDEPENDENT** - and the seller, who said they were commoned, was
   wrong. Per-signal isolation is real and the Cat 6 pairing gives each signal a forced return in its
   own twist. See [`ig57-drives.md`](ig57-drives.md).
6. **How a fault is cleared.** PROCEDURE:
   [`../commissioning/bench-session.md`](../commissioning/bench-session.md), while the motors are
   still loose. The manual does not say. It describes the alarm output and the LED and
   never states what clears an alarm condition - so whether a power cycle is required, or the enable
   input does it, is unestablished. It decides whether the cabinet needs the drives' supply
   switchable independently of the controller, which is cheap to build in now and expensive later.
   **EN polarity is not the worry it was** on the previous drives: these inputs take 3.3-24 V
   directly on a defined differential pair, so there is no floating-opto ambiguity to reason about.
7. **The limit sensor junction.** See the 1.2 m cable above - needed per axis, not yet designed.
8. **Target plates.** 4 mm non-shielded sensing means something ferrous has to come within 4 mm at
   each end of travel. Not yet specified.
9. ~~**The TST57 manual is not yet committed.**~~ SETTLED: **Committed 2026-10-12** as
   [`../manufacturer-assets/TST57-Integrated-Stepper-Manual.pdf`](../manufacturer-assets/TST57-Integrated-Stepper-Manual.pdf).
   FLAG: **It does not close items 3, 5 or 6** - the voltage is a decision rather than a lookup, the
   opto commoning is not stated in the manual at all, and how a fault is cleared is described
   nowhere in it.
10. **The manual's section 11 does not exist.** Its contents list "11. Error Codes" and the document
    stops at section 10. So a red LED means something is wrong and nothing says what. Worth asking
    the vendor for by number.
