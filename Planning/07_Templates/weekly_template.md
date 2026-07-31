---
date: {{date}}
week:
week_range:
tags:
  - weekly
---

<%*
const start = new Date("2026-08-01T00:00:00").getTime();
const now = new Date();
const day = Math.floor((now.getTime() - start) / 86400000) + 1;
const week = Math.ceil(day / 7);
const fmt = (d) => d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
const dow = now.getDay();
const diffToSat = (6 - dow + 7) % 7;
const sat = new Date(now.getTime() - diffToSat * 86400000);
const weekEnd = new Date(sat.getTime() + 5 * 86400000);
tp.frontmatter.week = week;
tp.frontmatter.week_range = fmt(sat) + " .. " + fmt(weekEnd);
%>

# Week <%+ tp.frontmatter.week %> — <%+ tp.frontmatter.week_range %>

> [[01_Milestones|Milestones]] · [[02_Task_Bank|Task Bank]] · [[03_Scripted_Actions|Weekly review script]]

## Won this week
- 

## Numbers
- Billable hours total:
- Revenue total (DA):
- Avg yield (DA/hr):
- Projects moved: SOMIK / Workshop / Clients / Report

## Slippage & fixes
- What fell behind:
- Why:
- Next-week fix:

## Next week's bank (pull from [[02_Task_Bank]])
- [ ] High:
- [ ] High:
- [ ] Medium:
- [ ] Low:
- [ ] Client commitments:

## Recovery check
- Rest days taken: /1
- Sleep ok? · Energy ok?
- Planned Friday:
