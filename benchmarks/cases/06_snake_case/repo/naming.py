import re

def snake_case(value):
    return re.sub(r"([A-Z])", r"_\1", value).strip("_").lower()
