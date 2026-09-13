import base64
import json

def claims(token):
    return json.loads(base64.b64decode(token.split(".")[1]))
