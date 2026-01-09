from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime

# Import scanner logic
try:
    from web_scanner.detector import WebPrivacyScanner
except ImportError:
    # Fallback for local development or different path structure
    try:
        from .detector import WebPrivacyScanner
    except ImportError:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))
        from web_scanner.detector import WebPrivacyScanner

app = FastAPI(
    title="Privacy Sentinel AI API",
    description="Backend API for Privacy Sentinel AI Web Scanner and Extension",
    version="0.1.0"
)

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:3000",  # Example frontend
    "*" # Allow all for now, tighten for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    url: str

class ScanResponse(BaseModel):
    url: str
    scan_id: str
    status: str
    timestamp: datetime
    results: Optional[dict] = None

@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/scan", response_model=ScanResponse)
async def scan_url(request: ScanRequest):
    """
    Scan a URL for privacy policies and risks.
    """
    try:
        async with WebPrivacyScanner() as scanner:
            results = await scanner.scan_website_privacy(request.url)
            
        return {
            "url": request.url,
            "scan_id": f"scan_{int(datetime.now().timestamp())}",
            "status": "completed",
            "timestamp": datetime.now(),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
