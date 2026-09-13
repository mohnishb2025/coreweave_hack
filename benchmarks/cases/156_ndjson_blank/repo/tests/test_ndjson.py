from ndjson import load

def test_blank_line_is_skipped():
    assert load('{"a": 1}\n\n{"b": 2}\n') == [{"a": 1}, {"b": 2}]
