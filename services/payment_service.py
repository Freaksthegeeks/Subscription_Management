from utils.db import users, payments
from datetime import datetime


def process_payment(user_email, amount, plan_id):
    user = users.find_one({"email": user_email})

    if user["wallet"] >= amount:
        users.update_one(
            {"email": user_email},
            {"$inc": {"wallet": -amount}}
        )
        status = "Paid"
    else:
        status = "Failed"

    payments.insert_one({
        "user_email": user_email,
        "plan_id": plan_id,
        "amount": amount,
        "status": status,
        "payment_date": datetime.now().strftime("%Y-%m-%d")
    })

    return status == "Paid"
