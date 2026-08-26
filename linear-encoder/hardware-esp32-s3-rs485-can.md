# Waveshare ESP32-S3-RS485-CAN - pin allocation

The module in [`design-can-position-feedback.md`](design-can-position-feedback.md): an ESP32-S3 that
decodes the Hall readers' A/B quadrature in PCNT and reports position to the Teensy over CAN.

**Why this file exists:** the Waveshare wiki does **not** document the 20-pin header's GPIOs - it lists
only the 4-pin SH1.0 connector. The header map exists solely in the schematic, as component `P1`, so it
is easy to look for and conclude it was never published. It was extracted here once and lost; the
schematic is now committed beside this file.

## Sources

| What | Where |
|---|---|
| Wiki | <https://www.waveshare.com/wiki/ESP32-S3-RS485-CAN> |
| Schematic (the authority for everything below) | [`ESP32-S3-RS485-CAN-Schematic.pdf`](ESP32-S3-RS485-CAN-Schematic.pdf) - from <https://files.waveshare.com/wiki/ESP32-S3-RS485-CAN/ESP32-S3-RS485-CAN-Schematic.pdf> |

Both waveshare.com URLs return **HTTP 403 to a plain fetch**; they serve normally with a browser
User-Agent. That is what makes this hard to re-find with a tool rather than a browser.

## P1 - the 20-pin header (2x10, 2.0 mm pitch)

Odd pins are the left column, even the right.

| Pin | Signal | | Pin | Signal |
|---|---|---|---|---|
| 1 | 3V3 | | 2 | 5V |
| 3 | GND | | 4 | GND |
| 5 | TXD - GPIO43 (U0TXD) | | 6 | D_P - GPIO20 (USB D+) |
| 7 | RXD - GPIO44 (U0RXD) | | 8 | D_N - GPIO19 (USB D-) |
| 9 | **IO3** | | 10 | **IO14** |
| 11 | **IO4** | | 12 | **IO13** |
| 13 | **IO5** | | 14 | **IO12** |
| 15 | **IO6** | | 16 | **IO11** |
| 17 | **IO7** | | 18 | **IO10** |
| 19 | **IO8** | | 20 | **IO9** |

**Twelve free GPIOs on the header: IO3-IO14.**

`TXD`/`RXD` are labelled by function, not number, in the schematic. They are GPIO43/GPIO44: they land on
module pins 49/50 (`U0TXD`/`U0RXD`) and sit between `IO42` and `IO45` in the schematic's own numerically
ordered GPIO table. Identified from the document, not assumed.

## What the board already uses

From the GPIO allocation table on the left of the schematic.

| Function | GPIOs |
|---|---|
| CAN / TWAI | **IO15 = TXD2, IO16 = RXD2** |
| RS485 | **IO17 = TXD1, IO18 = RXD1, IO21 = RS485_EN** (automatic direction switching) |
| USB | IO19 = D_N, IO20 = D_P |
| RTC (PCF85063) | IO38 = SCL, IO39 = SDA, IO40 = INT |
| Internal (PSRAM / flash) | IO33-IO37 |
| Boot button | IO0 |
| UART0 | GPIO43 (TXD) / GPIO44 (RXD) - also on header pins 5 and 7 |

That table's **Relay, DIN, Network, EXIO and SD Card columns are empty** on this board - it is a table
shared across the product family, so a blank column means "not fitted here", not "undocumented".

**IO1 and IO2 are not on P1.** They come out on the SH1.0 connector `J4` (GND, 3V3, GPIO2, GPIO1) - the
only GPIOs the wiki page itself documents.

## Consequences for the encoder design

Four axes x A/B = **8 inputs**, and IO3-IO14 gives 12. Comfortable, and it matches
[`design-can-position-feedback.md`](design-can-position-feedback.md) §1.1: PCNT has exactly 4 units,
one per axis, no spare.

- **GPIO3 is a strapping pin** (JTAG source select) on the ESP32-S3 - fine as an input after boot, but
  it must not be driven during reset. This is general ESP32-S3 knowledge, **not** from this schematic.
  Using IO4-IO14 and leaving header pin 9 unused sidesteps the question entirely.
- **IO19/IO20 are USB.** They are on the header as D_N/D_P; taking them costs the USB port.
- Nothing else on the header is shared with the RS485 or CAN transceivers, so an encoder harness on
  IO4-IO14 cannot interfere with the bus this board exists to drive.

## Board power

DC 7-36 V wide-input screw terminal, 3.3 V / 2 A onboard DC-DC, plus USB Type-C (power, flashing,
communication). Isolated RS485 and CAN sides, each with a jumper-enabled 120R termination resistor.
