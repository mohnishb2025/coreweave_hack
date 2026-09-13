def get(text, section, key):
    values = {}
    for line in text.splitlines():
        if "=" in line:
            name, _, value = line.partition("=")
            values[name.strip()] = value.strip()
    return values[key]
