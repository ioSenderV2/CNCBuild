# Egg crate, not blocking

> **Lifted out of `torsion-box.md` on 2026-10-11, when that file was archived.** The
> archived prose walked through dimension chains the registry now owns, and it
> kept going stale against them. This is the part that does **not** reduce to
> symbols - the comparison, the rejected option, the reason a shape was chosen.
>
> **Numbers here are comparative, not specifications.** They weigh one option
> against another; they do not define a part. For any dimension of a part the
> registry is the authority - see [`../dimensions/VALUES.md`](../dimensions/VALUES.md).

### The ribs are egg crate - half-lapped both ways, not blocking

> NOTE: **"Blocking" means two different things in this repo and they are one section apart.** Here it
> is a **construction method for the grid** - full-length ribs one way with short pieces fitted
> between them the other - and it was rejected. Elsewhere it means **local packing under a part that
> bears on the skin**, which is a separate question, asked of the fins and the rear plate and
> answered independently. Rejecting the first says nothing about the second.

SETTLED: **Decided 2026-09-30.** Continuous ribs in both directions, half-depth notches at every crossing.
The alternative considered was full-length ribs one way with blocking between them the other.

**Why, for this box specifically:** the three support points put the front-centre post half a machine
width inboard of the front corners, so load has to travel **diagonally** to reach it. That needs
two-way plate action, and only continuous ribs both ways give it. Blocking would make one axis a
proper continuous web and the other a row of **butt joints** - plywood edge glued to face, at every
junction - leaving a strong axis and a weak one.

Two build reasons reinforce it: an egg crate **self-jigs**, assembling square and holding its own
spacing with no clamps, so the whole grid can be checked flat on a reference before either skin goes
on; and only the notch positions are critical, where blocking needs every piece cut to length with
the errors accumulating.

#### Five things to get right

1. **Cut the notches to 18 mm — the sheets in hand mic 18, to five thousandths.** Sheet sold at a
   nominal commonly runs under and varies between sheets, so test-cut on scrap **from the same sheet**
   before cutting the set. Too tight splits the rib; too loose leaves no glue line. **The width is
   set by where the nibbling stops rather than by a cutter's thickness** - see the notch procedure in
   [`assembly.md`](assembly.md#cut-the-notches-with-all-eight-ribs-clamped-as-one-stack), which cuts
   all eight ribs as one clamped stack on the sliding miter saw.
2. **Notch depth half, and the two directions of error are not symmetric - err DEEP.** SETTLED:
   **This read the other way round until 2026-10-15 and it was wrong.** It said a set cut slightly
   deep "sits low and loses contact with a skin along its whole length". It cannot: **the ribs stand
   on the bottom skin**, so an over-deep notch leaves the rib exactly where it was and only opens a
   gap notch floor to notch floor, which carries nothing - the structural glue lines are rib edge to
   skin. It is **under**-depth that holds a mating rib up off the bottom skin and leaves the top skin
   bearing on half the grid. FLAG: **The claim survived because nothing had tested it** - it was
   written from the shape of the joint rather than from a part, and his practice pair is what closed
   it. **Exactly half is still what makes the eight ribs one part**: at 50 of 100 a rib turned upside
   down is a rib notched from the other edge, so one stack serves both directions.
3. **A step at a crossing that closes when the rib is pressed flat is the rib's bow, not the saw.**
   SETTLED: **His test, 2026-10-15.** A released rib bows slightly in its own plane - plausibly from
   the notching itself, which unbalances the sheet's locked-in stresses toward the notched edge -
   and that lifts a station off the reference and shows a step that is not in the part. Two
   consequences: **check every crossing pressed flat**, and **measure notch depth on a released rib
   rather than on the clamped stack**, because 144 of plywood in clamps reads straight whatever the
   ribs do when they come out. NOTE: **The bow does not survive assembly** - 32 crossings and two
   perimeter webs pull every rib straight, and then both skins lock it.
4. FLAG: **Notch the bottom edge of every rib** where it meets the bottom skin, roughly 20 × 15 mm. An
   egg crate seals every cell, so without this a corner residue has nowhere to go but its own port.
   Every bay has its own port now, so this is no longer what makes draining possible - it is kept
   because it is one more cut on the stack and it lets a residue find a neighbouring port. **It is
   also the only cut that tells a rib which way up it goes**, so it comes after the notching. See
   Transport.
5. **Clamp the skins hard onto the rib edges.** That edge-to-face glue line is where the sandwich
   action lives. Screws through the skins into the ribs are the simplest way to get uniform
   pressure, and they can stay in.

#### What the tenons ask of the grid

Less than it first appears, and the two cases are different:

| Post | Where its tenon sits | What the grid must do |
|---|---|---|
| **Rear left / rear right** | **Hard in the box corner**, snug against both perimeter walls - the ledges put its outer faces exactly on the walls' inner faces | Only that the **first interior rib in from each perimeter clears it**. It is not a mid-cell case at all |
| **Front centre** | Against the front wall, **mid-span along it** | The two front-to-back ribs either side must **clear the 86 mm width**. This is the only mid-cell case |

So the corner tenons constrain nothing but the first rib offset, and they are **laterally located by
the two walls** for free. Only the front-centre tenon has to be placed between ribs deliberately - and
it is also the only one wanting blocking, since the corners already have walls on two sides.

Conventional torsion-box spacing is 200-300 mm; that is convention rather than calculation, and it
should bend to the front-centre tenon rather than the other way round.
