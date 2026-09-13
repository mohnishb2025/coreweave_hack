from ratios import reduce

def test_other_gcd_and_sign():
    assert reduce(15, 25) == (3, 5)
    assert reduce(-4, 6) == (-2, 3)
    assert reduce(3, 3) == (1, 1)
