# The lateral fix: tapered front fins, a full-width back panel

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

✅ **Decided 2026-09-30.** The full-height outboard plate took over the **fore-aft (Y)** support, and
[`outboard-plate.md`](outboard-plate.md) records it at ~670 000 N/mm in-plane against the
risers' ~1 500. What it did not
touch is **across the machine (X)**, which is out-of-plane for that plate and therefore still carried
by the four risers alone, 3" wide, at the two ends only.

🔴 **Do not confuse this with the gusset recommendation the outboard plate superseded.** That one was
a triangle in the **Y-Z plane**, doing the job the outboard plate now does far better. This is the
**X-Z plane** - the riser's own face - and nothing covers it. Both are called "gussets" and they are
not the same part.

## Front: widen the riser in its own plane

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

## Cut two from one 12" square, and reference off the factory edges

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

- **No bed area.** The fin is a 10 mm slice in the riser's own plane, not a wedge intruding into the
  work volume.
- **No travel.** It lives in the plane of the end plate, which the gantry already cannot reach past.

## ✅ The fin, fully dimensioned - 2026-10-02

**The taper is pinned, so everything below is arithmetic rather than judgement.** Datum is the
**top-outboard corner**, the two factory edges, per the layout rule above. X runs inboard, Y runs
down.

| | |
|---|---|
| Top width | **100 mm** |
| Base width | **200 mm** |
| Height | **302 mm** |
| Thickness | 🔴 **10 mm** - the measured stock, see below |
| Taper | corner to corner, **18.33° from vertical** (rate 0.3311 mm per mm) |

### ✅ The stock is 10 mm, not 1/2" - and that is acceptable, by this file's own test

**Measured 2026-10-02: the 302 mm square is 10 mm thick.** It is **not 3/8"** either - 3/8" is 9.525,
so this is metric plate, 5% thicker than 3/8" and 21% thinner than the 1/2" this file had specified.
✅ **Decision: stay with 10 mm.**

✅ **The fin drawing is untouched.** Every dimension in the table above - 100 / 200 / 302, the taper
angle, columns 35 and 65, rows 15 / 45 / 75 / 105, the window at X 19 and 81 - is **in-plane**, and
none of it is a function of thickness. Nothing has to be redrawn.

**What the thickness actually costs, and the two directions are not the same:**

| | Scales as | 10 against 12.7 |
|---|---|---|
| **In-plane (X-Z), the fin's real job** | **t** | **21% less** |
| Out-of-plane (fore-aft, Y) | t³ | 51% less |

🔴 **The 51% is the frightening number and it is the one that does not apply.** This file records
the fin's job as carrying **across the machine (X)**, which is *"the riser's own face"* - the X-Z
plane. That is **in-plane** loading, where stiffness is linear in thickness. The out-of-plane
direction is **fore-aft**, and that was handed to the full-height outboard plate at **~670 000 N/mm
in-plane against the risers' ~1 500** - about 400 times stiffer, so the fin's contribution there was
already noise.

✅ **And this is exactly the condition the earlier 3/8" discussion named.** That section says a
thinner riser *"would have been acceptable **only if** the full-height plate took the fore-aft load
in-plane"*, and concluded 1/2" only because *"the Y risers went to 1/2" and are made, so the coupling
never had to be managed."* **These fins are not made, and the full-height plate does take the
fore-aft load in-plane.** The stated condition is satisfied, so this is not a reversal of that
decision - it is that decision's own escape clause being used as written.

📌 **It also makes the 60.5 × 50 window easier to cut**, which is a live question - 10 mm of
aluminium is a materially easier jigsaw or router job than 12.7.

✅ **The 1.8 mm proud figure is unaffected - confirmed 2026-10-02.** It comes from the **plate width
and the offset from the vertical edge to the M8 bolt column**, both in-plane. **Thickness is not a
term**, so the 10 mm stock does not disturb it and the curb condition carried to the box's list
stands as written.

🔴 **But the 1.8 itself was stale, and is now corrected to ~16.6 - 2026-10-02.** It had been
computed off a superseded M8 column at **20**. With the column at **35**, the corner bore 15 in from
the beam's outboard face puts that face at X 20, so **20 mm of fin overhangs it**, and the side plate
takes about 3.2-3.4 of that back:

| | |
|---|---|
| M8 column from the fin's outboard edge | **35** |
| Corner bore inset in the `30-6060` | − 15 |
| **Fin overhanging the Y beam's outboard face** | **20 mm** |
| Side plate, **1/8" nominal** | − 3.175 |
| **Fin proud of the side plate's outer face** | **16.825 mm** |

⚠️ **3.175 is the nominal, and the delivered sheet is still an open item.** A 3.36 was floated
on 2026-10-02 and **withdrawn as a guess** - it is not a measurement and should not reappear. If the
sheet arrives as **11 gauge (3.04)** rather than 1/8", the figure becomes **16.96**. Either way it is
~17 mm, which is what the curb decision turns on; **caliper the sheet on arrival and settle it here.**

📌 **Second part this session to come back metric where the file assumed imperial** - the Z
spacers read 16.41 against a nominal 5/8". **Caliper the stock, do not trust the fraction it was
sold as.**

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

**The 60.5 × 50 window:**

| | |
|---|---|
| Outboard edge, from the fin's outboard edge | **X = 20** - on the beam's outboard face |
| Inboard edge | **X = 80.5** |
| Top edge, below the fin's top | **120 mm** - the beam's own height, i.e. the underside of the lower extrusion |
| Bottom edge | **170 mm** - ⚠️ 50 mm height is a **guess**, see below |

✅ **The window is ALIGNED on the beam's outboard face, not centred on the beam - decided
2026-10-03.** The beam spans X 20-80. Putting the window's outboard edge on **X 20** rather than
centring 62 mm about X 50 does three things at once:

| | Centred, 62 wide | **Aligned, 60.5 wide** |
|---|---|---|
| Window | X 19 - 81 | **X 20 - 80.5** |
| Outboard strip | 19 | **20** |
| Clearance over the 60 mm casting | 1 each side | **0 outboard, 0.5 inboard** |

🔴 **The point is that it puts the clearance where there is room for it.** The outboard side is the
tight one - it is the factory edge, and the side plate's end lands on it - while inboard the fin's
tapered edge is out past X 150 at the window's height. **All the rotation clearance now falls
inboard.**

✅ **And it closes the breakout.** The side plate's end occupies X 16.825 to 20, so a window edge at
X 20 is **flush with that plate's inner face** instead of cutting 1 mm into its band.

🔴 **The width is a slip fit, NOT the rotation clearance - corrected 2026-10-03.** The casting is
**60 mm** wide in a **60.5** window, which is 0.5 mm total and deliberately little. That is all it
needs, because **the casting does not rotate in the plane of the plate.** It rotates **fore and
aft**, about an axis running across the window - so the clearance the rotation consumes is the
window's **height**, which is the 40.49 under the bar against a 27 mm casting.

📋 **The assembly sequence, and the plate is scrap if it will not go:**

1. **Approach from BEHIND the fin** - from inboard, the beam side.
2. **Hold the casting UPSIDE DOWN.**
3. **Insert the top of the stepper motor bracket into the window first.**
4. **Rotate CCW** until the **bottom of the casting lands flat on the interposer bar**.

⚠️ **So if it binds, the remedy is HEIGHT, not width.** Opening the window sideways buys nothing -
the casting is already only 0.5 mm narrower than the hole and the rotation never uses that axis.
**This is the first thing the plywood mockup is for.**

🔴 **Corrected 2026-10-02: the top edge is 120, not 129.5.** It was recorded as *120 + the
interposer thickness*, on the reading that only the **casting** passes through the window. It does
not: [`y-beam-support.md`](y-beam-support.md) specifies the bar's outboard end **30 mm past the fin's
outer face** so that *"the casting and bar protrude through the window together"*. The bar's top face
**is** the beam underside, so the window top is the beam underside - **120** - and the interposer
thickness does not enter it. **The window top does not move if the bar ever goes to 1/2".**

🔴 **Nothing rests on anything - the whole assembly HANGS, and that is the point.** The load path,
top to bottom:

1. **Six M8 into slide-in T-nuts** in the beam's bottom-face slots. Everything below is suspended
   from these.
2. **The interposer bar**, hanging from those bolts, its top face against the beam underside.
3. **The casting**, bolted up into the bar with M5 and hanging from *its* bolts.

📌 **So the bar is the higher of the two parts, and the window has to pass it.** The 129.5 figure came
from imagining the casting resting on a bar that stops at the plate - it does not rest, and the bar
does not stop. The bar continues through the window and the casting hangs off it, past its end, which
is what the stepped foot is for.

📌 **The 62 mm width is the same fact from the other side.** The bar is **60 mm** wide, so a 62 mm
window clears it by **1 mm a side** - the same 1 mm the window leaves against the 60 mm extrusion end
it is centred on. Two parts of the same width pass through it.

✅ **The 50 mm height is no longer a budget - it is two stacked clearances plus rotation room.**
Given 2026-10-03:

| | mm |
|---|---|
| Upper band: the **interposer bar** passing through, 3/8" | **9.525** |
| Lower opening, the remainder | **40.49** |
| → the **casting**, as it sits in the window | **27** |
| → **surplus, and it is the point** | **13.49** |

🔴 **The surplus is what the casting is rotated into.** It does not drop straight in. That is why the
window is not simply 9.525 + 27 = 36.5, and it retires the earlier note that 50 was a guess expected
to shrink. ⚠️ **Mark the bar's underside on the plate** - 9.525 below the window top - because the
lower opening is the only part the casting can use. **A plywood mockup is being cut to find the real number** - see the plate list in
[`drawings/README.md`](drawings/README.md). Nothing downstream depends on it: the window's tight
dimension is the 19 mm outboard strip, which is set by the width, and the bottom edge at 170 is far
from the 61 mm tongue at the plate's base.

## 🔴 The 60.5 × 50 window, and why the taper does not help it

**Added 2026-10-02 when the steppers moved to the front.** The cast stepper frame passes through the
front plate, so each fin needs a **60.5 mm wide × 50 mm tall** rectangular window below the beam.

**The finding that matters, and it is assumption-free:** the window's tight side is the **outboard
factory edge**, and **the taper does not rescue it** - the taper adds material *inboard*. Widening
the top of the fin is the only thing that buys outboard material. That is why the window is aligned
on the beam face rather than centred: it spends the clearance inboard, where the taper has already
provided it.

⚠️ **And the nesting is what pays for it.** Two identical-by-rotation halves only come out of one 12"
square when **top + base = 12**. So 3" / 9" works, and **4" / 8" works**, but 4" / 9" needs a 13"
blank.

⚠️ **The 20 mm strip is not 20 mm of free material - the side plate's end uses the outer part of
it.** The 1/8" × 12" outboard plate lies against the beam's outboard face at **X 20** and is
**3.175** thick, so its end occupies **X 16.825 to 20**. About **16.8 mm** of the strip is clear
fin, and the rest is under the plate. ⚠️ **3.175 is nominal** - if the sheet arrives as 11 gauge the
band moves.

✅ **Closed by the realignment, 2026-10-03.** When the window ran X 19 to 81 its outboard edge
fell **inside** the plate's band and broke out into the space the plate's end occupies. At **X 20**
the window edge is flush with the plate's inner face and the overlap is gone. The thing to watch on
the mockup
before the real plate is cut.

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

## ✅ The M8 columns sit at 35 and 65 mm from the factory edge

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

📌 **The rear needed the same thought and got it 2026-10-03** - the plate's length is now derived
and fixed at **1211.75**, not a window. See "The length" under the rear plate.

## The second gain is bolt spacing, and it is the bigger one

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

### ✅ T2 at 170

**At Y 30, T2's perpendicular edge distance is 19.1 mm** - a little over 2 × the 9 mm hole
diameter, and confirmed good on the template.

✅ **Y 30 is one datum across all three plates** - the front fin's two bolts, the side plates' row
and the back plate's row all sit at 30 mm above the plate's bottom edge, 31 mm below the top of the
61 mm tongue. One number to transfer instead of three, which is worth more than the millimetre it
moved. **The pitches differ because the plates do**: 100 mm on the side plates (eleven over
1000 mm), ~150 mm on the back plate (eight over 1211.75 mm). Both are correct; neither is the other's
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

## Back: one 1211.75 mm steel plate, replacing both risers and the panel

✅ **Decided 2026-10-02.** The two rear risers are **scrapped**. One plate spanning the full machine
width does both jobs - carrying the two beam ends down to the box, and acting as the shear panel
that turns the rear face from a portal frame with two bending legs into a diaphragm.

| | |
|---|---|
| Plate | **1211.75 mm × 12" × 1/4" hot-rolled A36 steel** |
| To the beams | **8 × M8 into each beam's corner bores** - the same proven pattern, 16 bolts total |
| To the box | **8 bolts through the back tongue at Y 30**, 150 mm pitch from X 80.875, plus bottom-edge bearing over the full 1211.75 mm |
| Also carries | **BF12 on its inside face**, 4 × M5 tapped into the plate, one per beam |

- **It costs no travel** - the gantry stops well forward of the rear plate plane, and the spindle sits
  ~109 mm ahead of the carriage plate.
- **Bonus: a rear chip fence** the width of the machine.

### 🔴 This reverses the 2026-09-30 rejection, and three of its four grounds lapsed

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

### ⚠️ On the datum, and a correction to how it was first described

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
right; the conclusion drawn from it was not. **A 1211.75 mm steel plate standing on edge is not a
conforming object**, and the single ratio hides the fact that it is rigid in one of the modes that
matters.

### What the plate actually controls, mode by mode

Treating it as a beam 1211.75 mm long with a 305 × 6.35 section:

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

### 🔴 The tolerance this puts on the drilling

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

### The length: 1211.75 mm, settled 2026-10-03 - it is a TARGET now, not a window

✅ **Decided: the plate runs FLUSH with the outboard plates' outer faces, so it is 1211.75** - the
upper bound of the window below, taken exactly. The window closed because of what it does to
**Sheet 7's coordinates**: with the WCS on the plate's lower-left corner, the Y2 beam's eight bores
and four of the BF12 holes are **absolute from the plate's left edge**, so the plate's length is a
datum rather than a dimension. Cut it over-long and the Y2 station is out by the excess.

📌 **Why flush rather than butted between the two side plates.** Butting gives a rounder
1205.4 and puts Y1's own corner back on X 0, which is how Sheet 7 was first drawn. It also lands the
outermost bores exactly on their 15 mm edge-distance minimum with nothing left over for a saw cut
that comes up short. The overlap buys **3.175 mm of edge distance at the eight most loaded holes**,
and the beam ties the side plate and the rear plate to itself regardless - side plate on its outboard
face, rear plate on its rear face - so the corner joint between them carries nothing either way.

⚠️ **The chain below is still a DERIVED NOMINAL, not a measurement.** The real number comes off
the assembled machine standing on a flat surface, exactly as the box width does. It is written down
because it gates a purchase - the stock has to be ordered before the machine is standing - and
because every X on Sheet 7 now hangs off it.

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

🔴 **The window was about 7 mm wide, and the plate is pinned to its top:**

| Bound | mm | Set by |
|---|---|---|
| **Minimum** | **~1205** | Edge distance. The outermost M8 sits 15 mm in from the beam's outer face; a shorter plate eats into that |
| **Chosen** | **1211.75** | Flush with the outboard plates. Buys 3.175 of edge distance over the minimum and squares the corner |
| **Maximum** | **~1212** | Past the outboard plates' outer faces the **rear plate** becomes the proud member at the corner - the direction curb bearing cannot take |

📌 **"1200 mm" was a round number, not this calculation, and it has been retired** - every file
and every sheet now carries **1211.75**. The registry derives it: REAR_PLATE_L = Y_BEAM_GAP +
2 × Y_BEAM_ASSY_W.

✅ **A 48" sheet (1219.2 mm) covers it** with 7.5 mm of trim - but that is the entire margin, and
there is now no slack to give back, because the length is a datum. **60" removes the question** and
leaves an offcut, which is the better buy on a part cut once.

✅ **Both of this chain's assumed terms were confirmed 2026-10-02.** The Y rails are on the beams'
**inside faces, facing each other**, and **X, Y1 and Y2 all run the same HGR20 kit**, so the 30 mm
rail-and-block stack measured on X applies to both Y beams. The chain above is nominal only because
the machine has not been assembled and measured - not because any of its terms are guesses.

### ⚠️ Open: can the mill hold a datum across 1211.75 mm

Two bolt patterns a metre apart, both of which must match extruded corner bores, on a **4' × 1'
manual-XY** mill. Bed size is not travel. If the part has to be repositioned mid-job the datum is
lost exactly where it is most needed. **Gated on the mill model and DRO question already in the open
items**, expected ~2026-10-04.

### ⚠️ The bottom-edge bearing now runs the full 1211.75 mm

So the rib under it has to as well. The box is built last, so this is free - but it joins the list
of things that must be decided before the skins are cut.

⚠️ **The back panel does not cover the front.** The load path from a gantry parked at min-Y back to
that panel runs sideways through the Y beams - their 60 mm dimension, not their 120 mm - and the
outboard plates contribute nothing laterally, that being their out-of-plane direction. So the front
fins are carrying a front-position gantry largely alone. That is why the front is taken to 200 mm rather
than left minimal. *(Reasoning from the 60-vs-120 proportions; the 30-6060 section about the vertical
axis has not been looked up.)*

## The tongues that back both

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

## 🔴 Open: how far past the riser plane the spindle reaches

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

## Span deflection: not a problem

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
