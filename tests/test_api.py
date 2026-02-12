import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add agent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agent'))
from api.summarizer import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_privacy_policy_basic():
    """Test basic privacy policy analysis"""
    payload = {
        "snippet": "We collect your email and location data for marketing purposes.",
        "timestamp": "2026-02-10T09:00:00Z"
    }
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "summary" in data
    # In development mode, risks should be detected from the snippet
    assert len(data["risks"]) > 0

def test_analyze_privacy_policy_too_long():
    """Test that overly long snippets are rejected"""
    long_snippet = "A" * 20000
    payload = {
        "snippet": long_snippet
    }
    response = client.post("/api/summarize", json=payload)
    assert response.status_code == 422 # Pydantic validation error
