from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Optional
import os
import stripe
import logging
import httpx
import uuid
from abc import ABC, abstractmethod

router = APIRouter()
logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "price_1_month_1usd")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock")

# In-memory storage for demo purposes (In production, use PostgreSQL)
from datetime import datetime, timedelta

mock_user_db = {
    "user123": {
        "is_subscribed": False, 
        "level": "free", 
        "stripe_customer_id": None,
        "flutterwave_customer_id": None,
        "trial_ends_at": datetime.now() + timedelta(days=7),
        "daily_scans": 0,
        "last_scan_date": datetime.now().date()
    }
}

# Mock transaction storage
mock_transaction_db = {}

# Flutterwave Configuration
FLUTTERWAVE_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY", "FLWSECK_TEST_MOCK")
FLUTTERWAVE_BASE_URL = "https://api.flutterwave.com/v3"

class PaymentProvider(ABC):
    @abstractmethod
    async def initiate_payment(self, user_id: str, amount: float, currency: str, **kwargs):
        pass

class FlutterwaveProvider(PaymentProvider):
    async def initiate_payment(self, user_id: str, amount: float, currency: str, **kwargs):
        phone_number = kwargs.get("phone_number")
        network = kwargs.get("network", "M-PESA")
        country = kwargs.get("country", "KE")
        
        # 1. Create/Get Customer (Simplified for demo)
        customer_id = mock_user_db[user_id].get("flutterwave_customer_id") or f"cus_flw_{user_id}"
        
        # 2. In a real implementation, we would call Flutterwave API here
        # For this task, we'll simulate the logic and provide the implementation structure
        
        transaction_id = f"flw_tx_{uuid.uuid4().hex[:8]}"
        mock_transaction_db[transaction_id] = {
            "user_id": user_id,
            "status": "pending",
            "amount": amount,
            "currency": currency
        }
        
        logger.info(f"Flutterwave: Initiated {network} payment for {user_id} ({phone_number})")
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "message": f"STK Push sent to {phone_number}. Please authorize the {currency} {amount} payment."
        }

payment_gateway = FlutterwaveProvider()

async def get_current_user():
    # Mock authentication - in production, this would be a JWT or OAuth dependency
    return "user123"

@router.get("/subscription/status")
async def get_subscription_status(user_id: str = Depends(get_current_user)):
    """Check the current user's subscription status."""
    user_data = mock_user_db.get(user_id)
    if not user_data:
        return {"is_subscribed": False, "level": "free"}
    
    in_trial = datetime.now() < user_data.get("trial_ends_at", datetime.now())
    
    return {
        "user_id": user_id,
        "is_subscribed": user_data["is_subscribed"],
        "subscription_level": "pro" if user_data["is_subscribed"] else "free",
        "in_trial": in_trial,
        "trial_days_left": (user_data["trial_ends_at"] - datetime.now()).days if in_trial else 0,
        "can_use_background": user_data["is_subscribed"] or in_trial
    }

@router.post("/subscription/checkout")
async def create_checkout_session(user_id: str = Depends(get_current_user)):
    """Creates a Stripe Checkout Session for the $1/month plan."""
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': STRIPE_PRICE_ID,
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://privacy-sentinel.ai/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://privacy-sentinel.ai/cancel',
            client_reference_id=user_id,
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        logger.error(f"Stripe Checkout Error: {e}")
        return {
            "checkout_url": f"https://checkout.stripe.com/pay/mock_{user_id}",
            "message": "Development mode: Mock checkout URL provided."
        }

@router.post("/subscription/mobile-money/initiate")
async def initiate_mobile_money(
    phone_number: str, 
    network: str = "M-PESA",
    currency: str = "KES",
    user_id: str = Depends(get_current_user)
):
    """
    Initiates a Mobile Money payment via Flutterwave.
    """
    # $1 USD is approx 130 KES (example rate)
    amount = 130.0 if currency == "KES" else 1.0
    
    result = await payment_gateway.initiate_payment(
        user_id=user_id,
        amount=amount,
        currency=currency,
        phone_number=phone_number,
        network=network
    )
    return result

@router.post("/subscription/flutterwave/webhook")
async def flutterwave_webhook(request: Request):
    """Handles Flutterwave Webhooks for mobile money payments."""
    # In production, verify signature: request.headers.get('verif-hash')
    data = await request.json()
    
    if data.get("status") == "successful":
        tx_id = data.get("tx_ref") or data.get("id")
        tx_data = mock_transaction_db.get(tx_id)
        
        if tx_data:
            user_id = tx_data["user_id"]
            if user_id in mock_user_db:
                mock_user_db[user_id]["is_subscribed"] = True
                mock_user_db[user_id]["level"] = "pro"
                tx_data["status"] = "completed"
                logger.info(f"Mobile Money subscription activated for user: {user_id}")
    
    return {"status": "success"}

@router.post("/subscription/webhook")
async def stripe_webhook(request: Request):
    """Handles Stripe Webhooks to activate/deactivate subscriptions."""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('client_reference_id')
        if user_id in mock_user_db:
            mock_user_db[user_id]["is_subscribed"] = True
            mock_user_db[user_id]["level"] = "pro"
            logger.info(f"Subscription activated for user: {user_id}")

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Logic to find user by stripe_customer_id and deactivate
        logger.info("Subscription cancelled.")

    return {"status": "success"}

@router.post("/subscription/mock-activate")
async def mock_activate(user_id: str = Depends(get_current_user)):
    """Utility to manually activate for testing."""
    mock_user_db[user_id] = {"is_subscribed": True, "level": "pro"}
    return {"message": "Pro status activated for user123"}
