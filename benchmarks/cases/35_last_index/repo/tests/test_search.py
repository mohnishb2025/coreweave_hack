from search import last_index

def test_last_duplicate_is_returned():
    assert last_index([1, 2, 2, 2, 3], 2) == 3
