import js
from pyodide.http import pyfetch
from pyscript import document, when
import asyncio

# Core Configuration
API_URL = "https://privacy-sentinel-api.onrender.com/api/summarize"

async def get_active_tab_content():
    """
    In a real Chrome extension, the popup cannot directly access the page's DOM.
    It must message the content script or use chrome.scripting.
    This logic handles both the PyScript demo environment and the real extension context.
    """
    try:
        # Try to use Chrome Extension API if available
        if hasattr(js, "chrome") and hasattr(js.chrome, "tabs"):
            # Get current active tab
            tabs = await js.chrome.tabs.query({"active": True, "currentWindow": True})
            active_tab = tabs[0]
            
            # Execute script to get body text
            result = await js.chrome.scripting.executeScript({
                "target": {"tabId": active_tab.id},
                "func": js.eval("(lambda: document.body.innerText)")
            })
            return result[0].result
        else:
            # Fallback for local browser testing/PyScript demo
            return js.document.body.innerText if js.document.body else ""
    except Exception as e:
        print(f"Content extraction error: {e}")
        return js.document.body.innerText if js.document.body else ""

async def analyze_current_page(event=None):
    """Triggers the analysis of the current page's privacy policy."""
    score_element = document.getElementById("score")
    status_element = document.getElementById("risk-level")
    summary_element = document.getElementById("summary")
    
    # Update UI to loading state
    score_element.innerText = "..."
    status_element.innerText = "Analyzing..."
    summary_element.innerText = "Sentinel is scanning the page content for privacy risks..."
    
    content = await get_active_tab_content()
    
    if not content or len(content) < 100:
        display_error("Could not find enough text on this page to analyze. Make sure you're on a page with a privacy policy.")
        return

    try:
        # Send to your live Render API
        response = await pyfetch(
            url=API_URL,
            method="POST",
            headers={
                "Content-Type": "application/json"
            },
            body=js.JSON.stringify({
                "snippet": content[:10000], # Send a larger chunk for better AI context
                "source_url": js.window.location.href
            })
        )
        
        if response.status == 200:
            data = await response.json()
            update_ui(data)
        else:
            display_error(f"API Error ({response.status}): The backend might be waking up. Please try again in a moment.")
    except Exception as e:
        display_error(f"Connection failed: {str(e)}. Check your internet or if the API is online.")

def update_ui(data):
    """Updates the popup UI with real analysis data."""
    score = data.get("risk_score", 0)
    summary = data.get("summary", "No summary available.")
    
    score_element = document.getElementById("score")
    status_element = document.getElementById("risk-level")
    summary_element = document.getElementById("summary")
    
    score_element.innerText = str(score)
    
    # Color coding based on score (0 is safe, 100 is dangerous)
    if score < 35:
        score_element.style.color = "#27ae60" # Green
        status_element.innerText = "Low Risk"
        status_element.style.color = "#27ae60"
    elif score < 70:
        score_element.style.color = "#f39c12" # Orange
        status_element.innerText = "Moderate Risk"
        status_element.style.color = "#f39c12"
    else:
        score_element.style.color = "#e74c3c" # Red
        status_element.innerText = "High Risk"
        status_element.style.color = "#e74c3c"
        
    summary_element.innerText = summary

def display_error(message):
    """Displays an error message in the UI."""
    document.getElementById("score").innerText = "!"
    document.getElementById("score").style.color = "#7f8c8d"
    document.getElementById("risk-level").innerText = "Notice"
    document.getElementById("risk-level").style.color = "#7f8c8d"
    document.getElementById("summary").innerText = message

# Auto-start analysis when the popup opens
asyncio.ensure_future(analyze_current_page())
