# Daily Prompts

Copy-paste these prompts to me. Fill in the blanks, I do the rest.

---

## Morning Prompt (every work day)

```
Good morning. Today is [DATE].

My tasks today:
1. [TASK 1] — [TIME START]-[TIME END] — [PROJECT] — est [X]h
2. [TASK 2] — [TIME START]-[TIME END] — [PROJECT] — est [X]h
3. [TASK 3] — [TIME START]-[TIME END] — [PROJECT] — est [X]h

My energy is: fresh / medium / tired

Fill my daily note.
```

**Example:**
```
Good morning. Today is 2026-08-26.

My tasks today:
1. PCB Repair 2 — 06:00-09:00 — Client_Jobs — est 3h
2. PCB Repair 3 — 09:00-12:00 — Client_Jobs — est 3h
3. Build Prototype — 13:00-16:00 — own project — est 3h

My energy is: fresh

Fill my daily note.
```

---

## Evening Prompt (every work day)

```
Good evening. Day done.

What I finished:
1. [TASK] — actual [X]h — revenue [X] DA
2. [TASK] — actual [X]h — revenue [X] DA

What I didn't finish:
- [TASK] → move to tomorrow

Client work today? → invoice sent: yes / no
Photos snapped? → yes / no

Expenses today:
- Parts: [X] DA — [what]
- Tools: [X] DA — [what]
- Transport: [X] DA — [what]
- Overhead: [X] DA — [what]

Tool cleanup done? → yes / no

Close my day.
```

**Example:**
```
Good evening. Day done.

What I finished:
1. PCB Repair 2 — actual 4h — revenue 3000 DA
2. PCB Repair 3 — actual 3h — revenue 2000 DA

What I didn't finish:
- Build Prototype → move to tomorrow

Client work today? → invoice sent: yes
Photos snapped? → yes

Expenses today:
- Parts: 500 DA — resistors + capacitors
- Transport: 200 DA — bus to client

Tool cleanup done? → yes

Tomorrow's tasks:
1. PCB Repair 3 — 06:00-09:00 — Client_Jobs — est 3h
2. Build Prototype — 09:00-12:00 — own project — est 3h
3. SOMIK teardown — 13:00-16:00 — SOMIK — est 3h

Close my day.
```

I update: daily note + `05_Financial/ITS_Finance_Tracker.csv` + `14_Finance_Dashboard.md` + re-export tracker data.

---

## Weekly Prompt (Thursday evening or Friday morning)

```
Good evening. Weekly review. Week: [W__]

What went well:
- [what]

What slipped:
- [what] → fix: [how]

Next week's priorities:
1. [TASK]
2. [TASK]
3. [TASK]

Fill my weekly note.
```

I auto-fill: hours, revenue, avg yield, invoice status from your daily notes.

**Example:**
```
Good evening. Weekly review. Week: W04

What went well:
- PCB repairs finished fast
- Good client follow-up

What slipped:
- Mach3 bench test → need parts ordered first

Next week's priorities:
1. Mach3 bench test
2. SOMIK teardown
3. Report outline

Fill my weekly note.
```

---

## Monthly Prompt (last work day of month)

```
Good evening. Monthly review. Month: [MONTH]

Behind on anything? → [what]
Next month's focus: [what]

Update my project notes.
```

I auto-fill: project scores, P&L, milestone status from your notes and finance tracker.

**Example:**
```
Good evening. Monthly review. Month: August 2026

Behind on anything? → no
Next month's focus: SOMIK assembly + report Ch 1

Update my project notes.
```

---

## Maintenance Reminders

Standing reminders — I'll mention these automatically.

### Weekly (Thursday)
- [ ] Soldering tip tinning

### Monthly (last work day)
- [ ] 3D printer bed cleaning + belt check

### Annually (December)
- [ ] Oscilloscope calibration

---

## What happens automatically

| When | I do |
|------|------|
| Morning | Update daily note: tasks, schedule, energy, Kanban |
| Evening | Update daily note: actual hours, revenue, yield, Money section, expenses, move unfinished tasks. Update `05_Financial/ITS_Finance_Tracker.csv` + `14_Finance_Dashboard.md`. Re-export obsidian_data.js for HTML tracker. |
| Thursday | Auto-fill weekly note: hours, revenue, yield, invoices from daily notes |
| Month-end | Auto-fill project scores, P&L, milestone status from notes + finance tracker |

---

## Quick rules

- **3 tasks max** per day
- **Clients are fixed tasks** — not checked for urgency
- **PCB course** — 30 min first thing, not in the 3-task table
- **Friday** — no work, recovery day only
- **Every evening** — invoice if client work, tool cleanup, snap photos
