# Three load-bearing points, not four

> **Lifted out of `torsion-box.md` on 2026-10-11, when that file was archived.** The
> archived prose walked through dimension chains the registry now owns, and it
> kept going stale against them. This is the part that does **not** reduce to
> symbols - the comparison, the rejected option, the reason a shape was chosen.
>
> **Numbers here are comparative, not specifications.** They weigh one option
> against another; they do not define a part. For any dimension of a part the
> registry is the authority - see [`../dimensions/VALUES.md`](../dimensions/VALUES.md).

## The three load-bearing points

**Front left corner, front right corner, and the middle of the back.** Each is a **laminated plywood
leg, 72 across the machine by 86 fore and aft** — four 18 mm strips, the lamination running across
the machine so the base's fore-aft rails pass through it. It replaced a dressed cedar 4×4 on
2026-10-15, and the three-point argument below is indifferent to which: it is about the number of
contact points, not the material.

Three points, not four, and the reason is the whole argument: a three-point mount is statically
determinate, so **the box cannot be racked by a twisted floor or a twisted base**. That matters
because the property being protected is the two Y beams staying **coplanar**, which is what the X
gantry rides on and what the entire riser exercise existed to guarantee.

The three-point mount is between **box and base** - not between base and floor. So the base should be
made as rigid as possible; stiffening it costs the mount nothing and the box is isolated from its
twist either way.

### Stiffen it against RACKING, which is not what it looks like

Folded in 2026-10-12 from the 2026-09-26 session notes. The timber base's weakness is **racking - the
frame going out of square as a parallelogram - and not bending.** So the thing that stiffens it is
**plywood shear panels on at least two adjacent sides**, not deeper members.

FLAG: **DO NOT REBUILD THE BASE IN THE LEFTOVER 25-SERIES EXTRUSION.** Depth is cubed and timber buys
it cheaply: a 2x6 is of order **twice** as stiff as a 2550, and a 4x4 about **seven times** a 2525 and
better in buckling. Timber also damps, where aluminium rings. Extrusion's one real advantage over
timber here is dimensional stability - **and that is precisely what the three-point mount above
already solves**, which is why it is not a reason to spend the extrusion on the base. Spend it on the
machine's own structure, where spans are short and the rails locate off it.

Comparative figures from that session, like the rest of this file - they say which way the choice
goes, not what a part is.

## It is one interface, and the risers are the other - do not conflate them

FLAG: **THE RISERS BOLT TO THE BOX ON ALL FOUR, SOLIDLY, WITH SHIMS. YOU CANNOT THREE-POINT A
GANTRY.** Folded in 2026-10-12 from the 2026-09-26 session notes. There are two separate interfaces
stacked here and they want opposite things:

| Interface | How | Why |
|---|---|---|
| Box to base | **Three points**, one bolt per pad, retention not alignment | the box must not inherit the base's twist |
| Risers to box | **All four**, solid, **shimmed** | the two Y beams have to end up coplanar, and that is a four-point condition |

The reason the shimming stays valid is the three-point mount underneath it: because the box is not
being racked by the base from one season to the next, a shim set established once keeps meaning what
it meant. **The determinate mount below is what makes the over-constrained joint above safe** - so
the two are not in tension, the lower one is what licenses the upper one.

The failure this heading guards against is reading "three points, not four" as a principle of the
machine rather than a property of one joint, and then trying to apply it one level up, where it would
give away the coplanarity the whole riser exercise exists to protect.

---

**The tenon and ledge detail is not here.** How each post is reduced, how deep the
ledge is and what that leaves for the tenon are dimension chains the registry owns -
see POST_W, T_BOX_LEDGE, TENON_CORNER and POST_TENON_L in
[`../dimensions/VALUES.md`](../dimensions/VALUES.md). This file is only the
argument for three points rather than four.
