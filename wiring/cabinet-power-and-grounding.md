# Cabinet power and grounding

Where the power comes in, what the E-stop switches, how many supplies there are, and the one
grounding arrangement that the signal integrity of everything else depends on.

This is the cabinet. [`breakout-box.md`](breakout-box.md) is the box out at the machine and carries
the star rule for the **motor supply returns** specifically; this file is the layer above it - mains, the
separate logic supply, and the single point every ground meets at.

> **The picture of all of this is [`panel-schematic.html`](panel-schematic.html)** - five sheets with
> wire colour and gauge on every run. It is **derived, never authoritative**: this file is where the
> decisions and their provenance live, and the drawing is regenerated from them by hand. It is a
> connection diagram and **not** a DIN rail layout, which gets done with the real components against
> the real box.

## What switches what - the chain from the wall

Two circuits come into the box:

| Circuit | Carries |
|---|---|
| **110 V, 20 A** | Everything that must **survive an E-stop**: the 12 V logic supply, the paddle's own control circuit, and the receptacle for the laptop and cameras |
| **220 V, 20 A** | Everything that **does work** and must stop: the 36 V motor supply, the VFD, the pump |

🔴 **THE E-STOP DOES NOT KILL THE CONTROLLER - his decision, 2026-11-06, and it is the one that
shapes the whole 110 V side.** The 12 V supply moved off pair 4 and onto the 110 V circuit, so the
paddle drops the **spindle and the steppers** while the **RP23 stays up** with its position, its
alarm state and the ioSender session intact. Safety is unchanged - motion dies the instant the drives
lose 36 V and the VFD loses mains. What changes is the recovery: no reboot, no re-home, and a
controller that can say **why** it stopped.

FLAG: **THIS FILE SAID THE OPPOSITE UNTIL 2026-11-06**, when the 12 V supply was on pair 4 and the
paddle took the controller with it. Do not reinstate that; the sense relay below exists because of
this change and is not optional with it.

Everything downstream of that is behind **one magnetic paddle switch** - big red stop paddle, small
green start button, 110 V. Its output drives the **coil** of a **25 A 220 V contactor with a 110 V
coil**, and that contactor is what actually carries the 220 V. His scheme, 2026-11-05.

### The paddle switch is a POWERTEC 71054

His part, 2026-11-05. From the manufacturer's own page, [powertecproducts.com/71054-magnetic-paddle-switch-120v](https://powertecproducts.com/71054-magnetic-paddle-switch-120v/):

| | |
|---|---|
| Rated voltage | **120 V** |
| Rated HP | **1/2 HP** |
| Continuous load | *"Motor class continuous load limited to 9 amps or 1/2 HP at 120 Volts"* - the listing calls it 16 A rated |
| Approvals | **UL, TUV, CSA, CE, ETL** |
| In the box | **the switch and a wiring diagram.** *"Electrical box not included"* |
| Mounting | **POWERTEC 71834 deep gang box, ordered 2026-11-05** on the vendor's advice |
| Variant | **The no-cord option** - his choice, 2026-11-05, because it gets wired differently anyway |

✅ **9 A CONTINUOUS AGAINST A CONTACTOR COIL IS ENORMOUS HEADROOM**, and 120 V is the circuit it is
already on. This switch is built to carry a 1/2 HP tool directly; here it carries nothing but the
coil, which is the easiest duty it will ever see.

NOTE: **A MAGNETIC PADDLE SWITCH DROPS OUT ON A POWER LOSS AND STAYS OUT** - and that is the vendor's
own claim for this part, not an inference: *"preventing tools from powering up after unexpected
outages, blown breakers and other power interruptions."* Coming back takes a deliberate press of the
green button. That is the property being bought, and it is the reason this is not a toggle: a toggle
restores power to a machine nobody is standing at, the moment the mains returns.

SETTLED: **THE TERMINALS ARE 13/14 AND 23/24, TWO POLES, ON 1/4 INCH SPADE TABS.** From the wiring
diagram on the listing, 2026-11-05 - so this no longer waits on unboxing the switch:

| Terminal | The diagram's label | Here |
|---|---|---|
| **13** | Hot 1 in | **hot in**, from the 110 V control branch behind the 1 A fuse |
| **14** | Hot 1 out | **to contactor A1** |
| **23** | 125 V Neutral in | **neutral in** |
| **24** | 125 V Neutral out | **to contactor A2** |

✅ **BOTH POLES ARE SWITCHED, SO THE COIL IS FULLY ISOLATED WHEN THE PADDLE IS DOWN.** 13-14 and
23-24 is the IEC numbering for **two normally-open contacts**, which is the behaviour wanted: both
open together when the paddle drops, and the coil circuit is broken on both sides rather than left
sitting on a neutral.

NOTE: **IT TAKES FOUR 1/4 INCH FEMALE QUICK-DISCONNECTS** - the diagram calls them out as the
terminal type. A buy item, and not one that turns up in a DIN rail parts list.

NOTE: **The diagram's warnings are AC 120 V only and motor power ≤ 1/2 HP.** Both are already
satisfied - it is on the 110 V branch driving a contactor coil.

SETTLED: **THE SWITCH IS NOT IN THE PANEL. It lives in its own deep gang box bolted to the side of
the machine** - his, 2026-11-05 - well away from the PVC box and everything in it. So the control
circuit runs **out to the switch and back**: hot and neutral out to 13 and 23, switched hot and
neutral back from 14 and 24 to the contactor's A1 and A2. **Four conductors in one cable between the
panel and the switch box**, which is a run the drawing has to show and a parts item on its own.

NOTE: **THE CORD QUESTION IS MOOT - he bought the bare switch on purpose.** Two sources disagreed on
whether a pre-wired cord ships with it; he did not order that option, because a switch used as a
pilot device for a contactor coil gets wired differently from one feeding a tool outlet. **Which is
what this chain does with it**, so nothing in the design changes.

OPEN: **WHETHER THE REMOVABLE SAFETY LOCK KEY IS REAL.** The Amazon copy claims one and the
manufacturer's page does not mention it. Apparent on arrival, and worth having if it is there: it
does not make the box safe, but it stops a restart while hands are inside.

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
| 110 V | **10 ft**, 12 AWG, feeds the receptacle inside the CNC | **locking, L5-20P** into an **L5-20R** at the wall |
| 220 V | **10 ft**, 12 AWG | **locking, L6-20P** into an **L6-20R** at the wall |

SETTLED: **BOTH PIGTAILS LOCK, AND THE REASON IS THE KEYING RATHER THAN THE LOCK - his, 2026-11-05.**
L5-20 and L6-20 have different blade orientations and are **physically non-interchangeable**. Two
captive cords of the same size and colour hang off this machine; with these two devices they
**cannot be cross-plugged**, by anyone, in bad light. The twist-lock is the lesser benefit.

NOTE: **The cost is that the 110 V wall outlet becomes an L5-20R and stops taking anything else.**
That circuit is already dedicated to the machine, so it reads as a feature.

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

NOTE: **L14-20 was the other candidate and was declined.** It is the single-phase device that also
carries a neutral, which would have let one pigtail serve both circuits - and nothing in the box
wants 120 V off the 220 V cord.

✅ **AND THE VFD MANUAL CONFIRMS IT INDEPENDENTLY.** Its description of the R/S/T input reads *"220V
class, for both single/three phase, single phase connected to any two phases"* - so the drive takes
single-phase on **any two** of its three input terminals, and the third is simply left off. That also
answers the question nobody had asked yet: which two.

**12 AWG on both pigtails.** It is what the 110 V cord was called out at, and what a 20 A device
asks for.

### The 110 V side - a breaker, a 2 x 6 splitter, three pairs out

His, 2026-11-06. **Nothing on this circuit is switched by the paddle.** It is the half of the cabinet
that stays alive.

| | |
|---|---|
| In | the **L5-20P pigtail**, hot and neutral, into the **top** of the breaker |
| Breaker | the **third 6 A 2-pole**, repurposed - across **hot and neutral**, so the branch gets double-pole isolation |
| Then | a **2 x 6 splitter block** |

| Pair | Feeds |
|---|---|
| 1 | The **12 V supply** |
| 2 | The **paddle switch**, behind its **1 A fuse** |
| 3 | The **receptacle** the power strip plugs into |

**Three spare pairs on the splitter**, which is the right side of the panel to have them on.

✅ **THE SPARE BREAKER LANDS EXACTLY RIGHT AND NOTHING EXTRA GETS BOUGHT.** Four 2-pole breakers were
ordered for four pairs off the 2 x 8 block. Moving the 12 V supply here frees one, and a 2-pole 240 V
MCB works perfectly well on 120 V across hot and neutral. The 220 V side keeps **6 A, 16 A, 6 A** and
the fourth comes here.

NOTE: **THE RECEPTACLE IS NOW BEHIND A BREAKER, WHICH IT WAS NOT BEFORE.** Until 2026-11-06 the strip
had only the wall's 20 A. **6 A is ample**: the laptop charger is a couple of amps at 120 V, the
powered USB and cameras well under one, and the 12 V supply about 0.4 A at this voltage. A **curve C**
is what carries the chargers' switch-on inrush without nuisance tripping, which is the reason it had
to be C rather than B here too.

NOTE: **The 1 A fuse stays where it is - on the paddle's pair only.** It protects the four conductors
running out to the remote switch box, which is a different job from protecting the branch, and a
laptop charger would never run behind it.

### The 2 x 8 terminal block - four pairs out

The contactor's output lands on a **2 x 8 terminal block**: the two switched legs in, **four pairs
out**.

| Pair | Feeds |
|---|---|
| 1 | The **36 V motor supply** |
| 2 | The **VFD**, 220 V in |
| 3 | The **pump contactor** |
| 4 | The **sense relay coil** - the 12 V supply left this pair on 2026-11-06 |

SETTLED: **THE BLOCK GOES ON THE RAIL UPSIDE DOWN - his, 2026-11-06, and it is not a violation of
anything that matters.** The contactor's load terminals are at the **bottom**; the breakers' line
terminals are at the **top**. Inverting the block puts its input at the bottom and its outputs at the
top, so the contactor makes one short U-turn into it and each pair makes one short U-turn out to a
breaker. **No long runs and nothing crossing.**

✅ **A PASSIVE BLOCK HAS NO LINE AND LOAD SIDE, WHICH IS WHY THIS IS FREE.** The top-in bottom-out
convention exists for devices that care - breakers, where busbar combs feed the top and some makes
mark a direction. A feed-through terminal block is symmetric: there is nothing inside it to install
backwards.

🔴 **BUT THE BLOCK'S OWN PRINTING WILL READ UPSIDE DOWN, SO LABEL THE ROWS ON THE PANEL.** Whatever
is moulded or printed on it - numbers, a label field - is now inverted, and the row that looks like
the first one is the second. **Write L1 and L2 on the panel beside it.** This is the repo's recurring
failure in miniature: a thing that looks right and is not, costing nothing to prevent and an
afternoon to find.

**Every contactor in here is DIN rail mounted.** There are **two**, and they are not the same size:

✅ **BOTH ARE THE SAME PART IN TWO COIL VARIANTS - Wengart WCT-25 2P 2NO, about $10 each.** His,
2026-11-05. One model to know, one set of terminals to remember, and a spare of either is a spare of
both on the power side.

| | Coil | Fed from | Switched by |
|---|---|---|---|
| **Main** | **AC 110-120 V** | the 110 V control branch, behind the 1 A fuse | the paddle switch |
| **Pump** | **AC 230 V** | **pair 3** | the VFD's **FA/FC** relay |

**The WCT-25's specification**, off the product listings - the same for both except the coil:

| | |
|---|---|
| Model | **WCT-25, 2P 2NO** |
| Rated current | **25 A (AC-7a) / 9 A (AC-7b)**. 250 V AC Ue; the listing also puts AC-7a at 5500 W resistive |
| Contacts | **2NO**, normally open |
| Coil, main | **AC 110-120 V**, 50/60 Hz |
| Coil, pump | **AC 230 V**, 50/60 Hz - **inrush 11.5 VA, holding 2.8 VA / 1.2 W max** |
| Coil terminals | **A1 / A2** |
| Power terminals | **1-2 and 3-4** |
| Width | **18 mm - one DIN module**, 35 mm rail |
| Wiring | power **1.5-6 mm²**, stripped **9 mm**, **0.8 N·m**. Coil **1.5-2.5 mm²** |
| Life | **1,000,000** mechanical / **100,000** electrical at full load |
| Certifications | CE / ETL |

NOTE: **18 mm each, so two contactors are 36 mm.** FLAG: **this line read "the rail is a non-issue"
until the four 2-pole breakers were added** - see the rail budget below, which is no longer
comfortable on one rail.

NOTE: **THE VENDOR ASKS FOR A GAP BETWEEN THEM, SO LEAVE ONE.** *"If installing multiple contactors
side-by-side in a closed panel, using heat dissipation spacers between units is recommended."* At
1.2 W each that is 2.4 W into a sealed box and nothing to worry about - but the rail has room to
spare, so do not butt them together for no reason.

NOTE: **A 230 V COIL ON US 240 V NOMINAL SITS ABOVE ITS RATING, AND IT DOES NOT MATTER HERE.** Coil
tolerance on these parts is normally wide enough to cover it and the Ue is 250 V AC; the heat it costs
is 1.2 W scaled by the voltage ratio squared, which is a fraction of a watt. Recorded because "230 V
coil on a 240 V circuit" is the kind of thing that looks like an oversight later.

SETTLED: **2NO - so both hots are switched.** This was the open question and the spec table answers
it. On a 1NO + 1NC part the second pole would have been a normally-closed *auxiliary* rather than a
second switched leg, leaving one hot live downstream of the paddle for ever while the machine started,
stopped and behaved perfectly.

PROCEDURE: **METER IT ANYWAY, ONCE, BEFORE IT GOES IN** - both load terminals against their line
terminals with the coil de-energised. This is a vendor's word on a listing, and in this repo a
vendor's word on exactly this kind of claim has already been **wrong**: the IG57 seller said the four
opto minus legs were commoned inside the drive and a one-minute meter check overturned it, which is
why [`ig57-drives.md`](ig57-drives.md) carries the reading rather than the claim. One minute, and it
is the one failure here that cannot be seen in operation.

FLAG: **THE TWO RATINGS ARE NOT INTERCHANGEABLE, AND THE SAME PART READS OFF A DIFFERENT COLUMN IN
EACH POSITION.** The vendor's own words: AC-7a is *"resistive household loads"* at 25 A, AC-7b is
*"inductive motor loads ... which have high inrush currents"* at 9 A.

| Position | Column that binds | Load | Margin |
|---|---|---|---|
| **Main** | **AC-7a, 25 A** | two switch-mode supplies, the VFD's input rectifier, one coil - no motor | ~14.9 A |
| **Pump** | **AC-7b, 9 A** | the 80 W pump, a real motor | ~0.4 A |

**The 9 A is the figure that looks alarming and it only applies to the pump**, where it has twenty-odd
times the margin it needs. The main contactor never sees a motor: the spindle sits downstream of the
VFD's own output stage and never touches these contacts, and the pump is behind the second contactor.
**FLAG: this file said "an AC-1 part" until the listings were read** - that was wrong, and the real
categories are AC-7a/AC-7b.

NOTE: **Neither AC-7 category actually describes the load, and that is the honest limit of the
datasheet.** A rectifier-and-capacitor front end is not resistive and not slightly inductive - it is a
**capacitive inrush** at the instant the contacts make, and all three supplies do it at once.
**100,000 cycles against a machine that lives powered** is what makes this a non-issue rather than any
number in the table: on his usage the paddle closes for an emergency, a motor fault or a wiring job,
so the cycle count will never be approached.

✅ **AND THE LOW-HOLDING-POWER COIL IS A REAL MATCH FOR THIS BOX, NOT MARKETING.** The listing sells
*"less holding power ... reducing the hot-to-touch issue ... safer for enclosed distribution
boards"*. This coil is **energised continuously** - the machine lives on - inside a **sealed PVC box
with no ventilation**. A cool-running coil is exactly the right property for that combination, and it
is worth remembering when the question of what else goes in the box gets answered.

NOTE: **THE PUMP CONTACTOR IS SIZED BY WHAT IS SOLD, NOT BY THE LOAD.** The pump is **80 W** - about
0.4 A at 220 V - and the bottom of most DIN ranges is a 9 A body, already twenty-odd times what it
draws. The contactor is there to keep a motor off the VFD's internal relay, which is not a
replaceable part; see the pump section below.

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
SETTLED: **the pump contactor takes a 220 V coil, off pair 3 - his decision, 2026-11-05**, and the
relay switches it directly. No 24 V anywhere, no extra supply, no flyback diode - a dry contact does
not care about polarity and has no inductive kick to catch. **220 V rather than 110 V keeps the whole
pump branch on the switched 220 V**, with no conductor crossing between the two circuits.

NOTE: **A 12 V DIN relay off the UPF opto output was the alternative and was declined.** It would
have kept mains off the VFD's control strip at the cost of a relay and a parameter. His call, and the
caution below is what it would have bought.

🔴 **SO THERE IS MAINS ON THE VFD'S CONTROL TERMINAL STRIP, BESIDE THE ANALOG.** The same strip
carries the **0-10 V speed reference** and **FOR / DCM** from the interface board, and RS485 if it is
ever used. **Bring the coil pair in sleeved and separate, and out the opposite end of the strip from
the analog pair** - not bundled with them, and not down the same sleeve. A 0-10 V reference running
alongside a switched 220 V coil is the kind of coupling that shows up as spindle speed jitter and
gets blamed on the drive.

**One parameter sets the output:**

| | |
|---|---|
| **PD052** | Multi-Output 3, the FA/FB/FC function. **Factory setting 02**, Fault Indication |
| **Set it to 01** | *"In Run: the contact will act when the inverter has output or receives the running command"* |

NOTE: **PD053 and the KA/KB pair are a spare of the same rating**, factory-set to 00, invalid - so if
the fault indication is wanted as well, it does not cost the pump its relay.

OPEN: **WHICH OF FB AND FC IS THE NORMALLY-OPEN LEG.** The manual gives the pair as *"N/O or N/C"*
and does not say which is which. It is a meter on the real part with the drive unpowered, not
something to take from a convention.

SETTLED: **THE COIL INRUSH AGAINST THE RELAY'S 3 A - CLOSED, WITH ROOM TO SPARE.** The WCT-25's
230 V coil is **inrush 11.5 VA, holding 2.8 VA**. At 230 V that is **50 mA to pull in and 12 mA to
hold**, against a contact rated **3 A** - about sixty times the margin. This was the open question
that gated the pump contactor and it is answered by the part's own datasheet rather than by a
measurement.

### The paddle is for emergencies and for service - the machine lives powered

**His usage, 2026-11-05: the CNC stays on all the time.** The paddle comes down for three reasons and
no others - an emergency, **clearing a motor fault**, and working on the wiring.

NOTE: **THAT MAKES DROPPING POWER A DIAGNOSTIC STEP, NOT ONLY A SAFETY ONE.** A latched drive alarm
is cleared by taking the rail away from it, which is why the paddle is the tool he reaches for. Worth
knowing beside the IG57's alarm output and the fact that its manual contains no fault code table -
see [`ig57-drives.md`](ig57-drives.md).

✅ **AND THE VFD MANUAL ASKS FOR EXACTLY THIS USAGE, IN SO MANY WORDS.** Its installation notes say:
*"Do not use the electromagnetic contactor as the on/off button of power supply for the inverter."*
**His usage already satisfies that** - the paddle is for an emergency, a motor fault or a wiring job,
not for turning the machine off at night. Recorded with the manual's own wording because the day
someone starts using the paddle as a daily switch, this is the sentence that explains why the drive
started failing. The run/stop command belongs on FOR/DCM from the controller, which is where the
interface board already puts it.

### The controller survives the E-stop - and that is why the sense relay is not optional

SETTLED: **his, 2026-11-06.** The 12 V supply sits on the 110 V side, so the paddle takes the
**36 V rail and the VFD's mains** and leaves the **RP23 running**. Motion stops the same instant it
always did; what survives is the controller's position, its alarm state and the ioSender session.

🔴 **A CONTROLLER THAT OUTLIVES THE DRIVES AND DOES NOT KNOW IT IS WORSE THAN ONE THAT DIES WITH
THEM.** If the paddle only removes power and the RP23 is never told, it keeps issuing step pulses
into drives that cannot move. **The motors stay still and the position counter does not** - so when
power comes back the machine's idea of where it is, is wrong by however far it "moved" while dead.
Nothing about that is visible until the next rapid puts the spindle somewhere it should not be.

SETTLED: **A SENSE RELAY, AND IT SENSES THE SWITCHED 220 V RATHER THAN THE PADDLE.**

| | |
|---|---|
| Coil | **230 V**, on **pair 4** of the block - the pair the 12 V supply vacated |
| Contact | into the interface board's **e-stop input** - the Mini-Fit Jr 4P already carries one, see [`kicad/interface-board/README.md`](kicad/interface-board/README.md) |
| Size | one more **18 mm** DIN module |

✅ **SENSING THE LOAD SIDE RATHER THAN THE SWITCH IS THE WHOLE POINT.** It reports **power actually
present at the drives**, not what the operator pressed. A welded contactor reads as powered, which is
true and is what you want to know; a paddle-side sense would have read "stopped" while the machine
was still live.

NOTE: **This is the same pattern as the pump contactor** - a coil on the switched side, a contact
doing the telling. One part, one idea, used twice.

🔴 **BUT IT IS ALSO THE SERVICE DISCONNECT, AND IT DOES NOT MAKE THE BOX SAFE.** This is the one
thing to have straight before hands go in. With the paddle down, all four pairs off the block are
dead - and **two things are still live**:

| With the paddle down | |
|---|---|
| The pairs off the 2 x 8 block | **dead** |
| **The entire 110 V side** - the 6 A breaker, the 2 x 6 splitter and all three of its pairs | **LIVE** |
| The **12 V supply, and everything it feeds** | **LIVE** - the controller is still running |
| The **receptacle and the power strip in it** | **LIVE** |
| The **paddle's own control circuit**, upstream of the switch | **LIVE** |
| The **220 V on the contactor's line side** | **LIVE**, up to the contactor's own terminals |

🔴 **ONE ROW IS DEAD AND FIVE ARE LIVE.** That is the design working as intended and it is also the
thing to have straight before hands go in: **more of this box is live with the paddle down than is
dead.** The paddle is an emergency stop that happens to be convenient for service; it is not a
disconnect, and nothing about its position tells you which circuit it dropped.

PROCEDURE: **FOR WIRING WORK, PULL BOTH PIGTAILS.** His, 2026-11-05, and it is the reason the inputs
are captive cords. Two plugs on the floor is a disconnect you can **see** from inside the box - which
is the whole advantage over a breaker in another room, and the reason to pull **both** rather than
only the 220.

SETTLED: **WHAT ELSE GOES ON THE 110 V CIRCUIT - the laptop and the USB cameras, unswitched.** His,
2026-11-05, and written up above.

SETTLED: **A DIN BREAKER PER BRANCH - his, 2026-11-05.** Resettable, one per branch so a fault takes
down one load instead of the cabinet, and it reads as a row. **Three on the 220 V rail and one on the
110 V rail** since 2026-11-06.

SETTLED: **THREE 6 A AND ONE 16 A, ALL 2-POLE - his, ordered 2026-11-05.** Same manufacturer as the
16 A. FLAG: **this read 10 A for one commit** - 6 A turned out to be available in the same family and
is the better number, because it is closer to the loads and so catches a fault sooner.

SETTLED: **ALL FOUR ARE CURVE C - ordered, his 2026-11-05.**

| Pair | Branch | Breaker | Load |
|---|---|---|---|
| 1 | 36 V motor supply | **6 A, Type C** | **3.5 A** in at 220 V - nameplate |
| 2 | VFD | **16 A, Type C** | see below |
| 3 | Pump contactor | **6 A, Type C** | **80 W**, about 0.4 A, plus an 11.5 VA coil |
| 4 | **Sense relay coil** | **none** | The 12 V supply left this pair on 2026-11-06; the sense relay took it |

NOTE: **PAIR 4 CARRIES NO BREAKER, AND THAT IS DELIBERATE.** All four breakers are spoken for - three
here and the fourth on the 110 V side - and what is left on this pair is a **sealed relay coil of a
couple of watts** on 14 AWG, behind the main contactor, with the wall's 20 A as the backstop. A
breaker sized for 2 W does not exist and would protect nothing the conductor does not already
survive.

✅ **CURVE C IS WHAT PAIRS 1 AND 2 ACTUALLY NEEDED, AND THE OTHER TWO COME ALONG FOR FREE.** Pair 1 is
6 A against a **3.5 A** nameplate - a ratio of 1.7 - and a 600 W switch-mode supply charges its input
capacitors at the instant the main contactor closes. A Type B there would have nuisance-tripped on
every power-up, which presents as the machine intermittently refusing to start and gets blamed on
the drive. Pair 2 is the same argument with the VFD's DC bus behind it.

NOTE: **Curve C on pairs 3 and 4 costs nothing.** A C curve trips magnetically higher than a B, which
matters only for how fast a dead short clears - and on 14 AWG behind a 20 A wall breaker there is
nothing in that gap to worry about. One curve across the panel is one less thing to get wrong at the
rail.

NOTE: **THESE ARE NOT PROTECTING THE LOADS AND DO NOT NEED TO.** A branch breaker here protects the
**conductor** and gives **isolation**. The loads look after themselves: both supplies carry their own
internal fusing, and nothing short of an overload relay would catch an 80 W pump stalling, which is
absurd at 80 watts. What 6 A over 10 A buys is a tighter envelope on the wiring, not load protection.

**14 AWG on all four branches, which is now generous rather than exact.** The conductor has to be
rated for its breaker rather than for its load, and at 6 A a lighter gauge would be legitimate - but
14 AWG was already the plan, costs nothing in a cabinet, and keeps one wire size across the panel.

NOTE: **SIX FUSES WAS THE ALTERNATIVE AND IT BUYS NOTHING.** Both legs of a 240 V two-hot branch are
ungrounded, so fusing would need **two per branch - six**, and the arithmetic comes out level: six
18 mm holders plus the VFD's 2-pole breaker is **144 mm**, which is exactly four 2-pole breakers.
Same width, seven devices instead of four, and **two independent fuses do not open together** - one
blows and the load sits half-energised with 120 V to ground on the surviving leg, which is a branch
that looks dead and is not.

SETTLED: **16 A ON THE VFD BRANCH, TYPE C.** Two reasons, and the second is the stronger one:

1. **It coordinates.** The wall breaker is **20 A**. A 20 A branch breaker beside a 20 A main gives no
   discrimination at all - a VFD fault would be as likely to drop the whole circuit as its own branch.
   16 A is the step below, which is the point of having a branch breaker.
2. **The duty is nowhere near it.** [`../machine/spindle-and-mount.md`](../machine/spindle-and-mount.md)
   establishes that a respectable cut on this frame draws about **0.3 kW at the cutter**, and that the
   spindle is five to seven times more powerful than the cut this machine can take. The VFD will spend
   its life at a few amps in.

FLAG: **AT THE DRIVE'S OWN FULL RATING 16 A WOULD BE CLOSE, AND THIS FRAME CANNOT GET THERE.** My
estimate, not a manual figure: 2.2 kW out plus losses is about 2.3 kW in, and a diode-bridge-and-
capacitor front end draws that at a poor distortion power factor, which puts the input RMS current
somewhere in the **14 to 16 A** region at full rated output. **The manual gives no input current
figure at all.** It does not bite here because the cut cannot reach full output - but it is the reason
not to read the margin as larger than it is.

🔴 **AND IT CORRECTS A NUMBER IN THIS FILE'S OWN MAINS TABLE.** Observation, from the manual's
specification table: the **HY02D223B is 2.2 kW, 4.4 kVA capacity, 11 A OUTPUT current**, single or
three phase 220 V in. The mains table below carries *"2.2 kW spindle | ~11 A"* as a **draw** - and
11 A is exactly the manual's **output** figure. **Output and single-phase input current are not the
same number for this drive**, and the input one is larger. Interpretation, not established: that
~11 A looks like an output rating being read as a mains draw. **What would settle it is a clamp meter
on the VFD's input while cutting** - which also belongs in
[`../commissioning/bench-session.md`](../commissioning/bench-session.md) rather than being computed.

🔴 **ALL FOUR ARE 2-POLE, AND THIS IS THE SAME TRAP AS THE CONTACTOR'S 2NO.** Every pair off the
block is **two hots with no neutral**, so a single-pole breaker breaks one leg and leaves the other
connected - the load is then half-isolated when the breaker is off or tripped, with one leg still live
to ground at its terminals. For a branch you will switch off to work on a supply, that is the
difference between dead and looking dead.

FLAG: **TYPE C ON THE VFD'S BREAKER, NOT TYPE B.** The drive charges its DC bus every time the main
contactor closes, and that inrush will trip a tightly-sized Type B curve - which presents as the
machine refusing to power up intermittently and gets blamed on the drive. The same argument applies
in miniature to pair 1, which is a switch-mode supply doing the same thing.

SETTLED: **TWO RAILS, AND THE SPLIT IS BY VOLTAGE - his, 2026-11-06.** A 2-pole breaker is **two
modules, 36 mm**:

| Rail | On it |
|---|---|
| **Top - the 220 V side** | Main contactor, pump contactor, the **2 x 8 block**, the **three** 220 V breakers, the sense relay, and **every ground terminal** |
| **Bottom - the 110 V side and the supplies** | The **6 A 110 V breaker**, the **2 x 6 splitter**, the 1 A fuse holder, the **MDR 12 V supply**, and the **36 V brick** |

✅ **SPLITTING BY VOLTAGE RATHER THAN BY DEVICE TYPE IS THE BETTER ARRANGEMENT**, and it falls out of
the 12 V supply moving: everything the paddle kills is on one rail and everything that stays live is
on the other. Anyone opening this box can tell at a glance which row is dead.

🔴 **EVERY GROUND TERMINAL GOES ON ONE RAIL, AND IT MUST BE THE SAME ONE.** The green-and-yellow
terminals use **the rail itself as the bus**, so **two rails are two separate ground buses** unless
they are bonded - and a bond between rails puts a joint in the one path this arrangement exists to
keep single. The top rail is the PE bar.

NOTE: **Nine terminal bodies at two positions each is eighteen**, against the eight conductors named
below. His, 2026-11-06. Generous, which is the right direction.

**What a DIN rail needs vertically.** FLAG: **these are standard-practice figures, not measured off
his parts** - the WCT-25 listing gives 18 mm of width and says nothing about height, so check them
against the real breakers before the back panel is drilled:

| | |
|---|---|
| The rail itself | **35 mm** across, **7.5 mm** deep. A 15 mm deep version exists and is not needed here |
| A modular device, across the rail | **about 85 mm** - call it 80 to 90 depending on make |
| Rail centre to rail centre | **150 mm** is the comfortable convention. 125 mm works. Below about 110 mm the wiring between rows gets mean |

✅ **SO TWO RAILS FIT A 12 INCH BOX WITH ROOM, AND THREE DO NOT.** At 150 mm centres, two rails plus
roughly 45 mm of clearance above the top device and below the bottom one comes to about **240 mm of
the 305**. Three rails at the same pitch needs 300 mm before any clearance at all, so three means
crowding the pitch rather than using the space.

NOTE: **DEPTH IS NOT THE CONSTRAINT.** A modular device stands roughly 70 mm off the panel plus the
rail, against **6 inches** of box. The 600 W supply and the VFD are the parts that would test it -
which is the open question above, not this one.

PROCEDURE: **LAY THE WHOLE THING OUT IN THE BOX BEFORE ANYTHING IS DRILLED, AND SEND THE BOX BACK IF
IT DOES NOT FIT.** His, 2026-11-05. That is why none of the figures above need to be right to the
millimetre - the parts in the real box settle it, and the box is the cheapest thing in the cabinet to
change. It also means the what-goes-inside question gets answered by the same mock-up rather than on
paper.

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

### OPEN: a DIN-rail motor supply, so the VFD is the only thing outside the box

**His thought, 2026-11-06, and the motive is layout rather than electrical:** the 600 W brick is the
one piece of high-voltage gear that is neither DIN nor small. Put the motor supply on the rail and
**everything high-voltage lives in the DIN enclosure or the VFD's**, which closes the
what-is-in-the-box question outright.

| Candidate | |
|---|---|
| **Mean Well XDR-480E-36** | **36 V, 13.3 A, 480 W**, DIN rail. The one to look at |
| Mean Well DRS-480-36 | Same output, but carries a **battery charge circuit** that is not wanted here |
| The 36 V 600 W brick | Already owned. **16.5 A**, not DIN |

✅ **IT DOES NOT TOUCH THE 36 V DECISION, WHICH IS THE POINT.** The thought started as a **48 V 10 A
480 W** DIN unit and that was declined: **48 V is the top of the manual's own §7.3 range, DC24V~48V**,
with about 2 V to the over-voltage alarm - the exact argument that settled 36 V on 2026-10-12. **And
13.3 A at 36 V is more comfortable than 10 A at 48 V** - his call, and it is the same 480 W either
way, so the voltage came free.

🔴 **THE REAL COST IS HEAT, NOT WATTS, AND IT CUTS AGAINST THE TIDINESS.** A brick outside the box
dissipates outside it. **On the rail it dissipates into a dust-proof PVC enclosure with no
ventilation** - tens of watts at half load, against the **2.4 W** the two contactors contribute. That
is the enclosure section's heat question arriving for real.

SETTLED: **WHERE THE BOX MOUNTS - underneath the torsion box, middle and back. His, 2026-11-06.** The
box's **back wall and its centre wall seal that bay off**, so the enclosure sees **general shop dust
and no chips at all**.

**His answer to the heat: drill it and let air through** - and that location is what makes it cheap.
FLAG: **this file argued for venting the face rather than the top, and for filtering the holes.
Both were built on the box being somewhere swarf lands, and it is not.** Vent it wherever is
convenient.

✅ **AND THAT BAY IS NOT A SEALED POCKET - his, 2026-11-06.** There is a gap **all the way around**
between the underside of the torsion box and the top of the base walls, and **the whole front is
open**. Warm air leaving the enclosure has somewhere to go.

NOTE: **That clearance is not there for cooling - it is the three-point mount.** The box lands on
three posts and **nothing else may touch it**, or there is a fourth contact point and the mount stops
being three-point, silently - see [`../machine/assembly.md`](../machine/assembly.md). The ventilation
is a free consequence of a decision taken for geometry.

FLAG: **He gave the gap as both 4 mm and 10 mm in one sentence and I have not recorded either.** It
does not matter here - what matters is that the bay breathes - but do not take a figure for it from
this page.

**The other cost is 480 W against the brick's 594 W**, and that is unestablished either way - see the
comparison below, which [`../commissioning/bench-session.md`](../commissioning/bench-session.md)
settles. **Not decided.** The mock-up in the real box is what should decide it, because the heat is
the half that cannot be reasoned out on paper.

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

SETTLED: **THE LOGIC RAIL IS ITS OWN MAINS-FED 12 V SUPPLY - and since 2026-11-06 it is fed from the
110 V side, not from pair 4.** That is what keeps the controller alive through an E-stop. Then
**point-of-load regulation per consumer** rather than one rail fanned out.

SETTLED: **MEAN WELL MDR SERIES, 12 V 40 W - his, 2026-11-05.** FLAG: **this read MDR-60-12, 60 W,
5 A for one commit** - the 60 W listing was pasted twice and the choice is the **40 W**.

| | |
|---|---|
| Output | **12 V, 3.3 A, 40 W** |
| Form | **DIN rail**, screw terminals |
| Part | **MDR-40-12** by the series' naming - confirm against the order rather than from the pattern |
| Input draw | about **0.2 A** at 220 V, from 40 W out at a typical efficiency - not a nameplate figure |
| Rail width | **not established.** The MDR-40 body is narrower than the MDR-60's 40 mm; the figure in the rail budget is the 60's and is therefore pessimistic |

NOTE: **3.3 A is sufficient - his call, 2026-11-05: he doubts the whole 12 V side pulls even 2 A.**
The supply reports nothing, so the figure to compare it against comes off the rail when the box is
first powered. Not a gate on anything.

✅ **BEING DIN RAIL NARROWS THE WHAT-IS-IN-THE-BOX QUESTION.** This supply goes on the **bottom rail,
beside the 110 V breaker that feeds it** - so the only part still unplaced is the **VFD**, which is
neither DIN nor small. The 36 V brick is on that rail too.

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

## The enclosure is a 12 x 12 x 6 PVC box

SETTLED: **his, ordered 2026-11-05** - and it closes the question of which box the DIN rail lives in.

| | |
|---|---|
| Size | **12 x 12 x 6 inches** |
| Material | **PVC**, grey, non-metallic |
| Entries | pre-moulded **3/4 inch and 1 inch** punch-in holes, **all four sides** |
| Cover | **dust-proof**, screw-on. Rated indoor/outdoor |

✅ **NON-CORRODING AND COVERED IS THE RIGHT CALL FOR WHERE THIS LIVES**, which since 2026-11-06 is
**underneath the torsion box, middle and back** - sealed off by the box's back wall and its centre
wall. **General shop dust, no chips.** FLAG: **this paragraph argued the dust-proof cover against
conductive swarf until 2026-11-06**; the location rules that out, and it is why venting the enclosure
is cheap rather than a trade.

✅ **AND A PLASTIC BOX MAKES THE SINGLE-POINT STAR BELOW ACTUALLY SINGLE-POINT.** In a metal
enclosure every mounting screw, every DIN rail foot and every supply case touching the panel is
another ground path in parallel with the bar - which is the loop the next section exists to prevent,
arriving by accident. PVC cannot make one.

🔴 **BUT NOTHING IN A PVC BOX IS BONDED BY BEING MOUNTED IN IT.** In a metal box a supply's case
earths through its own screws for free. Here it does not. **Every metal-cased device gets its own PE
conductor to the bar** - the 36 V supply, the 12 V supply, the VFD - and that is a wire per device,
not an afterthought.

FLAG: **A PVC BOX IS NOT A SHIELD EITHER.** The VFD is the aggressor this file already flags, and a
non-metallic enclosure does nothing to contain it. That is an argument about what goes **inside** the
box rather than against the box - see the open item below.

OPEN: **WHAT IS IN THIS BOX AND WHAT IS OUTSIDE IT.** His words are *"all the DIN rail
components"*, and 12 x 12 is **144 square inches of back panel**. The DIN gear - two contactors, the
2 x 8 block, the fuse holders - is small. The **36 V 600 W supply is a brick**, the VFD is another,
and neither is a DIN part. Whether those two mount in this box, beside it, or in something larger
that contains it is not stated, and it decides whether "the cabinet" in this file means this box.

FLAG: **AND IT IS A HEAT QUESTION, NOT ONLY A SPACE ONE - a dust-proof box has no ventilation.**
Whatever goes in dissipates into a sealed plastic volume that is **energised continuously**, because
the machine lives powered. **The DIN gear is nothing: 1.2 W per contactor, 2.4 W for both.** A 600 W
supply is a different proposition even at a fraction of load, and the VFD has a heatsink for a
reason.

NOTE: **SO VENTING IT IS CHEAP, AND SO IS LEAVING THE COVER OFF.** Both looked like a trade against
dust-proofing until the mounting position was recorded on 2026-11-06. Under the torsion box behind
two walls there are **no chips to keep out**, only general dust - which is a thing to blow out of a
terminal block occasionally, not a thing that kills one.

## Grounds meet at one PE bus bar

Every ground conductor in the cabinet lands on **one PE bus bar**, and nothing daisy-chains.

| Conductor | Note |
|---|---|
| PE in - 220 V pigtail | the conductor that actually connects this bar to earth |
| PE in - 110 V pigtail | the second one |
| ~~Cabinet chassis~~ | **n/a - the box is PVC.** There is no chassis to bond; see above |
| Machine frame | |
| 36 V supply case | **its own conductor** - the box bonds nothing |
| 12 V supply case | the MDR is DIN mounted and still needs its own |
| Motor supply 0 V | the 36 V rail's return |
| 12 V 0 V | the logic supply's return |
| VFD **E** terminal | **its own short heavy conductor.** FLAG: **the VFD's case is plastic - his, 2026-11-05 - and that changes nothing here.** There is no case to bond, but the drive has an earth terminal: the manual's main-circuit table lists **E, "ground terminal ... of Electrical Engineering Regulations"**. A plastic case means no case bond, not no earth |
| Cable shields | **one end only** |

**So the bar needs ten terminals, not six.** Eight are named and firm:

| | Conductor |
|---|---|
| 1 | PE in - 220 V pigtail |
| 2 | PE in - 110 V pigtail |
| 3 | Machine frame |
| 4 | VFD **E** terminal |
| 5 | 36 V supply case |
| 6 | 12 V supply case |
| 7 | Motor supply 0 V |
| 8 | 12 V supply 0 V |

SETTLED: **TEN IS THE BUY - the signal cables contribute nothing.** His, 2026-11-05: **all the drive
cables terminate at the interface board, in its own 3D printed enclosure**, not in this box. And they
are **Cat 6 UTP** - see [`kicad/interface-board/README.md`](kicad/interface-board/README.md), which
notes the jack is shielded but *"the patch cables are UTP so it carries nothing"*. **No drain wire,
no terminal.**

OPEN: **THE ONLY SHIELDS IN THE SYSTEM ARE THE FOUR 18/2 MOTOR SUPPLY RUNS, and they follow the 36 V
supply rather than this bar.** Each drive's supply is **18/2 shielded** - see
[`ig57-drives.md`](ig57-drives.md) - so there are four drains, grounded at one end only. Whether they
reach this bar is the same question as where the 36 V supply ends up. **Ten leaves two spare if they
land elsewhere and comes up short if all four land here**, which is the argument for buying more than
ten rather than exactly ten.

NOTE: **EVERY ENCLOSURE IN THIS BUILD IS PLASTIC - the distribution box, the paddle's gang box and
now the interface board's.** Nothing anywhere is bonded by being mounted in something, so every earth
in the system is a conductor somebody ran on purpose. That is the arrangement working as intended
rather than a problem, and it is worth knowing before anyone goes looking for a chassis to test
against.

NOTE: **ERR UP, BECAUSE A SECOND BAR IS THE AWKWARD FIX.** Running out means either a second bar
bonded to the first, which puts a joint in the one path this whole arrangement exists to keep
single, or re-landing conductors two to a screw. Terminals are the cheapest thing on the rail.

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
| ~~12 V supply~~ | **moved to the 110 V circuit, 2026-11-06** |
| **Total** | **~14.9 A** against a **16 A** continuous limit |

NOTE: **EVERY LOAD LEFT ON THIS CIRCUIT HAS A NUMBER, AND ONLY ONE OF THEM IS IN DOUBT.** **The
spindle's 11 A is the term that decides this table** and it is the one flagged above as possibly the
drive's *output* current rather than its mains draw - so the right reading of ~14.9 against 16 is
"comfortable if the 11 is right, and the 11 is what to go and measure."

**On the 110 V circuit, against its own 20 A:** the 12 V supply at about **0.4 A** at this voltage,
the laptop charger at a couple of amps, the cameras and powered USB well under one. A few amps of
twenty, and all of it behind the 6 A breaker.

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
