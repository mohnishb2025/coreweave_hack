from hexes import hex_of

def test_ten_in_four_digits():
    assert hex_of(10, 4) == "000a"
