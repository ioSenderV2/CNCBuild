# Shop pack notes — archived

The reasoning that used to sit in [the shop pack](../drawings/shop-pack.html), moved out when the pack became a drilling document. **Nothing here is a dimension to work from** - every number that gets drilled is on its own sheet.


## Sheet 1

**1.1** — **The stock is 10 mm, measured.** Not 3/8" (9.525) and not 1/2". **Each fin is its own piece of plate.** [WARN] **They used to nest, and that is why the top width was 99.625 rather than 100.** Both came out of a single 301.625 square on one diagonal bandsaw cut, which only closed because top + base + kerf had to equal the square: 99.625 + 200 + 2. The base is the reference end — it is the one that bolts down and bears — so it stayed a fixed 200 and the top absorbed the remainder. On its own piece nothing couples the two widths and **the top is a chosen 100 again**. [RED] **The square was never 302 either**: it measures 301.625, the same 11 7/8" as the side plates and the back plate, and that common height is what lets all five parts be dimensioned off one bearing bottom edge.

**1.2** — **ø9, not 8.2, and punched rather than measured.** The bolts land in *extruded* corner bores, whose positions carry looser tolerance than anything drilled in plate, so a close fit is impossible in principle. The joint works by **friction, not bearing** - about 36 kN across eight bolts against loads of one to two kN - so the bolts never touch the hole walls. The nominal pattern is 15 and 45 in from each face; a stacked pair gives 15 / 45 / 75 / 105.

**1.3** — **The window is two stacked clearances, not one opening.** The upper 10 is the **interposer bar** passing through; the lower 40 is for the **casting, 27 tall**. The 13 surplus is the room the casting is **rotated** into - it does not drop straight in. The rotation is **fore and aft**, about an axis across the window, so the clearance it consumes is HEIGHT. The width, 60.5 over a 60 mm casting, is a slip fit and nothing more: if it binds, the remedy is height.
[DONE] **The sheet standing up is what makes that readable.** The bar band is the window's **Y 172-182** top, sitting directly under the beam's underside at 182 — which is where the bar physically is, bolted up to that face — and the casting hangs below it at Y 132-172. Drawn on its side the stack ran along X and the word "upper" contradicted the drawing.
**Assembly:** from behind the fin, casting upside down, stepper-bracket top into the window first, then rotate CCW until the casting lands flat on the bar.
The outboard edge is **aligned on the beam face at X 20** rather than centred on the beam, which puts all the clearance inboard where the taper has already provided room, and makes the window edge flush with the side plate's inner face. [WARN] **That side plate is {{T_SIDE_PLATE}}, not 3.175** — ordered 10 gauge — so the fin now stands **{{FIN_PROUD}}** proud of its outer face rather than 16.825. The window edge does not move: it is on the beam face, and the side plate is outboard of it.

**1.4** — **These two are L-bracket holes, and the coordinates did not move when they became them.** They used to pass through the fin into a front tongue on the torsion box. **There is no front tongue any more** — the box runs 140 past the fins instead, the fin sits on its top skin, and **two L-brackets behind each fin** tie it down. These are the holes their vertical legs bolt to, so the part changed and the pattern did not. **T2's perpendicular edge distance is 19.1**, checked against the physical MDF template, and **the 145 mm couple with T1 is still the moment restraint** — which is the reason to keep the pattern rather than re-pick it for a bracket. **Y 30** also still holds the one bolt height shared with the side plates' and the back plate's rows — it reads as a height now rather than as an X, which is the point of standing the sheet up.

**1.5** — **The taper is gated on spindle clearance.** The spindle is confirmed to pass this plate's plane; the risk is a corner-of-envelope case - low Z, minimum Y, X near the beam. Four numbers decide it and three are unmeasured. **One bandsaw pass, and it cannot be put back.**

**1.6** — **The sheet stands up now, and that is what put it on the same numbers as Sheets 7 and 9.** It used to be drawn with the 302 lying along the mill X and the width measured off the outboard factory edge, so the eight beam-bore holes read X 197 / 227 / 257 / 287 and Y 35 / 65. Those are the same eight holes; the frame turned. Standing the plate up with **Y measured from the bearing bottom edge** makes them read **Y 197 / 227 / 257 / 287** — which is literally the set Sheet 7 carries for the rear plate's beam bores and Sheet 9 carries for its T-slot rows, because all three plates stand on the same top skin and the beam's height comes from **this plate's window** rather than from any plate edge. The two L-bracket holes land on **X 25 and 170, both at Y 30**, which is how y-beam-support.md had always written them. **Nothing moved. Three sheets now say the same numbers the same way round**, and that is the whole value of the change.

**1.7** — **1a and 1b are the same part, and the sheets are separate anyway.** Every feature on this plate goes through — eight clearance holes, a window, two bracket holes — and the outline is a right trapezoid whose straight edge is the outboard one. Turning the plate over about that straight edge maps it onto itself and leaves every feature at the same distance from it. So **one pattern, drilled twice**; Y1 presents one face outboard and Y2 the other. [RED] **Do not mirror the pattern.** Mirroring it within a fixed frame is a different part and would put the bolt columns 125 and 155 from the outboard edge instead of 35 and 65. The sheets are split per beam because what differs is **which way the part is installed**, and that is worth a page each at the machine rather than a parenthesis on one. **1a as drawn is the view from the front; 1b as drawn is the view from the rear.**


## Sheet 2

**2.3** — **The plate's tightest edge distance.** The beam's back face is flush with the plate's back edge, so the 15 is anchored and the 45 follows from the corner bores being symmetric in a 60 × 60. **15 mm of edge leaves 10.5 mm of material beside a ø9** - do not let it drift.

**2.4** — **Bore it first, but it no longer sets anything.** Its height is the Y beam's **seam** centreline, which the vertical chain puts at **{{BEAM_SEAM_XEP}}** — the plate's bottom end {{XEP_SOLE_TAB}} below the nut plane, the nut face 55 below the beam, and the seam {{EXT_W}} up from the beam's underside — so the number drawn here is that chain exactly, not an independent choice. It sits in the gap between the block rows, which is **46** by geometry. That gap is a **KEEP-OUT, not something to lay holes out from**: the magnetic linear encoder tape runs down it and this ø35 sensor rides over the tape, both centred on the seam. The **measured 45 is kept as the conservative figure** for it — under-stating a keep-out is safe — and at 45 there is **5 each side of the sensor, so no room for a flange or clamp ring**. Y 77 is half of 154, so it is centred on the plate as well as on the block pattern.

**2.5** — **Where the sixteen come from.** They used to be laid out off the **measured 45 mm gap** between the block rows, which put their centres 44.5 either side of X 115. **That was the wrong driver.** The blocks sit on the rails, and both rails go in the beam's **outside T-slot** - 15 in from each outer face of a 120 beam, so **90 apart**, centres at the seam ±45 = X **70 and 160**. The gap that follows is 46, not 45; the 45 was a measurement off the machine and is only conservative, never wrong, for the clearance it is used for in 2.4. **The correction moved all sixteen holes 0.5**, which an ø5.2 clearance on an M5 cannot absorb, so it had to be made. The 32 × 36 bolt pattern is the kit's own, measured. The butted pair reads 154.18 against a 154 plate - that 0.09 of overhang at each end is **end cap**, which carries nothing, so the pattern is centred on the plate and the Y values are round. **Measure the X/Y kit, not the Z kit**: they are different suppliers and have only happened to agree so far.

**2.6** — **Machined separately, aligned on Y and offset on X.** The doubler is *not* clamped to the plate and drilled through — each part is machined on its own. Hold the doubler **the short way**: X along its 45 from its tapped end face, Y along its 154 from the plate's back edge. **Its Y values are the same numbers 2a carries; its X values are {{DOUBLER_BOTTOM_X}} less**, because the plate reaches that far past the block's end face to back the sole plate — so the D column is {{DOUBLER_BOLT_X}} here and {{DOUBLER_BOLT_X_PLATE}} on 2a. These bolts run along X through the plate, in shear. The doubler is 154 × 45, which is the width of the offcut the pair comes out of; its gap to the lower bearing block row is {{DOUBLER_BLOCK_CLEAR}} and a 60 would overlap.

**2.7** — **One root row, into the doubler, and nothing into the plate.** The **doubler's** four root holes are drilled and tapped as part of machining the doubler — Sheet 2d's R1-R4, the only edge holes on this assembly that need the mill. The plate itself takes **no** bolts from the sole plate: it reaches **{{XEP_SOLE_TAB}}** past the doubler's end face, and the sole plate's base **butts that strip**. A face it sits against locates it better than a second row of bolts would, and it is the X carriage's joint the right way up.
**20 deep max**: a ø{{M5_D}} doubler bolt at X {{DOUBLER_BOLT_X}} spans 22.5 to 27.5, and R1-R4 stop at {{SOLE_ROOT_TAP_DEPTH}} — {{SOLE_ROOT_WALL}} short of it. {{SOLE_ROOT_ENGAGE}} of thread is all the bolt needs, so the cap costs nothing.

**2.8** — **M8 × 35, not × 40.** These break out onto the face the **lower Y bearing block row** seats against, and a protruding bolt there would hold a block off its mounting face - the one surface on this plate that must be flat. Through 25.4 of shelf bar into 12.7 of plate, an M8 × 35 gives ~9.6 mm of engagement and stops short; an M8 × 40 protrudes ~1.6 mm. Blind-tapping used to make that impossible by construction; with a through hole the **bolt length is the safeguard**.

**2.9** — **The two plates are no longer interchangeable.** Everything below the top edge is one drawing - outline, block holes, encoder bore, shelf, sole plate and doubler all common. Only the right-hand plate carries the BF12 tongue, which is the stock's own far end left uncut over the upper extrusion's end, with the same 4 × M5 pattern the Y end plates use.

**2.10** — **60 long, and the change deleted a hazard.** The bar was 76.2 to span "the beam's 60 mm depth plus the back plate". With the beam flush, its back face **is** the plate's back edge, so the joining plate now sits entirely behind the plate in air. The old sheet warned that the joining plate's bottom edge had to be flush, never proud, or the gantry would sit on a plate edge in line contact. **That risk existed only because the bar reached under it.** Ending at Y 0 removes the failure mode by construction.

**2.11** — **[WARN] Check the counterbore diameter before cutting to exactly 60.** V1 at Y 15 leaves 15 mm to the bar's end, which is only ~7.5 mm of wall outside a ø15 counterbore. If it reads tight on the real counterbore, 65 costs nothing and still stops short of the joining plate.

**2.12** — **Separated in Z, not in Y, and that is the better axis.** Both sit at Y 30 because the vertical T-nut bolts hold Y 15 and Y 45 and two M8 need ~12 mm between centres - so Y 30 is the only free station. Stacking them 20 mm apart in Z resists the bar pitching nose-down, which is the load that matters.

**2.13** — **ø8.4 on all four, and the reason is the shim.** Roll is trammed by shimming
between this bar's **top face** and the X beam's bottom extrusion, so the bar is the platform that
shim bears against. The bar carries its share of the gantry into the end plate by friction and bolt
shear, and if that joint ever slips the bar drops by whatever radial clearance the holes have —
**0.5 mm on a ø9, which is the whole roll adjustment, against 0.2 mm on a ø8.4.** It costs
no adjustment range, because the shim goes above the bar and these bolts do not move when roll is set.
**Drill the bar's P1 and P2 first and spot the plate's H1 and H2 off the bar** — the bar's are
through and the plate's are blind, and at this fit the two pairs have to agree closely across the 20 mm
between them. The verticals get the same fit for the opposite reason: they are **slackened** to slide
a shim in, and a loose hole would let the bar shift in Y on re-torque and walk off the T-nuts.

**2.13** — **The tongue's X carries the interposer, because the interposer is under the casting.X 235 is the top of the X beam's upper extrusion**, and both rows are measured up from it. The cast stepper
frame at this end **does not land on the beam**: a **10 mm interposer sits between beam and casting**, so
the frame and the screw it carries both stand 10 higher, and the holes that mount BF12 must be drilled where the
screw actually ends up. So the X is two terms, both forced — **7 and 25 above the beam top** give 242 and
260 bare, **plus 10** for the interposer, giving **252.0 and 270.0**. The 7 and 25 are Sheet 7's own
offsets before *it* took the interposer; there are **three interposers — Y1, Y2 and this end** — so
the same screw has the same arrangement at all three.

**The sign is an addition on both sheets, for opposite physical reasons:** the Y stepper frames hang *below*
their beam and the interposer drops them further, while this tongue sits *above* its beam and the interposer
lifts it. On each sheet's own frame, measured from its own beam face, both are +10.

**The Y columns are forced too.** BF12's 46 mm column spacing centred in the tongue's 60 gives **7 and 53**
— the same two columns Sheet 7 uses, and the same 7 / 53 measured on the cast stepper frame.

**T_INTERPOSER is a measured 10** — a metric plate, not the 3/8&quot; this chain once assumed. If it
ever reads otherwise, **both rows move by the difference and so does the casting**, together, which is the
point: they are one assembly on one shim.

**The tongue's own length is not in that chain.** It has a floor and no target: it must reach both rows of
BF12's mounting bolts, which is **40**, and the 300 stock gives **65**. Below that floor the block overhangs
unsupported plate; above it, longer buys nothing but edge distance.

**2.14** — **The corner cut.** Both plates lose the far-front corner on a straight line ending at **X {{CORNER_CUT_X_END}}, Y {{XEP_W}}** — 2a from **X {{XEP_CUT}}, Y {{CORNER_CUT_Y}}**, 2b from **X 300, Y {{CORNER_CUT_Y}}**. **Y {{CORNER_CUT_Y}} is where it has to start:** below that is the upper extrusion's end and the plate must stay full length to cover it; above it the corner carries nothing. **Clearance, computed and not measured:** the nearest feature to either line is the far-upper bearing block M5 at **X {{BLOCK_HIGH_COL_B}}, Y 133.5** — **19.9 mm** from 2a's line and 23.4 from 2b's, so a ~ø10 counterbore leaves about **15 mm** of material on the tighter one. The cut's end and that block both sit on the beam, so both carry the plate's {{XEP_SOLE_TAB}} and those two figures hold. Nothing else comes near: E1-E4 are all at Y 45 or below, and the ø35 bore is 100 clear.


## Sheet 3

**3.1** — **Both rails are tapped M5, fixed.** Seven holes each at a 60 pitch, **20 from each end of the 400 mm rail**. The rails are set flush with the plate's bottom edge, so they finish 7 short of its top - that is just what 407 minus 400 leaves, and the rail outlines on the drawing show it.

**3.2** — **These cannot be adjusted later.** Their heads are buried under the Z rails once assembled. **Tram is set here, once, at build.**

**3.3** — The plate exists and is dyed. Rails, BF12, the four X blocks, the Z casting and the sensor bore are all dimensioned; **only the top stop is open**.

**3.4** — **The top stop is a bolt-on block now, not a plate with a lip.** The idea of a stop plate overhanging the carriage is dropped. In its place is a **1" 6061 block, Sheet 3c**, bored ø22 so the Z screw passes through it and bolted flat to the carriage plate's front face by two M5. All this sheet carries for it is TS1 and TS2 — two tapped holes at X 322.7, Y 62 and 92. **Nothing else on the plate is near them**: the closest rail holes are at X 320 and 380 but out at Y 20 and 134, and the Z casting pattern does not start until X 360.

**3.5** — **X 10 puts the support flush with the plate's X 0 end.** The two holes are 46 apart, centred on Y 77 - the plate's mid - so 54 and 100.

**3.6** — **The cantilever is deliberate.** The bottom ~150 is over the X gantry and the rest stands above it, which is how the owner's Mega V is built: 300 mm rails there give 150 over and 150 in air, and the 400 mm rails here add the height.

**3.7** — **X 398.5 leaves 8.5 mm to the plate's end**, so a ø4.2 drill leaves about 6.4 mm of wall. It used to be 403 with 4 mm, and the 4.5 it moved is what the casting gained when it was remeasured at 77. The pattern is the casting's own - spacings 13 and 30 along X, 46 across - the same six holes the interposer carries on Sheet 6, and those spacings matching is how the shift was caught: both sheets drew the same pattern from different ends and only one had been corrected.


## Sheet 4

**4.1** — **Edge distance and the rail pitch together set the 164.** The outer M5 column sits **73** from plate centre and the counterbore is a measured ø8.9, so it reaches 77.45; at 164 the half-width is 82 and they clear by **4.55**. [RED] **The 73 is the reason the width is EVEN.** It is the rail column (57) plus half the block's own bolt pitch (16), and the rail column is 57 because Sheet 3a insets both rails 20 from the plate edges - a 114 pitch. On a 115 pitch the columns would be ±73.5 and ±41.5, and then an odd width is needed for the C-holes while the nut and clamp holes go to half millimetres. **164 and 114 go together, and 165 and 115 went together; the sets cannot be mixed.** The plate also has to cover the spacers, which needs 164 on its own. [WARN] The plate was briefly specified at 165 while the pitch was believed to be 115.

**4.2** — **Clamp bolts.** They pass through the clamp, where the clearance is, and thread into this plate - ~15 N·m, 10 mm of engagement, which is 1.25 diameters and develops roughly ten times the margin the clamp reaction needs. The footprint is 122 × 55 centred on ±58, with the 100 × 25 pattern centred in it, which is what leaves 2 mm of relief at each plate end.

**4.3** — **Why the clamp centres are 116 and never 144.** Spread the clamps far enough and an M8 column walks into an M5 column until the two features physically overlap - there is no counterbore depth that fixes a hole in the same place as another hole. The specific numbers that first showed this are dead (they were computed on the ±41.5 columns and a ~ø10 counterbore), but the shape of the constraint is not: **the clamp bolt columns and the block bolt columns share this plate and the clamps are the ones free to move.** See 4.9 for where that freedom was deliberately not spent.

**4.5** — [RED] **Drill 5.2, counterbore, then open to 6 — and the order is forced.** The counterbore is piloted 5.2, so the hole must BE 5.2 while it is bored; open it first and the pilot has nothing to steer on. [RED] **It is also a one-way door:** once a hole is 6 the pilot no longer fits, so there is no second attempt at the depth. Prove the depth on the first hole of a group, do that group's counterbores, and only then open them. The 6 is cut with an **end mill, not a reamer** - a reamer takes 0.1 to 0.3 and follows the hole it is given, so it can neither remove 0.8 nor move a hole. [WARN] **TWO WEBS, SO TWO DEPTH SETTINGS: 4 mm on C1-C16, 6 mm on N1-N4.** The 4 is forced only where the bolt also crosses the 15.2 spacer - at a 6 web an M5 × 25 would engage 3.8 in the block, under a diameter. The N bolts cross only the web and the shim, so they can afford the thicker one, and it leaves 2 mm more material under the four heads that sit beneath the lower clamp. **The web is specified rather than the depth** because engagement is bolt less web less what lies between, so a web target holds whatever the plate measures - caliper the plate, subtract the web, dial that depth.

**4.6** — **The four N holes must be counterbored, and it is not for the look of it.** They thread into the ball nut housing, which is behind the plate, so their heads land on the FRONT face - and the lower spindle clamp's footprint runs X 2 to 57, which contains all four. **Proud heads would hold the clamp off the plate.** They take the same 5.2 pilot and ø8.9 bore as C1-C16 but a **6 mm web**, not 4. **The housing is ALUMINIUM and gets tapped from its as-supplied 8 mm to 12**, then takes **M5 × 16** for 9.7 of engagement. **The 12 is measured:** a spare housing was tapped as deep as the tap would go, an M5 × 30 run in until it bottomed, and 16 left standing out - so a bolt reaches **14**, and 12 holds it 2 clear. That 14 is the **plug tap's** limit, not the hole's. [WARN] **The deeper tap is margin, not a requirement.** This joint is loaded in SHEAR and a bolted joint carries shear by friction, so what it needs is preload - and at the as-supplied 8 mm thread the aluminium already stripped at a higher load than the bolt itself could reach. **Torquing these four properly matters more than the last few millimetres of thread**, because their holes are 6 mm clearance on M5 and a joint that slips gives up to a millimetre of Z lost motion. [WARN] **M5 × 20 is too long even on the tapped housing**, reaching 13.7. [WARN] **And these are NOT the M5 × 25 that C1-C16 take** - two lengths, two webs, holes that look alike from the front.

**4.7** — [WARN] **Two numbers on this sheet are open, and both are thicknesses.The plate's** is a nominal 12.7 while the half-inch stock for the X end plates measured 12.19 - it is absorbed by both webs, so caliper the plate and subtract. **The new spacer bar's** is unmeasured and sets how much of the M5 × 25 reaches the bearing block - mic the FACED pair, since both bars are skimmed in one setup and the starting thickness feeds nothing. **Neither moves a hole on this sheet; both move a depth or a bolt.** [RED] **The two tapped holes this plate bolts into read identically and are different problems.** Both are M5 with 8 mm of thread as supplied. The **bearing block is STEEL** and its hole is 8.7 deep - 0.7 of chip space, nothing to tap into, and nothing needed, because 5.8 mm is 1.16 diameters and steel is content with about one. The **nut housing is ALUMINIUM** and its hole is 16 deep - so it gets tapped to 12, because aluminium wants about two. [WARN] **The 8 mm of plain hole below a thread is NOT usable travel**: it is tap-drill diameter, about 4.2 on an M5, so a 5 mm thread cannot enter it and a longer bolt simply jams. Chip space is not depth.

**4.8** — **The access holes are the reason the bearing blocks are spread at all.** A 4 mm hex driver passes through here and through the spacer into the 9.91 gap between each rail's pair of blocks, to reach a rail bolt beneath; slide the carriage to bring each rail bolt under it in turn. That lets the Z plate, spacers, blocks and rails be built as one sub-assembly on the bench and then bolted to the X carriage plate by fastening the rails LAST - and lets the whole assembly come off again. They sit on the rail centrelines, at Y 25 and 139, and on X 87.5 which is the gap's own centre. **The driver needs about 36 mm of reach past the handle**: 12 of plate, 15 of bar, 8.5 of rail counterbore. It costs 9.91 mm of Z travel, 245.82 down to 235.91.

**4.9** — **The clamps were deliberately not moved to buy hole clearance.** The tightest counterbore-to-tap bridge on this plate is **4.88 mm**, between a C-hole and the outermost M8. Spreading the clamp pair 2 mm - spending the end relief - would take it to about 6, and that was nearly done. [RED] **It would have been the wrong trade.** The clamps already sit 12.5 mm outboard of the block centres, and z-carriage.md wants them OVER the block centres because then the load goes straight into the blocks and the plate does no bending - it says plainly that plate bending is the soft thing, so alignment matters more than spread. The overhang is cube law: 12.5 to 14.5 is 56% more on that term, to gain wall that 4.88 does not need. **The clearance came from the rail pitch instead, which cost nothing.**


## Sheet 6

**6.1** — **X 0 is the bar's outboard end** - the end that protrudes past the fin's outer face and goes through the window. How far it protrudes is not chosen: the bar slides along the beam until the casting's bearing contains the screw's journal, and INTERPOSER_PROUD is whatever that leaves, currently 16.5. 123.5 of the bar then sits over beam, which is the only part that can reach a T-nut.

**6.2** — **The casting's own six holes**, tapped into 10 mm = 2.0 diameters of engagement, at the top of the 1.5-2 band aluminium wants. The thread shears near 18 kN against an M5 class 8.8 bolt breaking near 11, so the plate thread outlasts the fastener.

**6.3** — **No counterbores anywhere.** Row 135 leaves 15 mm to the bar's inboard end, against the ~9 mm half-head of an M8 flange bolt.

**6.4** — **X inherits these rows from Y geometry, and there are two of them now.** They were 82 / 110 / 138 when the bar stood 30 past the fin and the casting was thought to be 72.5 long. **The 82 row is gone and the other two moved in to 105 and 135:** the bar slid back to meet the screw, the casting measured 77, and an M8 flange centred at 82 lands on its face. 105 clears that face by 28, so its flange clears by 19. On X the bar sits on *top* of the beam and overhangs its end. **Check both land over beam before drilling.**


## Sheet 7

**7.1** — **The length is a stackup, not a window, and that is what sets every X on this sheet.** His stackup: the X beam is 1000, and each side adds a 12.7 end plate and a 30 rail-and-block stack, so the beams' inboard faces are **1084.38** apart. Each beam as assembled is **60 + 1/8" = 63.175** across, the side plate being outboard, so the rear plate taken flush with the side plates' outer faces would be **1210.73** — which is NOT how it is placed any more. [RED] **Its left edge goes on the Y1 extrusion's outboard face instead**, his call 2026-10-10, so the side plate is proud of the plate at that end and the far end falls where the bought **1210.47** puts it. The stackup still sets the holes; it no longer sets the edge. That is the same ~1212 that **lateral-stiffness.md already named as the MAXIMUM** — past it the rear plate becomes the proud member at the corner, the one direction the side tongue's face bearing cannot take — so this length is pinned to its upper bound, not pushed through it. Butting the plate between the side plates instead would give a rounder 1204.38 and put Y1's corner back on X 0, but it lands A1 and A9 exactly on their 15 mm edge-distance minimum with nothing left for a short cut; the overlap buys **3.175 of margin at the eight most loaded holes**, and the beam ties both plates anyway, so the corner joint carries nothing either way. **The consequence to respect: the plate's left edge is the WCS origin now, not just an edge.** A9-A16 and F3/F4/F7/F8 are absolute from it, so if the stock comes back over-long, trim it to 1210.73 before clamping or add the excess to every right-hand X.

**7.2** — **The same 8-bolt corner-bore pattern as every other beam joint.** 16 bolts, 8 per beam. **Lay it out by scribing:** two lines at the column positions, four stations ticked along each. **A scribed line beats working off an extruded bore**, whose own position error would come along with it — and these holes are ø9 on an M8 in any case, about a millimetre of float, which this joint wants because it works by friction rather than bearing.

**7.3** — **Y 30, the same number the side plates and the front fin carry.** One bolt line across every plate that lands on the box, and from the installed bottom edge it reads as itself with no arithmetic. It took two reframings to get here: it was a round **270** measured from the installed top, which put the row 34.8 up and 4.8 off every other plate while a note called the difference *deliberate* — **it was not** — then 271.625 once the plate height was corrected, and now simply 30. **The pitch no longer differs**: 150 here, and the side plates run 150 from 50 as well. Eight at 150 span 1050, and from **X 75** they run to **1125** — 75 clear at the left edge, 85.47 at the right on the 1210.47 plate. The fractions cost nothing — see 7.8, these eight are a drill guide with no mating pattern to miss — so round them at the mill if it is easier.

**7.4** — **BF12 face-mounts on 4 × M5 into the FIN**, Sheets 1a and 1b — not into this plate. Face-mounted takes 4; top-mounted takes 2. Any BF12 hole count in this repo has to name its orientation or it means nothing.

**7.5** — **[WARN] This gates the plate more than any hole on it.** Bed size is not travel: the question is whether the two 8-bolt patterns' relative HEIGHT survives a reposition across 1210.73 mm. The budget is well inside 1 mm - the float the 9 mm holes give - and past it the plate wins and a beam end has to be jacked.

**7.6** — **One reference edge across every plate, and it is the bottom one.** The bottom edge bears on the box's top skin, so it is the edge that locates the part. Sheet 9 has been dimensioned from it since the side plate's T-slot rows were corrected, and this sheet now matches. **It costs nothing to do so**, which is worth stating because the sheet was drawn upside down until 2026-10-07 on the belief that it did. [RED] **The beam bores are located by the FIN, not by this plate.** Y_BEAM_UNDERSIDE is 182 above the box skin because the fin's window puts the beam there — the fin is the riser that actually carries it, settled 2026-10-03 after the side plate was ruled out as the reference. So every plate standing on that skin sees the beam's corner bores at the same four heights, **197 / 227 / 257 / 287**, whatever height that plate happened to be bought at. Sheets 1a and 1b carry exactly those numbers for the fin, and Sheet 1 did before them. [WARN] **The old inverted frame was 2.8 mm out and nobody had caught it.** It listed the A-holes at Y 15 / 45 / 75 / 105 from the installed top edge and called the beam's corner Y 0, which only holds if the beam's top face is flush with the plate's top edge. On a 304.8 plate it stood *2.8 proud* of the beam top, so those bores were a plate-height error of the same size and from the same 2026-10-03 correction that left Sheet 9's lines behind. Re-referencing to the bottom edge removes the error rather than rescaling it. **The four Y values live in the registry** as RP_BEAM_ROW_1 to RP_BEAM_ROW_4, on the same expression as SIDE_TSLOT_ROW_1, so the two plates cannot drift apart. **In X nothing changed**: the bores still carry the 3.175 offset of the side plate the rear plate runs flush with (7.1), and Y2's are the same pattern mirrored off X 1210.73.

**7.7** — **The BF12 rows carry the interposer, and the full thickness applies.** The screw's near end is carried by the cast stepper frame, which sits *on* the 10 mm interposer and is therefore LOWER than bare metal. BF12 at the far end has to drop by the same amount or the screw is not parallel to its own beam. This sheet is clamped inverted, so lower is a **larger** Y. **It is the full 10, not 5.** The registry's NUT_FACE_BELOW_BEAM does subtract a 5 mm standoff, but only because its base figure was *measured* on a machine that still had one. **The standoff no longer exists in the design**, so there is nothing here to take back off. [DONE] **T_INTERPOSER is a measured 10** — his micrometer, and a metric plate rather than the 3/8&quot; this chain once assumed. These two rows follow it automatically if it ever changes again.

**7.8** — **The plywood tongues are never drilled to a coordinate, and the drill guide is always the plate being secured.** Not a template, not a story stick, and not a set of numbers off these sheets: **the plate itself**. Assemble the machine, set it on the torsion box, and spot each tongue through the holes of the plate that bolts to it — **this rear plate drills the back tongue** (X1-X8), and **each outboard plate drills its own side tongue** (K1-K7 on Sheet 9). That holds for every tongue on the box without exception, which is why the rule also sits in the standing-rules box at the front of the pack rather than only here. So the eight X stations here only have to clear obstructions and spread the load — nothing downstream has to agree with them, because the mating holes do not exist until the steel is bolted up and sitting in place. That is why 150 is a decision rather than a measurement, and why a hole landing a millimetre off costs nothing. **A hole you transfer needs no coordinate and fits better than one you compute.**

**7.9** — **The tongue fastener, and it is the same stack at every tongue hole.** From the plate side: an **M8 flange bolt**, then the **plate**, then the **19 mm baltic birch tongue**, then an **M8 fender washer**, then an **M8 acorn nut**. The ø9 holes in plate and tongue both are clearance, so this is a clamped joint, not a bearing one, and the two washer faces do the work: the **bolt's own flange** bears on the steel, and the **fender washer** spreads the clamp over enough plywood face that the nut cannot pull into it.



**Head inside, acorn nut outside**, and that is the way round to assemble it: the nut sits out in the open where a wrench reaches it easily, and the bolt is driven from inside. The acorn nut is for **appearance** on the face of the machine you see.



**LENGTH IS PER PLATE, BECAUSE A CLOSED NUT CUTS BOTH WAYS.** A flange bolt's length is measured **under the flange**, and an acorn nut is capped — too short and the thread does not reach, **too long and the bolt bottoms out in the dome and never clamps.**

**7.10** — **The window is a T, and the notch does two jobs.** The full-width opening is **{{WINDOW_W}} × {{WINDOW_H_CUT}}** as cut, its top edge **{{WINDOW_TOP_OVER}} above the beam's underside at Y {{WINDOW_TOP_Y}}** so that no steel can stand below the beam's bottom face, and a **{{PROBE_NOTCH_W}}** wide notch centred on it carries on **{{PROBE_NOTCH_H}}** further, to {{PROBE_NOTCH_BOTTOM_Y}}. That is **{{WINDOW_CLEAR_TOTAL}} below the beam face in all**.

**It clears the back of the proximity probe body**, which is narrower than the casting the opening above it is cut for — so the plate keeps its full width either side of the probe rather than losing it across the whole window.

[DONE] **And it is how the casting and interposer go in.** They are fitted from **behind the machine**, slid through the window **BK12 end first**, which this depth is what makes possible — there is no need to get at them from the front or to part the beam.

[RED] **R{{PROBE_NOTCH_R}} at all four of the notch's corners**, the two where it meets the window's bottom edge as well as the two at its own bottom. **The bottom pair is the one that matters:** there the metal wraps around the end of the notch, and this plate is the rear shear panel — that is where a crack would start. The pair at the mouth is a protruding corner of metal rather than a notch tip, so rounding it is tidiness. It is smaller than the window's own {{WINDOW_CORNER_R}} on purpose — a {{WINDOW_CORNER_R}} in a {{PROBE_NOTCH_W}} wide notch leaves 5 of flat across its bottom where this leaves 13.

**8.1** — **One part made three times, and it is 4 mm not 1/4".** The Y front strip came down to 1/4", breaking the old "same as its back plate" rule, and that is what made all three beams identical. [RED] **It came down again to 4 mm, because 1/4" does not fit**: the bolt heads reach past the strip's edge and have to pass under the bearing block, which leaves at most 6 mm. At 4 mm the stack is 5 and clears; at 1/4" it is 7.35 and hits, both measured on a real beam. The stiffness gain quoted in gantry-beam-joint.md is the 1/4" figure and no longer applies. It is also the magnetic encoder tape surface, so its face finish matters more than its edges do.

**8.2** — **[RED] The strip is now WIDER than the gap it used to fit, and runs under the blocks.** It was 45, chosen as BLOCK_ROW_GAP so it sat *between* the bearing block rows with about half a millimetre either side — 46 is the geometric gap, the 90 rail pitch less a 44 block, and 45 was the conservative measured figure. At 50.8 it overlaps each block by **2.4 and passes beneath it**, which a thin strip may do: he proved it with 60 × 60 × 4 test pieces, which overlap 7.0 a side at a *thicker* stack and clear. **The gain is Y tolerance.** At 45 the strip had essentially nowhere to go sideways; at 50.8 the next thing in its way is the **rail, 9.6 from the strip edge**. [WARN] **Which is why the rows must be dimensioned from the centreline.** The two rows sit ±15 from the seam because the T-slots put them there — that separation is 30 whatever the strip's width — so centre-referenced holes absorb a 50-versus-50.8 stock variation and edge-referenced ones do not. **The encoder lane is unaffected by any of this**: it is the row separation less the head, 30 &minus; 13.8 = 16.2, and the strip's width is not in that sum.

**8.4** — **[RED] The six bolt-on plates are on the trip, and the reason that kept them off was not wrong.** Sheets 8, 9 and 10 were home drill-press work because every hole on them is a ø9 clearance into a T-slot and **the T-nut slides to meet the bolt**, so an individual hole’s position hardly matters. That is still true. **His call 2026-10-09 overrules it on a different argument:** 14 holes on a front strip and 28 on a back plate, across six plates, is 126 holes of hand layout, and small errors creep in. A plate whose rows have wandered still bolts up — and fights for an afternoon while it does, because every bolt needs its nut nudged to a different place. **On Sheets 9 and 10 that is the whole of it: perfect holes are not needed for the joint, they are wanted for the assembly.**

REJECTED: **A clash argument stood here and the 2" strip removed it.** While the strip was 45 wide it sat in the block gap with nothing either side, so a row wandering in Y drove it into a bearing block — the nut slides *along* its slot, forgiving X and forgiving nothing in Y, so a hole off in Y moves the strip rather than being taken up. All of that is still true except the part that mattered: at 50.8 the strip runs *under* the blocks and the next obstruction is the rail, **9.6 away**. **So Sheet 8 is on the trip for the same reason as the rest — 14 holes a strip, three strips, and they want to be straight.**

OPEN: **It puts six more metre-long parts on a trip whose X traverse is still an open question** — the same one gating the 1210.47 rear plate, "can the mill traverse ~1212 in X". **If something has to be repositioned mid-job for want of travel, take it out of Sheets 9 and 10**, where the T-nut genuinely does forgive a shifted station. **Not Sheet 8, and not the rear plate** — the strips because Y is a clearance, the rear plate because its two patterns must meet extruded bores a metre apart.

**8.5** — **[DONE] The stock measured 3, and the bolt is what that decides.** Ordered as 1/8" 6061 flat bar and this sheet warned it might come 3.175 or 4.0; it came **metric at 3**. [DONE] **Block clearance is the best of the three cases** — the strip plus a flange rim is 4.0 against the 6 mm under a block. [RED] **THE M8 × 10 IS TOO SHORT, NOT TOO LONG — AND THIS SHEET HAD THE SUM BACKWARDS.** It said the bolt must not reach more than 7.2 past the plate. That 7.2 is measured from the **T-nut's front face**, and the bolt does not start there: from the plate's back face it crosses **2.3 of lip** first, then meets **6 of thread**, and the **slot floor is 9.3** past the plate. So a bolt wants to reach **between 8.3 and 9.3** past the plate — full thread, still clear of the floor. The M8 × 10 in this 3 strip reaches 7.0: it engages **4.7 of the 6** and sits **2.3 clear of the floor**. Nothing bottoms and nothing projects. **An M8 × 12 reaches 9.0 — the full 6 of thread, 0.3 clear of the floor**, and the head is unchanged so nothing about block clearance moves. **A washer here must be A4 / 316**, for the same reason these bolts are: the magnetic tape runs between their rows.

**8.3** — **[DONE] First hole at 50, then 150 pitch, on all three bolt-on plates.** That is **seven per row**, 50 to 950, with 50 clear at each end. The pitch had been in gantry-beam-joint.md for weeks — M8 T-nuts at 150, four rows on the back and two on the front — but where along the 1000 the first one sat had never been written anywhere, which is why these rows were amber rather than wrong. Eight at 150 would have spanned 1050 and not fitted at all. Nothing was ever blocked by it: these are ø9 clearance holes into T-slots and the T-nut slides to meet the bolt.

**9.1** — **This plate replaced two parts.** It is the full-height outboard plate and the Y back joining plate at once, grown rather than bolted alongside, which is why it carries the beam's four T-slot rows. That is also why the Y beams have no Sheet 10 part and the X beam does.

**9.2** — **10 gauge, and this plate's thickness has now been wrong twice in prose.** outboard-plate.md's cross-section said 6.35 mm (1/4") in three places, left behind when the plate went to 1/8" steel; the 1/8" was then itself a nominal, with the listing also offering 11 gauge (3.04) and a 3.36 floated and withdrawn as a guess. [DONE] **The order ends it**: 10 GA (.135) cold-rolled, which is 3.429. None of the three earlier numbers was right, and the question was closed by buying the part rather than by reading the listing again. **It does not drop into a channel** — that question is dead, not open: the plate stands flat on the box's top skin and the 60 mm proud outer lamination, the **tongue**, laps it from outboard on a plain bolted lap. The channel had been dimensioned around 6.35 and there is nothing left to size. The delivered thickness still matters, but for the riser-proud check, not for a groove.

**9.3** — **[DONE] The reference edge is the BOTTOM one, and that is what closed this sheet.** The four T-slot rows were first drawn as 15 / 45 / 75 / 105 from the top edge, which is the extrusion's own slot grid measured down from the beam's top face. That was only right if the plate's top edge finished *flush* with that face — and 304.8 is a **bought 12" size**, not a derived one, so there was nothing guaranteeing it. Dimensioned from the bottom instead the rows become **197 / 227 / 257 / 287**, the same four holes, but now **a plate that comes out short loses material at the top and nothing moves**. [RED] **199.8 / 229.8 / 259.8 / 289.8 is the wrong set — 2.8 too high** — computed as if the plate's 304.8 finished flush with the beam top, which is the very assumption dimensioning off the bottom exists to avoid. The beam's height comes from the FIN: the window's top edge is the beam's underside at 182, and 182 + 120 puts the beam's top face at **302**. [WARN] **The fin itself is 301.625, not 302** — it is the same ordered 11 7/8" as this plate — so the beam top stands **0.375 proud** of every one of these plates. That is SIDE_PLATE_PROUD, and it is harmless for exactly the reason this footnote exists: nothing is measured from a top edge. The bottom edge earns the job because it is the one that bears, on the box's top skin. Sheet 10 never had this problem: at 120 tall its top edge IS the beam top by construction.

**9.5** — **The plate is shorter than the beam, and which end gets the slack is a layout choice.** Ordered 39 5/16" = 998.54 against a 1000 beam. The seven T-slot stations are absolute from the plate's left edge and run 50 to 950, leaving 48.54 past the last hole, so 1.46 of it simply disappears from that margin. **Lay out from the left edge and the shortfall all lands at the right.** Sheet 10 is the same length and the same argument. [WARN] This is the benign version of the problem the back plate has: there, the stations also run from the left edge, but the plate's length sets where the *second beam* goes, so a shortfall is not margin — it is error. See checklist row 3.

**9.4** — **The 9 mm hole is the slot.** An earlier draft wanted the holes slotted progressively toward the ends for thermal differential. Unnecessary: ø9 on M8 is 1 mm of float per hole, several times the whole differential across a metre of plywood in a climate-controlled shop, and the Y risers were reamed to 9 for the same reason. **Do not transfer that conclusion to the T-nut rows** — those are a preloaded friction joint whose whole job is shear transfer, and they are a different argument.

**10.1** — **X only, and that asymmetry is deliberate.** The Y beams do not move and bolt to the torsion box, so their outboard plate reaches all the way down and does this job on the way past. The X beam moves and has nothing to bolt down to, so it keeps a plain 120 back plate and nothing more.

**10.2** — **Same X stations as Sheets 8 and 9** — 50 then 150, seven per row. See 8.3.

**3.8** — **The X ball nut had nothing to attach to, and this column is it.** The X screw runs on TOP of the beam, so the nut is above the carriage and the drive has to reach up and over. The **doubler of Sheet 2d** — the same block the Y ends use, now made three times — bolts to this plate's rear face with its bottom edge at **161** and its top edge at **206**, which is the nut's mounting face: 151 to the beam top, 10 for the interposer, 25 for the casting's axis, 20 for the nut's own h off the DSG1605 page. The column lands at **186** because it sits 25 up the block, the same DOUBLER_BOLT_X the Y side uses. **Sheet 11** is the plate that lies across the top. [WARN] **This plate already exists, dyed and undrilled**, and nothing in its schedule put a doubler on it before 2026-10-09 — these four are genuinely new, not a correction.


## Sheet 11

**11.1** — **One part, three copies, and the X one is simply inverted.** On Y the ball nut hangs under the beam, its mounting face points DOWN, and the sole plate bolts UP into it off a doubler on the X end plate. On X the screw sits on TOP of the beam and everything turns over: the face points up and the plate lies on it. **The doubler is the same block and the plate is the same plate.** Each bolts into the doubler's end face alone, and in both cases the plate carrying the doubler runs {{XEP_SOLE_TAB}} past that face so the sole plate's base has something to butt.

**11.2** — **[DONE] Why the two ends land on identical numbers.** Both plates are measured from the face the doubler bolts to, and **neither carries the thickness of the plate behind it**. SCREW_AXIS_X is {{SCREW_AXIS_X}} on Y because it measures from the end plate's INNER face; take that plate's {{T_X_ENDPLATE}} off and it is {{X_SCREW_AXIS}}, which is what X_SCREW_AXIS already reads from the carriage plate's REAR face. **Rail stack + half beam, on both axes.** So T_X_CARRIAGE_PLATE — still a nominal 12.7 flagged to caliper — cannot move a number on either sheet, and SOLE_SAME_AS_X_CHECK holds the two chains to one answer.
**It closes on the nut rather than on a chosen length:** the length is {{SOLE_BRACKET_L}}, the far nut row is at {{NUT_BOLT_X_FAR}}, and the difference is {{NUT_INSET_X}} — NUT_INSET_X — so the tip finishes flush with the nut face's edge.

**10.3** — **Ordered 4 11/16" × 39 5/16", and the sheet draws 120 × 1000.** The 120 was never arbitrary: it is the stacked pair's full section height, so the plate reaches all four back slots. The sheared piece is 119.06, **0.94 short**. [DONE] **It costs nothing, and the reason is the reference edge.** This sheet measures Y *down from the top edge*, which is the beam's top face, so the four rows at 15 / 45 / 75 / 105 are fixed against the beam and the shortfall falls off the bottom — 14.06 below the last row where 15 was intended, against a ø9 clearance hole. [RED] **Do not re-reference this sheet to its bottom edge.** Sheets 1a, 1b, 7 and 9 all measure from their bottom edges because those edges *bear on the torsion box*; this plate bolts to a moving beam and its bottom edge bears on nothing. The two conventions are each right for their own part, and footnote 9.3 is the argument for the other one. The 1.46 of length is the same slack as Sheet 9 — see 9.5.


## The front matter it used to open with

Plates for the one machining visit. Generated from **machine/*.md**, which remain the source of
truth — **revision 2026-10-04**. If a sheet here and a .md file disagree, the .md file
wins and the sheet is the stale one.

Status — what is missing and what is in progress

The pack reflects the Y end rework: cast stepper frames replaced BK12 and the M5
standoffs, the Y steppers moved to the **front**, each Y beam end carries a **tapered front fin**,
and one **full-width, full-height back plate** serves both beams. **Every sheet below has been
brought up to that design.**

**WCS ORIGIN — THE SAME ON EVERY SHEET, unless that sheet says otherwise.It is the FRONT-LEFT-TOP corner of the part as clamped.X** along the longest dimension, **Y** across it, **Z = 0 at the top face** and negative
into the material. All coordinates positive in X and Y, **absolute, never chained**.

Each sheet states only what X 0 and Y 0 mean *on that part*. **Three sheets override
this and say so in their own header:** Sheets 1a and 1b stand the plate **up**, so X runs
across the 200 and **Y up the 301.625**; Sheet 2d is clamped **the short way** on 2a's
origin. **Sheet 5 overrides it as well** — machine X runs the short way, over the
{{SOLE_BRACKET_L}} — but says so in its figcaption rather than its header.

**AN AMBER ROW IN ANY HOLE SCHEDULE IS A DIMENSION THAT DOES NOT EXIST ANYWHERE IN THE REPO.** It has not been invented here. **Do not drill an amber row** — measure or decide it first, and the pre-trip checklist says which.

**FLAG: AT THE MILL YOU DRILL. EVERY THREADED HOLE GOES THROUGH.** Nothing here is tapped on the
trip — each threaded feature is listed as its **tap drill, drilled through**, with the
thread it is for named alongside.



**OPEN: Sheet 2, H1 and H2: use M8 × 35. NOT M8 × 40** — a longer bolt breaks
through onto a bearing block seat.

**THE Y DRIVE IS AT THE REAR, and every sheet now shows it.**



The casting, interposer and motor are at the **back** of the machine; BF12 face-mounts into the
**front fins**. So the **window is in the rear plate** — Sheet 7, W1 and
W2, a **{{WINDOW_W}} × {{WINDOW_H_CUT}}** opening with a {{PROBE_NOTCH_W}} notch carrying on
below it, {{WINDOW_CLEAR_TOTAL}} in all — and BF12's four tapped M5 per beam are on the
**fins**, Sheets 1a and 1b, F1-F4 each. The fins are solid otherwise.



**Both ends are not alike on Sheet 7.** W1 runs out to the plate's left edge, because the
casting's outboard face and that edge are the same face — the Y1 extrusion's outboard face,
which is also X 0. W2 is a closed window with about 6 of plate past it.



**THE THREE NUT SOLE PLATES ARE ONE PART.** Y1, Y2 and the X carriage all take the same
**steel T**: a base **154 × {{SOLE_BASE_D}}** on the doubler's end face carrying the four
root bolts, then a **{{SOLE_STEM_W}}** wide stem out to the nut — the nut's own width,
leaving **8** to the M5 centres — with a **{{SOLE_FILLET_R}}** radius where the stem
meets the base. **Sheet 5 is the part; Sheet 11 says where the X one goes.Steel because the bracket is then its own ferrous target** for the Y limit sensor — and
because the tapered edge was the face that sensor had to read, which is a trip point that drifts
with standoff. All three brackets are 1/4", the same sheet as this plate.



Every other sheet in this pack is unaffected.



**The window's HEIGHT is not settled either** — the limit sensor mounts on the casting's
top face and stands LIMIT_SENSOR_STACK_H above it, and whether the window has to clear it waits on
a bench test. The sensor stack is 55 deep against CASTING_INBOARD_RUN's 50.5.

**Sheets that exist and are drawable** — each still subject to
its own amber rows:

**Every sheet number above is a link** to its own sheet. The sheet count in the page furniture is the cross-check:
if the printed pack has sheets this table does not name, this table is the stale one.

**Only the right-hand X end plate carries the BF12
tongue**, so the two are not interchangeable at assembly.

**In progress — a 1/2" baltic birch mockup**, being cut while
the mill visit is a couple of weeks out. Sheet 1 first: it settles the window's height (the
50 mm is a budget, and the casting projects only about 20 mm below the bar) and the spindle
clearance that gates the taper cut. **Plywood is for fit, never for transfer** — its
thickness runs under 12 mm and M5 inserts need a far bigger bore than a 4.2 mm tap drill,
so insert positions are representative, not a clearance test.

**Two questions still gate drilling**, and each needs a part or the
mill in front of you:

- How far past the front riser plane the spindle reaches, and whether it fouls the widened fin at
low Z — gates Sheet 1's taper, which is one bandsaw pass and cannot be put back

- The mill's model, and whether its DRO is 2-axis or 3-axis

**Derived, never authoritative.** The source of truth is **machine/*.md** — start at
**machine/README.md**. If a sheet here and a .md file disagree, **the .md file wins**.

- **One WCS origin per plate, never chain dimensions.** Each drawing names its origin corner; every hole
is an absolute X/Y from it. On a manual mill with a DRO the operator types absolute coordinates, and
chained dimensions accumulate error.

- **Lay the extrusion bolt patterns out by scribing.** Two lines, four stations ticked along
each — that is the eight-hole pattern at a beam end.

- **M5 clearance is ø6 throughout.** One size, every sheet, whether the joint wants float or not — it is one drill on the trip instead of three, and no hole in this pack is positioned by being a tight fit on its bolt. The counterbored M5 on Sheet 4 still get there the long way, 5.2 for the pilot and opened to 6 after, which is the same finished hole.

- **9 mm clearance on M8 wherever a plate meets extrusion.** That is the repo's deliberate
figure — the joint works by friction, not bearing, and the float is wanted.

- **Every hole in a schedule is tagged on the drawing, and the numbering runs ACROSS X,
THEN UP IN Y.** One rule for the whole pack: finish a row left to right before starting the
row above it. So on a four-by-four pattern, **1 to 4 is the whole bottom row** across every
block it passes through — not the first block's four. A single column numbers upward; a
single row numbers left to right. **Run tools/check-shop-pack-refs.py** — it fails if
any schedule Ref has no matching tag on its own sheet.

- **The plate is the drill guide for its own plywood tongue.** No tongue on the torsion box is
ever drilled to a coordinate. Bolt the machine up, set it on the box, and **spot every tongue hole
through the plate that secures it** — the rear plate drills the back tongue, each outboard
plate drills its own side tongue. Nothing downstream has to agree with the coordinates on these
sheets, because the mating hole does not exist until the steel is in place.

- **One fastener through every plywood tongue**, the same stack everywhere: an **M8 flange
bolt**, head on the plate — **through the plate**, **through the 19 mm baltic birch
tongue**, **through an M8 fender washer**, into an **M8 acorn nut**. **Head inside, nut
outside**, so one wrench sits on the nut out in the open while the bolt is driven from inside.
**M8 × 35 at the rear plate, M8 × 30 at the outboard plates** — the two plates
are not the same thickness.

### What is on the trip


## Fragments the sheets no longer carry

Where each sat, and what it said.

- **Sheet 1a stock** — Both real stock corners.
- **Sheet 1a stock** — That edge bears on the torsion box's top skin, which is why every plate standing on that skin is dimensioned from it - and it is why B1-B8 read the same 197 / 227 / 257 / 287 as Sheet 7's beam bores and Sheet 9's T-slot rows.1.6
- **Sheet 1a figcaption** — Every feature is dimensioned off the bottom-left corner, and every feature goes through - which is why Sheet 1a and Sheet 1b are the same part, drilled from one pattern and simply turned over to hand them. As drawn is the view from the FRONT of the machine.1.7
- **Sheet 1a prose** — ⚠ Do not cut the taper line yet - the spindle clearance is unsettled and the cut is one bandsaw pass that cannot be put back.1.5
- **Sheet 1b stock** — Both real stock corners.
- **Sheet 1b stock** — That edge bears on the torsion box's top skin, which is why every plate standing on that skin is dimensioned from it - and it is why B1-B8 read the same 197 / 227 / 257 / 287 as Sheet 7's beam bores and Sheet 9's T-slot rows.1.6
- **Sheet 1b figcaption** — Every feature is dimensioned off the bottom-left corner, and every feature goes through - which is why Sheet 1a and Sheet 1b are the same part, drilled from one pattern and simply turned over to hand them. As drawn is the view from the REAR of the machine.1.7
- **Sheet 1b prose** — ⚠ Do not cut the taper line yet - the spindle clearance is unsettled and the cut is one bandsaw pass that cannot be put back.1.5
- **Sheet 2a figcaption** — Dashed = not this plate, or on its far face. Outer face, seen from outboard. The drawing's horizontal is machine X - the plate's 245 from its bottom end, left to right. The vertical is Y across the 154, Y 0 at the back edge, running up the page. The beam's back face is flush with the plate's back edge.2.14
- **Sheet 2b figcaption** — Dashed = not this plate, or on its far face. Outer face, seen from outboard. The drawing's horizontal is machine X - the plate's 300 from its bottom end, left to right. The vertical is Y across the 154, Y 0 at the back edge, running up the page. The whole plate is drawn, tongue included, so this sheet can be cut and drilled without a second one beside it. The beam's back face is flush with the plate's back edge.2.14
- **Sheet 2c stock** — 🔴 All four holes are o8.4, the close fit - NOT the o9 used everywhere else on M8. This is the one part on the trip where the float is not wanted.2.13
- **Sheet 2d stock** — 🔴 THREE OF THEM, AND THE THIRD IS NOT LIKE THE OTHER TWO. The block is identical; where it goes is not.
- **Sheet 2d stock** — Two for the Y ends. Cut from the 45 mm offcut left when an end plate is taken out of a 200 mm wide piece. Each bolts to the end plate's OUTER face at the bottom, the same face the bearing blocks are on, with its end face level with the ball nut's mounting face. That end face is the whole seating - {{SOLE_BASE_D}} - and the sole plate of Sheet 5 lies across it and bolts into its edge.
- **Sheet 2d stock** — One for the X axis. It comes out of the {{XEP_WASTE_L}} * {{XEP_STOCK_W}} left past the LEFT plate's end - that plate is cut to {{XEP_CUT}} of the 300, so the remainder takes this block turned 90deg, its 154 across the width. All three come off the two end plate pieces and nothing is bought for them. It bolts to the X carriage plate's REAR face, the other way up, with its bottom edge at 161 and its tapped end face at the TOP, carrying the X ball nut through the same sole plate. All three joints are now the same joint, the Y pair being the X one inverted.11.1
- **Sheet 2d stock** — X runs along this block's 45 from its tapped end face, and Y along its 154 from the same back edge 2a uses. Every Y below is the number 2a carries; every X is {{DOUBLER_BOTTOM_X}} less, because the end plate reaches that far past this block's end face to back the sole plate. The two parts are machined separately and it is the shared Y origin plus that one known offset that makes them agree.2.6
- **Sheet 2d stock** — The height has an upper bound, and 45 is inside it. The doubler shares this face with the lower Y bearing block row, and the gap to that row's bottom edge is {{DOUBLER_BLOCK_CLEAR}}. Nothing bears across it. A 60 would overlap.
- **Sheet 2d stock** — 🔴 D1-D4 are NOT centred in the 45, and must not be re-centred. They stay at X 25, which leaves 20 above and 25 below. R1-R4 depend on it: they bore in from the end face on these same four Y stations, straight at these bolts, and stop with {{SOLE_ROOT_WALL}} of aluminium left. Centre the column and that margin shrinks.2.7
- **Sheet 2d figcaption** — D1-D4 at Y 32, 62, 92, 122 are the same four values the end plate carries in its own schedule, and R1-R4 into the end face sit on the same four again, so one spread serves every row across 2a, 2d and Sheet 5. Nothing is clamped together at the mill - the parts are machined separately and it is the shared WCS that makes them agree, which is why the block is clamped the short way on 2a’s origin rather than on its own long edge. Held that way, every number above is a number already on Sheet 2a. The grey projection lines carry the stations across to the end-face view: if a hole in one view does not land on its partner in the other, the error is in this drawing and not in the schedule.
- **Sheet 2d box** — Three parts whose holes must agree across an assembly - end plate (2a), this doubler (2d) and the sole plate (Sheet 5). They are machined separately, and the shared Y origin is what makes them agree - nothing is clamped together at the mill. On X the doubler and the plate differ by {{DOUBLER_BOTTOM_X}}, the strip the plate reaches past it.2.7
- **Sheet 3a stock** — The plate already exists, sprayed with layout dye.
- **Sheet 3a stock** — The bottom ~150 is over the X gantry; the rest stands above it.3.6
- **Sheet 3a stock** — Fully dimensioned - 45 features. The top stop is now a bolt-on block, Sheet 3c, and the two holes it needs are in the schedule below.3.3
- **Sheet 3a figcaption** — Every hole carries its schedule ref, and the numbering runs across X, then up in Y: R1-R7 is the whole lower rail before R8 starts the upper one, and X1-X4 is the whole Y 20 row across both bearing blocks.
- **Sheet 3b stock** — It sits between the Z bearing blocks and the Z plate, one per rail, each spanning that rail's pair of blocks.
- **Sheet 3b stock** — ⚠ 5/8" is a nominal and this bar has been wrong twice before - 15.875 as a fraction, 16.41 on calipers, 16.22 on a micrometer. Mic the new bar on arrival and write the number down before the Z plate is counterbored.3b.1
- **Sheet 3b stock** — 🔴 Face 1 mm off both bars in ONE setup. That is the only operation that makes the pair coplanar, and it is the reason the cut exists.3b.2
- **Sheet 3b figcaption** — The four o6 holes carry the M5 that bolt the Z plate through this bar into the bearing blocks - they are clearance at both ends, with the counterbore in the Z plate and the thread in the block. The fifth hole is driver access and meets nothing.
- **Sheet 3b box** — ⚠ Three numbers on this sheet are open. The bar's thickness is a nominal until the new stock is miked. BF12's width has not been caliper'd, and it is what the 50 mm width has to clear - about 1.9 mm each side by the current reckoning. And the X positions carry half millimetres, because a 160 bar puts the symmetric hole pattern on .5; a 161 bar would read 19, 55, 106 and 142.
- **Sheet 3c stock** — What it does. It bolts to the front face of the X carriage plate and the Z ball nut lands on its lower face. The Z screw runs on past it through the o22 bore, so the block stops the nut and nothing else.3c.1
- **Sheet 3c stock** — SB1, the o22 bore, runs up the block through the 25.4. TS1 and TS2 run in toward the plate through the 45. They are at right angles to each other, so the block gets turned once.3c.3
- **Sheet 3c stock** — Installed: 50 across the carriage, centred on the screw at Y 77 - 25.4 up the carriage, stop face at X 310 - 45 standing out from the plate face. It bolts to TS1 and TS2 on Sheet 3a.3c.2
- **Sheet 3c figcaption** — View A is the one to read before drilling - it is the only place the o22 bore and the two M5 runs appear together, and the whole reason the bore is 22 rather than 27.3c.3
- **Sheet 3c prose** — Setup 1 - the 50 * 45 face up. One hole, down through the 25.4.
- **Sheet 3c prose** — Setup 2 - the 50 * 25.4 outer face up. Two holes, in toward the plate through the 45.
- **Sheet 3c prose** — The fastener: M5 * 50, counterbored, two of them - through the 45 of block and about 11 into the carriage plate, which TS1 and TS2 on Sheet 3a are drilled and tapped for.3c.3
- **Sheet 4 stock** — 🔴 All twenty-eight holes are whole millimetres. That holds only at 164 wide with the Z rails on a 114 pitch - see Sheet 3a, R1 at Y 20 and R2 at Y 134.4.1
- **Sheet 4 stock** — 🔴 Twenty counterbores, TWO depths. C1-C16 and N1-N4 share the 5.2 pilot and the o8.9 bore, but the web differs - 4 mm on the C holes, 6 mm on the N holes. The 4 is forced only where the bolt also has to cross the spacer.4.5
- **Sheet 4 figcaption** — The dashed outlines are what sits behind or in front - the two spindle clamps on the front face, the ball nut's mounting face and the two bearing-block pairs on the back.
- **Sheet 4 box** — Every hole on this plate is a whole millimetre - all twenty-eight. It holds because the Z rails are on a 114 pitch (Sheet 3a, Y 20 and 134), which puts the block bolt columns on +-73 and +-41 rather than +-73.5 and +-41.5. On an odd plate width the nut and clamp holes land on half millimetres instead, so the 164 and the 114 go together. ⚠ Two things on this sheet are still open, and both are thicknesses. The plate's is a nominal 12.7 while the half-inch stock elsewhere on this machine came in at 12.19 - it sets the counterbore depth through the 4 mm web. The new spacer bar's is unmeasured, and it sets how much of the M5 reaches the bearing block. Neither moves a hole on this sheet.4.7
- **Sheet 4 prose** — Clamp footprint 122 * 55, centred on X 29.5 and X 145.5, with the 100 * 25 bolt pattern centred in each - which leaves 2 mm of relief at each end of the plate. 116 and never 1444.3, and the clamps are deliberately NOT moved to buy hole clearance.4.9
- **Sheet 5 prose** — One part, three copies - Y1, Y2 and the X carriage - it carries the ball nut into the end of a doubler, and the same joint serves all three - the X one is installed inverted, Sheet 11
- **Sheet 5 box** — Why these exist, and why there is only one of them. A doubler bolts to the face of a plate with its end face level with the ball nut's mounting face; this plate lies across that end face, bolts into its edge, and reaches out to the nut. The plate it is bolted beside carries on {{XEP_SOLE_TAB}} past the doubler, and the base butts that strip - which is what locates it, so no bolts go into the plate itself. On Y the nut hangs under the beam, its mounting face pointing DOWN, so the joint is upside down and the bolts go up into the nut. On X the screw sits on top of the beam and it is the right way up. Nothing else differs, which is why the three are one drawing. The Y screw axis is {{SCREW_AXIS_X}} mm from the end plate's inner face - {{T_X_ENDPLATE}} plate + 30 rail stack + 30 half beam - so the nut's flange never comes near the plate and this is a cantilever, not a strip. That leaves {{NUT_AIR_CLEAR}} of clear air between the doubler's outer face and the nut's side, against a {{NUT_AIR_MIN}} mm minimum measured off the built Y beam.
- **Sheet 5 figcaption** — That strip is what squares it - there is no second row to pull it true, and none needed.Plan view, WCS 0,0 on the root's left corner - a real stock corner. Machine X runs up the page from the root to the tip, machine Y across the 154. The bolt row sits at {{ROOT_BOLT_X_DOUBLER}}, centred in the doubler's {{T_DOUBLER}}, and on Y 32, 62, 92, 122 - D1-D4's stations, so one spread serves both rows. Neither number is a free choice. The stem is centred on the plate's fore-aft mid (Y 77), a free choice made for symmetry - thrust runs along Y, so an offset in Y produces no moment. The four red holes are the nut's M5 clearance holes.
- **Sheet 5 box** — Three parts whose holes must agree across an assembly. The end plate, the doubler and this bracket are each machined on their own, held on a common WCS - that shared origin is what makes them agree, not clamping them together. Take the ball nut housing itself to the mill - the N1-N4 pattern gets checked against the real flange before anything is cut.
- **Sheet 5 box** — ⚠ The tip is the nut's own width. The 98.19 is derived. The tip and the stem are {{SOLE_STEM_W}}, which is {{NUT_FACE_Y}} - the nut's mounting face. Nothing else is on that end, so the plate is as wide as the thing it bolts to, and the M5 at +-12 leaves 8 mm of edge, which is plenty in 1/4" steel. The 98.19 is derived - 72.19 screw axis + 26 for half the nut - and it includes the 24.38 seating, which is the two plate end faces the bracket covers rather than length added beyond them. ⚠ A 107.4 counts that seating twice and is wrong. The numbers that are not free are the four M5 at +-20 in X and +-12 in Y, and the root's 154.
- **Sheet 5 box** — ✅ The doubler is 45 tall. Its upper bound is the bottom edge of the lower Y bearing block row, which shares the same face in the same X band. With the block's measured 44 width that edge lands at X 55.5 - the lower rail at 77.5 less 22 - so 45 clears it by 10.5, where a 60 would overlap by 4.5. It is not gated on the Y beam underside - the doubler sits ~17 mm inboard of the beam's inside face.
- **Sheet 6 stock** — One drawing, quantity 3 - Y1, Y2 and the X stepper end are the same part.
- **Sheet 6 stock** — Y across the 60.6.1
- **Sheet 6 figcaption** — Nothing rests on anything. On X the same part sits on top of the beam instead.
- **Sheet 6 prose** — FLAG: X's bar inherits these rows from Y geometry. On X the bar sits on top of the beam and overhangs its end - check both rows land over beam before drilling.6.4
- **Sheet 7 stock** — One plate carries both Y beams and is also the rear shear panel.
- **Sheet 7 stock** — The bottom edge is the reference because it bears on the box's top skin - the same edge every other plate on this machine is dimensioned from.7.6
- **Sheet 7 stock** — 🔴 The beam bores do NOT depend on this plate's height. They sit 182 above the box's top skin because that is where the fin carries it, so A1-A16 read the same 197 / 227 / 257 / 287 that Sheets 1a and 1b carry for the fin.7.6
- **Sheet 7 stock** — W1 and W2 are beam-referenced, like everything else on this sheet. Their top edge is cut {{WINDOW_TOP_OVER}} above the beam's underside, at {{WINDOW_TOP_Y}} - the underside itself is {{Y_BEAM_UNDERSIDE}} above the box's top skin, and the overcut is there so that no steel can stand below the beam's bottom face. The opening runs {{WINDOW_H}} below that underside to {{WINDOW_BOTTOM_Y}}, and a {{PROBE_NOTCH_W}} wide notch centred on it carries on another {{PROBE_NOTCH_H}} to {{PROBE_NOTCH_BOTTOM_Y}} - {{WINDOW_CLEAR_TOTAL}} of clearance in all.7.10 Nothing about the delivered plate can move them. BF12 is not on this plate - it face-mounts into the front fins, Sheets 1a and 1b.7.47.7
- **Sheet 7 stock** — Everything at the Y1 end is measured straight off that face, which is why A1-A8 land on a round 15 and 45 and W1 starts on X 0. The Y2 end is 1204.38 away by the beam spacing, not by this plate's length, so measure the built spacing before drilling that end and treat the Y2 numbers below as provisional. The delivered plate runs about 6 past Y2's face, so there is material either way.7.1
- **Sheet 7 figcaption** — Both beams sit at the plate's top. At plate scale the two stations are a few millimetres wide, so the Y1 station is drawn again at 1.2* below; the Y2 station is its mirror about X 602.19, so every Y2 coordinate is 1204.38 &minus; X - the beam spacing, not this plate's length. The schedule carries all sixteen A-holes explicitly rather than making anyone do that subtraction at the mill.
- **Sheet 7 prose** — 🔴 Whether the Laguna can hold the height reference across 1210.47 mm is still open, and it gates this plate more than any hole on it.7.5
- **Sheet 8 stock** — ✅ THE THICKNESS IS SETTLED AT 3. Ordered as 1/8" and the sheet warned it might come 3.175 or 4.0; it came as neither. The M8 * 10 still stands, and this is the tightest of the three cases - it reaches 7.0 past the strip against a 7.2 limit, so 0.2 of slack, where 1/8" would have given 0.375 and 4 mm 1.2. A thinner strip lets the same bolt reach further into the slot, which is the opposite of the intuition.8.5
- **Sheet 8 stock** — ✅ THE WIDTH CAME IN AT 50, NOT 50.8 - AND THE PRECAUTION PAID. Because both rows are laid out from the strip's centreline rather than from an edge, the strip self-centres on the seam and the rows simply move in to 10 and 40 from an edge. Nothing had to be re-chosen, and the old contradiction on this sheet is gone with it - the schedule used to be headed for a 45 strip with rows at 7.5 and 37.5, which matched neither the stock line nor the drawing.s centred in that. Settle the width before drilling: on a 50.8 strip the schedule's own Y values put the rows 7.5 and 13.3 from the two edges rather than centred.
- **Sheet 8 stock** — One part made three times - X, Y1 and Y2 carry an identical strip. It ties the two stacked extrusions across the seam on the FRONT face, and it is also the magnetic encoder tape surface.8.1
- **Sheet 8 stock** — 14 holes per strip, three strips, and they want to be straight.8.4
- **Sheet 8 stock** — 🔴 DIMENSION BOTH ROWS FROM THE STRIP'S CENTRELINE, 30 APART - NOT FROM AN EDGE. The rows are +-15 from the beam's seam because that is where the T-slots are, and the stock came in at 50 rather than the 50.8 it was ordered as - which is exactly the case this rule was written for. Measured from the centre, a narrower strip still self-centres on the seam. Measured from an edge, the stock's width tolerance lands straight in the hole positions.8.2
- **Sheet 8 stock** — This strip runs UNDER the bearing blocks, not between them - 2.0 of overlap each side, and that is what buys the Y tolerance.8.2
- **Sheet 8 figcaption** — Both rows run the whole 1000, 30 apart, centred on the seam. The strip is wider than the gap between the bearing block rows and runs underneath them - 2.0 of overlap each side - which is what gives it room to sit off-centre without touching anything. The red line is the strip’s centreline and the seam at once; lay the two rows out from it, not from an edge.8.2
- **Sheet 9 stock** — Y beams only - one per beam, outboard. It is also the Y back joining plate, grown rather than added alongside, which is why it carries the beam's four T-slot rows as well as the bolt row into the torsion box.9.1
- **Sheet 9 stock** — 🔴 Y IS MEASURED FROM THE BOTTOM EDGE, not the top. The bottom edge is the reference because it bears on the box's top skin, so every row stays correct even if the plate comes out slightly short of the Y beam's top face.9.3
- **Sheet 9 stock** — 🔴 10 GAUGE AS ORDERED - 3.429, and it is neither the 1/4" an old cross-section table said nor the 1/8" that replaced it. The sheet bought is 10 GA (.135) cold-rolled. Caliper it on arrival: a gauge is a nominal.9.2
- **Sheet 9 stock** — ⚠ The plate is 998.54, not 1000 - 1.46 shorter than the beam. It costs nothing: the seven T-slot stations run 50 to 950, so the slack lands in the margin past the last hole. Lay out from the left edge and all of it falls at the right.9.5
- **Sheet 9 figcaption** — The four orange rows are the beam's own back slots, 197 to 287; the green row is the bolt line into the plywood tongue at 30, the same line the front fin and the rear plate use. Cut the plate a little short and nothing moves - it loses material at the top, where there is nothing.
- **Sheet 10 stock** — X gantry only. The Y beams do not need one - Sheet 9's full-height plate is their back joining plate. The X beam moves and has nothing to bolt down to, so it keeps the plain 120.10.1
- **Sheet 10 stock** — ⚠ 119.06 AS ORDERED, against the section's 120. The intent was the full section height - width beats thickness on the back face, and 120 is the widest the section offers - and the sheared piece is 0.94 shy of it. It costs nothing because this sheet is referenced to the TOP edge, which is the beam's top face: the four rows at 15 / 45 / 75 / 105 do not move and the shortfall lands at the bottom, 14.06 below the last row instead of 15. 🔴 Do not re-reference this sheet to its bottom edge to "fix" that - the top edge is the reference because it is the face that registers against the beam, and the bottom edge registers against nothing.10.3
- **Sheet 10 stock** — ⚠ 998.54 long, not 1000 - same shear length as the side plates, and harmless for the same reason.10.3
- **Sheet 10 figcaption** — The four rows are the extrusion's own back slots on a 30 grid, so this plate's Y needs no derivation at all. Sheet 9 reaches the same four slots from the other end, off its bottom edge, because its height is a bought 12" rather than the beam's own 120.
- **Sheet 11 - the sole plate on the X carriage - whole page, no holes on it** — The part is Sheet 5, and this is the third of its three copies - nothing here is a dimension to cut to Why it is on top. The X ball screw runs on TOP of the X beam, so the nut is above the carriage and something has to reach up and over to it. The doubler of Sheet 2d bolts to the back of the X carriage plate with its top edge level with the nut's mounting face; the sole plate lies across that top edge and bolts down into it, then down into the nut.11.1 🔴 The bolts go in from ABOVE, which is the whole reason the plate is on top - they stay reachable while the gantry is being assembled. THE Y PAIR IS THIS JOINT UPSIDE DOWN. There the nut hangs under the beam with its face pointing down, so the doubler's end face is at the bottom and the bolts go up. The part does not change, and neither does a single one of its coordinates.11.2 Where it goes WhatFigureWhy that Doubler's bottom edge on the carriage plate{{X_DOUBLER_BOTTOM}}Its top edge is the nut's mounting face; the block is {{DOUBLER_H}} tall Doubler's top edge - the sole plate lands here{{X_NUT_FACE_Z}}The nut's own mounting face, which sets everything above D column through the carriage plate{{X_DOUBLER_BOLT_XC}}{{DOUBLER_BOLT_X}} up the doubler, measured in the carriage plate's frame Gap to the bearing block row above{{X_DOUBLER_BLOCK_CLEAR}}Nothing bears across it - it must not go negative Screw axis out from the carriage plate's rear face{{X_SCREW_AXIS}}Rail stack + half the beam, and the plate's own thickness is not in it11.2 ✅ The holes are on Sheet 5 and there are none here. All three copies carry the same four root bolts at X {{ROOT_BOLT_X_DOUBLER}} and the same four nut bolts at X {{NUT_BOLT_X_NEAR}} and {{NUT_BOLT_X_FAR}}, on Y 32, 62, 92, 122 and Y 65, 89. Cut three, drill three the same, and install one here and one at each Y end.
