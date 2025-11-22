# Google Apps Script Version (Lite)

This is a "Serverless" version of the automation. It runs entirely within your Google Account, costing $0 and requiring no external hosting (Docker/Python).

## Use Case
Best for personal use, small businesses, or low-volume workflows (under 500 emails/day).

## Setup Instructions

1. **Open your Google Sheet.**
2. Go to **Extensions > Apps Script**.
3. Clear the default code and paste the content of `Code.gs`.
4. Edit the `CONFIG` object at the top of the file:
   - `SEARCH_QUERY`: The filter for emails (e.g., `label:orders is:unread`).
   - `SHEET_NAME`: The name of the tab to write to.
5. Save the project (Floppy disk icon).
6. Run the `setup()` function once:
   - Click the dropdown menu (Select function) -> `setup`.
   - Click **Run**.
   - Accept the Google Permissions dialog (Review Permissions -> Allow).
7. **Automate it:**
   - Click the **Clock icon** (Triggers) on the left sidebar.
   - Click **+ Add Trigger**.
   - Function: `checkGmail`.
   - Event Source: `Time-driven`.
   - Type: `Minutes timer` -> `Every 10 minutes`.
   - Save.

Done! The script will now wake up every 10 minutes, check for emails matching your query, and log them to the sheet.