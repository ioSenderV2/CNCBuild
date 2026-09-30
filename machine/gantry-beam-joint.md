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
| Thickness | 3/8" (9.53 mm) or 10 mm on **Y**; **1/4" (6.35 mm) on X** | same as its back plate |
| Fasteners | M8 T-nuts, **150 mm** spacing, four rows | M8 **flange** bolts, two rows, no counterbore |
| Also carries | drag chain — bolts pass **through** the plate into T-nuts in the outer slots | — |

**Material is aluminium, not steel.** Steel would give roughly three times the modulus, but over
1000 mm a shop temperature swing puts a couple of tenths of differential expansion into a joint held
by preloaded T-nuts that cannot comfortably slip. Matched aluminium removes the question. The plates'
job is shear connection and flange area, not modulus.

**Buy 120 mm stock and rip the 46 mm front strips from it** — one thickness, one order.

### Why the thicknesses differ

The Y beams **do not move** (measured: their end plates bolt to the torsion box), so weight there is
static load and the stiffer plate is free. The X gantry moves, so its ~3 lb saving is real.

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

---

## Measured values

Taken off the parts on the bench, 2026-09-29. These outrank anything derived.

| | |
|---|---|
| Profile | 8020 `30-6060`, two stacked, **1000 mm** |
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
