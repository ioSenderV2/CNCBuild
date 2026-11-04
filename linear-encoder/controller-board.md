# Controller board (daughter board)

Four shielded RJ45 jacks fanned out to the ESP32-S3's GPIOs, on a board that sits over the
**ESP32-S3-RS485-CAN** module and mates with its 20-pin header. The controller end of the wiring
described in [`design-can-position-feedback.md`](design-can-position-feedback.md) §14; the sensor end is
§14's *sensor board*.

Status: **design sketch, 2026-08-25. Nothing ordered, nothing laid out.**

---

## OPEN: The jacks must NOT have integrated magnetics

Most 4-port RJ45 assemblies sold for Ethernet are **MagJacks** - transformers inside. Transformers
**block DC**, and every signal here is DC-coupled: `A`, `B`, `MagDECn` and the 3.3 V feed. With
magnetics fitted **nothing works at all** - not degraded, dead - and it costs a board spin to discover.

Required: **shielded, no magnetics.** Shielded is correct at *this* end, because this is where the cable
screen grounds (§14). It is the magnetics that must go, not the shield.

## Mechanical envelope

The module is 85 mm long with a **15 mm terminal block at each end**; the gap between them is 64 mm at
board level. Their back faces slope away, so the usable length grows with height:

| At height | Usable length |
|---|---|
| board level | 64 mm |
| 12 mm | 67-68 mm |
| **14 mm (the chosen standoff)** | **>= 67-68 mm** |

67-68 mm was measured at 12 mm and is a **floor, not a ceiling** - the terminal blocks' backs slope
away, so the 14 mm standoff gives slightly more. Kept at 67-68 mm as the conservative figure.
**Settled 2026-11-04 by measurement: the board maximum is 67 x 19.5** - see *Board outline*.

**Four discrete jacks, 15.6 mm wide, on a 16 mm pitch = 64 mm** (ordered 2026-08-25). A ganged 1x4 in a
single shielded housing was looked for and **not found**, so discrete it is. 64 mm against the 67-68 mm
budget leaves ~1.7 mm of board edge at each end - comfortable for fab clearance.

At 16 mm pitch the metal shells sit **0.4 mm apart**. Electrically that is a non-event: all four shields
are the same net, so contact changes nothing. Mechanically, check the footprint's recommended spacing so
the shells seat rather than fouling each other.

| Stack | |
|---|---|
| Daughter board underside | **~12.9 mm** (the three-socket totem below; 14 was the old working figure) |
| PCB | 1.6 mm |
| RJ45 jack | ~13.5 mm |
| **Total above the module** | **~28 mm** |

The jacks stand well proud of the 15 mm terminal blocks, so cable access is clear.

### The interconnect problem: 5 mm pins, a ~13 mm standoff

The male header stands only **5 mm** proud; the board must sit high enough to clear the tallest
component (**10.5 mm, measured** - the relay-looking isolation brick). **A taller socket does not
solve this** - a socket's contact springs are near its mating face, so a tall socket still grips
only in its first few millimetres and the pins fall far short of the contacts. The height has to
come from somewhere else. **Settled 2026-11-04: the three-socket totem below.** The options it
beat, kept for the record:

| Option | Verdict |
|---|---|
| **Riser PCB** - socket down onto P1, male up, standoffs | Was the preference until the totem replaced it - the totem is the same idea with the PCB deleted. Falls back here only if the totem fails its bench checks. |
| **Ribbon jumper** - 2x10 2.0 mm IDC each end, board on standoffs | Works, and frees the jacks to be **panel-mounted** so cables plug in from outside the enclosure. But the ribbon has to escape the slot between the terminal blocks and be anchored. |
| Replace the module's header with taller pins | 20 pins of desoldering at 2.0 mm pitch on a board that is not easily replaced. Only if the stacked form factor is mandatory. |

**2.0 mm stacking/pass-through headers barely exist** - in 2.54 mm this would be a catalogue part. That
absence is the whole reason this is awkward.

> OPEN: **The header is 2.0 mm pitch, not 2.54 mm.** Easy to order wrong; the wrong part is unusable.

### Riser part numbers - sourced 2026-11-04, datasheets committed

Both Sullins, both in stock at Digi-Key, drawings in
[`../manufacturer-assets/`](../manufacturer-assets/index.html):

| Part | What | Key figures (from the committed drawings) |
|---|---|---|
| **NPPN102AFCN-RC** | 2x10 female socket, 2.0 mm, through-hole | insulator **4.30** tall, tail 2.40, accepts 0.50 sq posts, ~$1.56 |
| **NRPN102PAEN-RC** | 2x10 male header, 2.0 mm, through-hole | insulator **2.00**, mating post **3.60±0.20**, tail 2.80, 0.50 sq, ~$0.69 |

The two series mate with each other by the female drawing's own note 11.

### The plan: a three-socket totem, no riser PCB - his, 2026-11-04

Three NPPN102AFCN-RC stacked, all receptacle-down. The first plugs onto P1; each next one plugs
onto the 2.40 mm tails of the one below (tails are 0.50 sq - exactly the post the socket is rated
for, so the socket-on-socket joints are within the part's own spec); the third one's tails solder
into this board. No riser PCB, no male header, one part number. Three butted 4.30 bodies put the
board's underside at **12.9**, clear of the tallest component on the module - **10.5, the
relay-looking isolation brick, his measurement** - by 2.4. The NRPN male header stays in the
table above only as the fallback part if the totem fails its bench checks.

**P1 as measured, 2026-11-04 - and the one joint that is out of spec:**

| | |
|---|---|
| Pitch | **2.0 mm confirmed**: ten-pin span 18.46 mm |
| Pin size | **0.6 (caliper) / 0.67 (micrometer)** square |
| Pin length proud | 5 mm |

The socket is rated to accept **0.50 ± 0.05 sq**, so the bottom joint - the socket that grips
P1 - is asking a 0.5-rated contact to take a ~0.64 pin. The joints above it are unaffected.

> OPEN: **the bench test decides the bottom joint.** Four sockets ordered 2026-11-04, $16.50
> delivered price, not yet shipped (his call - "easy enough to order a couple just to see how
> they work").
> What the test has to show, on the module with the header supported so insertion force does not
> work the header's own solder joints: the entry funnel admits the 0.64 pin at all, the socket
> seats, continuity on all 20, and it still grips on a second mating. A socket that takes a set
> on P1's fat pins is acceptable - that socket lives on P1 forever - but it must not need enough
> force to damage the module. If it fails: either a 2 mm female from the same ecosystem as the
> module's header (the no-name 2x10s sold alongside these modules will be sized for these pins -
> measured on arrival, like the FMHXG), or a small riser PCB with ø1.0 holes soldered permanently
> onto P1's pins (the 0.64 pin's diagonal is ~0.9, so the earlier ø0.8 figure does not clear),
> with the separable Sullins joint moved to its top.

> OPEN: **one more bench check before the board is committed.** Tail engagement: the 2.40
> tail against a contact point that reads as ~1.45 below the mating face on the drawing -
> interpreted, not measured - so mate two sockets, continuity plus a tug.

**The fillets under jack 1: clipped flush - his call, 2026-11-04.** The third socket's tails
solder on the board's top face, and P1's position puts those 20 joints under jack 1's body,
which stands off the board only 0.1 mm. Resolution: solder the socket, clip the joints flush
with flush cutters, re-wet each sheared face with the iron, dress proud ones with a file -
target is below the plane of the jack's own pads. The assembly order makes it checkable:
socket first, straightedge across the area (if it rocks, dress again), jack last by iron, same
order as the puck. Joint strength lives in the plated barrel, so the clipped dome costs
nothing. A look at a real jack's underside is still worth taking when one is in hand - a
recess there is free margin - but it no longer gates anything.

The stack height is measured off the standing totem before the standoffs are cut: if P1's 5 mm
pins cannot pass out the tail side of the first socket, the whole totem rides 0.7 proud (board
at ~13.6 instead of 12.9). Either way clears the brick; the standoffs just get cut to what is
measured.

## The ordered part

**FMHXG `RJ45NMCCFC-90D-10`** (ASIN `B0BRQ2R8HW`), ordered 2026-08-25 as a 10-pack:
*"Shielded RJ45 8P8C 90 Degree Angle Network Modular Connector for PCB, CAT5/5e/6"*. 16 mm listed
length; 15.6 mm body on a 16 mm pitch (above).

**Magnetics: none. Confirmed.** The listing's photographs show the PCB side carrying **eight signal
pins plus two shield tabs, and nothing else**. That is decisive rather than suggestive: integrated
magnetics cannot be hidden, because transformers need centre-tap pins brought out - a MagJack shows
12-16 pins and usually LED pins too. The supporting signals all agree: **"8P8C"** describes exactly
eight contacts, magnetics is an expensive selling point nobody omits from a title, a 10-pack at this
price is plain-jack territory, and `RJ45**NM**...` plausibly reads as *No Magnetics*.

**90 degree = right-angle**, so the openings face sideways and cables exit horizontally out the long
edge rather than upward. That suits a board recessed between two 15 mm terminal blocks - nothing needs
to clear overhead - but it makes the ~21 mm typical depth of a right-angle jack collide with open
check 1, and it makes the facing direction a decision (check 5).

There is **no manufacturer datasheet** for this part, only the marketplace listing, so dimensions and
the footprint will have to be measured off the parts themselves.

## Orientation

**Jacks lie across the 19.5 mm width, openings facing out one long side. The module's terminal blocks
face out the two ends.** So the two never conflict, and check 5 is closed.

The consequence is that **jack depth is now spent against the 19.5 mm width**, not the length. The
listing's 16 mm is the *width* (4 x 16 = 64 mm along the board); depth is unpublished and right-angle
RJ45s commonly run ~21 mm - hence check 7. Cables also exit sideways now, so there must be room beyond
the module's long edge for the plug, its boot and the cable's bend radius.

## Board outline

**67 mm x 19.5 mm - his measurement, 2026-11-04: the maximum that fits between the two terminal
blocks.** This supersedes the earlier 67-68 x 20 working figure. The jack is **18.2 mm deep** and
fits inside the 19.5 with 1.3 mm to spare. No overhang.

| | |
|---|---|
| Four jacks at 16 mm | 64 mm, against 67 mm of length - 1.5 mm per end |
| Jack depth 18.2 mm | against 19.5 mm of width, **1.3 mm spare** |

The jack body does sit over the header's area - the header starts 16 mm from the back edge, i.e. 4 mm
from the front, and an 18.2 mm deep jack reaches to 1.8 mm from the back. That is harmless: the header
is on the **bottom** face and the jacks on the **top**, so only the through-hole pin fields have to
clear each other, and they do by 3 mm (below).

## The header-versus-jack collision

Four jacks at 16 mm pitch use 64 mm of the 67-68 mm length. That leaves **3-4 mm total**, nowhere near
enough to place the 2x10 header beside them - so the header has to sit **underneath** the jacks: female
header on the bottom, jacks on top. Fine in principle, except **both are through-hole**, so their pin
fields must not overlap in X-Y.

And the header's position is not a free choice: it must align with **P1, which sits in a corner** of the
free area - exactly where jack 1 wants to be.

### Resolved by measurement, 2026-08-25 - there is no collision

Measured across the 20 mm width, from the back edge:

| Feature | Distance from back edge |
|---|---|
| RJ45 eight signal pins | at the **back** of the jack, well clear |
| RJ45 shield tabs - the nearest feature | **13 mm max** |
| 2x10 header begins | **16 mm** |
| **Clearance** | **3 mm** |

The header sits in the front ~4 mm strip, flush with one corner, and every RJ45 through-hole feature
stays behind 13 mm. The shield tabs were the only things that came close and they miss by 3 mm.

**So the riser stands.** The collision was the one thing that would have forced the ribbon; with the
header free to align with P1 as originally intended, the riser keeps everything inside the measured
footprint. The ribbon remains the fallback, and keeps its own advantage - panel-mounted jacks - if that
is ever wanted for service access.

## Pin map

12 signals - 4 sensors x (A, B, `MagDECn`) - against exactly the 12 free GPIOs, IO3-IO14. No spare,
which is why Z's allocation was reserved rather than spent (§11.9).

Assigned so each header column feeds two adjacent jacks: J1/J2 walk **down** the odd column, J3/J4 walk
**up** the even one, which keeps the fan-out short and free of crossings.

| Jack | Axis | A | B | `MagDECn` |
|---|---|---|---|---|
| J1 | X | IO3 (p9) | IO4 (p11) | IO5 (p13) |
| J2 | Y | IO6 (p15) | IO7 (p17) | IO8 (p19) |
| J3 | A | IO9 (p20) | IO10 (p18) | IO11 (p16) |
| J4 | Z | IO12 (p14) | IO13 (p12) | IO14 (p10) |

Any GPIO reaches any PCNT unit through the ESP32-S3 matrix, so nothing forces A and B onto particular
pins - the grouping is purely for routing.

Header pins used: **1** (3V3), **3, 4** (GND), and **9-20** (the twelve GPIOs). Pins 2 (5V), 5/7
(UART) and 6/8 (USB D+/D-) are **not connected** - see [`hardware-esp32-s3-rs485-can.md`](hardware-esp32-s3-rs485-can.md).

### RJ45 pinout - identical on all four jacks

Straight from §14's pair scheme, so an ordinary straight-through patch cable works end to end:

| Pin | Signal | Pair (T568B) |
|---|---|---|
| 1 / 2 | **A** / GND | orange |
| 3 / 6 | **B** / GND | green |
| 4 / 5 | **3V3** / GND | blue |
| 7 / 8 | **`MagDECn`** / GND | brown |

Every signal travels with a ground return in its own twist - that is what collapses the loop area, and
it is the reason for this specific assignment rather than a tidier-looking one.

## What else is on the board

- **4 x 2.2 kΩ pull-ups**, `MagDECn` to 3V3. The sensor drives these open-drain (§1.3), so the pull-up
  belongs at this end, where the line is read.
- **12 x 330 pF - 1 nF to ground**, one per signal, forming the RC with the series resistors at the
  sensor. At ~10 kHz there is enormous timing margin, so filter hard.
- **Bulk decoupling at P1 pin 1: `C13` 10 µF + `C14` 100 nF**, +3V3 to GND, before the fan-out.
  Decided 2026-11-04 — see the settled item 0 below.
- **Shield link.** Tie all four jack shells together and to GND at **one** point. Fit it as a 0 Ω pad
  with an alternative 1 nF ‖ 1 MΩ position, so the strategy can change without cutting traces.
- **Ground pour** under the signal fan-out. The return path matters more than trace width here.

## Power - the board makes none of it

This board is a **fan-out, not a supply**. `3V3` arrives on **P1 pin 1** from the module and goes
straight out to the four jacks' pin 4 and the four pull-ups. Nothing is regulated here, and there is
no local energy storage - see the open item below.

The chain, read off `ESP32-S3-RS485-CAN-Schematic.pdf` in
[`../manufacturer-assets/`](../manufacturer-assets/index.html):

| | |
|---|---|
| Regulator | **U1, MP1605GTF-Z** synchronous buck (L1 = 1 µH) |
| Input | 5 V - VIN range 2.3-5.5 V |
| Feedback | 0.6 V, R4 200 kΩ ‖ R5 44.2 kΩ, both 1% |
| **Output** | **0.6 x (1 + 200/44.2) = 3.314 V** |
| **Rated** | **Iout max 2 A** |

`U3` (`B0505LS-1W`) is the isolated 1 W DC-DC for the RS485 side only. It does not feed this rail.

**The budget, with numbers rather than "far above it":**

| | |
|---|---|
| 4 x AS5311 at 21 mA max (16 mA typ) | 84 mA (64 mA) |
| 4 x 2.2 kΩ pull-ups, only while `MagDECn` is asserted | 6 mA |
| **Total against a 2 A regulator** | **~90 mA, about 4%** |

Cable drop is a non-issue: 2.4 m of 24 AWG is ~0.4 Ω out and back, so ~9 mV at 21 mA, against an
AS5311 that accepts 3.0-3.6 V on a 3.314 V rail.

**The constraint is upstream of the module, not here.** The MP1605 has room to spare; what feeds the
module's 5 V does not necessarily. On USB-C at 500 mA the ESP32-S3 itself dominates and these sensors
are a modest addition; off the terminal block it is whatever supply is fitted. Size that supply for
the module *plus* ~90 mA, not for the module alone.

## Open - check before layout

0. ~~There is no bulk decoupling on this board's `3V3`~~ **Settled 2026-11-04: added.** `C13` 10 µF
   + `C14` 100 nF, +3V3 to GND at P1 pin 1, before the fan-out - in the schematic and `netlist.txt`
   together, ERC clean, both pins verified on the right nets in the KiCad netlist export. The
   argument that decided it: four cables fan out from a single header pin, and each sensor's own
   `100 nF + 10 µF` sits 2.4 m away at the far end of its cable, exactly where it cannot help this
   end.

1. ~~Does the 20 mm width constraint relax at 12 mm?~~ **Moot - and superseded 2026-11-04: the
   measured maximum is 19.5 wide.** See *Board outline*.
2. ~~Do the terminal blocks' screws face up?~~ **No - they are accessed from the ENDS of the module,
   not the sides or top** (confirmed 2026-08-25). Overhanging their sloped backs blocks nothing, so the
   board can take the full 67-68 mm without giving any length back.
3. ~~Tallest component / standoff height~~ **Settled 2026-08-25, numbers superseded 2026-11-04.**
   The 2026-08-25 figures were 12 mm tallest and a 14 mm standoff; the tallest component now
   measures **10.5** and the board rides the three-socket totem at **~12.9** - see *The
   interconnect problem*. Still ~2.4 of clearance, same conclusion.
4. ~~Confirm no integrated magnetics~~ **Confirmed 2026-08-25: none.** The listing's photographs show
   **eight signal pins plus two shield tabs and nothing else**. Magnetics cannot hide - transformers
   need centre-tap pins - so a bare 8+2 pin field settles it.
5. ~~Which way the jack openings face~~ **Settled 2026-08-25** - see *Orientation* below.
6. ~~Where does P1 sit, and does its pin field clear the jacks'?~~ **Resolved 2026-08-25 by
   measurement - 3 mm of clearance.** See *The header-versus-jack collision* below.
7. ~~Reconcile the jack's two published dimensions~~ **Settled 2026-08-25: 16 mm is the WIDTH,
   18.2 mm is the LENGTH (depth).** The favourable reading was the right one - four jacks need 64 mm of
   the 67-68 mm length, and 18.2 mm of depth clears the 20 mm width with 1.8 mm spare.
