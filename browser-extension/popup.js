document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scan-btn');
    const resultsArea = document.getElementById('results-area');
    const loadingArea = document.getElementById('loading-area');
    const errorArea = document.getElementById('error-area');
    const statusBadge = document.getElementById('status-badge');

    // Check if we have stored results for current tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const currentTab = tabs[0];
        if (currentTab) {
            // Request status from background
            // In a real implementation, we might check local storage or ask background script
        }
    });

    scanBtn.addEventListener('click', () => {
        showLoading();

        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            const currentTab = tabs[0];
            if (currentTab) {
                chrome.runtime.sendMessage({
                    action: "scanPage",
                    url: currentTab.url
                }, (response) => {
                    if (chrome.runtime.lastError) {
                        showError(chrome.runtime.lastError.message);
                    }
                });
            }
        });
    });

    // Listen for messages
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === "scanResults") {
            displayResults(request.results);
        } else if (request.action === "scanError") {
            showError(request.error);
        }
    });

    function showLoading() {
        scanBtn.disabled = true;
        resultsArea.classList.add('hidden');
        errorArea.classList.add('hidden');
        loadingArea.classList.remove('hidden');
        statusBadge.textContent = "Scanning...";
        statusBadge.style.background = "#e2e8f0";
        statusBadge.style.color = "#64748b";
    }

    function displayResults(data) {
        loadingArea.classList.add('hidden');
        resultsArea.classList.remove('hidden');
        scanBtn.disabled = false;
        statusBadge.textContent = "Complete";
        statusBadge.style.background = "#d1fae5";
        statusBadge.style.color = "#10b981";

        const overall = data.overall_assessment || {};
        const analysis = data.scan_results ? Object.values(data.scan_results)[0]?.analysis : {};

        // Update Score
        document.getElementById('score-value').textContent = overall.risk_score || 0;

        // Update Level
        const riskLevel = document.getElementById('risk-level');
        riskLevel.textContent = overall.risk_level || 'Unknown';
        riskLevel.className = 'risk-level ' + (overall.risk_level || 'low').toLowerCase();

        // Update Summary
        document.getElementById('summary-text').textContent = overall.message || "Analysis complete.";

        // Update Risks List
        const list = document.getElementById('risks-list');
        list.innerHTML = '';

        const risks = overall.unique_risks || [];
        if (risks.length === 0) {
            const li = document.createElement('li');
            li.textContent = "No significant risks detected.";
            li.style.borderLeftColor = "#10b981";
            list.appendChild(li);
        } else {
            risks.forEach(risk => {
                const li = document.createElement('li');
                li.textContent = risk;
                list.appendChild(li);
            });
        }
    }

    function showError(msg) {
        loadingArea.classList.add('hidden');
        errorArea.classList.remove('hidden');
        document.getElementById('error-message').textContent = msg;
        scanBtn.disabled = false;
        statusBadge.textContent = "Error";
        statusBadge.style.background = "#fee2e2";
        statusBadge.style.color = "#ef4444";
    }
});
