from bits import bits

def test_zero_and_full_nibble():
    assert bits(0, 3) == "000"
    assert bits(15, 4) == "1111"
