"""
Privacy Sentinel AI - Core API
Production-ready privacy policy analysis with LLM integration
"""

import hashlib
import logging
import json
import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import psycopg2
from psycopg2.extras import RealDictCursor
from openai import OpenAI

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('privacy_sentinel.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Security configuration
class SecurityConfig:
    MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", 16000))
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 100))
    REQUIRE_ENCRYPTION = os.getenv("REQUIRE_ENCRYPTION", "True") == "True"

# LLM Client Setup
llm_mode = os.getenv("LLM_MODE", "development")
client = None
if llm_mode == "production":
    # Uses environment variables OPENAI_API_KEY and OPENAI_BASE_URL if provided
    client = OpenAI()

app = FastAPI(
    title="Privacy Sentinel AI", 
    version="1.1.0",
    description="AI-powered privacy policy analysis"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "privacy_sentinel"),
            user=os.getenv("DB_USER", "dev"),
            password=os.getenv("DB_PASSWORD", "dev"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Request/Response Models
class PrivacyAnalysisRequest(BaseModel):
    source_url: Optional[str] = None
    snippet: str
    timestamp: Optional[str] = None
    
    @field_validator('snippet')
    @classmethod
    def validate_snippet(cls, v):
        if len(v) > SecurityConfig.MAX_TEXT_LENGTH:
            raise ValueError(f"Text too long (max {SecurityConfig.MAX_TEXT_LENGTH} chars)")
        return v

class PrivacyAnalysisResponse(BaseModel):
    summary: str
    risk_score: int
    risks: List[str]
    recommended_action: str
    hash_id: str
    analysis_timestamp: str
    processing_time_ms: float

# AI Analysis Logic
async def perform_ai_analysis(text: str) -> dict:
    """Perform analysis using LLM or fallback to keyword matching"""
    if llm_mode == "production" and client:
        try:
            prompt = f"""
            Analyze the following privacy policy snippet and provide a JSON response with:
            1. 'summary': A 2-sentence professional summary of privacy implications.
            2. 'risk_score': An integer from 0-100 (higher is riskier).
            3. 'risks': A list of specific risk categories found (e.g., 'location_tracking', 'data_sharing').
            4. 'recommended_action': A short advice for the user.

            Snippet: {text[:4000]}
            """
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"LLM Analysis failed, falling back to keywords: {e}")
    
    # Fallback / Development Mode
    risks = detect_privacy_risks_fallback(text)
    score = calculate_risk_score_fallback(risks)
    return {
        "summary": "Development mode analysis based on keyword detection.",
        "risk_score": score,
        "risks": risks,
        "recommended_action": "Review manually as this is a development-level assessment."
    }

def detect_privacy_risks_fallback(text: str) -> List[str]:
    risk_keywords = {
        "email": "email_collection", "location": "location_tracking", 
        "biometric": "biometric_data", "voice": "voice_data",
        "third party": "data_sharing", "advertising": "marketing_data"
    }
    text_lower = text.lower()
    return list(set([risk for kw, risk in risk_keywords.items() if kw in text_lower]))

def calculate_risk_score_fallback(risks: List[str]) -> int:
    return min(100, len(risks) * 15 + 10) if risks else 5

# API Endpoints
@app.post("/api/summarize", response_model=PrivacyAnalysisResponse)
async def analyze_privacy_policy(request: PrivacyAnalysisRequest, background_tasks: BackgroundTasks, http_request: Request):
    start_time = datetime.now()
    content_hash = hashlib.sha256(request.snippet.encode('utf-8')).hexdigest()[:16]
    
    try:
        analysis = await perform_ai_analysis(request.snippet)
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        background_tasks.add_task(
            log_analysis_result, content_hash, analysis['risk_score'], 
            len(analysis['risks']), http_request.client.host
        )
        
        return PrivacyAnalysisResponse(
            summary=analysis['summary'],
            risk_score=analysis['risk_score'],
            risks=analysis['risks'],
            recommended_action=analysis['recommended_action'],
            hash_id=content_hash,
            analysis_timestamp=datetime.now().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.1.0", "llm_mode": llm_mode}

async def log_analysis_result(content_hash: str, risk_score: int, risk_count: int, client_ip: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_audit_log (content_hash, risk_score, risk_count, client_ip, timestamp) 
            VALUES (%s, %s, %s, %s, %s)
        """, (content_hash, risk_score, risk_count, client_ip, datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Audit log failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("summarizer:app", host="0.0.0.0", port=8000, reload=True)
