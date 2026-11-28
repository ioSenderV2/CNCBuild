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

## 2026-11-28 - the 220 V side, first branches

- **XDR-960-36 checks out at 36 V** - which also proves the whole 220 path by operation:
  pigtail, breaker, and both poles of the main contactor under the paddle.
- **The FBS bridges on the Phoenix 36 V groups must be driven fully flush** - sitting loose
  in the shafts they conduct NOTHING, and the first meter pass showed voltage only on the
  fed block. Seated flush (they take real force), **36 V reads across all six blocks** of
  the bridged group. A loose bridge looks installed and is open - check flushness by eye
  on any future group.

- **DVRD-36 window set on the live rail**: overvolt **39 V** (that knob's floor), undervolt
  **33 V** (knob reaches 30). Out of the box it sat in TRIP with a healthy 36 on the rail -
  the factory knob positions put 36 outside the window; TRIP red with rail voltage present
  means the window is wrong, not the rail. The undervolt stays well below nominal on purpose:
  a threshold at 36 would e-stop on ordinary sag. ⚠ Watch during the stepper session: the
  rail lifts on braking, and if hard decels blink TRIP past 39, the overvolt knob has room
  above.

## Still to run, in order

1. **DVRD contact proof**: continuity across 15-18 - closed with NORM lit, open on a paddle
   press as the rail dies.
2. **Rest of the 220 branches**: the VFD powering, the pump contactor.
3. **Steppers** - the drive bench session, [`bench-session.md`](bench-session.md).
