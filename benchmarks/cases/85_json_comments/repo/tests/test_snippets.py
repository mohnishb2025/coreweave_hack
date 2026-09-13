from snippets import parse

def test_leading_line_comment():
    assert parse('// note\n{"a": 1}') == {"a": 1}
