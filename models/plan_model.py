from utils.db import plans_collection

def create_plan(name, price, cycle_days):
    plan = {
        "name": name,
        "price": price,
        "billing_cycle_days": cycle_days,
        "active": True
    }
    plans_collection.insert_one(plan)

def get_all_plans():
    return list(plans_collection.find({"active": True}))

def get_plan_by_id(plan_id):
    return plans_collection.find_one({"_id": plan_id})
