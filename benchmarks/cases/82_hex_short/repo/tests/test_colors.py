from colors import expand

def test_three_digit_hex_expands():
    assert expand("#AbC") == "#aabbcc"
