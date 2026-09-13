from spans import values

def test_negatives_and_singleton():
    assert values(-1, 1) == [-1, 0, 1]
    assert values(5, 5) == [5]
