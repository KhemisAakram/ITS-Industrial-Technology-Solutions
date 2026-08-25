---
date: 2026-08-01
tags: [finance, dashboard, planning]
---

# Finance Dashboard — ITS

> Tracks income, expenses, and balance from daily notes. For the interactive tracker, open the [[documents/05_Financial/ITS_Finance_Tracker.html|HTML Finance Tracker]].

## Balance Summary

```dataviewjs
const pages = dv.pages('"Planning/05_Daily_Notes"')
  .where(p => p.income_da || p.expense_parts || p.expense_tools || p.expense_transport || p.expense_overhead);

const totalIncome = pages.reduce((s, p) => s + (parseInt(p.income_da) || 0), 0);
const totalParts = pages.reduce((s, p) => s + (parseInt(p.expense_parts) || 0), 0);
const totalTools = pages.reduce((s, p) => s + (parseInt(p.expense_tools) || 0), 0);
const totalTransport = pages.reduce((s, p) => s + (parseInt(p.expense_transport) || 0), 0);
const totalOverhead = pages.reduce((s, p) => s + (parseInt(p.expense_overhead) || 0), 0);
const totalExpenses = totalParts + totalTools + totalTransport + totalOverhead;
const netBalance = totalIncome - totalExpenses;
const daysTracked = pages.length;

dv.paragraph(`
| Metric | Value |
|--------|-------|
| Days tracked | ${daysTracked} / 137 |
| **Total Income** | **${totalIncome.toLocaleString()} DA** |
| Parts & components | ${totalParts.toLocaleString()} DA |
| Tools & equipment | ${totalTools.toLocaleString()} DA |
| Transport | ${totalTransport.toLocaleString()} DA |
| Overhead | ${totalOverhead.toLocaleString()} DA |
| **Total Expenses** | **${totalExpenses.toLocaleString()} DA** |
| **Net Balance** | **${netBalance.toLocaleString()} DA** |
`);
```

## Income by Day

```dataview
TABLE WITHOUT ID
  date AS "Date",
  income_da AS "Income (DA)"
FROM "Planning/05_Daily_Notes"
WHERE income_da AND income_da != "" AND int(income_da) > 0
SORT date DESC
LIMIT 14
```

## Expenses by Day

```dataview
TABLE WITHOUT ID
  date AS "Date",
  expense_parts AS "Parts",
  expense_tools AS "Tools",
  expense_transport AS "Transport",
  expense_overhead AS "Overhead"
FROM "Planning/05_Daily_Notes"
WHERE (expense_parts AND int(expense_parts) > 0) OR (expense_tools AND int(expense_tools) > 0) OR (expense_transport AND int(expense_transport) > 0) OR (expense_overhead AND int(expense_overhead) > 0)
SORT date DESC
LIMIT 14
```

## Days with Zero Income

```dataview
LIST WITHOUT ID
  date + " — Day " + day
FROM "Planning/05_Daily_Notes"
WHERE (!income_da OR income_da = "" OR income_da = "0") AND date < date(today) AND (hours_worked AND hours_worked != "")
SORT date DESC
LIMIT 10
```

## Monthly Breakdown

```dataviewjs
const pages = dv.pages('"Planning/05_Daily_Notes"')
  .where(p => p.date);

const months = {};
for (const p of pages) {
  if (!p.date) continue;
  const d = new Date(p.date);
  const key = d.toISOString().slice(0, 7); // YYYY-MM
  if (!months[key]) months[key] = { income: 0, parts: 0, tools: 0, transport: 0, overhead: 0 };
  months[key].income += parseInt(p.income_da) || 0;
  months[key].parts += parseInt(p.expense_parts) || 0;
  months[key].tools += parseInt(p.expense_tools) || 0;
  months[key].transport += parseInt(p.expense_transport) || 0;
  months[key].overhead += parseInt(p.expense_overhead) || 0;
}

const rows = Object.entries(months)
  .sort((a, b) => b[0].localeCompare(a[0]))
  .map(([m, v]) => {
    const exp = v.parts + v.tools + v.transport + v.overhead;
    return [m, v.income.toLocaleString() + ' DA', exp.toLocaleString() + ' DA', (v.income - exp).toLocaleString() + ' DA'];
  });

dv.table(['Month', 'Income', 'Expenses', 'Net'], rows);
```

## Recent Transactions

```dataview
TABLE WITHOUT ID
  date AS "Date",
  income_da AS "Income",
  expense_parts AS "Parts",
  expense_tools AS "Tools",
  expense_transport AS "Transport",
  expense_overhead AS "Overhead"
FROM "Planning/05_Daily_Notes"
WHERE income_da AND income_da != ""
SORT date DESC
LIMIT 7
```

## Links
- [[02_Task_Bank|Task Bank]] — pick tasks
- [[04_Projects/ITS_Kanban|Kanban]] — manage work
- [[documents/05_Financial/ITS_Finance_Tracker.html|HTML Finance Tracker]] — full interactive view
- [[13_Workshop_Dashboard|Workshop Dashboard]] — yield + hours
