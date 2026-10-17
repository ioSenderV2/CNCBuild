# Measured masses

**Weighed, 2026-09-26.** His figures, taken off the assemblies as they stood that day. They are here
rather than in `machine/` because they are measurements of the machine, and this folder outranks any
figure computed from a drawing.

| Assembly | Mass | As weighed |
|---|---|---|
| Z carriage | **9 kg** | **No spindle fitted** |
| X gantry | **15 kg** | |
| Y1 assembly | **17 kg** | |
| Y2 assembly | **17 kg** | |
| **Four moving assemblies** | **58 kg** | |

**Weighed, 2026-10-16** — the two steel plates, on his scale.

| Part | Mass | As weighed |
|---|---|---|
| Rear plate, 1/4" A36 | **38 lb 10 oz** | the whole plate, undrilled |
| Side plate, 10 gauge | **18 lb** | one of the two |

**Weighed, 2026-10-16** — the torsion box's plywood, on his scale, before assembly.

| Part | Mass | As weighed |
|---|---|---|
| Web and rib strip, 100 | **3 lb 3 oz** | each, 12 of them |
| Front laminations, 24 | **6 lb 9 oz** | the pair |
| Back laminations, 24 | **9 lb 3 oz** | the pair |
| Side laminations, 24 | **8 lb 12 oz** | each, before the proud strip is sawn off |
| **The box less its skins and the sand** | **71 lb 8 oz** | the four rows above |

Two corrections pull against each other and neither reaches a pound: the **front and back webs are
each 36 longer** than the strip that was weighed, which adds about **3 oz** across the two, and the
**60 strip sawn off each side lamination** is about 4.9% of that board, which takes about **14 oz**
back off. **Call it 71 lb.**

**The skins are not in it** — they need a different scale — and neither is the sand.

NOTE: **This is the first real number under the 565 lb estimate below.** The box less skins and sand
was never weighed before, so the installation figure has had nothing measured in it at all.

🔴 **These were weighed to settle a disagreement, and they settled it.** The order sheet's weight
column put the rear plate at **80 lb**, which would need half-inch stock over that outline. The
scale says otherwise and so does the micrometer: computed from the registry outline at the measured
6.19 the plate is **39.11 lb**, against **38.625** on the scale — **1.2% apart**. The side plate
comes out **17.67** computed against **18** weighed, **1.9%**. **The plates are what they were
ordered as; the order sheet's weight figure is the thing that was wrong.**

NOTE: **The Z figure is the one that goes stale first, and it is the one most used.** It was weighed
without the spindle, so every use of it has to say whether the spindle is in or out. The spindle
settled after this weighing - Ø80 2.2 kW water-cooled, see
[`../machine/spindle-and-mount.md`](../machine/spindle-and-mount.md) - so the loaded Z carriage has
never been weighed. **Weigh it once the spindle and its clamp block are on**, and record it as a
second row rather than correcting this one: the bare figure is what the moving-mass arguments were
built on.

OPEN: **The whole-machine and whole-installation figures are ESTIMATES, not weighings, and should not
be quoted as measurements.** From the 2026-09-26 session: the machine with spindle, risers and
cabling at roughly **80 kg**, and the whole installation - machine, torsion box, sand and timber base
- at roughly **565 lb**. Both carry a tilde in their source and neither has been on a scale. The 565
is the figure the moving plan is built on, so it is the one worth checking against something real
before anybody tries to lift it: see [`../machine/assembly.md`](../machine/assembly.md) for filling
the sand last, which is what keeps that number off anybody's back.

## Why these were weighed

FLAG: **Reflected inertia is why the gantry's mass nearly vanishes from the motor decision, and these
are the numbers that showed it.** Through a 5 mm lead, load mass reaches the motor shaft as
mass x (lead / 2π)² - and [`../machine/stepper-sizing.md`](../machine/stepper-sizing.md) works that
to 6.3 x 10⁻⁷ kg·m² per kilogram, which puts the whole 58 kg below the screw's own inertia. So these
masses settle the *structural* questions - what the risers carry, what the three-point mount carries,
what has to be lifted - and are very nearly irrelevant to motor sizing. Reading them the other way
round is the mistake they invite.

## Provenance

Weighed during the 2026-09-26 design session, which ran in the **ioSender** repo rather than this one
- so the reasoning around them is in that project's conversation log for that date, not here. The
figures were carried in a memory note until 2026-10-12 and are now in the repo, which is where this
project keeps things that the repo can state for itself.
