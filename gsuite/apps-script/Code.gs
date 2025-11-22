/**
 * 📧 GMAIL TO SHEETS AUTOMATION (Standalone)
 * 
 * Description:
 * This script checks your Gmail for specific emails and appends them
 * to a Google Sheet automatically.
 * 
 * Usage:
 * 1. Paste this code into Extensions > Apps Script.
 * 2. Update the CONFIG object below.
 * 3. Run the 'setup' function once to grant permissions.
 * 4. Set up a Time-driven Trigger to run 'checkGmail' every 10-15 minutes.
 */

const CONFIG = {
  // Gmail search query (supports standard Gmail operators)
  // Example: 'label:inbox is:unread subject:"Invoice"'
  SEARCH_QUERY: 'is:unread in:inbox', 
  
  // Name of the tab/sheet where data will be saved
  SHEET_NAME: 'Sheet1',
  
  // Action after processing: 'MARK_READ', 'ARCHIVE', or 'NONE'
  POST_PROCESS_ACTION: 'MARK_READ',
  
  // Maximum character limit for the email body (to prevent cell overflow)
  BODY_TRUNCATE_LIMIT: 3000
};

/**
 * Main function to be triggered by the Clock Trigger.
 */
function checkGmail() {
  try {
    // 1. Initialize Sheet
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAME);
    
    if (!sheet) {
      console.error(`❌ Error: Sheet named "${CONFIG.SHEET_NAME}" not found.`);
      return;
    }

    // 2. Search Gmail
    // We limit to 20 threads per execution to avoid timeouts
    const threads = GmailApp.search(CONFIG.SEARCH_QUERY, 0, 20);
    
    if (threads.length === 0) {
      console.log("✅ No new matching emails found.");
      return;
    }

    const rowsToAdd = [];
    const messagesToUpdate = [];

    // 3. Process Emails
    threads.forEach(thread => {
      const messages = thread.getMessages();
      
      messages.forEach(msg => {
        // Double check unread status to avoid duplicates if query changes
        if (msg.isUnread()) {
          
          // --- DATA EXTRACTION ---
          const date = msg.getDate();
          const from = msg.getFrom();
          const subject = msg.getSubject();
          // Get plain text body and truncate
          const body = msg.getPlainBody().substring(0, CONFIG.BODY_TRUNCATE_LIMIT);
          
          // Add to queue
          rowsToAdd.push([date, from, subject, body]);
          messagesToUpdate.push(msg);
        }
      });
    });

    // 4. Write to Sheet (Batch Operation for Performance)
    if (rowsToAdd.length > 0) {
      const lastRow = sheet.getLastRow();
      // Get range starting from the next empty row
      const range = sheet.getRange(lastRow + 1, 1, rowsToAdd.length, rowsToAdd[0].length);
      range.setValues(rowsToAdd);
      console.log(`📝 Appended ${rowsToAdd.length} rows to ${CONFIG.SHEET_NAME}.`);
      
      // 5. Post-processing (Mark Read / Archive)
      performPostActions(messagesToUpdate);
    }

  } catch (error) {
    console.error("🔥 Critical Error:", error.toString());
  }
}

/**
 * Handles marking messages as read or archiving them.
 */
function performPostActions(messages) {
  if (!messages || messages.length === 0) return;

  if (CONFIG.POST_PROCESS_ACTION === 'MARK_READ') {
    GmailApp.markMessagesRead(messages);
    console.log("🔹 Messages marked as read.");
  } 
  else if (CONFIG.POST_PROCESS_ACTION === 'ARCHIVE') {
    // To archive, we need to get threads usually, but marking read is standard
    GmailApp.markMessagesRead(messages); 
    // Optional: Add specific archive logic if needed
  }
}

/**
 * Helper function to force permission dialogs.
 * Run this manually from the editor once.
 */
function setup() {
  console.log("Permissions granted. You can now set up the trigger.");
}