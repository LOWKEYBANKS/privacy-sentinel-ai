import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add agent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agent'))
from api.summarizer import app

client = TestClient(app)

def test_language_detection_spanish():
    """Test that the API correctly detects Spanish content"""
    payload = {
        "snippet": "Recopilamos su correo electrónico y datos de ubicación para fines de marketing."
    }
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 200
    assert response.json()["detected_language"] == "es"

def test_granular_risk_breakdown_exists():
    """Test that the response includes a granular risk breakdown"""
    payload = {
        "snippet": "We share your data with third parties and keep it forever."
    }
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_breakdown" in data
    assert "data_collection" in data["risk_breakdown"]
    assert "third_party_sharing" in data["risk_breakdown"]

def test_legal_violations_field_exists():
    """Test that the legal_violations field is present in the response"""
    payload = {
        "snippet": "Standard privacy policy text."
    }
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 200
    assert "legal_violations" in response.json()
