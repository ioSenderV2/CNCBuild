# Cabinet power and grounding

Where the power comes in, how many supplies there are, and the one grounding arrangement that the
signal integrity of everything else depends on.

This is the cabinet. [`breakout-box.md`](breakout-box.md) is the box out at the machine and carries
the star rule for the **motor supply returns** specifically; this file is the layer above it - mains, the
separate logic supply, and the single point every ground meets at.

## The motor supply is not settled

SETTLED: **THE RAIL IS 36 V - his decision, 2026-10-12.** It is the voltage the TST57 manual
recommends, and it leaves the Mega V's 48 V supply in the Mega V instead of being dug out. The
reasoning is in [`ig57-drives.md`](ig57-drives.md); the short version is that 48 V would have sat at
the manual's lowest stated maximum with about 2 V of regeneration headroom.

OPEN: **WHICH SUPPLY, AND AT WHAT RATING.** The 600-against-800 W question was asked and answered
"not decided" earlier the same day, **at 48 V** - and the volts have since changed, so the arithmetic
has to be redone rather than carried across. Watts over volts is the whole calculation, and at 36 V
the same wattage buys **more** current than it did at 48 V, not less.

FLAG: **THE 12.5 A BUDGET IN [`../machine/stepper-sizing.md`](../machine/stepper-sizing.md) IS A
48 V FIGURE AND IS NOW STALE.** That file carries a standing item that rated phase current across
four motors may exceed it, with the resolution that *either the supply or the motor has to move*.
**The rail moved instead**, and it moved in the helpful direction - so that item wants re-reading
against 36 V rather than answering as written.

NOTE: **DO NOT BUDGET FOUR MOTORS AT 5 A EACH - the manual says so directly, and then declines to
give a number.** §6.2 explains that the supply input current is **smaller** than the motor phase
current, because the drive converts a high-voltage low-current input into a low-voltage high-current
winding drive, and that the input current also depends on speed and load. Its conclusion is that
*"users need to carry out specific analysis and estimation"*. So **20 A is the wrong figure to size
against**, and the right one is not in the documentation - which makes this a measurement to take
with a clamp meter once one axis runs, not an arithmetic problem.

NOTE: **The under-voltage end now matters more than the over-voltage end.** The manual warns that
below 24 V the drive can alarm on an unstable supply and recommends a bulk capacitor at the input. A
36 V rail is well clear of both ends, but the margin below is smaller than the margin above - which
is the opposite of how this page read at 48 V, and it is why the no-daisy-chaining rule in
[`breakout-box.md`](breakout-box.md) is still worth following.

PROCEDURE: **Commission on the final voltage and the final supply.** Every acceleration limit and
every threshold that gets tuned is a function of the rail. Tuning on one supply and then swapping
the other in means doing it twice, and the second time nobody will remember which figures were
measured and which were inherited.

## Separate the logic supply from the motor rail

On the **Mega V** the Teensy runs off its **48 V stepper rail** through a 5 V regulator. The **VUSB pad is cut**,
so there is no back-feed - that part is already right and should not be undone.

For the new build: a **24 V supply of order 50 W for logic**, then **point-of-load regulation per
consumer** rather than one rail fanned out.

| Consumer | Fed | Regulated |
|---|---|---|
| Teensy | 24 V | to 5 V at the controller |
| Probe | 24 V | **its own regulator and its own return** |
| ESP32 sensor board | 24 V up the chain | at the board |

The probe having its own regulator and return is the point of the arrangement, not a refinement of
it: a probe is the one input where a false trigger costs a crash, and sharing a return with anything
that switches is how it gets one.

FLAG: **CHECK THE 5 V REGULATOR'S ABSOLUTE MAXIMUM INPUT BEFORE TRUSTING ANY OF THIS, AND SIZE IT ON
WHAT THE RAIL CAN REACH RATHER THAN ON ITS NOMINAL 36 V.** The ceiling is whatever the drives tolerate before
they trip, and the TST57 manual puts the drives' **over-voltage alarm above 50 V** - see
[`ig57-drives.md`](ig57-drives.md), where the rail voltage is now the largest open decision. A regulator
chosen with no margin dies **taking the controller with it, mid-job**, which is the failure that
looks like a random crash and gets diagnosed as firmware. FLAG: **This paragraph said 55 V until
2026-10-12**, from the Mega V's drives; do not reinstate that figure.

FLAG: **THE ISOLATION IS THERE, AND IT IS EASY TO SHORT OUT BY ACCIDENT.** The IG57 brings its control
signals out as plus/minus pairs - PU+/PU-, DR+/DR-, EN+/EN-, AL+/AL- - which is an opto input
presented at its two ends, so the galvanic isolation is real. The four minus legs are commoned inside
the drive on the seller's word, so it is **one isolated common per drive** rather than four isolated
signals; the boundary that matters, between each drive and the controller, is the one that exists.
See [`ig57-drives.md`](ig57-drives.md), where the meter check that confirms it is written down.

It is free, already paid for in the drives, and lost by any of three ordinary-looking decisions: a
**shared rail** between logic and motor supply, a **merged ground bus**, or a **USB
cable to an earthed PC**.

## Grounds meet at one PE bus bar

Every ground conductor in the cabinet lands on **one PE bus bar**, and nothing daisy-chains.

| Conductor | Note |
|---|---|
| PE in | from the supply cord |
| Cabinet chassis | |
| Machine frame | |
| Motor supply 0 V | the 36 V rail's return |
| 24 V 0 V | |
| VFD PE | **its own short heavy conductor** |
| Cable shields | **one end only** |

FLAG: **NOT AT THE 240 V INPUT, AND NEVER THROUGH A SIGNAL WIRE.** The supplies are isolated, so the
mains input is not a ground reference for the DC side. And a ground that arrives through a signal
conductor is a ground that carries signal current - which is the same mistake as the daisy-chained
motor returns in [`breakout-box.md`](breakout-box.md), one level up.

Shields at one end only is the rule that gets broken by instinct, because grounding both ends feels
more thorough. It makes a loop.

## USB is a ground path, and the cable stays plugged in

The current connection habit defeats the isolation without looking like it does. ioSender connects
over **USB**, reads the controller's IP from **$I**, then reconnects by **telnet** - but **the USB
cable is left plugged in**. So switching transport changes nothing about the ground path: the earthed
PC is still tied to the controller.

PROCEDURE: **On the new build - static IP, connect straight to telnet, USB unplugged except for
firmware updates.** That is the whole fix and it costs nothing.

A **USB isolator** preserves the discovery flow if that habit is worth keeping. It is an alternative
to the static IP, not an addition to it.

## The mains circuit

**20 A at 240 V, with nothing else on it.** His figures from the 2026-09-26 session, against the
spindle that was subsequently settled at Ø80 2.2 kW:

| Load | Draw |
|---|---|
| 2.2 kW spindle | ~11 A |
| Motor PSU | ~4 A — **his figure, taken for the 48 V supply**; the mains draw follows the supply's wattage rather than its output voltage, so it moves only if the wattage does |
| **Total** | **~15 A** against a **16 A** continuous limit |

NOTE: **That margin is why the spindle decision and the circuit decision were the same decision.** A
4.5 kW spindle would have drawn roughly 23-25 A and needed its own 30 A circuit on 10 AWG. The
spindle was settled at 2.2 kW on structural grounds - see
[`../machine/spindle-and-mount.md`](../machine/spindle-and-mount.md) - and the existing circuit
covering it is a consequence of that, not an independent piece of luck.

FLAG: **PUT THE VFD ON ITS OWN BRANCH REGARDLESS, and an EMI filter or line reactor on its input.**
VFDs are electrically filthy. This is the same principle as keeping the ESP32 off the probe rail,
at mains scale - and the reason to do it even when the arithmetic says one circuit carries the load
is that the arithmetic is about *current*, not about noise.

## Provenance

Decided in the 2026-09-26 design session, which ran in the **ioSender** repo rather than this one.
Carried in a memory note until 2026-10-12 and now here. The 600-versus-800 W question above is the
only part that was still open on the day it was folded in.
