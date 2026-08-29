# Controller board (daughter board)

Four shielded RJ45 jacks fanned out to the ESP32-S3's GPIOs, on a board that sits over the
**ESP32-S3-RS485-CAN** module and mates with its 20-pin header. The controller end of the wiring
described in [`design-can-position-feedback.md`](design-can-position-feedback.md) §14; the sensor end is
§14's *sensor board*.

Status: **design sketch, 2026-08-25. Nothing ordered, nothing laid out.**

---

## ⚠️ The jacks must NOT have integrated magnetics

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

**Four discrete jacks, 15.6 mm wide, on a 16 mm pitch = 64 mm** (ordered 2026-08-25). A ganged 1x4 in a
single shielded housing was looked for and **not found**, so discrete it is. 64 mm against the 67-68 mm
budget leaves ~1.7 mm of board edge at each end - comfortable for fab clearance.

At 16 mm pitch the metal shells sit **0.4 mm apart**. Electrically that is a non-event: all four shields
are the same net, so contact changes nothing. Mechanically, check the footprint's recommended spacing so
the shells seat rather than fouling each other.

| Stack | |
|---|---|
| Daughter board underside | **14 mm** |
| PCB | 1.6 mm |
| RJ45 jack | ~13.5 mm |
| **Total above the module** | **~29 mm** |

The board underside sits 1 mm below the top of the 15 mm terminal blocks, and the jacks stand ~14 mm
proud of them, so cable access is clear.

### The interconnect problem: 5 mm pins, 14 mm standoff

The male header stands only **5 mm** proud; the board must sit at **14 mm** to clear the tallest
blocks. **A taller socket does not solve this** - a socket's contact springs are near its mating face,
so a tall socket still grips only in its first few millimetres and the pins fall **9 mm** short of the
contacts. The height has to come from somewhere else:

| Option | Verdict |
|---|---|
| **Riser PCB** - male 2.0 mm down, female up, **14 mm** standoffs | **Preferred.** Keeps everything inside the measured footprint, which matters when recessed between two 15 mm walls. One more small board on an order already being placed. |
| **Ribbon jumper** - 2x10 2.0 mm IDC each end, board on standoffs | Works, and frees the jacks to be **panel-mounted** so cables plug in from outside the enclosure. But the ribbon has to escape the slot between the terminal blocks and be anchored. |
| Replace the module's header with taller pins | 20 pins of desoldering at 2.0 mm pitch on a board that is not easily replaced. Only if the stacked form factor is mandatory. |

**2.0 mm stacking/pass-through headers barely exist** - in 2.54 mm this would be a catalogue part. That
absence is the whole reason this is awkward.

> ⚠️ **The header is 2.0 mm pitch, not 2.54 mm.** Easy to order wrong; the wrong part is unusable.

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

**Jacks lie across the 20 mm width, openings facing out one long side. The module's terminal blocks
face out the two ends.** So the two never conflict, and check 5 is closed.

The consequence is that **jack depth is now spent against the 20 mm width**, not the length. The
listing's 16 mm is the *width* (4 x 16 = 64 mm along the board); depth is unpublished and right-angle
RJ45s commonly run ~21 mm - hence check 7. Cables also exit sideways now, so there must be room beyond
the module's long edge for the plug, its boot and the cable's bend radius.

## Board outline

**67-68 mm x 20 mm.** The width is fixed at 20 mm to match the module rather than chase extra room -
and it does not need to grow, because the jack is **18.2 mm deep** and fits inside it with 1.8 mm to
spare. No overhang, though up to ~1 mm would have been accepted if it had come to that.

| | |
|---|---|
| Four jacks at 16 mm | 64 mm, against 67-68 mm of length |
| Jack depth 18.2 mm | against 20 mm of width, **1.8 mm spare** |

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

0. **There is no bulk decoupling on this board's `3V3`, and there probably should be.** The netlist's
   twelve capacitors are all 330 pF-1 nF RC filters on *signal* lines; `+3V3` carries only
   `J1.4 J2.4 J3.4 J4.4 J5.1` and the four pull-up tops - **not one capacitor**. Four cables fan out
   from a single header pin with nothing local to supply a transient, and each sensor's own
   `100 nF + 10 µF` sits 2.4 m away at the far end of its cable, which is exactly where it *cannot*
   help this end. Proposed: **10 µF + 100 nF at P1 pin 1**, before the fan-out. Cheap, two parts, and
   the alternative is finding out on a bench with four sensors hot-plugging one at a time.
   Not yet in the schematic - decide, then add it there and to `netlist.txt` together.

1. ~~Does the 20 mm width constraint relax at 12 mm?~~ **Moot - the board stays 20 mm** (decided
   2026-08-25, matching the module) and the 18.2 mm jack depth fits inside it. See *Board outline*.
2. ~~Do the terminal blocks' screws face up?~~ **No - they are accessed from the ENDS of the module,
   not the sides or top** (confirmed 2026-08-25). Overhanging their sloped backs blocks nothing, so the
   board can take the full 67-68 mm without giving any length back.
3. ~~Tallest component / standoff height~~ **Settled 2026-08-25.** Tallest component in the footprint
   is **12 mm** (the 15 mm terminal blocks sit outside it, at the ends); **standoff set to 14 mm**, so
   2 mm of clearance. Costs nothing - the sloped backs mean more height gives more length, not less.
4. ~~Confirm no integrated magnetics~~ **Confirmed 2026-08-25: none.** The listing's photographs show
   **eight signal pins plus two shield tabs and nothing else**. Magnetics cannot hide - transformers
   need centre-tap pins - so a bare 8+2 pin field settles it.
5. ~~Which way the jack openings face~~ **Settled 2026-08-25** - see *Orientation* below.
6. ~~Where does P1 sit, and does its pin field clear the jacks'?~~ **Resolved 2026-08-25 by
   measurement - 3 mm of clearance.** See *The header-versus-jack collision* below.
7. ~~Reconcile the jack's two published dimensions~~ **Settled 2026-08-25: 16 mm is the WIDTH,
   18.2 mm is the LENGTH (depth).** The favourable reading was the right one - four jacks need 64 mm of
   the 67-68 mm length, and 18.2 mm of depth clears the 20 mm width with 1.8 mm spare.
