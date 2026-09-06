# ITS Client Portal — Setup Guide

This guide gets your client request portal live and free (no monthly cost).
Stack: **GitHub Pages** (hosting) + **Google Apps Script** (backend) + **Google Drive/Sheets** (storage) + **Telegram** (notifications).

---

## Part 1 — Create a Google Sheet (for tracking requests)

1. Go to https://sheets.new (or Google Drive → New → Google Sheets)
2. Rename it: **ITS Client Requests**
3. You don't need to build headers — the backend does that. Leave it blank or with one empty "Requests" tab.

---

## Part 2 — Upload the backend to Google Apps Script

1. Go to https://script.google.com and click **New project**
2. Name it **ITS Client Portal**
3. Delete any default code and **paste the entire contents of `Client_Request_Backend.gs`** into `Code.gs`
4. Click the **Save** (disk) icon.

---

## Part 3 — Create the form HTML in Apps Script (optional, but recommended)

If you want Google to also host the form itself (a second, simpler option), do this:

1. In the Apps Script editor, click **+** next to Files → **HTML**
2. Name it exactly **`Form`**
3. **Paste the entire contents of `Client_Request_Form.html`** into it.

> ☝️ Note: `doGet()` in the backend already serves a file named `Form`. If you host the HTML yourself (GitHub Pages) instead, just ignore this step — you'll paste the same HTML into your repo instead.

---

## Part 4 — Set up Telegram notifications

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`, follow the prompts, choose a name (e.g. `ITS Client Alerts`) and username (e.g. `ITS_Client_Alerts_bot`)
3. BotFather replies with an **HTTP API token** — copy it (looks like `123456789:ABC...`)
4. Open Telegram, search for **@userinfobot**, send it any message → it replies with your numeric **id** (e.g. `987654321`)
5. You now have:
   - **Bot token** → `CONFIG.telegramBotToken`
   - **Chat id** → `CONFIG.telegramChatId`

---

## Part 5 — Configure & run setup

1. In the Apps Script editor, edit the **`CONFIG`** object at the top:
   - Set `telegramBotToken` to your token
   - Set `telegramChatId` to your id
   - Set `telegramEnabled = true`
   - Set `notifyEmail` to your email (optional, for a backup email alert)
2. Click **Run → setupNewClientPortal** (first time it asks for permissions — click through, the file may appear "unsafe", proceed)
3. An alert appears with two IDs:
   - **Tracking Sheet ID** → paste into `CONFIG.sheetId`
   - **Drive folder ID** → paste into `CONFIG.portalFolderId`

---

## Part 6 — Deploy as a Web App

1. In the Apps Script editor click **Deploy → New deployment**
2. Click the gear ⚙️ → **Web app**
3. Set:
   - **Description:** ITS Client Portal
   - **Execute as:** *Me (you)*
   - **Who has access:** *Anyone*
4. Click **Deploy** → authorise if prompted
5. Copy the **Web app URL** — it ends in `/exec`
6. Save it somewhere safe (you'll need it below)

> ⚠️ Every time you change the `.gs` code, click **Deploy → Manage deployments → edit → New version** to push the update.

---

## Part 7 — Wire up the form (frontend)

Edit `Client_Request_Form.html` and, near the top of the `<script>`, replace:

```
var WEB_APP_URL = "PASTE_YOUR_DEPLOYED_SCRIPT_URL_HERE";
```

with your `/exec` URL.

### Where to put the HTML on your site
- **Option A (GitHub Pages):** save this as `client_request.html` inside `website/` and link to it.
- **Option B (Google hosts it):** skip GitHub. Just open your `/exec` URL directly — Google renders the `Form` HTML.

---

## Part 8 — Test the whole flow

1. Open the form URL
2. Fill in the fields, attach a test file
3. Submit
4. Check:
   - ✅ Files appear in **Google Drive → ITS Client Projects → <date>_<name>** folder
   - ✅ A row is added to your **Google Sheet**
   - ✅ A **Telegram** message arrives with the summary + links
   - ✅ (if set) An **email** notification arrives

---

## Part 9 — Link from the main website

Add a button to `website/index.html` (hero + nav) linking to your portal page
(`client_request.html` on GitHub Pages, or your `/exec` URL).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Root folder not configured" | Run `setupNewClientPortal()` and paste the IDs into CONFIG |
| No Telegram alert | Check `telegramEnabled`, token, and chatId; send a test message |
| Files > ~48MB rejected | Apps Script limit ~50MB. Compress to ZIP or ask client to send a Drive link |
| Changes not live | Apps Script: Deploy → Manage → New version |
| Form says "PASTE_YOUR..." | You forgot to put the real URL in `WEB_APP_URL` |
| Load page redirects to `script.google.com` | Add `mode:'no-cors'` is already set; if error, host via GitHub Pages instead of Apps Script doGet |

---

## Costs
- GitHub Pages: **free**
- Google Apps Script / Drive / Sheets: **free tier**
- Telegram Bot API: **free**

## Files
- `Client_Request_Backend.gs` — Google Apps Script backend
- `Client_Request_Form.html` — branded frontend form (FR/AR)
