"""ITS Command Center — local web app over the ITS Profile vault.

The vault folder IS the database: every page reads the real files live and
every edit writes straight back into them (with a .bak safety copy).
"""
from __future__ import annotations

import calendar as _cal
import io
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import zipfile

from flask import Flask, abort, flash, redirect, render_template, request, send_file, session, url_for

import readers
import writers

app = Flask(__name__)
app.secret_key = "its-command-center-local"


def fmt_da(v: float) -> str:
    return f"{int(round(v or 0)):,}".replace(",", " ")


app.jinja_env.filters["da"] = fmt_da


@app.context_processor
def inject_vault():
    return {"vault": str(readers.BASE), "now": datetime.now().strftime("%Y-%m-%d"),
            "locked": bool(_lock_password())}


# --------------------------------------------------------------------------- lock screen
def _lock_password() -> str:
    """Password for the opt-in lock screen: env ITS_APP_PASSWORD or its-app/.password file."""
    env = os.environ.get("ITS_APP_PASSWORD")
    if env:
        return env
    pfile = Path(__file__).resolve().with_name(".password")
    if pfile.exists():
        pw = pfile.read_text(encoding="utf-8").strip()
        if pw:
            return pw
    return ""


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        if request.form.get("password") == _lock_password():
            session["unlocked"] = True
            return redirect(request.args.get("next") or url_for("dashboard"))
        flash("Wrong password", "err")
    return render_template("login.html")


@app.get("/logout")
def logout():
    session.pop("unlocked", None)
    flash("Locked", "ok")
    return redirect(url_for("login_page"))


@app.before_request
def _lock_gate():
    if request.endpoint == "static" or not _lock_password():
        return None
    if session.get("unlocked"):
        return None
    if request.endpoint == "login_page":
        return None
    return redirect(url_for("login_page", next=request.path))


# --------------------------------------------------------------------------- forms
def form_str(name: str, default=""):
    v = request.form.get(name, "").strip()
    return v if v else default


def form_num(name: str, default=0):
    v = request.form.get(name, "").strip().replace(",", "").replace("DA", "").replace(" ", "")
    try:
        return float(v) if v else float(default)
    except ValueError:
        return float(default)


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _this_month() -> str:
    return datetime.now().strftime("%Y-%m")


def _sparkline(series, w=560, h=70):
    """Build an SVG polyline of cumulative profit."""
    if len(series) < 2:
        return ""
    vals = [s["cum"] for s in series]
    mn, mx = min(vals), max(vals)
    rng = (mx - mn) or 1
    pts = []
    for i, v in enumerate(vals):
        x = i * (w - 10) / (len(vals) - 1) + 5
        y = h - 6 - (v - mn) / rng * (h - 12)
        pts.append(f"{x:.1f},{y:.1f}".rstrip() if v != v else "5,0")
    poly = " ".join(pts)
    color = "--good" if vals[-1] >= 0 else "--bad"
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
            f'<line x1="0" y1="{h/2:.0f}" x2="{w}" y2="{h/2:.0f}" class="spark-line"/>'
            f'<polyline class="spark-sm" points="{poly}"/>'
            f'<polyline class="spark" style="stroke: var({color})" points="{poly}"/></svg>')


@app.route("/")
def dashboard():
    tx = readers.finance()
    income = sum(t["amount"] for t in tx if t["type"] == "income")
    expense = sum(t["amount"] for t in tx if t["type"] == "expense")
    profit = income - expense

    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for t in tx:
        ym = t["date"][:7]
        by_month[ym][t["type"]] += t["amount"]
    months = sorted(by_month, reverse=True)[:8]
    monthly = [{"month": m, "income": by_month[m]["income"], "expense": by_month[m]["expense"]}
               for m in months]
    max_month = max([by_month[m]["income"] for m in months] + [by_month[m]["expense"] for m in months]
                    + [1])

    cum = 0.0
    profit_series = []
    for m in sorted(by_month):
        cum += by_month[m]["income"] - by_month[m]["expense"]
        profit_series.append({"month": m, "cum": cum})

    cat_income = defaultdict(float)
    cat_expense = defaultdict(float)
    for t in tx:
        (cat_income if t["type"] == "income" else cat_expense)[t["category"]] += t["amount"]
    income_cats = sorted(cat_income, key=lambda k: cat_income[k], reverse=True)
    expense_cats = sorted(cat_expense, key=lambda k: cat_expense[k], reverse=True)

    invoices = readers.invoices()
    receivables = sum(i["amount"] for i in invoices if not i["paid"] and i["amount"] > 0)

    notes = readers.daily_notes()
    worked = sum(n["hours_worked"] for n in notes)
    billable = sum(n["hours_billable"] for n in notes)
    notes_income = sum(n["income_da"] for n in notes)
    yield_per_hr = (notes_income / billable) if billable else 0
    energy = defaultdict(int)
    for n in notes:
        if n["energy"]:
            energy[n["energy"]] += 1

    jobs = readers.jobs()
    open_jobs = [j for j in jobs if j["status"] and j["status"].lower() not in readers.JOB_TERMINAL]
    job_income = sum(j["paid"] for j in jobs)
    lead_rows = readers.leads()
    leads_by_status = defaultdict(int)
    for l in lead_rows:
        leads_by_status[l["status"] or "New"] += 1

    projects = readers.projects()
    active_projects = [p for p in projects if p["status"] in ("in-progress", "active", "ongoing", "planned")]
    week_no = datetime.now().isocalendar()[1]

    attention = _attention_items(projects, lead_rows, jobs, invoices)

    backups = []
    try:
        for zp in sorted(writers.BACKUP_DIR.glob("ITS_Backup_*.zip"), reverse=True)[:4]:
            backups.append({"name": zp.name, "size_mb": round(zp.stat().st_size / 1024 / 1024, 1)})
    except OSError:
        pass

    return render_template("dashboard.html",
                           income=income, expense=expense, profit=profit,
                           n_tx=len(tx), monthly=monthly, max_month=max_month,
                           profit_series=profit_series,
                           income_cats=income_cats, cat_income=cat_income,
                           max_cat_income=max(cat_income.values()) if cat_income else 1,
                           expense_cats=expense_cats, cat_expense=cat_expense,
                           max_cat_expense=max(cat_expense.values()) if cat_expense else 1,
                           sparkline=_sparkline(profit_series),
                           receivables=receivables, n_unpaid=sum(1 for i in invoices if not i["paid"]),
                           worked=worked, billable=billable, notes_income=notes_income,
                           yield_per_hr=yield_per_hr, energy=energy, n_notes=len(notes),
                           open_jobs=open_jobs, job_income=job_income,
                           leads_by_status=leads_by_status, n_leads=len(lead_rows),
                           active_projects=active_projects, week_no=week_no,
                           attention=attention, backups=backups)


def _attention_items(projects, lead_rows, jobs, invoices):
    """Things needing the owner's attention right now."""
    out = []
    today = datetime.now().date()
    for inv in invoices:
        if not inv["paid"] and inv["amount"] > 0:
            due = ""
            try:
                age = (today - datetime.strptime(inv["date"][:10], "%Y-%m-%d").date()).days
                due = f" · {age}d outstanding"
            except Exception:
                due = ""
            out.append({"type": "invoice", "label": f"Invoice {inv['number']} unpaid",
                        "detail": f"{inv['client'] or '—'} · {fmt_da(inv['amount'])} DA{due}"})
    for p in projects:
        if p["status"] in ("done", "completed", "delivered", "cancelled", "archived"):
            continue
        if p["due"]:
            try:
                if datetime.strptime(p["due"][:10], "%Y-%m-%d").date() < today:
                    out.append({"type": "project", "label": f"Project past due: {p['title']}",
                                "detail": f"due {p['due']}"})
            except Exception:
                pass
    for l in lead_rows:
        if l["status"].lower() in ("won", "done", "closed", "lost", "converted"):
            continue
        if l["last_contact"]:
            try:
                age = (today - datetime.strptime(l["last_contact"][:10], "%Y-%m-%d").date()).days
            except Exception:
                age = 999
            if age > 14:
                out.append({"type": "lead", "label": f"Lead cold: {l['company'] or l['contact']}",
                            "detail": f"last contact {l['last_contact']} ({age}d)"})
    for j in jobs:
        if j["status"].lower() in readers.JOB_TERMINAL:
            continue
        age = readers.job_age_days(j["date_in"])
        if age > 15 and j["status"].lower() != "done":
            out.append({"type": "job", "label": f"Job stuck: {j['wo'] or 'WO'}",
                        "detail": f"{j['customer'] or j['company'] or '—'} · {age}d since in"})
    return out[:8]


# ------------------------------------------------------------------ finance
@app.route("/finance")
def finance_page():
    tx = readers.finance()
    q = request.args.get("q", "").strip()
    month = request.args.get("month", "").strip()
    if q:
        ql = q.lower()
        tx = [t for t in tx if ql in t["description"].lower() or ql in t["category"].lower()]
    if month:
        tx = [t for t in tx if t["date"].startswith(month)]
    income = sum(t["amount"] for t in tx if t["type"] == "income")
    expense = sum(t["amount"] for t in tx if t["type"] == "expense")
    all_dates = {t["date"][:7] for t in readers.finance()}
    cats = readers.categories()
    return render_template("finance.html", tx=tx, income=income, expense=expense,
                           q=q, month=month, months=sorted(all_dates, reverse=True),
                           cats=cats)


@app.post("/finance/add")
def finance_add():
    date = form_str("date", _today())
    writers.add_finance({
        "date": date,
        "type": form_str("type", "income"),
        "category": form_str("category"),
        "description": form_str("description"),
        "amount": form_num("amount"),
    })
    synced = writers.sync_finance_to_daily(date)
    msg = "Transaction added — written to ITS_Finance_Tracker.csv"
    if synced:
        msg += " · daily note updated"
    flash(msg, "ok")
    return redirect(url_for("finance_page"))


@app.post("/finance/edit/<int:index>")
def finance_edit(index):
    date = form_str("date")
    writers.update_finance(index, {
        "date": date,
        "type": form_str("type"),
        "category": form_str("category"),
        "description": form_str("description"),
        "amount": form_num("amount"),
    })
    synced = writers.sync_finance_to_daily(date) if date else False
    msg = "Transaction updated — CSV rewritten"
    if synced:
        msg += " · daily note updated"
    flash(msg, "ok")
    return redirect(url_for("finance_page"))


@app.post("/finance/delete/<int:index>")
def finance_delete(index):
    rows = readers.finance()
    date = rows[index]["date"] if 0 <= index < len(rows) else None
    writers.delete_finance(index)
    synced = writers.sync_finance_to_daily(date) if date else False
    msg = "Transaction deleted — CSV rewritten"
    if synced:
        msg += " · daily note updated"
    flash(msg, "ok")
    return redirect(url_for("finance_page"))


@app.get("/finance/export")
def finance_export():
    tx = readers.finance()
    out = io.StringIO()
    out.write(",".join(readers.FINANCE_HEADER) + "\n")
    for t in tx:
        out.write(f'{t["date"]},{t["type"]},{t["category"]},"{t["description"].replace(chr(34), chr(34) * 2)}",{t["amount"]}\n')
    data = out.getvalue().encode("utf-8")
    return send_file(io.BytesIO(data), as_attachment=True,
                     download_name="ITS_Finance_Export.csv", mimetype="text/csv")


# ------------------------------------------------------------------ report
@app.route("/report")
def report_page():
    month = request.args.get("month") or _this_month()
    tx = [t for t in readers.finance() if t["date"].startswith(month)]
    income = sum(t["amount"] for t in tx if t["type"] == "income")
    expense = sum(t["amount"] for t in tx if t["type"] == "expense")
    cat_income = defaultdict(float)
    cat_expense = defaultdict(float)
    daily = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for t in tx:
        if t["type"] == "income":
            cat_income[t["category"]] += t["amount"]
            daily[t["date"]]["income"] += t["amount"]
        else:
            cat_expense[t["category"]] += t["amount"]
            daily[t["date"]]["expense"] += t["amount"]
    clients = {}
    for name in readers.known_client_names():
        d = readers.client_detail(name)
        if d["income"] or d["expense"]:
            clients[name] = {"income": d["income"], "expense": d["expense"],
                             "profit": d["profit"]}
    months = sorted({t["date"][:7] for t in readers.finance()}, reverse=True)
    return render_template("report.html", month=month, months=months,
                           income=income, expense=expense, net=income - expense, tx=tx,
                           cat_income=dict(sorted(cat_income.items(), key=lambda kv: -kv[1])),
                           cat_expense=dict(sorted(cat_expense.items(), key=lambda kv: -kv[1])),
                           daily_rows=sorted(daily.items()),
                           clients=dict(sorted(clients.items())))


@app.get("/report/export.xlsx")
def report_export():
    from openpyxl import Workbook
    month = request.args.get("month") or _this_month()
    tx = [t for t in readers.finance() if t["date"].startswith(month)]
    income = sum(t["amount"] for t in tx if t["type"] == "income")
    expense = sum(t["amount"] for t in tx if t["type"] == "expense")

    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws.append(["ITS — Monthly report", month])
    ws.append([])
    ws.append(["Income", income])
    ws.append(["Expenses", expense])
    ws.append(["Net", income - expense])

    ws2 = wb.create_sheet("Transactions")
    ws2.append(readers.FINANCE_HEADER)
    for t in tx:
        ws2.append([t["date"], t["type"], t["category"], t["description"], t["amount"]])

    cat_income = defaultdict(float)
    cat_expense = defaultdict(float)
    for t in tx:
        (cat_income if t["type"] == "income" else cat_expense)[t["category"]] += t["amount"]
    ws3 = wb.create_sheet("By Category")
    ws3.append(["Type", "Category", "Amount"])
    for k, v in sorted(cat_income.items()):
        ws3.append(["income", k, v])
    for k, v in sorted(cat_expense.items()):
        ws3.append(["expense", k, v])

    ws4 = wb.create_sheet("Clients")
    ws4.append(["Client", "Income", "Expenses", "Profit"])
    for name in readers.known_client_names():
        d = readers.client_detail(name)
        if d["income"] or d["expense"]:
            ws4.append([name, d["income"], d["expense"], d["profit"]])

    daily = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for t in tx:
        daily[t["date"]][t["type"]] += t["amount"]
    ws5 = wb.create_sheet("Daily")
    ws5.append(["Date", "Income", "Expenses", "Net"])
    for d, v in sorted(daily.items()):
        ws5.append([d, v["income"], v["expense"], v["income"] - v["expense"]])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f"ITS_Report_{month}.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ------------------------------------------------------------------ search
@app.route("/search")
def search_page():
    q = request.args.get("q", "").strip()
    results = readers.search(q) if q else {}
    counts = {k: len(v) for k, v in results.items()} if results else {}
    total = sum(counts.values()) if counts else 0
    return render_template("search.html", q=q, results=results, counts=counts, total=total)


# ------------------------------------------------------------------ daily
@app.route("/daily")
def daily_page():
    notes = readers.daily_notes()
    month = request.args.get("month", "")
    focus = request.args.get("date", "")
    if focus and re.fullmatch(r"\d{4}-\d{2}-\d{2}", focus):
        month = month or focus[:7]
    if month:
        notes = [n for n in notes if n["date"].startswith(month)]
    months = sorted({n["date"][:7] for n in readers.daily_notes()}, reverse=True)
    n_income = sum(n["income_da"] for n in notes)
    n_expense = sum(n["expense_parts"] + n["expense_tools"] + n["expense_transport"] + n["expense_overhead"] + n["expense_other"] for n in notes)
    hours = sum(n["hours_worked"] for n in notes)

    mismatches = []
    for n in notes:
        fin_inc, fin_exp = readers.note_totals(n["date"])
        note_inc = n["income_da"]
        note_exp = n["expense_parts"] + n["expense_tools"] + n["expense_transport"] + n["expense_overhead"] + n["expense_other"]
        if abs(fin_inc - note_inc) > 0.5 or abs(fin_exp - note_exp) > 0.5:
            mismatches.append({"date": n["date"], "note_income": note_inc, "fin_income": fin_inc,
                               "note_expense": note_exp, "fin_expense": fin_exp})
    return render_template("daily.html", notes=notes, months=months, month=month,
                           n_income=n_income, n_expense=n_expense, hours=hours,
                           mismatches=mismatches, focus=focus if any(n["date"] == focus for n in notes) else "")


@app.post("/daily/update/<date>")
def daily_update(date):
    fields = {}
    if request.form.get("energy") not in (None, ""):
        fields["energy"] = request.form["energy"].strip() or "''"
    for k in ("hours_worked", "hours_billable", "income_da",
              "expense_parts", "expense_tools", "expense_transport", "expense_overhead", "expense_other"):
        v = request.form.get(k, "")
        if v != "":
            fields[k] = v.strip()
    if request.form.get("status") not in (None, ""):
        fields["status"] = request.form["status"].strip()
    fields["revenue_da"] = request.form.get("income_da", "0").strip() or "0"
    if fields:
        try:
            writers.update_daily_note(date, fields)
            synced = writers.sync_daily_to_finance(date)
            writers.sync_finance_to_daily(date)
            msg = f"Daily note {date} updated"
            if synced:
                count = len(synced)
                msg += f" — {count} finance entr{'y' if count == 1 else 'ies'} auto-synced"
            flash(msg, "ok")
        except FileNotFoundError:
            flash(f"No daily note for {date}", "err")
    return redirect(url_for("daily_page", month=date[:7]))


# ------------------------------------------------------------------ calendar
@app.route("/calendar")
def calendar_page():
    ym = request.args.get("month") or _this_month()
    try:
        year, month = int(ym[:4]), int(ym[5:7])
    except ValueError:
        year, month = datetime.now().year, datetime.now().month
    month_days = _cal.monthrange(year, month)[1]
    first_weekday = _cal.monthrange(year, month)[0]  # Monday == 0
    prev_m = (datetime(year, month, 1) - timedelta(days=1)).strftime("%Y-%m")
    next_m = (datetime(year, month, month_days) + timedelta(days=1)).strftime("%Y-%m")

    fin_by_day = defaultdict(lambda: [0.0, 0.0])
    for t in readers.finance():
        if t["date"].startswith(ym):
            fin_by_day[t["date"][-2:]][0 if t["type"] == "income" else 1] += t["amount"]
    note_by_day = {n["date"][-2:]: n for n in readers.daily_notes() if n["date"].startswith(ym)}

    days = []
    for d in range(1, month_days + 1):
        dd = f"{d:02d}"
        inc, exp = fin_by_day[dd]
        note = note_by_day.get(dd)
        cls = "day-empty"
        if inc and exp:
            cls = "day-both"
        elif inc:
            cls = "day-income"
        elif exp:
            cls = "day-expense"
        if note:
            cls += " has-note"
        days.append({"d": d, "date": f"{ym}-{dd}", "income": inc, "expense": exp,
                     "note": bool(note), "cls": cls})
    return render_template("calendar.html", ym=ym, year=year, month=month,
                           first_weekday=first_weekday,
                           month_days=month_days, days=days,
                           prev_month=prev_m, next_month=next_m)


# ------------------------------------------------------------------ projects
@app.route("/projects")
def projects_page():
    return render_template("projects.html", projects=readers.projects())


@app.post("/projects/update/<project_id>")
def projects_update(project_id):
    fields = {}
    for k in ("status", "due", "progress"):
        v = request.form.get(k, "").strip()
        if v != "":
            fields[k] = v
    if fields:
        try:
            writers.update_project(project_id, fields)
            flash(f"Project '{project_id}' updated", "ok")
        except FileNotFoundError:
            flash("Project not found", "err")
    return redirect(url_for("projects_page"))


# ------------------------------------------------------------------ jobs
@app.route("/jobs")
def jobs_page():
    return render_template("jobs.html", jobs=readers.jobs())


@app.route("/jobs/board")
def jobs_board():
    jobs = readers.jobs()
    columns = []
    for s in readers.JOB_STAGES:
        columns.append({"stage": s, "terminal": s.lower() in readers.JOB_TERMINAL,
                        "jobs": [j for j in jobs if (j["status"] or "Received").lower() == s.lower()]})
    others = [j for j in jobs if (j["status"] or "Received") not in [s.lower() for s in readers.JOB_STAGES]]
    if others:
        columns.append({"stage": "Other", "terminal": True, "jobs": others})
    return render_template("board.html", columns=columns)


@app.post("/jobs/add")
def jobs_add():
    from writers import write_jobs, JOBS_COLS
    rows = [dict(j) for j in readers.jobs()]
    rows.append({
        "date_in": form_str("date_in", _today()),
        "wo": form_str("wo"),
        "customer": form_str("customer"),
        "company": form_str("company"),
        "phone": form_str("phone"),
        "board": form_str("board"),
        "equipment": form_str("equipment"),
        "symptoms": form_str("symptoms"),
        "diagnosis": form_str("diagnosis"),
        "quote": form_num("quote"),
        "accepted": form_str("accepted"),
        "date_out": form_str("date_out"),
        "paid": form_num("paid"),
        "status": form_str("status", "Received"),
        "notes": form_str("notes"),
    })
    write_jobs(rows)
    flash("Job added — written to PCB_Job_Tracker.xlsx", "ok")
    return redirect(url_for("jobs_page"))


@app.post("/jobs/update/<wo>")
def jobs_update(wo):
    from writers import write_jobs
    rows = [dict(j) for j in readers.jobs()]
    for row in rows:
        if row["wo"] == wo:
            for k in ("date_in", "customer", "company", "phone", "board", "equipment",
                      "symptoms", "diagnosis", "quote", "accepted", "date_out",
                      "paid", "status", "notes"):
                v = request.form.get(k)
                if v is not None:
                    row[k] = v.strip() if k not in ("quote", "paid") else form_num(k, v)
            break
    write_jobs(rows)
    flash(f"Job {wo} updated — XLSX rewritten", "ok")
    return redirect(url_for("jobs_page"))


@app.post("/jobs/delete/<wo>")
def jobs_delete(wo):
    from writers import write_jobs
    rows = [dict(j) for j in readers.jobs() if j["wo"] != wo]
    write_jobs(rows)
    flash(f"Job {wo} deleted", "ok")
    return redirect(url_for("jobs_page"))


# ------------------------------------------------------------------ leads
@app.route("/leads")
def leads_page():
    return render_template("leads.html", leads=readers.leads(),
                           mapping=readers.leads_prospecting_xlsx())


@app.post("/leads/add")
def leads_add():
    from writers import write_leads
    rows = [dict(r) for r in readers.leads()]
    rows.append({
        "id": str(len(rows) + 1),
        "company": form_str("company"),
        "contact": form_str("contact"),
        "title": form_str("title"),
        "phone": form_str("phone"),
        "zone": form_str("zone"),
        "status": form_str("status", "New"),
        "value_da": str(int(form_num("value_da"))),
        "last_contact": form_str("last_contact"),
        "notes": form_str("notes"),
    })
    write_leads(rows)
    flash("Lead added — saved to ITS_Leads.csv", "ok")
    return redirect(url_for("leads_page"))


@app.post("/leads/update/<lead_id>")
def leads_update(lead_id):
    from writers import write_leads
    rows = [dict(r) for r in readers.leads()]
    for row in rows:
        if row["id"] == lead_id:
            for k in ("company", "contact", "title", "phone", "zone", "status", "notes", "last_contact"):
                v = request.form.get(k)
                if v is not None:
                    row[k] = v.strip()
            v = request.form.get("value_da")
            if v is not None:
                row["value_da"] = str(int(form_num("value_da", v)))
            break
    write_leads(rows)
    flash("Lead updated", "ok")
    return redirect(url_for("leads_page"))


@app.post("/leads/delete/<lead_id>")
def leads_delete(lead_id):
    from writers import write_leads
    rows = [dict(r) for r in readers.leads() if r["id"] != lead_id]
    write_leads(rows)
    flash("Lead deleted", "ok")
    return redirect(url_for("leads_page"))


# ------------------------------------------------------------------ clients
@app.route("/clients")
def clients_page():
    return render_template("clients.html", clients=readers.clients(),
                           known=readers.known_client_names())


@app.route("/clients/<name>")
def client_detail_route(name):
    return render_template("client.html", client=readers.client_detail(name))


@app.post("/clients/add")
def clients_add():
    from writers import write_clients
    rows = [dict(r) for r in readers.clients()]
    rows.append({
        "id": str(len(rows) + 1),
        "name": form_str("name"),
        "company": form_str("company"),
        "phone": form_str("phone"),
        "email": form_str("email"),
        "source": form_str("source"),
        "notes": form_str("notes"),
    })
    write_clients(rows)
    flash("Client added — saved to ITS_Clients.csv", "ok")
    return redirect(url_for("clients_page"))


@app.post("/clients/update/<client_id>")
def clients_update(client_id):
    from writers import write_clients
    rows = [dict(r) for r in readers.clients()]
    for row in rows:
        if row["id"] == client_id:
            for k in ("name", "company", "phone", "email", "source", "notes"):
                v = request.form.get(k)
                if v is not None:
                    row[k] = v.strip()
            break
    write_clients(rows)
    flash("Client updated", "ok")
    return redirect(url_for("clients_page"))


@app.post("/clients/delete/<client_id>")
def clients_delete(client_id):
    from writers import write_clients
    rows = [dict(r) for r in readers.clients() if r["id"] != client_id]
    write_clients(rows)
    flash("Client deleted", "ok")
    return redirect(url_for("clients_page"))


# ------------------------------------------------------------------ invoices
@app.route("/invoices")
def invoices_page():
    return render_template("invoices.html", invoices=readers.invoices(),
                           next_number=writers.next_invoice_number())


@app.post("/invoices/add")
def invoices_add():
    number = form_str("number", writers.next_invoice_number())
    client = form_str("client")
    date = form_str("date", _today())
    items = writers.parse_line_items(request.form.get("line_items", ""))
    amount = round(sum(it["amount"] for it in items), 2) if items else form_num("amount")
    try:
        writers.create_invoice(number, client, date, amount, line_items=items or None)
        flash(f"Invoice {number} created — 'Mark paid' will auto-log income in Finance", "ok")
    except FileExistsError:
        flash(f"Invoice {number} already exists", "err")
    return redirect(url_for("invoices_page"))


@app.post("/invoices/toggle/<number>")
def invoices_toggle(number):
    try:
        writers.toggle_invoice_paid(number)
        created = writers.sync_invoice_to_finance(number)
        msg = f"Invoice {number} marked {'paid' if created else 'unpaid'}"
        if created:
            msg += " · income auto-logged in Finance"
        flash(msg, "ok")
    except FileNotFoundError:
        flash("Invoice not found", "err")
    return redirect(url_for("invoices_page"))


@app.post("/invoices/update/<number>")
def invoices_update(number):
    client = form_str("client")
    date = form_str("date")
    items = writers.parse_line_items(request.form.get("line_items", ""))
    amount = round(sum(it["amount"] for it in items), 2) if items else form_num("amount")
    try:
        writers.update_invoice(number, client=client or None, date=date or None,
                               amount=(amount or None), line_items=(items or None))
        writers.sync_invoice_to_finance(number)
        flash(f"Invoice {number} updated", "ok")
    except FileNotFoundError:
        flash("Invoice not found", "err")
    return redirect(url_for("invoices_page"))


@app.post("/invoices/delete/<number>")
def invoices_delete(number):
    writers.sync_invoice_to_finance(number, keep=False)
    writers.delete_invoice(number)
    flash(f"Invoice {number} deleted — its Finance income row removed", "ok")
    return redirect(url_for("invoices_page"))


@app.route("/invoices/<number>/print")
def invoice_print(number):
    inv = readers.invoice_by_number(number)
    if not inv:
        abort(404)
    amount = inv["amount"] or 0
    ht = round(amount / 1.19, 2)
    tva = round(amount - ht, 2)
    return render_template("invoice_print.html", inv=inv, ht=ht, tva=tva)


# ------------------------------------------------------------------ backup
@app.get("/backup")
def backup_page():
    zpath = writers.create_backup()
    flash(f"Backup created: {zpath.name}", "ok")
    return send_file(zpath, as_attachment=True, download_name=zpath.name)


@app.get("/backups")
def backups_list():
    backups = []
    try:
        for zp in sorted(writers.BACKUP_DIR.glob("ITS_Backup_*.zip"), reverse=True):
            backups.append({"name": zp.name,
                            "size_mb": round(zp.stat().st_size / 1024 / 1024, 1),
                            "modified": datetime.fromtimestamp(zp.stat().st_mtime).strftime("%Y-%m-%d %H:%M")})
    except OSError:
        pass
    return render_template("backups.html", backups=backups)


@app.post("/backup/restore/<path:name>")
def backup_restore(name):
    target = (writers.BACKUP_DIR / name).resolve()
    try:
        if not target.is_relative_to(writers.BACKUP_DIR.resolve()):
            raise ValueError("Bad name")
        restored, skipped = writers.restore_backup(name)
        flash(f"Restored {restored} file{'s' if restored != 1 else ''} from {name}"
              + (f" · {skipped} skipped" if skipped else ""), "ok")
    except FileNotFoundError:
        flash("That backup file does not exist", "err")
    except (ValueError, zipfile.BadZipFile) as e:
        flash(f"Restore failed: {e}", "err")
    return redirect(url_for("backups_list"))


# ------------------------------------------------------------------ documents
@app.route("/vault/<path:relpath>")
def vault_file(relpath):
    target = (readers.BASE / relpath).resolve()
    if not target.is_relative_to(readers.BASE.resolve()) or not target.is_file():
        abort(404)
    return send_file(target)


@app.route("/documents")
def documents_page():
    docs = readers.documents()
    q = request.args.get("q", "").strip()
    ext = request.args.get("ext", "").strip()
    if q:
        ql = q.lower()
        docs = [d for d in docs if ql in d["name"].lower() or ql in d["folder"].lower()]
    if ext:
        docs = [d for d in docs if d["ext"] == ext]
    exts = sorted({d["ext"] for d in docs})
    sizes = sum(d["size_kb"] for d in docs)
    return render_template("documents.html", docs=docs, q=q, ext=ext,
                           exts=exts, total_mb=sizes / 1024, n=len(docs))


if __name__ == "__main__":
    print("\n  ITS Command Center — local web app")
    print(f"  Vault: {readers.BASE}")
    print("  Open:  http://localhost:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=True)