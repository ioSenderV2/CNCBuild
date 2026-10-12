# Rib height beats thicker skins

> **Lifted out of `torsion-box.md` on 2026-10-11, when that file was archived.** The
> archived prose walked through dimension chains the registry now owns, and it
> kept going stale against them. This is the part that does **not** reduce to
> symbols - the comparison, the rejected option, the reason a shape was chosen.
>
> **Numbers here are comparative, not specifications.** They weigh one option
> against another; they do not define a part. For any dimension of a part the
> registry is the authority - see [`../dimensions/VALUES.md`](../dimensions/VALUES.md).

### If more stiffness is wanted, rib height beats thicker skins

Stiffness goes with **skin separation squared**, so thickening the skins is the weaker lever.
Relative bending stiffness, closed-form:

| Build | Relative stiffness |
|---|---|
| 19 mm skins, 100 mm ribs (138 mm deep) | baseline |
| 25 mm skins, 100 mm ribs (150 mm deep) | +46% |
| 25 mm skins, 88 mm ribs (holding 138 mm deep) | +20% |
| **19 mm skins, 150 mm ribs** (188 mm deep) | **+100%** |

Much of that +46% is the box simply getting 12 mm deeper, not the skins working harder. **50 mm
more rib height doubles it**, for roughly 22 lb of extra plywood against 35 lb for thicker skins -
ribs are cheap because there is very little rib material next to two full sheets. The real cost of
taller ribs is **sand volume**, which is a choice at fill time and the part that gets drained for a
move anyway.

**Where 25 mm does earn its place is the top skin**, and not for sag: it takes the riser feet, the
Y plate bolt line and the plate bottom edges **in bearing**. Asymmetric skins are fine in a torsion
box, so **25 mm top over 19 mm bottom** is the sensible split if anything is spent.

SETTLED: **Settled 2026-10-11: 25 mm top, 19 mm bottom.** The box is **144 mm** deep rather than 138. The
underside of the top skin **does not move** - it is set by the post ledge, the bottom skin and the
cavity - so the 6 mm is all on the outside and the machine simply stands 6 mm higher off the floor.
Z 0 is the top skin, so nothing above the box moves at all.
