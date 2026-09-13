from fields import fields

def test_leading_and_trailing_empty():
    assert fields(",a,") == ["", "a", ""]
    assert fields("x") == ["x"]
