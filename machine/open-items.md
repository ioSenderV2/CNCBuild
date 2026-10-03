# ⚠️ Open items

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

## From the 2026-10-02 stepper frame rework - all unmeasured

- ✅ ~~**The as-built BK12 screw axis height**~~ **Closed 2026-10-02**, and reframed: the number
  that matters is the **10 mm** between the beam underside and the nut top, with the supports
  mounted 5 mm above the extrusion. The casting hangs below the beam, so that clearance grows.
- ✅ ~~**The casting's 6-hole pattern against the T-nut holes**~~ **Closed 2026-10-02.** Measured at
  columns 7 / 53 and rows 28 / 58 / 71. The columns clash with the T-slots at 8 mm, which is why
  the bar runs ~30 mm past the casting and the four T-nut bolts live in the overhang.
- ✅ ~~**The two strip widths either side of the window**~~ **Measured 2026-10-02: 19 mm outboard**,
  and it now derives from the geometry too. The fins are **100 / 200 over 302**, both halves out of
  the measured 302 mm square with 2 mm for the kerf.
- ✅ ~~**The window's horizontal position does not reconcile**~~ **Closed 2026-10-02 - it was my
  arithmetic, off a wrong column position.** With the M8 columns at **35 and 65** rather than 20
  and 50, the beam spans X 20-80 and its centreline is X 50, so a 62 mm window centred on the screw
  runs **19 to 81** - exactly the 19 mm strip measured off the template. Nothing about the casting
  or the bar had to move.
- 🔴 ~~**The riser stands 1.8 mm proud of the side plate**~~ **WRONG, corrected 2026-10-02 to
  16.8 mm.** The 1.8 was computed off a superseded M8 column at **20**; the column is **35**, which
  this file had already corrected elsewhere while this bullet kept the old consequence. The chain:
  **35 − 15 = 20 mm of fin overhanging the Y beam's outboard face**, less the side plate's
  thickness. ✅ Thickness of the fin is not a term, so the 10 mm stock is irrelevant to it.
  🔴 **The curb decision gets more important, not less** - a curb reaching the riser's station
  would be held out by **~16.8 mm**, not 1.8, so terminating it short is now clearly required rather
  than merely tidy.
- ⚠️ **Terminate the side curb short of the front riser's station** so the curb bears on the side
  plate rather than being held out by the riser. A box decision, free while the box is unbuilt.
- ✅ ~~**T2's edge distance, on the template**~~ **Closed 2026-10-02.** X 25 and 170 on the Y 30
  line both check out against the physical template - photo committed. **The front fin's geometry
  is fully settled.**
- 🔴 **Whether the Laguna can hold the HEIGHT datum across a 1200 mm part.** Bed size is not travel,
  and the question is not whether the part fits - it is whether the two 8-bolt patterns' relative
  height survives a reposition. **The budget is well inside 1 mm**, that being the float the 9 mm
  holes give; past it the plate wins and a beam end has to be jacked. Gated on the mill model and
  DRO item below.
- ⚠️ **A sensor reading at the min-Y end of the tape**, with the stepper in place, against
  mid-travel. Before 3 m of one-shot PSA goes down.
- ✅ ~~**Which extrusion face the casting bolts to**~~ **Closed 2026-10-02 - the question had no
  answer because its premise was wrong.** The casting does not bolt to an extrusion face at all.
  **X, Y1 and Y2 go casting → interposer → beam**, the interposer held by **M8 flange bolts into
  slide-in T-nuts** - on **top** of the X beam, **under** the Y beams. Z has no interposer and lands
  straight on the 1/2" X carriage plate. The face is therefore the top slot face on X and the bottom
  slot face on Y, which was the standing expectation; what was missing was the plate between.
- ⚠️ **The curb channel width** - dimensioned around 6.35 mm, now taking 3.175 mm, or 3.04 mm if
  the sheet arrives at a true 11 gauge.
- ⚠️ **The delivered thickness of the 1/8" sheet.** The listing says both 1/8" and 11 gauge, which
  differ by 0.135 mm. Harmless structurally, but the curb channel and the riser-proud check key off
  it. **Caliper it on arrival and write the number here.**
- ✅ ~~**Two assumed terms in the rear plate length chain**~~ **Closed 2026-10-02.** The Y rails are
  on the inside faces facing each other, and X / Y1 / Y2 share one HGR20 kit, so the measured 30 mm
  stack applies to all three. The ~1205 chain rests on no guesses.
- ✅ ~~**Is the X end plate really 154 wide**~~ **Measured 2026-10-02: 154.18 for two blocks
  butted.** The number stands; the "2-3 mm between the blocks" that this file gave as its reason
  never existed.
- ✅ ~~**The X end plate's height and outline**~~ **Closed 2026-10-02 at 242.5 mm.** Set by putting
  the plate's bottom level with the Y ball nut's downward mounting face: 58 mm as built, plus 4.525
  for the 3/8" interposer, plus the 120 mm beam, plus 60 above the beam top. The shop pack's 170 was
  a placeholder and is superseded.
- ✅ ~~**Whether the plate's lower tail clears the front riser across Y travel**~~ **Closed
  2026-10-02 - it never gets there.** Max Y travel is reached with the plate's front face level with
  the beam end, where the riser starts. **Redo this check if Y travel is ever extended.**
- ✅ ~~**The Y ball nut housing's flange footprint and bolt pattern**~~ **Given 2026-10-02: 40 × 52
  mounting face, 4 × M5 threaded into the nut, 24 × 40 pattern.** The M5s terminate in the nut, so
  nothing from the nut reaches the end plate's edge and the edge-tap size is free - **M6**, and the
  M8 wall worry is moot.
- ✅ ~~**The nut pattern's edge inset**~~ **Closed 2026-10-02: 8 mm**, corrected from a first-given 7.
  The pattern is centred - 8 + 24 + 8 = 40 and 6 + 40 + 6 = 52, both closing exactly.
- ✅ ~~**Which of the nut face's 40 / 52 runs along Y**~~ **Closed 2026-10-02: the long dimension is
  parallel with the X beam**, so 52 along X and 40 along Y, putting the four M5 at ±20 in X and ±12
  in Y. ⚠️ Rests on reading "block" as the nut housing - see the note in that section.
- ✅ ~~**The X offset from the X end plate's inner face to the Y screw axis**~~ **Closed 2026-10-02 at
  72.7 mm** - 12.7 plate + 30 rail stack + 30 half beam. It is the **cantilever case**: ~100 mm of
  reach, thrust 60 mm outboard of the plate's outer face.
- ✅ ~~**The sole bracket's form - flat foot or an L**~~ **Closed 2026-10-02: a doubler block.** A
  154 × 60 × 1/2" block on the plate's outer face gives a 25.4 mm seating, and the sole bracket is a
  1/4" trapezoid, 154 at the root to ~46 over the nut. **Two rows of bolts across the 25.4.**
- ⚠️ **The doubler's 60 mm height** is gated on the **lower bearing block row's bottom edge** - the
  same unmeasured pattern as the 16 holes. It is *not* gated on the Y beam underside, which an earlier
  draft wrongly gave as the limit; the doubler sits ~17 mm inboard of the beam's inside face.
- ⚠️ **Three plates now carry holes that must agree across an assembly** - end plate, doubler and
  sole bracket. **Drill the doubler's through-holes and the end plate's together**, and leave the
  sole bracket's root holes until the first two are mated.
- ✅ ~~**The shelf's rear bolt is at Y 0, off the plate**~~ **Closed 2026-10-02.** The shelf becomes a
  **2" bar** with **two M8 at Y 30, stacked at Z 15 and Z 35**, blind-tapped. All four holes are now
  dimensioned from the **plate's back edge**, which is the actual fix - the beam front was never a
  datum.
- ⚠️ **Confirm the lower shelf bolt against the block pattern** once measured. Blind-tapping should
  make it moot; this is a check that the skin left is sane, not a gate.
- ⚠️ **Rib under the full 1200 mm of rear bottom-edge bearing.** Decide before the skins are cut.

## Carried forward

- ✅ ~~**Height from the top of the beam to the torsion box fixing line**, and whether the box has
  a **vertical face** to bolt against.~~ **Both closed 2026-09-30** - the box gets a purpose-built
  vertical face and the plate's bottom edge bears on the top skin. See "How it lands on the torsion
  box" above.
- **The exact box width**, which sets the top skin and therefore the spacing of the two curbs. Not a
  design number: it is **measured off the fully assembled CNC standing on a flat surface**, and the box
  is not built until then. Nothing else is blocked by it in the meantime.
- ✅ ~~**Where the three-point mount pads sit relative to the two outer walls**~~ **Already answered,
  and this item was stale - corrected 2026-10-02.** They are not pads. Each post is reduced over its
  top 118 mm to a tenon, and the **38 mm ledge** left behind is cut on the **outward-facing** faces
  **precisely so the perimeter wall lands on it** - which is exactly what this item was asking for.
  Front posts carry a ledge on their outside *and* front edges, taking the side and front walls plus
  their laminated tongues; the back-centre post has a single-sided ledge under the back wall and its
  tongue. The two rear corner legs have no tenon and stand ~2 mm shy, so the box never touches them.
  🔴 **The claim that the scheme was "only in the project notes, not in this repo" was simply
  wrong** - [`torsion-box.md`](torsion-box.md) carries the mount, the tenons, the ledge depth, the
  back post's single-sided shoulder and what the tenons ask of the rib grid. **It was repeated twice
  in conversation on 2026-10-02 on the strength of this list rather than the file.** An open-items
  entry is a pointer, not evidence; read the file it points at before believing it.
- ✅ ~~**The L bracket specification** - "15 × 1.5" has not been resolved.~~ **Moot 2026-09-30** - the
  tapered base gives the bolt spacing directly, so there are no L brackets. See "The lateral fix".
- ✅ ~~**Front corner three-way convergence**~~ **Closed 2026-09-30** - the front and back tongues run
  long and lap the side tongues' ends; nothing is notched. See "The lateral fix".
- 🔴 **How far past the front riser plane the spindle reaches**, and whether it fouls the widened fin
  at low Z. Confirmed to pass the plane; the amount is unmeasured. **Needed before the front plates are
  cut.** Four numbers listed under "The lateral fix".
  **Worse as of 2026-10-02**: the cast stepper frame and a NEMA 23 now occupy that end too, so the
  question is no longer only "does the spindle clear the fin" but "does it clear the fin, the
  casting and the motor". Add the casting's envelope to the four numbers.
- **Whether the front fins need the rib layout fixed first** - the bottom-edge bearing wants blocking
  under the full 203 mm base.
- ✅ **How nod is adjusted - answered 2026-09-30.** The question was whether the spacer M5 counterbore
  pattern clears the clamp footprint. **It does not clear it by position alone** - the M8 column at
  50 mm and the M5 column at 41.5 mm are only 8.5 mm apart and overlap at equal height - so the
  clearance is bought **vertically**, by bringing the clamp centres to **116 mm**. Worst case is
  **14.1 mm centre-to-centre**, about 5 mm of web. **No tram sub-plate, no added moment arm.** Full
  working in the Z plate section.
- **The mill's model number and whether it has a DRO** (2-axis or 3-axis) - expected ~2026-10-04. If there is no DRO, the drawings want dimensioning differently.
- 🔴 **Can Garen's mill traverse ~1200 mm in X?** The direct question, and the one the rear plate waits on: the M8 patterns sit at **both ends of a 1200 mm plate**, so either the machine reaches both or the part is repositioned mid-job - and a reposition is where the height datum between the two patterns gets lost. Ask the travel, not the model number; the model is only a proxy for it.
- **Z travel floor** - where the confirmed 246 mm sits relative to the spoilboard. A machine
  measurement, and the one item the travel budget still waits on.
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
