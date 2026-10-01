# The stiffness test: push the nose, find where it moves

**Not yet run.** This is the procedure for the test that
[`../machine/gantry-beam-joint.md`](../machine/gantry-beam-joint.md) and
[`../machine/end-plates-risers-and-spindle.md`](../machine/end-plates-risers-and-spindle.md) both call
for and neither specifies. Results go in the tables at the bottom and then **outrank every computed
figure in this repo**.

**What it settles:**

- 🔴 **Whether the X beam's joining plates should be 1/4" or 3/8".** That choice was made on the claim
  that the Z assembly is the largest compliance in the stack - **a claim, not a measurement**. The
  plates are bolt-on precisely so the swap stays cheap if this says otherwise.
- **The gantry's torsional stiffness**, which cannot be computed - 8020 publish Ix and Iy for the
  `30-6060` but not J.
- **Lost motion**, which matters more than stiffness and shows up nowhere else.

---

## The one rule that governs everything below

**The indicator stem points along the line of the push.** Stiffness is force divided by deflection
*along the force*. Push fore-aft, read fore-aft. A reading taken at 90° to the load is measuring a
different thing and cannot be divided into the force.

---

## Setup

| | |
|---|---|
| **Force** | **250 N (~56 lbf)**, applied with a luggage or fish scale. **Not 1000 N** - that is 225 lbf, hard to hold steady by hand and enough to unseat a joint or mark a part. Deflection is linear in force, so scale the answer |
| **Pull, don't push** | A spring scale in tension holds a steadier value than a hand |
| **Indicator base** | **A stand on the floor or bench. Never on the machine.** An indicator referenced to the gantry measures a difference, not a displacement |
| **Contact tip** | Ball or radius. On the round spindle body, contact **on its horizontal centreline** - off-centre on a cylinder gives a cosine error and the tip skates under load |
| **Z position** | Mid-travel, and **write down which**. The answer changes with Z extension |
| **X position** | **Mid-span of the gantry** for the beam numbers. Repeat near one end later if you want the end-plate contribution separated |

### 🔴 Energise the drives, or the reading is nonsense

With the steppers off, the Y ballscrew back-drives and the whole gantry simply rolls - you would be
measuring the screw, not the structure. **Power the drives so they hold**, and note that motor and
drive compliance is then part of every reading. Mechanically blocking the axis is cleaner if you can
rig it.

### Cycle it, and watch the return to zero

**Load, release, re-zero, repeat. Three cycles. Push both directions.**

⚠️ **Anything that does not come back to zero is LOST MOTION, not stiffness** - and it matters more.
A joint that slips 20 µm and stays slipped shows up in your parts; 20 µm of elastic deflection
largely does not. Record it separately. Do not average it away.

---

## Push 1 - fore-aft (Y). Do this one first.

**The softest path and the one this repo predicts worst.** It loads the X beam about its weak axis
(Iy ~1.71 × 10⁶ against Ix 3.37 × 10⁶ - see the beam file), plus beam torsion through the drop from
the beam down to the nose, plus the entire Z stack.

**Pull the spindle nose horizontally, toward the front of the machine.** Every indicator below reads
**fore-aft**, stem horizontal, pointing along the pull.

| # | Indicator contacts | Stem points | Reading is |
|---|---|---|---|
| **1** | **Spindle body, just below the lower clamp.** On the body's horizontal centreline | fore-aft | **Total** - beam, plates, carriage, Z stack, clamps. ⭐ **The primary number** |
| **2** | **Spindle body, as near the nose as you can reach.** Same centreline, same side as #1 | fore-aft | Pairs with #1 to give **tilt** - see below |
| **3** | **Z plate front face**, beside the lower clamp | fore-aft | Everything below the spindle and clamps |
| **4** | **X carriage plate front face** - exposed above or below the 175 mm Z plate | fore-aft | Everything below the Z assembly |
| **5** | **Beam front face beside the carriage** - the extrusion, or the 46 mm front joining plate | fore-aft | Beam and below |
| **6** | **X end plate, beside a Y bearing block** | fore-aft | Everything but the beam |

### The subtraction - this is the whole point

A single reading on the nose gives a **total**, and a total cannot tell you *where* the compliance
is. Each difference is one subassembly:

| Difference | Is the contribution of |
|---|---|
| 1 − 3 | Spindle body and the two clamps |
| 3 − 4 | **The Z assembly** - rails, blocks, spacers, ball nut |
| 4 − 5 | X carriage plate, X rails and blocks |
| **5 − 6** | 🔴 **The X beam itself. This is the 1/4" vs 3/8" answer** |
| 6 | End plates, Y blocks, Y beams, risers, torsion box |

⚠️ **Approximate, and knowingly so.** Points on different parts rotate as well as translate, so the
differences mix bending and rotation. This is good for finding **which term dominates**, which is the
question being asked. It is not a modal analysis.

### 🔴 Indicators 1 and 2 are the pair that matters most

A nose reading mixes two things that matter very differently:

- the assembly **translating** fore-aft - which is just translation, and
- the spindle **tipping**, because the force acts well below the beam.

**Tipping is what cuts a tapered wall.** A small angle at the clamps becomes a large error at the
tool: **0.001 rad with 50 mm of stickout is 0.05 mm at the cutting edge**, and a single nose reading
would never show it.

**Tilt angle = (reading 1 − reading 2) ÷ (vertical separation between them).** Measure and write down
that separation. Multiply the angle by your working tool stickout to get the error that actually
reaches the part.

---

## Push 2 - vertical (Z)

**This is the torsion measurement**, and torsion is the one number this repo cannot compute. The
spindle sits ~152 mm forward of the beam face, so a vertical force at the nose twists the beam about
its own axis.

**Hang a known weight from the nose** - easier and far more repeatable than pushing upward. All
indicators read **vertical**, stem up or down, contacting a horizontal surface: the nose shoulder,
or the clamp's underside.

| # | Indicator contacts | Reading is |
|---|---|---|
| 1 | Spindle nose shoulder, or collet nut bottom face | Total vertical |
| 2 | Z plate bottom edge | Below the spindle |
| 3 | **Beam front face, top edge** and **beam front face, bottom edge**, beside the carriage | ⭐ **The pair whose difference gives beam twist** |
| 4 | X end plate, at a Y block | Everything but the beam |

**Beam twist = (top reading − bottom reading) ÷ 120 mm**, the section height. That is the number
standing in for the unpublished J.

---

## Push 3 - along the beam (X)

**Lowest priority, skip it unless the first two leave a question.** It loads the X carriage, rails
and ballscrew and barely touches the beam. If the gantry racks in plan, push one end of the beam and
indicate the other instead - that is a different test.

---

## What to avoid

- ❌ **Do not take the primary reading off the collet nut.** It is a threaded part that can shift
  independently of everything you are trying to measure. Use the spindle body.
- ❌ **Do not indicate off a long tool in the collet** for the structural numbers - that adds collet
  and tool compliance, which is real but is not the structure you are deciding about. Worth a
  *separate* reading on a short ground stub if you want the tool-holding contribution.
- ❌ **Do not reference the indicator to any part of the machine.**
- ❌ **Do not average out a failure to return to zero.** Record it as lost motion.

---

## Results

**Push 1 - fore-aft, 250 N, Z at ______ mm, X at mid-span. Date: ______**

| # | Position | Out (µm) | Back (µm) | Residual (µm) |
|---|---|---|---|---|
| 1 | Spindle body below lower clamp | | | |
| 2 | Spindle body near nose | | | |
| 3 | Z plate front face | | | |
| 4 | X carriage plate front face | | | |
| 5 | Beam front face by carriage | | | |
| 6 | End plate at Y block | | | |

Vertical separation between indicators 1 and 2: ______ mm → tilt ______ rad
→ at ______ mm stickout, tool-tip error ______ mm

| Subassembly | Contribution (µm) | % of total |
|---|---|---|
| Spindle and clamps (1−3) | | |
| Z assembly (3−4) | | |
| X carriage and rails (4−5) | | |
| **X beam (5−6)** | | |
| Everything below the beam (6) | | |

**Push 2 - vertical, ______ N hung at the nose. Date: ______**

| # | Position | Out (µm) | Back (µm) | Residual (µm) |
|---|---|---|---|---|
| 1 | Nose shoulder | | | |
| 2 | Z plate bottom edge | | | |
| 3a | Beam front, top edge | | | |
| 3b | Beam front, bottom edge | | | |
| 4 | End plate at Y block | | | |

Beam twist = (3a − 3b) ÷ 120 mm = ______ rad

---

## Then what

| If the X beam term (5−6) is… | Then |
|---|---|
| **a small share of the total** | The 1/4" plate choice was right. Record it and stop - the claim it rested on is now measured |
| **comparable to the Z assembly** | 3/8" is worth the ~3 lb. The plates are bolt-on for exactly this |
| **dominant** | Something is wrong with the joint, not the plate thickness. Check the T-nut preload before buying anything |

⚠️ **Whatever this test says, go back and correct the computed figures in
[`../machine/gantry-beam-joint.md`](../machine/gantry-beam-joint.md).** They are estimates with a
crude beam model behind them, and a note that contradicts its own correction is worse than no note.
