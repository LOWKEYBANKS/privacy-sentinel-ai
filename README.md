# 🛡️ Privacy Sentinel AI

AI-powered privacy policy analysis platform that helps users understand data collection practices before they click "Accept."

## 🌟 Overview

Privacy Sentinel AI is an open-source platform designed to analyze, summarize, and rate privacy policies. It leverages AI to identify what data is collected, shared, or monetized, providing users with a clear risk assessment.

The project follows a **privacy-by-design** approach, optimized for local or self-hosted operation to ensure user data remains private.

## ✨ Key Features (Vision)

- 🤖 **AI-Powered Analysis** — Uses Mistral / LLaMA family models for policy decoding.
- 🔒 **Privacy-First** — Local inference support with zero personal data collection.
- 📊 **Risk Scoring** — 0-100 privacy risk scale for policy transparency.
- 💬 **Explainable Summaries** — AI-generated summaries with highlighted concerning clauses.
- 🌐 **Cross-Platform (Roadmap)** — Future support for browser extensions, desktop, and mobile apps.

## 📦 Current Repository Status (Phase 0)

This repository currently contains the **core backend and scraping foundation**:

- `agent/` — FastAPI backend for privacy analysis and risk scoring.
- `scrapers/` — Python-based web scrapers and policy detectors.
- `database/` — PostgreSQL schema for audit logging and risk assessment.
- `docker-compose.yml` — Multi-service stack for local development.

> **Note:** The broader product modules (Desktop app, Mobile app, and actual Browser Extension) are part of the roadmap and are not yet implemented in this repository.

## 🧩 Repository Structure

```text
.
├── agent/               # FastAPI backend & AI analysis engine
├── scrapers/            # Python-based policy detection & extraction
├── database/            # PostgreSQL bootstrap SQL
├── nginx/               # Nginx reverse-proxy config
├── docker-compose.yml   # Local orchestration
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

3. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

### API Endpoints

- **FastAPI Health Check:** `http://localhost:8000/health`
- **Analysis API:** `POST http://localhost:8000/api/summarize`
- **Risk Catalog:** `GET http://localhost:8000/api/risks/catalog`

## 🔍 Example Use Case

1. A user provides a URL or a snippet of a privacy policy.
2. The `scrapers` module extracts the relevant legal text.
3. The `agent` analyzes the text and flags risks like "location tracking" or "biometric data collection."
4. The user receives a risk score (e.g., 72/100) and a summary of concerns.

## 💡 Roadmap

- [ ] Integration with local LLMs (Ollama/LocalAI)
- [ ] Policy crawling + ingestion pipeline
- [ ] User dashboard for score history
- [ ] Actual Browser Extension (Chrome/Firefox)
- [ ] Mobile SDK for Android/iOS
- [ ] Hosted + self-hosted deployment options

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
