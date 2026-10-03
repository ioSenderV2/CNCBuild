# Y beam support and the cast stepper frames

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

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
| Front plates | Tapered fins, 3/8" | Tapered fins, **10 mm** (measured stock, see below), with a **62 × 50 mm window** for the casting |
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
