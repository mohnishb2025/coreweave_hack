from datetime import datetime

def parse(value):
    return datetime.strptime(value, "%Y-%m-%d").date()
