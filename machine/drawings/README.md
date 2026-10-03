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

🔴 **STALE as of 2026-10-02. The pack has not been regenerated and must not go to the mill.**

The Y end design was reworked that day: cast stepper frames replaced BK12 and the M5 standoffs, the
Y steppers moved to the **front**, all four as-built Y risers are scrapped, and the two rear risers
became one 1200 mm × 12" × 1/4" A36 steel plate that is also the rear shear panel. **Every riser
sheet here is superseded**, three parts were added to the trip, and the materials changed.

This is the folder's own rule firing exactly as designed - derived, never authoritative, and the
`.md` file wins. See [`../open-items.md`](../open-items.md),
which lists the four measurements that gate cuts which cannot be undone. **Regenerate
before the visit.**

⚠️ **No plate in this pack has a complete hole schedule yet**, and that is the pack's main finding.
What it does have is every dimension the repo actually holds, with the gaps named - which turns
"design ahead of the build" from an instruction into a list.

The full merged build document - all four `machine/*.md` as one PDF with general-arrangement
drawings - is the next artifact, and is not started.
