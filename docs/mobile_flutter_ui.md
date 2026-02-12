# Mobile App: Flutter UI & Subscription Flow

This document outlines the Flutter-based user interface and the integration of the $1/month subscription model.

## 1. Dashboard View
The main screen of the app will display the user's current protection status and recent scan history.

```dart
class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('🛡️ Privacy Sentinel')),
      body: Column(
        children: [
          ProtectionStatusCard(), // Shows "Active" or "Upgrade to Pro"
          RecentActivityList(),    // List of sites visited and their scores
          SubscriptionBanner(),    // $1/month call to action
        ],
      ),
    );
  }
}
```

## 2. Subscription Flow ($1/Month)
We will use a simple "One-Tap" subscription model.

1. **The Offer**: "Get real-time background protection for just $1/month."
2. **The Payment**: Integrated via **Stripe** or **Lemon Squeezy**.
3. **The Activation**:
   - User clicks "Subscribe."
   - App opens a secure checkout.
   - On success, the backend `subscription.py` updates the user's `is_subscribed` flag.
   - The Mobile App receives a push notification or WebSocket update to enable the Background Accessibility Service.

## 3. Background Service Toggle
Users can manually enable or disable the background monitoring.

```dart
SwitchListTile(
  title: Text("Background Monitoring"),
  subtitle: Text("Scan websites automatically in the background"),
  value: user.isSubscribed && settings.backgroundEnabled,
  onChanged: (val) {
    if (!user.isSubscribed) {
      showUpgradeDialog(context);
    } else {
      toggleBackgroundService(val);
    }
  },
)
```

## 4. Why $1/Month?
- **Low Barrier to Entry**: $1 is a "no-brainer" for most users.
- **Sustainable**: 10,000 users = $10,000/month, which easily covers the API costs for GPT-4o-mini and the Render hosting.
- **Privacy First**: By paying a small fee, users are the *customers*, not the *product*. We don't need to sell their data to keep the lights on.
