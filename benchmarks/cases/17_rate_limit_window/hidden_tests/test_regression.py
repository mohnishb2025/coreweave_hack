from limiter import accept

def test_zero_window_is_exact_timestamp_only():
    assert accept([], 5, limit=1, window=0) is True
    assert accept([5], 5, limit=1, window=0) is False
    assert accept([4], 5, limit=1, window=0) is True
