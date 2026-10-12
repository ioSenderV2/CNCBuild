# Archived prose — read the registry instead

FLAG: **Nothing in this folder is current.** These six files were archived on 2026-10-11. They are
kept because they contain the reasoning behind decisions that are still live, and because one
`git mv` brings any of them back — but **every dimension in them may be stale**, and several are
known to be.

**For any dimension of any part, the authority is
[`../../dimensions/registry.toml`](../../dimensions/registry.toml)**, read through
[`../../dimensions/VALUES.md`](../../dimensions/VALUES.md).

## Why they were archived

They were walkthroughs of dimension chains the registry now owns. Across 66,000 words they
carried **4,950 numbers**, almost all of them duplicating a registry symbol — and a duplicate is
a thing that can disagree.

**The failure that settled it.** A sole plate position was read out of `x-gantry-end-plates.md`
as **−182.5** when the registry had moved it to **−175** the week before, and the number went
into a new document before anyone noticed. The prose had been superseded by the interposer going
from 3/8" to 10 mm and by the as-built 58 being retired — the file still described an arrangement
that no longer existed.

OPEN: **The prose audit cannot catch that class of drift.** `tools/audit-prose.py` looks for *near
misses* — a literal close to a registry value but not equal to it. A 7.5 mm error does not read
as a near miss, it reads as a different quantity. Widened far enough to see it, the report runs
to **1,426 lines**, which is not a report anybody acts on.

## What was kept

Four arguments came out into files of their own, one each, in [`..`](..):

| File | The argument |
|---|---|
| `box-stiffness.md` | Rib height beats thicker skins |
| `three-point-mount.md` | Three posts, not four |
| `egg-crate.md` | Continuous ribs both ways, not blocking |
| `lateral-fix.md` | Widen the riser in its own plane |

NOTE: **Their numbers are comparative, not specifications** — they weigh one option against another
rather than defining a part, so they cannot go stale against the registry.

## The files here

| File | What it was |
|---|---|
| [`torsion-box.md`](torsion-box.md) | The box: skins, ribs, walls, ledges, tenons, the post stack |
| [`lateral-stiffness.md`](lateral-stiffness.md) | The front fins fully dimensioned, the rear plate, the tongues |
| [`x-gantry-end-plates.md`](x-gantry-end-plates.md) | The end plate stack-up, the 242.5 height, the sole plate |
| [`z-carriage.md`](z-carriage.md) | The Z plate, spacer blocks, clamp geometry, travel budget |
| [`y-beam-support.md`](y-beam-support.md) | How each Y beam is held: end plate, castings, thrust block, BF12 |
| [`outboard-plate.md`](outboard-plate.md) | The full-height outboard plate, its sourcing and galvanic cost |
