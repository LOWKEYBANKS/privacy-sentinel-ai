# 🛠️ Phase 0 Development Setup

> **Privacy Sentinel AI - Security-first privacy analysis platform**  
> **Version:** 1.0.0 | **Branch:** summarizer-py-(phase-0-implementation)

---

## 🚀 Quick Start

### Prerequisites
- **Docker** & **Docker Compose** (latest versions)
- **Git** version control
- **8GB+ RAM, 4+ CPU cores** (development optimized)
- **PostgreSQL client** (optional, for direct database access)

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/LOWKEYBANKS/privacy-sentinel-ai.git
cd privacy-sentinel-ai

# Switch to Phase 0 implementation branch
git checkout summarizer-py-(phase-0-implementation)

# Start development environment
docker-compose up -d

# Verify API health
curl http://localhost:8000/health

# View development logs
docker-compose logs -f fastapi

🌐 API Documentation
Core Endpoints
Privacy Policy Analysis
Bash

curl -X POST "http://localhost:8000/api/summarize" \
-H "Content-Type: application/json" \
-d '{
  "source_url": "https://example.com/privacy",
  "snippet": "We collect your email address, location data, and share with third parties for advertising purposes.",
  "timestamp": "2025-01-01T12:00:00Z"
}'
__CODE_BLOCK_PLACEHOLDER_2json
{
  "summary": "This application collects extensive personal data including sensitive information. Privacy risks are high - review carefully before proceeding.",
  "risk_score": 85,
  "risks": ["email_collection", "location_tracking", "data_sharing"],
  "recommended_action": "High Risk - Consider alternatives or proceed with maximum precautions",
  "hash_id": "a1b2c3d4",
  "analysis_timestamp": "2025-01-01T12:00:01.000Z",
  "processing_time_ms": 245.67
}
System Health
Bash

curl http://localhost:8000/health
Security Configuration
Bash

curl http://localhost:8000/api/security/status
Risk Category Reference
Bash

curl http://localhost:8000/api/risks/catalog
🏗️ Architecture Overview
Service Architecture
text

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Browser Extension│───►│ FastAPI Backend │───►│ PostgreSQL DB   │
│ (JavaScript)    │    │ (Python)        │    │ (Audit Logging) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Redis Cache     │
                       │ (Performance)   │
                       └─────────────────┘
Data Flow

Browser Extension detects privacy policies on web pages
FastAPI API receives and validates requests
Risk Analysis processes text without storing PII
PostgreSQL stores audit logs with content hashes
Redis provides caching for improved performance

🔧 Development Services
Service Configuration


Service	Port	Purpose	Dependencies
fastapi	8000	Core API server	PostgreSQL, Redis
postgres	5432	Primary database	None
redis	6379	Caching layer	None
nginx	80	Reverse proxy (optional)	FastAPI
Environment Variables
Bash

# Database Configuration
DATABASE_URL=postgresql://dev:dev@postgres:5432/privacy_sentinel
DB_HOST=localhost
DB_NAME=privacy_sentinel
DB_USER=dev
DB_PASSWORD=dev

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Development Settings
LLM_MODE=development
LOG_LEVEL=info
🧪 Development & Testing
Running Tests
Bash

# Run all tests
docker-compose exec fastapi pytest

# Run with coverage
docker-compose exec fastapi pytest --cov=api --cov-report=html

# Run specific test file
docker-compose exec fastapi pytest tests/test_api.py
Manual Testing
Bash

# Test privacy analysis with sample data
curl -X POST "http://localhost:8000/api/summarize" \
-H "Content-Type: application/json" \
-d '{"snippet": "We collect email addresses and location data for personalized advertising."}'

# Test error handling
curl -X POST "http://localhost:8000/api/summarize" \
-H "Content-Type: application/json" \
-d '{"snippet": ""}'  # Should return validation error
🗄️ Database Management
Database Administration
Bash

# Connect to PostgreSQL
docker-compose exec postgres psql -U dev -d privacy_sentinel

# View audit logs (last 10 entries)
SELECT * FROM analysis_audit_log 
ORDER BY timestamp DESC 
LIMIT 10;

# Check system performance metrics
SELECT endpoint, COUNT(*) as request_count, AVG(processing_time_ms) as avg_time
FROM api_metrics 
WHERE timestamp >= NOW() - INTERVAL '1 hour'
GROUP BY endpoint;

# Verify database schema
\d analysis_audit_log
\d risk_types
\d system_config
Database Backup/Restore
Bash

# Backup database
docker-compose exec postgres pg_dump -U dev privacy_sentinel > backup.sql

# Restore database (if needed)
docker-compose exec -T postgres psql -U dev privacy_sentinel < backup.sql

🔒 Security Features
Built-in Security
✅ Input Validation: All requests validated before processing
✅ PII Detection: Personal indicators detected and logged (not stored)
✅ Rate Limiting: 100 requests per minute per IP
✅ Audit Trails: Complete request/response logging (content hashed)
✅ CORS Protection: Configured for browser extension access
✅ HTTPS Enforcement: Production requires TLS encryption

Risk Assessment Algorithm
Python

# Scoring Methodology

                    
ƒ
BASE SCORE

                 = len(risks) * 5         # Multiple risks increase base score

                    
ƒ
WEIGHTED SCORE

                 = Σ(risk_weights[risk]) # Weighted by sensitivity

                    
ƒ
FINAL SCORE

                 = min(100, 
                    
ƒ
BASE SCORE

                 + 
                    
ƒ
WEIGHTED SCORE

                )

Risk Categories
High Risk (70-100): Biometric data, extensive data sharing
Moderate Risk (40-69): Location tracking, email collection
Low Risk (0-39): Minimal data collection, clear policies

📊 Monitoring & Analytics
Performance Monitoring

Bash

# API response times
docker-compose exec fastapi curl -s http://localhost:8000/health | jq

# Docker resource usage
docker stats

# Application logs
docker-compose logs -f fastapi | grep ERROR
Health Checks
Bash

# All services healthy?
docker-compose ps

# Database connection
docker-compose exec postgres pg_isready -U dev -d privacy_sentinel

# Redis connection
docker-compose exec redis redis-cli ping
Development Metrics
API Response Time: Target < 500ms for analysis requests
Database Query Performance: < 100ms for audit log inserts
Memory Usage: < 2GB total for development stack
CPU Usage: < 50% under normal load

🌍 Browser Extension Testing
Extension Development
Open Chrome: Navigate to chrome://extensions/
Developer Mode: Enable in top-right
Load Extension: Click "Load unpacked" → Select browser-extension/
Test: Visit sites with privacy policies (google.com, facebook.com)
Extension Debugging
JavaScript

// Browser console debugging
window.privacySentinel  // Access detector object

// Check last analysis
chrome.storage.local.get(['lastAnalysis'], (result) => {
    console.log('Last analysis:', result.lastAnalysis);
});
🚀 Deployment Guide
Production Prerequisites
16GB+ RAM: For full production workloads
PostgreSQL 13+: Production database version
Docker Swarm/K8s: Container orchestration
SSL/TLS: HTTPS certification required
Production Configuration
Bash

# Environment variables for production
LLM_MODE=production          # Use local Ollama models
RATE_LIMIT=1000             # Higher limit for production
LOG_LEVEL=warning           # Production logging level
ENCRYPTION_REQUIRED=true    # Enforce HTTPS
Health Endpoints
Bash

# Production health check
curl https://api.privacysentinel.ai/health

# Security status verification
curl https://api.privacysentinel.ai/api/security/status
🔄 CI/CD Pipeline
GitHub Actions (Planned)
Testing: Automated test suite on PR
Security: Dependency scanning and vulnerability checks
Deployment: Automatic deployment to staging environment
Performance: Load testing for API endpoints
Development Workflow
Feature Branch: Create from summarizer-py-(phase-0-implementation)
Development: Build and test locally with Docker
PR Creation: Submit to development branch
Code Review: Security and architecture review
Merge: Integrate into main branch

📚 Phase 0 Scope & Limitations
Phase 0 Capabilities
✅ Privacy policy detection: JavaScript browser extension
✅ Risk assessment: Keyword-based scoring algorithm
✅ Audit logging: Hashed content logging (no PII)
✅ RESTful API: Professional FastAPI backend
✅ Development environment: Docker-compose setup

Phase 0 Limitations
❌ Advanced ML: No local LLM inference (development mode)
❌ Vector search: No semantic similarity matching
❌ Mobile apps: No native iOS/Android support
❌ Production scaling: Not load-tested for enterprise

🎯 Phase 1 Roadmap (Next Implementation)
Planned Features
Local LLM Integration: Ollama with Mistral 7B model
Advanced Legal Processing: LexNLP deep semantic analysis
Vector Database: Milvus for semantic search
Automation Workflows: n8n integration for policy monitoring
Mobile SDKs: Flutter cross-platform applications
Technical Upgrades
Performance: Caching layer with Redis optimization
Security: JWT authentication and API key management
Monitoring: Prometheus metrics + Grafana dashboards
Scalability: Horizontal scaling with load balancer

🤝 Contributing Guidelines
Code Standards
Python: Follow PEP 8, use type hints, document with docstrings
Security: Always validate inputs, never store PII, audit all endpoints
Testing: Write unit tests for new features, maintain 80%+ coverage
Documentation: Update this README for API changes
Reporting Issues
Security Issues: Email maintainers directly (do not open public issues)
Bugs: Use GitHub Issues with reproduction steps
Feature Requests: Open issue with technical requirements
Questions: Participate in GitHub Discussions

📞 Support & Communication
Development Team
Lead Developer: @LOWKEYBANKS
Project Lead: @Ms-Lorrah
Contact Information
Technical Issues: Create GitHub Issue
Security Concerns: Private communication channel
Project Questions: GitHub Discussions section

🔍 Technical Specifications
API Performance Targets
Response Time: < 500ms for privacy analysis
Throughput: 100+ requests/minute (development mode)
Availability: 99.9% uptime target
Memory Usage: < 2GB per container
Database Specifications
Schema Version: 1.0.0
Audit Retention: 90 days maximum
Max Text Length: 16,000 characters per analysis
Hash Algorithm: SHA-256 (truncated to 16 chars)
Security Requirements
Encryption: AES-256 at rest, TLS 1.3 in transit
Authentication: API key authentication (Phase 1+)
Authorization: Role-based access control (Phase 1+)
Compliance: GDPR/CCPA privacy framework compliance

🎯 Success Metrics
Phase 0 Success Criteria
✅ API Functionality: All endpoints responsive and documented
✅ Security Standards: Input validation and audit logging active
✅ Performance: Sub-second response times for analysis
✅ Development Environment: Ready-to-use Docker setup
✅ Documentation: Complete developer onboarding guide

Quality Metrics
Code Coverage: 80%+ test coverage (target)
Security Score: 0 high-severity vulnerabilities
Documentation: 100% API endpoint documentation
Performance: < 500ms average response time

📈 Monitoring Dashboard
Development Metrics
Request Volume: Number of API calls per hour
Response Time: Average API response time
Error Rate: Percentage of failed requests
Database Performance: Query execution times
Memory Usage: Container resource utilization

Health Checks
Bash

# Comprehensive health check
curl -s http://localhost:8000/health | jq '.'
Performance Monitoring
Bash

# Docker resource monitoring
docker stats --no-stream

🛡️ Privacy & Compliance Statement
Data Protection Principles
Privacy by Design: All architecture decisions prioritize user privacy
Minimal Data Collection: Store only what's necessary for functionality
User Control: Users maintain control over their privacy decisions
Transparency: Clear disclosure of data processing practices

Compliance Framework
GDPR Ready: Full compliance with EU data protection regulations
CCPA Compliant: California consumer privacy act alignment
Data Minimization: Collect and process only essential data
Right to Erasure: Automated deletion of user traces

🛡️ Building privacy-first AI tools with enterprise-grade security and professional development practices.

🔗 Quick Reference
Essential Commands
Bash

# Start development environment
docker-compose up -d

# Stop environment
docker-compose down

# View logs
docker-compose logs -f fastapi

# Database access
docker-compose exec postgres psql -U dev -d privacy_sentinel

# Run tests
docker-compose exec fastapi pytest

Important URLs
API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/health
Redis CLI: docker-compose exec redis redis-cli
Database: postgresql://dev:dev@localhost:5432/privacy_sentinel
Version: 1.0.0
Branch: summarizer-py-(phase-0-implementation)
Last Updated: 04-12-2025
Maintainers: @LOWKEYBANKS, @Ms-Lorrah
