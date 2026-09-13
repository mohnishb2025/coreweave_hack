def deep_merge(base, override):
    merged = base
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
