"""
Privacy Sentinel AI - Core API
Production-ready privacy policy analysis with specialized legal intelligence,
granular risk scoring, and multi-language support.
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
from langdetect import detect, DetectorFactory

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Import specialized legal knowledge
from knowledge.legal_frameworks import LEGAL_FRAMEWORKS

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
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434/v1")
client = None

if llm_mode == "production":
    client = OpenAI()
elif llm_mode == "local":
    # Use OpenAI client pointed to Ollama's local API
    client = OpenAI(base_url=ollama_base_url, api_key="ollama")

app = FastAPI(
    title="Privacy Sentinel AI", 
    version="1.3.0",
    description="AI-powered privacy policy analysis with specialized legal intelligence and multi-language support"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"), 
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

class RiskBreakdown(BaseModel):
    data_collection: int
    third_party_sharing: int
    user_rights: int
    data_retention: int

class PrivacyAnalysisResponse(BaseModel):
    summary: str
    risk_score: int
    risk_breakdown: RiskBreakdown
    risks: List[str]
    legal_violations: List[str]
    detected_language: str
    recommended_action: str
    hash_id: str
    analysis_timestamp: str
    processing_time_ms: float

# AI Analysis Logic
async def perform_specialized_analysis(text: str, language: str) -> dict:
    """Perform specialized legal analysis using LLM and the Knowledge Base."""
    if llm_mode == "production" and client:
        try:
            knowledge_context = json.dumps(LEGAL_FRAMEWORKS, indent=2)
            
            prompt = f"""
            You are a specialized Privacy Legal Expert. Analyze the following privacy policy snippet (Language: {language}).
            
            Use this Legal Knowledge Base for reference:
            {knowledge_context}
            
            Provide a JSON response with:
            1. 'summary': A professional 2-sentence summary of privacy implications.
            2. 'risk_score': An overall integer from 0-100.
            3. 'risk_breakdown': {{'data_collection': 0-100, 'third_party_sharing': 0-100, 'user_rights': 0-100, 'data_retention': 0-100}}
            4. 'risks': A list of specific risk categories.
            5. 'legal_violations': A list of potential violations against GDPR, CCPA, or HIPAA.
            6. 'recommended_action': Clear, actionable advice for the user.

            Snippet: {text[:4000]}
            """
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "system", "content": "You are a Privacy Sentinel AI specialized in global data regulations."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Specialized LLM Analysis failed: {e}")
    
    # Local / Fallback Mode
    if llm_mode == "local" and client:
        try:
            knowledge_context = json.dumps(LEGAL_FRAMEWORKS, indent=2)
            prompt = f"""
            You are a specialized Privacy Legal Expert. Analyze the following privacy policy snippet.
            Use this Legal Knowledge Base for reference: {knowledge_context}
            Provide a JSON response with summary, risk_score, risk_breakdown, risks, legal_violations, and recommended_action.
            Snippet: {text[:4000]}
            """
            response = client.chat.completions.create(
                model=os.getenv("OLLAMA_MODEL", "mistral"),
                messages=[{"role": "system", "content": "You are a Privacy Sentinel AI."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Local Ollama Analysis failed: {e}")

    risks = detect_privacy_risks_fallback(text)
    score = calculate_risk_score_fallback(risks)
    return {
        "summary": "Development mode analysis. Specialized legal intelligence is inactive.",
        "risk_score": score,
        "risk_breakdown": {
            "data_collection": score,
            "third_party_sharing": score // 2,
            "user_rights": 50,
            "data_retention": 30
        },
        "risks": risks,
        "legal_violations": ["Specialized analysis requires production mode"],
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
        # Detect language
        try:
            detected_lang = detect(request.snippet)
        except:
            detected_lang = "unknown"
            
        analysis = await perform_specialized_analysis(request.snippet, detected_lang)
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        background_tasks.add_task(
            log_analysis_result, content_hash, analysis['risk_score'], 
            len(analysis['risks']), http_request.client.host
        )
        
        return PrivacyAnalysisResponse(
            summary=analysis['summary'],
            risk_score=analysis['risk_score'],
            risk_breakdown=analysis.get('risk_breakdown', {
                "data_collection": 0, "third_party_sharing": 0, "user_rights": 0, "data_retention": 0
            }),
            risks=analysis['risks'],
            legal_violations=analysis.get('legal_violations', []),
            detected_language=detected_lang,
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
    return {"status": "healthy", "version": "1.3.0", "llm_mode": llm_mode}

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
        # In mock/dev mode, don't fail the whole request if DB is down
        if os.getenv("LLM_MODE") == "mock":
            logger.warning("Continuing without audit log in mock mode")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("summarizer:app", host="0.0.0.0", port=8000, reload=True)
