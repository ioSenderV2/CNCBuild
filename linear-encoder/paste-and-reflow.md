# Pasting and reflowing the boards

One sheet for both boards: the **sensor board** (two sides) and the **CAN controller
board** (bottom only). Read it with the paste warming on the bench.

What is in play: **Alpha OM-5100 leaded paste** (35 g syringe), **4 mil stainless
stencils**, the **30 mil plastic spreaders**, tweezers, the **hot plate**, isopropyl
and lint-free wipes. The sensor board uses the **MDF jig** - Forstner recess, two
3 mm pins through the mounting holes and the stencil's matching holes. The controller
board uses the **acrylic jig set** that came with its stencil.

## How long you actually have

**Hours, not minutes.** A 15-minute rush is not real - this class of leaded no-clean
paste stays workable on the board far longer than any one session needs:

| Stage | Window | What actually goes wrong past it |
|---|---|---|
| Syringe out of the fridge | warm **30-60 min before printing** | cold paste prints ragged and tears coming off the stencil |
| Printed deposits, waiting for parts | **a few hours** | deposits slowly dry out and lose their stick |
| Parts placed, waiting for the plate | **a few hours** | same - the tack that holds parts fades |
| Overnight | no | dried paste wets badly; wipe it off and print again |

So: print, place at a comfortable pace, reflow in the same sitting. If life
interrupts and a printed board has sat long enough to look dry or doubtful, the
reset costs two minutes - **wipe the board clean with isopropyl, dry it, print
again.** Never reflow a doubtful print; cleaning up bad joints costs far more.

## Set up the board

The stencil has to lie dead flat on the board, and neither can move.

- **Sensor board:** drop it into the MDF recess over the two pins, stencil onto the
  same pins. **Push board and stencil toward the same corner before every pass** -
  the pins have a few tenths of play, and one corner makes all four boards print
  the same.
- **Controller board:** board into the acrylic jig pocket, jig taped to the bench.
  Lay the stencil on, slide it under good light until every opening sits centered
  on its pad, then **tape one full edge of the stencil down as a hinge** - from then
  on it lifts for inspection and drops back aligned.

## Print the paste

1. Push out a bead along the hinge edge, **just outside the openings** - about
   pencil thickness, a little wider than the pad field. Generous is right; the
   excess stays on the stencil.
2. Spreader at **45-60 degrees, one firm continuous pass** across every opening.
   The stencil should be wiped clean behind the stroke. The foil thickness meters
   the paste - even pressure matters, force does not.
3. A missed spot gets **one more full pass**. Never dab at a single opening.
4. **Peel straight up**, pivoting on the hinge or lifting off the pins - a clean
   vertical lift, not a slide.
5. Look at the result: **crisp separate bricks of paste, one per pad.** Paste
   smeared between pads means wipe the board with isopropyl and print again.
6. **Wipe the stencil both sides with isopropyl now**, not after reflow - paste
   dried into the openings is miserable to clear.

## Place the parts

Tweezers, one part at a time, pressed just far enough in that the paste grips it.
Close is good enough - when the solder melts, surface tension pulls every part
square onto its pads. There is no clock running; get each one roughly centered and
move on.

- Sensor board: the **chip side goes first** - set the chip's pin-1 corner against
  the board marking before pressing it in.
- Controller board: all 18 passives in one pass - 12 small caps, the 0805, the
  100 nF, the four resistors.

## Reflow on the hot plate

Watch the solder, not the dial.

1. Board goes on the plate. Sensor board second side: board sits on the **short
   pipe** so the already-built chip side hangs clear; the copper still carries the
   heat. Pipe end faced flat so the board sits level.
2. Bring the plate up. The paste goes dull and slumps first, then **flows bright
   silver and every part settles and pulls itself square** - that is the melt,
   183 C at the joints.
3. **Count a few seconds after the last joint flows**, then take the heat away -
   slide the board gently off, or plate off. Do not touch any part until the
   joints freeze; it takes seconds.
4. First board of a batch is the pilot: find the dial setting that gets flow in a
   few minutes, write it on this sheet, photograph the placed and the reflowed
   board, and run the rest against the photos.

Dial setting that flows in a few minutes: ______________

## After reflow

- Every joint shiny with a small fillet, every part sitting flat. A bridge between
  pads comes off with the iron and wick.
- The paste is a no-clean type: residue can stay. Isopropyl if it should look nice.
- Syringe capped and back in the fridge. Jig and spreader wiped.

## The jacks go on last, with the iron - they never ride the plate

**Sensor board - the jack is surface-mount, soldered by iron.** The metal on this
jack is the **eight signal fingers** - each finger's tip lands flat on its gold
pad - and the **one wide shield tab** on the other side, which lands between the
two gold shield pads and catches about a millimeter of each. That geometry is
the manufacturer's own recommended layout: the shield joint is a **fillet at
each end of the tab where it crosses a pad**, never a buried tab, and the
stamped holes in the tab sit over bare board and do nothing. Wire solder brings
its own flux.

1. **Tin one corner finger's pad** lightly - finger 1 or finger 8, a small
   amount.
2. **Set the jack down, hold it flat, and tack that finger** - reheat the tinned
   pad against the finger's tip, hold still a second while it freezes.
3. **Check all eight fingers sit centered on their pads.** Off? Reheat the one
   tack and nudge - that is what tacking one joint first is for. Then tack the
   opposite corner finger; the jack is now fixed and square.
4. **The shield tab, one end at a time** - iron on the exposed gold outboard of
   the tab, solder fed right at the tab's edge, until a fillet climbs from pad
   onto the tab. The tab is continuous with the whole shell and drinks heat:
   big tip, hold longer than feels natural, flux helps.
5. **The remaining fingers, one at a time** - tip touching finger and pad
   together, feed a little solder, one second each. A small shiny fillet
   climbing from pad onto finger is right. A bridge between neighbours comes
   off with wick.

**Controller board - the jacks and the socket stack are through-hole.** Pins
through the board, soldered from the far side; the filter parts sit well back
from the pin rows so the iron has room. Same tack-one-pin-and-check habit: one
pin, check the part is seated flat and square, then the rest.
