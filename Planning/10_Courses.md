---
date: 2026-08-01
tags: [courses, planning]
---

# Courses — Ranked Watch List

**Rule:** every work day · 45 min SOMIK + 45 min VFD (1h30 total) · the Electronics/PCB course replaces whichever track is behind · work top-down · tick off when watched.
Take notes straight into the linked project file so each video feeds the job, not just the playlist.
Friday = recovery, no courses.

---

## SOMIK CNC conversion (watch first — project priority)

Ranked by value to converting the KOTEC KTPG-320 to Mach3. SOMIK axes are **AC servos** → servo videos are Tier 1.

### Tier 1 — before parts lock (📅 2026-09-03)
- [ ] **1.** [Bulkman3d Queenbee Pro — UC300 Mach3 Configuration](https://www.youtube.com/watch?v=nls07DjwXqI) — exact stack match: UC300 + Mach3 → use for config + axis tuning
- [ ] **2.** [Bulkman3d Queenbee Pro — UC300 Controller Wiring](https://www.youtube.com/watch?v=wXa83Jor9fA) — feeds the wiring plan (Sentrol 2 → Mach3 layout)
- [ ] **3.** [How To Setup Chinese AC Servo Motor 80ST-M02430 — Step/Dir + Analog Speed](https://www.youtube.com/watch?v=7Ozw7p_7EPw) — the exact servo drive family SOMIK uses
- [ ] **4.** [Setting up Mach 3 Made Easy How To Part 1 of 2](https://www.youtube.com/watch?v=qwMgmlbDRVw) — foundational Mach3 config: ports & pins, live-5V E-stop, homing, motor tuning, ref each axis
- [ ] **5.** [How To Setup AC Servos with Mach3 USB RNR Board](https://www.youtube.com/watch?v=e9_ye1-ISjQ) — AC servos + Mach3 together, bridging steps 1–4
- [ ] **6.** [DIY Plasma CNC Wiring — Detailed Instructions](https://www.youtube.com/watch?v=Mnb6VxSAvds) — plasma interface / THC wiring for the integration
- [ ] **7.** [Chinese AC Servo — MACH3 Setup (Vs. Stepper Motor)](https://www.youtube.com/watch?v=rfJOJ7xSrlQ) — why servos behave differently under Mach3
- [ ] **8.** [CNCnutz ep 122 — UC300ETH-5LPT with Mach3](https://www.youtube.com/watch?v=_1wqZFhTCVs) — install + pitfalls for the exact motion controller SOMIK uses

### Tier 2 — before machine runs (📅 2026-10-08)
- [ ] **9.** [AC Servo in Velocity Mode as CNC Spindle in MACH3](https://www.youtube.com/watch?v=x6Pp3G4Ia9c) — spindle/velocity control option
- [ ] **10.** [How to install this NEW Mach3 Screenset](https://www.youtube.com/watch?v=MrH7RNtko2g) — clean UI for handover to SOMIK
- [ ] **11.** [Mach 3 Has Never Looked This Good!](https://www.youtube.com/watch?v=7o_V_1AIaXE) — showcase; sells the result
- [ ] **12.** [AC Servo Motors and FogBuster Mist Coolant](https://www.youtube.com/watch?v=bPM9XwzF2LY) — optional coolant add-on
- [ ] **13.** [Mach 4 SUCKS (CNC Software Part 1)](https://www.youtube.com/watch?v=G28eXR42e9w) — context for staying on Mach3
- [ ] **14.** [Build a BIG CNC Plasma Cutter for under 750$](https://www.youtube.com/watch?v=2jZwh6mvMhQ) — budget build reference, optional
- [ ] **15.** [Construction d'une cnc PLASMA Ep1 — Fabrication du chassis](https://www.youtube.com/watch?v=9llIKZ1k8FQ) — FR; chassis build, optional
- [ ] **16.** [CNCnutz ep 129 — How to Troubleshooting the UC300ETH](https://www.youtube.com/watch?v=rzsuPMN7U94) — fix comms/board issues when the machine runs
- [ ] **17.** [CNC tuning (1/4) — Feedback Loop Tuning](https://www.youtube.com/watch?v=qIrf1PMvlNU) — axis stability / accel / jerk principles for the AC servo axes
- [ ] **18.** [Lec #14 How to use Sheetcam for CNC Plasma Cutting](https://www.youtube.com/watch?v=xCvWG4F7wqo) — CAM for the plasma side
- [ ] **19.** [Opensource Standalone Torch Height Control for Plasma Cutting](https://www.youtube.com/watch?v=LxGfTt5eavE) — THC add-on build, optional

---

## VFD repair (VFD-001 — 3 units, 📅 2026-08-22)

Ranked by what actually fixes the 3 client units: repair/testing first, commissioning reference after.

- [ ] **1.** [AC Tech MC-3000 main board test + circuit tracing](https://www.youtube.com/watch?v=g4GWQ6W8XiI) — direct fault-location method for the bench
- [ ] **2.** [No-load induction motor test — INVT GD350A](https://www.youtube.com/watch?v=884SSz0amJM) — how to verify a VFD on the bench without the machine
- [ ] **3.** [IGBT FP25R12KE3 multimeter test](https://www.youtube.com/watch?v=G4Js_QLZQgs) — check the most common dead part
- [ ] **4.** [IGBT test — multimeter method](https://www.youtube.com/watch?v=z3Mdc5qQx8k) — second method, cross-check
- [ ] **5.** [IPM — Intelligent Power Module](https://www.youtube.com/watch?v=Mx7wTclVjbs&list=PLgsKzaoLQUjpDnE8vjR_S07EKKi95fMZk) — module-level diagnosis (playlist)
- [ ] **6.** [Bootstrap gate driving circuit](https://www.youtube.com/watch?v=em5BuCFSuBw) — why outputs stop mid-phase
- [ ] **7.** [Bootstrap capacitor](https://www.youtube.com/watch?v=DvkXXYvWZog) — component-level check
- [ ] **8.** [Introduction to VFD Troubleshooting | Where to Start?](https://www.youtube.com/watch?v=MyFaFsoM8BA) — primer: failure classes + fault codes before touching a board
- [ ] **9.** [Basic VFD Troubleshooting](https://www.youtube.com/watch?v=QS5b7MIgyno) — broad workflow before you touch a board
- [ ] **10.** [VFD Troubleshooting "DC Bus Over Voltage"](https://www.youtube.com/watch?v=rd7Xa5ZbI7E) — field workflow for a specific fault class
- [ ] **11.** [Yaskawa J1000 VFD Complete Wiring & Programming Guide](https://www.youtube.com/watch?v=NQVavdCnrhE) — commissioning reference after repair
- [ ] **12.** [Getting Started with Altivar Process ATV600](https://www.youtube.com/watch?v=1A_9ZUAXjpQ) — commissioning reference (Schneider)
- [ ] **13.** [VFD Braking Resistor Sizing — Real Calculations](https://www.youtube.com/watch?v=9E-Z_fxoNIE) — sizing math, only if a unit needs a braking resistor

---

## Electronics / PCB (all about PCB)

Foundation for the PCB-repair jobs + embedded work (STM32). The PCB course swaps in for whichever of SOMIK/VFD is behind that day.

### Course anchor — take in order (Arabic)
- [ ] [دبلومة الالكترونيات العملية — Practical Electronics Diploma (playlist)](https://www.youtube.com/playlist?list=PLww54WQ2wa5qVh1p8iPi7HspX7N9hbvbc) — the main structured course
- [ ] [دورة الالكترونيات العملية :: 54- مضاعفات الجهد (Voltage Multiplier)](https://www.youtube.com/watch?v=6iKQEyuwbuA) — lesson 54, voltage multipliers

### Power electronics (feeds VFD repair)
- [ ] **1.** [How Buck, Boost & Buck-Boost DC-DC Converters Work](https://www.youtube.com/watch?v=PgTR7226sHU) — power conversion fundamentals
- [ ] **2.** [في المختبر:: 178 — شرح دوائر التغذية النبضية (Switched Mode Power Supply) جزء 1](https://www.youtube.com/watch?v=Eb2KqEKlDsc) — SMPS theory behind VFD internals
- [ ] **3.** [في المختبر:: 219 — Double Pulse Testing + اختبار الضياعات (Losses)](https://www.youtube.com/watch?v=Tl67mSy-dxw) — power-semiconductor testing (IGBTs)
- [ ] **4.** [DIY Linear Power Supply | Part-1](https://www.youtube.com/watch?v=1rAUrbnq2WY) — build a bench supply
- [ ] **5.** [Every Component of a Linear Power Supply Explained](https://www.youtube.com/watch?v=UTetQhGyUVg) — component-level understanding

### PCB design — STM32 / embedded
- [ ] **1.** [KiCad 6 STM32 PCB Design Full Tutorial — Phil's Lab #65](https://www.youtube.com/watch?v=aVUqaB0IMh4) — complete STM32 board: schematic → layout → routing → Gerber
- [ ] **2.** [A simple way to design a professional board — Part 1](https://www.youtube.com/watch?v=d6N_W6E9dgE) — professional layout habits
- [ ] **3.** [How to make your First PCB! Beginner KiCAD Design Tutorial](https://www.youtube.com/watch?v=TJPyqRnhytA) — beginner KiCad flow
- [ ] **4.** [How To Make Your Own Printed Circuit Boards (PCB)](https://www.youtube.com/watch?v=djBMQhjfbys) — design → manufacture overview

### Repair technique (feeds PCB-repair jobs)
- [ ] **1.** [PCB Voltage Testing Explained — Find Faults Fast](https://www.youtube.com/watch?v=9kMwK1EUAzo) — safe voltage-point diagnosis before blind part swapping
- [ ] **2.** [iPhone 15 Pro Max Turns On But NO DISPLAY? (Common Short Fixed!)](https://www.youtube.com/watch?v=5hf8dx5xdbc) — voltage injection + thermal camera short-finding

### Practical / extras
- [ ] **1.** [Connecting a Relay Module to a Microcontroller](https://www.youtube.com/watch?v=FWvEEtrTGRQ) — MCU I/O for controller builds
- [ ] **2.** [Carvera Air Cnc — Double Sided PCB Milling](https://www.youtube.com/watch?v=EiicIzQ-ReA) — PCB milling on a CNC
- **Channels:** [Phil's Lab](https://www.youtube.com/@PhilsLab) — STM32/embedded design · [EEVblog playlists](https://www.youtube.com/@EEVblog/playlists)
