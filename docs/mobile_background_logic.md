# Mobile Background Service: Pure Python Implementation (Kivy + PyJNIus)

To maintain a **100% pure Python ecosystem**, the Privacy Sentinel mobile background service is implemented using **Kivy** and **PyJNIus**. This allows us to interact with native Android APIs (like Accessibility Services) directly from Python code.

## 1. Core Logic (Python + PyJNIus)

The background monitoring logic is written in Python. It runs as an Android Service via `python-for-android`.

```python
from jnius import autoclass, cast
import time
import requests

# Android Native Classes
PythonService = autoclass('org.kivy.android.PythonService')
AccessibilityService = autoclass('android.accessibilityservice.AccessibilityService')
AccessibilityEvent = autoclass('android.view.accessibility.AccessibilityEvent')

class PrivacySentinelService:
    def __init__(self):
        self.api_url = "https://privacy-sentinel-api.onrender.com/api/summarize"
        self.last_url = ""

    def on_accessibility_event(self, event):
        # Detect URL changes in browsers
        if event.getEventType() in [AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED, 
                                   AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED]:
            
            root_node = self.get_root_node()
            url = self.find_url_in_node(root_node)
            
            if url and url != self.last_url:
                self.last_url = url
                self.analyze_privacy_background(url)

    def analyze_privacy_background(self, url):
        # 1. Check subscription via Python Requests
        if not self.is_subscribed(): return

        # 2. Trigger AI Analysis
        response = requests.post(
            self.api_url, 
            json={"source_url": url, "snippet": "Background Mobile Scan"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['risk_score'] > 70:
                self.show_python_overlay(data)

    def show_python_overlay(self, data):
        # Logic to trigger a Kivy-based "Pop Icon" overlay
        print(f"ALERT: High Risk ({data['risk_score']}) detected on {self.last_url}")
```

## 2. Why this is Pure Python:
- **No Kotlin/Java required**: PyJNIus handles the bridge to Android's Accessibility APIs.
- **Unified Logic**: The same `requests` and `json` logic from the backend is used here.
- **Kivy Overlay**: The "Pop Icon" and alerts are rendered using the Kivy graphics engine, which is Python-based.

## 3. Subscription Integration
The service periodically pings `GET /api/subscription/status` to verify if the $1/month Proactive Mode should be active. This ensures the background scanner only runs for active subscribers, managing server load efficiently.
