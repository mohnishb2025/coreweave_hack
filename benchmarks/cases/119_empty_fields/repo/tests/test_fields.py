from fields import fields

def test_keeps_empty_middle():
    assert fields("a,,b") == ["a", "", "b"]
