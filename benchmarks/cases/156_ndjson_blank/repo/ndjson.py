import json

def load(text):
    return [json.loads(line) for line in text.splitlines()]
