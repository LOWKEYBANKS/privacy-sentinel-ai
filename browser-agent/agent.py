import js
from pyodide.http import pyfetch
import asyncio
import json

class BrowserPrivacyAgent:
    def __init__(self):
        # Dynamically determine API URL: use production if not on localhost
        self.api_url = "https://api.privacysentinel.ai" if "localhost" not in js.window.location.hostname else "http://localhost:8000"
        self.detection_keywords = ["privacy", "policy", "terms", "data protection", "legal", "compliance", "gdpr"]
        
    async def scan_current_page(self):
        js.console.log("Privacy Sentinel: Scanning page...")
        
        # Update UI to show scanning state
        self.update_ui_status("Scanning...", "--")
        
        links = js.document.querySelectorAll("a")
        found_policies = []
        for i in range(links.length):
            link = links.item(i)
            text = link.innerText.lower()
            href = link.getAttribute("href")
            if href and any(keyword in text for keyword in self.detection_keywords):
                found_policies.append({"text": text, "url": href})
        
        if found_policies:
            policy_url = found_policies[0]['url']
            if not policy_url.startswith('http'):
                policy_url = js.window.location.origin + policy_url
            js.console.log(f"Privacy Sentinel: Analyzing {policy_url}")
            await self.analyze_policy(policy_url)
        else:
            self.update_ui_status("No Policy Found", "N/A")
            js.console.log("Privacy Sentinel: No policies detected")

    def update_ui_status(self, status, score):
        score_el = js.document.getElementById("score")
        status_el = js.document.getElementById("risk-level")
        if score_el: score_el.innerText = score
        if status_el: status_el.innerText = status

    async def analyze_policy(self, url):
        try:
            payload = {
                "source_url": url,
                "snippet": f"Policy found at {url}. (Content extraction in progress via Python WASM)",
                "timestamp": js.Date.new().toISOString()
            }
            response = await pyfetch(
                url=f"{self.api_url}/api/summarize",
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps(payload)
            )
            if response.status == 200:
                data = await response.json()
                self.show_alert(data)
        except Exception as e:
            js.console.error(f"Privacy Sentinel: Analysis failed: {str(e)}")

    def show_alert(self, analysis):
        risk_score = analysis.get('risk_score', 0)
        color = "#ff4d4d" if risk_score >= 70 else "#ffa500" if risk_score >= 40 else "#4CAF50"
        alert_div = js.document.createElement("div")
        alert_div.style.cssText = f"position:fixed; top:20px; right:20px; padding:15px; background:white; border-left:5px solid {color}; box-shadow:0 4px 8px rgba(0,0,0,0.2); z-index:9999; max-width:300px; font-family:sans-serif;"
        alert_div.innerHTML = f'<h4>🛡️ Privacy Sentinel</h4><p>Risk Score: <strong>{risk_score}/100</strong></p><p style="font-size:12px;">{analysis.get("summary", "")}</p><button onclick="this.parentElement.remove()">Dismiss</button>'
        js.document.body.appendChild(alert_div)

agent = BrowserPrivacyAgent()
asyncio.ensure_future(agent.scan_current_page())
