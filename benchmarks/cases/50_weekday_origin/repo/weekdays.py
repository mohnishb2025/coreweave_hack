from datetime import date

NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def weekday_name(value):
    year, month, day = (int(part) for part in value.split("-"))
    return NAMES[date(year, month, day).weekday()]
