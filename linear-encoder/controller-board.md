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
| **12 mm (the planned standoff)** | **67-68 mm** |

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

**Magnetics: almost certainly none, not yet confirmed.** The listing does not mention them, and four
things point the same way - **"8P8C"** describes exactly eight contacts, where a MagJack brings out
centre taps and usually LEDs (12-16 PCB pins); integrated magnetics is an expensive selling point that
is never hidden; a 10-pack at this price is plain-jack territory; and `RJ45**NM**...` plausibly reads as
*No Magnetics*. None of that is proof from a marketplace listing, hence open check 4.

**90 degree = right-angle**, so the openings face sideways and cables exit horizontally out the long
edge rather than upward. That suits a board recessed between two 15 mm terminal blocks - nothing needs
to clear overhead - but it makes the ~21 mm typical depth of a right-angle jack collide with open
check 1, and it makes the facing direction a decision (check 5).

There is **no manufacturer datasheet** for this part, only the marketplace listing, so dimensions and
the footprint will have to be measured off the parts themselves.

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

1. **Does the 20 mm width constraint relax at 12 mm?** It was measured at board level. If everything in
   the width direction is under 12 mm tall, the board can be wider - which removes the jack-depth
   overhang question entirely and gives the passives room. Cheapest square millimetres available.
2. **Do the terminal blocks' screws or wire entries face up?** The extra 3-4 mm of length comes from
   overhanging their sloped backs. If a full 67-68 mm board covers the screws, landing an RS485, CAN or
   power wire means removing this board first. Give back a few millimetres if so - there is slack now.
3. **Measure the tallest component in the footprint yourself**, including the RTC battery header. 15 mm
   is from the terminal blocks; the standoff must clear whatever is actually highest.
4. **Count the pins when the jacks arrive.** Eight signal pins in two staggered rows plus two shield
   tabs = plain, which is what is wanted. More than eight signal pins, or a deep heavy body (~25 mm),
   means integrated magnetics and they are unusable here. See *The ordered part* below.
5. **Which way the jack openings face.** They must point away from the terminal blocks' wire entries,
   or plugging an encoder cable fights the field wiring. Mirror-image work to change after layout.
6. **Confirm the jack's depth** against the board width - see check 1.
