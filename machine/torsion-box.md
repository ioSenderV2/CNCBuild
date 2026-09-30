# The torsion box and its base

What the machine stands on. The box carries the two Y beams; the base carries the box on **three
points** and is also the pallet it travels on.

The box's *interface* to the Y beams - the laminated outer wall, the 61 mm curb and the bolt row -
is not here. It lives with the plate it belongs to, in
[`end-plates-risers-and-spindle.md`](end-plates-risers-and-spindle.md) under "How it lands on the
torsion box". Read that first; this file is everything below the top skin.

---

## The box

| | |
|---|---|
| Skins | **19 mm Baltic birch**, top and bottom |
| Grid | **19 mm strips, 100 mm high**, between the skins |
| Depth overall | **138 mm** (19 + 100 + 19) |
| Fill | **Sand in the cavities** - filled **last**, on site |
| Outer left and right walls | **Two 19 mm laminations, 38 mm total** - see the Y beam interface |

⚠️ **The grid spacing is not decided.** One constraint on it is already fixed: each post's tenon
rises into a cavity, so **a post must land mid-cell, between two ribs**, never under one.

---

## The three load-bearing points

**Front left corner, front right corner, and the middle of the back.** Each is an **86 mm square
cedar post** (4×4).

Three points, not four, and the reason is the whole argument: a three-point mount is statically
determinate, so **the box cannot be racked by a twisted floor or a twisted base**. That matters
because the property being protected is the two Y beams staying **coplanar**, which is what the X
gantry rides on and what the entire riser exercise existed to guarantee.

The three-point mount is between **box and base** - not between base and floor. So the base should be
made as rigid as possible; stiffening it costs the mount nothing and the box is isolated from its
twist either way.

### Tenon and ledge

Each post is reduced over its **top 118 mm** to form a tenon that passes up through a hole in the
bottom skin. The bottom skin lands on the shoulder, or **ledge**, that the reduction leaves behind.

The stack closes exactly:

| | |
|---|---|
| Ledge to top of post | 118 mm |
| Bottom skin resting on the ledge | 19 mm |
| Cavity above it | 100 mm |
| **So the underside of the top skin is at** | **119 mm** |
| **Post top therefore stops** | **1 mm shy** |

That 1 mm is stable: 118 mm along the grain of a vertical cedar post moves essentially nothing
seasonally, so the gap will not close on its own.

### 🔴 Ledge depth follows the wall above it - and it is not 19 mm everywhere

The ledges are cut on the **outward-facing** faces on purpose, so that the **perimeter wall lands
directly over the shoulder**. The load then runs wall, skin, shoulder, post in a straight line with
no plate bending anywhere. Good intent, and it dictates the depth: **each ledge must be as deep as
the wall standing on it.**

The left and right outer walls are **two laminations, 38 mm**. A 19 mm ledge there would put the
tenon directly under that wall, leaving the wall with a hole where it needs to bear.

| Post | Face | Ledge depth | Wall above it |
|---|---|---|---|
| Front left / front right | The **side** face (left or right) | **38 mm** | Laminated outer wall, 38 mm |
| Front left / front right | The **front** face | 19 mm | Single-thickness perimeter |
| Back centre | The **back** face | 19 mm | Single-thickness perimeter |

So the **front corner tenons are 48 × 67**, and the holes in the bottom skin with them - *not* 67
square. The back centre post is unaffected: tenon **86 × 67**, hole to match.

Two side effects of the deeper corner ledge, both welcome: the corner shoulder area rises to about
**4180 mm²**, and each corner tenon ends up snug against both perimeter walls, so it is **laterally
located by the walls themselves**.

⚠️ This assumes the **front and back** perimeter members are single 19 mm. If either is doubled, the
same correction applies there.

### Bearing, and the one single-sided shoulder

| Post | Shoulder area | Note |
|---|---|---|
| Front corners | ~4180 mm² | Wraps two faces |
| Back centre | **~1634 mm²** (19 × 86) | **Single-sided**, centroid ~33 mm off the post axis |

Both are far inside cedar loaded **parallel to the grain** - the ledge is a cross-cut, so the plywood
bears on end grain in the post's strong direction. The back post carries a small permanent moment
from its off-axis bearing. Harmless, but if the eccentricity is ever disliked, ledging the **front and
back** faces instead gives symmetric bearing and double the area, at the cost of the
wall-over-shoulder alignment on the front side.

⚠️ **Cut each hole to its own post.** 86 mm is the working figure; S4S 4×4 is commonly 88.9 mm, and
cedar varies between sticks. Measure the three you have.

---

## Why the box is not fastened to the posts

**Gravity and 99 mm of tenon engagement, and nothing else.** Checked rather than assumed:

- Weight is in the hundreds of pounds; the largest horizontal the machine can generate is gantry
  acceleration, on the order of tens of newtons.
- That has to overcome friction on three large end-grain bearings **and** shear a 99 mm tenon.
- The CG stays well inside the support triangle at both ends of Y travel, so no post ever unloads.

Nothing in operation lifts or shifts the box. **No fastener is needed for what the machine does.**

### The exception is transport, and the decision has a deadline

Two cases can separate box from post, and neither happens in the shop:

1. **Road shock.** Freight is conventionally designed for vertical accelerations above 1 g - a design
   convention, not a measurement of any particular route. Above 1 g the box momentarily unloads, and a
   gravity-only joint can lift and re-seat.
2. **Being picked up by the wrong part.** Slings or forks under the *box* instead of under the frame,
   and the three posts hang from their tenons.

**One screw driven at an angle into the side of each tenon, from inside the cavity, covers both.** It
must be done **before the top skin is glued**, because after that there is no access to those tenons
ever again. Not a vertical bolt down through the shoulder - that is withdrawal from cedar end grain,
the weakest direction available.

The screws are **backup, not the plan**. The restraint that should actually be relied on is a strap
over the box down to the base frame - see Transport.

---

## The base

The base locates the three posts, stiffens them against each other, and is the pallet.

| Member | What it does |
|---|---|
| **2x6 bottom frame** | Locates the posts. **5/16" bolts** through post and frame |
| Clearance beneath it | High enough for a **pallet jack to enter and lift** |
| **2x4 top frame** | Ties the post tops together and is the top chord the shear walls fasten to. Sits **just shy of the bottom of the box** |
| **Shear walls** | Plywood cabinet carcases, standing on the bottom frame and reaching the top frame |

**Two bolts minimum per post-to-frame joint.** A single bolt lets the post rotate about it, and a post
that rotates lets its tenon walk in the skin hole.

### 🔴 The 2x4 top frame must never touch the box

"Just shy" is the load-bearing phrase in the whole design. The moment that frame touches, there is a
fourth and fifth contact point, **the mount is no longer three-point, and the failure is completely
silent** - no noise, no visible change, nothing but the Y beams drifting out of coplanar.

- **The clearance must exceed the box's own sag** between its three points under full sand load. That
  deflection has not been computed - it needs the grid spacing and the sand mass. Until it is,
  **10 mm or more**, not 1 mm.
- **Keep the gap inspectable.** A feeler or a strip of paper should slide between box and frame at
  several points, years from now. If the carcases make that impossible, the ability to check the one
  thing that fails silently has been designed out.

A near-touching frame would also be a useful **transport catch**, limiting how far the box can move.
That is a real benefit and it is in direct conflict with the above. **Resolve it with removable
transport blocks** - packers set on the 2x4 frame for a move and taken out on arrival. Determinacy
wins in service because it costs accuracy every day; the catch matters on the two or three days the
machine ever moves.

### The shear walls

Three plywood cabinet carcases fill the void under the box:

| Carcase | Position | Openings | Attached to |
|---|---|---|---|
| Rear left | Back left corner | Facing **out** | Bottom frame, top frame, and **back panel to the back-centre post** |
| Rear right | Back right corner | Facing **out** | Same, mirrored |
| Front | Between the two front posts | Facing **out** | Both front posts; **back to the sides of the two rear carcases** |

This works better than it might appear. A carcase with one open face still contributes panels in
**both** vertical planes - its back plus its two sides - so front-back and left-right racking are both
resisted by each of the three. There is no direction gap.

🔴 **Edge fastening is what makes a shear wall a shear wall.** A panel transfers load only through its
perimeter connections: **glue plus screws at roughly 150 mm all the way round** - to the bottom frame,
the top frame, the posts, and carcase-to-carcase where they meet. A carcase that merely sits in the
void with screws in its corners contributes close to nothing, **and looks identical to one that
works.**

⚠️ **The left and right sides are the least-stiffened perimeter.** The rear carcases cover the back and
the front carcase covers the front; the sides get only carcase ends. That is where to add a panel if
more is ever wanted - and it is also the least useful face for storage access, so it may be free.

---

## Transport

**The 2x6 frame is the pallet.** The jack lifts the frame directly; there is no separate pallet under
it. That makes the connection chain:

| Interface | How it is held |
|---|---|
| Frame to posts | **5/16" bolts** - positive |
| **Posts to box** | **Gravity and 99 mm of tenon** - the only non-positive joint in the stack |
| Carcases to frames and posts | Glued and screwed - positive |

So the tenon screws above are protecting the single interface in the entire assembly that nothing but
gravity holds. That is the argument for them, rather than "transport" in general.

- **Strap over the box, down to the 2x6 frame.** Two straps make box, posts and frame one object and
  neither separation case can happen. This is the restraint to rely on.
- **Put the fork positions under or very near the three posts.** The 2x6 frame is now a structural
  lifting member in bending between the tines, and a post landing mid-span between forks is the case
  to avoid. Add a cross member where the forks land if the layout does not cooperate.
- **The CG is high** - box, 305 mm risers, beams, gantry, spindle. On a jack on a tilting lift gate,
  **tipping is the hazard, not weight.** Long axis fore-aft, strapped.
- **Mass is a design budget only** - somewhere under half a ton, enough to size a jack and a gate.
  The assembly gets **weighed on a weighing pallet jack** when it is built; that is the only figure
  worth quoting, and it belongs in [`../commissioning/`](../commissioning/).

### Drain ports - and why they cannot go in the bottom skin

Dumping the sand is the single biggest lever on a move: roughly **165 lb that never gets carried**,
turning a ~240 lb box into ~73 lb. But with the 2x4 frame just under the box and three carcases
filling the void, **the bottom skin is unreachable** - bottom ports would need a carcase pulled out to
use.

- **Put the ports low in the front and back perimeter walls instead.** Still gravity-drains into a
  bucket, and reachable for the life of the machine.
- ⚠️ **Keep them out of the laminated left and right walls.** Those are the 38 mm shear webs the Y beam
  plates bolt to; a 2 inch hole through one is a hole in the load path.
- 🔴 **A rib grid makes closed cells, and each cell traps its own sand.** Either a port per cell, or
  **notch the ribs at the bottom** so sand can migrate to a few ports. The notches cost a little glue
  line to the bottom skin and nothing else.

Same deadline as everything else on this page: before the box is closed.

---

## ⚠️ Open items

- **The grid spacing**, subject to each post landing mid-cell between two ribs.
- **The box's deflection between the three points** under full sand load. This sets the minimum 2x4
  clearance above, and it needs the grid spacing and the sand mass first. **The one number on this page
  that a wrong guess would quietly cost accuracy for.**
- **The exact box width** - measured off the fully assembled CNC on a flat surface, not designed. See
  the Y beam interface.
- **Where the stabiliser legs go.** The project notes carry "three points plus a fifth leg". With a
  post at the **middle** of the back, the support triangle has **zero width at the rear**; tipping is
  fine either way the gantry travels, but there is little to resist a side load at the back corner.
  Whatever those legs are, they must be set **deliberately short** - if they carry load, it is no
  longer a three-point mount.
- **Whether the front and back perimeter members are single 19 mm**, which the ledge depths above
  assume.
