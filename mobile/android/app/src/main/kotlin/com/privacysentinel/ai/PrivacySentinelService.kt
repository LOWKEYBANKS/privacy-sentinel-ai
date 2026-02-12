package com.privacysentinel.ai

import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import android.util.Log
import okhttp3.*
import org.json.JSONObject
import java.io.IOException

class PrivacySentinelService : AccessibilityService() {

    private val TAG = "PrivacySentinel"
    private val API_URL = "https://privacy-sentinel-api.onrender.com/api/summarize"
    private val client = OkHttpClient()
    private var lastScannedUrl = ""

    override fun onAccessibilityEvent(event: AccessibilityEvent) {
        // We look for content changes or window state changes (new page/tab)
        if (event.eventType == AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED || 
            event.eventType == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            
            val rootNode = rootInActiveWindow ?: return
            val url = findUrlInNode(rootNode)
            
            if (url != null && url != lastScannedUrl && url.startsWith("http")) {
                lastScannedUrl = url
                Log.d(TAG, "Detected new URL: $url")
                analyzePrivacyBackground(url)
            }
        }
    }

    private fun findUrlInNode(node: AccessibilityNodeInfo): String? {
        // Common resource IDs for URL bars in Chrome and other browsers
        val urlResourceIds = arrayOf(
            "com.android.chrome:id/url_bar",
            "org.mozilla.firefox:id/url_bar_title",
            "com.opera.browser:id/url_field"
        )

        for (id in urlResourceIds) {
            val nodes = node.findAccessibilityNodeInfosByViewId(id)
            if (nodes.isNotEmpty()) {
                return nodes[0].text?.toString()
            }
        }

        // Recursive search fallback
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            val result = findUrlInNode(child)
            if (result != null) return result
        }
        return null
    }

    private fun analyzePrivacyBackground(url: String) {
        val json = JSONObject()
        json.put("source_url", url)
        json.put("snippet", "Background scan for $url")

        val body = RequestBody.create(
            MediaType.parse("application/json; charset=utf-8"),
            json.toString()
        )

        val request = Request.Builder()
            .url(API_URL)
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e(TAG, "API Call failed: ${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (!it.isSuccessful) return
                    val responseData = it.body()?.string() ?: return
                    val data = JSONObject(responseData)
                    val riskScore = data.optInt("risk_score", 0)
                    
                    if (riskScore > 60) {
                        Log.w(TAG, "HIGH RISK detected for $url: $riskScore")
                        // In a real app, this would trigger a system notification
                    }
                }
            }
        })
    }

    override fun onInterrupt() {
        Log.d(TAG, "Service Interrupted")
    }
}
