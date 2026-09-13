from quotes import unquote

def test_backslash_and_plain():
    assert unquote('"a\\\\b"') == "a\\b"
    assert unquote("plain") == "plain"
