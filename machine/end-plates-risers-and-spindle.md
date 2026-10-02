# End plates, Z risers, and the spindle mount

**Partly settled, 2026-09-29.** The beams themselves are finished - see
[`gantry-beam-joint.md`](gantry-beam-joint.md). This file covers what holds them up and what hangs
off them. Several dimensions are still **⚠️ Open** and are marked as such rather than guessed.

---

## Cutting forces: 500-1000 N, not 250

🔴 **Read this before using any deflection figure in this repo.** Much of the analysis on
2026-09-29 was done against an assumed **250 N** cutting force. That is a trim-router number and it
is wrong for this machine.

This table was built when the spindle was expected to be **3 kW**. What that would have made
available:

| | Torque | 12 mm cutter | 6 mm cutter |
|---|---|---|---|
| 18 000 rpm | 1.6 N·m | ~265 N | ~530 N |
| 9 000 rpm | 3.2 N·m | ~530 N | ~1060 N |

⚠️ **Two corrections, neither of which moves the design target - 2026-09-30:**

1. **The spindle is 2.2 kW, not 3 kW.** Rated torque at 400 Hz is ~1.17 N·m rather than 1.6.
2. **The 9 000 rpm row assumes constant power below base speed, and a VFD spindle does not do
   that** - it is roughly constant *torque* down from 400 Hz, so the torque does not double, it stays
   put while the power halves. The doubled row overstates what the spindle can deliver.

**Design to 500-1000 N anyway.** The envelope is *not* being relaxed to match a smaller spindle, for
two reasons: a crash or a plunge into workholding generates forces the spindle rating has nothing to
do with, and relaxing a structural margin because a motor got smaller is the wrong direction of
travel. **Treat 500-1000 N as the structural envelope and the table as a note on what the spindle can
sustain in a cut** - they are different questions and were merged here.

Every deflection figure scales linearly, so anything quoted at 250 N is two to four times optimistic.
Where the original estimate still stands, it is because the conclusion was insensitive to the force -
not because the force was right.

---

## Y beam support

### 🔴 Reworked 2026-10-02 - read this before anything below it

**Cast stepper frames were bought, and they moved the steppers to the front of the machine.** That
one part change cascaded through the whole Y end design, and several decisions recorded further down
this file were reversed on purpose. The short form:

| | Before (2026-09-30) | **Now (2026-10-02)** |
|---|---|---|
| Stepper mount | NEMA 23 on four 18 mm M5 standoffs off the rear plate, BK12 beside it | **One cast frame** carrying motor face, bearing housing and coupler - see below |
| Stepper end | Rear | **Front**, both Y beams |
| Front plates | Tapered fins, 3/8" | Tapered fins, **1/2"**, with a **62 × 50 mm window** for the casting |
| Rear plates | Two 3" risers, kept as built | **Scrapped.** One **1200 mm × 1/4" hot-rolled A36 steel** back plate replaces both risers *and* the separate shear panel |
| Outboard plates | 12" × 1000 × 1/4" **6061** | 12" × 1000 × **1/8" cold-rolled steel sheet** |
| Front strips | 3/8" on Y, 1/4" on X | **46 mm × 1/4" 6061 on all three beams**, X included |

Two reversals are deliberate and are recorded with their reasons where they occur: the
**monolithic rear plate**, rejected on 2026-09-30 and adopted now because three of its four grounds
lapsed; and **steel joining plates**, rejected in
[`gantry-beam-joint.md`](gantry-beam-joint.md) and adopted now with the thermal cost accepted rather
than avoided.

---

✅ **Both Y beams are built** as described here - stacked pairs, rails, screws, BK12/BF12, steppers
and all four risers. See [`photos/y-beam-end-plate-outer.jpg`](photos/y-beam-end-plate-outer.jpg) and
the three beside it. **The riser geometry below is as-built, not a proposal**, and the 8-bolt pattern
into the corner bores is proven hardware rather than a first attempt - which is why the X end plates
copy it.

⚠️ **As-built is no longer as-designed.** All four risers come off. The 8-bolt corner-bore pattern
is the part that carries forward; the plates themselves do not.

Each Y beam is carried at its two ends only. It cannot be supported along its length: **the ball
screw runs underneath the beam**, which is also why the outboard plate below matters so much.

### End plate / Z riser

| | **Front (2026-10-02)** | **Rear (2026-10-02)** |
|---|---|---|
| Size | **Tapered: 100 mm at the top, 200 mm at the base, 302 mm tall, 1/2" thick** | **One plate for both beams: 1200 mm × 12" × 1/4" steel** |
| To the beam | **8 × M8 × 35 mm flange bolts** - four per profile | Same 8-bolt pattern, **× 2 beams = 16 bolts** |
| To the torsion box | **Two M8 through the front tongue at X 25 and 170, Y 30**, plus bottom-edge bearing | **8 bolts through the back tongue at Y 30**, ~150 mm pitch, plus bottom-edge bearing over the full 1200 mm |
| Also carries | the **62 × 50 window** for the cast stepper frame | **BF12**, 4 × M5 tapped into the plate, one per beam |

⚠️ **The old rear column of this table is gone, not merged.** The two 3" rear risers are scrapped.
Nothing in the rear column above is as-built hardware.

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

⚠️ ~~**Do not remake the Y risers on cosmetics.**~~ **Overtaken 2026-10-02 - all four come off.**
The rule was right and it is not being abandoned on cosmetics: the front plates change shape *and*
gain a window, and the rear pair is replaced by a single member that does a job neither of them
could. The sentiment behind the rule still applies to anything else that is built and calibrated.

📌 **What survives from the as-built risers is the 8-bolt pattern and the 9 mm hole**, both of which
carry straight into the new plates. The existing plates were drilled at home with a **mag drill**, so
the pattern itself costs no mill time; only the window and the 1200 mm plate's two patterns need the
trip.

---

## The cast stepper frames

✅ **Bought, in hand, and the reason the Y ends were reopened - 2026-10-02.** A one-piece cast
aluminium frame carrying the **NEMA 23 mounting face, the ball screw bearing housing and the coupler
window** in a single part. It replaces **both** the BK12 support block and the four 18 mm stainless
M5 standoffs the motor currently stands on - see
[`photos/y-beam-stepper-mounted.jpg`](photos/y-beam-stepper-mounted.jpg) for the arrangement it
supersedes.

### 🔴 Every axis gets one - X, Y1, Y2 and Z

**Decided 2026-10-02, and for one reason on all four: get rid of the standoffs.** This started as a
Y-axis change and is not one; it is now the machine's standard way of mounting a motor to a screw.

| Axis | Where the casting goes | BF12 stays |
|---|---|---|
| **Y1, Y2** | Under the beam at the **front**, on a 60 × 150 × 3/8" interposer bar | On the rear plate's inside face |
| **X** | On **top** of the beam, on a **3/8"** interposer, overhanging the end | On a 3/8" interposer at the far end |
| **Z** | On the **X carriage plate** - 1/2" aluminium, so **no interposer**, the casting taps straight in | At the bottom of the plate |

📌 **Only Y and X need an interposer, and for the same reason**: the casting lands on an extrusion
face whose wall is 2.21 mm, which is 0.44 × D for an M5 and not a thread. **Z lands on 1/2" plate -
2.5 × D - so it bolts direct.**

✅ **Every interposer is 3/8" 6061** - settled 2026-10-02, one thickness across the machine. M5 into
9.525 mm is **1.9 × D**, inside the 1.5-2 band aluminium wants, and the thread shears near **18 kN**
against an M5 class 8.8 bolt breaking near **11** - so the plate thread outlasts the fastener. It
also takes a button-head counterbore with 6.5 mm left under it, which is what the bolts inside the
casting's footprint need. **1/2" was available and buys only margin**; its one effect would be the
screw axis sitting 3.2 mm lower, which increases nut-to-beam clearance rather than eating it.

✅ **Z's travel budget is untouched - confirmed 2026-10-02.** The span between BF12 and the
casting's own bearing is still **272 mm**, so 246 mm rail-limited and ~26 mm of screw overrun both
stand, and with them the 7 mm / 10 mm hard-stop working.

✅ **And the casting-versus-hard-stop fit is resolved**: the single plate becomes **two blocks, one
either side of the casting**, 47 mm wide each. See the Z travel section.

### Why it was worth reopening a built axis

Two complaints, and only one of them is a stiffness problem:

1. **Stiffness.** Four thin standoffs in bending are the soft link in a path that runs stepper →
   coupler → screw.
2. 🔴 **Squareness, and this is the one that cannot be fixed by buying better standoffs.** Nothing in
   the standoff stack holds the motor face square to the plate except four standoffs being identical
   and four holes being true. Both are hand work. The casting makes motor face, bearing bore and
   coupler alignment **features of one part machined in one setup** - the error source is removed
   rather than reduced.

### How it mounts, and why that needs a bar

🔴 **The casting bolts to a face of the extrusion, not to the end plate.** This is the whole
difference from BK12 and it drives everything else. Its foot is **stepped, not one flat plane** -
there is a ledge where the stepper mount begins.

**Six through-bolt holes**, and they cannot land directly in the extrusion: the wall at that face is
**2.21 mm** (measured), which is 0.44 diameters for an M5 and not a thread. So an interposer carries
them:

| | |
|---|---|
| Bar | **60 mm wide × 150 mm long × 3/8" aluminium** |
| Position | its **outboard end 30 mm past the fin's outer face**, so the casting and bar protrude through the window together |
| Bar to extrusion | **6 × M5 flange bolts** in **3 rows**, into T-nuts in the `30-6060`'s bottom-face slots at 15 and 45 mm |
| Rows, from the bar's outboard end | **82, 110 and 138** |
| Counterbores | **none anywhere** |
| Casting to bar | its 6 through holes, **tapped into 3/8"** = **1.9 × D** |

✅ **3/8" confirmed 2026-10-02, and it is a thread-engagement decision.** M5 into 9.525 mm of 6061
sits in the 1.5-2 × D band aluminium wants, and the thread shears near **18 kN** against an M5
class 8.8 bolt breaking near **11 kN** - stronger than the fastener it holds. Same thickness on X;
Z needs none, landing on 1/2" plate.

#### The 30 mm protrusion is what sets everything else

Measuring along the beam from its end face, with the fin occupying 0 to −12.7:

| | |
|---|---|
| Fin's outer face | **−12.7** |
| Bar's outboard end, 30 mm proud of it | **−42.7** |
| Bar's inboard end, at 150 long | **+107.3** |
| **Bar length actually over the beam** | **107.3 mm** - the only part that can reach a T-nut |

🔴 **That is why the bar went to 150 and why the counterbores disappeared.** At 120 the bolted
length would have been 77 mm and **all four** counterbored bolts would have fallen off the beam -
the rows at 14 and 43 landing at −28.7 and +0.3. The casting's own tapped holes occupy bar
coordinates 28 to 71, which is mostly past the beam's end, so there is simply nowhere under the
casting to put a T-nut bolt. **Three rows of flange bolts inboard of the casting is the only
arrangement available**, and 150 is what makes room for the third.

**Why 82 / 110 / 138**, which are the two checks that bind:

- **82 clears the casting's last tapped row at 71** - 11 mm along, 13.6 mm in 2D against the 8 mm
  lateral offset, leaving ~5 mm of web.
- **138 leaves 12 mm to the bar's inboard end**, enough for an 11.8 mm flange head.

✅ **Peel is comfortable.** Thrust acts 34.5 mm off the extrusion face, so ~700 N gives ~24 N·m;
over the 56 mm spread of the bolt group that is about **400 N of uplift** against six M5 of clamp.

⚠️ **The casting now cantilevers 42.7 mm past the beam's end**, carried by the bar alone. That is
accepted, and it is the same call made on X: roughly 2.5 kg at that reach is under 2 N·m, and the
thrust it carries runs **along** the beam rather than down.

#### ✅ The ball nut clears the bar by 5 mm

The bar hangs 9.525 mm below the beam's underside, directly in the screw's lane, so the nut has to
pass beneath it for the whole 107 mm the bar is over the beam.

| | |
|---|---|
| Beam underside to nut top | **3/8" + 5 mm = 14.5 mm** |
| **Nut top to the bar's underside** | **5 mm** |

**So the bar's length does not limit Y travel**, which is what the question was.

❌ **And it is not the ball nut tongue that had to clear it.** An earlier note here said the bar's
inboard end was an input to the tongue's design. **Wrong** - the tongue is vertical, on the nut's
**outboard face**, so it never passes under the beam where the bar is. The two are in different
planes. What had to clear was the nut housing itself, and it does, by 5 mm.

#### 📌 The clash that shaped the earlier design, and why it is now moot

Both hole patterns are **centred on the beam**, so there was never any lateral freedom:

| | Column positions across the 60 mm bar |
|---|---|
| Casting | **7 and 53** - **46 apart, which is the BK12 pattern** |
| T-nut slots | **15 and 45** (30 apart) |
| Gap | **8 mm** |

**The 46 is BK12's own bolt spacing**, which the casting inherits along with the bearing housing -
7 + 46 + 7 across a 60 mm face. So **the 8 mm offset is a property of the pattern pair, not of this
part**: it is half the difference of the two spacings, **(46 − 30) / 2 = 8**. That makes it
general - **any BK12-family footprint lands 8 mm off the slots** when bolted flat to a `30-6060`
face.

At 8 mm a Ø10 M5 counterbore and a tapped M5 leave **0.5 mm of wall**, which is why an earlier
design staggered four counterbored button heads along the bar to dodge the casting's rows.

✅ **None of that survives, and the reason is worth keeping**: once the casting moved out to
protrude through the window, there was no bar-over-beam left underneath it, so the counterbores
went away entirely rather than being made to fit. **The clash was solved by the layout moving, not
by the stagger.** Keep the 8 mm figure though - it will recur on any other BK12-family part bolted
to an extrusion face.

📌 **The bar can only extend inboard.** At the stepper-mount end the casting's ledge hooks over the
front edge, so there is no room that way - which is why all six bolts are inboard of the casting
rather than spread either side of it.

**What the six bolts are for:** stopping the bar sliding, and holding it flat against the extrusion.

⚠️ **The step in the foot has to be matched or cleared.** If the bar sits under the stepped portion
it either steps too or holds the casting off its intended bearing face.

#### The casting's hole pattern, measured 2026-10-02

| | |
|---|---|
| Columns, from the 60 mm bar's edge | **7 and 53 mm** |
| Rows, from the bar's front edge | **28, 58 and 71 mm** |
| **Screw axis above the casting's foot** | **25 mm** |
| → **screw bottom above the casting's foot** | **17 mm** (25 − 8, the 1605 being ø16) |

🔴 **Do not add the bar thickness to the 25 and call it a clearance.** An earlier version of this
file recorded "34.5 mm below the extrusion face" as *the* screw axis figure. That number is real -
it is where the axis sits relative to the face - but it decides nothing, because **the bar lifts
screw, BF12 and casting as one unit.** Every clearance that matters is internal to the casting and
is unchanged by how thick the bar is. **17 mm is the number to carry.**

### 🔴 The thrust path changed direction, and a block fixes it

**Observation:** BK12 bolts to the end plate with the screw axis **perpendicular** to its mounting
face, so screw thrust is reacted in bolt tension one way and face bearing the other, into a plate
M8'd to the extrusion's corner bores.

**What changes:** bolted under the beam, the same thrust runs **parallel** to both new interfaces -
casting on bar, bar on extrusion - so it is carried in **friction**, and the T-slot lip sets the
usable preload rather than the bolt.

**Interpretation, labelled as such:** the rough figure is several times the ~500-700 N per screw this
axis sees, so this is not expected to need designing around. It is recorded because it is the one
load path that genuinely changed character, and because friction is the kind of margin that is fine
until it isn't.

⚠️ **A positive stop at the casting end was discussed and is NOT currently in the design.** An
earlier draft of this file recorded "a block bolted to the plate with a 20 mm bore" as settled
insurance. It was neither settled nor, as written, in the right place - the block that *was* settled
is **BF12 at the far end**, which is a floating support and not a thrust stop. If the friction path
above ever needs backing up, a stop at the casting end is the cheap way; nothing has been drawn.

### ✅ The steppers move to the front

**Decided 2026-10-02, and it is the change with the widest reach.** Both Y steppers go to the front
of the machine, with **BF12 bolted to the rear plate's inside face** at the other end.

- **~20 mm less encroachment** in front of the machine than the current standoff arrangement, because
  the casting is shorter than motor-plus-standoffs-plus-BK12.
- **Maintenance is far easier** - the motors are at the operator's end rather than reached over the
  bed.

⚠️ **Three consequences, all live:**

1. The **62 × 50 window moves to the front plates**, which are the tapered fins about to be cut.
   See "The lateral fix" below.
2. **Nothing passes through the rear plane any more**, which is part of why one monolithic rear plate
   became practical.
3. 🔴 **A NEMA 23 permanent-magnet rotor now sits at the min-Y end of the magnetic tape.** That is a
   far larger magnetic object than the bolt heads the austenitic-stainless section below exists for.
   **Fit a tape offcut and a sensor and read at that end before 3 m of one-shot PSA goes down.**

### ✅ The screw height, and the clearance that actually matters - closed 2026-10-02

**The as-built reference**, for comparison:

| | |
|---|---|
| BK12 / BF12 mounted | **5 mm above the extrusion** |
| Beam underside to the top of the ball nut | **10 mm** |

**That 10 mm is the live clearance** - the nut runs the length of the beam and must stay clear of
its underside. It is the number any change to the screw height has to be checked against, not the
axis position on its own.

✅ **The new arrangement moves the screw down, so this clearance grows rather than shrinks** - the
casting hangs below the beam on the bar, where the current supports sit on the end plates.

### The ball nut is inverted, and it lands on a sole plate - not a tongue

✅ **Decided 2026-10-02.** The ball nut housing runs **upside down on both Y beams**.

🔴 **Superseded later the same day: there is no tongue.** The X end plate now runs down to
**−182.5**, level with the nut's downward-facing mounting face, and a **1/4" sole plate** bolts
across its bottom. The nut's own fixing ties the two together. **Full working in the X end plate
section - "The plate height: 242.5 mm".**

❌ ~~"bolting to a **tongue coming off the bottom of the X carriage plate**"~~ - dead twice over. The
scheme is a sole plate, and the plate named was wrong or at best loose: the Y nut lands on the X
**end** plate, which is the Y carriage. The 154 × 407 carriage plate rides the X beam and is nowhere
near a Y screw. ⚠️ **Recorded rather than silently fixed**, because "carriage plate" may have meant
"the plate that is the Y carriage" - the sentence is gone either way, but if a drawing anywhere
inherited that reading it needs checking.

📌 **The reason is assembly access, and it is the kind of thing that is free to decide now and
expensive later** - inverted, the nut's mounting bolts are reachable while the gantry is being put
together. Right way up they are trapped between the nut and the plate.

✅ **This also answers what the 120 mm bar was an open input to.** The bracket is a tongue off the
carriage plate, not a wrap-around, so the bar's inboard end is something to draw the tongue clear
of rather than an unknown. **Still true with the sole plate** - it is the sole plate rather than a
tongue that has to be drawn clear of the bar's inboard end.

### BF12 goes straight onto the rear plate - no bar at that end

✅ **Decided 2026-10-02.** BF12 bolts to the **inside face of the 1200 mm rear plate**. The bar
exists only because the casting lands on a 2.21 mm extrusion wall; BF12 lands on 1/4" steel and
needs nothing.

| | |
|---|---|
| Fixing | **4 × M5 tapped into the 1/4" plate** - not through-bolted, for maximum engagement |
| Engagement | 6.35 mm = **1.27 × D** |

✅ **1.27 D is enough in steel, which is worth stating because the same figure would not be in
aluminium.** The internal thread shears at roughly **14 kN** against an M5 class 8.8 bolt breaking
near **11 kN** - so the plate thread is stronger than the bolt it holds, and the joint fails at the
fastener as it should. The repo's "aluminium wants 1.5-2 × D" rule is about aluminium; do not carry
it across.

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

Material is **added inboard**, toward the machine centre, tapering from **100 mm at the top to
200 mm at the base** (settled 2026-10-02; earlier drafts had 3"/9" and 4"/7.8"). It is not a bolt-on outrigger; it is the plate's own outline, which is why the
plates are remade rather than scabbed.

Lateral stiffness goes as **width cubed**, and a taper puts the section where the moment is. Treating
the riser as a cantilever over the ~185 mm between box top and beam underside:

| Base width, at the same thickness | Stiffness vs the 3" prismatic riser |
|---|---|
| 6" | ~4.9× |
| 8" | ~9.6× |
| **200 mm - chosen 2026-10-02** | **~9.2×** |
| 12" | ~25× |

📌 **At 1/2" the chosen figure is the full ~9.2×.** Stiffness scales linearly with thickness, and
as of 2026-10-02 the front plates are **1/2"**, the same as the as-built risers they are compared
against. *(An earlier draft had them at 3/8" and derated this to ~9.5×; that no longer applies.)*

⚠️ **Calculated, not measured.** Tapered cantilever, width varying linearly, load at the top, fixed
base. The fixed-base assumption is doing real work - see the bolt note below.

### Cut two from one 12" square, and reference off the factory edges

✅ **Decided 2026-09-30.** One **12" square of 3/8" aluminium**, cut once on a line from **3" in at the
top to 200 mm in at the bottom**, yields **both front plates** - each half is 100 mm at the top,
200 mm at the base, 302 mm tall. **100 + 200 + 2 = 302**, the 2 being the kerf.

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

📌 **The front plates went to 1/2" on 2026-10-02**, so the "is 3/8" acceptable" discussion below is
now moot for these plates rather than resolved. The reason is the window: these plates stopped being
pure fins when they took on the cast stepper frame, and the thickness went back up with the duty.
M8 × 35 leaves **22.3 mm** in the extrusion, as on the as-built risers.

Cost is about **+1.5 lb per front plate**, static. Two things it does *not* cost:

- **No bed area.** The fin is a 12.7 mm slice in the riser's own plane, not a wedge intruding into the
  work volume.
- **No travel.** It lives in the plane of the end plate, which the gantry already cannot reach past.

### ✅ The fin, fully dimensioned - 2026-10-02

**The taper is pinned, so everything below is arithmetic rather than judgement.** Datum is the
**top-outboard corner**, the two factory edges, per the layout rule above. X runs inboard, Y runs
down.

| | |
|---|---|
| Top width | **100 mm** |
| Base width | **200 mm** |
| Height | **302 mm** |
| Thickness | **1/2"** |
| Taper | corner to corner, **18.33° from vertical** (rate 0.3311 mm per mm) |

📌 **The stock is a MEASURED 302 mm square, not a nominal 12".** That is what sets the numbers:
**100 + 200 + 2 = 302**, the 2 mm being the kerf of the single diagonal cut. Both halves come out
identical by rotation, with nothing left over and nothing assumed about the cut being free.

**The 8 × M8, 9 mm clearance**, from the top-outboard corner:

| | |
|---|---|
| Columns | **X = 35 and 65** |
| Rows | **Y = 15, 45, 75 and 105** |

📌 **Those rows are the corner bores and they self-check**: the fin's top edge is the beam's top, and
a `30-6060`'s bores sit 15 and 45 in from each face, so a stacked pair gives 15, 45, 75, 105.

**The 62 × 50 window:**

| | |
|---|---|
| Outboard edge, from the fin's outboard edge | **X = 19** |
| Inboard edge | **X = 81** |
| Top edge, below the fin's top | **120 mm + the interposer thickness** = **129.5 mm** at 3/8" |
| Bottom edge | **179.5 mm** |

✅ **The horizontal position derives rather than being measured, and it agrees with the template.**
The beam spans X 20-80, so its centreline - and the screw's - is **X 50**. A 62 mm window centred
there runs **19 to 81**, giving the **19 mm outboard strip measured off the MDF**. Two independent
routes to the same number.

📌 **Recorded as a formula as well as a number**, because the 120 is the beam's own height and the
rest is the interposer - so if the bar ever goes to 1/2" the window drops 3.2 mm to 132.7 and
nothing else changes. **The interposer is 3/8", confirmed 2026-10-02.**

### 🔴 The 62 × 50 window, and why the taper does not help it

**Added 2026-10-02 when the steppers moved to the front.** The cast stepper frame passes through the
front plate, so each fin needs a **62 mm wide × 50 mm tall** rectangular window below the beam.

**The finding that matters, and it is assumption-free:** 62 mm of window in a 76.2 mm plate leaves
**14.2 mm total**, split between the two sides. **The taper does not rescue this** - it adds material
**inboard**, while the window's tight side is the **outboard factory edge**. Widening the top of the
fin is the only thing that buys outboard material.

⚠️ **And the nesting is what pays for it.** Two identical-by-rotation halves only come out of one 12"
square when **top + base = 12**. So 3" / 9" works, and **4" / 8" works**, but 4" / 9" needs a 13"
blank.

✅ **Measured off the MDF template, 2026-10-02: the outboard strip is 19 mm**, from the factory
edge reference.

**That is the only strip that matters, and it was the number in doubt** - the fear was 7, which
would not have worked. At 19 the window sits in the plate with no thin edge, so **the 12" square
still yields both plates** and no bigger blank is needed. (The inboard side runs 60-72 mm across
the window's height; recorded only to show it is nowhere near a constraint.)

📌 **The taper angle is free.** What is fixed is **4" at the top** and a base that comes out
**slightly under 8"**, because the single diagonal cut takes half the saw kerf off each half. The
exact base figure is not a number anything depends on - and per the layout rule above, working
from the factory edges keeps the kerf out of the hole pattern entirely.

📌 **Thickness cannot buy edge distance.** A 7 mm strip is 7 mm at 3/8" or at 1/2". What 1/2" buys
back is the **bending stiffness** the window removes, which is a different question and a real gain.
Both were in play here and they are easy to merge by accident.

### ✅ The M8 columns sit at 35 and 65 mm from the factory edge

**Settled 2026-10-02, off the MDF template.** The `30-6060`'s corner bores sit 15 and 45 mm in from
each face, so columns at **35 and 65** put the beam's outboard face **20 mm inboard** of the
plate's outboard factory edge - and the beam therefore spans **X 20 to 80**, centred in the fin's
100 mm top width with 20 mm of overhang each side.

**The outboard plate is 1/8" steel (3.175 mm), so the riser's edge stands 16.8 mm proud of it** -
and as of 2026-10-02 **that is wanted, not tolerated.** The end plate overhanging the side plate
looks better, and the two never meet in any case: the side plate stops **1 mm shy of the beam's
end**.

✅ **35 and 65 are settled.** The condition that made this look like a problem belongs to the box,
not to this plate.

⚠️ **The coupling, stated properly, because an earlier version of this section had it wrong.** The
worry was never that riser and side plate touch each other - they do not, and the 1 mm gap settles
that. It is that both want to bear against **the same curb inner face**. The box's outer wall
stands 61 mm proud as a curb and the design has **the full-height plate's outer face bearing on
it** - that is the full-metre lateral restraint, and "bias the top skin wide, never narrow" exists
because it is a hard bearing face with no float. If the riser's edge is the proud member **and the
curb reaches that far forward**, the curb is held out by the riser and leaves a 1.8 mm gap along
the plate's whole length.

✅ **So the fix goes in the part that is not built yet: terminate the side curb short of the
riser's station.** Costs nothing, keeps the plate's bearing, and leaves the overhang free to be the
deliberate choice it is. **Carried to the box's list, not the plate's.**

📌 **The rear needs the same thought** once the 1200 mm plate's length is fixed against the measured
machine width - see "The length" under the rear plate.

### The second gain is bolt spacing, and it is the bigger one

The project note's rule is that moment capacity comes from **bolt spacing, not bolt count** - two M8
200 mm apart beat six clustered in 50 mm. A 3" foot cannot give you that spacing at all, which is why
this file previously had to reach for L brackets to avoid a hinge at the base. **A 200 mm base
gives the spacing directly.**

✅ **Fixing, fully dimensioned: two M8 at X = 25 and 170 mm** from the outboard edge,
**Y = 30 mm** above the plate's bottom edge - **31 mm down from the top of the 61 mm proud
tongue** - plus the plate's bottom edge **bearing on the top skin** the way the outboard plate does.
*(X 25 settled 2026-09-30; T2 moved 175 → 170 and Y 31 → 30 on 2026-10-02.)*

📌 **T1 and T2 are those two bolts** - the labels are used below and were never defined. **T1 is
the outboard one**, near the straight factory edge; **T2 is the inboard one**, near the tapered
edge. T2 is the one that needs watching, because the taper is what takes its edge distance away.

🔴 **Not 200, and the reason is edge distance at the taper.** The plate narrows as it rises, so a
bolt too far inboard runs out of material - and what counts is the distance measured
**perpendicular** to the sloping edge, not horizontally. On the original 9" outline X 200 came out
around **12 mm**, less than the 9 mm hole's own diameter plus any sensible margin, on the bolt
carrying the larger share of the moment. **That is the constraint that sets T2, and it is why the
number moved again when the base came in to 8" - see below.**

| | X | Y | Edge distance to the taper, perpendicular |
|---|---|---|---|
| **T1** - outboard | **25** | **30** | n/a - straight factory edge, 20.5 mm |
| **T2** - inboard | **170** | **30** | **19.1 mm** |
| ~~T2 on the 9" base~~ | ~~175~~ | ~~31~~ | ~~34 mm - the old outline, at Y 31~~ |
| ~~T2 as first drawn~~ | ~~200~~ | ~~31~~ | ~~~12 mm - rejected~~ |

⚠️ **The 9" working's figures do not carry**: 213 mm of plate width at Y 31 and a 26.6 deg taper
both belong to the old outline.

#### ✅ T2 at 170

**At Y 30, T2's perpendicular edge distance is 19.1 mm** - a little over 2 × the 9 mm hole
diameter, and confirmed good on the template.

✅ **Y 30 is one datum across all three plates** - the front fin's two bolts, the side plates' row
and the back plate's row all sit at 30 mm above the plate's bottom edge, 31 mm below the top of the
61 mm tongue. One number to transfer instead of three, which is worth more than the millimetre it
moved. **The pitches differ because the plates do**: 100 mm on the side plates (eleven over
1000 mm), ~150 mm on the back plate (eight over 1200 mm). Both are correct; neither is the other's
typo.

❌ **A zigzag row was considered and rejected, 2026-10-02.** Alternating ±10 mm about the 30 line
would lift any single horizontal plane from ~90% to ~95% net section. It is not worth it here:

- **Net section is not what governs a bolt in plywood** - bearing and edge tear-out are. The
  staggering rule it comes from is a *sawn lumber* rule, there to stop a split running along the
  grain, and Baltic birch is cross-laminated.
- **±10 spends the margin that does govern.** On a 61 mm tongue the upper half would drop to 21 mm
  from the free top edge.
- **The row is not at the worst height anyway** - the tongue cantilevers up from the box, so peak
  bending is at its base, not at mid-height.
- On the side plates these bolts are **retention, not the load path**, so little is trying to tear
  that line at all.

📌 **Where a stagger would be right**, recorded so this is not read as a blanket rule: a row close
to a free edge and loaded *parallel* to itself, where group tear-out is the failure mode.

✅ **The taper is pinned corner to corner at 100 / 200 over 302, so the figures above are
determined** -
earlier drafts of this section fussed over where the taper started, which stopped being a question
once the outline was specified rather than measured.

✅ **Checked on the template and settled, 2026-10-02.** Both bolts marked at **X 25 and 170 on the
Y 30 line** land well, with no edge tight anywhere. See
[`photos/front-fin-template-tongue-bolts.jpg`](photos/front-fin-template-tongue-bolts.jpg). **The
plate geometry is closed** - nothing about the front fin now waits on a measurement.

| Direction | What takes it |
|---|---|
| Vertical | **Bearing** - fin bottom edge on the top skin |
| Lateral moment | The two through-bolts as a **145 mm couple** |


🔴 **The bolts are now the soft part, not the plate.** A 9.2× stiffer fin only pays if the base is
genuinely fixed, and the reaction at those bolts is vertical load bearing into plywood. The project
note's standing warning is that **plywood creeps in compression** with nothing to tell you. Use a
steel backing strip or large fender washers on both faces here, not plain washers.

⚠️ **Blocking under the 200 mm base** has to be in the rib layout - the bottom-edge bearing is only
worth having if it lands on structure rather than on skin spanning between grid members. The box is
built last, so this is free, but it must be decided before the skins are cut.

### Back: one 1200 mm steel plate, replacing both risers and the panel

✅ **Decided 2026-10-02.** The two rear risers are **scrapped**. One plate spanning the full machine
width does both jobs - carrying the two beam ends down to the box, and acting as the shear panel
that turns the rear face from a portal frame with two bending legs into a diaphragm.

| | |
|---|---|
| Plate | **1200 mm × 12" × 1/4" hot-rolled A36 steel** |
| To the beams | **8 × M8 into each beam's corner bores** - the same proven pattern, 16 bolts total |
| To the box | **8 bolts through the back tongue at Y 30**, ~150 mm pitch, plus bottom-edge bearing over the full 1200 mm |
| Also carries | **BF12 on its inside face**, 4 × M5 tapped into the plate, one per beam |

- **It costs no travel** - the gantry stops well forward of the rear plate plane, and the spindle sits
  ~109 mm ahead of the carriage plate.
- **Bonus: a rear chip fence** the width of the machine.

#### 🔴 This reverses the 2026-09-30 rejection, and three of its four grounds lapsed

The earlier text read: *"a monolithic replacement would put two 8-bolt patterns, two bores, two
stepper patterns and two BK12 patterns on one 1.2 m part, cut on a 4' × 1' manual-XY mill on a
one-shot trip, and would become the coplanarity datum before that datum has been measured."*

| Ground | Status 2026-10-02 |
|---|---|
| Two stepper patterns | **Gone** - the steppers are at the front |
| Two BK12 patterns | **Gone** - BK12 is inside the cast frame, at the front |
| Two 35 mm shaft bores | **Gone** - same reason |
| Becomes the coplanarity datum before that datum is measured | **Stands. Accepted deliberately.** |

**What is left on the part is two 8-bolt patterns and a clearance bore per screw** - fewer accurate
features than either rear riser carried before.

#### ⚠️ On the datum, and a correction to how it was first described

A one-piece plate **does** pre-commit geometry that was previously set by assembling on a flat
surface with the 9 mm reamed holes absorbing error. That inverts this repo's loudest standing rule
for one dimension, so it is a deliberate reversal rather than a side effect.

**But the inversion is narrower than it first looked** - and getting to that took two wrong turns,
both recorded because the wrong versions are the ones that sound reasonable.

⚠️ **Wrong turn one: "buy it flat."** An earlier draft made cold-rolled or ground stock a condition,
on the grounds that a wavy plate would leave the beam ends non-coplanar. That treated surface
flatness as the thing that matters, and it is not. It is also not a product - **A36 is a hot-rolled
structural spec**, while cold-rolled flat goes out as 1008/1018 to A1008, so "cold-rolled A36" would
get a substitution or a blank look.

⚠️ **Wrong turn two: "the plate follows the table."** The correction to the first was that the plate
is **~2300× stiffer in-plane than out**, so the flat assembly surface would overrule it. The ratio is
right; the conclusion drawn from it was not. **A 1200 mm steel plate standing on edge is not a
conforming object**, and the single ratio hides the fact that it is rigid in one of the modes that
matters.

#### What the plate actually controls, mode by mode

Treating it as a beam 1200 mm long with a 305 × 6.35 section:

| What you would have to do to it | Force needed | Who wins |
|---|---|---|
| Shift one beam-end pattern **0.1 mm vertically** relative to the other | **~8.3 kN** | **The plate.** Rigid - nothing argues with this |
| **Twist** one end 1 mrad relative to the other | ~2 N·m, about **17 N** at the beam | The flat assembly surface |
| Bow the middle **1 mm fore-aft** | **~36 N** | The flat assembly surface |

🔴 **So "coplanarity" is not one quantity.** The plate rigidly sets the two beam ends' **spacing and
relative height**; the table still sets their **roll and fore-aft tilt**. Collapsing those into a
single claim is what produced both wrong turns above.

📌 **And nothing conforms past 1 mm in any mode.** What absorbs error is the **9 mm clearance on
M8** - 1 mm of float per hole. Inside that the joint slides and takes up what it finds. Outside it
you are fighting the plate, and in the vertical direction you lose.

#### 🔴 The tolerance this puts on the drilling

**The two 8-bolt patterns' relative height must land well inside 1 mm across the metre**, or the
plate cannot be bolted on without jacking a beam end. That is a sharper statement of the mill risk
below: the question is not whether the part fits on the table, it is **whether the height datum
survives a reposition.**

✅ **Material: plain hot-rolled A36 is correct**, and the reason is the drilling setup rather than
the stock. Out-of-plane bow is the soft mode and bolting pulls it out. What would hurt is **camber**
- in-plane curvature along the length - and only if the part is datumed off a sawn or sheared edge
carrying it, because then the second pattern walks vertically by the camber amount. **Datum off a
scribed and indicated line, or indicate the first pattern back in before drilling the second.** Ask
for **P&O** if mill scale is unwelcome; same flatness, no scale, small premium.

#### The length: ~1205 mm nominal, and it is a window not a target

⚠️ **This is a DERIVED NOMINAL, not a measurement.** The real number comes off the assembled machine
standing on a flat surface, exactly as the box width does. It is written down because it gates a
purchase - the stock has to be ordered before the machine is standing.

| Term | mm |
|---|---|
| X beam | 1000 |
| 2 × X end plate, 1/2" | 25.4 |
| 2 × Y rail and bearing block stack, 30 mm | 60 |
| **Y beam inboard face to inboard face** | **1085.4** |
| 2 × Y beam width, 60 mm | 120 |
| **Y beam outboard face to outboard face** | **1205.4** |
| 2 × outboard plate, 1/8" | 6.4 |
| **Outside of the machine** | **1211.8** |

🔴 **The plate length has a lower and an upper bound, about 7 mm apart:**

| Bound | mm | Set by |
|---|---|---|
| **Minimum** | **~1205** | Edge distance. The outermost M8 sits 15 mm in from the beam's outer face; a shorter plate eats into that |
| **Maximum** | **~1212** | Past the outboard plates' outer faces the **rear plate** becomes the proud member at the corner - the direction curb bearing cannot take |

📌 **"1200 mm" as used elsewhere in this file is a round number, not this calculation.** The figure
to buy and cut against is **1205**.

✅ **A 48" sheet (1219.2 mm) covers it** with 7 to 14 mm of trim - but that is the entire margin.
**60" removes the question** and leaves an offcut, which is the better buy on a part cut once.

✅ **Both of this chain's assumed terms were confirmed 2026-10-02.** The Y rails are on the beams'
**inside faces, facing each other**, and **X, Y1 and Y2 all run the same HGR20 kit**, so the 30 mm
rail-and-block stack measured on X applies to both Y beams. The chain above is nominal only because
the machine has not been assembled and measured - not because any of its terms are guesses.

#### ⚠️ Open: can the mill hold a datum across 1200 mm

Two bolt patterns a metre apart, both of which must match extruded corner bores, on a **4' × 1'
manual-XY** mill. Bed size is not travel. If the part has to be repositioned mid-job the datum is
lost exactly where it is most needed. **Gated on the mill model and DRO question already in the open
items**, expected ~2026-10-04.

#### ⚠️ The bottom-edge bearing now runs the full 1200 mm

So the rib under it has to as well. The box is built last, so this is free - but it joins the list
of things that must be decided before the skins are cut.

⚠️ **The back panel does not cover the front.** The load path from a gantry parked at min-Y back to
that panel runs sideways through the Y beams - their 60 mm dimension, not their 120 mm - and the
outboard plates contribute nothing laterally, that being their out-of-plane direction. So the front
fins are carrying a front-position gantry largely alone. That is why the front is taken to 200 mm rather
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
to the bottom of the plate at 200 mm inboard. **Interference is therefore a corner-of-the-envelope case:
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
3. **Reduce the base below 200 mm** - the last resort, since the whole point was the base width,
   and it has already come down once from 9".

🔴 **Settle this before the plate is cut.** The taper line is one bandsaw pass and cannot be put back.

### Span deflection: not a problem

End support was queried and checked rather than assumed. With the 1/4" joining plates on, vertical
**I = 3.37 × 10⁶ mm⁴**, and the gantry's share of load per beam gives about **0.022 mm** of sag.
Going to 3/8" plates would make it 0.019 mm - a 3 micron difference. **The span is fine end-supported.**

⚠️ **0.022 mm is DEAD LOAD - the gantry's own weight. It is not the deflection under cutting force**,
and it has already been misread that way once. Under the 1000 N envelope the same beam moves roughly
**0.065 mm vertically and 0.13 mm fore-aft** (indicative only). **Fore-aft is the soft axis, by about
2×**, because the section is 120 tall and 60 deep and stiffness goes as (height/width)². The full
working, and why a single 40×120 was compared and rejected on exactly this, is in
[`gantry-beam-joint.md`](gantry-beam-joint.md).

---

## The full-height outboard plate

✅ **Decided 2026-09-29, material changed 2026-10-02. One per Y beam, 12" × 1000 mm × 1/8"
cold-rolled steel sheet**, replacing the existing 12" × 6" × 1/4" gusset - the dimensions rotate,
from 12" along the beam to 12" tall and a metre long.

### 🔴 It is steel now, and it is also the Y back joining plate

**Both halves of that sentence matter, and the second is what makes the first a reversal.** On Y
there is no separate 120 mm back joining plate - this plate *is* it, grown. So choosing steel here
overturns the explicit decision in [`gantry-beam-joint.md`](gantry-beam-joint.md):

> **Material is aluminium, not steel.** Steel would give roughly three times the modulus, but over
> 1000 mm a shop temperature swing puts a couple of tenths of differential expansion into a joint
> held by preloaded T-nuts that cannot comfortably slip. Matched aluminium removes the question.

**That reasoning was not wrong and is not being dismissed - the cost is being accepted instead of
avoided.** The differential is **0.17 mm over a metre at 15 K**, and the file had the magnitude
right at "a couple of tenths".

#### Why 1/8", and it is the thin one on purpose

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
is what was found.** Flatness does not bind here regardless: eleven M8 along the bottom edge plus
the curb channel pull 1/8" steel straight over a metre without argument, and the holes are 9 mm
clearance into T-slots where the T-nut moves to meet the bolt.

#### Sourcing, found 2026-10-02

| | |
|---|---|
| Listing | 1/8" × 12" × 48" mild steel sheet, **A36 hot rolled, "11 gauge"**, uncoated |
| Price | **$81.99 each** - and **two are needed**, one plate per sheet |
| Yield | 48" = 1219 mm against a 1000 mm plate, so a 219 mm offcut each |

⚠️ **"11 gauge" and "1/8" are not the same number** - 11 ga is 0.1196" (3.04 mm) against 0.125"
(3.175). Harmless for the structure: transformed area goes 9.2 → 8.8 mm equivalent aluminium, still
on the 3/8" target. **But measure what arrives and record it here**, because the curb channel width
and the riser-proud check at the front plates both key off this thickness.

📌 **~$4/lb is retail.** A steel service centre is typically around half that; at $164 for the pair
it is a judgement call whether the errand is worth it. **Mill scale comes off before paint** - and
paint is not optional here, see the galvanic note above.

#### 🔴 Galvanic is the real cost of this change

Steel against aluminium, with **a metre of face-to-face contact** against the beam plus eleven bolts
- and this plate is the **chip barrier**, so it is the part that actually gets wet with swarf and
coolant. Aluminium is the anode and the extrusion is the part that cannot be replaced.

**Powder coat or paint both faces**, and isolate the mating face if anything wetter than mist is
ever run. This is a bigger exposure than the rear plate's two bolt patterns and it is the one
downside that does not have a number attached.

⚠️ **The curb channel was dimensioned around a 6.35 mm plate** - see "How it lands on the torsion
box" below, where the plate occupies the outer 6.35 mm of the 19 mm web. At 3.175 mm that channel
needs resizing or the plate rattles in it. The box is not built, so this is free - but it is another
item on the decide-before-the-skins list.

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

📌 **The steel parts in absolute terms: ~17 lb per side plate and ~40 lb for the 1200 mm rear
plate**, so roughly **75 lb of steel** on the fixed frame. A delta against the old scheme is not
quoted because the shear panel it absorbs was never sized. All static, all low down, against a
figure that was always offered as a design budget rather than a limit.

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
| Height | **Y 30** above the plate's bottom edge - the same row height as the front fin and the back plate |
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

## Plate and riser thicknesses

**Material matters as much as thickness now that steel is in the machine, so both are given.**
Current as of 2026-10-02.

| Part | Size | Material |
|---|---|---|
| Front strip, **all three beams** | 46 mm × 1000 mm × **1/4"** | **6061** - connector across the seam and the magnetic tape surface |
| X back joining plate | 120 mm × 1000 mm × **1/4"** | **6061** - X moves, so weight is real |
| **Y outboard / back joining plate** | 12" × 1000 mm × **1/8"** | **cold-rolled steel sheet** - see the reversal above |
| **Y front plate / Z riser** | tapered 100→200 mm × 302 mm × **1/2"** | 6061, with the 62 × 50 window |
| **Y rear plate**, one for both beams | 1200 mm × 12" × **1/4"** | **hot-rolled A36 steel**, P&O if preferred |
| Cast stepper frame interposer bar | 60 × **150** × **3/8"** | 6061, one per Y beam and per X end |
| **X gantry end plates** | 154 mm wide × **1/2"** | 6061 - two identical plates, specified above |
| X carriage plate | 154 × 407 × **1/2"** | 6061 |
| Z plate | **164** × 175 × **1/2"** | 6061 |

⚠️ **Y and X back plates are no longer the same part in a different length.** Y's is steel, 12"
tall and carries the box fixing; X's stays 6061 at 120 mm. Do not let the old "all three axes, 1/4"
aluminium" line survive in anyone's head.

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
| Spindle | **Ø80 mm, 2.2 kW, water-cooled**, with matching VFD |
| Nameplate | **Φ80×200, 2.2 kW, 220 V, 8.5 A, 400 Hz** (24,000 rpm at 400 Hz) |
| Collet | **ER20**, supplied with Ø6 mm, range Ø1-12 mm |
| Cooling | two **Ø8 mm** water fittings, exiting **radially at the rear** |
| Clamps | **two 80 mm aluminium clamps**, one at each end of the spindle |
| Clamp size | 120 mm × 55 mm × 100 mm |
| Fixing | **4 × M8 × 80 mm socket head** per clamp, into the Z plate |

**Two clamps at either end is the right arrangement** and matches the dual-clamp recommendation
already carried in the project notes for a round-body spindle. Eight M8 holding the spindle is not
where this assembly will be soft.

### The body dimensions, off the vendor drawing

The three dimensions on the product drawing are **sequential, not overlapping** - confirmed by the
user 2026-09-30:

| Segment | |
|---|---|
| Collet nut face to the nose flange (nut + exposed shaft) | **52 mm** |
| Nose flange / front bearing cap | **25 mm** |
| **Nose flange to the rear end - the Ø80 body** | **199 mm** |
| Overall, collet nut face to rear | **276 mm** |

📌 **The full 199 mm is Ø80 and clampable.** The black bands at each end are finish, not steps - the
Ø80 dimension line on the drawing is drawn across the rear band. Only the two Ø8 water fittings near
the rear obstruct anything, and they sit above where the upper clamp goes.

⚠️ **The 52 and 25 are read off a listing drawing, not measured.** The 199 is the one that carries the
design and it has margin to spare (see the Z plate below), so this does not need confirming before the
plate is cut - but mic the nose stack before anything depends on the *vertical* arm.

### 📌 Why 2.2 kW and not 3 kW - the choice was made and reversed deliberately

A Ø100 3 kW unit was considered on 2026-09-30 and **rejected**. It is recorded because the reasoning
governs any future spindle change, not because the part is interesting:

- **Power is not the limit on this machine.** Aluminium's specific cutting energy is ~0.7 J/mm³, so a
  respectable adaptive cut for a router of this class - 6 mm three-flute, 18,000 rpm, 6 mm deep ×
  1.5 mm wide, ~24 cm³/min - draws about **0.3 kW at the cutter**. Consuming 2.2 kW in aluminium would
  need ~190 cm³/min, which is machining-centre territory. **Both spindles are five to seven times
  more powerful than the cut this frame can take.**
- **Rigidity is the limit, and Ø100 makes it worse.** The bigger clamp puts the bore centre ~75.5 mm
  off the mounting face instead of 50, taking the gantry moment arm from **187 mm to ~212 mm**, while
  roughly doubling the moving mass. More mass on a longer arm lowers the natural frequency and the
  chatter threshold - it spends capability on the axis that binds to buy it on the axis that doesn't.
- **It cost travel and plate width too:** a Ø100 clamp is 169 mm across the flanges, forcing a 180 mm
  Z plate and **13 mm of X travel at each end**, and its blank flanges would have put the mounting
  bolts *outboard* of the spacer centrelines rather than inboard.

**The one honest argument for 3 kW is hardwood** - a large surfacing or profile cutter genuinely can
pull 2 kW plus. If this machine's work shifts that way, that is the trigger to revisit, not aluminium.

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

### ✅ The Z plate: 164 mm W × 175 mm H × 1/2"

#### 🔴 164, not 154 - the width is set by the spacers, and 154 could not be drilled

**Corrected 2026-10-02.** The plate inherited 154 from the X end plate, and that number does not
work here:

| | On 154 | **On 164** |
|---|---|---|
| Plate half-width | 77 | **82** |
| Outer M5 column, from plate centre | 73.5 | 73.5 |
| **Edge distance** | **3.5 mm** | **8.5 mm** |
| Ø10 counterbore (5 mm radius) | **breaks through by 1.5 mm** | **clears by 3.5 mm** |

**Two independent reasons land on the same number.** The plate has to **cover the spacers** - with
the rails 10 mm in from each side of the carriage plate, that needs 164. And 164 is also what stops
eight of the sixteen M5 counterbores breaking out of the plate edge.

✅ **Nothing in the clamp working is disturbed.** The M8-to-M5 column offset is 8.5 mm measured
*from plate centre* either way, so the 116 mm clamp separation, the ±45.5 / ±70.5 M8 rows and the
14.1 mm worst-case clearance all survive unchanged. Only the outline moved.

⚠️ **It may cost ~10 mm of X travel** - the Z plate is now 5 mm wider than the carriage plate on
each side, so it reaches the X end plates sooner if it is the widest moving part. Not checked
against the end-stop geometry; flagged rather than claimed.

**The M5 pattern sets the clamp separation.** Not the barrel, not the block run - the four M5
counterbores that hold the plate to the bearing blocks share the plate's front face with the M8 tapped
holes, and dodging them is what fixes everything else.

| | |
|---|---|
| Plate | **164 mm W × 175 mm H × 1/2"** |
| **Clamp centres** | **116 mm** - clamp mid-height at **±58 mm** from plate centre |
| Clamp extent | **171 mm**, on a 199 mm barrel |
| M8 columns | **±50 mm** from plate centre |
| **M8 rows, from plate centre** | **±45.5 and ±70.5 mm** |
| **M8 rows, from the nearer plate end** | **17 and 42 mm** ← the drilling dimension |
| Relief at each plate end | 2 mm |
| Blocks | **butted**, full **246 mm** travel |
| Spacers | **6 inch, unchanged** |

#### The measurements this rests on - all read off parts, 2026-09-30

| | |
|---|---|
| Bearing block hole pattern | **32 × 36 mm** |
| M5 columns, from the rail centreline | **±16 mm** - ✅ this confirms the figure the file had carried as its one unverified number |
| M5 columns, from plate centre | **41.5 and 73.5 mm** (rail centrelines at ±57.5) |
| M5 rows, from the spacer bottom | **17, 53, 97, 133 mm** |
| **M5 rows, from plate centre** | **−59.2, −23.2, +20.8, +56.8 mm** |
| Clamp bolts | 4 × M8, **columns 100 mm apart**, **rows 25 mm apart** |

📌 **The 36 in the 32 × 36 is self-checking:** 53 − 17 = 36 and 133 − 97 = 36, so the row measurements
and the block pattern agree independently.

#### 🔴 Why 116 mm and not 144 - the columns are only 8.5 mm apart

**The M8 column at 50 mm sits just 8.5 mm from the M5 column at 41.5 mm.** An M5 counterbore is ~Ø10
and an M8 thread is Ø8, so **at the same height those two features physically overlap** - there is no
web at all. The M8 rows therefore have to stand vertically clear of every M5 row.

🔴 **That kills 144 mm centres outright.** At 144 the inner M8 rows land at **±59.5 mm**, against M5
rows at **−59.2 and +56.8**. A direct hit at both ends - it would have been found at the mill.

Holding **12 mm centre-to-centre in 2D**, and with 8.5 mm of that already spent on the column offset,
each M8 row needs ~8.5 mm of *vertical* clearance from every M5 row. That confines the clamp
mid-height to **55.2 to 60.8 mm** from plate centre. **±58 is the middle of that window**, and gives
a worst case of **14.1 mm centre-to-centre - about 5 mm of solid web** at the tightest pair.

#### What 116 mm buys and costs

- ❌ **Costs ~35% of the angular stiffness** against the unobtainable 144. Two clamps resist the tool's
  tipping couple on a lever equal to their separation, so stiffness goes as separation *squared*.
- ✅ **Still 37% better than the 99 mm** an earlier draft proposed, which set the clamp extent to the
  154 mm block run.
- ✅ **Zero overhang, and it costs nothing to get.** At ±70.5 **all four M8 rows are inside the ±76.2
  of the existing 6" spacers.** Every bolt is over supported metal without spreading the blocks.
- ✅ **Nothing gets re-cut and no travel is spent.** Blocks butted, full 246 mm, spacers as built.

📌 **This is also why 205 mm spacers do not help.** The collision is between two features **in the
plate**; spacer length has no bearing on it, and the M5 positions are set by the blocks and cannot
move. See the rejection note below.

📌 **175 mm is where the first draft of this section landed too**, by a completely different route -
that one sized the plate to the block run, this one to the M5 pattern. Coincidence, but a reassuring
one.

⚠️ **175 assumes nothing else lives on this plate** - no drag chain anchor, cable strain relief or
water line clamp. If one turns up, height is the cheap thing to change, but only before it is cut.

**Still measure on arrival:**

- **Where the water fittings and cable exit sit** - they cap the clamp spread and set the drag chain
  routing
- **Nose to collet nut face** - the fixed part of the torsional arm; the drawing says 52 mm, unverified
- **Weight**, for the moving mass
- **Body diameter** over the whole clamping length rather than nominally

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

⚠️ **That 77 was measured on the Z kit.** The X/Y kit's blocks measure **77.09** and so the two
agree - but they are different suppliers and the agreement is not guaranteed. See the kit note
under the X gantry end plates.

⚠️ **272 mm is the screw-side travel and it is NOT discarded** - it is the span the nut can run
between its two supports, which overruns the rails. It is simply not the limit; the rails are.
*(An earlier wording here said the measurement was "discarded", which was too strong and would
invite the next reader to ignore a live figure.)*

✅ **The casting leaves it at 272 - confirmed 2026-10-02.** Replacing BK12 with the cast frame does
not move the upper bearing relative to BF12, so **the whole travel budget below is unchanged**:
246 mm rail-limited, ~26 mm of screw overrun, and the 7 mm / 10 mm stop working still stands.

#### ✅ The screw outruns the rails by ~26 mm upward - and a physical stop catches it

**Both ends of Z travel have a mechanical stop.** Going down, the nut bottoms on BF12. Going up,
blocks bolted to the top of the X carriage plate overhang the rail ends and the rising bearing
block meets them. The **proximity sensor is at the top of Z**; the stop is what catches the axis if
the control runs past it.

#### ✅ The top stop is TWO blocks, not one plate - 2026-10-02

The cast stepper frame now occupies the middle of that top edge, so a single 6" plate spanning both
rails cannot go there. **One block per rail, either side of the 60 mm casting:**

Each block caps the plate's top edge and overhangs forward over the rail end:

| | |
|---|---|
| Width, across the plate | **47 mm** - 154 − 60 = 94, halved, less whatever relief is wanted at the casting |
| Front-to-back | **32.5 mm** = **12.5 of plate + 20 of rail**, so the overhang is flush with the rail top |
| Vertical thickness | **1/4"** |
| Fixing | **2 × M4 × 16 socket head** per block, down through it into tapped holes in the plate's **12.7 mm top edge** |

📌 **M4 rather than M5 on edge distance**: tapping a 12.7 mm edge leaves 4.35 mm of wall each side
of an M4 against 3.85 for an M5.

🔴 **Do not size these by strength.** They fire only if **the soft limit and the proximity sensor
have both already failed**, and the design intent is that they are **sacrificial** - if one is ever
used, replace the block and the bolts and move on. That is the same reasoning the superseded 1/4"
plate was chosen on. *(A load analysis was written here and removed: a part deliberately made the
weak link does not get a safety factor.)*

✅ **This is better than the plate it replaces, not just a way round the casting.** Each block sits
**directly over its own rail** - centres at ~23.5 and ~130.5 against rail centrelines at 19.5 and
134.5 - so the rising block meets metal immediately above itself instead of at the end of a lip
spanning the gap. The old warning to "keep the overhang short so impact loads the bolts in shear
rather than bending a cantilevered lip" is satisfied by the geometry rather than by discipline.

📌 **Matching the rail's height is what makes the contact square.** The bearing block stands 30 mm
off the plate and wraps the rail; a stop flush with the rail top gives it a full-width face to hit,
where the old 1/4" plate presented a 6.35 mm lip.

✅ **Rail height taken off the part: 20 mm** - which is what the 32.5 is built from, and why the
derivation is written out rather than just the total. This mattered because **Z is a different
supplier from X / Y1 / Y2** and this file already carries one near-miss from quoting a dimension
measured on the wrong kit.

⚠️ **This heading used to read "with no hard stop", and it was wrong** - the resolution was already
written in the paragraphs below it while the alarm stayed in the title. Corrected 2026-10-01, after
that stale heading was read at face value and propagated into
[`../commissioning/stiffness-test.md`](../commissioning/stiffness-test.md) as a reason not to put the
carriage near the top of travel. **A headline that contradicts its own body is worse than no note**,
because skimming is how a long file gets read.

**The hazard being guarded against was real and is worth keeping.** A soft limit is a configured
value, and if it is ever wrong, missing or bypassed - a homing move, a lost setting, a restored config
- nothing in software stops the carriage leaving the rail. That is the failure this repo's standing
rule exists for, and it is why the stop is physical.

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

✅ **The ±16 mm is measured, 2026-09-30** - the block hole pattern is **32 × 36 mm**. So the M5 columns
fall at **41.5 and 73.5 mm** from the plate centre, and **the clamp bolt at 50 mm is bracketed between
them** rather than cantilevered outside. Load goes bolt → plate → spacer → block with the plate barely
working.

🔴 **But 8.5 mm of bracketing is also a clash.** The M8 at 50 and the M5 counterbore at 41.5 are close
enough that at equal height the two features *overlap* - which is what drives the clamp separation. See
the Z plate section above.

📌 **This is the left-right axis only.** Vertical alignment - clamp centres against block centres up
the rail - was the open one, and the only one that could cost travel.

✅ **It closed on 2026-09-30 costing nothing.** The procedure below was written expecting a trade, and
it resolved to the no-trade corner: the Ø80 body is 199 mm, two 55 mm clamps need only 154 mm of
extent to match the **butted** block run, so step 3's spread is **zero** and step 5's re-cut does not
happen. Full **246 mm** travel, zero overhang, 6" spacers as built. See the Z plate section above.

**The ordering is kept because it is the method, not the answer** - a different spindle or a different
clamp puts the trade back on the table:

1. **Set the Z travel floor first** and treat it as hard - material thickness plus tool length plus
   clearance over workholding. 🔴 **This is the one that gets quietly eroded** while optimising the
   other end, and it is the one noticed every day.
2. **Measure the spindle's usable body length** → that sets clamp separation.
3. **Spread the blocks until the supported span covers the clamps.** Aim for **zero overhang**, not
   one inch - the cube law makes an inch cheap, not free.
4. **Check the remaining travel against step 1.**
5. **Cut spacers to suit** (8" rather than 6", if spread that far).

⚠️ **Step 1 is still open.** The travel floor was never set as a number, and 246 mm is now confirmed
available - so the question is no longer "how much can we get" but "where does the 246 sit relative to
the spoilboard". That is a machine measurement, not a design decision.

### Which half moves - settled

| Fixed | Moving |
|---|---|
| **X carriage plate** (the blue one), bolted to the X-axis bearing blocks | Z bearing blocks |
| HGR20 rails, mounted on it | 5/8" spacer blocks |
| 1605 screw, BK12 + motor, BF12 | ball nut housing |
| | **Z plate** - **154 W × 175 H × 1/2"** - bolted to both the spacers and the nut housing, carrying the spindle |

The motor stays put and only the carriage travels. The Z plate picks up **two** interfaces - the
spacer blocks and the ball nut housing - which is what makes the shim below matter.

**The blue is layout dye, not a finish.** The X carriage plate is plain 1/2" aluminium sprayed for
scribing; **30 holes** to lay out on it.

| X carriage plate | |
|---|---|
| Size | **154 mm W × 407 mm H × 1/2"** |
| Width | ✅ **154 mm, confirmed 2026-09-30** - the same width as the X gantry end plates. **The Z plate is 164** as of 2026-10-02 and no longer matches |

📌 **154 mm recurs across the X end plate and this one, and it is not a coincidence.** The X end
plate's 154 is set by **two HGH20 blocks butted - measured 154.18 on 2026-10-02**; this plate
inherits it.

🔴 **The Z plate broke away from 154 on 2026-10-02 and is now 164.** It had only ever inherited the
number, and at 154 eight of its M5 counterbores broke out of the plate edge. **Do not "tidy" it
back into line with these two** - see the Z plate section. Worth knowing
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

### ❌ Do not lengthen the spacers - the question is closed twice over

Raised repeatedly on 2026-09-30, while the plate was provisionally 205 mm and the clamps overhung the
block run. **Both reasons to reject it still stand, and the second one ended the discussion:**

**1. An unbolted spacer end is a one-way support, not a stiffener.** The spacers carry no fasteners of
their own - they are clamped only by the M5 that runs from the plate into the bearing block, and past
the block ends there is nothing to bolt into and nothing behind them. The extra length would be
**unclamped bar in face contact with the plate**: it can push but not pull, so it stiffens in
**compression only** - one direction of the tipping couple and not the other. An unpreloaded one-way
contact opens and closes on every direction change, which is a hysteresis source, not a stiffener.

**2. 🔴 It was aimed at a problem that no longer exists.** At the settled **116 mm** clamp centres,
all four M8 rows sit at **±70.5 mm**, inside the **±76.2 mm** of the existing 6" spacers. **There is no
overhang left to support.**

📌 **And it never addressed the real constraint anyway.** The binding problem turned out to be the M8
tapped holes clashing with the M5 counterbores - two features **in the plate**. Spacer length has no
bearing on that, and the M5 positions are set by the blocks and cannot move.

📌 **Keeping them also keeps the matched pair.** Both are halves of one 12" bar with the 5/8" as
supplied - see below. A re-cut only preserves that if both new pieces come from a single bar.

📌 **It is also solving a problem that is not there.** The clamp bolts land inside the spacer run - see
the Z plate section above - so the overhanging plate is not carrying the load in the first place.
**Keep the 6" spacers as built.**

### Use M5 × 35, not M5 × 30

Through a counterbore in a 12.7 mm plate - leaving about 7.7 mm of material under a 5 mm head - plus
the 15.875 mm spacer is roughly 23.6 mm of grip. An M5 × 30 leaves only about **6.4 mm in the
bearing block**, 1.3 diameters, with no margin if a counterbore runs deep. The blocks have the
thread depth for 35 mm.

---

### ✅ The clamp mount geometry - settled 2026-09-30

- **Orientation.** The **100 mm dimension is front-to-back**, with the 80 mm bore centred
  in it leaving 10 mm of wall front and back; 55 mm is axial (vertical) and 120 mm wide, giving
  20 mm of wall either side of the bore. This follows from the "half of 100" term in the offset
  chain above and is consistent throughout.
- ✅ **Z plate thickness is 1/2" (12.7 mm)**, settled with the plate size.
- ✅ **The bolts run through the clamp into a TAPPED plate.** Measured: the **M8 × 80 stands 10 mm
  proud of the clamp's mounting face** when fully seated, so 70 mm is swallowed by the clamp. A
  12.7 mm plate cannot be through-bolted with that - the bolt never reaches the back face, so there
  is no nut - and there is nowhere for a nut to go anyway: the inner row has the spacer directly
  behind it and the outer row has open air.

#### 🔴 Tap the plate, and torque to ~15 N·m - not 25

**10 mm of engagement is 1.25 diameters.** In 6061 that develops roughly **60% of an M8 8.8's proof
load** - call it 10 kN of preload per bolt, **40 kN per clamp**, against a clamp reaction on the order
of 2-3 kN at peak cutting load. Ten times the margin, so **the engagement is fine.**

⚠️ **What is not fine is torquing it like an M8 in steel.** The aluminium thread is the limit, not the
bolt. **~15 N·m**, not the ~25 N·m an M8 8.8 would otherwise take. If you would rather not have to
remember that, **four M8 helicoils per clamp position** takes it to full spec for the price of a tap.

#### 🔴 The M8 tapped holes and the M5 counterbores share the plate's front face

**Both features are entered from the clamp side, so they compete for the same surface** - this is a
layout constraint, not just a depth one.

| | |
|---|---|
| M5 socket head counterbore | ~**Ø10** |
| M8 tapping drill / thread major | **6.8** / **8** |
| Bare non-overlap | (10 + 8)/2 = **9 mm** centre to centre |
| **Working minimum, with a web that survives the tap** | **12 mm centre to centre** |

📌 **Depth is in your favour and needs no separate check:** the M5 counterbore leaves ~7.7 mm of plate
under the head while the M8 taps 10 mm into 12.7 mm, so if they clear on the face they never meet.

✅ **Resolved 2026-09-30.** The M5 rows were measured and they *did* collide with the 144 mm layout, so
the clamp centres came in to **116 mm** and the M8 rows to **±45.5 and ±70.5**. Worst-case clearance is
**14.1 mm centre-to-centre**, about 5 mm of web. Full working in the Z plate section above.

---

## The X gantry end plates

**Two identical plates, 1/2" aluminium, 154 mm wide**, stopping at the **top of the X beam**. They
carry the X beam and ride the Y rails on four bearing blocks.

### 🔴 Reworked 2026-10-02 - the screw and stepper left this plate

The X axis gets a cast stepper frame like the others, mounted on an interposer on **top** of the X
beam and overhanging the end. **Three things therefore come off the X end plate:**

| Gone | Why |
|---|---|
| The **35 mm stepper shaft bore** | the shaft is up on the casting now, above the beam, not through the plate |
| The **stepper mount pattern** | the motor bolts to the casting's own flange |
| Everything in the stack-up **above +60** | the screw support and stepper no longer land on this plate at all |

✅ **Both plates stop at the top of the X beam, +60 from the Y beam top, and stay identical.** The
alternative was raising the far end by the interposer thickness to cover its end face - cosmetic -
while the stepper end could not be raised at all, the casting overhanging it. Letting the stepper
assembly hang unsupported costs nothing worth having: roughly **2.5 kg at ~70 mm is under 2 N·m**,
and the load that matters is screw thrust, which runs **along** the beam and is reacted by the
interposer's own bolt run rather than by anything beneath the overhang. **One drawing, one setup**
is worth more on a one-shot trip than covering an end face.

📌 **The four M8 into the top extrusion's corner bores sit below +60**, so nothing is lost by
stopping there.

✅ **The X interposer is 3/8", the same as Y** - settled 2026-10-02. One thickness across the
machine; see the casting section for why 3/8" is the right number and not merely an available one.

✅ **154 mm is set by the bearing blocks, and it is now measured: 154.18 mm for two blocks butted**
(2026-10-02, calipers - see
[`photos/y-bearing-blocks-butted-154.jpg`](photos/y-bearing-blocks-butted-154.jpg)). Each block is
**77.09 mm**. Anything wider eats usable Y travel at both ends.

🔴 **The number was right and the reason this file gave for it was wrong.** It used to read "two
HGH20 blocks end to end with **2-3 mm between**". There is no gap - 154 *is* the butted dimension.

#### The block is not one surface - 128.24 is the part that bears

**Measured 2026-10-02** - see
[`photos/y-bearing-blocks-machined-pads-128.jpg`](photos/y-bearing-blocks-machined-pads-128.jpg):

| | mm |
|---|---|
| Two blocks butted, **full body** | **154.18** |
| Two blocks butted, **machined pads only** | **128.24** |
| → each end cap | **12.97** |
| → each block's machined pad | **51.15** |

📌 **That cross-checks against the HGH20CA standard**, whose body length without end seals is about
50.5 mm - so the reading behaves like the real part rather than like a misread.

✅ **The functional floor for any carriage plate is 128.24 mm**, not 154. The end caps are seals and
scrapers; they carry nothing. A plate wider than 128.24 has full bearing on both pads.

⚠️ **A plate edge must land outside a pad, never partway across one** - a partial edge loads the
pad's corner instead of its face.

🔴 **154 still stands, but for the other reason.** Its constraint was never bearing coverage, it was
*"anything wider eats usable Y travel at both ends."* **Narrowing below 154 buys none of that back**,
because the blocks themselves are 154.18 long and they are what reaches the rail end. So 128.24 is a
floor already cleared by ~13 mm a side, not a new target.

*(An earlier version of this section said 154 was "the minimum, not a choice" and that there was "no
relief at the ends". Both were wrong - they came from treating the block as one surface. The 0.09 mm
of block standing proud of a 154 plate is **end cap**.)*

📌 **Recorded because of how it was nearly missed.** The 77 mm block length this file carried was
measured on the **Z** kit, and the Z kit is a different supplier from the one X, Y1 and Y2 share.
The two numbers happened to agree. **They did not have to** - see the kit note below.

### 🔴 The rails come from two different suppliers - do not quote one kit's dimension for the other

**Recorded 2026-10-02.** It is not one rail order:

| Axes | Kit |
|---|---|
| **X, Y1, Y2** | the same HGR20 kit, one supplier |
| **Z** | a **400 mm HGR20 kit from a different supplier** |

Both are HGH20-class and so far every dimension agrees - block length 77.09 against 77, the same
32 × 36 hole pattern, the same 30 mm stack. **That is an observation, not a guarantee.** They are
different parts from different makers and a clone's block length, height or hole pattern can differ
while the designation does not.

⚠️ **This nearly bit once already.** The 154 mm X end plate width - which the X carriage plate and
the Z plate both inherit - rested on a 77 mm block length measured on the **Z** kit. The X/Y blocks
turned out to measure 77.09, so nothing moved. Had the clones differed by a millimetre, three plates
would have gone to a one-shot mill trip at the wrong width.

**The rule: a dimension measured on the Z kit is a Z dimension.** Measure the X/Y kit separately for
anything that sets a plate.

### Vertical stack-up, from the top of the Y beam

| From the Y beam top | |
|---|---|
| Four M8 into the **top extrusion's** corner bores, **9 mm clearance** - start just above the Y beam top | 0 |
| **Top of the extrusion, and the top of the plate** | **+60 mm** |
| ~~Top of the ball screw support block mount~~ | ~~+80~~ - **on the beam's top face now, not the plate** |
| ~~Top of the stepper mount, shaft through a 35 mm hole~~ | ~~+140~~ - **on the casting now** |
| Y beam underside - the X beam's bottom extrusion ends here too | **−120** |
| **Bottom of the plate, level with the Y ball nut's mounting face** | **−182.5** |

**So the plate is 242.5 mm tall** - see the next section for where −182.5 comes from. It is ~70 mm
taller than the 170 the shop pack carried as a placeholder.

**The bottom extrusion is not bolted to the plate at all.** It sits alongside the Y beam, carried on
a shelf - see below. This is the half-overlap: only the top extrusion is above the Y beam, which is
what keeps the whole machine low.

### ✅ The plate height: 242.5 mm, set by the Y ball nut - closed 2026-10-02

**The bottom of the plate is level with the downward-facing mounting face of the Y ball nut**, so the
nut's own fixing can tie the plate to a sole plate across its bottom. That is what sets the height;
nothing else was asking for a particular number.

| Term | mm |
|---|---|
| Beam underside to the nut's mounting face, **as built** with BK12 / BF12 **5 mm off the beam** | **58** |
| The 3/8" interposer replaces that 5 mm standoff: 9.525 − 5 | **+4.525** |
| **Beam underside to the nut's mounting face** | **62.5** |
| Y beam height, two `30-6060` stacked | +120 |
| **Below the Y beam top** | **182.5** |
| Plus the plate above the Y beam top | +60 |
| **PLATE HEIGHT** | **242.5 mm** |

📌 **The 58 is an as-built measurement off the machine; the 4.525 is arithmetic off the settled 3/8"
interposer.** The two halves are different kinds of number and the chain is only as good as the 58.

⚠️ **This was briefly computed at 245.7 on a 1/2" interposer.** The interposer is **3/8"** - settled
2026-10-02 and confirmed again when this section was written. **The 1/2" figure is dead; if 245.7
appears anywhere it is stale.**

#### The 1/4" sole plate, and one bolt set doing two jobs

A **1/4" plate across the bottom of the end plate**, horizontal. The ball nut hangs under it, and
**the nut's own mounting bolts pass up through the sole plate and into tapped holes in the end
plate's bottom edge** - so one set of fasteners both mounts the nut and ties the sole plate to the
end plate. No separate bracket.

**Why the plate bottom had to be level with the nut face for this to work:** the sole plate needs one
flat seating that takes the end plate's bottom edge and the nut's mounting face at the same height.
Any step between them and the sole plate becomes a bent or shimmed part.

⚠️ **Open: the sole plate's footprint.** It is 154 mm wide to match, but its depth in Y and its hole
pattern both come off the **ball nut housing's flange**, which is not recorded in this repo. Measure
the housing before drawing it.

⚠️ **These are edge taps into 12.7 mm, so the M6 wall rule applies** - see the joining-plate tie
below. **But the size here is not free**: it is set by the nut housing's bolt holes. If the housing
wants M8, the 2.35 mm of wall each side is below the usual 1.5-2 D of material around a tapped hole,
and the fix is a clearance hole through the sole plate into a **nut or an insert** rather than a tap
into the plate's edge. **Resolve this with the housing in hand.**

#### ✅ The tail does not reach the front riser - travel runs out first

The plate now hangs ~62 mm below the Y beam and sweeps the full Y travel at that depth, which raises
a clearance question that did not exist when the plate stopped near the blocks. **It is already
closed by the travel limit:**

> **Max Y travel is reached when the front face of the X end plate is even with the end of the beam,
> which is where the riser starts.**

So the plate's lower tail stops at the beam end and never enters the riser's plane. **The riser is
not in the picture at all** - it is not a clearance to design around, and the 62 × 50 window has
nothing to do with this plate.

📌 **Noted as a travel fact, not a measurement I took.** It comes from the axis's own limit, so if
the Y travel is ever extended - soft limits opened up, or the blocks repositioned - **this is the
check that has to be redone.** It is also a separate question from the already-open "how far past the
front riser plane does the spindle reach", which is about the spindle at low Z, not the end plate.

✅ **The load path is in the right plane, which is why a 122 mm tail below the shelf is not a
worry.** Screw thrust runs along **Y**, which lies **in** the plate's plane, so the tail below the
bottom extrusion works in-plane shear rather than as a cantilever in bending. The Y bearing blocks
pick it up ~90 to ~150 mm above the nut.

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

Rear bolt pair **15 mm from the plate's back edge**, which puts the top extrusion's back face
**flush with the plate's back edge**. The bolt is still 15 mm in from the beam's back face, into the
same corner bore - only the plate shifted under it. **Both pairs, from the back edge: 15 and 45.**
(The 45 follows from the corner bores being symmetric in a 60 × 60 - four corners at 15 from each
face. Only the 15 is anchored in a stated dimension; transfer-punch them anyway, per the drawings
convention for extruded features.)

Back-mounting matters because the forward-hanging mass acts at an arm from the **block group's
centroid** at Y 77:

| Beam position | Beam centreline, from the back edge | Arm | Load per block pair |
|---|---|---|---|
| **Back, flush (chosen)** | **30 mm** | **92 mm** | **1.19 × F** |
| ~~Back, 10 mm in~~ | ~~40 mm~~ | ~~102 mm~~ | ~~1.32 × F~~ |
| Centred | 77 mm | 139 mm | 1.8 × F |

**Roughly a third less than centred**, for free - the block travel sets the envelope either way, and
the plate's 154 mm is set by the butted blocks, so none of this changes the outline. **This is a
hole position, not a size.**

#### 🔴 Changed 2026-10-02 - the 25 mm is dead, and why it was abandoned

It used to read *"25 mm from the plate's back edge, putting the beam's back face 10 mm in"*, and the
reason given was that **the 6.35 mm back joining plate takes most of that, leaving 3.65 mm.** That
cover was the only justification the file ever offered for the 10 mm, and it does not survive
examination:

- **It is not structural.** The joining plate's end face is a 6.35 mm edge; the end plate standing
  behind it is end-grain bearing and carries nothing. The joining plate's real fixing is the T-nut
  run along its length.
- **The design already tolerates overhang at that edge.** The shelf bar's holes are dimensioned from
  the **beam front** on a 76.2 mm bar, so it overhung the plate's back edge by ~6 mm even at 25.
  Flush makes that ~16 mm. Harmless, and it shows the edge was never a "nothing may project past
  this" line.
- **What it did buy was practical**, and it is what was given up: the plate edge was the rearmost
  surface, and it registered the joining plate during assembly.

**The exchange: 10 % off the worst block load for the loss of a 3.65 mm cover.** ⚠️ Those two halves
are not the same kind of claim - the 10 % is arithmetic off this file's own proportional model, the
"not structural" is reasoning from the joint geometry and has not been measured.

📌 **One thing flush gains that the old layout could not have.** With the beam's back face in the
plane of the plate's back edge, the joining plate now lies **directly over the plate's 12.7 mm back
edge**, so it can be tied to the end plate with M8 tapped into that edge - see the question below.
At 10 mm in, the joining plate stood clear of the edge and no such tie existed.

⚠️ **Edge distance check**: 15 mm to the back edge with a 9 mm clearance hole leaves 10.5 mm of
material. Fine, but it is now the plate's tightest edge distance - do not let the hole drift
outboard.

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

### ✅ The two plates are now genuinely identical

**Reworked 2026-10-02.** With the screw support and the stepper both off this plate, the thing that
used to differentiate the two ends is gone.

❌ ~~"The plate at the idle end gets no 35 mm hole and no stepper mount holes. Everything else is
common."~~ **Neither end has either any more**, so there is no idle-end variant - one drawing, one
setup, two identical parts.

📌 **The BK12-and-BF12-share-a-pattern note is retired too**, along with the "35 mm is enough for
the coupler" working: the coupler now lives inside the casting, not in a bore through this plate.

✅ **And the 35 mm ambiguity resolves itself.** This file used to warn that two different 35 mm
holes would exist in the X end plate - a stepper shaft clearance and the **encoder sensor bore**
from
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md).
**Only the encoder bore remains**, so "the 35 mm hole in the X end plate" is now unambiguous.

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

🔴 **The 2026-10-02 rework put three more parts on this trip.** The list had been shrinking; it is
not any more:

| Part | Why the mill |
|---|---|
| **Two Y front plates**, 1/2" | the 8-bolt corner-bore pattern *and* the 62 × 50 window |
| **The 1200 mm rear plate**, 1/4" steel | two 8-bolt patterns a metre apart that must match extruded bores - and the part may exceed the machine's X travel |
| **Interposer bars**, 60 × 150 × 3/8" - two for Y, plus X | six tapped M5 under a bearing face and six flange clearance holes, all in a small part |

❌ ~~**The four Y risers are already made and in service** - they are not on this list.~~
**Reversed 2026-10-02 - all four are scrapped.** The front pair is remade with the window; the rear
pair is replaced by the single 1200 mm plate.

Still to make, but **no mill needed** - T-slot clearance holes throughout: two **12" × 1 m × 1/8"
steel** outboard plates and three **46 mm × 1 m × 1/4" 6061** front strips, one per beam.

⚠️ **The outboard plates are steel now**, so that "no mill needed" afternoon on roughly 25 holes
per plate runs several times longer than it would have in aluminium. Still a drill press job, but
budget for it.

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

### From the 2026-10-02 stepper frame rework - all unmeasured

- ✅ ~~**The as-built BK12 screw axis height**~~ **Closed 2026-10-02**, and reframed: the number
  that matters is the **10 mm** between the beam underside and the nut top, with the supports
  mounted 5 mm above the extrusion. The casting hangs below the beam, so that clearance grows.
- ✅ ~~**The casting's 6-hole pattern against the T-nut holes**~~ **Closed 2026-10-02.** Measured at
  columns 7 / 53 and rows 28 / 58 / 71. The columns clash with the T-slots at 8 mm, which is why
  the bar runs ~30 mm past the casting and the four T-nut bolts live in the overhang.
- ✅ ~~**The two strip widths either side of the window**~~ **Measured 2026-10-02: 19 mm outboard**,
  and it now derives from the geometry too. The fins are **100 / 200 over 302**, both halves out of
  the measured 302 mm square with 2 mm for the kerf.
- ✅ ~~**The window's horizontal position does not reconcile**~~ **Closed 2026-10-02 - it was my
  arithmetic, off a wrong column position.** With the M8 columns at **35 and 65** rather than 20
  and 50, the beam spans X 20-80 and its centreline is X 50, so a 62 mm window centred on the screw
  runs **19 to 81** - exactly the 19 mm strip measured off the template. Nothing about the casting
  or the bar had to move.
- ✅ ~~**The M8 column position**~~ **Settled 2026-10-02 at 20 / 50.** The riser standing 1.8 mm
  proud of the side plate is wanted, and they never touch. The curb condition moved to the box -
  below.
- ⚠️ **Terminate the side curb short of the front riser's station** so the curb bears on the side
  plate rather than being held out by the riser. A box decision, free while the box is unbuilt.
- ✅ ~~**T2's edge distance, on the template**~~ **Closed 2026-10-02.** X 25 and 170 on the Y 30
  line both check out against the physical template - photo committed. **The front fin's geometry
  is fully settled.**
- 🔴 **Whether the Laguna can hold the HEIGHT datum across a 1200 mm part.** Bed size is not travel,
  and the question is not whether the part fits - it is whether the two 8-bolt patterns' relative
  height survives a reposition. **The budget is well inside 1 mm**, that being the float the 9 mm
  holes give; past it the plate wins and a beam end has to be jacked. Gated on the mill model and
  DRO item below.
- ⚠️ **A sensor reading at the min-Y end of the tape**, with the stepper in place, against
  mid-travel. Before 3 m of one-shot PSA goes down.
- ⚠️ **Which extrusion face the casting bolts to**, recorded here because this file says "a face"
  rather than naming it. The ball screws run underneath, so the underside is the expectation, not a
  measurement.
- ⚠️ **The curb channel width** - dimensioned around 6.35 mm, now taking 3.175 mm, or 3.04 mm if
  the sheet arrives at a true 11 gauge.
- ⚠️ **The delivered thickness of the 1/8" sheet.** The listing says both 1/8" and 11 gauge, which
  differ by 0.135 mm. Harmless structurally, but the curb channel and the riser-proud check key off
  it. **Caliper it on arrival and write the number here.**
- ✅ ~~**Two assumed terms in the rear plate length chain**~~ **Closed 2026-10-02.** The Y rails are
  on the inside faces facing each other, and X / Y1 / Y2 share one HGR20 kit, so the measured 30 mm
  stack applies to all three. The ~1205 chain rests on no guesses.
- ✅ ~~**Is the X end plate really 154 wide**~~ **Measured 2026-10-02: 154.18 for two blocks
  butted.** The number stands; the "2-3 mm between the blocks" that this file gave as its reason
  never existed.
- ✅ ~~**The X end plate's height and outline**~~ **Closed 2026-10-02 at 242.5 mm.** Set by putting
  the plate's bottom level with the Y ball nut's downward mounting face: 58 mm as built, plus 4.525
  for the 3/8" interposer, plus the 120 mm beam, plus 60 above the beam top. The shop pack's 170 was
  a placeholder and is superseded.
- ✅ ~~**Whether the plate's lower tail clears the front riser across Y travel**~~ **Closed
  2026-10-02 - it never gets there.** Max Y travel is reached with the plate's front face level with
  the beam end, where the riser starts. **Redo this check if Y travel is ever extended.**
- ⚠️ **The Y ball nut housing's flange footprint and bolt pattern** - not recorded anywhere in this
  repo, and it sets the 1/4" sole plate's depth, hole pattern **and the bolt size tapped into the end
  plate's bottom edge**. At M8 the 12.7 mm edge gives only 2.35 mm of wall each side, so the housing
  may force a nut or insert rather than a tap. **Measure the housing before the sole plate is drawn.**
- ⚠️ **Rib under the full 1200 mm of rear bottom-edge bearing.** Decide before the skins are cut.

### Carried forward

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
  tapered base gives the bolt spacing directly, so there are no L brackets. See "The lateral fix".
- ✅ ~~**Front corner three-way convergence**~~ **Closed 2026-09-30** - the front and back tongues run
  long and lap the side tongues' ends; nothing is notched. See "The lateral fix".
- 🔴 **How far past the front riser plane the spindle reaches**, and whether it fouls the widened fin
  at low Z. Confirmed to pass the plane; the amount is unmeasured. **Needed before the front plates are
  cut.** Four numbers listed under "The lateral fix".
  **Worse as of 2026-10-02**: the cast stepper frame and a NEMA 23 now occupy that end too, so the
  question is no longer only "does the spindle clear the fin" but "does it clear the fin, the
  casting and the motor". Add the casting's envelope to the four numbers.
- **Whether the front fins need the rib layout fixed first** - the bottom-edge bearing wants blocking
  under the full 203 mm base.
- ✅ **How nod is adjusted - answered 2026-09-30.** The question was whether the spacer M5 counterbore
  pattern clears the clamp footprint. **It does not clear it by position alone** - the M8 column at
  50 mm and the M5 column at 41.5 mm are only 8.5 mm apart and overlap at equal height - so the
  clearance is bought **vertically**, by bringing the clamp centres to **116 mm**. Worst case is
  **14.1 mm centre-to-centre**, about 5 mm of web. **No tram sub-plate, no added moment arm.** Full
  working in the Z plate section.
- **The mill's model number and whether it has a DRO** (2-axis or 3-axis) - expected ~2026-10-04. If there is no DRO, the drawings want dimensioning differently.
- 🔴 **Can Garen's mill traverse ~1200 mm in X?** The direct question, and the one the rear plate waits on: the M8 patterns sit at **both ends of a 1200 mm plate**, so either the machine reaches both or the part is repositioned mid-job - and a reposition is where the height datum between the two patterns gets lost. Ask the travel, not the model number; the model is only a proxy for it.
- **Z travel floor** - where the confirmed 246 mm sits relative to the spoilboard. A machine
  measurement, and the one item the travel budget still waits on.
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
it.** That settles whether the beam plate should be 1/4" or 3/8", and the plate is bolt-on precisely
so the swap stays cheap.

📋 **Procedure: [`../commissioning/stiffness-test.md`](../commissioning/stiffness-test.md).**
⚠️ **It is not a single number.** One reading on the nose is a *total*, and a total cannot say which
part of the stack is moving - which is the entire question. The procedure uses six indicator
positions and subtracts.
