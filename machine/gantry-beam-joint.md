# The gantry beam, and how the two extrusions are joined

**Settled 2026-09-29.** Each gantry beam is **two 8020 `30-6060` profiles stacked**, 60 mm wide by
120 mm tall, 1000 mm long. This file records how they are tied together, why the obvious methods do
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

⚠️ **All percentages below are estimates**, computed assuming roughly 1200 mm² area and
5.5 × 10⁵ mm⁴ per profile. **8020 publishes the real area and Ix/Iy — fetch them and redo this
table.** The ratios between the rows are more trustworthy than the absolute figures.

Fore-aft bending stiffness, against the bare stacked pair:

| Configuration | Fore-aft | Added weight per axis |
|---|---|---|
| Back 60 × 10 only | +54 % | — |
| Back 120 × 10 only | +90 % | ~9 lb |
| Back 120 + front 46, **1/4"** | **+99 %** | ~8.8 lb |
| Back 120 + front 46, 3/8" | +161 % | ~11.9 lb |
| Back 120 + front 46, 10 mm | +171 % | ~12.4 lb |

Fore-aft is the direction that matters: it is where the spindle deflects under cutting load.

Two things fall out of this that are easy to get backwards:

- **On the back, width beats thickness.** The flange contribution scales with plate *area at the
  face*, and extra width also spans the section depth for vertical bending and widens the bolt
  pattern. Do not trade 120 mm wide for something narrower and thicker.
- **On the front, width beyond 46 mm buys nothing.** Past the block gap there is only 4.5 mm of
  height (measured), so any extra width would have to be rebated thin — about 14 % more area for a
  machining operation on a 1000 mm strip.

### ⚠️ Open: is the beam even the bottleneck?

The riser plates are flagged elsewhere as far weaker along Y and wanting gussets. **If they dominate
the fore-aft compliance at the tool, the difference between these rows disappears into the noise.**
Gusset the risers first, measure, and only then decide whether the X plate wants to go thicker. The
plate is bolt-on precisely so that swap stays cheap.

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

### From the 8020 drawing — catalog, not measured

`60.00` overall · `30.00` module · `15.00` slot centreline from each edge · **`8.14` slot opening** ·
`16.51` slot channel · `4.20` lip · **`2.21` wall** · **ø`6.65` corner bores** · `27.62` central
cavity diagonal.

The corner bores **run lengthwise**, parallel to the 1000 mm axis. They are reachable only from the
ends. This is not obvious from an end-view photograph and is the reason a whole family of mid-span
bolting schemes does not exist.

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

- **8020 published section properties** — area and Ix/Iy for `30-6060`, to replace the estimates in
  the stiffness table. Also their **T-nut pull-out and shear ratings**, which set the real joint
  capacity. Both are catalog facts and should be committed, not estimated.
- **Alloy.** 6105-T5 is recalled, not verified. It sets the thread and lip strength figures.
- **Are the Y beams also stacked pairs?** The ball screw mounting arrangement was confirmed common to
  all three axes, but whether the Y beams are doubled 60×60 like X was never stated outright. Most of
  this file assumes they are.
- **Riser plate orientation**, which governs whether the 64× weak-axis concern applies as written.
  Unverified, and it decides whether the X plate thickness is worth revisiting.
