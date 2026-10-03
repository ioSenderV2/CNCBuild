# The machine

The build itself: extrusions, rails, screws, plates, and the mechanical decisions with their reasons.
Measured values belong in [`../commissioning/`](../commissioning/).

| File | What is in it |
|---|---|
| [`gantry-beam-joint.md`](gantry-beam-joint.md) | Each gantry beam is two stacked 8020 `30-6060`. How they are tied together, and the four schemes that were killed getting there |
| [`torsion-box.md`](torsion-box.md) | What the machine stands on. The box, its three cedar posts, the base frame and shear walls, and the transport plan |
| **The ten plate files** | What holds the beams up and what hangs off them — listed below |
| [`drawings/`](drawings/) | **Derived, not authoritative.** The shop pack for the machining trip - one sheet per plate, printable to PDF. If a sheet and a file above disagree, **the file wins** |

## The plates, risers and the spindle mount

**Partly settled.** The beams themselves are finished — see
[`gantry-beam-joint.md`](gantry-beam-joint.md). These ten files cover what holds them up and what
hangs off them. Several dimensions are still **⚠️ Open** and are marked as such rather than guessed;
[`open-items.md`](open-items.md) is the generated-adjacent list of them, and the repo-wide one is
[`../STATUS.md`](../STATUS.md).

They were one 2877-line file, `end-plates-risers-and-spindle.md`, until 2026-10-02. The split is
verbatim — no decision was reopened in the move — and it is along the seams the prose already had.

| File | What is in it |
|---|---|
| [`loads-and-plate-thicknesses.md`](loads-and-plate-thicknesses.md) | **Read this first.** The cutting-force recalibration (500-1000 N, not 250) that **every deflection figure in this repo depends on**, the plate and riser thicknesses it sets, and the one measurement that would settle the 1/4" question |
| [`y-beam-support.md`](y-beam-support.md) | How each Y beam is held at its ends: the end plate / Z riser, the **cast stepper frames** on all four axes, the thrust block, the inverted ball nut and its sole plate, and BF12 at the rear |
| [`lateral-stiffness.md`](lateral-stiffness.md) | The lateral fix — tapered front fins per beam, the **one 1200 mm steel back plate** replacing both rear risers and the shear panel, and the tongues that back them |
| [`outboard-plate.md`](outboard-plate.md) | The full-height outboard plate: **1/8" steel**, also the Y back joining plate, how it lands on the torsion box, the galvanic cost, and the encoder tape that runs on the front plate |
| [`spindle-and-mount.md`](spindle-and-mount.md) | The Ø80 2.2 kW water-cooled spindle, its body dimensions, why not 3 kW, and the 109 mm offset from the X beam to its centreline |
| [`z-carriage.md`](z-carriage.md) | The 164 × 175 × 1/2" Z plate, the spacer blocks and why they get skimmed, the clamp mount geometry, the travel budget and the top stop |
| [`x-gantry-end-plates.md`](x-gantry-end-plates.md) | The two X gantry end plates: the vertical stack-up, the 242.5 mm height, the sole plate and doubler block, the four bolts above the Y beam top, and the shelf |
| [`tramming.md`](tramming.md) | Roll by **shimming the shelf**, nod still open, and why the carriage plate joint is deliberately not adjustable |
| [`machining.md`](machining.md) | **One trip, so design ahead of the build.** One datum per plate, one reference rail, and what mating hardware to take |
| [`open-items.md`](open-items.md) | Everything still unmeasured, grouped by where it came from |

## Frame and motion

| | |
|---|---|
| Beams, all three axes | **Two 8020 `30-6060` stacked** — 60 mm wide × 120 mm tall, **1000 mm** long |
| Rails | **HGR20**, one per profile, 17 × M5 at 60 mm into T-nuts. **Y rails are on the beams' inside faces, facing each other.** X, Y1 and Y2 share one kit; **Z is a 400 mm kit from a different supplier** - do not quote one kit's dimension for the other |
| Bearing blocks | **77.09 mm** each, measured - two butted read **154.18 mm**, which is what sets the 154 mm plate width. Of that, only the **51.15 mm machined pad** bears; a butted pair spans **128.24 mm** of pad, and that is the real floor for any carriage plate |
| Ball screws | **1605**. **Every axis drives through a cast stepper frame** — X, Y1, Y2 and Z — carrying motor face, bearing housing and coupler in one part, which is what retired the M5 standoffs. BF12 stays at each far end. Y ball nuts run **inverted**, on a tongue off the bottom of the carriage plate, so their bolts are reachable at assembly |
| Ball screw position | **X on top** (preserves vertical milling height); **both Y underneath** (Y1's top must stay clear for the X stepper) |
| Y steppers | **At the FRONT of the machine** (2026-10-02) — one cast frame carries motor face, bearing housing and coupler |
| Y beams | **Do not move** — their end plates bolt to the torsion box |
| Y axis assembly mass | **37 lb** each, before the joining plates |
| Spindle | **Ø80 mm, 2.2 kW water-cooled** with matching VFD, on two 80 mm clamps |
| Y beam support | **Front:** a tapered 100→200 mm × 302 mm × 1/2" plate per beam, with a 62 × 50 window for the stepper frame. **Rear:** one **1200 mm × 12" × 1/4" A36 steel** plate for both beams. Ends only — the ball screw runs under the beam |
| Plate materials | 6061 throughout **except** the two Y outboard plates (**1/8" steel**) and the Y rear plate (**1/4" A36**) — see [`loads-and-plate-thicknesses.md`](loads-and-plate-thicknesses.md), [`outboard-plate.md`](outboard-plate.md) and [`lateral-stiffness.md`](lateral-stiffness.md) |

**Axes:** X, plus a ganged **Y1 (Y) / Y2 (A)** pair, plus Z. `Y_GANGED` + `Y_AUTO_SQUARE` in the
firmware config, so the second Y motor is M3.

### End plates

Partly specified - see [`y-beam-support.md`](y-beam-support.md) and
[`lateral-stiffness.md`](lateral-stiffness.md). They bolt the Y beams to the torsion box.

🔴 **Reworked 2026-10-02 and all four as-built Y risers are scrapped.** Cast stepper frames replaced
BK12 and the M5 standoffs, the Y steppers moved to the front, and the two rear risers became one
1200 mm steel plate that is also the rear shear panel. Four measurements gate cuts that cannot be
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
