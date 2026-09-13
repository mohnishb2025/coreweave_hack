def wrap(degrees):
    if degrees >= 360:
        degrees -= 360
    if degrees < 0:
        degrees += 360
    return degrees
