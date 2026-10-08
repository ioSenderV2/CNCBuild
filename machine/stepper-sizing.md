# Stepper sizing — 2.2 N·m on all four axes

| Axis | Motor |
|---|---|
| X | **2.2 N·m, NEMA 23** |
| Y1 | **2.2 N·m, NEMA 23** |
| Y2 | **2.2 N·m, NEMA 23** |
| Z | **2.2 N·m, NEMA 23** |

**One motor type for the whole machine, so one spare covers every axis.** The candidates were
1.5, 2.2 and 3.2 N·m, all NEMA 23 and all available in the 57 frame the cast stepper frames take —
see [`y-beam-support.md`](y-beam-support.md) for the frames themselves. The drives are TOSEASTARS
HBT57C on a 48 V rail; that part of the machine is settled in
[`../wiring/breakout-box.md`](../wiring/breakout-box.md) and is not reopened here.

🔴 **The size is not set by force, and the usual intuition is wrong on this machine.** A 5 mm lead
gives so much mechanical advantage that all three candidates deliver several times the thrust the
structure is designed for. What separates them is **torque in the 1000–1500 rpm band**, and there
the smaller motor is the better one.

## The inputs, and where each came from

| | Value | Where from |
|---|---|---|
| Ball screw | **1605** — 16 mm major, **5 mm lead** | spec sheet |
| Ca, dynamic | **780** | spec sheet — ⚠️ units read as **kgf**, so 7650 N |
| Coa, static | **1790** | spec sheet — ⚠️ units read as **kgf**, so 17 560 N |
| Bearing-to-bearing span | **930 mm** | **measured** on the built Y beams |
| Motor frame | **NEMA 23**, all four axes | given |
| Drive | HBT57C, **24–55 V DC**, 36 V recommended | [`../wiring/breakout-box.md`](../wiring/breakout-box.md) |
| Supply | **48 V, 600 W — 12.5 A across all axes** | [`../wiring/breakout-box.md`](../wiring/breakout-box.md) |
| Screw efficiency | **0.9 assumed** | ⚠️ not from a sheet — a conventional ball-screw figure |
| Screw root diameter | **13.5 mm assumed** | ⚠️ the sheet gives only the 16 mm major — see below |

⚠️ **The kgf reading is an inference, not a datum.** 780 / 1790 are the standard pair for a 1605 and
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
thrust used in the Y peel check in [`y-beam-support.md`](y-beam-support.md). Even 1.5 N·m clears
both. **Every candidate is oversized on thrust, so thrust cannot choose between them.**

📌 **The motor is the fuse, and that is the right way round.** The largest candidate reaches 3620 N,
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
| A NEMA 23 rotor | ~4.8 × 10⁻⁵ kg·m² — ⚠️ a typical figure, not read off a sheet |
| **20 kg of gantry reflected through the lead** | **1.3 × 10⁻⁵ kg·m²** |

🔴 **The screw and the rotor are the inertia; the moving mass is a rounding error.** That inverts
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
⚠️ **Use the 1510 rpm row as the working figure** and treat the other as headroom that may or may
not be there.

📌 **The sensitivity runs the other way from where the effort wants to go.** Whip speed is
**linear** in root diameter and goes as **one over span squared**. The 930 mm measurement was worth
taking; chasing the root diameter with a caliper is not, because the whole 13.5-to-16 range moves
the ceiling by 16% and changes no decision. **If Y travel is ever extended, this is the figure to
recompute** — not the motor choice.

**A NEMA 23 on 48 V is well down its torque curve before 1500 rpm**, so the motor reaches its limit
at or below the whip ceiling. **The axis is motor-limited, not screw-limited** — which is precisely
the regime where the candidates differ.

## Why not 1.5 N·m

Nothing in the analysis above rules it out: it clears the thrust envelope and the inertia by wide
margins on every axis. It loses on two practical counts rather than an engineering one.

1. **Z carries gravity continuously** as well as plunge force, and it is the one axis where a
   derated holding torque is working all the time rather than only in a cut.
2. **One motor type for four axes means one spare on the shelf.** Splitting the order to save on one
   or two motors buys a second part number into the machine.

## Why not 3.2 N·m

It is mechanically available — all four frames are NEMA 23 and the 3.2 comes in that frame — so this
is a choice, not a constraint.

1. **No thrust is needed.** It buys 1130 N of stall thrust over the 2.2 in a machine whose envelope
   is 1000 N, against a screw whose static rating neither motor approaches.
2. **It is worse where the machine runs.** A higher-torque motor in the same frame carries more
   inductance, which rolls the torque curve off earlier. Above roughly 1200 rpm on a 48 V rail the
   2.2 is expected to deliver **more** torque than the 3.2, and 1200 rpm is inside the band this
   machine's rapids live in. ⚠️ **Expected, from the shape of the curves — not measured.** This is
   the one claim in this chapter that a torque curve could overturn, and it is the claim the
   decision rests on most heavily.
3. **It adds hanging mass at a reach already budgeted.** Both
   [`x-gantry-end-plates.md`](x-gantry-end-plates.md) and [`y-beam-support.md`](y-beam-support.md)
   accept the stepper-and-casting cantilever on the figure *"roughly 2.5 kg at that reach is under
   2 N·m"*. A 3.2 is a longer, heavier motor than that figure assumes. The 2.2 sits inside it.
4. **The current budget is 12.5 A for all four axes.** ⚠️ Rated phase current per motor is not in
   this repo for any of the three candidates; it wants the motor datasheet before an order, and it
   is the one place where the larger motor could fail outright rather than merely fail to help.

## ⚠️ Open — the torque curve at 48 V

Everything above is settled except the figure that sets the **rapid feed rate in the firmware**: how
much torque a 2.2 N·m HBT57C-driven motor actually has at 1200 and 1500 rpm on a 48 V rail.

**Do not measure torque to get it.** A torque-speed curve needs a brake or a dynamometer, and the
number it yields then has to be converted back into a feed rate through the same assumed efficiency
that already appears twice above. **Measure the feed rate directly instead** — that is the quantity
the firmware wants, and the stall point is a sharper reading than any torque figure derived from it.

**The test, once the axis runs:** command increasing rapid moves with the axis under its real load
and find the feed rate at which the drive throws its tracking-error alarm — seven LED flashes on the
HBT57C, per [`../wiring/breakout-box.md`](../wiring/breakout-box.md). Closed-loop drives make this
easy, because the drive detects the loss of sync itself rather than leaving it to be inferred from a
part cut wrong. **Back off 30% from the first alarm** and that is the rapid.

📌 **Run it on Z as well as X and Y, and run Z both directions.** Z is the axis where gravity adds to
the load in one direction and subtracts in the other, so its two stall points differ and the
down-travel figure is the misleading one.

⚠️ Two cross-checks belong with that test and are not yet done:

- **Whether the 1510 rpm whip figure or the motor stalls first.** 1510 rpm is 7.6 m/min; if the
  alarm comes in below that, the axis is motor-limited as predicted and the whip calculation never
  binds. If it comes in above, the whip figure is the operative ceiling and the conservative row was
  the wrong one to use.
- **Audible whip is its own evidence.** A screw approaching its first mode is heard before anything
  faults. ⚠️ **Hearing it below the computed figure means the span, the preload or the support
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
| **Rated phase current × 4 exceeds 12.5 A** | the supply or the motor has to move, whichever the budget favours |
| **Y travel is extended** | recompute whip — it goes as one over span squared, and 930 mm is the measured basis |

**None of them is affected by the root diameter**, which is why it is left as an assumption.
