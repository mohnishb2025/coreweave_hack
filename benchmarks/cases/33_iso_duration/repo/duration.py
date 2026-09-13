import re

def seconds(text):
    match = re.search(r"(\d+)H", text)
    return int(match.group(1)) * 3600 if match else 0
