from urllib.parse import unquote

def decode(value):
    return unquote(value)
