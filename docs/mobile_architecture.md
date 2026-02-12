# Mobile/Tablet Architecture: Proactive Privacy Monitoring

This document outlines the architectural strategy for extending Privacy Sentinel AI to mobile phones and tablets, ensuring proactive privacy monitoring in the background while maintaining a pure Python core for intelligence.

## 1. Core Principles

-   **Pure Python Core:** The intelligence engine (analysis, risk scoring, legal compliance) remains entirely in Python, leveraging the existing FastAPI backend.
-   **Cross-Platform UI:** Utilize Flutter for a single codebase to build native-looking applications for both Android and iOS.
-   **Background Monitoring:** Implement system-level services to detect and analyze privacy policies of applications and websites in real-time.
-   **API-Driven:** Mobile clients will communicate with the existing FastAPI backend for policy analysis and data synchronization.

## 2. Technology Stack Alignment

Based on the `tools-and-technology-stack.md`:

| Category | Official Tool | Role in Mobile Architecture |
| :--- | :--- | :--- |
| **Frontend & UI** | `Flutter` | **Primary UI Framework.** Will be used to build the user-facing application for both Android and iOS, providing a consistent and performant experience. |
| **Backend & Logic** | `FastAPI` | **Core Intelligence Hub.** The mobile apps will send extracted policy data to the existing FastAPI backend for AI analysis, risk scoring, and legal compliance checks. |
| **Background Tasks (Android)** | `Android Accessibility Services` | **Proactive Monitoring.** Will be used to monitor app usage, detect privacy policy URLs, and potentially extract content from within apps or webviews. |
| **Background Tasks (iOS)** | `iOS Screen Time API` | **Proactive Monitoring.** Will be explored for monitoring app usage and web activity to identify privacy policies. Due to Apple's stricter sandboxing, this may require creative solutions or user permissions. |
| **Communication** | `WebSockets` / `Webhooks` | For real-time updates and notifications from the backend to the mobile application. |
| **Notifications** | `Android Foreground Services` / `Native OS Notifications` | To provide persistent, user-friendly alerts about privacy risks detected in the background. |

## 3. Architectural Components

### 3.1. Flutter Mobile Application (UI Layer)

-   **User Interface:** Built with Flutter, providing a clean and intuitive interface for users to:
    -   View real-time privacy scores and summaries.
    -   Access historical analysis data (from the User Dashboard).
    -   Configure monitoring preferences.
    -   Receive notifications and alerts.
-   **Platform Channels:** Flutter will use platform channels to communicate with native Android/iOS code for accessing system-level features (e.g., Accessibility Services, Screen Time API).
-   **API Client:** A Python-generated client (e.g., using `openapi-python-client`) or a custom HTTP client will interact with the FastAPI backend.

### 3.2. Native Background Services (Android & iOS)

#### Android
-   **Accessibility Service:** A dedicated Android Accessibility Service will run in the background to:
    -   Detect when new applications are opened or web pages are loaded.
    -   Identify potential privacy policy URLs or consent dialogs.
    -   Extract visible text content or URLs to be sent to the Python core for analysis.
-   **Foreground Service:** For persistent background operation and user awareness, a Foreground Service will be utilized, displaying a continuous notification.

#### iOS
-   **Screen Time API:** Investigation into using the Screen Time API to monitor web activity and app usage for privacy policy detection. This approach will be more constrained by Apple's privacy policies.
-   **Network Extension (VPN):** As an alternative, a local VPN-like network extension could be explored to intercept and analyze network traffic for policy URLs, sending relevant data to the Python core.

### 3.3. Python Core (Backend Intelligence)

-   **FastAPI Backend:** The existing FastAPI application will serve as the central processing unit for all mobile clients.
    -   Receives extracted text/URLs from mobile devices.
    -   Performs AI-powered analysis, risk scoring, and legal compliance checks.
    -   Stores analysis results in PostgreSQL.
    -   Sends back privacy scores, summaries, and recommended actions.
-   **Trafilatura/Playwright:** The backend will utilize these tools for robust content extraction if only a URL is provided by the mobile client, ensuring comprehensive analysis.

## 4. Workflow for Proactive Monitoring

1.  User installs the Privacy Sentinel mobile app.
2.  User grants necessary permissions (e.g., Accessibility Service on Android, Screen Time on iOS).
3.  The native background service continuously monitors app usage and web browsing.
4.  Upon detecting a new app launch or website visit, the service identifies potential privacy policy links or consent dialogs.
5.  The relevant text or URL is sent to the FastAPI backend.
6.  The FastAPI backend processes the data using AI and returns a privacy score and summary.
7.  The mobile app receives the analysis and displays a discreet, real-time notification or overlay to the user, informing them of the privacy risk *before* they proceed.

This architecture ensures that Privacy Sentinel AI provides robust, real-time privacy protection across mobile devices, fully leveraging your pure Python backend and adhering to your specified open-source tool stack.
