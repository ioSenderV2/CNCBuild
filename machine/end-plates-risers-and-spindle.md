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

✅ **Both Y beams are built** as described here - stacked pairs, rails, screws, BK12/BF12, steppers
and all four risers. See [`photos/y-beam-end-plate-outer.jpg`](photos/y-beam-end-plate-outer.jpg) and
the three beside it. **The riser geometry below is as-built, not a proposal**, and the 8-bolt pattern
into the corner bores is proven hardware rather than a first attempt - which is why the X end plates
copy it.

Each Y beam is carried at its two ends only. It cannot be supported along its length: **the ball
screw runs underneath the beam**, which is also why the outboard plate below matters so much.

### End plate / Z riser

| | Rear (as built) | **Front (2026-09-30, to be remade)** |
|---|---|---|
| Size | 3" W × 12" H × 1/2" (76.2 × 304.8 × 12.7 mm) | **Tapered: 3" at the top, 9" at the base, 12" tall, 3/8" thick** |
| To the beam | **8 × M8 × 35 mm flange bolts** - four per profile | Same 8-bolt pattern, unchanged |
| To the torsion box | see the back panel under "The lateral fix" | **Two M8 through the front tongue at 50 and 200 mm**, plus bottom-edge bearing |

The riser lands on the **same top skin** the full-height plate bears on, just inboard of it - see
"How it lands on the torsion box" below. Both fixings share that surface, and the riser is the one
that sets the beam height and the two beams' coplanarity. So the riser is the datum of the pair and
the plate follows it.

**Those 8 bolts land in the ø6.65 lengthwise corner bores** - four per profile, which is exactly
what those bores exist for and the only way they are reachable.

At 1/2" plate, an M8 × 35 leaves 22.3 mm in the extrusion; at 3/8" it leaves 25.5 mm.

### 🔴 The holes are 9 mm, and that is deliberate

**As built the Y risers were laid out by hand, aimed at 8.2 mm, and reamed to 9 mm** to absorb
position error. That is the right dimension and should be specified on purpose everywhere this
pattern is used, including the X end plates:

- **A close fit is impossible in principle.** The bolts land in *extruded* corner bores, whose
  feature positions carry looser tolerance than anything drilled in plate. A perfect hole pattern
  would still not line up across eight bores in two profiles.
- **The joint does not want bearing.** M8 thread-forming into ø6.65 with ~22 mm of engagement in
  6063-T6 strips near 34 kN, so roughly 15 kN of preload per bolt is available - about **36 kN of
  friction across eight bolts**, against loads of one to two kN. The bolts never touch the hole walls.
- **The float is wanted** if the shelves are to set roll. A close fit would fight the adjustment.

⚠️ **Do not remake the Y risers on cosmetics.** The only question those holes had to answer is
whether the two Y beams ended up **parallel and coplanar** - that is what the X gantry rides on.
Measure that first; if it is within tolerance the holes did their job. Remaking calibrated hardware
also spends mill time already committed to plates that do not exist yet.

📌 **The two front plates are a deliberate exception**, and not on cosmetics - they change shape, see
below. They cost no mill time either: the existing plates were drilled at home with a **mag drill**,
and the 12 holes in a new plate are the same job. The **rear plates are not remade** - they carry the
steppers, the 35 mm shaft bores and BK12, and they stay exactly as they are.

---

## The lateral fix: tapered front fins, a full-width back panel

✅ **Decided 2026-09-30.** The full-height outboard plate took over the **fore-aft (Y)** support, and
the section above records it at ~670 000 N/mm in-plane against the risers' ~1 500. What it did not
touch is **across the machine (X)**, which is out-of-plane for that plate and therefore still carried
by the four risers alone, 3" wide, at the two ends only.

🔴 **Do not confuse this with the gusset recommendation the outboard plate superseded.** That one was
a triangle in the **Y-Z plane**, doing the job the outboard plate now does far better. This is the
**X-Z plane** - the riser's own face - and nothing covers it. Both are called "gussets" and they are
not the same part.

### Front: widen the riser in its own plane

Material is **added inboard**, toward the machine centre, tapering from the existing 3" at the top to
**9" at the base**. It is not a bolt-on outrigger; it is the plate's own outline, which is why the
plates are remade rather than scabbed.

Lateral stiffness goes as **width cubed**, and a taper puts the section where the moment is. Treating
the riser as a cantilever over the ~185 mm between box top and beam underside:

| Base width, at the same thickness | Stiffness vs the 3" prismatic riser |
|---|---|
| 6" | ~4.9× |
| 8" | ~9.6× |
| **9" - chosen** | **~12.7×** |
| 12" | ~25× |

📌 **At 3/8" the chosen figure is ~9.5×, not 12.7×.** Stiffness scales linearly with thickness, and
the front plates are 3/8" while the as-built risers they are compared against are 1/2". Use **9.5×**
as the real number; the table above is the shape-only effect.

⚠️ **Calculated, not measured.** Tapered cantilever, width varying linearly, load at the top, fixed
base. The fixed-base assumption is doing real work - see the bolt note below.

### Cut two from one 12" square, and reference off the factory edges

✅ **Decided 2026-09-30.** One **12" square of 3/8" aluminium**, cut once on a line from **3" in at the
top to 9" in at the bottom**, yields **both front plates with zero waste** - each half is 3" at the top,
9" at the base, 12" tall.

The two halves are **rotations of each other, not mirrors**: turn one 180° and the outline is
identical. Left and right are obtained by flipping one plate over, which costs nothing on a
through-drilled flat plate.

🔴 **Lay both hole patterns out from the factory vertical edge and the factory top edge.** Each half
keeps one uncut vertical edge, and that is the **outboard** edge, with the taper facing inboard. Done
that way the bandsaw kerf never enters the layout - it only shortens one piece's taper by about a
millimetre. Laid out from the **cut** edge instead, the kerf becomes a ~1.5 mm offset built into one
plate's bolt pattern, and that pattern has to line up with formed threads in the beam.

⚠️ **Flipping one plate over swaps which face is outboard.** Harmless for through holes; check it
before spot-facing or counterboring anything on one face only.

📌 **3/8" here is consistent with "The 3/8" question is closed" below, not a contradiction of it.**
That section's condition was that 3/8" is acceptable **only if the full-height plate takes the
fore-aft load in-plane** - which is exactly what was settled. Two consequences to keep: M8 × 35 leaves
**25.5 mm** in the extrusion rather than 22.3 mm, and **front and rear plates now differ in thickness
on purpose.**

Cost is about **+1.5 lb per front plate**, static. Two things it does *not* cost:

- **No bed area.** The fin is a 12.7 mm slice in the riser's own plane, not a wedge intruding into the
  work volume.
- **No travel.** It lives in the plane of the end plate, which the gantry already cannot reach past.

### The second gain is bolt spacing, and it is the bigger one

The project note's rule is that moment capacity comes from **bolt spacing, not bolt count** - two M8
200 mm apart beat six clustered in 50 mm. A 3" foot cannot give you that spacing at all, which is why
this file previously had to reach for L brackets to avoid a hinge at the base. **A 9" base gives the
spacing directly.**

**Fixing: two M8 through the front tongue at 50 mm and 200 mm** from the outboard edge, plus the
plate's bottom edge **bearing on the top skin** the way the outboard plate does.

| Direction | What takes it |
|---|---|
| Vertical | **Bearing** - fin bottom edge on the top skin |
| Lateral moment | The two through-bolts as a **150 mm couple** |

🔴 **The bolts are now the soft part, not the plate.** A 12.7× stiffer fin only pays if the base is
genuinely fixed, and the reaction at those bolts is vertical load bearing into plywood. The project
note's standing warning is that **plywood creeps in compression** with nothing to tell you. Use a
steel backing strip or large fender washers on both faces here, not plain washers.

⚠️ **Blocking under the 229 mm base** has to be in the rib layout - the bottom-edge bearing is only
worth having if it lands on structure rather than on skin spanning between grid members. The box is
built last, so this is free, but it must be decided before the skins are cut.

### Back: one full-width panel, added rather than remade

The two rear risers are joined by a **panel spanning the full machine width**, in the same plane,
turning the rear face from a portal frame with two bending legs into a shear panel.

- **It costs no travel** - the gantry stops well forward of the rear plate plane, and the spindle sits
  ~109 mm ahead of the carriage plate.
- **Bonus: a rear chip fence** the width of the machine.
- **It is an added panel, not a replacement for the rear plates.** Those carry the steppers, the 35 mm
  shaft bores and BK12; a monolithic replacement would put two 8-bolt patterns, two bores, two stepper
  patterns and two BK12 patterns on one 1.2 m part, cut on a 4' × 1' manual-XY mill on a one-shot
  trip, and would become the coplanarity datum before that datum has been measured.

⚠️ **The back panel does not cover the front.** The load path from a gantry parked at min-Y back to
that panel runs sideways through the Y beams - their 60 mm dimension, not their 120 mm - and the
outboard plates contribute nothing laterally, that being their out-of-plane direction. So the front
fins are carrying a front-position gantry largely alone. That is why the front is taken to 9" rather
than left minimal. *(Reasoning from the 60-vs-120 proportions; the 30-6060 section about the vertical
axis has not been looked up.)*

### The tongues that back both

Both fixings need a bearing face, so **the box's doubled outer wall now runs all four sides** - the
outer lamination standing **61 mm proud** front and back exactly as it does left and right. See
[`torsion-box.md`](torsion-box.md), which carries the consequences: every ledge goes to 38 mm, front
corner tenons become **48 × 48**, the back centre tenon **86 × 48**, and the back post's shoulder
roughly doubles.

✅ **The front corner convergence is resolved: the front and back tongues run long and lap the side
tongues' ends.** Each runs the full width and extends **19 mm past the front post tenon**, covering the
end grain of the side tongue in a butt joint. That makes the front and back tongues the continuous
members and the side tongues the ones that die into them.

It also settles what was the awkward part. Everything at that corner ends in one plane - the **front
wall's inner web front face** - and the front tongue simply runs across all of it:

| Member | Where it stops |
|---|---|
| Full-height outboard plate | Ends at that plane; the front tongue sits in front of its end edge |
| Side tongue (curb) | Ends at that plane; its end grain is covered by the front tongue |
| Front riser | Bears against the **back face** of the front tongue, bolted through it |

So **nothing needs notching or mitring.** The one thing to keep in mind is that the corner butt joint
is plywood end grain onto face, which is a weak glue joint - it is not load path here (the fins' bolts
land in the front tongue's face, and that tongue is glued to the inner web over its whole area), but
do not let the corner carry anything on purpose.

### 🔴 Open: how far past the riser plane the spindle reaches

**Confirmed by the user, 2026-09-30: the spindle with its overhang does pass the plane of the front Z
riser.** So this is a real interference case, not a hypothetical, and the widened fins make the region
it passes through much larger.

The mechanism: the spindle sits ~152 mm forward of the X beam's front face, so as the gantry runs to
min-Y the spindle **crosses the riser plane and ends up in front of it.** The fin occupies that plane,
and its added material is a triangle whose top edge slopes from the top of the plate at 3" inboard down
to the bottom of the plate at 9" inboard. **Interference is therefore a corner-of-the-envelope case:
low Z, minimum Y, and X near either beam.** The existing 3" risers barely reach inboard of the beam, so
this problem is largely created by the widening.

**To determine it, four numbers are needed and only one is in this file:**

| Number | Status |
|---|---|
| Spindle centreline forward of the X beam face | ✅ ~152 mm, settled above |
| **X beam centreline down to the spindle nose, Z fully retracted**, plus Z travel | ⚠️ already an open item below - this is now a second reason it is needed |
| **The forward-most point of the moving assembly** - spindle body is ø80 so centreline +40 mm, but the clamps or drag chain may reach further | ⚠️ not measured |
| **The gantry's forward hard stop** relative to the riser plane | ⚠️ not measured |

Three ways out, in order of preference:

1. **It clears with Z retracted** - then this is a soft-limit rule, not a geometry problem: no low Z in
   the two front corners.
2. **Shape the fin's top edge to clear** rather than cutting a straight taper. Costs stiffness where
   the fin is already thinnest, so it is cheap.
3. **Reduce the base below 9"** - the last resort, since the whole point was the base width.

🔴 **Settle this before the plate is cut.** The taper line is one bandsaw pass and cannot be put back.

### Span deflection: not a problem

End support was queried and checked rather than assumed. With the 1/4" joining plates on, vertical
**I = 3.37 × 10⁶ mm⁴**, and the gantry's share of load per beam gives about **0.022 mm** of sag.
Going to 3/8" plates would make it 0.019 mm - a 3 micron difference. **The span is fine end-supported.**

---

## The full-height outboard plate

✅ **Decided 2026-09-29. One per Y beam, 12" × 1000 mm × 1/4" aluminium**, replacing the existing
12" × 6" × 1/4" gusset - the dimensions rotate, from 12" along the beam to 12" tall and a metre long.

At 12" it reaches from the beam down to the torsion box on a 12" riser, which is what makes it the
continuous shear web rather than just a longer gusset. **A 6" plate would have spanned the beam plus
32 mm and stopped 150 mm short of the box, doing none of what follows.** Same face, same length, same
thickness - the height is the whole difference.

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

### Two things to get right - both now resolved

✅ **Thermal - closed 2026-09-30, no slotting needed.** A metre of aluminium bolted along its length
to a wooden box: aluminium moves ~23 µm/m/K, plywood barely moves, so a 15 °C swing is roughly
**0.35 mm of differential over the length**. An earlier draft called for fixing solid at the centre and
slotting the holes progressively toward the ends. **That is unnecessary here.** The bolts are **9 mm
clearance on M8**, which is 1 mm of float per hole - nearly three times the whole differential - and
the shop is climate controlled with Baltic birch skins. The 9 mm hole *is* the slot. This follows the
precedent set on the Y risers, reamed to 9 mm for the same reason.

The figure is kept because it is the one that had to be beaten, not because it is still a worry. Note
also that for plywood the larger term is **moisture, not temperature**; it is dismissed here on the
climate-controlled shop, not on the thermal arithmetic.

✅ **The box has a vertical face, because one is being built for it** - see the next section. The
warning this bullet used to carry stands, and it is the reason the interface took the shape it did:
landing only on the box's top surface through an angle would reintroduce a bending element and give
back much of the gain.

**Y beams only.** The X gantry moves and has nothing to bolt down to, so X keeps the 120 mm back
plate. All of this added weight - roughly **14 lb per Y beam** at 1/4" - is therefore static.

### How it lands on the torsion box

✅ **Decided 2026-09-30.** This is the plate's bottom fixing, and it is what closes the "does the
box have a vertical face" question above: **one is built into the box for the purpose.**

The box is **19 mm Baltic birch skins top and bottom over a grid of 19 mm strips 100 mm high**, so
138 mm deep overall. Two changes make it the plate's foundation:

1. **The box is widened to the machine's width at the plates**, so its top skin reaches out far enough
   that the plates stand on it rather than hanging alongside it.
2. **Each outer wall is two 19 mm laminations instead of one.** The inner one is an ordinary 100 mm web
   between the skins. The outer one is **180 mm tall, standing on the bottom skin's top face**, glued
   to the inner web's outer face and to the edge of the top skin. It spans the 100 mm web plus the
   19 mm top skin and so **stands 61 mm proud** of the top surface as a **curb, outboard of the plate.**

The top skin's outer edge terminates at the inner web's outer face, which is also the curb's inner
face. The plate drops into the channel between the two, and since the plate is 6.35 mm thick it
occupies **the outer 6.35 mm of the 19 mm web** - so its bottom edge bears **directly over the wall**,
never on skin spanning between grid members.

#### Cross-section at the outer wall, inboard to outboard

| Member | Thickness | Vertical extent |
|---|---|---|
| Inner web of the outer wall | 19 mm | Between the skins, 100 mm high |
| *of which the outer 6.35 mm carries the plate's bottom edge* | | *bearing face is the top skin's top surface* |
| The full-height plate | 6.35 mm (1/4") | Up to the Y beam - 12", 305 mm tall |
| Outer lamination, the curb | 19 mm | 180 mm tall, **61 mm proud** of the top skin |

#### The plate is captured on three sides

| Direction | What takes it |
|---|---|
| Vertical | **Bearing** - plate bottom edge on the top skin, directly over the wall |
| Outboard, across the machine | **Bearing** - plate outer face against the curb's inner face |
| Inboard | **Bolt tension** |

The consequence worth noticing: **the bolts are retention, not the load path.** Vertical and outboard
loads both arrive in bearing on plywood faces, which plywood is good at. So the bolt row is sized by
convenience rather than by strength - an estimated ~500 N of static vertical per Y beam shared across
eleven M8 is orders of magnitude clear, and this joint's real limits are geometric, not structural.

#### The bolt row

| | |
|---|---|
| Fastener | **M8, one every 100 mm** - eleven per beam over the 1000 mm |
| Direction | From **outboard**: washer, curb, plate, **M8 locknut** on the inboard face |
| Holes | **9 mm clearance** in curb and plate both - see the thermal bullet above |
| Why not tapped into the plate | M8 into 6.35 mm of aluminium is about **5 threads, 0.8 × D**, where aluminium wants 1.5-2 × D. It would strip before the bolt came near yield and could never be properly preloaded. The inboard face is open air - the beam is up on 12" risers - so a through-bolt costs nothing and was always available |

Glue area is not a constraint: roughly **100 000 mm²** of face-to-face plywood per wall over the box
depth, plus the top skin's edge.

#### What this buys beyond a fixing: restraint along the whole metre

Loads **along Y** lie in the plate's plane and were always handled. Loads **across the machine** -
gantry acceleration, cutting force in X, the two Y beams wanting to spread - are out-of-plane for the
plate, and the previous answer was that the risers take them edge-on, which means **at the two ends
only.** The curb now takes that same load in plywood face bearing over the **full 1000 mm.**

That is a structural gain rather than a side effect of the assembly method, and it is part of why the
interface is shaped this way instead of bolted flat to the box's top surface.

#### Two things to get right when cutting

⚠️ **Bias the top skin wide, never narrow.** The skin's width sets the distance between the two
curbs' inner faces, and a curb is a hard bearing face with no float - the 9 mm holes let the *bolt*
move, not the bearing. A millimetre or two **too wide** leaves a gap a shim fixes in minutes. **Too
narrow and the plates will not drop between the curbs at all**, and planing a glued-up skin edge in
place is a miserable job. The same cost at cut time, wildly different cost if you are out.

⚠️ **The plate-to-curb seam is a swarf trap** running the length of the machine - the plate is
the chip barrier and the curb sits outboard of it. Either seal the top of the seam or leave it
deliberately open at both ends so it can be blown through.

#### 🔴 The machine is the datum, not the box - so the box is built last

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

### The magnetic encoder tape runs on the front plate

The **10 mm magnetic tape** for the AS5311 sensors runs on the face of the **46 mm front plate**,
centred in the gap between its two rows of seven M8 flange bolts. Two rows at ±15 mm with 17.3 mm
flange heads leaves about **12.7 mm clear**, so a 10 mm tape sits with roughly 1 mm each side.

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

**Only the front plates need this**, since that is where the tape runs: 14 per plate, so 28 for the
two Y beams, plus 14 more if the X beam's front plate carries tape the same way.

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

## Plate and riser thicknesses

| Part | Thickness | Notes |
|---|---|---|
| Beam joining plates, all three axes | **1/4"** | settled - see [`gantry-beam-joint.md`](gantry-beam-joint.md) |
| Y end plates / Z risers | **1/2"** | ✅ built |
| **X gantry end plates** | **1/2"** | specified above - two identical 154 mm plates |

### The 3/8" question is closed - the Y risers are built at 1/2"

Recorded because the reasoning still applies to anything cut later. 3/8" loses **58 %** of the
weak-axis stiffness against only 25 % of the strong-axis, which would have been acceptable **only
if the full-height plate took the fore-aft load in-plane**. The Y risers went to 1/2" and are made,
so the coupling never had to be managed.

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

**From the X carriage plate's front face:**

| | |
|---|---|
| Z rails, bearing blocks and 5/8" spacers | 46.5 mm |
| Z plate, 1/2" | 12.7 mm |
| Clamp mounting face to the 80 mm bore centre (half of 100 mm) | 50 mm |
| **To the spindle centreline** | **109 mm** |

⚠️ **That reference is the carriage plate, not the beam.** The X carriage plate is itself bolted to
the X-axis bearing blocks, so from the **X beam's front face** add the X rail-and-block stack
(30 mm, measured) and the carriage plate (12.7 mm):

| | |
|---|---|
| X beam front face to spindle centreline | **~152 mm** |
| X beam **neutral axis** to spindle centreline (add ~35 mm) | **~187 mm** |

**~187 mm is the arm for gantry bending**, and at 1000 N that is **~187 N·m**. ⚠️ Confirm the
reference before this is used for anything - the 109 mm and the 152 mm differ by a whole rail-block-
plate stack and are easy to interchange.

⚠️ **Still missing: the vertical arm.** The 109 mm converts a *vertical* cutting force into gantry
torsion; a *vertical* offset converts a fore-aft force into the same. That vertical figure is **the X
beam centreline down to the spindle nose with Z retracted, plus Z travel** - not "tool tip", which
moves with Z position, tool length and stickout and is not a machine dimension. Even with it, 8020
publish Ix and Iy for `30-6060` but not J, so any torsional number stays an estimate.

---

## The Z carriage

| | |
|---|---|
| Plate | **154 mm W × 407 mm H × 1/2"** aluminium |
| Rails | **HGR20, 400 mm, down both sides, mounted on the plate** |
| Screw | 1605, with **BK12 and BF12 bolted to the same plate** - so screw and motor are fixed relative to it |
| Spacers | **two 6" lengths of 5/8" (15.875 mm) aluminium bar**, cut from one 12" piece, sandwiched between the bearing blocks and the Z plate. Each spans two bearing blocks |
| Bolt count | **16 × M5 × 35** - 8 per spacer, 4 per bearing block |
| Fixing | **one M5 per hole does the whole stack** - counterbored in the Z plate, through a 6 mm clearance hole in the spacer, into the bearing block's tapped M5 |

Blocks, spacers and the ball nut housing form one assembly and present their faces at a common
height; plate, rails, screw and motor form the other. They are the two halves of the axis.

Dry-assembled in [`photos/z-carriage-assembly-end.jpg`](photos/z-carriage-assembly-end.jpg) and
[`photos/z-carriage-assembly-oblique.jpg`](photos/z-carriage-assembly-oblique.jpg).

### 🔴 Open: the Z plate height waits on the spindle

**The spindle arrives 2026-09-30 and its body sets the plate.** Clamp separation, and therefore plate
height, cannot be settled until it is in hand - anything decided before then rests on a guessed body
length.

**Measure on arrival:**

- 🔴 **Usable parallel body length** - not the overall figure, but the clean 80 mm cylinder available
  *between obstructions*. A stepped nose at the bottom and a cable gland or connector boss at the top
  usually leave considerably less than the datasheet length. **This is what places the clamps.**
- **Body diameter**, confirmed over the whole clamping length rather than nominally
- **Where the water fittings and cable exit sit** - they constrain clamp placement and set the drag
  chain routing
- **Nose to collet nut face** - the fixed part of the torsional arm
- **Weight**, for the moving mass

#### The overhang below the spacer blocks is cubed

Anything below the spacers is unsupported plate, and putting the lower clamp there inserts a
cantilever right where it hurts. The lower clamp also carries **more** than the cutting force, since
the two clamps react the tool's overhang as a couple - roughly 1.5 to 1.8×.

| Overhang | Deflection at the lower clamp, peak load |
|---|---|
| 2" (50.8 mm) | ~0.03-0.04 mm |
| **1" (25.4 mm)** | **~0.004-0.005 mm** |

**A factor of eight for one inch.** If the clamps need more separation than the supported region
offers, **spread the bearing blocks and lengthen the spacers** rather than hanging plate off the
bottom - that widens the supported base with no cantilever at all. The cost is Z travel, which is the
honest trade: **spend travel, not stiffness.**

#### The travel budget

Rails are **400 mm**, blocks **77 mm**, so with the blocks butted the usable travel is **246 mm**.

⚠️ **A measurement of 272 mm was taken and discarded** - it was the *ball nut's* travel, which
overruns the rails. Recorded because the number is real and it matters: see the hazard below.

#### 🔴 The screw outruns the rails by ~26 mm, upward, with no hard stop

Going down, the nut bottoms on BF12 - a mechanical stop. **Going up, the blocks run off the rail end
before the nut reaches BK12.** Nothing catches it.

That is the failure this repo's standing rule exists for. A soft limit is a configured value, and if
it is ever wrong, missing or bypassed - a homing move, a lost setting, a restored config - the
machine drives the carriage off the rail and drops the Z assembly.

✅ **A physical top stop is designed:** a **6" × 1" × 1/4" plate** bolted over the top of the X
carriage plate, overhanging the rail ends. The **proximity sensor is at the top of Z**; if the axis
runs past it, the rising bearing block meets that plate.

**The failure being guarded against is not the crash - it is losing the ball train.** Run a block off
a rail end and the balls escape the recirculation path and the block is scrap. The design allows the
block **7 mm past the rail end** before contact, against the **first 10 mm of the block carrying no
balls**.

✅ **Measured with calipers: 10 mm** from the end of the block to the first exposed bearing. So the
7 mm of overrun has **3 mm to spare** and the design stands - **no rail shift needed, the carriage
plate can be drilled as laid out.**

📌 That 3 mm is nominal. Rail length, plate height and the flush-mount datum each carry a little
tolerance, so the real figure could land between roughly 1.5 and 4 mm. Positive in every case, and
the stop only fires if the control has already failed - but it is why the nominal should not go any
tighter.

📌 **Not to be confused with the plastic arbor.** The plastic strips supplied with the blocks are a
**transfer and storage tool** - slide a block off the rail onto the strip to store it, and it is
pushed out again as the block goes back on. They do nothing during an overrun in service.

An **integral retainer** - a wire or cage inside the block holding the balls captive off the rail -
is a separate optional feature on some series, usually flagged in the part number rather than
visible. Worth a glance if the part number is to hand, but it changes nothing: **the measured 10 mm
is the protection either way.**

Keep the arbors. Re-spacing blocks for clamp alignment needs no removal - unbolt the spacers, slide
the blocks along the rail - but nothing else substitutes the day one is needed.

**The 7 mm is forced, not chosen:** the X carriage plate is 16" (407 mm), the rail is 400 mm mounted
flush with the plate's bottom edge, and the stop sits on the top edge - leaving 7 mm. There is
nowhere lower for the stop to go.

📌 **But the rail position is still free, and only until the plate is drilled.** Mounting the rail
**3 mm up from the bottom edge instead of flush** makes the top gap 4 mm. It costs nothing:

- **Travel is unchanged** - 246 mm is rail length minus block span, wherever the rail sits.
- **The bottom end does not care** - BF12 stops the nut before the lower blocks near the rail's lower
  end, so nothing is given up; if anything it gains 3 mm.
- The travel band shifts up 3 mm, absorbed by mounting the spindle 3 mm lower if it matters.

✅ **Measured at 10 mm, so this lever was not needed** - kept because the reasoning applies to any
rail-and-plate pairing done later, and because the option genuinely expires when the plate is
drilled.

The block is hardened steel and the plate 1/4" aluminium, so **the plate is sacrificial** - correct
for something that should fire once or twice in the machine's life. **Keep the overhang short** so
impact loads the bolts in shear rather than bending a cantilevered lip.

The bottom end needs nothing: the nut bottoms on BF12 before the rails run out, so one stop at the
top covers the whole ~26 mm of screw overrun.

#### 🔴 Travel + clamp separation ≈ 323 mm

Align **clamp centres over block centres** - then the load goes straight into the blocks and the
plate does no bending at all. The block span is then clamp separation plus 77 mm, so:

| Clamp separation | Z travel |
|---|---|
| 77 mm (blocks butted) | 246 mm |
| 120 mm | 203 mm |
| 150 mm | 173 mm |
| 200 mm | 123 mm |

Less end clearances. **Every millimetre of clamp separation costs a millimetre of
travel.** The spindle's usable body length says how far the clamps *can* spread; this line says what
it costs.

**Two things soften it:**

- **Clamps need not sit exactly over the blocks.** Slightly outside buys travel back for a small
  cantilever, and the cube law makes small overhangs genuinely cheap - 20 mm costs about an eighth of
  what 40 mm does. A curve to slide along, not a hard constraint.
- **Wider is not purely better.** Clamp couple force goes as one over the separation, so spreading
  reduces load on plate and blocks - but that path is already stiff. **Plate bending is the softer
  thing, so alignment matters more than spread.**

#### ✅ Left-right alignment is settled, and it lands well

Measured: **clamp bolt holes 100 mm apart**, **spacer centrelines 115 mm apart**. So each clamp bolt
sits at ±50 mm from the plate centre, **7.5 mm inboard of its spacer's centreline** - over the
spacer, and therefore over the bearing block.

If the block's M5 pattern is the usual ±16 mm from the rail centreline, those columns fall at about
41.5 mm and 73.5 mm from the plate centre, so **the clamp bolt at 50 mm is bracketed between them**
rather than cantilevered outside. Load goes bolt → plate → spacer → block with the plate barely
working. ⚠️ Confirm that ±16 mm against the actual blocks - it is the one figure here not read off
the parts.

📌 **This is the left-right axis only.** Vertical alignment - clamp centres against block centres up
the rail - is the open one, and the only one that costs travel.

**There is room to manoeuvre** - a router of this size wants perhaps 150-200 mm, against ~246 mm
available. So work in this order rather than iterating:

1. **Set the Z travel floor first** and treat it as hard - material thickness plus tool length plus
   clearance over workholding. 🔴 **This is the one that gets quietly eroded** while optimising the
   other end, and it is the one noticed every day.
2. **Measure the spindle's usable body length** → that sets clamp separation.
3. **Spread the blocks until the supported span covers the clamps.** Aim for **zero overhang**, not
   one inch - the cube law makes an inch cheap, not free.
4. **Check the remaining travel against step 1.**
5. **Cut spacers to suit** (8" rather than 6", if spread that far).

### Which half moves - settled

| Fixed | Moving |
|---|---|
| **X carriage plate** (the blue one), bolted to the X-axis bearing blocks | Z bearing blocks |
| HGR20 rails, mounted on it | 5/8" spacer blocks |
| 1605 screw, BK12 + motor, BF12 | ball nut housing |
| | **Z plate**, bolted to both the spacers and the nut housing, carrying the spindle |

The motor stays put and only the carriage travels. The Z plate picks up **two** interfaces - the
spacer blocks and the ball nut housing - which is what makes the shim below matter.

**The blue is layout dye, not a finish.** The X carriage plate is plain 1/2" aluminium sprayed for
scribing; **30 holes** to lay out on it.

| X carriage plate | |
|---|---|
| Size | **154 mm W × 407 mm H × 1/2"** |
| Width | ✅ **154 mm, confirmed 2026-09-30** - the same width as the X gantry end plates and the Z plate |

📌 **154 mm recurs across three plates and it is not a coincidence.** The X end plate's 154 is set by
two HGH20 blocks end to end with 2-3 mm between; the Z plate and this plate inherit it. Worth knowing
before anyone "tidies" one of them to a different number - changing it here changes what rides the Y
rails.

### 🔴 The ball nut sits 1 mm below the spacer blocks - shim it with a plate, not washers

Measured: the spacer blocks stand **1 mm higher** than the ball nut housing, so the Z plate cannot
bear on both without something in between.

**Use a full-face shim cut to the housing footprint**, or skim 1 mm off the spacer blocks and have
no shim at all. **Not washers.** The ball nut is the one joint here that must not be pulled out of
alignment: washers bear at four points, and as the bolts come down the housing tilts to whatever
those points dictate. That tilt becomes a side load on the screw - binding, uneven wear, and lost
motion that reads like backlash.

**Assembly order: rails and spacers first, nut housing last.** The rails define the geometry; the
nut should follow the screw rather than be forced into position by its own bolts. Leave its four
bolts finger-tight, run the carriage through full travel, then torque them.

⚠️ Measure the 1 mm rather than assuming it is exactly 1.00 - shim stock comes in 0.5, 0.8 and 1.0.

### 🔴 Match the two spacers to each other before anything else

The spacers carry **no fasteners of their own** - they are compression members, clamped by the same
M5 that runs from the Z plate into the bearing block. Two consequences:

- **Their faces set the Z plate's plane relative to the rails.** A few hundredths of difference
  between the left and right spacer twists the plate and preloads all four bearing blocks against
  each other permanently.

  ✅ **Largely handled by how they were made:** both are halves of a single 12" bar, so the 5/8" is
  the as-supplied bar dimension on both, untouched - the cut sets length only. Still **mic both at
  both ends** to confirm, since flat bar carries a thickness tolerance along its length, but this is
  a check rather than a problem. The pair sets the geometry; the nut housing shim only has to avoid
  fighting it.
- **They locate nothing.** A 6 mm hole on an M5 bolt is 0.5 mm of radial float per side, so the
  spacer sits wherever it is put. Geometry comes from the blocks and the plate, which is correct -
  just do not expect the spacer to square anything up.

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

## The X gantry end plates

**Two identical plates, 1/2" aluminium, 154 mm wide.** They carry the X beam, ride the Y rails on
four bearing blocks, and mount the X ball screw supports and stepper.

**154 mm is set by the bearing blocks** - two HGH20 blocks end to end with 2-3 mm between. Anything
wider eats usable Y travel at both ends.

### Vertical stack-up, from the top of the Y beam

| From the Y beam top | |
|---|---|
| Four M8 into the **top extrusion's** corner bores, **9 mm clearance** - start just above the Y beam top | 0 |
| Top of the extrusion | **+60 mm** |
| Top of the ball screw support block mount | **+80 mm** |
| Top of the stepper mount, motor on the outside, shaft through a **35 mm hole** | **+140 mm** |

**The bottom extrusion is not bolted to the plate at all.** It sits alongside the Y beam, carried on
a shelf - see below. This is the half-overlap: only the top extrusion is above the Y beam, which is
what keeps the whole machine low.

### 🔴 Why the four bolts are above the Y beam top

Their heads land on the plate's **outer** face - the same face the Y bearing blocks bolt to, where
four blocks occupy a 2 × 2 grid across the full 154 mm. Putting the top extrusion entirely above the
Y beam puts those heads in clear air.

Raising the beam further to expose all eight would raise the whole Z assembly, meaning more Z
extension for the same tool height - and Z extension is the softest direction in the machine. **Do
not raise it for wrench access.**

### Why four bolts is enough

The joining plates tie the two profiles along the whole metre, with T-nuts to within 50 mm of each
end, so the bottom extrusion's load reaches the end plate **through the top extrusion** rather than
needing its own path.

| | Worst bolt at 1000 N |
|---|---|
| All 8, over 60 × 120 | ~830 N |
| **Top 4 only, over 60 × 60** | **~1640 N** |

Against roughly 4800 N of friction capacity per M8 at full preload - about **3× margin**. The shelf
takes the vertical load directly in bearing rather than through bolt shear, which is better anyway.

### Position in Y: as far back as it will go

Rear bolt pair **25 mm from the plate's back edge**, putting the beam's back face 10 mm in. The
6.35 mm back joining plate takes most of that, leaving 3.65 mm, and the nearest joining-plate T-nut
is 50 mm inboard so no bolt head comes near.

Back-mounting matters because the forward-hanging mass acts at an arm from the **block group's
centroid** at Y 77:

| Beam position | Arm | Load per block pair |
|---|---|---|
| **Back (chosen)** | 102 mm | **1.32 × F** |
| Centred | 139 mm | 1.8 × F |

**Roughly a quarter less**, for free - the block travel sets the envelope either way.

### The plate is tall, and the beam is what makes that safe

A 12.7 mm plate cantilevering 80 mm with screw thrust on it would be a problem. It is not one,
because the X beam is bolted across the bottom 60 mm, so the support block sits only **20 mm beyond
the bracing**:

| | At 1000 N |
|---|---|
| Unbraced over the full 80 mm | 0.094 mm |
| **Braced by the beam, 20 mm effective** | **0.0015 mm** |

A factor of 64. **Keep the support block tight down onto the extrusion** rather than floating it
higher up the plate - that bracing is doing all the work. The stepper at 140 mm is hanging mass only,
no thrust.

### The shelf

**A 3" length of 1" square aluminium bar** per plate - 25.4 × 25.4 × 76.2 mm - spanning the beam's
60 mm depth plus the back plate, with room to spare.

| Hole | Y from beam front | Purpose |
|---|---|---|
| Vertical, counterbored from below | **15** | M8 up into a T-nut in the bottom extrusion's underside slot |
| Horizontal, into a tapped M8 in the end plate | **30** | shelf to plate |
| Vertical, counterbored from below | **45** | M8 up into the second underside slot |
| Horizontal, into a tapped M8 in the end plate | **60** | shelf to plate |

The 15 and 45 are the `30-6060`'s bottom-face slot centrelines, so the T-nuts drop straight in. The
even 15 mm spacing is forced, not chosen - 30 is exactly midway between 15 and 45 and moving it only
trades clearance from one side to the other.

**The holes clear in three dimensions**, which is the part that is not obvious in plan: the vertical
counterbores reach about 9 mm up from the underside, the horizontal holes are centred at 12.7 mm.
They never meet.

⚠️ **Not 70 mm for the rear horizontal hole** - on a 76.2 mm bar that leaves 1.7 mm of edge. 60 mm
gives 16 mm, comfortable.

Two things to watch:

- **M8 into 12.7 mm of plate** is 1.6 diameters, around 39 kN strip - far above what an M8 delivers.
- **The back joining plate's bottom edge must be flush with the beam's underside, not proud.** The
  bar passes under where that plate lands; if it hangs even a millimetre low the gantry sits on a
  plate edge in line contact instead of on the extrusion.

Assembly falls out of this nicely: **bolt both end plates on, slide the T-nuts in, drop the beam onto
the two shelves, then bolt down.** That is a one-person job, which the alternative is not.

### Same pattern, minus the stepper holes on the idle end

**BF12 and BK12 share the same horizontal mounting pattern** - only the vertical holes differ (2
against 4), and the horizontal ones are what get used here. So one support-block pattern serves both
ends and there is no handedness to worry about.

**The plate at the idle end gets no 35 mm hole and no stepper mount holes.** Everything else is
common.

This follows the precedent already set on the Y risers, where the steppers sit on the rear plates and
the front ones were left clean. Drilling unused holes as interchangeability insurance was considered
and rejected: **a plate that is built and calibrated does not get swapped**, and the cost is
permanent holes in a visible part.

### 35 mm is enough for the coupler

✅ **Measured: the coupler is 25 mm outside diameter**, so a 35 mm hole leaves 5 mm of annulus all
round and the coupler and screw shaft both pass comfortably.

Not a prediction - **the Y axes already run this exact arrangement**, stepper outboard, shaft through
the plate, coupler inside. See [`photos/y-beam-coupler-bk12.jpg`](photos/y-beam-coupler-bk12.jpg).

### ⚠️ Two different 35 mm holes will exist in this plate

The **stepper shaft clearance** here, and the **encoder sensor bore** called for in
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md).
Same diameter, same plate, different position and purpose. **Name them distinctly on the drawing**,
or "the 35 mm hole in the X end plate" becomes ambiguous later.

---

## Tramming

⚠️ **Partly open - the nod adjustment is undecided and has a deadline** (see the machining section
below; hole sizes depend on it).

### The rule that constrains every option

**A bolted face can only tilt about axes lying in that face.** Shimming or jacking changes standoff
along the face's *normal*, which produces rotations about the two axes *in* the face and never about
the normal itself. So each interface corrects exactly two of the three rotations, fixed by which way
it points:

| Interface | Face normal | Gives |
|---|---|---|
| X carriage plate ↔ X bearing blocks | Y (fore-aft) | **nod** + yaw |
| Spacers / spindle clamps ↔ Z plate | Y | **nod** + yaw |
| **X end plates ↔ Y carriage blocks** | X (across) | **roll** + yaw |

### 🔴 Do not make the carriage plate joint adjustable

Set screws over each bearing block is the usual arrangement and it is wrong here, for two reasons:

1. **The bolt heads are buried.** They sit on the carriage plate's front face, under the Z rails, the
   screw and the travelling nut housing. There is no access once assembled.
2. **That joint carries everything.** Replacing ~3400 mm² of face contact per block with four set
   screw tips gives local yielding, brinelling under cyclic load, and a joint that keeps settling for
   months. At 1000 N it undoes the stiffness the rest of the design is chasing.

**Build it solid and treat it as a datum.** Get it right at the mill.

### Roll: at the X end plates, and it is free

The X end plate to Y carriage interface gives roll directly, and **its bolt heads are on the outer
face at the ends of the machine, where nothing covers them**. Oversize those holes, add jack screws,
and roll becomes a screw adjustment reachable with the machine assembled.

**The X end plates are undesigned, so this costs nothing to build in** - decide it before they are
drilled.

### ⚠️ Open: nod

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

### 🔴 Decided: tram at assembly. No sub-plate.

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

### Doing the tilt

**A row, not a column.** A complete column adjusts one side against the other, rotating the plate
about a vertical axis - yaw, which does nothing on a round spindle.

**Use the two outermost rows:** one as the hinge, the other as the adjuster. Angular resolution is
jack travel divided by row separation, so the widest pair gives the finest control. The two middle
rows are simply torqued once the tilt is set. **One accessible bolt per side at a common height** is
enough to jack the adjusting row evenly - all four are not needed.

### Never tram the two clamps against each other

They bore a round body and **must stay coaxial**. Shim one relative to the other and the spindle is
pinched in misaligned bores. A sub-plate carrying both is fine - they move together.

### What tramming actually buys

**Surfacing the spoilboard with the machine itself removes the table-to-spindle error in Z**, so tram
governs wall squareness and scallop depth rather than whether a surfaced face comes out flat.

---

## Machining: one trip, so design ahead of the build

Accurate holes are drilled on **a single visit to a friend's shop** - a Laguna mill, 4' × 1' bed,
**manual X and Y**, DRO to be confirmed. **As of 2026-09-29 none of the 30 holes in the X carriage
plate are drilled.**

🔴 **Every plate needing accurate holes must be fully dimensioned before that trip**, including
assemblies that will not be built for months: **X carriage plate, Z plate, two X end plates**. One
more plate on the visit costs an hour; a second trip costs a weekend.

✅ **The four Y risers are already made and in service** - they are not on this list.

Still to make, but **no mill needed** - T-slot clearance holes throughout: two **12" × 1 m × 1/4"**
full-height plates and two **46 mm × 1 m × 1/4"** front plates, one of each per Y beam.

✅ **The two X end plates are specified** - one drawing, one setup, with the stepper holes omitted
on the idle end.

**Triage - not everything needs the mill:**

| Home drill press | The mill |
|---|---|
| Beam joining plates - 9 mm clearance into T-slots at 150 mm, and the T-nut moves to meet the bolt | Rail mounting patterns |
| | Bearing block and nut housing patterns, with counterbores |
| | The 8-bolt end plate patterns that must match the extrusion corner bores |

### Make one rail the reference, and give the second rail clearance

Two rails parallel and coplanar over 407 mm is what decides whether the Z runs sweetly or binds.
**Close-fit holes for rail one; oversize the holes for rail two** by about a millimetre. Then at
assembly, mount rail one, put an indicator on its carriage and sweep rail two into parallel before
tightening. Fixed holes on both rails makes whatever error the mill leaves permanent.

### Take the mating hardware, not just the plates

Bearing blocks, ball nut housing, BK12, BF12, and **an offcut of the `30-6060` with its corner
bores**. Every pattern can then be checked against the real part while still standing next to a
mill. The end plate pattern especially - a transfer punch through the real extrusion beats measuring
from a drawing.

### One datum per plate

Pick a corner, dimension every hole from it, **never chain dimensions**. On a manual mill with a DRO
the operator types absolute coordinates; chained dimensions accumulate error and invite arithmetic
slips.

---

## ⚠️ Open items

- ✅ ~~**Height from the top of the beam to the torsion box fixing line**, and whether the box has
  a **vertical face** to bolt against.~~ **Both closed 2026-09-30** - the box gets a purpose-built
  vertical face and the plate's bottom edge bears on the top skin. See "How it lands on the torsion
  box" above.
- **The exact box width**, which sets the top skin and therefore the spacing of the two curbs. Not a
  design number: it is **measured off the fully assembled CNC standing on a flat surface**, and the box
  is not built until then. Nothing else is blocked by it in the meantime.
- **Where the three-point mount pads sit relative to the two outer walls.** The entire Y beam load now
  comes down those walls, so the pads want to be under them rather than under the field of the bottom
  skin. The three-point-plus-fifth-leg scheme is still only in the project notes, not in this repo.
- ✅ ~~**The L bracket specification** - "15 × 1.5" has not been resolved.~~ **Moot 2026-09-30** - the
  9" tapered base gives the bolt spacing directly, so there are no L brackets. See "The lateral fix".
- ✅ ~~**Front corner three-way convergence**~~ **Closed 2026-09-30** - the front and back tongues run
  long and lap the side tongues' ends; nothing is notched. See "The lateral fix".
- 🔴 **How far past the front riser plane the spindle reaches**, and whether it fouls the widened fin
  at low Z. Confirmed to pass the plane; the amount is unmeasured. **Needed before the front plates are
  cut.** Four numbers listed under "The lateral fix".
- **Whether the front fins need the rib layout fixed first** - the bottom-edge bearing wants blocking
  under the full 229 mm base.
- 🔴 **How nod is adjusted** - does the spacer M5 counterbore pattern clear the 120 mm clamp
  footprint? Free if yes, a tram sub-plate and 13 mm of moment arm if no. **Needed before the
  machining trip, and now the only open question on that list.**
- **The mill's model number and whether it has a DRO** (2-axis or 3-axis) - expected ~2026-10-04. If there is no DRO, the drawings want dimensioning differently.
- **The spindle clamp geometry**, three questions above.
- **Vertical distance from the X beam centreline down to the spindle nose, Z fully retracted** - plus
  the **Z travel**. Together these give the torsional arm; worst case is the fixed distance plus full
  travel plus tool stickout. (Earlier drafts asked for "tool tip to beam", which is not a machine
  dimension - it moves with Z position, tool length and stickout. Use the **spindle nose**, a fixed
  feature of the body, rather than the collet nut, which shifts with collet type.) The horizontal arm
  is settled at 109 mm from the carriage plate, ~152 mm from the beam face.
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
