import os
import time
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# SCOPES: Permissions to read/modify Gmail and write to Sheets
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_credentials():
    """
    Handles Google API authentication.
    Priority 1: Service Account (Best for server/cloud deployment).
    Priority 2: OAuth User Token (Best for local testing without SA).
    """
    # 1. Try Service Account (from file defined in ENV or default name)
    sa_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON', 'service-account.json')
    if os.path.exists(sa_path):
        return service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    
    # 2. Try OAuth User Token (generated via local flow)
    if os.path.exists('token.json'):
        return Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # No credentials found
    print("⚠️ Warning: No valid credentials found (service-account.json or token.json). Check .env")
    return None

def fetch_unread_emails(query='is:unread label:INBOX'):
    """
    Fetches unread emails from Gmail, extracts key fields, 
    and removes the 'UNREAD' label to prevent processing duplicates.
    """
    creds = get_credentials()
    if not creds:
        return []

    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # List messages (max 10 per batch to avoid rate limits)
        results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
        messages = results.get('messages', [])
        
        email_data = []
        if not messages:
            return []

        print(f"🔎 Found {len(messages)} new emails...")

        for msg in messages:
            # Get full message details
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload.get('headers', [])
            
            # Safe header extraction
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown)')
            # Use email date or fallback to current time
            email_date = next((h['value'] for h in headers if h['name'] == 'Date'), time.strftime('%Y-%m-%d %H:%M:%S'))
            
            # Get body snippet (short summary shown in inbox)
            body = txt.get('snippet', '')

            email_data.append({
                'received_at': email_date,
                'from_email': sender,
                'subject': subject,
                'body': body
            })

            # Mark as read (Remove UNREAD label)
            service.users().messages().modify(
                userId='me', 
                id=msg['id'], 
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
        return email_data

    except Exception as e:
        print(f"❌ Error fetching Gmail: {e}")
        return []

def append_row_to_sheet(row_data):
    """
    Appends a single row of data to the configured Google Sheet.
    """
    creds = get_credentials()
    if not creds:
        return False

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet_id = os.getenv('SHEET_ID')
        range_name = os.getenv('SHEET_RANGE', 'Sheet1!A1')
        
        if not sheet_id:
            print("⚠️ SHEET_ID not set in environment variables.")
            return False

        # Map dictionary to row list
        values = [[
            row_data.get('received_at'),
            row_data.get('from_email'),
            row_data.get('subject'),
            row_data.get('body')
        ]]
        
        body = {'values': values}
        
        service.spreadsheets().values().append(
            spreadsheetId=sheet_id, 
            range=range_name, 
            valueInputOption='RAW', 
            insertDataOption='INSERT_ROWS', 
            body=body
        ).execute()
        return True
    except Exception as e:
        print(f"❌ Error writing to Sheet: {e}")
        return False