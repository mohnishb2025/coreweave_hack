from limiter import accept

def test_event_on_window_boundary_still_counts():
    history = [0, 4]
    assert accept(history, 10, limit=3, window=10) is True
    assert accept([0, 4, 10], 10, limit=3, window=10) is False
