import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from .services import fetch_unread_emails, append_row_to_sheet

# Load environment variables
load_dotenv()

# Configuration
POLLING_INTERVAL = 60  # Seconds between Gmail checks
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'changeme_secret')

async def gmail_poller():
    """
    Background task that runs in an infinite loop.
    It checks for new emails if ENABLE_GMAIL_POLLING is set to true in .env.
    """
    print("⏳ Gmail Polling Service initialized...")
    while True:
        # Check if polling is enabled in environment
        is_enabled = os.getenv('ENABLE_GMAIL_POLLING', 'false').lower() == 'true'
        
        if is_enabled:
            try:
                # Fetch emails using logic from services.py
                emails = fetch_unread_emails()
                if emails:
                    for email in emails:
                        success = append_row_to_sheet(email)
                        status = "✅ Saved" if success else "❌ Failed"
                        print(f"{status}: {email['subject'][:30]}...")
            except Exception as e:
                print(f"❌ Error in polling loop: {e}")
        
        # Wait before next check
        await asyncio.sleep(POLLING_INTERVAL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifecycle Manager.
    Starts the background poller when the app starts.
    """
    # Startup: Create background task
    task = asyncio.create_task(gmail_poller())
    yield
    # Shutdown: Task will be cancelled automatically when main process stops

# Initialize FastAPI with lifespan
app = FastAPI(title='Gmail -> Sheets Automation', lifespan=lifespan)

@app.get('/health')
async def health():
    """
    Health check endpoint.
    Returns the current status and polling configuration.
    """
    polling_status = os.getenv('ENABLE_GMAIL_POLLING', 'false').lower()
    return { 
        'status': 'active', 
        'polling_enabled': polling_status == 'true'
    }

@app.post('/webhook/email')
async def email_webhook(payload: dict, request: Request):
    """
    Optional Webhook Endpoint.
    Allows pushing data manually or from external services (e.g., SendGrid, Postman).
    """
    # Verify Secret Header
    secret = request.headers.get('X-WEBHOOK-SECRET') or request.query_params.get('secret')
    if secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail='Invalid webhook secret')

    # Normalize payload to match our internal structure
    data = {
        'received_at': payload.get('received_at', ''),
        'from_email': payload.get('from_email', ''),
        'subject': payload.get('subject', ''),
        'body': payload.get('body', '')
    }

    # Save to Sheet
    success = append_row_to_sheet(data)
    
    return { 
        'success': success, 
        'message': 'Data processed',
        'data': data 
    }