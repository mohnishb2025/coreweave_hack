import re

def text_of(html):
    return re.sub(r"<.*>", "", html)
