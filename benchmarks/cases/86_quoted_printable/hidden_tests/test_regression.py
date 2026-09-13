from quoted import decode

def test_soft_break_and_hex_bytes():
    assert decode("A=\nB") == "AB"
    assert decode("=41=42") == "AB"
