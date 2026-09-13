def join(base, relative):
    return base.rstrip("/") + "/" + relative.lstrip("/")
