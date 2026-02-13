from flask import Blueprint, render_template, redirect, session
from bson import ObjectId
from datetime import datetime

from utils.db import plans, subscriptions, payments, payment_requests, users

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return "role" in session and session["role"] == "admin"


@admin_bp.route("/dashboard")
def dashboard():
    if not admin_required():
        return redirect("/")

    # ✅ TOTAL PLANS
    total_plans = plans.count_documents({})

    # ✅ ACTIVE SUBSCRIPTIONS (DISTINCT USERS)
    active_users = subscriptions.distinct(
        "user_email",
        {"status": "Active"}
    )
    active_subs = len(active_users)

    # ✅ TOTAL REVENUE (ONLY PAID PAYMENTS)
    revenue_cursor = payments.find({"status": "Paid"})
    total_revenue = sum(p["amount"] for p in revenue_cursor)

    return render_template(
        "admin_dashboard.html",
        total_plans=total_plans,
        active_subs=active_subs,
        total_revenue=total_revenue
    )


@admin_bp.route("/wallet-requests")
def wallet_requests():
    if not admin_required():
        return redirect("/")

    reqs = list(payment_requests.find({"status": "Pending"}))

    return render_template(
        "admin_wallet_requests.html",
        requests=reqs
    )


@admin_bp.route("/wallet-approve/<req_id>")
def wallet_approve(req_id):
    if not admin_required():
        return redirect("/")

    # mark request approved
    req = payment_requests.find_one({"_id": ObjectId(req_id)})
    if not req:
        return redirect("/admin/wallet-requests")

    payment_requests.update_one({"_id": ObjectId(req_id)}, {"$set": {"status": "Approved"}})

    # credit user wallet
    users.update_one({"email": req["user_email"]}, {"$inc": {"wallet": float(req["amount"])}})

    # record as a payment (top-up)
    payments.insert_one({
        "user_email": req["user_email"],
        "plan_id": None,
        "amount": float(req["amount"]),
        "status": "Paid",
        "payment_date": datetime.now().strftime("%Y-%m-%d")
    })

    return redirect("/admin/wallet-requests")
