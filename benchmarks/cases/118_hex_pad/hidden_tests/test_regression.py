from hexes import hex_of

def test_zero_and_byte():
    assert hex_of(0, 2) == "00"
    assert hex_of(255, 2) == "ff"
