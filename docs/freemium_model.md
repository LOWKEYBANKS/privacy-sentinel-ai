# Privacy Sentinel AI: Freemium Model

To ensure the project is accessible to everyone while remaining sustainable, we implement a clear distinction between the **Free Tier** and the **Pro Tier ($1/month)**.

## 1. Feature Comparison

| Feature | Free Tier | Pro Tier ($1/month) |
| :--- | :--- | :--- |
| **Manual Scans** | Limited (3 per day) | Unlimited |
| **Web Extension** | Manual Click Only | Automated Background Scanning |
| **Mobile App** | Manual URL Entry | **Proactive Background Interception** |
| **AI Analysis** | Basic Summary | Deep Legal Analysis (GDPR/CCPA/HIPAA) |
| **Support** | Community | Priority |

## 2. The "Free Trial" Logic
Non-subscribers get a **7-day Pro Trial** upon first sign-up to experience the "Interception Popup" on mobile. After 7 days, the app reverts to "Manual Mode" unless the $1/month subscription is activated.

## 3. Backend Enforcement (`subscription.py`)
The backend now tracks the number of scans and the trial expiration date.

```python
# Logic implemented in agent/api/subscription.py
def check_feature_access(user_id: str, feature: str):
    user = db.get_user(user_id)
    if user.is_pro or user.in_trial:
        return True
    if feature == "background_monitoring":
        return False
    if feature == "manual_scan" and user.daily_scans < 3:
        return True
    return False
```
