# Stepper sizing — 2.2 N·m on the three working axes, 1.5 on Z

| Axis | Motor |
|---|---|
| X | **2.2 N·m, NEMA 23** |
| Y1 | **2.2 N·m, NEMA 23** |
| Y2 | **2.2 N·m, NEMA 23** |
| **Z** | **1.5 N·m, NEMA 23** — his, 2026-10-12 |
| **Spare** | **2.2 N·m** — covers X, Y1 and Y2 |

**The spare covers the three axes that do the work.** Four 2.2 were bought and three are fitted, so
the fourth is on the shelf for the axes carrying the hours and the load. Z runs the 1.5, which is the
lightest duty on the machine and the one least likely to need a spare. **This is a better
arrangement than one spare covering all four**, which is what this file argued for until the Z motor
was settled.

The candidates were 1.5, 2.2 and 3.2 N·m, all NEMA 23 and all available in the 57 frame the cast
stepper frames take — see [`archive/y-beam-support.md`](archive/y-beam-support.md) for the frames
themselves.

🔴 **SUPERSEDED BY PURCHASE, 2026-11-25: the machine runs four new HBT57112C** - the Mega V's
family, one type on all four axes, see
[`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md). OPEN: **their torque rating is
not recorded** - off the part or its manual, not from memory. The selection this file argues -
2.2 N·m on X, Y1, Y2 and 1.5 on Z, from torque in the 1000-1500 rpm band - **stays as the record
of the reasoning**; its conclusion no longer names the part on the machine, and where it leans on
a *drive* characteristic it describes the IG57.

~~FLAG: **BOTH MOTORS MUST BE IG57.** The 1.5 on Z is an IG57, not one of the HBT57C spares -
their alarm asserts on fault where the IG57's asserts when healthy, and one drive wired the
opposite way disables the guard for the whole machine.~~ RETIRED 2026-11-25: all four drives are
HBT and the mixed-chain hazard now points at the IG57 instead - the HBT-spares section below
carries the live version.

NOTE (history): this document chose 2.2 N·m before any drive was bought; the IG57 bought
2026-10-12 was 2.2 N·m, so the conclusion held then. The file had named the HBT57C even earlier,
was corrected the same day because that was the Mega V's drive - and the 2026-11-25 purchase
makes the HBT the machine's family after all.

FLAG: **The size is not set by force, and the usual intuition is wrong on this machine.** A 5 mm lead
gives so much mechanical advantage that all three candidates deliver several times the thrust the
structure is designed for. What separates them is **torque in the 1000–1500 rpm band**, and there
the smaller motor is the better one.

## The inputs, and where each came from

| | Value | Where from |
|---|---|---|
| Ball screw | **1605** — 16 mm major, **5 mm lead** | spec sheet |
| Ca, dynamic | **780** | spec sheet — OPEN: units read as **kgf**, so 7650 N |
| Coa, static | **1790** | spec sheet — OPEN: units read as **kgf**, so 17 560 N |
| Bearing-to-bearing span | **930 mm** | **measured** on the built Y beams |
| Motor frame | **NEMA 23**, all four axes | given |
| Drive | **HBT57112C** - his, 2026-11-25; family recorded 24-55 V, current rating OPEN | [`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md) — OPEN: its manual is not committed either |
| Supply | **XDR-960-36: 36 V, 960 W — 26.6 A across all axes** | spec, bought 2026-11-13; the 600 W 16.5 A brick stands down to spare. Output adjusts 36-42 V, so the 36 is still a setting to meter — see [`../wiring/cabinet-power-and-grounding.md`](../wiring/cabinet-power-and-grounding.md) |
| Screw efficiency | **0.9 assumed** | OPEN: not from a sheet — a conventional ball-screw figure |
| Screw root diameter | **13.5 mm assumed** | OPEN: the sheet gives only the 16 mm major — see below |

OPEN: **The kgf reading is an inference, not an established fact.** 780 / 1790 are the standard pair for a 1605 and
the units column was not captured. **If they turn out to be newtons rather than kgf the life
calculation below collapses by a factor of 9.6** and the screw becomes a term in the decision
instead of a non-term. Worth one glance at the sheet's column header.

## Thrust is not the constraint

Thrust at the nut is 2π·T·η / lead. At η = 0.9 and a 5 mm lead:

| Motor | Stall thrust | At half of rated torque |
|---|---|---|
| 1.5 N·m | 1700 N | 850 N |
| 2.2 N·m | **2490 N** | **1240 N** |
| 3.2 N·m | 3620 N | 1810 N |

Against that, two figures this repo already works to: the **500–1000 N structural envelope** in
[`loads-and-plate-thicknesses.md`](loads-and-plate-thicknesses.md), and the **~700 N** working
thrust used in the Y peel check in [`archive/y-beam-support.md`](archive/y-beam-support.md). Even 1.5 N·m clears
both. **Every candidate is oversized on thrust, so thrust cannot choose between them.**

NOTE: **The motor is the fuse, and that is the right way round.** The largest candidate reaches 3620 N,
a fifth of the 17 560 N static rating. **A crash stalls the motor long before anything can brinell
the screw** — so there is no screw-protection argument for the smaller motor, and no
screw-damage argument against the larger one. Neither direction gets a vote.

## Nor is screw life

L10 life is (Ca / F)³ × 10⁶ revolutions:

- at the **~700 N** working thrust: **1.3 billion revolutions**, which at 5 mm a turn is
  thousands of kilometres of axis travel;
- at the full **2490 N** stall thrust, held continuously, which never happens: 29 million
  revolutions, about **145 km** of travel.

**Screw life is not a term in this decision.** It survives the chosen motor's worst case by orders
of magnitude.

## Nor is inertia

Reflected load inertia through a 5 mm lead is mass × (lead / 2π)², which is **6.3 × 10⁻⁷ kg·m² per
kilogram**. So the machine's own mass very nearly vanishes at the motor shaft:

| | Inertia at the motor shaft |
|---|---|
| The 930 mm screw itself, 16 mm | 4.7 × 10⁻⁵ kg·m² |
| A NEMA 23 rotor | ~4.8 × 10⁻⁵ kg·m² — OPEN: a typical figure, not read off a sheet |
| **20 kg of gantry reflected through the lead** | **1.3 × 10⁻⁵ kg·m²** |

FLAG: **The screw and the rotor are the inertia; the moving mass is a rounding error.** That inverts
the usual sizing instinct, which reaches for a bigger motor when the gantry is heavy. Here a bigger
motor mostly accelerates its own rotor.

Summing the three and accelerating the axis at 2 m/s² — angular acceleration 2π·a / lead, so
2510 rad/s² — asks for about **0.27 N·m**. All three candidates are many times that.

## What the constraint actually is: whip, then the torque curve

With nothing mechanical or structural choosing between the motors, the ceiling on the axis is
**rotational speed**, and the first wall is the screw's own first bending mode.

Computed on the **assumed 13.5 mm root** rather than the 16 mm major, which understates the real
shaft stiffness and is therefore the conservative direction, over the **measured 930 mm** span:

| Support condition | First mode | At an 0.8 derate | Rapid at 5 mm lead |
|---|---|---|---|
| Both ends simple | 1890 rpm | **1510 rpm** | **7.6 m/min** |
| BK12 fixed, BF12 simple | 2950 rpm | 2360 rpm | 11.8 m/min |

The arrangement is BK12 at one end and BF12 at the other, which is the second row — **but that row
holds only if the BK12 angular-contact pair is preloaded and genuinely behaving as a fixed end.**
OPEN: **Use the 1510 rpm row as the working figure** and treat the other as headroom that may or may
not be there.

NOTE: **The sensitivity runs the other way from where the effort wants to go.** Whip speed is
**linear** in root diameter and goes as **one over span squared**. The 930 mm measurement was worth
taking; chasing the root diameter with a caliper is not, because the whole 13.5-to-16 range moves
the ceiling by 16% and changes no decision. **If Y travel is ever extended, this is the figure to
recompute** — not the motor choice.

**A NEMA 23 on 48 V is well down its torque curve before 1500 rpm**, so the motor reaches its limit
at or below the whip ceiling. **The axis is motor-limited, not screw-limited** — which is precisely
the regime where the candidates differ.

🔴 **THE RAIL IS 36 V NOW, NOT 48, AND THIS PARAGRAPH IS THE ONE MOST AFFECTED.** Settled 2026-10-12 -
see [`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md). Corner speed scales with supply voltage,
so torque rolls off **earlier** at 36 V and the motor-limited regime starts **lower** than this
chapter assumes. The conclusion that the axis is motor-limited rather than screw-limited is therefore
**more** true, not less - but every rpm figure below was written against 48 V and none of them has
been recomputed. OPEN: **Do not quote a speed from this chapter as if it applied at 36 V.** The stall
test below returns the one number that matters and it does not care what the rail is.

## Why not 1.5 N·m — except on Z, where it is the motor

~~SETTLED: **Z RUNS THE 1.5 - his decision, 2026-10-12.** X, Y1 and Y2 keep the 2.2.~~ SUPERSEDED
2026-11-25: **all four axes run the same new HBT57112C, Z included.** This section is kept because
its reasoning - gravity, spares, what a closed loop makes acceptable - is the record the decision
was taken against, and the IG57 1.5 it names is no longer on the machine.

Nothing in the analysis above ever ruled the 1.5 out: it clears the thrust envelope and the inertia
by wide margins on every axis. It lost on two practical counts rather than an engineering one, and
**both of them failed on Z**:

1. ~~**Z carries gravity continuously**~~ as well as plunge force, and it is the one axis where a
   derated holding torque is working all the time rather than only in a cut.
2. ~~**One motor type for four axes means one spare on the shelf.**~~ Splitting the order to save on
   one or two motors buys a second part number into the machine.

**Why each failed:**

- **On gravity:** the **Mega V runs 1.5 N·m on its Z and it has not been a problem** - his, and an
  operator's years of watching a machine outrank a concern written down here. The arithmetic agrees:
  the Z carriage weighed **9 kg** in [`../commissioning/masses.md`](../commissioning/masses.md), which
  through a 5 mm lead at the 0.9 efficiency assumed above needs about **0.08 N·m** to hold, or about
  **0.16** if the spindle and clamp block double the mass. Against 1.5 N·m that is not a derating
  worth the name.
- **On the spare:** he has an **IG57 1.5 N·m**, same family as the four 2.2 - so the second part
  number was already in the building, and fitting it to Z leaves a **spare 2.2 covering X, Y1 and
  Y2**, the three axes that do the work. That is a better spare than one covering all four, because
  the fourth is the one least likely to need it.

**What the 1.5 gives up, recorded because it is real:** 850 N of thrust at half rated torque against
the 2.2's 1240 N, on a structural envelope of 500-1000 N - so on the heaviest plunge the design
contemplates, the motor is nearer to being the limit than the structure is. And less torque through
the speed band, which costs Z retract time.

NOTE: **A CLOSED LOOP IS WHAT MAKES THAT ACCEPTABLE.** Under-torquing on these drives produces a
**detected tracking fault**, not a silently mispositioned part - the machine stops and says so. The
cost of being under-motored here is a stopped job, not a scrapped one, which is a different class of
risk from the open-loop case this kind of decision is usually made in.

### The HBT spares - the same family as the machine since 2026-11-25

He holds **three HBT57C spares: two at 2.0 N·m and one at 1.5 N·m** - his, 2026-10-12 - and the
machine's own drives are now four new **HBT57112C** (his, 2026-11-25), so the spares and the
machine are **one family**. What this section used to guard against - an HBT assert-on-fault
alarm wired into an IG57 assert-when-healthy chain, disabling the guard for the whole machine -
dissolved with the IG57: every drive in the building asserts on fault, and a spare bolted on in
a pinch keeps the alarm chain consistent **by construction**.

MEASURED, his bench, 2026-11-25 - **the family's alarm sense has numbers.** Two HBT57112C units,
12 V through a 10K onto AL+, AL- commoned to the supply's 0 V, EN disconnected: powered with a
solid green LED the output reads the full pull-up - **12.185 V and 12.184 V: released when
healthy** - and unpowered reads 0.37 V and 0.054 V, conduction through the dead electronics
rather than a designed assertion. Consistent with the Mega V's service history of paralleled
alarms giving "any drive faulted". Worth knowing at a bench: a plain continuity check across a
healthy unit's AL+ / AL- correctly reads **open**. Details and open items in
[`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md).

What stays open about the spares: OPEN - whether a 2.0 or 1.5 N·m spare moves a given axis
acceptably depends on the new units' own torque rating, which is not recorded. And the hazard
now runs the other way: 🔴 **an IG57 pressed into service is the odd one out** - its alarm sense
was never measured, and one assert-when-healthy output in the parallel chain is a stuck alarm
that hides every real one behind it. Bench it first; the drives file carries the warning.

~~🔴 **The same argument kills a Mega V motor swap.**~~ RETIRED 2026-11-25 - the machine runs the
Mega V's family by purchase, so there is nothing left for the argument to kill; the chain is
consistent and the firmware's alarm polarity is set once, for one sense, in
[`../commissioning/bench-session.md`](../commissioning/bench-session.md)'s commissioning of
$744/$745. OPEN: **the 3.2 vs 2.2 stall comparison** this section once offered is moot as a
decision input and stays moot - the parts on the machine are bought.

## Why not 3.2 N·m

It is mechanically available — all four frames are NEMA 23 and the 3.2 comes in that frame — so this
is a choice, not a constraint.

1. **No thrust is needed.** It buys 1130 N of stall thrust over the 2.2 in a machine whose envelope
   is 1000 N, against a screw whose static rating neither motor approaches.
2. **It is worse where the machine runs.** A higher-torque motor in the same frame carries more
   inductance, which rolls the torque curve off earlier. Above roughly 1200 rpm on a 48 V rail — the
   rail this was written for, now 36 V, so the crossover sits lower — the
   2.2 is expected to deliver **more** torque than the 3.2, and 1200 rpm is inside the band this
   machine's rapids live in. OPEN: **Expected, from the shape of the curves — not measured.** This is
   the one claim in this chapter that a torque curve could overturn, and it is the claim the
   decision rests on most heavily.
3. **It adds hanging mass at a reach already budgeted.** Both
   [`archive/x-gantry-end-plates.md`](archive/x-gantry-end-plates.md) and [`archive/y-beam-support.md`](archive/y-beam-support.md)
   accept the stepper-and-casting cantilever on the figure *"roughly 2.5 kg at that reach is under
   2 N·m"*. A 3.2 is a longer, heavier motor than that figure assumes. The 2.2 sits inside it.
4. SETTLED: ~~**The current budget is 12.5 A for all four axes.**~~ **It is 16.5 A** - the 36 V 600 W
   supply's nameplate, 2026-10-12. **The budget grew by 4 A as a side effect of dropping the rail to
   36 V for over-voltage headroom**, which is the rare case of a safety decision paying for itself.
   The phase current was known too - the IG57 was **5 A**; OPEN: the HBT57112C's rating waits on
   its manual (2026-11-25), and supply current runs below phase current by an unstated margin
   either way. SETTLED
   again 2026-11-13: **the budget is 26.6 A - the XDR-960-36 replaced the brick**, and the sizing
   comparison is over before it starts. OPEN: what they
   actually draw is still worth a reading - it sets the heat into the DIN enclosure - and it is now
   a **DC clamp meter** reading, because the XDR has no display.

## OPEN: The torque curve at 36 V

Everything above is settled except the figure that sets the **rapid feed rate in the firmware**: how
much torque the drive actually delivers at 1200 and 1500 rpm on a **36 V** rail - asked of a 2.2 N·m
IG57 when written, now of the HBT57112C. FLAG: **This heading
read "Openthe torque curve at 48 V" until 2026-10-12** - a marker mangled when the emoji markers
became words, which meant it was not being harvested into STATUS.md at all, and a voltage that has
since changed.

**Do not measure torque to get it.** A torque-speed curve needs a brake or a dynamometer, and the
number it yields then has to be converted back into a feed rate through the same assumed efficiency
that already appears twice above. **Measure the feed rate directly instead** — that is the quantity
the firmware wants, and the stall point is a sharper reading than any torque figure derived from it.

**The test, once the axis runs:** command increasing rapid moves with the axis under its real load
and find the feed rate at which the drive throws its tracking-error alarm. **The HBT family
signals that as seven LED flashes** - its own manual's code, recorded in
[`../wiring/hbt57112c-drives.md`](../wiring/hbt57112c-drives.md), and bench-session §6 is where
the real part confirms it. Closed-loop drives make this
easy, because the drive detects the loss of sync itself rather than leaving it to be inferred from a
part cut wrong. **Back off 30% from the first alarm** and that is the rapid.

NOTE: **Run it on Z as well as X and Y, and run Z both directions.** Z is the axis where gravity adds to
the load in one direction and subtracts in the other, so its two stall points differ and the
down-travel figure is the misleading one.

OPEN: Two cross-checks belong with that test and are not yet done:

- **Whether the 1510 rpm whip figure or the motor stalls first.** 1510 rpm is 7.6 m/min; if the
  alarm comes in below that, the axis is motor-limited as predicted and the whip calculation never
  binds. If it comes in above, the whip figure is the operative ceiling and the conservative row was
  the wrong one to use.
- **Audible whip is its own evidence.** A screw approaching its first mode is heard before anything
  faults. OPEN: **Hearing it below the computed figure means the span, the preload or the support
  condition is not what this chapter assumed** — and the measurement to revisit is the 930 mm and
  the BK12 preload, not the motor.

The reading goes in [`../commissioning/`](../commissioning), which outranks every computed figure
in this chapter.

## What would change the answer

Stated plainly, because three of the figures above are assumptions rather than data:

| If this turns out differently | Then |
|---|---|
| **Ca / Coa are newtons, not kgf** | screw life drops by 9.6× and becomes a real term; recheck the 2490 N stall case |
| **The 2.2 does not beat the 3.2 above 1200 rpm** on the actual curves | the "why not 3.2" argument loses its main leg and the choice is worth reopening |
| **Four drives draw more than the supply can give at 36 V** | the supply has to move — the motor is bought, and the rail is settled at the manual's recommended voltage |
| **Y travel is extended** | recompute whip — it goes as one over span squared, and 930 mm is the measured basis |

**None of them is affected by the root diameter**, which is why it is left as an assumption.
