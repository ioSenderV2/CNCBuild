# The lateral fix - widen the riser in its own plane

> **Lifted out of `lateral-stiffness.md` on 2026-10-11, when that file was archived.** The
> archived prose walked through dimension chains the registry now owns, and it
> kept going stale against them. This is the part that does **not** reduce to
> symbols - the comparison, the rejected option, the reason a shape was chosen.
>
> **Numbers here are comparative, not specifications.** They weigh one option
> against another; they do not define a part. For any dimension of a part the
> registry is the authority - see [`../dimensions/VALUES.md`](../dimensions/VALUES.md).

## Front: widen the riser in its own plane

Material is **added inboard**, toward the machine centre, tapering from **100 mm at the top to
200 mm at the base** (settled 2026-10-02; earlier drafts had 3"/9" and 4"/7.8"). It is not a bolt-on outrigger; it is the plate's own outline, which is why the
plates are remade rather than scabbed.

Lateral stiffness goes as **width cubed**, and a taper puts the section where the moment is. Treating
the riser as a cantilever over the ~185 mm between box top and beam underside:

| Base width, at the same thickness | Stiffness vs the 3" prismatic riser |
|---|---|
| 6" | ~4.9× |
| 8" | ~9.6× |
| **200 mm - chosen 2026-10-02** | **~9.2×** |
| 12" | ~25× |

📌 **At 1/2" the chosen figure is the full ~9.2×.** Stiffness scales linearly with thickness, and
as of 2026-10-02 the front plates are **1/2"**, the same as the as-built risers they are compared
against. *(An earlier draft had them at 3/8" and derated this to ~9.5×; that no longer applies.)*

⚠️ **Calculated, not measured.** Tapered cantilever, width varying linearly, load at the top, fixed
base. The fixed-base assumption is doing real work - see the bolt note below.
