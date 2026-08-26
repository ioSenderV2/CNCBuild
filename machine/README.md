# The machine

**Mega V XL.** Recorded as established; measured values belong in [`../commissioning/`](../commissioning/).

## Frame and motion

| | |
|---|---|
| Extrusions | **1080 mm** on X, Y and A |
| Rack gear | 1000 mm, centred in the 1080 mm ⚠️ *see the open question below* |
| Rails | 1 m linear rails |
| Ball screws | 1 m; **1605** on Z |
| Plates | **150 mm (6")** on X and Y |
| Ball nut block | **55 mm** along the screw |
| Closest approach before the plate hits a stop | **76 mm** ⚠️ *reference edge not yet established* |
| Z gantry plate | 1/2" (12.7 mm) aluminium |
| Sensor bores | **35 mm** in each X-axis endplate and in the X gantry plate |

**Axes:** X, plus a ganged **Y1 (Y) / Y2 (A)** pair, plus Z. `Y_GANGED` + `Y_AUTO_SQUARE` in the
firmware config, so the second Y motor is M3.

### ⚠️ Open: rack gear *and* ball screws?

Both are recorded above because both were stated, and they are normally alternatives. Either the machine
is mid-conversion from rack-and-pinion to ball screw, or they apply to different axes. Resolve before
either number is used for anything.

### ⚠️ Open: what the 76 mm is measured from

It decides travel per long axis - roughly 778 mm if it is the plate's outer edge against the extrusion
end, roughly 848 mm if it is clearance at each end of the screw. Both fit the tape budget, so nothing is
blocked; it matters because the number will otherwise get quoted later as though it were measured. The
marking procedure in [`../linear-encoder/`](../linear-encoder/) §14 produces the real figure.

## Cable routing

The two gantry-end encoder cables run **inside the extrusion**, then through the **drag chain** - which
also carries **the spindle cable** and the stepper cables.

**The spindle cable is the first thing to move if anything looks wrong.** A VFD lead is the worst emitter
on the machine and in the chain it runs parallel to the encoder cables for their whole length. The route
is already chosen: overhead, with the coolant and air lines. This is written down because the failure
signature is counts drifting over hours, which reads exactly like lost steps and sends you to the
mechanics instead of the cable.
