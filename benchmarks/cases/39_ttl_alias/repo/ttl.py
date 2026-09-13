def get(cache, key, now):
    item = cache.get(key)
    if item is None or now >= item["expires"]:
        return None
    return item["value"]
