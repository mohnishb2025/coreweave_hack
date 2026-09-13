def merge_patch(target, patch):
    if not isinstance(patch, dict):
        return patch
    result = dict(target)
    for key, value in patch.items():
        if value is None:
            result[key] = None
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_patch(result[key], value)
        else:
            result[key] = value
    return result
