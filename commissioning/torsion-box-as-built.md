# The torsion box, as built

**Measured off the parts, not taken off the drawing.** Where this disagrees with the registry, this
file is what the remaining parts get cut to — the registry's figures are what the box was drawn at.

## The back outer lamination is 1211, and the corner is reversed

| | As built | Drawn |
|---|---|---|
| Back outer lamination | **1211**, one piece, glued **flush at both ends** | {{BACK_LAM_L}}, two pieces butted |
| Side outer laminations, as cut | **1211** each | {{SIDE_LAM_L}} |
| Back corners | **a 24 × 24 × {{TONGUE_FULL_H}} hardwood filler in each**, two off | the back lamination lapping both sides' end grain |

A 1211 back lamination spans the top skin exactly and, flush at both ends, sits **between** the two
side laminations' inner faces rather than over their ends. So the back corner is a butt, and the
sides' end grain stands at the two back corners instead of being capped.

**The lap is bought back with a hardwood filler in each corner** — his call, machined to fit. Each
void is a **24 square column the full height of the lamination**: 24 across by 24 fore-and-aft, the
24 being the tongue's own thickness in both directions, and the full height because the lamination
caps both skins' end grain and stands {{BOX_TONGUE_PROUD}} proud of the top skin.

**Grain direction matters more than the fit.** Run the filler's grain **vertically**, the way the
plywood laminations' face grain runs along the wall: a filler with its grain across the corner is
end grain to the glue line on both faces, which is the weak way round in the one place the corner
has no lap.

**The back tongue's bolt line is unaffected.** Eight bolts at X 75 on a 150 pitch run 75 to 1125,
well inside the 1211.

## The two back pieces become the second side

The back's {{BACK_LAM_PIECE_L}} and {{BACK_LAM_PIECE_SHORT}} pieces are reassigned: one side
lamination is the remaining 1211 piece, and **the other side is made from the two back pieces butted
end to end** and cut to length. The front cap keeps its own pair.

**The butt is sound and it is where it already wanted to be:** the inner web behind it is one
continuous piece, so the joint is staggered against solid material, which is what laminating a wall
is for.

## The order the walls actually went on

1. **Back**, the 1211 piece, flush at both ends.
2. **Left side**, from the two back pieces butted, with a **1/4 gap at the back** set off a
   waterjet sole plate used as the spacer against a backer board. Rearmost piece first, second piece
   cut to fit flush with the front.
3. **Right side**, the remaining 1211 piece, same 1/4 gap at the back. **It therefore stands about 6
   proud at the box's front edge and gets trimmed off that end before glue-up** — the front cap beds
   on that face.
4. **Front cap**, the 630 and 629 pieces, 142 tall against the back and sides' 202.

**Clamping is screws from inside the cavity**, not clamps across the box — a 52" parallel clamp
cannot reach the middle of a side with the box on edge. Jug weight held the back lamination down
while the screws went in and **a 4 ft level lays flat on it**, so that glue line closed.

## SETTLED: The top skin is 1210, and the plates fit between the tongues

| | As built | Drawn |
|---|---|---|
| Top skin, both ways | **1210** | {{BOX_W}} |
| Side plates between the tongues | **they fit** | the span had to beat {{MACHINE_OUTER_W}} |

**The skin came out 1 under the drawn box and that was the live risk.** A tongue's inner face is a
hard bearing face with no float, the span between the tongues *is* the skin's width, and the machine's
outer width — plate outer face to plate outer face, set by the beam spacing the rear plate's bores
already fix — is {{MACHINE_OUTER_W}}. On paper that was 1.28 too narrow and the remedy would have been
sanding the tongues' inner faces back where the plates land.

**It did not bite. Both plates went in.** Nothing was removed from the plywood.

**Both Y beams are up** on one bolt into each extrusion end plus three or four through the side plate
into T-slot nuts. Clamps were used and were not needed, which says the plate seats on the tongue
rather than being pulled to it.

SETTLED: **Both of the back plate's 8-bolt patterns fit.** All sixteen M8 x 35 flange bolts went
into the extrusion ends with no binding. That was the last hole position on the machine with
anything riding on it.

## FLAG: The Y block gap comes out under what the X assembly needs

**Measured between the two Y bearing blocks' faces, tape hooked magnetically on one block so the
reading is repeatable single-handed.** All 28 T-slot bolts torqued, all sixteen rear bolts in, **no
tongue bolts yet**.

| Station | Gap |
|---|---|
| Back | **1022** |
| Middle | **1021** |
| Front | **1020** |

**Two separate findings, and only one of them is slack.**

**The taper is 2 mm and it is LINEAR**, which is toe rather than bow - a bowed plate reads high at
the ends and low in the middle, or the reverse. It was 4 mm with the plates on a clamp at each end
and halved when the T-slot line came down, so the tongue line should take more out of it. 🔴 **It has
to end near nothing: an HG20 block has fractions of a tenth of internal clearance, so a taper over
the travel is a bind, not a tolerance.**

🔴 **The absolute is the one that is not slack.** The X assembly is two end plates at
{{T_X_ENDPLATE}} plus the {{BEAM_LEN}} beam - **1024.38** - and that is what must fit between the
block faces. The **widest** reading is 1022, at the back, which is exactly where the back plate's
bores fix the spacing and where sixteen bolts just went in without binding. **2.38 short, and the
tongue line will not find it.**

OPEN: **The measurement that separates the causes has not been taken: the gap between the two Y
beams' INNER FACES, at the back.** {{Y_BEAM_GAP}} is the chain's figure.

- Read 1084 and {{RAIL_STACK}} is wrong - a 31.19 stack accounts for the whole 2.38 across both sides.
- Read 1082 and the beams sit closer than the chain says, despite the bores fitting, which the 9 mm
  clearance on M8 allows by about a millimetre each.

NOTE: **Nothing on the X gantry is cut**, so a correction is still cheap - but the X beam is not free
either: it is {{BEAM_LEN}} and the three front joining strips arrived at exactly that to match it.

## The tongue line is M8 LOCK NUTS, not acorns

**The acorn nuts bottomed out on their thread before seating**, with M8 fender washers under both
head and nut. He went to **M8 lock nuts**, which is what the outboard plate's own table in
[`../machine/assembly.md`](../machine/assembly.md) already called for: from outboard, washer, tongue,
plate, lock nut on the inboard face.

**That retires the acorn arithmetic on this line.** {{ACORN_NUT_DEPTH}} is a hard ceiling - past it
the bolt lands on the dome and the joint never clamps however hard the nut is turned, which is the
failure you cannot see from outside. A lock nut has no dome, so the ceiling and everything derived
from it stops applying.

SETTLED: **The rear plate's THIRD fender washer comes off.** It existed only to lift an acorn far
enough that an M8 x 45 would not bottom. With a lock nut there is nothing to bottom on, and the bolt
length comes back as protrusion past the nut, which is what a nylon collar wants.

**Two fender washers stay**, head and nut. That is the bearing-area reason, not a locking one - this
is the line whose plywood creeps under the bolt, and the standing answer to that is re-torque.

## Drilling the tongue holes: go in from outside

**A 9 mm bit cannot be brought in square from inside** - the hole sits 30 mm above the skin and no
drill that holds a 9 mm bit gets that low, so it enters at a downward angle and shaves the entry
edge. It does not wander, and the angle costs nothing: this line is a CLAMP and not a locator, so
the hole is pure clearance and nothing bears on its wall. The locating is the T-slot line against
the beam and the sixteen bores at the beam ends.

**The tongue is the outboard layer, so its outside face is in free air.** Transfer-punch through the
plate's hole, then drill the 9 mm from outside, square, with the whole drill clear. Or pilot small
from inside - a stubby 3 mm in a hex holder fits where a 9 mm will not - and open out from outside.

## FLAG: Check the rear plate's overhang before the side laminations go on

The sides were cut **1211**, where the drawing has them start {{SIDE_TONGUE_START}} forward of the
box's back edge. That offset exists for one reason: **the rear plate's end overhangs the box by
2.66**, and a side lamination running all the way back to the back face runs into it.

**So before gluing a side on, hold it in place and look at the back end.** If it reaches the back
face, the back 6.35 of it has to come off at that end, or the rear plate will not sit down. This is
the same clash the 2026-10-11 corner reversal caused and is the reason the offset is in the drawing.
