from pointer import resolve

def test_escaped_slash_is_one_key():
    document = {"a/b": 3, "a": {"b": 9}}
    assert resolve(document, "/a~1b") == 3
