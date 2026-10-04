# Cutting loads and plate thicknesses

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

## The structural envelope: 500-1000 N

**Every part in this document is designed to 500-1000 N of cutting force.** A deflection figure
anywhere in this repo is read against that number.

🔴 **A figure quoted at 250 N is two to four times optimistic.** Deflection scales linearly with
force, so anything carried over from the 2026-09-29 analysis needs multiplying before it means
anything.[^loads-250n] The envelope is a structural target and is **not** tied to what the spindle
can deliver in a cut; the spindle's own figure is a separate question with a separate
answer.[^loads-spindle-torque]

---

## Plate and riser thicknesses

**Material matters as much as thickness now that steel is in the machine, so both are given.**
Current as of 2026-10-03.

| Part | Size | Material |
|---|---|---|
| Front strip, **all three beams** | 45 mm × 1000 mm × **4 mm** | **6061** - connector across the seam and the magnetic tape surface |
| X back joining plate | 120 mm × 1000 mm × **1/4"** | **6061** - X moves, so weight is real |
| **Y outboard / back joining plate** | 12" × 1000 mm × **1/8"** | **cold-rolled steel sheet** |
| **Y front plate / Z riser** | tapered 100→200 mm × 302 mm × **10 mm** | 6061, with the 60.5 × 50 window. 🔴 **Measured stock, not 1/2" and not 3/8"** |
| **Y rear plate**, one for both beams | 1211.75 mm × 12" × **1/4"** | **hot-rolled A36 steel**, P&O if preferred |
| Cast stepper frame interposer bar | 60 × **150** × **3/8"** | 6061, **3 off** - Y1, Y2 and the X stepper end. One drawing; X's BF12 end takes none, using a tongue off the end plate |
| **X gantry end plates** | 154 × **242.5** × **1/2"** | 6061, 2 off - identical below the top edge; the **right-hand one carries a 40 × 60 BF12 tongue** above it |
| **Y nut doubler block** | 154 × 50 × **1/2"** | 6061, 2 off - on the end plate's outer face, giving a 25.4 mm seating |
| **Y nut sole bracket** | trapezoid **154 → 46** over **98.7** × **1/4"** | 6061, 2 off - carries the inverted Y ball nut |
| X carriage plate | 154 × 407 × **1/2"** | 6061 |
| Z plate | **164** × 175 × **1/2"** | 6061 |

**The Y and X back plates are different parts.** Y's is steel, 12" tall and carries the box fixing;
X's is 6061 at 120 mm.[^loads-back-plates]

**The Y risers are 1/2".**[^loads-38] The **X end plates are 1/2" for different reasons than the Y
risers are** - they carry the whole gantry into the Y carriage blocks, they take the full cutting
moment as a couple, **they move**, and they get no full-height plate to lean on. The Y reasoning does
not transfer, and they are the likeliest subject of the "riser plates far weaker along Y, gusset
them" warning in the project notes.

---

## The measurement that would settle the 1/4" question

The X gantry plate is **1/4"**, chosen partly on the argument that **the Z assembly is the largest
compliance in the stack** and stiffening the beam past it buys nothing measurable. That is a claim,
not a measurement.

**Once the Z assembly is built: push on the spindle nose with a known force and put an indicator on
it.** That settles whether the beam plate should be 1/4" or 3/8", and the plate is bolt-on precisely
so the swap stays cheap.

📋 **Procedure: [`../commissioning/stiffness-test.md`](../commissioning/stiffness-test.md).**
⚠️ **It is not a single number.** One reading on the nose is a *total*, and a total cannot say which
part of the stack is moving - which is the entire question. The procedure uses six indicator
positions and subtracts.

### ⚠️ Open: the X carriage plate goes to 5/8" if the stiffness test says it is the compliance

**Deferred on purpose 2026-10-02**, and recorded because "consider it in future if it is a problem"
is the kind of intent that evaporates. The plate is **154 × 407 × 1/2"**, already cut and dyed, and
nothing says yet that it needs to be thicker - that is the same measurement the 1/4" question above
waits on. **Do not act on this before the test.**

🔴 **If it moves, it goes to thicker aluminium, not to a bolted-on steel backer.** Thicker aluminium
wins on stiffness and on mass at the same time, and the backer is the answer that looks
obvious.[^loads-steel-backer]

[^loads-250n]:
    Much of the analysis on 2026-09-29 was done against an assumed **250 N** cutting force. That is a
    trim-router number and it is wrong for this machine. Where an estimate from that round still
    stands, it is because the conclusion was insensitive to the force - not because the force was
    right.

[^loads-spindle-torque]:
    **Where 500-1000 N came from, and why it did not move when the spindle got smaller.** The
    envelope was first set against a **3 kW** spindle, which at 1.6 N·m would have made ~265 N
    available on a 12 mm cutter and ~530 N on a 6 mm at 18 000 rpm. Two corrections landed on
    2026-09-30, neither of which moved the target: the spindle is **2.2 kW, not 3 kW** (~1.17 N·m at
    400 Hz rather than 1.6), and the old table's 9 000 rpm row assumed constant power below base
    speed, which a VFD spindle does not do - it is roughly constant *torque* down from 400 Hz, so the
    torque stays put while the power halves, and the doubled row overstated the spindle. The envelope
    was **not** relaxed to match: a crash or a plunge into workholding generates forces the spindle
    rating has nothing to do with, and relaxing a structural margin because a motor got smaller is
    the wrong direction of travel. What the spindle can sustain in a cut and what the structure is
    designed to survive are different questions, and they were merged in the original table.

[^loads-back-plates]:
    They were once the same part in two lengths - "all three axes, 1/4" aluminium". Y's went to
    steel, to 12" tall and to carrying the box fixing, which broke that. Do not let the old line
    survive in anyone's head.

[^loads-38]:
    **The 3/8" question is closed**, recorded because the reasoning still applies to anything cut
    later. 3/8" loses **58 %** of the weak-axis stiffness against only 25 % of the strong-axis, which
    would have been acceptable **only if the full-height plate took the fore-aft load in-plane**. The
    risers went to 1/2" and are made, so the coupling never had to be managed. The saving was only
    about 0.44 lb per riser, 1.76 lb across all four, and it is static weight - thin something later
    for cost or machinability if you like, but there is nothing to gain in weight.

[^loads-steel-backer]:
    **The arithmetic, so it is not re-derived in six months** - 6061 at 69 GPa, mild steel at
    200 GPa, bending stiffness per unit width. This is a calculation, not a measurement.

    | | Bending stiffness | Mass per unit area |
    |---|---|---|
    | 1/2" aluminium, as cut | 1.00 | 1.00 |
    | Plus a 1/4" steel backer on **corner bolts only** | 1.36 | **2.45** |
    | **5/8" aluminium instead** | **1.95** | 1.25 |

    The gain depends entirely on whether the two plates transfer shear across the whole face: bolted
    on a grid they approach one section and ~5×, but **bolted at the corners they only share
    curvature and give 1.36×** for 2.45× the mass.

    📌 **Where the idea came from, so the precedent is not misread later.** The Mega V's aftermarket
    300 mm Z has a 154 × 310 × 12.7 mm carriage plate backed by 1/4" steel. Its backer is held by
    **four M5 socket heads, one per corner**, so it cannot be acting compositely - whatever it is
    for, it is not buying bending stiffness. The owner's reading is that it provides the mounting for
    the **V-wheel axles**, which is a concentrated point load into a hole and a job steel genuinely
    does better than aluminium. ⚠️ **That does not explain why it covers the full plate** - the wheel
    axles are only 5" apart and would fit in the bottom 6" - and no explanation for the full coverage
    has been established. **None of it transfers to this build regardless**: HGR20 blocks spread their
    load over a bolt pattern, so there is no axle stub, no eccentric and no point load.
