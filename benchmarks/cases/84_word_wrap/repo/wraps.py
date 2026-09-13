def wrap(text, width):
    return [text[index : index + width] for index in range(0, len(text), width)]
