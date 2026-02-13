from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import users_collection
from datetime import datetime

def create_user(name, email, password, role="client"):
    user = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "wallet_balance": 1000,
        "role": role,  # admin or client
        "created_at": datetime.utcnow()
    }
    users_collection.insert_one(user)

def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)

def update_wallet(email, amount):
    users_collection.update_one(
        {"email": email},
        {"$inc": {"wallet_balance": amount}}
    )
