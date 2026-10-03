# The spindle and its mount

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

| | |
|---|---|
| Spindle | **Ø80 mm, 2.2 kW, water-cooled**, with matching VFD |
| Vendor | **RATTMMOTOR**, kit with VFD, 80 mm clamp, ER20 collet and pump |
| Nameplate | 🔴 **Φ80×213, 2.2 kW, 220 V, 8 A, 400 Hz** (24,000 rpm at 400 Hz) - **corrected 2026-10-02 from Φ80×200 and 8.5 A** |
| **Mass** | **5.2 kg** |
| Body | **stainless steel**, 4 bearings, **P4 class**, grease lubricated |
| Runout | **< 0.01 mm**; precision tapered bore **0.003-0.005 mm** |
| Collet | **ER20**, supplied with Ø6 mm, range Ø1-12 mm |
| Cooling | two **Ø8 mm** water fittings, exiting **radially at the rear** |
| Clamps | **two 80 mm aluminium clamps**, one at each end of the spindle |
| Clamp size | 120 mm × 55 mm × 100 mm |
| Fixing | **4 × M8 × 80 mm socket head** per clamp, into the Z plate |

**Two clamps at either end is the right arrangement** and matches the dual-clamp recommendation
already carried in the project notes for a round-body spindle. Eight M8 holding the spindle is not
where this assembly will be soft.

## ✅ Closed: the body is 213, and the 199 is retired

**Settled 2026-10-03.** He confirmed **213**, which is what the vendor listing said all along: the
nameplate designation is **Φ80×213** and its drawing carries a **213 mm** dimension spanning the
body to the rear end, plus a **27 mm** segment at the rear and a **33 mm** dimension across the
collet nut. See
[`../manufacturer-assets/Spindle-2.2kW-80mm-RATTMMOTOR-listing.png`](../manufacturer-assets/Spindle-2.2kW-80mm-RATTMMOTOR-listing.png).

🔴 **The 199 that this file used to carry is wrong and must not be reused.** It never
reconciled with anything - not with 213, and not as 199 + the 25 mm front cap, which gives 224. If
199 turns up anywhere it is stale. The registry's SPINDLE_BODY_L is now simply another name for
SPINDLE_BARREL_L.

⚠️ **Read the listing's two vertical dimensions as DIAMETERS.** The 33 and the 80 are both
drawn vertically, so 33 is the ER20 nut's outside diameter and not a length. The drawing gives no
axial figure for the nose or the nut at all, which is why the two numbers below had to come off a
real spindle.

✅ **Measured off the Mega V 2026-10-03** - the same part - both **from the end of the barrel**:

| | mm |
|---|---|
| Barrel end to the nose shoulder | **17** |
| Barrel end to the collet nut's outer end | **60** |

**The 60 is what places the tool.** Everything above it is a stack from the X beam; everything below
it is stickout.

📌 **The clamps were never at risk.** At 116 mm centres with 55 mm axial clamps the pair spans
171 mm, which fitted inside 199 as well as 213 - which is why the dispute, while it lasted, moved the
*vertical* chain and nothing else.

## The body dimensions, off the vendor drawing

⚠️ **Superseded - the body is 213, see the closed note above. Every 199 in this section is stale and kept only so the reasoning that used it can still be followed.**

The three dimensions on the product drawing are **sequential, not overlapping** - confirmed by the
user 2026-09-30:

| Segment | |
|---|---|
| Collet nut face to the nose flange (nut + exposed shaft) | **52 mm** |
| Nose flange / front bearing cap | **25 mm** |
| ~~Nose flange to the rear end - the Ø80 body~~ | ~~199 mm~~ → **213** |
| Overall, collet nut face to rear | **276 mm** |

📌 **The full barrel is Ø80 and clampable** (213, not the 199 this line used to say). The black bands at each end are finish, not steps - the
Ø80 dimension line on the drawing is drawn across the rear band. Only the two Ø8 water fittings near
the rear obstruct anything, and they sit above where the upper clamp goes.

⚠️ **The 52 and 25 are read off a listing drawing, not measured.** The body length is the one that carries the
design and it has margin to spare (see the Z plate below), so this does not need confirming before the
plate is cut - but mic the nose stack before anything depends on the *vertical* arm.

## 📌 Why 2.2 kW and not 3 kW - the choice was made and reversed deliberately

A Ø100 3 kW unit was considered on 2026-09-30 and **rejected**. It is recorded because the reasoning
governs any future spindle change, not because the part is interesting:

- **Power is not the limit on this machine.** Aluminium's specific cutting energy is ~0.7 J/mm³, so a
  respectable adaptive cut for a router of this class - 6 mm three-flute, 18,000 rpm, 6 mm deep ×
  1.5 mm wide, ~24 cm³/min - draws about **0.3 kW at the cutter**. Consuming 2.2 kW in aluminium would
  need ~190 cm³/min, which is machining-centre territory. **Both spindles are five to seven times
  more powerful than the cut this frame can take.**
- **Rigidity is the limit, and Ø100 makes it worse.** The bigger clamp puts the bore centre ~75.5 mm
  off the mounting face instead of 50, taking the gantry moment arm from **187 mm to ~212 mm**, while
  roughly doubling the moving mass. More mass on a longer arm lowers the natural frequency and the
  chatter threshold - it spends capability on the axis that binds to buy it on the axis that doesn't.
- **It cost travel and plate width too:** a Ø100 clamp is 169 mm across the flanges, forcing a 180 mm
  Z plate and **13 mm of X travel at each end**, and its blank flanges would have put the mounting
  bolts *outboard* of the spacer centrelines rather than inboard.

**The one honest argument for 3 kW is hardwood** - a large surfacing or profile cutter genuinely can
pull 2 kW plus. If this machine's work shifts that way, that is the trigger to revisit, not aluminium.

## The offset from the X beam to the spindle centreline: 109 mm

🔴 **This is the moment arm.** It is the number that turns cutting force into gantry deflection, and
it was a placeholder in every calculation in this repo until now.

**From the X carriage plate's front face:**

| | |
|---|---|
| Z rails, bearing blocks and the spacers | 46.5 mm |
| Z plate, 1/2" | 12.7 mm |
| Clamp mounting face to the 80 mm bore centre (half of 100 mm) | 50 mm |
| **To the spindle centreline** | **109 mm** - ⚠️ **~108 after the spacer skim**, see [`z-carriage.md`](z-carriage.md) |

⚠️ **That reference is the carriage plate, not the beam.** The X carriage plate is itself bolted to
the X-axis bearing blocks, so from the **X beam's front face** add the X rail-and-block stack
(30 mm, measured) and the carriage plate (12.7 mm):

| | |
|---|---|
| X beam front face to spindle centreline | **~152 mm** |
| X beam **neutral axis** to spindle centreline (add ~35 mm) | **~187 mm** |

**~187 mm is the arm for gantry bending**, and at 1000 N that is **~187 N·m**. ⚠️ Confirm the
reference before this is used for anything - the 109 mm and the 152 mm differ by a whole rail-block-
plate stack and are easy to interchange.

⚠️ **Still missing: the vertical arm.** The 109 mm converts a *vertical* cutting force into gantry
torsion; a *vertical* offset converts a fore-aft force into the same. That vertical figure is **the X
beam centreline down to the spindle nose with Z retracted, plus Z travel** - not "tool tip", which
moves with Z position, tool length and stickout and is not a machine dimension. Even with it, 8020
publish Ix and Iy for `30-6060` but not J, so any torsional number stays an estimate.

---
