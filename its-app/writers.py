"""Safe writers — write edits straight back into the vault files.

Every write first copies the target to `path.bak` so a bad edit never loses data.
"""
from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime
from pathlib import Path

import openpyxl

from readers import (BASE, CLIENT_COLS, CLIENTS_CSV, DAILY_DIR, FINANCE_CSV,
                     FINANCE_HEADER, INVOICES_DIR, JOB_TRACKER_XLSX, LEAD_COLS,
                     LEADS_CSV, PROJECTS_DIR)

_FRONT_RE = re.compile(r"^---\s*$")


class BackupError(Exception):
    pass


def backup(path: Path) -> None:
    """Copy `path` to `path + .bak` before any modification."""
    if not path.exists():
        return
    bak = path.with_name(path.name + ".bak")
    shutil.copy2(path, bak)


def _write_text_utf8(path: Path, content: str) -> None:
    backup(path)
    path.write_text(content, encoding="utf-8")


def _rel(p: Path) -> str:
    return str(p.relative_to(BASE))


# --------------------------------------------------------------------------- finance
def write_finance(rows) -> None:
    """Rewrite ITS_Finance_Tracker.csv from a list of dicts (index ignored)."""
    ordered = sorted(rows, key=lambda r: (r["date"], r["description"]))
    lines = [",".join(FINANCE_HEADER)]
    for r in ordered:
        def esc(s):
            s = str(s)
            if "," in s or '"' in s or "\n" in s:
                return '"' + s.replace('"', '""') + '"'
            return s
        lines.append(",".join([
            esc(r["date"]), esc(r["type"]), esc(r["category"]),
            esc(r["description"]), esc(r["amount"]),
        ]))
    _write_text_utf8(FINANCE_CSV, "\n".join(lines) + "\n")


def add_finance(entry) -> int:
    rows = _read_finance_rows()
    row = {
        "date": entry.get("date", ""),
        "type": entry.get("type", "income"),
        "category": entry.get("category", ""),
        "description": entry.get("description", ""),
        "amount": entry.get("amount", 0),
    }
    rows.append(row)
    write_finance(rows)
    return len(rows) - 1


def _read_finance_rows():
    import readers
    return [dict(r) for r in readers.finance()]


def update_finance(index, entry) -> None:
    import readers
    rows = [dict(r) for r in readers.finance()]
    if not (0 <= index < len(rows)):
        return
    for k, v in entry.items():
        rows[index][k] = v
    write_finance(rows)


def delete_finance(index) -> None:
    import readers
    rows = [dict(r) for r in readers.finance()]
    if 0 <= index < len(rows):
        rows.pop(index)
        write_finance(rows)


# --------------------------------------------------------------------------- frontmatter (daily notes / projects)
def _replace_frontmatter(path: Path, fields: dict) -> None:
    """Surgically replace or add YAML frontmatter keys, preserving the rest of the file."""
    lines = path.read_text(encoding="utf-8").split("\n")
    markers = [i for i, ln in enumerate(lines) if _FRONT_RE.match(ln)]
    if len(markers) < 2:
        raise ValueError(f"No frontmatter in {path}")
    start, end = markers[0], markers[1]

    key_re = {k: re.compile(r"^" + re.escape(k) + r"(\s*:\s*)(.*)$") for k in fields}
    seen = set()
    out = lines[: start + 1]
    inserted = []
    for ln in lines[start + 1: end]:
        matched = False
        for k, rx in key_re.items():
            m = rx.match(ln)
            if m and k not in seen:
                out.append(f"{k}: {str(fields[k]).strip()}")
                seen.add(k)
                matched = True
                break
        if not matched:
            out.append(ln)
    missing = [k for k in fields if k not in seen]
    if missing:
        for k in missing:
            inserted.append(f"{k}: {fields[k]}")
        if inserted:
            out = out[: start + 1] + inserted + out[start + 1:]
    out.append(lines[end])
    for ln in lines[end + 1:]:
        out.append(ln)
    _write_text_utf8(path, "\n".join(out))


def update_daily_note(date: str, fields: dict) -> None:
    path = DAILY_DIR / f"{date}.md"
    if not path.exists():
        raise FileNotFoundError(f"Daily note not found: {path}")
    _replace_frontmatter(path, fields)


DAILY_TAG = "[daily "


def _is_daily_tagged(row) -> bool:
    return str(row.get("description", "")).startswith(DAILY_TAG)


def sync_daily_to_finance(date: str):
    """Reconcile the finance CSV to the daily note totals for `date`.

    Never edits manual rows and never double-counts: it only adds a tagged
    '[daily <date>] <category>' row when the note amount is greater than what
    is already logged for the same (type, category) on that date. Returns the
    list of created entries.
    """
    import readers
    note = readers.daily_note(date)
    if not note:
        return []
    target = {
        ("income", "General"): note["income_da"],
        ("expense", "parts"): note["expense_parts"],
        ("expense", "tools"): note["expense_tools"],
        ("expense", "transport"): note["expense_transport"],
        ("expense", "overhead"): note["expense_overhead"],
    }

    rows = [dict(r) for r in readers.finance()]
    day_rows = [r for r in rows if r["date"] == date]
    rows = [r for r in rows if not (_is_daily_tagged(r) and r["date"] == date)]

    manual = {}
    for r in day_rows:
        if _is_daily_tagged(r):
            continue
        key = (r["type"], r["category"] or "General")
        manual[key] = manual.get(key, 0) + r.get("amount", 0)

    created = []
    for (typ, cat), amt in target.items():
        if amt <= 0:
            continue
        existing = manual.get((typ, cat), 0)
        delta = amt - existing
        if delta > 0:
            row = {"date": date, "type": typ, "category": cat,
                   "description": f"{DAILY_TAG}{date}] {cat}", "amount": delta}
            rows.append(row)
            created.append(row)

    if created:
        write_finance(rows)
    return created


# --------------------------------------------------------------------------- projects
def update_project(project_id: str, fields: dict) -> None:
    path = PROJECTS_DIR / f"{project_id}.md"
    if not path.exists():
        raise FileNotFoundError(f"Project not found: {path}")
    _replace_frontmatter(path, fields)


# --------------------------------------------------------------------------- jobs (XLSX)
JOBS_COLS = ["Date In", "WO #", "Customer Name", "Company", "Phone", "Board Model",
             "Equipment", "Symptoms", "Diagnosis", "Quote (DA)", "Accepted?",
             "Date Out", "Paid (DA)", "Status", "Notes"]


def _load_job_workbook():
    wb = openpyxl.load_workbook(JOB_TRACKER_XLSX)  # keep formulas/styles
    return wb


def write_jobs(job_rows) -> None:
    backup(JOB_TRACKER_XLSX)
    wb = _load_job_workbook()
    if "Job Tracker" not in wb.sheetnames:
        raise ValueError("Job Tracker sheet missing")
    ws = wb["Job Tracker"]
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)
    for row in job_rows:
        ws.append([
            row.get("date_in", ""), row.get("wo", ""), row.get("customer", ""),
            row.get("company", ""), row.get("phone", ""), row.get("board", ""),
            row.get("equipment", ""), row.get("symptoms", ""), row.get("diagnosis", ""),
            row.get("quote", 0), row.get("accepted", ""), row.get("date_out", ""),
            row.get("paid", 0), row.get("status", "Received"), row.get("notes", ""),
        ])
    wb.save(JOB_TRACKER_XLSX)


# --------------------------------------------------------------------------- clients / leads (CSV)
def write_clients(rows) -> None:
    _write_csv(CLIENTS_CSV, CLIENT_COLS, rows)


def write_leads(rows) -> None:
    _write_csv(LEADS_CSV, LEAD_COLS, rows)


def _write_csv(path: Path, cols: list, rows) -> None:
    lines = [",".join(cols)]
    for r in rows:
        cells = []
        for c in cols:
            v = str(r.get(c, "") or "")
            if "," in v or '"' in v or "\n" in v:
                v = '"' + v.replace('"', '""') + '"'
            cells.append(v)
        lines.append(",".join(cells))
    _write_text_utf8(path, "\n".join(lines) + "\n")


# --------------------------------------------------------------------------- invoices
def create_invoice(number: str, client: str, date: str, amount, line_items=None) -> Path:
    INVOICES_DIR.mkdir(parents=True, exist_ok=True)
    path = INVOICES_DIR / f"{number}.md"
    if path.exists():
        raise FileExistsError(f"Invoice {number} already exists")
    today = date or datetime.now().strftime("%Y-%m-%d")
    content = (
        f"# ITS — Invoice\n\n"
        f"**Invoice #:** {number}\n"
        f"**Date:** {today}\n"
        f"**Due:** On receipt\n\n"
        f"---\n\n## Bill To\n\n"
        f"**Client:** {client}\n\n"
        f"---\n\n## Line Items\n\n"
        f"| # | Description | Qty | Unit | Rate (DA) | Amount (DA) |\n"
        f"|---|-------------|-----|------|-----------|-------------|\n"
    )
    if line_items:
        for i, it in enumerate(line_items, start=1):
            content += (f"| {i} | {it.get('description', '')} | {it.get('qty', 1)} | "
                        f"{it.get('unit', 'pcs')} | {it.get('rate', 0)} | {it.get('amount', 0)} |\n")
    content += (
        f"\n---\n\n## Summary\n\n"
        f"| | Amount (DA) |\n|---|-------------|\n"
        f"| **Total** | **{int(amount):,}** |\n\n"
        f"---\n\n## Notes\n\n"
        f"- All prices in DA (Algerian Dinar)\n\n"
        f"---\n\n**ITS — Industrial Technology Solutions**\n"
        f"El Harrouch, Skikda\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def toggle_invoice_paid(number: str) -> None:
    path = INVOICES_DIR / f"{number}.md"
    if not path.exists():
        raise FileNotFoundError(f"Invoice {number} not found")
    text = path.read_text(encoding="utf-8")
    backup(path)
    if re.search(r"(?mi)^\*\*Status:\*\*\s*Paid", text):
        text = re.sub(r"(?mi)^\*\*Status:\*\*\s*Paid.*$\n", "", text)
    else:
        date = datetime.now().strftime("%Y-%m-%d")
        text = re.sub(r"(?m)^(\*\*Client:\*\*.*)$", r"\1\n**Status:** Paid (" + date + ")", text, count=1)
    path.write_text(text, encoding="utf-8")


def delete_invoice(number: str) -> None:
    path = INVOICES_DIR / f"{number}.md"
    if path.exists():
        backup(path)
        path.unlink()


# --------------------------------------------------------------------------- next number helper
def next_invoice_number() -> str:
    from readers import invoices
    year = datetime.now().year
    prefix = f"ITS-{year}-"
    existing = [inv["number"] for inv in invoices() if inv["number"].startswith(prefix)]
    m = 0
    for num in existing:
        try:
            m = max(m, int(num.rsplit("-", 1)[1]))
        except (ValueError, IndexError):
            continue
    return f"{prefix}{m + 1:03d}"