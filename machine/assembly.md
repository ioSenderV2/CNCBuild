# Building the machine

**How the machine goes together.** Parts, hardware, and what bolts to what, in the order it is
done.

This document states the build and nothing else. It does not carry the reasoning, the options that
were weighed, or what any figure used to be — that is the design record, the twelve chapters listed
in [`README.md`](README.md), and it is a separate printout. **Where this document and a chapter
disagree, the chapter wins.**

**Drilled hole coordinates are not here.** They are on the sheets in
[`drawings/shop-pack.html`](drawings/shop-pack.html), one sheet per part. This document says which
parts meet, with what hardware, and when.

⚠️ **Items marked Open are not yet specified anywhere in this repo.** They are not omissions from
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
| Steppers | **Y steppers at the FRONT** of the machine |
| Y beams | Fixed — their end plates bolt to the torsion box. Only X, Y-carriage and Z move |
| Spindle | **Ø80 mm, 2.2 kW water-cooled**, 5.2 kg, on two 80 mm clamps |
| Stands on | A sand-filled **torsion box** on **three cedar posts**, on a 2x6 base frame that is also the pallet |

### Rails come from two suppliers

| Axes | Kit |
|---|---|
| **X, Y1, Y2** | one HGR20 kit, one supplier |
| **Z** | a **400 mm** HGR20 kit, **a different supplier** |

**A dimension measured on the Z kit is a Z dimension.** Measure the X/Y kit separately for anything
that sets a plate.

---

## Order of work

**The box is cut from the standing machine, and the spindle goes on after the box.** Two ordering
rules carry the whole sequence, and neither can be worked around:

- 🔴 **The machine is assembled on a flat surface and its width measured off the standing
  assembly.** That measurement is what the box skins are cut to — so the machine comes before the
  box, not after it.
- 🔴 **The spindle and tram come last, after the machine is bolted to the box.** Tram is set in the
  installed position or it is set against a datum the machine does not have yet.

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
| The **1211.75 mm rear plate**, 1/4" steel | two 8-bolt patterns a metre apart |
| Two **X gantry end plates**, 1/2" | one drawing, right-hand variant carries the BF12 tongue |
| **X carriage plate**, 1/2" | 30 holes |
| **Z plate**, 1/2" | |
| **Interposer bars**, 60 × 150 × 3/8", 3 off | six tapped M5 under a bearing face, six flange clearance holes |
| **Both Z spacers** | **face 1 mm off both in the same setup** — see [the Z axis](#6-the-z-axis) |
| Rail mounting patterns, bearing block and nut housing patterns, counterbores | |

| Home drill press | |
|---|---|
| Beam joining plates | 9 mm clearance into T-slots at 150 mm — the T-nut moves to meet the bolt |
| Two **outboard plates**, 12" × 1 m × 1/8" steel | ~25 holes each, and steel runs several times longer than aluminium would |
| Three **front strips**, 45 mm × 1 m × 4 mm | |

**Take the mating hardware, not just the plates.** Bearing blocks, ball nut housing, BK12, BF12,
**the Z ball nut housing**, and **an offcut of the `30-6060` with its corner bores**. Every pattern
gets checked against the real part while still standing next to the mill; a transfer punch through
the real extrusion beats measuring from a drawing.

**One datum per plate.** Pick a corner, dimension every hole from it, never chain dimensions.

**Make one rail the reference and give the second rail clearance** — close-fit holes for rail one,
oversize by about a millimetre for rail two. At assembly, mount rail one, put an indicator on its
carriage and sweep rail two into parallel before tightening.

⚠️ **Open: whether the mill can hold one datum across the 1211.75 mm rear plate.** Bed size is not
travel. The two 8-bolt patterns' relative height must land well inside 1 mm across the metre.
If the part is repositioned mid-job, **indicate the first pattern back in before drilling the second**,
and datum off a scribed and indicated line rather than off a sawn edge.

---

## 2. The beams

Three identical stacked pairs — X, Y1 and Y2. Each is two `30-6060` × 1000 mm.

### Load every T-nut first

🔴 **The `13025` T-nut slides in from the end of the slot.** Once a joining plate or an end plate
closes the slot ends, the only way to add one is to take the beam apart.

| Plate | Slots | Per slot | Per beam |
|---|---|---|---|
| Back plate | 4 — full section height | 7 | 28 |
| Front strip | 2 — flanking the seam | 7 | **14** |
| | | | **42 per beam, 126 for the machine** |

**Seven per slot is first at 50 mm, then every 150.**

⚠️ **The front strip's two slots are the ones that get forgotten** while counting out the back, and
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

🔴 **Bias every bolt the same direction as you tighten it, and bias both rails the same way.** The
hole is a clearance hole and the T-slot adds more float; tighten 17 bolts with the rail floating and
it snakes. **Common mode — both rails pulled the same way.** Do not pull the two rails apart or
together.

📌 **The X beam's rails are already mounted with an opposed bias** — lower rail toward the lower
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

🔴 **The lengths are not interchangeable, and the long one fails silently.** There is
**1.2 mm of air behind the T-nut** (slot floor measured at 9.5, nut back face at 8.3), so a bolt may
reach at most **7.2 mm** past the back of a plate. **An M8 × 12 in the 4 mm front strip reaches 8.0
and bottoms on the slot floor before its head seats** - it feels tight and the strip is still loose.
Engagement is capped at **6 mm by the nut**, so a longer bolt buys nothing anywhere on this machine.
The washer on the Y back is margin, not decoration: bare, that bolt clears by 0.24 mm if the sheet is
the 11-gauge it was sourced as. Full derivation in
[`gantry-beam-joint.md`](gantry-beam-joint.md#-bolt-lengths-settled-2026-10-04---and-the-slot-depth-is-what-settled-them).

**The buy: 42 × M8 × 10 A4 / 316** (front strips) · **56 × M8 × 10 plain + 56 washers** (Y backs) ·
**28 × M8 × 12** (X back). 126 bolts, 126 T-nuts.

🔴 **The front strip is 4 mm, not 1/4".** At 1/4" the flange head rim passes under the bearing block
and hits — there is at most 6 mm of clearance there, and the 1/4" stack is 7.35.

🔴 **The front strip's 14 flange bolts must be austenitic stainless — A4 / 316.** The magnetic
encoder tape runs on this strip's face, and ferromagnetic bolt heads 1 mm from a magnetic scale put a
periodic error at the bolt spacing into the axis. **42 bolts across the three beams.**

⚠️ **Put a magnet on them when they arrive.** Generic "stainless" bolts bought for this job were
tested and **are magnetic**. 410, 416 and 430 are sold as stainless and are as bad as carbon steel
here. **Ask for A4 rather than A2.** Socket heads are fine if A4 flange heads are awkward to source —
a 13 mm socket head leaves more room for the tape than the flange does.

### 🔴 Assemble the stack against a flat reference

Nothing indexes one profile to the other, and the joining plates lock in whatever they are bolted at.
**Both front faces must end up flush**, or the rails are not coplanar and the carriage plate twists
all four blocks.

**Stack front-face-down on a known-flat surface, or clamp a straightedge across both front faces,
before the joining plate bolts come up tight.** This is the moment the rail geometry is set.

### The magnetic tape

**10 mm tape on the face of the 45 mm front strip**, centred between the two bolt rows. Two rows at
±15 with 17.3 mm flange heads leaves about 12.7 mm clear — roughly 1 mm each side of the tape. **All
three beams carry tape.**

⚠️ **Before 3 m of one-shot PSA goes down:** fit a tape offcut and a sensor and **read at the stepper
end against mid-travel.** A NEMA 23 permanent-magnet rotor sits at the min-Y end of both Y tapes.

⚠️ **Open: the application order.** Either the bolts go in first as a guide channel and the PSA is
threaded into a 12 mm slot, or the tape goes down first against a straightedge and the bolts follow.
Not decided.

---

## 3. The Y beam ends

Each Y beam is carried **at its two ends only** — the ball screw runs underneath it, so nothing can
support it along its length.

### The interposer bar and the cast stepper frame — front end

**One part, three off** (Y1, Y2, X): **60 × 150 × 3/8" 6061**, no counterbores anywhere.

| | |
|---|---|
| Bar to beam | **6 × M8 flange bolts into slide-in T-nuts**, three rows at **82 / 110 / 138** from the bar's outboard end |
| Position | the bar's **outboard end 30 mm past the fin's outer face**, so casting and bar protrude through the window together |
| Casting to bar | its **6 through holes, M5 tapped into the 3/8"** — bar coordinates, columns 7 and 53, rows 28 / 58 / 71 |
| Motor | NEMA 23 onto the casting's own flange |

🔴 **At the Y ends everything below the beam is in tension.** Six M8 hold the bar **up** against the
beam's underside, and the casting is bolted **up** into the bar and hangs from its own M5. Nothing
rests on anything.

⚠️ **The casting's foot is stepped, not one flat plane.** Match or clear the step — if the bar sits
under the stepped portion it holds the casting off its bearing face.

⚠️ **Open on X only: whether all three bolt rows land over beam.** The 82 / 110 / 138 rows came from
Y geometry, and on X the bar sits on top and overhangs the end. **Check before drilling X's bar** —
it is the same part, so the check is on the position, not the drawing.

### BF12 — rear end

**4 × M5 tapped into the inside face of the 1211.75 mm rear plate**, one set per beam. Not
through-bolted.

📌 **BF12's hole count depends on its orientation.** Face-mounted into a plate it is **4 × M5**;
top-mounted down through its base onto a horizontal surface it is **2 × M5**. Any BF12 figure that
does not name the orientation means nothing.

### The front plate — the fin

**Two off**, cut from one 12" square: **tapered 100 mm at the top to 200 mm at the base, 302 mm
tall, 10 mm** 6061, with a **60.5 × 50 mm window** below the beam for the casting.

The two halves are **rotations of each other, not mirrors** — turn one 180° and the outline is
identical. Left and right come from flipping one plate over.

🔴 **Lay both hole patterns out from the factory vertical edge and the factory top edge.** Each half
keeps one uncut vertical edge and that is the **outboard** one, taper facing inboard. Laid out from
the cut edge instead, the bandsaw kerf becomes a ~1.5 mm offset built into one plate's bolt pattern —
and that pattern has to line up with formed threads in the beam.

⚠️ **Flipping one plate swaps which face is outboard.** Harmless for through holes; check it before
spot-facing or counterboring on one face only.

| | |
|---|---|
| To the beam | **8 × M8 × 35 flange bolts** into the ø6.65 lengthwise corner bores — four per profile |
| Hole | **9 mm**, deliberately. The bores are extruded features and a close fit is impossible in principle |
| M8 columns | **35 and 65 mm** from the factory edge, so the beam spans X 20 to 80 |
| To the box | **two M8 at X 25 and X 170, Y 30** above the plate's bottom edge — these are **L-bracket holes** |

**M8 × 35 leaves 22.3 mm in the extrusion.**

🔴 **There is no front tongue on the box.** The fin sits on the box's **top skin** and **two
L-brackets behind each fin** tie it down, bolting into T1 at X 25 and T2 at X 170. The box runs
**140 mm past the fins**.

⚠️ **Open: the L-bracket itself is not specified** — no size, no fixing into the box. Four are needed.

**Use a steel backing strip or large fender washers on both faces** where these bolts land in
plywood, not plain washers.

### The rear plate

**One plate for both beams: 1211.75 mm × 12" × 1/4" hot-rolled A36 steel**, P&O if mill scale is
unwelcome.

| | |
|---|---|
| To the beams | **8 × M8 into each beam's corner bores** — 16 bolts total |
| To the box | **8 bolts through the back tongue at Y 30**, 150 mm pitch from X 80.875, plus bottom-edge bearing over the full length |
| Also carries | **BF12 on its inside face**, 4 × M5 tapped, one per beam |

🔴 **1211.75 is a datum, not a dimension.** The plate runs flush with the outboard plates' outer
faces, and Sheet 7's X coordinates are absolute from the plate's left edge. **Cut it over-long and
the Y2 station is out by the excess.**

**Buy 60" stock rather than 48".** A 48" sheet is 1219.2 mm and leaves 7.5 mm of trim, which is the
entire margin on a part cut once.

**Clean the mill scale off before paint. Paint is not optional** — this is steel against aluminium
over a metre of contact.

### The outboard plates

**One per Y beam: 12" × 1000 mm × 1/8" cold-rolled steel sheet.** This **is** the Y back joining
plate — there is no separate 120 mm plate on Y. It runs from the beam down to the torsion box.

| | |
|---|---|
| To the beam | T-nuts along its length, **9 mm clearance** holes |
| To the box | **M8 at 150 mm, first at 50** — seven per beam, at **Y 30** above the plate's bottom edge |
| Direction | from **outboard**: washer, **tongue**, plate, **M8 locknut** on the inboard face |
| Holes | **9 mm clearance** in **tongue** and plate both |
| Position | against the beam's outboard face at X 20, ending **1 mm shy of the beam's end** |

⚠️ **Measure the thickness of what arrives and record it.** Sheet sold as 1/8" is often "11 gauge",
which is 3.04 mm not 3.175. The riser-proud check keys off it.

**Powder coat or paint both faces.** This plate is the chip barrier and it is the part that gets wet
with swarf — aluminium is the anode and the extrusion is what cannot be replaced.

⚠️ **The plate-to-tongue seam is a swarf trap** running the length of the machine. Either seal the top
of it or leave it deliberately open at both ends so it can be blown through.

---

## 4. The X gantry

### The end plates

**Two, 1/2" 6061, 154 mm wide × 242.5 mm tall**, stopping at the top of the X beam. **Identical
below the top edge.** The **right-hand plate only** carries a **60 × 60 BF12 tongue** — the stock's own end, left uncut — rising off the
top edge, 60 mm wide, with **4 × M5 tapped**.

⚠️ **They are not interchangeable at assembly.** Cut both outlines together and leave the tongue on
one; nothing below the top edge moves.

| | |
|---|---|
| To the X beam | **4 × M8** into the **top** extrusion's corner bores, **9 mm clearance**, both pairs **15 and 45 mm from the plate's back edge** |
| To the Y rails | **four bearing blocks** in a 2 × 2 grid across the full 154 mm — two butted in Y by two rows 90 mm apart |
| ø35 encoder bore | **Y 77, 60 mm below the Y beam top** |

**The bottom extrusion is not bolted to the plate at all.** It sits alongside the Y beam, carried on
a shelf.

⚠️ **The 15 mm to the back edge with a 9 mm hole leaves 10.5 mm of material** — the plate's tightest
edge distance. Do not let that hole drift outboard.

📌 **Transfer-punch the corner bores through the real extrusion** rather than working from the 15/45
figures alone.

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

🔴 **M8 × 35, not × 40.** Through 25.4 mm of bar into 12.7 mm of plate, an M8 × 35 gives ~9.6 mm of
engagement and stops short of the far face. **An M8 × 40 protrudes ~1.6 mm onto the Y bearing block
seat** — the one surface on this plate that has to be flat. **Check the length at assembly.**

⚠️ **Check the counterbore diameter before cutting the bar to exactly 60.** The vertical at Y 15
leaves only ~7.5 mm of wall outside a ø15 counterbore. **65 costs nothing** and still stops short of
the joining plate.

### Hang the beam

**Bolt both end plates on, slide the T-nuts in, drop the beam onto the two shelves, then bolt down.**
One person can do it that way.

⚠️ **The back joining plate's bottom edge must be flush with the beam's underside, not proud.** The
bar passes under where that plate lands.

### The X stepper end

**Interposer on TOP of the beam**, overhanging the end — same 60 × 150 × 3/8" part as Y, same six M8
into slide-in T-nuts. 🔴 **On X the parts are in compression, stacked** — the opposite of the Y ends.

**BF12 face-mounts on the right-hand end plate's tongue**, 4 × M5.

### The X carriage plate

**154 mm W × 407 mm H × 1/2"** 6061 — **30 holes**. It bolts to the four X-axis bearing blocks and
carries the whole Z axis. The blue is layout dye, not a finish.

🔴 **Do not make this joint adjustable.** No set screws over the bearing blocks. The bolt heads are
buried under the Z rails, the screw and the nut housing once assembled, and this joint carries
everything. **Build it solid and treat it as a datum.**

---

## 5. The Y ball nuts

The Y ball nut housings run **inverted** on both beams, so their mounting faces look **down** and
their bolts are reachable.

| Part | Size | Qty |
|---|---|---|
| **Doubler block** | **154 × 50 × 1/2"** 6061, on the end plate's **outer** face at the bottom | 2 |
| **Sole bracket** | **1/4"** 6061 trapezoid, **154 at the root → ~46 at the tip, 98.7 overall** | 2 |

**The doubler gives the plate a 25.4 mm seating at its bottom; the sole bracket bolts up into that.**

🔴 **Two rows of bolts across the 25.4, not one row down the middle.** A single row leaves the joint
nothing to resist rolling about Y.

**The doubler's bolts pass through the end plate along X. The sole bracket's go into the doubler** —
M6 is correct there; nothing from the nut lands in the end plate's edge.

**The nut sits ON the sole plate, bolted up from underneath** — **4 × M5 threaded into the nut body**,
at **±20 mm in X and ±12 mm in Y** about the nut face centre. The nut's mounting face is **40 × 52**,
its long dimension running **along X**.

⚠️ **If "block" in the source meant anything other than the ball nut housing, these four holes are
90° out.** Confirm against the real part before drilling.

⚠️ **Open: the doubler's 50 mm height is not yet checkable** — it is gated on the lower Y bearing
block row's bottom edge, which lands at about −127 from the Y beam top. Same measurement as the
sixteen block holes.

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

🔴 **M5 × 35, not × 30.** An M5 × 30 leaves only ~5.9 mm in the bearing block.

🔴 **The Z plate is 164 and the X carriage plate is 154. Do not "tidy" them into line.** At 154
eight of the Z plate's M5 counterbores break out of the edge.

### Face the spacers before assembly

🔴 **The spacer blocks stand 1 mm higher than the ball nut housing.** Skim **1 mm off the spacers —
both in the same setup, at the mill**, so they come out identical. **No shim, and not washers** —
washers bear at four points and tilt the housing, which becomes a side load on the screw.

⚠️ **Measure the 1 mm again before cutting** rather than assuming it is exactly 1.00. The cut cannot
be undone and the spacers are a matched pair. **Take the ball nut housing to the mill** — the 1 mm is
measured against that part.

🔴 **Re-mic both spacers after facing and write the number into the design record.** Everything
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

🔴 **These are sacrificial.** They fire only if the soft limit and the proximity sensor have both
failed. If one is ever used, replace the block and the bolts. Do not size them by strength.

The block runs **7 mm past the rail end** before contact, against **10 mm** of the block carrying no
balls — measured. The bottom end needs no stop; the nut bottoms on BF12 before the rails run out.

**Keep the plastic arbors** that came with the blocks — they are the transfer and storage tool, and
nothing else substitutes the day one is needed.

### Assembly order

**Rails and spacers first, nut housing last.** The rails define the geometry; the nut follows the
screw rather than being forced into position by its own bolts.

**Leave the nut housing's four bolts finger-tight, run the carriage through full travel, then
torque them.**

⚠️ **Open: the Z travel floor.** 246 mm is confirmed available, but where that 246 sits relative to
the spoilboard has never been set — material thickness plus tool length plus clearance over
workholding. **This is the one that gets quietly eroded, and it is the one noticed every day.**
It is a machine measurement, taken once the machine stands.

---

---

## 7. Stand it up and measure it

🔴 **The machine is the datum, not the drawing. The box is not built until the whole machine is
assembled on a flat surface and its width measured.**

The machine jigs itself for that measurement, so nothing has to be computed:

| What sets it | How |
|---|---|
| The two Y beams' spacing | the **X gantry** bridging them — its length, its end plates, the bearing block footprint |
| Their coplanarity and parallelism | the **flat surface** they are assembled on, plus the 9 mm reamed holes absorbing the error |
| The box's top skin width | **measured off that assembly**, once it is standing and square |

**Record the measured width in [`../commissioning/`](../commissioning/) before cutting skins.** Do
not let a nominal or catalogue figure substitute for it.

⚠️ **Bias the top skin wide, never narrow.** The skin's width sets the distance between the two
**tongues'** inner faces, and a tongue's inner face is a hard bearing face with no float. A
millimetre or two too wide is a shim; **too narrow and the plates will not fit between the tongues
at all.** They stand on the top skin and are lapped from outboard - nothing drops into a groove,
but the gap is still a hard dimension.

---

## 8. The torsion box

| | |
|---|---|
| Skins | **19 mm Baltic birch** top and bottom — **25 mm top over 19 mm bottom** if anything is spent |
| Grid | **19 mm strips, 100 mm high**, **egg crate** — continuous both ways, half-depth notches at every crossing |
| Depth overall | **138 mm** |
| Outer walls, all four sides | **two 19 mm laminations, 38 mm total** — the outer one 180 mm tall, standing on the bottom skin and **60 mm proud** of the top skin as a **tongue** |
| Footprint | **1211.75 across** by **1156.35 front to back** — ⚠️ derived, verify against the standing machine |
| Fill | **sand in the cavities, LAST, on site** |

### Four things to get right on the grid

1. ⚠️ **Cut the notches to the measured sheet thickness, not to 19 mm.** Baltic birch sold as 19 mm
   is commonly 18.2-18.5 and varies between sheets. **Test-cut on scrap from the same sheet.**
2. ⚠️ **Notch depth exactly half.** A set cut slightly deep sits low and loses contact with a skin
   along its whole length.
3. 🔴 **Notch the bottom edge of every rib where it meets the bottom skin, roughly 20 × 15 mm.** An
   egg crate seals every cell; without this each cell traps its own sand and needs its own drain port.
4. **Clamp the skins hard onto the rib edges.** Screws through the skins into the ribs give uniform
   pressure and can stay in.

**Assemble the grid and check it flat on a reference before either skin goes on** — an egg crate
self-jigs and holds its own spacing with no clamps.

⚠️ **Open: the grid spacing.** Conventional is 200-300 mm. Two constraints: the **first interior rib
in from each perimeter must clear the front corner tenons**, and the **two front-to-back ribs either
side of the back-centre tenon must clear its 86 mm width**. Let the spacing bend to the back-centre
tenon.

⚠️ **Blocking has to be in the rib layout under the 200 mm fin bases and under the full 1211.75 mm
of the rear plate's bottom edge** — bottom-edge bearing is only worth having if it lands on structure
rather than on skin spanning between grid members.

### The three posts

**Front left corner, front right corner, and the middle of the back.** Each an **86 mm square cedar
post (4×4)**, reduced over its **top 118 mm** to a tenon that passes up through a hole in the bottom
skin. The bottom skin lands on the shoulder.

| | |
|---|---|
| Ledge to top of post | 118 mm |
| Bottom skin on the ledge | 19 mm |
| Cavity | 100 mm |
| Underside of the top skin | **119 mm** — so the post top stops **1 mm shy** |

**Every ledge is 38 mm, cut on the outward-facing faces**, so the perimeter wall lands directly over
the shoulder.

| Post | Faces ledged | Tenon |
|---|---|---|
| Front left / front right | the **side** face and the **front** face | **48 × 48** |
| Back centre | the **back** face | **86 × 48** |

⚠️ **Cut each hole to its own post.** 86 mm is the working figure; S4S 4×4 is commonly 88.9 and
cedar varies between sticks. **Measure the three you have** — a 38 mm ledge on two adjacent faces of
an 88.9 stick leaves ~51 mm, not 48.

🔴 **Drive one screw at an angle into the side of each tenon, from inside the cavity, BEFORE the top
skin is glued.** After that there is no access to those tenons ever again. Not a vertical bolt down
through the shoulder — that is withdrawal from cedar end grain.

**The box is not otherwise fastened to the posts.** Gravity and 99 mm of tenon engagement hold it.

### Drain ports

**Low in the front and back perimeter walls.** They gravity-drain into a bucket and stay reachable.

🔴 **Not in the bottom skin** — the 2x4 frame and three carcases make it unreachable.
⚠️ **Not in the laminated left and right walls** — those are the 38 mm webs the Y beam plates bolt to.

### The base

| Member | |
|---|---|
| **2x6 bottom frame** | locates the posts, **5/16" bolts** through post and frame, **two minimum per joint**. It is also the pallet |
| Clearance beneath | high enough for a **pallet jack to enter and lift** |
| **2x4 top frame** | ties the post tops together, the top chord for the shear walls. Sits **just shy of the bottom of the box** |
| **Shear walls** | three plywood cabinet carcases — rear left, rear right, and one across the front between the two front posts, all openings facing **out** |

🔴 **The 2x4 top frame must never touch the box.** The moment it does there is a fourth and fifth
contact point, the mount is no longer three-point, **and the failure is completely silent** — nothing
but the Y beams drifting out of coplanar.

- **Clearance 10 mm or more**, not 1 mm.
- **Keep the gap inspectable** — a feeler or a strip of paper must slide between box and frame at
  several points, years from now.
- For transport, use **removable packers** set on the 2x4 frame, taken out on arrival. Not a
  permanent catch.

⚠️ **Open: the box's deflection between its three points under full sand load.** It sets the minimum
clearance and needs the grid spacing and the sand mass first. **The one number here that a wrong
guess would quietly cost accuracy for.**

🔴 **Edge fastening is what makes a shear wall a shear wall.** **Glue plus screws at roughly 150 mm
all the way round** — to the bottom frame, the top frame, the posts, and carcase to carcase where
they meet. A carcase that merely sits in the void with screws in its corners contributes close to
nothing **and looks identical to one that works.**

⚠️ **Open: where the stabiliser legs go.** Whatever they are, they must be set **deliberately
short** — if they carry load it is no longer a three-point mount.

---

## 9. Set the machine on the box

Both the front fin and the outboard plate land on the **same top skin**. **The fin sets the beam
height and the two beams' coplanarity, so the fin is the datum of the pair and the plate follows
it.**

| Part | How it lands |
|---|---|
| **Front fin** | bottom edge **bearing on the top skin**; **two L-brackets behind it** into T1 and T2 |
| **Outboard plate** | bottom edge bearing on the top skin directly over the wall; outer face **bearing against the side tongue's inner face**; **seven M8 from outboard** into locknuts |
| **Rear plate** | bottom edge bearing over the full 1211.75 mm; **eight bolts through the back tongue at Y 30** |

**The side tongue runs 1000 mm, starting 1/4" from the box's back edge** — so it spans exactly the
beam and the side plate it laps, and ends where the fin begins.

⚠️ **The front and back tongue arrangement is inconsistent between the design record and the shop
pack.** The shop pack (2026-10-03, the later of the two) says **there is no front tongue** and the
fin is tied by L-brackets; [`torsion-box.md`](torsion-box.md) and
[`lateral-stiffness.md`](lateral-stiffness.md) still describe a continuous front tongue lapping the
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

🔴 **Torque the clamp bolts to ~15 N·m, NOT the ~25 N·m an M8 8.8 would take.** 10 mm of engagement
in 6061 is the limit, not the bolt. **Four M8 helicoils per clamp position** takes it to full spec if
you would rather not have to remember.

🔴 **Never shim the two clamps against each other.** They bore a round body and must stay coaxial.

**Measure on arrival:** where the water fittings and cable exit sit, the body diameter over the whole
clamping length, and the weight.

### 🔴 Tram here, with the machine bolted down

🔴 **Tram is set on the installed machine** — standing on the box, bolted to the tongues, in the
position it will run in. Tramming a free-standing assembly sets it against a datum the machine does
not have yet.

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

🔴 **Slot the roll shim open from one edge at Y 15 and Y 45**, so it slides in with the two vertical
M8 loosened rather than removed. A plain rectangle means pulling the beam off.

**Order of work for roll: loosen the four M8, slide the shim in, re-torque.**

⚠️ **Range is capped at about 0.5 mm by the 9 mm bolt clearance**, so the beam is deliberately not
centred in those holes once shimmed.

**For nod, use a row and not a column**, and use the two outermost rows — angular resolution is jack
travel over row separation. **Every bolt above the hinge has to be free** while the tilt is set.

### Then run the stiffness test

**It pushes on the spindle nose, so it cannot run before this stage**, and it is run on the
machine bolted down in its installed position — the condition worth measuring.

📋 **Procedure: [`../commissioning/stiffness-test.md`](../commissioning/stiffness-test.md).** Six
indicator positions and a subtraction — **do not improvise it at the machine.** One reading on the
spindle nose is a total, and a total cannot say which part of the stack is moving.

It settles two deferred decisions: whether the X gantry back plate goes from 1/4" to 3/8", and
whether the X carriage plate goes from 1/2" to 5/8". ⚠️ **Do not act on either before the test.**
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

- **Two straps over the box, down to the 2x6 frame.** This is the restraint to rely on, not the
  tenon screws.
- **Put the fork positions under or very near the three posts.** Add a cross member where the forks
  land if the layout does not cooperate.
- **Drain the sand.** ~240 lb box becomes ~73 lb.
- **The CG is high.** Long axis fore-aft, strapped. **Tipping is the hazard, not weight.**
- **Set the removable packers on the 2x4 frame** before the move; take them out on arrival.

**Weigh the assembly on a weighing pallet jack** when it is built, and put the figure in
[`../commissioning/`](../commissioning/).

---

## Still open

Everything marked ⚠️ above, and in full in [`open-items.md`](open-items.md). The ones that gate
cutting or drilling:

| | |
|---|---|
| The **4 × HGH20 block hole pattern** measured on the **X/Y** kit — not the Z kit | gates the sixteen M5 in each X end plate |
| Whether the mill holds one datum across **1211.75 mm** | gates the rear plate |
| Whether X's interposer rows at **82 / 110 / 138** all land over beam | gates X's bar |
| The **grid spacing**, and the box's deflection between its three points | gates the skins and the 2x4 clearance |
| The front/back **tongue** inconsistency | gates the box walls |
| The **L-bracket** specification | gates the fin fixing |
| How far past the front riser plane the **spindle** reaches | gates the fin's taper cut |
| The **Z travel floor** against the spoilboard | a machine measurement, taken once it stands |
| Whether the **stiffness test wants the sand in** | the order above runs it at stage 10 and fills at stage 11, because the sand is specified as last. Nothing states whether 165 lb of base mass changes the reading |
| **Torque figures** — only the spindle clamp's ~15 N·m is specified anywhere in this repo | |
