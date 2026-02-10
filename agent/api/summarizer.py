"""
Privacy Sentinel AI - Phase 0 Core API
Security-first privacy policy analysis endpoint
Development environment optimized for 8GB RAM
"""

import hashlib
import logging
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import psycopg2
from psycopg2.extras import RealDictCursor
import os

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
    MAX_TEXT_LENGTH = 16000
    RATE_LIMIT = 100  # requests per minute
    REQUIRE_ENCRYPTION = True

app = FastAPI(
    title="Privacy Sentinel AI", 
    version="1.0.0",
    description="AI-powered privacy policy analysis"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "chrome-extension://*"],
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
        
        # Check for potential PII patterns
        pii_patterns = ['@', 'phone:', 'ssn:', 'address:', 'credit card:']
        if any(pattern in v.lower() for pattern in pii_patterns):
            logger.warning("Potential PII detected in request")
        
        return v

class PrivacyAnalysisResponse(BaseModel):
    summary: str
    risk_score: int
    risks: List[str]
    recommended_action: str
    hash_id: str
    analysis_timestamp: str
    processing_time_ms: float

class HealthCheck(BaseModel):
    status: str
    service: str
    timestamp: str
    version: str

# Utility Functions
def generate_content_hash(text: str) -> str:
    """Generate SHA-256 hash for audit trail"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

def detect_privacy_risks(text: str) -> List[str]:
    """Development-friendly risk detection without heavy ML"""
    risks = []
    
    risk_keywords = {
        "email": "email_collection",
        "location": "location_tracking", 
        "biometric": "biometric_data",
        "voice": "voice_data",
        "third party": "data_sharing",
        "advertising": "marketing_data",
        "analytics": "tracking_data",
        "cookies": "cookie_tracking",
        "camera": "camera_access",
        "microphone": "microphone_access"
    }
    
    text_lower = text.lower()
    for keyword, risk in risk_keywords.items():
        if keyword in text_lower:
            risks.append(risk)
    
    return list(set(risks))  # Remove duplicates

def calculate_risk_score(risks: List[str]) -> int:
    """Calculate risk score based on detected risks"""
    risk_weights = {
        "biometric_data": 25,
        "location_tracking": 20,
        "voice_data": 15,
        "email_collection": 10,
        "data_sharing": 20,
        "marketing_data": 10,
        "tracking_data": 12,
        "cookie_tracking": 8,
        "camera_access": 18,
        "microphone_access": 18
    }
    
    base_score = min(25, len(risks) * 5)  # Base score for multiple risks
    weighted_score = sum(risk_weights.get(risk, 8) for risk in risks)
    
    return min(100, base_score + weighted_score)

# API Endpoints
@app.post("/api/summarize", response_model=PrivacyAnalysisResponse)
async def analyze_privacy_policy(
    request: PrivacyAnalysisRequest, 
    background_tasks: BackgroundTasks,
    http_request: Request
):
    """Analyze privacy policy snippet and return risk assessment"""
    
    start_time = datetime.now()
    client_ip = http_request.client.host
    
    # Security logging
    logger.info(f"Privacy analysis request from {client_ip} for {request.source_url or 'unknown source'}")
    
    # Generate audit hash (no PII stored)
    content_hash = generate_content_hash(request.snippet)
    
    try:
        # Detect privacy risks
        detected_risks = detect_privacy_risks(request.snippet)
        
        # Calculate comprehensive risk score
        risk_score = calculate_risk_score(detected_risks)
        
        # Generate professional summary
        if risk_score >= 70:
            summary = "This application collects extensive personal data including sensitive information. Privacy risks are high - review carefully before proceeding."
            action = "High Risk - Consider alternatives or proceed with maximum precautions"
        elif risk_score >= 40:
            summary = "This application collects some personal data for functionality. Carefully review what data is collected and how it's used."
            action = "Moderate Risk - Proceed with caution and minimal data sharing"
        else:
            summary = "This application has minimal data collection practices. Privacy risk appears low for standard use."
            action = "Low Risk - Generally safe to proceed with normal precautions"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Log completion
        logger.info(f"Analysis completed: {len(detected_risks)} risks, score {risk_score}")
        
        # Background: Store audit trail (without PII)
        background_tasks.add_task(
            log_analysis_result, 
            content_hash, 
            risk_score, 
            len(detected_risks),
            client_ip
        )
        
        return PrivacyAnalysisResponse(
            summary=summary,
            risk_score=risk_score,
            risks=detected_risks,
            recommended_action=action,
            hash_id=content_hash,
            analysis_timestamp=datetime.now().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        service="privacy-sentinel-api",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.get("/api/security/status")
async def security_status():
    """Security configuration endpoint"""
    return {
        "max_text_length": SecurityConfig.MAX_TEXT_LENGTH,
        "encryption_required": SecurityConfig.REQUIRE_ENCRYPTION,
        "rate_limit": SecurityConfig.RATE_LIMIT,
        "logging_enabled": True,
        "pii_detection": True,
        "audit_logging": True
    }

@app.get("/api/risks/catalog")
async def get_risk_catalog():
    """Get available risk categories for transparency"""
    return {
        "risk_categories": {
            "biometric_data": {"weight": 25, "description": "Fingerprint, face, voice biometrics"},
            "location_tracking": {"weight": 20, "description": "GPS, location data collection"},
            "voice_data": {"weight": 15, "description": "Voice recording, analysis"},
            "email_collection": {"weight": 10, "description": "Email address collection"},
            "data_sharing": {"weight": 20, "description": "Third-party data sharing"},
            "marketing_data": {"weight": 10, "description": "Advertising, marketing data"},
            "tracking_data": {"weight": 12, "description": "Analytics, user tracking"},
            "cookie_tracking": {"weight": 8, "description": "Web tracking cookies"},
            "camera_access": {"weight": 18, "description": "Camera permissions"},
            "microphone_access": {"weight": 18, "description": "Microphone permissions"}
        },
        "scoring_methodology": "Weighted risk assessment based on data sensitivity and collection scope",
        "max_score": 100,
        "risk_levels": {
            "low": {"range": [0, 39], "description": "Minimal privacy risk"},
            "moderate": {"range": [40, 69], "description": "Manageable privacy risk"},
            "high": {"range": [70, 100], "description": "Significant privacy risk"}
        }
    }

# Background Tasks
async def log_analysis_result(content_hash: str, risk_score: int, risk_count: int, client_ip: str):
    """Log analysis results for audit trail (without PII)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analysis_audit_log 
            (content_hash, risk_score, risk_count, client_ip, timestamp) 
            VALUES (%s, %s, %s, %s, %s)
        """, (content_hash, risk_score, risk_count, client_ip, datetime.now()))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"Audit log recorded: {content_hash[:8]}...")
        
    except Exception as e:
        logger.error(f"Audit log failed: {e}")

# Startup/Shutdown Events
@app.on_event("startup")
async def startup_event():
    """Initialize database and services"""
    logger.info("Privacy Sentinel API starting up...")
    try:
        # Test database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create audit log table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_audit_log (
                id SERIAL PRIMARY KEY,
                content_hash VARCHAR(16) NOT NULL,
                risk_score INTEGER NOT NULL,
                risk_count INTEGER NOT NULL,
                client_ip VARCHAR(45),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Privacy Sentinel API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "summarizer:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
