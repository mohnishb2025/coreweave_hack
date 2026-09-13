def resolve(document, pointer):
    current = document
    for part in pointer.lstrip("/").split("/"):
        current = current[part]
    return current
