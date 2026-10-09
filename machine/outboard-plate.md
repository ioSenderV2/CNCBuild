# The full-height outboard plate

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

✅ **Decided 2026-09-29, material changed 2026-10-02, size settled by the order 2026-10-08. One per Y beam, 11 7/8" × 39 5/16" × 10 gauge
cold-rolled steel sheet**, replacing the existing 12" × 6" × 1/4" gusset - the dimensions rotate,
from 12" along the beam to 12" tall and a metre long.

## 🔴 It is steel now, and it is also the Y back joining plate

**Both halves of that sentence matter, and the second is what makes the first a reversal.** On Y
there is no separate 120 mm back joining plate - this plate *is* it, grown. So choosing steel here
overturns the explicit decision in [`gantry-beam-joint.md`](gantry-beam-joint.md):

> **Material is aluminium, not steel.** Steel would give roughly three times the modulus, but over
> 1000 mm a shop temperature swing puts a couple of tenths of differential expansion into a joint
> held by preloaded T-nuts that cannot comfortably slip. Matched aluminium removes the question.

**That reasoning was not wrong and is not being dismissed - the cost is being accepted instead of
avoided.** The differential is **0.17 mm over a metre at 15 K**, and the file had the magnitude
right at "a couple of tenths".

### Why 1/8", and it is the thin one on purpose

| | 1/8" steel | 1/4" 6061 (superseded) |
|---|---|---|
| In-plane shear and bending | **~1.5×** | 1.0× |
| Out-of-plane bending | 0.36× | **2.8×** |
| **Transformed area** - the flange term that drives composite bending | **9.2 mm equivalent aluminium** | 6.35 mm |
| Weight each | ~17 lb | ~12 lb |

Two things point the same way:

1. ✅ **9.2 mm equivalent is almost exactly the 3/8" (9.53 mm)** that
   [`gantry-beam-joint.md`](gantry-beam-joint.md) specifies for the Y back plate. So 1/8" steel is
   **sized right for the job it is taking over**, not merely adequate.
2. ✅ **Thermal restraint force scales with E·A**, so 1/8" generates **half** the load at the end
   T-nuts that 1/4" steel would. Against an objection that is specifically thermal, the thinner plate
   is the better answer.

The one argument for 1/4" steel is bolt bearing and durability as a chip barrier. It does not beat
halving the live objection, and 18.4 mm of equivalent aluminium is roughly double what anything here
asks for.

📌 **Cold-rolled sheet is the tidier product at this thickness, but hot-rolled A36 is acceptable and
is what was found.** Flatness does not bind here regardless: seven M8 along the bottom edge plus
the bolted lap against the tongue pull 1/8" steel straight over a metre without argument, and the holes are 9 mm
clearance into T-slots where the T-nut moves to meet the bolt.

### Sourcing, found 2026-10-02

| | |
|---|---|
| Listing *(superseded - not what was bought)* | 1/8" × 12" × 48" mild steel sheet, **A36 hot rolled, "11 gauge"**, uncoated |
| **Ordered** | **10 GA (.135) × 11 7/8" × 39 5/16" cold-rolled**, sheared, two pieces |
| Price | **$81.99 each** - and **two are needed**, one plate per sheet |
| Yield | 48" = 1219 mm against a 1000 mm plate, so a 219 mm offcut each |

✅ **CLOSED 2026-10-08: neither. It was bought as 10 gauge, .135" = 3.429 mm.** The listing's two
numbers disagreed - "11 gauge" is 0.1196" (3.04) against 1/8" at 0.125" (3.175) - and the sheet
actually ordered is thicker than both. Harmless for the structure either way: transformed area is
still on the 3/8" target. ⚠️ **Record the caliper reading in T_SIDE_PLATE**, not here and not in
T_OUTBOARD_PLATE, because the riser-proud check at the
front plates keys off this thickness.

📌 **~$4/lb is retail.** A steel service centre is typically around half that; at $164 for the pair
it is a judgement call whether the errand is worth it. **Mill scale comes off before paint** - and
paint is not optional here, see the galvanic note above.

### 🔴 Galvanic is the real cost of this change

Steel against aluminium, with **a metre of face-to-face contact** against the beam plus seven bolts
- and this plate is the **chip barrier**, so it is the part that actually gets wet with swarf and
coolant. Aluminium is the anode and the extrusion is the part that cannot be replaced.

**Powder coat or paint both faces**, and isolate the mating face if anything wetter than mist is
ever run. This is a bigger exposure than the rear plate's two bolt patterns and it is the one
downside that does not have a number attached.

✅ ~~**The channel was dimensioned around a 6.35 mm plate and the plate went to 1/8"**~~
**Dead - there is no channel**, and this warning outlived by a day the correction that killed it.
The plate sits flat on the top skin and the tongue laps it from outboard; see "THERE IS NO CHANNEL"
under "How it lands on the torsion box" below. Nothing to resize and nothing to rattle in.

At 12" it reaches from the beam down to the torsion box on a 12" riser, which is what makes it the
continuous shear web rather than just a longer gusset. **A 6" plate would have spanned the beam plus
32 mm and stopped 150 mm short of the box, doing none of what follows.** Same face, same length, same
thickness - the height is the whole difference.

Instead of stopping the back joining plate at the beam's 120 mm, **run it all the way down to the
torsion box** and bolt its bottom edge there. It then sits in the vertical plane containing the beam
axis, on the outboard face.

**This supersedes the gusset recommendation** carried in the project notes. Do not do both - a
gusset is a discrete triangle, this is a continuous one a metre long.

## What it does

1. **The span stops being a span.** Vertical load anywhere along the beam passes down through the
   plate, in its own plane, into the box. The ball screw never had to move - the support arrives
   from the side instead of from below.
2. **It removes the riser fore-aft weakness entirely.** Ball screw reaction and cutting force along
   Y lie **in the plane** of this plate.

| | Stiffness against fore-aft sway |
|---|---|
| Risers alone, bending about their weak axis | ~1 500 N/mm |
| Full-height plate, in-plane shear | **~670 000 N/mm** |

3. **The two members cover each other.** The plate is weak out-of-plane, across the machine - which
   is the direction the risers are strong in, edge-on. Neither is soft in the same axis.
4. **It is a chip barrier**, a metre of skirt on the outboard side of each Y beam.

## Two things to get right - both now resolved

✅ **Thermal - closed 2026-09-30, no slotting needed, and steel improved it.** A metre of plate
bolted along its length to a wooden box, against plywood that barely moves over a 15 °C swing:

| Plate material | Differential over 1000 mm at 15 K |
|---|---|
| Aluminium, as originally specified | **0.35 mm** |
| **Steel, as of 2026-10-02** | **0.18 mm** |

An earlier draft called for fixing solid at the centre and slotting the holes progressively toward
the ends. **That is unnecessary here.** The bolts are **9 mm clearance on M8**, which is 1 mm of
float per hole - several times the whole differential - and the shop is climate controlled with
Baltic birch skins. The 9 mm hole *is* the slot. This follows the precedent set on the Y risers,
reamed to 9 mm for the same reason.

🔴 **Do not transfer this conclusion to the T-nut row.** It is a different joint with a different
duty, and conflating them is how the steel question gets waved through without being answered:

| | Plate to box | Plate to extrusion |
|---|---|---|
| Differential at 15 K | 0.18 mm, steel to plywood | **0.17 mm, steel to aluminium** |
| What the bolts do | **"retention, not the load path"** - vertical and outboard loads arrive in bearing on plywood faces | **Preloaded friction joint whose entire job is shear transfer** across the seam |
| Can it take up the movement in the clearance? | Yes - nothing needs the bolts to grip | **This is the open question**, and it is what [`gantry-beam-joint.md`](gantry-beam-joint.md) rejected steel over |

The two numbers being near-identical is a coincidence of the materials, not evidence that the second
joint is as relaxed as the first.

The figure is kept because it is the one that had to be beaten, not because it is still a worry. Note
also that for plywood the larger term is **moisture, not temperature**; it is dismissed here on the
climate-controlled shop, not on the thermal arithmetic.

✅ **The box has a vertical face, because one is being built for it** - see the next section. The
warning this bullet used to carry stands, and it is the reason the interface took the shape it did:
landing only on the box's top surface through an angle would reintroduce a bending element and give
back much of the gain.

**Y beams only.** The X gantry moves and has nothing to bolt down to, so X keeps the 120 mm back
plate, **in 6061**. All of this added weight - roughly **17 lb per Y beam** at 1/8" steel - is
therefore static.

📌 **The steel parts in absolute terms: ~17 lb per side plate and ~40 lb for the 1210.73 mm rear
plate**, so roughly **75 lb of steel** on the fixed frame. A delta against the old scheme is not
quoted because the shear panel it absorbs was never sized. All static, all low down, against a
figure that was always offered as a design budget rather than a limit.

## How it lands on the torsion box

✅ **Decided 2026-09-30.** This is the plate's bottom fixing, and it is what closes the "does the
box have a vertical face" question above: **one is built into the box for the purpose.**

The box is **19 mm Baltic birch skins top and bottom over a grid of 19 mm strips 100 mm high**, so
138 mm deep overall. Two changes make it the plate's foundation:

1. **The box is widened to the machine's width at the plates**, so its top skin reaches out far enough
   that the plates stand on it rather than hanging alongside it.
2. **Each outer wall is two 19 mm laminations instead of one.** The inner one is an ordinary 100 mm web
   between the skins. The outer one is **180 mm tall, standing on the bottom skin's top face**, glued
   to the inner web's outer face and to the edge of the top skin. It spans the 100 mm web plus the
   19 mm top skin and so **stands 60 mm proud** of the top surface as a **tongue, outboard of the plate.**
   📌 **It is a tongue, not a curb.** The word "curb" is retired across the repo as of
   2026-10-04 - it carried the dead implication of a face the plate drops in against, and the plate
   is bolted through a lap instead.

🔴 **THERE IS NO CHANNEL - corrected 2026-10-03.** An earlier version of this section had the
top skin stopping short of the tongue's inner face and the plate dropping into the groove between
them. **It does not.** The plate sits **flat on the top skin** and the tongue laps it from
**outboard**: tongue inner face against plate outer face, a plain bolted lap. The bottom edge still
bears **directly over the wall** and never on skin spanning between grid members, which was the point
of the original arrangement and survives unchanged.

✅ **What that kills:** the open question about the channel's width. It was dimensioned around
6.35 when the plate was 1/4", the plate went to 1/8", and the groove was then 3 mm wider than the
thing it was supposed to locate. With no groove there is nothing to size, and the plate is located
by the tongue it is bolted through.

### Cross-section at the outer wall, inboard to outboard

| Member | Thickness | Vertical extent |
|---|---|---|
| Inner web of the outer wall | 19 mm | Between the skins, 100 mm high |
| The top skin | 19 mm | **Runs out to the tongue** - the plate stands on it |
| The full-height plate | **3.429 mm (10 gauge, ordered)** | Up to the Y beam - 11 7/8", 301.625 mm tall |
| Outer lamination, the tongue | 19 mm | 180 mm tall, **60 mm proud** of the top skin, **outboard of the plate** |

### The plate is captured on three sides

📌 **Unchanged by the no-channel correction** - all three still hold. The groove only ever did the same job the tongue does, from the other side.

| Direction | What takes it |
|---|---|
| Vertical | **Bearing** - plate bottom edge on the top skin, directly over the wall |
| Outboard, across the machine | **Bearing** - plate outer face against the tongue's inner face |
| Inboard | **Bolt tension** |

The consequence worth noticing: **the bolts are retention, not the load path.** Vertical and outboard
loads both arrive in bearing on plywood faces, which plywood is good at. So the bolt row is sized by
convenience rather than by strength - an estimated ~500 N of static vertical per Y beam shared across
seven M8 is orders of magnitude clear, and this joint's real limits are geometric, not structural.

### The bolt row

| | |
|---|---|
| Fastener | **M8 at 150 mm, first at 50** - seven per beam over the 1000 mm. 🔴 Was eleven at 100 until 2026-10-03; unified with the other bolt-on plates |
| Height | **Y 30** above the plate's bottom edge - the same row height as the front fin and the back plate |
| Direction | From **outboard**: washer, **tongue**, plate, **M8 locknut** on the inboard face |
| Holes | **9 mm clearance** in **tongue** and plate both - see the thermal bullet above |
| Why not tapped into the plate | M8 into 6.35 mm of aluminium is about **5 threads, 0.8 × D**, where aluminium wants 1.5-2 × D. It would strip before the bolt came near yield and could never be properly preloaded. The inboard face is open air - the beam is up on 12" risers - so a through-bolt costs nothing and was always available |

Glue area is not a constraint: roughly **100 000 mm²** of face-to-face plywood per wall over the box
depth, plus the top skin's edge.

### What this buys beyond a fixing: restraint along the whole metre

Loads **along Y** lie in the plate's plane and were always handled. Loads **across the machine** -
gantry acceleration, cutting force in X, the two Y beams wanting to spread - are out-of-plane for the
plate, and the previous answer was that the risers take them edge-on, which means **at the two ends
only.** The tongue now takes that same load in plywood face bearing over the **full 1000 mm.**

That is a structural gain rather than a side effect of the assembly method, and it is part of why the
interface is shaped this way instead of bolted flat to the box's top surface.

### Two things to get right when cutting

⚠️ **Bias the top skin wide, never narrow.** The skin's width sets the distance between the two
**tongues'** inner faces, and a tongue's inner face is a hard bearing face with no float - the 9 mm
holes let the *bolt* move, not the bearing. A millimetre or two **too wide** leaves a gap a shim
fixes in minutes. **Too narrow and the plates will not fit between the tongues at all**, and planing
a glued-up skin edge in place is a miserable job. The same cost at cut time, wildly different cost
if you are out.

📌 **"Fit between", not "drop between"** - the plates are not lowered into anything. They stand on
the top skin and each is lapped from outboard by its tongue. The gap still has to be right, for the
same reason and to the same tolerance; what is gone is the groove.

⚠️ **The plate-to-tongue seam is a swarf trap** running the length of the machine - the plate is
the chip barrier and the tongue sits outboard of it. Either seal the top of the seam or leave it
deliberately open at both ends so it can be blown through.

### 🔴 The machine is the reference, not the box - so the box is built last

**The box will not be built until the whole CNC is assembled on a flat surface and the width measured
exactly.** That is the standing rule of this repo applied to a structural part: the machine is the
authority, not the drawing.

It also means the machine **jigs itself** for that measurement, and nothing has to be computed:

| What sets it | How |
|---|---|
| The two Y beams' spacing | The **X gantry** bridging them - its length, its end plates and the bearing block footprint |
| Their coplanarity and parallelism | The **flat surface** they are assembled on, plus the risers' 9 mm reamed holes absorbing the error |
| The box's top skin width | **Measured off that assembly**, once it is standing and square |

So there is no box-width number to derive and no X-span figure to look up first. The sequence is
**assemble, measure, then cut skins**, and the measured value belongs in
[`../commissioning/`](../commissioning/) when it is taken.

Two consequences worth holding on to:

- **The bias-wide rule above still applies**, but as insurance against a transfer error rather than
  against a design unknown.
- **Do not let a nominal or catalog width substitute for the measurement.** That is exactly the failure
  the `$130` story in the [root README](../README.md) records - 889 mm written where the real number
  was 860 mm - and here the cost is a set of plywood skins cut to the wrong size.

## The magnetic encoder tape runs on the front plate

The **10 mm magnetic tape** for the AS5311 sensors runs on the face of the **45 mm front plate**,
centred in the gap between its two rows of seven M8 flange bolts. Two rows at ±15 mm with **13.8 mm**
flange heads leaves **16.2 mm clear**. 🔴 **What has to fit in that lane is the SENSOR PUCK, not the
tape**: it needs **15 mm**, so the margin is **0.6 mm a side**. ⚠️ At the old 17.3 mm head the lane
was 12.7 and the puck missed by 1.15 a side - the tape fitted and the thing that reads it did not,
which is the trap in sizing this gap off the tape width.

🔴 **Those bolts must be austenitic stainless.** They put ferromagnetic material about 1 mm from
the edge of a magnetic scale, repeating every 150 mm, and steel draws flux laterally. The failure
mode is not a constant offset but a **periodic error at exactly the bolt spacing**, which would read
as a scale or pitch fault while everything else about the axis looked healthy.

🔴 **Checked 2026-09-29: the generic "stainless" bolts on hand ARE magnetic.** Sold as stainless,
bought from Amazon, and a magnet grabs them. **Sourcing A4 / 316 from Tacoma Screw instead.**

"Stainless" does not mean non-magnetic. A2 (304) and A4 (316) are austenitic and effectively
non-magnetic - around a hundred-fold less flux distortion than carbon steel. **410, 416 and 430 are
martensitic or ferritic, as bad as carbon steel here**, and are sold as "stainless" with no
qualification. Cold-forming a bolt head also raises permeability locally, right at the part nearest
the tape, so **ask for A4 rather than A2** and **put a magnet on them when they arrive** - the label
has already been wrong once.

**Only the front strips need this**, since that is where the tape runs: 14 per strip.

✅ **Settled 2026-10-02: all three beams carry tape**, X included. This file previously left X
conditional - "plus 14 more if the X beam's front plate carries tape the same way". It does. **So
the count is 42 A4 / 316 flange bolts, not 28**, and the magnet-on-arrival check applies to all
three sets.

🔴 **A new magnetic object arrived with the stepper move.** A NEMA 23 permanent-magnet rotor now
sits at the **min-Y end** of both Y tapes. That is a far larger disturbance than a bolt head, and it
is *not* the periodic error this section was written about - it is a localised one at one end of
travel. **Read a sensor at that end against mid-travel before laying the tape.**

📌 **If A4 flange bolts are awkward to source, socket heads are fine and slightly better.** A 13 mm
socket head leaves 17 mm between rows against the flange's 12.7 mm; with an M8 washer, about 14 mm.
More room for the tape either way - do not fight the supplier over head style.

⚠️ **This is reasoning from principle, not a measurement.** The AS5311's sensitivity to lateral
disturbance is not established here, and
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md)
is the authority on the sensing side. To know rather than assume: fit a tape offcut and a sensor, and
read across a bolt head against between bolt heads. Worth doing before 3 m of one-shot PSA goes down.

⚠️ **Decide the application order.** 1 mm of margin each side over a metre. Either the bolts go in
first as a guide channel - appealing, but then PSA has to be threaded into a 12 mm slot - or the tape
goes down first against a straightedge and the bolts follow.

✅ **The X end plate's sensor bore lines up with this tape**, which runs on the Y beam's seam
centreline, placing the 35 mm bore in the gap between the upper and lower Y bearing block rows.
**Measured: that gap is 45 mm**, so the bore fits with 5 mm each side. (An earlier estimate of 56 mm
was optimistic.)

⚠️ 5 mm is clearance and not much else - **no room for a flanged puck or an external clamp ring.**
Check that against the puck design in
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md).

---
