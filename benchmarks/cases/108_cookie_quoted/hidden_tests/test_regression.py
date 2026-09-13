from crumbs import get

def test_neighbors_and_unquoted():
    assert get('x=1; a="b;c"; y=2', "a") == "b;c"
    assert get("session=ok", "session") == "ok"
