from ring import Ring

def test_full_buffer_is_not_empty():
    ring = Ring(2)
    ring.push(1)
    ring.push(2)
    assert ring.empty() is False
