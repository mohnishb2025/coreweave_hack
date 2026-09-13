def max_value(items, capacity):
    total = 0
    used = 0
    for weight, value in sorted(items, key=lambda item: item[1] / item[0], reverse=True):
        if used + weight <= capacity:
            used += weight
            total += value
    return total
