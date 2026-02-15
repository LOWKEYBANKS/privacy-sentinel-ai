# Changelog

## [1.3.0] - 2026-02-15

### **Added**
- **100% Pure Python Ecosystem:** Successfully eliminated all JavaScript, Kotlin, and C++ source artifacts from the project logic.
- **Proactive Mobile Monitoring:** Implemented a background service for Android using **PyJNIus** to interface with Accessibility APIs directly from Python.
- **PyScript Integration:** Stabilized the browser extension to run 100% Python logic via WebAssembly, enabling proactive scanning of privacy policies.
- **Python-Native n8n Workflows:** Replaced JavaScript hash nodes with Python-based nodes in the `policy_monitor` workflow.
- **Subscription Engine:** Added backend support for $1/month Proactive Mode with Stripe and Flutterwave integrations.

### **Fixed**
- **GitHub Actions CI/CD:** Resolved `pytest-asyncio` configuration issues and added missing dependencies to the pipeline.
- **Module Imports:** Fixed relative import issues and added missing `__init__.py` files to ensure project-wide package stability.
- **Language Statistics:** Purged `.buildozer` and other non-Python build artifacts to ensure GitHub correctly identifies the project as Pure Python.

### **Changed**
- **Documentation:** Completely overhauled the `Tools and Technology Stack` and `Mobile Background Logic` docs to reflect the pure Python architecture.
- **Deployment:** Optimized `render.yaml` for high-performance Python deployment on Render.com.

## v1.0.0 - 2026-02-12

### Added
- **Mobile Money Integration:** Implemented a flexible payment gateway supporting M-Pesa and other mobile wallets via Flutterwave for $1/month subscriptions.
- **Proactive "Interception" Flow:** Enhanced browser extension and mobile background service to proactively detect and analyze policies before user acceptance.
- **Python-Native Mobile Strategy:** Developed a 100% Python mobile app core using Kivy and python-for-android for background monitoring.
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
- Native Kotlin/Android code to maintain a **100% Pure Python Ecosystem**.
