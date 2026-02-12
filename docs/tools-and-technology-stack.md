# 🛠️ Privacy Sentinel AI - Open Source Tools & Technology Stack

> **Last Updated:** 2026-02-12  
> **Version:** 1.1.0  
> **Status:** Production-Ready with Professional Standards

---

## ⚠️ **Licenses & Usage Considerations**

| Tool | License | Usage Caveats | Commercial Use |
|------|---------|---------------|----------------|
| [PyScript](https://pyscript.net/) | Apache 2.0 | Enables Python in the browser via WebAssembly | Yes |
| [Ollama](https://ollama.ai/) | Apache 2.0 | Free serveware, check model licenses separately | Yes |
| [Mistral 7B](https://mistral.ai/) | Apache 2.0 | Free for commercial use | Yes |
| [LLaMA 3](https://llama.meta.com/) | Llama 3 Community License | Free but requires Meta permission for >700M users | Yes (with terms) |
| [Unstructured.io](https://unstructured.io/) | Apache 2.0 | Open source core, commercial features exist | Yes |
| [n8n](https://n8n.io/) | Apache 2.0 | Self-hosted is free, cloud has pricing | Yes (self-hosted) |
| [JustlyAI LMSS](https://github.com/JustlyAI/lmss_entity_extractor) | MIT | Completely free | Yes |
| [Label Studio](https://labelstud.io/) | Apache 2.0 | Free self-hosted, cloud has limits | Yes (self-hosted) |

> **Note:** This is not a legal compliance analysis. Consult with legal counsel for production use.

---

## 🏗️ **Core Infrastructure**

### **Container & Deployment**
- [Docker](https://www.docker.com/) - **(In Use)** Container platform for all services
- [Docker Compose](https://docs.docker.com/compose/) - **(In Use)** Multi-service orchestration for local development
- [GitHub Actions](https://github.com/features/actions) - **(In Use)** CI/CD pipeline automation
- [Render.com](https://render.com/) - **(In Use)** Cloud platform for production deployment

### **Database & Storage**
- [PostgreSQL](https://www.postgresql.org/) - **(In Use)** Primary relational database
- [MinIO](https://min.io/) / S3 - **(Planned)** File storage for documents and media
- [Redis](https://redis.io/) - **(In Use)** Caching layer for fast responses

---

## 🕷️ **Web Discovery & Extraction (Pure Python Strategy)**

### **Web Crawling & Browser Automation**
- [Playwright](https://playwright.dev/) - **(Planned)** Primary tool for backend scraping of dynamic, JavaScript-heavy websites.
- **Note:** Non-Python tools like `Crawlee (Node.js)` and `Colly (Go)` are explicitly **avoided** to maintain the pure Python ecosystem.

### **Document Processing**
- [Trafilatura](https://trafilatura.readthedocs.io/) - **(Next Step)** To be integrated as the primary tool for robust text and metadata extraction from web pages.
- [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/) - **(In Use)** Currently used for basic HTML parsing within the PyScript browser extension.
- [Apache Tika](https://tika.apache.org/) - **(Planned)** For universal document parsing (PDF, DOCX, etc.) in the backend.
- [Unstructured.io](https://unstructured.io/) - **(Planned)** For advanced document parsing and ML-powered chunking.
- [JustlyAI LMSS Entity Extractor](https://github.com/JustlyAI/lmss_entity_extractor) - **(Planned)** For advanced legal semantic classification.

---

## 🤖 **AI & Machine Learning**

### **Model Inference**
- [Ollama](https://ollama.ai/) - **(Planned)** For local LLM serving, fulfilling the privacy-first requirement.
- [Mistral 7B](https://mistral.ai/news/mistral-7b) / [LLaMA 3](https://llama.meta.com/) - **(Planned)** Primary open-source models for local analysis via Ollama.

### **Cloud API Alternatives**
- [OpenAI API](https://openai.com/api/) - **(In Use)** GPT-4o-mini is used for the current production backend on Render.com.

---

## 🌐 **Frontend & User Interfaces**

### **Browser Extension (Pure Python)**
- [PyScript](https://pyscript.net/) - **(In Use)** Core technology enabling the use of Python for the browser extension, avoiding JavaScript.
- [Manifest V3](https://developer.chrome.com/docs/extensions/mv3/intro/) - **(In Use)** The extension is packaged using the modern browser standard.
- [Chrome/Firefox/Safari WebExtensions API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions) - **(In Use)** Interacting with native browser functions via PyScript.

### **Mobile Applications**
- [Flutter](https://flutter.dev/) - **(Planned)** Cross-platform framework for the mobile UI (iOS + Android).
- [Android Accessibility Services](https://developer.android.com/guide/topics/ui/accessibility/services) / [iOS Screen Time API](https://developer.apple.com/documentation/screen_time) - **(Planned)** For system-level background monitoring.

---

## 🛣️ **Implementation Status & Priority**

### **Phase 0 & 1 (Foundation & MVP) - COMPLETED** ✅

- [x] **Core API:** FastAPI + PostgreSQL backend is live on Render.com.
- [x] **Containerization:** Docker Compose is configured for local development.
- [x] **CI/CD:** GitHub Actions pipeline is operational with automated tests.
- [x] **Cloud LLM:** OpenAI GPT-4o-mini is integrated for production analysis.
- [x] **Browser Extension:** A functional PyScript-based extension exists for real-time analysis.
- [x] **Risk Scoring:** A sophisticated risk scoring algorithm is implemented.
- [x] **Legal Intelligence:** GDPR, CCPA, and HIPAA knowledge base is integrated.
- [x] **Multi-language Support:** The system can analyze policies in multiple languages.

### **Phase 2 (Intelligence & Extraction) - Current Focus**

- [ ] **Advanced Extraction:** Integrate **Trafilatura** and **Playwright** into the backend for superior data extraction.
- [ ] **Local LLM Integration:** Implement **Ollama** with **Mistral 7B** as a user-selectable option for private, local inference.
- [ ] **Semantic Search:** Integrate **JustlyAI LMSS** for deeper legal entity extraction.
- [ ] **User Dashboard:** Build a Python-based dashboard for users to view their history.

### **Phase 3 (Scale & Platform Growth) - Future**

- [ ] **Mobile App:** Develop the **Flutter**-based mobile application for iOS and Android.
- [ ] **Subscription System:** Implement the $1/month subscription model with Stripe/LemonSqueezy.
- [ ] **Automated Workflows:** Use **n8n** for advanced workflow automation.
- [ ] **Vector Database:** Implement **Milvus** or **ChromaDB** for a full-fledged RAG system.
- [ ] **Monitoring:** Set up **Prometheus** and **Grafana** for enterprise-grade observability.
