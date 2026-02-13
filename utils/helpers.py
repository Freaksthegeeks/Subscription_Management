from datetime import datetime, timedelta

def get_next_billing_date(days=30):
    return datetime.utcnow() + timedelta(days=days)
