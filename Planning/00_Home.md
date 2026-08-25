---
date: 2026-08-01
tags: [moc, planning]
---


# ITS — 4-Month Command Center

**Start:** Sat 1 Aug 2026 — **Deadline:** Tue 15 Dec 2026 (137 days / ~19.5 weeks)
**Work week:** Sat–Thu · **Friday = recovery, no exceptions**

> System: wake up → 3 questions → pick 3 tasks → work → log → sleep. Repeat.

## Setup (mostly done automatically)
- [x] Core plugins **Templates** + **Daily notes** enabled
- [x] Daily notes → `Planning/05_Daily_Notes`, template `07_Templates/daily_template.md` (config file written)
- [x] Templates folder → `Planning/07_Templates` (config file written)
- [x] Community plugins installed: **Periodic Notes, Dataview, Tasks, Kanban, Git, Templater, Calendar, Excalidraw, QuickAdd, NL Dates, PDF++, Iconize**
- [x] Templater triggers (daily + weekly) + Git auto-backup (20 min) configured (config files written)
- [x] First check: `Ctrl+P` → "Open today's daily note" → heading should read **Day X of 137 (Week W)** ✅ 2026-07-31
- [x] First weekly review: `Ctrl+P` → "Open weekly note" → check `06_Weekly_Notes` ✅ 2026-07-31

## Start here
- [[01_Milestones|Milestones — 19.5-week map]]
- [[02_Task_Bank|Task Bank — flow-matched by mental demand]]
- [[03_Scripted_Actions|Scripted Actions — checklists]]
- [[10_Courses|Courses — ranked watch list (SOMIK + VFD)]]
- **Projects:** [[ITS_Business]] · [[SOMIK_CNC_Conversion]] · [[Workshop_Setup]] · [[Client_Jobs]] · [[Flowaxs]] · [[CNC_Laser]] · [[Final_Report_Defense]]
- [[ITS_Kanban|Kanban board]]
- [[15_Daily_Prompts|Daily Prompts — copy & paste each day]]
- [[09_Plugin_Setup|Plugin setup — Git, Templater, QuickAdd, diagrams]]
- [[08_Diagrams|Diagrams — Excalidraw canvases (SOMIK wiring, workshop layout)]]
- **Today:** open the daily note → fill 3 tasks + estimate hours → work → log actual at end of day
- **Weekly review:** create a note in `06_Weekly_Notes` from the weekly template, every Thursday evening or Friday morning
- **Workshop tracking:** [[13_Workshop_Dashboard|Workshop Dashboard]] (Obsidian) · [[documents/07_Time_Management/Workshop_Dashboard.html|Interactive Dashboard]] · [[documents/07_Time_Management/ITS_Daily_Tracker.html|Daily Tracker]]
- **Finance:** [[14_Finance_Dashboard|Finance Dashboard]] (Obsidian) · [[documents/05_Financial/ITS_Finance_Tracker.html|Interactive Finance Tracker]] · [[documents/05_Financial/ITS_Finance_Tracker.csv|CSV Export]]

## Vault notes already in this repo (linkable)
- [[PCB_Diagnosis_Checklist]] — Services/PCB Service/03_Operations
- [[First_Job_Record]] — PCB-001 (3,000 DA, paid)
- [[FB Digital Strategy]] / [[WhatsApp_Scripts]] — PCB outreach (only if you restart client work)

## Projects
```dataview
TABLE status AS Status, progress AS "%", due AS Due
FROM #project
SORT due ASC
```

## Open tasks before deadline
```tasks
not done
due before 2026-12-16
sort by due
group by due
```

## Rules (the system in 3 lines)
1. Morning: 3 questions → energy, biggest task, blockers → fill daily note (2 min).
2. Work from the [[02_Task_Bank|Task Bank]], estimate hours before starting.
3. End of day: log actual hours + revenue + expenses → check [[14_Finance_Dashboard|balance]].
