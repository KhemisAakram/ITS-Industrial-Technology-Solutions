---
date: 2026-08-01
tags: [moc, planning]
---

# ITS — 4-Month Command Center

**Start:** Sat 1 Aug 2026 — **Deadline:** Tue 15 Dec 2026 (137 days / ~19.5 weeks)
**Work week:** Sat–Thu · **Friday = recovery, no exceptions**

> System: flow-match tasks → run scripted actions → work the weekly bank → log everything → rest on schedule.

## Setup (2 min, once)
- [ ] Enable core plugin **Templates**
- [ ] Enable core plugin **Daily notes**
  - Date format: `YYYY-MM-DD` · New file location: `05_Daily_Notes` · Template: `07_Templates/daily_template.md`
- [ ] Install community plugins (all optional — notes work fine without them):
  - [ ] **Periodic Notes** (weekly notes) → weekly template: `07_Templates/weekly_template.md`
  - [ ] **Dataview** (dashboard queries below)
  - [ ] **Tasks** (open-task query below)
  - [ ] **Kanban** (opens [[ITS_Kanban]] as a board)

## Start here
- [[01_Milestones|Milestones — 19.5-week map]]
- [[02_Task_Bank|Task Bank — flow-matched by mental demand]]
- [[03_Scripted_Actions|Scripted Actions — checklists]]
- **Projects:** [[SOMIK_CNC_Conversion]] · [[Workshop_Setup]] · [[Client_Jobs]] · [[Final_Report_Defense]]
- [[ITS_Kanban|Kanban board]]
- **Today:** open the daily note (Daily notes plugin) → created in `05_Daily_Notes`
- **Weekly review:** create a note in `06_Weekly_Notes` from the weekly template, every Thursday evening or Friday morning

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

## Rules (the system in one line)
1. Work from the [[02_Task_Bank|Task Bank]], not from memory.
2. Match task demand to your energy — morning = high demand, evening = low demand.
3. Run the [[03_Scripted_Actions|script]], don't think about what's next.
4. Log hours + revenue every day — yield target **≥ 1,000 DA/hr**.
5. Friday is recovery. Yield drops are a signal to rest, not to grind.
