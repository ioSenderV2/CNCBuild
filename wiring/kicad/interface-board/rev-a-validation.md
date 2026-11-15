# Rev A checkout - the board itself, before anything connects

OPEN: **Not yet run.** Three boards in hand - OSH Park order xPBWS3rt, ordered 2026-11-03.
This is the meter session that says the populated board can be trusted: the fab's copper
and the hand soldering, checked against the netlist the board was cut from. **Nothing here
needs the RP23, a machine cable, or the cabinet** - a DMM on continuity does all of it
except the last section, which wants a bench 12 V.

**It validates the BOARD, not the wiring.** The split-pair trap in the
[README](README.md#what-is-on-it) cannot be caught here - all four RJ45 evens are one GND
net, so a split pair passes every check below and costs only signal integrity. That stays
a cable-end discipline.

**The connection tables below are read off the routed Rev A board file** on main, which
matches main's `netlist.txt` node for node - 42 nets, 154 pads. Rev B (this branch) adds
nets and connectors that do not exist on the boards in hand; do not check against this
branch's `netlist.txt`.

---

## 1. Before the iron - the two project-drawn footprints

The 85508 jack and the 39-30-1039 3P header are the two footprints drawn by hand from the
committed Molex sheets rather than taken from a library. On the board that gets populated,
before soldering anything:

| Check | Result |
|---|---|
| 85508 jack seats flush, all 8 legs and both tabs home | |
| 39-30-1039 seats flush, 3 legs and peg home | |
| Bare board: J18 pad 1 to GND pour reads open | |

A part that will not seat is a footprint error and affects all of its positions - stop and
measure which hole is off before forcing anything.

---

## 2. Dead board, populated - the bridge sweep and the net list

Meter on continuity, nothing connected to the board. Two readings per net, one row each:

- **Closed across its own points** - every pad listed, pad to pad. A miss is a joint that
  did not wet.
- **Open to GND** - one probe stays on **J18 pin 2**, the board's single GND entry. The
  GND pour runs both sides of this board, so a solder bridge lands on GND far more often
  than anywhere else. A closed reading here is a bridge at one of that net's joints.

### The five axis columns

Each column is one jack (pins 1/3/5/7), its stops on the 2x10 ribbon J16, the Teensy
header, the alarm ribbon J17, and the limit 3P with its terminal-block position.

| Net | Points | Closed | Open to GND |
|---|---|---|---|
| STEP_X | J1.1, J16.3, J40.2 | | |
| EN_X | J1.3, J16.2, J40.4 | | |
| DIR_X | J1.5, J16.1, J40.3 | | |
| AL_X | J1.7, J17.1 | | |
| LIM_X | J6.2, J21.1 | | |
| STEP_Y | J2.1, J16.7, J41.2 | | |
| EN_Y | J2.3, J16.6, J41.4 | | |
| DIR_Y | J2.5, J16.5, J41.3 | | |
| AL_Y | J2.7, J17.3 | | |
| LIM_Y | J7.2, J21.2 | | |
| STEP_A | J3.1, J16.15, J42.2 | | |
| EN_A | J3.3, J16.14, J42.4 | | |
| DIR_A | J3.5, J16.13, J42.3 | | |
| AL_A | J3.7, J17.5 | | |
| LIM_A | J8.2, J21.3 | | |
| STEP_Z | J4.1, J16.11, J43.2 | | |
| EN_Z | J4.3, J16.10, J43.4 | | |
| DIR_Z | J4.5, J16.9, J43.3 | | |
| AL_Z | J4.7, J17.4 | | |
| LIM_Z | J9.2, J21.4 | | |
| STEP_B | J5.1, J16.19, J44.2 | | |
| EN_B | J5.3, J16.18, J44.4 | | |
| DIR_B | J5.5, J16.17, J44.3 | | |
| AL_B | J5.7, J17.6 | | |
| LIM_B | J10.2, J21.5 | | |

### Probes, spindle, pass-throughs

| Net | Points | Closed | Open to GND |
|---|---|---|---|
| PROBE | J11.2, J13.1, J14.1, J23.1 | | |
| DOOR | J12.2, J23.2 | | |
| SPIN_EN | J15.1, J22.1 | | |
| SPIN_PWM | J15.4, J22.4 | | |
| MIST_A | J30.1, J34.1 | | |
| MIST_B | J30.2, J34.2 | | |
| FLOOD_A | J31.1, J35.1 | | |
| FLOOD_B | J31.2, J35.2 | | |
| CYCLE_START | J32.1, J36.1 | | |
| FEED_HOLD | J32.2, J36.2 | | |
| ESTOP | J32.3, J36.3 | | |
| SPARE | J32.4, J36.4 | | |
| UART_TX | J33.1, J37.1 | | |
| UART_RX | J33.2, J37.2 | | |
| UART_3V3 | J33.3, J37.3 | | |

### The rails

**+12V** - one probe on J18 pin 1, the other to each of the eight other pads. And the rail
pair itself: J18.1 to J18.2 must read **open**.

| Pad | J19.1 | J6.1 | J7.1 | J8.1 | J9.1 | J10.1 | J11.1 | J12.1 | J18.1-J18.2 open |
|---|---|---|---|---|---|---|---|---|---|
| Closed to J18.1 | | | | | | | | | |

**GND** - one probe on J18 pin 2, the other to each connector's GND pin. On the jacks,
check all four evens: each is its own leg into the pour, and one dry joint among four
grounds is exactly the fault the drive-end wiring would then hide.

| Connector | GND pins | All closed |
|---|---|---|
| J1-J5 jacks | 2, 4, 6, 8 each | |
| J6-J12 3Ps | 3 | |
| J13, J14 | 2 | |
| J15 spindle | 2 and 3 | |
| J16 ribbon | 4, 8, 12, 16, 20 | |
| J17 ribbon | 2 | |
| J19 12 V out | 2 | |
| J22 spindle TB | 2 and 3 | |
| J33, J37 UART | 4 | |
| J40-J44 headers | 1 | |

### Adjacent pins - the other bridge class

Walk every connector pin to its neighbour. **Everything adjacent reads open**, with two
exceptions that read closed because they are the same net: **J15's two GND pins** and
**J22 pins 2-3**. A closed reading anywhere else is a signal-to-signal or signal-to-12V
bridge that the GND sweep above cannot see.

---

## 3. The jack face - one jack, through the port

The checks above probe the jack's pads from the board side, so they cannot catch a
footprint drawn mirrored - the part would seat, every net would pass, and pin 1 at the
cable end would land on pin 8's pad. Plug a patch cable stub with its far end cut and
fanned into **J1** and read the fan against the board:

| Jack pin | Lands on | Reads |
|---|---|---|
| 1 | STEP_X - J16.3 | |
| 3 | EN_X - J16.2 | |
| 5 | DIR_X - J16.1 | |
| 7 | AL_X - J17.1 | |
| any even | GND - J18.2 | |

All five jacks share the one footprint, so one jack passing clears the class. T568 colors
for the fan are on the cable's own pairs - pin 1 is white/orange in T568B.

**The shield tab reads open to everything, and that is correct.** Its two holes are
unplated with no net - read off the board file, both revisions - so the shield floats.
The patch cables are UTP, so it carries nothing anyway.

---

## 4. First 12 V

Bench 12 V into **J18, + on pin 1**, polarity against the silk. Nothing else connected.

**The board should draw nothing a bench meter can see** - there are no actives on it. Any
visible steady draw is a fault; find it before going further.

Then, meter on DC volts, black probe on J18.2:

| Pad | J19.1 (12 V out) | J6.1 | J7.1 | J8.1 | J9.1 | J10.1 | J11.1 | J12.1 |
|---|---|---|---|---|---|---|---|---|
| Reading | | | | | | | | |

---

## What a result means

- **Open within a net, closed to GND, or a closed neighbour pair** - a soldering fault on
  this board: fix, re-check the row.
- **Section 1 or 3 fails** - a footprint fault: it is in the design, affects every board
  of this rev, and goes on the [Rev A lessons list](README.md#still-open-before-any-rev-b-order)
  that gates the Rev B order.
- **Everything passes** - the board is trusted, and every later fault in the enclosure is
  wiring, not board.
