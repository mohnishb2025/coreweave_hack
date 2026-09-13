def match(name, pattern):
    return pattern.replace("*", "") in name
