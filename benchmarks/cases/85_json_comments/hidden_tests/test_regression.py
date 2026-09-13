from snippets import parse

def test_other_comment_and_url_string():
    assert parse('// skip\n{"b": 2}') == {"b": 2}
    assert parse('{"a": "http://x"}') == {"a": "http://x"}
