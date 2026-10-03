# The Z carriage

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

| | |
|---|---|
| Plate | **154 mm W × 407 mm H × 1/2"** aluminium |
| Rails | **HGR20, 400 mm, down both sides, mounted on the plate** |
| Screw | 1605, with **BK12 and BF12 bolted to the same plate** - so screw and motor are fixed relative to it |
| Spacers | **two lengths of 2" × nominally 5/8" aluminium bar**, cut from one 12" piece, sandwiched between the bearing blocks and the Z plate. Each spans two bearing blocks. 🔴 **Measured 2026-10-02: 150.5 and 151.6 long, 16.41 and 16.43 thick** - they are *not* 15.875; see "The spacers are not 5/8"" below |
| Bolt count | **16 × M5 × 35** - 8 per spacer, 4 per bearing block |
| Fixing | **one M5 per hole does the whole stack** - counterbored in the Z plate, through a 6 mm clearance hole in the spacer, into the bearing block's tapped M5 |

Blocks, spacers and the ball nut housing form one assembly and present their faces at a common
height; plate, rails, screw and motor form the other. They are the two halves of the axis.

Dry-assembled in [`photos/z-carriage-assembly-end.jpg`](photos/z-carriage-assembly-end.jpg) and
[`photos/z-carriage-assembly-oblique.jpg`](photos/z-carriage-assembly-oblique.jpg).

## ✅ The Z plate: 164 mm W × 175 mm H × 1/2"

### 🔴 164, not 154 - the width is set by the spacers, and 154 could not be drilled

**Corrected 2026-10-02.** The plate inherited 154 from the X end plate, and that number does not
work here:

| | On 154 | **On 164** |
|---|---|---|
| Plate half-width | 77 | **82** |
| Outer M5 column, from plate centre | 73.5 | 73.5 |
| **Edge distance** | **3.5 mm** | **8.5 mm** |
| Ø10 counterbore (5 mm radius) | **breaks through by 1.5 mm** | **clears by 3.5 mm** |

**Two independent reasons land on the same number.** The plate has to **cover the spacers** - with
the rails 10 mm in from each side of the carriage plate, that needs 164. And 164 is also what stops
eight of the sixteen M5 counterbores breaking out of the plate edge.

✅ **Nothing in the clamp working is disturbed.** The M8-to-M5 column offset is 8.5 mm measured
*from plate centre* either way, so the 116 mm clamp separation, the ±45.5 / ±70.5 M8 rows and the
14.1 mm worst-case clearance all survive unchanged. Only the outline moved.

⚠️ **It may cost ~10 mm of X travel** - the Z plate is now 5 mm wider than the carriage plate on
each side, so it reaches the X end plates sooner if it is the widest moving part. Not checked
against the end-stop geometry; flagged rather than claimed.

**The M5 pattern sets the clamp separation.** Not the barrel, not the block run - the four M5
counterbores that hold the plate to the bearing blocks share the plate's front face with the M8 tapped
holes, and dodging them is what fixes everything else.

| | |
|---|---|
| Plate | **164 mm W × 175 mm H × 1/2"** |
| **Clamp centres** | **116 mm** - clamp mid-height at **±58 mm** from plate centre |
| Clamp extent | **171 mm**, on a 199 mm barrel |
| M8 columns | **±50 mm** from plate centre |
| **M8 rows, from plate centre** | **±45.5 and ±70.5 mm** |
| **M8 rows, from the nearer plate end** | **17 and 42 mm** ← the drilling dimension |
| Relief at each plate end | 2 mm |
| Blocks | **butted**, full **246 mm** travel |
| Spacers | **6 inch, unchanged** |

### The measurements this rests on - all read off parts, 2026-09-30

| | |
|---|---|
| Bearing block hole pattern | **32 × 36 mm** |
| M5 columns, from the rail centreline | **±16 mm** - ✅ this confirms the figure the file had carried as its one unverified number |
| M5 columns, from plate centre | **41.5 and 73.5 mm** (rail centrelines at ±57.5) |
| M5 rows, from the spacer bottom | **17, 53, 97, 133 mm** |
| **M5 rows, from plate centre** | **−59.2, −23.2, +20.8, +56.8 mm** |
| Clamp bolts | 4 × M8, **columns 100 mm apart**, **rows 25 mm apart** |

📌 **The 36 in the 32 × 36 is self-checking:** 53 − 17 = 36 and 133 − 97 = 36, so the row measurements
and the block pattern agree independently.

### 🔴 Why 116 mm and not 144 - the columns are only 8.5 mm apart

**The M8 column at 50 mm sits just 8.5 mm from the M5 column at 41.5 mm.** An M5 counterbore is ~Ø10
and an M8 thread is Ø8, so **at the same height those two features physically overlap** - there is no
web at all. The M8 rows therefore have to stand vertically clear of every M5 row.

🔴 **That kills 144 mm centres outright.** At 144 the inner M8 rows land at **±59.5 mm**, against M5
rows at **−59.2 and +56.8**. A direct hit at both ends - it would have been found at the mill.

Holding **12 mm centre-to-centre in 2D**, and with 8.5 mm of that already spent on the column offset,
each M8 row needs ~8.5 mm of *vertical* clearance from every M5 row. That confines the clamp
mid-height to **55.2 to 60.8 mm** from plate centre. **±58 is the middle of that window**, and gives
a worst case of **14.1 mm centre-to-centre - about 5 mm of solid web** at the tightest pair.

### What 116 mm buys and costs

- ❌ **Costs ~35% of the angular stiffness** against the unobtainable 144. Two clamps resist the tool's
  tipping couple on a lever equal to their separation, so stiffness goes as separation *squared*.
- ✅ **Still 37% better than the 99 mm** an earlier draft proposed, which set the clamp extent to the
  154 mm block run.
- ✅ **Zero overhang, and it costs nothing to get.** At ±70.5 **all four M8 rows are inside the ±76.2
  of the existing 6" spacers.** Every bolt is over supported metal without spreading the blocks.
- ✅ **Nothing gets re-cut and no travel is spent.** Blocks butted, full 246 mm, spacers as built.

📌 **This is also why 205 mm spacers do not help.** The collision is between two features **in the
plate**; spacer length has no bearing on it, and the M5 positions are set by the blocks and cannot
move. See the rejection note below.

📌 **175 mm is where the first draft of this section landed too**, by a completely different route -
that one sized the plate to the block run, this one to the M5 pattern. Coincidence, but a reassuring
one.

⚠️ **175 assumes nothing else lives on this plate** - no drag chain anchor, cable strain relief or
water line clamp. If one turns up, height is the cheap thing to change, but only before it is cut.

**Still measure on arrival:**

- **Where the water fittings and cable exit sit** - they cap the clamp spread and set the drag chain
  routing
- **Nose to collet nut face** - the fixed part of the torsional arm; the drawing says 52 mm, unverified
- **Weight**, for the moving mass
- **Body diameter** over the whole clamping length rather than nominally

### The overhang below the spacer blocks is cubed

Anything below the spacers is unsupported plate, and putting the lower clamp there inserts a
cantilever right where it hurts. The lower clamp also carries **more** than the cutting force, since
the two clamps react the tool's overhang as a couple - roughly 1.5 to 1.8×.

| Overhang | Deflection at the lower clamp, peak load |
|---|---|
| 2" (50.8 mm) | ~0.03-0.04 mm |
| **1" (25.4 mm)** | **~0.004-0.005 mm** |

**A factor of eight for one inch.** If the clamps need more separation than the supported region
offers, **spread the bearing blocks and lengthen the spacers** rather than hanging plate off the
bottom - that widens the supported base with no cantilever at all. The cost is Z travel, which is the
honest trade: **spend travel, not stiffness.**

### The travel budget

Rails are **400 mm**, blocks **77 mm**, so with the blocks butted the usable travel is **246 mm**.

⚠️ **That 77 was measured on the Z kit.** The X/Y kit's blocks measure **77.09** and so the two
agree - but they are different suppliers and the agreement is not guaranteed. See the kit note
under the X gantry end plates.

⚠️ **272 mm is the screw-side travel and it is NOT discarded** - it is the span the nut can run
between its two supports, which overruns the rails. It is simply not the limit; the rails are.
*(An earlier wording here said the measurement was "discarded", which was too strong and would
invite the next reader to ignore a live figure.)*

✅ **The casting leaves it at 272 - confirmed 2026-10-02.** Replacing BK12 with the cast frame does
not move the upper bearing relative to BF12, so **the whole travel budget below is unchanged**:
246 mm rail-limited, ~26 mm of screw overrun, and the 7 mm / 10 mm stop working still stands.

### ✅ The screw outruns the rails by ~26 mm upward - and a physical stop catches it

**Both ends of Z travel have a mechanical stop.** Going down, the nut bottoms on BF12. Going up,
blocks bolted to the top of the X carriage plate overhang the rail ends and the rising bearing
block meets them. The **proximity sensor is at the top of Z**; the stop is what catches the axis if
the control runs past it.

### ✅ The top stop is TWO blocks, not one plate - 2026-10-02

The cast stepper frame now occupies the middle of that top edge, so a single 6" plate spanning both
rails cannot go there. **One block per rail, either side of the 60 mm casting:**

Each block caps the plate's top edge and overhangs forward over the rail end:

| | |
|---|---|
| Width, across the plate | **47 mm** - 154 − 60 = 94, halved, less whatever relief is wanted at the casting |
| Front-to-back | **32.5 mm** = **12.5 of plate + 20 of rail**, so the overhang is flush with the rail top |
| Vertical thickness | **1/4"** |
| Fixing | **2 × M4 × 16 socket head** per block, down through it into tapped holes in the plate's **12.7 mm top edge** |

📌 **M4 rather than M5 on edge distance**: tapping a 12.7 mm edge leaves 4.35 mm of wall each side
of an M4 against 3.85 for an M5.

🔴 **Do not size these by strength.** They fire only if **the soft limit and the proximity sensor
have both already failed**, and the design intent is that they are **sacrificial** - if one is ever
used, replace the block and the bolts and move on. That is the same reasoning the superseded 1/4"
plate was chosen on. *(A load analysis was written here and removed: a part deliberately made the
weak link does not get a safety factor.)*

✅ **This is better than the plate it replaces, not just a way round the casting.** Each block sits
**directly over its own rail** - centres at ~23.5 and ~130.5 against rail centrelines at 19.5 and
134.5 - so the rising block meets metal immediately above itself instead of at the end of a lip
spanning the gap. The old warning to "keep the overhang short so impact loads the bolts in shear
rather than bending a cantilevered lip" is satisfied by the geometry rather than by discipline.

📌 **Matching the rail's height is what makes the contact square.** The bearing block stands 30 mm
off the plate and wraps the rail; a stop flush with the rail top gives it a full-width face to hit,
where the old 1/4" plate presented a 6.35 mm lip.

✅ **Rail height taken off the part: 20 mm** - which is what the 32.5 is built from, and why the
derivation is written out rather than just the total. This mattered because **Z is a different
supplier from X / Y1 / Y2** and this file already carries one near-miss from quoting a dimension
measured on the wrong kit.

⚠️ **This heading used to read "with no hard stop", and it was wrong** - the resolution was already
written in the paragraphs below it while the alarm stayed in the title. Corrected 2026-10-01, after
that stale heading was read at face value and propagated into
[`../commissioning/stiffness-test.md`](../commissioning/stiffness-test.md) as a reason not to put the
carriage near the top of travel. **A headline that contradicts its own body is worse than no note**,
because skimming is how a long file gets read.

**The hazard being guarded against was real and is worth keeping.** A soft limit is a configured
value, and if it is ever wrong, missing or bypassed - a homing move, a lost setting, a restored config
- nothing in software stops the carriage leaving the rail. That is the failure this repo's standing
rule exists for, and it is why the stop is physical.

**The failure being guarded against is not the crash - it is losing the ball train.** Run a block off
a rail end and the balls escape the recirculation path and the block is scrap. The design allows the
block **7 mm past the rail end** before contact, against the **first 10 mm of the block carrying no
balls**.

✅ **Measured with calipers: 10 mm** from the end of the block to the first exposed bearing. So the
7 mm of overrun has **3 mm to spare** and the design stands - **no rail shift needed, the carriage
plate can be drilled as laid out.**

📌 That 3 mm is nominal. Rail length, plate height and the flush-mount datum each carry a little
tolerance, so the real figure could land between roughly 1.5 and 4 mm. Positive in every case, and
the stop only fires if the control has already failed - but it is why the nominal should not go any
tighter.

📌 **Not to be confused with the plastic arbor.** The plastic strips supplied with the blocks are a
**transfer and storage tool** - slide a block off the rail onto the strip to store it, and it is
pushed out again as the block goes back on. They do nothing during an overrun in service.

An **integral retainer** - a wire or cage inside the block holding the balls captive off the rail -
is a separate optional feature on some series, usually flagged in the part number rather than
visible. Worth a glance if the part number is to hand, but it changes nothing: **the measured 10 mm
is the protection either way.**

Keep the arbors. Re-spacing blocks for clamp alignment needs no removal - unbolt the spacers, slide
the blocks along the rail - but nothing else substitutes the day one is needed.

**The 7 mm is forced, not chosen:** the X carriage plate is 16" (407 mm), the rail is 400 mm mounted
flush with the plate's bottom edge, and the stop sits on the top edge - leaving 7 mm. There is
nowhere lower for the stop to go.

📌 **But the rail position is still free, and only until the plate is drilled.** Mounting the rail
**3 mm up from the bottom edge instead of flush** makes the top gap 4 mm. It costs nothing:

- **Travel is unchanged** - 246 mm is rail length minus block span, wherever the rail sits.
- **The bottom end does not care** - BF12 stops the nut before the lower blocks near the rail's lower
  end, so nothing is given up; if anything it gains 3 mm.
- The travel band shifts up 3 mm, absorbed by mounting the spindle 3 mm lower if it matters.

✅ **Measured at 10 mm, so this lever was not needed** - kept because the reasoning applies to any
rail-and-plate pairing done later, and because the option genuinely expires when the plate is
drilled.

The block is hardened steel and the plate 1/4" aluminium, so **the plate is sacrificial** - correct
for something that should fire once or twice in the machine's life. **Keep the overhang short** so
impact loads the bolts in shear rather than bending a cantilevered lip.

The bottom end needs nothing: the nut bottoms on BF12 before the rails run out, so one stop at the
top covers the whole ~26 mm of screw overrun.

### 🔴 Travel + clamp separation ≈ 323 mm

Align **clamp centres over block centres** - then the load goes straight into the blocks and the
plate does no bending at all. The block span is then clamp separation plus 77 mm, so:

| Clamp separation | Z travel |
|---|---|
| 77 mm (blocks butted) | 246 mm |
| 120 mm | 203 mm |
| 150 mm | 173 mm |
| 200 mm | 123 mm |

Less end clearances. **Every millimetre of clamp separation costs a millimetre of
travel.** The spindle's usable body length says how far the clamps *can* spread; this line says what
it costs.

**Two things soften it:**

- **Clamps need not sit exactly over the blocks.** Slightly outside buys travel back for a small
  cantilever, and the cube law makes small overhangs genuinely cheap - 20 mm costs about an eighth of
  what 40 mm does. A curve to slide along, not a hard constraint.
- **Wider is not purely better.** Clamp couple force goes as one over the separation, so spreading
  reduces load on plate and blocks - but that path is already stiff. **Plate bending is the softer
  thing, so alignment matters more than spread.**

### ✅ Left-right alignment is settled, and it lands well

Measured: **clamp bolt holes 100 mm apart**, **spacer centrelines 115 mm apart**. So each clamp bolt
sits at ±50 mm from the plate centre, **7.5 mm inboard of its spacer's centreline** - over the
spacer, and therefore over the bearing block.

✅ **The ±16 mm is measured, 2026-09-30** - the block hole pattern is **32 × 36 mm**. So the M5 columns
fall at **41.5 and 73.5 mm** from the plate centre, and **the clamp bolt at 50 mm is bracketed between
them** rather than cantilevered outside. Load goes bolt → plate → spacer → block with the plate barely
working.

🔴 **But 8.5 mm of bracketing is also a clash.** The M8 at 50 and the M5 counterbore at 41.5 are close
enough that at equal height the two features *overlap* - which is what drives the clamp separation. See
the Z plate section above.

📌 **This is the left-right axis only.** Vertical alignment - clamp centres against block centres up
the rail - was the open one, and the only one that could cost travel.

✅ **It closed on 2026-09-30 costing nothing.** The procedure below was written expecting a trade, and
it resolved to the no-trade corner: the Ø80 body is 199 mm, two 55 mm clamps need only 154 mm of
extent to match the **butted** block run, so step 3's spread is **zero** and step 5's re-cut does not
happen. Full **246 mm** travel, zero overhang, 6" spacers as built. See the Z plate section above.

**The ordering is kept because it is the method, not the answer** - a different spindle or a different
clamp puts the trade back on the table:

1. **Set the Z travel floor first** and treat it as hard - material thickness plus tool length plus
   clearance over workholding. 🔴 **This is the one that gets quietly eroded** while optimising the
   other end, and it is the one noticed every day.
2. **Measure the spindle's usable body length** → that sets clamp separation.
3. **Spread the blocks until the supported span covers the clamps.** Aim for **zero overhang**, not
   one inch - the cube law makes an inch cheap, not free.
4. **Check the remaining travel against step 1.**
5. **Cut spacers to suit** (8" rather than 6", if spread that far).

⚠️ **Step 1 is still open.** The travel floor was never set as a number, and 246 mm is now confirmed
available - so the question is no longer "how much can we get" but "where does the 246 sit relative to
the spoilboard". That is a machine measurement, not a design decision.

## Which half moves - settled

| Fixed | Moving |
|---|---|
| **X carriage plate** (the blue one), bolted to the X-axis bearing blocks | Z bearing blocks |
| HGR20 rails, mounted on it | spacer blocks, **16.41 mm measured** |
| 1605 screw, BK12 + motor, BF12 | ball nut housing |
| | **Z plate** - **154 W × 175 H × 1/2"** - bolted to both the spacers and the nut housing, carrying the spindle |

The motor stays put and only the carriage travels. The Z plate picks up **two** interfaces - the
spacer blocks and the ball nut housing - which is what makes the shim below matter.

**The blue is layout dye, not a finish.** The X carriage plate is plain 1/2" aluminium sprayed for
scribing; **30 holes** to lay out on it.

| X carriage plate | |
|---|---|
| Size | **154 mm W × 407 mm H × 1/2"** |
| Width | ✅ **154 mm, confirmed 2026-09-30** - the same width as the X gantry end plates. **The Z plate is 164** as of 2026-10-02 and no longer matches |

📌 **154 mm recurs across the X end plate and this one, and it is not a coincidence.** The X end
plate's 154 is set by **two HGH20 blocks butted - measured 154.18 on 2026-10-02**; this plate
inherits it.

🔴 **The Z plate broke away from 154 on 2026-10-02 and is now 164.** It had only ever inherited the
number, and at 154 eight of its M5 counterbores broke out of the plate edge. **Do not "tidy" it
back into line with these two** - see the Z plate section. Worth knowing
before anyone "tidies" one of them to a different number - changing it here changes what rides the Y
rails.

## ✅ The ball nut sits 1 mm below the spacer blocks - SKIM THE SPACERS, decided 2026-10-02

Measured: the spacer blocks stand **1 mm higher** than the ball nut housing, so the Z plate cannot
bear on both without something in between.

✅ **Decided: skim 1 mm off the spacer blocks. No shim.** The alternative was a full-face shim cut
to the housing footprint, and it is no longer needed.

🔴 **Face BOTH spacers in the same setup.** That is the whole reason this route wins: they come
out identical to whatever the machine holds, which is far better than their as-found **0.02 mm**
difference, **and it costs nothing extra because they are on the cutter anyway.** Two parts, one
setup, one depth.

❌ **Not washers**, in either scheme. The ball nut is the one joint here that must not be pulled out
of alignment: washers bear at four points, and as the bolts come down the housing tilts to whatever
those points dictate. That tilt becomes a side load on the screw - binding, uneven wear, and lost
motion that reads like backlash.

### ⚠️ The skim takes 1 mm out of the stack, and three recorded numbers move with it

The spacer is part of the chain from the X carriage plate to the spindle, so removing 1 mm from it
removes 1 mm from everything downstream:

| | Before | After the skim |
|---|---|---|
| Spacer thickness | 16.41 / 16.43 measured | **~15.4, both identical** |
| Z rails + blocks + spacers | 46.5 | **~45.5** |
| Carriage plate face to spindle centreline | 109 | **~108** |
| X beam front face to spindle centreline | ~152 | **~151** |
| X beam neutral axis to spindle centreline | ~187 | **~186** |

📌 **None of it changes a conclusion** - it is half a percent on the gantry arm, and every
deflection figure in this repo is quoted to two significant figures at best. It is recorded so that
nobody later finds 108 on the machine and 109 in the file and goes looking for the error.

🔴 **Re-mic both spacers after facing and write the number here.** The ~15.4 above is
arithmetic, not a measurement, and this repo's rule is that the machine is the authority.

🔴 **This is a milling operation, so it belongs on the one trip.** Facing 1 mm off a 2" bar is
not a drill-press job. **Take the ball nut housing with them** - the 1 mm is measured against that
part, and the whole point is that the faced spacers finish level with it.

⚠️ Measure the 1 mm again before cutting rather than assuming it is exactly 1.00. In the shim
scheme that mattered because stock comes in 0.5, 0.8 and 1.0; in the skim scheme it matters more,
because **the cut cannot be undone** and the spacers are a matched pair that would have to be
replaced together.

**Assembly order: rails and spacers first, nut housing last.** The rails define the geometry; the
nut should follow the screw rather than be forced into position by its own bolts. Leave its four
bolts finger-tight, run the carriage through full travel, then torque them.

## 🔴 Match the two spacers to each other before anything else

The spacers carry **no fasteners of their own** - they are compression members, clamped by the same
M5 that runs from the Z plate into the bearing block. Two consequences:

- **Their faces set the Z plate's plane relative to the rails.** A few hundredths of difference
  between the left and right spacer twists the plate and preloads all four bearing blocks against
  each other permanently.

  ✅ **Checked 2026-10-02, and it passes: 16.41 and 16.43 - 0.02 mm apart.** Both are halves of a
  single bar, so the thickness is the as-supplied bar dimension on both, untouched; the cut set length
  only. 0.02 mm is at the scale this bullet warned about and also at the limit of caliper
  repeatability. ✅ **And it is about to be settled outright:** the ball nut skim faces both spacers in
  one setup, so they finish identical and this check becomes a before-the-cut record rather than a
  live concern. The pair sets the geometry.
- **They locate nothing.** A 6 mm hole on an M5 bolt is 0.5 mm of radial float per side, so the
  spacer sits wherever it is put. Geometry comes from the blocks and the plate, which is correct -
  just do not expect the spacer to square anything up.

## 🔴 The spacers are not 5/8" - measured 16.41 and 16.43 on 2026-10-02

| | Left | Right |
|---|---|---|
| **Length** | **150.5** | **151.6** |
| **Thickness** | **16.41** | **16.43** |

**5/8" is 15.875.** The bar is **0.54 mm thicker than the nominal this file called it** in six
places, which is far outside any normal rolling tolerance for 5/8" flat - so it is not a 5/8" bar
that came in heavy, it is a different bar. **The nominal is now gone from this file; use the
measured numbers.**

✅ **And the file already contained the right number under the wrong label.** The moment-arm stack
gives *"Z rails, bearing blocks and spacers = 46.5 mm"*, measured. The rail-and-block stack is 30, so
the spacer in that measurement was **16.4** - not 15.875, which would have made the stack 45.9.
**Two independent measurements agree; it is the 5/8" label that was wrong.** Nothing downstream of
the 46.5 moves, including the **109 mm** offset and the **~187 mm** gantry arm.

✅ **The 1 mm ball nut shim is unaffected** - it was measured on the real assembly ("the spacer
blocks stand 1 mm higher than the ball nut housing"), so it already reflects 16.41 rather than a
nominal.

✅ **Leave the lengths alone - 150.5 and 151.6 both do the job, and the 1.1 mm difference does not
matter.** The spacers carry no fasteners, locate nothing, and float 0.5 mm radially on their
clearance holes. The only thing length has to do is cover the M8 rows at **±70.5 mm**:

| | Half length | Covers ±70.5? |
|---|---|---|
| 150.5 | 75.25 | ✅ by 4.75 mm |
| 151.6 | 75.8 | ✅ by 5.3 mm |

❌ **Do not cut them to match each other.** Matching matters in **thickness**, which sets the Z
plate's plane, and that already passes at 0.02 mm apart. Length matching buys nothing and a re-cut
risks the one property that does matter.

## ❌ Do not lengthen the spacers - the question is closed twice over

Raised repeatedly on 2026-09-30, while the plate was provisionally 205 mm and the clamps overhung the
block run. **Both reasons to reject it still stand, and the second one ended the discussion:**

**1. An unbolted spacer end is a one-way support, not a stiffener.** The spacers carry no fasteners of
their own - they are clamped only by the M5 that runs from the plate into the bearing block, and past
the block ends there is nothing to bolt into and nothing behind them. The extra length would be
**unclamped bar in face contact with the plate**: it can push but not pull, so it stiffens in
**compression only** - one direction of the tipping couple and not the other. An unpreloaded one-way
contact opens and closes on every direction change, which is a hysteresis source, not a stiffener.

**2. 🔴 It was aimed at a problem that no longer exists.** At the settled **116 mm** clamp centres,
all four M8 rows sit at **±70.5 mm**, inside the **±76.2 mm** of the existing 6" spacers. **There is no
overhang left to support.**

📌 **And it never addressed the real constraint anyway.** The binding problem turned out to be the M8
tapped holes clashing with the M5 counterbores - two features **in the plate**. Spacer length has no
bearing on that, and the M5 positions are set by the blocks and cannot move.

📌 **Keeping them also keeps the matched pair.** Both are halves of one 12" bar with the thickness
as supplied - **measured 16.41 and 16.43**, see above. A re-cut only preserves that if both new
pieces come from a single bar.

📌 **It is also solving a problem that is not there.** The clamp bolts land inside the spacer run - see
the Z plate section above - so the overhanging plate is not carrying the load in the first place.
**Keep the 6" spacers as built.**

## Use M5 × 35, not M5 × 30

Through a counterbore in a 12.7 mm plate - leaving about 7.7 mm of material under a 5 mm head - plus
the spacer is roughly **24.1 mm of grip** at the measured 16.41. An M5 × 30 would leave only about
**5.9 mm in the bearing block**, 1.2 diameters, with no margin if a counterbore runs deep. An
M5 × 35 leaves about **10.9 mm**. The blocks have the thread depth for 35 mm.

📌 **This paragraph used to read 23.6 mm of grip and 6.4 mm left in the block, computed off a
nominal 15.875 spacer.** The real spacer is 16.41, so the margin was half a millimetre thinner than
stated all along - which does not change the decision, it strengthens it.

---

## ✅ The clamp mount geometry - settled 2026-09-30

- **Orientation.** The **100 mm dimension is front-to-back**, with the 80 mm bore centred
  in it leaving 10 mm of wall front and back; 55 mm is axial (vertical) and 120 mm wide, giving
  20 mm of wall either side of the bore. This follows from the "half of 100" term in the offset
  chain above and is consistent throughout.
- ✅ **Z plate thickness is 1/2" (12.7 mm)**, settled with the plate size.
- ✅ **The bolts run through the clamp into a TAPPED plate.** Measured: the **M8 × 80 stands 10 mm
  proud of the clamp's mounting face** when fully seated, so 70 mm is swallowed by the clamp. A
  12.7 mm plate cannot be through-bolted with that - the bolt never reaches the back face, so there
  is no nut - and there is nowhere for a nut to go anyway: the inner row has the spacer directly
  behind it and the outer row has open air.

### 🔴 Tap the plate, and torque to ~15 N·m - not 25

**10 mm of engagement is 1.25 diameters.** In 6061 that develops roughly **60% of an M8 8.8's proof
load** - call it 10 kN of preload per bolt, **40 kN per clamp**, against a clamp reaction on the order
of 2-3 kN at peak cutting load. Ten times the margin, so **the engagement is fine.**

⚠️ **What is not fine is torquing it like an M8 in steel.** The aluminium thread is the limit, not the
bolt. **~15 N·m**, not the ~25 N·m an M8 8.8 would otherwise take. If you would rather not have to
remember that, **four M8 helicoils per clamp position** takes it to full spec for the price of a tap.

### 🔴 The M8 tapped holes and the M5 counterbores share the plate's front face

**Both features are entered from the clamp side, so they compete for the same surface** - this is a
layout constraint, not just a depth one.

| | |
|---|---|
| M5 socket head counterbore | ~**Ø10** |
| M8 tapping drill / thread major | **6.8** / **8** |
| Bare non-overlap | (10 + 8)/2 = **9 mm** centre to centre |
| **Working minimum, with a web that survives the tap** | **12 mm centre to centre** |

📌 **Depth is in your favour and needs no separate check:** the M5 counterbore leaves ~7.7 mm of plate
under the head while the M8 taps 10 mm into 12.7 mm, so if they clear on the face they never meet.

✅ **Resolved 2026-09-30.** The M5 rows were measured and they *did* collide with the 144 mm layout, so
the clamp centres came in to **116 mm** and the M8 rows to **±45.5 and ±70.5**. Worst-case clearance is
**14.1 mm centre-to-centre**, about 5 mm of web. Full working in the Z plate section above.

---
