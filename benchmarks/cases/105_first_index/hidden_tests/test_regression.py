from search import first_index

def test_other_run_and_missing():
    assert first_index([0, 0, 1, 1, 1, 1, 1], 1) == 2
    assert first_index([1, 3, 5], 2) == -1
