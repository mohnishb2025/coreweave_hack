def clamp(value, low, high):
    if value >= high:
        return high - 1
    return max(low, value)
