"""ITS Command Center — local web app over the ITS Profile vault.

The vault folder IS the database: every page reads the real files live and
every edit writes straight back into them (with a .bak safety copy).
"""
from __future__ import annotations

import io
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, send_file, url_for

import readers
import writers

app = Flask(__name__)
app.secret_key = "its-command-center-local"


def fmt_da(v: float) -> str:
    return f"{int(round(v or 0)):,}".replace(",", " ")


app.jinja_env.filters["da"] = fmt_da


@app.context_processor
def inject_vault():
    return {"vault": str(readers.BASE), "now": datetime.now().strftime("%Y-%m-%d")}


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


# --------------------------------------------------------------------------- routes
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
    monthly = [{"month": m, **by_month[m]} for m in months]

    by_category = defaultdict(float)
    for t in tx:
        if t["type"] == "income":
            by_category[t["category"]] += t["amount"]

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
    open_jobs = [j for j in jobs if j["status"] and j["status"].lower() not in ("picked up", "cancelled", "closed")]
    job_income = sum(j["paid"] for j in jobs)
    lead_rows = readers.leads()
    leads_by_status = defaultdict(int)
    for l in lead_rows:
        leads_by_status[l["status"] or "New"] += 1

    projects = readers.projects()
    active_projects = [p for p in projects if p["status"] in ("in-progress", "active", "ongoing", "planned")]
    week_no = datetime.now().isocalendar()[1]

    return render_template("dashboard.html",
                           income=income, expense=expense, profit=profit,
                           n_tx=len(tx), monthly=monthly, by_category=by_category,
                           worked=worked, billable=billable, notes_income=notes_income,
                           yield_per_hr=yield_per_hr, energy=energy, n_notes=len(notes),
                           open_jobs=open_jobs, job_income=job_income,
                           leads_by_status=leads_by_status, n_leads=len(lead_rows),
                           active_projects=active_projects, week_no=week_no)


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
    writers.add_finance({
        "date": form_str("date", datetime.now().strftime("%Y-%m-%d")),
        "type": form_str("type", "income"),
        "category": form_str("category"),
        "description": form_str("description"),
        "amount": form_num("amount"),
    })
    flash("Transaction added — written to ITS_Finance_Tracker.csv", "ok")
    return redirect(url_for("finance_page"))


@app.post("/finance/edit/<int:index>")
def finance_edit(index):
    writers.update_finance(index, {
        "date": form_str("date"),
        "type": form_str("type"),
        "category": form_str("category"),
        "description": form_str("description"),
        "amount": form_num("amount"),
    })
    flash("Transaction updated — CSV rewritten", "ok")
    return redirect(url_for("finance_page"))


@app.post("/finance/delete/<int:index>")
def finance_delete(index):
    writers.delete_finance(index)
    flash("Transaction deleted — CSV rewritten", "ok")
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


# ------------------------------------------------------------------ daily
@app.route("/daily")
def daily_page():
    notes = readers.daily_notes()
    month = request.args.get("month", "")
    if month:
        notes = [n for n in notes if n["date"].startswith(month)]
    months = sorted({n["date"][:7] for n in readers.daily_notes()}, reverse=True)
    n_income = sum(n["income_da"] for n in notes)
    n_expense = sum(n["expense_parts"] + n["expense_tools"] + n["expense_transport"] + n["expense_overhead"] for n in notes)
    hours = sum(n["hours_worked"] for n in notes)
    return render_template("daily.html", notes=notes, months=months, month=month,
                           n_income=n_income, n_expense=n_expense, hours=hours)


@app.post("/daily/update/<date>")
def daily_update(date):
    fields = {}
    if request.form.get("energy") not in (None, ""):
        fields["energy"] = request.form["energy"].strip() or "''"
    for k in ("hours_worked", "hours_billable", "income_da",
              "expense_parts", "expense_tools", "expense_transport", "expense_overhead"):
        v = request.form.get(k, "")
        if v != "":
            fields[k] = v.strip()
    if request.form.get("status") not in (None, ""):
        fields["status"] = request.form["status"].strip()
    fields["revenue_da"] = request.form.get("income_da", "0").strip() or "0"
    if fields:
        try:
            writers.update_daily_note(date, fields)
            flash(f"Daily note {date} updated (YAML frontmatter)", "ok")
        except FileNotFoundError:
            flash(f"No daily note for {date}", "err")
    return redirect(url_for("daily_page", month=date[:7]))


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


@app.post("/jobs/add")
def jobs_add():
    from writers import write_jobs, JOBS_COLS
    rows = [dict(j) for j in readers.jobs()]
    rows.append({
        "date_in": form_str("date_in", datetime.now().strftime("%Y-%m-%d")),
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
    return render_template("clients.html", clients=readers.clients())


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
    try:
        writers.create_invoice(number, form_str("client"), form_str("date"),
                               form_num("amount"), line_items=None)
        flash(f"Invoice {number} created", "ok")
    except FileExistsError:
        flash(f"Invoice {number} already exists", "err")
    return redirect(url_for("invoices_page"))


@app.post("/invoices/toggle/<number>")
def invoices_toggle(number):
    try:
        writers.toggle_invoice_paid(number)
        flash(f"Invoice {number} status toggled", "ok")
    except FileNotFoundError:
        flash("Invoice not found", "err")
    return redirect(url_for("invoices_page"))


@app.post("/invoices/delete/<number>")
def invoices_delete(number):
    writers.delete_invoice(number)
    flash(f"Invoice {number} deleted", "ok")
    return redirect(url_for("invoices_page"))


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