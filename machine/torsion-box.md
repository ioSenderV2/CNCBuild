# The torsion box and its base

What the machine stands on. The box carries the two Y beams; the base carries the box on **three
points** and is also the pallet it travels on.

The box's *interface* to the Y beams - the laminated outer wall, the 60 mm curb and the bolt row -
is not here. It lives with the plate it belongs to, in
[`outboard-plate.md`](outboard-plate.md) under "How it lands on the
torsion box". Read that first; this file is everything below the top skin.

---

## The box

| | |
|---|---|
| Skins | **19 mm Baltic birch**, top and bottom - 25 mm is available, see below |
| Grid | **19 mm strips, 100 mm high**, between the skins - **egg crate**, see below |
| Depth overall | **138 mm** (19 + 100 + 19) |
| Fill | **Sand in the cavities** - filled **last**, on site |
| Outer walls, **all four sides** | **Two 19 mm laminations, 38 mm total**, the outer one standing **60 mm proud** of the top skin - see the Y beam interface |

✅ **Decided 2026-09-30: the doubled wall runs the whole perimeter, not just left and right.** It
began as the left/right detail that captures the full-height outboard plates. The front and back now
get it too, because the **front taper fins and the full-width back panel need the same backing face**
- see [`lateral-stiffness.md`](lateral-stiffness.md). Three consequences, all good:

- **One detail everywhere** instead of two. Inner web between the skins, outer lamination 180 mm tall
  standing on the bottom skin and 60 mm proud, aluminium bolted through it.
- **The front and back tongues are the continuous ones.** Each runs the full width and **19 mm past
  the front post tenon**, covering the end grain of the side tongue in a butt joint - so the side
  tongues die into them, not the other way round. That is what resolves the front-corner convergence
  in the riser file. ⚠️ The butt joint itself is end grain onto face and is a weak glue joint; it is
  not load path, so do not make it one.
- **It resolves the ⚠️ under "Ledge depth"** below, which anticipated exactly this. Every ledge is
  now 38 mm, the tenons shrink accordingly, and the **back post's single-sided shoulder roughly
  doubles** - which fixes the one wart in that section rather than working around it.
- **It is the deep back-edge member** the sag section asks for. The back wall becomes a composite
  ~180 mm deep along the whole back edge, on the span that is supported only at its midpoint.

⚠️ **The grid spacing is not decided.** Every tenon rises into the cavity, so no rib may cross
one - but that lands differently for the front and back posts. See "What the tenons ask of the
grid" below.

### The ribs are egg crate - half-lapped both ways, not blocking

✅ **Decided 2026-09-30.** Continuous ribs in both directions, half-depth notches at every crossing.
The alternative considered was full-length ribs one way with blocking between them the other.

**Why, for this box specifically:** the three support points put the back-centre post half a machine
width inboard of the back corners, so load has to travel **diagonally** to reach it. That needs
two-way plate action, and only continuous ribs both ways give it. Blocking would make one axis a
proper continuous web and the other a row of **butt joints** - plywood edge glued to face, at every
junction - leaving a strong axis and a weak one.

Two build reasons reinforce it: an egg crate **self-jigs**, assembling square and holding its own
spacing with no clamps, so the whole grid can be checked flat on a reference before either skin goes
on; and only the notch positions are critical, where blocking needs every piece cut to length with
the errors accumulating.

#### Four things to get right

1. ⚠️ **Cut the notches to the measured sheet thickness, not to 19 mm.** Baltic birch sold as 19 mm
   is commonly 18.2-18.5 and varies between sheets. Test-cut on scrap **from the same sheet**. Too
   tight splits the rib; too loose leaves no glue line.
2. ⚠️ **Notch depth exactly half.** If one set goes slightly deep, that set sits low and loses
   contact with a skin **along its whole length** - which is the glue joint the whole sandwich
   depends on.
3. 🔴 **Notch the bottom edge of every rib** where it meets the bottom skin, roughly 20 × 15 mm. An
   egg crate seals every cell, so without this the sand cannot migrate and you need a **drain port
   per cell** instead of a few. Same cut, far fewer ports - see Transport.
4. **Clamp the skins hard onto the rib edges.** That edge-to-face glue line is where the sandwich
   action lives. Screws through the skins into the ribs are the simplest way to get uniform
   pressure, and they can stay in.

#### What the tenons ask of the grid

Less than it first appears, and the two cases are different:

| Post | Where its tenon sits | What the grid must do |
|---|---|---|
| **Front left / front right** | **Hard in the box corner**, snug against both perimeter walls - the ledges put its outer faces exactly on the walls' inner faces | Only that the **first interior rib in from each perimeter clears it**. It is not a mid-cell case at all |
| **Back centre** | Against the back wall, **mid-span along it** | The two front-to-back ribs either side must **clear the 86 mm width**. This is the only mid-cell case |

So the corner tenons constrain nothing but the first rib offset, and they are **laterally located by
the two walls** for free. Only the back-centre tenon has to be placed between ribs deliberately - and
it is also the only one wanting blocking, since the corners already have walls on two sides.

Conventional torsion-box spacing is 200-300 mm; that is convention rather than calculation, and it
should bend to the back-centre tenon rather than the other way round.

### If more stiffness is wanted, rib height beats thicker skins

Stiffness goes with **skin separation squared**, so thickening the skins is the weaker lever.
Relative bending stiffness, closed-form:

| Build | Relative stiffness |
|---|---|
| 19 mm skins, 100 mm ribs (138 mm deep) | baseline |
| 25 mm skins, 100 mm ribs (150 mm deep) | +46% |
| 25 mm skins, 88 mm ribs (holding 138 mm deep) | +20% |
| **19 mm skins, 150 mm ribs** (188 mm deep) | **+100%** |

Much of that +46% is the box simply getting 12 mm deeper, not the skins working harder. **50 mm
more rib height doubles it**, for roughly 22 lb of extra plywood against 35 lb for thicker skins -
ribs are cheap because there is very little rib material next to two full sheets. The real cost of
taller ribs is **sand volume**, which is a choice at fill time and the part that gets drained for a
move anyway.

**Where 25 mm does earn its place is the top skin**, and not for sag: it takes the riser feet, the
Y plate bolt line and the plate bottom edges **in bearing**. Asymmetric skins are fine in a torsion
box, so **25 mm top over 19 mm bottom** is the sensible split if anything is spent.

✅ **And gross sag mostly does not matter.** Three points symmetric left-to-right means both Y beams
sag together, so they stay **coplanar** - the property that counts. A uniformly dished table is
irrelevant on a router; the spoilboard gets surfaced. Twist arises only from the X carriage sitting
at one end of its travel. Along each Y edge the stiffness is dominated by the 12" × 1 m × 1/4"
plate bolted to the 38 mm wall every 100 mm, which is far deeper than the box - **the skins are not
the main load path there.**

🔴 **What does deserve the material is the back edge.** With posts at the front corners and the
middle of the back, the back edge is a beam supported at its **midpoint**, carrying both back
corners - and those corners cannot be propped, because the rear carcases sit right under them and
letting the box land on one destroys the three-point mount. Skin thickness is a weak lever on a
spanning problem; a **deep back-edge member**, running below the bottom skin if it has to, is the
right spend.

✅ **Partly answered 2026-09-30.** The doubled back wall is a 38 mm lamination ~180 mm deep running
the full back edge, which is a considerably deeper member than the 138 mm box. It was adopted for the
back panel's sake, not for this, so treat it as a windfall rather than a solved problem - if the back
edge still wants more, it now wants it **below the bottom skin**, since the wall has taken the space
above.

---

## The three load-bearing points

**Front left corner, front right corner, and the middle of the back.** Each is an **86 mm square
cedar post** (4×4).

Three points, not four, and the reason is the whole argument: a three-point mount is statically
determinate, so **the box cannot be racked by a twisted floor or a twisted base**. That matters
because the property being protected is the two Y beams staying **coplanar**, which is what the X
gantry rides on and what the entire riser exercise existed to guarantee.

The three-point mount is between **box and base** - not between base and floor. So the base should be
made as rigid as possible; stiffening it costs the mount nothing and the box is isolated from its
twist either way.

### Tenon and ledge

Each post is reduced over its **top 118 mm** to form a tenon that passes up through a hole in the
bottom skin. The bottom skin lands on the shoulder, or **ledge**, that the reduction leaves behind.

The stack closes exactly:

| | |
|---|---|
| Ledge to top of post | 118 mm |
| Bottom skin resting on the ledge | 19 mm |
| Cavity above it | 100 mm |
| **So the underside of the top skin is at** | **119 mm** |
| **Post top therefore stops** | **1 mm shy** |

That 1 mm is stable: 118 mm along the grain of a vertical cedar post moves essentially nothing
seasonally, so the gap will not close on its own.

### 🔴 Ledge depth follows the wall above it - and it is not 19 mm everywhere

The ledges are cut on the **outward-facing** faces on purpose, so that the **perimeter wall lands
directly over the shoulder**. The load then runs wall, skin, shoulder, post in a straight line with
no plate bending anywhere. Good intent, and it dictates the depth: **each ledge must be as deep as
the wall standing on it.**

Every outer wall is **two laminations, 38 mm**. A 19 mm ledge under one would put the tenon directly
under that wall, leaving the wall with a hole where it needs to bear.

✅ **Since the perimeter was doubled on all four sides (2026-09-30), every ledge is 38 mm.** The
earlier version of this table had 19 mm on the front and back faces and carried a ⚠️ saying the
correction would apply if either were doubled. Both were.

| Post | Face | Ledge depth | Wall above it |
|---|---|---|---|
| Front left / front right | The **side** face (left or right) | **38 mm** | Laminated outer wall |
| Front left / front right | The **front** face | **38 mm** | Laminated outer wall |
| Back centre | The **back** face | **38 mm** | Laminated outer wall |

So the **front corner tenons are 48 × 48**, and the holes in the bottom skin with them. The **back
centre tenon is 86 × 48** - 19 mm thinner front-to-back than it was.

| | Was (19 mm front/back ledges) | **Now (38 mm all round)** |
|---|---|---|
| Front corner tenon | 48 × 67 | **48 × 48** |
| Back centre tenon | 86 × 67 | **86 × 48** |

Two side effects of the deeper ledges, both welcome: the corner shoulder area rises, and each corner
tenon ends up snug against both perimeter walls, so it is **laterally located by the walls themselves**.

⚠️ **48 mm is where the corner tenons stop being generous.** They carry no vertical load - that is
all on the shoulder - and they have 99 mm of engagement, so this is location duty only. But the rule
below about cutting each hole to its own post matters more at 48 mm than it did at 67, and a 38 mm
ledge on two adjacent faces of a stick that measures 88.9 rather than 86 leaves ~51 mm, not 48.

### Bearing, and the shoulder that stopped being single-sided

| Post | Shoulder area | Note |
|---|---|---|
| Front corners | **~5090 mm²** (was ~4180) | Wraps two faces |
| Back centre | **~3270 mm²** (was ~1634) | Still one face, but **double the area**, and the centroid moves in from ~33 mm off the post axis to ~24 mm |

Both are far inside cedar loaded **parallel to the grain** - the ledge is a cross-cut, so the plywood
bears on end grain in the post's strong direction.

✅ **The back post's eccentricity complaint is largely answered by the 38 mm perimeter.** This section
used to note a small permanent moment from single-sided bearing and offer front-and-back ledging as a
remedy, at the cost of wall-over-shoulder alignment. Doubling the back wall got most of the benefit
without paying that price: twice the area, a third less eccentricity, and the wall still lands
directly over the shoulder.

⚠️ **Cut each hole to its own post.** 86 mm is the working figure; S4S 4×4 is commonly 88.9 mm, and
cedar varies between sticks. Measure the three you have.

---

## Why the box is not fastened to the posts

**Gravity and 99 mm of tenon engagement, and nothing else.** Checked rather than assumed:

- Weight is in the hundreds of pounds; the largest horizontal the machine can generate is gantry
  acceleration, on the order of tens of newtons.
- That has to overcome friction on three large end-grain bearings **and** shear a 99 mm tenon.
- The CG stays well inside the support triangle at both ends of Y travel, so no post ever unloads.

Nothing in operation lifts or shifts the box. **No fastener is needed for what the machine does.**

### The exception is transport, and the decision has a deadline

Two cases can separate box from post, and neither happens in the shop:

1. **Road shock.** Freight is conventionally designed for vertical accelerations above 1 g - a design
   convention, not a measurement of any particular route. Above 1 g the box momentarily unloads, and a
   gravity-only joint can lift and re-seat.
2. **Being picked up by the wrong part.** Slings or forks under the *box* instead of under the frame,
   and the three posts hang from their tenons.

**One screw driven at an angle into the side of each tenon, from inside the cavity, covers both.** It
must be done **before the top skin is glued**, because after that there is no access to those tenons
ever again. Not a vertical bolt down through the shoulder - that is withdrawal from cedar end grain,
the weakest direction available.

The screws are **backup, not the plan**. The restraint that should actually be relied on is a strap
over the box down to the base frame - see Transport.

---

## The base

The base locates the three posts, stiffens them against each other, and is the pallet.

| Member | What it does |
|---|---|
| **2x6 bottom frame** | Locates the posts. **5/16" bolts** through post and frame |
| Clearance beneath it | High enough for a **pallet jack to enter and lift** |
| **2x4 top frame** | Ties the post tops together and is the top chord the shear walls fasten to. Sits **just shy of the bottom of the box** |
| **Shear walls** | Plywood cabinet carcases, standing on the bottom frame and reaching the top frame |

**Two bolts minimum per post-to-frame joint.** A single bolt lets the post rotate about it, and a post
that rotates lets its tenon walk in the skin hole.

### 🔴 The 2x4 top frame must never touch the box

"Just shy" is the load-bearing phrase in the whole design. The moment that frame touches, there is a
fourth and fifth contact point, **the mount is no longer three-point, and the failure is completely
silent** - no noise, no visible change, nothing but the Y beams drifting out of coplanar.

- **The clearance must exceed the box's own sag** between its three points under full sand load. That
  deflection has not been computed - it needs the grid spacing and the sand mass. Until it is,
  **10 mm or more**, not 1 mm.
- **Keep the gap inspectable.** A feeler or a strip of paper should slide between box and frame at
  several points, years from now. If the carcases make that impossible, the ability to check the one
  thing that fails silently has been designed out.

A near-touching frame would also be a useful **transport catch**, limiting how far the box can move.
That is a real benefit and it is in direct conflict with the above. **Resolve it with removable
transport blocks** - packers set on the 2x4 frame for a move and taken out on arrival. Determinacy
wins in service because it costs accuracy every day; the catch matters on the two or three days the
machine ever moves.

### The shear walls

Three plywood cabinet carcases fill the void under the box:

| Carcase | Position | Openings | Attached to |
|---|---|---|---|
| Rear left | Back left corner | Facing **out** | Bottom frame, top frame, and **back panel to the back-centre post** |
| Rear right | Back right corner | Facing **out** | Same, mirrored |
| Front | Between the two front posts | Facing **out** | Both front posts; **back to the sides of the two rear carcases** |

This works better than it might appear. A carcase with one open face still contributes panels in
**both** vertical planes - its back plus its two sides - so front-back and left-right racking are both
resisted by each of the three. There is no direction gap.

🔴 **Edge fastening is what makes a shear wall a shear wall.** A panel transfers load only through its
perimeter connections: **glue plus screws at roughly 150 mm all the way round** - to the bottom frame,
the top frame, the posts, and carcase-to-carcase where they meet. A carcase that merely sits in the
void with screws in its corners contributes close to nothing, **and looks identical to one that
works.**

⚠️ **The left and right sides are the least-stiffened perimeter.** The rear carcases cover the back and
the front carcase covers the front; the sides get only carcase ends. That is where to add a panel if
more is ever wanted - and it is also the least useful face for storage access, so it may be free.

---

## Transport

**The 2x6 frame is the pallet.** The jack lifts the frame directly; there is no separate pallet under
it. That makes the connection chain:

| Interface | How it is held |
|---|---|
| Frame to posts | **5/16" bolts** - positive |
| **Posts to box** | **Gravity and 99 mm of tenon** - the only non-positive joint in the stack |
| Carcases to frames and posts | Glued and screwed - positive |

So the tenon screws above are protecting the single interface in the entire assembly that nothing but
gravity holds. That is the argument for them, rather than "transport" in general.

- **Strap over the box, down to the 2x6 frame.** Two straps make box, posts and frame one object and
  neither separation case can happen. This is the restraint to rely on.
- **Put the fork positions under or very near the three posts.** The 2x6 frame is now a structural
  lifting member in bending between the tines, and a post landing mid-span between forks is the case
  to avoid. Add a cross member where the forks land if the layout does not cooperate.
- **The CG is high** - box, 305 mm risers, beams, gantry, spindle. On a jack on a tilting lift gate,
  **tipping is the hazard, not weight.** Long axis fore-aft, strapped.
- **Mass is a design budget only** - somewhere under half a ton, enough to size a jack and a gate.
  The assembly gets **weighed on a weighing pallet jack** when it is built; that is the only figure
  worth quoting, and it belongs in [`../commissioning/`](../commissioning/).

### Drain ports - and why they cannot go in the bottom skin

Dumping the sand is the single biggest lever on a move: roughly **165 lb that never gets carried**,
turning a ~240 lb box into ~73 lb. But with the 2x4 frame just under the box and three carcases
filling the void, **the bottom skin is unreachable** - bottom ports would need a carcase pulled out to
use.

- **Put the ports low in the front and back perimeter walls instead.** Still gravity-drains into a
  bucket, and reachable for the life of the machine.
- ⚠️ **Keep them out of the laminated left and right walls.** Those are the 38 mm shear webs the Y beam
  plates bolt to; a 2 inch hole through one is a hole in the load path.
- 🔴 **A rib grid makes closed cells, and each cell traps its own sand.** Either a port per cell, or
  **notch the ribs at the bottom** so sand can migrate to a few ports. The notches cost a little glue
  line to the bottom skin and nothing else.

Same deadline as everything else on this page: before the box is closed.

---

## ⚠️ Open items

- **The grid spacing**, subject to the first interior ribs clearing the two corner tenons and the
  back-centre tenon falling between two ribs.
- **The box's deflection between the three points** under full sand load. This sets the minimum 2x4
  clearance above, and it needs the grid spacing and the sand mass first. **The one number on this page
  that a wrong guess would quietly cost accuracy for.**
- ✅ **The box footprint is now DESIGNED, not measured** - closed 2026-10-03, then **corrected the
  same day**. The first answer had the box tucking *inside* the plates at 1205.4 by 983.65. It does
  not: the plates sit **flat on the top skin** and the tongues lap them from **outboard**, so the box
  is the larger part, not the smaller. **1211.75 across** (inside the two side tongues, which is the
  machine's own outer envelope) by **1156.35 front to back** - the 1000 beam *plus* the 6.35 rear
  plate, the 10 mm fin and a **140 mm front overhang**. Verify against the standing machine before the
  skins are cut, but it no longer blocks anything. See
  the Y beam interface.
- **Where the stabiliser legs go.** The project notes carry "three points plus a fifth leg". With a
  post at the **middle** of the back, the support triangle has **zero width at the rear**; tipping is
  fine either way the gantry travels, but there is little to resist a side load at the back corner.
  Whatever those legs are, they must be set **deliberately short** - if they carry load, it is no
  longer a three-point mount.
- **Whether the front and back perimeter members are single 19 mm**, which the ledge depths above
  assume.
