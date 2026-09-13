from datetime import timedelta

def parse(text):
    return timedelta(hours=int(text))
