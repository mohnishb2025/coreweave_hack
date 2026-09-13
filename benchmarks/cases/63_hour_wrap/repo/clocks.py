def wrap_hour(value):
    if value < 0:
        value += 24
    if value >= 24:
        value -= 24
    return value
