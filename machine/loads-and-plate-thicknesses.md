# Cutting loads and plate thicknesses

> Split out of `end-plates-risers-and-spindle.md` on 2026-10-02 - the section below is
> **verbatim**, nothing was re-decided in the move. Its nine siblings are listed in
> [`README.md`](README.md).

---

## Cutting forces: 500-1000 N, not 250

🔴 **Read this before using any deflection figure in this repo.** Much of the analysis on
2026-09-29 was done against an assumed **250 N** cutting force. That is a trim-router number and it
is wrong for this machine.

This table was built when the spindle was expected to be **3 kW**. What that would have made
available:

| | Torque | 12 mm cutter | 6 mm cutter |
|---|---|---|---|
| 18 000 rpm | 1.6 N·m | ~265 N | ~530 N |
| 9 000 rpm | 3.2 N·m | ~530 N | ~1060 N |

⚠️ **Two corrections, neither of which moves the design target - 2026-09-30:**

1. **The spindle is 2.2 kW, not 3 kW.** Rated torque at 400 Hz is ~1.17 N·m rather than 1.6.
2. **The 9 000 rpm row assumes constant power below base speed, and a VFD spindle does not do
   that** - it is roughly constant *torque* down from 400 Hz, so the torque does not double, it stays
   put while the power halves. The doubled row overstates what the spindle can deliver.

**Design to 500-1000 N anyway.** The envelope is *not* being relaxed to match a smaller spindle, for
two reasons: a crash or a plunge into workholding generates forces the spindle rating has nothing to
do with, and relaxing a structural margin because a motor got smaller is the wrong direction of
travel. **Treat 500-1000 N as the structural envelope and the table as a note on what the spindle can
sustain in a cut** - they are different questions and were merged here.

Every deflection figure scales linearly, so anything quoted at 250 N is two to four times optimistic.
Where the original estimate still stands, it is because the conclusion was insensitive to the force -
not because the force was right.

---

## Plate and riser thicknesses

**Material matters as much as thickness now that steel is in the machine, so both are given.**
Current as of 2026-10-02.

| Part | Size | Material |
|---|---|---|
| Front strip, **all three beams** | 46 mm × 1000 mm × **1/4"** | **6061** - connector across the seam and the magnetic tape surface |
| X back joining plate | 120 mm × 1000 mm × **1/4"** | **6061** - X moves, so weight is real |
| **Y outboard / back joining plate** | 12" × 1000 mm × **1/8"** | **cold-rolled steel sheet** - see the reversal above |
| **Y front plate / Z riser** | tapered 100→200 mm × 302 mm × **10 mm** | 6061, with the 62 × 50 window. 🔴 **Measured stock, not 1/2" and not 3/8"** |
| **Y rear plate**, one for both beams | 1200 mm × 12" × **1/4"** | **hot-rolled A36 steel**, P&O if preferred |
| Cast stepper frame interposer bar | 60 × **150** × **3/8"** | 6061, one per Y beam and per X end |
| **X gantry end plates** | 154 × **242.5** × **1/2"** | 6061 - two identical plates, specified above |
| **Y nut doubler block** | 154 × 60 × **1/2"** | 6061, 2 off - on the end plate's outer face, giving a 25.4 mm seating |
| **Y nut sole bracket** | trapezoid **154 → ~46** over ~75 × **1/4"** | 6061, 2 off - carries the inverted Y ball nut |
| X carriage plate | 154 × 407 × **1/2"** | 6061 |
| Z plate | **164** × 175 × **1/2"** | 6061 |

⚠️ **Y and X back plates are no longer the same part in a different length.** Y's is steel, 12"
tall and carries the box fixing; X's stays 6061 at 120 mm. Do not let the old "all three axes, 1/4"
aluminium" line survive in anyone's head.

### The 3/8" question is closed - the Y risers are built at 1/2"

Recorded because the reasoning still applies to anything cut later. 3/8" loses **58 %** of the
weak-axis stiffness against only 25 % of the strong-axis, which would have been acceptable **only
if the full-height plate took the fore-aft load in-plane**. The Y risers went to 1/2" and are made,
so the coupling never had to be managed.

The saving is only about 0.44 lb per riser, 1.76 lb across all four, and it is static weight. Thin
them for cost or machinability if you like; there is nothing to gain in weight.

### Why the X end plates are different

They carry the whole gantry into the Y carriage blocks, they take the full cutting moment as a
couple, **they move**, and they get no full-height plate to lean on. The Y reasoning does not
transfer. They are also the likeliest subject of the "riser plates far weaker along Y, gusset them"
warning in the project notes.

---

## The measurement that would settle the 1/4" question

The X gantry plate thickness was chosen as 1/4" partly on the argument that **the Z assembly is the
largest compliance in the stack** and stiffening the beam past it buys nothing measurable. That is a
claim, not a measurement.

**Once the Z assembly is built: push on the spindle nose with a known force and put an indicator on
it.** That settles whether the beam plate should be 1/4" or 3/8", and the plate is bolt-on precisely
so the swap stays cheap.

📋 **Procedure: [`../commissioning/stiffness-test.md`](../commissioning/stiffness-test.md).**
⚠️ **It is not a single number.** One reading on the nose is a *total*, and a total cannot say which
part of the stack is moving - which is the entire question. The procedure uses six indicator
positions and subtracts.
