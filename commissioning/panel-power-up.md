# Panel power-up - measured on the bench

The electronics panel standing alone, off the machine. Everything here is a meter reading
taken on the real panel; the wiring design it validates is
[`../wiring/cabinet-power-and-grounding.md`](../wiring/cabinet-power-and-grounding.md).

## 2026-11-28 - the 110 V side and the 12 V path

110 V pigtail only; the 220 V pigtail not connected.

- **12 V present on the correct pins at every point checked**: all limit-sense sockets,
  the 3D probe socket, the tool setter socket, and both fan headers (J60 radiator,
  J61 case - pins 1/2).
- **MDR-40-12 output trimmed from 12.125 V to 12.02 V** at the supply's pot.
- **Paddle and main contactor, coil chain - PASSED**, still on 110 V alone, 220 pigtail
  not connected:
  - Green button: audible pull-in, the contactor's window shows **red**.
  - Red stop paddle: window goes **blank** (not green - blank is this part's released state).
  - Mushroom: same drop-out - and **resetting the mushroom does NOT restore power; only the
    green button does.** That observed behaviour proves the mushroom sits **upstream** of the
    paddle's feed - the wiring direction the design file flagged as silently invertible is
    confirmed right on the real panel.

## Still to run, in order

1. **Line-pole continuity on the main contactor** - coil held in, 220 pigtail unplugged:
   continuity across each line pole proves the 220 path will conduct before 220 exists.
2. **220 V pigtail in** - branch by branch behind the breakers: the 2 x 8 block's pairs,
   the XDR-960-36 rail (and the DVRD-36 picking up), the VFD powering, the pump contactor.
3. **Steppers** - the drive bench session, [`bench-session.md`](bench-session.md).
