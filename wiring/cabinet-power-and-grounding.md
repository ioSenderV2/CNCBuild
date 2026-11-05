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
| **110 V, 20 A** | Two branches: the **control circuit** - paddle switch and contactor coil, behind a 1 A fuse - and an **unswitched receptacle** for the laptop and the USB cameras |
| **220 V, 20 A** | Everything that does work. All four pairs off the block are on this one |

Everything downstream of that is behind **one magnetic paddle switch** - big red stop paddle, small
green start button, 110 V. Its output drives the **coil** of a **25 A 220 V contactor with a 110 V
coil**, and that contactor is what actually carries the 220 V. His scheme, 2026-11-05.

NOTE: **A MAGNETIC PADDLE SWITCH DROPS OUT ON A POWER LOSS AND STAYS OUT.** Coming back takes a
deliberate press of the green button. That is the property being bought, and it is the reason this is
not a toggle: a toggle restores power to a machine nobody is standing at, the moment the mains
returns.

SETTLED: **A 1 A FUSE ON THE CONTROL CIRCUIT - his, 2026-11-05.** The paddle switch and the
contactor coil are the whole of the load on the 110 V side, and a coil draws almost nothing, so the
20 A breaker at the wall is protecting the house rather than this wiring. **1 A puts a fuse in front
of the control conductors that is sized for what they actually carry** - and it is the branch where a
fault is most likely to be a pinched wire in a door hinge rather than a load fault.

### How power gets in - two 10 ft pigtails

His, 2026-11-05. Both circuits arrive on a **captive 10 ft cord out of the back of the CNC, with
proper strain relief** - nothing plugs into the machine.

| Circuit | Pigtail | Plug |
|---|---|---|
| 110 V | **10 ft**, feeds the receptacle inside the CNC | ordinary 110 V |
| 220 V | **10 ft**, 12 AWG | **locking, L6-20P** into an **L6-20R** at the wall |

✅ **A CAPTIVE CORD IS THE BETTER ANSWER, NOT THE COMPROMISE.** A panel inlet was the fix offered
here for the double-ended cord it replaces; the pigtail beats it on both counts. There is **no
connector on the machine at all** to be left live or to work loose in a shop full of chips, and
unplugging at the wall is a **break you can see** - which a tripped breaker in another room is not.

SETTLED: **L6-20P, NOT L15-20P - his decision, 2026-11-05.** This read L15-20P for one commit.
**L15-20 is the THREE-PHASE configuration** - 250 V three-phase, 20 A, 3 pole 4 wire, three hots and
a ground. **L6-20 is the single-phase one**: two hots and a ground, 250 V, 20 A. Do not reinstate the
L15.

NOTE: **The whole cabinet reads single-phase and that is what caught it** - the spindle VFD is a
**HY02D223B**, the motor supply's nameplate is **220 V at 3.5 A**, and the block is fed by **two**
switched legs with no neutral anywhere in the chain. There is nothing in here a third hot would feed.

✅ **AND THE VFD MANUAL CONFIRMS IT INDEPENDENTLY.** Its description of the R/S/T input reads *"220V
class, for both single/three phase, single phase connected to any two phases"* - so the drive takes
single-phase on **any two** of its three input terminals, and the third is simply left off. That also
answers the question nobody had asked yet: which two.
**L14-20** was the other candidate and was declined: it is the single-phase device that also carries a
neutral, which would have let one pigtail serve both circuits, and nothing in the box wants 120 V off
the 220 V cord.

**12 AWG on both pigtails.** It is what the 110 V cord was called out at, and what a 20 A device
asks for.

### The 110 V side is deliberately NOT switched

His arrangement, 2026-11-05. The 110 V is there for the **laptop and the USB-powered cameras**, and
he does not want it shut off. The pigtail feeds a **receptacle inside the CNC**, and into that goes a
**power strip** - the laptop charger and the powered USB ports.

**So the 110 V has two branches and only one of them is fused at 1 A.** The control branch - paddle
and coil - is behind the fuse. The receptacle branch is not, and must not be: a 1 A fuse would not
carry a laptop charger, and the strip has the wall's 20 A behind it as any receptacle does.

✅ **AND THE LAPTOP STAYS UP WHEN THE PADDLE COMES DOWN**, which is the point of putting it here
rather than on a switched pair. The controller drops and the sender does not, so whatever it was
showing when the machine stopped is still on the screen.

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

The 220 V pump is switched by **its own contactor**, and the contactor is driven from **one of the
VFD's outputs** - so the pump runs whenever the spindle runs. Nothing to remember and nothing to
forget, which is the right arrangement for the one pump a water-cooled spindle cannot run without.

**The VFD is a Huanyang HY02D223B** and its manual is now committed at
[`../manufacturer-assets/Huanyang-HY02D223B-VFD-Manual.pdf`](../manufacturer-assets/Huanyang-HY02D223B-VFD-Manual.pdf).
Everything below is out of its control terminal table, pages 11-12.

🔴 **THERE IS NO 24 V SUPPLY ON THIS VFD, SO THE COIL IS NOT A 24 V COIL.** The only rails it brings
out are **+10 V** for the speed pot and **+12 V at 200 mA max**. The trap is the terminal's *name*:

| Terminal | What the manual's function table says |
|---|---|
| **EV (IPV) / P24** | *"+12V Power Supply, Max. output current 200mA"* - **named P24, supplies 12 V** |
| **+10** | Power supply for speed setting, +10 V |
| **DRV** | Multi-Output 1, **optical couple output** |
| **UPF** | Multi-Output 2, **optical couple output** - rated **DC24V/100mA** |
| **FA / FB / FC** | Multi-Output 3, **N/O or N/C**, **3 A / 250 VAC** |
| **KA / KB** | Multi-Output 4, N/O, **3 A / 250 VAC** |

**The DC24V/100mA is the switching RATING of the two opto outputs, not a rail you can draw from.**
That is almost certainly where the 24 V came from, and it is exactly the distinction this repo keeps
datasheets for - a number beside a terminal is not a supply.

✅ **WHAT CLOSES IT IS SIMPLER THAN A 24 V COIL: FA/FB/FC IS A REAL RELAY CONTACT AT 3 A / 250 VAC.**
So the pump contactor takes a **220 V or 110 V coil** and the relay switches it directly. No 24 V
anywhere, no extra supply, no flyback diode - a dry contact does not care about polarity and has no
inductive kick to catch. **One parameter sets it:**

| | |
|---|---|
| **PD052** | Multi-Output 3, the FA/FB/FC function. **Factory setting 02**, Fault Indication |
| **Set it to 01** | *"In Run: the contact will act when the inverter has output or receives the running command"* |

NOTE: **PD053 and the KA/KB pair are a spare of the same rating**, factory-set to 00, invalid - so if
the fault indication is wanted as well, it does not cost the pump its relay.

OPEN: **WHICH OF FB AND FC IS THE NORMALLY-OPEN LEG.** The manual gives the pair as *"N/O or N/C"*
and does not say which is which. It is a meter on the real part with the drive unpowered, not
something to take from a convention.

OPEN: **THE PUMP CONTACTOR'S COIL INRUSH AGAINST 3 A.** Comfortable for a contactor coil, and the
contactor is not chosen yet - so the number to check when it is picked is the coil's own inrush VA,
not its sealed rating.

### The paddle is for emergencies and for service - the machine lives powered

**His usage, 2026-11-05: the CNC stays on all the time.** The paddle comes down for three reasons and
no others - an emergency, **clearing a motor fault**, and working on the wiring.

NOTE: **THAT MAKES DROPPING POWER A DIAGNOSTIC STEP, NOT ONLY A SAFETY ONE.** A latched drive alarm
is cleared by taking the rail away from it, which is why the paddle is the tool he reaches for. Worth
knowing beside the IG57's alarm output and the fact that its manual contains no fault code table -
see [`ig57-drives.md`](ig57-drives.md).

NOTE: **SO THE CONTROLLER COMING DOWN WITH EVERYTHING ELSE COSTS LITTLE.** The 12 V supply is on pair
4, on the switched side, and the RP23 is fed 12 V through the interface board - see
[`kicad/interface-board/README.md`](kicad/interface-board/README.md) - so the paddle drops the
controller too, and coming back is a reboot and a re-home. On a machine that is switched off daily
that would be a nuisance; on one that is only ever dropped for a fault, a wiring job or an emergency,
a re-home is already part of all three.

🔴 **BUT IT IS ALSO THE SERVICE DISCONNECT, AND IT DOES NOT MAKE THE BOX SAFE.** This is the one
thing to have straight before hands go in. With the paddle down, all four pairs off the block are
dead - and **two things are still live**:

| With the paddle down | |
|---|---|
| The four pairs off the block | **dead** |
| The **110 V control branch** - paddle switch, contactor coil | **LIVE**, it is upstream of the paddle |
| The **110 V receptacle inside the box, and the power strip in it** | **LIVE** - it is not switched by design |
| The **220 V on the contactor's line side** | **LIVE**, up to the contactor's own terminals |

🔴 **THE SECOND AND THIRD ROWS ARE THE ONES THAT SURPRISE.** There is a live power strip inside this
enclosure with the paddle down, on purpose, and the 220 V reaches the contactor's line terminals. The
paddle is an emergency stop that happens to be convenient for service; it is not a disconnect, and
nothing about its position tells you which of the two circuits it dropped.

PROCEDURE: **FOR WIRING WORK, PULL BOTH PIGTAILS.** His, 2026-11-05, and it is the reason the inputs
are captive cords. Two plugs on the floor is a disconnect you can **see** from inside the box - which
is the whole advantage over a breaker in another room, and the reason to pull **both** rather than
only the 220.

SETTLED: **WHAT ELSE GOES ON THE 110 V CIRCUIT - the laptop and the USB cameras, unswitched.** His,
2026-11-05, and written up above.

OPEN: **THE FOUR PAIRS OFF THE BLOCK ARE STILL UNFUSED AS DRAWN.** What exists now: the two 20 A
breakers at the wall, the **1 A** on the control circuit, and the four **5 A fast-blow per drive**
downstream of the 36 V supply - see [`ig57-drives.md`](ig57-drives.md). Nothing between the block and
the 36 V supply, the VFD, the pump contactor or the 12 V supply.

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
| Pump | **80 W** - his, 2026-11-05. About **0.4 A** at 220 V, and he budgets it at 1 A |
| 12 V supply | **not recorded** - size not chosen |
| **Total** | **~14.9 A** against a **16 A** continuous limit |

OPEN: **ONE OF THE FOUR PAIRS STILL HAS NO NUMBER.** The 12 V supply is not sized, and it is the
last term in that total. The pump at 80 W barely moved it - the headroom was always going to be
decided by the spindle.

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
