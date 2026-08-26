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
| **12 mm** | **67-68 mm** |

12 mm is where that budget was measured, **not a ceiling** - the sloped backs mean more height gives
more length. Since the tallest component in the footprint also measures 12 mm (check 3), the standoff
will likely need to be 13-14 mm, which only improves the length available.

**Four discrete jacks, 15.6 mm wide, on a 16 mm pitch = 64 mm** (ordered 2026-08-25). A ganged 1x4 in a
single shielded housing was looked for and **not found**, so discrete it is. 64 mm against the 67-68 mm
budget leaves ~1.7 mm of board edge at each end - comfortable for fab clearance.

At 16 mm pitch the metal shells sit **0.4 mm apart**. Electrically that is a non-event: all four shields
are the same net, so contact changes nothing. Mechanically, check the footprint's recommended spacing so
the shells seat rather than fouling each other.

| Stack | |
|---|---|
| Daughter board underside | 12 mm |
| PCB | 1.6 mm |
| RJ45 jack | ~13.5 mm |
| **Total above the module** | **~27 mm** |

The jacks stand ~12 mm proud of the terminal blocks, so cable access from above is clear.

### The interconnect problem: 5 mm pins, 12 mm standoff

The male header stands only **5 mm** proud; the board must sit at **12 mm** to clear the terminal
blocks. **A taller socket does not solve this** - a socket's contact springs are near its mating face,
so a 12 mm socket still grips only in its first few millimetres and the pins fall 7 mm short of the
contacts. The height has to come from somewhere else:

| Option | Verdict |
|---|---|
| **Riser PCB** - male 2.0 mm down, female up, 12 mm standoffs | **Preferred.** Keeps everything inside the measured footprint, which matters when recessed between two 15 mm walls. One more small board on an order already being placed. |
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

Current draw is trivial: 4 x 21 mA ≈ 84 mA (§1.3), on a rail rated far above it.

## Open - check before layout

1. ~~Does the 20 mm width constraint relax at 12 mm?~~ **Moot - the board stays 20 mm** (decided
   2026-08-25, matching the module) and the 18.2 mm jack depth fits inside it. See *Board outline*.
2. ~~Do the terminal blocks' screws face up?~~ **No - they are accessed from the ENDS of the module,
   not the sides or top** (confirmed 2026-08-25). Overhanging their sloped backs blocks nothing, so the
   board can take the full 67-68 mm without giving any length back.
3. 🔶 **Tallest component in the footprint measures 12 mm** (2026-08-25) - the 15 mm terminal blocks
   sit outside it, at the ends. **Open: the standoff must therefore be MORE than 12 mm**, or the board
   rests on that component. Suggest 13-14 mm. This costs nothing: the terminal blocks' backs slope away,
   so raising the standoff only grows the length budget beyond 67-68 mm. Confirm whether the 12 mm
   figure is the component height or a clearance already allowed.
4. ~~Confirm no integrated magnetics~~ **Confirmed 2026-08-25: none.** The listing's photographs show
   **eight signal pins plus two shield tabs and nothing else**. Magnetics cannot hide - transformers
   need centre-tap pins - so a bare 8+2 pin field settles it.
5. ~~Which way the jack openings face~~ **Settled 2026-08-25** - see *Orientation* below.
6. ~~Where does P1 sit, and does its pin field clear the jacks'?~~ **Resolved 2026-08-25 by
   measurement - 3 mm of clearance.** See *The header-versus-jack collision* below.
7. ~~Reconcile the jack's two published dimensions~~ **Settled 2026-08-25: 16 mm is the WIDTH,
   18.2 mm is the LENGTH (depth).** The favourable reading was the right one - four jacks need 64 mm of
   the 67-68 mm length, and 18.2 mm of depth clears the 20 mm width with 1.8 mm spare.
