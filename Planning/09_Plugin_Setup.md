---
date: 2026-08-01
tags: [setup, plugins, planning]
---

# Plugin Setup & Quick Reference

> `.obsidian/` is gitignored → plugin settings stay on **your machine only**. Vault notes (this one included) are committed to GitHub.

## 0. The big one: all daily/weekly notes are pre-generated
All **137 daily notes** (`05_Daily_Notes/YYYY-MM-DD.md`) and **20 weekly notes** (`06_Weekly_Notes/W01..W20.md`) already exist on disk with the correct **Day X of 137** and **Week W** filled in, mapped back from the deadline **Tue 15 Dec 2026**.

- You never need Templater to create a daily note.
- Just open the Calendar (or `Ctrl+P` → "Open today's daily note") and start filling it in.
- Templates in `07_Templates` are a **fallback only** (used if a note is ever missing).

## 1. Git (obsidian-git) — auto backup to GitHub
Config already written to `.obsidian/plugins/obsidian-git/data.json` (verify in Settings → Git if needed):
- `autoSaveInterval: 20` → auto **commit + push** every 20 min while Obsidian is open
- `autoPullOnBoot: true` → pull once on startup
- `pullBeforePush: true`, `disablePush: false`
- `autoCommitMessage`: `vault: daily backup`

What it does: every 20 min your vault commits + pushes to GitHub. Daily notes are never lost. `.obsidian/` never gets committed.

## 2. Templater — NOT needed anymore (kept installed as fallback)
All notes are pre-generated, so the auto-trigger does not matter. If you ever need a fresh note from a template: `Ctrl+P` → **"Templater: Create new note from template"** → pick the template → save with the correct name. Templates are core-safe (no raw `<% %>`).

## 3. Calendar — see/open days
Community **Calendar** plugin: no config needed — it reads your daily-notes folder (`05_Daily_Notes`). Click a date to open that day.

## 4. QuickAdd — one-click captures
Settings → QuickAdd → Manage choices → Add:
- **"Add task to today"** → type `Capture`
  - File name: `05_Daily_Notes/{{DATE:YYYY-MM-DD}}`
  - Format: `- [ ] {{VALUE}}`
  - Enable **Create or open file** · Append to end
- **"Log job"** → type `Capture`
  - File name: `05_Daily_Notes/{{DATE:YYYY-MM-DD}}`
  - Format: `- Job: {{VALUE}}`
  - Enable **Create or open file** · Append to end

Then: Settings → Hotkeys → set a hotkey (e.g. `Ctrl+Shift+T`) for "QuickAdd: Add task to today".

## 5. Natural Language Dates (with Tasks)
Just type dates in plain words in task lines, e.g.:
- `- [ ] SOMIK wiring plan 📅 tomorrow`
- `- [ ] Report Ch 2 📅 next Friday`
- `- [ ] Buy BOB driver 📅 in 3 days`

## 6. Excalidraw — diagrams
Settings → Excalidraw → **Excalidraw file/folder location**: `08_Diagrams`
Draw there (SOMIK wiring plan, workshop layout). Link a canvas into a note with `![[SOMIK_wiring_plan.excalidraw]]`. Recommended at most **1 canvas per project** so notes stay readable.

## 7. PDF++ — annotate reference PDFs
Open any PDF in the vault (e.g. `documents/00_reference/FLOWAXS.pdf`) → highlight/underline/comment. Copy an annotation link into a note to jump back to that page.

## 8. Iconize — cosmetics only
Right-click a folder → Iconize → pick an icon. Zero effect on notes.

## Daily flow
1. Open today's daily note — Day/Week already filled in (`Ctrl+P` → "Open today's daily note", or Calendar)
2. Run QuickAdd "Add task to today" from the workshop bench, even mid-task
3. Type task dates with plain words (NL Dates)
4. Evening: shutdown checklist → obsidian-git pushes everything automatically
5. Friday: weekly review in `06_Weekly_Notes`
