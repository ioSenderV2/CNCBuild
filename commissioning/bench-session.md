# The bench session: four motors, no machine

**Not yet run in full.** Everything here is done with the **four HBT motors loose on the
bench** - three HBT57112C and the Z axis's HBT5776C, the machine's drives since 2026-11-25, see
[`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md) - before any axis is assembled.
Results go in the tables and then outrank anything stated in that file or on the supply's label.
Section 5 was answered on 2026-11-25, ahead of the rest.

**What it settles:**

- ~~Whether the **36 V 600 W supply covers four drives**~~ - **the supply changed under this
  question, 2026-11-13: it is the XDR-960-36, 26.6 A.** The old 20 A ceiling was four drives at
  the TST57's 5 A phase rating; the HBT manual (2026-11-26) rates the drive at **4 A continuous,
  5 A peak**, so the paper ceiling sits where it did and the 26.6 A supply clears it either way.
  **No reading here can change the supply.** The
  current readings stay because they buy the **heat number** for the drilled DIN enclosure - the
  open half of the old supply gate - and the per-drive sanity checks below.
- Whether **all four can be switched on at once** without tripping the supply.
- ~~Whether the **alarm output really asserts when healthy**~~ - ANSWERED 2026-11-25, section 5:
  it does not. Released when healthy, asserts on fault, measured on two units.
- **How a fault clears** - which decides whether the cabinet needs the drives' 36 V switchable
  separately from the controller.

---

## Why on the bench, and not later

**An uncoupled motor is the best rig this build will ever have, and it exists now.** Provoking a
fault once the motors are in the machine means moving a gantry to do it. Finding out the supply is
undersized after the plates are machined means finding out late.

**Do not skip ahead to the loaded numbers.** A free motor cannot tell you the peak draw during
acceleration of the real gantry. These readings are a **floor**, not the worst case - enough to say
the supply is fine or marginal, not enough to say what the peak is.

---

## Before the session - two prerequisites, found 2026-11-13

- OPEN: **grblHAL for the RP23 is not built or flashed yet.** Top of the todo list. It gates
  sections 3 onward - everything that jogs. Sections 1 and 2 are power-only and do not wait on it:
  supply, drives, a meter, no controller. The firmware build is its own session in the firmware
  repo, not here.
- OPEN: **Short test power cables.** One per drive, from the stepper's power terminal block to a
  2x6 terminal block carrying the 36 V. One leg per drive off the block - the no-daisy-chain rule
  in [`../wiring/breakout-box.md`](../wiring/breakout-box.md) applies on the bench too. Run at
  least one leg through the real 18/2 so section 1's drop reading means something.

---

## Setup

| | |
|---|---|
| **Motors** | All four, **uncoupled**, lying on the bench. Nothing on the shafts |
| **Supply** | **The XDR-960-36** - 36 V, 26.6 A, 960 W, DIN rail, arriving 2026-11-14. Adjust range is **36-42 V, so 36 is the pot's floor**. Label checked against the model on arrival, output **set and metered to 36.0 V** before anything connects |
| **Reading current** | **A DC clamp meter on the supply's output leg.** The XDR has **no display** - a DC-OK LED, a DC-OK relay contact and Modbus, nothing that reads amps (committed spec PDF). The LCD went with the brick |
| **Commanding motion** | grblHAL, jogging each axis. The motors need no mechanics to turn |
| **DIP switches** | **2000 pulses/rev** on all four drives - his call 2026-11-13, $100-$103 = **400** steps/mm. SETTLED 2026-11-26: the HBT manual's own 2000 row is **SW1 OFF, SW2 ON, SW3 ON, SW4 OFF** - the same positions the TST table gave, now on the right authority. Mind **SW6: OFF = FOC, ON = point-to-point mode** on this family, see [`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md) |
| **Meter** | For the rail and for the alarm output |

### The RJ45 breakout at the drive end - mapping toned out 2026-11-15

Signals reach each drive through an RJ45-to-8P-terminal breakout board, jumpered to the
drive's signal terminal block with ferruled patch-cable pairs. The jack and the block
number in **opposite directions**, so **block terminal k carries jack pin 9−k** - every
terminal confirmed by tone, with a T568B patch cable:

| Terminal | Jack pin | T568B conductor | Signal |
|---|---|---|---|
| 1 (square pad) | 8 | brown | GND - Alarm's return |
| 2 | 7 | white/brown | **Alarm** |
| 3 | 6 | green | GND - Enable's return |
| 4 | 5 | white/blue | **Dir** |
| 5 | 4 | blue | GND - Dir's return |
| 6 | 3 | white/green | **Enable** |
| 7 | 2 | orange | GND - Step's return |
| 8 | 1 | white/orange | **Step** |

Three pairs land on adjacent terminals - orange on 8-7, blue on 5-4, brown on 2-1 - and
**the green pair lands split across terminals 6 and 3**, with the blue pair between its
legs. That is the T568 3-6 split arriving intact at the block, not a board quirk: any
scheme that assumes a pair is two neighbouring terminals comes out wrong in the middle
four positions. Partner discipline is unchanged from the
[interface board README](../wiring/kicad/interface-board/README.md#what-is-on-it).

**Restrain each motor.** A free NEMA 23 with 2.2 N·m available will walk off a bench and whip its own
cable. His scheme, 2026-11-13: all four laid on a piece of plywood, a second piece the same size on
top, C-clamped. Keep the drive end of each motor proud of the plywood - the terminal blocks and the
LEDs have to stay reachable and visible, and section 7 is nothing but watching those LEDs. The
shafts stick out the other side, which is what section 6's held-shaft test needs anyway.

---

## 1. Set the rail and verify it

The output is adjustable, so **36 V is a setting**. Everything below is measured at whatever this
actually reads.

| Where | Reading | Date |
|---|---|---|
| Supply terminals, set to 36 V | | |
| At a drive's V+ / V- through the 18/2 | | |

**The second row is the one that matters** - the difference is the drop in the cable, and the drives
see the second number, not the first.

**Mark the adjustment** once set. A dab of paint or a line across the pot, so a knock shows.

> The drives alarm and stop above 50 V. Nothing here goes near that at 36, but an adjustable output
> that nobody marked is how a rail moves without anyone deciding it should.

---

## 2. Power-on inrush - all four at once

**Connect all four drives, then switch the supply on.**

| | Result |
|---|---|
| Supply comes up clean, all four drives show green | |
| Supply trips, hiccups, or a drive does not start | |

**Test this before anything else draws current, and test it with all four connected.** Four input
capacitor banks charging together is the one failure mode that is invisible when motors are tested
one at a time, and it can trip a supply that is comfortable in steady state.

**If it trips:** the fix is staging - a switch per drive, or an inrush limiter - not a bigger supply.
Record which, because it is a cabinet change.

---

## 3. Idle draw, enabled, all four

Drives enabled, motors stationary and holding.

| Condition | Current | Power | Date |
|---|---|---|---|
| One drive enabled | | | |
| All four enabled | | | |

Take the single-drive reading first. **If four is not close to four times one, something is wrong
with one of them** and this is the cheapest moment in the whole build to find out.

---

## 4. Free-running draw

All four jogging at the rapid you intend to use. Then one axis at a time if the total looks high.

| Condition | Current | Power | Date |
|---|---|---|---|
| All four at rapid | | | |
| All four at half rapid | | | |
| One axis at rapid | | | |
| All four, shuttle cycle - peak on the meter | | | |

**The shuttle cycle is [`shuttle-cycle.nc`](shuttle-cycle.nc)** - all four axes out and back 50
times as G0 rapids, so the run is spent accelerating and decelerating, which is where the draw
peaks. It reads higher than constant-speed jogging and is the closest an unloaded bench gets to
all four at max. Two conditions, both in the file's header: the rapids and accelerations must be
set to the machine's intended values first, since G0 takes both from the controller settings -
and if the meter settles to a steady value mid-move the axes are cruising, so shorten the stroke.
Still a floor: the real peak is the loaded gantry, measured once the machine stands.

---

## What the numbers mean

**Against 26.6 A available - the XDR-960-36's nameplate - the sizing question is closed before the
meter comes out.** Four drives rated 5 A phase are a ceiling of 20 A the manual says will not be
reached, and 20 is under 26.6. No reading off this bench changes the supply. What the readings
still buy:

- The **real draw**, which sets the **heat into the drilled DIN enclosure** - heat scales with
  draw, not rating, and that number is the surviving half of the old supply gate.
- The **four-close-to-four-times-one check**, which catches a sick drive at the cheapest moment
  there will ever be.
- A baseline for the **DVRD-36's thresholds and delay** against what the rail really does.
- **The 36 V fuse link value - 15 or 20 A.** The draw readings above decide it; the
  arithmetic is with the fuse in
  [`../wiring/cabinet-power-and-grounding.md`](../wiring/cabinet-power-and-grounding.md).

**Why free-running is informative at all, given no load:** supply input current on an integrated
closed-loop drive runs below motor phase current (the TST57 manual said so and declined to say by
how much - IG57 record; the HBT57112C's figures wait on its manual). Whatever the paper ceiling
turns out to be, these readings are what replace it with a real number.

---

## 5. Does the alarm assert when healthy?

The manual says the alarm output is **normally closed by default, output when normal** - so a healthy
drive asserts, and a fault, a broken wire or an unpowered drive all read the same. **The entire
fail-safe argument rests on that sentence**, in a machine-translated manual.

Meter on AL+ / AL-, drive powered and healthy, nothing wrong.

| | Result |
|---|---|
| Healthy drive - output asserted? | **NO - released.** 12.185 V and 12.184 V against a 12 V / 10K pull-up, two HBT57112C units |
| Supply off - output released? | **Reads conducting** - 0.37 V and 0.054 V. A parasitic path through the dead electronics, not a designed assertion - nothing gets built on it |

ANSWERED 2026-11-25, two units, **and it reads the other way round: ALM is released when healthy
and asserts on fault.** Rig: 12 V through a 10K onto AL+, AL- jumpered to the supply's 0 V, meter
on AL+ against that 0 V, EN disconnected, drive standalone with a solid green LED. A plain
continuity check across a healthy unit's AL+ / AL- reads open - a *correct* reading of a released
output, not a meter limitation. Still unobserved: the assertion itself - section 6's provoked
stall is where a real fault gets watched closing the output, and the asserted-state voltage gets
read there while it sits faulted.

**If it reads the other way round**, the series alarm chain in
[`../wiring/breakout-box.md`](../wiring/breakout-box.md) is wrong and becomes a parallel one, and the
driver-power-present input that was dropped has to come back. **It did read the other way round** -
the chain is parallel (see [`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md)), and
the driver-power-present question is back open: a broken alarm wire on this family fails silent.

---

## 6. How a fault clears

**Provoke a tracking fault:** stall a shaft against slow commanded motion until the drive faults.
It is the fault this family actually produces and the only one that can be provoked safely.

His rig, 2026-11-13: a small T-clamp on the shaft, so when the shaft tries to turn the clamp arm
fights against the table. Keeps hands off the shaft. Keep the commanded motion slow - the arm hits
the table at whatever speed is commanded. If the drive never faults, check whether the clamp is
slipping on the shaft instead of stalling it: slip caps the torque below what provokes the fault,
and it looks exactly like a drive that tolerates stall.

NOTE: **The HBT manual's answer, on record before the bench's (committed 2026-11-26): power off
and restart, for every protection - no enable-clear exists in it.** The attempts below still get
run; a manual that buries features is already on file, and the cabinet consequence is expensive
enough to deserve the observation.

Then try each in turn, watching the LED and the alarm output:

| Attempt | Clears the fault? |
|---|---|
| Pulse the enable input, about 500 ms | |
| Hold enable asserted | |
| Power cycle the drive only | |

**What each answer costs:**

- **Enable clears it** - the cabinet can reset a drive without dropping motor power. Simplest.
- **Only a power cycle clears it** - the drives' 36 V must be switchable **independently of the
  controller**, so a reset does not reboot the Teensy mid-session. That is a cabinet change, cheap
  now and expensive once it is built.

## 7. Record what the LED does - it is the only fault-code source there is

The manual's section 11, Error Codes, is listed in its contents and **missing from the document**.
The vendor has been asked for it and has not replied. **So whatever the LED is observed doing here is
the fault-code information this build has**, and it is worth recording carefully rather than in
passing.

**Count the flashes and time the cycle.** Red and green separately, and note the gap - a code is
usually a burst, a pause, then a repeat.

| Condition | Green | Red | Flash count | Cycle |
|---|---|---|---|---|
| Powered, healthy | | | | |
| Tracking fault, held shaft | | | | |
| Supply below range | | | | |
| Enable deasserted | | | | |

🔴 **DO NOT FILL THIS FROM AN AI ANSWER OR A SIMILAR DRIVE'S MANUAL.** One generic table has already
been offered for this and is recorded as rejected in
[`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md): it contradicts the HBT57C's own
flash-code table - now the machine's table - on every row, transposing over-current and
over-voltage and moving tracking error from 7 flashes to 4. **An observed blink is worth more than
a plausible table**, and this is the session that checks the real table against the real part.

---

## While the motors are out

Two more that want a loose motor and cost nothing extra now:

- **Body length and shaft**, against the cast stepper frames - 94 mm body and 21 mm shaft off the
  manual, unverified against the frames.
- **Weigh one.** The manual's table says 700 g for the 2.2 N·m and the listing says 1.1 kg; his scale
  said 1.1 kg. Confirm, and the manual's whole weight column stays untrusted.

| | Reading |
|---|---|
| Body length | |
| Shaft length and diameter | |
| Mass, one motor | |

---

## The limit sensor on the stepper frame - not yet run

**This is the one that holds the rear plate's window.** Everything else about the flip is settled;
the window's height and the sensor's station wait on this, because the answer cannot be computed.

**Why it is a bench test and not arithmetic.** The frame is **ferrous** - a magnet sticks to it, his
test 2026-10-13, and it had been taken for cast aluminium. An SN04 is **non-shielded**, so the one
material that can trip it off its own mount is the one it is bolted to. No datasheet figure settles
whether it does; a wired sensor on the real casting does.

### What to set up

The casting, with **BK12 in place**, the bracket on the two M3 at `LIMIT_SENSOR_M3_PITCH`, and the
sensor wired to 12 V. Nothing else needs to be real.

### The three readings, in this order

1. 🔴 **Does it trip with NO target present?** Run the bracket through the whole of
   `LIMIT_SENSOR_ADJUST` with nothing approaching, and watch the LED. **This is the test** - a
   sensor that reads its own mount is useless at any standoff.
2. **Does flopping fix it?** The sensor sat under the bracket first and was flopped on top to get
   the face away from the frame. If 1 passes flopped, try it under as well: the flop costs
   `LIMIT_SENSOR_BRACKET_H` of window height and is worth giving back if it is not needed.
3. **Where does it trip on a real target?** Bring a piece of the **steel sole bracket stock**
   squarely at it and note the gap. The bracket is the target now - there is no separate tab.

| | Flopped, sensor on top | Sensor under the bracket |
|---|---|---|
| Trips with no target | | |
| Trips on BK12 alone | | |
| Gap at trip, steel target | | |

### What each outcome means

| | |
|---|---|
| **No false trip either way** | Put the sensor **under** the bracket and take `LIMIT_SENSOR_BRACKET_H` back off the window |
| **No false trip flopped only** | It stays flopped; the window carries `LIMIT_SENSOR_STACK_H` |
| **False trips both ways** | The frame is the wrong mount. Get creative - off the rear plate's inner face, or a non-ferrous standoff |

### The other one worth doing while a motor is loose

**Fit a tape offcut and a reader and see what a NEMA 23 rotor does to the magnetic tape at that
end** - [`../machine/archive/y-beam-support.md`](../machine/archive/y-beam-support.md) has carried
this since 2026-10-02 and the flip does **not** retire it: moving the motor to the other end of the
beam moves the magnet to the other end of the tape, and `TAPE_OVERRUN_END` is the same 30 at both.
**Before 3 m of one-shot PSA goes down.**
