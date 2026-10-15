# Building the machine

**How the machine goes together.** Parts, hardware, and what bolts to what, in the order it is
done.

This document states the build and nothing else. It does not carry the reasoning, the options that
were weighed, or what any figure used to be — that is the design record, the thirteen chapters listed
in [`README.md`](README.md), and it is a separate printout. **Where this document and a chapter
disagree, the chapter wins.**

**Drilled hole coordinates are not here.** They are on the sheets in
[`drawings/shop-pack.html`](drawings/shop-pack.html), one sheet per part. This document says which
parts meet, with what hardware, and when.

OPEN: **Items marked Open are not yet specified anywhere in this repo.** They are not omissions from
this document — do not fill one in from a catalogue or from inference. [`open-items.md`](open-items.md)
is the full list.

---

## The machine

| | |
|---|---|
| Beams, all three axes | **Two 8020 `30-6060` stacked** — 60 mm wide × 120 mm tall, **1000 mm** long |
| Axes | X, a ganged **Y1 / Y2** pair, and Z. `Y_GANGED` + `Y_AUTO_SQUARE` in firmware, so the second Y motor is M3 |
| Rails | **HGR20**, one per profile, in the **outside** T-slot — rails 90 mm apart on each beam. **Y rails face each other**, on the beams' inside faces |
| Ball screws | **1605** on every axis, through a **cast stepper frame** at one end and **BF12** at the other |
| Screw position | **X on top** of its beam; **both Y underneath** theirs |
| Steppers | **2.2 N·m, NEMA 23 — four, one per axis.** **Y steppers at the FRONT** of the machine |
| Y beams | Fixed — their end plates bolt to the torsion box. Only X, Y-carriage and Z move |
| Spindle | **Ø80 mm, 2.2 kW water-cooled**, 5.2 kg, on two 80 mm clamps |
| Stands on | A sand-filled **torsion box** on **three of five laminated plywood legs**, held by **two grids** whose lower one is also the pallet |

### Rails come from two suppliers

| Axes | Kit |
|---|---|
| **X, Y1, Y2** | one HGR20 kit, one supplier |
| **Z** | a **400 mm** HGR20 kit, **a different supplier** |

**A dimension measured on the Z kit is a Z dimension.** Measure the X/Y kit separately for anything
that sets a plate.

### Thread locker

**Blue, and not on everything.** It goes on threads that run into **tapped metal**, which are the
joints that have nothing but thread holding them:

| Where | |
|---|---|
| Fin into its angle | M8 into the tapped fin |
| Shelf bar into the X end plate | the horizontal pair, into blind taps |
| BF12 into the rear plate and into the X tongue | M5 |
| Cast stepper frame into the interposer | M5, both rows |
| Spindle clamps into the Z plate | M8 x 90 |
| Ball nut, all four | M5 into the nut housing |

**Leave it off anything you are still setting.** Tram, the Z top stop and anything you expect to
move during commissioning get locker when the adjustment is finished, not before.

**None on T-nut joints.** A slide-in T-nut gives 6 mm of thread and the clamp comes from the
flange bearing on the extrusion, not from the thread. You will also be loosening these to slide
things along, which is what the slot is for.

FLAG: **None in the acorn nuts, and this one is not a preference.** The nut takes **11 mm** of bolt.
The rear plate's M8 x 45 puts **9.65** in and the side plates' M8 x 40 put **9.571** in, so there is
about **1.3 mm** of space left at the closed end. Locker is a liquid and a closed nut gives it
nowhere to go: the bolt can come up against trapped liquid and **feel tight while the joint is not
clamped**. That is the same false reading the 11 mm was measured to rule out, arriving the other way
round, and it is the one you cannot see from outside.

**Re-torque the tongue bolts instead.** What relaxes on that line is the plywood under the bolt, not
the thread — it is why the tongue is the thick sheet, for bearing area. Check them after the machine has run a
few hours and again after the first weeks. Locker does nothing about wood creeping and makes the
re-check harder.

NOTE: **Do not reach for a longer bolt to get more thread into an acorn nut.** The 11 mm is a
ceiling: the rear plate needed a **second fender washer** to make an M8 x 45 fit, which is why that
joint has two.

**Buy the stick, not a jar to dip into.** Thread locker sets where air cannot reach it, which is why
it keeps in its own bottle and why an open pot skins over and thickens. The semi-solid stick wipes on
like a crayon, does not drip, and suits doing a lot of bolts in one sitting.

---

## Order of work

**The box is cut from the standing machine, and the spindle goes on after the box.** Two ordering
rules carry the whole sequence, and neither can be worked around:

- FLAG: **The machine is assembled on a flat surface and its width measured off the standing
  assembly.** That measurement is what the box skins are cut to — so the machine comes before the
  box, not after it.
- FLAG: **The spindle and tram come last, after the machine is bolted to the box.** Tram is set in the
  installed position or it is set against a reference the machine does not have yet.

| | Stage |
|---|---|
| 1 | [Make the plates](#1-the-mill-trip) — one trip to the mill |
| 2 | [Build the three beams](#2-the-beams) — T-nuts, rails, joining plates |
| 3 | [The Y beam ends](#3-the-y-beam-ends) — interposers, castings, screws, fins, rear plate, outboard plates |
| 4 | [The X gantry](#4-the-x-gantry) — end plates, shelves, beam, carriage plate |
| 5 | [The Y ball nuts](#5-the-y-ball-nuts) — doublers and sole brackets |
| 6 | [The Z axis](#6-the-z-axis) |
| 7 | [Stand it up and measure](#7-stand-it-up-and-measure-it) — this is where the box width comes from |
| 8 | [Build the box and its base](#8-the-torsion-box) |
| 9 | [Set the machine on the box](#9-set-the-machine-on-the-box) |
| 10 | [Fit the spindle and **tram**](#10-fit-the-spindle-and-tram), then the [stiffness test](#then-run-the-stiffness-test) |
| 11 | [Fill the sand](#11-fill-the-sand) |

---

## 1. The mill trip

Accurate holes are drilled on **one visit** — a Laguna mill, 4' × 1' bed, **manual X and Y**.
Every plate must be fully dimensioned before the trip, including assemblies that will not be built
for months.

| On the mill | |
|---|---|
| Two **Y front plates / fins**, 10 mm | the 8-bolt corner-bore pattern and the 60.5 × 50 window |
| The **1210.73 mm rear plate**, 1/4" steel | two 8-bolt patterns a metre apart |
| Two **X gantry end plates**, 1/2" | one drawing, right-hand variant carries the BF12 tongue |
| **X carriage plate**, 1/2" | 30 holes |
| **Z plate**, 1/2" | |
| **Interposer bars**, 60 × 150 × 3/8", quantity 3 | six tapped M5 under a bearing face, six flange clearance holes |
| **Both Z spacers** | **face 1 mm off both in the same setup** — see [the Z axis](#6-the-z-axis) |
| Rail mounting patterns, bearing block and nut housing patterns, counterbores | |

| Home drill press | |
|---|---|
| Beam joining plates | 9 mm clearance into T-slots at 150 mm — the T-nut moves to meet the bolt |
| Two **outboard plates**, 11 7/8" × 39 5/16" × 10 gauge steel | ~25 holes each, and steel runs several times longer than aluminium would |
| Three **front strips**, 45 mm × 1 m × 4 mm | |

FLAG: **Five plates stand on the box and all five are 301.625 high: the two side plates, the back
plate and the two front fins.** Measure all five against each other as they arrive, before any of
them is drilled. **A part that is not 301.625 is misordered or mismade — send it back.** Two parts
wrong by the same amount would still assemble, so check them against each other and not only
against the number.

**Every hole on those five is measured from the bottom edge**, because the bottom edge is what
bears on the box's top skin. One height and one reference edge is what lines the beam up without
any plate having to know about any other.

**Lay the extrusion bolt patterns out by scribing.** Two lines, four stations ticked along each —
that is the eight-hole pattern at a beam end.

**Each plate only has one WCS origin for the holes to be drilled.** Pick a corner, dimension
every hole from it, never chain dimensions.

**Make one rail the reference and set the second one fastener at a time.** Both rails tap **M5 into
the plate**, so the holes are fixed and nothing is oversized at the mill — the float is the rail's
own, **ø6 through under a ø9.5 counterbore** on an M5. **Lock rail one down completely.** Then work
**along rail two, bolt by bolt**: set parallel at that station with an indicator on rail one's
carriage, tighten that bolt, move to the next. OPEN: **Never tighten rail two as a set** — it snakes,
and a bolt already home fights the next one you set.

OPEN: **Open: whether the mill can hold one height reference across the 1210.73 mm rear plate.** Bed size is not
travel. The two 8-bolt patterns' relative height must land well inside 1 mm across the metre.
If the part is repositioned mid-job, **indicate the first pattern back in before drilling the second**,
and work from a scribed and indicated line rather than from a sawn edge.

---

## 2. The beams

Three identical stacked pairs — X, Y1 and Y2. Each is two `30-6060` × 1000 mm.

### Load every T-nut first

FLAG: **The `13025` T-nut slides in from the end of the slot.** Once a joining plate or an end plate
closes the slot ends, the only way to add one is to take the beam apart.

| Plate | Slots | Per slot | Per beam |
|---|---|---|---|
| Back plate | 4 — full section height | 7 | 28 |
| Front strip | 2 — flanking the seam | 7 | **14** |
| | | | **42 per beam, 126 for the machine** |

**Seven per slot is first at 50 mm, then every 150.**

OPEN: **The front strip's two slots are the ones that get forgotten** while counting out the back, and
they are just as closed once the ends are on. Count them twice.

**Test the slide with one nut before planning the rest of the build.**

The beam ends also take T-nuts for the parts that come later — the **interposer bar** (6 × M8 in the
bottom-face slots at 15 and 45 on Y, the top-face slots on X) and the **shelf bars** on X
(M8 at Y 15 and Y 45 into the bottom extrusion's underside slots). **Those go in now too.**

### Mount the rails

One HGR20 per profile, in that profile's **outside** T-slot — 15 mm in from each outer face of the
120 mm stack, so the two rails end up **90 mm apart**.

| | |
|---|---|
| Fixing | **M5 × 16 into T-nuts**, 17 per rail at 60 mm |
| Hole | ø6 through with a ø9.5 counterbore — M5 socket head. An M6 head will not enter a 9.5 counterbore |

FLAG: **Bias every bolt the same direction as you tighten it, and bias both rails the same way.** The
hole is a clearance hole and the T-slot adds more float; tighten 17 bolts with the rail floating and
it snakes. **Common mode — both rails pulled the same way.** Do not pull the two rails apart or
together.

NOTE: **The X beam's rails are already mounted with an opposed bias** — lower rail toward the lower
edge, upper toward the upper. **Check by feel before redoing 34 bolts**: mount the four blocks to the
carriage plate and slide the assembly the length of the beam. Smooth and even means leave it. A
binding zone tells you roughly where, and only those bolts need revisiting. For a number, put an
indicator on the plate against a straightedge and sweep.

### Join the stack

| | Back | Front |
|---|---|---|
| **X** | 120 mm × 1/4" 6061, full section height | 45 mm × **4 mm** 6061 |
| **Y1, Y2** | no separate back plate — the **outboard plate** is it, see [the Y beam ends](#3-the-y-beam-ends) | 45 mm × **4 mm** 6061 |
| Fixing, back | M8 T-nuts, four rows, 150 mm | — |
| Fixing, front | — | M8 **flange** bolts, two rows, no counterbore |
| Holes | **9 mm clearance** | 9 mm clearance |
| **Bolt** | **M8 × 12** on X · **M8 × 10 + plain washer** on Y | **M8 × 10**, bare |

FLAG: **The lengths are not interchangeable, and the long one fails silently.** There is
**1.2 mm of air behind the T-nut** (slot floor measured at 9.5, nut back face at 8.3), so a bolt may
reach at most **7.2 mm** past the back of a plate. **An M8 × 12 in the 4 mm front strip reaches 8.0
and bottoms on the slot floor before its head seats** - it feels tight and the strip is still loose.
Engagement is capped at **6 mm by the nut**, so a longer bolt buys nothing anywhere on this machine.
The washer on the Y back is margin, not decoration: bare, that bolt clears by 0.24 mm if the sheet is
the 11-gauge it was sourced as. Full derivation in
[`gantry-beam-joint.md`](gantry-beam-joint.md#-bolt-lengths-settled-2026-10-04---and-the-slot-depth-is-what-settled-them).

**The buy: 42 × M8 × 10 A4 / 316** (front strips) · **56 × M8 × 10 plain + 56 washers** (Y backs) ·
**28 × M8 × 12** (X back). 126 bolts, 126 T-nuts.

FLAG: **The front strip is 4 mm, not 1/4".** At 1/4" the flange head rim passes under the bearing block
and hits — there is at most 6 mm of clearance there, and the 1/4" stack is 7.35.

FLAG: **The front strip's 14 flange bolts must be austenitic stainless — A4 / 316.** The magnetic
encoder tape runs on this strip's face, and ferromagnetic bolt heads 1 mm from a magnetic scale put a
periodic error at the bolt spacing into the axis. **42 bolts across the three beams.**

OPEN: **Put a magnet on them when they arrive.** Generic "stainless" bolts bought for this job were
tested and **are magnetic**. 410, 416 and 430 are sold as stainless and are as bad as carbon steel
here. **Ask for A4 rather than A2.** Socket heads are fine if A4 flange heads are awkward to source —
a 13 mm socket head leaves more room for the tape than the flange does.

### FLAG: Assemble the stack against a flat reference

Nothing indexes one profile to the other, and the joining plates lock in whatever they are bolted at.
**Both front faces must end up flush**, or the rails are not coplanar and the carriage plate twists
all four blocks.

**Stack front-face-down on a known-flat surface, or clamp a straightedge across both front faces,
before the joining plate bolts come up tight.** This is the moment the rail geometry is set.

### The magnetic tape

**10 mm tape on the face of the 45 mm front strip**, centred between the two bolt rows. Two rows at
±15 with **13.8 mm** flange heads leaves **16.2 mm clear**. **All three beams carry tape.**

FLAG: **The clear lane is sized by the SENSOR, not by the tape.** The AS5311 puck needs **15 mm**
kept clear centred over the tape - the PCB and its mounting points, not the chip - which leaves
**0.6 mm each side**. OPEN: **At the old 17.3 mm head the lane was 12.7 and the puck did not fit at
all**, which is why the bolt changed. The bolt rows cannot move to help: they are at ±15 because
that is where the extrusion's T-slots are.

FLAG: **Bias the strip bolts OUTBOARD as you tighten them.** The holes are ø9 clearance on M8 into
sliding T-nuts, so nothing centres a bolt and ±0.5 is available - both rows drifting inboard takes
the 0.6 down to **0.1**. It costs nothing to push them out, and it is not something to find out
about after the tape is down.

OPEN: **Before 3 m of one-shot PSA goes down:** fit a tape offcut and a sensor and **read at the stepper
end against mid-travel.** A NEMA 23 permanent-magnet rotor sits at the min-Y end of both Y tapes.

OPEN: **Open: the application order.** Either the bolts go in first as a guide channel and the PSA is
threaded into a 12 mm slot, or the tape goes down first against a straightedge and the bolts follow.
Not decided.

---

## 3. The Y beam ends

Each Y beam is carried **at its two ends only** — the ball screw runs underneath it, so nothing can
support it along its length.

### The interposer bar and the cast stepper frame — front end

**One part, quantity 3** (Y1, Y2, X): **60 × 150 × 3/8" 6061**, no counterbores anywhere.

| | |
|---|---|
| Bar to beam | **4 × M8 × 20 flange bolts into slide-in T-nuts** — two rows, two slots. FLAG: **Not six in three rows**, which this line said until 2026-10-11; the 3D model has always drawn four and he confirms four |
| Position | the bar's **outboard end 30 mm past the fin's outer face**, so casting and bar protrude through the window together |
| Casting to bar | its **6 through holes, M5 tapped into the 3/8"** — bar coordinates, columns 7 and 53, rows 28 / 58 / 71 |
| Motor | NEMA 23 onto the casting's own flange |

FLAG: **At the Y ends everything below the beam is in tension.** Six M8 hold the bar **up** against the
beam's underside, and the casting is bolted **up** into the bar and hangs from its own M5. Nothing
rests on anything.

OPEN: **The casting's foot is stepped, not one flat plane.** Match or clear the step — if the bar sits
under the stepped portion it holds the casting off its bearing face.

FLAG: **The stepper frame is FERROUS — a magnet sticks to it.** His test, 2026-10-13, and it had been
taken for cast aluminium. It matters because the **limit sensor mounts on the casting's top face**:
an SN04 is non-shielded, so a ferrous host is the one material that can trigger it from the side or
the back rather than off the target. **Whether it false-triggers there is a bench test, not a
calculation** — wire one up on the real casting with BK12 in place before the mount is drilled.

OPEN: **Open on X only: whether both bolt rows land over beam.** The rows come from Y geometry, and on
X the bar sits on top and overhangs the end. **Check before drilling X's bar** — it is the same
part, so the check is on the position, not the drawing.

FLAG: **This read "all three bolt rows ... the 82 / 110 / 138 rows" until 2026-10-11, and that was
stale twice over.** There are **two** rows, not three, and the registry puts them at
**105 and 135** — see INTERPOSER_BOLT_ROW_1 and _2. The 3D model has drawn two rows all along.

### BF12 — rear end

**4 × M5 tapped into the inside face of the 1210.73 mm rear plate**, one set per beam. Not
through-bolted.

NOTE: **BF12's hole count depends on its orientation.** Face-mounted into a plate it is **4 × M5**;
top-mounted down through its base onto a horizontal surface it is **2 × M5**. Any BF12 figure that
does not name the orientation means nothing.

### The front plate — the fin

**Two off, each on its own piece of plate** - they used to nest out of one square: **tapered 100 mm at the top to 200 mm at the base, 301.625 mm
tall, 10 mm** 6061, with a **60.5 × 50 mm window** below the beam for the casting.

The two halves are **rotations of each other, not mirrors** — turn one 180° and the outline is
identical. Left and right come from flipping one plate over.

FLAG: **Lay both hole patterns out from the factory vertical edge and the factory top edge.** Each half
keeps one uncut vertical edge and that is the **outboard** one, taper facing inboard. Laid out from
the cut edge instead, the bandsaw kerf becomes a ~1.5 mm offset built into one plate's bolt pattern —
and that pattern has to line up with formed threads in the beam.

OPEN: **Flipping one plate swaps which face is outboard.** Harmless for through holes; check it before
spot-facing or counterboring on one face only.

| | |
|---|---|
| To the beam | **8 × M8 × 35 flange bolts** into the ø6.65 lengthwise corner bores — four per profile |
| Hole | **9 mm**, deliberately. The bores are extruded features and a close fit is impossible in principle |
| M8 columns | **35 and 65 mm** from the factory edge, so the beam spans X 20 to 80 |
| To the box | **two M8 at X 25 and X 170, Y 20** above the plate's bottom edge — **TAPPED**, for the angle in front |

**M8 × 35 leaves 22.3 mm in the extrusion.**

FLAG: **There is no front tongue on the box.** The fin sits on the box's **top skin**, and **one
170 mm length of 40 × 40 angle extrusion in FRONT of it** ties it down - two across the machine,
bolting into **T1 at X 25 and T2 at X 170, tapped, at Y 20**. FLAG: **In front because the tee track
bed leaves zero room behind**: the bed's front edge and the fin's back face are both at 1006.35.
The box runs **194.65 mm past the fins**.

SETTLED: **Settled 2026-10-11: one 170 mm length of 40 × 40 angle extrusion per fin, in FRONT of it.** Two
across the machine, not four. It starts flush with the box's side edge, the two M8 run into **tapped**
holes in the fin — no nuts — and four bolts through its horizontal leg go into **prong-type threaded
inserts in the top skin**.

FLAG: **The angle is in front because there is no room behind.** The tee track bed's front edge and the
fin's back face are both at 1006.35 — zero gap. The bed, settled the same day, is what closed that
space.

FLAG: **The fin is tapped because of the bed too.** The bed's top face is at 16, so an M8 nut and washer
at Y 20 would reach down to 11.5 and foul it by 4.5. Tapping puts nothing on the back face.

FLAG: **The inserts go in BEFORE the top skin is glued to the ribs.** They fit from underneath and there
is no access afterwards, and the only fix then is a hole in the box. **It is the one step of the
glue-up that cannot be undone.**

**Use a steel backing strip or large fender washers on both faces** where these bolts land in
plywood, not plain washers.

### The rear plate

**One plate for both beams: 1210.73 mm × 12" × 1/4" hot-rolled A36 steel**, P&O if mill scale is
unwelcome.

| | |
|---|---|
| To the beams | **8 × M8 into each beam's corner bores** — 16 bolts total |
| To the box | **8 bolts through the back tongue at Y 30**, 150 mm pitch from X 80.365, plus bottom-edge bearing over the full length |
| Also carries | **BF12 on its inside face**, 4 × M5 tapped, one per beam |

FLAG: **1210.73 is a reference, not a dimension.** The plate runs flush with the outboard plates' outer
faces, and Sheet 7's X coordinates are absolute from the plate's left edge. **Cut it over-long and
the Y2 station is out by the excess.**

**Buy 60" stock rather than 48".** A 48" sheet is 1219.2 mm and leaves 7.5 mm of trim, which is the
entire margin on a part cut once.

**Clean the mill scale off before paint. Paint is not optional** — this is steel against aluminium
over a metre of contact.

### The outboard plates

**One per Y beam, as ordered: 11 7/8" × 39 5/16" × 10 gauge cold-rolled steel sheet** - 301.625 × 998.54 × 3.429. This **is** the Y back joining
plate — there is no separate 120 mm plate on Y. It runs from the beam down to the torsion box.

| | |
|---|---|
| To the beam | T-nuts along its length, **9 mm clearance** holes |
| To the box | **M8 at 150 mm, first at 50** — seven per beam, at **Y 30** above the plate's bottom edge |
| Direction | from **outboard**: washer, **tongue**, plate, **M8 locknut** on the inboard face |
| Holes | **9 mm clearance** in **tongue** and plate both |
| Position | against the beam's outboard face at X 20, ending **1 mm shy of the beam's end** |

SETTLED: **Settled by the order, 2026-10-08: it is 10 gauge, .135" = 3.429 mm** - not 1/8" (3.175) and
not the "11 gauge" (3.04) the listing also offered. That question stood open for weeks and was
closed by buying the part. The riser-proud check keys off it, and the figure is now **16.571**.
OPEN: **Still caliper what arrives**: a gauge is a nominal, and three nominals on this machine have
already come in wrong.

**Powder coat or paint both faces.** This plate is the chip barrier and it is the part that gets wet
with swarf — aluminium is the anode and the extrusion is what cannot be replaced.

OPEN: **The plate-to-tongue seam is a swarf trap** running the length of the machine. Either seal the top
of it or leave it deliberately open at both ends so it can be blown through.

---

## 4. The X gantry

### The end plates

**Two, 1/2" 6061, 154 mm wide × 242.5 mm tall**, stopping at the top of the X beam. **Identical
below the top edge.** The **right-hand plate only** carries a **BF12 tongue** — 60 across, running to the stock's 300, left uncut — rising off the
top edge, 60 mm wide, with **4 × M5 tapped**.

OPEN: **They are not interchangeable at assembly.** Cut both outlines together and leave the tongue on
one; nothing below the top edge moves.

| | |
|---|---|
| To the X beam | **4 × M8** into the **top** extrusion's corner bores, **9 mm clearance**, both pairs **15 and 45 mm from the plate's back edge** |
| To the Y rails | **four bearing blocks** in a 2 × 2 grid across the full 154 mm — two butted in Y by two rows 90 mm apart |
| ø35 encoder bore | **Y 77, 60 mm below the Y beam top** |

**The bottom extrusion is not bolted to the plate at all.** It sits alongside the Y beam, carried on
a shelf.

OPEN: **The 15 mm to the back edge with a 9 mm hole leaves 10.5 mm of material** — the plate's tightest
edge distance. Do not let that hole drift outboard.

NOTE: **Scribe and tick the 15/45 pattern**; the ø9 hole on an M8 carries the float.

### The shelf

**One per plate: 1" × 2" aluminium bar — 25.4 wide × 50.8 tall × 60 long**, spanning the beam's
footprint at Y 0 to 60.

**Y is measured from the plate's back edge. Z is from the bar's underside.**

| Hole | Y | Z | |
|---|---|---|---|
| Vertical, counterbored from below | **15** | — | M8 up into a T-nut in the bottom extrusion's underside slot |
| Vertical, counterbored from below | **45** | — | M8 up into the second underside slot |
| Horizontal | **30** | **15** | **M8 × 35** into the end plate |
| Horizontal | **30** | **35** | **M8 × 35** into the end plate |

FLAG: **M8 × 35, not × 40.** Through 25.4 mm of bar into 12.7 mm of plate, an M8 × 35 gives ~9.6 mm of
engagement and stops short of the far face. **An M8 × 40 protrudes ~1.6 mm onto the Y bearing block
seat** — the one surface on this plate that has to be flat. **Check the length at assembly.**

OPEN: **Check the counterbore diameter before cutting the bar to exactly 60.** The vertical at Y 15
leaves only ~7.5 mm of wall outside a ø15 counterbore. **65 costs nothing** and still stops short of
the joining plate.

### Hang the beam

**Bolt both end plates on, slide the T-nuts in, drop the beam onto the two shelves, then bolt down.**
One person can do it that way.

OPEN: **The back joining plate's bottom edge must be flush with the beam's underside, not proud.** The
bar passes under where that plate lands.

### The X stepper end

**Interposer on TOP of the beam**, overhanging the end — same 60 × 150 × 3/8" part as Y, same
**four M8 × 20** into slide-in T-nuts. FLAG: **On X the parts are in compression, stacked** — the opposite of the Y ends.

**BF12 face-mounts on the right-hand end plate's tongue**, 4 × M5.

### The X carriage plate

**154 mm W × 407 mm H × 1/2"** 6061 — **30 holes**. It bolts to the four X-axis bearing blocks and
carries the whole Z axis. The blue is layout dye, not a finish.

FLAG: **Do not make this joint adjustable.** No set screws over the bearing blocks. The bolt heads are
buried under the Z rails, the screw and the nut housing once assembled, and this joint carries
everything. **Build it solid - everything else is set from it.**

---

## 5. The Y ball nuts

The Y ball nut housings run **inverted** on both beams, so their mounting faces look **down** and
their bolts are reachable.

| Part | Size | Qty |
|---|---|---|
| **Doubler block** | **154 × 45 × 1/2"** 6061, on the end plate's **outer** face at the bottom | 2 |
| **Sole bracket** | **1/4"** 6061 trapezoid, **154 at the root → ~46 at the tip, 98.19 overall** | 2 |

**The doubler gives the plate a 24.38 mm seating at its bottom; the sole bracket bolts up into that.**

FLAG: **Two rows of bolts across the 24.38, not one row down the middle.** A single row leaves the joint
nothing to resist rolling about Y.

**The doubler's bolts pass through the end plate along X. The sole bracket's go into the doubler** —
M6 is correct there; nothing from the nut lands in the end plate's edge.

**The nut sits ON the sole plate, bolted up from underneath** — **4 × M5 threaded into the nut body**,
at **±20 mm in X and ±12 mm in Y** about the nut face centre. The nut's mounting face is **40 × 52**,
its long dimension running **along X**.

OPEN: **If "block" in the source meant anything other than the ball nut housing, these four holes are
90° out.** Confirm against the real part before drilling.

OPEN: **Open: the doubler's upper bound is not yet checked on the machine** — the lower Y bearing
block row's bottom edge, computed to land at about −127 from the Y beam top. Same measurement as the
sixteen block holes. **At 45 there is 10.5 of slack against it**, so that measurement would have to
be badly wrong to matter.

---

## 6. The Z axis

| | |
|---|---|
| Fixed | the **X carriage plate**, its two HGR20 400 mm rails, the 1605 screw, the cast frame and BF12 |
| Moving | the Z bearing blocks, the two spacers, the ball nut housing, and the **Z plate** |
| Z plate | **164 mm W × 175 mm H × 1/2"** |
| Spacers | **two lengths of 2" aluminium bar, measured 150.5 and 151.6 long, 16.41 and 16.43 thick** |
| Bolt count | **16 × M5 × 35** — 8 per spacer, 4 per bearing block |
| Fixing | **one M5 per hole does the whole stack** — counterbored in the Z plate, through a 6 mm clearance hole in the spacer, into the bearing block's tapped M5 |
| Travel | **246 mm**, blocks butted |

FLAG: **M5 × 35, not × 30.** An M5 × 30 leaves only ~5.9 mm in the bearing block.

FLAG: **The Z plate is 164 and the X carriage plate is 154. Do not "tidy" them into line.** At 154
eight of the Z plate's M5 counterbores break out of the edge.

### Face the spacers before assembly

FLAG: **The spacer blocks stand higher than the ball nut housing — between 1 and 1.3.** Skim **1 mm off
the spacers, both in the same setup, at the mill**, so they come out identical.

FLAG: **Skim 1 mm and no more, even if the step measures 1.3.** The cut cannot be undone. Whatever is
left over gets closed with a shim at the nut, where it can be measured on the assembled machine
instead of guessed at the mill.

FLAG: **A full-face shim, not washers.** The shim covers the nut housing's whole 40 × 52 mounting face.
**Washers bear at four points and tilt the housing, which becomes a side load on the screw.**

OPEN: **Measure the step again before cutting**, and **take the ball nut housing to the mill** — the
step is measured against that part.

FLAG: **Re-mic both spacers after facing and write the number into the design record.** Everything
downstream of the spacer thickness moves with it, including the spindle offset.

**Do not re-cut the spacers to match each other in length.** Matching matters in **thickness**.
150.5 and 151.6 both cover the M8 rows at ±70.5.

### The top stop

**Two blocks, one per rail, either side of the 60 mm casting** — the casting occupies the middle of
the plate's top edge.

| | |
|---|---|
| Width across the plate | **47 mm** each |
| Front to back | **32.5 mm** — 12.5 of plate plus 20 of rail, so the overhang is flush with the rail top |
| Thickness | **1/4"** |
| Fixing | **2 × M4 × 16 socket head** per block, down into tapped holes in the plate's 12.7 mm top edge |

**M4 not M5** — a 12.7 mm edge leaves 4.35 mm of wall each side of an M4.

FLAG: **These are sacrificial.** They fire only if the soft limit and the proximity sensor have both
failed. If one is ever used, replace the block and the bolts. Do not size them by strength.

The block runs **7 mm past the rail end** before contact, against **10 mm** of the block carrying no
balls — measured. The bottom end needs no stop; the nut bottoms on BF12 before the rails run out.

**Keep the plastic arbors** that came with the blocks — they are the transfer and storage tool, and
nothing else substitutes the day one is needed.

### Assembly order

**Rails and spacers first, nut housing last.** The rails define the geometry; the nut follows the
screw rather than being forced into position by its own bolts.

0. **Tap the ball nut housing's four M5 holes from 8 mm deep to 12.** It is aluminium and taps
   easily; the holes are already drilled 16 deep, so there is room. **Blow the chips out.** The four
   bolts into it are **M5 × 16** and they need that depth — at the as-supplied 8 mm they would reach
   less than half the thread aluminium wants.
1. **Bolt the Z plate down onto the spacers and bearing blocks, and torque it.**
2. **Measure the gap at the nut housing with feeler gauges**, with the plate already tight.
3. **Cut a full-face shim to what you read** and fit it behind the housing.
4. **Leave the nut housing's four bolts finger-tight, run the carriage through full travel, then
   torque them.**

FLAG: **Never close that gap by tightening the nut's bolts.** The nut cannot move — it is captive on the
screw — so tightening across an open gap pulls the nut off the screw axis and holds it there for
every move the axis makes.

OPEN: **Open: the Z travel floor.** 246 mm is confirmed available, but where that 246 sits relative to
the spoilboard has never been set — material thickness plus tool length plus clearance over
workholding. **This is the one that gets quietly eroded, and it is the one noticed every day.**
It is a machine measurement, taken once the machine stands.

---

---

## 7. Stand it up and measure it

FLAG: **The machine is the reference, not the drawing. The box is not built until the whole machine is
assembled on a flat surface and its width measured.**

The machine jigs itself for that measurement, so nothing has to be computed:

| What sets it | How |
|---|---|
| The two Y beams' spacing | the **X gantry** bridging them — its length, its end plates, the bearing block footprint |
| Their coplanarity and parallelism | the **flat surface** they are assembled on, plus the 9 mm reamed holes absorbing the error |
| The box's top skin width | **measured off that assembly**, once it is standing and square |

**Record the measured width in [`../commissioning/`](../commissioning/) before cutting skins.** Do
not let a nominal or catalogue figure substitute for it.

OPEN: **Bias the top skin wide, never narrow.** The skin's width sets the distance between the two
**tongues'** inner faces, and a tongue's inner face is a hard bearing face with no float. A
millimetre or two too wide is a shim; **too narrow and the plates will not fit between the tongues
at all.** They stand on the top skin and are lapped from outboard - nothing drops into a groove,
but the gap is still a hard dimension.

---

## 8. The torsion box

| | |
|---|---|
| Skins | **24 mm Baltic birch top, 18 mm bottom** — the thick sheet on top is for **bearing** not stiffness |
| Grid | **18 mm strips, 100 mm high**, **egg crate** — continuous both ways, half-depth notches at every crossing |
| Depth overall | **142 mm** (24 + 100 + 18) |
| Outer walls, all four sides | **24 mm outer + 18 mm inner web, 42 mm total** — the outer one **202 mm tall, capping the end grain of both skins** and **60 mm proud** of the top skin as a **tongue**. The thick sheet outboard is for **bolt bearing** |
| Footprint | **1211 square**, both whole millimetres so a tape can lay them out. The machine's own envelope is 1211.238 and the skin is cut 0.24 under it, so the plate stands a hair proud of the skin's edge and the tongue beds on the plate |
| Grid, both ways | **223** from each web to the first rib, then **219** between ribs — the same layout in both directions, so **all eight ribs are one part**: 1175 × 100, notches at 223, 460, 697 and 934 |
| Fill | **sand in the cavities, LAST, on site** |

### Cut the notches with all eight ribs clamped as one stack

**On the sliding miter saw.** The eight ribs are one part — same length, same four offsets — so they
get notched together: stack them face to face **on edge**, 144 across, clamp them as one block, set
the depth stop to **50**, and nibble each notch out in overlapping slides. Four positions, six or
seven passes each.

1. **Register the ends against a stop block and do not unclamp until all four notches are cut.** The
   stack is one part for as long as it is clamped; the moment a rib shifts, that rib's notches move
   and nothing tells you.
2. **A sacrificial piece of the same stock on each face of the stack.** It takes the blade's exit
   tear-out and gives the clamps something to crush instead of a finished rib.
3. **Plywood sub-base on the saw table**, so the 50 comes off a continuous flat surface rather than
   across the saw's own kerf slot. **Tall fence** too — the ribs stand 100 on edge.
4. **Cut a test notch in an offcut and try a real rib in it.** Nibbling means **18 is where you
   stop**, so the width does not depend on a blade being the right thickness — which is the whole
   advantage over a stacked cutter. Check that same test notch for a **flat floor**: 50 all the way
   across. A dished floor means the blade is dropping rather than sliding through the cut.
5. **Overlap each pass by about a millimetre** and the floor needs no cleanup. Set the depth stop
   against a test cut **that you then measure**, not off the screw.

**Prove the depth on a practice pair before the eight go in the clamp.** Cut two offcuts exactly the
way the eight will be cut, then flip one, turn it 90° and cross the two at **every** station in turn:

- **Press the rib down flat against the reference while you look.** A released rib bows slightly in
  its own plane, enough to lift a station a millimetre off the table and show a step that is not
  there. The box will press it far harder than your hand does.
- Pressed flat, a correct pair reads **even at every station** — both bottom edges down, both top
  edges flush, and the notch floors just meeting.
- **Measure the notch depth on a released rib, never on the clamped stack.** 144 of plywood clamped
  is stiff enough to read straight whatever the ribs do when they come out.

**Bias the stop a touch deep.** The bottom skin is the reference the grid stands on, so a notch a
few tenths over cannot lift anything — the rib still stands on the skin, both its edges still reach
both skins, and all that is lost is contact notch floor to notch floor, which carries nothing. A
notch a few tenths **under** holds its mating rib up off the skin, and that is a glue line you
cannot get back. Aim half a millimetre over and let the rib's own bow live inside that.

**Cut all eight from the same edge, then turn four of them over.** One direction has to be notched
from the top edge and the other from the bottom, and that is free here because the notch is
*exactly* half of 100: a rib turned upside down is a rib notched from the other edge, and the
offsets are symmetric end to end as well.

**Notch depth half, and err over rather than under** — see the bias above.

### What a millimetre of error actually costs

**The notches are the layout.** A rib does not sit at a measured position — it sits where the mating
rib's notch puts it. That is why three of the four ways to be a millimetre out cost nothing.

| Error | What happens |
|---|---|
| **A position off by 1, on all eight** — the stack shifted against the stop | **Nothing jams.** All eight are identical, so the grid is still self-consistent and that rib line simply lands 1 off the drawing. The bays either side go 220 and 218. Everything that measures off the last rib line has 36 of room, the sand ports are 25.4 in a 219 bay with 97 clear either side, and the back tenon blocks come out of the scrap bin and get cut to fit |
| **One rib of the eight off** — it moved in the clamp | **That rib will not drop in.** Its notches fight the grid the other seven define, so it gets pared or recut. This is the error the stop block and the do-not-unclamp rule exist for |
| **A notch too wide by 1** | Slop at every crossing, so the grid stops holding itself square. Not structural, and the glue fills it — square the grid on the reference before the skins go on. **Too narrow by 1 is worse**: it splits a rib, or the grid will not go together |
| **A notch too deep by 1** | **Harmless, and it is the side to err on.** The rib stands on the bottom skin, so it cannot sink: both its edges still reach both skins, and all that is lost is contact notch floor to notch floor, which carries nothing |
| 🔴 **A notch too shallow by 1** | **The only one that touches the structure.** It holds its mating rib 1 up off the bottom skin, so the top skin bears on that set while sitting clear of the other four and of the perimeter webs |
| **A step at one station that closes when you press the rib flat** | Not an error at all — the rib's own bow lifting it off the reference. Check every station pressed flat |

**So the figure to get right at setup is the depth stop, with a test cut you then measure** — and it
only has to be right in **one direction**. The stop block's position is forgiving, over-depth is
forgiving, under-depth is not.
FLAG: **Notch the bottom edge of every rib where it meets the bottom skin, roughly 20 × 15 mm.** An
egg crate seals every cell, so without this a corner residue has nowhere to go but its own port.
**This is the only cut that tells a rib which way up it goes**, so it is done after the notching, on
whichever edge ends up down.

**Clamp the skins hard onto the rib edges.** Screws through the skins into the ribs give uniform
pressure and can stay in.

**Assemble the grid and check it flat on a reference before either skin goes on** — an egg crate
self-jigs and holds its own spacing with no clamps.

**The reference is two 4' square sheets of 3/4" MDF stacked, 38 mm thick, on the Festool plywood
cart.** No seam anywhere under the box, and 38 mm of MDF does not sag between the cart's rails.
The box is **1211 square** on a **1219.2** reference, so it lands with **4 mm a side**. Shim the
cart, not the MDF.

**Clamp the perimeter with 52" parallel clamps laid across the top, one over each rib.** They reach
the 1211 with room, and putting each bar on a rib line backs the pressure with structure instead of
pinching unsupported skin. That takes the sides and the front and back; the skin-to-rib pressure is
the screws in item 4 above.

OPEN: **Open: the grid spacing.** Conventional is 200-300 mm. Two constraints: the **first interior rib
in from each perimeter must clear the front corner tenons**, and the **two front-to-back ribs either
side of the back-centre tenon must clear its 86 mm width**. Let the spacing bend to the back-centre
tenon.

SETTLED: **No blocking under the front fins — closed 2026-10-11 on the measurement.** The last
across-rib's front face is at **970** and the fin's base starts bearing at **1006.35**, so it is
**36.35 mm** from a rib. At that distance a 24 mm top skin is not spanning anything; it is a short
overhang off a support that is right there.

NOTE: **The warning this replaces was written before any rib layout existed to check it against** —
"bottom-edge bearing is only worth having if it lands on structure rather than on skin spanning
between grid members", which is true in general and does not bite here. The fin angle's T-nuts are
**69.35 mm** from the same rib and pull *up* rather than bear down; the weak link there is the
T-nut's own grip on the plywood, not the span.

FLAG: **If the fin's bearing is ever wanted harder, move a rib under it — do not add blocking.** A rib
is continuous and a block is not, and the grid is egg crate precisely because continuity is what
gives the two-way plate action.

SETTLED: **And none under the rear plate either — closed 2026-10-11.** Its bottom edge occupies the first
**6.35 mm** of the box's fore-aft run and the back perimeter web occupies the first **18 mm**, so the
plate bears on skin backed by solid wall over its whole footprint, with **11.65 mm of web to spare**
and the 24 mm tongue outboard of that as well. There is no span to block.

FLAG: **The back centre tenon does want blocking, and it is the only one that does.** The two front
corner tenons are snug into the box corners and located by both perimeter walls for free; this one
has the back wall behind it and nothing either side. **Two blocks, one against each of its
across-machine faces at X 562.62 and 648.62**, running forward from the back web to the first
across-rib so each is captured at both ends. NOTE: **They are for location, not bearing** — the tenon
carries no vertical load, all of it is on the shoulder.

### The three posts

**Front left corner, front right corner, and the middle of the back.** Each a **laminated plywood leg,
72 across the machine by 86 fore and aft**, reduced over its **top 116 mm** to a tenon that passes up
through a hole in the bottom skin. The bottom skin lands on the shoulder.

The **72 is the lamination** — four 18 mm strips face to face — and it runs **across the machine** so
the base's fore-aft rails can pass through as a through tenon formed by leaving the middle two strips
out at glue-up. The **86 is the strip's width**, ripped at 90 and trimmed after the glue dries.

| | |
|---|---|
| Ledge to top of post | 116 mm |
| Bottom skin on the ledge | 18 mm |
| Cavity | 100 mm |
| Underside of the top skin | **118 mm** — so the post top stops **2 mm shy** |

**Every ledge is 42 mm, cut on the outward-facing faces**, so the perimeter wall lands directly over
the shoulder. The ledge is as deep as the wall standing on it.

| Post | Faces ledged | Tenon, across × fore-aft |
|---|---|---|
| Front left / front right | the **side** face and the **front** face | **30 × 44** |
| Back centre | the **back** face | **72 × 44** |

**Trim all five legs to the same 72 × 86 after the glue dries** — so the two corner tenon holes are
identical and come off one setup, and the back one differs only in being the full 72 wide. The older
instruction to cut each hole to its own post is retired; it existed when the posts were cedar sticks
that varied.

FLAG: **Square faces matter more here than the width.** The ledge is a cross-cut shoulder and the
perimeter wall lands directly over it, so a post face out of square puts the bearing on an edge
instead of a face.

NOTE: **The holes stay 2 mm generous** — machining the posts makes them identical, not the assembly
easier. A 565 lb box still has to be lowered onto three tenons.

SETTLED: **No screw into the tenons — his call 2026-10-15.** One angled screw per tenon was carried
for the two cases that can separate box from post: road shock above 1 g, which momentarily unloads a
gravity-only joint, and being picked up under the **box** instead of the frame, which leaves the
posts hanging from their tenons. **The strap over the box to the base frame covers both**, it was
always the restraint to rely on rather than the screws, and the screws bought their small margin at
the price of being one of only two steps in the whole glue-up that cannot be undone. **Nothing goes
into the tenons.** Gravity and 99 mm of engagement hold the box, and the strap holds it for a move.

**The box is not otherwise fastened to the posts.** Gravity and 99 mm of tenon engagement hold it.

### Glue up — the order, and the one step that cannot be undone

The six glue joints and what each one carries are in
[`drawings/torsion-box-construction.html`](drawings/torsion-box-construction.html), chapter 5, with
the Domino stations. **Two per web corner, eight in all**, and **a few per side on the outer
laminations** — those are the two joints with nothing else locating them. FLAG: **No Dominos in the
rib ends.** Each rib is already located by its notches and by the bottom skin, so pinning its ends
as well is a third constraint that has to agree with the other two across sixteen rib ends and
sixteen crossings. A rib end half a millimetre shy is harmless now and would be a part that will not
seat.

The order is here because getting it wrong is not recoverable:

1. **Dry-assemble the grid on the flat reference** — four ribs each way into the perimeter webs.
   Press every crossing flat and check it seats. An egg crate self-jigs, so this is the squareness
   check as well.
2. **Glue the grid to the bottom skin**, standing on the reference. That skin's three tenon holes
   are already cut.
3. 🔴 **Fit the fin angles' T-nuts into the top skin from underneath, BEFORE the top skin goes
   down.** There is no access afterwards, ever, and the only fix then is a hole in the box.
4. **Glue the perimeter webs, two Dominos at each corner**, then the **outer laminations** on their
   own pins, the tongues capping the skins' end grain.
5. **Glue the top skin on and clamp it hard onto the rib edges.** Screws through the skin into the
   ribs give uniform pressure and can stay in; the 52" parallel clamps go across the top, **one over
   each rib**, so the pressure lands on structure rather than on unsupported skin.
6. **Sand last, on site**, through the top ports.

### Sand ports — one per bay, through both skins

**25.4 through both skins, 5 × 5 in each, one centred in every bay.** Centres from the skin's edge,
the same figures in X and Y because the box is square and the grid is the same both ways:
**129.5, 368.5, 605.5, 842.5, 1081.5**. The steps are **239, 237, 237, 239** — not a constant
pitch, because the end bays are wider.

Centred, and not for looks: dry sand stands at about a **34° repose angle**, so from a centre hole
the drain crater reaches roughly 100 / tan 34° ≈ **150**, more than the 110 half-bay, and the bay
empties to a shallow corner residue. A port in a corner would strand a wedge.

| | |
|---|---|
| **The plug** | A **rubber plug fitted from below with a pull tab underneath**. Nothing goes in from above and nothing is attached to it |
| **Filling** | Pour each bay full through its top port. **Once, at assembly, before the bed goes down** — the bed cannot come out of the assembled machine and the plates are not to be drilled, so a refill means lifting a Y beam |
| **Draining** | Lying under the machine: **pull the plug out**, the sand runs into a tray, **push it back in**. The CNC is untouched |

**Why a plug needs nothing but friction.** The sand bearing on one plug is a 100 mm column at about
1.5 g/cc over the port's own area — **76 grams**. That is nothing against the grip of a rubber plug
in a hole, so the plug does not need a taper seated from above, a chain, or any access from the top.

FLAG: **A magnet-and-chain scheme was carried for one commit and is retired.** It pushed the cork
**up** into the bay to drain, which made reseating depend on reaching down through the top port —
and the top ports turn out to be the access that is not there.

**The front row of five lands on the open apron**, since the tee track bed runs to 1006.35 and that
row is centred at 1081.5. **Skin the apron with 6.35 Baltic birch on double-sided tape** — a cover
and not structure, so it comes off the day a port is used, and it gives the apron a sacrificial
surface the bare top skin did not have.

**Draining needs the carcases out, and they are built to come out** — pull them and the whole bottom
is open to a tarp or a tray.

FLAG: **This replaces ports low in the front and back perimeter walls, which would not have worked.**
Sand does not walk sideways to a wall port: it would have needed the whole box tipped to a
significant angle, and there is no way to do that to a 565 lb box standing on three posts.

NOTE: **The bays stay connected by the bottom-edge rib notches.** Each bay has its own port now, so
the notches are no longer what makes draining possible — they are kept because they cost one pass
one more cut on the stack and they let a corner residue find a neighbouring port.

### The base

FLAG: **The base comes BEFORE the box, and the legs before the base.** His order, and it is a
prerequisite chain rather than a preference: the base is what holds the three load-bearing legs in
position, so the box cannot be lowered onto tenons that are not yet located. Build the five legs,
build the base around them, then the box.

**The legs are laminated from 18 mm Baltic birch strips** — his, 2026-10-15, replacing dressed cedar
4x4. Strips are **4 ft long**, laminated face to face, and the leg is **trimmed square after the glue
has dried** rather than relying on the stack coming out at size. **Legs are cut to length as needed**,
which is the right way round: nothing in this repo sets their full height, and the length is taken
from the standing base rather than predicted.

SETTLED: **72 × 86 — his, 2026-10-15.** Four strips of 18 is **72**, and that is the lamination
direction, running **across the machine**; the other axis is the strip's own width, ripped at 90 and
trimmed to **86**. **Twenty strips are cut**, four per leg for five legs.

FLAG: **The fore-aft rails pass THROUGH the legs as a through tenon formed at glue-up**, by leaving the
middle two strips out at rail height. 18 + 36 + 18 = 72 exactly, so the rail is two laminations thick
and the gap is two strips — which is why the leg is four strips and not five. It goes at the base's
real weakness, racking, where a bolt through a face does not. Three things to control:

1. 🔴 **The mortise height has to agree across the legs** or the frame sits twisted. Lay all five up
   on **one flat surface with the mortise blocks set off a single stop**, then **cut each leg to
   length measuring from the mortise** and let the floor end take the error. The legs are cut to
   length after glue-up anyway, so that correction is free.
2. **Two mortises at one height in the same leg would intersect.** A leg taking both a fore-aft and a
   cross-machine rail cannot have both as through tenons at the same height — offset them vertically,
   or make one a stub.
3. **Keep every gap well clear of the top**, where the ledge and the tenon are cut and the geometry
   assumes solid material.

#### What the base is

**Two grids that locate and constrain all five legs** — his, 2026-10-15. That is the whole
definition: the base is not a table that happens to have legs, it is two horizontal grids whose job
is to hold five legs in position, three of which the box lands on.

| | |
|---|---|
| **Top of the box** | **1016 — 40"**, his, and it is the figure the base's whole height hangs off. The work surface lands **66 above that at 1082**, because the tee track and two MDF sheets stand on the skin |
| **Legs below the box** | **874** from the box's underside to the floor |
| **Lower grid** | its **underside 100 above the floor** — set by the pallet jack and nothing else, so the forks go under it with the jack lowered |
| **Upper grid** | its **top 10 below the box's underside** |
| **The two side volumes** | **564 of clear height** between the grids. On 2x6 members it would be 484 |
| **Both grids together** | have to carry **800 lb** on a pallet jack: box, sand, machine and base at once. His budget, offered with a question mark, so it is a figure to design past |
| **Five legs** | three at the back — left, centre, right — and two at the front. The box sits on **front left, front right and back centre**; the two rear corner legs carry the grids and the back shear wall |

🔴 **The 10 is the three-point mount.** The box touches three leg tops and nothing else. The moment
the upper grid touches the box there is a fourth and fifth contact point, the mount stops being
determinate, **and the failure is silent** — nothing shows but the two Y beams drifting out of
coplanar. Keep the gap **inspectable**: a feeler or a paper strip has to slide between grid and box
anywhere along it, which is why it is 10 and not 1.

#### Two shear walls, and two volumes left free

| | |
|---|---|
| **Fore-aft wall** | on the **centreline**, from the front of the base back to the **back centre leg** — which is the box's rear support, so the wall lands under the load it braces |
| **Back wall** | across the back, **left rear leg to right rear leg**, taking in the back centre leg on the way |

They make a **T** in plan, which braces both directions, and that is what leaves the **left and right
volumes completely open**. Those two volumes are **free for any use, independent of the base's and the
box's function, and making them as large as possible is a stated goal** — which is what the member
depth is really being chosen against.

**The central wall is two sheets of 18 — 36, the same as a grid member.** That is not a coincidence
and it is what makes the back joint disappear.

#### How the three shear-wall joints actually go

| | |
|---|---|
| **Central wall into the rear middle leg** | 🔴 **There is no joint.** The wall's **two sheets continue as the middle two laminations of that leg** — the leg's outer two strips sandwich them. One continuous piece from the front of the base into the leg |
| **Back wall to the legs** | **Screwed to the back faces of all three rear legs.** A face joint, nothing let in |
| **Central wall at the front** | **The WALL'S END IS NOTCHED and the rail is not touched** — his, and it settles which piece gives way. The notch lets the wall sit on the cross rail, the wall's end face finishes **flush with the outside of the rail**, and **two long screws go through the rail into the end of the wall**. The only work on the rail is drilling for those two screws |

FLAG: **The continuity at the back reorders the build, and it is the one thing here that cannot be
fixed later.** The rear middle leg **cannot be laminated as a part before the wall exists** — its
middle two strips *are* the wall. So that leg is built **with** the central wall rather than before
it, and the "five legs, then the base" order holds for the other four only.

NOTE: **The rail's through mortise and the wall both want the leg's middle two strips.** Where the
fore-aft rail passes through the rear middle leg, the **wall** is what gets notched for it — the same
cut as a rib notch, and for the same reason: whichever piece is continuous wins, and here that is the
rail passing through.

**So the rule across the whole base is one rule: the rails stay whole and the wall gives way.** At the
front the wall is notched to sit on the rail; where a rail crosses the rear middle leg the wall is
notched to let it through; the only cutting a rail ever takes is two screw holes. That is worth
stating as a rule rather than three times as a detail, because it is what makes the frame a frame —
every rail is continuous end to end in both grids.

OPEN: **The front notch is not in the 3D model yet.** The model draws the central wall as a plain
sheet between the two grids, which is right in plan and wrong at the front end. **It needs one figure
— how far up the notch goes** — and then the wall, its lip over the rail and the two screws can all be
drawn.

| Member | |
|---|---|
| **Grid members** | OPEN: **2x6 or a 36 × 100 plywood lamination** — see below. Either way the grid **locates the legs**, and the lower one is also the pallet |
| **Shear walls** | **two**, the T above. OPEN: the three cabinet carcases this file carried are superseded by the two walls and the two free volumes — what fills those volumes is now his to choose |

#### 2x6 or a 36 × 100 plywood lamination

**On section alone the 2x6 wins and it is not close.** A 2x6 is 38 × 140, so against a 36 × 100
lamination it has about **2.9 times the second moment** and **2.1 times the section modulus** in
bending. The two materials' stiffness along the member is close enough to call a wash — Doug fir and
Baltic birch loaded in the plane of its plies are both of order 10 GPa — so the geometry is the
answer.

**And it does not matter, because neither member is working hard.** On the 800 lb budget, with a rail
spanning about 1100 and taking half the lift as a point load, the bending stress comes out near
**4 MPa** in the 2x6 and **8 MPa** in the lamination, against ultimates in the tens of MPa either
way, and the mid-span sag is **under 0.6 mm** against **under 1.8 mm**. A base that is three-point
mounted cannot pass its own sag to the box in any case — that is what the mount is for.

So the choice goes on the three things that do bite:

| | |
|---|---|
| 🔴 **The leg's mortise is already 36** | Two omitted strips leave a **36** slot. A 2x6 is **38** — so a 2x6 rail cannot pass through the leg without chopping the mortise wider, which gives up the whole reason the tenon was free |
| **The side volumes** | 100 deep instead of 140 returns **40 per grid, 80 over the two** of clear height to the volumes he wants maximised |
| **Dimensional behaviour** | Plywood does not crown, cup or twist. A 2x6 does, and **a twisted member in a grid whose only job is locating five legs is precisely the wrong failure** — the same argument that put the box on three points, except here the grid's own stability is the deliverable rather than something the mount protects against |

**So: the lamination**, unless something else wants the depth. The 2x6's advantage is real and sits in
a part of the design that has nothing to spend it on.

FLAG: **Neither grid may ever touch the box.** The moment one does there is a fourth and fifth contact
point, the mount is no longer three-point, **and the failure is completely silent** — nothing but the
Y beams drifting out of coplanar.

- **Clearance 10 mm or more**, not 1 mm.
- **Keep the gap inspectable** — a feeler or a strip of paper must slide between box and grid at
  several points, years from now.
- For transport, use **removable packers** set on the upper grid, taken out on arrival. Not a
  permanent catch.

OPEN: **Open: the box's deflection between its three points under full sand load.** It sets the minimum
clearance and needs the grid spacing and the sand mass first. **The one number here that a wrong
guess would quietly cost accuracy for.**

FLAG: **Edge fastening is what makes a shear wall a shear wall.** **Glue plus screws at roughly 150 mm
all the way round** — to the bottom frame, the top frame, the posts, and carcase to carcase where
they meet. A carcase that merely sits in the void with screws in its corners contributes close to
nothing **and looks identical to one that works.**

OPEN: **Open: where the stabiliser legs go.** Whatever they are, they must be set **deliberately
short** — if they carry load it is no longer a three-point mount.

---

## 9. Set the machine on the box

Both the front fin and the outboard plate land on the **same top skin**. **The fin sets the beam
height and the two beams' coplanarity, so the fin is the reference for the pair and the plate follows it.**

| Part | How it lands |
|---|---|
| **Front fin** | bottom edge **bearing on the top skin**; **one 170 mm 40 × 40 angle in front of it**, tapped M8 into T1 and T2 at Y 20, four bolts into skin inserts |
| **Outboard plate** | bottom edge bearing on the top skin directly over the wall; outer face **bearing against the side tongue's inner face**; **seven M8 from outboard** into locknuts |
| **Rear plate** | bottom edge bearing over the full 1210.73 mm; **eight bolts through the back tongue at Y 30** |

**The side tongue runs 1000 mm, starting 1/4" from the box's back edge** — so it spans exactly the
beam and the side plate it laps, and ends where the fin begins.

OPEN: **The front and back tongue arrangement is inconsistent between the design record and the shop
pack.** The shop pack (2026-10-03, the later of the two) says **there is no front tongue** and the
fin is tied by L-brackets; [`archive/torsion-box.md`](archive/torsion-box.md) and
[`archive/lateral-stiffness.md`](archive/lateral-stiffness.md) still describe a continuous front tongue lapping the
side tongues. **Resolve before the walls are glued up.**

## 10. Fit the spindle and tram

| | |
|---|---|
| Spindle | **Ø80 × 213 mm, 2.2 kW, 220 V, 8 A, 400 Hz** water-cooled, RATTMMOTOR, with VFD, ER20 collet and pump |
| Mass | **5.2 kg** |
| Clamps | **two 80 mm aluminium clamps**, 120 × 55 × 100 mm, one at each end of the barrel |
| Clamp centres | **116 mm** — mid-height at ±58 mm from plate centre |
| Fixing | **4 × M8 × 80 socket head** per clamp, into **tapped** holes in the Z plate |
| M8 rows | **17 and 42 mm from the nearer plate end** ← the drilling dimension |
| Water | two **Ø8 mm** fittings, exiting radially at the rear |

**Orientation: the clamp's 100 mm dimension is front-to-back**, with the 80 mm bore centred in it.
55 mm is axial.

FLAG: **Torque the clamp bolts to ~15 N·m, NOT the ~25 N·m an M8 8.8 would take.** 10 mm of engagement
in 6061 is the limit, not the bolt. **Four M8 helicoils per clamp position** takes it to full spec if
you would rather not have to remember.

FLAG: **Never shim the two clamps against each other.** They bore a round body and must stay coaxial.

**Measure on arrival:** where the water fittings and cable exit sit, the body diameter over the whole
clamping length, and the weight.

### FLAG: Tram here, with the machine bolted down

FLAG: **Tram is set on the installed machine** — standing on the box, bolted to the tongues, in the
position it will run in. Tramming a free-standing assembly sets it against a reference the machine
does not have yet.

**It is set once, and only with the clamps off** — all 16 M8 are accessible only then. There is no
sub-plate and no permanent jacking provision, so redoing it later means lifting the spindle out of
its two clamps.

| Rotation | Where it is taken |
|---|---|
| **Roll** | **Shim between the shelf bar's top face and the X beam's bottom extrusion**, at one end plate only. Shim the low end |
| **Nod** | At the Z plate, using the two outermost M8 rows — one as the hinge, the other as the adjuster. The two middle rows are torqued once the tilt is set |
| Yaw | Does nothing on a round spindle |

**Roll shim stock: 1" wide aluminium strip**, which is exactly the bar's 25.4 width — a strip cut to
the bar's 60 mm length is a full-face shim. **0.03 mm of shim moves tram by 0.003 mm per 100 mm.**

FLAG: **Slot the roll shim open from one edge at Y 15 and Y 45**, so it slides in with the two vertical
M8 loosened rather than removed. A plain rectangle means pulling the beam off.

**Order of work for roll: loosen the four M8, slide the shim in, re-torque.**

OPEN: **Range is capped at about 0.5 mm by the 9 mm bolt clearance**, so the beam is deliberately not
centred in those holes once shimmed.

**For nod, use a row and not a column**, and use the two outermost rows — angular resolution is jack
travel over row separation. **Every bolt above the hinge has to be free** while the tilt is set.

### Then run the stiffness test

**It pushes on the spindle nose, so it cannot run before this stage**, and it is run on the
machine bolted down in its installed position — the condition worth measuring.

PROCEDURE: **Procedure: [`../commissioning/stiffness-test.md`](../commissioning/stiffness-test.md).** Six
indicator positions and a subtraction — **do not improvise it at the machine.** One reading on the
spindle nose is a total, and a total cannot say which part of the stack is moving.

It settles two deferred decisions: whether the X gantry back plate goes from 1/4" to 3/8", and
whether the X carriage plate goes from 1/2" to 5/8". OPEN: **Do not act on either before the test.**
If the carriage plate does move, it goes to **thicker aluminium, not a bolted-on steel backer.**

---

## 11. Fill the sand

**Last, on site.** Roughly 165 lb. Everything above it has to be finished first, and dumping it is
the single biggest lever on ever moving the machine.

### If the machine is moved

| Interface | How it is held |
|---|---|
| Frame to posts | **5/16" bolts** — positive |
| **Posts to box** | **gravity and 99 mm of tenon** — the only non-positive joint in the stack |
| Carcases to frames and posts | glued and screwed — positive |

- **Two straps over the box, down to the lower grid.** This is the restraint, and it is the only one —
  nothing fastens the box to the posts. It is what covers both road shock and a lift taken under the
  box instead of the frame.
- **Put the fork positions under or very near the three posts.** Add a cross member where the forks
  land if the layout does not cooperate.
- **Drain the sand.** ~240 lb box becomes ~73 lb.
- **The CG is high.** Long axis fore-aft, strapped. **Tipping is the hazard, not weight.**
- **Set the removable packers on the upper grid** before the move; take them out on arrival.

**Weigh the assembly on a weighing pallet jack** when it is built, and put the figure in
[`../commissioning/`](../commissioning/).

---

## Still open

Everything marked OPEN: above, and in full in [`open-items.md`](open-items.md). The ones that gate
cutting or drilling:

| | |
|---|---|
| The **4 × HGH20 block hole pattern** measured on the **X/Y** kit — not the Z kit | gates the sixteen M5 in each X end plate |
| Whether the mill holds one height reference across **1210.73 mm** | gates the rear plate |
| Whether X's **two** interposer rows at **105 and 135** both land over beam | gates X's bar |
| The **grid spacing**, and the box's deflection between its three points | gates the skins and the upper grid's clearance |
| The front/back **tongue** inconsistency | gates the box walls |
| The **L-bracket** specification | gates the fin fixing |
| How far past the front riser plane the **spindle** reaches | gates the fin's taper cut |
| The **Z travel floor** against the spoilboard | a machine measurement, taken once it stands |
| Whether the **stiffness test wants the sand in** | the order above runs it at stage 10 and fills at stage 11, because the sand is specified as last. Nothing states whether 165 lb of base mass changes the reading |
| **Torque figures** — only the spindle clamp's ~15 N·m is specified anywhere in this repo | |
