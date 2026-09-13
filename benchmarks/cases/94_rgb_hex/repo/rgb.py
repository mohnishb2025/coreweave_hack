def to_rgb(color):
    return tuple(int(color[index : index + 2], 16) for index in (1, 3, 5))
