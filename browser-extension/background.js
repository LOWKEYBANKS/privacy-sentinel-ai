// Privacy Sentinel AI - Background Service Worker
// MV3 Compliant

const API_URL = 'http://localhost:8000';

// On Install
chrome.runtime.onInstalled.addListener(() => {
    console.log('Privacy Sentinel AI Extension Installed');
    chrome.contextMenus.create({
        id: "scan-privacy",
        title: "Scan Privacy Policy",
        contexts: ["page"]
    });
});

// Context Menu Click Handler
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "scan-privacy") {
        scanUrl(tab.url, tab.id);
    }
});

// Message Listener
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scanPage") {
        scanUrl(request.url, sender.tab.id);
        sendResponse({ status: "scanning_started" });
    }
    return true; // Keep channel open for async response
});

async function scanUrl(url, tabId) {
    console.log(`Scanning URL: ${url}`);

    try {
        // Notify content script to show loading state
        chrome.tabs.sendMessage(tabId, { action: "scanStatus", status: "loading" });

        const response = await fetch(`${API_URL}/scan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();
        console.log('Scan results:', data);

        // Send results to content script to display
        chrome.tabs.sendMessage(tabId, {
            action: "scanResults",
            results: data
        });

    } catch (error) {
        console.error('Scan failed:', error);
        chrome.tabs.sendMessage(tabId, {
            action: "scanError",
            error: error.message
        });
    }
}
