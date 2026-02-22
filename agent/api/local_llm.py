"""
Privacy Sentinel AI - Local LLM Support
Integration with Ollama for offline and private analysis.
"""

import os
import json
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)

class LocalLLMClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = os.getenv("LOCAL_LLM_MODEL", "llama3")

    async def analyze_text(self, prompt: str, system_prompt: str) -> Optional[dict]:
        """Send a request to the local Ollama instance."""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": system_prompt,
                        "stream": False,
                        "format": "json"
                    }
                )
                response.raise_for_status()
                result = response.json()
                return json.loads(result.get("response", "{}"))
        except Exception as e:
            logger.error(f"Local LLM Analysis failed: {e}")
            return None

def is_local_llm_available() -> bool:
    """Check if the local LLM mode is enabled via environment variables."""
    return os.getenv("LLM_MODE") == "local"
