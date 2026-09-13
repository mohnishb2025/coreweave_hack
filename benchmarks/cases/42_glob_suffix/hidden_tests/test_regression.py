from globs import match

def test_interior_star_and_dotfile():
    assert match("ab", "a*b") is True
    assert match("acb", "a*b") is True
    assert match("abx", "a*b") is False
    assert match(".env", ".*") is True
    assert match("txt", "*.txt") is False
