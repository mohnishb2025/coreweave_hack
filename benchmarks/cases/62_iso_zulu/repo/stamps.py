from datetime import datetime

def parse(value):
    return datetime.fromisoformat(value.replace("Z", ""))
