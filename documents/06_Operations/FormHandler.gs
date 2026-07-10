/**
 * ITS — Contact Form Handler
 * Deploy as Web App: Deploy > New Deployment > Web App
 * Set "Execute as" = Me, "Who has access" = Anyone
 * Copy the web app URL into index.html
 */

const SHEET_ID = '1M4HERV0Fyt-wAqwCKYEm2PoezxIAW-kCdOMsg9Scp44';
const SHEET_NAME = 'Submissions';
const TO_EMAIL = 'industrialtechnologysolutions2@gmail.com';

function doPost(e) {
  try {
    const data = e.parameter;

    // Log to sheet
    const ss = SpreadsheetApp.openById(SHEET_ID);
    let sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
      sheet.appendRow(['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Service', 'Message', 'SendGuide']);
    }

    const now = new Date();
    sheet.appendRow([
      now,
      data.name || '',
      data.email || '',
      data.phone || '',
      data.company || '',
      data.service || '',
      data.message || '',
      data.sendGuide ? 'Yes' : 'No'
    ]);

    // Build email
    let subject = 'ITS Website — New Contact Form Submission';
    let body = '';
    body += 'Name: ' + (data.name || '') + '\n';
    body += 'Email: ' + (data.email || '') + '\n';
    body += 'Phone: ' + (data.phone || '') + '\n';
    body += 'Company: ' + (data.company || '') + '\n';
    body += 'Service: ' + (data.service || '') + '\n';
    body += 'Message: ' + (data.message || '') + '\n';
    body += 'Send Guide: ' + (data.sendGuide ? 'Yes' : 'No') + '\n';

    let htmlBody = '';
    htmlBody += '<h2>New Contact Form Submission</h2>';
    htmlBody += '<table style="border-collapse:collapse;width:100%">';
    const fields = [
      ['Name', data.name],
      ['Email', data.email],
      ['Phone', data.phone],
      ['Company', data.company],
      ['Service', data.service],
      ['Message', data.message],
      ['Send Guide', data.sendGuide ? 'Yes' : 'No']
    ];
    fields.forEach(function (f) {
      htmlBody += '<tr style="border:1px solid #ddd">';
      htmlBody += '<td style="padding:8px;font-weight:600;background:#f5f5f5;width:120px">' + f[0] + '</td>';
      htmlBody += '<td style="padding:8px">' + (f[1] || '') + '</td>';
      htmlBody += '</tr>';
    });
    htmlBody += '</table>';
    htmlBody += '<p style="color:#999;font-size:12px;margin-top:20px">Sent via ITS website contact form.</p>';

    GmailApp.sendEmail(TO_EMAIL, subject, body, {
      htmlBody: htmlBody,
      replyTo: data.email || TO_EMAIL
    });

    return ContentService
      .createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'running' }))
    .setMimeType(ContentService.MimeType.JSON);
}
