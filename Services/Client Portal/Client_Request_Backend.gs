/**
 * ITS Industrial Technology Solutions — Client Project Request Backend
 * Google Apps Script (Web App)
 *
 * WHAT IT DOES:
 *  - Serves the branded request form (doGet)
 *  - Receives client requests + uploaded files (doPost)
 *  - Saves files to a per-project subfolder in Google Drive
 *  - Logs each request as a row in a Google Sheet
 *  - Sends a Telegram notification with the project summary + file links
 *
 * ----------------------------------------------------------------
 * INSTALLATION (see Client_Portal_Setup.md for full guide):
 *  1. Open https://script.google.com and create a new project
 *  2. Paste this entire file into Code.gs
 *  3. Optionally create an HTML file named "Form" with the contents
 *     of Client_Request_Form.html and uncomment doGet below.
 *  4. Edit the CONFIG values below (sheet ID, last 3 rows = TRUE).
 *  5. Run setupNewClientPortal() once — it creates the Drive folder
 *     and the tracking sheet, and prints IDs to paste into CONFIG.
 *  6. Deploy -> New deployment -> Web app:
 *       - Execute as: Me
 *       - Who has access: Anyone
 *     Copy the /exec URL and paste it into the form's fetch URL.
 * ----------------------------------------------------------------
 */

// ============================================================
// CONFIGURATION — EDIT THESE
// ============================================================
var CONFIG = {
  // Google Sheet ID (from the URL of your tracking sheet).
  // Example: https://docs.google.com/spreadsheets/d/<THIS_PART>/edit
  sheetId: "",

  // Name of the tab inside the sheet where rows are logged.
  sheetTab: "Requests",

  // Google Drive root folder that will hold per-project subfolders.
  // Set to TRUE after you run setupNewClientPortal() and paste the
  // value below, OR paste the folder ID directly.
  portalFolderId: "",

  // ---------- TELEGRAM ----------
  // Set telegramEnabled = true and fill the bot token + chat id.
  telegramEnabled: false,
  telegramBotToken: "",          // from @BotFather
  telegramChatId: "",            // your numeric chat id (from @userinfobot)
  // ------------------------------

  // Email you want notifications sent to as well (optional).
  notifyEmail: "",

  maxFileMb: 48                   // per-file limit (Apps Script caps ~50MB)
};

// Name of the root folder inside Drive (used by setupNewClientPortal)
var PORTAL_FOLDER_NAME = "ITS Client Projects";

// ============================================================
// SETUP — run once from the Apps Script editor
// ============================================================
function setupNewClientPortal() {
  var ui = SpreadsheetApp.getUi();
  if (!ui) {
    throw new Error("Run this from the Apps Script editor (after opening a Google Sheet).");
  }

  // 1. Create root Drive folder
  var folder;
  var it = DriveApp.getFoldersByName(PORTAL_FOLDER_NAME);
  if (it.hasNext()) {
    folder = it.next();
  } else {
    folder = DriveApp.createFolder(PORTAL_FOLDER_NAME);
  }

  // 2. Create/setup the tracking sheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var tab = ss.getSheetByName("Requests");
  if (!tab) {
    tab = ss.insertSheet("Requests");
  }
  var headers = [
    "Timestamp", "Name", "Phone/WhatsApp", "Email", "Company",
    "Service", "Project Type", "Description", "Details", "Quantity",
    "Target Budget (DA)", "Delivery City", "Ship To", "Contacts Preferred",
    "File 1", "File 2", "File 3", "File 4", "File 5", "File 6"
  ];
  // Rebuild header row cleanly
  tab.clear();
  tab.getRange(1, 1, 1, headers.length).setValues([headers]);
  tab.setFrozenRows(1);
  tab.getRange(1, 1, 1, headers.length).setFontWeight("bold");
  tab.setColumnWidths(1, 1, 180);

  var out = [];
  out.push("✅ Portal ready!");
  out.push("");
  out.push("Root Drive folder: " + folder.getUrl());
  out.push("  → Paste this folder ID in CONFIG.portalFolderId:");
  out.push("  " + folder.getId());
  out.push("");
  out.push("Tracking Sheet ID:");
  out.push("  " + ss.getId());
  out.push("  → Paste this in CONFIG.sheetId");
  out.push("");
  out.push("Then: paste the /exec URL from Deploy → New deployment");
  out.push("into the form's WEB_APP_URL constant.");

  ui.alert(out.join("\n"));
}

// ============================================================
// SERVE THE FORM (optional — you can also host the HTML yourself)
// ============================================================
function doGet() {
  return HtmlService.createHtmlOutputFromFile("Form")
    .setTitle("ITS — Submit Your Project")
    .addMetaTag("viewport", "width=device-width, initial-scale=1")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// ============================================================
// RECEIVE SUBMISSION (POST from the form)
// ============================================================
function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(30000);

  try {
    // Parse incoming JSON
    var data;
    if (e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    } else if (e.parameter && e.parameter.payload) {
      data = JSON.parse(e.parameter.payload);
    } else {
      return jsonReply({ ok: false, error: "No data received." });
    }

    // ---- Get the root folder ----
    var rootFolder;
    if (CONFIG.portalFolderId) {
      rootFolder = DriveApp.getFolderById(CONFIG.portalFolderId);
    } else {
      var it = DriveApp.getFoldersByName(PORTAL_FOLDER_NAME);
      if (it.hasNext()) rootFolder = it.next();
    }
    if (!rootFolder) {
      return jsonReply({ ok: false, error: "Root folder not configured." });
    }

    // ---- Build a per-project subfolder ----
    var stamp = Utilities.formatDate(new Date(), "GMT+1", "yyyy-MM-dd_HHmm");
    var safeName = sanitize(String(data.name || "Client"));
    var subName = stamp + "_" + safeName;
    var subFolder = rootFolder.createFolder(subName);

    // ---- Save uploaded files ----
    var fileUrls = [];
    var files = data.files || [];
    for (var i = 0; i < files.length; i++) {
      var f = files[i];
      if (!f || !f.name || !f.b64) continue;
      // base64 size guard
      if (f.b64.length > CONFIG.maxFileMb * 1024 * 1024 * 1.34) {
        continue; // too large, skip silently
      }
      try {
        var blob = Utilities.newBlob(
          Utilities.base64Decode(f.b64),
          f.mimeType || null,
          sanitize(f.name)
        );
        var driveFile = subFolder.createFile(blob);
        fileUrls.push(driveFile.getUrl());
      } catch (err) {
        fileUrls.push("(upload error: " + err + ")");
      }
      // Apps Script runtime is limited; be safe with several files
      if (fileUrls.length >= 6) break;
    }

    // ---- Log row to sheet ----
    if (CONFIG.sheetId) {
      var ss = SpreadsheetApp.openById(CONFIG.sheetId);
      var tab = ss.getSheetByName(CONFIG.sheetTab) || ss.getSheetByName("Requests") || ss.insertSheet("Requests");
      var row = [
        new Date(),
        data.name || "",
        data.phone || "",
        data.email || "",
        data.company || "",
        data.service || "",
        data.projectType || "",
        data.description || "",
        data.details || "",
        data.quantity || "",
        data.budget || "",
        data.city || "",
        data.ship || "",
        data.contactPref || "",
        fileUrls[0] || "",
        fileUrls[1] || "",
        fileUrls[2] || "",
        fileUrls[3] || "",
        fileUrls[4] || "",
        fileUrls[5] || ""
      ];
      tab.appendRow(row);
    }

    // ---- Send email notification (optional) ----
    if (CONFIG.notifyEmail) {
      try {
        MailApp.sendEmail(CONFIG.notifyEmail, "ITS New Client Request — " + (data.name || "?"),
          buildSummary(data, fileUrls));
      } catch (err) {}
    }

    // ---- Send Telegram notification ----
    if (CONFIG.telegramEnabled && CONFIG.telegramBotToken && CONFIG.telegramChatId) {
      try {
        sendTelegram(buildSummary(data, fileUrls));
      } catch (err) {}
    }

    return jsonReply({ ok: true, folder: subFolder.getUrl() });
  } catch (err) {
    return jsonReply({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

// ============================================================
// HELPERS
// ============================================================
function buildSummary(data, fileUrls) {
  var s = channelBold("*ITS — NEW CLIENT REQUEST*\n");
  s += "━━━━━━━━━━━━━━━━\n";
  s += "👤 " + (data.name || "-") + "\n";
  s += "📞 " + (data.phone || "-") + "\n";
  s += "📧 " + (data.email || "-") + "\n";
  if (data.company) s += "🏢 " + data.company + "\n";
  s += "🔧 " + (data.service || "-");
  if (data.projectType) s += " — " + data.projectType;
  s += "\n\n📝 " + (data.description || "-") + "\n";
  if (data.details) s += "🔎 Details:\n" + data.details + "\n";
  if (data.quantity) s += "🔢 Quantity: " + data.quantity + "\n";
  if (data.budget) s += "💰 Budget: " + data.budget + " DA\n";
  if (data.city) s += "📍 City: " + data.city + "\n";
  if (data.ship) s += "🚚 Ship to: " + data.ship + "\n";
  if (data.contactPref) s += "✉️ Prefers: " + data.contactPref + "\n";
  if (fileUrls.length) {
    s += "\n📎 Files:\n" + fileUrls.map(function(u){ return u; }).join("\n");
  }
  s += "\n\n_Reply to this client with your quote._";
  return s;
}

function sendTelegram(message) {
  var url = "https://api.telegram.org/bot" + CONFIG.telegramBotToken +
    "/sendMessage?chat_id=" + CONFIG.telegramChatId +
    "&text=" + encodeURIComponent(message) +
    "&parse_mode=Markdown&disable_web_page_preview=true";
  UrlFetchApp.fetch(url);
}

// Strip markup chars that Telegram Markdown would choke on
function channelBold(t){ return t; } // plain bold handled by *...*

function sanitize(name) {
  return String(name).replace(/[^\w.\- ]+/g, "_").trim() || "file";
}

function jsonReply(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// ============================================================
// TEST — run from editor with fake data to verify the pipeline
// ============================================================
function testSubmission() {
  var fake = {
    name: "Test Client",
    phone: "0699 32 40 76",
    email: "test@example.com",
    service: "PCB Fabrication",
    projectType: "2-layer PCB",
    description: "This is a test submission.",
    details: "Board type / layers: 2-layer FR-4\nQuantity: 100 units\nVenue: Recommended\nWhat to fabricate: Test board",
    quantity: "100 units",
    budget: "50000",
    city: "Skikda",
    ship: "Local DZ",
    contactPref: "WhatsApp",
    files: []
  };
  var resp = doPost({ postData: { contents: JSON.stringify(fake) } });
  Logger.log(resp.getContent());
}
