import pytest
from fastapi.testclient import TestClient
from web_scanner.main import app
from web_scanner.summarizer import PolicySummarizer
import asyncio

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_summarizer_mock():
    summarizer = PolicySummarizer()
    text = "This is a test policy. It has multiple sentences. We collect data."
    result = await summarizer.summarize_text(text)
    
    assert result["summary"] is not None
    assert "error" not in result
    assert result["original_length"] == len(text)

@pytest.mark.asyncio
async def test_summarizer_empty():
    summarizer = PolicySummarizer()
    result = await summarizer.summarize_text("")
    assert result["error"] == "No text provided"

# Note: Integration tests for /scan would require mocking the WebPrivacyScanner
# which involves network calls. For Phase 0, we focus on unit tests.
