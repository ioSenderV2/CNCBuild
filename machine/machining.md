# Machining: one trip, so design ahead of the build

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

Accurate holes are drilled on **a single visit to a friend's shop** - a Laguna mill, 4' × 1' bed,
**manual X and Y**, DRO to be confirmed. **As of 2026-09-29 none of the 30 holes in the X carriage
plate are drilled.**

🔴 **Every plate needing accurate holes must be fully dimensioned before that trip**, including
assemblies that will not be built for months: **X carriage plate, Z plate, two X end plates**. One
more plate on the visit costs an hour; a second trip costs a weekend.

🔴 **The 2026-10-02 rework put three more parts on this trip.** The list had been shrinking; it is
not any more:

| Part | Why the mill |
|---|---|
| **Two Y front plates**, 1/2" | the 8-bolt corner-bore pattern *and* the 60.5 × 50 window |
| **The 1210.73 mm rear plate**, 1/4" steel | two 8-bolt patterns a metre apart that must match extruded bores - and the part may exceed the machine's X travel |
| **Interposer bars**, 60 × 150 × 3/8" - two for Y, plus X | six tapped M5 under a bearing face and six flange clearance holes, all in a small part |

🔴 **The six bolt-on plates went ONTO the trip on 2026-10-09** - two **11 7/8" × 39 5/16" × 10
gauge steel** outboard plates, three **45 mm × 1 m × 4 mm 6061** front strips, and the **4 11/16" ×
39 5/16" × 1/4"** X back joining plate.

They had been "no mill needed" on a sound argument: every hole is a ø9 clearance into a T-slot and
the nut slides to meet the bolt, so an individual hole's position hardly matters. **His call
overrules it on a different one** - 14 holes on a strip and 28 on a back plate, 126 across the six,
is more hand layout than comes out straight. A wandered row still bolts up and merely fights for an afternoon - the
holes are not needed perfect for the joint, they are wanted perfect for the assembly.

❌ **A sharper reason stood here for the front strips and the 2" stock removed it.** While they were
45 wide they filled the block gap exactly, so a row wandering in Y drove the strip into a bearing
block. At 50.8 the strip runs *under* the blocks and the next obstruction is the rail, 9.6 away.

⚠️ **This is six more metre-long parts on a trip that already has an open question about X
traverse** - the one gating the rear plate. If the answer comes back short, **reposition the two outboard plates or the X back
plate** - there the T-nut reason that used to keep them home does make a shifted station cheap.
**Not the front strips, and not the rear plate**: the strips because their Y is a clearance against a
bearing block, the rear plate because its two patterns must meet extruded bores a metre apart.

✅ **The two X end plates are specified** - one drawing, one setup, with the stepper holes omitted
on the idle end.

**Triage - not everything needs the mill:**

| Home drill press | The mill |
|---|---|
| Beam joining plates - 9 mm clearance into T-slots at 150 mm, and the T-nut moves to meet the bolt | Rail mounting patterns |
| | Bearing block and nut housing patterns, with counterbores |
| | The 8-bolt end plate patterns that must match the extrusion corner bores |

## The two Z rails need nothing special at the mill

Two rails parallel and coplanar over 407 mm is what decides whether the Z runs sweetly or binds, and
it is tempting to try to buy that at the mill. **There is nothing to buy.** Both rails tap **M5
straight into the plate**, so both patterns are fixed — drill them to the sheet and move on.

**The adjustment is the rail's own and it happens at assembly**, not here: HGR20's mounting holes are
**ø6 through under a ø9.5 counterbore** on an M5, about a millimetre of float. The procedure for
using it — lock rail one, then set rail two one fastener at a time — is an assembly step and lives in
[`assembly.md`](assembly.md).

## Scribe the extrusion bolt patterns; do not punch them

**Scribe two lines and tick four stations along each** - that is the eight-hole pattern at a beam
end, and it is quicker and more accurate than the alternative. **Punching through an offcut of the
`30-6060` is the less accurate of the two**: you are working off that offcut's own bores, which are
extruded features, and their error comes with you.

It costs nothing to be approximate here in any case. Every one of these holes is **ø9 clearance on
an M8** - about a millimetre of float, which this joint wants because it works by friction rather
than bearing.

**Take instead:** a scriber and a centre punch.

## Each plate only has one WCS origin for the holes to be drilled

Pick a corner, dimension every hole from it, **never chain dimensions**. On a manual mill with a DRO
the operator types absolute coordinates; chained dimensions accumulate error and invite arithmetic
slips.

---
