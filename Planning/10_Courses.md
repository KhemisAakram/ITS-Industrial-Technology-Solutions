---
date: 2026-08-01
tags: [courses, planning]
---

# Courses — Ranked Watch List

**Rule:** Block 4 [LOW] only · 30 min/day · work top-down · tick off when watched.
Take notes straight into the linked project file so each video feeds the job, not just the playlist.

---

## SOMIK CNC conversion (watch first — project priority)

Ranked by value to converting the KOTEC KTPG-320 to Mach3. SOMIK axes are **AC servos** → servo videos are Tier 1.

### Tier 1 — before parts lock (📅 2026-09-03)
- [ ] **1.** [Bulkman3d Queenbee Pro — UC300 Mach3 Configuration](https://www.youtube.com/watch?v=nls07DjwXqI) — exact stack match: UC300 + Mach3 → use for config + axis tuning
- [ ] **2.** [Bulkman3d Queenbee Pro — UC300 Controller Wiring](https://www.youtube.com/watch?v=wXa83Jor9fA) — feeds the wiring plan (Sentrol 2 → Mach3 layout)
- [ ] **3.** [How To Setup Chinese AC Servo Motor 80ST-M02430 — Step/Dir + Analog Speed](https://www.youtube.com/watch?v=7Ozw7p_7EPw) — the exact servo drive family SOMIK uses
- [ ] **4.** [How To Setup AC Servos with Mach3 USB RNR Board](https://www.youtube.com/watch?v=e9_ye1-ISjQ) — AC servos + Mach3 together, bridging steps 1–3
- [ ] **5.** [DIY Plasma CNC Wiring — Detailed Instructions](https://www.youtube.com/watch?v=Mnb6VxSAvds) — plasma interface / THC wiring for the integration
- [ ] **6.** [Chinese AC Servo — MACH3 Setup (Vs. Stepper Motor)](https://www.youtube.com/watch?v=rfJOJ7xSrlQ) — why servos behave differently under Mach3

### Tier 2 — before machine runs (📅 2026-10-08)
- [ ] **7.** [AC Servo in Velocity Mode as CNC Spindle in MACH3](https://www.youtube.com/watch?v=x6Pp3G4Ia9c) — spindle/velocity control option
- [ ] **8.** [How to install this NEW Mach3 Screenset](https://www.youtube.com/watch?v=MrH7RNtko2g) — clean UI for handover to SOMIK
- [ ] **9.** [Mach 3 Has Never Looked This Good!](https://www.youtube.com/watch?v=7o_V_1AIaXE) — showcase; sells the result
- [ ] **10.** [AC Servo Motors and FogBuster Mist Coolant](https://www.youtube.com/watch?v=bPM9XwzF2LY) — optional coolant add-on
- [ ] **11.** [Mach 4 SUCKS (CNC Software Part 1)](https://www.youtube.com/watch?v=G28eXR42e9w) — context for staying on Mach3
- [ ] **12.** [Build a BIG CNC Plasma Cutter for under 750$](https://www.youtube.com/watch?v=2jZwh6mvMhQ) — budget build reference, optional
- [ ] **13.** [Construction d'une cnc PLASMA Ep1 — Fabrication du chassis](https://www.youtube.com/watch?v=9llIKZ1k8FQ) — FR; chassis build, optional

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
- [ ] **8.** [Basic VFD Troubleshooting](https://www.youtube.com/watch?v=QS5b7MIgyno) — broad workflow before you touch a board
- [ ] **9.** [Yaskawa J1000 VFD Complete Wiring & Programming Guide](https://www.youtube.com/watch?v=NQVavdCnrhE) — commissioning reference after repair
- [ ] **10.** [Getting Started with Altivar Process ATV600](https://www.youtube.com/watch?v=1A_9ZUAXjpQ) — commissioning reference (Schneider)
- [ ] **11.** [VFD Braking Resistor Sizing — Real Calculations](https://www.youtube.com/watch?v=9E-Z_fxoNIE) — sizing math, only if a unit needs a braking resistor
