def attr(tag, name):
    return tag.split(name + "=")[1].split()[0].strip('"')
