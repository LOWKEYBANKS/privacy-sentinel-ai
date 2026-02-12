import js
from pyodide.http import pyfetch
from pyscript import document, when
import asyncio

# Core Configuration
API_URL = "https://privacy-sentinel-api.onrender.com/api/summarize"

def get_page_content():
    """Extracts the text content from the current active tab."""
    # In a real extension, this would use chrome.scripting.executeScript
    # For the PyScript demo, we use the current document
    return js.document.body.innerText if js.document.body else ""

async def analyze_current_page(event=None):
    """Triggers the analysis of the current page's privacy policy."""
    score_element = document.getElementById("score")
    status_element = document.getElementById("risk-level")
    summary_element = document.getElementById("summary")
    
    # Update UI to loading state
    score_element.innerText = "..."
    status_element.innerText = "Analyzing..."
    summary_element.innerText = "Fetching policy data and running AI analysis..."
    
    content = get_page_content()
    
    if not content or len(content) < 100:
        display_error("No significant content found to analyze.")
        return

    try:
        response = await pyfetch(
            url=API_URL,
            method="POST",
            headers={
                "Content-Type": "application/json"
            },
            body=js.JSON.stringify({
                "snippet": content[:8000], # Send a safe chunk
                "source_url": js.window.location.href
            })
        )
        
        if response.status == 200:
            data = await response.json()
            update_ui(data)
        else:
            display_error(f"API Error: {response.status}")
    except Exception as e:
        display_error(f"Connection failed: {str(e)}")

def update_ui(data):
    """Updates the popup UI with real analysis data."""
    score = data.get("risk_score", 0)
    summary = data.get("summary", "No summary available.")
    
    score_element = document.getElementById("score")
    status_element = document.getElementById("risk-level")
    summary_element = document.getElementById("summary")
    
    score_element.innerText = str(score)
    
    # Color coding based on score
    if score < 30:
        score_element.style.color = "#27ae60" # Green
        status_element.innerText = "Safe"
    elif score < 60:
        score_element.style.color = "#f39c12" # Orange
        status_element.innerText = "Moderate Risk"
    else:
        score_element.style.color = "#e74c3c" # Red
        status_element.innerText = "High Risk"
        
    summary_element.innerText = summary

def display_error(message):
    """Displays an error message in the UI."""
    document.getElementById("score").innerText = "!"
    document.getElementById("risk-level").innerText = "Error"
    document.getElementById("summary").innerText = message

# Initialize analysis when the popup is opened
asyncio.ensure_future(analyze_current_page())
