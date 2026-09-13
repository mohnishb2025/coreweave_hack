def get_all(query, key):
    for part in query.lstrip("?").split("&"):
        name, _, value = part.partition("=")
        if name == key:
            return [value]
    return []
