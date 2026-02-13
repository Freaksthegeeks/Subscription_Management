from flask import Blueprint, render_template, redirect, session, request
from bson import ObjectId
from datetime import datetime

from utils.db import (
    users,
    plans,
    subscriptions,
    payments,
    payment_requests
)

from services.payment_service import process_payment
from services.subscription_service import create_subscription

client_bp = Blueprint("client", __name__, url_prefix="/client")


def client_required():
    return "role" in session and session["role"] == "client"


# =========================
# CLIENT DASHBOARD
# =========================
@client_bp.route("/dashboard")
def dashboard():
    if not client_required():
        return redirect("/")

    user_email = session["email"]
    today = datetime.now().strftime("%Y-%m-%d")

    # 🔁 Expire old subscriptions
    subscriptions.update_many(
        {
            "user_email": user_email,
            "status": "Active",
            "end_date": {"$lt": today}
        },
        {"$set": {"status": "Expired"}}
    )

    user = users.find_one({"email": user_email})
    active_plans = list(plans.find({"status": "Active"}))
    user_subs = list(subscriptions.find({"user_email": user_email}))

    return render_template(
        "client_dashboard.html",
        user=user,
        plans=active_plans,
        subscriptions=user_subs
    )


# =========================
# SUBSCRIBE TO PLAN
# =========================
@client_bp.route("/subscribe/<plan_id>", methods=["POST"])
def subscribe(plan_id):
    if not client_required():
        return redirect("/")

    user_email = session["email"]
    plan = plans.find_one({"_id": ObjectId(plan_id)})

    if not plan:
        return redirect("/client/dashboard")

    # Prevent duplicate active subscription
    if subscriptions.find_one({
        "user_email": user_email,
        "plan_id": str(plan["_id"]),
        "status": "Active"
    }):
        return redirect("/client/dashboard")

    payment_success = process_payment(
        user_email=user_email,
        amount=plan["price"],
        plan_id=str(plan["_id"])
    )

    if payment_success:
        create_subscription(user_email, plan)

    return redirect("/client/dashboard")


# =========================
# WALLET TOP-UP REQUEST (UPI)
# =========================
@client_bp.route("/wallet/request", methods=["POST"])
def wallet_request():
    if not client_required():
        return redirect("/")

    payment_requests.insert_one({
        "user_email": session["email"],
        "amount": float(request.form["amount"]),
        "utr": request.form["utr"],
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return redirect("/client/dashboard")


# =========================
# PAYMENT HISTORY
# =========================
@client_bp.route("/payments")
def payment_history():
    if not client_required():
        return redirect("/")

    history = list(
        payments.find(
            {"user_email": session["email"]}
        ).sort("payment_date", -1)
    )

    return render_template(
        "client_payments.html",
        history=history
    )
