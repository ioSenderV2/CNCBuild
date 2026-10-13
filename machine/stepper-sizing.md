# Stepper sizing — 2.2 N·m on all four axes

| Axis | Motor |
|---|---|
| X | **2.2 N·m, NEMA 23** |
| Y1 | **2.2 N·m, NEMA 23** |
| Y2 | **2.2 N·m, NEMA 23** |
| Z | **2.2 N·m, NEMA 23** |

**One motor type for the whole machine, so one spare covers every axis.** The candidates were
1.5, 2.2 and 3.2 N·m, all NEMA 23 and all available in the 57 frame the cast stepper frames take —
see [`archive/y-beam-support.md`](archive/y-beam-support.md) for the frames themselves. The drives are
**IG57** all-in-one closed-loop units on a **36 V** rail - see
[`../wiring/ig57-drives.md`](../wiring/ig57-drives.md) - and that part of the machine is not reopened
here.

NOTE: **The part bought agrees with this file, which is worth saying plainly.** This document chose
2.2 N·m before the drives were bought; the IG57 is 2.2 N·m. So the conclusion below needed no
revision when the drive was settled on 2026-10-12. FLAG: **This file previously named the HBT57C,
which is the Mega V's drive and 3.2 N·m on X, Y1 and Y2** - corrected by him the same day. Where the
reasoning below leans on a *drive* characteristic rather than a motor one, it is now carrying an
assumption about a part this machine does not have.

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
| Drive | **IG57**, **24–50 V DC**, **5 A** | [`../wiring/ig57-drives.md`](../wiring/ig57-drives.md) — OPEN: off a retail listing, no manual committed |
| Supply | **36 V** — SETTLED 2026-10-12, the manual's recommended voltage. OPEN: wattage not recorded, so the current across all axes is not either | [`../wiring/ig57-drives.md`](../wiring/ig57-drives.md) |
| Screw efficiency | **0.9 assumed** | OPEN: not from a sheet — a conventional ball-screw figure |
| Screw root diameter | **13.5 mm assumed** | OPEN: the sheet gives only the 16 mm major — see below |

OPEN: **The kgf reading is an inference, not a datum.** 780 / 1790 are the standard pair for a 1605 and
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
see [`../wiring/ig57-drives.md`](../wiring/ig57-drives.md). Corner speed scales with supply voltage,
so torque rolls off **earlier** at 36 V and the motor-limited regime starts **lower** than this
chapter assumes. The conclusion that the axis is motor-limited rather than screw-limited is therefore
**more** true, not less - but every rpm figure below was written against 48 V and none of them has
been recomputed. OPEN: **Do not quote a speed from this chapter as if it applied at 36 V.** The stall
test below returns the one number that matters and it does not care what the rail is.

## Why not 1.5 N·m

Nothing in the analysis above rules it out: it clears the thrust envelope and the inertia by wide
margins on every axis. It loses on two practical counts rather than an engineering one.

1. **Z carries gravity continuously** as well as plunge force, and it is the one axis where a
   derated holding torque is working all the time rather than only in a cut.
2. **One motor type for four axes means one spare on the shelf.** Splitting the order to save on one
   or two motors buys a second part number into the machine.

OPEN: **BOTH OF THOSE REASONS ARE NOW CONTESTED, AND THE Z MOTOR IS AN OPEN QUESTION AS OF
2026-10-12.** His question, and his evidence:

- **On gravity:** the **Mega V runs 1.5 N·m on its Z and it has not been a problem** - his, and an
  operator's years of watching a machine outrank a concern written down here. The arithmetic agrees:
  the Z carriage weighed **9 kg** in [`../commissioning/masses.md`](../commissioning/masses.md), which
  through a 5 mm lead at the 0.9 efficiency assumed above needs about **0.08 N·m** to hold, or about
  **0.16** if the spindle and clamp block double the mass. Against 1.5 N·m that is not a derating
  worth the name.
- **On the spare:** he has an **IG57 1.5 N·m**, same family as the four 2.2 - so the second part
  number is already in the building, and fitting it to Z would leave a **spare 2.2 covering X, Y1 and
  Y2**, the three axes that do the work. That is arguably a better spare than one covering all four,
  because the fourth is the one least likely to need it.

**Not changed here pending his decision.**

### The HBT spares are a limp-home, not a spare - and the difference is the alarm

He holds **three HBT57C spares: two at 2.0 N·m and one at 1.5 N·m** - his, 2026-10-12. They are the
**Mega V's** family. Worth being exact about what they are and are not for this machine:

- **As a motor they would turn a screw.** Same NEMA 23 frame, and 36 V suits both families, so
  nothing stops one being bolted on to finish a job if an IG57 fails.
- 🔴 **As a drive they break the alarm guard, and not only for their own axis.** The HBT57C's alarm
  asserts **on fault**; the IG57's asserts when **healthy**. grblHAL's Teensy driver implements a
  **single combined** motor-fault input, so the four alarms are one chain - and one drive wired the
  opposite way does not degrade that axis, it **disables the guard for the whole machine**. See
  [`../wiring/ig57-drives.md`](../wiring/ig57-drives.md).

**So they are a limp-home with a known cost**: fit one, accept that motor-fault detection is off
until it comes out, and know that rather than discover it. They do **not** remove the case for an
IG57 spare, which is what the paragraph above is actually about.

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
4. ~~**The current budget is 12.5 A for all four axes.**~~ OPEN: **That was a 48 V figure and the
   rail is now 36 V, so it is stale.** The phase current is also no longer unknown - the IG57 is
   **5 A** - but the manual says the *supply* input current is smaller than the phase current and
   declines to give a figure, so four motors is not 20 A either. The budget now wants the supply's
   wattage, which is unrecorded, and a clamp meter once an axis runs.

## OPEN: The torque curve at 36 V

Everything above is settled except the figure that sets the **rapid feed rate in the firmware**: how
much torque a 2.2 N·m IG57 actually has at 1200 and 1500 rpm on a **36 V** rail. FLAG: **This heading
read "Openthe torque curve at 48 V" until 2026-10-12** - a marker mangled when the emoji markers
became words, which meant it was not being harvested into STATUS.md at all, and a voltage that has
since changed.

**Do not measure torque to get it.** A torque-speed curve needs a brake or a dynamometer, and the
number it yields then has to be converted back into a feed rate through the same assumed efficiency
that already appears twice above. **Measure the feed rate directly instead** — that is the quantity
the firmware wants, and the stall point is a sharper reading than any torque figure derived from it.

**The test, once the axis runs:** command increasing rapid moves with the axis under its real load
and find the feed rate at which the drive throws its tracking-error alarm. OPEN: **How the IG57
signals that is not established** - the HBT57C showed it as seven LED flashes, and whether this drive
uses the same scheme wants the manual, not an assumption. See
[`../wiring/ig57-drives.md`](../wiring/ig57-drives.md). Closed-loop drives make this
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

The reading goes in [`../commissioning/`](../commissioning/), which outranks every computed figure
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
