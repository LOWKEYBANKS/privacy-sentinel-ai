# Changelog

## v1.0.0 - 2026-02-12

### Added
- **Real AI Model Integration:** Implemented OpenAI GPT-4o-mini for production analysis with a dual-mode system (production/development).
- **Specialized Legal Knowledge Base:** Integrated GDPR, CCPA, and HIPAA compliance detection with multi-language support.
- **Alembic Database Migrations:** Set up Alembic for robust PostgreSQL schema management.
- **Automated Testing Suite:** Created comprehensive `pytest` suite for API endpoints and functionality.
- **PyScript-based Browser Extension:** Developed a pure Python browser extension (`browser-agent/`) running in the browser via WebAssembly.
- **Cloud Deployment:** Successfully deployed to Render.com with a live API at `https://privacy-sentinel-api.onrender.com`.
- **CI/CD Pipeline:** Configured GitHub Actions for automated testing and deployment (all tests passing).
- **Redis Caching:** Integrated Redis for improved performance and scalability.

### Changed
- **Directory Structure:** Renamed `browser-extension/` to `scrapers/` for clarity and consistency.
- **API Syntax & Encoding:** Fixed critical API syntax errors and encoding issues in `agent/api/summarizer.py`.
- **Browser Extension Connection:** Updated the browser extension to connect to the live Render API.

### Fixed
- All critical bugs, including syntax errors, dependency conflicts, and Docker build issues.

### Removed
- Problematic `lexnlp` dependency from `requirements.txt`.
