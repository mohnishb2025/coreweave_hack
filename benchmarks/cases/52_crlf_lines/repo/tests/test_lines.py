from lines import lines

def test_crlf_does_not_keep_a_carriage_return():
    assert lines("a\r\nb") == ["a", "b"]
