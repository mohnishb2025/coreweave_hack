import base64

def accept(key):
    return base64.b64encode(key.encode()).decode()
