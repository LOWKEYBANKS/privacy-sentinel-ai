# Mobile Money Integration: M-Pesa & Flutterwave

To make the $1/month subscription accessible globally, especially in regions with high mobile money usage (like Africa), we are integrating **Flutterwave**. This gateway supports M-Pesa, MTN MoMo, Airtel Money, and more.

## 1. Why Flutterwave?
- **Global Reach**: Supports 30+ currencies and multiple mobile money providers.
- **Developer Friendly**: Robust Python SDK and clean REST API.
- **Affordable**: Transaction fees are competitive for small $1 payments.

## 2. Payment Flow
1. **Selection**: User chooses "Mobile Money" in the Flutter app.
2. **Initiation**: App calls `/api/subscription/mobile-money/initiate`.
3. **Payment**: 
   - **M-Pesa**: User receives an STK Push (PIN prompt) on their phone.
   - **Others**: User is redirected to a secure Flutterwave payment page.
4. **Verification**: Backend receives a webhook or verifies the transaction ID.
5. **Activation**: User's "Pro" status is instantly activated.

## 3. Backend Logic (`subscription.py`)
We add a dedicated router for Mobile Money handling.

```python
@router.post("/subscription/mobile-money/initiate")
async def initiate_mobile_money(phone_number: str, user_id: str):
    # Call Flutterwave API to trigger STK Push or payment link
    # ...
    return {"status": "pending", "message": "Check your phone for the payment prompt"}
```
