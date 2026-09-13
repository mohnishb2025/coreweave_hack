from blanks import words

def test_nbsp_is_whitespace():
    assert words("a\u00a0b") == ["a", "b"]
