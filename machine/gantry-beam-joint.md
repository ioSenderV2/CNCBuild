# The gantry beam, and how the two extrusions are joined

**Settled 2026-09-29.** Every beam on the machine - X, Y1 and Y2 - is **two 8020 `30-6060` profiles
stacked**, 60 mm wide by 120 mm tall, 1000 mm long. This file records how they are tied together, why the obvious methods do
not work on this profile, and which numbers are measured versus estimated.

Photographs of the parts are in [`photos/`](photos/); the 8020 cross-section drawing is in
[`../manufacturer-assets/`](../manufacturer-assets/), untracked.

The repo's standing rule applies throughout: anything below marked **measured** came off the parts on
the bench. Anything marked **estimate** is arithmetic and is labelled as such, because it will
otherwise get quoted later as though it had been measured.

---

## The decision

**No holes are drilled in the extrusion. Nothing is tapped.** The two profiles are joined by bolt-on
aluminium plates running the full 1000 mm, anchored with M8 T-nuts in the existing slots.

| | Back plate | Front plate |
|---|---|---|
| Width | **120 mm** — full section height, all four back slots | **46 mm** — the two slots flanking the seam |
| Thickness | **1/4" (6.35 mm) on X**; on **Y** see the reversal below | **1/4" (6.35 mm), all three beams** |
| Material | **6061 on X**; **1/8" steel on Y** | **6061, all three beams** |
| Fasteners | M8 T-nuts, **150 mm** spacing, four rows | M8 **flange** bolts, two rows, no counterbore |
| Also carries | drag chain — bolts pass **through** the plate into T-nuts in the outer slots | the **magnetic encoder tape**, all three beams |

The plates' job is **shear connection and flange area, not modulus.**

### 🔴 The steel rejection was reversed on 2026-10-02, for Y only

This file used to read:

> **Material is aluminium, not steel.** Steel would give roughly three times the modulus, but over
> 1000 mm a shop temperature swing puts a couple of tenths of differential expansion into a joint
> held by preloaded T-nuts that cannot comfortably slip. Matched aluminium removes the question.

**It still holds on X, and X stays 6061.** On Y it has been overridden — and the override is not a
refutation. **The cost is accepted instead of avoided.** The full reasoning sits with the part that
took the decision over, in
[`end-plates-risers-and-spindle.md`](end-plates-risers-and-spindle.md) under "The full-height
outboard plate". In short:

- On Y there **is no separate 120 mm back plate any more.** The full-height outboard plate, running
  from the beam down to the torsion box, *is* the back joining plate — grown, not added alongside.
- The differential is **0.17 mm over a metre at 15 K**. The paragraph above had the magnitude right
  at "a couple of tenths"; none of its arithmetic was wrong.
- **1/8" was chosen over 1/4" specifically to halve it**, the restraint force scaling with E·A.
- At 1/8" steel presents **9.2 mm of equivalent aluminium** at the face — almost exactly the 3/8"
  this file asked for on Y. The flange term is satisfied, not overshot.

⚠️ **This is the one joint where the thermal question is live rather than dismissed.** The
plate-to-box bolt row takes up its own differential in 9 mm clearance because those bolts are
retention, not load path. **These T-nuts are a preloaded friction joint doing shear transfer** —
a different duty, and the two must not be waved through together because their numbers happen to
be similar.

❌ ~~**Buy 120 mm stock and rip the 46 mm front strips from it** — one thickness, one order.~~
**Retired 2026-10-02.** Y's back is steel, so there is no 120 mm aluminium order to rip from. The
three 46 mm × 1/4" 6061 strips need their own buy.

### Why the thicknesses differ

The Y beams **do not move** (measured: their end plates bolt to the torsion box), so weight there is
static load and the stiffer plate is free. The X gantry moves, so its ~3 lb saving is real.

📌 **The Y front strip came down to 1/4" on 2026-10-02**, breaking the old "same as its back plate"
rule. All three beams now carry an identical **46 mm × 1/4" 6061** strip, which is also the magnetic
tape surface — one part made three times, instead of two specifications.

---

## Why joining them matters at all

Two reasons, and the second is the one that decided the design.

1. **Composite bending.** Two 60 mm beams free to slide on each other are far less stiff than one
   120 mm-deep beam, because the second moment of area goes as depth cubed.

2. **The rail couple crosses the seam.** One HGR20 rail is on the front face of each profile
   (measured), so the upper rail sits on the upper extrusion and the lower rail on the lower one. The
   spindle hangs forward of the beam, and that forward offset turns cutting force into a moment
   reacted as a couple between the two rails — upper pulled one way, lower pushed the other.
   **That couple is carried straight across the interface as shear.** With nothing joining the
   profiles, each takes its half and bends independently in the direction the cutting load acts.
   ([photo](photos/gantry-stack-rails-front.jpg))

So the joint is in the primary load path, not a refinement.

---

## What the plates buy

Computed from 8020's **published** section properties (below), not estimated. Plate and extrusion
are both aluminium at ~68.9 GPa, so no transformed-section correction is needed.

⚠️ **That last sentence stopped being true for Y on 2026-10-02.** The Y back plate is steel, so the
table below reads correctly for **X only** as written. For Y, use the transformed area: 3.175 mm of
steel at the face behaves as **9.2 mm of aluminium**, so the **3/8" row is the Y row** — about
**+241% fore-aft**. The flange band that counts is only the 120 mm alongside the section; the rest
of the 12" plate is web carrying load down to the box and contributes nothing to composite bending.

Fore-aft bending stiffness — bending about the vertical axis, the direction the spindle deflects
under cutting load — against the bare stacked pair:

| Configuration | Fore-aft | Vertical | Added weight per axis |
|---|---|---|---|
| Back 60 × 10 only | +77 % | | — |
| Back 120 × 10 only | +124 % | | ~9 lb |
| Back 120 + front 46, **1/4"** | **+149 %** | +40 % | ~8.8 lb |
| Back 120 + front 46, 3/8" | +241 % | | ~11.9 lb |
| Back 120 + front 46, 10 mm | +256 % | +63 % | ~12.4 lb |

> **These replaced an earlier set of estimates, and every gain above is larger than was promised.**
> The assumed section properties were too *generous* — 1200 mm² against a real 929.9, and
> 5.5 × 10⁵ mm⁴ against a real 3.633 × 10⁵ — so the bare beam is **29 % smaller in area and 51 %
> lower in I** than credited, and each plate therefore carries a larger share. The same table
> previously read +54 / +90 / +99 / +161 / +171 %.
>
> **No decision changed.** The ordering of the options was unaffected, which is why deciding on the
> estimates was safe — and why the superseded figures are recorded here rather than quietly
> overwritten.

Two things fall out of this that are easy to get backwards:

- **On the back, width beats thickness.** The flange contribution scales with plate *area at the
  face*, and extra width also spans the section depth for vertical bending and widens the bolt
  pattern. Do not trade 120 mm wide for something narrower and thicker.
- **On the front, width beyond 46 mm buys nothing.** Past the block gap there is only 4.5 mm of
  height (measured), so any extra width would have to be rebated thin — about 14 % more area for a
  machining operation on a 1000 mm strip.

### 🔴 Fore-aft is the soft axis, and it is pure aspect ratio

**The section is 120 mm tall and 60 mm deep, so it is tall and narrow** - stiff in the direction
gravity and the spindle's tipping couple load it, and comparatively soft fore-aft. That is not a flaw,
it is the shape doing its job, but the asymmetry should be on the record because the percentages above
do not show it.

For a rectangle, I goes as width × depth³, so swapping axes swaps which dimension is cubed and the
stiffness ratio is simply **(height / width)²**:

| Configuration | Ix (vertical) | Iy (fore-aft) | Ratio |
|---|---|---|---|
| Two 6060s joined, no plates | 2.40 × 10⁶ | 7.27 × 10⁵ | **3.3×** |
| **+ back 120 and front 46, 1/4"** | **3.37 × 10⁶** | **~1.71 × 10⁶** | **2.0×** |

📌 **The plates halve the penalty, and that is their unadvertised second job.** They sit on the front
and back faces - the extreme fibres for *fore-aft* bending, which is exactly the direction short of
depth. They add ~40% to vertical and ~135% to fore-aft. (The section above gives +149% from the same
starting point; an independent recompute here gives +135%. Same conclusion, and neither is a measured
number.)

#### Indicative deflections, and keep these apart from the dead-load figure

⚠️ **A number already in this repo is a DEAD-LOAD sag and has been misread as a cutting deflection** -
the **0.022 mm** quoted in `end-plates-risers-and-spindle.md` is the gantry's own share of weight, not
a response to cutting force. Under the **1000 N structural envelope**, mid-span, ~900 mm free span,
end-supported:

| | Vertical | Fore-aft |
|---|---|---|
| At 1000 N | ~0.065 mm | **~0.13 mm** |
| At a more realistic 300 N component | ~0.020 mm | ~0.039 mm |

**Estimates, not measurements** - a point load at mid-span on a simply supported beam is a crude model
of a gantry on four bearing blocks, and 900 mm is an assumed free span. They are recorded for *ratio*
and *order of magnitude*, which is what they are good for. 0.13 mm sounds alarming until you note it is
the full crash-case envelope; the steady-cutting number is four times smaller.

### ❌ A single 40×120 (40 Series) was compared and rejected, 2026-10-01

Raised because the stacked pair is a built-up section and a one-piece 40×120 looks like it should beat
it. **It wins on two counts and loses decisively on the one that matters.**

8020 published properties for the 40×120: **Ix 306.32 cm⁴, Iy 36.80 cm⁴**, area 21.927 cm²,
0.3314 lb/in, 6063-T6, **4.32 mm wall**.

| | 2 × 6060 + both plates | 40×120 + back plate |
|---|---|---|
| Ix vertical | 3.37 × 10⁶ | 3.98 × 10⁶ (**+18%**) |
| **Iy fore-aft** | ~1.71 × 10⁶ | **~6.8 × 10⁵ (−60%)** |
| Weight, lb/in | 0.447 | 0.446 |
| J torsion, Bredt estimate | ~1.27 × 10⁶ ideal, ~9.6 × 10⁵ realistic | ~1.24 × 10⁶ |
| Max rail spacing | **90 mm** | 80 mm |

**What it would have bought:** 18% more vertical stiffness at identical weight, a 4.32 mm wall against
2.21, a genuine one-piece closed section worth perhaps 30% in torsion over a bolted approximation of
one, and it would have deleted the entire joint - 42 T-nuts per beam, the slide-in trap, the
clamp-share problem and the two dead schemes below.

🔴 **Why it lost: its aspect ratio is 3:1, so it starts at 8.3× (published, Ix/Iy = 306.3/36.8 - which
independently confirms the (h/b)² reasoning above) and a single back plate on a 40 mm-deep core has
too short a lever to pull it back.** Fore-aft deflection goes from ~0.13 mm to ~0.32 mm. Adding a front
strip in its middle slot was checked too and still lands at 53% of the current section's fore-aft
stiffness - **the 20 mm of extra core depth cannot be bought back with bolted plate.**

📌 **Secondary:** its slot centrelines are at 20 / 60 / 100, so **80 mm** is the widest rail spacing
available, against the **90 mm** actually used here. That is ~21% less carriage pitch stiffness and 12%
more force per rail reacting the spindle's forward moment.

📌 **The X beam was NOT built when this was raised** - only the rails were in the slots, loose. So the
decision was made on the engineering, not on sunk cost. **Recorded so it is not re-litigated.**

### Is the beam even the bottleneck?

Probably not, and that is why 1/4" was chosen on X. The riser plates are the obvious suspect. On the
X gantry the end plates are 1/2"; on the Y beams there is a **proposed** full-height outboard plate
that would remove the concern entirely - **proposed, not decided, nothing ordered**. See
[`end-plates-risers-and-spindle.md`](end-plates-risers-and-spindle.md).

🔴 **The percentages above are stiffness ratios and are force-independent, but any absolute
deflection quoted in this repo at 250 N is two to four times optimistic** - that was a router
figure, and this machine takes 500-1000 N as its structural envelope. The force table is in
that same file.

**The X plate choice is settled but testable.** Once the Z assembly exists, push on the spindle nose
with a known force and indicate it. The plate is bolt-on precisely so that swap stays cheap.

📋 **The procedure is written up:
[`../commissioning/stiffness-test.md`](../commissioning/stiffness-test.md)** - every indicator
position, which way its stem points, and the subtraction that turns the readings into per-subassembly
contributions. **Do not improvise this at the machine**; a single reading on the nose gives a total,
and a total cannot say *where* the compliance is, which is the only thing being asked.

---

## Measured values

Taken off the parts on the bench, 2026-09-29. These outrank anything derived.

| | |
|---|---|
| Profile | 8020 `30-6060`, two stacked, **1000 mm** |
| **Rail spacing, X** | ✅ **90 mm** - confirmed by the user 2026-10-01. The outermost of the four front slots, at 15 and 105 mm up the section. This is the widest the profile offers and it is what was used |
| Clear gap between bearing blocks, front face | **46.7 mm** - [trial fit](photos/front-plate-trial-flange-bolts.jpg) |
| Bearing block top, above extrusion face | **30 mm** |
| Clearance under the block overhang | **4.5 mm** |
| M8 flange head | **17.3 mm** diameter, **5 mm** high |
| Rails | HGR20, **17 × M5 at 60 mm** into T-nuts, one rail per profile, front face |
| Ball screw | 1605, BK12 / BF12 supports, M5 into the end plates |
| Support block offset from extrusion face | **5 mm**, giving a **12 mm** gap under the ball nut |
| Y axis assembly mass | **37 lb** each |

**Ball screw side:** X carries its screw **on top**, to preserve vertical milling height. Both Y
beams carry theirs **underneath**, because the top of Y1 must stay clear for the X stepper.

### The observation that decided everything

🔴 **At the centre of the face there is nothing behind the 2.21 mm skin. It is void.** 2.21 mm is
the thickest section anywhere in the profile.

This was checked by eye down the end of a real extrusion, and it **overrode a reading of the 8020
drawing** that had inferred a solid rib there. It is the single fact that killed two otherwise
plausible schemes below. The drawing does not make it obvious; the part does.

See [`photos/gantry-stack-end-view-bk12.jpg`](photos/gantry-stack-end-view-bk12.jpg) - the clearest
view of the voids, and of the corner bores running lengthwise.

### From 8020 — catalog, not measured

**Section, from the dimensioned drawing:** `60.00` overall · `30.00` module · `15.00` slot
centreline from each edge · **`8.14` slot opening** · `16.51` slot channel · `4.20` lip ·
**`2.21` wall** · **ø`6.65` corner bores** · `27.62` central cavity diagonal.

**Published properties**, from the 8020 product page for `30-6060`:

| | |
|---|---|
| Moment of inertia | **Ix = Iy = 36.3307 cm⁴** (3.633 × 10⁵ mm⁴) |
| Cross-sectional area | **9.299 cm²** (929.9 mm²) — their page labels this "Surface Area" |
| Alloy | **6063-T6**, clear anodised |
| Yield strength | **172.37 N/mm²** |
| Modulus of elasticity | **68 947.6 N/mm²** (68.9 GPa) |
| Weight | **0.1441 lb per inch** (~5.67 lb per metre, per profile) |
| Max stock length | 238.19 in (6050 mm) |

The area and the weight-per-inch agree to about 2 % on aluminium density, which cross-checks both
and confirms the mislabelled "Surface Area" field is really cross-sectional area.

🔴 **The alloy is 6063-T6, not 6105-T5.** This repo carried 6105-T5 for a while as an unverified
recollection. 6063-T6 yields at 172 MPa, **softer than what was assumed** while the tapping schemes
below were being argued. It changes no decision — every scheme that depended on aluminium thread
strength was already dead — but it makes those kills more firmly right, not less.

The corner bores **run lengthwise**, parallel to the 1000 mm axis. They are reachable only from the
ends. This is not obvious from an end-view photograph and is the reason a whole family of mid-span
bolting schemes does not exist.

---

## The fasteners

**8020 `13025` T-nut**, published spec:

| | |
|---|---|
| Thread | **M8 × 1.25** |
| Body | **16.00 × 16.00 mm** (A × B) |
| Boss height | **7.80 mm** (E) |
| Thickness | **6.00 mm** (F) |
| Step | 1.80 mm (D) |
| Material | **Steel, grade 1045**, bright zinc |
| Fits | 15 / 30 / 40 Series |
| Weight | 0.015 — *unit unstated on the page* |

### Why the slot lips are the limit, not the thread

M8 in 6 mm of 1045 steel will carry more than an M8 bolt can deliver. **The joint's capacity is set
entirely by the 6063-T6 slot lips** bearing on the nut's shoulders — roughly 4.1 mm of shoulder each
side over the nut's 16 mm length.

### Fit against the slot

| | T-nut | Slot | Clearance |
|---|---|---|---|
| Body width (A) | 16.00 | 16.51 channel | 0.51 mm total |
| Boss (E) | 7.80 | 8.14 mouth | 0.34 mm total |
| Thickness (F) | **6.00** | 8.14 mouth | **2.14 mm spare** |

### 🔴 It is a slide-in nut. Load them before the end plates go on

The `13025` **slides in from the end of the slot**. It does not roll in, and that is a deliberate
choice rather than a limitation - roll-in nuts cost more and are weaker.

**So every T-nut has to be in the slot before anything closes the ends.** Once the end plates are
bolted on, the only way to add one is to take the beam apart.

| | Slots | Per slot | Per beam |
|---|---|---|---|
| Back plate | 4 (full section height) | 7 | 28 |
| Front plate | 2 (flanking the seam) | 7 | **14** |
| | | | **42 total** |

Seven per slot is 150 mm spacing over 1000 mm - first at 50 mm, then every 150.

**All three beams - X, Y1 and Y2 - are stacked pairs**, so that is **126 T-nuts for the machine**.

⚠️ **The front plate is the one that gets forgotten.** Its two slots are easy to overlook while
counting out the back, and they are just as closed once the end plates are on.

**Test it with one nut before planning the build sequence.** Do not take the drawing's word for it —
reading a drawing rather than the part is exactly what produced the two dead schemes below.

### No load rating is published, and that is accepted

**The `13025` product page carries no pull-out figure, no slip figure and no recommended torque.**
The joint has large margin on every estimate made here, and the owner's call is that the T-nuts are
not a concern - so this is recorded as a known gap rather than carried as an open question. If a
number is ever actually needed it has to come from 8020 directly; the search has already been done
and the page does not have it.

---

## Assembling the stack

### The rails are aligned, not located

HGR20 mounting holes are **ø6 through with a ø9.5 counterbore, taking an M5 socket head** - mounted
here with **M5 × 16 into T-nuts**. An M6 shank would pass the 6 mm hole but its 10 mm head will not
enter a 9.5 mm counterbore, so M5 is correct and matches the rail spec.

**That 1 mm of float is deliberate.** The hole is a clearance hole so the rail can be *aligned*
rather than located, and the T-slot adds more float still. Tighten 17 bolts with the rail floating
freely and it is straight nowhere in particular - it snakes. **Every bolt must be biased the same
way while it is tightened.**

### 🔴 Bias both rails the same direction, not outward from each other

The four bearing blocks are locked together by the carriage plate, so what the assembly actually
cares about is that **rail-to-rail spacing stays constant** along the metre.

| Bias | Consequence |
|---|---|
| **Common mode** - both rails pulled the same way | The carriage follows the wander. A small position error, no fight. **Do this.** |
| **Differential** - rails pulled apart or together | The *spacing* varies, so the blocks are forced apart and together as the carriage travels. Preload variation and binding - the mode that shortens block life. |

Hand pressure repeats to a tenth or two. Common-mode that is harmless; differential it is not.

📌 **As built 2026-09-29:** the X beam rails were mounted with an **opposed** bias - lower rail pulled
toward the lower edge, upper rail toward the upper edge - each bolt biased consistently, which is far
better than random, but in the direction that varies spacing. Recorded as-built rather than as a
fault: **verify by feel before redoing 34 bolts** (see below).

### Rail parallelism is set twice, and the second time is at the joint

The two rails sit on **two separate extrusions**. Nothing indexes one profile to the other - the
T-slots let them shift, and the joining plates lock in whatever they are bolted at. So parallelism is
not settled when the rails are mounted; it is settled again when the stack goes together.

- **Both front faces must end up flush**, or the rails are not coplanar and the carriage plate twists
  all four blocks.
- **Assemble against a flat reference** - stack front-face-down on a known-flat surface, or clamp a
  straightedge across both front faces, before the joining plate bolts come up tight.

This is the moment the rail geometry is actually decided.

### How to know whether any of it matters

Do not redo bolts on suspicion. **Mount the four blocks to the carriage plate and slide the whole
assembly the length of the beam by hand.** Tight spots are obvious by feel. For a number, put an
indicator on the plate against a straightedge and sweep it.

Smooth and even means done. A binding zone tells you roughly where, and only those bolts need
revisiting.

---

## Schemes that were tried and killed

Recorded because each looked right for a while, and without the reasons written down the next
session will re-derive them and travel the same distance before hitting the same wall.

### ❌ Mid-span through-bolts tapped into the two touching walls

Bolt up from below, tapping M8 through the lower profile's top wall plus the upper profile's bottom
wall — 4.42 mm of engagement.

**Died three times over.** First, it gives only about **3.5 threads of M8 in aluminium**, forcing a
torque limit near a third of a normal M8. Second — and this is the non-obvious part — take a free
body of the upper extrusion: the only forces on it are the thread reaction pulling down and the
contact push from the lower profile. **The interface clamp equals only the share of bolt tension
carried by the upper wall's threads**, roughly a third, since the first threads engaged take most of
the load. The other two thirds merely squeezes the lower profile. Flipping the bolt end-for-end just
swaps which wall gets the good threads. Third and fatally: there is no material behind the centre
land to react even that.

### ❌ Through-bolt the full 120 mm with a nut on top

The fix for the clamp-share problem: 9 mm clearance through all four walls, plain steel nut and
washer on the top face, so 100 % of preload becomes interface clamp and nothing can strip.

**Died on the void.** Preload has to react against something. Head and nut both bear on a 2.21 mm
skin spanning roughly 22 mm unsupported, with a 9 mm hole through the middle. The only stiff vertical
structure is the four bosses — which run lengthwise and cannot be reached transversely. The skin
yields long before a useful M8 preload is reached.

The 12 mm clearance under the ball nut would have accommodated a nut and washer, and 140 mm bolts cut
to ~135 mm were specified. None of that was the problem.

### ❌ T-nut in the mating slot, reached by a bolt from below

Slide an M8 T-nut into the upper profile's bottom slot and bolt up into it, giving a steel thread and
full clamp with no tapping.

**Died on geometry: a 9 mm drill will not pass through an 8.14 mm slot mouth.** The bolt would have
to enter the bottom face exactly on a slot centreline, where there is no material to drill and no
room for the drill body.

### ❌ M8 rivnut in the slot floor

**Died on access, not width.** The body would fit the 16.51 mm channel, but it cannot be got in
through the 8.14 mm mouth and a setting tool cannot reach it.

### ❌ Replacing the rail T-nuts with tapped holes

Considered, then rejected. **The rail bolts are loaded mainly in tension**, not shear — the spindle's
forward offset pulls the upper carriage blocks away from the face. A T-nut bears on the slot lips,
which is a positive mechanical engagement over a large area and exactly what the slot is designed
for. Tapping the 2.21 mm slot floor for M5 would give about **two threads** carrying that tension.

**The existing T-nut mounting is the stronger arrangement. Leave the rails alone**; thread-locker on
the M5s if insurance against creep is wanted.

---

## ⚠️ Open items

- **Riser plate orientation**, which governs whether the 64× weak-axis concern applies as written.
  Unverified, and it decides whether the X plate thickness is worth revisiting.
