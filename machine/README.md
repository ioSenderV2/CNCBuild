# The machine

The build itself: extrusions, rails, screws, plates, and the mechanical decisions with their reasons.
Measured values belong in [`../commissioning/`](../commissioning/).

| File | What is in it |
|---|---|
| [`gantry-beam-joint.md`](gantry-beam-joint.md) | Each gantry beam is two stacked 8020 `30-6060`. How they are tied together, and the four schemes that were killed getting there |

## Frame and motion

| | |
|---|---|
| Gantry beams | **Two 8020 `30-6060` stacked** — 60 mm wide × 120 mm tall, **1000 mm** long |
| Rails | **HGR20**, one per profile on the front face, 17 × M5 at 60 mm into T-nuts |
| Ball screws | **1605**, with BK12 / BF12 supports bolted to the end plates |
| Ball screw position | **X on top** (preserves vertical milling height); **both Y underneath** (Y1's top must stay clear for the X stepper) |
| Y beams | **Do not move** — their end plates bolt to the torsion box |
| Y axis assembly mass | **37 lb** each, before the joining plates |

**Axes:** X, plus a ganged **Y1 (Y) / Y2 (A)** pair, plus Z. `Y_GANGED` + `Y_AUTO_SQUARE` in the
firmware config, so the second Y motor is M3.

### ⚠️ Open: end plates not yet designed

They carry the ball screw supports (M5), bolt the Y beams to the torsion box, and are what ties both
stacked profiles together at each end. Nothing is drawn yet.

🔴 **This conflicts with the encoder design.**
[`../linear-encoder/design-can-position-feedback.md`](../linear-encoder/design-can-position-feedback.md)
§ "The sensor mount" states that each endplate and the X gantry plate **already has a 35 mm hole** -
written when those plates existed. On this build they do not exist yet. Either that 35 mm bore
becomes a **requirement on the end plate design** rather than an existing feature, or the mount
changes. Decide it before the end plates are cut; the puck mount depends on it.

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
