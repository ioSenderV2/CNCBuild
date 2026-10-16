# The machine

The build itself: extrusions, rails, screws, plates, and the mechanical decisions with their reasons.
Measured values belong in [`../commissioning/`](../commissioning/).

## FLAG: Two documents, split by register - read this first

**[`assembly.md`](assembly.md) says what gets built. The thirteen chapters say why.** Keep them apart.
A page that carries both is arguing with itself while somebody is holding a drill, which is how one
unusable document came about in the first place.

| | Source | Printout | What belongs in it |
|---|---|---|---|
| **The build document** | [`assembly.md`](assembly.md) | `build-document.pdf`, ~18 pages | Parts, hardware, what bolts to what, in the order it is done. Imperative. No reasoning, no options weighed, no figure's history |
| **The design record** | the thirteen chapters below | `design-record.pdf`, ~102 pages | Why the machine is that shape. The schemes that were tried and killed, the figures that moved and when, every OPEN: and NOTE:. Reference, never worked from |

PROCEDURE: **`tools\make-pdf.ps1`** from the repo root builds both. `-Doc build` or `-Doc record` for one.
Both are derived and untracked: **if either disagrees with a `.md` file, the `.md` file wins.**

FLAG: **A new decision goes in a chapter, and then into `assembly.md` if it changes what gets built.**
Writing the reasoning into `assembly.md` is the failure this split exists to prevent.

| File | What is in it |
|---|---|
| [`loads-and-plate-thicknesses.md`](loads-and-plate-thicknesses.md) | **Read this first.** The cutting-force recalibration (500-1000 N, not 250) that **every deflection figure in this repo depends on**, the plate and riser thicknesses it sets, and the one measurement that would settle the 1/4" question |
| [`gantry-beam-joint.md`](gantry-beam-joint.md) | Why the beams are joined at all, why the plate thicknesses differ, and the aspect-ratio argument for the soft axis |
| [`box-stiffness.md`](box-stiffness.md) | Why **rib height beats thicker skins** - the closed-form comparison, and what each option costs in weight and sand |
| [`three-point-mount.md`](three-point-mount.md) | Why **three posts and not four**: statically determinate, so a twisted floor cannot rack the box and the Y beams stay coplanar |
| [`egg-crate.md`](egg-crate.md) | Why the grid is **continuous both ways with half-depth notches** rather than ribs-plus-blocking, and the two meanings of "blocking" |
| [`lateral-fix.md`](lateral-fix.md) | The lateral stiffness fix - **widening the riser in its own plane**, why width cubed beats a bolt-on outrigger |
| [`spindle-and-mount.md`](spindle-and-mount.md) | The Ø80 2.2 kW water-cooled spindle, its body dimensions, and why not 3 kW |
| [`stepper-sizing.md`](stepper-sizing.md) | **2.2 N·m NEMA 23 on X, Y1 and Y2, 1.5 on Z**, and why not 3.2 - thrust is a non-term on a 5 mm lead, and the real ceiling is whip |
| [`spoilboard.md`](spoilboard.md) | The spoilboard stack and **both ends of the Z envelope**: why a thinner stack loses cut depth, and why the X carriage does not move down |
| [`assembly.md`](assembly.md) | The build sequence and its **ordering constraints** - the things that must happen before the top skin is glued, which no registry symbol can hold |
| [`tramming.md`](tramming.md) | Roll by **shimming the shelf**, nod still open, and why the carriage plate joint is deliberately not adjustable |
| [`machining.md`](machining.md) | **One trip, so design ahead of the build.** One WCS origin per plate, one reference rail, and what mating hardware to take |
| [`open-items.md`](open-items.md) | Everything still unmeasured, grouped by where it came from |

## FLAG: The dimensional prose is archived

Six files moved to [`archive/`](archive/) on 2026-10-11: **torsion-box**,
**lateral-stiffness**, **x-gantry-end-plates**, **z-carriage**, **y-beam-support** and
**outboard-plate**. They were walkthroughs of dimension chains that
[`../dimensions/registry.toml`](../dimensions/registry.toml) now owns, and they kept drifting
against it.

**The failure that settled it:** a sole plate position was read out of `x-gantry-end-plates.md`
as −182.5 when the registry had moved it to −175 the week before. OPEN: **The prose audit cannot
catch that class of drift** - it looks for near misses, and a 7.5 mm error reads as a different
quantity, not a stale one. At a tolerance wide enough to see it, the report runs to 1,426 lines.

NOTE: **They are archived, not deleted.** One `git mv` brings any of them back. What was worth
keeping is in the four argument files above, whose numbers are **comparative** - they weigh
options rather than define parts, so they cannot go stale against the registry.

## Frame and motion

| | |
|---|---|
| Beams, all three axes | **Two 8020 `30-6060` stacked** — 60 mm wide × 120 mm tall, **1000 mm** long |
| Rails | **HGR20**, one per profile, 17 × M5 at 60 mm into T-nuts. **Y rails are on the beams' inside faces, facing each other.** X, Y1 and Y2 share one kit; **Z is a 400 mm kit from a different supplier** - do not quote one kit's dimension for the other |
| Bearing blocks | **77.09 mm** each, measured - two butted read **154.18 mm**, which is what sets the 154 mm plate width. Of that, only the **51.15 mm machined pad** bears; a butted pair spans **128.24 mm** of pad, and that is the real floor for any carriage plate |
| Ball screws | **1605**. **Every axis drives through a cast stepper frame** — X, Y1, Y2 and Z — carrying motor face, bearing housing and coupler in one part, which is what retired the M5 standoffs. BF12 stays at each far end. Y ball nuts run **inverted**, on a tongue off the bottom of the carriage plate, so their bolts are reachable at assembly |
| Ball screw position | **X on top** (preserves vertical milling height); **both Y underneath** (Y1's top must stay clear for the X stepper) |
| Y steppers | **At the BACK of the machine** — one cast frame carries motor face, bearing housing and coupler. FLAG: **this said FRONT until 2026-10-15**; the model has them at the back, hanging off the back edge, and the whole point of putting them there was to keep the cable runs off the front |
| Steppers | **2.2 N·m, NEMA 23, on X, Y1 and Y2; 1.5 N·m on Z** — all IG57 all-in-one closed-loop, so the spare 2.2 covers the three axes that do the work. Not 3.2: no thrust is needed and a higher-inductance motor in the same frame is worse above ~1200 rpm, which is where the rapids live. See [`stepper-sizing.md`](stepper-sizing.md) |
| Y beams | **Do not move** — their end plates bolt to the torsion box |
| Y axis assembly mass | **37 lb** each, before the joining plates |
| Spindle | **Ø80 mm, 2.2 kW water-cooled** with matching VFD, on two 80 mm clamps |
| Y beam support | **Front:** a tapered 100→200 mm × 302 mm × 1/2" plate per beam, with a 60.5 × 50 window for the stepper frame. **Rear:** one **12" × 1/4" A36 steel** plate for both beams, **{{REAR_PLATE_L_ORDERED}}** long. Ends only — the ball screw runs under the beam |
| **Plate height** | FLAG: **The five plates that stand on the box are all 301.625 (11 7/8") high** — two side plates, the back plate, two front fins — and **every hole on them is measured from the bottom edge**, the edge that bears on the box's top skin. One height plus one reference edge is what lines the beam up without any plate knowing about another. **A part that is not 301.625 is misordered or mismade.** PLATE_H in the registry; the other three symbols derive from it so they cannot drift |
| Plate materials | 6061 throughout **except** the two Y outboard plates (**10 gauge steel**) and the Y rear plate (**1/4" A36**) — see [`loads-and-plate-thicknesses.md`](loads-and-plate-thicknesses.md), [`archive/outboard-plate.md`](archive/outboard-plate.md) and [`archive/lateral-stiffness.md`](archive/lateral-stiffness.md) |

**Axes:** X, plus a ganged **Y1 (Y) / Y2 (A)** pair, plus Z. `Y_GANGED` + `Y_AUTO_SQUARE` in the
firmware config, so the second Y motor is M3.

### End plates

Partly specified - see [`archive/y-beam-support.md`](archive/y-beam-support.md) and
[`archive/lateral-stiffness.md`](archive/lateral-stiffness.md). They bolt the Y beams to the torsion box.

FLAG: **Reworked 2026-10-02 and all four as-built Y risers are scrapped.** Cast stepper frames replaced
BK12 and the M5 standoffs, the Y steppers went to the back, and the two rear risers became one
steel plate, {{REAR_PLATE_L_ORDERED}} long, that is also the rear shear panel. Four measurements gate cuts that cannot be
undone — see [`open-items.md`](open-items.md) before ordering or cutting anything for the Y ends.

**Deferred, not blocking: the 35 mm sensor bore.**
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md)
§ "The sensor mount" reads as though each endplate and the X gantry plate **already has a 35 mm
hole**. That was written against plates that existed; on this build **nothing has been drilled**.

So it is not a conflict to resolve - it is simply a **feature to include when these plates are
designed**, and the encoder design's wording will want a light touch once they are. Carry it as an
input to the end plate design, not as an open question.

## Cable routing

The two gantry-end encoder cables run **inside the extrusion**, then through the **drag chain** -
which also carries **the spindle cable** and the stepper cables.

**The spindle cable is the first thing to move if anything looks wrong.** A VFD lead is the worst
emitter on the machine and in the chain it runs parallel to the encoder cables for their whole
length. The route is already chosen: overhead, with the coolant and air lines. This is written down
because the failure signature is counts drifting over hours, which reads exactly like lost steps and
sends you to the mechanics instead of the cable.

Drag chain brackets bolt **through the back joining plate** into T-nuts in the outer slots - see
[`gantry-beam-joint.md`](gantry-beam-joint.md).
