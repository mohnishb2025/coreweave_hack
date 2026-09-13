from ring import Ring

def test_wrap_preserves_fifo_order():
    ring = Ring(2)
    ring.push("a")
    ring.push("b")
    assert ring.pop() == "a"
    ring.push("c")
    assert ring.pop() == "b"
    assert ring.pop() == "c"
    assert ring.empty() is True
