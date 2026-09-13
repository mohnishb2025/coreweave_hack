import fnmatch

def ignored(name, patterns):
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns if not pattern.startswith("!"))
