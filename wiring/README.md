# Wiring

How the boxes connect to each other and to the machine. Decisions, not measurements - anything
metered off the machine belongs in [`../commissioning/`](../commissioning/).

| | |
|---|---|
| [`db37-axis-interconnect.md`](db37-axis-interconnect.md) | Controller box ↔ remote breakout box: one 1.5 m DB37 carrying Step/Dir/EN/GND/AL/Limit for five axis blocks, plus the 5 V and 12 V pairs beside it |
| [`breakout-box.md`](breakout-box.md) | What is in the breakout box, the Mini-Fit Jr back panel, the SN04-N limit sensors and the SN04-N2 that replace them, and the one ground arrangement that matters out at the machine |
| [`cabinet-power-and-grounding.md`](cabinet-power-and-grounding.md) | The two incoming circuits, the two E-stop switches in series - a mushroom at the bed and the magnetic paddle below - and the contactor they drive, the 2 x 8 block's four pairs, the separate mains-fed 12 V logic supply, the 36 V 600 W motor supply and why its variable output is a hazard, the single bar every ground lands on, and why the USB cable defeats the isolation |
| [`ig57-drives.md`](ig57-drives.md) | The four IG57 all-in-one closed-loop steppers: the part, the Cat 6 and 18/2 cabling, the 50 V input ceiling against a 48 V rail, and what still needs the vendor documentation |
| [`panel-schematic.html`](panel-schematic.html) | **The drawing.** Five sheets of hand-authored SVG: the 220 V power chain, the two control circuits, the 110 V side, and the PE bar - with wire colour and gauge on every run. **Derived, never authoritative** - `cabinet-power-and-grounding.md` is where the decisions live. Not a DIN rail layout; that gets done with the real components |
| [`kicad/interface-board/`](kicad/interface-board/) | The termination board replacing the DB37 breakout: 5 RJ45 + 5 prox pairs, probes and spindle in Mini-Fit Jr, ribbons and terminal blocks out to the RP23U5XBB controller |
