import httpx
import asyncio
import json
import pytest

API_URL = "https://privacy-sentinel-api.onrender.com/api/summarize"

# Extracted key points from the OpenAI Cookie Policy PDF (visual analysis)
POLICY_SNIPPET = """
OpenAI Cookie Policy - Last updated: February 2, 2026.
OpenAI uses cookies for:
1. Necessary cookies: Required to operate services (authentication, security).
2. Analytics cookies: Understand service usage.
3. Marketing cookies: Support marketing efforts.
Manage Cookies: Users can reject non-essential cookies.
Types of cookies include _puid (7 days), _uasid (1 day), _account (session), oai-sc (1 year), etc.
Third-party cookies: We use third-party services like Google Analytics and Intercom which may set their own cookies.
"""

@pytest.mark.asyncio
async def test_policy_analysis():
    print("Testing Privacy Sentinel AI Engine with OpenAI Cookie Policy...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                API_URL,
                json={
                    "snippet": POLICY_SNIPPET,
                    "source_url": "https://openai.com/policies/cookie-policy"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print("\n--- Analysis Result ---")
                print(f"Risk Score: {data.get('risk_score')}/100")
                print(f"Summary: {data.get('summary')}")
                print("-----------------------\n")
            else:
                print(f"Error: Received status code {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_policy_analysis())
