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
| 3/8" MDF sheet | 9.5 |
| 19 mm MDF, two layers, the upper one sacrificial | 38 |
| Sum | 63.5 |
| **MDF skimmed or shimmed to put the surface at** | **~67.5** |

📌 **Skim, do not shim, if it can be helped.** The upper layer is sacrificial and the machine
surfaces it anyway, so the 4 mm is better spent as thicker stock taken down than as a packer under
the aluminium - a packer would undo the continuous bedding that is the whole point of dropping the
2040s.

**Surface the MDF, never the aluminium.** Bedded on the box the remaining problem is flatness and
tram, not stiffness, and a sacrificial layer the machine can skim solves both. Tee nuts in the
tracks hold the MDF down, counterbored well below the surface so there is depth to skim into.

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
| Work surface | **67.5** |
| Collet nut face, bottom of travel | **96.0** |
| **Y sole plate underside** - the lowest thing that sweeps | **113.15** |
| Dust shroud frame bottom, bottom of travel | **129.0** |
| Tool tip, top of travel | **271.2** |

**The sole plate figure** comes off the Y beam top at **302** and the sole plate's top face at
**−182.5** from it, level with the inverted Y nut's mounting face, less the 1/4" plate. The spoilboard
runs under it - the sole plate reaches outboard from the X end plate toward the side plate while the
tracks span nearly plate to plate - so this is the swept clearance that matters: **45.65 mm** over a
67.5 surface, or **~41 mm** allowing for the nut bolt heads on the plate's underside.

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

**If it fouls, relieve the skin and not the spacer.** Sixteen scallops, roughly 10 across and 1.5
deep, one under each screw, marked off the panels at assembly rather than drilled to a drawing - the
panels own the hole spacing. 📌 **The reason to relieve the skin is that it cannot lift the panel.**
A filed spacer or a thinner one both can, and a 6 OD spacer - 1 mm of clearance on a 0.45 mm
stainless wall, which these no-load screws would carry fine - also depends on sourcing a part, where
a scallop depends on nothing.

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
