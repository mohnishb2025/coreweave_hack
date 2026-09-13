from lines import lines

def test_mixed_newlines_and_trailing_break():
    assert lines("a\nb\n") == ["a", "b"]
    assert lines("a\r\n\r\nb") == ["a", "", "b"]
    assert lines("solo") == ["solo"]
