# 🛡️ Privacy Sentinel AI

AI-powered privacy protection platform that intercepts data collection practices across Desktop and Mobile.

**Created and maintained by [LOWKEYBANKS](https://github.com/LOWKEYBANKS) and Partner Lorrah.**

## 🚀 Dual-Platform Strategy

### 💻 Desktop: The Web Extension
The Desktop Web Extension (Chrome, Firefox, Opera, etc.) is built using **PyScript** and our **Pure Python Stack**. It operates as a robust, background-scanning tool that automatically analyzes every site you visit.
- **Automated Scanning**: Analyzes policies using the backend AI as soon as a page loads.
- **Full Transparency**: Provides detailed risk scores and summaries directly in the extension popup.
- **Pure Python**: Leverages the open-source stack (FastAPI, Trafilatura, Playwright) for reliable analysis.

### 📱 Mobile: Proactive Interception (Phone/Tablet/iPad)
The Mobile experience is designed for **interception**. Using Android Accessibility Services, it monitors your browsing in the background and triggers a **real-time popup** before you interact with a site.
- **Background Interception**: Detects when you land on a new site and scans it instantly.
- **Decision Support**: The popup tells you exactly what to do—**"Accept Non-Essentials"** or **"Reject All"**—before you click the site's own consent buttons.
- **Sustainable Protection**: This proactive monitoring is available for a **$1/month subscription**, ensuring high-quality AI analysis remains affordable and privacy-focused.

## 🏗️ Technical Status
- **Backend**: Live on Render.com (FastAPI + PostgreSQL + Redis).
- **Web Extension**: MVP Complete and optimized for background auto-scanning.
- **Mobile Background Service**: Logic implemented for URL interception and popup triggering.
- **Subscription Engine**: Mock activation and status check logic integrated into the API.

## 🛠️ Getting Started
1. **Desktop**: Load the `browser-agent/` folder into your browser in Developer Mode.
2. **Mobile**: The Flutter/Android logic is located in the `mobile/` directory, ready for compilation.
3. **Backend**: Access the live API at `https://privacy-sentinel-api.onrender.com`.

---
Empowering you to make informed privacy decisions **before** you click "Accept."
