from pairs import zip_fill

def test_left_pad_and_custom_fill():
    assert zip_fill([1], ["a", "b"], fill=0) == [(1, "a"), (0, "b")]
    assert zip_fill([], ["x"], fill="-") == [("-", "x")]
