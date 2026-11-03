# First power-up - Y direction and homing check

**Run this before the Y axes are first jogged.** The cast stepper frames put both Y motors
at the front of their beams, driving each screw from the opposite end to the arrangement
the direction signals were last proven on. Same screws, same handedness - but an unchanged
direction signal now moves the gantry the other way, and an unchecked first homing cycle
drives the ganged pair into the hard stops.

The controller is an **RP23U5XB v2.02**, with its own grblHAL driver and pin map. Nothing
carries over from the Mega V's settings - re-measure everything here.

## The one trap: $3 and $8 on a ganged pair

The second Y motor's direction is **$8**, not an axis bit in $3, and the firmware applies
it **after** $3 - so $8 is an offset from the master motor, not an absolute direction.

- **Both motors moved to a new end** (this build): flip the Y bit in **$3**, which moves
  both together, and **leave $8 alone**.
- Changing $8 on its own is what makes a ganged pair fight each other.

## Useful settings

| | |
|---|---|
| $23 | Homing searches the **positive** direction unless the axis bit is set here |
| $22 bit 1 | Enables single-axis homing commands - **$HY** tests Y without running the whole cycle |
| $22 bit 3 | Machine origin lands at the homed position, so **+axis points toward its limit switch** - which makes the direction check visual |
| Auto-square | Alarms instead of grinding if the pair disagrees - but only once both switches are confirmed seen |

## Order of work

1. **Press each Y limit switch by hand** and watch the Pn: field in the status report.
   Both must register before anything moves.
2. **Jog Y+ a few mm** with the gantry clear of both ends. It must move **toward** the
   switches. If not, flip the Y bit in $3 - not $8.
3. **Enable single-axis homing** ($22 bit 1) and run **$HY** alone, parked 20-30 mm from
   the switches, a hand on reset.
4. Only then run a full homing cycle.
