---
date: 2026-08-01
tags: [setup, plugins, planning]
---

# Plugin Setup & Quick Reference

> `.obsidian/` is gitignored → plugin settings stay on **your machine only**. Vault notes (this one included) are committed to GitHub.

## 1. Git (obsidian-git) — auto backup to GitHub
Settings → Git (obsidian-git):
- **Auto backup after interval of operations** → on, minutes: `20`
- **Auto backup after failed note commit** → on
- **Push on backup** → **on**
- **Pull on startup** → on
- **Commit message on auto backup**: `vault: daily backup`
- Leave "Username/Password" empty — uses your existing GitHub login (same one CLI git uses).

What it does: every 20 min while Obsidian is open, it commits + pushes your vault. Daily notes are never lost. `.obsidian/` never gets committed.

## 2. Templater — auto-fills day/week numbers
Settings → Templater:
- **Template folder location**: `07_Templates`
- **Trigger Templater on new file creation** → Add:
  - Template: `07_Templates/daily_template.md` · Folder: `05_Daily_Notes` · File pattern: `2026-*.md`
  - Template: `07_Templates/weekly_template.md` · Folder: `06_Weekly_Notes` · File pattern: `W*.md`

Test: `Ctrl+P` → "Open today's daily note" → the heading should read **Day X of 137 (Week W#)**. If you see raw `<% %>` text instead → the trigger didn't run: re-check the two triggers above, or use the **backup method** below.

**Backup method (100% reliable):** `Ctrl+P` → **"Templater: Create new note from template"** → pick `daily_template.md` → save the new note as `Planning/05_Daily_Notes/YYYY-MM-DD.md` with the correct date. Use this any time the auto-trigger doesn't fire.

## 3. Calendar — see/open days
Community **Calendar** plugin: no config needed — it reads your daily-notes folder (`05_Daily_Notes`). Click a date to open/create that day.

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

## Daily flow with all plugins
1. `Ctrl+P` → "Open today's daily note" (Templater fills Day/Week automatically)
2. Run QuickAdd "Add task to today" from the workshop bench, even mid-task
3. Type task dates with plain words (NL Dates)
4. Evening: shutdown checklist → obsidian-git pushes everything automatically
5. Friday: weekly review in `06_Weekly_Notes` (Periodic Notes → "Open weekly note")
