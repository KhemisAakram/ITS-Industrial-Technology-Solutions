---
type: wiring
machine: KOTEC KTPG-320 CNC Plasma (SOMIK Skikda)
controller: Digital Dream UC300 (EC500) + Mach3
drive: YE-LI YPV series (X/Y, YE LI YBL13S)
tags: [somik, wiring, ypv, servo, rs232, cn3]
source: YE-LIElectricandMachinery_Manuals_1861.pdf (Appendix 1 + Driver Config, pp. 56-57, 68)
---

# CN3 Connector Cable — YPV Servo Drive (YPV Setup programming)

## What CN3 is
- **CN3** = the YPV drive's **communication connector** — a **9-pin D-Type (DB9) RS-232C** port, top-right of the drive (beside CN1/CN2).
- Purpose: link the drive to a PC running the **"YPV Setup"** program (YE LI icon) to read/write parameters — `CNTL`, `PMOD`, `ELGN/ELGD`, `ENCO`, `RPM`, `PACC`, etc. (see `generate_electric_plane.py` §10).
- Manual note: *"CN3 port is as same as USB, but RS232 is designed for internal use."*
- Connect : power the drive (220V), plug CN3 → PC, open YPV Setup.

## Cable wiring (Appendix 1 — "YPV RS232-USB")
Factory cable = **DB9 (drive side) → USB (PC side)**. Only 3 signals + optional power.

| CN3 (DB9) pin | Signal                        | Wire (factory) | To (USB adapter)  |
| ------------- | ----------------------------- | -------------- | ----------------- |
| **2**         | **TX** (RS-232 transmit)      | White          | USB data+ (rx side) |
| **3**         | **RX** (RS-232 receive)       | Green          | USB data- (tx side) |
| **5**         | **GND** (signal ground)       | Black          | USB GND           |
| **4**         | VCC (power, optional)         | —              | USB 5V            |

- Standard RS-232 DB9: pin 2 = TXD, pin 3 = RXD, pin 5 = GND (only these 3 needed for comms).
- **TX/RX are crossed** (null-modem style, drive ↔ DTE PC). Verify orientation on your actual cable before use.

## Making your own cable
If the YE-LI USB cable is unavailable, use a standard **USB→RS-232 (DB9) adapter**:
1. CN3-2 (TX) → adapter driver RX
2. CN3-3 (RX) → adapter driver TX
3. CN3-5 (GND) → adapter GND
4. Only add CN3-4 (5V) if the adapter requires external power.

## YPV Setup workflow (manual pp. 56-57)
1. Install **YPV Setup** (VER7501 for VER0501 hw; unmarked VER2 = 031220 → use program 031220). Remove older versions first.
2. **Backup the default configuration file** before changing anything.
3. Connect CN3 → PC, power the drive, open the program.
4. `File > Load` config / `File > Save As` config (comment motor spec + speed on the file).
5. `Parameters` → set value → **Enter** → **Burn** → wait ~5 s → **Reboot** to apply.
6. On reboot, confirm the internal parameters/modes reflect your edits.
