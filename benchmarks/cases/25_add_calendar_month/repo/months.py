from datetime import timedelta

def add_months(value, months):
    return value + timedelta(days=31 * months)
