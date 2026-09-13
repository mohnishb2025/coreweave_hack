from search import first_index

def test_leftmost_duplicate():
    assert first_index([1, 2, 2, 2, 2, 2, 3], 2) == 1
