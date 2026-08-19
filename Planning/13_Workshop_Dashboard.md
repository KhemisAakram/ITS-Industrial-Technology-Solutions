---
date: 2026-08-01
tags: [dashboard, workshop, planning]
---

# Workshop Dashboard — Obsidian View

> This note pulls data from daily notes frontmatter. For the full interactive dashboard, open the [[documents/07_Time_Management/Workshop_Dashboard.html|HTML Dashboard]].

## Weekly Yield Summary

```dataview
TABLE WITHOUT ID
  date AS "Date",
  energy AS "Energy",
  hours_worked AS "Hours",
  hours_billable AS "Billable",
  revenue_da AS "Revenue (DA)",
  yield_da_hr AS "Yield (DA/hr)"
FROM "Planning/05_Daily_Notes"
WHERE hours_worked AND hours_worked != ""
SORT date DESC
LIMIT 14
```

## Billable Hours This Week

```dataview
LIST WITHOUT ID
  "Day " + day + ": " + hours_billable + "h billable, " + revenue_da + " DA"
FROM "Planning/05_Daily_Notes"
WHERE hours_billable AND hours_billable != "" AND hours_billable != "0"
SORT date DESC
LIMIT 7
```

## Days Below Yield Target

```dataview
TABLE WITHOUT ID
  date AS "Date",
  yield_da_hr AS "Yield",
  hours_worked AS "Hours",
  hours_billable AS "Billable"
FROM "Planning/05_Daily_Notes"
WHERE yield_da_hr AND yield_da_hr != "" AND int(yield_da_hr) < 1000 AND int(yield_da_hr) > 0
SORT date DESC
```

## Empty Days (No Data Logged)

```dataview
LIST WITHOUT ID
  date + " — Day " + day
FROM "Planning/05_Daily_Notes"
WHERE (!hours_worked OR hours_worked = "") AND date < date(today)
SORT date DESC
LIMIT 10
```

## Energy Distribution

```dataview
TABLE WITHOUT ID
  energy AS "Energy",
  length(rows) AS "Count"
FROM "Planning/05_Daily_Notes"
WHERE energy AND energy != ""
GROUP BY energy
```

## Project: Workshop Setup Status

```dataview
TABLE status AS "Status", progress AS "Progress", due AS "Due"
FROM "Planning/04_Projects/Workshop_Setup.md"
```

## Quick Stats

```dataviewjs
const pages = dv.pages('"Planning/05_Daily_Notes"')
  .where(p => p.hours_worked && p.hours_worked !== "");

const totalHours = pages.reduce((s, p) => s + (parseFloat(p.hours_worked) || 0), 0);
const totalBillable = pages.reduce((s, p) => s + (parseFloat(p.hours_billable) || 0), 0);
const totalRevenue = pages.reduce((s, p) => s + (parseInt(p.revenue_da) || 0), 0);
const daysLogged = pages.length;
const avgYield = totalBillable > 0 ? Math.round(totalRevenue / totalBillable) : 0;
const billableRatio = totalHours > 0 ? Math.round(totalBillable / totalHours * 100) : 0;

dv.paragraph(`
| Metric | Value |
|--------|-------|
| Days logged | ${daysLogged} / 137 (${Math.round(daysLogged/137*100)}%) |
| Total hours | ${totalHours.toFixed(1)} |
| Total billable | ${totalBillable.toFixed(1)} |
| Billable ratio | ${billableRatio}% |
| Total revenue | ${totalRevenue.toLocaleString()} DA |
| Avg yield | ${avgYield} DA/hr |
| Target | 1,000 DA/hr |
`);
```

## Links
- [[02_Task_Bank|Task Bank]] — pick tasks from here
- [[03_Scripted_Actions|Scripted Actions]] — run the scripts
- [[01_Milestones|Milestones]] — check gates
- [[documents/07_Time_Management/ITS_Daily_Tracker.html|HTML Daily Tracker]] — fill daily
- [[documents/07_Time_Management/Workshop_Dashboard.html|HTML Dashboard]] — full interactive view
