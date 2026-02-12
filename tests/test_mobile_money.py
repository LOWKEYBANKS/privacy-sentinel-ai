import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add agent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agent'))
from api.summarizer import app

client = TestClient(app)

def test_initiate_mobile_money():
    """Test initiating a mobile money payment."""
    payload = {
        "phone_number": "254700000000",
        "network": "M-PESA",
        "currency": "KES"
    }
    # Using query params as defined in the route
    response = client.post(f"/api/subscription/mobile-money/initiate?phone_number={payload['phone_number']}&network={payload['network']}&currency={payload['currency']}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "transaction_id" in data
    assert "STK Push sent" in data["message"]

def test_flutterwave_webhook_success():
    """Test the Flutterwave webhook for successful payment."""
    # 1. Initiate to get a transaction ID
    init_resp = client.post("/api/subscription/mobile-money/initiate?phone_number=254700000000")
    tx_id = init_resp.json()["transaction_id"]
    
    # 2. Simulate webhook
    webhook_payload = {
        "status": "successful",
        "tx_ref": tx_id,
        "amount": 130.0,
        "currency": "KES"
    }
    response = client.post("/api/subscription/flutterwave/webhook", json=webhook_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # 3. Check subscription status
    status_resp = client.get("/api/subscription/status")
    assert status_resp.json()["is_subscribed"] is True
    assert status_resp.json()["subscription_level"] == "pro"
