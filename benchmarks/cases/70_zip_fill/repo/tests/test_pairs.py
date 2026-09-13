from pairs import zip_fill

def test_right_is_padded():
    assert zip_fill([1, 2, 3], ["a"]) == [(1, "a"), (2, None), (3, None)]
