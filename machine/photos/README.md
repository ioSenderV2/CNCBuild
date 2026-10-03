# Photographs of the build

**A deliberate addition to this repo's conventions, 2026-09-29.** Until now the premise was that the
reasoning is the artifact and source means KiCad plus Python - there were no images here at all.
That premise held right up until it didn't.

## Why these exist

The gantry joint design turned on a fact **no drawing shows**: behind the 2.21 mm skin at the centre
of each `30-6060` face there is nothing. The 8020 cross-section drawing is dimensionally complete and
still led to the wrong conclusion, because a rib was inferred where there is void. Three bolting
schemes were designed and killed on that single observation, and it came off a photograph and an eye
down the end of a real extrusion.

Two things follow, and they are the rule for adding anything here:

1. **A photograph is admissible evidence in this repo when it shows something a drawing cannot.**
   Cross-sections, clearances, what is actually bolted to what, a part that disagrees with its
   catalog entry.
2. **It is not a substitute for a measurement.** Nothing here should be scaled off. Every number in
   the prose came from a caliper or a vendor drawing, and stays labelled that way - see the standing
   rule in the [root README](../../README.md).

These are photographs of **this build**, taken by the owner. Third-party material - vendor drawings
and datasheets - goes to [`../../manufacturer-assets/`](../../manufacturer-assets/) instead, where it
is deliberately untracked because this repository is public.

## What each one shows

| File | What it is evidence of |
|---|---|
| `gantry-stack-end-view.jpg` | The two `30-6060` stacked, end on. The butt joint with nothing mechanical across it - the problem the joining plates solve |
| `gantry-stack-end-view-bk12.jpg` | Same, closer, with the BK12 support in place. **The clearest view of the internal voids** and of the corner bores running lengthwise |
| `gantry-stack-rails-front.jpg` | 1000 mm, one HGR20 rail on the front face of each profile. Shows why the spindle's rail couple crosses the seam |
| `gantry-stack-ballscrew-front.jpg` | The 1605 screw with BK12 / BF12 supports, mounted above the stack on X |
| `front-plate-trial-single-bolt.jpg` | Trial plate in the gap between bearing blocks, establishing that the two slots flanking the seam are reachable |
| `front-plate-trial-flange-bolts.jpg` | **The clearance test that settled the front plate.** Four M8 flange bolts seated in the 46.7 mm gap, blocks clearing - after arithmetic had said they would not fit |
| `z-carriage-assembly-end.jpg` | Z carriage dry-assembled on the **X carriage plate** - HGR20 rails on it, the spacer blocks (**16.41 mm measured**, not the 5/8" this repo used to call them) sandwiched on the bearing blocks, ball nut housing between them (shown dry-fitted, without the Z plate that finally clamps them). The blue is **layout dye**, not a finish |
| `z-carriage-assembly-oblique.jpg` | Same, oblique - shows BK12 with motor and BF12 both on the plate, so screw and motor are fixed relative to it |
| `y-beam-end-plate-outer.jpg` | **A Y beam as built.** End plate / Z riser on the stacked pair, bolt heads on the outer face, fully exposed - the arrangement the X end plates copy |
| `y-beam-stepper-mounted.jpg` | Stepper on the outside of the riser, shaft through the plate. The riser runs well below the beam |
| `y-beam-coupler-bk12.jpg` | Coupler between motor and screw, BK12 inboard, screw running under the beam |
| `y-beam-riser-and-gusset.jpg` | The riser with the existing **12" × 6" × 1/4" gusset** on the outboard face |
| `y-bearing-blocks-butted-154.jpg` | **Calipers reading 154.18 mm across two HGH20 blocks butted** on the X/Y kit's rail. The measurement that confirmed the X end plate width and killed the "2-3 mm between the blocks" this repo had carried as its reason for it |
| `y-bearing-blocks-machined-pads-128.jpg` | **128.24 mm across the two blocks' machined pads only.** The pair with the end caps excluded - which is what actually bears, and the number any carriage plate has to exceed. Pads are 51.15 each, end caps 12.97 |
| `front-fin-template-tongue-bolts.jpg` | The 1/4" MDF front-fin template, bottom corner. **The Y 30 line with T1 and T2 marked at X 25 and 170** - the check that closed the fin's geometry, against an outline whose taper is not corner-to-corner. The 7 / 46 / 7 and 28 / 58 / 73 pencil marks are the cast stepper frame's bolt pattern, laid out separately |
| `casting-with-interposer-mockup.jpg` | **The cast stepper frame with an aluminium bar standing in for the 3/8" interposer.** Shows the thing the prose had to be corrected on: the bar sits **on** the casting's stepped top and **overhangs its end**, so the casting hangs below it and both pass through the front plate's 62 × 50 window together — the bar being the higher of the two, which is what puts the window's top edge at the beam underside. A combination square is set against the casting's lower body; **the reading is the casting's height as it sits in the window** |

`front-plate-trial-flange-bolts.jpg` is worth keeping for its own sake: the calculation said
47.3 mm against a 46.7 mm gap and the parts said otherwise. The parts were right.
