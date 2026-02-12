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
mock_user_db = {
    "user123": {"is_subscribed": False, "level": "free", "stripe_customer_id": None}
}

async def get_current_user():
    # Mock authentication - in production, this would be a JWT or OAuth dependency
    return "user123"

@router.get("/subscription/status")
async def get_subscription_status(user_id: str = Depends(get_current_user)):
    """Check the current user's subscription status."""
    user_data = mock_user_db.get(user_id, {"is_subscribed": False, "level": "free"})
    return {
        "user_id": user_id,
        "is_subscribed": user_data["is_subscribed"],
        "subscription_level": user_data["level"]
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
        # Fallback for demo/dev mode
        return {
            "checkout_url": f"https://checkout.stripe.com/pay/mock_{user_id}",
            "message": "Development mode: Mock checkout URL provided."
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
