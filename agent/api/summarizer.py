"""
Privacy Sentinel AI - Core API
Production-ready privacy policy analysis with specialized legal intelligence,
granular risk scoring, and multi-language support.
"""

import hashlib
import logging
import json
import trafilatura
import asyncio
try:
    from scrapers.playwright_scraper import scrape_dynamic_content
except ImportError:
    try:
        from agent.scrapers.playwright_scraper import scrape_dynamic_content
    except ImportError:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from scrapers.playwright_scraper import scrape_dynamic_content
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
try:
    from knowledge.legal_frameworks import LEGAL_FRAMEWORKS
except ImportError:
    from agent.knowledge.legal_frameworks import LEGAL_FRAMEWORKS

# Local LLM Support
try:
    from .local_llm import LocalLLMClient, is_local_llm_available
except ImportError:
    from agent.api.local_llm import LocalLLMClient, is_local_llm_available

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
local_client = None

if llm_mode == "production":
    client = OpenAI()
elif llm_mode == "local":
    local_client = LocalLLMClient(base_url=os.getenv("LOCAL_LLM_URL", "http://localhost:11434"))

app = FastAPI(
    title="Privacy Sentinel AI", 
    version="1.3.2",
    description="AI-powered privacy policy analysis with specialized legal intelligence and multi-language support"
)

# Include subscription router
from . import subscription
app.include_router(subscription.router, prefix="/api")

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
    # Priority: Environment Variable -> Direct URL -> Local Dev
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Fallback to hardcoded URL if provided previously (caution: should be in env)
        db_url = "postgresql://privacy_sentinel_db_user:6UqQqF22kALSPxdUeaMw4Py3hxTdTdaM@dpg-d66jahvgi27c738uuer0-a.oregon-postgres.render.com/privacy_sentinel_db"
        
    try:
        if db_url:
            conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        else:
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
        return None

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
    cookie_summary: Optional[str] = "No specific cookie information detected."
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
    knowledge_context = json.dumps(LEGAL_FRAMEWORKS, indent=2)
    
    # Use Trafilatura to extract main content from the HTML snippet
    extracted_text = trafilatura.extract(text, output_format='text', include_comments=False, include_tables=False)
    if not extracted_text:
        extracted_text = text # Fallback to raw text if extraction fails

    system_prompt = "You are a Privacy Sentinel AI specialized in global data regulations. Analyze the following privacy policy snippet."
    prompt = f"""
    Analyze the following privacy policy snippet (Language: {language}).
    
    Use this Legal Knowledge Base for reference:
    {knowledge_context}
    
    Provide a JSON response with:
    1. 'summary': A professional 2-sentence summary of privacy implications.
    2. 'cookie_summary': A specific breakdown of cookie types used (Tracking, Marketing, Essential) and their intrusiveness.
    3. 'risk_score': An overall integer from 0-100.
    4. 'risk_breakdown': {{'data_collection': 0-100, 'third_party_sharing': 0-100, 'user_rights': 0-100, 'data_retention': 0-100}}
    5. 'risks': A list of specific risk categories.
    6. 'legal_violations': A list of potential violations against GDPR, CCPA, HIPAA, or ePrivacy (Cookie Law).
    7. 'recommended_action': Clear, actionable advice for the user.

    Snippet: {extracted_text[:4000]}
    """

    # 1. Local LLM Mode
    if llm_mode == "local" and local_client:
        logger.info("Using Local LLM for analysis.")
        analysis = await local_client.analyze_text(prompt, system_prompt)
        if analysis:
            return analysis

    # 2. Production OpenAI Mode
    if llm_mode == "production" and client:
        try:
            logger.info("Using Production OpenAI for analysis.")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Specialized LLM Analysis failed: {e}")
    
    # 3. Fallback / Development Mode
    logger.warning("Using Fallback analysis logic.")
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
        "legal_violations": ["Specialized analysis requires production or local mode"],
        "recommended_action": "Review manually as this is a development-level assessment."
    }

def detect_privacy_risks_fallback(text: str) -> List[str]:
    risk_keywords = {
        "email": "email_collection", 
        "location": "location_tracking", 
        "biometric": "biometric_data", 
        "voice": "voice_data",
        "third party": "data_sharing", 
        "advertising": "marketing_data",
        "collect": "data_collection",
        "share": "data_sharing",
        "retain": "data_retention",
        "marketing": "marketing_data"
    }
    text_lower = text.lower()
    detected = []
    for kw, risk in risk_keywords.items():
        if kw in text_lower:
            detected.append(risk)
    return list(set(detected))

def calculate_risk_score_fallback(risks: List[str]) -> int:
    return min(100, len(risks) * 15 + 10) if risks else 5

# API Endpoints
@app.post("/api/summarize", response_model=PrivacyAnalysisResponse)
async def analyze_privacy_policy(request: PrivacyAnalysisRequest, background_tasks: BackgroundTasks, http_request: Request):
    start_time = datetime.now()
    content_hash = hashlib.sha256(request.snippet.encode('utf-8')).hexdigest()[:16]
    
    try:
        # Determine content for analysis
        content_to_analyze = request.snippet
        if request.source_url:
            logger.info(f"Source URL provided: {request.source_url}. Using Playwright scraper.")
            try:
                scraped_content = await scrape_dynamic_content(request.source_url)
                if scraped_content:
                    content_to_analyze = scraped_content
                else:
                    logger.warning("Scraping returned empty content, using snippet instead.")
            except Exception as scrape_err:
                logger.warning(f"Scraping failed: {scrape_err}. Falling back to snippet.")

        # Detect language
        try:
            detected_lang = detect(content_to_analyze)
        except:
            detected_lang = "unknown"
            
        analysis = await perform_specialized_analysis(content_to_analyze, detected_lang)
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        background_tasks.add_task(
            log_analysis_result, content_hash, analysis['risk_score'], 
            len(analysis['risks']), http_request.client.host
        )
        
        return PrivacyAnalysisResponse(
            summary=analysis['summary'],
            cookie_summary=analysis.get('cookie_summary', 'No specific cookie information detected.'),
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
    return {"status": "healthy", "version": "1.3.2", "llm_mode": llm_mode}

async def log_analysis_result(content_hash: str, risk_score: int, risk_count: int, client_ip: str):
    try:
        conn = get_db_connection()
        if not conn:
            logger.warning("Skipping audit log due to missing database connection.")
            return
            
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_audit_log (
                id SERIAL PRIMARY KEY,
                content_hash VARCHAR(16),
                risk_score INTEGER,
                risk_count INTEGER,
                client_ip VARCHAR(45),
                timestamp TIMESTAMP
            )
        """)
        cursor.execute("""
            INSERT INTO analysis_audit_log (content_hash, risk_score, risk_count, client_ip, timestamp) 
            VALUES (%s, %s, %s, %s, %s)
        """, (content_hash, risk_score, risk_count, client_ip, datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Audit log failed: {e}")

# Python-Native Background Sentinel (Replacement for n8n)
async def background_sentinel_task():
    """Periodically crawls high-risk URLs to detect policy changes."""
    logger.info("Background Sentinel Task Started.")
    monitored_urls = [
        "https://www.google.com/policies/privacy/",
        "https://www.facebook.com/policy.php",
        "https://twitter.com/en/privacy",
        "https://www.tiktok.com/legal/privacy-policy"
    ]
    
    while True:
        for url in monitored_urls:
            try:
                logger.info(f"Sentinel checking: {url}")
                content = await scrape_dynamic_content(url)
                if content:
                    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
                    # Check if hash already exists in DB to detect changes
                    conn = get_db_connection()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT id FROM analysis_audit_log WHERE content_hash = %s LIMIT 1", (content_hash,))
                        exists = cursor.fetchone()
                        if not exists:
                            logger.info(f"CHANGE DETECTED in {url}. Triggering re-analysis.")
                            # Simulate analysis call
                            await perform_specialized_analysis(content, "en")
                            # Log the new state
                            await log_analysis_result(content_hash, 0, 0, "sentinel-bot")
                        cursor.close()
                        conn.close()
            except Exception as e:
                logger.error(f"Sentinel check failed for {url}: {e}")
        
        # Wait for 1 hour before next check
        await asyncio.sleep(3600)

@app.on_event("startup")
async def startup_event():
    """Start the background sentinel when the API launches."""
    asyncio.create_task(background_sentinel_task())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("summarizer:app", host="0.0.0.0", port=10000)
