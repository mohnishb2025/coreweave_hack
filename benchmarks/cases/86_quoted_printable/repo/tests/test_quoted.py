from quoted import decode

def test_utf8_hex_bytes():
    assert decode("caf=C3=A9") == "café"
