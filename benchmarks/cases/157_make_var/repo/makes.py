def value(text, name):
    for line in text.splitlines():
        if line.startswith(name + "="):
            return line.split("=", 1)[1]
    return ""
