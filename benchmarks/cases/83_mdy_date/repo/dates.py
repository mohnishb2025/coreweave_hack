from datetime import date

def parse(text):
    day, month, year = (int(part) for part in text.split("/"))
    return date(year, month, day)
