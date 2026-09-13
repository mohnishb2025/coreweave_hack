from remainders import remainder

def test_negative_dividend_is_non_negative():
    assert remainder(-5, 3) == 1
