# Cabinet power and grounding

Where the power comes in, what the E-stop switches, how many supplies there are, and the one
grounding arrangement that the signal integrity of everything else depends on.

This is the cabinet. [`breakout-box.md`](breakout-box.md) is the box out at the machine and carries
the star rule for the **motor supply returns** specifically; this file is the layer above it - mains, the
separate logic supply, and the single point every ground meets at.

## What switches what - the chain from the wall

Two circuits come into the box:

| Circuit | Carries |
|---|---|
| **110 V, 20 A** | The control circuit - the paddle switch and the main contactor's coil |
| **220 V, 20 A** | Everything that does work |

Everything downstream of that is behind **one magnetic paddle switch** - big red stop paddle, small
green start button, 110 V. Its output drives the **coil** of a **25 A 220 V contactor with a 110 V
coil**, and that contactor is what actually carries the 220 V. His scheme, 2026-11-05.

NOTE: **A MAGNETIC PADDLE SWITCH DROPS OUT ON A POWER LOSS AND STAYS OUT.** Coming back takes a
deliberate press of the green button. That is the property being bought, and it is the reason this is
not a toggle: a toggle restores power to a machine nobody is standing at, the moment the mains
returns.

### The 2 x 8 terminal block - four pairs out

The contactor's output lands on a **2 x 8 terminal block**: the two switched legs in, **four pairs
out**.

| Pair | Feeds |
|---|---|
| 1 | The **36 V motor supply** |
| 2 | The **VFD**, 220 V in |
| 3 | The **pump contactor** |
| 4 | The **12 V supply** |

**Every contactor in here is DIN rail mounted.**

### The pump follows the spindle

The 220 V pump is switched by **its own contactor with a 24 V coil**, and that coil is driven from
**one of the VFD's outputs** - so the pump runs whenever the spindle runs. Nothing to remember and
nothing to forget, which is the right arrangement for the one pump a water-cooled spindle cannot run
without.

SETTLED: **THE 24 V COMES OUT OF THE VFD - his word, 2026-11-05.** So no fifth pair and no extra
supply: the VFD sources the coil and one of its own outputs switches it.

🔴 **THE VFD IS A HUANYANG HY02D223B, AND ITS MANUAL IS NOT IN THIS REPO.** Model his, 2026-11-05.
The root README's rule is that datasheets are committed, not linked, and there is no VFD document in
[`../manufacturer-assets/`](../manufacturer-assets/) - the only spindle item is the RATTMMOTOR
listing image. Two questions need one page of it, and **neither should be answered from recollection
of the HY series**: the control terminal names and ratings are exactly the kind of detail this repo
has already had to recover once from a schematic. Two questions:

1. **What that 24 V terminal can source, against what the coil draws to pull in and to hold.** A VFD's
   24 V terminal is usually there to bias digital inputs and can be rated in tens of milliamps; a DIN
   contactor's DC coil is a different order. If it cannot carry the coil, the fix is small - the 24 V
   comes off the 12 V supply's own rail or a dedicated one - but it is a part to buy, not a wire to
   move.
2. **Whether the output is a relay contact or a transistor.** A dry contact is polarity-blind and
   takes the coil directly. An open-collector output sinks rather than sources, which puts the coil
   between +24 V and the output pin and makes a flyback diode across the coil the difference between
   working and killing the output on the first spindle stop.

FLAG: **These two are the same question the pump cannot run without, so they gate the pump contactor
and nothing else in the chain.** Everything upstream - the paddle, the main contactor, the block, the
four pairs - is settled and buildable without them.

### What the E-stop takes down, and what it does not

FLAG: **IT TAKES THE CONTROLLER WITH IT.** The 12 V supply is on pair 4, on the switched side, and
the RP23 is fed 12 V through the interface board - see
[`kicad/interface-board/README.md`](kicad/interface-board/README.md). So the paddle drops the
controller, not only the drives: position is lost, the telnet session goes, and coming back is a
reboot and a re-home. That follows from *everything is behind the E-stop* and is not an oversight -
it is written down because it is the one property of this topology that gets noticed every single
time it happens.

FLAG: **THE PADDLE IS ALSO THE EVERYDAY ON/OFF, SO THE VFD'S MAINS IS CYCLED ON EVERY SHUTDOWN.**
Observation: pair 2 is the VFD's mains and it sits on the switched side, so the green button and the
red paddle are the VFD's power switch. Claim, not established here: VFD manuals commonly tell you
**not** to use an upstream contactor as the routine start/stop, because the spindle then stops by
coasting instead of under the drive's control, and every cycle re-charges the DC bus through its
pre-charge path. **Whether this VFD says so is a question for its manual**, which is not in this
repo. It changes no part if it is fine, and adds a run/stop input off the paddle's auxiliary if it is
not.

OPEN: **THE 110 V CIRCUIT IS CARRYING A PADDLE SWITCH AND ONE CONTACTOR COIL AGAINST A 20 A
BREAKER.** Nothing else is assigned to it. Whatever else wants 110 V - the PC, cabinet lights, a
dust collector trigger - goes here, and it is worth deciding before the box is populated rather than
after.

OPEN: **NO PROTECTION IS SPECIFIED BETWEEN THE BLOCK AND THE FOUR LOADS.** The two 20 A breakers are
at the wall and the four **5 A fast-blow per drive** are downstream of the 36 V supply - see
[`ig57-drives.md`](ig57-drives.md). Each of the four pairs off the block is unfused as drawn.

OPEN: **WHICH BOX THIS DIN RAIL IS IN.** This chain is written as the cabinet.
[`breakout-box.md`](breakout-box.md) still describes a separate remote box out at the machine holding
the 36 V supply and the bucks, and the interface board's README puts the 12 V source in the same
enclosure as the board. One word settles it; nothing above depends on the answer.

## The motor supply is not settled

SETTLED: **THE RAIL IS 36 V - his decision, 2026-10-12.** It is the voltage the TST57 manual
recommends, and it leaves the Mega V's 48 V supply in the Mega V instead of being dug out. The
reasoning is in [`ig57-drives.md`](ig57-drives.md); the short version is that 48 V would have sat at
the manual's lowest stated maximum with about 2 V of regeneration headroom.

SETTLED: **THE SUPPLY IS THE 36 V 600 W ALREADY IN THE MACHINE - nameplate, 2026-10-12.**

| | |
|---|---|
| Input | **220 V at 3.5 A** |
| Output | **36 V DC at 16.5 A**, 600 W |

**So the 600-against-800 W question is answered by nothing moving.** It was a 48 V question, and
choosing 36 V dissolved it: the supply that was already here is the right one, and the Mega V keeps
its 48 V 800 W.

NOTE: **THE CURRENT BUDGET WENT UP, NOT DOWN - 16.5 A against the 12.5 A this repo worked to.** Watts
over volts is the whole of it, and the same 600 W at a lower rail buys more current. The budget that
[`../machine/stepper-sizing.md`](../machine/stepper-sizing.md) worried four motors might exceed has
gained **4 A** as a side effect of a decision taken for over-voltage headroom.

FLAG: **NAMEPLATE, NOT MEASURED.** This is the supply's own claim about itself.

### It is a VARIABLE supply with an LCD display - which cuts both ways

His, 2026-10-12. The output is adjustable and there is a power display on the top of the unit.

🔴 **SO 36 V IS A SETTING, NOT A PROPERTY - AND THIS REPO HAS BEEN BITTEN BY EXACTLY THAT.** The
standing rule at the top of the root README exists because $130 read 889 mm against a real 860 mm
and quietly cost soft-limit protection. **A rail that can be turned is a rail that can be turned by
accident**, and the drives alarm and stop above 50 V. PROCEDURE: **Set it, verify it with a meter at
the drive end, record the reading in [`../commissioning/`](../commissioning/), and mark the
adjustment** - a dab of paint or a note on the case. Do not take 36 V from this page; take it from
the meter.

NOTE: **The adjustment is also the fix if the rail is ever wrong.** Nothing has to be bought to move
it, which is worth knowing before anyone orders a different supply over a voltage question.

✅ **THE LCD CLOSES THE MEASUREMENT PROBLEM BELOW, AND IT DOES NOT NEED A MACHINE.** The open item
about what four drives actually draw had been waiting on a clamp meter and a working axis; the supply
reports its own output, and the readings that matter come off **four motors loose on a bench**.
PROCEDURE: **[`../commissioning/bench-session.md`](../commissioning/bench-session.md)** - rail,
power-on inrush with all four connected, idle draw, free-running draw. It also catches the one
failure mode that is invisible when motors are tested singly: four input capacitor banks charging at
once.

NOTE: **THAT CLOSED A STANDING ITEM IN
[`../machine/stepper-sizing.md`](../machine/stepper-sizing.md) WITHOUT ANSWERING IT.** That file
carried a 12.5 A budget and a worry that four motors might exceed it, with the resolution that
*either the supply or the motor has to move*. **Neither moved - the rail did**, and the budget went
up 4 A as a side effect of a decision taken for over-voltage headroom.

NOTE: **DO NOT BUDGET FOUR MOTORS AT 5 A EACH - the manual says so directly, and then declines to
give a number.** §6.2 explains that the supply input current is **smaller** than the motor phase
current, because the drive converts a high-voltage low-current input into a low-voltage high-current
winding drive, and that the input current also depends on speed and load. Its conclusion is that
*"users need to carry out specific analysis and estimation"*. So **20 A is the wrong figure to size
against**, and the right one is not in the documentation - which makes it a measurement rather than
an arithmetic problem. **The supply's own LCD is the instrument**, so the measurement costs nothing
but a cut to read it during.

**What that leaves is a comparison, not a calculation:** 16.5 A available against four drives rated
5 A phase each, with the manual saying supply current runs below phase current by an amount it will
not quantify. That is probably comfortable and is **not** established.

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

SETTLED: **THE LOGIC RAIL IS ITS OWN MAINS-FED 12 V SUPPLY, on pair 4 of the block above - his
scheme, 2026-11-05.** Then **point-of-load regulation per consumer** rather than one rail fanned out.

| Consumer | Fed | Regulated |
|---|---|---|
| RP23 controller | **12 V**, in through the interface board | on the controller |
| Limit sensors | **12 V** | none - the SN04 takes 6-36 V direct |
| Probe | **12 V** | **its own regulator and its own return** |
| ESP32 sensor board | **12 V** up the chain | at the board |

FLAG: **THIS REPLACES A 24 V 50 W SUPPLY AND A 36 V BUCK, AND BOTH WERE WRITTEN DOWN.** This section
said 24 V until 2026-11-05, from the 2026-09-26 session; the interface board's README says the 12 V
*"arrives regulated from the existing 36 V -> 12 V buck"*. Neither is the design. **It is a separate
supply off the mains, and 12 V, not 24 V.** Do not reinstate either figure.

✅ **A SEPARATE SUPPLY IS ALSO WHAT KEEPS THE DRIVES' ISOLATION, AND THE BUCK WOULD HAVE THROWN IT
AWAY.** A shared rail between logic and motor supply is the first of the three ways listed below to
lose it. A plain buck off the 36 V rail is exactly that: it would have tied the controller's logic
ground to the motor return, and the per-signal optos **measured** at the drives on 2026-10-12 would
then have been isolating two things already connected. The separate supply keeps the break real, and
it costs one supply and one pair off the block.

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
| 12 V 0 V | the logic supply's return |
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

**Two circuits, 20 A each: 110 V and 220 V** - and nothing of the house on either. The four pairs off
the block are all on the 220 V one. His figures from the 2026-09-26 session, against the spindle that
was subsequently settled at Ø80 2.2 kW:

| Load | Draw |
|---|---|
| 2.2 kW spindle | ~11 A |
| Motor PSU | **3.5 A** — **nameplate**, 220 V in, 2026-10-12. Replaces a ~4 A estimate |
| Pump | **not recorded** - it came with the RATTMMOTOR kit |
| 12 V supply | **not recorded** - size not chosen |
| **Total** | **~14.5 A** of the two known, against a **16 A** continuous limit |

OPEN: **TWO OF THE FOUR PAIRS HAVE NO NUMBER AGAINST THEM.** The ~14.5 A was computed when the
spindle and the motor PSU were the whole of it, and the pump and the 12 V supply are now on the same
circuit with about 1.5 A of headroom between them. Both are nameplate readings rather than
measurements - the pump's off its own label, the 12 V supply's off whatever gets bought.

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
Carried in a memory note until 2026-10-12 and now here. The 600-versus-800 W question it was folded
in with was closed the same day, by choosing a 36 V rail - which made the supply already in the
machine the right one.

**The distribution chain at the top of this file is his, 2026-11-05** - the two circuits, the paddle
switch, the 25 A contactor, the 2 x 8 block and its four pairs, and the pump following the spindle off
a VFD output. It also settled the logic rail, which three files had been describing three different
ways.
