# End plates, Z risers, and the spindle mount

**Partly settled, 2026-09-29.** The beams themselves are finished - see
[`gantry-beam-joint.md`](gantry-beam-joint.md). This file covers what holds them up and what hangs
off them. Several dimensions are still **⚠️ Open** and are marked as such rather than guessed.

---

## Cutting forces: 500-1000 N, not 250

🔴 **Read this before using any deflection figure in this repo.** Much of the analysis on
2026-09-29 was done against an assumed **250 N** cutting force. That is a trim-router number and it
is wrong for this machine.

The spindle is **3 kW**. What that makes available:

| | Torque | 12 mm cutter | 6 mm cutter |
|---|---|---|---|
| 18 000 rpm | 1.6 N·m | ~265 N | ~530 N |
| 9 000 rpm | 3.2 N·m | ~530 N | ~1060 N |

**Design to 500-1000 N.** Every deflection figure scales linearly, so anything quoted at 250 N is
two to four times optimistic. Where the original estimate still stands, it is because the
conclusion was insensitive to the force - not because the force was right.

---

## Y beam support

Each Y beam is carried at its two ends only. It cannot be supported along its length: **the ball
screw runs underneath the beam**, which is also why the outboard plate below matters so much.

### End plate / Z riser

| | |
|---|---|
| Size | **3" W × 12" H × 1/2" thick** aluminium (76.2 × 304.8 × 12.7 mm) |
| To the beam | **8 × M8 × 35 mm flange bolts** - four per profile |
| To the torsion box | two M8, either into the plate's bottom edge **or** via L brackets |

**Those 8 bolts land in the ø6.65 lengthwise corner bores** - four per profile, which is exactly
what those bores exist for and the only way they are reachable. They are also what ties the two
stacked profiles together at each end, which the beam design assumes.

At 1/2" plate, an M8 × 35 leaves 22.3 mm in the extrusion; at 3/8" it leaves 25.5 mm.

### 🔴 Use the L brackets, not bolts into the plate edge

Two M8 bolts into the bottom edge of a plate, in a line, give **essentially no moment restraint
about the axis that matters** - the riser becomes a hinge at its base rather than a fixed
cantilever, which roughly quadruples its sway. The L bracket turns it into a real moment joint.

⚠️ **Open: size the bracket so the bracket is not the soft part.** The spec given was "3 inch long
15 × 1.5 L brackets", which has not been pinned down - if that is a 1.5 mm wall it is not enough.

### Span deflection: not a problem

End support was queried and checked rather than assumed. With the 1/4" joining plates on, vertical
**I = 3.37 × 10⁶ mm⁴**, and the gantry's share of load per beam gives about **0.022 mm** of sag.
Going to 3/8" plates would make it 0.019 mm - a 3 micron difference. **The span is fine end-supported.**

---

## The full-height outboard plate

⚠️ **Proposed 2026-09-29, not yet dimensioned. Nothing is ordered.**

Instead of stopping the back joining plate at the beam's 120 mm, **run it all the way down to the
torsion box** and bolt its bottom edge there. It then sits in the vertical plane containing the beam
axis, on the outboard face.

**This supersedes the gusset recommendation** carried in the project notes. Do not do both - a
gusset is a discrete triangle, this is a continuous one a metre long.

### What it does

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

### Two things to get right

⚠️ **Thermal.** A metre of aluminium bolted rigidly along its length to a wooden box: aluminium
moves ~23 µm/m/K, plywood barely moves. A 15 °C swing is roughly **0.35 mm of differential over the
length**. **Fix solid at the centre and slot the holes progressively toward the ends** - friction
still carries the shear and the plate can grow. Cheap now, miserable to retrofit.

⚠️ **Bolt face-to-face if the torsion box has a vertical side face.** Landing only on the box's top
surface through an angle reintroduces a bending element and gives back much of the gain.

**Y beams only.** The X gantry moves and has nothing to bolt down to, so X keeps the 120 mm back
plate. All of this added weight - roughly **14 lb per Y beam** at 1/4" - is therefore static.

---

## Plate and riser thicknesses

| Part | Thickness | Notes |
|---|---|---|
| Beam joining plates, all three axes | **1/4"** | settled - see [`gantry-beam-joint.md`](gantry-beam-joint.md) |
| Y end plates / Z risers | **1/2"** as designed | 3/8" is acceptable **only** if the full-height plate is built |
| **X gantry end plates** | **1/2"** | |

### 🔴 The riser thickness is coupled to the full-height plate

3/8" risers lose **58 %** of their weak-axis stiffness and only 25 % of their strong-axis. That is
acceptable **only because the full-height plate takes the fore-aft load in-plane**. Across the
machine, where the riser still works, 3/8" gives about 0.025 mm at 250 N - so **0.10 mm at 1000 N**,
which is now the dominant remaining compliance in the support structure.

**If the full-height plate is not built, go back to 1/2".** Do not let these two decisions get
separated in time.

The saving is only about 0.44 lb per riser, 1.76 lb across all four, and it is static weight. Thin
them for cost or machinability if you like; there is nothing to gain in weight.

### Why the X end plates are different

They carry the whole gantry into the Y carriage blocks, they take the full cutting moment as a
couple, **they move**, and they get no full-height plate to lean on. The Y reasoning does not
transfer. They are also the likeliest subject of the "riser plates far weaker along Y, gusset them"
warning in the project notes.

---

## The spindle and its mount

| | |
|---|---|
| Spindle | **80 mm, 3 kW, water-cooled**, with matching VFD |
| Clamps | **two 80 mm aluminium clamps**, one at each end of the spindle |
| Clamp size | 120 mm × 55 mm × 100 mm |
| Fixing | **4 × M8 × 80 mm socket head** per clamp, into the Z plate |

**Two clamps at either end is the right arrangement** and matches the dual-clamp recommendation
already carried in the project notes for a round-body 3 kW. Eight M8 holding the spindle is not
where this assembly will be soft.

### The offset from the X beam to the spindle centreline: 109 mm

🔴 **This is the moment arm.** It is the number that turns cutting force into gantry deflection, and
it was a placeholder in every calculation in this repo until now.

| From the X beam's front face | |
|---|---|
| Rails, bearing blocks and 5/8" spacers | 46.5 mm |
| Z carriage plate, 1/2" | 12.7 mm |
| Clamp mounting face to the 80 mm bore centre (half of 100 mm) | 50 mm |
| **To the spindle centreline** | **109 mm** |

**For gantry bending, add about 35 mm** to reach the beam's neutral axis - the combined centroid of
the stacked profiles plus their joining plates sits roughly that far behind the front face. So the
bending arm is **~144 mm**, and at 1000 N that is **~144 N·m** into the gantry.

⚠️ **Still missing: the vertical distance from the tool tip to the beam.** The 109 mm arm converts a
*vertical* cutting force into gantry torsion; the *vertical* offset converts a fore-aft force into
the same. Both are needed before the torsional case can be worked, and 8020 publish Ix and Iy for
`30-6060` but not J.

---

## The Z carriage

| | |
|---|---|
| Plate | **154 mm W × 407 mm H × 1/2"** aluminium |
| Rails | **HGR20 down both sides, mounted on the plate** |
| Screw | 1605, with **BK12 and BF12 bolted to the same plate** - so screw and motor are fixed relative to it |
| Spacers | **5/8" (15.875 mm) aluminium blocks on top of the bearing blocks** |
| Fixing | M5 × 30 socket head, 6 mm clearance through the spacers, counterbored into the plate |

Blocks, spacers and the ball nut housing form one assembly and present their faces at a common
height; plate, rails, screw and motor form the other. They are the two halves of the axis.

Dry-assembled in [`photos/z-carriage-assembly-end.jpg`](photos/z-carriage-assembly-end.jpg) and
[`photos/z-carriage-assembly-oblique.jpg`](photos/z-carriage-assembly-oblique.jpg).

### ⚠️ Open: which half moves?

Not yet established, and it changes the whole stack-up:

- **Plate fixed** to the X gantry, spindle carried on the spacer bars. Motor stays put, nut travels.
  This is the conventional arrangement and what the assembled hardware looks like.
- **Plate moves**, carrying rails, screw, motor and spindle, with the spacers bolted to the X
  gantry. Simpler, but the motor travels and the moving mass goes up.

The 109 mm offset above is unaffected either way.

### Use M5 × 35, not M5 × 30

Through a counterbore in a 12.7 mm plate - leaving about 7.7 mm of material under a 5 mm head - plus
the 15.875 mm spacer is roughly 23.6 mm of grip. An M5 × 30 leaves only about **6.4 mm in the
bearing block**, 1.3 diameters, with no margin if a counterbore runs deep. The blocks have the
thread depth for 35 mm.

---

### ⚠️ Open: the clamp mount geometry

- **Orientation - resolved.** The **100 mm dimension is front-to-back**, with the 80 mm bore centred
  in it leaving 10 mm of wall front and back; 55 mm is axial (vertical) and 120 mm wide, giving
  20 mm of wall either side of the bore. This follows from the "half of 100" term in the offset
  chain above and is consistent throughout.
- **Which way do the M8 × 80 bolts run?** Front-to-back through the clamp into the plate, or from
  behind through the plate into tapped holes in the clamp? With an 80 mm bolt against a 55 mm clamp
  dimension, one of those leaves 25 mm to land in the plate and the other does not fit at all.
- **Z plate thickness**, and whether it is tapped or through-bolted with nuts.

---

## ⚠️ Open items

- **Height from the top of the beam to the torsion box fixing line**, and whether the box has a
  **vertical face** to bolt against. These size the full-height plate; nothing else is missing.
- **The L bracket specification** - "15 × 1.5" has not been resolved.
- **The spindle clamp geometry**, three questions above.
- **Vertical distance from the tool tip to the beam**, the other half of the torsional case. The
  horizontal arm is settled at 109 mm.
- **Which half of the Z axis moves** - see above.
- **A torsion constant J for `30-6060`.** 8020 publish Ix and Iy but not J, so the gantry's
  torsional stiffness cannot yet be computed rather than estimated.
- **Riser plate orientation** for the X end plates, which governs whether the weak-axis warning
  applies as written.

## The measurement that would settle the 1/4" question

The X gantry plate thickness was chosen as 1/4" partly on the argument that **the Z assembly is the
largest compliance in the stack** and stiffening the beam past it buys nothing measurable. That is a
claim, not a measurement.

**Once the Z assembly is built: push on the spindle nose with a known force and put an indicator on
it.** That single number settles whether the beam plate should be 1/4" or 3/8", and the plate is
bolt-on precisely so the swap stays cheap.
