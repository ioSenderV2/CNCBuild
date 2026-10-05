# Tramming

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

⚠️ **Partly open - the nod adjustment is undecided and has a deadline** (see [`machining.md`](machining.md);
hole sizes depend on it).

## The rule that constrains every option

**A bolted face can only tilt about axes lying in that face.** Shimming or jacking changes standoff
along the face's *normal*, which produces rotations about the two axes *in* the face and never about
the normal itself. So each interface corrects exactly two of the three rotations, fixed by which way
it points:

| Interface | Face normal | Gives |
|---|---|---|
| X carriage plate ↔ X bearing blocks | Y (fore-aft) | **nod** + yaw |
| Spacers / spindle clamps ↔ Z plate | Y | **nod** + yaw |
| **X end plates ↔ Y carriage blocks** | X (across) | **roll** + yaw |

## 🔴 Do not make the carriage plate joint adjustable

Set screws over each bearing block is the usual arrangement and it is wrong here, for two reasons:

1. **The bolt heads are buried.** They sit on the carriage plate's front face, under the Z rails, the
   screw and the travelling nut housing. There is no access once assembled.
2. **That joint carries everything.** Replacing ~3400 mm² of face contact per block with four set
   screw tips gives local yielding, brinelling under cyclic load, and a joint that keeps settling for
   months. At 1000 N it undoes the stiffness the rest of the design is chasing.

**Build it solid and treat it as a datum.** Get it right at the mill.

## ✅ Roll: SHIM THE SHELF - decided 2026-10-02

**Roll is adjusted by shimming between the shelf bar's top face and the X beam's bottom extrusion, at
one end plate only.** Raising one end of the beam rotates it about Y, which leans the spindle
left-right. Shim the low end.

❌ ~~**Oversize the bearing block holes and add jack screws at the X end plate to Y carriage
interface.**~~ Same degree of freedom, worse joint:

| | ~~Oversized block holes~~ | **Shim on the shelf** |
|---|---|---|
| What is loosened | the **four Y bearing blocks** - the interface carrying the whole gantry into the rails | nothing |
| How the adjustment is held | friction at a deliberately sloppy precision mount | a shim **in compression** under a bearing joint |
| Where the slop would live | 🔴 **designed into a precision mount**, and permanent | in a **shim**, which can be changed |

**The shelf was already a bearing joint** - this file records that it *"takes the vertical load
directly in bearing rather than through bolt shear, which is better anyway."* A shim belongs in a
joint like that; slop does not belong in the block mounting.

### The shim stock on hand, and what each step is worth

**1" wide aluminium strip**, which is **exactly the bar's 25.4 width** - so a strip cut to the bar's
60 mm length is a **full-face shim**, no overhang and no line contact. Over the beam's 1000 mm the
tilt is t/1000, so at a 100 mm tramming circle the correction is t/10:

| Shim | Tram correction per 100 mm |
|---|---|
| 0.03 | 0.003 |
| 0.05 | 0.005 |
| 0.08 | 0.008 |
| 0.10 | 0.010 |
| 0.13 | 0.013 |
| 0.15 | 0.015 |
| 0.18 | 0.018 |
| 0.23 | 0.023 |

✅ **Resolution is a non-issue.** The thinnest strip moves tram by **0.003 mm per 100 mm**, several
times finer than a good tram, and the set combines in roughly 0.03 steps. **The problem will be
measuring the error, not correcting it.**

🔴 **Range is capped at about 0.5 mm by the bolt clearance, not by the shim stack.** The beam's
four M8 run in **9 mm clearance holes**, giving ~0.5 mm of radial float before a bolt binds - about
**0.05 mm per 100 mm** of correctable roll. Far more than tramming needs, but it is the ceiling, and
it means the beam is deliberately **not** centred in those holes once shimmed. ⚠️ That float was
specified for a friction joint, not as an adjustment range; **confirm nothing else was relying on the
beam sitting centred.**

### Two practical points

🔴 **The shim needs clearance for the two vertical M8.** They pass up through the bar at **Y 15
and Y 45** into the extrusion's underside T-nuts, straight through the shim plane. **Slot the shim
open from one edge at both stations** so it slides in with those bolts loosened rather than removed -
a plain rectangle would mean pulling the beam off.

✅ **No creep concern.** The bearing area is 25.4 × 60, and the gantry's share per shelf puts the
shim at well under a tenth of a MPa. Aluminium shim extrudes under hundreds of times that.

**Order of work:** loosen the four M8, slide the shim in, re-torque. The adjustment is held by the
same friction joint that holds the beam, so nothing new carries load.

## ✅ The X end plates no longer need anything built in for roll

**This closes an item that had been left deliberately open.** The previous scheme asked for oversized
holes *"decided before they are drilled"* - a live constraint on a plate about to go to a one-shot
mill. **With roll taken at the shelf, the bearing block holes go close-fit as normal** and the plate
drawing is simpler, not more complex.

## ⚠️ Open: nod

Every face that produces nod points forward, and they all end up buried. Two candidates, in order:

1. **The spacer bolts.** The M5 × 35 heads are already counterbored into the Z plate's *front* face,
   so if they are reachable a jack screw beside each gives push-pull nod at an interface already in
   the design. Free if it fits.

   **The check, off the Z plate drawing:** a 120 mm clamp centred on a 154 mm plate covers **17 mm to
   137 mm**. So - **is the outer column of M5 counterbores within 17 mm of the plate edge?** (The
   6 mm clearance hole through the spacer itself is not the question - that is the layer underneath.)

   🔴 **Superseded - see below. Permanent access turns out not to be worth having.**
2. **A tram sub-plate** between the Z plate and the clamps. Both clamps bolt to the sub-plate so
   they stay coaxial. Pivot low, jack screw high, accessible from the front. **Costs about 13 mm of
   moment arm** (109 → ~122) and inserts an extra joint directly in the spindle load path.

## 🔴 Decided: tram at assembly. No sub-plate.

**An accessible row is not sufficient, which was an error in an earlier version of this file.** To
tilt the plate the gap must open *progressively* from the hinge - a little at the third row, more at
the second, most at the first. **Every bolt above the hinge has to be free.** A torqued bolt three
rows up does not permit the tilt; it just bends the plate. Permanent access would therefore need
**12 of the 16 reachable**, not 4.

Which reframes it: **at assembly all 16 are accessible, because the clamps are not on yet.** Tram
gets set once, with everything open. What permanent access would buy is only the ability to re-tram
*without pulling the spindle* - and that is eight M8 bolts and lifting the spindle out of two clamps,
maybe twenty minutes, on a job done perhaps twice in the machine's life.

**Paying 13 mm of permanent moment arm and an extra joint in the stiffest part of the machine to save
that is a bad trade.** Tram at assembly; accept that the spindle comes out if it is ever redone.

## Doing the tilt

**A row, not a column.** A complete column adjusts one side against the other, rotating the plate
about a vertical axis - yaw, which does nothing on a round spindle.

**Use the two outermost rows:** one as the hinge, the other as the adjuster. Angular resolution is
jack travel divided by row separation, so the widest pair gives the finest control. The two middle
rows are simply torqued once the tilt is set. **One accessible bolt per side at a common height** is
enough to jack the adjusting row evenly - all four are not needed.

## Never tram the two clamps against each other

They bore a round body and **must stay coaxial**. Shim one relative to the other and the spindle is
pinched in misaligned bores. A sub-plate carrying both is fine - they move together.

## What tramming actually buys

**Surfacing the spoilboard with the machine itself removes the table-to-spindle error in Z**, so tram
governs wall squareness and scallop depth rather than whether a surfaced face comes out flat.

---
