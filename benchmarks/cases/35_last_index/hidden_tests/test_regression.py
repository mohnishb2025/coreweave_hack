from search import last_index

def test_missing_and_edge_duplicates():
    assert last_index([2, 2, 2, 2], 2) == 3
    assert last_index([1, 1, 2, 3], 1) == 1
    assert last_index([1, 2, 3, 3], 3) == 3
    assert last_index([1, 2, 3], 4) == -1
    assert last_index([], 1) == -1
