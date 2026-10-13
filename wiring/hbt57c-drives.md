# The HBT57C drives - faults, clearing them, and configuring them

**TOSEASTARS HBT57C integrated closed-loop steppers.** 57 frame / NEMA 23, **24-55 V DC**, 36 V
recommended, drive mounted at the motor. Four of them, one per axis.

How they are *wired* is [`breakout-box.md`](breakout-box.md) - the AL pull-up, the opto commons, the
star rule and the no-daisy-chaining rule all live there because they are properties of the cabinet.
This file is what the drive itself does: how it reports a fault, how a fault gets cleared, and what
can be configured.

OPEN: **THE MANUAL IS STILL NOT COMMITTED.** This repo's standing rule is that datasheets are copied
in, not linked, and [`../manufacturer-assets/`](../manufacturer-assets/) does not have it. Everything
below was read out of it in an ioSender session on 2026-09-26 and **cannot be re-checked until the
PDF is in the repo.** The manual is thin and machine-translated, which is exactly why a second
reading will be wanted.

## Count the flashes - that is the whole diagnosis

The red LED flashes at 2 Hz - 200 ms on, 300 ms off - in a **5-second cycle**, and the **count**
identifies the fault. Green is power and nothing more.

| Flashes | Fault | What it actually means |
|---|---|---|
| **1** | Over-current, peak 6 A or more | drive or motor fault, or wiring |
| **2** | Over-voltage, 60 V or more | **regeneration on decel** - would need a clamp |
| **7** | Tracking error out of tolerance | tuning, accel, or mechanical binding - **or a crash** |

There is also an **under-voltage trip below 18 V** which is not in the LED table.

NOTE: **THE ONLY FAULT HE HAS EVER SEEN IS 7, from a spindle crashing into the spoilboard on a missed
probe signal** - his, 2026-09-26, across the Mega V's life on the same drive family. That is a
measurement of the installation, not of the drive, and it carries two conclusions. **Do not buy a
brake resistor:** fault 2 has never happened, and buying hardware for an unobserved fault is the
thing this repo argues against. And fault 7 is the one worth being able to tune, which is why the
RS232 cable below matters.

FLAG: **THE DRIVES HAVE NO BRAKE TERMINALS AT ALL** - the 12-pin connector is power, PUL, DIR, EN and
AL, and nothing else. If regeneration ever did need handling it goes across the shared DC bus at the
PSU as a **clamp or shunt regulator**, never a bare resistor. The VFD's brake resistor is on its own
mains-referenced bus of order 340 V DC and is **utterly unrelated - never connect the two.**

OPEN: **THE MANUAL DISAGREES WITH ITSELF ON THE OVER-VOLTAGE TRIP POINT, so design to 55 V.** The
spec table gives 55 / 60 / 65 as min / typ / max, the protection section says "higher than 55 Vdc",
and the LED table says 60 V or more. **The only number that matters is the drive that trips first**,
which is the minimum. This is the figure
[`breakout-box.md`](breakout-box.md)'s rail-voltage question is measured against, and it is stated
here rather than cited from a memory note, which is where it used to live.

## Clearing a fault - UNRESOLVED, and the vendor contradicted itself

OPEN: **THE VENDOR ANSWERED BOTH WAYS IN ONE MESSAGE, so this is a bench question and not an email
question.** The manual says only a power cycle clears a fault - "the fault must be removed and reset
by power-on", stated for all four protections - and current practice is power-cycling all the
steppers independently of the controller.

Asked directly, TOSEASTARS said first that **only a power-cycle reset is supported** and that EN+ is
only for enabling and disabling; then, in the same message, that **according to their engineering
team the proper way to reset a fault is a 5-24 V signal on ENA+**, either a momentary pulse of a few
hundred ms or a sustained voltage.

Those are three different behaviours, not one answer. A sustained voltage on ENA+ is simply enabling
the drive. And the first answer is somebody paraphrasing the same manual, so its "no" is **absence of
documentation, not evidence of absence** - the distinction this repo's standing rules are explicit
about.

PROCEDURE: **Bench it on a new uncoupled motor, before it goes in the machine.** These are the best
test conditions that will ever be available, and they exist right now - a motor on the bench with
nothing to crash.

1. Wire **EN+ / EN-** out. The manual recommends leaving EN unconnected, so they are almost certainly
   floating on the machine today - which on its own would explain why nobody has seen this work.
2. Pull **AL+** up and put a meter on it. See [`breakout-box.md`](breakout-box.md) for why there is
   no pull-up in the build today, and why it must not be the manual's 24 V one near a Teensy pin.
3. Provoke **fault 7** by holding the shaft during slow motion. It is the fault that actually happens,
   and the only one that can be provoked safely.
4. Pulse **ENA+** for about 500 ms. Watch the red LED and AL together.

**What distinguishes the outcomes:** if the LED clears on the pulse, ENA+ resets faults and the
cabinet can clear a fault without dropping motor power. If it clears only while ENA+ is held, that is
enabling and not resetting. If it does not clear at all, the manual is right and a power cycle is the
only route - which means the cabinet needs the drives' 48 V switchable independently of the
controller, and that is a wiring decision that is cheap during a build and expensive afterwards.

FLAG: **EN POLARITY IS GENUINELY AMBIGUOUS AND MUST BE MEASURED, NOT REASONED.** The FAQ says a low
enable signal prevents motion and that it should be "pulled high or not connected" - but it is an
**opto** input, where floating means no current rather than a logic high. Those two framings predict
opposite behaviour from the same wire. Measure it on the bench rig above while it is set up.

## Configuring them - the RS232 port, and get the cable now

The drive has a **4-pin RS232 debug port**: +5 V out, TXD, RXD, GND. It needs the vendor's own cable,
and **hot-plugging it is forbidden**.

FLAG: **RS232 IS NOT RS485, and the ESP32 board's RS485 port does not speak to it.** The two are named
alike and are not compatible - see
[`../linear-encoder/hardware-esp32-s3-rs485-can.md`](../linear-encoder/hardware-esp32-s3-rs485-can.md)
for what that port is actually for.

Their PC software sets subdivision, current, pulse edge and resonance - and quite possibly the
**tracking-error threshold**, which is what decides how twitchy fault 7 is. **Get the cable while the
machine is being built**, because it is the only route to that threshold and fault 7 is the only
fault this machine has ever produced.

### DIP switches

| Switch | Function |
|---|---|
| SW1-4 | Subdivision. All ON is the driver default, 400 pulse/rev |
| SW5 | Direction |
| SW6 | FOC versus point-to-point mode |

## Two hardware cautions

FLAG: **THERE IS NO REVERSE-POLARITY PROTECTION ON THE POWER INPUT.** Reversing it burns the internal
fuse. Four connectors, all identical, assembled by hand - this is worth a polarity check per drive
before the first power-on rather than after.

The no-daisy-chaining rule and the AL wiring are in [`breakout-box.md`](breakout-box.md), where the
cabinet is described.

## Provenance

Read out of the manual during the 2026-09-26 session, which ran in the **ioSender** repo. The
material was carried in a memory note until 2026-10-12 and is now here, which is where this project
keeps anything the repo can state for itself. The reasoning around it is in that project's
conversation log for that date.

OPEN: **The new machine has its OWN set of HBT57C drives** - the Mega V's go with it when it is sold.
So everything here applies to the machine being kept and should be **designed in rather than
retrofitted**: the AL pull-up and opto into the cabinet from day one, aux inputs reserved for motor
fault **and** driver-power-present before they are all allocated, and the ENA-reset answer known
before the drives are coupled to anything.
