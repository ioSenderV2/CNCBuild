# Wiring

How the boxes connect to each other and to the machine. Decisions, not measurements - anything
metered off the machine belongs in [`../commissioning/`](../commissioning/).

| | |
|---|---|
| [`db37-axis-interconnect.md`](db37-axis-interconnect.md) | Controller box ↔ remote breakout box: one 1.5 m DB37 carrying Step/Dir/EN/GND/AL/Limit for five axis blocks, plus the 5 V and 12 V pairs beside it |
| [`breakout-box.md`](breakout-box.md) | What is in the breakout box, the Mini-Fit Jr back panel, the SN04-N limit sensors and the SN04-N2 that replace them, and the one ground arrangement that matters out at the machine |
| [`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md) | Mains, the separate 24 V logic supply, the undecided 600-or-800 W motor supply, the single bar every ground lands on, and why the USB cable defeats the isolation |
| [`hbt57c-drives.md`](hbt57c-drives.md) | What the drives themselves do: the LED fault codes, the unresolved question of how a fault gets cleared and the bench test for it, and the RS232 configuration port |
