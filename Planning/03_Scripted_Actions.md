---
date: 2026-08-01
tags: [scripts, planning]
---

# Scripted Actions — Checklists so You Never Think About What's Next

> A task is only "scheduled" once it has a script. If a task bounces more than twice, split it and script it here.

## ☀️ Wake-up script (IF/THEN/ELSE — 2 min, first thing)
Run before opening anything else. The answers decide your day.

```
Q0  Yesterday's daily note — was it logged (Log section filled)?
    IF no                 → fill it now (5 min). A day without a log counts as missed.
    ELSE                 → continue

Q1  Day?
    IF Friday            → rest. No blocks. Stop here. (If this week's weekly note is empty, fill it first - 10 min.)
    ELSE                 → continue

Q2  Urgent client message?
    IF yes (job-blocking) → handle it first (15 min max), THEN continue
    ELSE                 → continue

Q3  Energy?
    IF very tired / sick → LIGHT DAY: only Medium + Low blocks, no deep work
    IF medium            → 1 High block, then Medium
    IF fresh             → full 4 blocks

Q4  High-priority work — anything blocked?
    IF SOMIK waiting on parts/delivery  → Block 1+2 = VFD + coil winding
    IF VFD / coil winding blocked       → Block 1+2 = SOMIK + ITS manage
    IF both blocked                     → Block 1+2 = report writing + ITS admin
    IF nothing blocked                  → Block 1+2 = the 2 most profitable tasks

THEN fill the day (3 time slots):
    Early morning = Block 1 + 2 (High) + PCB course first + SOMIK 45 min
    Before noon = Block 3 (Medium) + VFD 45 min
    Evening = Block 4 (optional, Low) + invoice + log hours/revenue + tomorrow's slots
    Previous evening (day before) = plan tomorrow's slots + pick courses
```

**The rule: never start a task without knowing what's blocked and what your energy is.**

## ☀️ Morning start (15 min, every work day)
- [ ] Tea/coffee
- [ ] Q0: check yesterday's note is logged — fill it if missed (5 min)
- [ ] Run the **Wake-up script** above → answers Q1–Q4
- [ ] Check WhatsApp for urgent client messages — **5 min max, then close it** (already handled in Q2? skip)
- [ ] Open today's daily note (Daily Notes plugin)
- [ ] Write today's Blocks 1–4 from [[02_Task_Bank]]
- [ ] First deep-work block starts — phone on silent, away from bench

## 🏭 Workshop session (any block)
- [ ] State the ONE outcome this block must produce
- [ ] Tools/parts ready before starting (no mid-task hunting)
- [ ] Run the block until the outcome is done or the block ends
- [ ] If stuck >30 min: note the blocker, switch to a [[02_Task_Bank|Medium/Low task]]
- [ ] Snap 1–2 photos if it's client-visible work

## 🚗 Client visit / site job
- [ ] Confirm appointment + address + parking day before
- [ ] Kit checklist: multimeter, laptop w/ Mach3, tools, parts, camera
- [ ] Arrive on time; note machine condition + symptoms (photos)
- [ ] Written diagnosis + quote before starting repair (use [[PCB_Diagnosis_Checklist]])
- [ ] Log hours + revenue same evening

## 📝 Report / defense session
- [ ] Decide the chapter/section for this session
- [ ] Gather sources first (photos, datasheets, SOMIK docs) — 10 min
- [ ] Write freely 25 min (no editing while writing)
- [ ] Break 5 min
- [ ] Edit/format what was written
- [ ] Move finished section to "done" in [[Final_Report_Defense]]

## 🌙 Shutdown (10 min, end of day)
- [ ] Bench cleaned, tools returned, power off
- [ ] Log hours + revenue in Yield Tracker (target ≥ 1,000 DA/hr)
- [ ] Update [[ITS_Kanban|Kanban]]
- [ ] Fill daily note: yield, blocker, one-line summary
- [ ] Write tomorrow's 3 focus tasks

## 📅 Weekly review (Thursday evening or Friday morning)
- [ ] Count billable hours + revenue; compute avg yield
- [ ] Mark milestone gates met/missed ([[01_Milestones]])
- [ ] List slippage + root cause + fix
- [ ] Pull next week's bank: 2 High + 2 Medium + 2 Low
- [ ] Confirm client commitments + Friday recovery plan
- [ ] File the weekly note in `06_Weekly_Notes`

## 📆 Monthly review (last work day of the month)
- [ ] Re-read the month's weekly notes (5 min)
- [ ] Score the 4 projects: SOMIK / Workshop / Clients / Report
- [ ] Update progress % on each project note
- [ ] Adjust the milestone map if >2 days behind
- [ ] Plan next month's gates
