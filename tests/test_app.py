import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

# FastAPI test client
client = TestClient(app)

def test_health_endpoint():
    """
    Verifies that the health endpoint responds correctly
    and reflects the polling configuration state.
    """
    # Simulate polling disabled for this test
    with patch.dict(os.environ, {"ENABLE_GMAIL_POLLING": "false"}):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "active"
        assert data["mode"] == "webhook-only"

def test_webhook_missing_secret():
    """
    Should fail with 403 if we don't send the correct X-WEBHOOK-SECRET header.
    """
    payload = {"subject": "Test"}
    response = client.post("/webhook/email", json=payload)
    assert response.status_code == 403
    assert "Invalid webhook secret" in response.text

@patch("app.main.append_row_to_sheet")
def test_webhook_success(mock_append):
    """
    Should process the payload and call the function that writes to Sheets.
    We mock 'append_row_to_sheet' to avoid hitting the real Google API.
    """
    # Simulate successful Sheets write (True)
    mock_append.return_value = True
    
    secret = "test_secret_123"
    payload = {
        "received_at": "2025-01-01",
        "from_email": "test@example.com",
        "subject": "New Order",
        "body": "Details here"
    }

    # Set the secret in the environment to match the request
    with patch.dict(os.environ, {"WEBHOOK_SECRET": secret}):
        response = client.post(
            "/webhook/email",
            json=payload,
            headers={"X-WEBHOOK-SECRET": secret}
        )

        # Assertions
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # Verify that the business logic was called with the correct data
        mock_append.assert_called_once()
        called_args = mock_append.call_args[0][0]
        assert called_args["subject"] == "New Order"
        assert called_args["from_email"] == "test@example.com"
