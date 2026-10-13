# The IG57 drives

**Four IG57 all-in-one closed-loop steppers, one per axis.** His, 2026-10-12. The drive is built onto
the motor, so there are no drives in the cabinet and no motor phases on any cable.

## The part

**CNCTOPBAOS Integrated NEMA 23 Closed Loop Stepper Motor**, from the listing he bought from:

| | |
|---|---|
| Holding torque | **2.2 N·m** |
| Current | **5 A** |
| Supply | **DC 24 V - 50 V** |
| Shaft | **8 mm** |
| Maximum speed | **3000 rpm** |
| Pulse input | **300 kHz** |
| Encoder | **1000-line** |
| Microstepping | multi-microstep, set on the drive |

NOTE: **2.2 N·m is what this repo had independently concluded.**
[`../machine/stepper-sizing.md`](../machine/stepper-sizing.md) worked through 1.5, 2.2 and 3.2 N·m and
chose 2.2 for all four axes, on torque in the 1000-1500 rpm band rather than on thrust. The part
bought agrees with that file's answer. **Its reasoning is now partly beside the point** - it was
choosing a motor to buy, and the motor is bought - but its *conclusion* needs no revision, and its
open questions about the current budget now have a real 5 A to work with instead of an unknown.

OPEN: **NO DATASHEET OR MANUAL IS COMMITTED, AND THIS REPO'S RULE SAYS ONE MUST BE.** Everything above
is off a retail listing, which is the weakest kind of source this repo accepts - the ESP32 header
pinout had to be recovered from a schematic once because a link was treated as a copy. **Nothing below
can be closed without the vendor documentation**, and several of the questions are the kind that cost
a part if guessed.

## "Basically the same specs as the HBT57C" - his, 2026-10-12 - and the two places it is not

The Mega V runs **TOSEASTARS HBT57C**, also an integrated closed-loop NEMA 23, and he puts the IG57 as
basically the same part by specification. That is useful: it makes the HBT57C's documented behaviour
the **right first hypothesis** for this drive rather than a blank sheet.

NOTE: **A full write-up of the HBT57C's behaviour is in this repo's history at commit 72df830** - the
LED fault codes by flash count, the alarm output being an open collector with no pull-up, the
unresolved question of whether the enable input clears a fault, the RS232 configuration port, and the
no-reverse-polarity warning. It was removed because this repo documents the new machine and those are
the Mega V's drives. **Read it as a set of things to look for in the IG57 documentation, never as a
statement about the IG57.** Different vendor, and a flash-code table is exactly the kind of thing that
differs between two parts built to the same shape.

FLAG: **TWO SPECIFICATIONS ARE NOT THE SAME, AND BOTH ARE LOAD-BEARING.**

| | IG57, this machine | HBT57C, the Mega V |
|---|---|---|
| Supply range | **24 - 50 V** | 24 - 55 V |
| Current | **5 A** | the driver index read 4 A continuous |
| Holding torque | **2.2 N·m**, all four axes | **3.2 N·m** on X, Y1, Y2 |

The **50 V** is the one to carry forward - see the next section. The **5 A** matters to the supply
sizing rather than to the motor, and it is a figure
[`../machine/stepper-sizing.md`](../machine/stepper-sizing.md)'s open current-budget question has been
waiting for. The torque difference is simply two different machines: 3.2 N·m was never this build's
specification, and that file chose 2.2 deliberately.

## The over-voltage headroom is the first thing to establish

FLAG: **THE INPUT RANGE TOPS OUT AT 50 V AND THE RAIL IS 48 V.** That is the figure from the listing,
and it is **5 V lower than the drives this repo previously assumed**, where the planning figure was
55 V. Every statement in this folder about regeneration headroom was written against the old number.

Keep the two apart, because they are different quantities and only one of them is known:

- **Observation:** the listing states an input range of DC 24 V - 50 V.
- **Not known:** the **over-voltage trip point**, which is a separate number from the top of the input
  range and is normally above it. On the previous drives the range topped at 55 while the trip was
  stated variously as 55, 60 and 65.

So **48 V may leave 2 V of headroom, or it may leave more** - and nothing here can say which. OPEN:
**Find the trip point in the vendor documentation before committing to a 48 V rail.** If it really is
at or near 50 V, then decelerating a 58 kg gantry on a 5 mm lead is worth thinking about properly
rather than assuming the previous machine's clean history transfers - it was accumulated on different
drives with a different ceiling.

The supply choice itself is in
[`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md), which also carries the open
600-versus-800 W question. **The 5 A figure is per drive**; what four of them draw from the supply is
not four times that, and is not established.

## The cabling - Cat 6 for signals, 18/2 shielded for power

His scheme, 2026-10-12. **One Cat 6 patch cable per stepper**, plus **18/2 shielded** carrying the
48 V.

| Cat 6 pair | Striped conductor | Solid conductor |
|---|---|---|
| 1 | **DR** - direction | its GND |
| 2 | **PU** - pulse / step | its GND |
| 3 | **EN** - enable | its GND |
| 4 | **AL** - alarm out | its GND |

NOTE: **EACH SIGNAL GETS ITS OWN RETURN, IN ITS OWN TWISTED PAIR, AND THAT IS THE POINT OF THE
SCHEME.** A twisted pair only does anything if the return current actually flows in the other half of
that pair. Pairing each signal with its own ground is what makes a Cat 6 run appropriate for stepped
pulses at up to 300 kHz over a drag chain - the loop area is tiny and the pair rejects common-mode.

FLAG: **THIS SUPERSEDES THE SINGLE-GND-PER-AXIS SCHEME DESCRIBED IN
[`breakout-box.md`](breakout-box.md).** That page argued that one GND per axis was sufficient because
the boxes share a common ground, and its reasoning about opto commons was built on four minus-legs
tied together at the connector. **Four separate returns is a different arrangement and a better one**,
but it is not the one that page describes. OPEN: Where the four returns are commoned - at the drive,
at the breakout board, or at the PSU negative - is the question the star rule on that page now has to
be re-answered for.

OPEN: **Whether these inputs are optoisolated pairs, and what the AL output is.** The previous drives
took PUL+/PUL-, DIR+/DIR-, EN+/EN- as opto pairs and gave AL as an open collector needing a pull-up -
which is why AL had never once asserted on the old machine. **Four signals each with a dedicated GND
is consistent with driving opto pairs**, but the AL direction is the one that matters most and it
cannot be assumed: if it is an open collector it needs a pull-up, and if that pull-up is specified at
24 V it must not go anywhere near a Teensy pin, which is 3.3 V and **not** 5 V tolerant.

**The 48 V on its own shielded pair, separate from the signals, is the right split** - it keeps the
chopped motor current out of the Cat 6 entirely. Shield grounded **at one end only**; see
[`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md).

## What the closed loop does and does not cover

The drive has its own **1000-line encoder** on the motor shaft and corrects its own position. That
means **lost steps at the motor are the drive's problem and are already handled** - which is one of
the reasons the linear-encoder project narrowed its own justification away from motor-side step loss.
See [`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md).

What a shaft encoder cannot see is anything **downstream of the shaft** - a coupling slipping, a grub
screw backing out, backlash - and it cannot see **Y1 against Y2**, because the two drives have no
knowledge of each other. Those are the linear scales' job and the reason that project exists.

OPEN: **How this drive reports a fault, and how a fault is cleared.** Both were live questions on the
previous drives and neither answer transfers. Specifically worth establishing from the documentation:
whether there is an LED fault code scheme and what the codes are; whether a fault clears by power
cycle only or by a signal on the enable input; and whether the drive exposes a tracking-error
threshold that can be configured, which is what decides how twitchy a closed-loop fault is on a
machine that cuts wood.

## grblHAL can take a motor fault input, and does not use it per axis

grblHAL has **$744** and **$745** and raises **Alarm 17, motor fault**. The core defines *per-axis*
fault inputs, but the Teensy driver implements only a **single combined** motor-fault pin across every
board map - so four separate AL conductors are ahead of the firmware and would have to be wire-ORed
into one input today.

Keeping them separate in the cabling is still right: the wiring is nearly free during a build and
expensive to retrofit, and per-axis needs only a board-map edit later. With AL already on its own pair
per stepper, that wiring is done.

FLAG: **AL ON ITS OWN IS NOT A GUARD, WHICHEVER DRIVE IT IS.** If the output is open collector then an
unpowered drive and a broken wire both read the same as healthy, so it only becomes a real guard
paired with a **driver-power-present** input: *power present AND no alarm* = healthy. That reasoning
is about fail direction and not about a particular part, so it survived the change of drive. There is
still no pin allocated for the power-present signal.

## Provenance

The part and the cabling scheme are his, given 2026-10-12. **This file replaced one written the same
day about the HBT57C**, which turned out to be the Mega V's drives and not this machine's - that error
came from a memory note, and it is why the note is deleted and this is in the repo instead. The
HBT57C material was removed rather than kept: this repo is the new machine.
