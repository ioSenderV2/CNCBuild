# The bench session: four motors, no machine

**Not yet run.** Everything here is done with the **four IG57 motors loose on the bench**, before any
axis is assembled. Results go in the tables and then outrank anything stated in
[`../wiring/ig57-drives.md`](../wiring/ig57-drives.md) or on the supply's label.

**What it settles:**

- Whether the **36 V 600 W supply covers four drives** - the sizing question the TST57 manual
  declines to answer.
- Whether **all four can be switched on at once** without tripping the supply.
- Whether the **alarm output really asserts when healthy**, which is the whole fail-safe story and
  currently rests on one machine-translated sentence.
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

## Setup

| | |
|---|---|
| **Motors** | All four, **uncoupled**, lying on the bench. Nothing on the shafts |
| **Supply** | The 36 V 600 W unit, **output variable** - so it gets set and verified, not assumed |
| **Reading current** | The supply's own **LCD**. No clamp meter needed |
| **Commanding motion** | grblHAL, jogging each axis. The motors need no mechanics to turn |
| **Meter** | For the rail and for the alarm output |

**Restrain each motor.** A free NEMA 23 with 2.2 N·m available will walk off a bench and whip its own
cable. Clamp them, or lay them in a box.

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

---

## What the numbers mean

**Against 16.5 A available:**

| Four free-running reads | Then |
|---|---|
| A few amps | **The supply is settled.** Cutting load cannot plausibly close a gap that size, and the sizing question closes here |
| Approaching double figures | **Marginal.** The loaded peak is above this and unmeasured, so decide before the plates are machined rather than after |
| At or above 16.5 A | **Undersized**, found before anything was built around it |

**Why free-running is informative at all, given no load:** the TST57 manual says supply input current
runs *below* motor phase current, and declines to say by how much. Four drives rated 5 A phase each
is therefore a ceiling of 20 A that will not be reached - these readings are what replace that
useless bound with a real one.

---

## 5. Does the alarm assert when healthy?

The manual says the alarm output is **normally closed by default, output when normal** - so a healthy
drive asserts, and a fault, a broken wire or an unpowered drive all read the same. **The entire
fail-safe argument rests on that sentence**, in a machine-translated manual.

Meter on AL+ / AL-, drive powered and healthy, nothing wrong.

| | Result |
|---|---|
| Healthy drive - output asserted? | |
| Supply off - output released? | |

**If it reads the other way round**, the series alarm chain in
[`../wiring/breakout-box.md`](../wiring/breakout-box.md) is wrong and becomes a parallel one, and the
driver-power-present input that was dropped has to come back.

---

## 6. How a fault clears

**Provoke a tracking fault:** hold a shaft by hand against slow commanded motion until the drive
faults. It is the fault this family actually produces and the only one that can be provoked safely.

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
[`../wiring/ig57-drives.md`](../wiring/ig57-drives.md): it contradicts the one real flash-code table
this repo holds on every row, transposing over-current and over-voltage and moving tracking error
from 7 flashes to 4. **An observed blink is worth more than a plausible table**, and this is the
session where observing it costs nothing.

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
