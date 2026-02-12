from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Optional
import os
import stripe
import logging

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
        "trial_ends_at": datetime.now() + timedelta(days=7),
        "daily_scans": 0,
        "last_scan_date": datetime.now().date()
    }
}

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
async def initiate_mobile_money(phone_number: str, user_id: str = Depends(get_current_user)):
    """
    Initiates a Mobile Money payment (e.g., M-Pesa STK Push).
    In production, this would call Flutterwave or a similar API.
    """
    logger.info(f"Initiating Mobile Money payment for {phone_number}")
    # Mock successful initiation
    return {
        "status": "success",
        "message": "STK Push sent to your phone. Please enter your PIN to authorize the \$1 payment.",
        "transaction_id": f"tx_mock_{user_id}"
    }

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
