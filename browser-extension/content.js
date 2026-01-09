// Privacy Sentinel AI - Content Script

console.log("Privacy Sentinel AI Content Script Loaded");

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scanResults") {
        displayResults(request.results);
    } else if (request.action === "scanError") {
        displayError(request.error);
    } else if (request.action === "scanStatus" && request.status === "loading") {
        showLoading();
    }
});

function createOverlay() {
    let overlay = document.getElementById('privacy-sentinel-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'privacy-sentinel-overlay';
        overlay.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      width: 300px;
      background: white;
      box-shadow: 0 4px 15px rgba(0,0,0,0.2);
      border-radius: 8px;
      z-index: 999999;
      font-family: Arial, sans-serif;
      padding: 15px;
      border: 1px solid #e0e0e0;
    `;
        document.body.appendChild(overlay);

        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
      position: absolute;
      top: 5px;
      right: 10px;
      border: none;
      background: none;
      font-size: 20px;
      cursor: pointer;
    `;
        closeBtn.onclick = () => overlay.remove();
        overlay.appendChild(closeBtn);
    }
    return overlay;
}

function showLoading() {
    const overlay = createOverlay();
    const content = document.createElement('div');
    content.innerHTML = `
    <h3 style="margin: 0 0 10px 0; color: #333;">Privacy Sentinel</h3>
    <p>Scanning privacy policy...</p>
  `;
    // Clear previous content except close button
    while (overlay.childNodes.length > 1) {
        overlay.removeChild(overlay.lastChild);
    }
    overlay.appendChild(content);
}

function displayResults(data) {
    const overlay = createOverlay();
    const results = data.results || {};
    const overall = results.overall_assessment || {};

    const riskColor = overall.risk_level === 'High' ? '#ff4444' :
        overall.risk_level === 'Medium' ? '#ffbb33' : '#00C851';

    const content = document.createElement('div');
    content.innerHTML = `
    <h3 style="margin: 0 0 10px 0; color: #333;">Scan Complete</h3>
    <div style="margin-bottom: 10px;">
      <strong>Risk Level:</strong> 
      <span style="color: ${riskColor}; font-weight: bold;">${overall.risk_level || 'Unknown'}</span>
    </div>
    <div style="font-size: 14px; color: #666;">
      ${overall.message || 'No details available.'}
    </div>
    <div style="margin-top: 10px; font-size: 12px;">
      Policies found: ${results.policies_found ? results.policies_found.length : 0}
    </div>
  `;

    while (overlay.childNodes.length > 1) {
        overlay.removeChild(overlay.lastChild);
    }
    overlay.appendChild(content);
}

function displayError(error) {
    const overlay = createOverlay();
    const content = document.createElement('div');
    content.innerHTML = `
    <h3 style="margin: 0 0 10px 0; color: #333;">Error</h3>
    <p style="color: red;">${error}</p>
  `;
    while (overlay.childNodes.length > 1) {
        overlay.removeChild(overlay.lastChild);
    }
    overlay.appendChild(content);
}
