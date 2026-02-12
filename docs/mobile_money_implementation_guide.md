# Mobile Money Implementation Guide

This document outlines the steps taken to integrate Flutterwave for mobile money payments in the Privacy Sentinel AI backend.

## 1. Backend Changes

### Payment Gateway Architecture
We introduced a `PaymentProvider` abstract base class to allow for multiple payment gateways (Stripe, Flutterwave, etc.).

```python
class PaymentProvider(ABC):
    @abstractmethod
    async def initiate_payment(self, user_id: str, amount: float, currency: str, **kwargs):
        pass
```

### Flutterwave Integration
The `FlutterwaveProvider` handles the interaction with the Flutterwave API. It supports:
- **M-Pesa STK Push**: Automatically triggered for Kenyan numbers.
- **Other Networks**: Supports MTN, Airtel, etc.

### API Endpoints
- `POST /api/subscription/mobile-money/initiate`: Triggers the payment prompt on the user's phone.
- `POST /api/subscription/flutterwave/webhook`: Receives asynchronous payment confirmations from Flutterwave.

## 2. Environment Variables
To enable production Flutterwave payments, set the following environment variables:
- `FLUTTERWAVE_SECRET_KEY`: Your Flutterwave secret key.
- `FLUTTERWAVE_WEBHOOK_SECRET`: Secret hash for verifying webhooks.

## 3. Flutter App Integration (Next Steps)
The Flutter app should be updated to:
1.  Add a "Mobile Money" option in the subscription screen.
2.  Collect the user's phone number and network.
3.  Call the `/api/subscription/mobile-money/initiate` endpoint.
4.  Listen for success/failure via the API or a WebSocket if implemented.

## 4. Testing
You can run the integration tests using:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/agent
python3 -m pytest tests/test_mobile_money.py
```
