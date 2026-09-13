from uescapes import unescape

def test_e_acute():
    assert unescape("caf\\u00e9") == "café"
