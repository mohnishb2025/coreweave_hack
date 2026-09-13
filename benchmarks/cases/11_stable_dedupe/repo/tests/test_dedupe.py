from dedupe import unique

def test_first_seen_order_is_preserved():
    assert unique([3, 1, 3, 2]) == [3, 1, 2]
