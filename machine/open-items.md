# Open items
> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

## The waterjet quote

- OPEN: **Which small holes the waterjet should pilot rather than cut to size** - waiting on the
  shop's own recommendation before anything goes in the DXFs. The guideline that raises it is
  theirs: minimum hole diameter roughly equal to material thickness, which the **8 × ø4.2** on the
  front fins (0.42 × the 10 mm) and nearly every hole on the **end plates** (only the ø35 bore beats
  their 12.19) fall under.
  **The scope is decided and the diameter is not: pilot the holes that get TAPPED plus the
  counterbored P row, and cut the clearance holes full size** - 40 holes across the two end plates
  and the fins. His call: float is wanted in the ø9 into extrusion bores and the ø5.2 block bolts,
  so jet taper costs nothing there, where a tapped or counterbored hole wants a clean wall.
  **A ø3 pilot opened out here was the working figure**; the shop may prefer a different size, a
  scribed mark, or to cut them as drawn. The intro page of the quote package asks them directly.
  ⚠ **A magdrill is not the tool for these** - every ø4.2 in the build is in 6061, so a magnetic
  base has nothing to grip unless the part is clamped on a steel plate.

## From the 2026-10-02 stepper frame rework - all unmeasured

- SETTLED: ~~**The as-built BK12 screw axis height**~~ **Closed 2026-10-02**, and reframed: the number
  that matters is the **10 mm** between the beam underside and the nut top, with the supports
  mounted 5 mm above the extrusion. The casting hangs below the beam, so that clearance grows.
- SETTLED: ~~**The casting's 6-hole pattern against the T-nut holes**~~ **Closed 2026-10-02.** Measured at
  columns 7 / 53 and rows 28 / 58 / 71. The columns clash with the T-slots at 8 mm, which is why
  the bar runs ~30 mm past the casting and the four T-nut bolts live in the overhang.
- SETTLED: ~~**The two strip widths either side of the window**~~ **Measured 2026-10-02 at 19 mm outboard
  on the MDF template; the design moved to 20 on 2026-10-03** when the window was realigned onto the
  beam face. The measurement confirmed the approach, not this number. The fins are **100 / 200 over 301.625**, and SETTLED: **each is now on its own piece of plate** -
  settled 2026-10-08. They used to nest out of one square with 2 mm for the kerf, which is the only
  reason the top width was ever 99.625 rather than 100; the base is the reference end at a fixed 200,
  so the top absorbed the remainder. On its own piece nothing couples the two widths.
- SETTLED: ~~**The window's horizontal position does not reconcile**~~ **Closed 2026-10-02, and the window
  was then realigned on 2026-10-03.** The original non-reconciliation was arithmetic off a wrong
  column position; with the M8 columns at **35 and 65** the beam spans X 20-80 and nothing about the
  casting or the bar had to move. **The window is now X 20 to 80.5** - its outboard edge aligned on
  the beam's outboard face rather than centred on the beam - which puts all the clearance over the
  60 mm casting inboard, where the taper has already provided room, and makes the window edge flush
  with the side plate's inner face.
- FLAG: ~~**The riser stands 1.8 mm proud of the side plate**~~ **WRONG, corrected 2026-10-02 to
  16.8 mm.** The 1.8 was computed off a superseded M8 column at **20**; the column is **35**, which
  this file had already corrected elsewhere while this bullet kept the old consequence. The chain:
  **35 − 15 = 20 mm of fin overhanging the Y beam's outboard face**, less the side plate's
  thickness. SETTLED: Thickness of the fin is not a term, so the 10 mm stock is irrelevant to it.
  FLAG: **The side tongue's termination gets more important, not less** - a tongue reaching the
  riser's station would be held out by **16.571 mm**, not 1.8, so terminating it short is now clearly
  required rather than merely tidy. SETTLED: **16.571, not the 16.8 this bullet carried**: the side plate
  was bought at 10 gauge (3.429) rather than the nominal 1/8" (3.175) the figure was computed on.
- OPEN: **Terminate the side tongue short of the front riser's station** so the tongue bears on the
  side plate rather than being held out by the riser. A box decision, free while the box is unbuilt.
- SETTLED: ~~**T2's edge distance, on the template**~~ **Closed 2026-10-02.** X 25 and 170 on the Y 30
  line both check out against the physical template - photo committed. **The front fin's geometry
  is fully settled.**
- FLAG: **Whether the Laguna can hold the HEIGHT REFERENCE across a {{REAR_PLATE_L_ORDERED}} part.** Bed size is not travel,
  and the question is not whether the part fits - it is whether the two 8-bolt patterns' relative
  height survives a reposition. **The budget is well inside 1 mm**, that being the float the 9 mm
  holes give; past it the plate wins and a beam end has to be jacked. Gated on the mill model and
  DRO item below.
- OPEN: **A sensor reading at the min-Y end of the tape**, with the stepper in place, against
  mid-travel. Before 3 m of one-shot PSA goes down.
- SETTLED: ~~**Which extrusion face the casting bolts to**~~ **Closed 2026-10-02 - the question had no
  answer because its premise was wrong.** The casting does not bolt to an extrusion face at all.
  **X, Y1 and Y2 go casting → interposer → beam**, the interposer held by **M8 flange bolts into
  slide-in T-nuts** - on **top** of the X beam, **under** the Y beams. Z has no interposer and lands
  straight on the 1/2" X carriage plate. The face is therefore the top slot face on X and the bottom
  slot face on Y, which was the standing expectation; what was missing was the plate between.
- SETTLED: ~~**The channel width between the side tongues**~~ **Dead 2026-10-03 - there is no channel.** It had been
  dimensioned around 6.35 for a 1/4" plate and the plate went to 1/8", leaving a groove 3 mm wider
  than the thing it located. The arrangement changed instead: the plates sit **flat on the box's top
  skin** and the tongues lap them from **outboard**, a plain bolted lap with nothing to size.
- OPEN: **The delivered thickness of the 1/8" sheet.** The listing says both 1/8" and 11 gauge, which
  differ by 0.135 mm. Harmless structurally, but the riser-proud check keys off
  it. **Caliper it on arrival and write the number here.**
- SETTLED: ~~**Two assumed terms in the rear plate length chain**~~ **Closed 2026-10-02.** The Y rails are
  on the inside faces facing each other, and X / Y1 / Y2 share one HGR20 kit, so the measured 30 mm
  stack applies to all three. The ~1205 chain rests on no guesses.
- SETTLED: ~~**Is the X end plate really 154 wide**~~ **Measured 2026-10-02: 154.18 for two blocks
  butted.** The number stands; the "2-3 mm between the blocks" that this file gave as its reason
  never existed.
- SETTLED: ~~**The X end plate's height and outline**~~ **Closed 2026-10-02 at 242.5 mm.** Set by putting
  the plate's bottom level with the Y ball nut's downward mounting face: 58 mm as built, plus 4.525
  for the 3/8" interposer, plus the 120 mm beam, plus 60 above the beam top. The shop pack's 170 was
  a placeholder and is superseded.
- SETTLED: ~~**Whether the plate's lower tail clears the front riser across Y travel**~~ **Closed
  2026-10-02 - it never gets there.** Max Y travel is reached with the plate's front face level with
  the beam end, where the riser starts. **Redo this check if Y travel is ever extended.**
- SETTLED: ~~**The Y ball nut housing's flange footprint and bolt pattern**~~ **Given 2026-10-02: 40 × 52
  mounting face, 4 × M5 threaded into the nut, 24 × 40 pattern.** The M5s terminate in the nut, so
  nothing from the nut reaches the end plate's edge and the edge-tap size is free - **M6**, and the
  M8 wall worry is moot.
- SETTLED: ~~**The nut pattern's edge inset**~~ **Closed 2026-10-02: 8 mm**, corrected from a first-given 7.
  The pattern is centred - 8 + 24 + 8 = 40 and 6 + 40 + 6 = 52, both closing exactly.
- SETTLED: ~~**Which of the nut face's 40 / 52 runs along Y**~~ **Closed 2026-10-02: the long dimension is
  parallel with the X beam**, so 52 along X and 40 along Y, putting the four M5 at ±20 in X and ±12
  in Y. OPEN: Rests on reading "block" as the nut housing - see the note in that section.
- SETTLED: ~~**The X offset from the X end plate's inner face to the Y screw axis**~~ **Closed 2026-10-02 at
  72.19 mm** - 12.7 plate + 30 rail stack + 30 half beam. It is the **cantilever case**: ~100 mm of
  reach, thrust 60 mm outboard of the plate's outer face.
- SETTLED: ~~**The sole bracket's form - flat foot or an L**~~ **Closed 2026-10-02: a doubler block.** A
  154 × 45 × 1/2" block on the plate's outer face, its end face level with the nut, gives the
  **{{SOLE_BASE_D}}** seating; the sole plate is a **1/4" steel T**, 154 at the root and
  **{{SOLE_STEM_W}}** across the stem. **One row of bolts into that end face**, the base butting the
  strip of plate past it.
- SETTLED: ~~**The doubler's 60 mm height**~~ **Closed at 45 mm, and 60 would have clashed.**
The height was always gated on the **lower bearing block row's bottom edge** - the
  same unmeasured pattern as the 16 holes. It is *not* gated on the Y beam underside, which an earlier
  draft wrongly gave as the limit. **With the block's 44 mm width given on 2026-10-03 that edge lands
  at X 56**, so the 60 overlapped it by 4 mm. **50 clears by 6.** The rule had been written down and
  the number was never checked against it.
- OPEN: **Three plates now carry holes that must agree across an assembly** - end plate, doubler and
  sole bracket. **Drill the doubler's through-holes and the end plate's together**, and leave the
  sole bracket's root holes until the first two are mated.
- SETTLED: ~~**The shelf's rear bolt is at Y 0, off the plate**~~ **Closed 2026-10-02.** The shelf becomes a
  **2" bar** with **two M8 at Y 30, stacked at Z 15 and Z 35**, blind-tapped. All four holes are now
  dimensioned from the **plate's back edge**, which is the actual fix - the beam front was never something to measure from.
- OPEN: **Confirm the lower shelf bolt against the block pattern** once measured. Blind-tapping should
  make it moot; this is a check that the skin left is sane, not a gate.
- SETTLED: ~~**Rib under the full {{REAR_PLATE_L_ORDERED}} of rear bottom-edge bearing.**~~ **Closed 2026-10-11: not
  needed.** The plate's 6.35 footprint sits wholly inside the 19 back web, with the {{TONGUE_CLEAR}} tongue
  outboard of that - backed by solid wall over its whole length, so there is no span.
- OPEN: **The two blocks beside the back centre tenon** - position settled at X 562.62 and 648.62,
  running forward from the back web. **Length is his call**; drawn to the first across-rib so each is
  captured at both ends.
- SETTLED: ~~**Blocking under the front fin bases and the fin angle's T-nuts.**~~ **Closed 2026-10-11: not
  needed.** The fin base is **34.55 mm** from the last across-rib and the T-nuts **67.55 mm** - short
  overhangs off a support, not spans. The item existed because the general warning predated any rib
  layout. If the bearing is ever wanted harder, **move a rib, do not add blocking**.

## SETTLED: From the 2026-10-08 order - the back plate's length

- SETTLED: **What Sheet 7's X 0 measures from. Closed 2026-10-10: the Y1 extrusion's outboard face.**
  The side plates came in at **10 gauge (3.429)** rather than the nominal 1/8" (3.175), so the
  envelope that runs the back plate flush with their outer faces grew 0.508 to **1211.238**, and
  the plate was bought at **47 21/32" = 1210.47** - **0.77 short of flush**. That was not cosmetic
  while Sheet 7's sixteen beam bores and its eight torsion-box stations were absolute from the
  plate's left edge: a plate 0.77 short put the **Y2 beam station out by the whole 0.77**.
  **His call:** the plate's left edge goes on the **Y1 extrusion's outboard face**, side plate not
  included, so the side plate stands proud of it there and the far end falls where the bought
  length puts it. **The plate's length now feeds nothing.** Sheet 7's near-end holes come out on a
  round 15 and 45 and 7 and 53, the Y2 station mirrors about the **beam spacing** at 1204.38
  rather than about the plate, and the eight torsion-box bolts start at **50** on the same 150
  pitch the other bolt-on plates use instead of being centred on the plate.
  **The envelope figure kept its meaning and lost the plate's name:** it is `MACHINE_OUTER_W` now,
  the width `BOX_W` takes and the ceiling lateral-stiffness.md names. `REAR_PLATE_L` is retired.
  OPEN: **The Y2-end holes are provisional** - measure the built beam spacing before drilling that
  end.

## From the 2026-10-08 datasheet pass

- FLAG: **The X ball nut has no mounting specified anywhere.** Not in prose, and Sheet 3a carries no
  holes for it — the X carriage plate has its rails, BF12, the Z cast stepper frame, the sensor
  bore, the four X bearing blocks and the top stop, and nothing that attaches the plate to the
  screw that drives it. **The same omission the Z plate had**, found the same way: by working
  through a neighbouring joint. All four nuts are the same part, so the pattern is known — 40 × 52
  face, 4 × M5 on a 24 × 40 grid, 8 mm of thread in a 16 mm hole — but where it lands on the plate
  and what carries it are not decided.
- OPEN: **One block measurement does not reconcile.** The body mics 75.68 and a pair pushed together
  with the button heads touching reads 154, which makes each head 1.32 proud — but the over-head
  reading was 76.24, which makes it 0.56. The two differ by 0.76 and it sets how much room the
  driver has between the blocks. **It does not move a hole**: the C-hole rows derive from the
  chosen 87 centre separation and the block’s own 36 bolt pitch.
- OPEN: **The C-hole row offsets imply the block centres sit 80 apart** where the closest they can
  physically sit is 77. The button heads account for 1.32 of that, not 3.

## From the 2026-10-11 spoilboard pass

- OPEN: **The M8 drop-in T-bolt that holds the MDF down - three figures, all off the drawer.** How far
  the thread stands **above the top of the aluminium** with the T home in its slot; the **washer
  thickness**; the **nut height**. Together they set the counterbore depth. FLAG: **The holes ARE now
  drawn in the 3D model**, on the 50 and on catalogue washer and nut figures, so the counterbore
  there will move when these are measured - this item said they were deliberately left out, and
  that stopped being true the same day. NOTE: **A 40 was photographed
  beside the sandwich and tops out around the seam between the two sheets - it dies inside the
  board. He reads a 50 as the one.** With a 66 surface over a 16 track there is 50 of MDF to get
  through, so the nut has to sit in a counterbore whichever bolt it is. See
  [`spoilboard.md`](spoilboard.md).
- OPEN: **The sole plate underside reads 113.15 in prose and 120.65 in the model.** `spoilboard.md`'s
  envelope table calls 113.15 the lowest thing that sweeps; the Y sole brackets in
  `tools/make-3d.py` bottom out at 120.65. Noticed 2026-10-11 and **not chased** - it moves a
  clearance, not a hole, and the two may be different elements of the same assembly.

## From the 2026-10-11 tooltip pass

- FLAG: **28 bolts are drawn on the machine that the fastener schedule has no entry for**, so they are
  on no buy list: **16 Y sole bolts** (the sole bracket's root rows into the end plate's end face
  and the doubler's edge), **6 Z casting bolts** into the carriage plate, **4 X sole bolts**, and
  **2 BF12 bolts** on the carriage plate. Found by making the model's tooltips read their length out
  of `dimensions/fasteners.toml`: the ones that came back empty are this list.
  `tools/make-3d.py` now prints it on every run, so it cannot go quiet again.

## Carried forward

- SETTLED: ~~**Height from the top of the beam to the torsion box fixing line**, and whether the box has
  a **vertical face** to bolt against.~~ **Both closed 2026-09-30** - the box gets a purpose-built
  vertical face and the plate's bottom edge bears on the top skin. See "How it lands on the torsion
  box" above.
- SETTLED: ~~**The exact box width**~~ **Closed 2026-10-03 - it turned into a design number after all.**
  It was going to be measured off the assembled CNC, which could not happen until the machine stood up.
  Then the rear plate's length stopped being a window and became **1210.73 derived** — the envelope as
  it stood that day, with a 1/8" side plate, and the one literal on this page that must NOT become
  {{REAR_PLATE_L_ORDERED}}: it is what the figure was then, not what the plate is — and his rule
  settles the rest: **the box with its laminated tongues fills the space inside the side plates, the
  rear plate and the front fins exactly.** FLAG: **That reading was WRONG and was corrected the same
  day** - the box is the larger part. **BOX_W = 1211** (inside the two side tongues, the machine's own
  outer envelope of {{MACHINE_OUTER_W}} rounded down to a whole millimetre) and **BOX_FORE_AFT = 1210**, his
  figure 2026-10-11, picked to make the box square - and since 2026-10-14 it IS square, both 1211.
  The front overhang is what falls out of it, **{{BOX_FRONT_OVERHANG}}**, and
  the chain was inverted to say so: he sizes the box and the apron is the remainder. NOTE: **Still
  check it against the standing machine before cutting the skins** - the chain is nominal in its plate
  thicknesses, so this closes the *design* question, not the verification.
- SETTLED: ~~**Where the three-point mount pads sit relative to the two outer walls**~~ **Already answered,
  and this item was stale - corrected 2026-10-02.** They are not pads. Each post is reduced over its
  top 116 mm to a tenon, and the **42 mm ledge** left behind is cut on the **outward-facing** faces
  **precisely so the perimeter wall lands on it** - which is exactly what this item was asking for.
  Front posts carry a ledge on their outside *and* front edges, taking the side and front walls plus
  their laminated tongues; the back-centre post has a single-sided ledge under the back wall and its
  tongue. The two rear corner legs have no tenon and stand ~2 mm shy, so the box never touches them.
  FLAG: **The claim that the scheme was "only in the project notes, not in this repo" was simply
  wrong** - [`archive/torsion-box.md`](archive/torsion-box.md) carries the mount, the tenons, the ledge depth, the
  back post's single-sided shoulder and what the tenons ask of the rib grid. **It was repeated twice
  in conversation on 2026-10-02 on the strength of this list rather than the file.** An open-items
  entry is a pointer, not evidence; read the file it points at before believing it.
- SETTLED: ~~**The L bracket specification** - "15 × 1.5" has not been resolved.~~ OPEN: **"Moot 2026-09-30 -
  there are no L brackets" WAS WRONG AND STAYED IN THIS FILE FOR ELEVEN DAYS.** Brackets came back on
  2026-10-03 when the front tongue was deleted and the fin needed tying down, and the item was never
  reopened. SETTLED: **Now genuinely closed, 2026-10-11, with a specified part**: one 170 mm length of
  40 × 40 angle extrusion per fin, in FRONT of it, tapped M8 into the fin at Y 20 and bolted to
  prong inserts in the top skin. See [`assembly.md`](assembly.md).
- SETTLED: ~~**Front corner three-way convergence**~~ **Closed 2026-09-30** - the front and back tongues run
  long and lap the side tongues' ends; nothing is notched. See "The lateral fix".
- FLAG: **How far past the front riser plane the spindle reaches**, and whether it fouls the widened fin
  at low Z. Confirmed to pass the plane; the amount is unmeasured. **Needed before the front plates are
  cut.** Four numbers listed under "The lateral fix".
  **Worse as of 2026-10-02**: the cast stepper frame and a NEMA 23 now occupy that end too, so the
  question is no longer only "does the spindle clear the fin" but "does it clear the fin, the
  casting and the motor". Add the casting's envelope to the four numbers.
- SETTLED: ~~**Whether the front fins need the rib layout fixed first.**~~ **Closed 2026-10-11** - the layout
  is fixed at 4 + 4 and the fin lands 34.55 from a rib, which needs nothing. Original wording: the
  bottom-edge bearing wants blocking
  under the full 203 mm base.
- SETTLED: **How nod is adjusted - answered 2026-09-30.** The question was whether the spacer M5 counterbore
  pattern clears the clamp footprint. **It does not clear it by position alone** - the M8 column at
  50 mm and the M5 column at 41.5 mm are only 8.5 mm apart and overlap at equal height - so the
  clearance is bought **vertically**, by bringing the clamp centres to **116 mm**. Worst case is
  **14.1 mm centre-to-centre**, about 5 mm of web. **No tram sub-plate, no added moment arm.** Full
  working in the Z plate section.
- **The mill's model number and whether it has a DRO** (2-axis or 3-axis) - expected ~2026-10-04. If there is no DRO, the drawings want dimensioning differently.
- FLAG: **Can Garen's mill traverse ~1212 mm in X?** The direct question, and the one the rear plate waits on: the M8 patterns sit at **both ends of a {{REAR_PLATE_L_ORDERED}} plate**, so either the machine reaches both or the part is repositioned mid-job - and a reposition is where the height reference between the two patterns gets lost. Ask the travel, not the model number; the model is only a proxy for it.
- SETTLED: ~~**Z travel floor** - where the confirmed travel sits relative to the spoilboard.~~
  **Closed 2026-10-11, and it was not a machine measurement.** The tip floor is **45.2 mm** above the
  box's top skin and the spoilboard surface is at **67.5 mm**; the gantry fixes the reach and the
  spoilboard stack positions the work in it. See [`spoilboard.md`](spoilboard.md).
- **Vertical distance from the X beam centreline down to the spindle nose, Z fully retracted** - plus
  the **Z travel**. Together these give the torsional arm; worst case is the fixed distance plus full
  travel plus tool stickout. (Earlier drafts asked for "tool tip to beam", which is not a machine
  dimension - it moves with Z position, tool length and stickout. Use the **spindle nose**, a fixed
  feature of the body, rather than the collet nut, which shifts with collet type.) The horizontal arm
  is settled at 109 mm from the carriage plate, ~152 mm from the beam face.
- **A torsion constant J for `30-6060`.** 8020 publish Ix and Iy but not J, so the gantry's
  torsional stiffness cannot yet be computed rather than estimated.
- **Riser plate orientation** for the X end plates, which governs whether the weak-axis warning
  applies as written.
