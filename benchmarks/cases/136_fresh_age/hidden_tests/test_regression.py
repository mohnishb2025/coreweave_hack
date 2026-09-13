from freshness import fresh

def test_below_and_zero():
    assert fresh(59, 60) is True
    assert fresh(0, 0) is False
