def replace_extension(path, extension):
    stem = path.split(".")[0]
    return f"{stem}.{extension.lstrip('.')}"
