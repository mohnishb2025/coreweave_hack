from nths import matches

def test_later_odd_and_keyword():
    assert matches("2n+1", 5) is True
    assert matches("2n+1", 2) is False
    assert matches("odd", 1) is True
