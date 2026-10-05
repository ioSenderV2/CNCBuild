# Drawings

**This folder is a convention change, made on purpose on 2026-09-30.**

Until now this repo had no drawings. The premise was that **the reasoning is the artifact** - prose
that says *why* a dimension is what it is survives a redesign, where a drawing does not. That premise
still holds for everything in `machine/*.md`, and those files remain the **source of truth**.

What forced the addition is the **one machining trip**. Prose cannot be taken to a mill. Two things in
particular are hard to carry in words and easy to get wrong later - the **riser geometry** and the
**three-point pad layout relative to the five legs** - and that was already flagged as a decision to
make deliberately rather than drift into.

## The rules this folder follows

- **Derived, never authoritative.** If a sheet and a `.md` file disagree, **the `.md` file wins** and
  the sheet is stale. Nothing is specified here for the first time.
- **Hand-authored SVG, inline in one HTML file.** No CAD dependency, no binary blobs, and it diffs.
  Print to PDF from a browser when a paper copy is wanted - the same route the Mega-XL build doc in
  the ioSender repo uses.
- **Unknowns are marked, never invented.** Amber rows are dimensions that do not exist anywhere in the
  repo. That is the repo's standing rule applied to drawings: an unknown stays unknown until it is
  measured.
- **One datum per plate, absolute coordinates, never chained.** The mill is manual in X and Y, so the
  operator types coordinates and chained dimensions accumulate error.
- **Extrusion corner-bore patterns are transfer-punched, not dimensioned.** Those are extruded
  features with looser position tolerance than anything drilled in plate.

## Files

| File | What it is |
|---|---|
| [`shop-pack.html`](shop-pack.html) | Four plate sheets plus a pre-trip checklist and pack list. Open in a browser, print to PDF |

## Status

**Regenerated through 2026-10-02**, after the Y end rework: cast stepper frames replaced BK12 and
the M5 standoffs, the Y steppers moved to the **front**, all four as-built Y risers are scrapped, and
the two rear risers became one 1200 mm × 12" × 1/4" A36 steel plate that is also the rear shear
panel. Every sheet in the pack has been brought up to that design.

### What is in the pack

| Sheet | Part | Note |
|---|---|---|
| 1 | Front Y end plate / Z riser | Regenerated 2026-10-02 — the 100 → 200 taper on the 302 mm square, the 60.5 × 50 window, columns 35 / 65 |
| 2 | X gantry end plate | Regenerated. Only the **right-hand** plate carries the BF12 tongue, so the two are not interchangeable |
| 3 | X carriage plate | 154 × 407, untouched by the rework and still correct |
| 4 | Z plate | **164** × 175 — corrected from 154; at 154 eight M5 counterbores break through the plate edge |
| 5 | Y nut doubler and sole bracket | Added 2026-10-02 |

### ⚠️ Not drawn yet - two trip parts have no sheet

- **The cast stepper frame interposer** - 60 × 150 × 3/8" 6061, **quantity 3** (Y1, Y2 and the X stepper
  end), one drawing. Six M8 clearance into slide-in T-nuts at rows 82 / 110 / 138, six M5 tapped for
  the casting at bar coords 28-71, no counterbores. **Fully dimensioned in the prose and simply not
  drawn here.**
- **The 1200 mm rear plate** - 1200 × 12" × 1/4" A36 steel, one for both Y beams: the 16-bolt beam
  pattern, the 8-bolt box row at Y 30, and **BF12 face-mounted on 4 × M5** per beam.

### 📋 In progress: a 1/2" baltic birch mockup

Being cut while the mill visit is a couple of weeks out, **Sheet 1 first**. It settles the window's
height - the 50 mm is a budget and the casting projects only about 20 mm below the bar - and the
spindle clearance that gates the taper cut, which is one bandsaw pass and cannot be put back.

🔴 **Plywood is for fit, never for transfer.** Its thickness runs under 12 mm and varies, and an M5
threaded insert needs a far larger bore than a 4.2 mm tap drill - so anywhere the design has fought
for edge distance or web, an insert will not sit where the real hole does. **A plywood plate must
never go to the mill as a template**: this folder is derived-never-authoritative, and a physical part
is far more persuasive than a sheet.

### What still gates drilling

⚠️ **No plate in this pack has a complete hole schedule yet**, and that is the pack's main finding.
What it does have is every dimension the repo actually holds, with the gaps named - which turns
"design ahead of the build" from an instruction into a list. Two questions gate cuts that cannot be
undone, and each needs a part or the mill in front of you - see
[`../open-items.md`](../open-items.md):

1. How far past the front riser plane the spindle reaches, and whether it fouls the widened fin at
   low Z
2. The mill's model, and whether its DRO is 2-axis or 3-axis

📌 **The merged build document exists now** - `tools\make-pdf.ps1` builds `build-document.pdf`, the
twelve `machine/*.md` in reading order with every photograph embedded. It links to the sheets here by
their anchors. It does **not** contain them: the pack is regenerated on its own cycle, and that is
deliberate.
