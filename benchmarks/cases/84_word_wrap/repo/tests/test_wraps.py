from wraps import wrap

def test_wraps_on_spaces():
    assert wrap("hello world", 8) == ["hello", "world"]
