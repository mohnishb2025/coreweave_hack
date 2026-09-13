from datetime import datetime

def parse_timestamp(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
