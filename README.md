# 🛡️ Privacy Sentinel AI

AI-powered privacy policy analysis platform that helps users understand data collection practices before they click "Accept."

## 🌟 Overview

Privacy Sentinel AI is an open-source platform designed to analyze, summarize, and rate privacy policies. It leverages AI to identify what data is collected, shared, or monetized, providing users with a clear risk assessment.

The project follows a **privacy-by-design** approach, optimized for local or self-hosted operation to ensure user data remains private. Our commitment to a **pure Python ecosystem** ensures consistency and avoids JavaScript "spoilage" across all components.

## ✨ Key Features (Current & Vision)

- 🤖 **AI-Powered Analysis** — Uses OpenAI GPT-4o-mini for production analysis, with a dual-mode system supporting local inference for privacy-first operations.
- 🔒 **Privacy-First** — Local inference support with zero personal data collection, upholding our privacy-by-design philosophy.
- 📊 **Risk Scoring** — Provides a 0-100 privacy risk scale for transparent policy assessment, incorporating advanced risk calculation.
- 💬 **Explainable Summaries** — AI-generated summaries with highlighted concerning clauses, now with multi-language support.
- 🌐 **Cross-Platform Accessibility** — Proactive privacy monitoring across desktop (browser extension), mobile, and tablet devices, ensuring protection before accepting policies.
- 🚀 **Production-Ready Deployment** — Live API on Render.com, backed by robust CI/CD with GitHub Actions.

## 📦 Current Repository Status (v1.0.0 - Production Ready)

This repository now contains the **fully deployed and operational core system**:

- `agent/` — FastAPI backend for privacy analysis, risk scoring, and legal compliance detection (GDPR, CCPA, HIPAA).
- `scrapers/` — Python-based web scrapers and policy detectors, now reorganized from `browser-extension/`.
- `browser-agent/` — PyScript-based browser extension logic, enabling pure Python execution in the browser via WebAssembly.
- `migrations/` — Alembic database migration scripts for PostgreSQL schema management.
- `tests/` — Comprehensive `pytest` suite for automated testing.
- `render.yaml` — Cloud deployment configuration for Render.com (web service, PostgreSQL, Redis).
- `.github/workflows/ci.yml` — GitHub Actions CI pipeline for automated testing.

> **Note:** The browser extension is fully functional but requires local installation in developer mode. Future plans include publishing to official browser stores.

## 🧩 Repository Structure

```text
.
├── agent/               # FastAPI backend & AI analysis engine
├── scrapers/            # Python-based policy detection & extraction
├── browser-agent/       # PyScript-based browser extension
├── migrations/          # Alembic database migration scripts
├── tests/               # Automated test suite
├── render.yaml          # Render.com deployment configuration
├── .github/             # GitHub Actions CI/CD workflows
├── .env.example         # Environment configuration template
├── requirements.txt     # Python dependencies
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Minimum 4GB RAM (8GB recommended for local AI models)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LOWKEYBANKS/privacy-sentinel-ai.git
   cd privacy-sentinel-ai
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your specific configuration if needed
   ```

3. **Run with Docker (for local development):**
   ```bash
   docker-compose up --build
   ```

### Live API Endpoints (Render.com)

- **Health Check:** `https://privacy-sentinel-api.onrender.com/health` (Status: Healthy)
- **Analysis API:** `POST https://privacy-sentinel-api.onrender.com/api/summarize`
- **Risk Catalog:** `GET https://privacy-sentinel-api.onrender.com/api/risks/catalog`

## 🔍 Example Use Case

1. A user navigates to a website with the Privacy Sentinel browser extension enabled.
2. The extension automatically sends the page's HTML content to the backend.
3. The `scrapers` module (now enhanced with **Playwright** for dynamic content and **Trafilatura** for robust text extraction) processes the HTML.
4. The `agent` analyzes the extracted text using AI, flags risks (e.g., "location tracking," "biometric data collection"), and detects compliance with GDPR, CCPA, and HIPAA.
5. The user receives a real-time risk score (e.g., 72/100) and a summary of concerns **before** they interact with the site, empowering informed consent.

## 💡 Roadmap (Next Steps)

- [x] **Advanced Extraction:** Integrated **Trafilatura** into the backend for superior data extraction from HTML snippets. **Playwright** is integrated into `scrapers/` for dynamic web crawling.
- [ ] **User Dashboard:** Develop a Python-based dashboard (e.g., Streamlit/Reflex) for users to view their privacy score history and track site changes.
- [ ] **Batch Analysis:** Implement a bulk URL processor for researchers/enterprise users to analyze multiple policies.
- [ ] **Local AI Integration:** Add a toggle for local LLM inference (Ollama/LocalAI) to enhance privacy-by-design.
- [ ] **Browser Extension Publishing:** Publish the PyScript browser extension to Chrome/Firefox stores.
- [ ] **Mobile/Tablet App:** Develop native mobile/tablet applications leveraging the Python core for background monitoring.
- [ ] **Subscription System:** Integrate a $1/month subscription tier for advanced features and sustainability.
- [ ] **Browser-level Opt-out Automation:** Implement automated opt-out mechanisms based on policy analysis.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-module`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push and open a Pull Request

## ⚖️ License

Licensed under the [Apache License 2.0](LICENSE).

## 🧠 Maintainers

- [@LOWKEYBANKS](https://github.com/LOWKEYBANKS)
- [@Ms-Lorrah](https://github.com/Ms-Lorrah)

---

Empowering users to make informed privacy decisions before they click “Accept.”
