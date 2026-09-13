from crumbs import get

def test_semicolon_inside_quotes():
    assert get('a="b;c"', "a") == "b;c"
