from flask import Blueprint, session, redirect
from models.subscription_model import create_subscription
from models.plan_model import get_plan_by_id
from models.user_model import find_user_by_email, update_wallet
from models.transaction_model import create_transaction
from utils.helpers import get_next_billing_date

subscription_bp = Blueprint("subscription", __name__)

@subscription_bp.route("/subscribe/<plan_id>")
def subscribe(plan_id):
    email = session.get("user_email")

    user = find_user_by_email(email)
    plan = get_plan_by_id(plan_id)

    price = plan["price"]
    wallet_balance = user["wallet_balance"]

    # Case 1: Payment success
    if wallet_balance >= price:
        update_wallet(email, -price)

        next_date = get_next_billing_date(plan["billing_cycle_days"])
        create_subscription(email, plan_id, next_date)

        create_transaction(email, plan_id, price, "SUCCESS")

    # Case 2: Payment failed
    else:
        create_transaction(email, plan_id, price, "FAILED")

    return redirect("/dashboard")
