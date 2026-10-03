# The X gantry end plates

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

**Two plates, 1/2" aluminium, 154 mm wide**, stopping at the **top of the X beam** - identical
below that edge, and the right-hand one carrying a 40 mm **BF12 tongue** above it. They carry the X
beam and ride the Y rails on four bearing blocks.

## 🔴 Reworked 2026-10-02 - the screw and stepper left this plate

The X axis gets a cast stepper frame like the others, mounted on an interposer on **top** of the X
beam and overhanging the end. **Three things therefore come off the X end plate:**

| Gone | Why |
|---|---|
| The **35 mm stepper shaft bore** | the shaft is up on the casting now, above the beam, not through the plate |
| The **stepper mount pattern** | the motor bolts to the casting's own flange |
| Everything in the stack-up **above +60** | the screw support and stepper no longer land on this plate at all |

✅ **Both plate bodies stop at the top of the X beam, +60 from the Y beam top** - only the
right-hand plate's BF12 tongue goes above it. The
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

✅ **It is held down by M8 flange bolts into slide-in T-nuts** - given 2026-10-02, and the same
joint on all three axes: **X on top of its beam, Y1 and Y2 under theirs.** The casting itself never
touches the extrusion; it is tapped into the interposer with M5. Only Z skips the plate, landing
straight on the 1/2" X carriage plate.

✅ **X takes ONE interposer, under the casting at the stepper end** - three across the machine, Y1
and Y2 taking one each. ❌ ~~A second X interposer under BF12~~ was specified and dropped the same
day; BF12 went to a tongue off the end plate instead. See the count table in
[`y-beam-support.md`](y-beam-support.md).

✅ **X's casting interposer is the SAME PART as Y1's and Y2's** - decided 2026-10-02. 60 × 150 ×
3/8", six M8 into T-nuts at rows 82 / 110 / 138, six M5 tapped for the casting. One drawing, three
off. 🔴 **The rows came out of Y geometry**, so the open check is whether all three land over beam on
X, where the bar sits on top and overhangs the end.

❌ ~~**The BF12 interposer, 60 × 80 × 3/8", top-mounting BF12 on 2 × M5**~~ **Dropped 2026-10-02,
hours after it was specified.** X's BF12 **face-mounts on a tongue off the end plate instead** - see
below - which is a 4 × M5 mount into a plate that already exists, against a 5th part plus four more
T-nut bolts. **That leaves THREE interposers, all identical casting bars.**

### 🔴 The BF12 tongue, and it is on ONE plate only

✅ **Given 2026-10-02.** The plate's top 60 mm already covers the end of the upper extrusion and
carries four M8 into its corner bores. **The tongue is a 40 mm extension rising off the top edge
above that 60 mm square**, 60 mm wide, carrying **4 × M5 tapped** for BF12 - **the same pattern used
on the Y end plates / Z risers**, so it is a pattern this repo already has rather than a new one.

🔴 **Only the right-hand plate gets it.** The left-hand plate is the stepper end: the casting and its
interposer sit there, on top of the beam.

✅ **154 mm is set by the bearing blocks, and it is now measured: 154.18 mm for two blocks butted**
(2026-10-02, calipers - see
[`photos/y-bearing-blocks-butted-154.jpg`](photos/y-bearing-blocks-butted-154.jpg)). Each block is
**77.09 mm**. Anything wider eats usable Y travel at both ends.

🔴 **The number was right and the reason this file gave for it was wrong.** It used to read "two
HGH20 blocks end to end with **2-3 mm between**". There is no gap - 154 *is* the butted dimension.

### The block is not one surface - 128.24 is the part that bears

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

## 🔴 The rails come from two different suppliers - do not quote one kit's dimension for the other

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

## Vertical stack-up, from the top of the Y beam

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

## ✅ The plate height: 242.5 mm, set by the Y ball nut - closed 2026-10-02

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

### The 1/4" sole plate - the plate is the tie, not a shared bolt

A **1/4" plate across the bottom of the end plate**, horizontal, at Z −182.5. **Its top face is one
flat seat** taking the end plate's 12.7 mm bottom edge and the nut's mounting face at the same
height. That is what the level bottom buys: any step between them and the sole plate becomes a bent
or shimmed part.

**The nut sits ON the sole plate, bolted up from underneath.** With the housing inverted its
mounting face looks **down**, so the mating surface is below it, and the bolt heads are on the
underside of the sole plate where a wrench can reach them - which was the whole reason for inverting
the nut.

### ✅ The nut's mounting interface, given 2026-10-02

| | |
|---|---|
| Mounting surface | **40 × 52 mm** |
| Fixing | **4 × M5, threaded into the nut body** - not through-holes |
| Pattern | **24 × 40 mm**, centred on the face |
| Edge inset, across the **40** | **8 mm** - 8 + 24 + 8 |
| Edge inset, across the **52** | **6 mm** - 6 + 40 + 6 |

✅ **Both insets close exactly, so the pattern is centred and the sole plate's four holes are fully
determined** once the face's orientation in Y is known. The pattern's 40 runs with the face's 52; its
24 runs with the face's 40.

🔴 **Threaded holes in the nut kill the "one bolt set does two jobs" idea**, which this section used
to claim. A bolt that threads into the nut **terminates** in the nut; it cannot also tap into the end
plate's bottom edge, and in any case the flange is laterally offset from that edge. ❌ ~~"the nut's
own mounting bolts pass up through the sole plate and into tapped holes in the end plate's bottom
edge - so one set of fasteners both mounts the nut and ties the sole plate to the end plate"~~.

✅ **The sole plate still ties the two together - as a member, not through a shared fastener.** Four
M5 up into the nut, and a **separate** set of fixings into the end plate's bottom edge. The scheme is
unchanged; only the mechanism was wrong.

✅ **And this frees the edge-tap size**, which was previously hostage to the nut. Nothing from the
nut lands in the end plate's edge, so those fixings can be **M6** per the wall rule - 3.35 mm each
side of a 12.7 mm edge - rather than being forced to M8. The M8 wall problem this section warned
about does not arise.

📌 **The inset was first given as 7 mm and corrected to 8 the same day.** Recorded only because the
8 is what makes the pattern close on both axes - if a 7 survives in any drawing it is the superseded
number.

### ✅ The face's orientation: the long dimension runs along X - 2026-10-02

**The nut block's long dimension is parallel with the X beam**, so the **52 runs along X** and the
**40 along Y**. Carrying the pattern through - the pattern's 40 goes with the face's 52, its 24 with
the face's 40:

| About the nut face centre | |
|---|---|
| Four M5 at | **± 20 mm in X**, **± 12 mm in Y** |
| Face extent | **52 along X**, **40 along Y** |

📌 **The consequence for the sole plate is that it reaches outboard, not fore-aft.** It needs only
40 mm of the plate's 154 mm Y extent to cover the flange, but 52 mm of span in X - all of it
outboard of the end plate's plane if the face is centred on the screw axis, which would put the
screw axis at least 26 mm out on its own. That is a **constraint on the still-open X offset**, not a
measurement of it.

⚠️ **One interpretation to confirm.** "Block" was read as the **ball nut housing**, which is the
question that had been asked. The other candidate - the Y bearing block - cannot be meant: its long
axis has to follow the rail, which runs along **Y**, so "parallel with the X beam" is impossible for
it. **If "block" meant something else, these four holes are 90° out.**

### ✅ The X offset to the screw axis: 72.7 mm - closed 2026-10-02

**From the end plate's inner face to the Y screw centreline**, assuming the screw runs under the
beam's width centreline:

| Term | mm |
|---|---|
| Plate thickness, inner face to **outer** face | 12.7 |
| Rail and block stack, outer face to the beam's **inside** face | 30 |
| Half the beam width, to the beam centreline | 30 |
| **Inner face to the screw axis** | **72.7** |
| *(From the plate's outer face)* | *60* |

Carrying the 52 × 40 face and the ±20 / ±12 pattern through it, all measured in X from the plate's
**inner** face:

| | X, mm |
|---|---|
| Nut face, inboard edge | **46.7** |
| First M5 column | **52.7** |
| Screw axis | **72.7** |
| Second M5 column | **92.7** |
| Nut face, outboard edge | **98.7** |

🔴 **So this is the cantilever case, not the strip case.** The sole plate reaches about **100 mm** in
X, and the nut's inboard edge is still **34 mm clear of the plate's outer face** - the flange never
comes near the end plate. Drive thrust therefore acts **60 mm outboard of the plate's outer face**,
or 66 mm off its mid-thickness.

📌 **It does not yaw the gantry.** The two screws are offset outboard in opposite senses, so their
moments cancel globally and the X beam ties the pair. What remains is **local**: each end plate is
pushed at a point 66 mm off its own plane, reacted by its blocks' lateral capacity and by the beam.

⚠️ **This is what makes the joint at the plate's bottom edge the weak link**, and why the bracket
form is still open - see below. A horizontal foot bolted only into a 12.7 mm edge is now carrying the
full drive thrust with a 66 mm arm on it.

### ✅ The bottom joint: a doubler block, not an L - decided 2026-10-02

**Two parts, both flat plate:**

| Part | Size | Qty |
|---|---|---|
| **Doubler block** | **154 × 60 × 1/2"** 6061, bolted to the end plate's **outer** face at the bottom | 2 |
| **Sole bracket** | **1/4"** 6061 trapezoid - see below | 2 |

**The doubler gives the plate a 25.4 mm (1") wide seating surface at its bottom**, and the sole
bracket bolts up into that.

❌ ~~**An L with a vertical leg, or a length of angle.**~~ The doubler does the same job with none of
the awkwardness: **everything stays flat plate** - no bending, no angle stock, and the doubler is a
plain rectangle off the same sheet in the same setup.

**Why it is the right fix, and it is a sharper reason than the one the L was proposed on.** The
bracket's bolts are loaded in **shear**, not tension - thrust runs along Y, in the bracket's own
plane - and the shear that matters bears **sideways on the thin wall beside the hole**:

| Seating width | Wall each side of an M6 |
|---|---|
| 12.7 mm, bare plate edge | 3.35 mm |
| **25.4 mm, with the doubler** | **9.7 mm** |

✅ **And the doubler's own bolts pass through the end plate along X, in shear, with full material all
round them** - which was the entire benefit the L leg was buying. It stiffens the plate's bottom
locally too, now its most heavily loaded region.

🔴 **Two rows of bolts across the 25.4, not one row down the middle.** A single row leaves the joint
nothing to resist rolling about Y, and the second row is free once the doubler is there. **That,
rather than the bolt size, is what the doubler actually buys.**

#### 🔴 Correction: the doubler's limit is the lower block row, not the Y beam underside

An earlier version of this section said the clear run was the **62.5 mm** between the Y beam
underside at −120 and the plate bottom at −182.5. **That was wrong** - the doubler is nowhere near
the Y beam. The beam's inside face is at **X 42.7** and the doubler occupies **X 12.7 to 25.4**,
some 17 mm inboard of it, so the beam's underside is not a constraint at all.

⚠️ **What does constrain it is the bottom edge of the lower Y bearing block row**, which sits on the
same face in the same X band. **So the 60 mm height is not yet checkable** - it is gated on the
bearing block pattern, the same measurement as the 16 holes. Likely fine with room to spare, but
unverified.

#### ✅ The sole bracket is a trapezoid

**154 mm at the root, tapering to ~46 mm over the nut, across ~75 mm of reach.**

| | |
|---|---|
| Root width | **154** - the full plate width |
| Tip width | **~46** |
| Reach | **~73 mm**, doubler outer face at X 25.4 to the nut face's outboard edge at 98.7 |

**Why the root is full width:** the 60 mm arm is reacted as a shear couple across the bolt group's
spread **along Y**, so width at the root is the thing that resists it, and 154 takes all there is.

**Why it tapers:** the required section falls off toward the tip, it is **moving mass on the
gantry** so the saving is real, and it matches the machine's own idiom - the front fin is already a
100→200 taper.

🔴 **The tip is ~46, not 40.** 40 would match the nut face exactly, but the nut's M5s sit at **±12 in
Y**, so a 40 mm tip leaves only 8 mm of edge - about 1.45 D on an M5 clearance hole, too tight on the
part taking drive thrust. **46 gives 11 mm**, and the nut's 40 mm face is then fully supported with a
little either side rather than flush to the edge.

⚠️ **The ~46 and ~75 carry tildes on purpose.** Both are shapes rather than fits - nothing mates to
either - so they can be rounded to whatever is convenient when the bracket is drawn. The numbers that
are **not** free are the four M5 at ±20 in X and ±12 in Y, and the root's 154.

### ✅ The tail does not reach the front riser - travel runs out first

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

## 🔴 Why the four bolts are above the Y beam top

Their heads land on the plate's **outer** face - the same face the Y bearing blocks bolt to, where
four blocks occupy a 2 × 2 grid across the full 154 mm. Putting the top extrusion entirely above the
Y beam puts those heads in clear air.

Raising the beam further to expose all eight would raise the whole Z assembly, meaning more Z
extension for the same tool height - and Z extension is the softest direction in the machine. **Do
not raise it for wrench access.**

## Why four bolts is enough

The joining plates tie the two profiles along the whole metre, with T-nuts to within 50 mm of each
end, so the bottom extrusion's load reaches the end plate **through the top extrusion** rather than
needing its own path.

| | Worst bolt at 1000 N |
|---|---|
| All 8, over 60 × 120 | ~830 N |
| **Top 4 only, over 60 × 60** | **~1640 N** |

Against roughly 4800 N of friction capacity per M8 at full preload - about **3× margin**. The shelf
takes the vertical load directly in bearing rather than through bolt shear, which is better anyway.

## Position in Y: as far back as it will go

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

### 🔴 Changed 2026-10-02 - the 25 mm is dead, and why it was abandoned

It used to read *"25 mm from the plate's back edge, putting the beam's back face 10 mm in"*, and the
reason given was that **the 6.35 mm back joining plate takes most of that, leaving 3.65 mm.** That
cover was the only justification the file ever offered for the 10 mm, and it does not survive
examination:

- **It is not structural.** The joining plate's end face is a 6.35 mm edge; the end plate standing
  behind it is end-grain bearing and carries nothing. The joining plate's real fixing is the T-nut
  run along its length.
- **The design already tolerates overhang at that edge.** The shelf bar's holes are dimensioned from
  the **beam front** on a 76.2 mm bar, so it overhung the plate's back edge by ~6 mm even at 25.
  (📌 **The bar is 60 now and overhangs nothing** - see the shelf section. The argument stands as
  the reason the edge was never a hard line.)
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

## The plate is tall, and the beam is what makes that safe

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

## The shelf

🔴 **Reworked 2026-10-02 - a 2" bar, and all four holes re-referenced to the plate's back edge.**

**A length of 1" × 2" aluminium bar** per plate - **25.4 wide × 50.8 tall × 60 long** - spanning
exactly the beam's footprint, **Y 0 to 60**.

✅ **60, not the old 76.2 - shortened 2026-10-02, and it deletes a hazard rather than trimming a
part.** The 3" existed to span *"the beam's 60 mm depth plus the back plate"*. With the beam flush,
its back face **is** the plate's back edge, so the 6.35 mm back joining plate now sits entirely
behind the plate in air and there is nothing back there to reach.

🔴 **And the overhang was carrying a documented trap.** This section used to warn: *"The back
joining plate's bottom edge must be flush with the beam's underside, not proud. The bar passes under
where that plate lands; if it hangs even a millimetre low the gantry sits on a plate edge in line
contact instead of on the extrusion."* **That risk existed only because the bar reached under the
joining plate.** Ending the bar at Y 0 removes the failure mode by construction rather than by being
careful at assembly.

⚠️ **Check the counterbore diameter before cutting to exactly 60.** The vertical at Y 15 leaves
15 mm to the bar's end, which is only ~7.5 mm of wall outside a ø15 counterbore. If it reads tight
on the real counterbore, **65 costs nothing and still stops short of the joining plate.**

**Y is measured from the PLATE'S BACK EDGE, not the beam front. Z is from the bar's underside.**

| Hole | Y | Z | Purpose |
|---|---|---|---|
| Vertical, counterbored from below | **15** | - | M8 up into a T-nut in the bottom extrusion's underside slot |
| Vertical, counterbored from below | **45** | - | M8 up into the second underside slot |
| **Horizontal, blind-tapped M8 in the end plate** | **30** | **15** | shelf to plate |
| **Horizontal, blind-tapped M8 in the end plate** | **30** | **35** | shelf to plate |

### 🔴 Why the datum moved, and it is the whole lesson of this section

The holes used to be dimensioned **from the beam front**. On 2026-10-02 the beam moved back to flush
with the plate's back edge, which put the beam front at Y 60 - and so put the rear horizontal hole,
specified as *"60 from the beam front"*, at **Y 0: off the edge of the plate.** It had been at Y 10
before the move, already too tight for a tapped M8.

**Nothing in the file connected the two.** The hole was a literal computed from a face that moved, with
no link back - the same failure as the "1.8 mm proud" figure, and the reason
[`../dimensions/`](../dimensions/) now exists. **Dimension from the plate's own datum; the beam is not
a datum, it is a part that moves.**

### Why both horizontals sit at Y 30, stacked in Z

❌ ~~Two horizontals spread along Y~~ - **there is only one free Y station.** The verticals are pinned
at Y 15 and Y 45 by the `30-6060`'s bottom-face slot centrelines, they run the full height of the bar
to reach those slots, and two M8 need about **12 mm between centres** for any web. That leaves
**Y 27-33**, so Y 30 and nothing else. Y 30 is midway between the verticals, which is where the
original single bolt already sat.

✅ **So the second bolt goes up, not along - and that is the better axis anyway.** The shelf carries
the beam's weight out in Y, so the bar wants to **pitch nose-down about X**. Resisting that needs the
bolts separated in **Z**: top in tension, bottom bearing on the plate. A single row at one height has
no such couple and leans on face friction. **The 2" bar is what buys the 20 mm of lever**, and the Z
separation is what does the work - not a third bolt.

| | |
|---|---|
| Z separation | **20 mm** |
| Edge to the bar's underside | 15 |
| Edge to the bar's top | 15.8 |
| Y clearance to each vertical | 15 mm centres, ~6 mm of web |

### 🔴 Blind-tap them. Do NOT break through the plate.

**This is the consequence of going to 2" and it was not obvious.** The taller bar drops the lower
horizontal bolt to roughly **Z −96 below the Y beam top**, and the plate's **outer** face at that
height is where the **lower Y bearing block row** sits. A bolt breaking through would hold a bearing
block off its mounting face - which is the one surface on this plate that has to be flat.

✅ **Blind-tapping removes the question instead of answering it.** M8 wants ~10 mm of engagement and
the plate is 12.7, so a blind tap leaves 2-3 mm of skin. **Tap both the same depth** rather than
treating them differently at the bench. The repo already does this where a face must stay clean -
BF12's four M5 are *"tapped into the 1/4in plate - not through-bolted, for maximum engagement"*.

⚠️ **The clash itself is unconfirmed**, because the block pattern is unmeasured - the −96 rests on
the measured 45 mm row gap and not on absolute rail positions. **Blind-tapping makes it moot either
way**, which is why it is the answer rather than a measurement.

⚠️ **A 25.4 mm bar would not have had this problem** - its single bolt at Z −73 sat inside the block
row gap. The 2" bar is still right; this is the price, and it is a drilling instruction rather than a
design cost.

### What the bar clears

| | Z from the Y beam top |
|---|---|
| Bar top, under the X beam's bottom extrusion | **−60** |
| Bar underside | **−110.8** |
| Y beam underside | −120 |
| X end plate bottom | −182.5 |

✅ **The bar's underside clears the Y beam's by ~9 mm** and sits well inside the plate.

Two things to watch:

- **M8 into 12.7 mm of plate** is 1.6 diameters, around 39 kN strip - far above what an M8
  delivers. **Blind-tapped at ~10 mm it is 1.25 D**, which is the same engagement the Z clamp
  bolts run at and was shown there to be ~10× margin. Still not the weak link.
- **The back joining plate's bottom edge must be flush with the beam's underside, not proud.** The
  bar passes under where that plate lands; if it hangs even a millimetre low the gantry sits on a
  plate edge in line contact instead of on the extrusion.

Assembly falls out of this nicely: **bolt both end plates on, slide the T-nuts in, drop the beam onto
the two shelves, then bolt down.** That is a one-person job, which the alternative is not.

## ⚠️ The two plates are identical below the top edge, and differ above it

🔴 **This section said "genuinely identical" and that lapsed the same day, 2026-10-02**, when BF12
moved onto a **tongue off the right-hand plate's top edge**. The body of the two plates - the 154 ×
242.5 outline, the block holes, the encoder bore, the shelf, the sole plate and doubler - is still
one drawing and still common. **What is no longer common is the tongue**, which only the right-hand
plate has.

**It is one drawing with a right-hand variant, not two drawings.** Cut both outlines together and
leave the 40 mm tongue on one; nothing below the top edge moves. ⚠️ **But they are no longer
interchangeable at assembly**, which is the thing the old wording promised and would now mislead.

**Reworked 2026-10-02.** With the screw support and the stepper both off this plate, the thing that
used to differentiate the two ends is gone - and then the tongue put a smaller difference back.

❌ ~~"The plate at the idle end gets no 35 mm hole and no stepper mount holes. Everything else is
common."~~ **Neither end has either any more**, so that particular idle-end variant is gone.

📌 **The BK12-and-BF12-share-a-pattern note is retired too**, along with the "35 mm is enough for
the coupler" working: the coupler now lives inside the casting, not in a bore through this plate.

✅ **And the 35 mm ambiguity resolves itself.** This file used to warn that two different 35 mm
holes would exist in the X end plate - a stepper shaft clearance and the **encoder sensor bore**
from
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md).
**Only the encoder bore remains**, so "the 35 mm hole in the X end plate" is now unambiguous.

---
