from quotes import unquote

def test_escaped_quote():
    assert unquote('"a\\"b"') == 'a"b'
