from pointer import resolve

def test_tilde_and_nested_escape():
    document = {"~": {"x": 1}, "m~n": 4}
    assert resolve(document, "/~0/x") == 1
    assert resolve(document, "/m~0n") == 4
