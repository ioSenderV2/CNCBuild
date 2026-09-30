# The machine

The build itself: extrusions, rails, screws, plates, and the mechanical decisions with their reasons.
Measured values belong in [`../commissioning/`](../commissioning/).

| File | What is in it |
|---|---|
| [`gantry-beam-joint.md`](gantry-beam-joint.md) | Each gantry beam is two stacked 8020 `30-6060`. How they are tied together, and the four schemes that were killed getting there |
| [`end-plates-risers-and-spindle.md`](end-plates-risers-and-spindle.md) | What holds the beams up and what hangs off them. **Carries the cutting-force recalibration that every deflection figure in this repo depends on** |
| [`torsion-box.md`](torsion-box.md) | What the machine stands on. The box, its three cedar posts, the base frame and shear walls, and the transport plan |
| [`drawings/`](drawings/) | **Derived, not authoritative.** The shop pack for the machining trip - one sheet per plate, printable to PDF. If a sheet and a file above disagree, **the file wins** |

## Frame and motion

| | |
|---|---|
| Beams, all three axes | **Two 8020 `30-6060` stacked** — 60 mm wide × 120 mm tall, **1000 mm** long |
| Rails | **HGR20**, one per profile on the front face, 17 × M5 at 60 mm into T-nuts |
| Ball screws | **1605**, with BK12 / BF12 supports bolted to the end plates |
| Ball screw position | **X on top** (preserves vertical milling height); **both Y underneath** (Y1's top must stay clear for the X stepper) |
| Y beams | **Do not move** — their end plates bolt to the torsion box |
| Y axis assembly mass | **37 lb** each, before the joining plates |
| Spindle | **80 mm, 3 kW water-cooled** with matching VFD, on two 80 mm clamps |
| Y beam support | Two **3" × 12" × 1/2"** end plates / Z risers per beam, ends only - the ball screw runs under the beam |

**Axes:** X, plus a ganged **Y1 (Y) / Y2 (A)** pair, plus Z. `Y_GANGED` + `Y_AUTO_SQUARE` in the
firmware config, so the second Y motor is M3.

### End plates

Partly specified - see [`end-plates-risers-and-spindle.md`](end-plates-risers-and-spindle.md). They
carry the ball screw supports (M5) and bolt the Y beams to the torsion box.

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
