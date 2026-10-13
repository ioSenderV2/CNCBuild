# Wiring

How the boxes connect to each other and to the machine. Decisions, not measurements - anything
metered off the machine belongs in [`../commissioning/`](../commissioning/).

| | |
|---|---|
| [`db37-axis-interconnect.md`](db37-axis-interconnect.md) | Controller box ↔ remote breakout box: one 1.5 m DB37 carrying Step/Dir/EN/GND/AL/Limit for five axis blocks, plus the 5 V and 12 V pairs beside it |
| [`breakout-box.md`](breakout-box.md) | What is in the breakout box, the Mini-Fit Jr back panel, the SN04-N limit sensors and the SN04-N2 that replace them, and the one ground arrangement that matters out at the machine |
| [`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md) | Mains, the separate 24 V logic supply, the undecided 600-or-800 W motor supply, the single bar every ground lands on, and why the USB cable defeats the isolation |
| [`ig57-drives.md`](ig57-drives.md) | The four IG57 all-in-one closed-loop steppers: the part, the Cat 6 and 18/2 cabling, the 50 V input ceiling against a 48 V rail, and what still needs the vendor documentation |
