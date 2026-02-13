from utils.db import subscriptions
from datetime import datetime, timedelta


def create_subscription(user_email, plan):
    start_date = datetime.now()

    if plan["billing_cycle"].lower() == "monthly":
        end_date = start_date + timedelta(days=30)
    else:
        end_date = start_date + timedelta(days=365)

    subscriptions.insert_one({
        "user_email": user_email,
        "plan_id": str(plan["_id"]),
        "plan_name": plan["name"],
        "price": plan["price"],
        "billing_cycle": plan["billing_cycle"],
        "status": "Active",
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    })
