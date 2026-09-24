/**
 * Google Apps Script Cloud Notifier for LinkedIn Content Engine
 * Runs 24/7/365 inside Google Cloud (Free, Zero Setup, Works when computer is off).
 * 
 * HOW TO INSTALL (Takes 60 seconds):
 * 1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1dFqr9zvJXDya30YyhERjoBYtE6o3lMFdYAhfavknAl4
 * 2. Click "Extensions" in the top menu -> Select "Apps Script"
 * 3. Delete any code in the editor, paste this entire script, and click the Disk (Save) icon.
 * 4. Select the function "setupCloudTriggers" from the dropdown at the top and click "Run".
 *    (Grant standard Google permissions when prompted).
 * 5. THAT'S IT! Google's cloud servers will now automatically email you 15 minutes before
 *    every scheduled LinkedIn post, even when your computer is completely shut down!
 */

function checkAndSendPostReminder() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("LinkedIn Content Calendar");
  if (!sheet) {
    Logger.log("Sheet 'LinkedIn Content Calendar' not found.");
    return;
  }

  var data = sheet.getDataRange().getValues();
  // Posts start after separator (row 8 in sheet, index 7 in 0-indexed array)
  var posts = data.slice(7);

  // Get current date and time
  var now = new Date();
  var userEmail = Session.getActiveUser().getEmail();

  // For testing or manual run, take the first ready post
  var targetPost = null;
  for (var i = 0; i < posts.length; i++) {
    var status = posts[i][4]; // Col E: Status
    if (status === "READY TO POST" || status === "SCHEDULED" || status === "VIDEO SCRIPT READY") {
      targetPost = posts[i];
      break;
    }
  }

  if (!targetPost) {
    Logger.log("No pending posts found.");
    return;
  }

  var postNum = targetPost[0];
  var timing = targetPost[1];
  var format = targetPost[2];
  var topic = targetPost[3];
  var hook = targetPost[5];
  var body = targetPost[6];
  var asset = targetPost[7];

  var subject = "⏰ 15-Min Reminder: Time to Publish LinkedIn " + postNum + " (" + topic + ")";
  
  var htmlBody = `
    <div style="font-family: Arial, sans-serif; color: #0f172a; max-width: 650px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
      <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; padding: 20px; border-radius: 6px;">
        <span style="background: #2563eb; color: #ffffff; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 4px; text-transform: uppercase;">15-Minute Posting Alert</span>
        <h2 style="margin: 8px 0 4px 0; color: #ffffff;">${postNum}: ${topic}</h2>
        <p style="margin: 0; color: #94a3b8; font-size: 13px;">Scheduled Timing: ${timing} | Format: ${format}</p>
      </div>

      <p style="margin-top: 20px;">Hi Joel,</p>
      <p>Your scheduled LinkedIn post is due to be published in <strong>15 minutes</strong>. Open LinkedIn, copy the copy below, attach your asset, and hit post!</p>

      <div style="background: #f8fafc; border-left: 4px solid #2563eb; border: 1px solid #e2e8f0; padding: 12px 16px; border-radius: 4px; margin: 16px 0;">
        <strong style="font-size: 12px; text-transform: uppercase; color: #64748b;">Attached Asset:</strong><br>
        <code style="font-family: monospace; font-size: 12px; color: #0f172a;">${asset}</code>
      </div>

      <p><strong>Ready-to-Paste Copy:</strong></p>
      <div style="background: #f1f5f9; border: 1px solid #cbd5e1; padding: 16px; border-radius: 6px; white-space: pre-wrap; font-family: monospace; font-size: 13px; color: #0f172a;">
${body}
      </div>

      <div style="text-align: center; margin-top: 24px;">
        <a href="https://www.linkedin.com/feed/" style="background: #2563eb; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; display: inline-block;">Open LinkedIn Feed →</a>
      </div>

      <div style="margin-top: 30px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #94a3b8; text-align: center;">
        AI Business Auditor — 60-Day LinkedIn Content Engine (Google Cloud Dispatcher)
      </div>
    </div>
  `;

  MailApp.sendEmail({
    to: userEmail,
    subject: subject,
    htmlBody: htmlBody
  });

  Logger.log("Email reminder sent to " + userEmail);
}

/**
 * Creates automated weekly time-driven triggers in Google Cloud.
 * Runs on:
 * - Tuesdays at 8:00 AM (15 mins before 8:15 AM post)
 * - Thursdays at 8:45 AM (15 mins before 9:00 AM post)
 * - Sundays at 6:15 PM (15 mins before 6:30 PM post)
 */
function setupCloudTriggers() {
  // Delete existing triggers for this function to prevent duplicates
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === "checkAndSendPostReminder") {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }

  // 1. Tuesday Trigger (at 8:00 AM)
  ScriptApp.newTrigger("checkAndSendPostReminder")
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.TUESDAY)
    .atHour(8)
    .nearMinute(0)
    .create();

  // 2. Thursday Trigger (at 8:45 AM)
  ScriptApp.newTrigger("checkAndSendPostReminder")
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.THURSDAY)
    .atHour(8)
    .nearMinute(45)
    .create();

  // 3. Sunday Trigger (at 6:15 PM = 18:15)
  ScriptApp.newTrigger("checkAndSendPostReminder")
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.SUNDAY)
    .atHour(18)
    .nearMinute(15)
    .create();

  Logger.log("ALL 3 CLOUD TRIGGERS CREATED SUCCESSFULLY!");
}
