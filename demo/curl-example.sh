# Simula un inbound email webhook
curl -X POST http://localhost:8000/webhook/email \          -H 'Content-Type: application/json' \          -H 'X-WEBHOOK-SECRET: changeme_secret' \          -d '{
    "message_id": "demo-1",
    "from_email": "client@example.com",
    "subject": "Order inquiry",
    "body": "Hola, quiero saber precios",
    "received_at": "2025-11-15T12:00:00Z"
}'
