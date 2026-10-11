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
machines with and without it, so parting with it costs nothing on the sale. The four **20 mm
aluminium tee track extrusions** are the expensive part of it and the new machine needs a tee-slot
fixturing surface regardless. There is no case for selling aluminium that would then be re-bought.

**What does not come across is the three 2040 extrusions.** On the Mega V they are the only support
under the rest of the stack, at **500 mm centres**, and that is why the board springs under the
cutter. Laid flat on a continuous plywood top skin the aluminium is supported everywhere and the
spring problem disappears - so the 2040s have no job left, and putting them back under the plates
would re-create exactly the spans being got rid of.

| The Mega V stack, his measurement | mm |
|---|---|
| Three 2040 extrusions, **laid flat** | 20 |
| Four tee track plates, 250 mm × 47" | 20 |
| One 3/8" MDF sheet | 9.5 |
| Six 19 mm MDF strips between the tracks | 19 |
| **Layer sum** | **68.5** |
| **Measured total, and the figure the Z chain uses** | **67.5** |

📌 **The 1 mm between the sum and the measurement is MDF nominal against actual, and nothing in the
envelope moves on it.** The measured total is the one to carry.

## 🔴 The height trap - a thinner stack cannot be surfaced

Bed the tee tracks straight on the box and keep only the 19 mm strips and the surface lands at
**39 mm** above the top skin. The tool tip floor is **45.2 mm**. The surface is then below the tool's
reach entirely, so it cannot be surfaced - which is the one job the sacrificial layer exists for.

**So any stack that drops the 2040s has to put that 20 mm back above the aluminium.** Two 19 mm
layers plus the 9.5 mm sheet over the 20 mm plates gives **67.5 mm**, the same surface height the Z
chain was already worked against, with the aluminium continuously bedded instead of spanning.

| The stack as built on this machine | mm |
|---|---|
| Four tee track plates, bedded directly on the box's top skin | 20 |
| 3/8" MDF sheet | 9.5 |
| 19 mm MDF, two layers, the upper one sacrificial | 38 |
| **Surface above the top skin** | **~67.5** |

**Surface the MDF, never the aluminium.** Bedded on the box the remaining problem is flatness and
tram, not stiffness, and a sacrificial layer the machine can skim solves both. Tee nuts in the
tracks hold the MDF down, counterbored well below the surface so there is depth to skim into.

## How it is anchored

The tee track sections are **47" = 1193.8 mm**, and the clear span between the side plates' inside
faces is **1211.238 − 2 × 3.429 = 1204.38 mm**. The tracks are therefore **10.58 mm short** of the
span - there is nothing to cut off. The gap is split, **5 mm of spacer at each end**, and bolts pass
through the side plate into the threaded holes in the track ends.

✅ **Those bolts only stop it walking.** Bedded flat on the box, gravity holds the stack down; the end
fixing has no hold-down duty, which is what makes a 5 mm spacer in the load path a non-issue. The
bolts land in plywood at the box end, so threaded inserts in the top skin rather than screws into a
ply edge.

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
[`drawings/model-3d.html`](drawings/model-3d.html), 20 thick, z 0 to 20 on the top skin, and the
group toggles off like any other assembly. **The MDF above them is deliberately not drawn** - it is
sacrificial, it gets skimmed, and its thickness is a build-time choice rather than a dimension.

✅ **The envelope sweep clears it at all eight corners of travel**, which is the check that the bed
does not foul the gantry anywhere. (The six overlaps the model still reports are the pre-existing
block-against-front-strip pairs and have nothing to do with the bed.)

⚠️ **The fore-aft placement is a placeholder.** `TT_BED_Y0` puts the bed's back edge 6.35 from the
box's back edge, just clear of the rear plate, which is also where the side tongue and the Y beam
start - and `TT_BED_FORE_AFT`'s 1000 then runs to 1006.35, coincident with the beam run, which is
the only thing that makes the choice better than arbitrary. **He has not said where the bed sits
fore-aft.** One symbol to change if it wants centring on the box's 1156.35 instead.

## Still to measure

- 🔴 **The 58 mm** that the whole 242.5 mm end-plate chain hangs on - an as-built measurement off the
  Mega V, and the file already says the chain is only as good as it. The sole plate clearance above
  derives straight through it, so re-check it on the real gantry before a stack height spends the
  margin.
- **Whether the four tee track plates' top faces come out coplanar** when laid on something flat, or
  need shimming where they meet the box.
- **Whether the vice can bolt straight down to the tee track** with the MDF layers off.
