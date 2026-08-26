# Linear scale position feedback over CAN

**Status: design only, parked 2026-08-21; sensor + module pinouts added 2026-08-25.** Nothing is built. Resume when there is CAN hardware to
connect to. Written while the details were fresh so the next session starts from the reasoning rather
than re-deriving it.

---

## 1. What this is

Magnetic linear scales on each axis, read by Hall sensors, decoded to positions by an ESP32, sent over
CAN to the Teensy, so grblHAL knows where each axis **actually** is rather than only where it commanded
the axis to go.

```
  4 mag tapes + 4 Hall readers          X, Y1, Y2, Z
            |
            |  A/B quadrature pairs
            v
   ESP32-S3-RS485-CAN module            PCNT decodes A/B in hardware
            |                           (see §1.1 - the counters are only 16-bit)
            |
        CAN bus  (differential, noise-tolerant - the reason the ESP32 sits near the machine)
            |
            v
   Teensy 4.1 / T41U5XBB  -> grblHAL plugin -> ? status report -> ioSender
```

Four tapes and four readers, matching the motor configuration: X, **Y1, Y2** (the ganged pair), Z. Two
tapes on the gantry is deliberate - see §3 and §11.

### 1.1 ESP32-S3 PCNT: exactly enough, and it wraps

The ESP32-S3's pulse counter has **4 units**, each with two channels. Quadrature uses both channels of
one unit, so four units is exactly four axes with **no spare**. Adding a fifth scale later means a
different decode strategy, not another unit.

Each unit's counter is **16-bit signed**, wrapping at ±32767 counts:

| Scale resolution | Counter wraps every |
|---|---|
| 1 µm | **32.7 mm** |
| **1.95 µm — the actual AS5311 figure (§1.3)** | **63.9 mm** |
| 5 µm | 163 mm |

The overflow/watchpoint interrupt must accumulate into a wider software total. "Decoded in hardware" is
true of the quadrature but **not of the range** - a 400 mm axis folds back on itself a dozen times at
1 µm. The failure looks like a plausible position, not an obvious fault, which is what makes it worth
writing down.

### 1.2 The module's pins

**[`hardware-esp32-s3-rs485-can.md`](hardware-esp32-s3-rs485-can.md)** - the 20-pin header map, what the
board already uses, and where the schematic is kept. Short version: the header exposes
**IO3-IO14 free** (12 pins, and the encoders need 8), CAN sits on IO15/IO16 and RS485 on IO17/IO18/IO21,
so an encoder harness cannot collide with the bus.

Worth knowing before going looking: **the wiki does not document the header's GPIOs at all** - only the
4-pin SH1.0 connector. That map is in the schematic and nowhere else, which is why it reads as missing.

### 1.3 The sensor: AS5311

Identified 2026-08-25. Datasheet in [`manufacturer-assets/`](../manufacturer-assets/index.html) - `AS5311-Datasheet.pdf`
(rev 1.12). Everything here is from it; wiring is §14.

| | |
|---|---|
| Incremental resolution | **1.95 µm/step** (10-bit / 2 mm pole pair) = 512 steps/mm, 1024 edges per pole pair |
| Absolute (SSI/PWM) resolution | 0.488 µm/step (12-bit / 2 mm pole pair) |
| Max speed, incremental incl. interpolation | **650 mm/s** (39 m/min) - far above any feedrate here |
| System propagation delay, incremental | **384 µs** |
| Internal sampling rate | 10.42 kHz typ (9.38-11.46 over temperature) |
| Hysteresis, incremental | 2 LSB = 3.9 µm |
| Transition noise | 0.6 µm RMS (1σ) |
| INL / DNL | ±5.6 µm (25 °C, ideal magnet) / ±0.97 µm, no missing codes |
| Supply | 3.0-3.6 V **or** 4.5-5.5 V |
| Outputs | A (pin 4), B (pin 5), Index (pin 7); MagINCn (pin 2), MagDECn (pin 3) open-drain |

Consequences for what is already written here:

- **§1.1's wrap arithmetic uses the wrong resolution.** At 1.95 µm/step the 16-bit PCNT counter wraps
  every **±63.9 mm**, not the 32.7 mm the 1 µm row assumes. Still a dozen wraps on a 400 mm axis, so the
  overflow accumulator is no less mandatory - the table is just pessimistic.
- **§5's latency budget `T` starts at 384 µs** before the ESP32, CAN or the Teensy add anything. That is
  the floor, and it is measured, not estimated - which §11.4 asked for.
- **The 3.9 µm hysteresis and 0.6 µm noise set §5's threshold floor.** An alarm tighter than ~5 µm is
  alarming on the sensor's own quantisation.

#### The Index output is not a datum

The AS5311 has an Index output, but it fires **once per 2 mm pole pair** - it repeats every 2 mm along
the tape. It is not a machine reference and does **not** solve §8's reboot/zeroing problem. Useful only
as a per-pole sanity check. Budget wiring for A and B, not A/B/Index (§14).

#### It does have a field-validity output - §11.1 is answered

Table 13 of the datasheet, decoded (both pins are open-drain, active low, "On" = asserted):

| Field | MagINCn | MagDECn | Meaning |
|---|---|---|---|
| GREEN (~10-40 mT) | Off | Off | Magnet OK |
| YELLOW (~3.4-54.5 mT) | **On** | Off | Still works, reduced accuracy |
| RED (<3.4 mT or >54.5 mT) | **On** | **On** | Out of range - not recommended |

So **`MagDECn` asserted ⟺ RED**, and a reader that has run off the end of its tape sees no field at all,
which is the `<3.4 mT` case. That makes the end-of-tape condition **detectable**, where §3 was written
assuming it could not be.

**This does not reopen §3.** The limit switches still stay - §3 lists three further reasons, each
independently sufficient, and none of them is about detectability. What changes is that the silent
failure becomes a reportable one: `MagDECn` goes straight into the `flags` byte (§6) and into §9's
failure table as a real signal rather than an inference.

### 1.4 Physical layout

Confirmed 2026-08-25. Three readers are mounted; the fourth is not solved.

| Reader | Mounted on | Reads | Cable run |
|---|---|---|---|
| 1 | X-axis endplate (one side) | **Y** scale | inside the gantry extrusion, then the drag chain |
| 2 | X-axis endplate (other side) | **A** scale (the ganged Y2 / M3) | inside the gantry extrusion, then the drag chain |
| 3 | back of the Z plate | **X** scale | up the Z plate - short, no chain |
| 4 | *not mounted* | **Z** - see §11.9 | - |

**The ESP32 lives at the top of the Z plate**, so it rides with the Z carriage and every cable terminates
there. That is what makes reader 3's run trivial, and it is what sets §14's 2.4 m figure for the two that
come off the gantry ends.

The pin budget in §14 is drawn for four readers. Three are wired today - 6 quadrature + 3 `MagDECn` = 9
of the 12 free pins - so the Z allocation is reserved, not spent.

#### The scales

**10 mm wide magnetic strip on a steel band, 3M PSA backing, 3 m in stock.** The steel band is the flux
return path - it is what makes the field readable at 0.3 mm - so an aluminium substrate is fine
everywhere; the tape brings its own ferrous backing.

**Laid flush with one edge, and that edge is the registration datum.** Lateral alignment then comes from
machining rather than from eyeballing, and it fixes one dimension for the sensor mount: the magnetic
centreline is **5 mm in from the tape edge**, so the Hall array must sit 5 mm from the registration edge
and hold to ±0.5 mm (§1.3).

| Axis | Tape runs | Why |
|---|---|---|
| X, Y, A | down the **centreline between each pair of linear rails** | closest to the load path, so carriage pitch/yaw barely translates into position error |
| Z | on the **edge of the 1/2" (12.7 mm) aluminium Z gantry plate** | the 1605 ball screw occupies the space between the Z rails, so the centreline is not available |

**Bond the full length, not one end.** Steel expands at ~11.7 µm/m/K, aluminium at ~23.1. A tape anchored
at one end and left to float would report *steel's* expansion while the machine moves with *aluminium* -
roughly 110 µm per metre per 10 °C of divergence, which is precisely the size of error that trips a
lost-step alarm on a warm afternoon. Bonded along its length, the band is dragged by the substrate and
the scale tracks the machine's real thermal growth. This is a correct choice, not a compromise; do not
"improve" it into a one-end anchor later.

Handling, because the PSA is one-shot and the tape is a magnet: degrease with IPA, work above ~15-20 °C,
lay it down progressively rather than stretching it taut (a stretched PSA strip creeps back over days),
allow a day or two for full bond, and dry-fit and mark the ends before peeling anything. **Keep magnetic
bases, magnetic trays and magnetic sweepers off it** - a strong magnet can permanently corrupt the
magnetisation, and the result would look like a localised position error with no discoverable cause.

**Length budget: it fits, comfortably.** The tape is fixed to the extrusion and the sensor rides in the
plate's bore, so what a tape must span is **the range that bore sweeps** - not the extrusion length, not
the plate width. Every bit of end-of-travel dead zone is tape not bought. The machine (Mega V XL) has
1080 mm extrusions on X, Y and A, but the plates stop well short of the ends.

| Axis | Tape - **upper bound**, pending measurement |
|---|---|
| X | ≤880 mm |
| Y | ≤880 mm |
| A | ≤880 mm |
| Z | ~200 mm |
| **Total** | **≤2840 mm of the 3000 in stock** |

Those are ceilings from 1 m rails and 150 mm plates (~848 mm of travel, agreeing with the ~860 mm the
`$130` investigation measured). The real dead zone is larger - the plate cannot approach closer than
76 mm - so expect nearer 780 mm per long axis and ~400 mm spare.

#### Mark it on the machine; do not compute it

There is a term that is easy to get wrong and expensive when it is: **where the sensor bore sits on the
150 mm plate.** If the bore is not centred, the sensor's sweep is offset from the plate's sweep, and the
tape's *start position* moves with it. Correct length, placement wrong by 50 mm, and the axis still runs
off the tape at one extreme. So:

1. Jog to one hard stop; mark the extrusion at the sensor bore's centreline.
2. Jog to the other stop; mark again.
3. Cut and lay the tape mark-to-mark plus ~10 mm beyond each.

That is immune to every assumption above - plate width, screw length, where the 76 mm is referenced from
- and it measures the thing that actually matters. It also yields the real travel figures before any
irreversible cut. **Do not take travels from the config:** `$130` read 889 against a real 860 because a
catalog preset overwrote the measured value. That one erred large, the harmless direction here, but it
settles that the configuration is not the authority.

**Sequencing still matters even with the larger margin**, because it does not depend on the number: a
long run is ~800 mm and the spare is ~400, so **no long run can be redone**. The PSA is one-shot, so a
mis-cut or a bad application costs a piece that does not exist. Cut the three long axes first - any
shortfall then lands on Z, which is cheap to re-order and is deferred anyway (§11.9) - and **err long
rather than short**. Overhang costs nothing; a tape stopping short leaves a band at one end of travel
where the axis moves and the counter does not, presenting as lost steps at one extreme and reading like
a mechanical fault.

#### Z's Abbe offset, and why its threshold is looser

The edge mount puts Z's measurement line a lateral distance *d* off the ball-screw axis, so carriage
pitch or roll appears as position error of about *d × θ* - with *d* ≈ 75 mm, 0.001 rad of tilt is ~75 µm,
against a 1.95 µm resolution.

That is acceptable **only because of what §2 scoped**: a DRO and a lost-step alarm, not metrology. The
error is a stable function of position, not noise - the carriage tilts the same way at the same place
every time - and a lost step is a discrete jump that stands clear of a smooth offset.

The consequence: **Z's alarm threshold is set looser than X/Y/A's**, using the per-axis settings §7
already provides. Recorded here so that nobody later tightens Z to match the others and gets nuisance
alarms out of geometry that was chosen deliberately.

#### The sensor mount: a clamped puck in a 35 mm bore

Each endplate and the X gantry plate already has a **35 mm hole**. The mount is a 35 mm aluminium round,
bored at the bottom to clear the RJ45 jack and drilled up the middle for the cable, sliding in that hole
and locked with a band clamp. The custom board (§14) is two-sided: **AS5311 on the tape-facing side**,
jack and passives on the other. Sliding the puck sets the 0.3 mm gap - close with a feeler gauge, then
**confirm with the sensor itself**: `MagINCn` and `MagDECn` are both off only in the GREEN range (§1.3),
which tests the thing that actually matters (field amplitude) rather than a proxy for it. Aluminium is
required here; steel would distort the field.

**Bore: 30 mm deep** (decided 2026-08-25). The board sits hard at the bottom of the puck - the AS5311 has
to be within 0.3 mm of the tape - so the whole 30 mm is above the board's top face, and it is spent like
this:

| | |
|---|---|
| Jack above the PCB (`69255` DIM C) | 15.62 mm |
| **Left for the plug tail + boot** | **14.38 mm** |

**That makes the slim patch cable a requirement, not a preference.** A standard RJ45 boot stands roughly
20 mm proud of the jack opening and **will not fit** - the plug would bottom out against the end of the
bore before it latched, or hold the puck off its setting. The slim cables (§14, *Choosing the actual
cable*) are far shorter and are what this budget assumes.

Two things to check against a real cable before machining: that the plug **latches** with 14.38 mm of
clearance, and that it can be **released** in situ - a latch tab needs finger or tool access, and a
recessed one 15 mm down a 35 mm bore may not have it. If it does not, that is an argument for the
13.62 mm variant of the jack, which buys back 2 mm.

Open, and worth settling before machining:

- **Anti-rotation.** A round puck in a round hole can spin, and the Hall array is a 2 mm *line* that must
  stay parallel to travel; a band clamp resists rotation only by friction, which vibration erodes. Two
  independent fixes, both worth doing: put the **die centreline on the puck's axis** so rotation cannot
  translate the array (note this means the chip is *not* centred on the puck, since the die sits ~3 mm
  along the package), and add a **positive feature** - a milled flat with a set screw, or a dowel.
- **Repeatable depth.** Servicing the cable means pulling the puck, which loses a gap that was set by
  clamp friction. A shoulder or stop collar that bottoms against the plate makes the setting a mechanical
  constant rather than something to re-dial each time.
- **The puck does not transfer to Z.** It sets a gap perpendicular to the plate face; Z's tape is on the
  plate *edge*, so the sensor approaches from the side and needs a different bracket - with the slide,
  clamp and feeler-gauge adjustment reinvented in that geometry.
- **Z's plate edge must be machined flat and parallel to the travel.** Gap tolerance is a few tenths and
  field strength falls off with it, so an edge wandering more than ~±0.1 mm walks from green into yellow
  partway along. Milled is fine; sawn or sheared is not. The other three axes mount to already-machined
  surfaces, which is the real reason Z is the awkward one (§11.9).
- **Swarf.** The tape is an exposed magnet and collects ferrous debris, which reads as position noise or
  jams the gap. Wood and aluminium chips are harmless; steel is not. Prefer faces that point down or
  inward, and check whether the tape is available with a stainless cover strip.

## 2. Scope

Decided 2026-08-21:

| | In scope |
|---|---|
| **Readout (DRO)** | Report actual position beside commanded, in the `?` report, shown in ioSender |
| **Lost-step alarm** | Raise an alarm when the deviation exceeds a settable per-axis threshold |

**Closed-loop correction is explicitly OUT.** grblHAL is an open-loop step generator whose planner has no
concept of a position error to null out. Feeding measurement back into motion is not a plugin, it is a
motion-control redesign, and a wrong sign or a stale frame *drives* an axis rather than reporting it. If
that is ever wanted it should be a separate design, starting from whether grblHAL is the right firmware
for it at all.

That boundary is what keeps this project tractable: **everything below is observational.** The plugin
reads, compares, and reports. The only action it ever takes is raising an alarm.

## 3. The limit switches stay

Asked 2026-08-21 whether the scales could replace the proximity sensors. **No.** The reasoning, because
this is exactly the kind of decision that gets re-litigated later.

### What a reader does at the end of a tape

The A/B pair carries **no validity information**. As the reader runs past the end of the tape the field
weakens and one of two things happens: the outputs freeze at their last state, or they chatter as the
sensor crosses its detection threshold and emit phantom counts in an arbitrary direction.

Neither is distinguishable, at the ESP32, from a genuinely stationary axis. **The failure is silent**,
and that alone settles it.

> **Refined 2026-08-25, and only partly.** The *A/B pair* still carries no validity information — that
> stays true. But the AS5311 has a separate `MagDECn` pin that is asserted exactly when the field is out
> of range, which is what an off-tape reader sees (§1.3). So the condition **is** detectable if that pin
> is wired, and the plan is to wire it. The conclusion below does not change: the reasons in
> *Fail-closed versus fail-open* and *Three more reasons* are each sufficient on their own and none of
> them depends on detectability.

### Fail-closed versus fail-open

| | Limit switch (NC) | Quadrature encoder |
|---|---|---|
| Broken wire | Reads **triggered** - machine stops | Reads **not moving** - machine drives on |
| Dead sensor | Reads triggered | Reads not moving |
| Connector out | Reads triggered | Reads not moving |

A normally-closed switch is fail-closed: every way it can break is a way it stops the machine. The
encoder is fail-open - every way it breaks looks like "all is well, the axis is parked". That is the
wrong direction to fail in for the one device whose job is preventing a crash.

### Three more reasons, each independently sufficient

- **Latency.** A hard limit is wired into the driver and can stop motion inside the ISR. A CAN report
  must be decoded, transmitted, received and compared. At a 16k rapid (267 mm/s) the axis is tens of
  millimetres further on before anything can notice that position stopped changing.
- **The encoder is not on the failure path.** A slipped coupling, a pinion that loses a set screw, a
  delaminated tape - in each case the encoder stops representing the axis. The switch is a physical
  backstop that does not care how the axis got there.
- **No absolute datum.** Homing is seek → back off → re-seek slowly against a physical reference.
  Incremental quadrature has no reference; it counts from wherever it powered up. Without an index track
  on the tape there is nothing to home *to*.

### The specific one that would bite

`Y_AUTO_SQUARE` squares the gantry by homing Y1 and Y2 **independently against their own switches** and
using the difference. That is the entire mechanism, and `$171` is its tuned result. Removing the Y
switches does not cost a convenience, it removes gantry squaring.

`my_machine.h:63` records that squaring was re-enabled once the loose Y pinion set screw was found. That
capability is worth more than two proximity sensors cost.

### What the scales do buy

- **Soft limits that can be trusted.** `$130`–`$132` are dead-reckoned from the homing datum today.
  Measured position makes them real - and soft limits are the layer that stops most crashes before a hard
  limit is ever involved.
- **Continuous rack detection on the gantry.** Two tapes on Y1/Y2 measure squareness all the time, not
  only at homing. Genuinely new: it would have shown the loose pinion as a drift trend rather than as a
  binding symptom.
- **End-of-tape detection - but only if bought for.** See §11.

## 4. Pin allocation - use CAN3 (pins 30 and 31)

The Teensy 4.1 has three CAN controllers: CAN1 (23, 22), CAN2 (0, 1), CAN3 (30, 31).

Checked against `boards/T41U5XBB_map.h` and the active config in `my_machine.h`:

| Bus | Pins | Verdict |
|---|---|---|
| CAN1 | 22, 23 | **Unusable.** 22 = `Z_LIMIT_PIN`, 23 = `M3_LIMIT_PIN` — the Y2 limit that `Y_AUTO_SQUARE` depends on |
| CAN2 | 0, 1 | Free in firmware — neither pin appears anywhere in the board map — but **unverified whether the T41U5XBB carrier breaks them out at all** |
| CAN3 | 30, 31 | **Use this.** 30 = `AUXINPUT1` (ST1), 31 = `AUXOUTPUT0`. Both on accessible terminals |

Why CAN3 rather than chasing CAN2:

- Both pins are already brought out to terminals, so no probing and no hardware question.
- Neither is bound to a function under the current config. `MOTOR_WARNING_ENABLE` is off (would take
  `AUXINPUT1`), `ENCODER_ENABLE` is off (would take it for QEI), and there is no second spindle (would
  take `AUXOUTPUT0` for direction). They are generic `$P` aux ports today.
- **CAN3 is the CAN-FD controller** on the Teensy 4.1; CAN1 and CAN2 are 2.0B only. 64-byte frames mean
  four axes plus sequence and status fit in one frame — which matters for §6.

**Cost:** one aux input and one aux output. `MOTOR_FAULT_ENABLE` uses `AUXINPUT0` (pin 36) and is
unaffected. Removing the two defines from the board map is the whole change on that side.

## 5. The central design problem: staleness

This is the part to get right, and the reason a naive implementation produces a machine that alarms
constantly and gets switched off.

**A measured position is always older than the commanded position it is compared against.** The delay is
the sum of encoder decode, ESP32 processing, CAN transmit, and grblHAL's receive-to-report path. Call it
`T`. During a move, the apparent deviation is:

```
apparent error  =  feed x T   +   real error
```

At a 16,000 mm/min rapid (≈267 mm/s), that first term dwarfs anything a lost step contributes:

| Latency `T` | Apparent error at 267 mm/s |
|---|---|
| 1 ms | 0.27 mm |
| 5 ms | 1.33 mm |
| 10 ms | 2.67 mm |
| 20 ms | 5.33 mm |

A genuine lost step is a fraction of a millimetre. **A threshold loose enough not to trip on latency is
too loose to detect what it exists to detect.** Comparing instantaneous commanded against delayed actual
does not work at any threshold — this is not a tuning problem.

Three ways out, in increasing order of cost:

**(a) Compare only when stationary.** Check at the end of each move, or whenever the planner is idle and
velocity is zero. Latency stops mattering because nothing is changing. Catches the cumulative error that
actually ruins a part, and cannot false-alarm on following distance.
*Recommended for phase 1.* Simple, robust, and it detects the failure that matters — a job that finishes
in the wrong place.

**(b) Compare against a delayed copy of commanded.** Keep a short ring buffer of commanded positions and
compare the measured sample against the commanded value from `T` ago. Needs `T` to be known and stable,
which over CAN it roughly is. Gives continuous monitoring during motion.

**(c) Timestamp both ends and interpolate.** The ESP32 stamps each sample; the Teensy maintains a clock
offset and interpolates commanded position to the sample's timestamp. Most accurate, needs time sync,
and the sync itself becomes a thing that can be silently wrong.

Do (a) first. It is genuinely useful on its own, and it is the baseline against which (b) can be shown
to work — build (b) only when (a) is trusted and its limits are the thing in the way.

## 6. CAN frame design

One CAN-FD frame per sample carrying all four axes, rather than one frame per axis. A single frame is
atomic: every axis comes from the same instant, and there is no partial update to reason about. This
matters most for Y1/Y2, where the whole point is the *difference* between two axes — reading them from
two frames would make rack indistinguishable from sampling skew.

Sketch, not final:

| Field | Bytes | Notes |
|---|---|---|
| `seq` | 1 | Increments per sample; wraps. A gap means a dropped frame |
| `flags` | 1 | Per-source validity, ESP32 reboot indicator, reader fault / weak-field |
| `t_us` | 4 | ESP32 microsecond timestamp — unused by phase 1, present so (b)/(c) do not need a protocol change |
| `pos[4]` | 4 each | Position per axis, signed |

Units: **int32 nanometres** gives ±2.147 m of range at 1 nm resolution — comfortably beyond both machine
travel and any mag tape's real resolution (typically 1–5 µm), with no floating point on the wire and no
scaling convention to get wrong at one end. Note this is the *wire* format; §1.1 is about the ESP32's
internal counter, which is a separate range problem.

Rate: 100 Hz is ample for a DRO and for §5(a). 1 kHz is affordable on CAN-FD if (b) later wants it. Pick
the rate the alarm needs, not the maximum the bus allows — every frame is work on both ends.

`seq` and `flags` are not optional garnish. §8 and §9 depend on both.

## 7. grblHAL integration

Confirmed present in this tree, so none of this requires forking the core:

- **`src/plugins/`** already holds 15 plugins — a supported extension point.
- **`grbl/core_handlers.h:109`** — `on_realtime_report_ptr`, the hook that appends fields to the `?`
  status report. The plugin chains onto it and adds an actual-position field.
- **`grbl/core_handlers.h:104`** — `on_report_options_ptr`, so the plugin announces itself in `$I`.
  ioSender should key its display off that rather than assuming the field exists.

What is genuinely new: **there is no CAN support of any kind in this driver.** Grepped for `FlexCAN`,
`CAN_ENABLE`, `CAN_TX`/`CAN_RX` across the whole tree — zero hits. FlexCAN_T4 integration is from
scratch, and it is the piece with no prior art here to copy.

Note `src/encoder/` and `ENCODER_ENABLE` exist but are **not** reusable: that is spindle/MPG quadrature,
not per-axis linear scales, and it hangs off different plumbing.

### Settings

Plugin settings group, `$`-numbered in the plugin range:

- enable mask (which axes are monitored — partial fitment must be normal, not a special case)
- deviation threshold, per axis
- comms timeout before the feed is declared stale
- what a sustained comms loss does (see §9)

Per-axis threshold rather than one global: a gantry axis has different real-world slop from a ballscrew
Z, and one number forces the loosest axis to set the sensitivity for all of them.

## 8. Reference frame, zeroing, and the reboot problem

The scale measures **its own position along the tape**. grblHAL's machine coordinates come from homing.
These are different origins and nothing correlates them automatically.

- Establish an offset at homing: after a successful home, record `encoder_raw - machine_position` per
  axis. Comparison uses that offset thereafter.
- **The offset is invalid until homing has run.** Before that, report actual position if you like but do
  not compare, and do not alarm. A comparison against an unestablished reference is exactly the kind of
  confident wrong answer that costs a part.
- **If the ESP32 reboots, its count restarts and the offset is silently wrong.** This must be detectable
  — hence the reboot indicator in `flags` and the `seq` discontinuity. On detection: invalidate the
  offset, stop comparing, and say so. Do **not** re-derive the offset automatically from current
  position, because that would define whatever error exists at that moment as zero and permanently
  conceal it.

## 9. Failure modes and what each should do

| Failure | Behaviour |
|---|---|
| No frames since boot | Report "not present". Not an error — partial fitment is legitimate |
| Frames stop mid-job | **Decide deliberately.** See below |
| `seq` gap (dropped frame) | Skip that comparison; count it. A rate worth reporting, not an alarm |
| ESP32 reboot flag | Invalidate offset, stop comparing, require re-home. Never silently re-zero |
| Deviation over threshold | Alarm |
| Reader fault / weak field | Treat that axis as unmonitored, report it. This is the end-of-tape case from §3 — **only available if the reader has such an output** |

The mid-job comms loss deserves thought rather than a default. Alarming on a single glitch is expensive —
it stops a job that was running correctly. Ignoring it silently is worse, because monitoring the operator
believes is running has quietly stopped. Suggested: a visible status flag immediately, alarm only on
**sustained** loss past the configured timeout, with the timeout settable and the flag always visible in
the report so "is it actually watching?" is answerable at a glance.

Whatever is chosen, it must **fail visibly**. The failure mode to design against is not a false alarm —
it is the operator believing an axis is monitored when it is not.

## 10. ioSender side

Both ends are ours, which removes the usual protocol-negotiation problem.

- Parse the new report field; gate on the `$I` option string so an un-flashed controller degrades to the
  existing display rather than showing blanks.
- Show actual beside commanded, and the deviation.
- Y1 vs Y2 difference deserves its own readout, not just two numbers to subtract by eye. That difference
  is the rack, and it is the number with diagnostic value.
- Make "monitoring is live" visibly distinct from "deviation is zero". They look identical on a DRO and
  mean opposite things — a dead feed reads as perfect tracking. This is the same failure the ioSender
  work has hit repeatedly: unknown rendered as a confident value.

## 11. Open questions

Listed so they are not rediscovered. The first two gate a purchase.

1. ~~Does the reader have a signal-valid / weak-field / error output?~~ **Answered 2026-08-25: yes.**
   The AS5311's `MagDECn` pin is asserted exactly in the RED range, which is what an off-tape reader
   (no field) looks like. Wire one per axis into `flags`; decode table and pin budget in §1.3 and §14.
2. ~~Does the tape have a reference/index track?~~ **Answered 2026-08-25: effectively no.** The AS5311
   emits an Index pulse, but once per 2 mm pole pair — it repeats, so it is not a datum and homing-to-index
   is not available from it (§1.3). The scales stay purely relative; §8 stands unchanged.
3. ~~Tape resolution and repeatability~~ **Answered 2026-08-25 from the datasheet** (§1.3): 1.95 µm/step
   incremental, 3.9 µm hysteresis, 0.6 µm RMS transition noise, ±0.97 µm DNL. So §5's threshold cannot
   usefully go below ~5 µm. Still worth **measuring on the actual machine** — the quoted figures assume an
   ideal magnet at the specified 0.3 mm gap, and the mounting will not be ideal.
4. **Measured end-to-end latency `T`.** §5 is parameterised on it. Measure, do not estimate.
5. **Bus topology and termination** — node count, cable length, whether anything else ever joins.
6. ~~What do the Hall readers output?~~ **Answered 2026-08-21: A/B quadrature**, into ESP32-S3 PCNT.
7. ~~Which axes get tapes?~~ **Answered: four — X, Y1, Y2, Z.**
8. Whether the ESP32 is needed at all, or whether the readers could feed the Teensy directly. Cable
   length and noise argue for the ESP32 at the machine end; pin scarcity on the Teensy argues the same
   way. Recorded as considered and rejected for those reasons, not overlooked.
9. **How the Z reader mounts.** The other three are placed (§1.4); Z is the awkward one - the sensor has
   to come out of the side of the Z plate, and the scale has to go somewhere that survives the full Z
   travel. Still in scope, still unsolved mechanically. Its GPIOs and PCNT unit stay reserved (§14) so
   nothing has to be rearranged when it is.
10. **Whether the spindle cable stays in the drag chain** (§14). Running as-is for now; the fallback route
    is already chosen. Listed because the answer arrives as drifting counts, not as an obvious fault.

## 12. Phasing

Each phase is independently testable and useful on its own — the point being that nothing later is a
prerequisite for value from what is already done.

1. **ESP32-S3 → CAN, standalone.** Frames on the wire, verified with a bus analyser. No Teensy
   involvement. Includes PCNT overflow accumulation (§1.1) — prove a count survives many wraps before
   trusting anything downstream of it.
2. **FlexCAN_T4 receive on the Teensy.** Frames arriving, counted, logged. No grblHAL integration.
3. **Plugin + `on_realtime_report`.** Actual position in the `?` report. Read-only, no comparison.
4. **ioSender display.** The chain is now visible end to end, which is what makes phase 5 debuggable.
5. **Offset at homing + stationary comparison + alarm** (§5a). The first phase that can stop a machine —
   and worth its own hardware-verified session rather than being tacked onto phase 4.
6. Optional: continuous monitoring during motion (§5b), once (a) is trusted.

## 13. Evidence already gathered

So the next session does not repeat it:

- `boards/T41U5XBB_map.h` is the pin map; `my_machine.h:60` selects the board; `driver.h:~103` chains
  them. `boards/generic_map.h` is included **after** as a fallback, so a mistyped pin name silently takes
  a default instead of failing to compile — grep the exact symbol when overriding.
- Pins 22, 23 taken (Z limit, M3/Y2 limit). Pins 0, 1 unreferenced in this board map. Pins 30, 31 are
  `AUXINPUT1` / `AUXOUTPUT0`, unbound under the current config.
- Active config: `Y_GANGED` + `Y_AUTO_SQUARE` (so `N_ABC_MOTORS` = 1, M3 in use, M4 not),
  `MOTOR_FAULT_ENABLE` on `AUXINPUT0` (pin 36), `TOOLSETTER_ENABLE` on `AUXINPUT6` (pin 29),
  `CONTROL_ENABLE 0`, no `ENCODER_ENABLE`, no `MOTOR_WARNING_ENABLE`, no second spindle.
- No CAN support anywhere in the driver tree.
- ESP32-S3 PCNT: 4 units, 2 channels each, 16-bit signed counters.

## 14. Encoder wiring - AS5311 to ESP32-S3

Longest run **2.4 m** (user, 2026-08-25). Sensor specs in §1.3; header pin map in
[`hardware-esp32-s3-rs485-can.md`](hardware-esp32-s3-rs485-can.md).

### Bandwidth is a non-issue; noise is the whole problem

512 steps/mm means **128 quadrature cycles/mm**, so even a 5 m/min rapid is only **~10.7 kHz per
channel** - a 93 µs period against a cable that settles in well under a microsecond. Length,
capacitance, reflections and propagation simply do not matter at 2.4 m.

What matters is that **quadrature has no error recovery**. One induced glitch is one count, permanently.
It never self-corrects, the position stays wrong until the next homing, and it reads as an entirely
plausible number. That is the same silent-wrongness this whole document is organised around (§3, §5,
§9), arriving through the cable instead of through the sensor.

The enormous timing margin is the thing to spend: filter aggressively, because nothing here is fast.

### The build

1. **Run the AS5311 at 3.3 V, not 5 V.** The datasheet supports either, and V<sub>OH</sub> = VDD-0.5
   gives a 2.8 V high - comfortably above the S3's V<sub>IH</sub>. **ESP32-S3 GPIOs are not 5 V
   tolerant**, so the 5 V option means level-shifting every line. There is no reason to take it.
2. **Shielded cable, twisted pairs, each signal twisted with its own ground return** - A/GND, B/GND,
   and a pair for 3V3/GND. *Not* A twisted with B. Pairing a signal with its return is what shrinks the
   loop area, and loop area is what couples the noise. 24 AWG multi-pair instrumentation cable, or
   CAT5e F/UTP, is fine.
3. **Shield to chassis at the ESP32 end only.** Both ends is a ground loop that injects current into the
   signal return.
4. **Series 100-220 Ω at the AS5311 output, 330 pF-1 nF to ground at the ESP32.** An RC in the tens of
   nanoseconds is invisible to a 10 kHz signal and swallows coupled spikes.
5. **Decouple at the sensor** - 100 nF + 10 µF. 2.4 m of 24 AWG has enough R and L that a supply dip
   during stepper commutation appears as an output glitch.
6. **Enable PCNT's hardware glitch filter.** Free rejection of anything under a microsecond, in the
   counter itself. Confirm the ESP32-S3 driver's API and units when implementing.
7. **Route away from motor phase and VFD cable** - separate bundle, separate drag-chain lane where
   possible, cross at 90°.

### The spindle cable shares the drag chain - the one to watch

Per §1.4 the two gantry-end cables run inside the extrusion and then through the drag chain, which today
also carries **the spindle cable** and the stepper cables. A VFD spindle lead is the worst emitter on the
machine - fast PWM edges into a long cable - and in the chain it runs *parallel* to the encoder cables
for their whole length, which is the geometry that couples best.

Two things soften it: these signals are slow enough to filter hard, and the gantry portion is inside
aluminium extrusion. The steppers matter much less - slower edges into a non-switching load.

**The decision, so it is not re-derived while debugging:** run it as-is, but if anything looks wrong, the
spindle cable is the **first** thing to move, not the last. The route is already identified - overhead
with the coolant and air lines, out of the chain entirely. What makes this worth writing down is the
failure signature: not "it does not work", but counts drifting over hours, which reads exactly like lost
steps and sends you looking at the mechanics.

Regardless of chain sharing: the spindle cable must be shielded with **its shield landed at the VFD
end**, and the encoder cables should use a different channel of the extrusion from anything switching.

**If count drift ever appears**, escalate to RS422: AM26C31 driver at the sensor, AM26C32 receiver at
the ESP32. That is what industrial encoders do and it makes 2.4 m trivially safe. Held in reserve rather
than built first, because these signals are slow enough that the measures above should be sufficient -
and the escalation is two ICs and a 2-pair cable per axis whenever it is needed.

### Pin budget - it fits exactly

12 free GPIOs on the header (IO3-IO14):

| Signal | Count | Pins |
|---|---|---|
| A/B quadrature, 4 axes | 8 | 4 PCNT units, both channels each |
| `MagDECn`, one per axis | 4 | per-axis RED / off-tape flag (§1.3) |
| **Total** | **12** | exactly IO3-IO14 |

`MagDECn` alone is the useful line: asserted ⟺ RED, so it gives a clean per-axis fault without needing
`MagINCn` too. If the YELLOW early-warning is wanted later, the four `MagINCn` pins are open-drain and
so **wire-OR onto a single line** with one pull-up - and `IO1`/`IO2` are still free on the SH1.0
connector, off the 20-pin header entirely. Use a stiffer pull-up (~2.2 kΩ) and filter it hard: a
high-impedance open-drain bus over 2.4 m is the most noise-prone thing in this design, and it is a
static signal, so there is no cost to filtering it heavily.

### CAT5, one cable per sensor - and the pair count is what decides it

Each sensor needs five conductors' worth of signal - 3V3, GND, A, B, `MagDECn` - and CAT5's four pairs
give exactly four signal-plus-return pairs. It fits, with nothing spare:

| Pair | T568B pins | Colours | Carries |
|---|---|---|---|
| 2 | 1, 2 | white-orange / orange | **A** + GND return |
| 3 | 3, 6 | white-green / green | **B** + GND return |
| 1 | 4, 5 | blue / white-blue | **3V3** + GND (power pair) |
| 4 | 7, 8 | white-brown / brown | **MagDECn** + GND return |

All four GND conductors are the same net at both ends. That is intended: at DC the return splits by
resistance, but the fast edges - the part that couples - return through the adjacent conductor in their
own twist, which is what collapses the loop area.

**Do not trunk several sensors into one cable.** Eight conductors would carry eight signals with *no*
returns, single-ended against a distant ground - strictly worse than unshielded zip cord. The pair
count, not tidiness, settles the earlier open question: **one cable per sensor.**

Power over one pair is ample. The AS5311 draws 16 mA typ / 21 mA max (§1.3), so 2.4 m of 24 AWG drops
~8.5 mV round trip, and even 28 AWG slim cable only ~22 mV, against a 3.0 V minimum on a 3.3 V rail.

`Index` gets no conductor: per §1.3 it is not a datum.

### Choosing the actual cable

- **Shielded (F/UTP or S/FTP).** Not optional here - it is the whole §14 premise. Many slim patch cables
  are UTP; check before buying.
- **Stranded, and continuous-flex rated for the drag-chain run.** Structured-wiring CAT5 is solid core
  and **will work-harden and break** in a drag chain. Patch cable is stranded and better, but still not
  built for continuous flexing; the run through the chain wants proper flex/torsion-rated Ethernet cable.
  The static runs inside the extrusion can be anything.
- **28 AWG slim is electrically fine** (see the drop above) and the small bend radius suits a drag chain.
- **"It works fine for PoE" does not transfer.** Ethernet is differential, transformer-isolated, and
  error-corrected; PoE only proves current capacity. These are single-ended CMOS signals with no error
  detection, where one coupled glitch is a permanent count error. The cable can be excellent for one and
  marginal for the other.

### Connectors - let the jack enforce the single-point shield ground

§14 requires the shield bonded at the controller end **only**. Shielded RJ45 hardware defeats that by
default: metal-shell plugs bond shield to jack shell at both ends, creating exactly the ground loop
being avoided. Choose the hardware so it cannot happen:

- **Controller end: shielded (metal) PCB jack**, shell bonded to chassis. This is the intended ground.
- **Sensor end: plastic, unshielded jack.** The plug's shield shell then has nothing to bond to, so the
  foil/drain floats at that end - correct by construction rather than by remembering.
  **Part chosen: Amphenol ICC `69255-004LF`** - 8P8C, vertical, through-hole, unshielded, **no integrated
  magnetics**. Its Cat3 rating is irrelevant here: that is an Ethernet bandwidth grade, and these are
  DC-coupled signals at ~10 kHz. Drawing in [`manufacturer-assets/`](../manufacturer-assets/index.html).
  **Height above PCB (drawing DIM C): 15.62 mm** - 13.62 mm on one variant of the series, worth
  identifying before ordering if the puck's bore depth gets tight (§1.4). "Vertical" means the plug
  inserts perpendicular to the board, i.e. along the puck axis, which is what suits the cable running
  straight up the middle.

**Buy jacks WITHOUT integrated magnetics - both ends.** A large fraction of PCB RJ45 jacks are MagJacks
with transformers inside. They pass Ethernet perfectly and **block DC completely**, and every signal
here is DC-coupled, so a MagJack means nothing works at all. Check the part number on the 4-jack
controller board as well as on the sensor boards.

### The sensor board: carry the chip, not a breakout

Decided 2026-08-25: **a custom board with the AS5311 on it**, an RJ45 jack and the passives - not a
carrier that a breakout plugs into. The reason is mechanical, not electrical.

What decides accuracy is where the **Hall array** sits relative to the magnetic strip, and Figure 14
(p.21 of [`AS5311-Datasheet.pdf`](../manufacturer-assets/index.html)) gives the datums: the array is **2.0 mm long,
centred on the die centreline**, which sits **3.035 ±0.235 mm** along the package and **2.576 / 3.200
±0.235 mm** across it, with **0.245 ±0.100** and **0.755 ±0.100 mm** around the die plane vertically.

**Those tolerances are the point.** The die's position inside its own package is already ±0.235 mm,
against a ±0.5 mm lateral budget (§1.3). There is no room to stack a breakout's mounting-hole tolerance
and an adapter on top of it. On a custom board the array-to-mounting-hole relationship is a fab
tolerance (~±0.1 mm) that is *yours*, and dropping the stacked board and headers also gets the package
closer to the strip - the other half of the same budget. TSSOP-20 on 0.65 mm pitch is hand-solderable,
so the chip is not the obstacle.

Transfer those datums from the figure directly when laying out; the numbers above were read off a
rendered page and the reference edges deserve a second look.

#### The pins a breakout was quietly handling

| Pin | Must be | Why it matters |
|---|---|---|
| **14 CSn** | **tied LOW** | "Must be low to enable incremental outputs", and it has an internal ~50 kΩ pull-up. Left floating, **A/B/Index stay locked high after power-up** - the board looks and measures dead. |
| **9 Prog** | to VSS | OTP programming input |
| **18 VDD3V3** | to VDD5V | Regulator output, "do not load externally" - it is not a second rail. This is how 3.3 V operation is selected. |
| **1, 6, 10, 11, 16, 17, 20** | **left unconnected** | The datasheet says so for each. Do not ground NC pins out of habit. |
| **2 MagINCn / 3 MagDECn** | open-drain | Need a pull-up: put it at the **controller** end (~2.2 kΩ) with the RC, so the long line is held stiffly where it is read. |

Tie CSn low through a **0 Ω or solder jumper** rather than a hard trace. Lifting it later allows SSI
readout - absolute position within the pole pair plus the full status word (OCF, COF, LIN, parity),
a far better bench diagnostic than the two hardware pins. Bring CLK and DO to test pads: no GPIO cost.

Also on the board: the series resistors at the source and the 100 nF + 10 µF decoupling (both have to be
at this end anyway), a TVS array on the connector side because it gets handled, and the plastic
unshielded jack per the shield rule above. **Panelise four** - three now, Z later (§11.9).
