def allows(origin, allowed):
    return origin in allowed or "*" in allowed
