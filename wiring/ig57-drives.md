# The IG57 drives

**Four all-in-one closed-loop steppers, one per axis.** His, 2026-10-12. The drive is built onto the
motor, so there are no drives in the cabinet and no motor phases on any cable.

## Three names for one part

| Where it appears | Name |
|---|---|
| The drive body | **IG57S series** |
| The manual | **TST57** series |
| The Amazon listing | **CNCTOPBAOS Integrated Nema23 Closed Loop Stepper Motor** |

**The specific model is TST57-76P.** The manual's selection table gives that model a 94 mm body,
2.2 N·m and 680 G·cm², which is what the listing sells. The series runs 41P / 56P / 76P / 100P / 112P
at 1.0 / 1.5 / 2.2 / 2.8 / 3.2 N·m - **all five share the same 5 A drive**, so a torque figure alone
does not identify the part.

NOTE: **Call it the TST57-76P when reading the manual and the IG57 when looking at the machine.**
Three names for one part is how a future session ends up believing there are two.

## The part

From the manual's own tables, with the listing agreeing except where noted:

| | |
|---|---|
| Holding torque | **2.2 N·m** |
| Drive output current | **5 A** (series range 0.2 - 5 A) |
| Phase resistance | **0.6 Ω** |
| Phase inductance | **2.5 mH** |
| Moment of inertia | **680 G·cm²** |
| Body length | **94 mm**, shaft **21 mm** beyond it |
| Shaft | **8 mm**, with a flat |
| Motor face | **56 mm** square, **4 × Ø5 mm** at **47 mm**, **38.1 mm** pilot boss |
| Encoder | **1000 line** |
| Control mode | **pulse + direction** |
| Communication | **TTL over MicroUSB**, 9600 8N1 |

SETTLED: **THE MOTOR WEIGHS 1.1 kg - his scale, 2026-10-12, and THE MANUAL'S WEIGHT COLUMN IS
WRONG.** The listing's 1.1 kg / 2.42 lb is right; the manual's table claims **700 g** for the 76P.

FLAG: **IT IS THE WHOLE COLUMN, NOT ONE ROW.** He also weighed the **1.5 N·m at 724 g** against the
manual's 460 g for the 56P. Two models, both heavy by roughly the same proportion, so this is a
systematic error in that table rather than a typo in one cell. **Do not take any figure from the
manual's weight column**, including for a model nobody has weighed.

NOTE: **A useful cross-check from the parts he already owns.** A spare **HBT5756C at 1.5 N·m weighs
736 g**, within about 1% of the TST57's 724 g at the same torque - two different vendors' NEMA 23
integrated units landing in the same place, which is what makes the manual's 460 g the outlier rather
than his scale.

OPEN: **A spare HBT5776C at 2.0 N·m was given as "1.7" with the unit dropped**, and 1.7 kg against
1.1 kg for a larger torque in the same frame does not sit easily with the other three readings.
Recorded as given rather than converted. It is a Mega V spare and nothing here depends on it.

**Four motors at 1.1 kg is 4.4 kg of the machine**, and the figure feeds the Z carriage weighed at
9 kg in [`../commissioning/masses.md`](../commissioning/masses.md) - which was weighed with its motor
on, so no correction is owed there.

OPEN: **The 94 mm body and 21 mm shaft want checking against the cast stepper frames** before
anything is bolted up - see [`../machine/stepper-sizing.md`](../machine/stepper-sizing.md) for the
frames. Nothing in [`../dimensions/`](../dimensions) currently carries a motor length.

## The supply voltage - SETTLED at 36 V

SETTLED: **THE RAIL IS 36 V - his decision, 2026-10-12.** That is the voltage the manual actually
recommends, and it also means the Mega V's 48 V supply stays where it is rather than being dug out.
Two reasons pointing the same way, one technical and one practical.

**What that buys.** 36 V sits in the middle of every range the manual states rather than at the top
of the lowest one, and it is comfortably clear of the over-voltage alarm above 50 V. Regeneration on
decel of a 58 kg gantry now has roughly 14 V to climb through instead of 2 before anything alarms,
which removes the failure mode entirely rather than managing it.

FLAG: **IT COSTS TOP SPEED, AND THAT IS THE HONEST PRICE - but it may cost nothing reachable.** Corner
speed scales with supply voltage, so a stepper's torque rolls off **earlier** at 36 V than at 48 V.
[`../machine/stepper-sizing.md`](../machine/stepper-sizing.md) is written throughout against a 48 V
rail, including its expectation that the 2.2 N·m beats a 3.2 above about 1200 rpm, and **those
statements now carry an assumption that no longer holds.** OPEN: **Whether the rapid feed rate
actually drops is a measurement, not an argument** - that file's own test is to command increasing
rapids under real load, find the feed rate where the drive alarms, and back off 30%. Its working whip
figure is 1510 rpm, which is a *screw* limit the motor may still clear at 36 V.

The record of why this was a problem at 48 V is kept below, because the next person to find a cheap
48 V supply will want to know why it was not taken.

### The manual's own numbers, which is what settled it

🔴 **AT 48 V THE RAIL WOULD HAVE SAT AT THE MANUAL'S LOWEST STATED MAXIMUM.**

**The manual states the supply range five different ways:**

| Where | What it says |
|---|---|
| §1.1 Product Features | **DC24V ~ DC50V** |
| §3 selection table | **24-48 VDC** |
| §5.1 what to prepare | **a 24~48V DC power supply** |
| §6.1 selecting the voltage | **"allowable maximum operating voltage range is 22VDC~50VDC"**, and **"performs best when powered by a 36V DC voltage"** |
| §7.3 pin definitions, V+ | **DC24V~48V** |

**And §6.1 is explicit about what happens at the top:** *"When the driver is powered by a regulated
power supply and the supply voltage is close to 50VDC, it is recommended to take voltage clamping
measures at the power input end to avoid the driver from overvoltage alarm and stopping working due
to the supply voltage being higher than 50VDC."* For an unregulated supply it says the **no-load**
output must not exceed 50 V.

**Separating the observation from what it means**, because this repo's rules are explicit about it:

- **Observed:** the over-voltage alarm is above **50 V**. The recommended voltage is **36 V**. The
  lowest stated maximum is **48 V**. The manual contradicts itself on the range but **not** on the
  alarm or the recommendation.
- **Therefore:** a 48 V rail is at the top of the lowest stated range, with about **2 V** to the
  alarm. Regeneration on decel of a 58 kg gantry has to fit in that 2 V, and the drive's response to
  exceeding it is to **alarm and stop working** - mid-job.
- **What does NOT transfer:** the Mega V has run 48 V for a long time with no over-voltage fault, but
  that is a **different drive** rated 24-55 V. Its clean history is evidence about the HBT57C, not
  about this part.

SETTLED: **So 36 V, and the 48 V option is closed.** It was never a comfortable 2 V - it was 2 V
against a drive whose response to exceeding it is to stop mid-cut, on a manual that cannot state its
own range consistently. **Do not reopen this for a 48 V supply that happens to be available**, which
is the form the temptation will take.

SETTLED: **The supply is the 36 V 600 W already in the machine - 16.5 A out, 220 V at 3.5 A in,
nameplate 2026-10-12.** So the 600-against-800 W question closed by nothing moving, and the current
budget went **up** from the 12.5 A the repo had worked to. FLAG: **its output is VARIABLE**, which
makes 36 V a setting to verify with a meter rather than a property to trust - see
[`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md).

## Inputs and outputs - what the manual settles

### The inputs take 3.3 V directly

SETTLED: **PUL, DIR and EN are optically isolated, DIFFERENTIAL, and a high level can be
3.3 - 24 VDC applied directly.** The manual says so in §1.1, §7.2 and the §7.3 pin table.

FLAG: **THAT REMOVES THE LEVEL-SHIFTING PROBLEM THE PREVIOUS DRIVES CREATED.** The Mega V's drives
wanted a 24 V pull-up that would destroy a Teensy pin, and this folder carries several warnings about
it. **A 3.3 V controller output drives these inputs with nothing in between** - no divider, no
pull-up, nothing to get the ratio wrong on.

| Input | Minimum pulse width | Maximum frequency |
|---|---|---|
| **PUL** | 2 µs | **300 kHz** |
| **DIR** | 2 µs | 300 kHz |
| **EN** | **100 µs** | **10 kHz** |

NOTE: **EN is a far slower input than the other two and that is by design.** 100 µs minimum against
2 µs. It is not a signal to pulse quickly at.

### The alarm output fails the RIGHT way

SETTLED: **ALM is normally closed by default and outputs when normal** - the manual's §7.3, which
also says it can be inverted in software or assigned another function. It is an **open collector**,
**30 V maximum**, **50 mA maximum** sink or source.

🔴 **THIS REVERSES WHAT THIS FOLDER HAS BEEN SAYING, AND IT IS GOOD NEWS.** The Mega V's alarm
asserted on fault, which meant an unpowered drive or a broken wire read as healthy - the failure
[`breakout-box.md`](breakout-box.md) calls failing silent. **Asserting when healthy inverts that: no
power, broken wire, or pulled connector all look like an alarm.** That is fail-safe in the direction
a guard needs, by default, with no extra input required.

OPEN: **Confirm the sense on the bench before relying on it** - the procedure is
[`../commissioning/bench-session.md`](../commissioning/bench-session.md) - because this is a machine-translated
manual and "normally closed, output when normal" is doing a lot of work in one sentence. The check is
one meter reading: power a drive with nothing wrong and see whether the output is asserted.

FLAG: **IT IS AN OPEN COLLECTOR, SO IT STILL NEEDS A PULL-UP - and now the pull-up can be 3.3 V.**
With a 30 V withstand and 50 mA capability, pulling up to the controller's own 3.3 V rail is well
within it and keeps everything on one logic level. **Do not pull it to 24 V.**

### The fifth pair is EX, in-place

The connector diagram labels pins 11 and 12 **EX+ / EX-**, *"positive signal in place"* and
*"negative signal in place"* - an in-position output.

OPEN: **The manual does not define EX anywhere.** §1.1 describes only *"1 group of independent
digital output"*, and the §7.3 pin table stops at ALM-. So the diagram shows a tenth and eleventh
signal that the text does not explain, and whether EX is a second independent output or a reassignment
of the same one is **not established**. Not used today, and worth knowing before anything is designed
around it.

## Connector pinout

From the manual's §7.3 and the connector diagram. **Two separate terminal blocks** - a 2P for power
and a small-gauge block for signals:

| Pin | Name | |
|---|---|---|
| 1 | **V+** | supply positive |
| 2 | **V-** | supply negative |
| 3 | **PU+** | pulse |
| 4 | **PU-** | |
| 5 | **DR+** | direction |
| 6 | **DR-** | |
| 7 | **EN+** | enable |
| 8 | **EN-** | |
| 9 | **AL+** | alarm out |
| 10 | **AL-** | |
| 11 | **EX+** | in place - undefined in the text, unused |
| 12 | **EX-** | |

## The cabling

**One Cat 6 patch cable per stepper**, plus **18/2 shielded** carrying the supply. His scheme,
2026-10-12. Each signal travels as a plus/minus pair in its own twist, **plus on the striped
conductor, minus on the solid**.

**The cable is plug-to-plug and never cut**: an RJ45 at the interface board, and an **RJ45 breakout
board at the drive** - his, 2026-11-07. **The wiring list that gets built from is the breakout table
below**, not the colour table; colour only matters if a cable ever gets cut.

🔴 **THE ORDER COMES FROM THE INTERFACE BOARD, WHICH IS ORDERED AND THEREFORE DEFINES IT - his,
2026-11-07.** Read the RJ45 pin numbers off the board's netlist, not off this signal's position in
the drive's terminal block:

| T568 pair | Striped - **odd** pin | Solid - **even** pin | At the drive |
|---|---|---|---|
| **1-2** | pin 1, **PU+** | pin 2, **PU-** | terminals 3, 4 |
| **3-6** | pin 3, **EN+** | pin **6**, **EN-** | terminals 7, 8 |
| **4-5** | pin 5, **DR+** | pin **4**, **DR-** | terminals 5, 6 |
| **7-8** | pin 7, **AL+** | pin 8, **AL-** | terminals 9, 10 |

✅ **PLUS-ON-STRIPED AND THE BOARD'S ODD-PIN SIGNALS ARE THE SAME RULE, which is why the two ends
agree without anybody arranging it.** In **both** T568A and T568B every **odd** pin is a striped
conductor and every **even** pin is a solid one - the two standards swap the colours and leave that
property alone. So the cable standard does not matter here, and neither does the colour: **strip the
jacket and the striped conductor of each twist is the plus leg.**

🔴 **THE RULE IS: KEEP EACH PAIR TOGETHER AND NEVER BREAK ONE. One colour pair carries one signal and
its own ground, and a standard cable does that by itself.** Because the board puts signals on odd
pins and grounds on even pins, and every odd pin's twist partner is an even pin, **each pair of a
stock T568 cable already arrives as a signal and its own return**:

| Pair, T568B | Board pins | Which are |
|---|---|---|
| **orange** | 1, 2 | Step and its GND |
| **green** | 3, 6 | Enable and its GND |
| **blue** | 5, 4 | Dir and its GND |
| **brown** | 7, 8 | Alarm and its GND |

✅ **SO THE PIN NUMBERS ARE AN EXPLANATION, NOT AN INSTRUCTION.** Work in pairs and colours and the
split-pair fault cannot happen. It only arises from **assigning minus legs by pin arithmetic** -
putting EN on 3 and 4 and DR on 5 and 6, because the numbers look adjacent. In T568 pins 3 and 6 are
one twist and 4 and 5 are the other; **pin 3 is not twisted with pin 4.** Do that and both signals
leave their own twist and land in each other's, which is the mechanism the next section says this
whole scheme rests on.

NOTE: **DIR IS THE ONE THAT GETS BUILT BACKWARDS.** It is the only pair whose **solid** conductor is
the **lower** pin number - DR+ on pin 5, DR- on pin 4. Every other pair runs low-to-high.

NOTE: **THE BOARD DOES NOT CARE WHICH EVEN PIN A MINUS LEG USES, AND THAT IS WHY THIS MUST BE
WRITTEN DOWN.** All four even pins are **GND** on the board - see
[`kicad/interface-board/README.md`](kicad/interface-board/README.md) - so a split pair raises no
error anywhere, passes continuity, and works. It costs signal integrity and nothing else, which is
the kind of fault that gets found by chasing a step loss months later.

### The drive end is an RJ45 breakout board, so the cable is never cut

SETTLED: **his, 2026-11-07. At each drive there is a small RJ45-to-screw-terminal breakout board** -
a jack and an 8-position screw block on one little PCB. So **the cable is plug-to-plug stock patch,
terminated by whoever made it**, and eight short wires go from the breakout's terminals to the
drive's own block.

🔴 **SO COLOUR NEVER APPEARS ANYWHERE, AND THE PIN NUMBERS ARE THE ONLY IDENTIFIER AT BOTH ENDS.**
Nothing is stripped, so no conductor is ever picked out by its stripe. The colour table below is
reference for a cut-end job and **is not the build instruction**; this is:

| **RJ45 pin** | Drive terminal | Signal |
|---|---|---|
| **1** | **3** | **PU+** |
| **2** | **4** | **PU-** |
| **3** | **7** | **EN+** |
| **4** | **6** | **DR-** |
| **5** | **5** | **DR+** |
| **6** | **8** | **EN-** |
| **7** | **9** | **AL+** |
| **8** | **10** | **AL-** |

🔴 **THE LEFT COLUMN IS THE RJ45 PIN, NOT THE BREAKOUT STRIP'S OWN TERMINAL NUMBER - and on this
board those run OPPOSITE ways.** The strip's terminal 1 is **jack pin 8**; see the section below.
**Mark each board with the jack pin numbers and work from those**, and the strip's own numbering
never enters the job.

**All four pairs stay inside their own twist**, which is the only thing that had to come out right.

🔴 **IT IS NOT A STRAIGHT 1-THROUGH-8 MARCH AND NO CABLE CONVENTION CAN MAKE IT ONE.** That is the
geometry of the jack, not a mistake in anything: **the drive's block runs its pairs on ADJACENT
terminals** - 3-4 PU, 5-6 DR, 7-8 EN, 9-10 AL - while **the RJ45's twists are 1-2, 3-6, 4-5, 7-8.**
Those two patterns cannot both be sequential at the same time.

NOTE: **A SEQUENTIAL HAND-CRIMPED CABLE DOES NOT HELP HERE - it was worked out both ways, 2026-11-07.**
Eight wires either way, all four pairs intact either way; the two schemes differ by **two wire
numbers** (6-to-8 and 4-to-6 with a standard cable, against 4-to-8 and 6-to-6 with a sequential
one). The labour is identical, so a non-standard cable buys nothing - see the crimping section below.

✅ **AND THE BREAKOUT BOARD IS WHAT MAKES THAT A GOOD TRADE.** The eight wires are a **one-time bench
job per drive**, done with the drive loose and then **labelled**. After that **every cable in the
system is an interchangeable stock patch lead** that can be replaced from any shelf. The oddity is
confined to a thing built once; the cables stay fungible.

PROCEDURE: **LABEL EACH BREAKOUT BOARD.** Nothing about that table is self-evident from either end,
and the next person to look - including him, later - will see eight wires in no obvious order.

#### Which terminal is pin 1 - his question, 2026-11-07, and the boards do not say

🔴 **THE BREAKOUT BOARDS CARRY NO PIN NUMBERS**, so the table above cannot be used until the terminal
order is established on the real part.

**The convention, anchored to what can be seen rather than to "left":** look into the jack opening
face on. **With the CONTACTS at the TOP of the opening and the LATCH SLOT at the BOTTOM, pin 1 is on
the left** and 8 is on the right. That is the normal mounting, and it is the answer he had.

FLAG: **"LEFT" ON ITS OWN IS NOT SAFE, BECAUSE IT MIRRORS.** Mounted the other way up - contacts at
the bottom of the opening - the same jack reads **1 on the right**. A board can be laid out either
way and nothing about a bare PCB says which. **The contacts-up landmark is the part that carries the
answer; left and right do not survive on their own.**

🔴 **AND A MIRRORED READING IS THE WORST SINGLE MISTAKE AVAILABLE HERE, BECAUSE IT SWAPS 1 WITH 8.**
Pin 1 is **Step** and pin 8 is **AL-**. Read backwards, the controller's step output lands on the
drive's **alarm output** and the drive's alarm lands on **PU+**. That is two outputs driving each
other, which is the one wiring fault on this cable that can do damage rather than just fail. **Do not
find this out by powering it up.**

#### The square pads are the pin 1 markers, and they are at OPPOSITE ends

**His, 2026-11-07, off the product listing's render.** FLAG: **A LISTING RENDER IS A CLAIM, NOT A
MEASUREMENT** - this is written down as the expectation the meter is checking against, not as the
answer.

| On the board | |
|---|---|
| **Top row, eight pads at 2.54 mm** | the **screw terminal strip**, with a **square** pad at one end |
| **Double row below, 4 and 4 staggered** | the **RJ45 jack** footprint, with a **square** pad at the opposite end of the board |
| Board | 24.49 x 33.00 mm, mounting holes on 20.00 mm |

FLAG: **DO NOT TAKE A LEFT OR A RIGHT FROM THIS TABLE.** It describes the **render**, and whether the
render matches the board in hand was itself in question - his row-offset check says the picture is
mirrored against the real part. **What survives is that the two square pads are at opposite ends of
the board**, which is true in any view. The sides do not survive, and the meter below is what
replaced them.

SETTLED: **THE METER HAS BEEN ON IT - his, 2026-11-07.** With a cable in the jack, **the terminal
that tones out to the white/orange conductor is jack pin 1.** That is the measurement, and it
outranks the render and the left-right convention both.

NOTE: **The render was read three different ways before the meter and the mechanical reason agreed.**
Not worth re-tracing: **the picture could not settle it and two minutes with a probe could.**

SETTLED: **JACK PIN 1 IS THE TERMINAL AT THE FAR END FROM THE STRIP'S SQUARE PAD - his, 2026-11-07.**
So **the strip's terminal 1 is jack pin 8**, and the strip runs 1-to-8 against the jack's 8-to-1.

🔴 **AND THE REASON IS MECHANICAL, WHICH IS WHAT MAKES IT WORTH KNOWING - his.** The two connectors
**face opposite directions** on the board: wires enter the strip from one edge, the plug enters the
jack from the other. **Each connector numbers its own pins from its own face**, so looked at from
above, one counts left to right and the other counts right to left. **The board is a straight
parallel fan-out with no crossing traces at all** - the reversal is the two connectors being turned
around, not the routing.

FLAG: **I ARGUED THE OPPOSITE FROM THE RENDER AND IT WAS WRONG.** The long sweeping traces were read
as a 1:1 map having to cross the board. They are not crossings - they are eight parallel runs routed
around the jack footprint and the mounting holes. **His first reading of the picture, terminal 1 to
jack pin 8, was right**, and the two rounds of doubt after it came from me, not from him.

✅ **SO THIS IS THE RULE FOR THE WHOLE CLASS OF PART, not a quirk of one board.** On any breakout
whose two connectors **face opposite ways**, the honest expectation is that **the numbering reverses
end to end** - the simplest possible layout produces it. A board that did NOT reverse would be the
one needing crossing traces.

NOTE: **ONE PROBE CONFIRMS IT BEYOND ARGUMENT, if it is ever doubted again: brown should land on the
square pad.** Brown is jack pin 8 on a T568B cable, and the square pad is the strip's terminal 1.

PROCEDURE: **METER IT, ONCE, PER BOARD TYPE - and it is about two minutes.**

1. **Cut one end off a sacrificial patch cable.** Any spare lead. The intact plug goes into the
   breakout's jack; the cut end gives eight conductors that can be told apart by colour.
2. **Read pin 1 off the intact plug by eye** - contacts toward you, latch away from you, cable
   hanging down, **pin 1 on the left**. On that plug the conductor at pin 1 is **white/orange** for
   a T568B cable and **white/green** for a T568A one, which also settles which standard it is.
3. **Buzz that conductor against each screw terminal in turn.** The terminal that beeps is **pin 1**.
   **Start at the square pad**, because it is the one position on the board that is marked, and
   whether it answers to pin 1 or to pin 8 is the open question above.
4. **Do the remaining seven**, so the whole map is read rather than inferred from pin 1 and an
   assumed direction.
5. **Write the RJ45 PIN numbers on the board** - paint pen, label, scratch. Then the table above is
   usable and this never has to be done again.

🔴 **MARK IT IN JACK PIN NUMBERS, NOT IN THE STRIP'S OWN TERMINAL NUMBERS - and that is the whole
lesson of this part.** The strip's numbering is a **vendor label**; the wiring list speaks **jack
pins**; and carrying both means translating between them every time. **Every mirror that came up
while establishing this board came from the strip's numbering**, not from the jack's.

✅ **THE SQUARE PAD IS THE ONLY LANDMARK THAT SURVIVES.** Left and right flipped twice here - once
between the listing render and the real part, once between viewing the board from the top and from
the bottom. **A feature etched on the board cannot flip; a direction can.** So state the finding
against the square pad - *"jack pin 1 is the terminal at the square pad"*, or *"at the far end from
it"* - and never against a side.

NOTE: **His row-offset check is the right way to tell which side a render is showing**, 2026-11-07:
the RJ45's two ranks are staggered, so the direction of the offset says whether you are looking at
the component side or through the board. **It stopped mattering the moment the part was in hand with
a meter on it** - which is this file's standing order anyway.

✅ **STEP 4 IS NOT BUSYWORK - it is what catches the mirror.** Finding pin 1 and counting along
assumes the direction, which is exactly the thing in doubt. Eight readings cost another minute and
leave nothing assumed.

NOTE: **THE METER OUTRANKS THE CONVENTION ABOVE, AND THIS FILE HAS BEEN HERE BEFORE.** The seller's
word that the drives' minus legs were commoned was written in as fact and his meter overturned it in
under a minute - see the section below. The same applies to a left-and-right convention read off a
board nobody has in front of them.

### The same map by conductor colour - reference only, for a cut end

🔴 **THE BOARD HAS NO COLOUR CONVENTION, AND IS NEITHER T568A NOR T568B.** Its netlist assigns nets
to **RJ45 contact numbers** and nothing else - a PCB jack has eight contacts and no wires in it.
**T568A and T568B are conventions for which conductor colour sits on which pin inside a cable**, so
they live entirely in the patch cable. The colours below are a property of the cable plugged in.

✅ **AND THE BOARD CANNOT BE WRONG ABOUT IT, WHICHEVER CABLE TURNS UP.** The pin-to-twist assignment
is **1-2, 3-6, 4-5, 7-8 in both standards** - A and B swap colours and leave the pairings alone - so
signals on odd pins with grounds on even pins is correct on the twists either way, because every odd
pin's twist partner is an even pin. **The standard is a cable question, not a board question.**

NOTE: **With the breakout board in the design, this table is for a cable that gets cut** - a
replacement made up in a hurry, or a drive wired without its breakout. **The wiring list above is the
one to work from.**

| Twist | Signal | Plus leg - pin, colour | Minus leg - pin, colour |
|---|---|---|---|
| **orange** | **PU**, pulse | pin 1, **white/orange** | pin 2, **orange** |
| **green** | **EN**, enable | pin 3, **white/green** | pin 6, **green** |
| **blue** | **DR**, direction | pin 5, **white/blue** | pin 4, **blue** |
| **brown** | **AL**, alarm | pin 7, **white/brown** | pin 8, **brown** |

**That is a T568B cable.** The striped conductor of each twist is the plus leg, which is the rule
already stated above - and that part holds under both standards, because every odd pin is a striped
conductor in A as well as B.

🔴 **T568A SWAPS ORANGE AND GREEN, AND NOTHING ELSE.** If the patch cables turn out to be A rather
than B, **PU becomes the green pair and EN becomes the orange one**; blue and brown are **identical in
both standards**. So:

| | |
|---|---|
| **DR is the blue pair** | always, either standard |
| **AL is the brown pair** | always, either standard |
| **PU and EN** | **depend on which standard the cable is.** PU is whichever of orange/green lands on pins 1 and 2 |

PROCEDURE: **CONFIRM THE STANDARD ONCE, OFF THE PLUG THAT IS STILL ON THE CABLE, AND DO NOT GUESS
FROM THE COUNTRY.** Look into the intact plug with the **contacts toward you and the latch behind**:
read the eight colours across and find which end has **white/orange** first. **White/orange at pin 1
is B; white/green at pin 1 is A.** Orienting it that way needs no left-or-right convention to be
remembered correctly - the colour sequence tells you which end you are looking at.

NOTE: **A patch cable is straight through, so A or B changes nothing electrically** - pin 1 reaches
pin 1 either way. It only changes **which colour** you pick up at the cut end, which is the whole of
why this matters here.

### The cable itself - flat 30 AWG stranded

**His, 2026-11-08: Monoprice Cat 6 FLEXboot, flat, 30 AWG stranded bare copper, 550 MHz, UTP.**

| | |
|---|---|
| **30 AWG stranded** | fine here, and the gauge is not the question. These drive inputs are **optos at a few milliamps** - a chain-length run is a few ohms and a drop measured in tens of millivolts |
| **Stranded** | the property that matters for a chain, and this file already says so |
| **Flat** | **helps, if it bends across its width.** Bending strain goes as conductor radius over bend radius, so 30 AWG sees **less** strain than a thicker lead |
| **Thin snagless boot** | small through a 1 inch hole, and it is **where slim cable actually fails** |

🔴 **ANCHOR THE CABLE TO THE CHAIN NEAR EACH END, AND NEVER LET THE CHAIN TWIST IT.** A flat cable
forced to twist fails where a round one shrugs, and a thin boot has very little strain relief in it -
so the chain's motion must be taken by the chain, not by the plug.

NOTE: **MONOPRICE SAY THE PAIRS ARE TWISTED, AND THAT IS A CLAIM, NOT A MEASUREMENT.** Asked directly
whether the conductors are twisted or parallel, their answer was *"The pairs are twisted, as expected
in a Cat6 Unshielded Twisted Pair (UTP) cable."* **That reasons from the product's name rather than
reporting the part** - and 550 MHz does need controlled pair geometry, so it is probably right.

🔴 **BUT THIS FILE HAS BEEN HERE BEFORE AND THE RULE CAME OUT OF IT: A VENDOR'S WORD GOES IN AS A
CLAIM.** The seller said the drives' minus legs were commoned inside; it was written down as a claim
**specifically so it would get checked**, and his meter overturned it in under a minute - see the
section below. PROCEDURE: **Strip 50 mm of jacket off one end when it arrives and look.** Twisted, or
laid parallel. Then this note becomes an observation and says whose.

✅ **AND IT IS NOT A PEDANTIC CHECK - IT IS THE SCHEME'S OWN FOUNDATION.** Everything this file argues
about the Cat 6 run rests on the return being **forced into the other half of its own twist**. If
these are parallel conductors in a flat jacket, that mechanism is not there, and the board's own
reason for putting **Step and Alarm on opposite edges of the jack** - Step the aggressor, Alarm
feeding EStop - stops being enough.

OPEN: **THE LISTING HE READ IS THE 5 FOOT.** The X chain run reaches the Z carriage and the Y1 run
reaches the cabinet, both with chain travel on top. **Work out the length per run before ordering** -
and remember these are stock patch leads precisely so a replacement is a shelf item.

### If the cables get crimped rather than bought

**His question, 2026-11-07: lay the colours out 1 through 8 in order, so each pair lands on adjacent
pins.** It would work - pairs on 1-2, 3-4, 5-6, 7-8 against signals on odds and grounds on evens puts
every signal in its own twist, same as T568 does.

🔴 **BUT IT SAVES NO WORK, WHICH IS THE ANSWER BEFORE ANY OF THE REST.** With the breakout board at
the drive it comes to **eight wires either way and all four pairs intact either way** - the two
schemes differ by two wire numbers. The simplicity a sequential cable looks like it buys is spent
again at the breakout, because the drive's block and the RJ45's twists cannot both be sequential.

🔴 **AND CRIMP THEM T568B, NOT SEQUENTIAL - this reason is not electrical either.** A sequential cable is
**not a T568 cable and therefore not an Ethernet patch cable**, while being indistinguishable from
one. Two hazards, both of them later rather than now:

| | |
|---|---|
| **It is a lookalike** | Anyone who grabs it for a network run gets a cable that splits Ethernet's own pairs. In a shop with network cable about, that is a trap left lying around |
| **Mixing is worse than either** | Buy cables for some axes and crimp sequential for others and there are **two incompatible types that look identical.** Nothing on the board or the drive would flag a swap |

✅ **AND T568B KEEPS THE REPLACEMENT A SHELF ITEM.** A standard cable can be bought at any time and
works with no thought; a sequential one has to be remade and understood first.

NOTE: **WHERE CRIMPING DOES EARN ITS PLACE IS LENGTH.** A made-to-length cable in a drag chain beats a
coiled-up 2 m patch lead - see the drag chain section in
[`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md). That is a reason to crimp; it is
not a reason to abandon the colour standard while doing it.

FLAG: **THIS TABLE READ PU / DR / EN / AL IN PAIR ORDER UNTIL 2026-11-07**, which put **DR and EN the
wrong way round** against the board, and it gave pair numbers rather than pin numbers so it could not
have caught a split pair either. Do not reinstate that order.

NOTE: **THE SOLID CONDUCTOR IS THE SIGNAL'S MINUS LEG, NOT A GROUND.** The manual calls these inputs
differential, which is what that means: each pair is the two ends of an opto LED. Calling the minus
leg a ground invites someone to tie the four together as a convenience.

### SETTLED: The minus legs are independent - measured, and the seller was wrong

**No continuity between any of the minus signals.** His meter, on the part, 2026-10-12.

🔴 **THE SELLER SAID THEY WERE COMMONED INSIDE THE DRIVE, AND THEY ARE NOT.** That answer was written
into this file as *a claim rather than a checked fact*, specifically so it would get checked. Checking it
took under a minute and overturned it. The manual never stated it either way. **This is the reason a
vendor's word does not go in as a fact** - the same vendor class answered the Mega V's enable-reset
question both ways in a single message.

**So the isolation is per signal, not per drive.** Each of PUL, DIR and EN is its own opto LED with
its own anode and cathode, isolated from the others; AL is a separate isolated output whose minus leg
is tied to none of them.

FLAG: **THAT MAKES THE CAT 6 SCHEME EXACTLY RIGHT, AND NOT BY LUCK.** Current entering PU+ has
**nowhere to leave except PU-** - there is no internal path to any other terminal - so each signal's
return is *forced* into the other half of its own twisted pair. That is the entire mechanism by which
a twisted pair rejects anything. A commoned drive would have let return current redistribute across
the four solid conductors; an independent one cannot. 300 kHz with a 2 µs minimum pulse width in a
drag chain is exactly the case where that matters.

**Commoning the four minus legs at the CONTROLLER end does not break it**, because the separation
that matters is at the drive end where there is no alternative path. That makes it a question of the
cabinet's convenience rather than of signal integrity - see
[`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md).

**18/2 is heavier than the manual asks for.** §7.1 recommends **AWG 20-24** for the supply
connection; 18 AWG exceeds that, which is the right direction to err.

FLAG: **IT IS STILL NOT THE SIX-WIRE SHELL [`breakout-box.md`](breakout-box.md) DESCRIBES**, and the
supply no longer shares a shell with the signals.

## Fit an external 5 A fast-blow fuse per drive

PROCEDURE: **§7.1 says the drive has an internal fuse in series with V+ that the user cannot
replace, and recommends an external 5 A fast-blow fuse in series with the positive supply so there
is a fuse that *can* be replaced.** Four drives, four fuses, fitted in the cabinet.

FLAG: **THERE IS NO REVERSE-POLARITY PROTECTION.** The listing is blunt: reversing the supply damages
the internal circuit. Four identical 2P connectors assembled by hand - **check polarity per drive
before the first power-on**, not after.

## Diagnosis - there is no fault code table

🔴 **THE MANUAL PROMISES ONE AND DOES NOT CONTAIN IT.** Its table of contents lists **"11. Error
Codes"**. The document ends at section 10, which says only:

> *"TST57 uses a dual-colour patch LED (red/green) to display the status. The normal status is that
> the green LED flashes. If the red LED flashes, it indicates an alarm or an error has occurred."*

So **red flashing means something is wrong, and nothing distinguishes what.** The Mega V's drives
could be diagnosed by counting flashes; this one cannot, on the documentation available.

OPEN: **Ask the vendor for the missing section 11.** It is a named, numbered section of their own
manual, which is a far easier thing to ask for than an explanation - and the alternative is diagnosing
a stopped machine from one red LED. **Asked 2026-10-12; a real response is still outstanding.**

### REJECTED: The flash codes an AI assistant produced for this question

🔴 **DO NOT USE THESE, AND DO NOT RE-ASK AND BELIEVE THE ANSWER.** Asked for the missing section 11
on 2026-10-12, Amazon's assistant returned a flash-code table. It is recorded here **so that the next
person to ask the same question recognises the same answer and does not adopt it**, which is the only
reason it is in the repo at all.

**It disclaims itself.** Its own words: *"similar"* motors, *"comparable"* controllers, *"typical"*,
*"most"*, and - decisively - *"I can't retrieve the complete Section 11 from your specific motor's
manual."* It is a generic pattern, not this drive.

**And it is not merely unsourced, it is contradicted by the one real table in this repo.** The
HBT57C's codes were read off that drive's own manual, and the two disagree on every row they share:

| Flashes | HBT57C, from its manual | The AI's generic table |
|---|---|---|
| 1 | **Over-current** | Overvoltage |
| 2 | **Over-voltage** | Overcurrent |
| 4 | — | Tracking error |
| 7 | **Tracking error** | — |

**So "most integrated closed-loop motors" demonstrably excludes the one family this build has real
data for.** The first two rows are transposed and the tracking-error code moves from 7 to 4. If it
were adopted, the most likely fault on this machine - tracking error, the only one the Mega V has
ever thrown - would be read as a phase connection failure, and a genuine over-current would be read
as over-voltage and chased toward regeneration and a brake resistor.

FLAG: **THE DANGER IS THAT IT IS SHAPED EXACTLY LIKE THE MISSING SECTION.** It is a plausible table
of the right form, arriving in answer to the right question, at the moment the real one is known to
be absent. That is the shape of thing this repo's rules are about: a signal is not the event, and an
answer is not a source.

**The only real flash-code information this build will have until the vendor replies is what the LED
is observed to do** - which is why
[`../commissioning/bench-session.md`](../commissioning/bench-session.md) records it while provoking a
tracking fault on an uncoupled motor.

## Configuration - and a contradiction about whether it is even allowed

The manual's §5.1 says to prepare **a PC running Windows and a matching MicroUSB cable**, and §9 gives
the TTL parameters: **9600 baud, 8 data bits, 1 stop bit, no parity**. That reads as a user-facing
configuration path.

🔴 **THE LISTING SAYS THE OPPOSITE.** Its own photograph of the MicroUSB port is captioned
*"For internal factory use only (firmware programming during the manufacturing process) and not for
end-user configuration."*

OPEN: **Which is true decides whether anything in this drive is adjustable at all** - including
whatever threshold governs how readily the closed loop faults, and whether the alarm output can
actually be inverted or reassigned as §7.3 claims. The manual describes a host-computer workflow;
the seller says the port is not for users. **Settle it before assuming either.**

### DIP switches

Everything else is set on the body. SW1-4 select microstep from the manual's table; the listing adds
SW5 and SW6, which the manual covers only partly.

| Switch | Function |
|---|---|
| **SW1-4** | Microstep - 400, 800, 1600, 3200, 6400, 12800, 25600, 51200, 1000, 2000, 4000, 5000, 8000, 10000, 20000, 40000 |
| **SW5** | Direction. **OFF = CCW, ON = CW** |
| **SW6** | Current. **OFF = large, ON = low** - from the listing image; the manual does not mention SW6 |

NOTE: **All four ON is 400 steps/rev, and the table is not in a sensible order** - it runs 400 up to
51200 and then restarts at 1000. Read the row, do not infer the pattern.

## What the closed loop does and does not cover

The drive has its own **1000-line encoder** and corrects its own position, so **lost steps at the
motor are the drive's problem and are already handled** - one of the reasons the linear-encoder
project narrowed its justification away from motor-side step loss. See
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md).

What a shaft encoder cannot see is anything **downstream of the shaft** - a coupling slipping, a grub
screw backing out, backlash - and it cannot see **Y1 against Y2**, because the drives have no
knowledge of each other. Those are the linear scales' job.

## grblHAL can take a motor fault input, and does not use it per axis

grblHAL has **$744** and **$745** and raises **Alarm 17, motor fault**. The core defines *per-axis*
fault inputs, but the Teensy driver implements only a **single combined** motor-fault pin across every
board map - so four separate AL conductors are ahead of the firmware and would be wire-ORed into one
input today.

Keeping them separate in the cabling is still right: nearly free during a build, expensive to
retrofit, and per-axis needs only a board-map edit later. With AL on its own pair per stepper that
wiring is already done.

FLAG: **WIRE-ORING AN ASSERT-WHEN-HEALTHY OUTPUT IS A SERIES CHAIN, NOT A PARALLEL ONE.** The Mega
V's alarms asserted on fault, so paralleling them gave "any drive faulted". These assert when
*healthy*, so the equivalent is all four in **series** - any drive dropping out breaks the chain. Easy
to get backwards, and getting it backwards produces a guard that reads healthy when every drive is
dead.

## Provenance

The part, the cabling and the correction that the HBT57C is the Mega V's drive are all his,
2026-10-12. The manual is the TST57 series user manual he supplied the same day.

SETTLED: **The manual is committed** as
[`../manufacturer-assets/TST57-Integrated-Stepper-Manual.pdf`](../manufacturer-assets/TST57-Integrated-Stepper-Manual.pdf),
2026-10-12, which is what this repo's datasheets-committed rule requires. Everything above was read
out of it and can be re-checked against it.

OPEN: **The LISTING carries facts the manual does not, and the listing is not captured.** SW6's
function, the weight of 1.1 kg, the "recommend 36VDC" on the specification image, and the MicroUSB
caption that contradicts the manual all come from Amazon images rather than from the PDF. A listing
is exactly the kind of source that disappears - which is why this folder exists. Worth saving those
images alongside the manual.
