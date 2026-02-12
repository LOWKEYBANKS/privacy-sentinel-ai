import js
from pyodide.http import pyfetch
from pyscript import document

# Placeholder for Trafilatura integration
# from trafilatura import extract

def get_page_content():
    # This function would extract the main content of the page
    # For now, it's a placeholder
    return js.document.documentElement.outerHTML

async def analyze_privacy_policy_in_browser():
    content = get_page_content()
    # In the future, we will use Trafilatura here
    # extracted_text = extract(content)
    
    # For now, simulate sending to API
    response = await pyfetch(
        url="https://privacy-sentinel-api.onrender.com/api/summarize",
        method="POST",
        headers={
            "Content-Type": "application/json"
        },
        body=js.JSON.stringify({"snippet": content})
    )
    
    if response.status == 200:
        data = await response.json()
        display_risk_score(data.risk_score, data.summary)
    else:
        display_error("Failed to analyze privacy policy.")

def display_risk_score(score, summary):
    # Create a simple overlay to display the score
    overlay = document.createElement("div")
    overlay.style.cssText = "position: fixed; top: 10px; right: 10px; background: #333; color: white; padding: 10px; border-radius: 5px; z-index: 10000;"
    overlay.innerText = f"Privacy Score: {score}/100\nSummary: {summary}"
    document.body.appendChild(overlay)

def display_error(message):
    error_overlay = document.createElement("div")
    error_overlay.style.cssText = "position: fixed; top: 10px; right: 10px; background: red; color: white; padding: 10px; border-radius: 5px; z-index: 10000;"
    error_overlay.innerText = f"Error: {message}"
    document.body.appendChild(error_overlay)

# This would be triggered by a browser event listener in a real extension
# For PyScript, we might trigger it on page load or a button click
# analyze_privacy_policy_in_browser() # This would be called by the extension's content script
