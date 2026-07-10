/**
 * ITS Industrial Technology Solutions — Labor Yield Tracker
 * Google Apps Script
 *
 * Installation:
 * 1. Open your Google Sheet
 * 2. Extensions → Apps Script
 * 3. Paste this entire file
 * 4. Click Save (disk icon), name the project "ITS Yield Tracker"
 * 5. Click Run → authorize (read your sheet, send emails)
 * 6. Refresh your sheet — a new menu "ITS Tools" appears
 */

// ============================================================
// MENU — appears in the Google Sheet after install
// ============================================================
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu("ITS Tools")
    .addItem("Check Yield Alerts Now", "checkYieldAlerts")
    .addItem("Send Weekly Summary Report", "sendWeeklySummary")
    .addSeparator()
    .addItem("Install Weekly Auto-Report", "installWeeklyTrigger")
    .addItem("Remove All Triggers", "removeTriggers")
    .addToUi();
}

// ============================================================
// CONFIGURATION — edit these to match your sheet
// ============================================================
var CONFIG = {
  sheetName: "Labor Yield Tracker",
  targetYield: 1000,            // DA/hr — your minimum threshold
  dataStartRow: 5,              // first row of data
  dataEndRow: 24,               // last row of data
  colDate: 1,                   // A
  colProject: 2,                // B
  colEstHours: 3,               // C
  colActualHours: 4,            // D
  colRevenue: 5,                // E
  colYield: 6,                  // F
  colStatus: 7,                 // G
  alertEmail: Session.getActiveUser().getEmail(),  // sends to you
};

// ============================================================
// CHECK YIELD ALERTS — flags any entry below target
// ============================================================
function checkYieldAlerts() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.sheetName);
  if (!sheet) {
    SpreadsheetApp.getUi().alert("Sheet '" + CONFIG.sheetName + "' not found.");
    return;
  }

  var data = sheet.getRange(
    CONFIG.dataStartRow, CONFIG.colDate,
    CONFIG.dataEndRow - CONFIG.dataStartRow + 1,
    CONFIG.colStatus - CONFIG.colDate + 1
  ).getValues();

  var alerts = [];
  var lowYieldCount = 0;

  for (var i = 0; i < data.length; i++) {
    var row = data[i];
    var rowNum = CONFIG.dataStartRow + i;
    var project = row[CONFIG.colProject - 1];
    var actualHours = row[CONFIG.colActualHours - 1];
    var revenue = row[CONFIG.colRevenue - 1];
    var yieldVal = row[CONFIG.colYield - 1];

    // Skip empty rows
    if (!project || !actualHours || !revenue) continue;

    if (yieldVal && yieldVal < CONFIG.targetYield) {
      lowYieldCount++;
      alerts.push(
        "⚠  " + project + "\n" +
        "   Actual Hours: " + actualHours.toFixed(1) + "\n" +
        "   Revenue: " + revenue.toFixed(0) + " DA\n" +
        "   Yield: " + yieldVal.toFixed(0) + " DA/hr\n" +
        "   Row: " + rowNum
      );

      // Update status column in sheet
      sheet.getRange(rowNum, CONFIG.colStatus).setValue("⚠ Below Target");
      sheet.getRange(rowNum, CONFIG.colStatus).setFontColor("FF0000");
    } else if (yieldVal && yieldVal >= CONFIG.targetYield) {
      sheet.getRange(rowNum, CONFIG.colStatus).setValue("✓ On Target");
      sheet.getRange(rowNum, CONFIG.colStatus).setFontColor("00AA00");
    }
  }

  // Send alert email if issues found
  if (alerts.length > 0) {
    var subject = "ITS Yield Alert — " + alerts.length + " project(s) below " + CONFIG.targetYield + " DA/hr";
    var body = "ITS LABOR YIELD ALERT\n";
    body += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";
    body += "The following projects are below your target yield of " + CONFIG.targetYield + " DA/hr:\n\n";
    body += alerts.join("\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n");
    body += "\n\nAction: Review these projects. Consider re-quoting, adjusting scope, or improving efficiency.\n";
    body += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
    body += "ITS Pricing Calculator — Automated Alert\n";

    MailApp.sendEmail(CONFIG.alertEmail, subject, body);
    SpreadsheetApp.getUi().alert("Found " + alerts.length + " issue(s). Email alert sent to " + CONFIG.alertEmail);
  } else {
    SpreadsheetApp.getUi().alert("All " + CONFIG.targetYield + " DA/hr+ — no alerts needed.");
  }
}

// ============================================================
// WEEKLY SUMMARY — sends a report of the week's activity
// ============================================================
function sendWeeklySummary() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.sheetName);
  if (!sheet) {
    SpreadsheetApp.getUi().alert("Sheet '" + CONFIG.sheetName + "' not found.");
    return;
  }

  var data = sheet.getRange(
    CONFIG.dataStartRow, CONFIG.colDate,
    CONFIG.dataEndRow - CONFIG.dataStartRow + 1,
    CONFIG.colStatus - CONFIG.colDate + 1
  ).getValues();

  var totalProjects = 0;
  var totalRevenue = 0;
  var totalHours = 0;
  var belowTargetCount = 0;
  var onTargetCount = 0;

  for (var i = 0; i < data.length; i++) {
    var row = data[i];
    var project = row[CONFIG.colProject - 1];
    var actualHours = row[CONFIG.colActualHours - 1];
    var revenue = row[CONFIG.colRevenue - 1];
    var yieldVal = row[CONFIG.colYield - 1];

    if (!project || !actualHours || !revenue) continue;

    totalProjects++;
    totalRevenue += revenue;
    totalHours += actualHours;

    if (yieldVal && yieldVal >= CONFIG.targetYield) {
      onTargetCount++;
    } else if (yieldVal) {
      belowTargetCount++;
    }
  }

  var avgYield = totalHours > 0 ? totalRevenue / totalHours : 0;
  var date = new Date();

  var subject = "ITS Weekly Yield Summary — " + Utilities.formatDate(date, Session.getScriptTimeZone(), "MMM dd");
  var body = "ITS WEEKLY YIELD SUMMARY\n";
  body += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";
  body += "Period: Week ending " + Utilities.formatDate(date, Session.getScriptTimeZone(), "MMMM dd, yyyy") + "\n";
  body += "Generated: " + Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm") + "\n\n";
  body += "━━━ OVERVIEW ━━━━━━━━━━━━━━━━━━━\n";
  body += "  Total Projects Tracked:  " + totalProjects + "\n";
  body += "  Total Revenue:           " + totalRevenue.toFixed(0) + " DA\n";
  body += "  Total Actual Hours:      " + totalHours.toFixed(1) + " hrs\n";
  body += "  Average Yield:           " + avgYield.toFixed(0) + " DA/hr\n\n";
  body += "  ✓ On Target (>=" + CONFIG.targetYield + "): " + onTargetCount + "\n";
  body += "  ⚠ Below Target:         " + belowTargetCount + "\n\n";

  // Recommendation
  body += "━━━ RECOMMENDATION ━━━━━━━━━━━━━━━\n";
  if (avgYield < CONFIG.targetYield) {
    body += "  ⚠ Your average yield is below target.\n";
    body += "  → Review pricing on fixed projects\n";
    body += "  → Check if hours are over-running estimates\n";
    body += "  → Consider scope-change billing\n";
  } else {
    body += "  ✓ Average yield is healthy at " + avgYield.toFixed(0) + " DA/hr.\n";
    if (belowTargetCount > 0) {
      body += "  → " + belowTargetCount + " project(s) need attention\n";
    }
  }

  body += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
  body += "ITS Pricing Calculator — Automated Report\n";

  MailApp.sendEmail(CONFIG.alertEmail, subject, body);

  // Show confirmation in sheet
  var ui = SpreadsheetApp.getUi();
  if (ui) {
    ui.alert("Weekly summary sent to " + CONFIG.alertEmail);
  }
}

// ============================================================
// TRIGGER SETUP — weekly auto-report
// ============================================================
function installWeeklyTrigger() {
  removeTriggers();

  ScriptApp.newTrigger("sendWeeklySummary")
    .timeBased()
    .everyWeeks(1)
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(8)
    .create();

  SpreadsheetApp.getUi().alert(
    "✅ Weekly report installed.\n\n" +
    "You'll receive an email every Monday at 8:00 AM.\n" +
    "To change day/time: Edit → Triggers (clock icon)"
  );
}

function removeTriggers() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
}
