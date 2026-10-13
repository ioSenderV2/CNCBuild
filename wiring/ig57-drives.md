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
frames. Nothing in [`../dimensions/`](../dimensions/) currently carries a motor length.

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

OPEN: **Confirm the sense on the bench before relying on it**, because this is a machine-translated
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
conductor, minus on the solid**:

| Cat 6 pair | Striped | Solid |
|---|---|---|
| 1 | **PU+** | **PU-** |
| 2 | **DR+** | **DR-** |
| 3 | **EN+** | **EN-** |
| 4 | **AL+** | **AL-** |

NOTE: **THE SOLID CONDUCTOR IS THE SIGNAL'S MINUS LEG, NOT A GROUND.** The manual calls these inputs
differential, which is what that means: each pair is the two ends of an opto LED. Calling the minus
leg a ground invites someone to tie the four together as a convenience.

### SETTLED: The minus legs are independent - measured, and the seller was wrong

**No continuity between any of the minus signals.** His meter, on the part, 2026-10-12.

🔴 **THE SELLER SAID THEY WERE COMMONED INSIDE THE DRIVE, AND THEY ARE NOT.** That answer was written
into this file as *a claim rather than a datum*, specifically so it would get checked. Checking it
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
a stopped machine from one red LED.

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
