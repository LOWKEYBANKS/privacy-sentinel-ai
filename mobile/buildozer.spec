[app]
title = Privacy Sentinel AI
package.name = privacysentinel
package.domain = ai.lowkeybanks
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1.0
requirements = python3,kivy,requests,certifi,urllib3,idna,charset-normalizer
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET, SYSTEM_ALERT_WINDOW, BIND_ACCESSIBILITY_SERVICE, PACKAGE_USAGE_STATS
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.arch = arm64-v8a
services = SentinelService:service.py:foreground:sticky

[buildozer]
log_level = 2
warn_on_root = 1
