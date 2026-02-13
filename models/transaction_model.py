from utils.db import transactions_collection
from datetime import datetime

def create_transaction(email, sub_id, amount, status):
    transaction = {
        "user_email": email,
        "subscription_id": sub_id,
        "amount": amount,
        "status": status,
        "date": datetime.utcnow()
    }
    transactions_collection.insert_one(transaction)

def get_transactions(email):
    return list(transactions_collection.find({"user_email": email}))
