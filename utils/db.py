from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users = db["users"]
plans = db["plans"]
subscriptions = db["subscriptions"]
payments = db["payments"]
payment_requests = db["payment_requests"]  
