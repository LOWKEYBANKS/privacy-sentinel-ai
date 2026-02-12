# Pure Python Background Monitoring & Pop Icon Implementation

This guide explains how to implement the background "pop icon" alert using **Python-only** tools (Kivy/BeeWare), maintaining our commitment to a pure Python ecosystem.

## 1. Architecture
We utilize **python-for-android** and **PyJNIus** to interact with native Android APIs directly from Python code. This allows us to avoid Kotlin while still accessing system-level features.

## 2. Background Service (`service.py`)
The background service runs in a separate process and monitors the active application.

### Step 1: Detect Active App
We use `PyJNIus` to access the Android `UsageStatsManager` or `AccessibilityService`.

```python
from jnius import autoclass
from os import environ

# Access Android System Services
Context = autoclass('android.content.Context')
UsageStatsManager = autoclass('android.app.usage.UsageStatsManager')

def check_active_app():
    # Logic to check if Chrome or Firefox is in the foreground
    # ...
    pass
```

### Step 2: Trigger Pop Icon (Overlay)
We use the Android `WindowManager` to draw a floating "pop icon" directly from Python.

```python
from jnius import autoclass, cast
import time

def show_pop_icon():
    WindowManager = autoclass('android.view.WindowManager')
    LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
    PixelFormat = autoclass('android.graphics.PixelFormat')
    Gravity = autoclass('android.view.Gravity')
    
    # Configure the floating window
    params = LayoutParams(
        LayoutParams.WRAP_CONTENT,
        LayoutParams.WRAP_CONTENT,
        LayoutParams.TYPE_APPLICATION_OVERLAY,
        LayoutParams.FLAG_NOT_FOCUSABLE,
        PixelFormat.TRANSLUCENT
    )
    params.gravity = Gravity.TOP | Gravity.LEFT
    
    # Add your Python-defined view to the screen
    # ...
```

## 3. Deployment Strategy
To maintain the "Python-only" status on GitHub:
1.  **Remove all .kt, .java, and .swift files.**
2.  **Use Buildozer**: Configure `buildozer.spec` to include your Python scripts and required Android permissions.
3.  **CI/CD**: GitHub Actions will use the `buildozer-action` to compile your Python code into a native APK.

## 4. Why this is better
- **No Language Spoilage**: Your GitHub language bar will show **100% Python**.
- **Unified Logic**: Use the same privacy analysis logic from your backend directly in the mobile app.
- **Easy Maintenance**: No need for Android/iOS specialized developers.
