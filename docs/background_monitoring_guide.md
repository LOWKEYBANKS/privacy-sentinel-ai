# Background Monitoring & Pop Icon Implementation

This guide explains how to implement the background "pop icon" alert that triggers when a user opens a web browser.

## 1. Android Implementation (The "Pop Icon")

To show an overlay over other apps, we use an **Accessibility Service** for detection and a **System Alert Window** for the UI.

### Step 1: Add Dependencies
Add these to your `pubspec.yaml`:
```yaml
dependencies:
  flutter_accessibility_service: ^1.0.0
  system_alert_window: ^2.0.7
```

### Step 2: Configure AndroidManifest.xml
You must declare the Accessibility Service and the Overlay permission.
```xml
<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
<uses-permission android:name="android.permission.BIND_ACCESSIBILITY_SERVICE" />

<service
    android:name="slayer.accessibility.service.flutter_accessibility_service.AccessibilityListener"
    android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"
    android:exported="true">
    <intent-filter>
        <action android:name="android.view.accessibility.AccessibilityService" />
    </intent-filter>
    <meta-data
        android:name="android.accessibilityservice"
        android:resource="@xml/accessibility_service_config" />
</service>
```

### Step 3: Background Detection Logic
```dart
import 'package:flutter_accessibility_service/flutter_accessibility_service.dart';
import 'package:system_alert_window/system_alert_window.dart';

void startMonitoring() {
  FlutterAccessibilityService.accessStream.listen((event) {
    List<String> browsers = [
      "com.android.chrome",
      "org.mozilla.firefox",
      "com.sec.android.app.sbrowser"
    ];

    if (browsers.contains(event.packageName)) {
      showPopIcon();
    } else {
      hidePopIcon();
    }
  });
}

void showPopIcon() async {
  await SystemAlertWindow.showSystemWindow(
    height: 100,
    width: 100,
    gravity: SystemWindowGravity.TOP,
    notificationTitle: "Privacy Sentinel",
    notificationBody: "Monitoring active browsing...",
  );
}
```

## 2. iOS Implementation (Live Activities)

Since iOS doesn't allow floating icons over other apps, we use **Live Activities** to provide a similar experience in the Dynamic Island and Lock Screen.

### Step 1: Enable Live Activities
In Xcode, add the "Live Activities" capability to your project.

### Step 2: Trigger on Browser Use
Use the **Device Activity API** to detect when the "Browsers" category is active.
```swift
// Swift code in your iOS Runner
let schedule = DeviceActivitySchedule(
    intervalStart: DateComponents(hour: 0, minute: 0),
    intervalEnd: DateComponents(hour: 23, minute: 59),
    repeats: true
)

// Start a Live Activity when the browser is opened
let attributes = PrivacySentinelAttributes(name: "Browsing Protected")
let initialState = PrivacySentinelAttributes.ContentState(riskLevel: "Low")
activity = try? Activity<PrivacySentinelAttributes>.request(attributes: attributes, contentState: initialState)
```

## 3. Summary of Experience
- **Android**: A small floating shield icon appears on the side of the screen when Chrome/Firefox is open. Tapping it expands to show privacy risks.
- **iOS**: A privacy shield appears in the **Dynamic Island** or on the **Lock Screen** as soon as browsing starts, providing real-time risk updates.
