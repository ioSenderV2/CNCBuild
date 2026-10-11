# The spoilboard and the Z envelope

Where the work surface sits, and what that costs at both ends of Z travel. This is the file that
closes the **Z travel floor** item the Z carriage budget waited on: the question was never "how much
travel can we get" but "where does the travel sit relative to the spoilboard", and the answer turns
out to be set by the spoilboard rather than by the machine.

> **Read the direction of the trade first, because it is counter-intuitive.** Thinning the spoilboard
> does not buy cut depth, it *loses* it. The tool's reach downward is fixed by the gantry; the work
> surface is what moves. Every millimetre taken out of the stack lowers the surface **away** from the
> tool, and every millimetre added lifts it into reach.

---

## ✅ The Mega V tee track spoilboard is carried over - settled 2026-10-11

The 1 m square T-track spoilboard was a Mega V addon, and used listings split about evenly between
machines with and without it, so parting with it costs nothing on the sale. The four **16 mm
aluminium tee track extrusions** are the expensive part of it and the new machine needs a tee-slot
fixturing surface regardless. There is no case for selling aluminium that would then be re-bought.

🔴 **The profile is non-standard, so every figure for it is his.** 2026-10-11: **16 thick, 250 deep,
47" wide, eight slots, 8 mm opening.** Across the 250 that is **2 × 16 end flats, 7 × 22 inner flats
and 8 × 8 slots**, which sums to exactly 250 - his breakdown, and `TT_PLATE_W_CHECK` is in the
registry to hold it closed.

⚠️ **Two figures in this profile were wrong before that breakdown arrived.** The plate was carried at
**20 thick** for one commit, off his first description of the Mega V stack - the 4 mm comes straight
off the bed's top. And the slot pitch was given as **40**, which needs 280 mm of span across a 250
plate; the flats make it **30**. `TT_SLOT_PITCH` is therefore derived from the flats rather than
stated, because the flats are what he measured and a stated pitch is what went wrong.

**What does not come across is the three 2040 extrusions.** On the Mega V they are the only support
under the rest of the stack, at **500 mm centres**, and that is why the board springs under the
cutter. Laid flat on a continuous plywood top skin the aluminium is supported everywhere and the
spring problem disappears - so the 2040s have no job left, and putting them back under the plates
would re-create exactly the spans being got rid of.

| The Mega V stack, his measurement | mm |
|---|---|
| Three 2040 extrusions, **laid flat** | 20 |
| Four tee track plates, 250 mm × 47" | 16 |
| One 3/8" MDF sheet | 9.5 |
| Six 19 mm MDF strips between the tracks | 19 |
| **Layer sum** | **64.5** |
| **Measured total, and the figure the Z chain uses** | **67.5** |

⚠️ **The sum and the measurement are 3 mm apart and I cannot reconcile them.** The measured 67.5 is
the one the envelope runs on - it is the figure off the real board - but a 3 mm gap is more than MDF
nominal-against-actual accounts for, so one of the layer figures is loose. It changes nothing that
gets built, because the stack on this machine is made up in MDF to suit; it is recorded so nobody
later reads the layer sum as a check on the total.

## 🔴 The height trap - a thinner stack cannot be surfaced

Bed the tee tracks straight on the box and keep only the 19 mm strips and the surface lands at
**39 mm** above the top skin. The tool tip floor is **45.2 mm**. The surface is then below the tool's
reach entirely, so it cannot be surfaced - which is the one job the sacrificial layer exists for.

**So any stack that drops the 2040s has to put that 20 mm back above the aluminium** - and with the
plate at 16 rather than 20 there is 4 mm more to find. The MDF above is what makes it up, and it is a
build-time choice rather than a dimension: aim the **surface at 67.5**, which is what the Z envelope
below is worked against.

| The stack as built on this machine | mm |
|---|---|
| Four tee track plates, bedded directly on the box's top skin | 16 |
| **Ultra lite MDF, two sheets of 25, the upper one sacrificial** | **50** |
| **A fresh surface above the box's top skin** | **66** |

🔴 **Two sheets of 25 mm ultra lite MDF - his, 2026-10-11, and it replaces the 3/8" sheet plus two
19s this table carried before.** Ultra lite is about a third lighter than ordinary board and the
stack covers a square metre, which is the reason for it: that weight sits on top of everything the
posts carry. `MDF_LAYER_T`, `MDF_LAYERS` and `SPOIL_SURFACE` are in the registry and the 3D model
draws both sheets.

⚠️ **The surface is 66, and the Z envelope below is worked on 67.5 - so every figure in it that is
measured from the surface is 1.5 too high, and every spare 1.5 too generous.** It is the safe
direction for the swept clearances and the costly one for reach, and reach has 20.8 mm to give: the
tool tip floor is 45.2 and the interference check measures the tool biting 20.80 into the sacrificial
sheet at the bottom of travel. 📌 **It only ever goes down from 66** - the top sheet is sacrificial
and the machine skims it, so there is no shimming to do and nothing to aim at.

**Surface the MDF, never the aluminium.** Bedded on the box the remaining problem is flatness and
tram, not stiffness, and a sacrificial layer the machine can skim solves both. Tee nuts in the
tracks hold the MDF down, counterbored well below the surface so there is depth to skim into.

## The MDF's own footprint - his, 2026-10-11

**The board only has to cover the range the tool can reach**, which is smaller than the aluminium
under it, so it is cut back on three sides:

| Edge | Where it lands |
|---|---|
| Front | **flush with the tee track bed's front edge** |
| Back | `SPOIL_BACK_SHY` = **200** short of the rear plate |
| Each side | `SPOIL_SIDE_SHY` = **150** short of the side plate's inside face |

That puts it at X 153.43-1057.81 and 206.35-1006.35 fore-aft - **904.38 × 800**.

✅ **It covers the sweep.** The tool tip runs X 192.62-1018.62, inside the board by **39.19 each
side**, and reaches back to 221.95, inside by **15.60**. ⚠️ **The tool overruns the FRONT edge by
45.00** - and that is the aluminium's own edge, so the bed stops there too. Work needing that last
45 mm sits on the tee track with no sacrificial layer under it.

🔴 **The setback also killed a clash the full-footprint board had.** Eight tongue bolt heads stand
**4 mm proud of the bed's back edge** at z 21.35-38.65, which is straight through a lower sheet that
runs to the back. The fix being considered was trimming 4 mm off that edge; 200 makes the question
go away.

## Holding the MDF down - M8 drop-in T-bolts

**His scheme, 2026-10-11.** Drill 8 mm through both sheets at the four corners, with the
**front-to-back hole spacing on the tee track's own slot spacing**, and counterbore from the top
deep enough to take the washer and nut below the surface. Then preinstall the T-bolts in the corners,
drop the whole sandwich onto the aluminium, turn each bolt so its T lines up with its slot, let it
drop in, and tighten.

📌 **The slot grid closes on it.** Slot centres sit at 26.35 + 250 × plate + 30 × slot. The board's
back edge at 206.35 is exactly a centre, and the nearest centre to the front edge is 986.35, 20 mm
back from it - **780 apart, 26 pitches**, so a front-to-back pair lands on real slots with no
fudging.

⚠️ **The bolt is not settled and the holes are NOT in the 3D model yet.** A 40 mm T-bolt photographed
beside the sandwich tops out around the seam between the two sheets, dying inside the board; **he
reads a 50 as the one**, to be measured off the drawer. See the open item.

## How it is anchored

The tee track sections are **47" = 1193.8 mm**, and the clear span between the side plates' inside
faces is **1211.238 − 2 × 3.429 = 1204.38 mm**. The tracks are therefore **10.58 mm short** of the
span - there is nothing to cut off. **Two M5 screws into each end of each panel** pass through the
side plate, each carrying **one 5 mm aluminium spacer** to fill the 5.29. That is **16 screws, eight
through each side plate**.

✅ **The ends are drilled and tapped M5, done 2026-10-11.** 4.2 drill, M5 tap, **15 mm of thread
engagement** gauged off the hole - three diameters, into real depth rather than through a skin, which
closes the question of what the wall thickness at the panel end was. The Mega V's own fixing was two **M4 self-tapping**
screws per end, and none of that carries over.

🔴 **M4 was recommended here and M4 was wrong.** The advice was to drill 3.3 and tap M4, reasoning
that three in-and-out cycles is light duty. **A 3.3 drill entered the existing hole with no
resistance** - his measurement - so the hole was already at or above the M4 tapping size and an M4
tap would have had almost nothing to cut. The cycle count was the wrong thing to judge it on; the
hole size was, and it was measurable the whole time.

✅ **Buy M5 × 20.** Each screw passes through 3.429 of side plate plus 5 of spacer before it reaches
aluminium, so a 20 reaches 11.57 into a hole tapped 15 and clamps with 3.4 of hole to spare. **Not a
25** - that wants 16.57 and would bottom out 1.57 short, tight to the wrist and holding nothing.

📌 **An 18 was the answer an hour earlier, on a depth of 10 rather than 15.** The two
recommendations are opposite off a 5 mm difference in one measurement, which is the argument for
gauging the hole rather than taking the first figure for it.

✅ **The gap and the part are different numbers on purpose.** The gap is 5.29 and the spacer is 5,
which leaves **0.29 per end, 0.58 across the bed** - and that float does not matter, because the
aluminium is not a reference surface and the MDF above it is surfaced in place. 🔴 **The gap was
first written as a spacer thickness**, and 5.29 is not a flat bar anybody stocks, which is exactly
how a part that cannot be bought gets onto a list. The standoff has one job: keep the bolt from
drawing the side plate inward as it tightens.

✅ **Those screws only stop it walking.** Bedded flat on the box, gravity holds the stack down and
the end fixing has no hold-down duty.

🔴 **Nothing in the bed's fixing touches the torsion box.** Both ends land in the **side plates**,
steel to aluminium, and the bed simply rests on the top skin. ⚠️ **This file claimed threaded
inserts in the top skin until 2026-10-11** - an invented detail, from reading his "anchor in either
end with bracket" as a bracket reaching down to the box. Once the scheme became screws through the
side plate into the panel ends there was nothing landing in plywood, and the sentence should have
gone with the bracket. It was then quoted back at him as an argument for a thicker top skin, which
is how an invented detail earns compound interest.

📌 **Hold the stack a few millimetres short of the side plates' inside faces** and the tongue bolt
heads at Y 30 live in a relief gap, with no plate geometry changed. That is cheaper than moving the
bolt line - see below.

## The Z envelope, both ends

Everything here hangs off one figure: **the tool tip's lowest point is 45.2 mm above the box's top
skin**, with the 2" stickout the model carries as a stand-in (`TOOL_L`,
[`../dimensions/VALUES.md`](../dimensions/VALUES.md)). He gave it as 45 and `tools\make-3d.py`
independently puts the tip at Z 197.20 with the down stop 152 below, which is 45.20 - two routes to
the same number. With that stickout the **collet nut face at the bottom of travel is at 96.0 mm**,
and that is the figure that does not move with tool choice.

🔴 **The travel to use here is 226 mm, not the rail-limited 235.91.** The 226 is what the two
mechanical stops leave with the 5 mm standoffs he set on 2026-10-10 - the nut 5 above BF12's face
going down, 5 below the stop block going up - and it is what an operator actually gets.
`Z_TRAVEL`'s 235.91 is the rail-and-block figure, and it is the wrong one for an envelope question.
⚠️ **An earlier pass of this file used the 235.91 and put the ceiling 9.7 mm too high**; every
figure below is on the 226.

| | mm above the box top skin |
|---|---|
| Tool tip, bottom of travel | **45.2** |
| Work surface | **66** - was 67.5, see the stack table above |
| Collet nut face, bottom of travel | **96.0** |
| **Y sole plate underside** - the lowest thing that sweeps | **113.15** |
| Dust shroud frame bottom, bottom of travel | **129.0** |
| Tool tip, top of travel | **271.2** |

**The sole plate figure** comes off the Y beam top at **302** and the sole plate's top face at
**−182.5** from it, level with the inverted Y nut's mounting face, less the 1/4" plate. The spoilboard
runs under it - the sole plate reaches outboard from the X end plate toward the side plate while the
tracks span nearly plate to plate - so this is the swept clearance that matters: **45.65 mm** over a
67.5 surface, or **~41 mm** allowing for the nut bolt heads on the plate's underside. ⚠️ **On the 66
surface it is 47.15**, and the same 1.5 is owed to every other figure here that is measured from the
surface - the four cases below included, where each spare is 1.5 smaller than it says. ✅ **The
spoilboard no longer runs under the sole plate at all.** The brackets sit at X 7.43-105.62 and
1105.62-1203.81 in the model; the MDF spans 153.43-1057.81, so they sweep over bare aluminium and
the clearance that matters there is over the **16**, not over the surface.

**The shroud frame** comes down to the top of the threads on the 23 mm shaft, his. The thread starts
**12 mm** below the nose shoulder and the shoulder is 15 below the barrel face, so the frame bottom
is 27 below the barrel face against the collet nut's 60 - **33 mm above the nut face**. At the bottom
of travel that is 129.0, which is **15.85 mm higher than the sole plate**, so the shroud never
becomes the low point.

⚠️ **The sole plate also sets a ceiling on the stack.** The surface could rise to roughly 100 mm
before the sole plate becomes the limit - well past anything the Z envelope wants, but it is the
number to check against before thickening the stack.

### The four fixturing cases

| Case | What the envelope gives |
|---|---|
| Wood, 2" stock + 1/4" waste board, through-cut | Tip must reach **73.85**; floor is 45.2, so **28.65 mm spare** |
| Vacuum table, 1" + 1/4" waste board, through-cut | Tip must reach **99.25**; **54.05 mm spare** |
| Machinist vice **on** the rotating base, 5.5" | Jaw tops at **207.2**; **64.0 mm** above them for stock and tool |
| Machinist vice **off** the base, 4" | Jaw tops at **169.1**; **102.1 mm** above them |

📌 **Two consequences of the shroud geometry, both checks rather than changes.** The brush skirt has
to reach **61 mm** down from the frame to seal on the surface at full Z down. And frame-to-tip is
33 + 50.8 = **83.8 mm**, so the frame clears the top of any stock thinner than that - 33 mm to spare
on the 2" wood case, and no clearance at all over the vice, which comes off with the shroud.

## ✅ The X carriage does not move down - settled 2026-10-11

Dropping the X carriage **20-25 mm** was on the table, which would have meant flipping the X doubler
and fitting the X sole plate to its bottom edge **before** the carriage went onto its bearing blocks
- an ordering that is irreversible once bolted up.

🔴 **It is the wrong lever, and it makes the machine worse.** A 25 mm drop lowers the floor to 20.2
and the ceiling to 246.2. The floor gains nothing, because the deepest wood through-cut already
clears by 28.65 mm. The ceiling loss takes vice headroom from **64.0 mm to 39.0 mm** - straight out
of the one case the travel was built for, and 39 mm is not much once a tool is in the collet.

✅ **The spoilboard is the adjustable element, and it moves in both directions.** Add layers if wood
depth ever gets tight; strip the MDF and bolt a vice down to the tee track to get the jaws lower for
metal. Reversible in an afternoon, where the doubler flip is not.

## ✅ The Y 30 bolt line holds - settled 2026-10-11

Raising `BOX_TONGUE_BOLT_Y` to clear spoilboard work was considered and rejected.

**It cannot clear the spoilboard.** The tongue stands **60 mm** proud of the top skin and the work
surface is at 67.5, so every bolt on that line is below the surface wherever it sits on the tongue.
Moving 30 to 45 changes which layer sits in front of the head, not whether one does; access still
means pulling spoilboard either way.

**And it costs edge distance.** At 30 the bolt is also exactly 30 below the tongue's top edge, which
is why the tongue came off 61 to 60. At 45 there would be 15 mm above a 9 mm hole - **1.7 × D**,
under the 2 × D confirmed on the template for T2. 40 would still clear at 2.2 × D and buys almost
nothing.

📌 **The 145 mm couple is not in this at all.** T1 and T2 both sit at Y 30 and the 145 is **fore-aft,
in plan** - it is not a vertical lever, so the bolt height does not touch it.

## It is in the 3D model

The four plates and the two end spacers are drawn as the **Tee track bed** group in
[`drawings/model-3d.html`](drawings/model-3d.html), 16 thick, z 0 to 16 on the top skin, and the
group toggles off like any other assembly. **The end gaps are deliberately empty** - what fills them
is one 5 mm spacer per bolt, which has no footprint across the bed, and the model briefly drew a
5.29 × 1000 bar there that does not exist.

**The slots are drawn as the flats between them.** Each flat is a full-thickness bar and the eight
slots are the open gaps, which puts the top face and the 8 mm openings exactly where they are and
invents nothing about the profile below. 🔴 **The undercut and the slot depth are not figures we
have** - a slot drawn as a pocket would need a depth, and a depth would be a guess. The generator
also checks the flats and slots sum to the plate's 250 and fails loudly if they ever stop. **The MDF above them is deliberately not drawn** - it is
sacrificial, it gets skimmed, and its thickness is a build-time choice rather than a dimension.

✅ **The envelope sweep clears it at all eight corners of travel**, which is the check that the bed
does not foul the gantry anywhere. (The six overlaps the model still reports are the pre-existing
block-against-front-strip pairs and have nothing to do with the bed.)

✅ **The bed is captured in both directions, and there is nothing to place.** Across the machine it
fits the 1204.38 between the side plates. Fore-aft, the clear run from the **rear plate's front face
at 6.35** to the **front fin's back face at 1006.35** is exactly **1000 - BEAM_LEN** - and four 250
plates are exactly 1000. It butts the rear plate and finishes on the fin.

⚠️ **This was briefly recorded as a free choice and it never was one.** `TT_BED_Y0` carried a note
saying he had not placed the bed fore-aft; his answer, 2026-10-11, is that the geometry had already
placed it. `TT_BED_FORE_AFT_CHECK` now subtracts the bed's depth from the beam length and must read
**zero**, so if either figure moves the registry says so rather than the drawing quietly going wrong.

## ⚠️ The spacer may not clear the skin - open, being tested

The M5 hole centre in the panel end is **4 mm above the top skin**, and the spacer he is ordering is
**8 mm OD with a 5.1 bore**, stainless. An 8 OD is a 4 radius, so **the spacer's bottom edge is
tangent to the skin** - zero clearance.

🔴 **That is a coincidence, not a fit, and it fails in the direction that matters.** Anything the
wrong way by a tenth and the spacer rides **on** the skin, which lifts the panel end off its
bedding - giving back exactly the continuous support that dropping the 2040s was for. Things that
can go the wrong way: the hole centre on panels he did not drill, spacer OD tolerance, glue
squeeze-out or a proud veneer patch, and the skin not being flat under a 1193.8 panel.

✅ **He is ordering spacers to test it**, 2026-10-11, so `TT_BED_SPACER_CLEAR` stays **OPEN** until a
real one is offered up to a real panel.

**If it fouls, relieve the skin and not the spacer.** 📌 **The reason is that a relief in the skin
cannot lift the panel.** A filed spacer or a thinner one both can, and a 6 OD spacer - 1 mm of
clearance on a 0.45 mm stainless wall, which these no-load screws would carry fine - also depends on
sourcing a part, where cutting the skin depends on nothing.

### ✅ How the relief gets cut: a router groove, not sixteen scallops

**His, 2026-10-11, and it is better than the scallops first proposed** for a reason beyond effort: a
groove does not need the hole positions at all. It only has to be in the right **band**, so nothing
gets marked off the panels - and the panels own the hole spacing, which is not a figure this repo
has.

| | |
|---|---|
| Depth | **1 mm** - turns the tangent into a clearance; nothing in a 25 mm skin |
| Outboard edge, inset from the box's skin edge | **3.429 mm**, the side plate's thickness |
| Width, inboard from there | **about 12 mm** - anything from 8 to 15 works |
| Length | the full fore-aft run the bed occupies, not stopping at the end spacers |

✅ **The side plate stands flush with the box's top-skin edge**, so a router fence off the box edge is
enough - no need to clamp the plate as a fence. The file agrees: BOX_W is measured **inside** the
side tongues and the tongue's inside face is the plate's **outer** face, so there is no channel and
the plate's outer face is the skin's edge.

🔴 **The inset is 3.429, not 1/8".** The plate was ordered **10 gauge** and
[`../dimensions/VALUES.md`](../dimensions/VALUES.md) records that a nominal 1/8" was carried for it
and was wrong. The 0.254 matters only because of which way it errs: insetting 3.175 starts the groove
**0.254 under the plate's footprint**, undercutting the one edge PLATE_H calls the edge that bears on
the top skin. **Inset 3.5 and let the error fall inboard**, where it costs nothing - the width is
slack and the inset is not.

⚠️ **Caliper the delivered sheet.** T_SIDE_PLATE's own note says 10 gauge is a gauge and the gauge is
the nominal, with a standing instruction to measure the real plate. The groove follows the plate in
hand, not the catalogue.

📌 **One thing to decide at the bench rather than here:** whether the groove is cut in the skin
**before** it is glued to the ribs, or after the box is assembled with the plates dry-fitted.

## Still to measure

- 🔴 **The 58 mm** that the whole 242.5 mm end-plate chain hangs on - an as-built measurement off the
  Mega V, and the file already says the chain is only as good as it. The sole plate clearance above
  derives straight through it, so re-check it on the real gantry before a stack height spends the
  margin.
- **Whether the four tee track plates' top faces come out coplanar** when laid on something flat, or
  need shimming where they meet the box.
- **Whether the vice can bolt straight down to the tee track** with the MDF layers off.
- ⚠️ **Whether the 8 mm OD spacer clears the top skin** - ordered to test, and tangent on paper. See
  the section above.
