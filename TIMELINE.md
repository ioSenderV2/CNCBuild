# Project timeline

The arc of the build, milestone level, written 2026-11-28. The fine grain lives in the git log —
the commit subjects narrate every decision — and in the session logs under the hub
(`claude-hub/projects/CNCBuild/conversations/`, and `ioSender` for everything before the repo).
This file is the orientation layer: which phase, when, and what each one closed.

## Before the repo — June to August 2026

The machine's design was argued out in ioSender sessions (they run from 2026-06-07) while the
Mega V / Mega-XL work was live, and its facts accumulated in the firmware fork's scratch folder.
Travels, plate dimensions, and which stored setting disagreed with the machine kept getting
re-derived in conversation — which is the stated reason this repo exists.

## The encoder boards open the repo — 2026-08-25 to 2026-09-10

- **2026-08-25** — the machine gets a repo. The controller board (the linear-encoder CAN node's
  carrier) arrives the same day as a write-up and a KiCad schematic, verified that evening.
- **2026-08-26** — the RJ45 question closes: four discrete jacks, FMHXG RJ45NMCCFC-90D-10
  ordered; board outline fixed at 67–68 × 20 mm, standoff at 14 mm.
- **2026-08-29** — the sensor board gets its schematic, and the repo gets its own sessions
  (work until then had run under ioSender).
- **2026-09-10** — the axis connections move to a breakout box of their own.

## The mechanical design sprint — 2026-09-29 to 2026-10-05

Three months of accumulated intent becomes dimensioned design in one week.

- **2026-09-29** — the big survey: gantry beams confirmed as stacked pairs of 8020 30-6060,
  published 8020 numbers replace estimates, photographs become admissible evidence, the Z
  topology and travel budget close (246 mm), and the constraint that shapes everything lands:
  **the milling is one trip**, so every plate is designed before the trip.
- **2026-09-30** — the torsion box is designed (egg-crate ribs, doubled walls), the spindle is
  2.2 kW, and drawings become a thing this repo has — the shop pack is born.
- **2026-10-02 to 10-05** — the end-plate marathon: steel on Y accepted as a recorded reversal,
  the **dimension registry** created (authoritative values, Fusion export), STATUS and INDEX
  generated from markers in the prose, the shop pack redrawn in machining coordinates, and the
  interposer scheme settled. The purge of trade jargon from the shop pack begins, repo-wide.

## Numbers firm up, the model arrives — 2026-10-07 to 2026-10-12

- **2026-10-07** — steppers settle at 2.2 N·m NEMA 23 on all four axes; measured thicknesses
  replace carried nominals and sweep the registry.
- **2026-10-09** — X travel measured at 820 mm; the six bolt-on plates join the mill trip
  (126 holes is too many by hand).
- **2026-10-10 to 10-11** — the 3D model push: all four drive assemblies, every bolt with its
  length from a new **fastener schedule**, the box cut list (two sheets of 4×8), and the
  interactive model grows jogging, a DRO, tooltips and a live clash check. registry.html makes
  the registry browsable.
- **2026-10-12** — the 2026-09-26 electrical notes land in the repo and the memory notes retire:
  drives identified as IG57 (the HBT57C was the Mega V's), the 36 V 600 W supply, the TST57
  manual committed. NC limit sensors bought.

## Wood: the torsion box and the base — 2026-10-13 to 2026-10-26

- **2026-10-13** — the plywood is measured at 24 and 18 against nominal 25 and 19, and every
  derived dimension moves. The Y drive flips to the rear. Sheet goods bought at Crosscut.
- **2026-10-14 to 10-15** — Torsion Box Construction and Base Construction become generated
  build documents; the base design closes (legs built from strips, cross rails, a full-height
  central wall, a back shear wall).
- **2026-10-16 to 10-17** — the aluminum quote goes out as three requests with its DXF package;
  six leveling casters on cut-to-fit blocks.
- **2026-10-18 to 10-22** — the base goes together, as-built measurements replacing targets as
  they land (central wall 1218 × 756 trimmed, fore-aft rails cut equal at 1223).
- **2026-10-23** — the waterjet takes the rear plate off the mill trip — **the mill trip is
  aluminum only** from here. The box walls go on: back, left, right, front.
- **2026-10-24 to 10-26** — the box is proven square (both diagonals 1564), a 2.0 mm symmetric
  tongue toe is found, a carriage jig built from the real shelf bars measures it, and the Y1
  tongue is router-skimmed to close it. The Z spacers are miked and their step closed with metal.

## Steel prep, and the gantry stands — 2026-10-27 to 2026-11-01

- **2026-10-27 to 10-29** — steel prep and finish scheme settle: abrasive for mill scale,
  self-etch on mating faces, 2K clear on show faces.
- **2026-11-01** — **the gantry is in.** The part answers the span the tape could only bound,
  and the Y block pitch is chosen at 80.

## The electronics sprint — 2026-11-02 to 2026-11-16

- **2026-11-02 to 11-03** — the interface board (the DB37 breakout's replacement, feeding the
  RP23U5XBB) is schematic'd, placed and routed in two days; **Rev A ordered** from OSH Park
  on 11-03 ($164.95 for 3).
- **2026-11-03 to 11-04** — the sensor puck goes to a 35 mm disc for the bored-rod mount and
  **six puck boards are ordered** ($27.50); the controller board is placed, routed and its fab
  package built.
- **2026-11-05 to 11-08** — cabinet power distribution designed end to end: the E-stop chain,
  two WCT-25 contactors, per-pair DIN breakers, the 12 V supply, a five-sheet panel drawing,
  the wiring document, drag chain contents and every wall penetration.
- **2026-11-09** — **Rev B** called and designed in a day: 121 × 104.5 on 4 layers, the DVRD-36
  rail sense replacing the rejected monitoring relay.
- **2026-11-10** — the three-socket totem passes its bench check, toned top to bottom.
- **2026-11-13 to 11-14** — the XDR-960-36 motor supply bought and in hand; the 36 V
  distribution moves off Rev B into the DIN box.
- **2026-11-15** — **Rev B ordered** — OSH Park Super Swift, $429.80 with Next Day Air.
- **2026-11-16** — stencils ordered for the sensor board; the PVC enclosure gives way to
  everything on a 500 mm square of 3/4 ply.

## The controller board rebuilt, the bench readied — 2026-11-19 to 2026-11-23

- **2026-11-19** — the controller board is re-laid out around through-hole 85508 jacks on a
  back band, turned 90° onto a 70 × 28 outline off his caliper measurement, routed clean.
- **2026-11-20** — **the controller board is ordered** (OSH Park, 3 boards, $23.75 delivered)
  with its stencil; the paste/reflow bench sheet covers both boards end to end; the VFD control
  wiring is nailed down off the Mega V's working run.
- **2026-11-21 to 11-23** — switch run, spindle connector orientation and drive flying-lead
  colours onto the figures; R1–R3 built at 150 Ω as the mid-range start.

## New drives, and Rev C — 2026-11-25 to now

- **2026-11-25** — **four new drives bought for this machine**: the alarm-OR gate opens once
  HBT57112C alarm sense is measured assert-on-fault on the bench. The drives file changes name
  for the second time — both machines now run the HBT family.
- **2026-11-26** — the HBT manual lands and its numbers sweep the repo (3.2 N·m, 1780 g,
  power-cycle alarm clearing). The axis split confirms: three 57112C on X/Y1/Y2, a 5776C at
  2.0 N·m on Z, all four new. **Rev C goes to copper** — the four changes placed, routed,
  silkscreened, ERC and DRC clean, quote package built, README reads Rev C.

## Where that leaves the build — 2026-11-28

The frame, base, torsion box and gantry are assembled and proven square. The electronics panel —
the 3/4 ply board with everything on it — is fully wired, standing alone off the machine. Next
is the bench power-up: apply power, validate the voltages through the system, then run the
steppers. Once that passes, the one board mounts on the machine and six hookups finish the job:
a 4-pin DT to the spindle motor, a 3-pin DT to the outlet, a 2-pin DT to the pump, a 4-position
DTM to the paddle, and the two wall pigtails — the 220 V straight to the contactor, the 110 V
to the breaker. Interface Rev C is designed and quoted (the Rev B boards and the controller
boards in fab/transit). Mechanically, what remains is finishing work: the Z plate and the X
carriage plate are back from the waterjet with rough holes to drill out, counterbore and tap,
and the Z stop block and the two shelf supports for the X gantry are still to be machined — no
more waterjet trips. STATUS.md carries the live open items.
