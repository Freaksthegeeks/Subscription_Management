from utils.db import subscriptions_collection
from datetime import datetime

def create_subscription(user_email, plan_id, next_billing_date):
    subscription = {
        "user_email": user_email,
        "plan_id": plan_id,
        "status": "ACTIVE",
        "start_date": datetime.utcnow(),
        "next_billing_date": next_billing_date
    }
    subscriptions_collection.insert_one(subscription)

def get_user_subscription(email):
    return subscriptions_collection.find_one({"user_email": email})

def update_subscription_status(sub_id, status):
    subscriptions_collection.update_one(
        {"_id": sub_id},
        {"$set": {"status": status}}
    )

def update_next_billing(sub_id, next_date):
    subscriptions_collection.update_one(
        {"_id": sub_id},
        {"$set": {"next_billing_date": next_date}}
    )
