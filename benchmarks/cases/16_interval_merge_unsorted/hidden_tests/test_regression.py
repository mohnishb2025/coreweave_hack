from intervals import merge

def test_touching_and_contained_ranges():
    assert merge([[5, 5], [1, 4], [4, 7], [15, 18]]) == [[1, 7], [15, 18]]
