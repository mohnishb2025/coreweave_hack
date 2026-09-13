from ratios import ratio

def test_spaces_and_integer():
    assert ratio("4 / 3") == 4 / 3
    assert ratio("2") == 2
