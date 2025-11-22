import requests
import time
import random
import datetime

# Configuration
WEBHOOK_URL = "http://localhost:8000/webhook/email"
SECRET = "changeme_secret"  # Must match your .env

# Sample test data
SAMPLES = [
    ("client@company.com", "Invoice #1001", "Please find attached invoice."),
    ("leads@website.com", "New Lead: John Doe", "Interested in your services."),
    ("support@desk.com", "Ticket #999", "System is down, help!"),
    ("newsletter@spam.com", "Weekly Digest", "Here are the news."),
]

def send_fake_email():
    sender, subject, body = random.choice(SAMPLES)
    
    payload = {
        "received_at": datetime.datetime.now().isoformat(),
        "from_email": sender,
        "subject": f"{subject} - {random.randint(1, 100)}",
        "body": body
    }
    
    headers = {
        "X-WEBHOOK-SECRET": SECRET,
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        print(f"Sent: {subject} -> Status: {r.status_code}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    print("🚀 Starting email traffic simulation...")
    # Send 5 emails with pauses
    for _ in range(5):
        send_fake_email()
        time.sleep(1)
    print("✅ Simulation finished.")
