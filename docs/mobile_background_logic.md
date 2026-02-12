# Mobile Background Service: Android Accessibility Implementation

To achieve the goal of **real-time background monitoring** on mobile devices, we utilize the **Android Accessibility Service**. This allows the app to "see" URLs in browsers and detect when other apps are launched, enabling proactive privacy analysis.

## 1. Core Logic (Kotlin/Android)

The following logic would be implemented in the native Android portion of the Flutter app.

```kotlin
class PrivacySentinelService : AccessibilityService() {

    private val API_URL = "https://privacy-sentinel-api.onrender.com/api/summarize"
    private val client = OkHttpClient()

    override fun onAccessibilityEvent(event: AccessibilityEvent) {
        // Detect URL changes in browsers (Chrome, Firefox, etc.)
        if (event.eventType == AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED || 
            event.eventType == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            
            val rootNode = rootInActiveWindow ?: return
            val url = findUrlInNode(rootNode)
            
            if (url != null && isNewWebsite(url)) {
                analyzePrivacyBackground(url)
            }
        }
    }

    private fun findUrlInNode(node: AccessibilityNodeInfo): String? {
        // Recursively search for URL bars or browser address fields
        if (node.viewIdResourceName?.contains("url_bar") == true || 
            node.viewIdResourceName?.contains("location_bar") == true) {
            return node.text?.toString()
        }
        for (i in 0 until node.childCount) {
            val result = findUrlInNode(node.getChild(i) ?: continue)
            if (result != null) return result
        }
        return null
    }

    private fun analyzePrivacyBackground(url: String) {
        // 1. Check if user is a $1/month subscriber
        if (!checkSubscriptionStatus()) return

        // 2. Send to Privacy Sentinel API
        val request = Request.Builder()
            .url(API_URL)
            .post(RequestBody.create(JSON, "{\"source_url\": \"$url\", \"snippet\": \"Background Scan\"}"))
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onResponse(call: Call, response: Response) {
                val data = JSONObject(response.body()?.string())
                val riskScore = data.getInt("risk_score")
                
                // 3. Trigger High-Risk Notification
                if (riskScore > 70) {
                    showPrivacyAlert(url, riskScore, data.getString("summary"))
                }
            }
            override fun onFailure(call: Call, e: IOException) {}
        })
    }

    private fun showPrivacyAlert(url: String, score: Int, summary: String) {
        // Native Android Notification with a "Don't Accept" action
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_sentinel_shield)
            .setContentTitle("⚠️ Privacy Risk Detected")
            .setContentText("Site: $url has a risk score of $score/100")
            .setStyle(NotificationCompat.BigTextStyle().bigText(summary))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()
            
        notificationManager.notify(NOTIFICATION_ID, notification)
    }
}
```

## 2. Subscription Integration ($1/Month)

The background service will verify the user's status against the FastAPI backend before performing heavy AI analysis.

- **Check**: `GET /api/subscription/status`
- **Logic**: If `is_subscribed` is `false`, the background monitoring remains in "Passive Mode" (manual scans only).
- **Activation**: Once the $1 payment is confirmed via Stripe/LemonSqueezy, the backend updates the database, and the mobile service activates "Proactive Mode."

## 3. Why this works for your vision:
- **Background**: No need to open the app; it runs as a system service.
- **Proactive**: Tells you the data collection practices *before* you interact with the site.
- **Affordable**: The $1/month fee covers the server costs for the AI analysis and the persistent database.
