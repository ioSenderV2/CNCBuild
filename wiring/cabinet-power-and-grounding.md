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

Everything downstream of that is behind **two E-stop switches in series** - a **locking mushroom** on
the apron and the **magnetic paddle** below it, with its big red stop paddle and small green start
button, at 110 V. The paddle's output drives the **coil** of a **25 A 220 V contactor with a 110 V
coil**, and that contactor is what actually carries the 220 V. His scheme, 2026-11-05; the second
switch is his, 2026-11-07, and the series arrangement is set out below.

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
restores power to a machine nobody is standing at, the moment the mains returns. **It is also why the
paddle stays in the circuit now that there are two switches** - the mushroom in series with it cannot
do this, and does not have to, because the paddle is still there doing it. See the two-switch section
below.

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

SETTLED: **A 1 A FUSE ON THE CONTROL CIRCUIT - his, 2026-11-05.** The two switches and the
contactor coil are the whole of the load on the 110 V side, and a coil draws almost nothing, so the
20 A breaker at the wall is protecting the house rather than this wiring. **1 A puts a fuse in front
of the control conductors that is sized for what they actually carry** - and it is the branch where a
fault is most likely to be a pinched wire in a door hinge rather than a load fault.

### Two switches in series - a mushroom at the bed, the paddle below

SETTLED: **his, 2026-11-07. There are TWO E-stop switches, in series on the contactor coil
circuit** - a **locking mushroom** up on the apron where a hand lands, and the **magnetic paddle**
below. Either one stops the machine; **neither one can start it.**

🔴 **THE MOTIVE IS WHERE THE HAND GOES, AND IT IS THE PADDLE'S ONE WEAKNESS.** The paddle has to
live about **a foot below the table surface**, because the torsion box is in the way. **The mushroom
sits on top, right in front of the bed, centred between the two fins** - the place you are already
standing when something goes wrong.

✅ **AND SERIES IS NOT A COMPROMISE BETWEEN THE TWO - IT IS BETTER THAN EITHER ALONE.** The paddle
stays in the coil circuit, so it keeps doing the thing it was bought for: **a mains failure drops it
and it stays dropped.** The mushroom adds a stop where the hand is, and gives up nothing.

| How it went dead | What has to happen to come back |
|---|---|
| **The mushroom was pressed** | **Twist it to release, then press the paddle's green button.** Releasing the mushroom on its own restores nothing |
| **The paddle was pressed** | **Press the green button** |
| **The mains went away on its own** - outage, tripped breaker, a pigtail pulled | **Press the green button.** The paddle dropped out for want of 110 V and does not pick up again by itself |

🔴 **THE ORDER IS NOT OPTIONAL: THE MUSHROOM GOES UPSTREAM OF THE PADDLE.** Between the **1 A fuse
and the paddle's 13 and 23** - so the paddle's own holding coil is fed *through* the mushroom.
Pressing the mushroom then takes line power away from the paddle, the paddle drops out, and the
green button is what brings it back. **That is the whole reason the arrangement works.**

FLAG: **DOWNSTREAM INVERTS IT, AND SILENTLY.** Wired between the paddle's **14/24** and the
contactor's A1/A2 instead, the paddle keeps its line power and **stays latched in**. The mushroom then
only interrupts the coil feed, so **twisting it back pulls the contactor straight in with no green
button** - a restart on a twist, at the one spot on the machine that is easiest to knock. It is the
worst of the arrangements and it looks identical from outside the box.

NOTE: **This follows from the switch having to hold itself in with a dead load side**, so its coil
must be fed from the in side. PROCEDURE: **Meter it on the real paddle before wiring** - with the
switch latched in and no load connected, the coil is being fed from 13/23 or it could never have
pulled in. Not a convention to take from this page.

SETTLED: **ONE NC CONTACT IS ENOUGH ON THE MUSHROOM.** The both-poles-isolated property that
13-14 and 23-24 bought survives for free: **the paddle drops out whenever the mushroom opens, and
the paddle opens both legs.** A 2NC block costs little and buys no isolation that is not already
there.

NOTE: **THE CONTROL CIRCUIT IS NOW A SERIES LOOP THROUGH TWO BOXES**, not one run out and back. Panel
to the mushroom, mushroom to the paddle box, paddle box back to the panel - or each device its own run
back to the panel, which is more cable and fewer joints. **A routing choice, not an electrical one.**

NOTE: **The four 1/4 inch female quick-disconnects are the paddle's requirement**; the mushroom
station's contact blocks are screw terminals. Both parts are in the design now, so both are a buy.

**The cost of the arrangement is the restart, not the stop.** Stopping moves up to the bed where it
is wanted. **The green button stays a foot down behind the torsion box**, and it is now needed after a
mushroom press as well as after a paddle press.

#### Where the mushroom mounts

SETTLED: **his, 2026-11-07 - on the apron, centred between the two fins, about 2 inches forward of
the tee track bed's front edge.**

✅ **THAT IS CLEAR DECK AND THE REPO ALREADY SAYS SO.** The bed's front edge and the fin's back face
are both at the same place, and the box's top skin runs **{{BOX_FRONT_OVERHANG}} mm past the fins** -
see [`../dimensions/VALUES.md`](../dimensions/VALUES.md). **2 inches sits well inside that apron**,
and the apron is **already where the toolsetter and the shop clutter live on the Mega V**, so a device
standing proud there is not a new idea.

✅ **CENTRED BETWEEN THE FINS IS ALSO CLEAR OF THE FIN ANGLES.** Each fin carries one length of
40 x 40 angle in **front** of it - see [`../machine/assembly.md`](../machine/assembly.md) - and those
sit at the fins, out at the two ends. The middle of the apron has nothing on it.

✅ **AND IT IS OUTSIDE THE TRAVEL ENVELOPE.** Max Y travel is reached with the **Z plate's front face
level with the beam end**, where the riser starts - closed 2026-10-02, see
[`../machine/open-items.md`](../machine/open-items.md). The apron is forward of that.

PROCEDURE: **Check it against what hangs off the FRONT of the Z plate, not against the plate.** The
envelope note is about the plate's own face; the spindle and anything on it project further forward
than that, and 2 inches is not a lot of margin. **Push the gantry to max Y by hand and look**, before
the hole is cut - the apron is the one place on this machine where a surface-mounted device and the
gantry are both trying to be.

NOTE: **AND THE DROP-OUT CAN BE BOUGHT BACK IF IT IS WANTED - a green start button and one normally-open
auxiliary contact on the contactor, wired across the button.** That is the ordinary three-wire
start/stop: the auxiliary holds the coil in, and losing the mains makes it let go. A contact block and
a button, not a redesign - recorded so the choice is a choice, not a thing discovered later.

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
| 4 | **Spare** - the 12 V supply left this pair on 2026-11-06, the sense relay took it, and on 2026-11-09 the sense moved to the 36 V rail and gave it back |

SETTLED: **THE BLOCK GOES ON THE RAIL UPSIDE DOWN - his, 2026-11-06, and it is not a violation of
anything that matters.** The contactor's load terminals are at the **bottom**; the breakers' line
terminals are at the **top**. Inverting the block puts its input at the bottom and its outputs at the
top, so the contactor makes one short U-turn into it and each pair makes one short U-turn out to a
breaker. **No long runs and nothing crossing.**

✅ **A PASSIVE BLOCK HAS NO LINE AND LOAD SIDE, WHICH IS WHY THIS IS FREE.** The top-in bottom-out
convention exists for devices that care - breakers, where busbar combs feed the top and some makes
mark a direction. A feed-through terminal block is symmetric: there is nothing inside it to install
backwards.

✅ **AND THERE IS NO PRINTING ON IT TO READ UPSIDE DOWN - his, 2026-11-06.** The two poles are told
apart by **colour, red and blue**, and colour survives being inverted. FLAG: **this file warned about
inverted printing until 2026-11-06**; there is none, so flipping the block costs nothing at all.

✅ **AND THE WIRE COLOURS NOW AGREE WITH THE BLOCK'S OWN - so nothing has to be written on the panel
to say which row is which.** See the scheme below. That was an open item for exactly one day.

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

✅ **AND IT CAN BE ANSWERED TODAY, BECAUSE THE MEGA V RUNS THE SAME DRIVE.** His, 2026-11-07: the
Mega V has the **identical spindle and VFD from the same supplier**. So this check does not wait on
the new machine - it is a meter on a drive that is already in the shop.

🔴 **THAT MAKES THE MEGA V A WORKING REFERENCE FOR THE WHOLE SPINDLE AND VFD HALF OF THIS BUILD, AND
IT HAS NOT BEEN USED AS ONE.** Anything uncertain about the HY02D223B - the relay legs, what PD052
does, what the control strip looks like, what the drive actually draws on its input - is a
measurement on a running machine rather than a question for a manual that declines to answer. The
clamp-meter reading this file wants on the VFD's input is in the same position.

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

SETTLED: **IT SENSES THE 36 V RAIL ITSELF - his, 2026-11-09**, moved there from a 230 V coil on
pair 4.

| | |
|---|---|
| Input | across the **36 V rail**, at the board end of it |
| Contact | **closed while the rail is up**, into the interface board's **e-stop input** - the Mini-Fit Jr 4P already carries one, see [`kicad/interface-board/README.md`](kicad/interface-board/README.md) |
| Direction | 🔴 **FAIL-SAFE, AND THAT IS WHY THE CONTACT IS CLOSED WHEN ALL IS WELL.** Rail gone, wire broken, part dead - all three open the loop and all three read as e-stop. A contact that had to *close* to call the stop would fail silently |

✅ **SENSING THE LOAD SIDE RATHER THAN THE SWITCH IS THE WHOLE POINT, AND THE RAIL IS AS LOAD-SIDE
AS IT GETS.** It reports **power actually present at the drives**, not what the operator pressed. A
welded contactor reads as powered, which is true and is what you want to know; a switch-side sense
would have read "stopped" while the machine was still live.

✅ **AND IT COVERS A CASE THE 230 V SENSE COULD NOT: THE SUPPLY ITSELF FAILING.** Every way the
machine goes dead now reaches the controller - mushroom, paddle, a mains outage, *and* a supply that
quits or shuts down on its own over-current protection.

🔴 **36 V IS NOT A STANDARD COIL VOLTAGE, AND THAT IS THE WHOLE DIFFICULTY OF THE PART.** Standard
DC coils are 12, 24 and 48. **A 24 V coil cooks on 36 V; a 48 V coil may not pull in at 36 V**,
since pull-in is typically three quarters of nominal and that is 36 V exactly - the worst place to
sit. So the part has to be one that takes 36 V by specification, not by luck.

⚠️ **THE RAIL DECAYS, IT DOES NOT VANISH.** The supply's output capacitance and five drives' input
capacitance hold it up after the contactor opens, so the sense drops late by however long that takes.
**A part with an adjustable threshold, set high - around 30 V - drops promptly instead of waiting for
the rail to sag to a quarter.** This is the argument for a monitoring relay over a plain coil.

OPEN: **the exact part is not chosen.** Two numbers decide it: the input must include **36 V DC** by
specification, and the output must suit the e-stop loop. Datasheet gets committed here when it is.

NOTE: **Pair 4 of the 2 x 8 block is free again** - the 12 V supply vacated it, the sense relay took
it, and now nothing does.

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
| 4 | **Spare** | **none** | Vacated twice: the 12 V supply on 2026-11-06, then the sense relay on 2026-11-09 when the sense moved to the 36 V rail |

NOTE: **PAIR 4 CARRIES NO BREAKER, AND THAT IS DELIBERATE.** All four breakers are spoken for - three
here and the fourth on the 110 V side - and what was left on this pair was a **sealed relay coil of a
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
| **Top - the 220 V side** | Main contactor, pump contactor, the **2 x 8 block**, the **three** 220 V breakers, and **every ground terminal** |
| **Bottom - the 110 V side and the supplies** | The **6 A 110 V breaker**, the **2 x 6 splitter**, the 1 A fuse holder, the **MDR 12 V supply**, the **36 V brick**, and the **rail sense** - it belongs beside the supply it watches now, not up with the 220 V |

✅ **SPLITTING BY VOLTAGE RATHER THAN BY DEVICE TYPE IS THE BETTER ARRANGEMENT**, and it falls out of
the 12 V supply moving: everything the paddle kills is on one rail and everything that stays live is
on the other. Anyone opening this box can tell at a glance which row is dead.

### The wire colours

SETTLED: **his scheme, 2026-11-07.**

| Colour | Is | Where |
|---|---|---|
| **Blue** | **L1** | 220 V side, everywhere |
| **Red** | **L2** | 220 V side, everywhere |
| **Black** | **Hot** | 110 V side only |
| **White** | **Neutral** | 110 V side only - there is no neutral anywhere in the 220 V chain |
| **Green** | **PE** | every ground conductor to the bar |

✅ **IT CLOSES THE BLOCK'S LABELLING QUESTION BY ITSELF.** The 2 x 8 block tells its two poles apart
with **red and blue**, which is the same pair - so the wire colour and the block agree and there is
nothing to write on the panel about which row is which.

✅ **AND COLOUR NOW SAYS WHAT THE PADDLE KILLS.** Since the 12 V supply moved to the 110 V side, the
voltage split **is** the switched split: **blue or red dies, black or white lives.** One glance at a
conductor answers the question the live/dead table above takes a paragraph to answer.

NOTE: **The DC outputs are not in the scheme and do not need to be** - the 36 V out to the drives,
the spindle's U/V/W, the sense relay's dry contact. The drawing shows them grey and dashed to say so.

PROCEDURE: **[`panel-schematic.html`](panel-schematic.html) HOLDS THE SCHEME IN ONE PLACE.** Its
five colours are defined once as named values at the top of the file and every conductor on every
sheet refers to **what it is** rather than to a colour. Changing the scheme is five edits there and
nothing anywhere else - which is the only way the drawing and the panel stay agreeing.

### Which end is in, device by device

**Four devices on these rails and three different answers.** His, 2026-11-06, confirmed part by
part - worth one table because the panel labelling has to carry it and nothing about the hardware
makes it obvious:

| Device | Power in | Power out |
|---|---|---|
| **Breakers** | **top** | bottom |
| **Both WCT-25 contactors** | **top** - terminals 1 and 3 | bottom - 2 and 4. Coil on **A1 / A2** |
| **2 x 8 block**, mounted inverted | **bottom** | top. Poles told apart by **colour, red and blue** - no printing |
| **MDR 12 V supply** | **bottom** - AC | top - 12 V DC |

✅ **AND THAT IS WHY THE INVERTED BLOCK WORKS.** Contactor out at the bottom, one short U-turn up
into the block's bottom, out the block's top, one short U-turn across into the breakers' tops, out the
breakers' bottoms to the loads. **Two short U-turns and no long runs** - which was the whole point of
flipping it.

PROCEDURE: **LABEL THE PANEL WHILE THE PARTS ARE STILL LOOSE.** Three orientations across four
devices, and the block's red-to-L1 assignment, which exists nowhere on the hardware. Minutes on the
bench against an afternoon once everything is wired in.

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

SETTLED: **THIS DIN RAIL IS IN THE 12 x 12 x 6 PVC BOX he ordered 2026-11-05** - see the enclosure
section below. "The cabinet" in this file means that box.

NOTE: **Two older descriptions disagree and neither is the design.**
[`breakout-box.md`](breakout-box.md) describes a separate remote box out at the machine holding the
36 V supply and the bucks - **the bucks are gone**, so the only thing that box still claims is the
36 V supply - and the interface board's README puts the 12 V source in the same enclosure as the
board, which the mains-fed MDR replaced. **What survives of the disagreement is one question: where
the 36 V supply goes**, which is the open item immediately below.

## The motor supply is not settled

SETTLED: **THE RAIL IS 36 V - his decision, 2026-10-12.** It is the voltage the TST57 manual
recommends, and it leaves the Mega V's 48 V supply in the Mega V instead of being dug out. The
reasoning is in [`ig57-drives.md`](ig57-drives.md); the short version is that 48 V would have sat at
the manual's lowest stated maximum with about 2 V of regeneration headroom.

SETTLED: **THE SUPPLY IS THE 36 V 600 W ALREADY IN THE MACHINE - nameplate, 2026-10-12.**

| | |
|---|---|
| Make | **Mean Well** - his, 2026-11-09 |
| Input | **220 V at 3.5 A** |
| Output | **36 V DC at 16.5 A**, 600 W |

SETTLED: **NOTHING GOES BETWEEN THE SUPPLY AND THE BOARD - his, 2026-11-09. The supply's own
protection is the protection.** No DC fuse, no breaker on the 36 V side. It is a Mean Well and
it looks after itself.

FLAG: **THE MODEL IS NOT RECORDED, SO THE DATASHEET IS NOT COMMITTED** - and this repo's rule is
that datasheets are committed, not linked. What the over-current protection actually *does* when
it acts - fold back, hiccup, latch off until it is power-cycled - is therefore not written down
anywhere, and it is the thing that decides how the machine behaves on a downstream short. **Read
the label once the box is open and put the model here.**

**So the 600-against-800 W question is answered by nothing moving.** It was a 48 V question, and
choosing 36 V dissolved it: the supply that was already here is the right one, and the Mega V keeps
its 48 V 800 W.

### OPEN: a DIN-rail motor supply - gated on the bench session, nothing bought before it

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

**The other cost is 480 W against the brick's 594 W**, and that is unestablished either way.

🔴 **HIS DECISION, 2026-11-07: NOTHING IS BOUGHT UNTIL THE BENCH SESSION HAS RUN.** The choice is
gated, not undecided, and the gate is
[`../commissioning/bench-session.md`](../commissioning/bench-session.md) - four motors loose on the
bench, read off the supply's own LCD.

**What the reading has to clear, for the XDR to be buyable at all: 13.3 A.** The brick has 16.5 A
and the XDR has 13.3, so the DIN unit is only an option if four drives fit under the lower number
with margin - and that figure exists nowhere, because **the TST57 manual declines to give a
per-drive input current** and says *"users need to carry out specific analysis and estimation"*. The
one instrument that can answer it is already owned and the measurement costs nothing.

NOTE: **IT IS A SEQUENCE, NOT A COIN TOSS - and only one order works.** The bench session **has** to
be run on the brick, because the brick is what exists; so the current figure arrives first either
way, and buying the XDR before it would be committing to the tighter rail with no number in hand. If
the draw turns out close to 13.3 A, the question is closed by the measurement and the brick stays -
no heat argument needed.

**And if the draw is comfortable, the heat is still the half that cannot be reasoned out on paper** -
that one goes to the mock-up in the real box, which is the step that was always going to decide it.

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
| Terminals | **AC in at the BOTTOM, 12 V out at the TOP** - his, 2026-11-06 |

✅ **THAT IS THE OPPOSITE OF A BREAKER AND IT IS DELIBERATE, NOT A QUIRK.** Mains and low voltage sit
at **opposite ends of the body**, which is the length of the unit keeping them apart. The cost is that
the 110 V feed and the 12 V output leave in opposite directions; the benefit is that **no mains
conductor ever has to run alongside the logic wiring** inside this box.

NOTE: **It is the same principle the VFD gets wrong**, where the pump contactor's 230 V coil pair has
to share a terminal strip with the 0-10 V speed reference - see Fig. 3's caution. Here the part does
the separating for you.

NOTE: **3.3 A is sufficient - his call, 2026-11-05: he doubts the whole 12 V side pulls even 2 A.**
The supply reports nothing, so the figure to compare it against comes off the rail when the box is
first powered. Not a gate on anything.

✅ **BEING DIN RAIL NARROWS THE WHAT-IS-IN-THE-BOX QUESTION.** This supply goes on the **bottom rail,
beside the 110 V breaker that feeds it**. What that leaves unplaced is the **VFD** and the **36 V
supply** - both bricks, neither DIN. FLAG: **this paragraph said the 36 V brick was "on that rail
too", which it cannot be** while it is a brick; whether it becomes a DIN part is the open item under
the motor supply section.

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

OPEN: **WHAT IS IN THIS BOX AND WHAT IS OUTSIDE IT - and it is the same question as the 36 V
supply's, gated on the bench session.** His words are *"all the DIN rail components"*, and 12 x 12 is
**144 square inches of back panel**. The DIN gear - two contactors, the 2 x 8 block, the fuse holders
- is small and all of it is in. The **36 V 600 W supply is a brick** and the VFD is another, so
neither is settled by that phrase. **The VFD mounts outside regardless** - it is a brick with a
heatsink in every version of this design. **So what the bench session actually decides is whether the
36 V supply joins the DIN gear inside or sits beside the box with the VFD**, and that is the one word
that makes "the cabinet" in this file mean this box or mean this box plus two parts bolted next to
it.

FLAG: **AND IT IS A HEAT QUESTION, NOT ONLY A SPACE ONE - a dust-proof box has no ventilation.**
Whatever goes in dissipates into a sealed plastic volume that is **energised continuously**, because
the machine lives powered. **The DIN gear is nothing: 1.2 W per contactor, 2.4 W for both.** A 600 W
supply is a different proposition even at a fraction of load, and the VFD has a heatsink for a
reason.

NOTE: **SO VENTING IT IS CHEAP, AND SO IS LEAVING THE COVER OFF.** Both looked like a trade against
dust-proofing until the mounting position was recorded on 2026-11-06. Under the torsion box behind
two walls there are **no chips to keep out**, only general dust - which is a thing to blow out of a
terminal block occasionally, not a thing that kills one.

## What the conductors are, and how they get out of the box

SETTLED: **EVERY RUN LEAVING THE ENCLOSURE IS SHIELDED, 4 OR 2 CONDUCTOR - his, 2026-11-07.** The VFD,
the interface box and the controller, and the two switch boxes. **Inside** the enclosure is a separate
question, below.

| Run | |
|---|---|
| Out to the **VFD** | mains to the drive, and the pump contactor's coil pair |
| Out to the **interface box and controller** | 12 V, and the sense relay's contact back |
| Out to the **two switch boxes** | the coil circuit, in series through the mushroom and then the paddle |

NOTE: **ON THE SWITCH RUN THE SHIELD IS CONTAINING AN AGGRESSOR, NOT PROTECTING A VICTIM.** That run
carries switched mains and nothing quiet, so the shield is there to keep it from radiating into
anything that shares its route - which is the same argument this file makes against the VFD. **It is
the one of the three where a shield is optional**; on the interface box run it is protecting the
12 V and the sense contact, which is the usual way round.

🔴 **EVERY SHIELD IS ANOTHER DRAIN ON THE PE BAR, AND THAT IS THE TERMINAL COUNT BELOW.** The bar was
sized for eight firm conductors with ten bought, and the only shields in the design were the four
motor supply runs - whose drains follow the 36 V supply and may not land here at all. **Three or four
more shielded runs land their drains in this box for certain.** See the open item under the bar:
buying more than ten stops being a precaution and becomes the requirement.

NOTE: **ONE END ONLY, AND IT IS THE PANEL END.** The rule is already in the bar's table and does not
change for these: a shield grounded at both ends is a loop carrying whatever the two grounds differ
by.

OPEN: **THAT RULE IS WRITTEN FOR RUNS LEAVING THE CABINET, AND THE PROBE CABLE IS NOT ONE.** The
probe's 3 conductor run is **shielded** - his, 2026-11-08 - but it goes from the Z plate down the
chains to the **interface board**, not to this panel, so "the panel end" names nothing for it. **One
end only still holds; which end is not decided here.** The probe is also the one input this file says
a false trigger on costs a crash, and it already has **its own regulator and its own return** - so
whichever end takes the drain should be the end that keeps that return alone.

### Inside the box - solid copper

SETTLED: **SOLID, THROUGHOUT - his, 2026-11-07.** It stays dressed where it is put, which is the whole
reason, and nothing here argues against it.

✅ **VIBRATION IS NOT A CONSIDERATION IN THIS BOX, AND THE THREE-POINT MOUNT IS WHY - his,
2026-11-07.** The moving mass is all on the torsion box; **the box lands on three posts and touches
the base nowhere else**, so the lower cabinet is isolated from the gantry and the spindle by the
mount. The usual panel-wiring caution about solid conductor fatiguing at a terminal is about a
cabinet that shakes. **This one does not**, so it does not apply - and that is a property the mount
was built for rather than a lucky side effect. See
[`../machine/three-point-mount.md`](../machine/three-point-mount.md).

NOTE: **If any stranded does go in, it gets ferrules.** Most DIN blocks ask for solid or ferruled
stranded rather than bare stranded, so that is the part of the question with no judgement in it.

### The pigtails come in through two gang boxes let into the back shear wall

SETTLED: **his, 2026-11-08. Each pigtail arrives at its own SINGLE GANG BOX, let into a notch cut
down from the TOP EDGE of the base's back shear wall** - **two notches, 2.5 x 4 inches.** From each
box the cable goes down the inside of the wall and **into the bottom of the DIN enclosure**, with
strain relief at the enclosure's knockout.

FLAG: **THIS REPLACED "a small hole centred high in the wall" the next day.** A gang box per pigtail
is the better job - it gives each cord a proper box to be clamped in rather than a bushing in a
plywood hole - and it is why the entry moved from the field of the panel to its top edge.

✅ **THAT IS THE SHORTEST WAY OUT AND IT IS WHY THE ENCLOSURE SITS WHERE IT DOES.** The box is in the
base's rear middle bay with the back shear wall directly behind it.

✅ **THE WALL TAKES THE TWO NOTCHES WITH ROOM - from the registry's own figures, 2026-11-08.** The
wall is **{{WALL_H}} mm tall**, so a 4 inch notch is about **13% of the height and leaves some 660 mm
of continuous panel below it**. Two at 2.5 inches are about **10% of the {{BACK_WALL_L}} mm length**.
And **nothing from either grid lands on the wall's face between the legs** - the fore-aft rails
terminate inside the three rear legs' slots - so the spans between them are clear to cut.

🔴 **BUT THE WALL IS NOT A SPARE PANEL - IT REPLACES THE BACK CROSS RAILS AT BOTH GRIDS**, so the
back of each grid is the wall rather than a rail - see
[`../machine/assembly.md`](../machine/assembly.md). It carries that through its full height, which is
why notching the top edge does not sever anything. **It is also why the three rules below are not
fussiness.**

PROCEDURE: **CUTTING THE TWO NOTCHES.**

1. **One notch each side of the BACK CENTRE LEG - his, 2026-11-08.** That puts both in the spans
   between the rear legs and **clear of the full-height rebates**, which is where the wall is
   actually screwed through its face - a notch reaching one spends the fixing rather than the
   plywood.
2. 🔴 **ROUND THE TWO BOTTOM CORNERS OF EACH NOTCH.** A square inside corner is where a crack starts,
   and this repo already says so in its own voice about the steel rear plate's probe notch: *"the
   metal wraps around the end of the notch, which is the stress raiser ... and that is where a crack
   would start."* **Drill a hole at each corner first and cut to it.**
3. **Add screws either side of each notch**, closer than the 150 mm rule, so the shear that cannot
   cross the notch goes round it and into the frame.

🔴 **AND NOTHING ON THOSE GANG BOXES MAY FINISH PROUD OF THE WALL'S TOP EDGE.** The back shear wall
stops **{{BASE_BOX_GAP}} mm shy of the torsion box** - see
[`../dimensions/VALUES.md`](../dimensions/VALUES.md) - and that gap **is** the three-point mount. A
box flange, a cover screw, a cable clamp or a cord turning upward out of an open notch is a **fourth
contact point**, and [`../machine/assembly.md`](../machine/assembly.md) names what that looks like:
**nothing, except the Y beams drifting out of coplanar.** **The notch is open at the top, so this one
is easier to get wrong here than it was with a drilled hole.**

NOTE: **The gang box is also what takes the strain now.** A cord grip in a proper box beats a bushing
in plywood: the pull lands on the box and its clamp, the enclosure's own knockout grip never sees it,
and no 220 V cable is bearing on a sawn plywood edge.

#### Which pigtail goes which side of the centre leg

SETTLED: **his, 2026-11-08.**

| | |
|---|---|
| **220 V** | the side **the enclosure is on**, so the cord **drops straight down into the box** |
| **110 V** | the **other side of the back centre leg**, and it **crosses over** to the enclosure |

🔴 **THE TWO SIDES OF THAT LEG ARE TWO DIFFERENT VOLUMES, AND THE CENTRAL WALL IS WHAT SEPARATES
THEM.** The back centre leg carries **the central wall's back end** as well as the back shear wall -
see [`../machine/assembly.md`](../machine/assembly.md) - so the fore-aft wall runs unbroken from that
leg to the front centre leg. **The 110 V run has a second wall in its way, not just a leg.**

SETTLED: **IT CROSSES THROUGH THE CENTRAL WALL, A DRILLED 3/8 INCH HOLE - his, 2026-11-08.** Going
round the front end past the front centre leg was the alternative; over the top was never one, being
the {{BASE_BOX_GAP}} mm mount gap.

✅ **AND 3/8 IN A 36 mm TWO-LAMINATION PANEL DOES NOT REGISTER.** The wall is {{WALL_H}} mm tall and
over a metre long, and a hole this size in the field of it costs nothing worth writing down. **It is
the notches in the back wall's top EDGE that needed rules, not this.**

PROCEDURE: **CHECK WHAT IS ACTUALLY GOING THROUGH IT BEFORE DRILLING, BECAUSE 3/8 IS THE FORK.**
**Three loose 12 AWG conductors go through with room** - bundled in a triangle they are about 7 mm
across in a 9.5 mm hole. **A jacketed 12/3 cable does not**: that is 11 to 13 mm over the sheath and
it will not pass. Drilling it bigger costs nothing now and is a nuisance later.

NOTE: **Chamfer or grommet it, same as the wall entries.** A 110 V conductor bearing on a sawn
plywood edge is the same argument, even at the low tension of a run inside a cabinet.

#### Every penetration in the two walls

SETTLED: **his, 2026-11-08.** Six in all, and they are not all the same size - see the plug rule
below.

| Where | Size | What goes through |
|---|---|---|
| **Back wall, top edge** - two notches | **2.5 x 4 in** | the two **gang boxes**, one each side of the back centre leg |
| **Back wall, field** - under **Y2**, inboard of the corner leg | **1 in** | Y2's **Cat 6, 18/2 and limit sensor** |
| **Back wall, field** - under **Y1**, inboard of the corner leg | **OPEN - off the real bundle** | the **whole Y1 drag chain**, twelve cables and up - see below |
| **Central wall** | **3/8 in** | the **110 V** run, loose conductors |
| **Central wall** - beside it | **1 in** | the **Y2 stepper's three cables**, crossing to the enclosure side |

NOTE: **Four of the six are field holes and cost nothing.** This file's rule is that a shear panel is
governed by **what holds its edges**. **The two notches in the back wall's top edge were the ones
that needed rules**; drilled holes in the middle of a panel do not.

🔴 **THE STEPPER HOLES MUST PASS A CONNECTOR, NOT A CABLE - and that is where 3/8 stops
generalising.** Those runs are **terminated leads that are never cut** - see
[`ig57-drives.md`](ig57-drives.md) - so **a connector has to be threaded through every penetration on
its path.** There is no option to pull a bare cable and terminate it afterwards.

**Three things share each stepper hole, and the biggest one sets its size - his parts, 2026-11-08:**

| What crosses | How big |
|---|---|
| **Limit sensor** - 3 circuit **Mini-Fit Jr** | **almost 3/4 in. THE GOVERNING PART** |
| **Cat 6 patch lead** | **the super-mini plugs** - small, and not the constraint |
| **18/2 motor supply** | **bare wire, no connector at all** |

SETTLED: **ONE INCH FOR THE Y2 HOLE - his, 2026-11-08.** A connector almost 3/4 across will not
thread through a 3/4 hole with a cable behind it and a chamfer eating the edge, so the hole is sized
off the part with room rather than to it.

NOTE: **THERE THE SIZE IS THE LARGEST SINGLE CONNECTOR, NOT THE SUM.** The three are threaded through
one at a time; they only have to **sit** in the hole together afterwards, and three small cables in
an inch is nothing.

🔴 **BUT THE Y1 HOLE IS NOT A STEPPER'S HOLE - IT IS WHERE THE WHOLE Y1 DRAG CHAIN LANDS, AND ONE
INCH DOES NOT SURVIVE IT.** Y1 is the chain everything accumulates in - see the drag chain section
below. **His list, 2026-11-08:**

| Through the Y1 hole | Count |
|---|---|
| **Stepper sets - Y1, Z and X**, each a **Cat 6 plus an 18/2** | **6 cables** |
| **Limit sensors**, Mini-Fit Jr 3 circuit each | **3** |
| **Probe**, 3 conductor, **shielded** - his, 2026-11-08 | **1** |
| **Z plate ground**, 2 conductor - the probe's return | **1** |
| **USB-C** from the **CAN controller on the Z axis** | **1** |
| | **twelve** |

**That is four times what the one inch was sized for.**

✅ **AND THE LIST IS COMPLETE - THE ENCODER PUCKS ADD NOTHING TO IT.** FLAG: **this file asked how
many puck leads came down here, and the answer is none.** The **CAN controller board is on the Z
axis**, so the puck cables travel **up** the X chain to reach it; **the USB-C already in the list
above IS the CAN bus coming back**, and it is the only thing the whole encoder system puts through
this hole. **One link back, not a lead per puck** - see the drag chain section below.

NOTE: **Measuring the bundle rather than tallying it is still the right method**, and it is now a
belt rather than the braces: the hole is sized off cables held as they will lie, so a miscount
cannot reach the drill.

PROCEDURE: **TAKE THE SIZE OFF THE REAL BUNDLE, NOT OFF A PAGE.** Gather the actual cables, **hold
them as they will lie**, measure across the bundle and add room to work. A diameter calculated from
catalogue cable ODs would be exactly the sort of figure this repo keeps out of its own files.

PROCEDURE: **THREAD THEM BIGGEST CONNECTOR FIRST - his order, 2026-11-08:**

1. **The 3 circuit Mini-Fit Jrs** - the **limit sensors and the probe.** They take the most room.
2. **The network connectors** - the Cat 6 patch leads.
3. **The bare wires last** - the 18/2 motor supplies and the Z plate ground, which have no connector
   at all and will go through whatever is left.

🔴 **ORDER IS PART OF THE PROCEDURE, NOT A KNACK.** A Mini-Fit Jr going through a hole that already
has eleven cables in it is the hard one, and finding that out at the end means pulling the lot back
out.

✅ **AND THE ORDER IS WHAT MAKES THE HOLE SIZE RELAXED RATHER THAN CRITICAL - his point.** Sized for
the bundle and loaded biggest-first, the last things through are bare wires that will find a gap.
**The pessimistic diameter is cheap insurance, not a dimension to agonise over.**

✅ **STRENGTH IS NOT THE QUESTION HERE - THREADING IS.** Even a 2 inch hole in the **field** of a
{{WALL_H}} x {{BACK_WALL_L}} panel is structurally nothing; this file's rule is that a shear panel is
governed by what holds its **edges**. **Size it for the bundle and the connectors, and do not trade
that against the plywood.**

FLAG: **I HAD THE RJ45 AS THE GOVERNING PART AND IT IS NOT.** That was the 8P8C standard's figures -
about 11.7 x 8 mm, 14 across the diagonal - applied to parts nobody had looked at. **His Cat 6 plugs
are super-mini and his 18/2 has no connector**, so the one that decides the hole is the limit
sensor's Mini-Fit Jr, which is larger than either. **Parts, not standards.**

🔴 **AND THE TWO BACK-WALL STEPPER HOLES WANT MOVING INBOARD OF THE CORNER LEGS.** The Y steppers sit
at the **min-Y end of both Y tapes** - see [`../machine/assembly.md`](../machine/assembly.md) - which
is the **back**, at the left and right extremes. **That is directly over the two rear CORNER legs**,
and a rear corner leg is where the back wall sits in its **full-height rebate and is screwed through
its face.** Drilling there spends the fixing rather than the plywood. **Bring each hole inboard of
its leg and run the cable across to it.**

## Grounds meet at one PE bus bar

Every ground conductor in the cabinet lands on **one PE bus bar**, and nothing daisy-chains.

| Conductor | Note |
|---|---|
| PE in - 220 V pigtail | the conductor that actually connects this bar to earth |
| PE in - 110 V pigtail | the second one |
| ~~Cabinet chassis~~ | **n/a - the box is PVC.** There is no chassis to bond; see above |
| **Fixed frame** - the steel Y back plate | **Not "the machine frame"** - see below, the machine is in two halves |
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
| 3 | **Fixed frame** - the steel Y back plate |
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
reach this bar is the same question as where the 36 V supply ends up, which is **gated on the bench
session**. **Ten leaves two spare if they land elsewhere and comes up short if all four land here**,
which is the argument for buying more than ten rather than exactly ten.

🔴 **AND SINCE 2026-11-07 IT IS NO LONGER ONLY AN ARGUMENT - every run leaving the box is shielded.**
The VFD run, the interface box run and the switch run each land a drain here, and those are not
gated on anything. **Ten does not cover eight firm conductors plus three or four certain drains**,
let alone the four motor supply drains if they come here too. His ten was right for the design as it
stood; **the shielded-cable decision is what moved it**, and terminals are the cheapest item in the
box.

OPEN: **WHAT THE COUNT SHOULD ACTUALLY BE IS HIS, AND IT IS A BUY, NOT A CALCULATION.** The firm
eight, plus one drain per shielded run out, plus up to four motor supply drains depending on where
the 36 V supply ends up. **Pick a bar with slack and the question never comes back.**

NOTE: **EVERY ENCLOSURE IN THIS BUILD IS PLASTIC - the distribution box, the paddle's gang box and
now the interface board's.** Nothing anywhere is bonded by being mounted in something, so every earth
in the system is a conductor somebody ran on purpose. That is the arrangement working as intended
rather than a problem, and it is worth knowing before anyone goes looking for a chassis to test
against.

NOTE: **ERR UP, BECAUSE A SECOND BAR IS THE AWKWARD FIX.** Running out means either a second bar
bonded to the first, which puts a joint in the one path this whole arrangement exists to keep
single, or re-landing conductors two to a screw. Terminals are the cheapest thing on the rail.

### "Machine frame" is two halves and a spindle

🔴 **THE MACHINE IS NOT ONE PIECE OF METAL, AND THE ONLY PATH BETWEEN ITS HALVES IS THROUGH THE
BEARINGS.** His question, 2026-11-07, and he is right twice over: a bond at the back plate does not
reach the spindle, **and it does not reach the X beam either** - the gantry rides the Y blocks, so
everything above them is on the far side of a rolling-element joint. **Fault current or VFD return
through bearing balls is how a bearing is destroyed.**

| What | Bonded by | Why |
|---|---|---|
| **Fixed frame** - Y beams, extrusion, the steel back plate | **Its own conductor to the bar** | Steel takes a ring terminal properly, it ties both beams and the box fixing, and it is near the enclosure |
| **Spindle** | **Its own earth, back with the motor cable to the VFD's E terminal** | Not to the bar. That conductor is also the return path for the switching noise the drive puts on the motor cable, and the loop wants to be tight |
| **Gantry** - X beam, end plates | **22 AWG stranded in the Y drag chain**, to the fixed frame | Noise only |
| **X carriage, Z plate** | **nothing of their own** - but see the probe return below | They sit between two bonded things, and the spindle's earth lands on a body clamped to the Z plate |

✅ **NEITHER NEW BOND ADDS A TERMINAL TO THE BAR.** The spindle's goes to the VFD and the gantry's
goes to the fixed frame. The count above stays at eight.

NOTE: **THE GANTRY BOND IS FOR NOISE, NOT FOR SAFETY - and saying so changes how much to care.**
Nothing on the moving structure can go to mains: both steppers and every sensor are 36 V or less, and
the one mains item up there is the spindle, which has its own earth. What the bond buys is that a
metre of aluminium extrusion running alongside the spindle's motor cable is not left floating.

✅ **AND THE SHIELDED MOTOR CABLE DOES MORE FOR THAT THAN THE BOND DOES.** Containing the noise at
the source beats giving the gantry somewhere to put what it picked up. **Get the spindle cable's
shield landed at the VFD first**; the gantry bond is then genuinely a belt-and-braces measure rather
than something being relied on.

NOTE: **22 AWG stranded is proportionate and heavier wire would buy almost nothing.** His call, and
the physics agrees: inductance per unit length goes with the **log** of the conductor diameter, so
22 AWG and 14 AWG are within a hair of each other at the frequencies that matter. The only thing that
meaningfully lowers it is **width** - which is what flat braid is for, and it is a geometry effect
rather than a copper-area one.

🔴 **THE TERMINATION IS WHAT FAILS, NOT THE WIRE.** Ring terminal under a bolt into **bare metal** -
**scrape or file the anodising** where it lands on the X beam. A perfect conductor into an anodised
surface is an open circuit, and it is an open circuit that looks exactly like a finished job.

### The touch plate wants the Z plate too, and it is not an earth

SETTLED: **COPY THE MEGA V - his, 2026-11-07.** A **ring terminal on a bolt in the Z plate**, and a
**dedicated wire from there all the way back to the ground on the controller board.** It saves
clipping an alligator lead to the tool every time the touch plate comes out.

| The path | |
|---|---|
| Plate &rarr; tool &rarr; collet &rarr; spindle shaft &rarr; **bearings** &rarr; body &rarr; clamps &rarr; Z plate | through metal - short, and unavoidable on any machine |
| Z plate &rarr; controller board ground | **a dedicated conductor**, the whole way |

✅ **THE LONG RUN IS A WIRE, NOT THE FRAME - which is why it works.** Only the unavoidable bit, tool
to Z plate, goes through structure. FLAG: **this file described it as a structure return and argued
the VFD would break it. Both were wrong.** It lands on the controller's ground rather than on PE,
which is exactly the *"its own return"* the probe design asks for.

✅ **AND THE MEGA V RUNS THE SAME SPINDLE AND THE SAME VFD** - the identical combination from the
same supplier. So this is not an arrangement being tried; it is one being copied off a machine that
has it working with the same drive injecting the same noise into the same spindle.

NOTE: **It adds one conductor to the drag chains**, Z plate back to the cabinet. FLAG: **this said
"alongside the spindle's own earth" for one commit** - the spindle cable does not go in the chain at
all; see the routing below.

### Two drag chains, and Y1 is where everything accumulates

SETTLED: **his, 2026-11-07. There is an X chain and a Y1 chain, and nothing on Y2.** FLAG: **this
listed the X stepper in the X chain for one commit** - it is not. The X stepper is fixed to the
gantry, so it joins at Y1.

**The X chain** - what moves with the X carriage:

| | |
|---|---|
| Z stepper supply | **18/2** |
| Z stepper signals | **Cat 5 patch** |
| Probe | the Z plate return to the controller's ground |
| Z limit sensor | **3-conductor** |
| **Y1 puck** | **Cat 6** - up to the CAN node on the Z axis. His, 2026-11-08 |
| **Y2 puck** | **Cat 6** - along the underside of the X beam, joining Y1's. His, 2026-11-08 |

**Four or five cables, his count** - plus the two encoder leads.

**The Y1 chain** - all of the above comes down the gantry and is joined by:

| | |
|---|---|
| X stepper supply | **18/2** |
| X stepper signals | **Cat 5 patch** |
| X limit sensor | **3-conductor** |
| Gantry bond | X beam to the steel back plate |
| **CAN bus back to the controller** | **one cable, and it is the ONLY thing the encoders put in this chain.** His, 2026-11-08 |

🔴 **THE TWO PUCK LEADS GO UP TO THE Z AXIS, NOT DOWN TO THE CABINET - and that is the whole point of
putting a CAN node on the machine.** The **controller board sits on the Z axis**, so **Y1's and Y2's
puck cables travel the X chain to reach it**, everything else encoder-side is already on the gantry
or the X carriage, and **one CAN bus run goes back to the grblHAL controller.**

✅ **SO THE ENCODER SYSTEM COSTS THE X CHAIN TWO CABLES AND THE Y1 CHAIN ONE**, rather than a lead
per puck all the way to the cabinet. That is the difference between a node on the machine and a fan
of cables off it.

**Y2 carries nothing** - its stepper and limit are static runs, so there is nothing to flex.

✅ **HIS READ: NOT THAT CROWDED.** Eight or nine cables at the worst point, none of them heavy, and
the one genuinely fat run in the build - the spindle's four-core with the water and air - is overhead
in the sleeve and never enters a chain at all.

NOTE: **Cat 5 patch cable is stranded, which is why it belongs in a chain.** It is already what runs
in the Mega V's chains.

### The spindle cable goes overhead, not in the chain

SETTLED: **his, 2026-11-07, and the Mega V already runs it this way.** The spindle's **four-conductor
shielded 16 AWG** cable goes **through a mesh sleeve with the two water lines and an air line,
carried in an overhead sling.** None of it is in the drag chain.

✅ **FOUR CONDUCTORS MEANS THE SPINDLE BODY IS EARTHED PROPERLY** - U, V, W and an earth back to the
VFD, which is what the design asked for. FLAG: **this file opened a question about whether that earth
existed and warned that without it a spindle winding fault would return through the probe's signal
wire into the controller.** It exists. That concern is closed, and with it most of the worry about
the Mega V having no separate frame bond: **the structure is bonded through the clamps to a spindle
body that is itself earthed.**

PROCEDURE: **Confirm the fourth conductor is landed at both ends** - spindle earth terminal and the
VFD's E. It is the obvious assumption and it is a two-minute look, and it is the whole of what the
paragraph above rests on.

✅ **AND THE ROUTING SEPARATES THE NOISIEST CABLE IN THE BUILD FROM EVERY SIGNAL CABLE, FOR FREE.**
The VFD's output goes overhead; the Cat 6 to the steppers, the limit sensors and the probe return go
in the chain. That is the separation an EMC guide would ask for, arrived at because the water and air
lines wanted to go overhead anyway.

NOTE: **IT ALSO WEAKENS THE CASE FOR THE GANTRY BOND, WHICH WAS ARGUED ON THE MOTOR CABLE RUNNING
ALONG THE GANTRY.** It does not. The bond is cheap and still worth having so the extrusion is not
left floating, but it is further down the list than this file first put it.

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
