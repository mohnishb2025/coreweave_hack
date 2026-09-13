from datetime import datetime

def iso_week(value):
    moment = datetime.strptime(value, "%Y-%m-%d")
    return f"{moment.year}-W{int(moment.strftime('%W')):02d}"
